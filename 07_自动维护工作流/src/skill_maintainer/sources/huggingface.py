"""Hugging Face Spaces 只读检索适配器。"""

from datetime import datetime, timezone
from typing import Mapping
from urllib.parse import quote, urlencode, urlparse

from .base import PagedHttpAdapter, SourceCandidate, SourceError, Watermark, _optional_first, _popularity
from ..queries import QueryJob


HUGGINGFACE = "https://huggingface.co/api/spaces"


class HuggingFaceAdapter(PagedHttpAdapter):
    platform = "Hugging Face Spaces"

    def search_url(self, job: QueryJob, watermark: Watermark | None, page: int) -> str:
        parameters = {
            "search": job.query,
            "limit": self.page_size,
            "offset": (page - 1) * self.page_size,
            # The public /api/spaces endpoint names this field in its wire format.
            # ``last_modified`` / ``desc`` are the client-library semantics, while
            # ``lastModified`` / ``-1`` is the currently accepted REST spelling.
            "sort": "lastModified",
            "direction": "-1",
        }
        return f"{HUGGINGFACE}?{urlencode(parameters)}"

    def identity_endpoint(self, identity: str) -> str:
        parsed = urlparse(identity)
        native_id = identity.strip("/")
        if parsed.scheme:
            if parsed.netloc.casefold() != "huggingface.co":
                raise ValueError("Hugging Face identity 必须是原生 ID 或 huggingface.co Spaces 地址")
            parts = parsed.path.strip("/").split("/")
            if len(parts) >= 3 and parts[0] in {"spaces", "api"}:
                native_id = "/".join(parts[2:] if parts[0] == "api" else parts[1:])
            else:
                raise ValueError("Hugging Face discovery URL 必须指向 Spaces")
        if len(native_id.split("/")) != 2:
            raise ValueError("Hugging Face identity 必须是 owner/space")
        return f"{HUGGINGFACE}/{quote(native_id, safe='/')}"

    def filter_records(self, records: list[Mapping[str, object]], watermark: Watermark | None) -> list[Mapping[str, object]]:
        if watermark is None or watermark.observed_at is None:
            return records
        return [record for record in records if (updated := _updated_at(record)) is not None and updated > watermark.observed_at]

    def should_stop_incremental(self, records: list[Mapping[str, object]], watermark: Watermark | None) -> bool:
        if watermark is None or watermark.observed_at is None or not records:
            return False
        dates = [_updated_at(record) for record in records]
        return all(value is not None for value in dates) and any(value <= watermark.observed_at for value in dates if value is not None)

    def incremental_coverage_error(self, records, watermark, job, url):
        if watermark is None or watermark.observed_at is None:
            return None
        if any(_updated_at(record) is None for record in records):
            return SourceError(self.platform, job.query_id, "Hugging Face record lacks a parseable lastModified timestamp", None, url)
        return None

    def normalize_record(self, record: Mapping[str, object], job: QueryJob, evidence_sha: str) -> SourceCandidate:
        native_id = _optional_first(record, "id") or ""
        return SourceCandidate(
            self.platform,
            native_id,
            f"https://huggingface.co/spaces/{native_id}" if native_id else "",
            _optional_first(record, "repository", "url"),
            self.version_from_record(record),
            native_id,
            _optional_first(record, "author"),
            _optional_first(record, "lastModified", "updated_at"),
            _popularity(record),
            job.query_id,
            evidence_sha,
        )


def _updated_at(record: Mapping[str, object]) -> datetime | None:
    value = _optional_first(record, "lastModified", "updated_at")
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)
