"""Task 8 contracts for rules, navigation, and final process records.

Expectations are rebuilt directly from the approved assignment ledger, the
plain-language catalog, the delivery manifest, and Task 7's finalized visual
inventory.  The tests deliberately do not import the Markdown generator.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSIGNMENT_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_assignments.json"
PLAIN_CATALOG_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "plain_language_catalog.json"
MANIFEST_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_manifest.json"
VISUAL_INVENTORY_FILE = PROJECT_ROOT / "06_过程记录" / "visual_review" / "task-7-inventory.json"
VISUAL_FINAL_FILE = PROJECT_ROOT / "06_过程记录" / "visual_review" / "task-7-finalized.json"

TOTAL_INDEX = PROJECT_ROOT / "00_索引" / "INDEX.md"
TAXONOMY_RULE = PROJECT_ROOT / "01_规则" / "TAXONOMY.md"
DATA_DICTIONARY = PROJECT_ROOT / "01_规则" / "DATA_DICTIONARY.md"
REPORTING_STANDARD = PROJECT_ROOT / "01_规则" / "REPORTING_STANDARD.md"
DECISION_LOG = PROJECT_ROOT / "06_过程记录" / "DECISION_LOG.md"
RESEARCH_LOG = PROJECT_ROOT / "06_过程记录" / "RESEARCH_LOG.md"

BIG_CATEGORY_DIRECTORIES = {
    "01": "01_学术写作引用与出版",
    "02": "02_文档表格演示文稿与办公自动化",
    "03": "03_文献检索与学术研究",
    "04": "04_图书馆与信息素养",
    "05": "05_编程数学数据分析和可视化",
}
BIG_CATEGORY_NAMES = {
    "01": "学术写作、引用与出版",
    "02": "文档、表格、演示文稿与办公自动化",
    "03": "文献检索与学术研究",
    "04": "图书馆与信息素养",
    "05": "编程、数学、数据分析和可视化",
}

DOMAIN_NAV_START = "<!-- SUBCATEGORY_NAVIGATION_START -->"
DOMAIN_NAV_END = "<!-- SUBCATEGORY_NAVIGATION_END -->"
TOTAL_NAV_START = "<!-- SUBCATEGORY_OVERVIEW_START -->"
TOTAL_NAV_END = "<!-- SUBCATEGORY_OVERVIEW_END -->"
RESEARCH_RESULT_START = "<!-- SUBCATEGORY_RESEARCH_RESULT_START -->"
RESEARCH_RESULT_END = "<!-- SUBCATEGORY_RESEARCH_RESULT_END -->"
LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?:<([^>]+)>|([^)]+))\)")


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _marked_block(text: str, start: str, end: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise AssertionError(f"标记块必须唯一且完整: {start} / {end}")
    start_at = text.index(start) + len(start)
    end_at = text.index(end, start_at)
    return text[start_at:end_at]


def _markdown_rows(block: str, header: str) -> list[list[str]]:
    lines = [line.strip() for line in block.splitlines()]
    try:
        header_index = lines.index(header)
    except ValueError as error:
        raise AssertionError(f"缺少表头: {header}") from error
    rows: list[list[str]] = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            if rows:
                break
            continue
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows


def _target(cell: str) -> str:
    match = LINK_PATTERN.fullmatch(cell.strip())
    if not match:
        raise AssertionError(f"单元格不是可点击 Markdown 链接: {cell}")
    return match.group(1) or match.group(2)


def _relative_target(from_path: Path, project_relative_target: str) -> str:
    return os.path.relpath(
        PROJECT_ROOT / Path(project_relative_target),
        start=from_path.parent,
    ).replace(os.sep, "/")


class SubcategorizedRulesAndNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assignment_data = _load_json(ASSIGNMENT_FILE)
        cls.taxonomy = sorted(cls.assignment_data["taxonomy"], key=lambda item: item["code"])
        cls.assignments = cls.assignment_data["assignments"]
        cls.plain_catalog = _load_json(PLAIN_CATALOG_FILE)
        cls.manifest = _load_json(MANIFEST_FILE)
        cls.inventory = _load_json(VISUAL_INVENTORY_FILE)
        cls.finalized = _load_json(VISUAL_FINAL_FILE)

        cls.taxonomy_by_code = {item["code"]: item for item in cls.taxonomy}
        cls.counts = Counter(cls.assignments.values())
        cls.manifest_by_subcategory = {}
        for item in cls.manifest:
            if item["scope"] == "subcategory":
                cls.manifest_by_subcategory.setdefault(item["subcategory_code"], {})[
                    item["format"]
                ] = item["path"]

    def test_derived_sources_are_the_complete_157_to_61_to_132_contract(self):
        """A missing record, category, assignment, or delivery path must fail Task 8."""
        source_ids = {row["id"] for row in self.plain_catalog}
        self.assertEqual(len(self.plain_catalog), 157)
        self.assertEqual(len(source_ids), 157)
        self.assertEqual(set(self.assignments), source_ids)
        self.assertEqual(len(self.taxonomy), 61)
        self.assertEqual(set(self.counts), set(self.taxonomy_by_code))
        self.assertEqual(sum(self.counts.values()), 157)
        self.assertEqual(len(self.manifest), 132)
        self.assertEqual(Counter(item["format"] for item in self.manifest), {"docx": 66, "xlsx": 66})
        self.assertEqual(set(self.manifest_by_subcategory), set(self.taxonomy_by_code))
        self.assertTrue(all(set(paths) == {"docx", "xlsx"} for paths in self.manifest_by_subcategory.values()))

    def test_taxonomy_rule_states_the_approved_general_task_model(self):
        """Rules must not turn this general-purpose sample into a discipline taxonomy."""
        text = TAXONOMY_RULE.read_text(encoding="utf-8")
        required = [
            "13 个大分类",
            "五个通用大分类",
            "任务用途",
            "大分类",
            "小分类",
            "唯一主分类",
            "辅助标签",
            "01-01",
            "157",
            "61",
            "不涉及专业或学科分类",
            "原始事实源",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_data_dictionary_defines_all_derived_and_reader_facing_fields(self):
        """Removing a new field or the fact-preservation boundary must be detected."""
        text = DATA_DICTIONARY.read_text(encoding="utf-8")
        required = [
            "小分类代码",
            "小分类名称",
            "小分类收录重点",
            "唯一主分类",
            "辅助标签",
            "通俗主要用途",
            "通俗主要产出",
            "通俗适用人员",
            "通俗适用场景",
            "通俗使用前准备",
            "通俗限制",
            "通俗接入说明",
            "通俗核验说明",
            "候选",
            "未安装",
            "未运行",
            "已验证可用",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_reporting_standard_defines_plain_dual_level_delivery(self):
        """The reporting contract must preserve facts while making both report levels usable."""
        text = REPORTING_STANDARD.read_text(encoding="utf-8")
        required = [
            "高等教育",
            "首次出现",
            "邻近解释",
            "软件名",
            "英文名称",
            "内部编号",
            "URL",
            "核验",
            "许可证",
            "11 pt",
            "大分类概览",
            "小分类独立",
            "66 份 Word",
            "66 份 Excel",
            "132",
            "未安装、未运行",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_total_index_is_derived_navigation_for_all_five_and_sixty_one_categories(self):
        """A stale total, omitted leaf entry, or wrong overview link must fail."""
        text = TOTAL_INDEX.read_text(encoding="utf-8")
        block = _marked_block(text, TOTAL_NAV_START, TOTAL_NAV_END)
        self.assertIn("157 项", block)
        self.assertIn("61 个小分类", block)
        self.assertIn(f"### {len(self.taxonomy)} 个小分类知识库入口", block)
        self.assertIn("132 个文件", block)
        self.assertIn("66 份 Word", block)
        self.assertIn("66 份 Excel", block)
        self.assertIn("未安装、未运行", block)

        delivery_link = "[通俗细分版交付目录](<../05_交付物/通俗细分版_2026-08-07/>)"
        archive_link = "[原始版存档](<../05_交付物/原始版_2026-08-06/>)"
        self.assertIn(delivery_link, block)
        self.assertIn(archive_link, block)

        big_rows = _markdown_rows(
            block,
            "| 大分类 | Skill 数 | 小分类数 | 大类导航 | Word 概览 | Excel 概览 |",
        )
        self.assertEqual(len(big_rows), 5)
        expected_big_rows = []
        for big_code in BIG_CATEGORY_DIRECTORIES:
            overview = {
                item["format"]: item["path"]
                for item in self.manifest
                if item["scope"] == "overview" and item["big_category_code"] == big_code
            }
            expected_big_rows.append(
                [
                    f"{big_code} {BIG_CATEGORY_NAMES[big_code]}",
                    str(sum(self.counts[code] for code in self.counts if code.startswith(f"{big_code}-"))),
                    str(sum(1 for item in self.taxonomy if item["code"].startswith(f"{big_code}-"))),
                    f"../02_知识库/functional_domains/{BIG_CATEGORY_DIRECTORIES[big_code]}/INDEX.md",
                    _relative_target(TOTAL_INDEX, overview["docx"]),
                    _relative_target(TOTAL_INDEX, overview["xlsx"]),
                ]
            )
        actual_big_rows = [row[:3] + [_target(cell) for cell in row[3:]] for row in big_rows]
        self.assertEqual(actual_big_rows, expected_big_rows)

        leaf_rows = _markdown_rows(block, "| 小分类代码 | 小分类名称 | 知识库入口 |")
        expected_leaf_rows = []
        for category in self.taxonomy:
            code, name = category["code"], category["name"]
            expected_leaf_rows.append(
                [
                    code,
                    name,
                    f"../02_知识库/functional_domains/{BIG_CATEGORY_DIRECTORIES[code[:2]]}/subcategories/{code}_{name}/INDEX.md",
                ]
            )
        actual_leaf_rows = [row[:2] + [_target(row[2])] for row in leaf_rows]
        self.assertEqual(actual_leaf_rows, expected_leaf_rows)

    def test_domain_indexes_match_taxonomy_assignments_manifest_and_real_files(self):
        """Every domain row must reject missing, duplicate, extra, reordered, or drifted metadata."""
        all_codes = []
        for big_code, directory in BIG_CATEGORY_DIRECTORIES.items():
            index_path = PROJECT_ROOT / "02_知识库" / "functional_domains" / directory / "INDEX.md"
            text = index_path.read_text(encoding="utf-8")
            block = _marked_block(text, DOMAIN_NAV_START, DOMAIN_NAV_END)
            rows = _markdown_rows(
                block,
                "| 小分类代码 | 小分类名称 | 成员数 | 知识库 | Word | Excel |",
            )
            categories = [item for item in self.taxonomy if item["code"].startswith(f"{big_code}-")]
            self.assertEqual(len(rows), len(categories), index_path)

            expected_rows = []
            for category in categories:
                code, name = category["code"], category["name"]
                paths = self.manifest_by_subcategory[code]
                expected_rows.append(
                    [
                        code,
                        name,
                        str(self.counts[code]),
                        f"subcategories/{code}_{name}/INDEX.md",
                        _relative_target(index_path, paths["docx"]),
                        _relative_target(index_path, paths["xlsx"]),
                    ]
                )
            actual_rows = [row[:3] + [_target(cell) for cell in row[3:]] for row in rows]
            self.assertEqual(actual_rows, expected_rows, index_path)
            all_codes.extend(row[0] for row in rows)

            for row in rows:
                for cell in row[3:]:
                    resolved = (index_path.parent / _target(cell)).resolve()
                    self.assertTrue(resolved.exists() and resolved.stat().st_size > 0, resolved)

        self.assertEqual(all_codes, [item["code"] for item in self.taxonomy])
        self.assertEqual(len(all_codes), len(set(all_codes)))

    def test_all_local_links_in_the_modified_markdown_files_exist(self):
        """A locally linked rule, knowledge page, delivery, archive, or log target must exist."""
        paths = [
            TAXONOMY_RULE,
            DATA_DICTIONARY,
            REPORTING_STANDARD,
            TOTAL_INDEX,
            DECISION_LOG,
            RESEARCH_LOG,
            *[
                PROJECT_ROOT / "02_知识库" / "functional_domains" / directory / "INDEX.md"
                for directory in BIG_CATEGORY_DIRECTORIES.values()
            ],
        ]
        checked = 0
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for match in LINK_PATTERN.finditer(text):
                target = (match.group(1) or match.group(2)).strip()
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"{path}: {target}")
                checked += 1
        minimum_expected = (
            len(self.plain_catalog)
            + 3 * len(self.taxonomy)
            + 3 * len(BIG_CATEGORY_DIRECTORIES)
            + len(self.taxonomy)
            + 2
        )
        self.assertGreaterEqual(checked, minimum_expected)

    def test_all_modified_markdown_links_render_as_commonmark_anchors(self):
        """A space-containing target must not silently render as ordinary text."""
        class HrefCollector(HTMLParser):
            def __init__(self):
                super().__init__()
                self.hrefs = []

            def handle_starttag(self, tag, attrs):
                if tag == "a":
                    self.hrefs.append(dict(attrs).get("href"))

        paths = [
            TAXONOMY_RULE,
            DATA_DICTIONARY,
            REPORTING_STANDARD,
            TOTAL_INDEX,
            DECISION_LOG,
            RESEARCH_LOG,
            *[
                PROJECT_ROOT / "02_知识库" / "functional_domains" / directory / "INDEX.md"
                for directory in BIG_CATEGORY_DIRECTORIES.values()
            ],
        ]
        renderer = """
