import hashlib
import importlib
import os
import tempfile
import unittest
from pathlib import Path

from skill_maintainer.cli import build_parser
from skill_maintainer.settings import SettingsError, load_settings


WORKFLOW_ROOT = Path(__file__).resolve().parents[1]
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
            "读取规则 → 校验配置哈希 → doctor → prepare → 审核固定证据 → "
            "通过标准输入应用评审 → finalize → 检查每一张 Word 页面图像 → "
            "批准或拒绝发布 → 仅在有变化或失败时通知"
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

    def test_renderer_is_loader_supplied_without_machine_paths(self):
        combined = "\n".join(
            self.read(path)
            for path in (SKILL_PATH, PROJECT_CONTRACT_PATH)
        )
        self.assertIn("工作区依赖加载器", combined)
        self.assertIn("RendererCommand", combined)
        self.assertIn("argv", combined)
        self.assertNotRegex(combined, r"[A-Za-z]:\\Users\\")
        self.assertNotIn(".cache/codex-runtimes", combined)

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


if __name__ == "__main__":
    unittest.main()
