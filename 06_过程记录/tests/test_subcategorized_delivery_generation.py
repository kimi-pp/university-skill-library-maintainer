"""Task 6 transaction and end-to-end integration tests."""

from __future__ import annotations

import hashlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = PROJECT_ROOT / "06_过程记录" / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from build_subcategorized_delivery import (  # noqa: E402
    OUTPUT_RELATIVE,
    archive_transaction_paths,
    build_complete_delivery,
    delivery_transaction_paths,
    discover_originals,
    expected_delivery_paths,
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
    for big, count in ((1, 9), (2, 9), (3, 11), (4, 12), (5, 20)):
        for local in range(1, count + 1):
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
    if len(items) != 132:
        raise AssertionError("测试 manifest 构造错误")
    return items


def write_originals(delivery_root: Path, *, uppercase: bool = False) -> list[Path]:
    delivery_root.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for big in range(1, 6):
        for suffix in ("docx", "xlsx"):
            actual_suffix = suffix.upper() if uppercase else suffix
            path = delivery_root / f"{big:02d}_原始报告.{actual_suffix}"
            path.write_bytes(f"original-{big}-{suffix}".encode())
            written.append(path)
    return written


def tree_hashes(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"), key=str)
        if path.is_file()
    }


class FixturePipeline:
    def __init__(self, project: Path, *, payload: str = "v1", manifest: list[dict] | None = None):
        self.project = project
        self.payload = payload
        self.manifest = list(manifest or fixture_manifest())
        self.records = [{"id": f"GH-FIXTURE-{index:04d}"} for index in range(157)]
        self.assignments = {record["id"]: "fixture" for record in self.records}
        self.inputs = {
            "records": self.records,
            "taxonomy": [],
            "manifest": self.manifest,
            "repositories": {},
            "assignments": self.assignments,
        }
        self.fail_documents: Exception | None = None
        self.add_noise = False

    def load_inputs(self, _project: Path) -> dict:
        return self.inputs

    def _write_format(self, staging_root: Path, suffix: str) -> list[Path]:
        if suffix == "docx" and self.fail_documents is not None:
            raise self.fail_documents
        written: list[Path] = []
        for item in self.manifest:
            if item["format"] != suffix:
                continue
            path = staging_root / Path(*item["path"].split("/"))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(f"{self.payload}:{item['path']}".encode())
            written.append(path)
        if self.add_noise and suffix == "xlsx":
            noise = staging_root / OUTPUT_RELATIVE / "noise.tmp"
            noise.write_bytes(b"noise")
        return written

    def build_documents(self, staging_root: Path, _inputs: dict) -> list[Path]:
        return self._write_format(staging_root, "docx")

    def build_spreadsheets(self, staging_root: Path, _inputs: dict) -> list[Path]:
        return self._write_format(staging_root, "xlsx")

    def verify_documents(self, _staging_root: Path, _inputs: dict) -> None:
        return None

    def verify_spreadsheets(self, _staging_root: Path, _inputs: dict) -> None:
        return None

    def kwargs(self) -> dict:
        return {
            "input_loader": self.load_inputs,
            "document_builder": self.build_documents,
            "spreadsheet_builder": self.build_spreadsheets,
            "document_verifier": self.verify_documents,
            "spreadsheet_verifier": self.verify_spreadsheets,
        }


class Task6SourceDiscoveryTests(unittest.TestCase):
    def test_requires_one_docx_and_one_xlsx_for_every_code(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_originals(root)
            (root / "01_原始报告.xlsx").unlink()
            (root / "02_原始报告.docx").unlink()
            (root / "01_另一个版本.docx").write_bytes(b"duplicate-docx")
            (root / "02_另一个版本.xlsx").write_bytes(b"duplicate-xlsx")
            with self.assertRaisesRegex(ValueError, "01.*docx|格式配对"):
                discover_originals(root)

    def test_rejects_missing_multiple_and_ambiguous_same_prefix(self):
        cases = ("missing", "multiple", "ambiguous")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                write_originals(root)
                if case == "missing":
                    (root / "03_原始报告.xlsx").unlink()
                elif case == "multiple":
                    (root / "03_第二份.xlsx").write_bytes(b"extra")
                else:
                    (root / "03_原始报告_副本.docx").write_bytes(b"ambiguous")
                with self.assertRaises(ValueError):
                    discover_originals(root)

    def test_accepts_case_insensitive_extensions_and_excludes_non_source_directories(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            write_originals(root, uppercase=True)
            (root / "0809_不在范围.DOCX").write_bytes(b"excluded")
            for name in ("通俗细分版_2026-08-07", "原始版_2026-08-06", ".task6_delivery.stage"):
                directory = root / name
                directory.mkdir()
                (directory / "01_目录内文件.docx").write_bytes(b"excluded")
            self.assertEqual(len(discover_originals(root)), 10)


class Task6CompleteDeliveryIntegrationTests(unittest.TestCase):
    def make_project(self) -> tuple[Path, tempfile.TemporaryDirectory, FixturePipeline]:
        temporary = tempfile.TemporaryDirectory()
        project = Path(temporary.name) / "project"
        write_originals(project / "05_交付物")
        pipeline = FixturePipeline(project)
        return project, temporary, pipeline

    def run_build(self, project: Path, pipeline: FixturePipeline, **overrides):
        kwargs = pipeline.kwargs()
        kwargs.update(overrides)
        return build_complete_delivery(project, **kwargs)

    def test_complete_orchestration_twice_is_byte_idempotent(self):
        project, temporary, pipeline = self.make_project()
        self.addCleanup(temporary.cleanup)
        delivery = project / OUTPUT_RELATIVE
        archive = project / "05_交付物" / "原始版_2026-08-06"
        source_root = project / "05_交付物"
        sources_before = {path.name: sha256(path) for path in discover_originals(source_root)}

        first = self.run_build(project, pipeline)
        state_one = (tree_hashes(delivery), tree_hashes(archive), sources_before)
        second = self.run_build(project, pipeline)
        state_two = (
            tree_hashes(delivery),
            tree_hashes(archive),
            {path.name: sha256(path) for path in discover_originals(source_root)},
        )

        self.assertEqual(len(first["published"]), 132)
        self.assertEqual(len(second["archive_inventory"]), 10)
        self.assertEqual(state_one, state_two)
        self.assertEqual(len(state_two[0]), 132)
        self.assertEqual(len(state_two[1]), 10)

    def test_manifest_missing_extra_and_staged_noise_fail_before_publish(self):
        for case in ("missing", "extra", "noise"):
            with self.subTest(case=case):
                project, temporary, pipeline = self.make_project()
                self.addCleanup(temporary.cleanup)
                if case == "missing":
                    pipeline.manifest.pop()
                    pipeline.inputs["manifest"] = pipeline.manifest
                elif case == "extra":
                    pipeline.manifest.append({**pipeline.manifest[-1], "path": "05_交付物/通俗细分版_2026-08-07/noise.xlsx"})
                    pipeline.inputs["manifest"] = pipeline.manifest
                else:
                    pipeline.add_noise = True
                with self.assertRaises(ValueError):
                    self.run_build(project, pipeline)
                self.assertFalse((project / OUTPUT_RELATIVE).exists())

    def test_wrong_archive_target_is_rejected_before_copy(self):
        project, temporary, pipeline = self.make_project()
        self.addCleanup(temporary.cleanup)
        for wrong in (project, project / "05_交付物", project / "outside" / "原始版_2026-08-06"):
            with self.subTest(wrong=wrong), self.assertRaisesRegex(ValueError, "归档目标"):
                self.run_build(project, pipeline, archive_root=wrong)

    def test_copy_failure_and_source_change_leave_no_partial_archive(self):
        for case in ("copy-failure", "source-change"):
            with self.subTest(case=case):
                project, temporary, pipeline = self.make_project()
                self.addCleanup(temporary.cleanup)
                calls = 0

                def copy_file(source: Path, target: Path):
                    nonlocal calls
                    calls += 1
                    shutil.copy2(source, target)
                    if case == "copy-failure" and calls == 3:
                        raise OSError("injected copy failure")
                    if case == "source-change" and calls == 3:
                        source.write_bytes(source.read_bytes() + b"changed")

                with self.assertRaises((OSError, ValueError)):
                    self.run_build(project, pipeline, copy_file=copy_file)
                paths = archive_transaction_paths(project)
                self.assertFalse(paths.final.exists())
                self.assertFalse(paths.stage_root.exists())
                self.assertFalse(paths.marker.exists())

    def test_archive_publish_failure_rolls_back_old_complete_archive(self):
        project, temporary, pipeline = self.make_project()
        self.addCleanup(temporary.cleanup)
        self.run_build(project, pipeline)
        paths = archive_transaction_paths(project)
        before = tree_hashes(paths.final)
        failed = False

        def replace(source: Path, target: Path):
            nonlocal failed
            if not failed and Path(source).resolve() == paths.stage_dir and Path(target).resolve() == paths.final:
                failed = True
                raise OSError("injected archive publish failure")
            return Path(source).replace(target)

        with self.assertRaises(OSError):
            self.run_build(project, pipeline, replace_path=replace)
        self.assertEqual(tree_hashes(paths.final), before)
        self.assertFalse(paths.backup.exists())
        self.assertFalse(paths.stage_root.exists())

    def test_delivery_publish_failure_rolls_back_old_complete_delivery(self):
        project, temporary, pipeline = self.make_project()
        self.addCleanup(temporary.cleanup)
        self.run_build(project, pipeline)
        paths = delivery_transaction_paths(project)
        before = tree_hashes(paths.final)
        pipeline.payload = "v2"
        failed = False

        def replace(source: Path, target: Path):
            nonlocal failed
            if not failed and Path(source).resolve() == paths.stage_dir and Path(target).resolve() == paths.final:
                failed = True
                raise OSError("injected delivery publish failure")
            return Path(source).replace(target)

        with self.assertRaises(OSError):
            self.run_build(project, pipeline, replace_path=replace)
        self.assertEqual(tree_hashes(paths.final), before)
        self.assertFalse(paths.backup.exists())
        self.assertFalse(paths.stage_root.exists())

    def test_crash_after_final_to_backup_is_recovered_on_next_build(self):
        project, temporary, pipeline = self.make_project()
        self.addCleanup(temporary.cleanup)
        self.run_build(project, pipeline)
        paths = delivery_transaction_paths(project)
        before = tree_hashes(paths.final)
        pipeline.payload = "v2"

        def crash(name: str, phase: str):
            if name == "delivery" and phase == "after_final_to_backup":
                raise SystemExit("simulated process death")

        with self.assertRaises(SystemExit):
            self.run_build(project, pipeline, transaction_hook=crash)
        self.assertFalse(paths.final.exists())
        self.assertTrue(paths.backup.exists())
        pipeline.fail_documents = RuntimeError("stop after startup recovery")
        with self.assertRaises(RuntimeError):
            self.run_build(project, pipeline)
        self.assertEqual(tree_hashes(paths.final), before)
        self.assertFalse(paths.backup.exists())
        self.assertFalse(paths.stage_root.exists())

    def test_crash_with_new_final_keeps_valid_final_or_rolls_back_invalid_final(self):
        for corrupt in (False, True):
            with self.subTest(corrupt=corrupt):
                project, temporary, pipeline = self.make_project()
                self.addCleanup(temporary.cleanup)
                self.run_build(project, pipeline)
                paths = delivery_transaction_paths(project)
                old = tree_hashes(paths.final)
                pipeline.payload = "v2"

                def crash(name: str, phase: str):
                    if name == "delivery" and phase == "after_stage_to_final":
                        raise SystemExit("simulated process death")

                with self.assertRaises(SystemExit):
                    self.run_build(project, pipeline, transaction_hook=crash)
                self.assertTrue(paths.final.exists())
                self.assertTrue(paths.backup.exists())
                if corrupt:
                    (paths.final / "noise.tmp").write_bytes(b"corrupt")
                pipeline.fail_documents = RuntimeError("stop after startup recovery")
                with self.assertRaises(RuntimeError):
                    self.run_build(project, pipeline)
                if corrupt:
                    self.assertEqual(tree_hashes(paths.final), old)
                else:
                    self.assertNotEqual(tree_hashes(paths.final), old)
                self.assertFalse(paths.backup.exists())

    def test_startup_cleans_only_task_owned_stage_backup_noise(self):
        project, temporary, pipeline = self.make_project()
        self.addCleanup(temporary.cleanup)
        self.run_build(project, pipeline)
        paths = delivery_transaction_paths(project)
        paths.stage_root.mkdir(parents=True)
        (paths.stage_root / "noise.tmp").write_bytes(b"noise")
        paths.backup.mkdir()
        (paths.backup / "noise.tmp").write_bytes(b"noise")
        user_dir = paths.final.parent / ".task6_delivery.backup-user"
        user_dir.mkdir()
        (user_dir / "keep.txt").write_text("keep", encoding="utf-8")
        pipeline.fail_documents = RuntimeError("stop after recovery")
        with self.assertRaises(RuntimeError):
            self.run_build(project, pipeline)
        self.assertFalse(paths.stage_root.exists())
        self.assertFalse(paths.backup.exists())
        self.assertTrue((user_dir / "keep.txt").exists())


if __name__ == "__main__":
    unittest.main()