const { marked } = require('marked');
const fs = require('fs');
process.stdout.write(marked.parse(fs.readFileSync(process.argv[1], 'utf8')));
"""
        for path in paths:
            text = path.read_text(encoding="utf-8")
            raw_targets = [
                (match.group(1) or match.group(2)).strip()
                for match in LINK_PATTERN.finditer(text)
            ]
            result = subprocess.run(
                ["node", "-e", renderer, str(path)],
                cwd=PROJECT_ROOT,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            collector = HrefCollector()
            collector.feed(result.stdout)
            rendered_targets = [unquote(href) for href in collector.hrefs if href]
            with self.subTest(path=path):
                self.assertEqual(Counter(rendered_targets), Counter(raw_targets))

    def test_decisions_and_research_log_record_approved_boundaries_and_actual_task7_metrics(self):
        """Logs must not omit an approval or report stale/manual visual totals."""
        decisions = DECISION_LOG.read_text(encoding="utf-8")
        for phrase in [
            "任务用途优先",
            "唯一主分类",
            "辅助标签",
            "通俗化",
            "原件保留",
            "五类先打样",
            "不涉及专业或学科分类",
        ]:
            with self.subTest(decision=phrase):
                self.assertIn(phrase, decisions)

        research = RESEARCH_LOG.read_text(encoding="utf-8")
        result = _marked_block(research, RESEARCH_RESULT_START, RESEARCH_RESULT_END)
        render_counts = Counter(item["render_kind"] for item in self.inventory["images"])
        formats = Counter(item["format"] for item in self.manifest)
        expected_phrases = [
            f"{len(self.plain_catalog)} 项",
            f"{len(self.taxonomy)} 个小分类",
            f"{len(self.manifest)} 个文件",
            f"DOCX {formats['docx']}/66",
            f"XLSX {formats['xlsx']}/66",
            f"{render_counts['docx_page']} 页",
            f"{render_counts['worksheet']} 张工作表整表图",
            f"{render_counts['segment']} 张长表分段图",
            f"{self.finalized['summary']['images']} 张原始检查图",
            f"{self.finalized['summary']['pass']}/{self.finalized['summary']['images']}",
            self.inventory["inventory_digest"],
            "结构验证",
            "发现的问题",
            "已关闭",
            "候选 Skill",
            "未安装、未运行",
        ]
        for phrase in expected_phrases:
            with self.subTest(result=phrase):
                self.assertIn(phrase, result)
        self.assertTrue(self.finalized["review_complete"])
        self.assertEqual(self.finalized["summary"]["nonpass"], 0)

    def test_updated_markdown_has_no_placeholder_overclaim_or_internal_noise(self):
        """The final reader-facing Markdown must not leak drafting or internal execution noise."""
        paths = [
            TAXONOMY_RULE,
            DATA_DICTIONARY,
            REPORTING_STANDARD,
            TOTAL_INDEX,
            DECISION_LOG,
            RESEARCH_LOG,
            *[
                PROJECT_ROOT / "02_知识库" / "functional_domains" / directory / "INDEX.md"
                for directory in BIG_CATEGORY_DIRECTORIES.values()
            ],
        ]
        forbidden = [
            r"\bTODO\b",
            r"\bTBD\b",
            r"\bPLACEHOLDER\b",
            r"\.superpowers[/\\]tmp",
            r"\.worktrees[/\\]",
            r"C:\\Users\\",
            r"node_modules",
            r"候选(?: Skill)?(?:已经|已)(?:安装|运行|验证可用)",
            r"学科小分类",
            r"专业小分类",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for pattern in forbidden:
                with self.subTest(path=path, pattern=pattern):
                    self.assertIsNone(re.search(pattern, text, re.IGNORECASE), path)


if __name__ == "__main__":
    unittest.main()
