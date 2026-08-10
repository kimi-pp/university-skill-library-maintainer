"""Contract tests for Task 7 visual-QA inventory and contact sheets."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


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


def write_png(
    path: Path,
    size: tuple[int, int] = (900, 500),
    *,
    background: tuple[int, int, int] = (255, 255, 255),
    content: tuple[int, int, int] | None = (62, 81, 103),
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", size, background)
    if content is not None:
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (size[0] // 10, size[1] // 5, size[0] * 9 // 10, size[1] * 3 // 10),
            fill=content,
        )
    image.save(path)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory_digest(images: list[dict]) -> str:
    bindings = [
        {
            "relative_path": row["relative_path"],
            "image_sha256": row["image_sha256"],
            "width": row["width"],
            "height": row["height"],
        }
        for row in sorted(images, key=lambda item: item["relative_path"])
    ]
    encoded = json.dumps(
        bindings,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def make_audit_fixture(root: Path) -> tuple[Path, Path, Path, dict, list[dict]]:
    image_a = root / "renders" / "a.png"
    image_b = root / "renders" / "b.png"
    write_png(image_a)
    write_png(image_b, content=(33, 106, 78))
    images = [
        {
            "artifact_key": "01-overview",
            "render_kind": "docx_page",
            "relative_path": "renders/a.png",
            "width": 900,
            "height": 500,
            "image_sha256": file_sha256(image_a),
            "review_status": "pending",
        },
        {
            "artifact_key": "01-overview",
            "render_kind": "worksheet",
            "relative_path": "renders/b.png",
            "width": 900,
            "height": 500,
            "image_sha256": file_sha256(image_b),
            "review_status": "pending",
        },
    ]
    digest = inventory_digest(images)
    inventory = {"schema_version": 2, "inventory_digest": digest, "images": images}
    records = [
        {
            "record_type": "session",
            "schema_version": 1,
            "session_id": "session-1",
            "inventory_digest": digest,
            "time_basis": "ordered review-session markers",
        },
        {
            "record_type": "batch",
            "sequence": 1,
            "batch_id": "B1",
            "reviewer_id": "reviewer-1",
            "session_id": "session-1",
            "started_at": "2026-08-09T00:01:00+08:00",
            "ended_at": "2026-08-09T00:02:00+08:00",
            "inspection_criteria": ["截断", "重叠", "缺字", "异常空白"],
        },
        {
            "record_type": "batch",
            "sequence": 2,
            "batch_id": "B2",
            "reviewer_id": "reviewer-1",
            "session_id": "session-1",
            "started_at": "2026-08-09T00:03:00+08:00",
            "ended_at": "2026-08-09T00:04:00+08:00",
            "inspection_criteria": ["截断", "重叠", "缺字", "异常空白"],
        },
        {
            "record_type": "image",
            "relative_path": "renders/a.png",
            "image_sha256": images[0]["image_sha256"],
            "batch_id": "B1",
            "status": "pass",
            "issues": [],
        },
        {
            "record_type": "image",
            "relative_path": "renders/b.png",
            "image_sha256": images[1]["image_sha256"],
            "batch_id": "B2",
            "status": "pass",
            "issues": [],
        },
    ]
    inventory_path = root / "inventory.json"
    review_path = root / "review.jsonl"
    result_path = root / "result.json"
    write_json(inventory_path, inventory)
    write_jsonl(review_path, records)
    return inventory_path, review_path, result_path, inventory, records


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
            self.assertTrue(all(len(row["image_sha256"]) == 64 for row in inventory))

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

    def test_inventory_document_digest_is_stable_and_binds_each_image(self):
        rows = [
            {
                "relative_path": "b.png",
                "image_sha256": "b" * 64,
                "width": 20,
                "height": 10,
                "review_status": "pending",
            },
            {
                "relative_path": "a.png",
                "image_sha256": "a" * 64,
                "width": 10,
                "height": 20,
                "review_status": "pending",
            },
        ]
        first = self.visual_qa.build_inventory_document(rows)
        second = self.visual_qa.build_inventory_document(list(reversed(rows)))
        self.assertEqual(first, second)
        self.assertEqual(first["schema_version"], 2)
        self.assertEqual(first["inventory_digest"], inventory_digest(rows))
        self.assertEqual(
            set(first["images"][0]),
            {"relative_path", "image_sha256", "width", "height", "review_status"},
        )

    def test_png_gate_rejects_pure_and_near_white_but_accepts_light_content(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            pure = root / "pure.png"
            near = root / "near.png"
            light = root / "light.png"
            write_png(pure, content=None)
            write_png(near, background=(253, 253, 253), content=None)
            write_png(light, background=(253, 253, 253), content=(235, 235, 235))
            with self.assertRaisesRegex(ValueError, "空白|近空白"):
                self.visual_qa._validate_png(pure)
            with self.assertRaisesRegex(ValueError, "空白|近空白"):
                self.visual_qa._validate_png(near)
            self.assertEqual(self.visual_qa._validate_png(light), (900, 500))

    def run_finalize_cli(
        self,
        root: Path,
        inventory_path: Path,
        review_path: Path | None,
        result_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(VISUAL_QA_PATH),
            "--finalize",
            "--project-root",
            str(root),
            "--inventory",
            str(inventory_path),
            "--result",
            str(result_path),
        ]
        if review_path is not None:
            command.extend(["--review-log", str(review_path)])
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_finalize_cli_requires_an_explicit_review_log(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path, _, result_path, _, _ = make_audit_fixture(root)
            completed = self.run_finalize_cli(root, inventory_path, None, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("--review-log", completed.stderr)
            self.assertFalse(result_path.exists())

    def test_finalize_cli_accepts_a_valid_multi_batch_hash_bound_review_log(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path, review_path, result_path, inventory, _ = make_audit_fixture(root)
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(result["inventory_digest"], inventory["inventory_digest"])
            self.assertEqual(result["summary"], {"images": 2, "batches": 2, "pass": 2, "nonpass": 0})
            self.assertTrue(result["review_complete"])

    def test_finalize_cli_rejects_missing_duplicate_and_extra_image_records(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path, review_path, result_path, _, records = make_audit_fixture(root)
            mutations = {
                "missing": records[:-1],
                "duplicate": records + [copy.deepcopy(records[-1])],
                "extra": records
                + [
                    {
                        "record_type": "image",
                        "relative_path": "renders/extra.png",
                        "image_sha256": "e" * 64,
                        "batch_id": "B2",
                        "status": "pass",
                        "issues": [],
                    }
                ],
            }
            for label, mutated in mutations.items():
                with self.subTest(label=label):
                    write_jsonl(review_path, mutated)
                    result_path.unlink(missing_ok=True)
                    completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertRegex(completed.stderr, "缺失|重复|额外|覆盖")
                    self.assertFalse(result_path.exists())

    def test_finalize_cli_rejects_wrong_review_hash_and_post_review_image_replacement(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path, review_path, result_path, _, records = make_audit_fixture(root)
            wrong_hash = copy.deepcopy(records)
            wrong_hash[-1]["image_sha256"] = "f" * 64
            write_jsonl(review_path, wrong_hash)
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("hash", completed.stderr.lower())

            write_jsonl(review_path, records)
            write_png(root / "renders" / "b.png", content=(120, 50, 40))
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertRegex(completed.stderr.lower(), "hash|替换")
            self.assertFalse(result_path.exists())

    def test_finalize_cli_rejects_inventory_and_review_digest_drift(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path, review_path, result_path, inventory, records = make_audit_fixture(root)
            drifted_inventory = copy.deepcopy(inventory)
            drifted_inventory["inventory_digest"] = "0" * 64
            write_json(inventory_path, drifted_inventory)
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("inventory_digest", completed.stderr)

            write_json(inventory_path, inventory)
            drifted_review = copy.deepcopy(records)
            drifted_review[0]["inventory_digest"] = "1" * 64
            write_jsonl(review_path, drifted_review)
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("inventory_digest", completed.stderr)
            self.assertFalse(result_path.exists())

    def test_finalize_cli_rejects_inconsistent_status_and_issues(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path, review_path, result_path, _, records = make_audit_fixture(root)
            pass_with_issue = copy.deepcopy(records)
            pass_with_issue[-1]["issues"] = ["存在裁切"]
            write_jsonl(review_path, pass_with_issue)
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertRegex(completed.stderr, "pass.*问题|issues")

            fail_without_issue = copy.deepcopy(records)
            fail_without_issue[-1]["status"] = "fail"
            write_jsonl(review_path, fail_without_issue)
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertRegex(completed.stderr, "非 pass|说明|issues")
            self.assertFalse(result_path.exists())

    def test_finalize_cli_rejects_incomplete_or_unreasonable_batch_metadata(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            inventory_path, review_path, result_path, _, records = make_audit_fixture(root)
            missing_reviewer = copy.deepcopy(records)
            del missing_reviewer[1]["reviewer_id"]
            write_jsonl(review_path, missing_reviewer)
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertRegex(completed.stderr, "reviewer|批次元数据")

            reversed_time = copy.deepcopy(records)
            reversed_time[2]["started_at"] = "2026-08-09T00:00:00+08:00"
            write_jsonl(review_path, reversed_time)
            completed = self.run_finalize_cli(root, inventory_path, review_path, result_path)
            self.assertNotEqual(completed.returncode, 0)
            self.assertRegex(completed.stderr, "时间|顺序")
            self.assertFalse(result_path.exists())


if __name__ == "__main__":
    unittest.main()
