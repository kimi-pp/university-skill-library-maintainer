"""来源适配器共用的只读传输、证据和水位契约。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
from stat import S_ISREG
import time
from typing import Callable, Literal, Mapping, Protocol
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..ledger import LedgerStore
from ..queries import QueryJob


SearchStatus = Literal["complete", "partial", "failed"]


@dataclass(frozen=True)
class HttpResponse:
    url: str
    status: int
    body: bytes


@dataclass(frozen=True)
class SourceCandidate:
    platform: str
    native_id: str
    discovery_url: str
    canonical_source_hint: str | None
    version_hint: str | None
    display_name: str
    publisher: str | None
    updated_at: str | None
    popularity: Mapping[str, int | float | str]
    query_id: str
    response_evidence_sha256: str


@dataclass(frozen=True)
class SourceRequestEvent:
    platform: str
    query_id: str
    url: str
    page: int
    status_code: int | None
    attempts: int
    response_sha256: str | None
    response_bytes: bytes | None
    last_page: bool = False
    evidence_path: Path | None = None


@dataclass(frozen=True)
class SourceError:
    platform: str
    query_id: str
    message: str
    status_code: int | None = None
    url: str | None = None


@dataclass(frozen=True)
class SearchBatch:
    platform: str
    job: QueryJob
    status: SearchStatus
    candidates: tuple[SourceCandidate, ...] = ()
    requests: tuple[SourceRequestEvent, ...] = ()
    errors: tuple[SourceError, ...] = ()


@dataclass(frozen=True)
class VersionObservation:
    platform: str
    identity: str
    version: str | None
    observed_at: datetime
    response_evidence_sha256: str | None
    error: SourceError | None = None


@dataclass(frozen=True)
class SnapshotResult:
    platform: str
    identity: str
    version: str | None
    destination: Path
    sha256: str | None
    error: SourceError | None = None


@dataclass(frozen=True)
class EvidenceRoot:
    """经解析和反链接检查的证据根；所有持久化证据必须经此对象写入。"""

    root: Path

    def __post_init__(self) -> None:
        resolved = self.root.resolve(strict=True)
        if not resolved.is_dir() or _is_link_or_reparse(self.root):
            raise ValueError("EvidenceRoot 必须是现有的非链接目录")
        object.__setattr__(self, "root", resolved)

    def write(self, relative_destination: Path, content: bytes) -> Path:
        if relative_destination.is_absolute() or ".." in relative_destination.parts:
            raise ValueError("证据目标必须是 EvidenceRoot 内的相对路径")
        destination = self.root.joinpath(relative_destination)
        self._ensure_safe_parents(destination.parent)
        resolved_parent = destination.parent.resolve(strict=True)
        if self.root not in (resolved_parent, *resolved_parent.parents):
            raise ValueError("证据目标超出 EvidenceRoot")
        requested_sha = sha256(content).hexdigest()
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        for attempt in range(3):
            if destination.exists():
                existing_sha = self._stable_existing_sha(destination)
                if existing_sha == requested_sha:
                    return destination
                if existing_sha is not None and attempt == 2:
                    raise ValueError(f"证据快照已存在且内容不同：{destination}")
                time.sleep(0.01)
                continue
            try:
                descriptor = os.open(destination, flags, 0o600)
            except FileExistsError:
                time.sleep(0.01)
                continue
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            if _is_link_or_reparse(destination) or not S_ISREG(destination.stat().st_mode):
                raise ValueError("证据写入后不是普通文件")
            if sha256(destination.read_bytes()).hexdigest() != requested_sha:
                raise OSError("证据快照写入后的 SHA-256 不一致")
            return destination
        raise OSError(f"证据快照排他创建未在限定重试内稳定：{destination}")

    @staticmethod
    def _stable_existing_sha(destination: Path) -> str | None:
        if _is_link_or_reparse(destination) or not S_ISREG(destination.stat().st_mode):
            raise ValueError("证据目标必须是普通文件")
        before = destination.stat()
        first = destination.read_bytes()
        time.sleep(0.01)
        after = destination.stat()
        second = destination.read_bytes()
        if (before.st_size, before.st_mtime_ns, sha256(first).digest()) != (after.st_size, after.st_mtime_ns, sha256(second).digest()):
            return None
        return sha256(second).hexdigest()

    def _ensure_safe_parents(self, parent: Path) -> None:
        relative = parent.relative_to(self.root)
        current = self.root
        for part in relative.parts:
            current = current / part
            if current.exists():
                if _is_link_or_reparse(current) or not current.is_dir():
                    raise ValueError("证据目录包含链接、重解析点或普通文件")
            else:
                current.mkdir()


class SourceAdapter(Protocol):
    def search(self, job: QueryJob, watermark: "Watermark | None") -> SearchBatch: ...

    def latest_version(self, identity: str) -> VersionObservation: ...

    def snapshot(self, identity: str, version: str | None, destination: Path) -> SnapshotResult: ...


@dataclass(frozen=True)
class DoctorSmokeResult:
    """不涉及候选、账本或证据写入的单页连通性结果。"""

    platform: str
    ok: bool
    pages_checked: int
    status_code: int | None
    detail: str | None = None


HttpTransport = Callable[[str, float], HttpResponse]


def urllib_transport(url: str, timeout: float) -> HttpResponse:
    """以显式超时获取字节，不执行或解释远端候选内容。"""
    request = Request(url, method="GET", headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:  # nosec B310 - adapter endpoints are constants
            return HttpResponse(url=response.geturl(), status=response.status, body=response.read())
    except HTTPError as error:
        return HttpResponse(url=url, status=error.code, body=error.read())
    except URLError:
        raise


class PagedHttpAdapter:
    """各 HTTP 注册表的分页和错误语义；子类仅提供 URL 与字段映射。"""

    platform = ""

    def __init__(
        self,
        *,
        transport: HttpTransport | None = None,
        timeout: float = 20,
        retries: int = 1,
        page_size: int = 50,
        evidence_root: EvidenceRoot | None = None,
    ) -> None:
        if timeout <= 0 or retries < 0 or page_size <= 0:
            raise ValueError("timeout、retries 和 page_size 必须为正当值")
        self.transport = transport or urllib_transport
        self.timeout = timeout
        self.retries = retries
        self.page_size = page_size
        self.evidence_root = evidence_root

    def search(self, job: QueryJob, watermark: "Watermark | None") -> SearchBatch:
        if job.platform != self.platform:
            raise ValueError(f"{self.platform} 适配器不能处理 {job.platform} 查询")
        candidates: list[SourceCandidate] = []
        requests: list[SourceRequestEvent] = []
        errors: list[SourceError] = []
        page = 1
        while True:
            url = self.search_url(job, watermark, page)
            response, attempts, error = self._get(url, job.query_id)
            if error is not None:
                requests.append(SourceRequestEvent(self.platform, job.query_id, url, page, error.status_code, attempts, None, None))
                errors.append(error)
                return self._batch(job, candidates, requests, errors)
            assert response is not None
            digest = sha256(response.body).hexdigest()
            try:
                payload = json.loads(response.body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                requests.append(SourceRequestEvent(self.platform, job.query_id, url, page, response.status, attempts, digest, response.body))
                errors.append(SourceError(self.platform, job.query_id, f"invalid-json: {exc}", response.status, url))
                return self._batch(job, candidates, requests, errors)
            raw_records = self.records_from_payload(payload)
            coverage_error = self.incremental_coverage_error(raw_records, watermark, job, url)
            records = self.filter_records(raw_records, watermark)
            last_page = self.is_last_page(payload, raw_records, page) or self.should_stop_incremental(raw_records, watermark)
            candidates.extend(self.normalize_record(record, job, digest) for record in records)
            try:
                evidence_path = self._save_page_evidence(page, digest, response.body)
            except (OSError, ValueError) as exc:
                requests.append(SourceRequestEvent(
                    self.platform, job.query_id, url, page, response.status, attempts, digest, response.body, False, None
                ))
                errors.append(SourceError(self.platform, job.query_id, f"evidence-write-error: {exc}", response.status, url))
                return self._batch(job, candidates, requests, errors)
            requests.append(SourceRequestEvent(
                self.platform, job.query_id, url, page, response.status, attempts, digest, response.body, last_page, evidence_path
            ))
            if coverage_error is not None:
                errors.append(coverage_error)
                return SearchBatch(
                    self.platform, job, "partial", tuple(sorted(candidates, key=_candidate_sort_key)), tuple(requests), tuple(errors)
                )
            if last_page:
                return SearchBatch(
                    self.platform, job, "complete", tuple(sorted(candidates, key=_candidate_sort_key)), tuple(requests), tuple(errors)
                )
            page += 1

    def latest_version(self, identity: str) -> VersionObservation:
        endpoint = self.identity_endpoint(identity)
        response, _, error = self._get(endpoint, "latest-version")
        observed_at = datetime.now(timezone.utc)
        if error is not None or response is None:
            return VersionObservation(self.platform, identity, None, observed_at, None, error)
        try:
            payload = json.loads(response.body.decode("utf-8"))
            records = self.records_from_payload(payload)
            record = records[0] if records else payload if isinstance(payload, Mapping) else {}
            return VersionObservation(self.platform, identity, self.version_from_record(record), observed_at, sha256(response.body).hexdigest())
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as exc:
            return VersionObservation(
                self.platform, identity, None, observed_at, sha256(response.body).hexdigest(),
                SourceError(self.platform, "latest-version", f"invalid-json: {exc}", response.status, endpoint),
            )

    def snapshot(self, identity: str, version: str | None, destination: Path) -> SnapshotResult:
        if self.evidence_root is None:
            return SnapshotResult(self.platform, identity, version, destination, None, SourceError(self.platform, "snapshot", "必须显式提供 EvidenceRoot", None, None))
        endpoint = self.version_endpoint(identity, version)
        response, _, error = self._get(endpoint, "snapshot")
        if error is not None or response is None:
            return SnapshotResult(self.platform, identity, version, destination, None, error)
        try:
            saved = self.evidence_root.write(destination, response.body)
        except (OSError, ValueError) as exc:
            return SnapshotResult(self.platform, identity, version, destination, None, SourceError(self.platform, "snapshot", str(exc), response.status, endpoint))
        return SnapshotResult(self.platform, identity, version, saved, sha256(response.body).hexdigest())

    def _get(self, url: str, query_id: str = "") -> tuple[HttpResponse | None, int, SourceError | None]:
        attempts = 0
        last_message = ""
        last_status: int | None = None
        for attempt in range(self.retries + 1):
            attempts += 1
            try:
                response = self.transport(url, self.timeout)
            except (OSError, URLError) as exc:
                last_message, last_status = str(exc), None
                if attempt < self.retries:
                    continue
                return None, attempts, SourceError(self.platform, query_id, f"network-error: {last_message}", None, url)
            if 200 <= response.status < 300:
                return response, attempts, None
            last_status = response.status
            last_message = _response_error_message(response.body)
            # Query syntax errors are deterministic; retrying them is both misleading and noisy.
            if response.status == 422 or not _retryable_status(response.status) or attempt == self.retries:
                return None, attempts, SourceError(self.platform, query_id, last_message or f"http-{response.status}", response.status, url)
        raise AssertionError("不可到达")

    def _save_page_evidence(self, page: int, digest: str, body: bytes) -> Path | None:
        if self.evidence_root is None:
            return None
        filename = f"{_safe_component(self.platform)}-page-{page:04d}-{digest}.json"
        return self.evidence_root.write(Path(filename), body)

    def _batch(
        self,
        job: QueryJob,
        candidates: list[SourceCandidate],
        requests: list[SourceRequestEvent],
        errors: list[SourceError],
    ) -> SearchBatch:
        status: SearchStatus = "partial" if candidates else "failed"
        return SearchBatch(self.platform, job, status, tuple(sorted(candidates, key=_candidate_sort_key)), tuple(requests), tuple(errors))

    def search_url(self, job: QueryJob, watermark: "Watermark | None", page: int) -> str:
        raise NotImplementedError

    def records_from_payload(self, payload: object) -> list[Mapping[str, object]]:
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, Mapping)]
        if isinstance(payload, Mapping):
            for key in ("items", "results", "data"):
                value = payload.get(key)
                if isinstance(value, list):
                    return [item for item in value if isinstance(item, Mapping)]
        return []

    def is_last_page(self, payload: object, records: list[Mapping[str, object]], page: int) -> bool:
        if isinstance(payload, Mapping):
            for key in ("has_next", "hasNext"):
                if key in payload:
                    return not bool(payload[key])
            if "next" in payload:
                return not bool(payload["next"])
        return len(records) < self.page_size

    def filter_records(self, records: list[Mapping[str, object]], watermark: "Watermark | None") -> list[Mapping[str, object]]:
        return records

    def should_stop_incremental(self, records: list[Mapping[str, object]], watermark: "Watermark | None") -> bool:
        return False

    def incremental_coverage_error(
        self, records: list[Mapping[str, object]], watermark: "Watermark | None", job: QueryJob, url: str
    ) -> SourceError | None:
        return None

    def identity_endpoint(self, identity: str) -> str:
        raise ValueError(f"{self.platform} 未定义 identity 到 API endpoint 的映射")

    def version_endpoint(self, identity: str, version: str | None) -> str:
        endpoint = self.identity_endpoint(identity)
        return endpoint if not version else f"{endpoint}?{urlencode({'version': version})}"

    def normalize_record(self, record: Mapping[str, object], job: QueryJob, evidence_sha: str) -> SourceCandidate:
        native_id = _first_text(record, "id", "slug", "name")
        display_name = _first_text(record, "name", "title", "id", "slug")
        discovery_url = _first_text(record, "url", "html_url", "web_url", "canonical_url")
        return SourceCandidate(
            self.platform, native_id, discovery_url, _optional_first(record, "canonical_source", "canonical_url", "repository"),
            self.version_from_record(record), display_name, _optional_first(record, "publisher", "author", "owner"),
            _optional_first(record, "updated_at", "updatedAt", "lastModified"), _popularity(record), job.query_id, evidence_sha,
        )

    def version_from_record(self, record: Mapping[str, object]) -> str | None:
        return _optional_first(record, "version", "tag", "sha", "lastModified", "updated_at", "updatedAt")


def doctor_smoke(adapter: PagedHttpAdapter, *, platform: str) -> DoctorSmokeResult:
    """以固定、无害查询仅探测一个端点页面。

    此函数刻意不调用 ``search``，因此不会解析候选、不追页，也不会写入证据或 Excel；
    命令层只有在 doctor --network 场景才应调用它。
    """
    if adapter.platform != platform:
        raise ValueError("doctor 探针平台必须与适配器一致")
    probe = QueryJob("Q-doctor-smoke", "doctor", platform, "doctor", "university skill")
    url = adapter.search_url(probe, None, 1)
    response, _, error = adapter._get(url, probe.query_id)
    if error is not None:
        return DoctorSmokeResult(platform, False, 1, error.status_code, error.message)
    assert response is not None
    return DoctorSmokeResult(platform, True, 1, response.status)


@dataclass(frozen=True)
class Watermark:
    platform: str
    query: str
    observed_at: datetime | None
    identifier: str | None
    note: str | None = None


@dataclass(frozen=True)
class WatermarkDecision:
    full_recheck: bool
    search_watermark: Watermark | None
    stored_watermark: Watermark | None


class SourceWatermarkStore:
    """将来源水位保存在唯一的 Excel ``来源水位`` 表，绝不另建业务存储。"""

    def __init__(self, ledger: LedgerStore) -> None:
        self.ledger = ledger

    def read(self, platform: str, query: str) -> Watermark | None:
        for row in self.ledger.rows("来源水位"):
            if row["来源平台"] == platform and row["检索词"] == query:
                return Watermark(platform, query, _as_utc(row["水位时间"]), _text_or_none(row["水位标识"]), _text_or_none(row["备注"]))
        return None

    def for_run(self, platform: str, query: str, now: datetime, *, full_recheck_interval_days: int) -> WatermarkDecision:
        if full_recheck_interval_days < 1:
            raise ValueError("full_recheck_interval_days 必须不小于 1")
        stored = self.read(platform, query)
        now_utc = _as_utc(now)
        assert now_utc is not None
        full = stored is None or stored.observed_at is None or now_utc - stored.observed_at >= timedelta(days=full_recheck_interval_days)
        return WatermarkDecision(full, None if full else stored, stored)

    def write(self, watermark: Watermark) -> None:
        worksheet = self.ledger.workbook["来源水位"]
        columns = self.ledger._resolve_columns("来源水位")
        values = {
            "来源平台": watermark.platform,
            "检索词": watermark.query,
            "水位时间": watermark.observed_at,
            "水位标识": watermark.identifier,
            "备注": watermark.note,
        }
        for row_number in range(2, worksheet.max_row + 1):
            if worksheet.cell(row_number, columns["来源平台"]).value == watermark.platform and worksheet.cell(row_number, columns["检索词"]).value == watermark.query:
                for name, value in values.items():
                    self.ledger._set_cell(worksheet.cell(row_number, columns[name]), value, name)
                self.ledger._resize_table("来源水位")
                return
        self.ledger.append_rows("来源水位", [values])

    def advance_if_complete(self, job: QueryJob, batch: SearchBatch, observed_at: datetime, identifier: str, note: str | None = None) -> bool:
        if batch.status != "complete":
            return False
        if job.platform != batch.platform:
            raise ValueError("水位平台必须与批次平台一致")
        self.write(Watermark(job.platform, job.query, _as_utc(observed_at), identifier, note))
        return True


def _retryable_status(status: int) -> bool:
    return status == 429 or 500 <= status < 600


def _response_error_message(body: bytes) -> str:
    try:
        parsed = json.loads(body.decode("utf-8"))
        if isinstance(parsed, Mapping):
            return _first_text(parsed, "message", "error", "detail")
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass
    return body.decode("utf-8", errors="replace").strip()


def _first_text(record: Mapping[str, object], *keys: str) -> str:
    value = _optional_first(record, *keys)
    return value or ""


def _optional_first(record: Mapping[str, object], *keys: str) -> str | None:
    for key in keys:
        value = record.get(key)
        if isinstance(value, Mapping):
            nested = _optional_first(value, "login", "name", "url", "html_url")
            if nested:
                return nested
        elif value is not None:
            text = str(value).strip()
            if text:
                return text
    return None


def _popularity(record: Mapping[str, object]) -> Mapping[str, int | float | str]:
    names = ("stars", "stargazers_count", "likes", "downloads", "downloadsCount", "upvotes")
    return {name: value for name in names if isinstance((value := record.get(name)), (int, float, str)) and not isinstance(value, bool)}


def _candidate_sort_key(candidate: SourceCandidate) -> tuple[str, str, str]:
    return (candidate.native_id.casefold(), candidate.display_name.casefold(), candidate.discovery_url)


def _safe_component(value: str) -> str:
    return "".join(character if character.isalnum() else "-" for character in value).strip("-").lower() or "source"


def _is_link_or_reparse(path: Path) -> bool:
    if path.is_symlink():
        return True
    attributes = getattr(path.stat(), "st_file_attributes", 0)
    return bool(attributes & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT on Windows


def _as_utc(value: object) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime):
        raise ValueError("水位时间必须是 datetime")
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _text_or_none(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
