"""GitHub 只读检索适配器；生产路径只通过 ``gh api`` 的参数列表调用。"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import threading
from typing import Callable, Mapping
from urllib.parse import quote, urlencode, urlparse

from .base import MAX_ARCHIVE_BYTES, MAX_HTTP_RESPONSE_BYTES, HttpResponse, PagedHttpAdapter, SearchBatch, SnapshotResult, SourceCandidate, SourceError, SourceRequestEvent, VersionObservation, Watermark, _optional_first, _popularity
from ..queries import QueryJob


GITHUB_API = "https://api.github.com"
GITHUB_SEARCH_CEILING = 1000
GitHubCommandRunner = Callable[[list[str]], object]
_COMMIT_SHA_RE = re.compile(r"[0-9a-fA-F]{40}(?:[0-9a-fA-F]{24})?\Z")
_MAX_GH_STDERR_BYTES = 1024 * 1024


@dataclass(frozen=True)
class _GhOutcome:
    returncode: int
    stdout: bytes
    stderr: bytes
    exceeded: bool = False


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

    def _get(self, url: str, query_id: str = ""):
        if not self._use_gh:
            return super()._get(url, query_id)
        endpoint = url.removeprefix(GITHUB_API)
        attempts = 0
        runner = self.command_runner or _run_gh
        max_bytes = MAX_ARCHIVE_BYTES if "/zipball/" in endpoint else MAX_HTTP_RESPONSE_BYTES
        for attempt in range(self.retries + 1):
            attempts += 1
            try:
                outcome = (
                    _run_gh(["gh", "api", "--method", "GET", endpoint], max_bytes=max_bytes)
                    if self.command_runner is None
                    else runner(["gh", "api", "--method", "GET", endpoint])
                )
                code = int(getattr(outcome, "returncode", 0))
                raw = getattr(outcome, "stdout", outcome if isinstance(outcome, (str, bytes)) else b"")
                body = raw.encode("utf-8") if isinstance(raw, str) else bytes(raw)
                error_raw = getattr(outcome, "stderr", b"")
                error_body = error_raw.encode("utf-8") if isinstance(error_raw, str) else bytes(error_raw)
            except (OSError, subprocess.SubprocessError) as exc:
                if attempt < self.retries:
                    continue
                return None, attempts, SourceError(self.platform, query_id, f"network-error: {exc}", None, url)
            exceeded = bool(getattr(outcome, "exceeded", False)) or len(body) > max_bytes
            if exceeded:
                message = "archive-compressed-byte-limit" if max_bytes == MAX_ARCHIVE_BYTES else "http-response-byte-limit"
                return None, attempts, SourceError(self.platform, query_id, message, None, url)
            if code == 0:
                return HttpResponse(url, 200, body), attempts, None
            status, message = _gh_error(error_body or body)
            if status == 422:
                return None, attempts, SourceError(self.platform, query_id, message, 422, url)
            if attempt < self.retries:
                continue
            return None, attempts, SourceError(self.platform, query_id, message, status, url)
        raise AssertionError("不可到达")

    def identity_endpoint(self, identity: str) -> str:
        owner_repo = _github_identity(identity)
        return f"{GITHUB_API}/repos/{owner_repo}"

    def latest_version(self, identity: str) -> VersionObservation:
        audit_id = f"latest-version:{identity}"
        metadata_endpoint = self.identity_endpoint(identity)
        metadata, attempts, error = self._get(metadata_endpoint, "latest-version")
        observed_at = datetime.now(timezone.utc)
        if error is not None or metadata is None:
            event = SourceRequestEvent(self.platform, audit_id, metadata_endpoint, 1, getattr(error, "status_code", None), attempts, None, None)
            return VersionObservation(self.platform, identity, None, observed_at, None, error, (event,))
        metadata_event = self._postcheck_event(f"{audit_id}:repository", metadata_endpoint, metadata, attempts, ".json")
        try:
            record = json.loads(metadata.body.decode("utf-8"))
            if not isinstance(record, Mapping):
                raise ValueError("repository metadata must be an object")
            default_branch = _optional_first(record, "default_branch")
            if not default_branch:
                raise ValueError("repository metadata lacks default_branch")
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            return VersionObservation(self.platform, identity, None, observed_at, sha256(metadata.body).hexdigest(), SourceError(self.platform, "latest-version", f"invalid-json: {exc}", metadata.status, metadata_endpoint), (metadata_event,), tuple(filter(None, (metadata_event.evidence_path,))))
        commit_endpoint = f"{metadata_endpoint}/commits/{quote(default_branch, safe='')}"
        commit, commit_attempts, error = self._get(commit_endpoint, "latest-version")
        if error is not None or commit is None:
            failed = SourceRequestEvent(self.platform, audit_id, commit_endpoint, 1, getattr(error, "status_code", None), commit_attempts, None, None)
            return VersionObservation(self.platform, identity, None, observed_at, sha256(metadata.body).hexdigest(), error, (metadata_event, failed), tuple(filter(None, (metadata_event.evidence_path,))))
        commit_event = self._postcheck_event(f"{audit_id}:commit", commit_endpoint, commit, commit_attempts, ".json")
        try:
            commit_record = json.loads(commit.body.decode("utf-8"))
            if not isinstance(commit_record, Mapping):
                raise ValueError("commit metadata must be an object")
            version = _optional_first(commit_record, "sha")
            if not version:
                raise ValueError("commit metadata lacks sha")
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            return VersionObservation(self.platform, identity, None, observed_at, sha256(commit.body).hexdigest(), SourceError(self.platform, "latest-version", f"invalid-json: {exc}", commit.status, commit_endpoint), (metadata_event, commit_event), tuple(path for path in (metadata_event.evidence_path, commit_event.evidence_path) if path))
        return VersionObservation(self.platform, identity, version, observed_at, sha256(commit.body).hexdigest(), None, (metadata_event, commit_event), tuple(path for path in (metadata_event.evidence_path, commit_event.evidence_path) if path))

    def snapshot(self, identity: str, version: str | None, destination: Path) -> SnapshotResult:
        audit_id = f"snapshot:{identity}"
        if self.evidence_root is None:
            return SnapshotResult(self.platform, identity, version, destination, None, SourceError(self.platform, "snapshot", "必须显式提供 EvidenceRoot"))
        if not isinstance(version, str) or not _COMMIT_SHA_RE.fullmatch(version):
            return SnapshotResult(self.platform, identity, version, destination, None, SourceError(self.platform, "snapshot", "GitHub 快照必须使用固定 commit SHA"))
        endpoint = f"{self.identity_endpoint(identity)}/zipball/{quote(version, safe='')}"
        response, attempts, error = self._get(endpoint, "snapshot")
        if error is not None or response is None:
            event = SourceRequestEvent(self.platform, audit_id, endpoint, 1, getattr(error, "status_code", None), attempts, None, None)
            return SnapshotResult(self.platform, identity, version, destination, None, error, (event,))
        digest = sha256(response.body).hexdigest()
        if len(response.body) > MAX_ARCHIVE_BYTES:
            event = SourceRequestEvent(self.platform, audit_id, endpoint, 1, response.status, attempts, digest, None)
            return SnapshotResult(self.platform, identity, version, destination, None, SourceError(self.platform, "snapshot", "archive-compressed-byte-limit", response.status, endpoint), (event,))
        try:
            saved = self.evidence_root.write(destination, response.body)
        except (OSError, ValueError) as exc:
            event = SourceRequestEvent(self.platform, audit_id, endpoint, 1, response.status, attempts, digest, None)
            return SnapshotResult(self.platform, identity, version, destination, None, SourceError(self.platform, "snapshot", str(exc), response.status, endpoint), (event,))
        event = SourceRequestEvent(self.platform, audit_id, endpoint, 1, response.status, attempts, digest, None, True, saved, True)
        return SnapshotResult(self.platform, identity, version, saved, digest, None, (event,), (saved,))

    def normalize_record(self, record: Mapping[str, object], job: QueryJob, evidence_sha: str) -> SourceCandidate:
        native_id = _optional_first(record, "full_name") or ""
        name = _optional_first(record, "full_name", "name") or native_id
        popularity = dict(_popularity(record))
        repository_id = record.get("id")
        if isinstance(repository_id, int) and not isinstance(repository_id, bool):
            popularity["repository_id"] = repository_id
        return SourceCandidate(
            self.platform,
            native_id,
            _optional_first(record, "html_url", "url") or "",
            _optional_first(record, "homepage", "clone_url", "html_url"),
            self.version_from_record(record),
            name,
            _optional_first(record, "owner"),
            _optional_first(record, "pushed_at", "updated_at"),
            popularity,
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


def _run_gh(arguments: list[str], *, max_bytes: int = MAX_HTTP_RESPONSE_BYTES) -> _GhOutcome:
    """Drain gh through bounded streams; stdout is never accumulated without a hard cap."""
    if max_bytes <= 0:
        raise ValueError("gh response byte limit must be positive")
    with tempfile.TemporaryDirectory(prefix="skill-maintainer-gh-") as temporary:
        stdout_path = Path(temporary) / "stdout.bin"
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
        process = subprocess.Popen(
            arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
            creationflags=creationflags,
        )
        exceeded = threading.Event()
        stderr_buffer = bytearray()

        def read_stdout() -> None:
            assert process.stdout is not None
            total = 0
            with stdout_path.open("xb") as handle:
                while True:
                    chunk = process.stdout.read(64 * 1024)
                    if not chunk:
                        break
                    remaining = max(0, max_bytes + 1 - total)
                    if remaining:
                        handle.write(chunk[:remaining])
                    total += len(chunk)
                    if total > max_bytes and not exceeded.is_set():
                        exceeded.set()
                        try:
                            process.terminate()
                        except OSError:
                            pass

        def read_stderr() -> None:
            assert process.stderr is not None
            while True:
                chunk = process.stderr.read(64 * 1024)
                if not chunk:
                    break
                remaining = max(0, _MAX_GH_STDERR_BYTES - len(stderr_buffer))
                if remaining:
                    stderr_buffer.extend(chunk[:remaining])

        stdout_thread = threading.Thread(target=read_stdout, daemon=True)
        stderr_thread = threading.Thread(target=read_stderr, daemon=True)
        stdout_thread.start()
        stderr_thread.start()
        timed_out = False
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            process.wait()
        stdout_thread.join()
        stderr_thread.join()
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
        body = stdout_path.read_bytes() if stdout_path.is_file() else b""
        if timed_out:
            raise subprocess.TimeoutExpired(arguments, 20, output=body, stderr=bytes(stderr_buffer))
        return _GhOutcome(int(process.returncode), body, bytes(stderr_buffer), exceeded.is_set())


def _gh_error(body: bytes) -> tuple[int | None, str]:
    try:
        value = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, body.decode("utf-8", errors="replace").strip() or "gh api failed"
    if isinstance(value, Mapping):
        status = value.get("status")
        return status if isinstance(status, int) else None, _optional_first(value, "message", "error") or "gh api failed"
    return None, "gh api failed"


def _github_identity(identity: str) -> str:
    parsed = urlparse(identity)
    if parsed.scheme:
        if parsed.netloc.casefold() != "github.com":
            raise ValueError("GitHub identity 必须是 owner/repo 或 github.com 仓库地址")
        value = parsed.path.strip("/")
    else:
        value = identity.strip("/")
    parts = value.split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("GitHub identity 必须是 owner/repo")
    return "/".join(quote(part, safe="") for part in parts)
