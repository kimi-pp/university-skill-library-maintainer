"""Hugging Face Spaces 只读检索适配器。"""

from typing import Mapping
from urllib.parse import urlencode

from .base import PagedHttpAdapter, SourceCandidate, Watermark, _optional_first, _popularity
from ..queries import QueryJob


HUGGINGFACE = "https://huggingface.co/api/spaces"


class HuggingFaceAdapter(PagedHttpAdapter):
    platform = "Hugging Face Spaces"

    def search_url(self, job: QueryJob, watermark: Watermark | None, page: int) -> str:
        parameters = {"search": job.query, "limit": self.page_size, "offset": (page - 1) * self.page_size}
        if watermark and watermark.observed_at:
            parameters["lastModified"] = f">={watermark.observed_at.isoformat()}"
        return f"{HUGGINGFACE}?{urlencode(parameters)}"

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
