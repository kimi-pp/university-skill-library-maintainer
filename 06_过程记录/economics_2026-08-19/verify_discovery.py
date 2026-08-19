from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def verify_discovery(matrix: dict[str, Any], output_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    ledger_path = output_root / "query_ledger.jsonl"
    candidate_path = output_root / "raw_candidates.jsonl"
    ledger = read_jsonl(ledger_path)
    jobs = matrix["jobs"]
    job_by_id = {row["query_id"]: row for row in jobs}
    if len(job_by_id) != len(jobs):
        errors.append("查询矩阵存在重复query_id")

    terminal_events = [row for row in ledger if row.get("event_type") == "terminal"]
    page_events = [row for row in ledger if row.get("event_type") == "page"]
    latest: dict[str, dict[str, Any]] = {}
    for row in terminal_events:
        latest[row["query_id"]] = row

    expected_ids = set(job_by_id)
    actual_ids = set(latest)
    for query_id in sorted(expected_ids - actual_ids):
        errors.append(f"缺少查询终态: {query_id}")
    for query_id in sorted(actual_ids - expected_ids):
        errors.append(f"存在矩阵外查询终态: {query_id}")

    pages_by_query: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in page_events:
        pages_by_query[row["query_id"]].append(row)
        path_value = row.get("response_path")
        if not path_value:
            errors.append(f"响应路径缺失: {row.get('query_id')} page={row.get('page')}")
            continue
        response_path = output_root / path_value
        if not response_path.is_file():
            errors.append(f"响应文件缺失: {path_value}")
            continue
        actual_sha = hashlib.sha256(response_path.read_bytes()).hexdigest()
        if actual_sha != row.get("response_sha256"):
            errors.append(f"响应SHA不匹配: {path_value}")

    for query_id in sorted(expected_ids & actual_ids):
        terminal = latest[query_id]
        if not (terminal.get("status") == "success" and terminal.get("complete") is True):
            errors.append(f"查询未成功闭合: {query_id} status={terminal.get('status')}")
            continue
        pages = pages_by_query.get(query_id, [])
        if len(pages) != int(terminal.get("page_count") or 0):
            errors.append(f"页数与终态不一致: {query_id}")
        if pages and sum(1 for row in pages if row.get("is_last_page") is True) != 1:
            errors.append(f"末页标记异常: {query_id}")

    successful_by_major: dict[str, set[str]] = defaultdict(set)
    for query_id, terminal in latest.items():
        if terminal.get("status") == "success" and terminal.get("complete") is True:
            job = job_by_id.get(query_id)
            if job:
                successful_by_major[job["major_code"]].add(job["platform"])
    required_platforms = set(matrix.get("platforms") or {job["platform"] for job in jobs})
    for major_code in sorted({job["major_code"] for job in jobs}):
        if successful_by_major.get(major_code, set()) != required_platforms:
            errors.append(f"专业四平台覆盖不完整: {major_code}")

    candidates = read_jsonl(candidate_path)
    historical_failed = sum(1 for row in terminal_events if row.get("status") == "failed")
    latest_success = sum(
        1 for row in latest.values() if row.get("status") == "success" and row.get("complete") is True
    )
    return {
        "schema_version": "1.0",
        "matrix_job_count": len(jobs),
        "terminal_event_count": len(terminal_events),
        "latest_terminal_count": len(latest),
        "latest_success_count": latest_success,
        "historical_failed_attempts": historical_failed,
        "retried_query_count": sum(1 for count in Counter(row["query_id"] for row in terminal_events).values() if count > 1),
        "page_event_count": len(page_events),
        "raw_candidate_record_count": len(candidates),
        "platform_latest_success_counts": dict(
            sorted(
                Counter(
                    job_by_id[query_id]["platform"]
                    for query_id, row in latest.items()
                    if query_id in job_by_id and row.get("status") == "success" and row.get("complete") is True
                ).items()
            )
        ),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="核验经济学四社区发现台账")
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
    result = verify_discovery(matrix, args.output)
    args.manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
