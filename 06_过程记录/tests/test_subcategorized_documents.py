"""Contract tests for the plain-language subcategory DOCX pipeline."""

from __future__ import annotations

import hashlib
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = PROJECT_ROOT / "06_过程记录" / "tools"
BUILDER_PATH = TOOLS_DIR / "build_subcategorized_documents.py"
VERIFIER_PATH = TOOLS_DIR / "verify_subcategorized_documents.py"
RENDERER_PATH = TOOLS_DIR / "render_subcategorized_documents.py"


def load_module(path: Path, name: str):
    """Load a task module only after asserting that the planned artifact exists."""
    if not path.exists():
        raise AssertionError(f"缺少计划脚本: {path.name}")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def fixture_record(skill_id: str, *, subcategory_code: str = "05-05", suffix: str = "") -> dict:
    number = int(skill_id.rsplit("-", 1)[1])
    long_note = (
        "先在一份可公开的样例任务上记录基线耗时，再逐项调整处理器数量、显存占用和批次大小；"
        "每次只改变一个条件，并把结果写进同一份比较记录。"
    )
    return {
        "id": skill_id,
        "name": f"parallel-tool-{number}{suffix}",
        "cn": f"并行计算工具 {number}",
        "cat": "05",
        "repo": f"example/repository-{number}",
        "path": f"skills/parallel-tool-{number}/SKILL.md",
        "ecosystem": "Agent Skills（兼容 Codex）",
        "form": "社区 skill、开源仓库",
        "tags": "并行计算、性能分析",
        "summary": "使用多个处理器缩短计算时间。",
        "detail": "按任务特点分配计算资源，并保留可比较的运行记录。",
        "roles": f"适合科研人员、数据分析人员 {number} 使用。",
        "scenario": "批量模拟、模型训练、数据转换",
        "compat": "A",
        "adapt": "先用小样例核对结果，再逐步增加工作量。",
        "deps": "可公开的样例数据、可用的处理器或显卡、基线运行记录",
        "risk": "并行任务可能增加内存占用；结果仍需与单任务版本比较。",
        "verify": "二级包内容验证",
        "priority": "高" if number % 2 else "中",
        "related": "",
        "repo_url": f"https://github.com/example/repository-{number}?tab=readme-ov-file&source=very-long-address-{number}",
        "skill_url": f"https://github.com/example/repository-{number}/blob/main/skills/parallel-tool-{number}/SKILL.md?plain=1&source=very-long-address-{number}",
        "stars": number * 10,
        "repo_pushed": "2026-08-03",
        "license": "MIT",
        "subcategory_code": subcategory_code,
        "subcategory_name": "并行计算与性能优化",
        "plain_purpose": f"把可拆分的计算任务分给多个处理器，缩短等待时间 {number}。",
        "plain_outputs": f"可得到性能比较报告、资源使用记录和调整建议 {number}。",
        "plain_audience": f"适合科研人员、数据分析人员 {number} 使用。",
        "plain_when_to_use": f"当单次计算等待时间较长、任务能够拆分时值得使用 {number}。",
        "plain_prerequisites": f"需要准备：可公开的样例数据、基线耗时和可用计算资源 {number}。",
        "plain_limitations": f"需要注意：{long_note}{number}。",
        "plain_integration": f"需要中等调整：先接入一条任务，再比较结果一致性和资源占用 {number}。",
        "plain_verification": "包内容已核验：已核对用途说明和包内文件；本次未安装、未运行，不能据此判断实际效果。",
    }


OVERVIEW = {
    "code": "05",
    "name": "编程、数学、数据分析和可视化",
    "subcategories": [
        {
            "code": "05-01",
            "name": "计算设备与资源规划",
            "inclusion_focus": "检查处理器、显卡、内存和磁盘，并据此安排计算任务",
        },
        {
            "code": "05-05",
            "name": "并行计算与性能优化",
            "inclusion_focus": "使用多个处理器或显卡加快计算，并查找性能瓶颈",
        },
    ],
}

SUBCATEGORY = {
    "code": "05-05",
    "name": "并行计算与性能优化",
    "inclusion_focus": "使用多个处理器或显卡加快计算，并查找性能瓶颈",
    "big_category_name": "编程、数学、数据分析和可视化",
}


