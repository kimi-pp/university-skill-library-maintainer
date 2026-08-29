"""Production discovery and the same-process fixed-material review capability.

The driver only fetches public metadata and immutable archives.  It never imports,
installs, or executes candidate content.  Marketplace metadata remains an
observation unless it resolves to a canonical GitHub repository whose exact commit
archive can be captured and statically reviewed.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Callable, Iterable, Mapping, TextIO
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen
import weakref

from .catalog import Catalog, build_scopes, load_catalog_with_ledger, verify_catalog_source
from .dedup import deduplicate
from .ledger import LedgerStore
from .paths import assert_ordinary_path, is_link_or_reparse
from .queries import PLATFORM_ORDER, QueryJob, build_queries
from .reports import make_project_report_builder
from .review import ReviewPacket, build_review_packet, clear_review_run_state
from .runner import CoordinatorError, PreparedRun, RunCoordinator, RunRequest, SourceRun
from .settings import load_settings
from .snapshots import SnapshotManifest, archive_skill_entries, build_archive_entry_snapshot, clear_snapshot_manifests
from .sources.base import (
    DoctorSmokeResult,
    EvidenceRoot,
    PagedHttpAdapter,
    SearchBatch,
    MAX_ARCHIVE_BYTES,
    SourceCandidate,
    SourceRequestEvent,
    SourceWatermarkStore,
    doctor_smoke,
)
from .sources.clawhub import ClawHubAdapter
from .sources.github import GitHubAdapter
from .sources.huggingface import HuggingFaceAdapter
from .sources.skillhub import SkillHubAdapter
from .workspace_renderer import build_workspace_renderer_command


_GITHUB_REPOSITORY = re.compile(r"https://github\.com/[^/?#]+/[^/?#]+(?:\.git)?\Z", re.IGNORECASE)


class ProductionDriverError(RuntimeError):
    """The production discovery contract cannot be completed truthfully."""


class MaterialReviewError(ValueError):
    """The controller returned unbound or incomplete fixed-material facts."""


@dataclass(frozen=True)
class CandidateObservation:
    candidate_id: str
    name: str
    canonical_source: str
    platforms: tuple[str, ...]
    reason_code: str
    detail: str
    skill_entry_path: str = ""
    fixed_version: str = ""
    fixed_content_hash: str = ""
    evidence_paths: tuple[str, ...] = ()
    status: str = "条件候选"


@dataclass(frozen=True)
class ReviewMaterial:
    candidate_id: str
    name: str
    canonical_source: str
    fixed_version: str
    fixed_content_hash: str
    snapshot_path: Path
    evidence_paths: tuple[str, ...]
    source_platforms: tuple[str, ...]
    scope_ids: tuple[str, ...]
    _manifest: SnapshotManifest = field(repr=False, compare=False)
    upstream_repository: str = ""
    skill_entry_path: str = ""
    approved_scopes: tuple[tuple[str, str], ...] = ()

    def protocol_mapping(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "name": self.name,
            "canonical_source": self.canonical_source,
            "fixed_version": self.fixed_version,
            "fixed_content_hash": self.fixed_content_hash,
            "snapshot_path": str(self.snapshot_path),
            "evidence_paths": list(self.evidence_paths),
            "source_platforms": list(self.source_platforms),
            "scope_ids": list(self.scope_ids),
            "upstream_repository": self.upstream_repository,
            "skill_entry_path": self.skill_entry_path,
            "approved_scopes": [list(item) for item in self.approved_scopes],
        }


@dataclass(frozen=True)
class NetworkSmokeEntry:
    source: str
    ok: bool
    pages_checked: int
    status_code: int | None
    detail: str | None = None


@dataclass(frozen=True)
class NetworkSmokeReport:
    checked_at: str
    status: str
    entries: tuple[NetworkSmokeEntry, ...]


@dataclass(frozen=True)
class _ArchiveCapture:
    path: Path
    content: bytes
    sha256: str
    identity: tuple[int, int, int, int]


class ProductionDriver:
    """Build four exact SourceRuns and retain snapshot capabilities in memory."""

    def __init__(
        self,
        *,
        project_root: str | Path,
        adapters: Mapping[str, object] | None = None,
        catalog_loader: Callable[[], Catalog] | None = None,
        catalog_source_fetch: Callable[[str], bytes] | None = None,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self.project_root = Path(project_root).absolute()
        self.workflow_root = self.project_root / "07_自动维护工作流"
        self.adapters = dict(adapters or {
            "SkillHub": SkillHubAdapter(),
            "ClawHub": ClawHubAdapter(),
            "GitHub": GitHubAdapter(),
            "Hugging Face Spaces": HuggingFaceAdapter(),
        })
        if tuple(self.adapters) != PLATFORM_ORDER:
            raise ValueError("生产来源适配器必须按固定四平台顺序提供")
        self._catalog_loader = catalog_loader or self._load_project_catalog
        self._catalog_source_fetch = catalog_source_fetch
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._review_materials: tuple[ReviewMaterial, ...] = ()
        self._observations: tuple[CandidateObservation, ...] = ()
        self._material_run_id: str | None = None
        self._material_consumed = False
        self._material_frame_issued = False
        self._prepared_ref: weakref.ReferenceType[PreparedRun] | None = None
        self._coordinator_ref: weakref.ReferenceType[RunCoordinator] | None = None
        self._issued_packets: tuple[ReviewPacket, ...] = ()

    @property
    def review_materials(self) -> tuple[ReviewMaterial, ...]:
        return self._review_materials

    @property
    def observations(self) -> tuple[CandidateObservation, ...]:
        return self._observations

    def load_catalog(self) -> Catalog:
        value = self._catalog_loader()
        if not isinstance(value, Catalog):
            raise ProductionDriverError("目录加载器必须返回 Catalog")
        return value

    def _load_project_catalog(self) -> Catalog:
        catalog_path = self.project_root / "06_过程记录" / "discipline_mapping" / "catalogs" / "undergraduate_2026.json"
        ledger_path = self.workflow_root / "ledger" / "Skills主台账.xlsx"
        assert_ordinary_path(catalog_path)
        assert_ordinary_path(ledger_path)
        catalog = load_catalog_with_ledger(catalog_path, ledger_path)
        ledger = LedgerStore.load(ledger_path)
        try:
            baselines = tuple(ledger.rows("目录基线"))
        finally:
            ledger.workbook.close()
        if len(baselines) != 1:
            raise ProductionDriverError("目录基线必须在 Excel 中存在且唯一")
        url = str(baselines[0].get("公开地址") or "").strip()
        expected_sha = str(baselines[0].get("SHA-256") or "").strip().casefold()
        if not url.casefold().startswith("https://www.moe.gov.cn/") or re.fullmatch(r"[0-9a-f]{64}", expected_sha) is None:
            raise ProductionDriverError("目录基线必须绑定教育部 HTTPS 地址和有效 SHA-256")
        status = verify_catalog_source(url, expected_sha, fetch=self._catalog_source_fetch)
        return replace(catalog, source_status=status)

    def discover(self, request: RunRequest, staging_dir: Path) -> tuple[SourceRun, ...]:
        """Run all six-dimensional jobs, aggregate four statuses, then snapshot once per global identity."""
        staging = Path(staging_dir).absolute()
        assert_ordinary_path(staging, require_directory=True)
        evidence_root_path = staging / "source-evidence"
        evidence_root_path.mkdir(exist_ok=False)
        assert_ordinary_path(evidence_root_path, require_directory=True)
        snapshot_root = staging / "fixed-snapshots"
        snapshot_root.mkdir(exist_ok=False)
        assert_ordinary_path(snapshot_root, require_directory=True)

        catalog = self.load_catalog()
        scopes = build_scopes(catalog)
        scope_names = {scope.scope_id: scope.scope_name for scope in scopes}
        settings = load_settings(request.settings_path)
        ledger = LedgerStore.load(self.workflow_root / "ledger" / "Skills主台账.xlsx")
        try:
            watermarks = SourceWatermarkStore(ledger)
            tracked_rows = tuple(ledger.rows("当前Skill"))
            candidate_rows = tuple(ledger.rows("候选观察"))
            version_aliases = {
                (str(row.get("内部标识") or "").strip(), str(row.get("固定版本") or "").strip())
                for row in ledger.rows("来源别名")
                if str(row.get("关系类型") or "").strip() == "版本别名观察"
                and str(row.get("内部标识") or "").strip() and str(row.get("固定版本") or "").strip()
            }
            reviewed_nonformal_versions = {
                (str(row.get("内部标识") or "").strip(), str(row.get("固定版本") or "").strip())
                for row in candidate_rows
                if str(row.get("观察状态") or "").strip() in {"条件候选", "需适配候选", "排除", "attention_required"}
                and str(row.get("内部标识") or "").strip() and str(row.get("固定版本") or "").strip()
            }
            reviewed_nonformal_versions.update(version_aliases)
            jobs_by_platform: dict[str, list[QueryJob]] = {platform: [] for platform in PLATFORM_ORDER}
            for scope in scopes:
                for job in build_queries(scope):
                    jobs_by_platform[job.platform].append(job)

            raw_by_platform: dict[str, list[dict[str, object]]] = {platform: [] for platform in PLATFORM_ORDER}
            requests_by_platform: dict[str, list[SourceRequestEvent]] = {platform: [] for platform in PLATFORM_ORDER}
            evidence_by_platform: dict[str, list[Path]] = {platform: [] for platform in PLATFORM_ORDER}
            evidence_roots_by_platform: dict[str, EvidenceRoot] = {}
            statuses_by_platform: dict[str, list[str]] = {platform: [] for platform in PLATFORM_ORDER}
            postcheck_failed: dict[str, bool] = {platform: False for platform in PLATFORM_ORDER}
            watermark_updates: dict[str, list[tuple[str, str]]] = {platform: [] for platform in PLATFORM_ORDER}
            now = self._now()

            for platform in PLATFORM_ORDER:
                platform_root = evidence_root_path / _safe_component(platform)
                platform_root.mkdir()
                evidence_root = EvidenceRoot(platform_root)
                evidence_roots_by_platform[platform] = evidence_root
                adapter = self.adapters[platform]
                if isinstance(adapter, PagedHttpAdapter):
                    adapter.evidence_root = evidence_root
                for job in jobs_by_platform[platform]:
                    decision = watermarks.for_run(
                        platform, job.query, now,
                        full_recheck_interval_days=settings.research.full_recheck_interval_days,
                    )
                    batch = adapter.search(job, decision.search_watermark)
                    if not isinstance(batch, SearchBatch) or batch.platform != platform or batch.job != job:
                        raise ProductionDriverError(f"{platform} 返回了不属于当前查询的批次")
                    statuses_by_platform[platform].append(batch.status)
                    bound_events = self._bind_request_events(batch.requests, evidence_root, job)
                    requests_by_platform[platform].extend(bound_events)
                    evidence_by_platform[platform].extend(
                        event.evidence_path for event in bound_events if event.evidence_path is not None
                    )
                    for candidate in batch.candidates:
                        raw_by_platform[platform].append(self._candidate_mapping(candidate, scope_id=job.scope_id))
                    if batch.status == "complete":
                        marker = sha256(f"{platform}|{job.query}|{now.isoformat()}".encode()).hexdigest()[:20]
                        watermark_updates[platform].append((job.query, marker))
        finally:
            ledger.workbook.close()

        all_candidates = [item for platform in PLATFORM_ORDER for item in raw_by_platform[platform]]
        production_ledger = LedgerStore.load(self.workflow_root / "ledger" / "Skills主台账.xlsx")
        try:
            deduped = deduplicate(all_candidates, production_ledger)
        finally:
            production_ledger.workbook.close()
        stable_by_identity = {
            _identity_key(item): str(item["内部标识"])
            for item in deduped.skills
        }
        for items in raw_by_platform.values():
            for item in items:
                item["内部标识"] = stable_by_identity.get(_identity_key(item), "")

        # Search indexes are not an authoritative update feed.  Every already admitted
        # canonical GitHub Skill is checked even when no query happens to rediscover it.
        discovered_canonicals = {
            str(item.get("canonical_source") or "") for item in all_candidates
            if str(item.get("canonical_source") or "")
        }
        trackable_candidate_rows = tuple(
            row for row in candidate_rows
            if str(row.get("内部标识") or "").strip()
            and str(row.get("Skill入口路径") or "").strip()
            and str(row.get("固定版本") or "").strip()
        )
        tracked_identity_rows = (*tracked_rows, *trackable_candidate_rows)
        tracked_by_canonical: dict[str, list[Mapping[str, object]]] = {}
        if settings.research.check_existing_skill_updates:
            for row in tracked_identity_rows:
                canonical = _normalize_url(str(row.get("Canonical source") or ""))
                stable_id = str(row.get("内部标识") or "").strip()
                if not stable_id or not _github_canonical(canonical):
                    continue
                tracked_by_canonical.setdefault(canonical, []).append(row)
                if canonical in discovered_canonicals:
                    continue
                synthetic = {
                    "platform": "GitHub", "source_url": canonical, "canonical_source": canonical,
                    "name": str(row.get("Skill名称") or row.get("候选名称") or stable_id), "publisher": "",
                    "version_hint": str(row.get("固定版本") or ""),
                    "updated_at": "", "observed_on": self._now().date().isoformat(),
                    "scope_id": "", "query_id": "existing-version-check",
                    "response_evidence_sha256": "", "内部标识": stable_id,
                    "repository_index_only": True,
                }
                raw_by_platform["GitHub"].append(synthetic)
                all_candidates.append(synthetic)
                discovered_canonicals.add(canonical)

        materials: list[ReviewMaterial] = []
        observations: list[CandidateObservation] = []
        structured_by_platform: dict[str, list[dict[str, object]]] = {platform: [] for platform in PLATFORM_ORDER}
        unique_groups: dict[str, list[dict[str, object]]] = {}
        for item in all_candidates:
            stable_id = stable_by_identity.get(_identity_key(item), str(item.get("内部标识") or ""))
            canonical = str(item.get("canonical_source") or "")
            group_id = f"github-repository:{canonical}" if _github_canonical(canonical) else stable_id
            if group_id:
                unique_groups.setdefault(group_id, []).append(item)
        github = self.adapters["GitHub"]
        for group_id, group in sorted(unique_groups.items()):
            canonical = str(next((item["canonical_source"] for item in group if item.get("canonical_source")), ""))
            repository_observation_id = _entry_stable_id(canonical, "__repository__") if canonical else group_id
            name = str(next((item.get("name") for item in group if item.get("name")), repository_observation_id))
            platforms = tuple(platform for platform in PLATFORM_ORDER if any(item["platform"] == platform for item in group))
            scopes_for_group = tuple(sorted({str(item["scope_id"]) for item in group if item.get("scope_id")}))
            if not _github_canonical(canonical):
                observation = CandidateObservation(
                    repository_observation_id, name, canonical, platforms, "fixed-package-unavailable",
                    "当前来源接口没有提供可审查的完整固定版本包；仅保留候选观察，不构建 ReviewPacket。",
                )
                observations.append(observation)
                self._mark_group_observation(group, observation, status="条件候选")
                continue
            version = github.latest_version(canonical)
            version_complete = self._record_postcheck(
                version, "GitHub", requests_by_platform, evidence_by_platform,
                require_evidence=isinstance(github, PagedHttpAdapter),
                evidence_root=evidence_roots_by_platform["GitHub"],
            )
            if getattr(version, "error", None) is not None or not getattr(version, "version", None) or not version_complete:
                postcheck_failed["GitHub"] = True
                deleted = _is_deleted_version_error(getattr(version, "error", None)) and canonical in tracked_by_canonical
                if deleted:
                    evidence = self._candidate_evidence(group, requests_by_platform)
                    for tracked_row in tracked_by_canonical.get(canonical, ()):
                        tracked_id = str(tracked_row.get("内部标识") or "").strip()
                        tracked_entry = str(tracked_row.get("Skill入口路径") or "").strip()
                        observation = CandidateObservation(
                            tracked_id, str(tracked_row.get("Skill名称") or tracked_row.get("候选名称") or tracked_id),
                            canonical, ("GitHub",), "upstream-deleted",
                            "上游已删除或不可用；保留既有当前版本和固定快照。",
                            tracked_entry, str(tracked_row.get("固定版本") or ""),
                            str(tracked_row.get("固定版本内容指纹") or ""), evidence, "attention_required",
                        )
                        observations.append(observation)
                        structured_by_platform["GitHub"].append(_candidate_observation_row(observation, now.date().isoformat()))
                    if observations:
                        self._mark_group_observation(group, observations[-1], status="attention_required")
                else:
                    reason_code = "postcheck-evidence-incomplete" if not version_complete else "fixed-version-unavailable"
                    observation = CandidateObservation(
                        repository_observation_id, name, canonical, platforms, reason_code,
                        "版本核验请求缺少完整、持久化的请求证据；不得进入正式评审。" if not version_complete else
                        "canonical GitHub 上游未能取得固定 commit SHA；不得进入正式评审。",
                        status="attention_required" if not version_complete else "条件候选",
                    )
                    observations.append(observation)
                    self._mark_group_observation(group, observation, status=observation.status)
                    if not version_complete:
                        structured_by_platform["GitHub"].append(_candidate_observation_row(observation, now.date().isoformat()))
                continue
            tracked = tracked_by_canonical.get(canonical, [])
            if tracked and all(
                str(row.get("固定版本") or "").strip() == str(version.version)
                or (str(row.get("内部标识") or "").strip(), str(version.version)) in reviewed_nonformal_versions
                for row in tracked
            ):
                continue
            archive_destination = self._snapshot_destination(github, evidence_root_path, repository_observation_id, version.version)
            snapshot = github.snapshot(canonical, version.version, archive_destination)
            snapshot_complete = self._record_postcheck(
                snapshot, "GitHub", requests_by_platform, evidence_by_platform,
                require_evidence=isinstance(github, PagedHttpAdapter),
                evidence_root=evidence_roots_by_platform["GitHub"],
            )
            if (getattr(snapshot, "error", None) is not None or not snapshot.sha256
                    or not Path(snapshot.destination).is_file() or not snapshot_complete):
                postcheck_failed["GitHub"] = True
                reason_code = "postcheck-evidence-incomplete" if not snapshot_complete else "fixed-package-unavailable"
                observation = CandidateObservation(
                    repository_observation_id, name, canonical, platforms, reason_code,
                    "固定包下载请求缺少完整、持久化的请求证据；不得进入正式评审。" if not snapshot_complete else
                    "canonical GitHub 固定 commit archive 获取失败；不得伪造固定包评审材料。",
                    status="attention_required" if not snapshot_complete else "条件候选",
                )
                observations.append(observation)
                self._mark_group_observation(group, observation, status=observation.status)
                if not snapshot_complete:
                    structured_by_platform["GitHub"].append(_candidate_observation_row(observation, now.date().isoformat()))
                continue
            archive_path = Path(snapshot.destination).absolute()
            try:
                capture = _capture_archive_snapshot(archive_path, evidence_root_path, str(snapshot.sha256))
                source_evidence = self._candidate_evidence(group, requests_by_platform)
                source_evidence += (f"{archive_path}#sha256={capture.sha256}",)
                entries = archive_skill_entries(capture.content, archive_path.name)
            except (OSError, ValueError, ProductionDriverError) as exc:
                postcheck_failed["GitHub"] = True
                observation = CandidateObservation(
                    repository_observation_id, name, canonical, platforms, "archive-integrity-failed",
                    f"固定包归档的声明哈希、路径身份或不可变字节校验失败；不得进入评审：{exc}",
                )
                observations.append(observation)
                self._mark_group_observation(group, observation, status="条件候选")
                continue
            if not entries:
                observation = CandidateObservation(
                    repository_observation_id, name, canonical, platforms, "no-skill-entry",
                    "固定归档不包含可识别的具体 SKILL.md 入口；仓库元数据不得作为 Skill 内容评审。",
                )
                observations.append(observation)
                self._mark_group_observation(group, observation, status="排除")
                continue
            archive_entry_keys = {_normalize_entry(value) for value in entries}
            for missing in (
                row for row in tracked_identity_rows
                if _normalize_url(str(row.get("Canonical source") or "")) == canonical
                and _normalize_entry(str(row.get("Skill入口路径") or "")) not in archive_entry_keys
            ):
                missing_id = str(missing.get("内部标识") or "").strip()
                missing_entry = str(missing.get("Skill入口路径") or "").strip()
                observation = CandidateObservation(
                    missing_id, str(missing.get("Skill名称") or missing_id), canonical, ("GitHub",),
                    "upstream-entry-deleted",
                    f"新 commit 已不含既有 Skill 入口 {missing_entry}；保留旧正式版本和固定快照。",
                    missing_entry, str(version.version), "",
                    (*self._candidate_evidence(group, requests_by_platform), f"{archive_path}#sha256={capture.sha256}"),
                    "attention_required",
                )
                observations.append(observation)
                structured_by_platform["GitHub"].append(_candidate_observation_row(observation, now.date().isoformat()))
                raw_by_platform["GitHub"].append({
                    "platform": "GitHub", "source_url": canonical, "canonical_source": canonical,
                    "upstream_identity": canonical, "entry_path": missing_entry,
                    "name": str(missing.get("Skill名称") or missing_id), "publisher": "",
                    "version_hint": str(version.version), "updated_at": "",
                    "observed_on": self._now().date().isoformat(), "scope_id": "",
                    "query_id": "upstream-entry-check", "response_evidence_sha256": "",
                    "evidence_paths": "；".join((*self._candidate_evidence(group, requests_by_platform), f"{archive_path}#sha256={capture.sha256}")),
                    "内部标识": missing_id, "observation_status": "attention_required",
                    "observation_reason_code": observation.reason_code,
                    "observation_reason": observation.detail,
                })
            evidence_by_platform["GitHub"].append(archive_path)
            for entry_path in entries:
                tracked_entry = next(
                    (row for row in tracked_identity_rows if _normalize_url(str(row.get("Canonical source") or "")) == canonical
                     and _normalize_entry(str(row.get("Skill入口路径") or "")) == _normalize_entry(entry_path)),
                    None,
                )
                entry_id = str(tracked_entry.get("内部标识") or "") if tracked_entry else _entry_stable_id(canonical, entry_path)
                if (entry_id, str(version.version)) in reviewed_nonformal_versions:
                    continue
                entry_platforms = tuple(
                    platform for platform in PLATFORM_ORDER
                    if any(item["platform"] == platform and (
                        platform == "GitHub" or _normalize_entry(str(item.get("entry_path") or "")) == _normalize_entry(entry_path)
                    ) for item in group)
                )
                entry_evidence_group = [
                    item for item in group if item["platform"] == "GitHub"
                    or _normalize_entry(str(item.get("entry_path") or "")) == _normalize_entry(entry_path)
                ]
                entry_source_evidence = self._candidate_evidence(entry_evidence_group, requests_by_platform)
                entry_source_evidence += (f"{archive_path}#sha256={capture.sha256}",)
                manifest = build_archive_entry_snapshot(
                    candidate_id=entry_id, fixed_version=version.version,
                    archive_bytes=capture.content, archive_name=archive_path.name,
                    skill_entry_path=entry_path,
                    destination=snapshot_root / _safe_component(entry_id),
                    source_evidence_paths=entry_source_evidence,
                )
                evidence_by_platform["GitHub"].append(Path(manifest.manifest_evidence_path))
                materials.append(ReviewMaterial(
                    entry_id, name if len(entries) == 1 else f"{name}:{entry_path}", canonical,
                    version.version, manifest.fixed_content_hash, manifest.destination,
                    tuple(dict.fromkeys((*manifest.source_evidence_paths, *manifest.evidence_paths))),
                    entry_platforms, scopes_for_group, manifest,
                    canonical, entry_path,
                    tuple((scope_id, scope_names[scope_id]) for scope_id in scopes_for_group if scope_id in scope_names),
                ))

        self._review_materials = tuple(materials)
        self._observations = tuple(observations)
        self._material_run_id = None
        self._material_consumed = False
        self._material_frame_issued = False
        self._prepared_ref = None
        self._coordinator_ref = None
        for platform, failed in postcheck_failed.items():
            if failed:
                statuses_by_platform[platform].append("partial")
                watermark_updates[platform].clear()
        return tuple(
            SourceRun(
                platform=platform,
                status=_aggregate_status(statuses_by_platform[platform]),
                candidates=tuple(raw_by_platform[platform]),
                watermark=watermark_updates[platform][-1][1] if watermark_updates[platform] else None,
                query="__multiple_queries__",
                evidence_files=tuple(dict.fromkeys(evidence_by_platform[platform])),
                request_events=tuple(requests_by_platform[platform]),
                watermark_updates=tuple(watermark_updates[platform]),
                structured_observations=tuple(structured_by_platform[platform]),
            )
            for platform in PLATFORM_ORDER
        )

    @staticmethod
    def _snapshot_destination(adapter: object, evidence_root: Path, stable_id: str, version: str) -> Path:
        filename = f"{stable_id}-{version}.zip"
        if isinstance(adapter, PagedHttpAdapter):
            return Path("archives") / filename
        directory = evidence_root / "github-archives"
        directory.mkdir(exist_ok=True)
        return directory / filename

    @staticmethod
    def _bind_request_events(
        events: Iterable[SourceRequestEvent], evidence_root: EvidenceRoot, job: QueryJob,
    ) -> tuple[SourceRequestEvent, ...]:
        bound: list[SourceRequestEvent] = []
        for index, event in enumerate(events, start=1):
            if event.evidence_path is not None:
                path = Path(event.evidence_path).absolute()
                if not path.is_file():
                    raise ProductionDriverError("来源请求证据路径不存在")
                bound.append(event)
                continue
            if event.response_bytes is None or not event.response_sha256:
                bound.append(event)
                continue
            if sha256(event.response_bytes).hexdigest() != event.response_sha256:
                raise ProductionDriverError("来源响应字节与声明 SHA-256 不一致")
            path = evidence_root.write(Path(f"{job.query_id}-{index:04d}-{event.response_sha256}.json"), event.response_bytes)
            bound.append(replace(event, evidence_path=path))
        return tuple(bound)

    def _candidate_mapping(self, candidate: SourceCandidate, *, scope_id: str) -> dict[str, object]:
        canonical = _canonical_for_candidate(candidate)
        return {
            "platform": candidate.platform,
            "source_url": candidate.discovery_url,
            "canonical_source": canonical,
            "name": candidate.display_name,
            "publisher": candidate.publisher or "",
            "version_hint": candidate.version_hint or "",
            "updated_at": candidate.updated_at or "",
            "observed_on": self._now().date().isoformat(),
            "scope_id": scope_id,
            "query_id": candidate.query_id,
            "response_evidence_sha256": candidate.response_evidence_sha256,
            "entry_path": candidate.skill_entry_path or "",
            "upstream_identity": canonical,
            "repository_index_only": candidate.platform == "GitHub" and not candidate.skill_entry_path,
        }

    @staticmethod
    def _record_postcheck(
        result: object, platform: str,
        requests_by_platform: dict[str, list[SourceRequestEvent]],
        evidence_by_platform: dict[str, list[Path]],
        *, require_evidence: bool = False,
        evidence_root: EvidenceRoot | None = None,
    ) -> bool:
        events = tuple(getattr(result, "request_events", ()) or ())
        if not events:
            error = getattr(result, "error", None)
            kind = "snapshot" if hasattr(result, "destination") else "latest-version"
            identity = str(getattr(result, "identity", ""))
            destination = Path(getattr(result, "destination")) if kind == "snapshot" and getattr(result, "destination", None) else None
            evidence_path = destination if destination is not None and destination.is_file() and error is None else None
            digest = str(getattr(result, "sha256", None) or getattr(result, "response_evidence_sha256", None) or "") or None
            events = (SourceRequestEvent(
                platform, f"{kind}:{identity}", str(getattr(error, "url", None) or identity), 1,
                getattr(error, "status_code", None) if error is not None else 200, 1,
                digest, None, True, evidence_path, error is None,
            ),)
        bound_events: list[SourceRequestEvent] = []
        for event in events:
            if event.evidence_path is None and not event.completed and evidence_root is not None:
                audit = json.dumps({
                    "platform": event.platform, "query_id": event.query_id, "url": event.url,
                    "page": event.page, "status_code": event.status_code, "attempts": event.attempts,
                    "response_sha256": event.response_sha256, "completed": event.completed,
                    "error": str(getattr(getattr(result, "error", None), "message", "")),
                }, ensure_ascii=False, sort_keys=True).encode("utf-8")
                try:
                    audit_path = evidence_root.write(
                        Path(f"postcheck-audit-{sha256(audit).hexdigest()}.json"), audit,
                    )
                    event = replace(event, evidence_path=audit_path)
                except (OSError, ValueError):
                    pass
            bound_events.append(event)
        events = tuple(bound_events)
        requests_by_platform[platform].extend(events)
        evidence_by_platform[platform].extend(event.evidence_path for event in events if event.evidence_path is not None)
        evidence_by_platform[platform].extend(
            Path(path) for path in tuple(getattr(result, "evidence_paths", ()) or ()) if path is not None
        )
        return bool(events) and all(
            event.completed and (not require_evidence or event.evidence_path is not None)
            for event in events
        )

    @staticmethod
    def _candidate_evidence(
        group: Iterable[Mapping[str, object]],
        requests_by_platform: Mapping[str, list[SourceRequestEvent]],
    ) -> tuple[str, ...]:
        paths: list[str] = []
        for item in group:
            platform = str(item.get("platform") or "")
            query_id = str(item.get("query_id") or "")
            digest = str(item.get("response_evidence_sha256") or "")
            for event in requests_by_platform.get(platform, ()):
                if event.query_id == query_id and event.response_sha256 == digest and event.evidence_path is not None:
                    paths.append(str(event.evidence_path))
        canonical = str(next((item.get("canonical_source") for item in group if item.get("canonical_source")), ""))
        for event in requests_by_platform.get("GitHub", ()):
            if event.query_id.startswith((f"latest-version:{canonical}", f"snapshot:{canonical}")) and event.evidence_path is not None:
                paths.append(str(event.evidence_path))
        return tuple(dict.fromkeys(paths))

    @staticmethod
    def _mark_group_observation(
        group: Iterable[dict[str, object]], observation: CandidateObservation, *, status: str,
    ) -> None:
        for item in group:
            item["observation_status"] = status
            item["observation_reason_code"] = observation.reason_code
            item["observation_reason"] = observation.detail

    def register_prepared(
        self, prepared: PreparedRun, authority: Callable[[PreparedRun], None],
    ) -> None:
        """Bind the one real coordinator-owned PreparedRun for this material capability."""
        coordinator = getattr(authority, "__self__", None)
        function = getattr(authority, "__func__", None)
        if not isinstance(coordinator, RunCoordinator) or function is not RunCoordinator.assert_prepared_authority:
            raise MaterialReviewError("材料评审必须由真实 RunCoordinator 注册")
        try:
            authority(prepared)
        except CoordinatorError as exc:
            raise MaterialReviewError("材料评审 PreparedRun 不属于当前协调器") from exc
        self._prepared_ref = weakref.ref(prepared)
        self._coordinator_ref = weakref.ref(coordinator)

    def clear_prepared(self, prepared: PreparedRun) -> None:
        if self._prepared_ref is not None and self._prepared_ref() is prepared:
            clear_snapshot_manifests(tuple(item._manifest for item in self._review_materials))
            clear_review_run_state(packets=self._issued_packets)
            self._issued_packets = ()
            self._prepared_ref = None
            self._coordinator_ref = None
            self._material_run_id = None
            self._material_consumed = True

    def _assert_prepared_authority(self, prepared: object) -> PreparedRun:
        bound = self._prepared_ref() if self._prepared_ref is not None else None
        coordinator = self._coordinator_ref() if self._coordinator_ref is not None else None
        if bound is not prepared or coordinator is None:
            raise MaterialReviewError("材料评审必须使用当前协调器签发的原始 PreparedRun")
        try:
            coordinator.assert_prepared_authority(prepared)
        except CoordinatorError as exc:
            raise MaterialReviewError("材料评审 PreparedRun 已失效") from exc
        return prepared

    def material_review_frame(self, prepared: object) -> dict[str, object]:
        prepared = self._assert_prepared_authority(prepared)
        run_id = str(getattr(prepared, "run_id", ""))
        if not run_id:
            raise MaterialReviewError("材料评审必须绑定非空 run_id")
        if self._material_run_id is not None or self._material_consumed or self._material_frame_issued:
            raise MaterialReviewError("材料评审 capability 已失效或属于其他运行")
        self._material_run_id = run_id
        self._material_frame_issued = True
        return {
            "type": "material_review_required",
            "run_id": run_id,
            "materials": [item.protocol_mapping() for item in self._review_materials],
            "observations": [
                {
                    "candidate_id": item.candidate_id, "name": item.name,
                    "canonical_source": item.canonical_source, "platforms": list(item.platforms),
                    "reason_code": item.reason_code, "detail": item.detail,
                }
                for item in self._observations
            ],
        }

    def apply_material_observations(
        self, prepared: object, frame: Mapping[str, object],
    ) -> Mapping[str, ReviewPacket]:
        prepared = self._assert_prepared_authority(prepared)
        run_id = str(getattr(prepared, "run_id", ""))
        if self._material_consumed or not self._material_frame_issued or self._material_run_id != run_id:
            raise MaterialReviewError("材料评审 capability 已失效或未由当前运行签发")
        if frame.get("type") != "material_observations" or frame.get("run_id") != run_id:
            raise MaterialReviewError("材料观察帧类型或 run_id 不匹配")
        raw = frame.get("observations")
        if not isinstance(raw, list) or any(not isinstance(item, Mapping) for item in raw):
            raise MaterialReviewError("material_observations 必须包含对象数组 observations")
        expected = {item.candidate_id: item for item in self._review_materials}
        supplied = [str(item.get("candidate_id") or "") for item in raw]
        if len(supplied) != len(set(supplied)) or set(supplied) != set(expected):
            raise MaterialReviewError("材料观察必须精确覆盖全部固定包，且不得重复或新增")
        packets: dict[str, ReviewPacket] = {}
        try:
            for value in raw:
                candidate_id = str(value.get("candidate_id") or "")
                material = expected[candidate_id]
                for field_name, expected_value in (
                    ("fixed_version", material.fixed_version),
                    ("fixed_content_hash", material.fixed_content_hash),
                    ("canonical_source", material.canonical_source),
                ):
                    if str(value.get(field_name) or "") != expected_value:
                        raise MaterialReviewError(f"{candidate_id} 的 {field_name} 未绑定当前固定材料")
                license_name = str(value.get("license") or "").strip()
                security_grade = str(value.get("security_grade") or "").strip()
                if not license_name or security_grade not in {"SA", "SB", "SB-A", "X"}:
                    raise MaterialReviewError("材料观察必须给出许可证事实和允许的安全等级")
                packet = build_review_packet(
                    {
                        "candidate_id": candidate_id,
                        "canonical_source": material.canonical_source,
                        "license": license_name,
                        "security_grade": security_grade,
                        "upstream_repository": material.upstream_repository,
                        "skill_entry_path": material.skill_entry_path,
                        "approved_scopes": material.approved_scopes,
                    },
                    material._manifest,
                )
                if packet.fixed_content_hash != material.fixed_content_hash:
                    raise MaterialReviewError("ReviewPacket 未绑定当前固定内容哈希")
                packets[candidate_id] = packet
        except BaseException:
            clear_review_run_state(packets=tuple(packets.values()))
            clear_snapshot_manifests(tuple(item._manifest for item in self._review_materials))
            self._material_consumed = True
            raise
        self._material_consumed = True
        self._issued_packets = tuple(packets.values())
        return packets


def build_production_driver(
    *,
    project_root: Path,
    command: str,
    loader_output: str | None,
    expected_config_sha: str | None,
    input_stream: TextIO,
    output_stream: TextIO,
) -> tuple[RunCoordinator, RunRequest]:
    """Bind the real driver, report builder, renderer, and three-gate protocol."""
    if not loader_output:
        raise ProductionDriverError("生产运行必须提供工作区依赖加载器原始输出")
    project = Path(project_root).absolute()
    workflow = project / "07_自动维护工作流"
    driver = ProductionDriver(project_root=project)
    renderer = build_workspace_renderer_command(loader_output, project)
    # Delayed import avoids a module cycle while keeping the public gate implementation
    # in the CLI protocol module.
    from .cli import InteractiveOfficeGate

    coordinator = RunCoordinator(
        root=workflow,
        discover=driver.discover,
        report_builder=make_project_report_builder(workflow),
        office_verifier=InteractiveOfficeGate(input_stream=input_stream, output_stream=output_stream, renderer=renderer),
    )
    request = RunRequest(
        settings_path=workflow / "workflow-settings.toml",
        catalog_loader=driver.load_catalog,
        discover=driver.discover,
        expected_config_sha=expected_config_sha,
        material_reviewer=driver,
    )
    return coordinator, request


def run_network_smoke(
    *,
    platform_smoke: Callable[[str], DoctorSmokeResult] | None = None,
    ministry_fetch: Callable[[str], int] | None = None,
    ministry_url: str,
    now: Callable[[], datetime] | None = None,
) -> NetworkSmokeReport:
    """Probe exactly one endpoint/page per source without search, snapshots, or ledger writes."""
    adapters = {
        "SkillHub": SkillHubAdapter(),
        "ClawHub": ClawHubAdapter(),
        "GitHub": GitHubAdapter(),
        "Hugging Face Spaces": HuggingFaceAdapter(),
    }

    def default_platform(name: str) -> DoctorSmokeResult:
        return doctor_smoke(adapters[name], platform=name)

    probe = platform_smoke or default_platform
    entries: list[NetworkSmokeEntry] = []
    for platform in PLATFORM_ORDER:
        try:
            result = probe(platform)
            entries.append(NetworkSmokeEntry(platform, result.ok, result.pages_checked, result.status_code, result.detail))
        except (OSError, ValueError, RuntimeError) as exc:
            entries.append(NetworkSmokeEntry(platform, False, 1, None, str(exc)))
    fetch = ministry_fetch or _ministry_status
    try:
        status_code = int(fetch(ministry_url))
        entries.append(NetworkSmokeEntry("教育部专业目录", 200 <= status_code < 400, 1, status_code))
    except (OSError, HTTPError, URLError, ValueError) as exc:
        entries.append(NetworkSmokeEntry("教育部专业目录", False, 1, getattr(exc, "code", None), str(exc)))
    status = "PASS" if all(item.ok for item in entries) else "PARTIAL"
    checked = (now or (lambda: datetime.now(timezone.utc)))()
    return NetworkSmokeReport(checked.isoformat(), status, tuple(entries))


def _ministry_status(url: str) -> int:
    request = Request(url, method="GET", headers={"Range": "bytes=0-0", "User-Agent": "university-skill-maintainer-doctor/0.1"})
    with urlopen(request, timeout=20) as response:  # nosec B310 - explicit configured Ministry URL only
        response.read(1)
        return int(response.status)


def _archive_path_identity(path: Path) -> tuple[int, int, int, int]:
    result = path.lstat()
    return (getattr(result, "st_dev", 0), getattr(result, "st_ino", 0), result.st_size, result.st_mtime_ns)


def _archive_handle_identity(handle: object) -> tuple[int, int, int, int]:
    result = __import__("os").fstat(handle.fileno())
    return (getattr(result, "st_dev", 0), getattr(result, "st_ino", 0), result.st_size, result.st_mtime_ns)


def _capture_archive_snapshot(path: Path, evidence_root: Path, declared_sha256: str) -> _ArchiveCapture:
    """Read once from one descriptor and bind path identity, bytes, and declared hash."""
    archive = Path(path).absolute()
    root = Path(evidence_root).absolute()
    try:
        archive.relative_to(root)
        assert_ordinary_path(root, require_directory=True)
        assert_ordinary_path(archive)
    except (OSError, ValueError) as exc:
        raise ProductionDriverError("固定包归档必须位于本轮普通证据目录") from exc
    if is_link_or_reparse(archive) or not archive.is_file():
        raise ProductionDriverError("固定包归档必须是非链接普通文件")
    before_path = _archive_path_identity(archive)
    if before_path[2] > MAX_ARCHIVE_BYTES:
        raise ProductionDriverError("固定包压缩字节数超过硬边界")
    with archive.open("rb") as handle:
        before_handle = _archive_handle_identity(handle)
        if before_handle != before_path:
            raise ProductionDriverError("固定包路径与已打开归档身份不一致")
        content = handle.read(MAX_ARCHIVE_BYTES + 1)
        if len(content) > MAX_ARCHIVE_BYTES:
            raise ProductionDriverError("固定包压缩字节数超过硬边界")
        after_handle = _archive_handle_identity(handle)
    if after_handle != before_handle:
        raise ProductionDriverError("固定包归档在单句柄读取期间被原地改写")
    if is_link_or_reparse(archive) or not archive.is_file() or _archive_path_identity(archive) != before_path:
        raise ProductionDriverError("固定包归档路径在读取后被替换")
    actual = sha256(content).hexdigest()
    if re.fullmatch(r"[0-9a-f]{64}", declared_sha256.strip(), re.IGNORECASE) is None or actual != declared_sha256.casefold():
        raise ProductionDriverError("固定包归档实际 SHA-256 与来源声明不一致")
    return _ArchiveCapture(archive, content, actual, before_path)


def _canonical_for_candidate(candidate: SourceCandidate) -> str:
    if candidate.platform == "GitHub" and _github_canonical(candidate.discovery_url):
        return _normalize_url(candidate.discovery_url)
    hint = candidate.canonical_source_hint or ""
    return _normalize_url(hint) if _github_canonical(hint) else ""


def _github_canonical(value: str) -> bool:
    return bool(_GITHUB_REPOSITORY.fullmatch(_normalize_url(value)))


def _normalize_url(value: str) -> str:
    parsed = urlsplit(str(value).strip())
    if not parsed.scheme or not parsed.netloc:
        return ""
    path = parsed.path.rstrip("/")
    if path.casefold().endswith(".git"):
        path = path[:-4]
    return urlunsplit((parsed.scheme.casefold(), parsed.netloc.casefold(), path, parsed.query, parsed.fragment))


def _identity_key(value: Mapping[str, object]) -> str:
    canonical = str(value.get("canonical_source") or "")
    if canonical:
        return f"canonical:{canonical}"
    return "discovery:" + str(value.get("source_url") or "")


def _aggregate_status(values: Iterable[str]) -> str:
    statuses = tuple(values)
    if not statuses or all(value == "failed" for value in statuses):
        return "failed"
    if all(value == "complete" for value in statuses):
        return "complete"
    return "partial"


def _is_deleted_version_error(error: object | None) -> bool:
    if error is None:
        return False
    status = getattr(error, "status_code", None)
    message = str(getattr(error, "message", "")).casefold()
    return status in {404, 410} or "not found" in message or "deleted" in message


def _candidate_observation_row(observation: CandidateObservation, recorded_on: str) -> dict[str, object]:
    material = "|".join((
        observation.candidate_id, observation.canonical_source, observation.skill_entry_path,
        observation.fixed_version, observation.reason_code,
    ))
    return {
        "观察标识": f"observation-{sha256(material.encode('utf-8')).hexdigest()[:20]}",
        "内部标识": observation.candidate_id,
        "候选名称": observation.name or observation.candidate_id,
        "Canonical source": observation.canonical_source,
        "Skill入口路径": observation.skill_entry_path,
        "观察状态": observation.status,
        "许可证": "待确认",
        "记录日期": recorded_on,
        "原因": observation.detail,
        "固定版本": observation.fixed_version,
        "固定版本内容指纹": observation.fixed_content_hash,
        "验证证据位置": "；".join(observation.evidence_paths),
        "原因代码": observation.reason_code,
        "显示层级": "不展示" if observation.status in {"排除", "attention_required"} else observation.status,
    }


def _safe_component(value: str) -> str:
    return "".join(character if character.isalnum() else "-" for character in value).strip("-").lower()


def _normalize_entry(value: str) -> str:
    return value.replace("\\", "/").strip(" /").casefold()


def _entry_stable_id(canonical: str, entry_path: str) -> str:
    material = f"source:{_normalize_url(canonical)}|entry:{_normalize_entry(entry_path)}"
    return f"SK-{sha256(material.encode('utf-8')).hexdigest()[:16].upper()}"
