from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "06_过程记录" / "economics_2026-08-19" / "adjudicate_economics.py"


def load_module():
    spec = importlib.util.spec_from_file_location("economics_adjudication", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


PROFILES = [
    {
        "major_code": "020101",
        "major_name": "经济学",
        "class_code": "0201",
        "core_learning_domains": ["微观经济学与宏观经济学", "计量经济学与因果推断"],
        "typical_tasks": ["构建与检验经济模型", "评估经济政策效果"],
        "inclusion_rules": ["直接支持经济模型、经济数据或政策分析"],
        "search_terms": {"zh": ["经济学分析", "计量经济学"], "en": ["econometrics", "economic policy evaluation"]},
    },
    {
        "major_code": "020201K",
        "major_name": "财政学",
        "class_code": "0202",
        "core_learning_domains": ["财政理论与税收制度"],
        "typical_tasks": ["分析税收政策与财政支出"],
        "inclusion_rules": ["支持税收归宿或财政政策分析"],
        "search_terms": {"zh": ["税收政策", "财政分析"], "en": ["tax incidence", "public finance"]},
    },
]


def base_row(**updates):
    row = {
        "candidate_key": "abc",
        "canonical_source_key": "github:owner/repo:skill.md",
        "skill_name": "Tax incidence research",
        "skill_description": "Estimate tax incidence and evaluate public-finance policy with economic data.",
        "skill_text": "Inputs: tax and household data. Steps: estimate tax incidence with econometrics. Output: policy evaluation report.",
        "formal_eligible": True,
        "blocking_reasons": [],
        "fixed_version": "1" * 40,
        "license": "MIT",
        "license_allowed": True,
        "security_grade": "SA",
        "snapshot_status": "success",
        "major_codes": ["020101", "020201K"],
        "platform": "GitHub",
        "repository_stars": 60,
        "maintenance_date": "2026-07-01T00:00:00Z",
        "network_behavior": "无",
        "external_api": "否",
        "local_runtime": "不使用",
        "local_interface": "不使用",
        "file_inventory": [{"path": "SKILL.md", "size": 500, "sha256": "2" * 64}],
        "evidence_paths": ["evidence/SKILL.md"],
        "discovery_platforms": ["GitHub"],
    }
    row.update(updates)
    return row


def test_quality_score_is_capped_at_five():
    module = load_module()
    assert module.quality_score({"admission_pass": True, "bonus_flags": [True] * 5}) == 5
    assert module.quality_score({"admission_pass": False, "bonus_flags": [True] * 5}) == 0


def test_explicit_economics_workflow_has_one_primary_class():
    module = load_module()
    result = module.adjudicate(base_row(), PROFILES)
    assert result["professional_relevance_pass"] is True
    assert result["primary_class_code"] in {"0201", "0202"}
    assert len(result["primary_class_code"]) == 4
    assert "020201K" in result["matched_major_codes"]


def test_generic_office_skill_is_excluded_even_if_discovered_for_economics():
    module = load_module()
    row = base_row(
        skill_name="Meeting note writer",
        skill_description="Write concise meeting notes and action items.",
        skill_text="Input: any meeting transcript. Output: generic summary and action list.",
        major_codes=["020101"],
    )
    result = module.adjudicate(row, PROFILES)
    assert result["professional_relevance_pass"] is False
    assert result["formal_included"] is False
    assert "professional_mismatch" in result["exclusion_reasons"]


def test_generic_research_ideation_does_not_pass_on_buried_economics_word():
    module = load_module()
    row = base_row(
        skill_name="Research idea brainstormer",
        skill_description="Generate creative research ideas for any discipline.",
        skill_text="May draw examples from psychology, computer science, sociology, and economics.",
        major_codes=["020101"],
    )
    result = module.adjudicate(row, PROFILES)
    assert result["professional_relevance_pass"] is False
    assert result["formal_included"] is False


def test_short_method_marker_does_not_match_inside_idea():
    module = load_module()
    row = base_row(
        skill_name="Research ideas",
        skill_description="Generate ideas for any academic field.",
        skill_text="A generic brainstorming workflow.",
        major_codes=["020108T"],
    )
    result = module.adjudicate(row, PROFILES)
    assert result["professional_relevance_pass"] is False


def test_insurance_keyword_alone_does_not_make_generic_seo_formal():
    module = load_module()
    profiles = [
        {"major_code": "020303", "major_name": "保险学", "class_code": "0203", "core_learning_domains": ["保险定价"], "typical_tasks": ["保险数据分析"], "inclusion_rules": [], "search_terms": {"en": ["insurance"]}},
    ]
    row = base_row(skill_name="seo", skill_description="SEO campaign planning for insurance companies.", skill_text="A generic marketing workflow.", major_codes=["020303"])
    assert module.adjudicate(row, profiles)["professional_relevance_pass"] is False


def test_insurance_claim_workflow_remains_relevant():
    module = load_module()
    profiles = [
        {"major_code": "020303", "major_name": "保险学", "class_code": "0203", "core_learning_domains": ["保险理赔"], "typical_tasks": ["理赔数据分析"], "inclusion_rules": [], "search_terms": {"en": ["insurance claims"]}},
    ]
    row = base_row(skill_name="insurance-claims-analysis", skill_description="Analyze insurance claim patterns and fraud risk.", skill_text="Input claim data. Workflow steps produce a claims analysis report.", major_codes=["020303"])
    assert module.adjudicate(row, profiles)["professional_relevance_pass"] is True


def test_external_api_requires_nonempty_network_evidence():
    module = load_module()
    row = base_row(external_api="是", network_behavior="无")
    result = module.adjudicate(row, PROFILES)
    assert result["formal_included"] is False
    assert "api_network_inconsistent" in result["exclusion_reasons"]


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__]))
