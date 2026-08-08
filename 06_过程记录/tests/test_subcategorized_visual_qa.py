"""Contract tests for Task 7 visual-QA inventory and contact sheets."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = PROJECT_ROOT / "06_过程记录" / "tools"
VISUAL_QA_PATH = TOOLS_DIR / "make_subcategorized_contact_sheets.py"


def load_visual_qa_module():
    if not VISUAL_QA_PATH.exists():
        raise AssertionError(f"缺少计划脚本: {VISUAL_QA_PATH.name}")
    spec = importlib.util.spec_from_file_location("make_subcategorized_contact_sheets", VISUAL_QA_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def fixture_manifest() -> list[dict]:
    return [
        {
            "key": "01-overview",
            "format": "docx",
            "path": "05_交付物/通俗细分版_2026-08-07/01_示例/00_大分类总览.docx",
        },
        {
            "key": "01-overview",
            "format": "xlsx",
            "path": "05_交付物/通俗细分版_2026-08-07/01_示例/00_大分类总览.xlsx",
        },
    ]


def write_png(path: Path, size: tuple[int, int] = (900, 500)) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, "white").save(path)


def write_docx_render_manifest(directory: Path, names: list[str]) -> None:
    (directory / "rendered-pages.json").write_text(
        json.dumps({"pages": names}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


class VisualQaContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.visual_qa = load_visual_qa_module()

    def test_delivery_validation_rejects_missing_empty_extra_and_non_manifest_files(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            manifest = fixture_manifest()
            for item in manifest:
                path = root / item["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"artifact")
            accepted = self.visual_qa.validate_delivery_tree(root, manifest)
            self.assertEqual({path.suffix for path in accepted}, {".docx", ".xlsx"})

            (root / manifest[0]["path"]).unlink()
            with self.assertRaisesRegex(ValueError, "缺失"):
                self.visual_qa.validate_delivery_tree(root, manifest)

            (root / manifest[0]["path"]).write_bytes(b"artifact")
            (root / manifest[1]["path"]).write_bytes(b"")
            with self.assertRaisesRegex(ValueError, "空文件"):
                self.visual_qa.validate_delivery_tree(root, manifest)

            (root / manifest[1]["path"]).write_bytes(b"artifact")
            (root / "05_交付物/通俗细分版_2026-08-07/01_示例/notes.txt").write_text(
                "noise", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "额外|非 manifest"):
                self.visual_qa.validate_delivery_tree(root, manifest)

    def test_docx_inventory_requires_sequential_nonblank_original_pages(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            render_root = Path(temporary_directory)
            directory = render_root / "01-overview"
            write_png(directory / "page-1.png")
            write_png(directory / "page-2.png")
            write_docx_render_manifest(directory, ["page-1.png", "page-2.png"])
            inventory = self.visual_qa.collect_docx_render_inventory(
                render_root, fixture_manifest()
            )
            self.assertEqual([row["page_number"] for row in inventory], [1, 2])
            self.assertTrue(all(row["review_status"] == "pending" for row in inventory))

            (directory / "page-2.png").rename(directory / "page-3.png")
            write_docx_render_manifest(directory, ["page-1.png", "page-3.png"])
            with self.assertRaisesRegex(ValueError, "连续"):
                self.visual_qa.collect_docx_render_inventory(render_root, fixture_manifest())

    def test_docx_inventory_rejects_stale_pages_outside_the_renderer_expected_set(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            render_root = Path(temporary_directory)
            directory = render_root / "01-overview"
            write_png(directory / "page-1.png")
            write_png(directory / "page-2.png")
            write_png(directory / "page-3.png")
            write_docx_render_manifest(directory, ["page-1.png", "page-2.png"])
            with self.assertRaisesRegex(ValueError, "预期集合|残留"):
                self.visual_qa.collect_docx_render_inventory(render_root, fixture_manifest())

    def test_render_inventory_derives_keys_from_the_real_manifest_shape(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            render_root = Path(temporary_directory)
            write_png(render_root / "01-overview" / "page-1.png")
            write_docx_render_manifest(render_root / "01-overview", ["page-1.png"])
            manifest = [
                {
                    "format": "docx",
                    "scope": "overview",
                    "big_category_code": "01",
                    "path": "05_交付物/通俗细分版_2026-08-07/01_示例/00_大分类总览.docx",
                }
            ]
            inventory = self.visual_qa.collect_docx_render_inventory(render_root, manifest)
            self.assertEqual(inventory[0]["artifact_key"], "01-overview")

    def test_xlsx_inventory_requires_four_original_sheets_and_long_table_segments(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            render_root = Path(temporary_directory)
            directory = render_root / "01-overview"
            originals = [
                "1_使用说明.png",
                "2_AI技能清单.png",
                "3_分类统计.png",
                "4_来源清单.png",
            ]
            for name in originals:
                write_png(directory / name)
            for label in ("title-header", "longest-text", "longest-url", "last-row"):
                write_png(directory / f"2_AI技能清单_segment_{label}_A1-V5.png", (2600, 240))
            inventory = self.visual_qa.collect_xlsx_render_inventory(
                render_root,
                fixture_manifest(),
                required_segment_keys={"01-overview"},
            )
            self.assertEqual(sum(row["render_kind"] == "worksheet" for row in inventory), 4)
            self.assertEqual(sum(row["render_kind"] == "segment" for row in inventory), 4)

            (directory / "2_AI技能清单_segment_last-row_A1-V5.png").unlink()
            with self.assertRaisesRegex(ValueError, "last-row"):
                self.visual_qa.collect_xlsx_render_inventory(
                    render_root,
                    fixture_manifest(),
                    required_segment_keys={"01-overview"},
                )

    def test_contact_sheet_generation_keeps_original_inventory_and_writes_navigation_images(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            originals = []
            for index in range(1, 4):
                path = root / "source" / f"page-{index}.png"
                write_png(path, (1000, 1300))
                originals.append(
                    {
                        "artifact_key": "01-overview",
                        "render_kind": "docx_page",
                        "relative_path": path.relative_to(root).as_posix(),
                        "review_status": "pending",
                    }
                )
            output_root = root / "contacts"
            result = self.visual_qa.make_navigation_contact_sheets(
                root, originals, output_root
            )
            self.assertEqual(len(result), 1)
            self.assertTrue((output_root / "docx_page" / "01-overview.png").is_file())
            self.assertEqual([row["review_status"] for row in originals], ["pending"] * 3)

    def test_finalize_review_requires_exact_reviewed_paths_and_records_attestation(self):
        inventory = [
            {"relative_path": "a/page-1.png", "review_status": "pending"},
            {"relative_path": "b/sheet.png", "review_status": "pending"},
        ]
        with self.assertRaisesRegex(ValueError, "缺少人工复核"):
            self.visual_qa.finalize_review_inventory(inventory, ["a/page-1.png"], "逐张查看原图")
        completed = self.visual_qa.finalize_review_inventory(
            inventory,
            ["a/page-1.png", "b/sheet.png"],
            "逐张打开原始 PNG，并检查截断、重叠、缺字和空白异常。",
        )
        self.assertTrue(all(row["review_status"] == "pass" for row in completed))
        self.assertTrue(all(row["inspection_method"].startswith("逐张打开") for row in completed))


if __name__ == "__main__":
    unittest.main()
