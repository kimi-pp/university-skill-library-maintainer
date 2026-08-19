from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent


def _load_platform_clients():
    module_path = HERE / "platform_clients.py"
    spec = importlib.util.spec_from_file_location("economics_platform_clients_runtime", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def completed_query_ids(ledger_path: Path) -> set[str]:
    return {
        row["query_id"]
        for row in read_jsonl(ledger_path)
        if row.get("event_type") == "terminal"
        and row.get("status") == "success"
        and row.get("complete") is True
    }


def _candidate_native_id(platform: str, item: dict[str, Any]) -> str:
    if platform == "SkillHub":
        namespace = item.get("namespace") or {}
        return str(item.get("id") or item.get("slug") or namespace.get("canonicalName") or "")
    if platform == "ClawHub":
        return str(item.get("slug") or item.get("id") or "")
    if platform == "GitHub":
        repo = item.get("repository") or {}
        return f"{repo.get('full_name') or repo.get('name') or ''}:{item.get('path') or ''}"
    return str(item.get("id") or item.get("_id") or item.get("author") or "")


def _candidate_url(platform: str, item: dict[str, Any]) -> str | None:
    if platform == "SkillHub":
        return item.get("url") or item.get("homepage")
    if platform == "ClawHub":
        return item.get("url") or (f"https://clawhub.ai/skills/{item.get('slug')}" if item.get("slug") else None)
    if platform == "GitHub":
        return item.get("html_url")
    identifier = item.get("id") or item.get("_id")
    return f"https://huggingface.co/spaces/{identifier}" if identifier else None


def _save_pages(output_root: Path, job: dict[str, Any], page_events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    saved: list[dict[str, Any]] = []
    page_root = output_root / "raw_responses" / job["query_id"]
    page_root.mkdir(parents=True, exist_ok=True)
    for event in page_events:
        serializable = dict(event)
        response_bytes = serializable.pop("response_bytes", b"")
        if not isinstance(response_bytes, bytes):
            response_bytes = bytes(response_bytes)
        page_path = page_root / f"page_{int(event['page']):05d}.json"
        page_path.write_bytes(response_bytes)
        response_sha = hashlib.sha256(response_bytes).hexdigest()
        serializable.update(
            {
                "event_type": "page",
                "query_id": job["query_id"],
                "major_code": job["major_code"],
                "platform": job["platform"],
                "round": job["round"],
                "status": "success",
                "response_sha256": response_sha,
                "response_path": page_path.relative_to(output_root).as_posix(),
                "captured_at": utc_now(),
            }
        )
        saved.append(serializable)
    return saved


def run_discovery(matrix: dict[str, Any], output_root: Path,
                  clients: dict[str, Callable[[str], tuple[list[dict[str, Any]], list[dict[str, Any]]]]]
                  ) -> dict[str, int]:
    output_root.mkdir(parents=True, exist_ok=True)
    ledger_path = output_root / "query_ledger.jsonl"
    candidates_path = output_root / "raw_candidates.jsonl"
    complete = completed_query_ids(ledger_path)
    network_calls = 0
    skipped_jobs = 0
    failed_jobs = 0
    successful_jobs = 0

    for job in matrix["jobs"]:
        query_id = job["query_id"]
        if query_id in complete:
            skipped_jobs += 1
            continue
        client = clients.get(job["platform"])
        if client is None:
            raise RuntimeError(f"missing client for {job['platform']}")
        network_calls += 1
        started_at = utc_now()
        try:
            items, page_events = client(job["query"])
            page_rows = _save_pages(output_root, job, page_events)
            append_jsonl(ledger_path, page_rows)
            candidates = []
            for rank, item in enumerate(items, start=1):
                candidates.append(
                    {
                        "query_id": query_id,
                        "major_code": job["major_code"],
                        "major_name": job["major_name"],
                        "class_code": job["class_code"],
                        "class_name": job["class_name"],
                        "platform": job["platform"],
                        "round": job["round"],
                        "query": job["query"],
                        "rank": rank,
                        "candidate_native_id": _candidate_native_id(job["platform"], item),
                        "candidate_url": _candidate_url(job["platform"], item),
                        "raw": item,
                        "captured_at": utc_now(),
                    }
                )
            append_jsonl(candidates_path, candidates)
            append_jsonl(
                ledger_path,
                [
                    {
                        "event_type": "terminal",
                        "query_id": query_id,
                        "major_code": job["major_code"],
                        "platform": job["platform"],
                        "round": job["round"],
                        "query": job["query"],
                        "status": "success",
                        "complete": True,
                        "result_count": len(items),
                        "page_count": len(page_events),
                        "started_at": started_at,
                        "finished_at": utc_now(),
                        "error": None,
                    }
                ],
            )
            successful_jobs += 1
        except Exception as exc:
            append_jsonl(
                ledger_path,
                [
                    {
                        "event_type": "terminal",
                        "query_id": query_id,
                        "major_code": job["major_code"],
                        "platform": job["platform"],
                        "round": job["round"],
                        "query": job["query"],
                        "status": "failed",
                        "complete": False,
                        "result_count": None,
                        "page_count": None,
                        "started_at": started_at,
                        "finished_at": utc_now(),
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                ],
            )
            failed_jobs += 1
    return {
        "network_calls": network_calls,
        "successful_jobs": successful_jobs,
        "failed_jobs": failed_jobs,
        "skipped_jobs": skipped_jobs,
    }


def production_clients() -> dict[str, Callable[[str], tuple[list[dict[str, Any]], list[dict[str, Any]]]]]:
    import requests

    platform = _load_platform_clients()
    session = requests.Session()
    session.headers.update({"User-Agent": "University-Skills-Research/1.0 read-only discovery"})

    last_github_call = [0.0]

    def gh_runner(args: list[str]):
        wait_seconds = 6.5 - (time.monotonic() - last_github_call[0])
        if wait_seconds > 0:
            time.sleep(wait_seconds)
        run = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        last_github_call[0] = time.monotonic()
        return run

    return {
        "SkillHub": lambda query: platform.skillhub_search(query, session),
        "ClawHub": lambda query: platform.clawhub_search(query, session),
        "GitHub": lambda query: platform.github_search(query, gh_runner),
        "Hugging Face Spaces": lambda query: platform.huggingface_search(query, session),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="执行经济学门类四社区只读候选发现")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--platform", action="append", choices=["SkillHub", "ClawHub", "GitHub", "Hugging Face Spaces"])
    args = parser.parse_args()
    matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
    if args.platform:
        selected = set(args.platform)
        matrix = {**matrix, "jobs": [job for job in matrix["jobs"] if job["platform"] in selected]}
    summary = run_discovery(matrix, args.output, production_clients())
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 1 if summary["failed_jobs"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
