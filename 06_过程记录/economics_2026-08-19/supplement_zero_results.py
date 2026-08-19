from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


FOUR_PLATFORMS = ("SkillHub", "ClawHub", "GitHub", "Hugging Face Spaces")
PLATFORM_CODES = {"SkillHub": "SH", "ClawHub": "CH", "GitHub": "GH", "Hugging Face Spaces": "HF"}


def zero_formal_major_codes(profiles: Iterable[dict[str, Any]], formal: Iterable[dict[str, Any]]) -> list[str]:
    covered = {code for row in formal for code in row.get("matched_major_codes", [])}
    return [profile["major_code"] for profile in profiles if profile["major_code"] not in covered]


def _focus_terms(profile: dict[str, Any]) -> list[str]:
    search = profile.get("search_terms", {})
    english = [str(value).strip() for value in search.get("en", []) if str(value).strip()]
    chinese = [str(value).strip() for value in search.get("zh", []) if str(value).strip()]
    tasks = [str(value).strip() for value in profile.get("typical_tasks", []) if str(value).strip()]
    domains = [str(value).strip() for value in profile.get("core_learning_domains", []) if str(value).strip()]
    first = english[0] if english else chinese[0] if chinese else profile["major_name"]
    second = english[1] if len(english) > 1 else chinese[0] if chinese else tasks[0] if tasks else domains[0]
    if second == first:
        second = tasks[0] if tasks and tasks[0] != first else f"{first} workflow"
    return [first, second]


def _platform_query(profile: dict[str, Any], platform: str, focus: str, variant: int) -> str:
    if platform == "GitHub":
        return f'filename:SKILL.md "{focus}"'
    if platform == "Hugging Face Spaces":
        return f"{focus} {profile['major_name']} analysis"
    suffix = "workflow" if variant == 1 else "data method"
    return f"{profile['major_name']} {focus} {suffix}"


