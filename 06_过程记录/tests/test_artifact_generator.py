import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "06_过程记录" / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "03_候选池" / "deduplicated"))

from catalog_data import CANDIDATES, CATEGORIES, REPOSITORIES  # noqa: E402
from artifact_generator import (  # noqa: E402
    build_manifest,
    records_for_category,
    validate_catalog,
    write_research_data,
)


class ArtifactGeneratorTests(unittest.TestCase):
    def test_catalog_is_valid_and_has_expected_category_counts(self):
        validate_catalog(CANDIDATES, CATEGORIES, REPOSITORIES)
        self.assertEqual(
            {cat: len(records_for_category(CANDIDATES, cat)) for cat in CATEGORIES},
            {"01": 20, "02": 22, "03": 31},
        )

    def test_validation_rejects_duplicate_ids(self):
        duplicate = [dict(CANDIDATES[0]), dict(CANDIDATES[0])]
        with self.assertRaisesRegex(ValueError, "重复 ID"):
            validate_catalog(duplicate, CATEGORIES, REPOSITORIES)

    def test_validation_rejects_unknown_repository(self):
        bad = [dict(CANDIDATES[0], repo="owner/repository-not-listed")]
        with self.assertRaisesRegex(ValueError, "仓库元数据"):
            validate_catalog(bad, CATEGORIES, REPOSITORIES)

    def test_manifest_contains_six_independent_deliverables(self):
        manifest = build_manifest(CATEGORIES)
        self.assertEqual(len(manifest), 6)
        self.assertEqual(len({item["path"] for item in manifest}), 6)
        self.assertEqual({item["format"] for item in manifest}, {"xlsx", "docx"})
        self.assertTrue(all(item["category"] in CATEGORIES for item in manifest))

    def test_write_research_data_keeps_only_selected_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_research_data(root, CANDIDATES, CATEGORIES, REPOSITORIES)
            for cat in CATEGORIES:
                payload = json.loads((root / f"category_{cat}.json").read_text(encoding="utf-8"))
                self.assertTrue(payload["records"])
                self.assertTrue(all(row["cat"] == cat for row in payload["records"]))
            jsonl_rows = [
                json.loads(line)
                for line in (root / "skills.jsonl").read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(jsonl_rows), len(CANDIDATES))


if __name__ == "__main__":
    unittest.main()
