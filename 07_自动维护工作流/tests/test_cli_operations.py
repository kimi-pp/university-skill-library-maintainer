"""Task 13: deployment operations and the long-lived two-gate CLI protocol."""

from __future__ import annotations

from contextlib import redirect_stdout
from dataclasses import asdict, replace
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from docx import Document
from openpyxl import Workbook

from skill_maintainer import cli
from skill_maintainer.ledger import LedgerStore
from skill_maintainer.locking import SingleWriterLock
from skill_maintainer.office import RendererCommand
from skill_maintainer.runner import RunCoordinator, RunRequest, SourceRun
from skill_maintainer.settings import load_settings, settings_sha256


WORKFLOW = "07_自动维护工作流"
RULE_FILES = (
    "SKILL_RESEARCH_WORKFLOW.md",
    "SECURITY_REVIEW_PROTOCOL.md",
    "DATA_DICTIONARY.md",
    "REPORTING_STANDARD.md",
)


class _DoctorEnvironment:
    def __init__(
        self,
        *,
        windows: bool = True,
        python: bool = True,
        gh: bool = True,
        word: bool = True,
        excel: bool = True,
        loader_output: str | None = None,
    ) -> None:
        self.is_windows = windows
        self.python_available = python
        self.gh_available = gh
        self.word_available = word
        self.excel_available = excel
        self.loader_output = loader_output


class _RecordingOutput:
    def __init__(self) -> None:
        self.text = ""
        self.flush_count = 0

    def write(self, value: str) -> int:
        self.text += value
        return len(value)

    def flush(self) -> None:
        self.flush_count += 1

    @property
    def frames(self) -> list[dict[str, object]]:
        return [json.loads(line) for line in self.text.splitlines() if line.strip()]


class _ReactiveInput:
    """Respond to the latest flushed request without precomputing evidence hashes."""

    def __init__(self, output: _RecordingOutput, *, visual_approved: bool = True, eof_at: str | None = None) -> None:
        self.output = output
        self.visual_approved = visual_approved
        self.eof_at = eof_at
        self.seen: set[str] = set()

    def readline(self) -> str:
        request = self.output.frames[-1]
        frame_type = str(request["type"])
        if frame_type in self.seen:
            raise AssertionError(f"protocol requested {frame_type} twice")
        self.seen.add(frame_type)
        if self.eof_at == frame_type:
            return ""
        if frame_type == "review_required":
            return json.dumps(
                {"type": "review_decisions", "run_id": request["run_id"], "decisions": []},
                ensure_ascii=False,
            ) + "\n"
        if frame_type == "word_visual_review_required":
            documents = []
            for document in request["documents"]:
                documents.append(
                    {
                        "source_sha256": document["source_sha256"],
                        "pdf_sha256": document["pdf_sha256"],
                        "reviewer": "Task13 离线复核",
                        "pages": [
                            {
                                "page_number": page["page_number"],
                                "sha256": page["sha256"],
                                "approved": self.visual_approved,
                            }
                            for page in document["pages"]
                        ],
                    }
                )
            return json.dumps(
                {"type": "word_visual_decisions", "run_id": request["run_id"], "documents": documents},
                ensure_ascii=False,
            ) + "\n"
        raise AssertionError(f"unexpected protocol request: {frame_type}")


class _UnitRenderer:
    def render(self, pdf: Path, output_dir: Path):
        page = output_dir / "page-1.png"
        page.write_bytes(b"visible-page-body")
        return (page,), (1,)


class CliOperationsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "中文 项目"
        self.root.mkdir()
        self.source_workflow = Path(__file__).resolve().parents[1]

    def _authority_fixture(self, *, missing: str | None = None) -> None:
        (self.root / "AGENTS.md").write_text("# authority\n", encoding="utf-8")
        rule_root = self.root / "01_规则"
        rule_root.mkdir()
        for name in RULE_FILES:
            if name != missing:
                (rule_root / name).write_text(f"# {name}\n", encoding="utf-8")

    def _workflow_fixture(self) -> Path:
        workflow = self.root / WORKFLOW
        workflow.mkdir()
        shutil.copyfile(self.source_workflow / "workflow-settings.example.toml", workflow / "workflow-settings.example.toml")
        shutil.copytree(self.source_workflow / "skill", workflow / "skill")
        source_dir = workflow / "src" / "skill_maintainer"
        source_dir.mkdir(parents=True)
        for name in ("pdf_renderer.py", "workspace_renderer.py", "daily_xlsx_builder.mjs"):
            shutil.copyfile(self.source_workflow / "src" / "skill_maintainer" / name, source_dir / name)
        return workflow

    def _setup_project(self) -> Path:
        self._authority_fixture()
        workflow = self._workflow_fixture()
        result = cli.setup_project(self.root, source_workflow=workflow)
        self.assertEqual(result.exit_code, 0)
        return workflow

    @staticmethod
    def _enabled_settings(path: Path) -> None:
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("enabled = false", "enabled = true").replace('mode = "manual"', 'mode = "daily"'),
            encoding="utf-8",
        )

    def test_parser_keeps_exact_public_commands_and_requires_explicit_project_root(self):
        parser = cli.build_parser()
        commands = parser._subparsers._group_actions[0].choices
        self.assertEqual(
            set(commands),
            {
                "setup", "import-existing", "doctor", "edit-settings", "apply-settings",
                "run-now", "scheduled-run", "status", "repair-ledger", "rebuild-report",
                "prepare", "apply-reviews", "finalize",
            },
        )
        with self.assertRaises(SystemExit) as caught:
            parser.parse_args(["doctor"])
        self.assertEqual(caught.exception.code, 2)

    def test_setup_is_idempotent_creates_disabled_manual_state_and_never_overwrites_settings(self):
        self._authority_fixture()
        workflow = self._workflow_fixture()
        first = cli.setup_project(self.root, source_workflow=workflow)
        self.assertEqual(first.exit_code, 0)
        settings_path = workflow / "workflow-settings.toml"
        settings = load_settings(settings_path)
        self.assertFalse(settings.workflow.enabled)
        self.assertEqual(settings.schedule.mode, "manual")
        self.assertTrue((workflow / "ledger" / "Skills主台账.xlsx").is_file())

        custom = settings_path.read_text(encoding="utf-8").replace("include_generic_skills = false", "include_generic_skills = true")
        settings_path.write_text(custom, encoding="utf-8")
        second = cli.setup_project(self.root, source_workflow=workflow)
        self.assertEqual(second.exit_code, 0)
        self.assertEqual(settings_path.read_text(encoding="utf-8"), custom)

    def test_setup_fails_closed_on_missing_authority_without_creating_state(self):
        self._authority_fixture(missing="SKILL_RESEARCH_WORKFLOW.md")
        workflow = self._workflow_fixture()
        result = cli.setup_project(self.root, source_workflow=workflow)
        self.assertEqual(result.exit_code, 1)
        self.assertFalse((workflow / "workflow-settings.toml").exists())
        self.assertFalse((workflow / "ledger").exists())

    def test_setup_installs_and_updates_skill_in_supplied_codex_root(self):
        self._authority_fixture()
        workflow = self._workflow_fixture()
        skills_root = Path(self.temporary.name) / "Codex Skills"
        first = cli.setup_project(self.root, source_workflow=workflow, codex_skills_root=skills_root)
        self.assertEqual(first.exit_code, 0)
        installed = skills_root / "university-skill-library-maintainer" / "SKILL.md"
        self.assertEqual(installed.read_bytes(), (workflow / "skill" / "university-skill-library-maintainer" / "SKILL.md").read_bytes())
        installed.write_text("stale", encoding="utf-8")
        second = cli.setup_project(self.root, source_workflow=workflow, codex_skills_root=skills_root)
        self.assertEqual(second.exit_code, 0)
        self.assertNotEqual(installed.read_text(encoding="utf-8"), "stale")

    def test_doctor_checks_dependencies_rules_renderer_and_blocks_non_windows_production(self):
        workflow = self._setup_project()
        environment = _DoctorEnvironment(windows=False, python=True, gh=True, word=True, excel=True)
        diagnostic = cli.doctor_project(self.root, environment=environment)
        self.assertEqual(diagnostic.exit_code, 0)
        self.assertFalse(diagnostic.production_ready)
        self.assertEqual(
            set(diagnostic.checks),
            {
                "AGENTS.md", *RULE_FILES, "workflow root", "settings", "ledger",
                "Python", "GitHub CLI", "Microsoft Word", "Microsoft Excel",
                "renderer", "production_driver",
            },
        )
        self.assertEqual(diagnostic.checks["renderer"], "等待 Codex 工作区依赖加载器")
        self._enabled_settings(workflow / "workflow-settings.toml")
        production = cli.doctor_project(self.root, environment=environment)
        self.assertEqual(production.exit_code, 1)
        self.assertIn("Windows", " ".join(production.errors))
        self.assertIn("生产发现驱动未配置", " ".join(production.errors))

    def test_doctor_fails_when_any_required_dependency_or_rule_is_missing(self):
        workflow = self._setup_project()
        (self.root / "01_规则" / "REPORTING_STANDARD.md").unlink()
        environment = _DoctorEnvironment(python=False, gh=False, word=False, excel=False)
        report = cli.doctor_project(self.root, environment=environment)
        self.assertEqual(report.exit_code, 1)
        self.assertEqual(report.checks["REPORTING_STANDARD.md"], "缺失")
        self.assertEqual(report.checks["Python"], "不可用")
        self.assertEqual(report.checks["GitHub CLI"], "不可用")
        self.assertEqual(report.checks["Microsoft Word"], "不可用")
        self.assertEqual(report.checks["Microsoft Excel"], "不可用")
        self.assertTrue((workflow / "workflow-settings.toml").is_file())

    def test_apply_settings_returns_validated_prompt_schedule_and_hash_without_mutating_automation(self):
        workflow = self._setup_project()
        settings_path = workflow / "workflow-settings.toml"
        before = {path.relative_to(self.root): sha256(path.read_bytes()).hexdigest() for path in self.root.rglob("*") if path.is_file()}
        plan = cli.build_apply_settings_plan(self.root)
        after = {path.relative_to(self.root): sha256(path.read_bytes()).hexdigest() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(plan["config_sha256"], settings_sha256(settings_path))
        self.assertEqual(plan["automation_action"], "ensure_absent")
        self.assertEqual(plan["schedule"]["mode"], "manual")
        self.assertEqual(plan["project_root"], str(self.root.absolute()))
        self.assertEqual(plan["toml_path"], str(settings_path.absolute()))
        self.assertIn("scheduled-run", plan["prompt"])
        self.assertNotIn("::automation", plan["prompt"])
        self.assertFalse(plan["production_ready"])

    def test_invalid_configuration_returns_exit_two(self):
        workflow = self._setup_project()
        (workflow / "workflow-settings.toml").write_text("not = [valid", encoding="utf-8")
        output = io.StringIO()
        with redirect_stdout(output):
            code = cli.main(["apply-settings", "--project-root", str(self.root)])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output.getvalue())["exit_code"], 2)

    def test_status_reports_driver_not_ready_and_import_defaults_to_safe_noop(self):
        self._setup_project()
        (self.root / "05_交付物").mkdir()
        status = cli.status_project(self.root)
        self.assertFalse(status["production_ready"])
        self.assertEqual(status["production_driver"], "生产发现驱动未配置")
        output = io.StringIO()
        with redirect_stdout(output):
            code = cli.main(["import-existing", "--project-root", str(self.root)])
        self.assertEqual(code, 3)
        self.assertEqual(json.loads(output.getvalue())["excel_files"], 0)

    def test_repair_lists_only_valid_backups_and_explicit_choice_never_overwrites_authority(self):
        workflow = self._setup_project()
        authority = workflow / "ledger" / "Skills主台账.xlsx"
        archive = workflow / "ledger" / "archive"
        archive.mkdir(exist_ok=True)
        valid = archive / "Skills主台账_20260829_010203.xlsx"
        shutil.copyfile(authority, valid)
        (archive / "Skills主台账_20260829_010204.xlsx").write_bytes(b"not-an-xlsx")
        original_sha = sha256(authority.read_bytes()).hexdigest()

        listed = cli.repair_ledger(self.root)
        self.assertEqual(listed.exit_code, 3)
        self.assertEqual(listed.valid_backups, (valid.absolute(),))
        chosen = cli.repair_ledger(self.root, backup=valid)
        self.assertEqual(chosen.exit_code, 0)
        self.assertEqual(sha256(authority.read_bytes()).hexdigest(), original_sha)
        self.assertIsNotNone(chosen.recovery_candidate)
        self.assertEqual(sha256(chosen.recovery_candidate.read_bytes()).hexdigest(), sha256(valid.read_bytes()).hexdigest())

    def test_rebuild_report_reads_only_current_ledger_and_never_calls_network(self):
        workflow = self._setup_project()
        output = workflow / "output" / "rebuild-test"
        calls: list[tuple[str, Path]] = []

        def word_builder(summary, path):
            calls.append(("word", Path(path)))
            Document().save(path)
            return Path(path)

        def excel_builder(summary, path):
            calls.append(("excel", Path(path)))
            Workbook().save(path)
            return Path(path)

        authority = workflow / "ledger" / "Skills主台账.xlsx"
        before = sha256(authority.read_bytes()).hexdigest()
        with patch("urllib.request.urlopen", side_effect=AssertionError("rebuild must be offline")):
            result = cli.rebuild_reports(self.root, output=output, word_builder=word_builder, excel_builder=excel_builder)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual([name for name, _ in calls], ["word", "excel"])
        self.assertEqual(sha256(authority.read_bytes()).hexdigest(), before)
        self.assertEqual({path.suffix for path in result.outputs}, {".docx", ".xlsx"})

    def _protocol_fixture(self, *, visual_approved: bool = True, eof_at: str | None = None):
        workflow = self._setup_project()
        output = _RecordingOutput()
        input_stream = _ReactiveInput(output, visual_approved=visual_approved, eof_at=eof_at)
        gate = cli.InteractiveOfficeGate(input_stream=input_stream, output_stream=output, renderer=_UnitRenderer())

        def build_reports(prepared, staging):
            delivery = staging / "deliveries"
            delivery.mkdir()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "执行概览"
            sheet.append(["项目", "结果"])
            sheet.append(["离线四源", "完成"])
            xlsx = delivery / "离线查验.xlsx"
            workbook.save(xlsx)
            word = Document()
            word.add_paragraph("离线四源查验；候选未安装、未运行。")
            docx = delivery / "离线查验.docx"
            word.save(docx)
            return (xlsx, docx)

        sources = (
            SourceRun("SkillHub", "complete"),
            SourceRun("ClawHub", "complete"),
            SourceRun("GitHub", "complete"),
            SourceRun("Hugging Face Spaces", "complete"),
        )
        coordinator = RunCoordinator(
            root=workflow,
            discover=lambda request, staging: sources,
            report_builder=build_reports,
            office_verifier=gate,
        )
        request = RunRequest(
            settings_path=workflow / "workflow-settings.toml",
            catalog_loader=lambda: {"fixture": "offline-four-source"},
            requested_run_id="run-task13-offline",
        )
        return workflow, coordinator, request, input_stream, output

    @staticmethod
    def _fake_office_result(arguments):
        if "-Excel" in arguments:
            role = arguments[arguments.index("-ExcelRole") + 1]
            return {
                "passed": True,
                "office_opened": True,
                "read_only": True,
                "key_sheet": "运行记录" if role == "ledger" else "执行概览",
                "last_row": 2,
                "last_column": 2,
                "last_value": "verified",
                "process_count_before": 0,
                "process_count_after": 0,
                "error": None,
            }
        render = Path(arguments[arguments.index("-RenderDirectory") + 1])
        pdf = render / "office.pdf"
        pdf.write_bytes(b"unit-pdf")
        return {
            "passed": True,
            "office_opened": True,
            "read_only": True,
            "pdf_path": str(pdf),
            "page_count": 1,
            "process_count_before": 0,
            "process_count_after": 0,
            "error": None,
        }

    def test_long_lived_protocol_keeps_one_process_through_review_visual_and_success(self):
        workflow, coordinator, request, input_stream, output = self._protocol_fixture()
        with patch("skill_maintainer.office._run_office", side_effect=lambda *args: self._fake_office_result(list(args))):
            code = cli.run_interactive_protocol(coordinator, request, input_stream=input_stream, output_stream=output)
        self.assertEqual(code, 0, output.text)
        self.assertEqual(
            [frame["type"] for frame in output.frames],
            ["review_required", "word_visual_review_required", "run_complete"],
        )
        self.assertGreaterEqual(output.flush_count, 3)
        self.assertTrue((workflow / "ledger" / "Skills主台账.xlsx").is_file())
        self.assertTrue(any((workflow / "output").rglob("*.docx")))
        lock = SingleWriterLock(workflow / ".runtime" / "writer.lock")
        self.assertTrue(lock.acquire())
        lock.release()

    def test_protocol_eof_after_prepare_abandons_staging_and_releases_capabilities(self):
        workflow, coordinator, request, input_stream, output = self._protocol_fixture(eof_at="review_required")
        code = cli.run_interactive_protocol(coordinator, request, input_stream=input_stream, output_stream=output)
        self.assertEqual(code, 1)
        self.assertEqual([frame["type"] for frame in output.frames], ["review_required", "run_failed"], output.text)
        self.assertFalse(any((workflow / ".runtime" / "staging").iterdir()))
        lock = SingleWriterLock(workflow / ".runtime" / "writer.lock")
        self.assertTrue(lock.acquire())
        lock.release()

    def test_protocol_requires_one_decision_for_every_review_packet_before_publish(self):
        workflow, coordinator, request, input_stream, output = self._protocol_fixture()
        request = replace(request, review_packets={"candidate-1": {"fixed_snapshot": "offline"}})
        authority = workflow / "ledger" / "Skills主台账.xlsx"
        before = sha256(authority.read_bytes()).hexdigest()
        code = cli.run_interactive_protocol(coordinator, request, input_stream=input_stream, output_stream=output)
        self.assertEqual(code, 2)
        self.assertEqual(sha256(authority.read_bytes()).hexdigest(), before)
        self.assertEqual([frame["type"] for frame in output.frames], ["review_required", "run_failed"])
        self.assertFalse(any((workflow / ".runtime" / "staging").iterdir()))

    def test_protocol_eof_at_visual_gate_preserves_authority_and_cleans_runtime(self):
        workflow, coordinator, request, input_stream, output = self._protocol_fixture(eof_at="word_visual_review_required")
        authority = workflow / "ledger" / "Skills主台账.xlsx"
        before = sha256(authority.read_bytes()).hexdigest()
        with patch("skill_maintainer.office._run_office", side_effect=lambda *args: self._fake_office_result(list(args))):
            code = cli.run_interactive_protocol(coordinator, request, input_stream=input_stream, output_stream=output)
        self.assertEqual(code, 1)
        self.assertEqual(sha256(authority.read_bytes()).hexdigest(), before)
        self.assertEqual(
            [frame["type"] for frame in output.frames],
            ["review_required", "word_visual_review_required", "run_failed"],
        )
        self.assertFalse(any((workflow / ".runtime" / "staging").iterdir()))
        lock = SingleWriterLock(workflow / ".runtime" / "writer.lock")
        self.assertTrue(lock.acquire())
        lock.release()

    def test_protocol_rejected_word_page_preserves_old_authority(self):
        workflow, coordinator, request, input_stream, output = self._protocol_fixture(visual_approved=False)
        authority = workflow / "ledger" / "Skills主台账.xlsx"
        before = sha256(authority.read_bytes()).hexdigest()
        with patch("skill_maintainer.office._run_office", side_effect=lambda *args: self._fake_office_result(list(args))):
            code = cli.run_interactive_protocol(coordinator, request, input_stream=input_stream, output_stream=output)
        self.assertEqual(code, 1)
        self.assertEqual(sha256(authority.read_bytes()).hexdigest(), before)
        self.assertEqual(
            [frame["type"] for frame in output.frames],
            ["review_required", "word_visual_review_required", "run_failed"],
            output.text,
        )
        self.assertFalse(any((workflow / ".runtime" / "staging").iterdir()))

    def test_public_run_commands_fail_before_prepare_when_production_driver_is_unavailable(self):
        workflow = self._setup_project()
        for command in ("run-now", "scheduled-run"):
            with self.subTest(command=command):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = cli.main([command, "--project-root", str(self.root)])
                self.assertEqual(code, 1)
                payload = json.loads(output.getvalue().splitlines()[-1])
                self.assertEqual(payload["type"], "run_failed")
                self.assertIn("生产发现驱动未配置", payload["error"])
                self.assertFalse((workflow / ".runtime").exists())

    def test_independent_stage_commands_refuse_cross_process_capability_reconstruction(self):
        self._setup_project()
        for command in ("prepare", "apply-reviews", "finalize"):
            with self.subTest(command=command):
                output = io.StringIO()
                with redirect_stdout(output):
                    code = cli.main([command, "--project-root", str(self.root)])
                self.assertEqual(code, 1)
                self.assertIn("同一长驻进程", output.getvalue())

    def test_installer_fails_before_creating_environment_when_target_rules_are_missing(self):
        workflow = self.root / WORKFLOW
        shutil.copytree(self.source_workflow, workflow)
        skills_root = Path(self.temporary.name) / "Codex Skills 目录"
        command = [
            "powershell", "-NoProfile", "-File", str(workflow / "install.ps1"),
            "-ProjectRoot", str(self.root), "-PythonExe", sys.executable,
            "-CodexSkillsRoot", str(skills_root),
        ]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((workflow / ".venv").exists())
        self.assertFalse((workflow / "workflow-settings.toml").exists())
        self.assertFalse(skills_root.exists())

    def test_installer_runs_offline_in_chinese_space_path_and_is_idempotent(self):
        self._authority_fixture()
        workflow = self.root / WORKFLOW
        shutil.copytree(self.source_workflow, workflow)
        skills_root = Path(self.temporary.name) / "Codex Skills 目录"
        python = Path(sys.executable)
        installer = workflow / "install.ps1"
        environment = os.environ.copy()
        environment["PIP_NO_INDEX"] = "1"
        command = [
            "powershell", "-NoProfile", "-File", str(installer),
            "-ProjectRoot", str(self.root), "-PythonExe", str(python),
            "-CodexSkillsRoot", str(skills_root),
        ]
        first = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment, timeout=180)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        settings_path = workflow / "workflow-settings.toml"
        settings = load_settings(settings_path)
        self.assertFalse(settings.workflow.enabled)
        self.assertEqual(settings.schedule.mode, "manual")
        self.assertTrue((workflow / ".venv" / "Scripts" / "python.exe").is_file())
        self.assertTrue((skills_root / "university-skill-library-maintainer" / "SKILL.md").is_file())
        self.assertFalse(any("automation" in path.name.casefold() for path in workflow.rglob("*") if path.name != "automation-prompt.md"))

        custom = settings_path.read_text(encoding="utf-8").replace("include_generic_skills = false", "include_generic_skills = true")
        settings_path.write_text(custom, encoding="utf-8")
        second = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment, timeout=180)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(settings_path.read_text(encoding="utf-8"), custom)


if __name__ == "__main__":
    unittest.main()
