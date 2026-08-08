import hashlib
import json
import re
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "03_候选池" / "deduplicated"
ASSIGNMENT_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_assignments.json"
OUTPUT_CONTRACT_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "plain_output_contract.json"
sys.path.insert(0, str(PROJECT_ROOT / "06_过程记录" / "tools"))

import subcategory_pipeline as pipeline
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
# Frozen after the 157-record, source-field-by-source-field human audit in repair
# round 2.  These literals are deliberately independent from the runtime contract.
APPROVED_OUTPUT_CONTRACT_SHA256 = "d67e83360ffbf3c51359fa99495703245f8d59dc213f4614a06625e745039b31"
APPROVED_OUTPUT_CONTRACT_CATEGORY_SHA256 = {
    "01": "3f3f945340cbfa74becde5c01b170f1c21ebbd623d4b961923efde4ea14f3be7",
    "02": "b471937a909a9462ace32dfe6c0e8ef935375621352969badde499c8b0ff32f7",
    "03": "3f4d9eb05cc2b2008d4c9d159d5337584a0b840c31971109ec5a00149ff2aa5a",
    "04": "8d0b6ce92e0165009e8eb76c8feb2731d1487615a9b6fb56446914124d34e8be",
    "05": "6a9d239997517b3a0405f564eb5c191dcd57aa1a0f00bdf00f6bb38157d4e0e5",
}
PLAIN_FIELDS = {
    "plain_purpose",
    "plain_audience",
    "plain_when_to_use",
    "plain_prerequisites",
    "plain_limitations",
    "plain_integration",
    "plain_verification",
    "plain_outputs",
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
    def _actual_plain_records(self):
        source_records = enrich_with_subcategory(
            load_source_records(DATA_DIR),
            load_assignment_file(ASSIGNMENT_FILE),
        )
        return [simplify_record(record) for record in source_records]

    def _output_contract(self):
        return json.loads(OUTPUT_CONTRACT_FILE.read_text(encoding="utf-8"))["records"]

    @staticmethod
    def _output_contract_snapshot_hash(records):
        canonical = json.dumps(
            records,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

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

    def test_specialist_ranges_do_not_reuse_generic_multi_field_profiles(self):
        """Restoring the two source-level bulk templates must fail multiple fields."""
        by_id = {row["id"]: row for row in self._actual_plain_records()}
        groups = [
            [f"GH-05-{number:04d}" for number in range(1, 28)],
            [f"GH-05-{number:04d}" for number in range(32, 46)],
        ]
        fields = (
            "plain_when_to_use",
            "plain_prerequisites",
            "plain_limitations",
            "plain_integration",
        )

        def semantic_core(text):
            text = re.sub(r"[A-Za-z0-9_.+/-]+", "", text)
            for boilerplate in (
                "基本可以直接放入现有工作台使用但仍需按本校制度和工具设置进行检查",
                "经过少量调整后可以使用常见调整包括更换工具路径或账号设置",
                "具体建议",
                "适用于",
                "需要准备",
                "需要注意",
            ):
                text = text.replace(boilerplate, "")
            return re.sub(r"\W+", "", text)

        for group in groups:
            for field in fields:
                cores = [semantic_core(by_id[skill_id][field]) for skill_id in group]
                with self.subTest(first=group[0], field=field):
                    self.assertEqual(len(set(cores)), len(group), cores)

    def test_repaired_profiles_contain_skill_specific_decision_information(self):
        """Replacing only a product name must not satisfy purpose-to-profile matching."""
        by_id = {row["id"]: row for row in self._actual_plain_records()}
        expected = {
            "GH-05-0001": {
                "plain_when_to_use": ("算力", "开跑"),
                "plain_prerequisites": ("查看系统信息",),
                "plain_limitations": ("资源快照",),
                "plain_integration": ("只查看", "不自动修改"),
            },
            "GH-05-0014": {
                "plain_when_to_use": ("样本量",),
                "plain_prerequisites": ("目标效应", "显著性水平"),
                "plain_limitations": ("假设",),
                "plain_integration": ("研究设计",),
            },
            "GH-05-0027": {
                "plain_when_to_use": ("预训练模型",),
                "plain_prerequisites": ("模型来源", "任务数据"),
                "plain_limitations": ("版本", "授权"),
                "plain_integration": ("小样本", "评估"),
            },
            "GH-05-0033": {
                "plain_when_to_use": ("数据表",),
                "plain_prerequisites": ("字段", "访问规则"),
                "plain_limitations": ("迁移",),
                "plain_integration": ("测试库",),
            },
            "GH-05-0039": {
                "plain_when_to_use": ("测试",),
                "plain_prerequisites": ("待测代码",),
                "plain_limitations": ("模拟",),
                "plain_integration": ("现有测试",),
            },
            "GH-04-0029": {
                "plain_when_to_use": ("Zotero", "目标网站"),
                "plain_prerequisites": ("样例网页",),
                "plain_limitations": ("网站改版", "访问限制"),
                "plain_integration": ("测试记录",),
            },
        }
        for skill_id, field_anchors in expected.items():
            for field, anchors in field_anchors.items():
                with self.subTest(skill_id=skill_id, field=field):
                    self.assertTrue(
                        all(anchor in by_id[skill_id][field] for anchor in anchors),
                        by_id[skill_id][field],
                    )

    def test_every_record_states_a_concrete_output(self):
        """A non-empty but generic outcome sentence must not satisfy the contract."""
        output_types = re.compile(
            r"报告|清单|检索结果|文献记录|数据表|图表|方案|计划|草稿|修订稿|"
            r"回复信|代码|配置|模型|预测结果|分析结果|审查意见|证明|演示文稿|"
            r"文档|工作簿|转换文件|术语结果|证据包|流程图|结构图|测试结果|规则|"
            r"元数据|综述|记录|概率"
        )
        forbidden = ("相关结果", "相应成果", "具体形式见", "满足需求")
        for row in self._actual_plain_records():
            with self.subTest(skill_id=row["id"]):
                output = row.get("plain_outputs", "")
                self.assertTrue(output_types.search(output), output)
                self.assertFalse(any(text in output for text in forbidden))

        by_id = {row["id"]: row for row in self._actual_plain_records()}
        self.assertRegex(by_id["GH-01-0014"].get("plain_outputs", ""), r"论文.*(?:草稿|修订稿)|回复信")
        self.assertRegex(by_id["GH-03-0019"].get("plain_outputs", ""), r"引用.*(?:调研报告|政策简报|主题综述)")

    def test_every_output_matches_its_independently_audited_id_contract(self):
        """A subcategory-generic output must not satisfy a Skill-specific source audit."""
        source_ids = {row["id"] for row in load_source_records(DATA_DIR)}
        contract = self._output_contract()
        self.assertEqual(set(contract), source_ids)
        self.assertEqual(len({item["output"] for item in contract.values()}), 157)

        for skill_id, item in contract.items():
            with self.subTest(skill_id=skill_id, part="shape"):
                self.assertEqual(set(item), {"output", "anchors"})
                self.assertGreaterEqual(len(item["anchors"]), 2)
                self.assertTrue(all(anchor in item["output"] for anchor in item["anchors"]))

        by_id = {row["id"]: row for row in self._actual_plain_records()}
        for skill_id, item in contract.items():
            with self.subTest(skill_id=skill_id, part="generated_contract"):
                self.assertEqual(pipeline.output_contract_issues(by_id[skill_id], contract), [])

    def test_output_contract_matches_frozen_source_audit_snapshot(self):
        """Editing the runtime contract and regenerating output must not move the gold standard."""
        contract = self._output_contract()
        self.assertEqual(
            self._output_contract_snapshot_hash(contract),
            APPROVED_OUTPUT_CONTRACT_SHA256,
        )
        for category_code, approved_hash in APPROVED_OUTPUT_CONTRACT_CATEGORY_SHA256.items():
            category_records = {
                skill_id: item
                for skill_id, item in contract.items()
                if skill_id.startswith(f"GH-{category_code}-")
            }
            with self.subTest(category=category_code):
                self.assertEqual(
                    self._output_contract_snapshot_hash(category_records),
                    approved_hash,
                )

        swapped = json.loads(json.dumps(contract, ensure_ascii=False))
        swapped["GH-02-0009"], swapped["GH-05-0046"] = (
            swapped["GH-05-0046"],
            swapped["GH-02-0009"],
        )
        generic = json.loads(json.dumps(contract, ensure_ascii=False))
        generic["GH-02-0009"]["output"] = "可得到分析报告、图表或行动建议。"
        self.assertNotEqual(
            self._output_contract_snapshot_hash(swapped),
            APPROVED_OUTPUT_CONTRACT_SHA256,
        )
        self.assertNotEqual(
            self._output_contract_snapshot_hash(generic),
            APPROVED_OUTPUT_CONTRACT_SHA256,
        )

    def test_output_contract_rejects_swapped_and_generic_results(self):
        """Swapping two plausible artifact sentences or using type-only prose must fail."""
        self.assertTrue(hasattr(pipeline, "output_contract_issues"))
        checker = pipeline.output_contract_issues
        contract = self._output_contract()
        by_id = {row["id"]: row for row in self._actual_plain_records()}

        for skill_id in ("GH-02-0009", "GH-05-0046"):
            with self.subTest(skill_id=skill_id, mutation="generic"):
                mutated = {**by_id[skill_id], "plain_outputs": "可得到分析报告、图表或行动建议。"}
                self.assertTrue(checker(mutated, contract))

        first = {**by_id["GH-02-0009"], "plain_outputs": by_id["GH-05-0046"]["plain_outputs"]}
        second = {**by_id["GH-05-0046"], "plain_outputs": by_id["GH-02-0009"]["plain_outputs"]}
        self.assertTrue(checker(first, contract))
        self.assertTrue(checker(second, contract))

    def test_office_embedded_objects_are_not_explained_as_vector_embeddings(self):
        """A global 'embedding' explanation must not corrupt Office document risks."""
        row = next(
            item for item in self._actual_plain_records()
            if item["id"] == "GH-02-0015"
        )
        self.assertIn(
            "嵌入对象（放在 Office 文件内的图片、图表或其他内容）",
            row["plain_limitations"],
        )
        self.assertNotIn("把复杂数据转成便于比较的一组数字", row["plain_limitations"])

    def test_later_explanation_does_not_rescue_unexplained_first_use(self):
        """Moving a term explanation to a later field must fail first-use auditing."""
        plain = simplify_record(SAMPLE_RECORD)
        plain["plain_purpose"] = "使用 API 查询资料。"
        plain["plain_prerequisites"] = "API（软件之间交换信息的接口）已由技术人员配置。"

        self.assertTrue(
            any("首次出现未解释" in issue for issue in readability_issues(plain)),
            readability_issues(plain),
        )

    def test_required_product_terms_are_explained_where_they_first_appear(self):
        """Dropping nearby explanations for audited product terms must fail."""
        by_id = {row["id"]: row for row in self._actual_plain_records()}
        self.assertIn(
            "python-docx（自动创建和修改 Word 文档的软件）",
            by_id["GH-02-0010"]["plain_purpose"],
        )
        self.assertIn(
            "GitHub Release（项目维护者正式发布的版本包）",
            by_id["GH-01-0020"]["plain_limitations"],
        )
        self.assertIn(
            "humanize（让机器生成文本更接近自然表达的处理步骤）",
            by_id["GH-01-0020"]["plain_limitations"],
        )
        self.assertIn(
            "APA（常用于学术写作的引用格式）",
            by_id["GH-03-0019"]["plain_outputs"],
        )
        self.assertIn(
            "Spark（把大数据任务分散处理的软件）",
            by_id["GH-05-0036"]["plain_purpose"],
        )
        self.assertIn(
            "TypeScript（在 JavaScript 基础上增加类型检查的编程语言）",
            by_id["GH-05-0045"]["plain_outputs"],
        )

    def test_plain_chinese_has_no_lint_replacement_artifact(self):
        """Reintroducing the mechanical '本地 lint' replacement must fail."""
        by_id = {row["id"]: row for row in self._actual_plain_records()}
        self.assertIn("人工确认和本地自动文字检查", by_id["GH-01-0010"]["plain_integration"])
        for row in by_id.values():
            joined = " ".join(str(row.get(field, "")) for field in PLAIN_FIELDS)
            self.assertNotRegex(joined, r"本地\s+自动文字检查")
            self.assertNotIn("。 具体建议", joined)

    def test_all_plain_fields_remove_mechanical_spaces_around_chinese_punctuation(self):
        """A new Chinese sentence must not reintroduce punctuation-space artifacts."""
        mechanical_spacing = re.compile(r"(?:[。，；：！？]\s+|\s+[。，；：！？])")
        for row in self._actual_plain_records():
            for field in PLAIN_FIELDS:
                with self.subTest(skill_id=row["id"], field=field):
                    self.assertNotRegex(row[field], mechanical_spacing)


if __name__ == "__main__":
    unittest.main()
