import hashlib
import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "03_候选池" / "deduplicated"
ASSIGNMENT_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_assignments.json"
sys.path.insert(0, str(PROJECT_ROOT / "06_过程记录" / "tools"))

from subcategory_pipeline import (
    enrich_with_subcategory,
    load_assignment_file,
    load_source_records,
    readability_issues,
    simplify_record,
    validate_assignments,
    write_plain_catalog,
)


EXPECTED_SUBCATEGORY_COUNTS = {
    "01-01": 2, "01-02": 5, "01-03": 1, "01-04": 1, "01-05": 3,
    "01-06": 2, "01-07": 2, "01-08": 1, "01-09": 3,
    "02-01": 2, "02-02": 4, "02-03": 5, "02-04": 2, "02-05": 1,
    "02-06": 3, "02-07": 2, "02-08": 1, "02-09": 2,
    "03-01": 5, "03-02": 7, "03-03": 1, "03-04": 2, "03-05": 3,
    "03-06": 1, "03-07": 2, "03-08": 5, "03-09": 3, "03-10": 1,
    "03-11": 1,
    "04-01": 2, "04-02": 2, "04-03": 2, "04-04": 4, "04-05": 1,
    "04-06": 2, "04-07": 2, "04-08": 2, "04-09": 4, "04-10": 2,
    "04-11": 4, "04-12": 2,
    "05-01": 1, "05-02": 2, "05-03": 2, "05-04": 4, "05-05": 5,
    "05-06": 1, "05-07": 2, "05-08": 5, "05-09": 3, "05-10": 2,
    "05-11": 3, "05-12": 2, "05-13": 2, "05-14": 3, "05-15": 5,
    "05-16": 3, "05-17": 2, "05-18": 3, "05-19": 4, "05-20": 1,
}
APPROVED_ASSIGNMENT_SHA256 = "ca2fa005329db69b4cb07e1ffd566e0c8f773a3e9bd0ca4d8a445f9ba7633082"
PLAIN_FIELDS = {
    "plain_purpose",
    "plain_audience",
    "plain_when_to_use",
    "plain_prerequisites",
    "plain_limitations",
    "plain_integration",
    "plain_verification",
}

SAMPLE_RECORD = {
    "id": "GH-01-0001",
    "name": "scientific-writing",
    "cn": "科学论文写作与审计",
    "cat": "01",
    "repo": "K-Dense-AI/scientific-agent-skills",
    "path": "skills/scientific-writing/SKILL.md",
    "ecosystem": "Agent Skills（兼容 Codex）",
    "form": "社区 skill、开源仓库",
    "tags": "科学写作、证据溯源、报告规范、投稿准备",
    "summary": "起草、修订并审计科学论文或研究报告。",
    "detail": "用证据清单把写作、事实核验与最终批准分开。",
    "roles": "学生、科研人员、教学人员",
    "scenario": "论文写作、投稿前一致性审查",
    "compat": "A",
    "adapt": "可直接按 Codex skill 方式使用；按学科补充本校模板。",
    "deps": "Python 3.11+ 仅用于可选本地脚本",
    "risk": "不应把生成文本视为证据；未发表材料需按授权边界处理。",
    "verify": "二级包内容验证",
    "priority": "高",
    "related": "",
    "repo_url": "https://github.com/K-Dense-AI/scientific-agent-skills",
    "skill_url": "https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md",
    "stars": 32822,
    "repo_pushed": "2026-08-03",
    "license": "MIT",
    "subcategory_code": "01-02",
    "subcategory_name": "论文与报告写作",
}


class SubcategoryAssignmentTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "GH-01-0001"},
            {"id": "GH-01-0002"},
        ]
        self.mapping = {
            "taxonomy": [
                {"code": "01-01", "name": "规划", "inclusion_focus": "测试"},
                {"code": "01-02", "name": "写作", "inclusion_focus": "测试"},
                {"code": "02-01", "name": "文档", "inclusion_focus": "测试"},
            ],
            "assignments": {
                "GH-01-0001": "01-01",
                "GH-01-0002": "01-02",
            },
        }

    def test_every_source_id_has_exactly_one_assignment(self):
        """Removing or duplicating a Skill ID must invalidate the ledger."""
        records = load_source_records(DATA_DIR)
        mapping = load_assignment_file(ASSIGNMENT_FILE)
        validate_assignments(records, mapping)

        self.assertEqual(len(records), 157)
        self.assertEqual(len(mapping["assignments"]), 157)
        self.assertEqual(set(mapping["assignments"]), {row["id"] for row in records})

    def test_subcategory_counts_match_approved_design(self):
        """Moving a Skill to the wrong task category must change this distribution."""
        records = enrich_with_subcategory(
            load_source_records(DATA_DIR),
            load_assignment_file(ASSIGNMENT_FILE),
        )

        self.assertEqual(
            Counter(row["subcategory_code"] for row in records),
            EXPECTED_SUBCATEGORY_COUNTS,
        )

    def test_assignment_mapping_matches_approved_id_to_code_ledger(self):
        """Swapping two IDs while preserving category totals must fail."""
        assignments = load_assignment_file(ASSIGNMENT_FILE)["assignments"]
        canonical = json.dumps(
            assignments,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        actual_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        self.assertEqual(actual_hash, APPROVED_ASSIGNMENT_SHA256)

    def test_taxonomy_and_big_category_totals_match_approved_design(self):
        """Omitting a category or shifting a Skill across big categories must fail."""
        mapping = load_assignment_file(ASSIGNMENT_FILE)
        records = enrich_with_subcategory(load_source_records(DATA_DIR), mapping)

        self.assertEqual(len(mapping["taxonomy"]), 61)
        self.assertEqual(
            Counter(row["subcategory_code"][:2] for row in records),
            {"01": 20, "02": 22, "03": 31, "04": 29, "05": 55},
        )

    def test_validate_rejects_missing_assignment_id(self):
        """Dropping a source Skill from the ledger must fail validation."""
        mapping = {**self.mapping, "assignments": {"GH-01-0001": "01-01"}}

        with self.assertRaisesRegex(ValueError, "missing=.*GH-01-0002"):
            validate_assignments(self.records, mapping)

    def test_validate_rejects_extra_assignment_id(self):
        """Adding a non-source Skill to the ledger must fail validation."""
        mapping = {
            **self.mapping,
            "assignments": {**self.mapping["assignments"], "GH-01-9999": "01-01"},
        }

        with self.assertRaisesRegex(ValueError, "extra=.*GH-01-9999"):
            validate_assignments(self.records, mapping)

    def test_validate_rejects_duplicate_source_id(self):
        """A repeated source ID cannot receive more than one ledger entry."""
        duplicate_records = [*self.records, {"id": "GH-01-0001"}]

        with self.assertRaisesRegex(ValueError, "重复 Skill ID"):
            validate_assignments(duplicate_records, self.mapping)

    def test_validate_rejects_unknown_subcategory_code(self):
        """A ledger entry outside the approved taxonomy must fail validation."""
        mapping = {
            **self.mapping,
            "assignments": {**self.mapping["assignments"], "GH-01-0002": "01-99"},
        }

        with self.assertRaisesRegex(ValueError, "未知小分类 01-99"):
            validate_assignments(self.records, mapping)

    def test_validate_rejects_cross_big_category_assignment(self):
        """A Skill may not be assigned to another big category's subcategory."""
        mapping = {
            **self.mapping,
            "assignments": {**self.mapping["assignments"], "GH-01-0002": "02-01"},
        }

        with self.assertRaisesRegex(ValueError, "大分类不一致"):
            validate_assignments(self.records, mapping)

    def test_validate_rejects_duplicate_taxonomy_code(self):
        """Two taxonomy rows with one code must fail rather than overwrite."""
        mapping = {
            **self.mapping,
            "taxonomy": [
                *self.mapping["taxonomy"],
                {"code": "01-01", "name": "重复", "inclusion_focus": "测试"},
            ],
        }

        with self.assertRaisesRegex(ValueError, "小分类代码重复"):
            validate_assignments(self.records, mapping)

    def test_load_rejects_duplicate_assignment_key_in_json(self):
        """A repeated JSON assignment key must not be silently overwritten."""
        duplicate_json = '''{
          "taxonomy": [{"code": "01-01", "name": "规划", "inclusion_focus": "测试"}],
          "assignments": {"GH-01-0001": "01-01", "GH-01-0001": "01-02"}
        }'''
        with tempfile.TemporaryDirectory() as temporary_directory:
            assignment_path = Path(temporary_directory) / "duplicate-key.json"
            assignment_path.write_text(duplicate_json, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "重复 JSON 键.*GH-01-0001"):
                load_assignment_file(assignment_path)


class PlainLanguageCatalogTests(unittest.TestCase):
    def test_plain_records_answer_user_questions_without_changing_facts(self):
        """Dropping a user field or rewriting a source fact must fail."""
        plain = simplify_record(SAMPLE_RECORD)

        self.assertTrue(PLAIN_FIELDS.issubset(plain))
        self.assertTrue(all(str(plain[field]).strip() for field in PLAIN_FIELDS))
        self.assertIn("未安装", plain["plain_verification"])
        self.assertIn("未运行", plain["plain_verification"])
        for key, value in SAMPLE_RECORD.items():
            self.assertEqual(plain[key], value, key)

    def test_technical_terms_are_explained_on_first_use(self):
        """Leaving a supported abbreviation unexplained must fail the audit."""
        plain = simplify_record({
            **SAMPLE_RECORD,
            "summary": "通过 MCP 和 API 检索资料并建立 RAG 知识库。",
            "scenario": "使用 OCR 整理资料并通过 ETL 汇总。",
            "deps": "需要 MLOps 流程。",
        })
        joined = " ".join(str(plain[key]) for key in PLAIN_FIELDS)

        self.assertIn("MCP（让 AI 连接外部工具的通用方式）", joined)
        self.assertIn("API（软件之间交换信息的接口）", joined)
        self.assertIn("OCR（把图片中的文字识别为可编辑文本）", joined)
        self.assertIn("RAG（先查资料再生成回答的方法）", joined)
        self.assertIn("MLOps（管理机器学习模型开发和维护的流程）", joined)
        self.assertIn("ETL（抽取、整理并保存数据的流程）", joined)
        self.assertEqual(readability_issues(plain), [])

    def test_readability_audit_catches_each_approved_risk(self):
        """Removing any readability guard must let a specified defect escape."""
        base = {field: "清楚说明具体用途。" for field in PLAIN_FIELDS}
        cases = {
            "empty": ({**base, "plain_purpose": ""}, "字段为空"),
            "placeholder": ({**base, "plain_purpose": "TODO"}, "占位或空话"),
            "audit_tail": (
                {**base, "plain_purpose": "本轮读取了 20 行说明。"},
                "审计尾句",
            ),
            "abbreviation": ({**base, "plain_purpose": "使用 API 查询。"}, "未解释缩写"),
            "long_paragraph": (
                {**base, "plain_purpose": "字" * 181},
                "单段超过 180 个汉字",
            ),
            "verification_overclaim": (
                {**base, "plain_verification": "说明核验后确认运行成功。"},
                "误写核验状态",
            ),
            "technical_jargon": (
                {**base, "plain_integration": "需要适配路由、编排、脚手架和门禁。"},
                "未转换技术措辞",
            ),
        }

        for name, (record, expected_issue) in cases.items():
            with self.subTest(name=name):
                self.assertTrue(
                    any(expected_issue in issue for issue in readability_issues(record)),
                    readability_issues(record),
                )

    def test_write_plain_catalog_covers_157_records_without_fact_drift(self):
        """Omitting a Skill, emitting boilerplate, or changing a fact must fail."""
        source_records = enrich_with_subcategory(
            load_source_records(DATA_DIR),
            load_assignment_file(ASSIGNMENT_FILE),
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "plain.json"
            write_plain_catalog(output_path, source_records)
            plain_records = json.loads(output_path.read_text(encoding="utf-8"))

        self.assertEqual(len(plain_records), 157)
        self.assertEqual(len({row["id"] for row in plain_records}), 157)
        self.assertEqual(
            Counter(row["subcategory_code"] for row in plain_records),
            EXPECTED_SUBCATEGORY_COUNTS,
        )
        self.assertEqual(len({row["plain_purpose"] for row in plain_records}), 157)
        self.assertFalse([
            (row["id"], readability_issues(row))
            for row in plain_records
            if readability_issues(row)
        ])
        source_by_id = {row["id"]: row for row in source_records}
        for plain in plain_records:
            for key, value in source_by_id[plain["id"]].items():
                self.assertEqual(plain[key], value, f"{plain['id']}:{key}")


if __name__ == "__main__":
    unittest.main()
