"""Task 6 integration tests for complete generation and safe archival."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = PROJECT_ROOT / "06_过程记录" / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from build_subcategorized_delivery import (  # noqa: E402
    archive_originals,
    discover_originals,
    expected_delivery_paths,
    publish_staged_delivery,
    seed_existing_delivery,
    staging_parent,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_manifest() -> list[dict]:
    items: list[dict] = []
    for big in range(1, 6):
        code = f"{big:02d}"
        for suffix in ("docx", "xlsx"):
            items.append(
                {
                    "path": f"05_交付物/通俗细分版_2026-08-07/{code}_大类/00_大分类总览.{suffix}",
                    "format": suffix,
                    "scope": "overview",
                    "big_category_code": code,
                }
            )
    subcategory_number = 0
    for big, count in ((1, 9), (2, 9), (3, 11), (4, 12), (5, 20)):
        for local in range(1, count + 1):
            subcategory_number += 1
            code = f"{big:02d}-{local:02d}"
            for suffix in ("docx", "xlsx"):
                items.append(
                    {
                        "path": f"05_交付物/通俗细分版_2026-08-07/{big:02d}_大类/{code}_小类/{code}_报告.{suffix}",
                        "format": suffix,
                        "scope": "subcategory",
                        "big_category_code": f"{big:02d}",
                        "subcategory_code": code,
                    }
                )
    self_count = sum(1 for item in items if item["scope"] == "subcategory")
    if subcategory_number != 61 or self_count != 122:
        raise AssertionError("测试清单构造错误")
    return items


class Task6DeliveryIntegrationTests(unittest.TestCase):
    def test_staging_directory_is_on_same_volume_as_project(self):
        project = Path("D:/workspace/project").resolve()
        parent = staging_parent(project)
        self.assertEqual(parent.drive.casefold(), project.drive.casefold())
        self.assertEqual(parent, project / "06_过程记录" / ".task6_staging")

    def test_staging_seeds_only_existing_manifest_files_for_byte_reuse(self):
        manifest = fixture_manifest()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            project = root / "project"
            staging = root / "staging"
            existing_relative = next(iter(expected_delivery_paths(manifest)))
            existing = project / existing_relative
            existing.parent.mkdir(parents=True, exist_ok=True)
            existing.write_bytes(b"stable-existing-bytes")
            unrelated = project / "05_交付物" / "通俗细分版_2026-08-07" / "noise.tmp"
            unrelated.write_bytes(b"exclude")

            seeded = seed_existing_delivery(project, staging, manifest)

            self.assertEqual(seeded, [staging / existing_relative])
            self.assertEqual((staging / existing_relative).read_bytes(), b"stable-existing-bytes")
            self.assertFalse((staging / unrelated.relative_to(project)).exists())

    def test_archive_copies_exact_ten_originals_without_changing_sources(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            delivery_root = root / "05_交付物"
            delivery_root.mkdir()
            for big in range(1, 6):
                for suffix in ("docx", "xlsx"):
                    path = delivery_root / f"{big:02d}_原始报告.{suffix}"
                    path.write_bytes(f"original-{big}-{suffix}".encode())
            (delivery_root / "0809_不在归档范围.docx").write_bytes(b"excluded")

            sources = discover_originals(delivery_root)
            before = {path.name: sha256(path) for path in sources}
            archive_root = delivery_root / "原始版_2026-08-06"
            inventory = archive_originals(sources, archive_root)

            self.assertEqual(len(sources), 10)
            self.assertEqual(len(inventory), 10)
            self.assertEqual(before, {path.name: sha256(path) for path in sources})
            self.assertEqual(before, {path.name: sha256(archive_root / path.name) for path in sources})
            self.assertTrue((delivery_root / "0809_不在归档范围.docx").exists())

    def test_publish_requires_and_promotes_exact_manifest_set(self):
        manifest = fixture_manifest()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            staging_root = root / "stage"
            final_root = root / "project"
            for relative in expected_delivery_paths(manifest):
                path = staging_root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(f"artifact:{relative.as_posix()}".encode("utf-8"))

            published = publish_staged_delivery(staging_root, final_root, manifest)
            expected = expected_delivery_paths(manifest)
            actual = {
                path.relative_to(final_root)
                for path in (final_root / "05_交付物" / "通俗细分版_2026-08-07").rglob("*")
                if path.is_file()
            }
            self.assertEqual(len(published), 132)
            self.assertEqual(actual, expected)
            self.assertEqual(sum(path.suffix == ".docx" for path in published), 66)
            self.assertEqual(sum(path.suffix == ".xlsx" for path in published), 66)

    def test_manifest_rejects_missing_pair_before_publication(self):
        manifest = fixture_manifest()
        manifest.pop()
        with self.assertRaisesRegex(ValueError, "132"):
            expected_delivery_paths(manifest)


if __name__ == "__main__":
    unittest.main()