def document_xml(document: Document) -> str:
    with tempfile.TemporaryDirectory() as temporary_directory:
        path = Path(temporary_directory) / "artifact.docx"
        document.save(path)
        with zipfile.ZipFile(path) as package:
            return package.read("word/document.xml").decode("utf-8")


def all_document_text(document: Document) -> str:
    parts = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        parts.extend(cell.text for row in table.rows for cell in row.cells)
    return "\n".join(parts)


class PlannedScriptsTests(unittest.TestCase):
    def test_all_three_planned_scripts_exist(self):
        """Removing any pipeline stage must make the documented workflow unusable."""
        self.assertTrue(BUILDER_PATH.exists(), f"缺少 {BUILDER_PATH.name}")
        self.assertTrue(VERIFIER_PATH.exists(), f"缺少 {VERIFIER_PATH.name}")
        self.assertTrue(RENDERER_PATH.exists(), f"缺少 {RENDERER_PATH.name}")


class DocumentLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_module(BUILDER_PATH, "build_subcategorized_documents_for_test")
        cls.records = [fixture_record("GH-05-0003"), fixture_record("GH-05-0024")]
        cls.document = cls.builder.build_subcategory_document(SUBCATEGORY, cls.records)

    def test_letter_geometry_and_compact_reference_styles_are_encoded(self):
        """A default Word template or style drift must fail the preset contract."""
        section = self.document.sections[0]
        self.assertEqual((section.page_width.twips, section.page_height.twips), (12240, 15840))
        self.assertEqual(
            tuple(value.twips for value in (section.top_margin, section.right_margin, section.bottom_margin, section.left_margin)),
            (1440, 1440, 1440, 1440),
        )
        normal = self.document.styles["Normal"]
        self.assertEqual(normal.font.name, "Calibri")
        self.assertEqual(normal._element.rPr.rFonts.get(qn("w:eastAsia")), "Microsoft YaHei")
        self.assertEqual(normal.font.size.pt, 11)
        self.assertEqual(normal.paragraph_format.space_after.pt, 6)
        self.assertEqual(normal.paragraph_format.line_spacing, 1.25)

        expected = {
            "Heading 1": (16, "2E74B5", 18, 10),
            "Heading 2": (13, "2E74B5", 14, 7),
            "Heading 3": (12, "1F4D78", 10, 5),
        }
        for style_name, (size, color, before, after) in expected.items():
            style = self.document.styles[style_name]
            with self.subTest(style=style_name):
                self.assertEqual(style.font.name, "Calibri")
                self.assertEqual(style._element.rPr.rFonts.get(qn("w:eastAsia")), "Microsoft YaHei")
                self.assertEqual(style.font.size.pt, size)
                self.assertEqual(str(style.font.color.rgb), color)
                self.assertEqual(style.paragraph_format.space_before.pt, before)
                self.assertEqual(style.paragraph_format.space_after.pt, after)

    def test_every_table_has_fixed_full_width_geometry_and_indent(self):
        """Autofit, percentage widths, or mismatched cells must fail XML inspection."""
        self.assertGreater(len(self.document.tables), 0)
        for table in self.document.tables:
            table_width = table._tbl.tblPr.find(qn("w:tblW"))
            table_indent = table._tbl.tblPr.find(qn("w:tblInd"))
            layout = table._tbl.tblPr.find(qn("w:tblLayout"))
            grid_widths = [int(node.get(qn("w:w"))) for node in table._tbl.tblGrid]
            with self.subTest(table=table):
                self.assertEqual((table_width.get(qn("w:type")), int(table_width.get(qn("w:w")))), ("dxa", 9360))
                self.assertEqual((table_indent.get(qn("w:type")), int(table_indent.get(qn("w:w")))), ("dxa", 120))
                self.assertEqual(layout.get(qn("w:type")), "fixed")
                self.assertEqual(sum(grid_widths), 9360)
                for row in table.rows:
                    self.assertIsNone(row._tr.get_or_add_trPr().find(qn("w:trHeight")))
                    for index, cell in enumerate(row.cells):
                        self.assertEqual(int(cell._tc.get_or_add_tcPr().tcW.get(qn("w:w"))), grid_widths[index])

    def test_editorial_cover_header_footer_and_page_number_are_present(self):
        """Losing the cover metadata, quiet header, or real PAGE field must fail."""
        cover_text = "\n".join(paragraph.text for paragraph in self.document.paragraphs[:12])
        self.assertIn("并行计算与性能优化", cover_text)
        self.assertIn("通俗版", cover_text)
        self.assertIn("2026-08-07", cover_text)
        self.assertIn("收录 2 项", cover_text)
        self.assertIn("未安装、未运行", cover_text)
        header_text = "".join(paragraph.text for paragraph in self.document.sections[0].header.paragraphs)
        self.assertEqual(header_text.strip(), "并行计算与性能优化")
        footer_xml = self.document.sections[0].footer._element.xml
        self.assertIn("PAGE", footer_xml)


class DocumentContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_module(BUILDER_PATH, "build_subcategorized_documents_content_test")

    def test_overview_uses_plain_fields_in_the_required_section_order(self):
        """Reverting to technical source prose or rearranging reader questions must fail."""
        records = [
            fixture_record("GH-05-0001", subcategory_code="05-01"),
            fixture_record("GH-05-0003"),
            fixture_record("GH-05-0024"),
        ]
        document = self.builder.build_overview_document(OVERVIEW, records)
        headings = [paragraph.text for paragraph in document.paragraphs if paragraph.style.name == "Heading 1"]
        self.assertEqual(
            headings,
            [
                "这类工具解决什么问题",
                "适合哪些人",
                "小分类导航与数量",
                "怎样选择",
                "共同使用条件",
                "共同限制",
                "本次核验到哪一步",
                "来源说明",
            ],
        )
        text = all_document_text(document)
        for field in (
            "plain_purpose",
            "plain_audience",
            "plain_when_to_use",
            "plain_prerequisites",
            "plain_limitations",
            "plain_verification",
        ):
            self.assertIn(records[0][field], text, field)
        navigation = document.tables[0]
        self.assertEqual([cell.text for cell in navigation.rows[0].cells], ["代码与名称", "通俗定义", "数量"])
        self.assertIn("05-05 并行计算与性能优化", navigation.rows[2].cells[0].text)
        self.assertEqual(navigation.rows[2].cells[2].text, "2")
        source_link_paragraphs = [
            paragraph
            for paragraph in document.paragraphs
            if "w:hyperlink" in paragraph._p.xml
        ]
        self.assertEqual(
            len(source_link_paragraphs),
            1,
            "概览仓库链接应紧凑排在同一段，避免少量链接被挤到孤立末页",
        )
        self.assertEqual(len(source_link_paragraphs[0]._p.findall(qn("w:hyperlink"))), 3)

    def test_subcategory_has_one_plain_reader_block_and_separate_trace_block_per_skill(self):
        """Omitting a user field, mixing trace facts into advice, or losing an ID must fail."""
        records = [fixture_record("GH-05-0003"), fixture_record("GH-05-0024")]
        document = self.builder.build_subcategory_document(SUBCATEGORY, records)
        text = all_document_text(document)
        skill_headings = [paragraph.text for paragraph in document.paragraphs if paragraph.style.name == "Heading 2"]
        self.assertEqual(skill_headings, ["并行计算工具 3", "并行计算工具 24"])
        for record in records:
            for field in (
                "plain_purpose", "plain_audience", "plain_when_to_use", "plain_prerequisites",
                "plain_limitations", "plain_integration", "plain_verification", "plain_outputs",
            ):
                self.assertIn(record[field], text, f"{record['id']}:{field}")
        self.assertEqual(
            [paragraph.text for paragraph in document.paragraphs if paragraph.style.name == "Heading 3"],
            ["技术追溯", "技术追溯"],
        )
        self.assertEqual(text.count("内部编号："), len(records))
        trace_paragraphs = [paragraph for paragraph in document.paragraphs if paragraph.text.startswith("内部编号：")]
        self.assertEqual(len(trace_paragraphs), len(records))
        for paragraph in trace_paragraphs:
            self.assertEqual(paragraph.paragraph_format.space_after.pt, 0)
            paragraph_text = paragraph.text
            for label in ("功能标签：", "原生生态：", "来源形态：", "许可证：", "仓库最近更新："):
                self.assertIn(label, paragraph_text)
        for record in records:
            self.assertEqual(text.count(record["id"]), 1)

        hyperlink_paragraphs = [paragraph for paragraph in document.paragraphs if "w:hyperlink" in paragraph._p.xml]
        self.assertEqual(len(hyperlink_paragraphs), len(records))
        for paragraph in hyperlink_paragraphs:
            self.assertTrue(paragraph.text.startswith("内部编号："))
            self.assertIn("原始资料地址：", paragraph.text)
            self.assertEqual(len(paragraph._p.findall(qn("w:hyperlink"))), 2)

        self.assertEqual(len(document.tables), len(records))
        for table, record in zip(document.tables, records):
            labels = [row.cells[0].text for row in table.rows]
            values = [row.cells[1].text for row in table.rows]
            self.assertEqual(labels, ["英文名称", "推荐程度", "接入难度", "核验层级"])
            self.assertEqual(values[0], record["name"])
            self.assertEqual(values[1], record["priority"])
            self.assertEqual(values[3], record["verify"])
            for row in table.rows[:-1]:
                for cell in row.cells:
                    self.assertTrue(
                        cell.paragraphs[0].paragraph_format.keep_with_next,
                        "四行摘要表必须整块留在同一页，不能只把后两行挤到下一页",
                    )

    def test_short_value_table_does_not_add_an_empty_spacer_paragraph(self):
        """Repeated blank paragraphs waste enough height to create orphaned trace-only pages."""
        document = Document()
        self.builder._add_short_value_table(document, fixture_record("GH-05-0003"))
        self.assertEqual(document.paragraphs, [])

    def test_long_text_and_urls_remain_complete_without_full_url_display(self):
        """Truncation or dumping long addresses into tables must fail."""
        record = fixture_record("GH-05-0003")
        record["plain_limitations"] += "补充说明：" + "这是用于检查长文本分页和换行的完整句子。" * 30
        document = self.builder.build_subcategory_document(SUBCATEGORY, [record])
        text = all_document_text(document)
        self.assertIn(record["plain_limitations"], text)
        self.assertNotIn(record["repo_url"], text)
        self.assertNotIn(record["skill_url"], text)
        xml = document_xml(document)
        self.assertGreaterEqual(xml.count("w:hyperlink"), 4)
        self.assertIn("原始资料地址", text)
        for heading in [p for p in document.paragraphs if p.style.name in {"Heading 1", "Heading 2", "Heading 3"}]:
            self.assertTrue(heading.paragraph_format.keep_with_next or heading.style.paragraph_format.keep_with_next)

    def test_empty_subcategory_is_rejected_instead_of_emitting_a_hollow_report(self):
        """An empty taxonomy leaf must stop generation before a misleading DOCX exists."""
        with self.assertRaisesRegex(ValueError, "空小分类"):
            self.builder.build_subcategory_document(SUBCATEGORY, [])


class VerificationAndGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_module(BUILDER_PATH, "build_subcategorized_documents_generation_test")
        cls.verifier = load_module(VERIFIER_PATH, "verify_subcategorized_documents_for_test")
        cls.renderer = load_module(RENDERER_PATH, "render_subcategorized_documents_for_test")

    def test_verifier_accepts_a_valid_document_and_rejects_structural_drift(self):
        """Bad margins, stale IDs, and placeholders must be reported independently."""
        records = [fixture_record("GH-05-0003"), fixture_record("GH-05-0024")]
        with tempfile.TemporaryDirectory() as temporary_directory:
            good_path = Path(temporary_directory) / "good.docx"
            self.builder.build_subcategory_document(SUBCATEGORY, records).save(good_path)
            self.assertEqual(
                self.verifier.verify_document(good_path, scope="subcategory", expected_records=records),
                [],
            )

            bad_document = Document(good_path)
            bad_document.sections[0].left_margin = 720
            bad_document.add_paragraph("TODO 已经运行成功 GH-05-9999")
            bad_path = Path(temporary_directory) / "bad.docx"
            bad_document.save(bad_path)
            issues = self.verifier.verify_document(bad_path, scope="subcategory", expected_records=records)
            self.assertTrue(any("左边距" in issue for issue in issues), issues)
            self.assertTrue(any("占位" in issue for issue in issues), issues)
            self.assertTrue(any("夸大" in issue for issue in issues), issues)
            self.assertTrue(any("Skill ID" in issue for issue in issues), issues)

    def test_manifest_selection_is_sorted_safe_and_scope_aware(self):
        """Unsafe paths, unstable ordering, or ambiguous selectors must fail before writes."""
        manifest = [
            {"path": "05_交付物/通俗细分版_2026-08-07/05_编程数学数据分析和可视化/05-05_并行计算与性能优化/05-05_并行计算与性能优化_GitHub技能调研.docx", "format": "docx", "scope": "subcategory", "big_category_code": "05", "subcategory_code": "05-05", "subcategory_name": "并行计算与性能优化"},
            {"path": "05_交付物/通俗细分版_2026-08-07/05_编程数学数据分析和可视化/00_大分类总览.docx", "format": "docx", "scope": "overview", "big_category_code": "05"},
            {"path": "05_交付物/通俗细分版_2026-08-07/05_编程数学数据分析和可视化/00_大分类总览.xlsx", "format": "xlsx", "scope": "overview", "big_category_code": "05"},
        ]
        selected = self.builder.select_manifest_items(manifest, ["05-overview", "05-05"])
        self.assertEqual([(item["scope"], item.get("subcategory_code")) for item in selected], [("overview", None), ("subcategory", "05-05")])
        with self.assertRaisesRegex(ValueError, "未知 --only"):
            self.builder.select_manifest_items(manifest, ["99-99"])
        unsafe = [{**manifest[0], "path": "../escape.docx"}]
        with self.assertRaisesRegex(ValueError, "不安全"):
            self.builder.select_manifest_items(unsafe, None)

    def test_manifest_driven_generation_is_idempotent_for_overview_and_subcategory(self):
        """Repeated generation with reversed input must preserve paths, order, and bytes."""
        records = [fixture_record("GH-05-0001", subcategory_code="05-01"), fixture_record("GH-05-0003")]
        taxonomy = OVERVIEW["subcategories"]
        manifest = [
            {"path": "05_交付物/通俗细分版_2026-08-07/05_编程数学数据分析和可视化/00_大分类总览.docx", "format": "docx", "scope": "overview", "big_category_code": "05"},
            {"path": "05_交付物/通俗细分版_2026-08-07/05_编程数学数据分析和可视化/05-05_并行计算与性能优化/05-05_并行计算与性能优化_GitHub技能调研.docx", "format": "docx", "scope": "subcategory", "big_category_code": "05", "subcategory_code": "05-05", "subcategory_name": "并行计算与性能优化"},
        ]
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first = self.builder.generate_documents(records, taxonomy, manifest, root, only=["05-overview", "05-05"])
            first_hashes = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in first}
            second = self.builder.generate_documents(list(reversed(records)), list(reversed(taxonomy)), list(reversed(manifest)), root, only=["05-05", "05-overview"])
            second_hashes = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in second}
            self.assertEqual(first_hashes, second_hashes)

    def test_renderer_plans_one_isolated_output_directory_per_document(self):
        """Two DOCX files must never overwrite each other's page-N PNGs."""
        items = [
            {"path": "05_交付物/通俗细分版_2026-08-07/05_编程数学数据分析和可视化/00_大分类总览.docx", "format": "docx", "scope": "overview", "big_category_code": "05"},
            {"path": "05_交付物/通俗细分版_2026-08-07/05_编程数学数据分析和可视化/05-05_并行计算与性能优化/05-05_并行计算与性能优化_GitHub技能调研.docx", "format": "docx", "scope": "subcategory", "big_category_code": "05", "subcategory_code": "05-05"},
        ]
        plan = self.renderer.build_render_plan(items, PROJECT_ROOT, PROJECT_ROOT / "06_过程记录" / "renders" / "subcategorized_docx")
        self.assertEqual([item["key"] for item in plan], ["05-overview", "05-05"])
        self.assertEqual(len({item["output_dir"] for item in plan}), 2)
        self.assertTrue(all(Path(item["docx_path"]).is_absolute() for item in plan))

    def test_renderer_rejects_a_missing_packaged_render_script(self):
        """A missing documents-skill renderer must fail before any false QA claim."""
        with self.assertRaisesRegex(FileNotFoundError, "documents 技能渲染器"):
            self.renderer.render_plan([], render_script=PROJECT_ROOT / "missing-render-docx.py")


if __name__ == "__main__":
    unittest.main()
