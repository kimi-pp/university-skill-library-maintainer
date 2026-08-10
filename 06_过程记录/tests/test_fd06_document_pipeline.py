from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_builder():
    path = ROOT / "06_过程记录" / "fd06_build_documents.py"
    spec = importlib.util.spec_from_file_location("fd06_build_documents", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_document_specs_cover_overview_and_twelve_subcategories():
    module = load_builder()
    catalog = json.loads((ROOT / "06_过程记录" / "fd06_catalog.json").read_text(encoding="utf-8"))

    specs = module.build_delivery_specs(catalog)

    assert len(specs) == 13
    assert specs[0]["key"] == "00"
    assert specs[0]["records"] == catalog
    assert {spec["key"] for spec in specs[1:]} == {f"06-{index:02d}" for index in range(1, 13)}
    assert sum(len(spec["records"]) for spec in specs[1:]) == 298


def test_skill_text_blocks_keep_plain_language_and_verification_boundary():
    module = load_builder()
    skill = json.loads((ROOT / "06_过程记录" / "fd06_catalog.json").read_text(encoding="utf-8"))[0]

    blocks = module.skill_text_blocks(skill)

    assert skill["plain_function"] in blocks["overview"]
    assert skill["inputs"] in blocks["preparation"]
    assert skill["outputs"] in blocks["result"]
    assert skill["security_grade"] in blocks["safety"]
    assert "未安装" in blocks["verification"] and "未运行" in blocks["verification"]
