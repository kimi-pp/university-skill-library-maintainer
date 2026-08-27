import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from skill_maintainer.import_existing import build_initial_ledger, scan_existing_deliveries
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


if __name__ == "__main__":
    unittest.main()
