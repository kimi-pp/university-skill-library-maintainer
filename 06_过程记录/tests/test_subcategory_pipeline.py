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
    validate_assignments,
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


if __name__ == "__main__":
    unittest.main()
