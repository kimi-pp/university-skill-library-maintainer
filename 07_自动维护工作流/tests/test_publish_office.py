"""Task 11: real Office verification and single-authority publication."""

from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZIP_DEFLATED, ZipFile

from docx import Document
from openpyxl import Workbook, load_workbook
from PIL import Image

from skill_maintainer.office import (
    OfficeCheck,
    OfficeVerificationError,
    WordRenderDecision,
    bind_word_visual_decision,
    verify_excel,
    verify_word,
)
from skill_maintainer.publish import (
    PublishFile,
    PublishError,
    build_publish_plan,
    publish_atomically,
)


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def write_excel(path: Path, *, rows: int) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "当前Skill"
    sheet.append(["内部标识", "Skill名称"])
    for index in range(1, rows + 1):
        sheet.append([f"GH-01-{index:04d}", f"skill-{index}"])
    workbook.save(path)
    workbook.close()


def write_corrupt_xlsx(path: Path) -> None:
    """A ZIP/OOXML-shaped input whose workbook part cannot be parsed by Excel."""
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Override PartName="/xl/workbook.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/></Types>',
        )
        archive.writestr("xl/workbook.xml", "<workbook><broken>")


def write_word(path: Path) -> None:
    document = Document()
    document.add_heading("高校专业 Skill 自动查验", level=1)
    document.add_paragraph("这是一份用于 Office 只读复读和逐页渲染验收的中文测试报告。")
    table = document.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "项目"
    table.cell(0, 1).text = "结果"
    table.cell(1, 0).text = "Office 复读"
    table.cell(1, 1).text = "待验证"
    document.save(path)


@unittest.skipUnless(os.name == "nt", "Microsoft Office COM acceptance requires Windows")
class OfficeVerificationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_excel_opens_read_only_reopens_and_keeps_520th_data_row(self):
        workbook_path = self.root / "ledger-520.xlsx"
        write_excel(workbook_path, rows=520)

        first = verify_excel(workbook_path)
        second = verify_excel(workbook_path)

        for check in (first, second):
            self.assertTrue(check.passed, check.error)
            self.assertTrue(check.office_opened)
            self.assertTrue(check.read_only)
            self.assertEqual(check.key_sheet, "当前Skill")
            self.assertEqual(check.last_row, 521)
            self.assertEqual(check.last_value, "skill-520")
            self.assertEqual(check.process_count_before, check.process_count_after)
            self.assertEqual(check.source_sha256, file_sha256(workbook_path))
        workbook = load_workbook(workbook_path, read_only=True, data_only=False)
        self.addCleanup(workbook.close)
        self.assertEqual(workbook["当前Skill"]["A521"].value, "GH-01-0520")

    def test_excel_rejects_header_only_and_corrupt_inputs_without_leaking_processes(self):
        empty = self.root / "empty.xlsx"
        corrupt = self.root / "corrupt.xlsx"
        write_excel(empty, rows=0)
        write_corrupt_xlsx(corrupt)

        empty_check = verify_excel(empty)
        corrupt_check = verify_excel(corrupt)

        self.assertFalse(empty_check.passed)
        self.assertIn("数据行", empty_check.error or "")
        self.assertEqual(empty_check.process_count_before, empty_check.process_count_after)
        self.assertFalse(corrupt_check.passed)
        self.assertTrue(corrupt_check.error)
        self.assertEqual(corrupt_check.process_count_before, corrupt_check.process_count_after)

    def test_word_exports_pdf_renders_pages_and_requires_hash_bound_visual_decision(self):
        word_path = self.root / "report.docx"
        write_word(word_path)

        first = verify_word(word_path, self.root / "render-first")
        second = verify_word(word_path, self.root / "render-second")

        for check in (first, second):
            self.assertTrue(check.office_passed, check.error)
            self.assertFalse(check.passed, "未绑定外部逐页视觉判定时不得发布")
            self.assertTrue(check.read_only)
            self.assertEqual(check.process_count_before, check.process_count_after)
            self.assertTrue(check.pdf_path and check.pdf_path.is_file())
            self.assertTrue(check.pdf_sha256)
            self.assertGreaterEqual(len(check.page_paths), 1)
            self.assertEqual(len(check.page_paths), len(check.page_sha256))
            self.assertFalse(check.blank_pages)
            self.assertTrue(all(path.is_file() and path.stat().st_size > 0 for path in check.page_paths))

        approved = bind_word_visual_decision(
            first,
            WordRenderDecision.from_check(first, approved=True, reviewer="Task 11 external visual review"),
        )
        self.assertTrue(approved.passed, approved.error)
        rejected = bind_word_visual_decision(
            second,
            WordRenderDecision.from_check(second, approved=False, reviewer="Task 11 external visual review", rejected_pages=(1,)),
        )
        self.assertFalse(rejected.passed)
        self.assertIn("视觉", rejected.error or "")

    def test_word_rejects_nonempty_render_directory_without_mutating_it(self):
        word_path = self.root / "report.docx"
        render = self.root / "existing-render"
        render.mkdir()
        sentinel = render / "keep.txt"
        sentinel.write_text("owned by caller", encoding="utf-8")
        write_word(word_path)

        with self.assertRaisesRegex(OfficeVerificationError, "空目录"):
            verify_word(word_path, render)

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "owned by caller")
        self.assertEqual(tuple(render.iterdir()), (sentinel,))

    def test_word_visual_binding_rejects_stale_page_hash_and_blank_page(self):
        page = self.root / "page-1.png"
        Image.new("RGB", (64, 64), "white").save(page)
        source = self.root / "sample.docx"
        pdf = self.root / "sample.pdf"
        source.write_bytes(b"docx")
        pdf.write_bytes(b"pdf")
        check = OfficeCheck(
            kind="word", source_path=source, source_sha256=file_sha256(source),
            passed=False, office_passed=True, office_opened=True, read_only=True,
            pdf_path=pdf, pdf_sha256=file_sha256(pdf), page_paths=(page,),
            page_sha256=(file_sha256(page),), blank_pages=(1,),
            process_count_before=0, process_count_after=0,
        )
        decision = WordRenderDecision.from_check(check, approved=True, reviewer="external")
        with self.assertRaisesRegex(OfficeVerificationError, "空白"):
            bind_word_visual_decision(check, decision)

        nonblank = self.root / "nonblank.png"
        image = Image.new("RGB", (64, 64), "white")
        image.putpixel((10, 10), (0, 0, 0))
        image.save(nonblank)
        current = replace(
            check,
            page_paths=(nonblank,), page_sha256=(file_sha256(nonblank),), blank_pages=(),
        )
        stale = WordRenderDecision.from_check(current, approved=True, reviewer="external")
        nonblank.write_bytes(nonblank.read_bytes() + b"tampered")
        with self.assertRaisesRegex(OfficeVerificationError, "哈希"):
            bind_word_visual_decision(current, stale)

        missing = self.root / "missing.png"
        image.save(missing)
        missing_check = replace(
            check,
            page_paths=(missing,), page_sha256=(file_sha256(missing),), blank_pages=(),
        )
        missing_decision = WordRenderDecision.from_check(missing_check, approved=True, reviewer="external")
        missing.unlink()
        with self.assertRaisesRegex(OfficeVerificationError, "缺失"):
            bind_word_visual_decision(missing_check, missing_decision)


class PublicationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def make_tree(self, name: str = "run-20260828-220000") -> tuple[Path, Path]:
        staging = self.root / "staging" / name
        production = self.root / f"production-{name}"
        deliveries = staging / "deliveries"
        deliveries.mkdir(parents=True)
        (deliveries / "受影响专业类").mkdir()
        (deliveries / "Skill库自动查验报告.docx").write_bytes(b"new-docx")
        (deliveries / "Skill库自动查验表.xlsx").write_bytes(b"new-xlsx")
        (deliveries / "受影响专业类" / "0809.xlsx").write_bytes(b"scope-xlsx")
        (staging / "Skills主台账.xlsx").write_bytes(b"new-ledger-authority")
        (production / "ledger" / "archive").mkdir(parents=True)
        (production / "output" / "generations").mkdir(parents=True)
        (production / "ledger" / "Skills主台账.xlsx").write_bytes(b"old-ledger-authority")
        return staging, production

    def test_build_plan_binds_every_input_and_single_authority(self):
        staging, production = self.make_tree()
        plan = build_publish_plan(staging, production)

        self.assertEqual(plan.run_id, staging.name)
        self.assertEqual(plan.authority_path, production / "ledger" / "Skills主台账.xlsx")
        self.assertEqual(plan.expected_authority_sha256, file_sha256(plan.authority_path))
        self.assertEqual(plan.staged_ledger_sha256, file_sha256(staging / "Skills主台账.xlsx"))
        self.assertEqual(
            tuple(item.relative_path for item in plan.delivery_files),
            ("Skill库自动查验报告.docx", "Skill库自动查验表.xlsx", "受影响专业类/0809.xlsx"),
        )
        self.assertTrue(all(item.sha256 for item in plan.delivery_files))
        self.assertEqual(plan.generation_path, production / "output" / "generations" / staging.name)
        self.assertEqual(plan.backup_path.parent, production / "ledger" / "archive")
        self.assertRegex(plan.backup_path.name, r"^Skills主台账_\d{8}_\d{6}(?:_\d+)?\.xlsx$")

    def test_publish_copies_backup_and_generation_before_authority_replace(self):
        staging, production = self.make_tree()
        plan = build_publish_plan(staging, production)

        receipt = publish_atomically(plan)

        self.assertEqual(file_sha256(plan.authority_path), plan.staged_ledger_sha256)
        self.assertTrue(receipt.backup_path.is_file())
        self.assertEqual(receipt.backup_sha256, sha256(b"old-ledger-authority").hexdigest())
        self.assertEqual(receipt.generation_path, plan.generation_path)
        self.assertTrue(receipt.generation_path.is_dir())
        for item in plan.delivery_files:
            published = receipt.generation_path / Path(item.relative_path)
            self.assertEqual(file_sha256(published), item.sha256)
        self.assertTrue((receipt.generation_path / "generation-manifest.json").is_file())
        self.assertFalse(any(production.rglob("*receipt*")), "发布回执只在内存返回，不落业务文件")

    def test_publish_fsyncs_every_staged_input_before_copying_or_committing(self):
        staging, production = self.make_tree()
        plan = build_publish_plan(staging, production)
        from skill_maintainer import publish as publish_module
        real_fsync_file = publish_module._fsync_file
        fsynced: list[Path] = []

        def record_and_fsync(path: Path) -> None:
            fsynced.append(path)
            real_fsync_file(path)

        with patch("skill_maintainer.publish._fsync_file", side_effect=record_and_fsync):
            publish_atomically(plan)

        required = {plan.staged_ledger}
        required.update(plan.deliveries_root / Path(item.relative_path) for item in plan.delivery_files)
        self.assertTrue(required.issubset(set(fsynced)), (required, fsynced))

    def test_changed_authority_is_rejected_immediately_before_replace(self):
        staging, production = self.make_tree()
        plan = build_publish_plan(staging, production)
        plan.authority_path.write_bytes(b"concurrent-change")

        with self.assertRaisesRegex(PublishError, "生产主台账.*变化"):
            publish_atomically(plan)

        self.assertEqual(plan.authority_path.read_bytes(), b"concurrent-change")
        self.assertFalse(plan.generation_path.exists())

    def test_failure_at_each_destination_preserves_old_authority_and_prior_backups(self):
        failure_points = (
            "delivery:Skill库自动查验报告.docx",
            "delivery:Skill库自动查验表.xlsx",
            "delivery:受影响专业类/0809.xlsx",
            "generation-replace",
            "authority-temp",
            "authority-replace",
        )
        for index, failure_point in enumerate(failure_points, start=1):
            with self.subTest(failure_point=failure_point):
                staging, production = self.make_tree(f"run-{index}")
                prior = production / "ledger" / "archive" / "Skills主台账_20260101_000000.xlsx"
                prior.write_bytes(b"prior-backup")
                plan = build_publish_plan(staging, production)
                old = plan.authority_path.read_bytes()

                with self.assertRaisesRegex(PublishError, "注入失败"):
                    publish_atomically(plan, fail_at=failure_point)

                self.assertEqual(plan.authority_path.read_bytes(), old)
                self.assertEqual(prior.read_bytes(), b"prior-backup")
                self.assertTrue(plan.backup_path.is_file())
                self.assertEqual(plan.backup_path.read_bytes(), old)
                self.assertFalse(plan.generation_path.exists())
                self.assertFalse(any(path.name.startswith(f".{plan.run_id}") for path in plan.generation_path.parent.iterdir()))
                self.assertFalse(any(production.rglob("*receipt*")))

    def test_staged_input_change_is_rejected_without_partial_publication(self):
        staging, production = self.make_tree()
        plan = build_publish_plan(staging, production)
        (staging / "deliveries" / "Skill库自动查验表.xlsx").write_bytes(b"changed-after-plan")

        with self.assertRaisesRegex(PublishError, "暂存.*变化"):
            publish_atomically(plan)

        self.assertEqual(plan.authority_path.read_bytes(), b"old-ledger-authority")
        self.assertFalse(plan.generation_path.exists())

    def test_forged_delivery_traversal_is_rejected_before_any_publication(self):
        staging, production = self.make_tree()
        escaped = staging / "escaped.xlsx"
        escaped.write_bytes(b"outside-deliveries")
        plan = build_publish_plan(staging, production)
        forged = replace(
            plan,
            delivery_files=(PublishFile("../escaped.xlsx", file_sha256(escaped)),),
        )

        with self.assertRaisesRegex(PublishError, "相对路径"):
            publish_atomically(forged)

        self.assertEqual(plan.authority_path.read_bytes(), b"old-ledger-authority")
        self.assertFalse(plan.generation_path.exists())


if __name__ == "__main__":
    unittest.main()
