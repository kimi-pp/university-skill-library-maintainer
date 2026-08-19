from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "06_过程记录" / "economics_2026-08-19" / "supplement_zero_results.py"


def load_module():
    spec = importlib.util.spec_from_file_location("economics_zero_results", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


PROFILES = [
    {
        "major_code": "020101",
        "major_name": "经济学",
        "class_code": "0201",
        "class_name": "经济学类",
        "core_learning_domains": ["计量经济学与因果推断"],
        "typical_tasks": ["构建与检验经济模型"],
        "search_terms": {"zh": ["计量经济学"], "en": ["econometrics", "causal inference"]},
    },
    {
        "major_code": "020303",
        "major_name": "保险学",
        "class_code": "0203",
        "class_name": "金融学类",
        "core_learning_domains": ["保险定价与风险管理"],
        "typical_tasks": ["进行承保与理赔数据分析"],
        "search_terms": {"zh": ["保险定价"], "en": ["insurance pricing", "claims analytics"]},
    },
]


def test_only_zero_formal_majors_receive_round_three_jobs():
    module = load_module()
    formal = [{"matched_major_codes": ["020101"]}]
    jobs = module.build_zero_result_jobs(PROFILES, formal)
    assert {job["major_code"] for job in jobs} == {"020303"}
    assert {job["platform"] for job in jobs} == set(module.FOUR_PLATFORMS)
    assert len(jobs) == 8
    assert {job["round"] for job in jobs} == {3}


def test_round_three_queries_are_task_expansions_and_unique():
    module = load_module()
    jobs = module.build_zero_result_jobs(PROFILES, [])
    assert len({job["query_id"] for job in jobs}) == len(jobs)
    assert len({(job["major_code"], job["platform"], job["query"]) for job in jobs}) == len(jobs)
    assert all("task_expansion" in job["term_types"] for job in jobs)
    github = [job for job in jobs if job["platform"] == "GitHub"]
    assert all("filename:SKILL.md" in job["query"] for job in github)


def test_select_new_raw_candidates_excludes_existing_platform_native_ids():
    module = load_module()
    existing = [{"platform": "GitHub", "candidate_native_id": "a/repo:SKILL.md"}]
    supplemental = [
        {"platform": "GitHub", "candidate_native_id": "a/repo:SKILL.md"},
        {"platform": "SkillHub", "candidate_native_id": "new-skill"},
    ]
    assert module.select_new_raw_candidates(existing, supplemental) == [supplemental[1]]


def test_completion_summary_requires_one_latest_success_per_job():
    module = load_module()
    matrix = {"jobs": [{"query_id": "q1", "platform": "GitHub"}, {"query_id": "q2", "platform": "SkillHub"}]}
    ledger = [
        {"event_type": "terminal", "query_id": "q1", "status": "failed", "complete": False},
        {"event_type": "terminal", "query_id": "q1", "status": "success", "complete": True},
        {"event_type": "terminal", "query_id": "q2", "status": "success", "complete": True},
    ]
    summary = module.completion_summary(matrix, ledger)
    assert summary["job_count"] == 2
    assert summary["latest_success_count"] == 2
    assert summary["historical_failed_attempts"] == 1
    assert summary["errors"] == []


def test_merge_audits_preserves_unique_platform_native_identity_and_unions_majors():
    module = load_module()
    base = [{"platform": "GitHub", "candidate_native_id": "a:r", "major_codes": ["020101"], "query_ids": ["q1"]}]
    supplement = [{"platform": "GitHub", "candidate_native_id": "a:r", "major_codes": ["020102"], "query_ids": ["q2"]}]
    merged = module.merge_audit_ledgers(base, supplement)
    assert len(merged) == 1
    assert merged[0]["major_codes"] == ["020101", "020102"]
    assert merged[0]["query_ids"] == ["q1", "q2"]


def test_supplement_report_keeps_four_platform_evidence_for_zero_major():
    module = load_module()
    jobs = module.build_zero_result_jobs([PROFILES[1]], [])
    ledger = [{"event_type": "terminal", "query_id": job["query_id"], "status": "success", "complete": True, "result_count": 0} for job in jobs]
    report = module.build_supplement_report({"jobs": jobs}, ledger, [], [], [], [])
    row = report["per_major"]["020303"]
    assert set(row["platforms"]) == set(module.FOUR_PLATFORMS)
    assert all(value["success_count"] == 2 for value in row["platforms"].values())
    assert report["still_zero_major_codes"] == ["020303"]


def test_recover_matrix_uses_terminal_ledger_scope_not_later_formal_results():
    module = load_module()
    jobs = module.build_zero_result_jobs(PROFILES, [])
    ledger = [
        {"event_type": "terminal", "query_id": job["query_id"], "major_code": job["major_code"], "platform": job["platform"], "round": 3, "query": job["query"], "status": "success", "complete": True}
        for job in jobs
    ]
    recovered = module.recover_matrix_from_ledger(PROFILES, ledger)
    assert recovered["job_count"] == len(jobs)
    assert recovered["zero_major_count"] == 2
    assert {job["query_id"] for job in recovered["jobs"]} == {job["query_id"] for job in jobs}


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__]))
