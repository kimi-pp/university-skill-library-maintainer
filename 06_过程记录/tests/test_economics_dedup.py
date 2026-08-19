from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "06_过程记录" / "economics_2026-08-19" / "deduplicate_economics.py"


def load_module():
    spec = importlib.util.spec_from_file_location("economics_dedup", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_same_upstream_across_platforms_is_one_candidate():
    module = load_module()
    rows = [
        {
            "candidate_key": "a",
            "platform": "GitHub",
            "repository": "owner/repo",
            "skill_path": "skills/tax/SKILL.md",
            "canonical_url": "https://github.com/owner/repo/blob/" + "1" * 40 + "/skills/tax/SKILL.md",
            "skill_text": "---\nname: tax-policy\ndescription: Tax policy incidence analysis\n---\nInputs and outputs.",
            "skill_content_sha256": "f" * 64,
            "formal_eligible": True,
            "major_codes": ["020201K"],
        },
        {
            "candidate_key": "b",
            "platform": "SkillHub",
            "upstream_url": "https://github.com/owner/repo/tree/main/skills/tax",
            "candidate_native_id": "namespace/tax-policy@1.0.0",
            "skill_text": "---\nname: tax-policy\ndescription: Tax policy incidence analysis\n---\nInputs and outputs.",
            "skill_content_sha256": "f" * 64,
            "formal_eligible": True,
            "major_codes": ["020201K"],
        },
    ]
    unique, relations = module.deduplicate(rows)
    assert len(unique) == 1
    assert unique[0]["discovery_platforms"] == ["GitHub", "SkillHub"]
    assert relations[0]["reason"] in {"same_content", "same_upstream"}


def test_mirror_repository_path_normalizes_to_upstream():
    module = load_module()
    row = {
        "platform": "GitHub",
        "repository": "mirror/archive",
        "skill_path": "mirrors/repos/original@economics-skills/skills/cge/SKILL.md",
    }
    assert module.canonical_source_key(row) == "github:original/economics-skills:skills/cge/skill.md"


def test_function_fingerprint_ignores_marketing_punctuation():
    module = load_module()
    a = {"skill_name": "CGE Analysis!", "skill_description": "Build an input-output CGE policy simulation."}
    b = {"skill_name": "cge-analysis", "skill_description": "Build an input output CGE policy simulation"}
    assert module.function_fingerprint(a) == module.function_fingerprint(b)


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__]))
