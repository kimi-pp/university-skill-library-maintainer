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

from .catalog import Catalog, build_scopes, load_catalog_with_ledger, verify_catalog_source
from .dedup import deduplicate
from .ledger import LedgerStore
from .paths import assert_ordinary_path
from .queries import PLATFORM_ORDER, QueryJob, build_queries
from .reports import make_project_report_builder
from .review import ReviewPacket, build_review_packet
from .runner import PreparedRun, RunCoordinator, RunRequest, SourceRun
from .settings import load_settings
from .snapshots import SnapshotCandidate, SnapshotManifest, build_snapshot
from .sources.base import (
    DoctorSmokeResult,
    EvidenceRoot,
    PagedHttpAdapter,
    SearchBatch,
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
        self._catalog_cache: Catalog | None = None
        self._now = now or (lambda: datetime.now(timezone.utc))
        self._review_materials: tuple[ReviewMaterial, ...] = ()
        self._observations: tuple[CandidateObservation, ...] = ()
        self._material_run_id: str | None = None
        self._material_consumed = False

    @property
    def review_materials(self) -> tuple[ReviewMaterial, ...]:
        return self._review_materials

    @property
    def observations(self) -> tuple[CandidateObservation, ...]:
        return self._observations

    def load_catalog(self) -> Catalog:
        if self._catalog_cache is None:
            value = self._catalog_loader()
            if not isinstance(value, Catalog):
                raise ProductionDriverError("目录加载器必须返回 Catalog")
            self._catalog_cache = value
        return self._catalog_cache

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
        settings = load_settings(request.settings_path)
        ledger = LedgerStore.load(self.workflow_root / "ledger" / "Skills主台账.xlsx")
        try:
            watermarks = SourceWatermarkStore(ledger)
            tracked_rows = tuple(ledger.rows("当前Skill"))
            jobs_by_platform: dict[str, list[QueryJob]] = {platform: [] for platform in PLATFORM_ORDER}
            for scope in scopes:
                for job in build_queries(scope):
                    jobs_by_platform[job.platform].append(job)

            raw_by_platform: dict[str, list[dict[str, object]]] = {platform: [] for platform in PLATFORM_ORDER}
            requests_by_platform: dict[str, list[SourceRequestEvent]] = {platform: [] for platform in PLATFORM_ORDER}
            evidence_by_platform: dict[str, list[Path]] = {platform: [] for platform in PLATFORM_ORDER}
            statuses_by_platform: dict[str, list[str]] = {platform: [] for platform in PLATFORM_ORDER}
            watermark_updates: dict[str, list[tuple[str, str]]] = {platform: [] for platform in PLATFORM_ORDER}
            now = self._now()

            for platform in PLATFORM_ORDER:
                platform_root = evidence_root_path / _safe_component(platform)
                platform_root.mkdir()
                evidence_root = EvidenceRoot(platform_root)
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
        tracked_by_canonical: dict[str, Mapping[str, object]] = {}
        if settings.research.check_existing_skill_updates:
            for row in tracked_rows:
                canonical = _normalize_url(str(row.get("Canonical source") or ""))
                stable_id = str(row.get("内部标识") or "").strip()
                if not stable_id or not _github_canonical(canonical):
                    continue
                tracked_by_canonical[canonical] = row
                if canonical in discovered_canonicals:
                    continue
                synthetic = {
                    "platform": "GitHub", "source_url": canonical, "canonical_source": canonical,
                    "name": str(row.get("Skill名称") or stable_id), "publisher": "",
                    "version_hint": str(row.get("固定版本") or ""),
                    "updated_at": "", "observed_on": self._now().date().isoformat(),
                    "scope_id": "", "query_id": "existing-version-check",
                    "response_evidence_sha256": "", "内部标识": stable_id,
                }
                raw_by_platform["GitHub"].append(synthetic)
                all_candidates.append(synthetic)

        materials: list[ReviewMaterial] = []
        observations: list[CandidateObservation] = []
        unique_groups: dict[str, list[dict[str, object]]] = {}
        for item in all_candidates:
            stable_id = stable_by_identity.get(_identity_key(item), str(item.get("内部标识") or ""))
            if stable_id:
                unique_groups.setdefault(stable_id, []).append(item)
        github = self.adapters["GitHub"]
        for stable_id, group in sorted(unique_groups.items()):
            canonical = str(next((item["canonical_source"] for item in group if item.get("canonical_source")), ""))
            name = str(next((item.get("name") for item in group if item.get("name")), stable_id))
            platforms = tuple(platform for platform in PLATFORM_ORDER if any(item["platform"] == platform for item in group))
            scopes_for_group = tuple(sorted({str(item["scope_id"]) for item in group if item.get("scope_id")}))
            if not _github_canonical(canonical):
                observation = CandidateObservation(
                    stable_id, name, canonical, platforms, "fixed-package-unavailable",
                    "当前来源接口没有提供可审查的完整固定版本包；仅保留候选观察，不构建 ReviewPacket。",
                )
                observations.append(observation)
                self._mark_group_observation(group, observation, status="条件候选")
                continue
            version = github.latest_version(canonical)
            if getattr(version, "error", None) is not None or not getattr(version, "version", None):
                deleted = _is_deleted_version_error(getattr(version, "error", None)) and canonical in tracked_by_canonical
                observation = CandidateObservation(
                    stable_id, name, canonical, platforms,
                    "upstream-deleted" if deleted else "fixed-version-unavailable",
                    "上游已删除或不可用；保留既有当前版本和固定快照。" if deleted else
                    "canonical GitHub 上游未能取得固定 commit SHA；不得进入正式评审。",
                )
                observations.append(observation)
                self._mark_group_observation(group, observation, status="attention_required" if deleted else "条件候选")
                continue
            tracked = tracked_by_canonical.get(canonical)
            if tracked is not None and str(tracked.get("固定版本") or "").strip() == str(version.version):
                continue
            archive_destination = self._snapshot_destination(github, evidence_root_path, stable_id, version.version)
            snapshot = github.snapshot(canonical, version.version, archive_destination)
            if getattr(snapshot, "error", None) is not None or not snapshot.sha256 or not Path(snapshot.destination).is_file():
                observation = CandidateObservation(
                    stable_id, name, canonical, platforms, "fixed-package-unavailable",
                    "canonical GitHub 固定 commit archive 获取失败；不得伪造固定包评审材料。",
                )
                observations.append(observation)
                self._mark_group_observation(group, observation, status="条件候选")
                continue
            archive_path = Path(snapshot.destination).absolute()
            evidence_by_platform["GitHub"].append(archive_path)
            candidate = SnapshotCandidate(
                stable_id, version.version, archive_path,
                tuple(str(path) for path in evidence_by_platform["GitHub"]),
            )
            manifest = build_snapshot(candidate, snapshot_root / stable_id)
            materials.append(ReviewMaterial(
                stable_id, name, canonical, version.version, manifest.fixed_content_hash,
                manifest.destination, manifest.evidence_paths, platforms, scopes_for_group, manifest,
            ))

        self._review_materials = tuple(materials)
        self._observations = tuple(observations)
        self._material_run_id = None
        self._material_consumed = False
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
        }

    @staticmethod
    def _mark_group_observation(
        group: Iterable[dict[str, object]], observation: CandidateObservation, *, status: str,
    ) -> None:
        for item in group:
            item["observation_status"] = status
            item["observation_reason_code"] = observation.reason_code
            item["observation_reason"] = observation.detail

    def material_review_frame(self, prepared: object) -> dict[str, object]:
        run_id = str(getattr(prepared, "run_id", ""))
        if not run_id:
            raise MaterialReviewError("材料评审必须绑定非空 run_id")
        if self._material_run_id not in (None, run_id) or self._material_consumed:
            raise MaterialReviewError("材料评审 capability 已失效或属于其他运行")
        self._material_run_id = run_id
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
        run_id = str(getattr(prepared, "run_id", ""))
        if self._material_consumed or self._material_run_id != run_id:
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
                },
                material._manifest,
            )
            if packet.fixed_content_hash != material.fixed_content_hash:
                raise MaterialReviewError("ReviewPacket 未绑定当前固定内容哈希")
            packets[candidate_id] = packet
        self._material_consumed = True
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


def _safe_component(value: str) -> str:
    return "".join(character if character.isalnum() else "-" for character in value).strip("-").lower()
