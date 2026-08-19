import importlib.util
import json
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
RUN_ROOT = PROJECT / "06_过程记录" / "economics_2026-08-19"
MODULE_PATH = RUN_ROOT / "build_professional_profiles.py"
SCOPE_PATH = RUN_ROOT / "economics_scope.json"
LEDGER_PATH = RUN_ROOT / "profile_source_ledger.jsonl"
PROFILES_PATH = RUN_ROOT / "professional_profiles.json"


def load_module():
    assert MODULE_PATH.is_file(), "专业画像构建模块尚未实现"
    spec = importlib.util.spec_from_file_location("build_professional_profiles", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_profile_builder_outputs_all_30_current_majors(tmp_path):
    module = load_module()
    output = tmp_path / "professional_profiles.json"
    ledger = tmp_path / "profile_source_ledger.jsonl"
    module.build_profiles(SCOPE_PATH, output, ledger)

    payload = json.loads(output.read_text(encoding="utf-8"))
    profiles = payload["profiles"]
    assert len(profiles) == 30
    assert len({row["major_code"] for row in profiles}) == 30
    assert Counter(row["class_code"] for row in profiles) == {
        "0201": 11,
        "0202": 3,
        "0203": 12,
        "0204": 4,
    }


def test_each_profile_has_learning_tasks_boundaries_and_search_terms(tmp_path):
    module = load_module()
    output = tmp_path / "professional_profiles.json"
    ledger = tmp_path / "profile_source_ledger.jsonl"
    module.build_profiles(SCOPE_PATH, output, ledger)
    profiles = json.loads(output.read_text(encoding="utf-8"))["profiles"]

    for row in profiles:
        assert len(row["core_learning_domains"]) >= 3, row["major_name"]
        assert len(row["typical_tasks"]) >= 3, row["major_name"]
        assert len(row["inclusion_rules"]) >= 2, row["major_name"]
        assert len(row["exclusion_boundaries"]) >= 2, row["major_name"]
        assert len(row["search_terms"]["zh"]) >= 3, row["major_name"]
        assert len(row["search_terms"]["en"]) >= 3, row["major_name"]
        assert len(row["source_ids"]) >= 2, row["major_name"]


def test_source_ledger_is_authoritative_and_covers_each_major(tmp_path):
    module = load_module()
    output = tmp_path / "professional_profiles.json"
    ledger = tmp_path / "profile_source_ledger.jsonl"
    module.build_profiles(SCOPE_PATH, output, ledger)

    sources = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line]
    source_by_id = {row["source_id"]: row for row in sources}
    assert len(source_by_id) == len(sources)
    assert any(row["publisher"] == "教育部" for row in sources)
    for source in sources:
        assert source["url"].startswith("https://")
        assert source["publisher"]
        assert source["title"]
        assert source["accessed_at"] == "2026-08-19"
        assert source["authority"] in {"教育部", "政府部门", "高校官网"}

    profiles = json.loads(output.read_text(encoding="utf-8"))["profiles"]
    for row in profiles:
        attached = [source_by_id[source_id] for source_id in row["source_ids"]]
        assert any(source["authority"] == "教育部" for source in attached)
        assert any(source["authority"] in {"政府部门", "高校官网"} for source in attached)
        assert any(row["major_code"] in source["major_codes"] for source in attached)


def test_known_professional_boundaries_prevent_cross_discipline_drift(tmp_path):
    module = load_module()
    output = tmp_path / "professional_profiles.json"
    ledger = tmp_path / "profile_source_ledger.jsonl"
    module.build_profiles(SCOPE_PATH, output, ledger)
    profiles = {
        row["major_name"]: row
        for row in json.loads(output.read_text(encoding="utf-8"))["profiles"]
    }

    actuarial = " ".join(profiles["精算学"]["core_learning_domains"])
    assert "风险模型" in actuarial and "精算" in actuarial
    assert any("泛财经" in value for value in profiles["精算学"]["exclusion_boundaries"])

    resource_audit = " ".join(profiles["资源环境审计"]["core_learning_domains"])
    assert "审计" in resource_audit and ("资源" in resource_audit or "环境" in resource_audit)
    assert any("普通会计" in value for value in profiles["资源环境审计"]["exclusion_boundaries"])

    digital_trade = " ".join(profiles["数字贸易"]["core_learning_domains"])
    assert "跨境" in digital_trade or "数字贸易" in digital_trade
    assert any("电商文案" in value for value in profiles["数字贸易"]["exclusion_boundaries"])


def test_checked_in_profiles_and_ledger_are_reproducible():
    module = load_module()
    assert PROFILES_PATH.is_file()
    assert LEDGER_PATH.is_file()
    assert module.validate_checked_in_outputs(SCOPE_PATH, PROFILES_PATH, LEDGER_PATH) == []
