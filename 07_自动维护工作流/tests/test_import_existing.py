import hashlib
import io
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from contextlib import redirect_stdout
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

from skill_maintainer.import_existing import (
    ImportInventory,
    ImportedRecord,
    build_initial_ledger,
    main,
    scan_existing_deliveries,
)
from skill_maintainer.ledger import LedgerStore


FIXTURES = Path(__file__).parent / "fixtures" / "import"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ExistingDeliveryImportTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)

    def copy_fixture_tree(self, name: str) -> Path:
        target = self.root / name
        shutil.copytree(FIXTURES / name, target)
        return target

    def formal_record(self, **overrides) -> ImportedRecord:
        inventory = scan_existing_deliveries(self.copy_fixture_tree("matching"))
        source = next(record for record in inventory.records if record.values.get("入库层级") == "正式")
        values = dict(source.values)
        for key, value in overrides.items():
            if value is None:
                values.pop(key, None)
            else:
                values[key] = value
        return ImportedRecord(source.source_path, source.source_row, values)

    def inventory_for(self, *records: ImportedRecord) -> ImportInventory:
        return ImportInventory(
            root=self.root,
            records=records,
            source_hashes={},
            excel_files=(),
            word_files=(),
            excel_skill_count=len(records),
            word_skill_count=len(records),
            duplicate_group_count=0,
            ambiguous_record_count=sum("API 或外部服务" in record.values for record in records),
            word_excel_count_mismatch=False,
        )

    def write_docx_table(self, path: Path, headers: list[str], rows: list[list[str]]) -> None:
        xml_rows = "".join(
            "<w:tr>" + "".join(
                f"<w:tc><w:p><w:r><w:t>{escape(value)}</w:t></w:r></w:p></w:tc>" for value in row
            ) + "</w:tr>"
            for row in [headers, *rows]
        )
        with ZipFile(path, "w", ZIP_DEFLATED) as archive:
            archive.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
            archive.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
            archive.writestr("word/document.xml", f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:tbl>{xml_rows}</w:tbl><w:sectPr/></w:body></w:document>')

    def test_duplicate_platform_skill_becomes_one_formal_row_and_two_aliases(self):
        deliveries = self.copy_fixture_tree("matching")
        inventory = scan_existing_deliveries(deliveries)
        output = self.root / "staging" / "initial-ledger.xlsx"

        summary = build_initial_ledger(inventory, output)
        ledger = LedgerStore.load(output)

        self.assertTrue(summary.written)
        self.assertEqual(summary.current_skill_count, 1)
        self.assertEqual(summary.source_alias_count, 2)
        self.assertEqual(len(ledger.rows("当前Skill")), 1)
        self.assertEqual(len(ledger.rows("来源别名")), 2)
        self.assertEqual(ledger.validate(), [])

    def test_historical_combined_api_field_is_observation_not_guessed_remote_api(self):
        inventory = scan_existing_deliveries(self.copy_fixture_tree("matching"))
        output = self.root / "staging" / "initial-ledger.xlsx"

        summary = build_initial_ledger(inventory, output)
        observation = LedgerStore.load(output).rows("候选观察")[0]

        self.assertEqual(summary.candidate_observation_count, 1)
        self.assertEqual(observation["观察状态"], "需人工对账")
        self.assertIn("API 或外部服务", observation["原因"])
        self.assertIn("不得推断为远程 API", observation["原因"])
        self.assertEqual(str(observation["记录日期"]), date.today().isoformat())

    def test_word_excel_count_mismatch_is_reported_and_blocks_formal_import(self):
        deliveries = self.copy_fixture_tree("mismatch")
        inventory = scan_existing_deliveries(deliveries)

        self.assertTrue(inventory.word_excel_count_mismatch)
        self.assertEqual(inventory.excel_skill_count, 0)
        self.assertEqual(inventory.word_skill_count, 2)
        with self.assertRaisesRegex(ValueError, "Word/Excel 数量不一致"):
            build_initial_ledger(inventory, self.root / "staging" / "blocked.xlsx")

    def test_scan_is_read_only_for_every_source_file(self):
        deliveries = self.copy_fixture_tree("matching")
        before = {path.relative_to(deliveries): sha256(path) for path in deliveries.rglob("*") if path.is_file()}

        inventory = scan_existing_deliveries(deliveries)

        after = {path.relative_to(deliveries): sha256(path) for path in deliveries.rglob("*") if path.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(inventory.source_hashes, before)

    def test_repeated_import_reuses_deterministic_stable_ids_and_counts(self):
        inventory = scan_existing_deliveries(self.copy_fixture_tree("matching"))
        first = self.root / "staging" / "first.xlsx"
        second = self.root / "staging" / "second.xlsx"

        first_summary = build_initial_ledger(inventory, first)
        second_summary = build_initial_ledger(inventory, second)
        first_rows = LedgerStore.load(first).rows("当前Skill")
        second_rows = LedgerStore.load(second).rows("当前Skill")

        self.assertEqual(first_summary.current_skill_count, second_summary.current_skill_count)
        self.assertEqual(first_summary.source_alias_count, second_summary.source_alias_count)
        self.assertEqual(
            [row["内部标识"] for row in first_rows],
            [row["内部标识"] for row in second_rows],
        )
        self.assertEqual(first_rows[0]["内部标识"], "GH-01-0001")

    def test_complete_formal_record_without_id_receives_deterministic_hash_id(self):
        record = self.formal_record(**{"内部标识": None})
        output = self.root / "staging" / "generated-id.xlsx"

        summary = build_initial_ledger(self.inventory_for(record), output)

        self.assertEqual(summary.current_skill_count, 1)
        self.assertRegex(summary.stable_ids[0], r"^IMP-01-[0-9A-F]{12}$")

    def test_same_validated_id_with_different_canonical_urls_is_one_skill_with_two_aliases(self):
        primary = self.formal_record()
        platform = ImportedRecord(
            self.root / "platform.xlsx",
            2,
            {
                "内部标识": primary.values["内部标识"],
                "Skill名称": primary.skill_name,
                "Canonical source": "https://skillhub.example/repeated-detail",
                "来源地址": "https://skillhub.example/repeated-detail",
                "来源平台": "SkillHub",
            },
        )
        output = self.root / "staging" / "same-id.xlsx"

        summary = build_initial_ledger(self.inventory_for(primary, platform), output)

        self.assertEqual(summary.current_skill_count, 1)
        self.assertEqual(summary.source_alias_count, 2)

    def test_unvalidated_partial_id_cannot_override_generated_stable_id(self):
        formal_without_id = self.formal_record(**{"内部标识": None})
        partial = ImportedRecord(
            self.root / "partial.xlsx",
            2,
            {
                "内部标识": "UNVALIDATED-001",
                "Skill名称": formal_without_id.skill_name,
                "Canonical source": formal_without_id.canonical_source,
            },
        )

        summary = build_initial_ledger(self.inventory_for(formal_without_id, partial), self.root / "staging" / "unvalidated-id.xlsx")

        self.assertRegex(summary.stable_ids[0], r"^IMP-01-[0-9A-F]{12}$")

    def test_semantically_invalid_historical_id_cannot_override_generated_id(self):
        valid_without_id = self.formal_record(**{"内部标识": None})
        invalid_values = dict(valid_without_id.values)
        invalid_values.update({"内部标识": "UNVALIDATED-SEMANTIC-001", "许可证": "待确认"})
        invalid_with_id = ImportedRecord(self.root / "invalid.xlsx", 2, invalid_values)

        summary = build_initial_ledger(self.inventory_for(valid_without_id, invalid_with_id), self.root / "staging" / "invalid-semantic-id.xlsx")

        self.assertRegex(summary.stable_ids[0], r"^IMP-01-[0-9A-F]{12}$")

    def test_semantically_valid_historical_id_wins_over_generated_id(self):
        valid_with_id = self.formal_record(**{"内部标识": "GH-01-0999"})
        no_id_values = dict(valid_with_id.values)
        no_id_values.pop("内部标识")
        valid_without_id = ImportedRecord(self.root / "no-id.xlsx", 2, no_id_values)

        summary = build_initial_ledger(self.inventory_for(valid_without_id, valid_with_id), self.root / "staging" / "valid-semantic-id.xlsx")

        self.assertEqual(summary.stable_ids, ("GH-01-0999",))

    def test_ambiguous_identity_group_keeps_every_source_as_observation(self):
        primary = self.formal_record()
        ambiguous = ImportedRecord(
            self.root / "historical.xlsx",
            2,
            {
                "内部标识": primary.values["内部标识"],
                "Skill名称": primary.skill_name,
                "Canonical source": "https://platform.example/repeated",
                "API 或外部服务": "需要；Abaqus",
            },
        )
        output = self.root / "staging" / "ambiguous-group.xlsx"

        summary = build_initial_ledger(self.inventory_for(primary, ambiguous), output)
        observations = LedgerStore.load(output).rows("候选观察")

        self.assertEqual(summary.current_skill_count, 0)
        self.assertEqual(len(observations), 2)
        self.assertTrue(all("同一身份组" in row["原因"] for row in observations))

    def test_unrecognized_word_table_blocks_even_when_word_and_excel_counts_are_zero(self):
        deliveries = self.root / "unrecognized"
        deliveries.mkdir()
        self.write_docx_table(deliveries / "unknown.docx", ["名称", "链接"], [["示例", "https://example.edu"]])

        inventory = scan_existing_deliveries(deliveries)

        self.assertEqual(inventory.excel_skill_count, 0)
        self.assertEqual(inventory.word_skill_count, 0)
        self.assertEqual(inventory.word_uncertainty_count, 1)
        with self.assertRaisesRegex(ValueError, "Word 结构无法确定"):
            build_initial_ledger(inventory, self.root / "staging" / "uncertain.xlsx")

    def test_multicolumn_word_header_counts_skill_rows(self):
        deliveries = self.root / "recognized"
        deliveries.mkdir()
        self.write_docx_table(deliveries / "recognized.docx", ["Skill名称", "来源地址"], [["一", "https://a"], ["二", "https://b"]])

        inventory = scan_existing_deliveries(deliveries)

        self.assertEqual(inventory.word_skill_count, 2)
        self.assertEqual(inventory.word_uncertainty_count, 0)

    def test_invalid_formal_data_never_publishes_or_overwrites_requested_output(self):
        invalid = self.formal_record(**{"许可证": "待确认"})
        output = self.root / "staging" / "existing.xlsx"
        output.parent.mkdir()
        output.write_bytes(b"existing-output")

        with self.assertRaisesRegex(ValueError, "许可证"):
            build_initial_ledger(self.inventory_for(invalid), output)

        self.assertEqual(output.read_bytes(), b"existing-output")

    def test_inventory_cli_prints_file_and_record_counts(self):
        original_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", original_argv)
        sys.argv = ["import_existing", str(self.root), "--inventory-only"]
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            self.assertEqual(main(), 0)

        self.assertIn("Excel文件=0", stdout.getvalue())
        self.assertIn("Word文件=0", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
