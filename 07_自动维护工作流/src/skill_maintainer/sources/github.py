"""GitHub 只读检索适配器；生产路径只通过 ``gh api`` 的参数列表调用。"""

from __future__ import annotations

from dataclasses import replace
import subprocess
from typing import Callable, Mapping
from urllib.parse import urlencode

from .base import HttpResponse, PagedHttpAdapter, SearchBatch, SourceCandidate, SourceError, Watermark, _optional_first, _popularity
from ..queries import QueryJob


GITHUB_API = "https://api.github.com"
GITHUB_SEARCH_CEILING = 1000
GitHubCommandRunner = Callable[[list[str]], object]


class GitHubAdapter(PagedHttpAdapter):
    platform = "GitHub"

    def __init__(self, *, command_runner: GitHubCommandRunner | None = None, **kwargs) -> None:
        transport_given = kwargs.get("transport") is not None
        super().__init__(**kwargs)
        self.command_runner = command_runner
        self._use_gh = command_runner is not None or not transport_given

    def search_url(self, job: QueryJob, watermark: Watermark | None, page: int) -> str:
        query = job.query
        if watermark and watermark.observed_at:
            query = f"{query} pushed:>={watermark.observed_at.date().isoformat()}"
        return f"{GITHUB_API}/search/repositories?{urlencode({'q': query, 'per_page': self.page_size, 'page': page})}"

    def search(self, job: QueryJob, watermark: Watermark | None) -> SearchBatch:
        batch = super().search(job, watermark)
        if batch.status == "failed" or not batch.requests:
            return batch
        first_payload = self._payload_for_event(batch.requests[0])
        total = first_payload.get("total_count") if isinstance(first_payload, Mapping) else None
        full_page_limit = (GITHUB_SEARCH_CEILING + self.page_size - 1) // self.page_size
        at_ceiling = len(batch.requests) >= full_page_limit and (not isinstance(total, int) or total > GITHUB_SEARCH_CEILING)
        if at_ceiling:
            error = SourceError(self.platform, job.query_id, "GitHub search result ceiling: only the first 1000 results are accessible", None, batch.requests[-1].url)
            return replace(batch, status="partial", errors=batch.errors + (error,))
        return batch

    def is_last_page(self, payload: object, records: list[Mapping[str, object]], page: int) -> bool:
        """GitHub 给出总数时，以其公开的前 1,000 条上限确定末页。"""
        if isinstance(payload, Mapping) and isinstance(payload.get("total_count"), int):
            visible_total = min(payload["total_count"], GITHUB_SEARCH_CEILING)
            expected_pages = max(1, (visible_total + self.page_size - 1) // self.page_size)
            return page >= expected_pages
        return super().is_last_page(payload, records, page)

    def _get(self, url: str):
        if not self._use_gh:
            return super()._get(url)
        endpoint = url.removeprefix(GITHUB_API)
        attempts = 0
        runner = self.command_runner or _run_gh
        for attempt in range(self.retries + 1):
            attempts += 1
            try:
                outcome = runner(["gh", "api", "--method", "GET", endpoint])
                code = int(getattr(outcome, "returncode", 0))
                raw = getattr(outcome, "stdout", outcome if isinstance(outcome, (str, bytes)) else b"")
                body = raw.encode("utf-8") if isinstance(raw, str) else bytes(raw)
            except (OSError, subprocess.SubprocessError) as exc:
                if attempt < self.retries:
                    continue
                return None, attempts, SourceError(self.platform, "", f"network-error: {exc}", None, url)
            if code == 0:
                return HttpResponse(url, 200, body), attempts, None
            if attempt < self.retries:
                continue
            return None, attempts, SourceError(self.platform, "", "gh api failed", None, url)
        raise AssertionError("不可到达")

    def normalize_record(self, record: Mapping[str, object], job: QueryJob, evidence_sha: str) -> SourceCandidate:
        native_id = _optional_first(record, "id", "full_name") or ""
        name = _optional_first(record, "full_name", "name") or native_id
        return SourceCandidate(
            self.platform,
            native_id,
            _optional_first(record, "html_url", "url") or "",
            _optional_first(record, "homepage", "clone_url", "html_url"),
            self.version_from_record(record),
            name,
            _optional_first(record, "owner"),
            _optional_first(record, "pushed_at", "updated_at"),
            _popularity(record),
            job.query_id,
            evidence_sha,
        )

    @staticmethod
    def _payload_for_event(event) -> object:
        if event.response_bytes is None:
            return {}
        try:
            import json
            return json.loads(event.response_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}


def _run_gh(arguments: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(arguments, check=False, capture_output=True, timeout=20)
