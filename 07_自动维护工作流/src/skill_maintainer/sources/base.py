"""来源适配器共用的只读传输、证据和水位契约。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Callable, Literal, Mapping, Protocol
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


def write_immutable_bytes(destination: Path, content: bytes) -> Path:
    """只允许创建或复用内容相同的证据快照，避免静默覆盖。"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if destination.read_bytes() != content:
            raise ValueError(f"证据快照已存在且内容不同：{destination}")
        return destination
    destination.write_bytes(content)
    return destination


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
        evidence_directory: Path | None = None,
    ) -> None:
        if timeout <= 0 or retries < 0 or page_size <= 0:
            raise ValueError("timeout、retries 和 page_size 必须为正当值")
        self.transport = transport or urllib_transport
        self.timeout = timeout
        self.retries = retries
        self.page_size = page_size
        self.evidence_directory = evidence_directory

    def search(self, job: QueryJob, watermark: "Watermark | None") -> SearchBatch:
        if job.platform != self.platform:
            raise ValueError(f"{self.platform} 适配器不能处理 {job.platform} 查询")
        candidates: list[SourceCandidate] = []
        requests: list[SourceRequestEvent] = []
        errors: list[SourceError] = []
        page = 1
        while True:
            url = self.search_url(job, watermark, page)
            response, attempts, error = self._get(url)
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
            records = self.records_from_payload(payload)
            last_page = self.is_last_page(payload, records, page)
            evidence_path = self._save_page_evidence(page, digest, response.body)
            requests.append(SourceRequestEvent(
                self.platform, job.query_id, url, page, response.status, attempts, digest, response.body, last_page, evidence_path
            ))
            candidates.extend(self.normalize_record(record, job, digest) for record in records)
            if last_page:
                return SearchBatch(
                    self.platform, job, "complete", tuple(sorted(candidates, key=_candidate_sort_key)), tuple(requests), tuple(errors)
                )
            page += 1

    def latest_version(self, identity: str) -> VersionObservation:
        response, _, error = self._get(identity)
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
                SourceError(self.platform, "version", f"invalid-json: {exc}", response.status, identity),
            )

    def snapshot(self, identity: str, version: str | None, destination: Path) -> SnapshotResult:
        response, _, error = self._get(identity)
        if error is not None or response is None:
            return SnapshotResult(self.platform, identity, version, destination, None, error)
        try:
            write_immutable_bytes(destination, response.body)
        except OSError | ValueError as exc:
            return SnapshotResult(self.platform, identity, version, destination, None, SourceError(self.platform, "snapshot", str(exc), response.status, identity))
        return SnapshotResult(self.platform, identity, version, destination, sha256(response.body).hexdigest())

    def _get(self, url: str) -> tuple[HttpResponse | None, int, SourceError | None]:
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
                return None, attempts, SourceError(self.platform, "", f"network-error: {last_message}", None, url)
            if 200 <= response.status < 300:
                return response, attempts, None
            last_status = response.status
            last_message = _response_error_message(response.body)
            # Query syntax errors are deterministic; retrying them is both misleading and noisy.
            if response.status == 422 or not _retryable_status(response.status) or attempt == self.retries:
                return None, attempts, SourceError(self.platform, "", last_message or f"http-{response.status}", response.status, url)
        raise AssertionError("不可到达")

    def _save_page_evidence(self, page: int, digest: str, body: bytes) -> Path | None:
        if self.evidence_directory is None:
            return None
        filename = f"{_safe_component(self.platform)}-page-{page:04d}-{digest}.json"
        return write_immutable_bytes(self.evidence_directory / filename, body)

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
    response, _, error = adapter._get(url)
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
