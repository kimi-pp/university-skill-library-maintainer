"""Staged, single-writer coordinator.  Task 10/11 supply report and Office callbacks."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import shutil
import uuid
from typing import Any, Callable, Iterable, Mapping

if os.name == "nt":
    import ctypes
    import msvcrt
    from ctypes import wintypes

from .dedup import deduplicate
from .ledger import LedgerStore
from .locking import SingleWriterLock
from .office import (
    OfficeEvidenceBundle,
    OfficeRunScope,
    OfficeVerificationError,
    clear_office_run_state,
    issue_office_run_scope,
)
from .paths import ProjectPaths, assert_ordinary_path, contained_child, is_link_or_reparse
from .publish import PublishError, PublishReceipt, commit_prepared_generation
from .review import ReviewDecision, apply_reviews_from_stream, clear_review_run_state, consume_applied_review
from .settings import load_settings, settings_sha256
from .sources.base import SourceRequestEvent, SourceWatermarkStore, Watermark
from .versioning import VersionDecision, apply_approved_version, compare_version


class CoordinatorError(RuntimeError):
    """A run was stale, tampered, outside its state transition, or unsafe to publish."""


@dataclass(frozen=True)
class SourceRun:
    platform: str
    status: str
    candidates: tuple[object, ...] = ()
    watermark: str | None = None
    query: str = "__run__"
    evidence_files: tuple[Path, ...] = ()
    request_events: tuple[SourceRequestEvent, ...] = ()


@dataclass(frozen=True)
class RunRequest:
    settings_path: Path
    catalog_loader: Callable[[], object]
    discover: Callable[["RunRequest", Path], Iterable[SourceRun]] | None = None
    expected_config_sha: str | None = None
    requested_run_id: str | None = None
    review_packets: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class PreparedRun:
    run_id: str
    staging_dir: Path
    staging_ledger: Path
    settings_sha256: str
    source_runs: tuple[SourceRun, ...]
    catalog_snapshot: object = field(repr=False, compare=False)
    office_scope: OfficeRunScope = field(repr=False, compare=False)
    _coordinator_token: str = field(repr=False, compare=False)


@dataclass(frozen=True)
class ReviewApplySummary:
    run_id: str
    decision_sha256: str
    applied_count: int
    staged_ledger_sha256: str
    receipts: tuple[object, ...] = field(default=(), repr=False, compare=False)


@dataclass(frozen=True)
class RunSummary:
    run_id: str
    blocked: bool
    source_statuses: dict[str, str]
    published_ledger: Path | None
    output_generation: Path | None
    warnings: tuple[str, ...] = ()
    office_evidence_sha256: str | None = None
    publish_receipt: PublishReceipt | None = field(default=None, repr=False, compare=False)


@dataclass
class _State:
    prepared: PreparedRun
    request: RunRequest
    lock: SingleWriterLock
    production_ledger_sha: str
    production_ledger_stat: tuple[int, int, int, int]
    staging_digest: str
    catalog_digest: str
    source_digest: str
    review_packets: Mapping[str, object]
    evidence_identity: tuple[tuple[Path, str, tuple[int, int, int, int]], ...]
    version_proposals: dict[str, Mapping[str, object]] = field(default_factory=dict)
    output_digest: str = ""
    owned_generation: Path | None = None
    committed: bool = False
    phase: str = "prepared"
    review_summary: ReviewApplySummary | None = None
    office_evidence: OfficeEvidenceBundle | None = None
    publish_receipt: PublishReceipt | None = None


def _sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _stat_identity(path: Path) -> tuple[int, int, int, int]:
    result = path.stat()
    return (getattr(result, "st_dev", 0), getattr(result, "st_ino", 0), result.st_size, result.st_mtime_ns)


class RunCoordinator:
    """Owns a lock from ``prepare`` to terminal cleanup; never writes production early."""

    def __init__(
        self,
        *,
        root: str | Path,
        discover: Callable[[RunRequest, Path], Iterable[SourceRun]] | None = None,
        report_builder: Callable[[PreparedRun, Path], Iterable[Path]] | None = None,
        office_verifier: Callable[[PreparedRun, tuple[Path, ...]], OfficeEvidenceBundle] | None = None,
        before_publish: Callable[[PreparedRun], None] | None = None,
        fail_at: str | None = None,
    ) -> None:
        self.paths = ProjectPaths.from_root(root)
        self.discover = discover or (lambda request, staging: ())
        self.report_builder = report_builder or (lambda prepared, staging: ())
        self.office_verifier = office_verifier
        self.before_publish = before_publish
        self.fail_at = fail_at
        self._token = uuid.uuid4().hex
        self._states: dict[str, _State] = {}

    def prepare(self, request: RunRequest) -> PreparedRun:
        self._validate_request_path(request.settings_path)
        config_sha = settings_sha256(request.settings_path)
        if request.expected_config_sha is not None and request.expected_config_sha != config_sha:
            raise CoordinatorError("请求配置哈希与当前设置不一致")
        load_settings(request.settings_path)
        self.paths.ensure_runtime()
        self._assert_production_inputs()
        lock = SingleWriterLock(self.paths.lock)
        lock.acquire()
        staging_dir: Path | None = None
        office_scope: OfficeRunScope | None = None
        try:
            run_id = self._run_id(request.requested_run_id)
            self._reclaim_orphan_generation(run_id)
            staging_dir = contained_child(self.paths.staging_root, run_id)
            if staging_dir.exists() or staging_dir.is_symlink():
                raise CoordinatorError("运行暂存目录已存在或不是普通目录")
            staging_dir.mkdir(mode=0o700)
            assert_ordinary_path(staging_dir, require_directory=True)
            office_scope = issue_office_run_scope(
                run_id=run_id,
                staging_root=staging_dir,
                project_root=self.paths.root,
            )
            staged_ledger = staging_dir / "Skills主台账.xlsx"
            shutil.copyfile(self.paths.ledger, staged_ledger)
            self._ensure_file_in_staging(staging_dir, staged_ledger)
            ledger = LedgerStore.load(staged_ledger)
            ledger.append_rows("运行记录", [{
                "运行标识": run_id, "运行类型": "维护", "开始时间": datetime.now(),
                "成功完成时间": None, "状态": "运行中", "摘要": "暂存运行中", "快照SHA-256": _sha256(self.paths.ledger),
            }])
            self._save_ledger(ledger, staged_ledger)
            catalog = request.catalog_loader()
            captured_catalog = catalog
            source_runs = tuple(request.discover(request, staging_dir) if request.discover else self.discover(request, staging_dir))
            self._validate_sources(source_runs)
            evidence_identity = self._bind_evidence(source_runs)
            self._write_source_statuses(staged_ledger, source_runs)
            self._inject("after_discovery")
            prepared = PreparedRun(
                run_id, staging_dir, staged_ledger, config_sha, source_runs,
                captured_catalog, office_scope, self._token,
            )
            self._states[run_id] = _State(
                prepared, request, lock, _sha256(self.paths.ledger), _stat_identity(self.paths.ledger), self._tree_digest(staging_dir),
                self._object_digest(captured_catalog), self._object_digest(source_runs), dict(request.review_packets), evidence_identity,
                output_digest=self._output_digest(),
            )
            return prepared
        except BaseException:
            if staging_dir is not None:
                try:
                    self._remove_owned_staging(staging_dir)
                except BaseException:
                    pass
            try:
                lock.release()
            except BaseException:
                pass
            try:
                clear_review_run_state(packets=tuple(request.review_packets.values()))
            except BaseException:
                pass
            if office_scope is not None:
                try:
                    clear_office_run_state(scope=office_scope)
                except BaseException:
                    pass
            raise

    def apply_reviews(self, prepared: PreparedRun, decisions: Iterable[ReviewDecision]) -> ReviewApplySummary:
        state = self._state_for(prepared, allowed=("prepared", "reviews_applied"))
        decisions = tuple(decisions)
        decision_sha = self._decision_digest(decisions)
        if state.review_summary is not None:
            if state.review_summary.decision_sha256 != decision_sha:
                raise CoordinatorError("已应用不同的审查决定；运行不可回写")
            return state.review_summary
        try:
            self._ensure_request_still_matches(state)
            self._ensure_staging_unchanged(state)
        except BaseException:
            self._fail_terminal(state)
            raise
        try:
            ledger = LedgerStore.load(prepared.staging_ledger)
            receipts: tuple[object, ...] = ()
            existing_ids = {str(row.get("内部标识") or "") for row in ledger.rows("当前Skill")}
            received: list[object] = []
            for decision in decisions:
                payload = {"decisions": [self._decision_mapping(decision)]}
                stream = io.BytesIO(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
                packets = {decision.candidate_id: state.review_packets.get(decision.candidate_id)}
                if decision.candidate_id in existing_ids:
                    shadow = prepared.staging_dir / f".version-review-{uuid.uuid4().hex}.xlsx"
                    shutil.copyfile(prepared.staging_ledger, shadow)
                    shadow_ledger = LedgerStore.load(shadow)
                    try:
                        issued = apply_reviews_from_stream(stream, shadow_ledger, packets)
                        proposed = next(row for row in shadow_ledger.rows("当前Skill") if row["内部标识"] == decision.candidate_id)
                        state.version_proposals[decision.candidate_id] = proposed
                        received.extend(issued)
                    finally:
                        shadow_ledger.workbook.close()
                        if shadow.exists() and not is_link_or_reparse(shadow):
                            shadow.unlink()
                else:
                    received.extend(apply_reviews_from_stream(stream, ledger, packets))
            receipts = tuple(received)
            self._save_ledger(ledger, prepared.staging_ledger)
            self._inject("after_review")
            summary = ReviewApplySummary(prepared.run_id, decision_sha, len(receipts), _sha256(prepared.staging_ledger), receipts)
            state.review_summary, state.phase, state.staging_digest = summary, "reviews_applied", self._tree_digest(prepared.staging_dir)
            return summary
        except BaseException:
            self._fail_terminal(state)
            raise

    def finalize(self, prepared: PreparedRun, reviews: ReviewApplySummary) -> RunSummary:
        state = self._state_for(prepared, allowed=("prepared", "reviews_applied"))
        if reviews.run_id != prepared.run_id or state.review_summary not in (None, reviews):
            raise CoordinatorError("审查摘要不属于当前准备运行")
        if state.review_summary is None and reviews.decision_sha256 != self._decision_digest(()) :
            raise CoordinatorError("未应用的审查摘要不能终结运行")
        try:
            self._ensure_request_still_matches(state)
            self._ensure_staging_unchanged(state)
        except BaseException:
            self._fail_terminal(state)
            raise
        statuses = {item.platform: item.status for item in prepared.source_runs}
        if prepared.source_runs and all(item.status == "failed" for item in prepared.source_runs):
            try:
                report = prepared.staging_dir / "failure-report.json"
                report.write_text(json.dumps({"run_id": prepared.run_id, "source_statuses": statuses}, ensure_ascii=False), encoding="utf-8")
                self._mark_run(prepared.staging_ledger, prepared.run_id, "失败", "四个平台均失败；仅保留暂存失败报告")
                self._terminal(state, remove_staging=False)
                return RunSummary(prepared.run_id, True, statuses, None, None)
            except BaseException:
                self._fail_terminal(state)
                raise
        try:
            ledger = LedgerStore.load(prepared.staging_ledger)
            self._apply_version_transactions(ledger, state, reviews)
            self._apply_dedup_and_watermarks(ledger, prepared.source_runs)
            self._save_ledger(ledger, prepared.staging_ledger)
            artifacts = self._artifacts_from_callback(prepared)
            self._inject("report")
            state.staging_digest = self._tree_digest(prepared.staging_dir)
            if self.before_publish:
                self.before_publish(prepared)
            self._ensure_staging_unchanged(state)
            self._assert_production_unchanged(state)
            self._inject("before_publish")
            self._assert_output_unchanged(state)
            output, delivery_hash, manifest_hash = self._prepare_generation(state)
            self._mark_run(prepared.staging_ledger, prepared.run_id, "成功", f"generation={output.relative_to(self.paths.root).as_posix()};delivery_sha256={delivery_hash};manifest_sha256={manifest_hash}")
            office_paths = (prepared.staging_ledger, *artifacts)
            if self.office_verifier is None:
                raise CoordinatorError("缺少结构化 Office 发布证据提供器")
            evidence = self.office_verifier(prepared, office_paths)
            if not isinstance(evidence, OfficeEvidenceBundle):
                raise CoordinatorError("Office 发布结果必须是结构化证据")
            if evidence.scope is not prepared.office_scope:
                raise CoordinatorError("Office 发布结果未绑定 Runner 持有的 OfficeRunScope token")
            try:
                evidence.assert_publication_roles(prepared.staging_ledger, office_paths)
            except OfficeVerificationError as exc:
                raise CoordinatorError(f"Office 发布证据未通过：{exc}") from exc
            state.office_evidence = evidence
            self._inject("office")
            self._reopen_staged_ledger(prepared.staging_ledger)
            self._inject("reopen")
            state.staging_digest = self._tree_digest(prepared.staging_dir)
            self._ensure_staging_unchanged(state)
            self._assert_production_unchanged(state)
            self._verify_generation_authority(output, prepared.run_id, delivery_hash, manifest_hash)
            self._inject("before_commit")
            receipt = self._commit_ledger_only(
                state, output, delivery_hash, manifest_hash,
                evidence=evidence, office_paths=office_paths,
            )
            state.publish_receipt = receipt
            # No callback, validation, or rollback occurs after this one linearization point.
            warnings = self._terminal(state, remove_staging=True, remove_generation=False)
            return RunSummary(
                prepared.run_id, False, statuses, self.paths.ledger, output, warnings,
                office_evidence_sha256=evidence.sha256, publish_receipt=receipt,
            )
        except BaseException:
            if state.committed or self._production_has_committed_run(state):
                state.committed, state.phase = True, "committed"
                self._terminal(state, remove_staging=True, remove_generation=False)
            else:
                self._fail_terminal(state)
            raise

    def abandon(self, prepared: PreparedRun) -> None:
        if prepared._coordinator_token != self._token:
            raise CoordinatorError("PreparedRun 不属于当前协调器")
        state = self._states.get(prepared.run_id)
        if state is None:
            raise CoordinatorError("PreparedRun 已失效")
        if state.phase != "finalized":
            self._fail_terminal(state)
        else:
            self._remove_owned_staging(prepared.staging_dir)
            self._states.pop(prepared.run_id, None)

    def _validate_request_path(self, path: Path) -> None:
        candidate = Path(path).absolute()
        try:
            candidate.relative_to(self.paths.root)
        except ValueError as exc:
            raise ValueError("设置文件必须位于项目根目录内") from exc
        if candidate != self.paths.settings:
            raise ValueError("设置文件路径不可由调用者改写")
        assert_ordinary_path(candidate)

    def _assert_production_inputs(self) -> None:
        assert_ordinary_path(self.paths.root, require_directory=True)
        assert_ordinary_path(self.paths.ledger.parent, require_directory=True)
        if not self.paths.ledger.is_file() or is_link_or_reparse(self.paths.ledger):
            raise ValueError("生产主台账必须是普通文件")
        ledger = LedgerStore.load(self.paths.ledger)
        errors = ledger.validate()
        try:
            successful = next((row for row in reversed(ledger.rows("运行记录")) if row.get("状态") == "成功"), None)
            if successful is not None:
                self._verify_recorded_generation(successful)
        finally:
            ledger.workbook.close()
        if errors:
            raise CoordinatorError("生产主台账校验失败：" + "；".join(errors))

    def _run_id(self, requested: str | None) -> str:
        value = requested or f"run-{uuid.uuid4().hex}"
        if not value.startswith("run-") or len(value) > 80:
            raise ValueError("运行标识格式不安全")
        contained_child(self.paths.staging_root, value)
        return value

    @staticmethod
    def _validate_sources(source_runs: tuple[SourceRun, ...]) -> None:
        expected = {"SkillHub", "ClawHub", "GitHub", "Hugging Face Spaces"}
        actual = [item.platform for item in source_runs]
        if set(actual) != expected or len(actual) != len(expected):
            raise CoordinatorError("来源集合必须精确为四个受支持平台且各出现一次")
        if any(item.status not in {"complete", "partial", "failed"} for item in source_runs):
            raise CoordinatorError("来源状态必须为 complete、partial 或 failed")
        if any(item.status in {"complete", "partial"} and item.candidates and not item.evidence_files for item in source_runs):
            raise CoordinatorError("含候选的完整或部分来源批次必须绑定证据文件")

    @staticmethod
    def _bind_evidence(source_runs: tuple[SourceRun, ...]) -> tuple[tuple[Path, str, tuple[int, int, int, int]], ...]:
        bound: list[tuple[Path, str, tuple[int, int, int, int]]] = []
        for run in source_runs:
            for raw in run.evidence_files:
                path = Path(raw).absolute()
                if not path.is_file() or is_link_or_reparse(path):
                    raise CoordinatorError("来源证据必须是普通文件")
                bound.append((path, _sha256(path), _stat_identity(path)))
        return tuple(bound)

    def _write_source_statuses(self, staged_ledger: Path, source_runs: tuple[SourceRun, ...]) -> None:
        # Existing schema intentionally has no sidecar run database.  Status stays in the staged run record.
        ledger = LedgerStore.load(staged_ledger)
        rows = ledger.rows("运行记录")
        if rows:
            latest = rows[-1]
            latest["摘要"] = json.dumps({item.platform: item.status for item in source_runs}, ensure_ascii=False, sort_keys=True)
            ledger.append_rows("运行记录", [])
            worksheet = ledger.workbook["运行记录"]
            columns = ledger._resolve_columns("运行记录")
            for row_number in range(2, worksheet.max_row + 1):
                if worksheet.cell(row_number, columns["运行标识"]).value == latest["运行标识"]:
                    ledger._set_cell(worksheet.cell(row_number, columns["摘要"]), latest["摘要"], "摘要")
        self._save_ledger(ledger, staged_ledger)

    def _state_for(self, prepared: PreparedRun, *, allowed: tuple[str, ...]) -> _State:
        if prepared._coordinator_token != self._token:
            raise CoordinatorError("PreparedRun 不属于当前协调器")
        state = self._states.get(prepared.run_id)
        if state is None or state.prepared is not prepared or state.phase not in allowed:
            raise CoordinatorError("PreparedRun 已失效或不在允许状态")
        return state

    def _ensure_staging_unchanged(self, state: _State) -> None:
        if self._tree_digest(state.prepared.staging_dir) != state.staging_digest:
            raise CoordinatorError("暂存目录在校验后被修改")

    def _ensure_request_still_matches(self, state: _State) -> None:
        """A prepared run is bound to the exact settings bytes used at discovery time."""
        if settings_sha256(state.request.settings_path) != state.prepared.settings_sha256:
            raise CoordinatorError("配置在 prepare 后变化；拒绝继续旧运行")
        if self._object_digest(state.request.catalog_loader()) != state.catalog_digest:
            raise CoordinatorError("目录快照在 prepare 后变化；拒绝继续旧运行")
        if self._object_digest(state.prepared.source_runs) != state.source_digest:
            raise CoordinatorError("来源快照在 prepare 后变化；拒绝继续旧运行")
        for path, digest, identity in state.evidence_identity:
            if not path.is_file() or is_link_or_reparse(path) or _sha256(path) != digest or _stat_identity(path) != identity:
                raise CoordinatorError("来源证据在 prepare 后变化；拒绝继续旧运行")

    def _assert_production_unchanged(self, state: _State) -> None:
        if _sha256(self.paths.ledger) != state.production_ledger_sha or _stat_identity(self.paths.ledger) != state.production_ledger_stat:
            raise CoordinatorError("生产台账在运行期间变化，拒绝覆盖")

    def _output_digest(self) -> str:
        if not self.paths.output.exists():
            return "absent"
        assert_ordinary_path(self.paths.output, require_directory=True)
        return self._tree_digest(self.paths.output)

    def _assert_output_unchanged(self, state: _State) -> None:
        if self._output_digest() != state.output_digest:
            raise CoordinatorError("既有输出或发布代次在运行期间变化，拒绝覆盖")

    @staticmethod
    def _summary_fields(summary: object) -> dict[str, str]:
        values: dict[str, str] = {}
        for item in str(summary or "").split(";"):
            key, separator, value = item.partition("=")
            if separator and key and value:
                values[key] = value
        return values

    def _verify_recorded_generation(self, record: Mapping[str, object]) -> None:
        fields = self._summary_fields(record.get("摘要"))
        relative = fields.get("generation")
        delivery_hash, manifest_hash = fields.get("delivery_sha256"), fields.get("manifest_sha256")
        if not relative or not delivery_hash or not manifest_hash:
            raise CoordinatorError("生产成功运行记录缺少发布代次权威信息")
        raw_path = Path(relative)
        if raw_path.is_absolute() or any(part in {"", ".", ".."} for part in raw_path.parts):
            raise CoordinatorError("生产成功运行记录的代次路径不安全")
        candidate = self.paths.root.joinpath(*raw_path.parts)
        try:
            candidate.relative_to(self.paths.output / "generations")
        except ValueError as exc:
            raise CoordinatorError("生产成功运行记录指向项目外代次") from exc
        self._verify_generation_authority(candidate, str(record.get("运行标识") or ""), delivery_hash, manifest_hash)

    def _reclaim_orphan_generation(self, run_id: str) -> None:
        generation = contained_child(self.paths.output / "generations", run_id)
        if not generation.exists():
            return
        manifest = generation / "generation-manifest.json"
        try:
            manifest_hash = _sha256(manifest)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            delivery_hash = str(payload.get("delivery_sha256") or "")
            self._verify_generation_authority(generation, run_id, delivery_hash, manifest_hash)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, CoordinatorError) as exc:
            raise CoordinatorError("同运行标识遗留的发布代次不可安全回收") from exc
        ledger = LedgerStore.load(self.paths.ledger)
        try:
            relative = generation.relative_to(self.paths.root).as_posix()
            referenced = any(self._summary_fields(row.get("摘要")).get("generation") == relative for row in ledger.rows("运行记录"))
        finally:
            ledger.workbook.close()
        if referenced:
            raise CoordinatorError("同运行标识发布代次已被生产台账引用，拒绝回收")
        self._remove_generation(generation, self.paths.output / "generations")

    def _verify_generation_authority(self, generation: Path, run_id: str, delivery_hash: str, manifest_hash: str) -> None:
        try:
            generation.relative_to(self.paths.output / "generations")
        except ValueError as exc:
            raise CoordinatorError("发布代次越出 output/generations") from exc
        try:
            assert_ordinary_path(generation, require_directory=True)
        except ValueError as exc:
            raise CoordinatorError("发布代次不是项目内普通目录") from exc
        manifest = generation / "generation-manifest.json"
        self._ensure_file_or_directory_in_staging(generation, manifest)
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CoordinatorError("发布代次 manifest 不可读取") from exc
        if not isinstance(payload, Mapping) or payload.get("run_id") != run_id or payload.get("delivery_sha256") != delivery_hash:
            raise CoordinatorError("发布代次 manifest 与运行权威信息不一致")
        if _sha256(manifest) != manifest_hash or self._tree_digest_excluding(generation, manifest) != delivery_hash:
            raise CoordinatorError("发布代次在校验后被修改")
        if payload.get("files") != self._authority_files(generation, excluded=manifest):
            raise CoordinatorError("发布代次 authority 文件集合或身份不一致")

    @staticmethod
    def _authority_files(root: Path, *, excluded: Path | None = None) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for item in sorted(root.rglob("*"), key=lambda path: str(path.relative_to(root)).casefold()):
            if item == excluded:
                continue
            if is_link_or_reparse(item):
                raise CoordinatorError("generation authority 包含链接或重解析点")
            if item.is_file():
                rows.append({"path": item.relative_to(root).as_posix(), "sha256": _sha256(item),
                    "identity": list(_stat_identity(item))})
        return rows

    @staticmethod
    def _fsync_tree(root: Path) -> None:
        for item in root.rglob("*"):
            if item.is_file() and not is_link_or_reparse(item):
                with item.open("r+b") as handle:
                    RunCoordinator._flush_file(handle)

    @staticmethod
    def _flush_file(handle: object) -> None:
        try:
            if os.name == "nt":
                flush = ctypes.windll.kernel32.FlushFileBuffers
                flush.argtypes = (wintypes.HANDLE,)
                flush.restype = wintypes.BOOL
                result = flush(wintypes.HANDLE(msvcrt.get_osfhandle(handle.fileno())))
                if not result:
                    raise OSError("FlushFileBuffers failed")
            else:
                os.fsync(handle.fileno())
        except OSError as exc:
            raise CoordinatorError("无法持久化发布文件") from exc

    def _save_ledger(self, ledger: LedgerStore, target: Path) -> None:
        temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp.xlsx")
        try:
            ledger.save_staged(temporary)
            self._ensure_file_in_staging(target.parent, temporary)
            os.replace(temporary, target)
        finally:
            ledger.workbook.close()
            if temporary.exists() and not is_link_or_reparse(temporary):
                temporary.unlink()

    def _reopen_staged_ledger(self, path: Path) -> None:
        ledger = LedgerStore.load(path)
        errors = ledger.validate()
        ledger.workbook.close()
        if errors:
            raise CoordinatorError("暂存主台账复读校验失败：" + "；".join(errors))

    def _mark_run(self, ledger_path: Path, run_id: str, status: str, summary: str) -> None:
        ledger = LedgerStore.load(ledger_path)
        worksheet = ledger.workbook["运行记录"]
        columns = ledger._resolve_columns("运行记录")
        for row_number in range(2, worksheet.max_row + 1):
            if worksheet.cell(row_number, columns["运行标识"]).value == run_id:
                ledger._set_cell(worksheet.cell(row_number, columns["状态"]), status, "状态")
                ledger._set_cell(worksheet.cell(row_number, columns["摘要"]), summary, "摘要")
                ledger._set_cell(worksheet.cell(row_number, columns["成功完成时间"]), datetime.now(), "成功完成时间")
                self._save_ledger(ledger, ledger_path)
                return
        ledger.workbook.close()
        raise CoordinatorError("暂存运行记录缺失")

    def _apply_dedup_and_watermarks(self, ledger: LedgerStore, source_runs: tuple[SourceRun, ...]) -> None:
        candidates = tuple(candidate for run in source_runs for candidate in run.candidates)
        result = deduplicate(candidates, ledger) if candidates else None
        if result is not None:
            observed = {str(row.get("观察标识") or "") for row in ledger.rows("候选观察")}
            today = datetime.now().date().isoformat()
            pending: list[dict[str, object]] = []
            for skill in result.skills:
                canonical = str(skill.get("Canonical source") or skill.get("canonical_source") or "").strip()
                stable = str(skill.get("内部标识") or "").strip()
                observation_id = f"discovered-{sha256((stable + '|' + canonical).encode('utf-8')).hexdigest()[:20]}"
                if observation_id not in observed:
                    pending.append({"观察标识": observation_id, "候选名称": str(skill.get("Skill名称") or skill.get("name") or stable),
                        "Canonical source": canonical, "观察状态": "待审查", "许可证": str(skill.get("许可证") or "待确认"),
                        "记录日期": today, "原因": "发现的规范候选；未完成 Task 7 审查，不进入当前Skill"})
                    observed.add(observation_id)
            for manual in result.manual_review:
                canonical = str(manual.get("Canonical source") or manual.get("canonical_source") or "").strip()
                reason = str(manual.get("原因") or manual.get("reason") or "需要人工复核")
                observation_id = f"manual-{sha256((canonical + '|' + reason).encode('utf-8')).hexdigest()[:20]}"
                if observation_id not in observed:
                    pending.append({"观察标识": observation_id, "候选名称": str(manual.get("候选名称") or manual.get("name") or "候选"),
                        "Canonical source": canonical, "观察状态": "人工复核", "许可证": str(manual.get("许可证") or "待确认"),
                        "记录日期": today, "原因": reason})
                    observed.add(observation_id)
            if pending:
                ledger.append_rows("候选观察", pending)
            existing = {str(row.get("别名标识") or "") for row in ledger.rows("来源别名")}
            current_ids = {str(row.get("内部标识") or "") for row in ledger.rows("当前Skill")}
            aliases = [row for row in result.aliases if row["别名标识"] not in existing and row["内部标识"] in current_ids]
            if aliases:
                ledger.append_rows("来源别名", aliases)
        watermarks = SourceWatermarkStore(ledger)
        # openpyxl stores Excel's timezone-naive serial dates; source adapters normalize on read.
        now = datetime.now()
        for run in source_runs:
            if run.status == "complete" and run.watermark:
                watermarks.write(Watermark(run.platform, run.query, now, run.watermark, "本轮完整覆盖"))

    def _apply_version_transactions(self, ledger: LedgerStore, state: _State, reviews: ReviewApplySummary) -> None:
        receipts_by_id = {getattr(receipt, "candidate_id", ""): receipt for receipt in reviews.receipts}
        if set(state.version_proposals) - set(receipts_by_id):
            raise CoordinatorError("已有版本审查缺少 Task 7 回执")
        current_by_id = {str(row.get("内部标识") or ""): row for row in ledger.rows("当前Skill")}
        for candidate_id, receipt in receipts_by_id.items():
            proposed = state.version_proposals.get(candidate_id)
            if proposed is None:
                # New formal entries were applied by Task 7 directly; their receipt is not a
                # version-transaction authority and must not leak into another run.
                consume_applied_review(receipt)
                continue
            current = current_by_id.get(candidate_id)
            if current is None:
                raise CoordinatorError("版本审查回执未绑定既有当前Skill")
            observed = {
                "fixed_version": receipt.fixed_version, "content_hash": receipt.fixed_content_hash,
                "canonical_source": receipt.canonical_source, "source_url": receipt.canonical_source,
                "evidence_paths": receipt.evidence_paths, "license": receipt.license,
                "security_grade": receipt.security_grade,
            }
            change = compare_version(current, observed)
            if change.status == "full_review_required":
                decision = VersionDecision.accept_from_applied_review(change, receipt, review_date=datetime.now().date().isoformat(), conclusion_change="完整复审通过")
                apply_approved_version(ledger, decision)
            else:
                consume_applied_review(receipt)

    def _artifacts_from_callback(self, prepared: PreparedRun) -> tuple[Path, ...]:
        returned = tuple(Path(item) for item in self.report_builder(prepared, prepared.staging_dir))
        try:
            assert_ordinary_path(prepared.staging_dir, require_directory=True)
            # Scan the complete callback result before Office sees a single artifact.
            self._tree_digest(prepared.staging_dir)
        except ValueError as exc:
            raise CoordinatorError("回调输出含链接、重解析点或越界父目录") from exc
        normalized: list[Path] = []
        for item in returned:
            path = item if item.is_absolute() else prepared.staging_dir / item
            try:
                path.relative_to(prepared.staging_dir)
                assert_ordinary_path(path)
                path.resolve(strict=True).relative_to(prepared.staging_dir.resolve(strict=True))
            except (OSError, RuntimeError, ValueError) as exc:
                raise CoordinatorError("回调 artifact 不在普通暂存根目录内") from exc
            self._ensure_file_in_staging(prepared.staging_dir, path)
            normalized.append(path.absolute())
        delivery = prepared.staging_dir / "deliveries"
        enumerated_office: set[Path] = set()
        if delivery.exists():
            try:
                assert_ordinary_path(delivery, require_directory=True)
                for path in delivery.rglob("*"):
                    if is_link_or_reparse(path):
                        raise ValueError(f"reparse:{path}")
                    if path.is_file() and path.suffix.casefold() in {".docx", ".xlsx"}:
                        assert_ordinary_path(path)
                        enumerated_office.add(path.absolute())
            except (OSError, RuntimeError, ValueError) as exc:
                raise CoordinatorError("交付树 Office 枚举遇到链接、重解析点或非普通文件") from exc
        returned_office = {
            path for path in normalized if path.suffix.casefold() in {".docx", ".xlsx"}
        }
        if returned_office != enumerated_office:
            missing = sorted(str(path) for path in enumerated_office - returned_office)
            extra = sorted(str(path) for path in returned_office - enumerated_office)
            raise CoordinatorError(f"report callback 未返回完整 Office artifact 集合；未返回={missing}；多余={extra}")
        return tuple(normalized)

    def _prepare_generation(self, state: _State) -> tuple[Path, str, str]:
        self.paths.output.mkdir(parents=True, exist_ok=True)
        assert_ordinary_path(self.paths.output, require_directory=True)
        generations = self.paths.output / "generations"
        generations.mkdir(exist_ok=True)
        assert_ordinary_path(generations, require_directory=True)
        generation = contained_child(generations, state.prepared.run_id)
        if generation.exists():
            raise CoordinatorError("不可覆盖既有发布代次")
        temporary_generation = contained_child(generations, f".{state.prepared.run_id}.pending")
        if temporary_generation.exists():
            raise CoordinatorError("不可覆盖既有暂存发布代次")
        delivery = state.prepared.staging_dir / "deliveries"
        try:
            if delivery.exists():
                self._ensure_file_or_directory_in_staging(state.prepared.staging_dir, delivery)
                shutil.copytree(delivery, temporary_generation)
            else:
                temporary_generation.mkdir()
            # A synchronous callback is still allowed to leave a background writer.  Rehash
            # the source after copying, before a private generation becomes publishable.
            self._ensure_staging_unchanged(state)
            delivery_hash = self._tree_digest(temporary_generation)
            manifest = temporary_generation / "generation-manifest.json"
            manifest.write_text(json.dumps({"run_id": state.prepared.run_id, "delivery_sha256": delivery_hash,
                "files": self._authority_files(temporary_generation)}, ensure_ascii=False, sort_keys=True), encoding="utf-8")
            self._fsync_tree(temporary_generation)
            manifest_hash = _sha256(manifest)
            self._verify_generation_authority(temporary_generation, state.prepared.run_id, delivery_hash, manifest_hash)
            os.replace(temporary_generation, generation)
            state.owned_generation = generation
            self._verify_generation_authority(generation, state.prepared.run_id, delivery_hash, manifest_hash)
            return generation, delivery_hash, manifest_hash
        except BaseException:
            if temporary_generation.exists() and not is_link_or_reparse(temporary_generation):
                shutil.rmtree(temporary_generation)
            raise

    def _commit_ledger_only(
        self,
        state: _State,
        generation: Path,
        delivery_hash: str,
        manifest_hash: str,
        *,
        evidence: OfficeEvidenceBundle,
        office_paths: tuple[Path, ...],
    ) -> PublishReceipt:
        self._verify_generation_authority(
            generation, state.prepared.run_id, delivery_hash, manifest_hash,
        )
        try:
            receipt = commit_prepared_generation(
                production_root=self.paths.root,
                run_id=state.prepared.run_id,
                staged_ledger=state.prepared.staging_ledger,
                expected_authority_sha256=state.production_ledger_sha,
                generation_path=generation,
                generation_manifest_sha256=manifest_hash,
                office_evidence=evidence,
                office_scope=state.prepared.office_scope,
                office_paths=office_paths,
            )
            state.committed, state.phase = True, "committed"
            return receipt
        except PublishError as exc:
            raise CoordinatorError(str(exc)) from exc

    def _production_has_committed_run(self, state: _State) -> bool:
        """Recover the linearization fact if an injected BaseException interrupts os.replace."""
        try:
            if not state.prepared.staging_ledger.is_file() or _sha256(self.paths.ledger) != _sha256(state.prepared.staging_ledger):
                return False
            ledger = LedgerStore.load(self.paths.ledger)
            try:
                row = next((item for item in reversed(ledger.rows("运行记录")) if item.get("运行标识") == state.prepared.run_id), None)
            finally:
                ledger.workbook.close()
            if row is None or row.get("状态") != "成功":
                return False
            self._verify_recorded_generation(row)
            return True
        except BaseException:
            return False

    def _inject(self, point: str) -> None:
        if self.fail_at == point:
            raise RuntimeError(f"injected failure: {point}")

    def _fail_terminal(self, state: _State) -> None:
        self._terminal(state, remove_staging=True, remove_generation=True)

    def _terminal(self, state: _State, *, remove_staging: bool, remove_generation: bool = False) -> tuple[str, ...]:
        warnings: list[str] = []
        state.phase = "finalized"
        try:
            if remove_staging:
                try:
                    self._remove_owned_staging(state.prepared.staging_dir)
                except BaseException as exc:
                    warnings.append(f"staging-cleanup:{exc}")
            if state.owned_generation is not None and remove_generation:
                try:
                    self._remove_generation(state.owned_generation, self.paths.output / "generations")
                except BaseException as exc:
                    warnings.append(f"generation-cleanup:{exc}")
        finally:
            try:
                state.lock.release()
            except BaseException as exc:
                warnings.append(f"lock-release:{exc}")
                handle = getattr(state.lock, "_handle", None)
                if handle is not None:
                    try:
                        handle.close()
                        state.lock._handle = None
                    except BaseException as close_error:
                        warnings.append(f"lock-force-close:{close_error}")
            finally:
                try:
                    receipts = state.review_summary.receipts if state.review_summary else ()
                    clear_review_run_state(packets=tuple(state.review_packets.values()), receipts=receipts)
                except BaseException as exc:
                    warnings.append(f"registry-clear:{exc}")
                finally:
                    try:
                        clear_office_run_state(scope=state.prepared.office_scope)
                    except BaseException as exc:
                        warnings.append(f"office-registry-clear:{exc}")
                    finally:
                        self._states.pop(state.prepared.run_id, None)
        return tuple(warnings)

    def _remove_owned_staging(self, staging: Path) -> None:
        try:
            staging.relative_to(self.paths.staging_root)
        except ValueError:
            raise CoordinatorError("拒绝清理项目外路径")
        if staging == self.paths.staging_root or not staging.exists():
            return
        self._ensure_file_or_directory_in_staging(self.paths.staging_root, staging)
        for item in staging.rglob("*"):
            if is_link_or_reparse(item):
                raise CoordinatorError("拒绝跟随链接清理暂存目录")
        shutil.rmtree(staging)

    @staticmethod
    def _remove_generation(generation: Path, root: Path) -> None:
        generation.relative_to(root)
        if generation.exists() and not is_link_or_reparse(generation):
            shutil.rmtree(generation)

    @staticmethod
    def _tree_digest(root: Path) -> str:
        if not root.is_dir() or is_link_or_reparse(root):
            raise CoordinatorError("暂存根不是普通目录")
        digest = sha256()
        for item in sorted(root.rglob("*"), key=lambda path: str(path.relative_to(root)).casefold()):
            if is_link_or_reparse(item):
                raise CoordinatorError("暂存目录包含链接或重解析点")
            relative = item.relative_to(root).as_posix().encode("utf-8")
            digest.update(relative + b"\0")
            if item.is_file():
                digest.update(_sha256(item).encode("ascii"))
        return digest.hexdigest()

    @staticmethod
    def _tree_digest_excluding(root: Path, excluded: Path) -> str:
        digest = sha256()
        for item in sorted(root.rglob("*"), key=lambda path: str(path.relative_to(root)).casefold()):
            if item == excluded:
                continue
            if is_link_or_reparse(item):
                raise CoordinatorError("generation 包含链接或重解析点")
            digest.update(item.relative_to(root).as_posix().encode("utf-8") + b"\0")
            if item.is_file():
                digest.update(_sha256(item).encode("ascii"))
        return digest.hexdigest()

    @staticmethod
    def _ensure_file_in_staging(root: Path, path: Path, *, require_staging: bool = True) -> None:
        if require_staging:
            path.relative_to(root)
        if not path.is_file() or is_link_or_reparse(path):
            raise CoordinatorError("文件必须是暂存目录内的普通文件")

    @staticmethod
    def _ensure_file_or_directory_in_staging(root: Path, path: Path) -> None:
        path.relative_to(root)
        if is_link_or_reparse(path) or not (path.is_file() or path.is_dir()):
            raise CoordinatorError("路径必须是暂存目录内的普通文件或目录")

    @staticmethod
    def _decision_mapping(decision: ReviewDecision) -> dict[str, Any]:
        facts, judgments, derived = decision.observed_facts, decision.project_judgments, decision.derived_fields
        return {"candidate_id": decision.candidate_id, "observed_facts": {
            "fixed_version": facts.fixed_version, "entry_description_complete": facts.entry_description_complete,
            "prerequisites_clear_and_available": facts.prerequisites_clear_and_available, "license": facts.license,
            "canonical_source": facts.canonical_source, "evidence_paths": list(facts.evidence_paths),
            "remote_api_call": facts.remote_api_call, "remote_endpoints": list(facts.remote_endpoints),
            "local_professional_software": facts.local_professional_software,
            "local_script_plugin_interface": facts.local_script_plugin_interface, "security_grade": facts.security_grade,
            "verification_status": facts.verification_status,
        }, "project_judgments": {
            "record_tier": judgments.record_tier, "display_in_product": judgments.display_in_product,
            "direct_deployable": judgments.direct_deployable, "relevance_score": judgments.relevance_score,
            "quality_bonus_flags": list(judgments.quality_bonus_flags),
        }, "derived_fields": {"quality_score": derived.quality_score, "ledger_row": derived.ledger_row}}

    def _decision_digest(self, decisions: tuple[ReviewDecision, ...]) -> str:
        payload = [self._decision_mapping(item) for item in decisions]
        return sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")).hexdigest()

    @staticmethod
    def _object_digest(value: object) -> str:
        """Stable, read-only binding for injected catalog/source snapshots."""
        if is_dataclass(value):
            value = asdict(value)
        elif isinstance(value, Mapping):
            value = dict(value)
        elif isinstance(value, (tuple, list)):
            value = [RunCoordinator._digest_value(item) for item in value]
        else:
            value = RunCoordinator._digest_value(value)
        return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")).hexdigest()

    @staticmethod
    def _digest_value(value: object) -> object:
        if is_dataclass(value):
            return asdict(value)
        if isinstance(value, Mapping):
            return {str(key): RunCoordinator._digest_value(item) for key, item in value.items()}
        if isinstance(value, (tuple, list)):
            return [RunCoordinator._digest_value(item) for item in value]
        if hasattr(value, "__dict__"):
            return {str(key): RunCoordinator._digest_value(item) for key, item in vars(value).items()}
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        # Opaque sentinels have no observable snapshot fields.  Their repr normally embeds
        # an address and must not manufacture a false catalog/source change on every call.
        return {"opaque_type": f"{type(value).__module__}.{type(value).__qualname__}"}
