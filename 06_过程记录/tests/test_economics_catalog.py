from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUN_ROOT = PROJECT_ROOT / "06_过程记录" / "economics_2026-08-19"
MODULE_PATH = RUN_ROOT / "update_economics_catalog.py"
CATALOG_PATH = (
    PROJECT_ROOT
    / "06_过程记录"
    / "discipline_mapping"
    / "catalogs"
    / "undergraduate_2026.json"
)
SOURCE_MANIFEST_PATH = (
    PROJECT_ROOT
    / "06_过程记录"
    / "discipline_mapping"
    / "source_manifest.json"
)
INDEX_PATH = PROJECT_ROOT / "02_知识库" / "discipline_catalog" / "INDEX.md"
SOURCE_METHOD_PATH = (
    PROJECT_ROOT
    / "02_知识库"
    / "discipline_catalog"
    / "SOURCE_AND_METHOD.md"
)

HISTORICAL_ECONOMICS_ROWS = """
| 020101 | 经济学 | 历史源表 |
| 020102 | 经济统计学 | 历史源表 |
| 020103T | 国民经济管理 | 历史源表 |
| 020104T | 资源与环境经济学 | 历史源表 |
| 020105T | 商务经济学 | 历史源表 |
| 020106T | 能源经济 | 历史源表 |
| 020107T | 劳动经济学 | 历史源表 |
| 020108T | 数字经济 | 历史源表 |
| 020201K | 财政学 | 历史源表 |
| 020202 | 税收学 | 历史源表 |
| 020301K | 金融学 | 历史源表 |
| 020302 | 金融工程 | 历史源表 |
| 020303 | 保险学 | 历史源表 |
| 020304 | 投资学 | 历史源表 |
| 020305T | 互联网金融 | 历史源表 |
| 020306T | 金融数学 | 历史源表 |
| 020307T | 信用管理 | 历史源表 |
| 020308T | 经济与金融 | 历史源表 |
| 020401 | 国际经济与贸易 | 历史源表 |
| 020402 | 贸易经济 | 历史源表 |
"""


def load_subject():
    if not MODULE_PATH.exists():
        raise AssertionError(f"missing implementation: {MODULE_PATH}")
    spec = importlib.util.spec_from_file_location("update_economics_catalog", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load update_economics_catalog")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EconomicsCatalogTests(unittest.TestCase):
    def test_official_scope_has_four_classes_and_thirty_majors(self):
        subject = load_subject()
        scope = subject.load_economics_scope(CATALOG_PATH)

        self.assertEqual(scope["category_code"], "02")
        self.assertEqual([row["major_count"] for row in scope["classes"]], [11, 3, 12, 4])
        self.assertEqual(sum(row["major_count"] for row in scope["classes"]), 30)
        self.assertEqual(
            len({major["major_code"] for row in scope["classes"] for major in row["majors"]}),
            30,
        )

    def test_index_patch_updates_only_economics_counts(self):
        subject = load_subject()
        scope = subject.load_economics_scope(CATALOG_PATH)
        original = INDEX_PATH.read_text(encoding="utf-8")
        updated = subject.patch_index(original, scope)

        self.assertIn("| 02 | 经济学 | 4 | 30 |", updated)
        self.assertIn("| 03 | 法学 | 6 | 26 |", updated)
        self.assertNotIn("| 02 | 经济学 | 4 | 20 |", updated)

    def test_category_render_contains_all_current_codes_and_no_old_code_mapping(self):
        subject = load_subject()
        scope = subject.load_economics_scope(CATALOG_PATH)
        rendered = subject.render_category(scope, subject.load_source_meta(SOURCE_MANIFEST_PATH))

        for code in ("020108T", "020109T", "020110TK", "020111T", "020203TK", "020312TK", "020404TK"):
            self.assertIn(f"| {code} |", rendered)
        self.assertIn("| 020108T | 经济工程 |", rendered)
        self.assertIn("| 020109T | 数字经济 |", rendered)
        self.assertNotIn("| 020108T | 数字经济 |", rendered)
        self.assertEqual(rendered.count("| 02"), 30)

    def test_source_method_patch_preserves_old_source_and_adds_current_authority(self):
        subject = load_subject()
        source_meta = subject.load_source_meta(SOURCE_MANIFEST_PATH)
        original = SOURCE_METHOD_PATH.read_text(encoding="utf-8")
        updated = subject.patch_source_method(original, source_meta)

        self.assertIn("国内大学本科专业目录.xlsx", updated)
        self.assertIn("普通高等学校本科专业目录（2026年）", updated)
        self.assertIn(source_meta["url"], updated)
        self.assertIn(source_meta["sha256"], updated)

    def test_catalog_diff_reports_code_changes_and_ten_net_new_majors(self):
        subject = load_subject()
        scope = subject.load_economics_scope(CATALOG_PATH)
        diff = subject.build_catalog_diff(HISTORICAL_ECONOMICS_ROWS, scope)

        self.assertEqual(diff["old_major_count"], 20)
        self.assertEqual(diff["current_major_count"], 30)
        self.assertEqual(diff["net_change"], 10)
        self.assertIn(
            {"major_name": "数字经济", "old_code": "020108T", "current_code": "020109T"},
            diff["code_changes"],
        )
        json.dumps(diff, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main()
