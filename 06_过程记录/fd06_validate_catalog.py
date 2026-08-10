#!/usr/bin/env python3
"""Validate the formal FD06 catalog and, optionally, the 26 deliverables."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "06_过程记录" / "fd06_catalog.json"
SCHEMA = ROOT / "06_过程记录" / "fd06_catalog.schema.json"
AUDIT = ROOT / "04_验证记录" / "2026-08-08-FD06静态安全审查.json"
DELIVERY_ROOT = ROOT / "05_交付物" / "06_课程设计、教学材料与教学评估_全网公开技能调研"
CODES = [f"06-{index:02d}" for index in range(1, 13)]
FORMAL_GRADES = {"SA", "SB", "SB-A"}


def validate(check_deliverables: bool = False) -> dict:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(catalog)
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    formal_audit = [item for item in audit if item["security_grade"] in FORMAL_GRADES]

    assert len(catalog) == len(formal_audit) == 298, "正式目录数量与安全审查不一致"
    assert [item["skill_id"] for item in catalog] == [f"FD-06-{index:04d}" for index in range(1, 299)]
    assert len({item["candidate_id"] for item in catalog}) == 298
    assert {item["primary_subcategory"] for item in catalog} == set(CODES)
    assert not ({item["security_grade"] for item in catalog} - FORMAL_GRADES)
    assert all(re.search(r"[\u4e00-\u9fff]", item["plain_function"]) for item in catalog)
    assert all(item["security_grade"] != "SB-A" or item["adaptation_requirements"] for item in catalog)
    assert all(item["canonical_url"].startswith("https://") for item in catalog)
    assert all("未安装" in item["verification_depth"] and "未运行" in item["verification_depth"] for item in catalog)

    catalog_candidates = {item["candidate_id"] for item in catalog}
    expected_candidates = {item["candidate_id"] for item in formal_audit}
    assert catalog_candidates == expected_candidates, "目录与静态审查的正式候选集合不一致"

    result = {
        "skills": len(catalog),
        "subcategories": dict(sorted(Counter(item["primary_subcategory"] for item in catalog).items())),
        "security_grades": dict(sorted(Counter(item["security_grade"] for item in catalog).items())),
    }
    if check_deliverables:
        xlsx = sorted(DELIVERY_ROOT.rglob("*.xlsx"))
        docx = sorted(DELIVERY_ROOT.rglob("*.docx"))
        assert len(xlsx) == 13, f"Excel 文件应为 13 个，实际 {len(xlsx)}"
        assert len(docx) == 13, f"Word 文件应为 13 个，实际 {len(docx)}"
        result["deliverables"] = {"xlsx": len(xlsx), "docx": len(docx)}
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-deliverables", action="store_true")
    args = parser.parse_args()
    print(json.dumps(validate(args.check_deliverables), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
