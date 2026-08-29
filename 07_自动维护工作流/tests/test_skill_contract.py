import builtins
import hashlib
import importlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from skill_maintainer.cli import build_parser
from skill_maintainer.office import RendererCommand
from skill_maintainer.settings import SettingsError, load_settings


WORKFLOW_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = WORKFLOW_ROOT.parent
SKILL_ROOT = WORKFLOW_ROOT / "skill" / "university-skill-library-maintainer"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
AUTOMATION_PROMPT_PATH = SKILL_ROOT / "assets" / "automation-prompt.md"
PROJECT_CONTRACT_PATH = SKILL_ROOT / "references" / "project-contract.md"
LAUNCHER_PATH = WORKFLOW_ROOT / "edit-settings.ps1"
PUBLIC_COMMANDS = {
    "setup",
    "import-existing",
    "doctor",
    "edit-settings",
    "apply-settings",
    "run-now",
    "scheduled-run",
    "status",
    "repair-ledger",
    "rebuild-report",
}


def editor_module():
    return importlib.import_module("skill_maintainer.settings_editor")


def renderer_module():
    return importlib.import_module("skill_maintainer.workspace_renderer")


def valid_toml(mode: str = "weekly") -> str:
    return f'''config_version = 1

[workflow]
enabled = true
timezone = "Asia/Shanghai"

[schedule]
mode = "{mode}"
start_time = "22:00"
weekdays = ["Monday", "Wednesday", "Friday"]
interval_days = 7
day_of_month = 15

[research]
incremental_search = true
full_recheck_interval_days = 14
check_existing_skill_updates = true
include_generic_skills = true

[delivery]
generate_word = true
generate_excel = true
only_refresh_affected_classes = true
notify_on_no_change = false
'''


class SkillContractTest(unittest.TestCase):
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_skill_requires_current_rules_before_research(self):
        text = self.read(SKILL_PATH)
        required = (
            "AGENTS.md",
            "01_规则/SKILL_RESEARCH_WORKFLOW.md",
            "01_规则/SECURITY_REVIEW_PROTOCOL.md",
            "01_规则/DATA_DICTIONARY.md",
            "01_规则/REPORTING_STANDARD.md",
        )
        positions = [text.index(item) for item in required]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("开始任何发现、复核或报告工作前", text)

    def test_skill_preserves_source_and_candidate_boundaries(self):
        text = self.read(SKILL_PATH)
        source_positions = [
            text.index(source)
            for source in ("SkillHub", "ClawHub", "GitHub", "Hugging Face Spaces")
        ]
        self.assertEqual(source_positions, sorted(source_positions))
        for phrase in ("不安装", "不执行", "不调用候选自身外部服务"):
            self.assertIn(phrase, text)
        for tier in ("正式推荐", "条件候选", "需适配候选"):
            self.assertIn(tier, text)
        self.assertIn("分别保存", text)

    def test_every_public_skill_command_exists_in_cli(self):
        text = self.read(SKILL_PATH)
        parser = build_parser()
        commands = set(parser._subparsers._group_actions[0].choices)
        self.assertTrue(PUBLIC_COMMANDS <= commands)
        for command in PUBLIC_COMMANDS:
            self.assertIn(f"`{command}`", text)

    def test_scheduled_run_contract_is_exact_and_fail_closed(self):
        text = self.read(SKILL_PATH)
        sequence = (
            "读取规则 → 校验配置哈希 → doctor → 同一长驻进程 prepare → "
            "材料事实观察 → 项目评审决定 → finalize → 逐页视觉决定 → "
            "原子发布 → 仅在有变化或失败时通知"
        )
        self.assertIn(sequence, text)
        for blocker in (
            "配置哈希不一致",
            "enabled=false",
            "mode=manual",
            "主台账无效",
            "重建范围前专业目录门发生变化",
        ):
            self.assertIn(blocker, text)

    def test_apply_settings_uses_app_tool_and_verifies_readback(self):
        text = self.read(SKILL_PATH)
        self.assertIn("搜索并调用应用提供的自动任务更新工具", text)
        self.assertIn("项目、计划、提示词和配置哈希", text)
        self.assertNotIn("::automation", text)
        self.assertNotIn("automation-update{", text)
        self.assertIn("每天", text)
        self.assertIn("运行记录", text)

    def test_renderer_is_built_from_loader_fields_without_machine_paths(self):
        combined = "\n".join(
            self.read(path)
            for path in (SKILL_PATH, PROJECT_CONTRACT_PATH)
        )
        self.assertIn("工作区依赖加载器", combined)
        self.assertIn("RendererCommand", combined)
        self.assertIn("build_workspace_renderer_command", combined)
        self.assertIn("pdf_renderer.py", combined)
        self.assertIn("argv", combined)
        self.assertNotIn("加载器提供的渲染 argv", combined)
        self.assertNotRegex(combined, r"[A-Za-z]:\\Users\\")
        self.assertNotIn(".cache/codex-runtimes", combined)

    def test_renderer_command_documents_loader_bound_project_built_ownership(self):
        self.assertIn("loader-bound dependencies", RendererCommand.__doc__)
        self.assertIn("project-built entrypoint", RendererCommand.__doc__)

    def test_automation_prompt_has_only_bound_runtime_inputs(self):
        text = self.read(AUTOMATION_PROMPT_PATH)
        for token in (
            "{{ABSOLUTE_PROJECT_ROOT}}",
            "{{ABSOLUTE_TOML_PATH}}",
            "{{APPLIED_TOML_SHA256}}",
        ):
            self.assertIn(token, text)
        self.assertIn("`scheduled-run`", text)
        self.assertIn("不得覆盖目标或专业范围", text)
        self.assertIn("无变化且成功时静默结束", text)

    def test_powershell_launcher_uses_project_virtual_environment(self):
        text = self.read(LAUNCHER_PATH)
        self.assertIn(".venv", text)
        self.assertIn("Scripts", text)
        self.assertIn("python.exe", text)
        self.assertIn("skill_maintainer.settings_editor", text)
        self.assertNotRegex(text, r"[A-Za-z]:\\Users\\")
        self.assertNotRegex(text, r"(?m)^\s*&\s+python(?:\.exe)?\b")


class SettingsEditorTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.path = Path(self.tempdir.name) / "workflow-settings.toml"

    def settings(self, mode: str):
        self.path.write_text(valid_toml(mode), encoding="utf-8")
        return load_settings(self.path)

    def test_chinese_form_round_trips_every_mode(self):
        editor = editor_module()
        labels = {
            "daily": "每天",
            "weekly": "每周",
            "interval": "按间隔天数",
            "monthly": "每月",
            "manual": "手动",
        }
        for mode, label in labels.items():
            with self.subTest(mode=mode):
                original = self.settings(mode)
                form = editor.settings_to_form(original)
                self.assertEqual(form.mode, label)
                self.assertEqual(form.weekdays, ("星期一", "星期三", "星期五"))
                self.assertEqual(editor.form_to_settings(form), original)

    def test_cancel_is_a_no_op(self):
        editor = editor_module()
        self.path.write_text(valid_toml(), encoding="utf-8")
        before = self.path.read_bytes()
        before_hash = hashlib.sha256(before).hexdigest()
        self.assertFalse(editor.apply_form_edit(self.path, None))
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(), before_hash)

    def test_invalid_form_cannot_save(self):
        editor = editor_module()
        original = self.settings("weekly")
        form = editor.settings_to_form(original)
        invalid = editor.replace(form, start_time="25:61")
        before = self.path.read_bytes()
        with self.assertRaises(SettingsError):
            editor.apply_form_edit(self.path, invalid)
        self.assertEqual(self.path.read_bytes(), before)

    def test_save_uses_same_directory_temporary_and_atomic_replace(self):
        editor = editor_module()
        original = self.settings("daily")
        form = editor.settings_to_form(original)
        updated = editor.replace(form, mode="每月", day_of_month="28")
        calls: list[tuple[Path, Path]] = []

        def replace_spy(source, destination):
            source_path = Path(source)
            destination_path = Path(destination)
            calls.append((source_path, destination_path))
            self.assertEqual(source_path.parent, self.path.parent)
            self.assertEqual(destination_path, self.path)
            os.replace(source_path, destination_path)

        self.assertTrue(editor.apply_form_edit(self.path, updated, replace_file=replace_spy))
        self.assertEqual(len(calls), 1)
        self.assertFalse(calls[0][0].exists())
        saved = load_settings(self.path)
        self.assertEqual(saved.schedule.mode, "monthly")
        self.assertEqual(saved.schedule.day_of_month, 28)


class WorkspaceRendererBuilderTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name).absolute()
        self.runtime = self.root / "runtime" / "dependencies"
        paths = self.create_runtime(self.runtime)
        self.python = paths["python"]
        self.packages = paths["packages"]
        self.override = paths["override"]
        self.fallback = paths["fallback"]
        self.poppler_bin = paths["poppler_bin"]

    def create_runtime(self, runtime: Path) -> dict[str, Path]:
        python = runtime / "python" / "python.exe"
        packages = runtime / "python"
        override = runtime / "bin" / "override"
        fallback = runtime / "bin" / "fallback"
        poppler_bin = runtime / "native" / "poppler" / "Library" / "bin"
        for directory in (python.parent, override, fallback, poppler_bin):
            directory.mkdir(parents=True, exist_ok=True)
        python.write_bytes(b"python")
        (poppler_bin / "pdftoppm.exe").write_bytes(b"pdftoppm")
        (poppler_bin / "pdfinfo.exe").write_bytes(b"pdfinfo")
        nested = runtime / "native" / "poppler" / "bin"
        nested.mkdir(parents=True)
        (nested / "pdftoppm.cmd").write_text(
            '@echo off\n"%~dp0..\\Library\\bin\\pdftoppm.exe" %*\n',
            encoding="utf-8",
        )
        (override / "pdftoppm.cmd").write_text(
            '@echo off\nset "SCRIPT_DIR=%~dp0"\ncall "%SCRIPT_DIR%..\\..\\native\\poppler\\bin\\pdftoppm.cmd" %*\n',
            encoding="utf-8",
        )
        return {
            "python": python,
            "packages": packages,
            "override": override,
            "fallback": fallback,
            "poppler_bin": poppler_bin,
        }

    def loader_output(self, **overrides: Path) -> str:
        values = {
            "python": self.python,
            "packages": self.packages,
            "override": self.override,
            "fallback": self.fallback,
        }
        values.update(overrides)
        return (
            "Workspace dependencies are available for this local desktop thread.\n\n"
            "### Workspace Dependencies\n"
            "- Bundle version: `test-bundle`\n"
            f"- Python executable: `{values['python']}`\n"
            f"- Python packages: `{values['packages']}`\n"
            f"- Override binaries: `{values['override']}`\n"
            f"- Fallback binaries: `{values['fallback']}`\n"
        )

    def test_real_loader_shape_builds_project_renderer_argv_only_from_bound_paths(self):
        module = renderer_module()
        command = module.build_workspace_renderer_command(self.loader_output(), PROJECT_ROOT)
        entrypoint = WORKFLOW_ROOT / "src" / "skill_maintainer" / "pdf_renderer.py"
        self.assertEqual(
            command.argv,
            (
                str(self.python),
                str(entrypoint),
                "--python-packages",
                str(self.packages),
                "--pdftoppm",
                str(self.poppler_bin / "pdftoppm.exe"),
            ),
        )

    def test_missing_loader_field_and_nonordinary_paths_fail_closed(self):
        module = renderer_module()
        missing = self.loader_output().replace(
            f"- Fallback binaries: `{self.fallback}`\n", ""
        )
        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(missing, PROJECT_ROOT)

        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(
                self.loader_output(python=self.python.parent), PROJECT_ROOT
            )

        absent_project = self.root / "empty-project"
        absent_project.mkdir()
        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(self.loader_output(), absent_project)

        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(self.loader_output(), Path("."))

    def test_reparse_runtime_component_is_rejected(self):
        module = renderer_module()
        real_override = self.root / "real-override"
        real_override.mkdir()
        linked_override = self.runtime / "bin" / "linked-override"
        try:
            linked_override.symlink_to(real_override, target_is_directory=True)
        except OSError as exc:
            self.fail(f"test environment must support a directory reparse point: {exc}")
        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(
                self.loader_output(override=linked_override), PROJECT_ROOT
            )

    def test_wrapper_escape_and_path_fallback_are_rejected(self):
        module = renderer_module()
        outside = self.root / "outside" / "pdftoppm.exe"
        outside.parent.mkdir()
        outside.write_bytes(b"outside")
        (self.override / "pdftoppm.cmd").write_text(
            f'@echo off\n"{outside}" %*\n', encoding="utf-8"
        )
        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(self.loader_output(), PROJECT_ROOT)

        (self.override / "pdftoppm.cmd").unlink()
        path_bin = self.root / "path-bin"
        path_bin.mkdir()
        (path_bin / "pdftoppm.exe").write_bytes(b"path")
        with patch.dict(os.environ, {"PATH": str(path_bin)}), self.assertRaises(
            module.WorkspaceRendererError
        ):
            module.build_workspace_renderer_command(self.loader_output(), PROJECT_ROOT)

    def test_mixed_adjacent_and_fake_dependency_roots_are_rejected(self):
        module = renderer_module()
        other = self.create_runtime(self.root / "runtime-b" / "dependencies")
        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(
                self.loader_output(
                    override=other["override"], fallback=other["fallback"]
                ),
                PROJECT_ROOT,
            )

        adjacent = self.create_runtime(self.root / "runtime" / "dependencies-adjacent")
        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(
                self.loader_output(
                    override=adjacent["override"], fallback=adjacent["fallback"]
                ),
                PROJECT_ROOT,
            )

        fake_root = self.create_runtime(self.root / "fake-parent")
        with self.assertRaises(module.WorkspaceRendererError):
            module.build_workspace_renderer_command(
                self.loader_output(
                    python=fake_root["python"],
                    packages=fake_root["packages"],
                    override=fake_root["override"],
                    fallback=fake_root["fallback"],
                ),
                PROJECT_ROOT,
            )


class ProjectPdfRendererCliTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name).absolute()
        self.entrypoint = WORKFLOW_ROOT / "src" / "skill_maintainer" / "pdf_renderer.py"
        self.packages = self.root / "packages"
        self.packages.mkdir()
        self.pdftoppm = self.root / "pdftoppm.exe"
        self.pdftoppm.write_bytes(b"not-used")
        (self.root / "pdfinfo.exe").write_bytes(b"not-used")
        self.pdf = self.root / "input.pdf"
        self.pdf.write_bytes(b"%PDF-not-rendered")
        self.output = self.root / "output"
        self.output.mkdir()

    def run_renderer(self, *, pdf: str | None = None):
        return subprocess.run(
            [
                sys.executable,
                str(self.entrypoint),
                "--python-packages",
                str(self.packages),
                "--pdftoppm",
                str(self.pdftoppm),
                "--pdf",
                str(self.pdf) if pdf is None else pdf,
                "--output-dir",
                str(self.output),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def test_relative_pdf_fails_without_stdout_or_output(self):
        result = self.run_renderer(pdf="relative.pdf")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith("renderer-error:"), result.stderr)
        self.assertEqual(tuple(self.output.iterdir()), ())

    def test_nonempty_output_fails_without_touching_existing_file(self):
        sentinel = self.output / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        result = self.run_renderer()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith("renderer-error:"), result.stderr)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        self.assertEqual(tuple(self.output.iterdir()), (sentinel,))

    def test_output_directory_may_contain_the_exact_word_com_input_pdf(self):
        module = importlib.import_module("skill_maintainer.pdf_renderer")
        word_pdf = self.output / "word.office.pdf"
        self.pdf.replace(word_pdf)
        argv = [
            "--python-packages", str(self.packages),
            "--pdftoppm", str(self.pdftoppm),
            "--pdf", str(word_pdf),
            "--output-dir", str(self.output),
        ]
        with patch.object(
            module, "_extend_package_path", side_effect=RuntimeError("reached-loader")
        ), self.assertRaisesRegex(RuntimeError, "reached-loader"):
            module.render(argv)
        self.assertEqual(tuple(self.output.iterdir()), (word_pdf,))

    def test_package_lib_reparse_is_rejected_before_import_or_sys_path_change(self):
        module = importlib.import_module("skill_maintainer.pdf_renderer")
        outside = self.root / "outside"
        (outside / "site-packages").mkdir(parents=True)
        try:
            (self.packages / "Lib").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.fail(f"test environment must support a directory reparse point: {exc}")
        before = tuple(sys.path)
        imports: list[str] = []
        original_import = builtins.__import__

        def import_spy(name, *args, **kwargs):
            imports.append(name)
            return original_import(name, *args, **kwargs)

        argv = [
            "--python-packages", str(self.packages),
            "--pdftoppm", str(self.pdftoppm),
            "--pdf", str(self.pdf),
            "--output-dir", str(self.output),
        ]
        with patch("builtins.__import__", side_effect=import_spy), self.assertRaises(
            module.PdfRendererError
        ):
            module.render(argv)
        self.assertEqual(tuple(sys.path), before)
        self.assertNotIn("pdf2image", imports)
        self.assertNotIn("PIL", imports)
        self.assertEqual(tuple(self.output.iterdir()), ())


if __name__ == "__main__":
    unittest.main()
