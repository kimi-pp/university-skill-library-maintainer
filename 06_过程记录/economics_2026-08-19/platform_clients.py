from __future__ import annotations

import hashlib
import json
import math
import subprocess
import urllib.parse
from typing import Any, Callable


SKILLHUB = "https://api.skillhub.cn/api/skills"
CLAWHUB_SEARCH = "https://clawhub.ai/api/v1/search"
GITHUB_SEARCH = "search/code"
HF_SPACES = "https://huggingface.co/api/spaces"


def _payload_bytes(response: Any, payload: Any) -> bytes:
    content = getattr(response, "content", None)
    if isinstance(content, bytes) and content:
        return content
    return json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")


def _page_event(page: int, url: str, items: list[dict[str, Any]], response_bytes: bytes,
                is_last_page: bool) -> dict[str, Any]:
    return {
        "page": page,
        "request_url": url,
        "item_count": len(items),
        "is_last_page": is_last_page,
        "response_sha256": hashlib.sha256(response_bytes).hexdigest(),
        "response_bytes": response_bytes,
        "retry_count": 0,
    }


def skillhub_search(query: str, session: Any, page_size: int = 100) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    ledger: list[dict[str, Any]] = []
    page = 1
    total_pages = 1
    while page <= total_pages:
        params = {"page": page, "pageSize": page_size, "keyword": query}
        url = SKILLHUB + "?" + urllib.parse.urlencode(params)
        response = session.get(url, timeout=60, headers={"Accept": "application/json"})
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise RuntimeError(f"SkillHub API error: {payload}")
        data = payload.get("data") or {}
        batch = list(data.get("skills") or [])
        total = int(data.get("total") or 0)
        total_pages = max(1, math.ceil(total / page_size))
        rows.extend(batch)
        response_bytes = _payload_bytes(response, payload)
        ledger.append(_page_event(page, url, batch, response_bytes, page >= total_pages))
        page += 1
    return rows, ledger


def clawhub_search(query: str, session: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    url = CLAWHUB_SEARCH + "?" + urllib.parse.urlencode({"q": query, "limit": 200})
    response = session.get(url, timeout=60, headers={"Accept": "application/json"})
    response.raise_for_status()
    payload = response.json()
    rows = list(payload.get("results") or [])
    response_bytes = _payload_bytes(response, payload)
    return rows, [_page_event(1, url, rows, response_bytes, True)]


def _default_github_runner(args: list[str]):
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def github_search(query: str, runner: Callable[[list[str]], Any] = _default_github_runner,
                  page_size: int = 100) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    encoded = urllib.parse.quote(query, safe="")
    rows: list[dict[str, Any]] = []
    ledger: list[dict[str, Any]] = []
    total = 0
    for page in range(1, 11):
        endpoint = f"{GITHUB_SEARCH}?q={encoded}&per_page={page_size}&page={page}"
        args = ["gh", "api", "--method", "GET", endpoint]
        run = runner(args)
        if run.returncode != 0:
            message = (getattr(run, "stderr", "") or "") + (getattr(run, "stdout", "") or "")
            raise RuntimeError(message.strip() or f"GitHub CLI failed with code {run.returncode}")
        response_bytes = (run.stdout or "").encode("utf-8")
        payload = json.loads(run.stdout)
        if page == 1:
            total = int(payload.get("total_count") or 0)
        batch = list(payload.get("items") or [])
        rows.extend(batch)
        last = not batch or len(rows) >= min(total, 1000)
        ledger.append(_page_event(page, "https://api.github.com/" + endpoint, batch, response_bytes, last))
        if last:
            break
    return rows, ledger


def huggingface_search(query: str, session: Any,
                       page_size: int = 100) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    ledger: list[dict[str, Any]] = []
    page = 1
    while True:
        params = {"search": query, "limit": page_size, "skip": (page - 1) * page_size, "full": "true"}
        url = HF_SPACES + "?" + urllib.parse.urlencode(params)
        response = session.get(url, timeout=60, headers={"Accept": "application/json"})
        response.raise_for_status()
        payload = response.json()
        batch = list(payload if isinstance(payload, list) else payload.get("items") or [])
        rows.extend(batch)
        last = len(batch) < page_size
        response_bytes = _payload_bytes(response, payload)
        ledger.append(_page_event(page, url, batch, response_bytes, last))
        if last:
            break
        page += 1
    return rows, ledger
