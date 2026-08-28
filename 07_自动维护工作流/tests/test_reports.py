"""Task 10: Chinese daily reports and affected-scope deliveries."""

from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
import tempfile
import unittest

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from openpyxl import load_workbook

from skill_maintainer.reports import (
    DAILY_SHEETS,
    DAILY_WORD_SECTIONS,
    affected_scopes,
    build_daily_docx,
    build_daily_xlsx,
    build_scope_deliveries,
)


NODE = Path(r"C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe")
NODE_MODULES = Path(r"C:\Users\34927\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules")


def formal_row(index: int, scope: str = "0809 计算机类") -> dict[str, object]:
    return {
        "内部标识": f"GH-05-{index:04d}",
        "Skill名称": f"campus-data-{index}",
        "规范名称": f"Campus Data Skill {index}",
        "固定版本": f"v1.{index}",
        "许可证": "Apache-2.0",
        "Canonical source": f"https://github.com/example/campus-data-{index}",
        "简要功能": "面向高校数据治理任务提供结构化分析。",
        "详细功能摘要": "读取课程数据并输出可审计的中文分析结果。",
        "适用用户角色": "教师、科研人员和数据管理员",
        "典型高校场景": "课程质量分析",
        "外部依赖": "Python",
        "安全限制条件": "仅处理已授权数据，不上传敏感教学数据。",
        "适配建议": "先在隔离环境复核输入字段。",
        "专业类": scope,
        "用途": "课程数据质量检查",
        "输入": "脱敏后的课程数据表",
        "输出": "中文质量报告和问题清单",
        "使用限制": "不得输入学生个人敏感信息",
        "专业任务": "课程数据治理",
        "收集日期": datetime(2026, 8, 28),
    }


def report_summary(count: int = 2) -> dict[str, object]:
    rows = [formal_row(index) for index in range(1, count + 1)]
    return {
        "run_id": "run-20260828-220000",
        "generated_at": datetime(2026, 8, 28, 22, 0),
        "source_statuses": {
            "SkillHub": "complete",
            "ClawHub": "partial",
            "GitHub": "complete",
            "Hugging Face Spaces": "failed",
        },
        "catalog_changes": [{"专业类": "0809 计算机类", "变化": "专业任务范围已复核"}],
        "formal_additions": rows,
        "version_updates": [{**rows[0], "原版本": "v1.0", "新版本": "v1.1"}],
        "updates_not_applied": [{**rows[0], "发现版本": "v2.0", "原因": "证据不足"}],
        "conditional_candidates": [{**rows[0], "内部标识": "COND-0001", "结论": "条件候选"}],
        "adaptation_candidates": [{**rows[0], "内部标识": "ADAPT-0001", "结论": "需适配候选"}],
        "aliases": [{"内部标识": rows[0]["内部标识"], "来源平台": "SkillHub", "来源地址": "https://skillhub.example/item/1"}],
        "affected_scopes": ["0809 计算机类"],
        "exclusions": [{"候选名称": "绝不能泄露的落选项目名", "原因": "许可证不明确"}],
        "manual_reviews": [{"事项": "ClawHub 覆盖降级，需人工复核"}],
        "source_requests": [{"来源平台": "GitHub", "请求地址": "https://api.github.com/search/repositories?q=campus", "状态": "200", "请求时间": datetime(2026, 8, 28, 21, 50)}],
    }


class ReportContentTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.old_node = os.environ.get("SKILL_MAINTAINER_NODE")
        self.old_modules = os.environ.get("SKILL_MAINTAINER_NODE_MODULES")
        os.environ["SKILL_MAINTAINER_NODE"] = str(NODE)
        os.environ["SKILL_MAINTAINER_NODE_MODULES"] = str(NODE_MODULES)
        self.addCleanup(self._restore_environment)

    def _restore_environment(self) -> None:
        if self.old_node is None:
            os.environ.pop("SKILL_MAINTAINER_NODE", None)
        else:
            os.environ["SKILL_MAINTAINER_NODE"] = self.old_node
        if self.old_modules is None:
            os.environ.pop("SKILL_MAINTAINER_NODE_MODULES", None)
        else:
            os.environ["SKILL_MAINTAINER_NODE_MODULES"] = self.old_modules

    def test_word_contains_fixed_sections_chinese_fields_and_non_execution_boundary(self):
        output = self.root / "日报.docx"
        build_daily_docx(report_summary(), output)
        document = Document(output)
        headings = [p.text for p in document.paragraphs if p.style.name == "Heading 1"]
        self.assertEqual(headings, list(DAILY_WORD_SECTIONS))
        text = "\n".join(p.text for p in document.paragraphs)
        text += "\n" + "\n".join(cell.text for table in document.tables for row in table.rows for cell in row.cells)
        for required in (
            "用途", "适用人员", "输入", "输出", "限制", "Campus Data Skill 1",
            "Apache-2.0", "https://github.com/example/campus-data-1", "未安装、未运行",
        ):
            self.assertIn(required, text)
        self.assertNotIn("绝不能泄露的落选项目名", text)
        section = document.sections[0]
        self.assertEqual((section.page_width, section.page_height), (Inches(8.5), Inches(11)))
        self.assertEqual(
            (section.top_margin, section.right_margin, section.bottom_margin, section.left_margin),
            (Inches(1), Inches(1), Inches(1), Inches(1)),
        )
        normal = document.styles["Normal"]
        self.assertEqual((normal.font.name, normal.font.size), ("Calibri", Pt(11)))
        self.assertEqual((normal.paragraph_format.space_after, normal.paragraph_format.line_spacing), (Pt(6), 1.1))
        expected_styles = {
            "Heading 1": (Pt(16), "2E74B5", Pt(16), Pt(8)),
            "Heading 2": (Pt(13), "2E74B5", Pt(12), Pt(6)),
            "Heading 3": (Pt(12), "1F4D78", Pt(8), Pt(4)),
        }
        for name, expected in expected_styles.items():
            style = document.styles[name]
            actual = (style.font.size, str(style.font.color.rgb), style.paragraph_format.space_before, style.paragraph_format.space_after)
            self.assertEqual(actual, expected)
        for paragraph in (p for p in document.paragraphs if p.style.name == "Heading 1"):
            self.assertIsNotNone(paragraph._p.pPr.find(qn("w:numPr")))
        self.assertNotIn("w:pBdr", section.header._element.xml)
        for table in document.tables:
            self.assertIn('w:w="9360"', table._tbl.tblPr.xml)
            self.assertIn('w:w="120"', table._tbl.tblPr.xml)

    def test_excel_has_exact_sheets_dynamic_520_row_tables_and_operational_features(self):
        output = self.root / "日报.xlsx"
        summary = report_summary(520)
        build_daily_xlsx(summary, output)
        workbook = load_workbook(output, data_only=False)
        self.addCleanup(workbook.close)
        self.assertEqual(workbook.sheetnames, list(DAILY_SHEETS))
        for sheet in workbook:
            self.assertEqual(sheet.freeze_panes, "A2", sheet.title)
            self.assertEqual(len(sheet.tables), 1, sheet.title)
        formal = workbook["新增正式推荐"]
        self.assertEqual(formal.max_row, 521)
        self.assertEqual(formal["A521"].value, "GH-05-0520")
        self.assertEqual(len({formal.cell(row, 1).value for row in range(2, 522)}), 520)
        self.assertEqual(formal.freeze_panes, "A2")
        self.assertEqual(len(formal.tables), 1)
        self.assertTrue(next(iter(formal.tables.values())).ref.endswith("521"))
        self.assertEqual(formal["G2"].value, "https://github.com/example/campus-data-1")
        self.assertEqual(formal["G2"].hyperlink.target, "https://github.com/example/campus-data-1")
        self.assertTrue(formal["H2"].alignment.wrap_text)
        self.assertEqual(formal["N2"].number_format, "yyyy-mm-dd")
        overview = workbook["执行概览"]
        self.assertEqual(overview["B3"].value, datetime(2026, 8, 28, 22, 0))
        formulas = [cell.value for row in overview.iter_rows() for cell in row if isinstance(cell.value, str) and cell.value.startswith("=")]
        self.assertTrue(any("521" in formula for formula in formulas), formulas)
        self.assertEqual(overview["B5"].value, 520)
        self.assertNotIn("绝不能泄露的落选项目名", "\n".join(str(cell.value or "") for sheet in workbook for row in sheet.iter_rows() for cell in row))

    def test_affected_scope_refresh_is_material_and_alias_only_is_not(self):
        base_skill = formal_row(1, "0801 力学类")
        before = {
            "当前Skill": [base_skill],
            "专业任务映射": [{"内部标识": base_skill["内部标识"], "专业类": "0801 力学类", "专业任务": "建模"}],
            "来源别名": [],
            "目录基线": [{"目录版本": "2025", "专业类": "0801 力学类"}],
        }
        alias_after = {**before, "来源别名": [{"内部标识": base_skill["内部标识"], "来源地址": "https://skillhub.example/alias"}]}
        self.assertEqual(affected_scopes(before, alias_after), ())

        cases = []
        added = formal_row(2, "0809 计算机类")
        cases.append({**before, "当前Skill": [base_skill, added], "专业任务映射": before["专业任务映射"] + [{"内部标识": added["内部标识"], "专业类": "0809 计算机类", "专业任务": "数据分析"}]})
        cases.append({**before, "当前Skill": [{**base_skill, "固定版本": "v2.0"}]})
        cases.append({**before, "当前Skill": [{**base_skill, "许可证": "BSD-3-Clause"}]})
        cases.append({**before, "当前Skill": [{**base_skill, "安全等级": "SB"}]})
        cases.append({**before, "专业任务映射": [{**before["专业任务映射"][0], "专业任务": "实验建模"}]})
        cases.append({**before, "目录基线": [{"目录版本": "2026", "专业类": "0801 力学类"}]})
        for after in cases:
            with self.subTest(after=after):
                self.assertTrue(affected_scopes(before, after))

    def test_scope_deliveries_reference_same_stable_ids_without_master_duplication(self):
        shared = formal_row(1, "0809 计算机类")
        ledger = {
            "当前Skill": [shared],
            "专业任务映射": [
                {"内部标识": shared["内部标识"], "专业类": "0809 计算机类", "专业任务": "课程分析", "输入": "课程表", "输出": "报告", "使用限制": "脱敏"},
                {"内部标识": shared["内部标识"], "专业类": "0201 经济学类", "专业任务": "计量分析", "输入": "统计表", "输出": "报告", "使用限制": "脱敏"},
            ],
        }
        paths = build_scope_deliveries(("0809 计算机类", "0201 经济学类"), ledger, self.root / "受影响专业类")
        self.assertEqual(len(paths), 4)
        for path in paths:
            self.assertTrue(path.exists())
        for docx_path in (path for path in paths if path.suffix == ".docx"):
            document = Document(docx_path)
            text = "\n".join(p.text for p in document.paragraphs)
            text += "\n" + "\n".join(cell.text for table in document.tables for row in table.rows for cell in row.cells)
            self.assertEqual(text.count("GH-05-0001"), 1)

    def test_committed_xlsx_template_reopens_with_all_required_sheets(self):
        template = Path(__file__).parents[1] / "templates" / "daily_review.xlsx"
        workbook = load_workbook(template, data_only=False)
        self.addCleanup(workbook.close)
        self.assertEqual(workbook.sheetnames, list(DAILY_SHEETS))
        self.assertEqual(workbook["使用说明"]["A2"].value, "报告用途")


if __name__ == "__main__":
    unittest.main()
