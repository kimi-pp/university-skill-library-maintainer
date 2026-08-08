import sys
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


class SubcategoryAssignmentTests(unittest.TestCase):
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

    def test_taxonomy_and_big_category_totals_match_approved_design(self):
        """Omitting a category or shifting a Skill across big categories must fail."""
        mapping = load_assignment_file(ASSIGNMENT_FILE)
        records = enrich_with_subcategory(load_source_records(DATA_DIR), mapping)

        self.assertEqual(len(mapping["taxonomy"]), 61)
        self.assertEqual(
            Counter(row["subcategory_code"][:2] for row in records),
            {"01": 20, "02": 22, "03": 31, "04": 29, "05": 55},
        )


if __name__ == "__main__":
    unittest.main()
