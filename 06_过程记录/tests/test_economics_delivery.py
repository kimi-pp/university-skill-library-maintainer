from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "06_过程记录" / "economics_2026-08-19" / "build_delivery_inputs.py"


def load_module():
    spec = importlib.util.spec_from_file_location("economics_delivery_inputs", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_four_payloads_partition_formal_ids_without_duplication():
    module = load_module()
    inputs = module.load_inputs(module.default_paths(ROOT))
    payloads = module.build_all_payloads(inputs)
    ids = [row["skill_id"] for payload in payloads for row in payload["formal_candidates"]]
    assert len(payloads) == 4
    assert len(ids) == len(set(ids)) == 95
    assert set(ids) == {row["skill_id"] for row in inputs["formal"]}


def test_payloads_cover_thirty_profiles_and_keep_dependency_fields_separate():
    module = load_module()
    payloads = module.build_all_payloads(module.load_inputs(module.default_paths(ROOT)))
    assert sum(len(payload["profiles"]) for payload in payloads) == 30
    for payload in payloads:
        for row in payload["formal_candidates"]:
            assert {"external_api", "network_behavior", "local_runtime", "local_interface"} <= row.keys()
            if row["external_api"] == "是":
                assert row["network_behavior"] not in {"", "无"}


def test_zero_result_major_has_four_platform_supplement_note():
    module = load_module()
    payloads = module.build_all_payloads(module.load_inputs(module.default_paths(ROOT)))
    statuses = {row["major_code"]: row for payload in payloads for row in payload["major_search_status"]}
    row = statuses["020110TK"]
    assert row["formal_count"] == 0
    assert row["supplement_completed"] is True
    assert set(row["supplement_platforms"]) == {"SkillHub", "ClawHub", "GitHub", "Hugging Face Spaces"}


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__]))
