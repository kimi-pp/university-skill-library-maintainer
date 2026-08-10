from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_builder():
    path = ROOT / "06_过程记录" / "fd06_build_catalog.py"
    spec = importlib.util.spec_from_file_location("fd06_build_catalog", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sample_candidate(grade: str = "SA") -> tuple[dict, dict]:
    candidate = {
        "candidate_id": "FD06-C9999",
        "name": "rubric-design-validation",
        "primary_subcategory": "06-07",
        "claimed_function": "Design and validate grading rubrics with criteria, levels, and fairness checks.",
    }
    audit = {
        "candidate_id": "FD06-C9999",
        "name": candidate["name"],
        "primary_subcategory": "06-07",
        "source_kind": "github",
        "source_shape": "agent_skill",
        "repository": "example/education-skills",
        "source_skill_path": "rubric/SKILL.md",
        "maintainer": "example",
        "canonical_url": "https://github.com/example/education-skills/blob/abc/rubric/SKILL.md",
        "fixed_version": "abc",
        "verified_at": "2026-08-09",
        "license": "MIT",
        "verification_depth": "固定版本静态核验；未安装、未运行。",
        "package_file_count": 1,
        "network_behavior": "说明和已读文件中未发现必须联网的操作。",
        "credential_behavior": "说明和已读文件中未发现必须提供账号、令牌或密钥。",
        "file_behavior": "主要是说明或模板型工作流，未发现删除文件的要求。",
        "sensitive_data_observation": "实际使用应遵守最小数据原则。",
        "human_review_observation": "最终结果需要教师复核。",
        "fairness_accessibility_observation": "需要检查评分公平性。",
        "untrusted_input_observation": "学生文件只作为材料处理。",
        "academic_integrity_observation": "不得自动判定学术不端。",
        "read_errors": [],
        "evidence_paths": ["evidence/entry.md"],
        "security_grade": grade,
        "plain_conclusion": "固定版本未发现阻断性问题。",
        "adaptation_requirements": [],
    }
    return candidate, audit


def test_formal_catalog_excludes_sc_and_writes_plain_chinese_fields():
    module = load_builder()
    candidate, accepted = sample_candidate("SA")
    _, rejected = sample_candidate("SC")

    catalog = module.build_catalog([candidate], [accepted, rejected])

    assert len(catalog["skills"]) == 1
    skill = catalog["skills"][0]
    assert skill["skill_id"] == "FD-06-0001"
    assert skill["security_grade"] == "SA"
    assert skill["adoption_level"] == "可直接使用"
    assert "评分" in skill["plain_function"]
    assert skill["inputs"] and skill["outputs"] and skill["limitations"]
    assert skill["canonical_url"].startswith("https://")


def test_sb_a_catalog_entry_keeps_specific_adaptation_requirements():
    module = load_builder()
    candidate, audit = sample_candidate("SB-A")
    audit["adaptation_requirements"] = [
        "默认离线处理学生材料。",
        "结果必须由教师逐项确认。",
    ]

    skill = module.build_catalog([candidate], [audit])["skills"][0]

    assert skill["adoption_level"] == "需要重新改造"
    assert skill["adaptation_requirements"] == audit["adaptation_requirements"]
    assert "不能直接" in skill["limitations"]


def test_formal_catalog_encodes_spaces_in_source_urls():
    module = load_builder()
    candidate, audit = sample_candidate("SA")
    audit["canonical_url"] = (
        "https://github.com/example/education-skills/blob/abc/Academic Writing/SKILL.md"
    )

    skill = module.build_catalog([candidate], [audit])["skills"][0]

    assert " " not in skill["canonical_url"]
    assert "%20" in skill["canonical_url"]