def build_zero_result_jobs(profiles: Iterable[dict[str, Any]], formal: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    profile_list = list(profiles)
    zero = set(zero_formal_major_codes(profile_list, formal))
    jobs: list[dict[str, Any]] = []
    serial = 1
    for profile in profile_list:
        if profile["major_code"] not in zero:
            continue
        for variant, focus in enumerate(_focus_terms(profile), start=1):
            for platform in FOUR_PLATFORMS:
                jobs.append(
                    {
                        "query_id": f"ECON-{profile['major_code']}-{PLATFORM_CODES[platform]}-R3-{serial:04d}",
                        "major_code": profile["major_code"],
                        "major_name": profile["major_name"],
                        "class_code": profile["class_code"],
                        "class_name": profile.get("class_name", ""),
                        "platform": platform,
                        "platform_code": PLATFORM_CODES[platform],
                        "round": 3,
                        "query": _platform_query(profile, platform, focus, variant),
                        "term_types": ["task_expansion", f"focus_{variant}", "zero_formal_supplement"],
                    }
                )
                serial += 1
    return jobs


def select_new_raw_candidates(existing: Iterable[dict[str, Any]], supplemental: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    known = {(row.get("platform"), row.get("candidate_native_id")) for row in existing}
    seen = set(known)
    selected: list[dict[str, Any]] = []
    for row in supplemental:
        key = (row.get("platform"), row.get("candidate_native_id"))
        if not key[1] or key in seen:
            continue
        seen.add(key)
        selected.append(row)
    return selected


def completion_summary(matrix: dict[str, Any], ledger: Iterable[dict[str, Any]]) -> dict[str, Any]:
    terminals: dict[str, dict[str, Any]] = {}
    historical_failed = 0
    for row in ledger:
        if row.get("event_type") != "terminal":
            continue
        if row.get("status") == "failed":
            historical_failed += 1
        terminals[str(row.get("query_id"))] = row
    expected = {str(job["query_id"]) for job in matrix.get("jobs", [])}
    errors: list[str] = []
    for query_id in sorted(expected):
        terminal = terminals.get(query_id)
        if terminal is None:
            errors.append(f"missing_terminal:{query_id}")
        elif terminal.get("status") != "success" or terminal.get("complete") is not True:
            errors.append(f"latest_not_success:{query_id}")
    extras = sorted(set(terminals) - expected)
    errors.extend(f"unexpected_terminal:{query_id}" for query_id in extras)
    return {
        "job_count": len(expected),
        "latest_terminal_count": len(expected & set(terminals)),
        "latest_success_count": sum(
            terminals.get(query_id, {}).get("status") == "success" and terminals.get(query_id, {}).get("complete") is True
            for query_id in expected
        ),
        "historical_failed_attempts": historical_failed,
        "errors": errors,
    }


def recover_matrix_from_ledger(profiles: Iterable[dict[str, Any]], ledger: Iterable[dict[str, Any]]) -> dict[str, Any]:
    profile_map = {profile["major_code"]: profile for profile in profiles}
    latest: dict[str, dict[str, Any]] = {}
    for row in ledger:
        if row.get("event_type") == "terminal" and row.get("round") == 3:
            latest[str(row.get("query_id"))] = row
    jobs = []
    for query_id in sorted(latest):
        row = latest[query_id]
        profile = profile_map[str(row["major_code"])]
        platform = str(row["platform"])
        jobs.append(
            {
                "query_id": query_id,
                "major_code": profile["major_code"],
                "major_name": profile["major_name"],
                "class_code": profile["class_code"],
                "class_name": profile.get("class_name", ""),
                "platform": platform,
                "platform_code": PLATFORM_CODES[platform],
                "round": 3,
                "query": row["query"],
                "term_types": ["task_expansion", "zero_formal_supplement", "recovered_from_terminal_ledger"],
            }
        )
    return {
        "schema_version": "economics-zero-result-round3-v1",
        "round": 3,
        "platforms": list(FOUR_PLATFORMS),
        "zero_major_count": len({job["major_code"] for job in jobs}),
        "job_count": len(jobs),
        "jobs": jobs,
    }


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def merge_audit_ledgers(base: Iterable[dict[str, Any]], supplement: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[tuple[Any, Any], dict[str, Any]] = {}
    for row in [*base, *supplement]:
        key = (row.get("platform"), row.get("candidate_native_id"))
        if not key[1]:
            continue
        if key in merged:
            prior = merged[key]
            row = dict(row)
            for field in ("query_ids", "major_codes", "major_names", "discovery_queries"):
                row[field] = sorted(set(prior.get(field, [])) | set(row.get(field, [])))
        merged[key] = row
    return [merged[key] for key in sorted(merged, key=lambda value: (str(value[0]), str(value[1])))]


def build_supplement_report(matrix: dict[str, Any], ledger: Iterable[dict[str, Any]], raw: Iterable[dict[str, Any]],
                            new_raw: Iterable[dict[str, Any]], audits: Iterable[dict[str, Any]],
                            final_formal: Iterable[dict[str, Any]]) -> dict[str, Any]:
    jobs = list(matrix.get("jobs", []))
    terminals: dict[str, dict[str, Any]] = {}
    for row in ledger:
        if row.get("event_type") == "terminal":
            terminals[str(row.get("query_id"))] = row
    raw_rows, new_rows, audit_rows, formal_rows = list(raw), list(new_raw), list(audits), list(final_formal)
    zero_codes = sorted({job["major_code"] for job in jobs})
    per_major: dict[str, Any] = {}
    for code in zero_codes:
        major_jobs = [job for job in jobs if job["major_code"] == code]
        platform_status = {}
        for platform in FOUR_PLATFORMS:
            selected = [job for job in major_jobs if job["platform"] == platform]
            terminal_rows = [terminals.get(job["query_id"], {}) for job in selected]
            platform_status[platform] = {
                "query_count": len(selected),
                "success_count": sum(row.get("status") == "success" and row.get("complete") is True for row in terminal_rows),
                "result_count": sum(int(row.get("result_count") or 0) for row in terminal_rows),
            }
        per_major[code] = {
            "major_name": major_jobs[0]["major_name"],
            "platforms": platform_status,
            "raw_record_count": sum(row.get("major_code") == code for row in raw_rows),
            "new_unique_native_count": sum(row.get("major_code") == code for row in new_rows),
            "audited_candidate_count": sum(code in row.get("major_codes", []) for row in audit_rows),
            "final_formal_count": sum(code in row.get("matched_major_codes", []) for row in formal_rows),
        }
    return {
        "schema_version": "economics-zero-result-supplement-v1",
        "initial_zero_major_count": len(zero_codes),
        "round3_job_count": len(jobs),
        "round3_latest_success_count": sum(
            terminals.get(job["query_id"], {}).get("status") == "success"
            and terminals.get(job["query_id"], {}).get("complete") is True
            for job in jobs
        ),
        "raw_record_count": len(raw_rows),
        "new_unique_native_count": len(new_rows),
        "audit_row_count": len(audit_rows),
        "still_zero_major_codes": [code for code, row in per_major.items() if row["final_formal_count"] == 0],
        "per_major": per_major,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--formal", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--existing-raw", type=Path)
    parser.add_argument("--supplement-raw", type=Path)
    parser.add_argument("--new-raw", type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--base-audits", type=Path)
    parser.add_argument("--supplement-audits", type=Path)
    parser.add_argument("--combined-audits", type=Path)
    parser.add_argument("--final-formal", type=Path)
    parser.add_argument("--supplement-report", type=Path)
    parser.add_argument("--recover-matrix-from-ledger", action="store_true")
    args = parser.parse_args()
    profile_doc = _read_json(args.profiles)
    profiles = profile_doc.get("profiles", profile_doc)
    formal = _read_json(args.formal)
    if args.recover_matrix_from_ledger:
        if not args.ledger:
            raise SystemExit("--recover-matrix-from-ledger requires --ledger")
        matrix = recover_matrix_from_ledger(profiles, _read_jsonl(args.ledger))
        jobs = matrix["jobs"]
    else:
        jobs = build_zero_result_jobs(profiles, formal)
        matrix = {
            "schema_version": "economics-zero-result-round3-v1",
            "round": 3,
            "platforms": list(FOUR_PLATFORMS),
            "zero_major_count": len({job["major_code"] for job in jobs}),
            "job_count": len(jobs),
            "jobs": jobs,
        }
    args.matrix.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.existing_raw and args.supplement_raw and args.new_raw:
        selected = select_new_raw_candidates(_read_jsonl(args.existing_raw), _read_jsonl(args.supplement_raw))
        _write_jsonl(args.new_raw, selected)
        print(json.dumps({"jobs": len(jobs), "new_candidates": len(selected)}, ensure_ascii=False))
    else:
        print(json.dumps({"jobs": len(jobs), "zero_majors": matrix["zero_major_count"]}, ensure_ascii=False))
    if args.ledger and args.manifest:
        summary = completion_summary(matrix, _read_jsonl(args.ledger))
        args.manifest.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if summary["errors"]:
            return 1
    if args.base_audits and args.supplement_audits and args.combined_audits:
        merged = merge_audit_ledgers(_read_jsonl(args.base_audits), _read_jsonl(args.supplement_audits))
        _write_jsonl(args.combined_audits, merged)
    if all((args.ledger, args.supplement_raw, args.new_raw, args.supplement_audits, args.final_formal, args.supplement_report)):
        report = build_supplement_report(
            matrix,
            _read_jsonl(args.ledger),
            _read_jsonl(args.supplement_raw),
            _read_jsonl(args.new_raw),
            _read_jsonl(args.supplement_audits),
            _read_json(args.final_formal),
        )
        args.supplement_report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
