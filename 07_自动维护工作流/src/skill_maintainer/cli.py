"""高校专业 Skill 库文件化维护工作流的安全命令入口。"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from typing import Callable, Iterable, Mapping, TextIO
from zipfile import BadZipFile

from .import_existing import build_initial_ledger, scan_existing_deliveries
from .ledger import LedgerStore
from .locking import LockUnavailable
from .office import (
    OfficeEvidenceBundle,
    OfficeVerificationError,
    WordPageDecision,
    WordRenderDecision,
    bind_word_visual_decision,
    verify_excel,
    verify_word,
)
from .paths import assert_ordinary_path, contained_child, is_link_or_reparse
from .reports import build_daily_docx, build_daily_xlsx
from .review import ReviewDecision
from .runner import CoordinatorError, RunCoordinator, RunRequest
from .scheduling import next_run_at, schedule_preview
from .settings import SettingsError, load_settings, settings_sha256
from .workspace_renderer import WorkspaceRendererError, build_workspace_renderer_command


SUCCESS = 0
OPERATIONAL_FAILURE = 1
INVALID_INPUT = 2
SAFE_NOOP = 3

COMMANDS = (
    "setup", "import-existing", "doctor", "edit-settings", "apply-settings",
    "run-now", "scheduled-run", "status", "repair-ledger", "rebuild-report",
    "prepare", "apply-reviews", "finalize",
)
WORKFLOW_DIRECTORY = "07_自动维护工作流"
SKILL_NAME = "university-skill-library-maintainer"
REQUIRED_RULES = (
    "SKILL_RESEARCH_WORKFLOW.md",
    "SECURITY_REVIEW_PROTOCOL.md",
    "DATA_DICTIONARY.md",
    "REPORTING_STANDARD.md",
)
BACKUP_PATTERN = re.compile(r"Skills主台账_\d{8}_\d{6}(?:_\d+)?\.xlsx\Z")

# Task 14 must bind discovery -> fixed upstream snapshot -> trusted ReviewPacket.
# Leaving this absent is safer than treating registry metadata as a reviewable Skill.
PRODUCTION_DRIVER_FACTORY: Callable[..., tuple[RunCoordinator, RunRequest]] | None = None


def _production_driver_ready() -> bool:
    return callable(PRODUCTION_DRIVER_FACTORY)


def _production_driver_status() -> str:
    if PRODUCTION_DRIVER_FACTORY is None:
        return "生产发现驱动未配置"
    if not callable(PRODUCTION_DRIVER_FACTORY):
        return "生产发现驱动配置不可调用"
    return "已配置"


class CliOperationalError(RuntimeError):
    """A safe operation could not be completed in the current environment."""


class CliInputError(ValueError):
    """A caller-supplied path or option violates the CLI contract."""


class ProtocolInputError(ValueError):
    """The long-lived stdin protocol received an invalid frame."""


class ProtocolEOF(CliOperationalError):
    """The controlling agent disconnected while a capability was live."""


@dataclass(frozen=True)
class OperationResult:
    exit_code: int
    message: str
    details: Mapping[str, object] | None = None


@dataclass(frozen=True)
class DoctorEnvironment:
    is_windows: bool
    python_available: bool
    gh_available: bool
    word_available: bool
    excel_available: bool
    loader_output: str | None = None


@dataclass(frozen=True)
class DoctorReport:
    exit_code: int
    production_ready: bool
    checks: Mapping[str, str]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class RepairResult:
    exit_code: int
    valid_backups: tuple[Path, ...]
    recovery_candidate: Path | None = None
    message: str = ""


@dataclass(frozen=True)
class RebuildResult:
    exit_code: int
    outputs: tuple[Path, ...]
    message: str = ""


def _project_root(value: str | Path) -> Path:
    root = Path(value).absolute()
    try:
        assert_ordinary_path(root, require_directory=True)
    except ValueError as exc:
        raise CliOperationalError(f"项目根必须是现有普通目录：{root}") from exc
    return root


def _workflow_root(project_root: str | Path) -> Path:
    return _project_root(project_root) / WORKFLOW_DIRECTORY


def _installed_workflow_root() -> Path:
    root = Path(__file__).resolve().parents[2]
    if root.name != WORKFLOW_DIRECTORY:
        raise CliOperationalError("无法从已安装包定位 07_自动维护工作流")
    return root


def _ordinary_directory(path: Path, *, create: bool = False) -> Path:
    absolute = path.absolute()
    if create and not absolute.exists():
        absolute.mkdir(parents=True, exist_ok=False)
    assert_ordinary_path(absolute, require_directory=True)
    return absolute


def _ordinary_file(path: Path, *, suffix: str | None = None) -> Path:
    absolute = path.absolute()
    assert_ordinary_path(absolute)
    if not absolute.is_file() or is_link_or_reparse(absolute):
        raise CliOperationalError(f"必须是普通文件：{absolute}")
    if suffix and absolute.suffix.casefold() != suffix.casefold():
        raise CliOperationalError(f"文件扩展名必须为 {suffix}：{absolute}")
    return absolute


def _create_contained_directories(base: Path, target: Path) -> Path:
    base = _ordinary_directory(base)
    target = target.absolute()
    try:
        relative = target.relative_to(base)
    except ValueError as exc:
        raise CliInputError(f"目标路径越出允许目录：{target}") from exc
    assert_ordinary_path(target)
    current = base
    for part in relative.parts:
        current = contained_child(current, part)
        if current.exists():
            _ordinary_directory(current)
        elif current.is_symlink():
            raise CliOperationalError(f"待创建目录不得是链接或重解析点：{current}")
        else:
            current.mkdir(mode=0o700)
            _ordinary_directory(current)
    return target


def _read_authority_files(project_root: Path) -> dict[str, str]:
    paths = {"AGENTS.md": project_root / "AGENTS.md"}
    paths.update({name: project_root / "01_规则" / name for name in REQUIRED_RULES})
    contents: dict[str, str] = {}
    for label, path in paths.items():
        try:
            text = _ordinary_file(path).read_text(encoding="utf-8")
        except (OSError, UnicodeError, CliOperationalError, ValueError) as exc:
            raise CliOperationalError(f"必读规则缺失或无法完整读取：{label}") from exc
        if not text.strip():
            raise CliOperationalError(f"必读规则为空：{label}")
        contents[label] = text
    return contents


def _copy_file_atomic(source: Path, destination: Path) -> None:
    _ordinary_file(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    assert_ordinary_path(destination.parent, require_directory=True)
    descriptor, name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(source.read_bytes())
            handle.flush()
            os.fsync(handle.fileno())
        if is_link_or_reparse(temporary):
            raise CliOperationalError("Skill 暂存文件不得是链接或重解析点")
        os.replace(temporary, destination)
    finally:
        if temporary.exists() and not is_link_or_reparse(temporary):
            temporary.unlink()


def _path_identity(path: Path) -> tuple[int, int, int, int]:
    result = path.lstat()
    if path.is_dir() and not is_link_or_reparse(path):
        return (getattr(result, "st_dev", 0), getattr(result, "st_ino", 0), 0, 0)
    return (
        getattr(result, "st_dev", 0),
        getattr(result, "st_ino", 0),
        result.st_size,
        result.st_mtime_ns,
    )


def _skill_tree_manifest(root: Path) -> tuple[tuple[object, ...], ...]:
    _ordinary_directory(root)
    entries: list[tuple[object, ...]] = []
    for item in sorted(root.rglob("*"), key=lambda value: value.relative_to(root).as_posix().casefold()):
        if is_link_or_reparse(item):
            raise CliOperationalError(f"Skill 包不得包含链接或重解析点：{item}")
        relative = item.relative_to(root).as_posix()
        if item.is_dir():
            _ordinary_directory(item)
            entries.append(("directory", relative))
        elif item.is_file():
            _ordinary_file(item)
            entries.append(("file", relative, sha256(item.read_bytes()).hexdigest()))
        else:
            raise CliOperationalError(f"Skill 包含不可复制的文件类型：{item}")
    return tuple(entries)


def _remove_owned_skill_tree(path: Path, parent: Path) -> None:
    try:
        path.relative_to(parent)
    except ValueError:
        return
    if path.exists() and path.is_dir() and not is_link_or_reparse(path):
        shutil.rmtree(path)


def _install_skill(source_workflow: Path, codex_skills_root: Path) -> Path:
    source = source_workflow / "skill" / SKILL_NAME
    source_manifest = _skill_tree_manifest(source)
    root = codex_skills_root.absolute()
    assert_ordinary_path(root)
    if root.exists():
        _ordinary_directory(root)
    else:
        root.mkdir(parents=True, exist_ok=False)
        _ordinary_directory(root)
    root_identity = _path_identity(root)
    destination = contained_child(root, SKILL_NAME)
    destination_identity = None
    if destination.exists():
        _skill_tree_manifest(destination)
        destination_identity = _path_identity(destination)
    elif destination.is_symlink():
        raise CliOperationalError("Skill 目标不得是链接或重解析点")

    operation = uuid.uuid4().hex
    staging = contained_child(root, f".{SKILL_NAME}.{operation}.pending")
    previous = contained_child(root, f".{SKILL_NAME}.{operation}.previous")
    if staging.exists() or staging.is_symlink() or previous.exists() or previous.is_symlink():
        raise CliOperationalError("Skill 目录级更新暂存路径发生冲突")
    staging.mkdir(mode=0o700)
    switched_previous = False
    try:
        for entry in source_manifest:
            kind, relative = str(entry[0]), str(entry[1])
            target = staging.joinpath(*Path(relative).parts)
            if kind == "directory":
                target.mkdir(parents=True, exist_ok=False)
                _ordinary_directory(target)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                _ordinary_directory(target.parent)
                _copy_file_atomic(source.joinpath(*Path(relative).parts), target)
        if _skill_tree_manifest(source) != source_manifest or _skill_tree_manifest(staging) != source_manifest:
            raise CliOperationalError("Skill 源包或完整暂存树在切换前发生变化")
        if _path_identity(root) != root_identity or is_link_or_reparse(root):
            raise CliOperationalError("Codex Skills 根目录在更新期间发生变化")
        if destination_identity is not None:
            if not destination.exists() or is_link_or_reparse(destination) or _path_identity(destination) != destination_identity:
                raise CliOperationalError("既有 Skill 目标在切换前发生变化")
            os.rename(destination, previous)
            switched_previous = True
        elif destination.exists() or destination.is_symlink():
            raise CliOperationalError("Skill 目标在切换前被占用")
        try:
            os.rename(staging, destination)
        except BaseException as switch_error:
            if switched_previous and previous.exists() and not destination.exists() and not destination.is_symlink():
                try:
                    os.rename(previous, destination)
                    switched_previous = False
                except BaseException as rollback_error:
                    if hasattr(switch_error, "add_note"):
                        switch_error.add_note(f"Skill 旧版回滚失败：{rollback_error}")
            raise
        if _skill_tree_manifest(destination) != source_manifest:
            raise CliOperationalError("安装后的 Skill 树与完整暂存快照不一致")
        if switched_previous:
            _remove_owned_skill_tree(previous, root)
            switched_previous = False
        return destination
    except BaseException as install_error:
        if switched_previous and previous.exists() and not is_link_or_reparse(previous):
            try:
                _remove_owned_skill_tree(destination, root)
                if not destination.exists() and not destination.is_symlink():
                    os.rename(previous, destination)
                    switched_previous = False
            except BaseException as rollback_error:
                if hasattr(install_error, "add_note"):
                    install_error.add_note(f"Skill 旧版回滚失败：{rollback_error}")
        raise
    finally:
        _remove_owned_skill_tree(staging, root)


def setup_project(
    project_root: str | Path,
    *,
    source_workflow: str | Path | None = None,
    codex_skills_root: str | Path | None = None,
) -> OperationResult:
    """Create only missing local state after every authority input passes."""

    try:
        project = _project_root(project_root)
        _read_authority_files(project)
        workflow = project / WORKFLOW_DIRECTORY
        source = Path(source_workflow).absolute() if source_workflow is not None else _installed_workflow_root()
        _ordinary_directory(source)
        example = _ordinary_file(source / "workflow-settings.example.toml", suffix=".toml")
        load_settings(example)
        for name in ("pdf_renderer.py", "workspace_renderer.py", "daily_xlsx_builder.mjs"):
            _ordinary_file(source / "src" / "skill_maintainer" / name)
        _ordinary_directory(source / "skill" / SKILL_NAME)
        if workflow.exists():
            _ordinary_directory(workflow)
        else:
            workflow.mkdir(parents=False, exist_ok=False)
            _ordinary_directory(workflow)

        settings = workflow / "workflow-settings.toml"
        if settings.exists() or settings.is_symlink():
            load_settings(_ordinary_file(settings, suffix=".toml"))
        else:
            with settings.open("xb") as handle:
                handle.write(example.read_bytes())
                handle.flush()
                os.fsync(handle.fileno())

        ledger_root = workflow / "ledger"
        for directory in (ledger_root, ledger_root / "archive", workflow / "output"):
            if directory.exists():
                _ordinary_directory(directory)
            else:
                directory.mkdir(parents=True, exist_ok=False)
                _ordinary_directory(directory)
        ledger_path = ledger_root / "Skills主台账.xlsx"
        if ledger_path.exists() or ledger_path.is_symlink():
            store = LedgerStore.load(_ordinary_file(ledger_path, suffix=".xlsx"))
            try:
                errors = store.validate()
            finally:
                store.workbook.close()
            if errors:
                raise CliOperationalError("既有主台账无效：" + "；".join(errors))
        else:
            store = LedgerStore.create(ledger_path)
            store.workbook.close()

        installed = None
        if codex_skills_root is not None:
            installed = _install_skill(source, Path(codex_skills_root))
        return OperationResult(
            SUCCESS,
            "项目工作流结构已检查；仅补齐缺失状态，设置保持禁用/手动。",
            {"workflow_root": str(workflow), "skill": str(installed) if installed else None},
        )
    except SettingsError as exc:
        return OperationResult(INVALID_INPUT, str(exc))
    except (OSError, ValueError, CliOperationalError) as exc:
        return OperationResult(OPERATIONAL_FAILURE, str(exc))


def _office_registered(prog_id: str) -> bool:
    if os.name != "nt":
        return False
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, rf"{prog_id}\CLSID") as key:
            value, _ = winreg.QueryValueEx(key, None)
        return bool(str(value).strip())
    except (OSError, ImportError):
        return False


def current_doctor_environment(*, loader_output: str | None = None) -> DoctorEnvironment:
    python_available = Path(sys.executable).is_file() and (3, 11) <= sys.version_info[:2] < (3, 14)
    return DoctorEnvironment(
        is_windows=os.name == "nt",
        python_available=python_available,
        gh_available=shutil.which("gh") is not None,
        word_available=_office_registered("Word.Application"),
        excel_available=_office_registered("Excel.Application"),
        loader_output=loader_output,
    )


def doctor_project(project_root: str | Path, *, environment: DoctorEnvironment | object | None = None) -> DoctorReport:
    """Inspect deployability without launching Office or guessing loader paths."""

    checks: dict[str, str] = {}
    errors: list[str] = []
    warnings: list[str] = []
    try:
        project = _project_root(project_root)
    except CliOperationalError as exc:
        return DoctorReport(OPERATIONAL_FAILURE, False, checks, (str(exc),), ())
    authority_paths = {"AGENTS.md": project / "AGENTS.md"}
    authority_paths.update({name: project / "01_规则" / name for name in REQUIRED_RULES})
    for label, path in authority_paths.items():
        try:
            text = _ordinary_file(path).read_text(encoding="utf-8")
            if not text.strip():
                raise ValueError("empty")
            checks[label] = "可读取"
        except (OSError, UnicodeError, ValueError, CliOperationalError):
            checks[label] = "缺失"
            errors.append(f"必读规则不可用：{label}")

    workflow = project / WORKFLOW_DIRECTORY
    try:
        _ordinary_directory(workflow)
        checks["workflow root"] = "可用"
    except (OSError, ValueError, CliOperationalError):
        checks["workflow root"] = "缺失"
        errors.append("07_自动维护工作流不存在或不是普通目录")

    settings = None
    configuration_invalid = False
    try:
        settings = load_settings(_ordinary_file(workflow / "workflow-settings.toml", suffix=".toml"))
        checks["settings"] = "有效"
    except SettingsError as exc:
        configuration_invalid = True
        checks["settings"] = "无效"
        errors.append(f"运行设置无效：{exc}")
    except (OSError, ValueError, CliOperationalError) as exc:
        checks["settings"] = "无效"
        errors.append(f"运行设置无效：{exc}")

    try:
        ledger = LedgerStore.load(_ordinary_file(workflow / "ledger" / "Skills主台账.xlsx", suffix=".xlsx"))
        try:
            ledger_errors = ledger.validate()
        finally:
            ledger.workbook.close()
        if ledger_errors:
            raise ValueError("；".join(ledger_errors))
        checks["ledger"] = "有效"
    except (OSError, ValueError, CliOperationalError) as exc:
        checks["ledger"] = "无效"
        errors.append(f"主台账无效：{exc}")

    env = environment or current_doctor_environment()
    dependency_values = {
        "Python": bool(getattr(env, "python_available", False)),
        "GitHub CLI": bool(getattr(env, "gh_available", False)),
        "Microsoft Word": bool(getattr(env, "word_available", False)),
        "Microsoft Excel": bool(getattr(env, "excel_available", False)),
    }
    for label, available in dependency_values.items():
        checks[label] = "可用" if available else "不可用"
        if not available:
            errors.append(f"运行依赖不可用：{label}")

    loader_output = getattr(env, "loader_output", None)
    if loader_output:
        try:
            build_workspace_renderer_command(str(loader_output), project)
            checks["renderer"] = "加载器绑定通过"
        except (WorkspaceRendererError, OSError, ValueError) as exc:
            checks["renderer"] = "加载器绑定失败"
            errors.append(f"Word 渲染前置条件无效：{exc}")
    else:
        checks["renderer"] = "等待 Codex 工作区依赖加载器"
        warnings.append("doctor 不从 PATH、用户名或缓存布局猜测 Word 渲染依赖")

    driver_ready = _production_driver_ready()
    checks["production_driver"] = _production_driver_status()
    production_requested = bool(settings and settings.workflow.enabled and settings.schedule.mode != "manual")
    windows = bool(getattr(env, "is_windows", False))
    if production_requested and not windows:
        errors.append("生产调度仅支持 Windows")
    if production_requested and not driver_ready:
        errors.append("生产发现驱动未配置，不能启用自动任务")
    if production_requested and not loader_output:
        errors.append("生产发布尚未取得 Codex 工作区依赖加载器输出")
    if not windows:
        warnings.append("当前不是 Windows；只允许离线诊断，不允许生产调度")
    if not driver_ready:
        warnings.append("Task 14 接通固定上游快照与受信 ReviewPacket 前不得启用自动任务")
    production_ready = not errors and windows and driver_ready and bool(loader_output)
    exit_code = INVALID_INPUT if configuration_invalid else (OPERATIONAL_FAILURE if errors else SUCCESS)
    return DoctorReport(exit_code, production_ready, checks, tuple(errors), tuple(warnings))


def _schedule_mapping(settings: object) -> dict[str, object]:
    schedule = settings.schedule
    result: dict[str, object] = {
        "mode": schedule.mode,
        "timezone": settings.workflow.timezone,
        "start_time": schedule.start_time.strftime("%H:%M"),
    }
    if schedule.mode == "weekly":
        result["weekdays"] = list(schedule.weekdays)
    elif schedule.mode == "monthly":
        result["day_of_month"] = schedule.day_of_month
    elif schedule.mode == "interval":
        result.update({"dispatcher": "daily", "interval_days": schedule.interval_days})
    return result


def _render_automation_prompt(project: Path, settings_path: Path, digest: str) -> str:
    template = _ordinary_file(
        project / WORKFLOW_DIRECTORY / "skill" / SKILL_NAME / "assets" / "automation-prompt.md"
    ).read_text(encoding="utf-8")
    for marker, value in {
        "{{ABSOLUTE_PROJECT_ROOT}}": str(project),
        "{{ABSOLUTE_TOML_PATH}}": str(settings_path),
        "{{APPLIED_TOML_SHA256}}": digest,
    }.items():
        template = template.replace(marker, value)
    if "{{" in template or "}}" in template:
        raise CliOperationalError("自动任务提示词模板仍含未绑定占位符")
    return template


def build_apply_settings_plan(
    project_root: str | Path,
    *,
    environment: DoctorEnvironment | object | None = None,
) -> dict[str, object]:
    """Validate settings and return an app-tool plan; never mutate automation."""

    project = _project_root(project_root)
    _read_authority_files(project)
    settings_path = _ordinary_file(project / WORKFLOW_DIRECTORY / "workflow-settings.toml", suffix=".toml")
    settings = load_settings(settings_path)
    digest = settings_sha256(settings_path)
    enabled_schedule = settings.workflow.enabled and settings.schedule.mode != "manual"
    diagnostic = doctor_project(project, environment=environment)
    return {
        "project_root": str(project),
        "toml_path": str(settings_path),
        "config_sha256": digest,
        "preview": schedule_preview(settings),
        "schedule": _schedule_mapping(settings),
        "automation_action": "upsert" if enabled_schedule else "ensure_absent",
        "prompt": _render_automation_prompt(project, settings_path, digest),
        "production_ready": diagnostic.production_ready,
        "doctor": diagnostic,
        "readback_required": True,
        "note": "必须由 Codex 应用自动任务更新工具执行并回读；CLI 未修改自动任务。",
    }


def _valid_ledger(path: Path) -> bool:
    try:
        store = LedgerStore.load(_ordinary_file(path, suffix=".xlsx"))
        try:
            return not store.validate()
        finally:
            store.workbook.close()
    except (OSError, ValueError, BadZipFile, CliOperationalError):
        return False


def _stream_sha256(path: Path) -> str:
    digest = sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _verified_success_records(workflow: Path, records: Iterable[Mapping[str, object]]) -> tuple[tuple[Mapping[str, object], Path, str], ...]:
    verifier = RunCoordinator(root=workflow)
    verified: list[tuple[Mapping[str, object], Path, str]] = []
    for record in records:
        if record.get("状态") != "成功":
            continue
        snapshot_sha = str(record.get("快照SHA-256") or "").strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", snapshot_sha):
            continue
        try:
            verifier._verify_recorded_generation(record)
            relative = verifier._summary_fields(record.get("摘要")).get("generation", "")
            generation = workflow.joinpath(*Path(relative).parts)
        except (CoordinatorError, OSError, UnicodeError, ValueError):
            continue
        verified.append((record, generation, snapshot_sha))
    return tuple(verified)


def _handle_identity(handle: object) -> tuple[int, int, int, int]:
    result = os.fstat(handle.fileno())
    return (
        getattr(result, "st_dev", 0),
        getattr(result, "st_ino", 0),
        result.st_size,
        result.st_mtime_ns,
    )


def _read_bound_backup_snapshot(
    path: Path,
    expected_sha256: str,
    expected_identity: tuple[int, int, int, int],
) -> bytes:
    path = _ordinary_file(path, suffix=".xlsx")
    path_before = _path_identity(path)
    if path_before != expected_identity:
        raise CliOperationalError("备份路径在验证与单句柄读取之间被替换")
    with path.open("rb") as handle:
        handle_before = _handle_identity(handle)
        if handle_before != path_before:
            raise CliOperationalError("备份路径与已打开文件身份不一致")
        content = handle.read()
        handle_after = _handle_identity(handle)
    if handle_after != handle_before:
        raise CliOperationalError("备份在单句柄读取期间被原地改写")
    if not path.is_file() or is_link_or_reparse(path) or _path_identity(path) != path_before:
        raise CliOperationalError("备份路径在单句柄读取后被替换")
    if sha256(content).hexdigest() != expected_sha256:
        raise CliOperationalError("备份字节快照与成功运行记录 SHA-256 不一致")
    return content


def repair_ledger(project_root: str | Path, *, backup: str | Path | None = None) -> RepairResult:
    """List verified backups or copy an explicit one to a non-authority recovery candidate."""

    try:
        project = _project_root(project_root)
        _read_authority_files(project)
        workflow = _workflow_root(project)
        archive = workflow / "ledger" / "archive"
        if not archive.exists():
            return RepairResult(SAFE_NOOP, (), None, "没有可恢复的验证备份")
        _ordinary_directory(archive)
        authority = LedgerStore.load(_ordinary_file(workflow / "ledger" / "Skills主台账.xlsx", suffix=".xlsx"))
        try:
            errors = authority.validate()
            records = authority.rows("运行记录")
        finally:
            authority.workbook.close()
        if errors:
            raise CliOperationalError("当前主台账无效：" + "；".join(errors))
        verified_records = _verified_success_records(workflow, records)
        authorized_hashes = {item[2] for item in verified_records}
        valid_evidence: dict[Path, tuple[str, tuple[int, int, int, int]]] = {}
        unstable: set[Path] = set()
        for discovered in sorted(archive.iterdir()):
            path = discovered.absolute()
            if (
                not path.is_file()
                or is_link_or_reparse(path)
                or not BACKUP_PATTERN.fullmatch(path.name)
            ):
                continue
            identity_before = _path_identity(path)
            ledger_valid = _valid_ledger(path)
            digest = _stream_sha256(path)
            identity_after = _path_identity(path)
            if identity_after != identity_before:
                unstable.add(path)
                continue
            if ledger_valid and digest in authorized_hashes:
                valid_evidence[path] = (digest, identity_after)
        valid = tuple(valid_evidence)
        if backup is None:
            return RepairResult(SAFE_NOOP, valid, None, "请选择一个已验证备份；当前主台账不会自动覆盖")
        selected = Path(backup).absolute()
        if selected in unstable:
            raise CliOperationalError("所选备份在验证与哈希绑定之间被替换")
        if selected not in valid:
            raise CliInputError("所选文件不是当前可用的已验证备份")
        selected_sha, selected_identity = valid_evidence[selected]
        if _path_identity(selected) != selected_identity:
            raise CliOperationalError("所选备份在哈希绑定后被替换")
        if selected_sha not in authorized_hashes:
            raise CliOperationalError("所选备份未绑定已复验的成功运行记录")
        snapshot = _read_bound_backup_snapshot(selected, selected_sha, selected_identity)
        recovery_root = workflow / "ledger" / "recovery"
        if recovery_root.exists():
            _ordinary_directory(recovery_root)
        else:
            _create_contained_directories(_ordinary_directory(workflow / "ledger"), recovery_root)
        suffix = sha256(snapshot).hexdigest()[:12]
        candidate = recovery_root / f"Skills主台账_恢复候选_{datetime.now():%Y%m%d_%H%M%S}_{suffix}.xlsx"
        if candidate.exists() or candidate.is_symlink():
            raise CliOperationalError("恢复候选已存在，拒绝覆盖")
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{candidate.stem}.", suffix=".xlsx", dir=recovery_root
        )
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(snapshot)
                handle.flush()
                os.fsync(handle.fileno())
            if _stream_sha256(temporary) != selected_sha or not _valid_ledger(temporary):
                raise CliOperationalError("恢复候选暂存复读失败")
            if candidate.exists() or candidate.is_symlink():
                raise CliOperationalError("恢复候选在切换前被占用")
            os.rename(temporary, candidate)
        finally:
            if temporary.exists() and temporary.is_file() and not is_link_or_reparse(temporary):
                temporary.unlink()
        if _stream_sha256(candidate) != selected_sha or not _valid_ledger(candidate):
            raise CliOperationalError("恢复候选切换后复读失败")
        return RepairResult(SUCCESS, valid, candidate, "已生成恢复候选；当前主台账保持不变")
    except CliInputError as exc:
        return RepairResult(INVALID_INPUT, (), None, str(exc))
    except (OSError, ValueError, CliOperationalError) as exc:
        return RepairResult(OPERATIONAL_FAILURE, (), None, str(exc))


def _ledger_rebuild_summary(ledger: LedgerStore) -> dict[str, object]:
    observations = ledger.rows("候选观察")
    mappings = ledger.rows("专业任务映射")
    scopes = sorted({
        " ".join(filter(None, (str(row.get("专业代码") or "").strip(), str(row.get("专业名称") or "").strip())))
        for row in mappings
        if str(row.get("专业代码") or row.get("专业名称") or "").strip()
    })
    return {
        "run_id": f"rebuild-{datetime.now():%Y%m%d-%H%M%S}",
        "generated_at": datetime.now(timezone.utc),
        "blocked": False,
        "source_statuses": {},
        "formal_additions": ledger.rows("当前Skill"),
        "conditional_candidates": [row for row in observations if row.get("观察状态") == "条件候选"],
        "adaptation_candidates": [row for row in observations if row.get("观察状态") == "需适配候选"],
        "aliases": ledger.rows("来源别名"),
        "affected_scopes": scopes,
        "manual_reviews": [{"事项": "本次为主台账离线重建，不执行来源检查。"}],
    }


def rebuild_reports(
    project_root: str | Path,
    *,
    output: str | Path | None = None,
    word_builder: Callable[[object, str | Path], Path] = build_daily_docx,
    excel_builder: Callable[[object, str | Path], Path] = build_daily_xlsx,
) -> RebuildResult:
    """Rebuild one Word/Excel pair strictly from the committed ledger."""

    try:
        project = _project_root(project_root)
        _read_authority_files(project)
        workflow = _workflow_root(project)
        ledger_path = _ordinary_file(workflow / "ledger" / "Skills主台账.xlsx", suffix=".xlsx")
        ledger_sha = sha256(ledger_path.read_bytes()).hexdigest()
        ledger = LedgerStore.load(ledger_path)
        try:
            errors = ledger.validate()
            if errors:
                raise CliOperationalError("主台账无效：" + "；".join(errors))
            summary = _ledger_rebuild_summary(ledger)
        finally:
            ledger.workbook.close()
        output_base = _ordinary_directory(workflow / "output")
        output_root = Path(output).absolute() if output is not None else output_base / "rebuild" / datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            output_root.relative_to(output_base)
        except ValueError as exc:
            raise CliInputError("重建输出必须位于 07_自动维护工作流/output 内") from exc
        assert_ordinary_path(output_root)
        if output_root.exists() or output_root.is_symlink():
            raise CliOperationalError("重建输出目标已存在，拒绝覆盖")
        output_parent = _create_contained_directories(output_base, output_root.parent)
        staging = contained_child(output_parent, f".{output_root.name}.{uuid.uuid4().hex}.pending")
        if staging.exists() or staging.is_symlink():
            raise CliOperationalError("重建暂存目录发生冲突")
        staging.mkdir(mode=0o700)
        try:
            staged_word = contained_child(staging, "Skill库离线重建报告.docx")
            staged_excel = contained_child(staging, "Skill库离线重建表.xlsx")
            built_word = Path(word_builder(summary, staged_word)).absolute()
            built_excel = Path(excel_builder(summary, staged_excel)).absolute()
            if built_word != staged_word or built_excel != staged_excel:
                raise CliOperationalError("重建器返回了暂存目录外的文件")
            _ordinary_file(staged_word, suffix=".docx")
            _ordinary_file(staged_excel, suffix=".xlsx")
            if sha256(ledger_path.read_bytes()).hexdigest() != ledger_sha:
                raise CliOperationalError("离线重建期间主台账发生变化")
            if output_root.exists() or output_root.is_symlink():
                raise CliOperationalError("重建输出目标在切换前被占用")
            os.rename(staging, output_root)
        except BaseException:
            if staging.exists() and staging.is_dir() and not is_link_or_reparse(staging):
                shutil.rmtree(staging)
            raise
        outputs = (
            contained_child(output_root, "Skill库离线重建报告.docx"),
            contained_child(output_root, "Skill库离线重建表.xlsx"),
        )
        return RebuildResult(SUCCESS, outputs, "已从当前主台账离线重建 Word/Excel；未联网")
    except CliInputError as exc:
        return RebuildResult(INVALID_INPUT, (), str(exc))
    except (OSError, ValueError, CliOperationalError) as exc:
        return RebuildResult(OPERATIONAL_FAILURE, (), str(exc))


def _json_value(value: object) -> object:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return {key: _json_value(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def _emit_frame(output_stream: TextIO, payload: Mapping[str, object]) -> None:
    output_stream.write(json.dumps(_json_value(payload), ensure_ascii=False, separators=(",", ":")) + "\n")
    output_stream.flush()


def _read_frame(input_stream: TextIO, *, expected_type: str, run_id: str) -> Mapping[str, object]:
    line = input_stream.readline()
    if line == "":
        raise ProtocolEOF(f"等待 {expected_type} 时控制端断开")
    try:
        payload = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ProtocolInputError("协议输入必须是单行 UTF-8 JSON") from exc
    if not isinstance(payload, Mapping):
        raise ProtocolInputError("协议输入必须是 JSON 对象")
    if payload.get("type") != expected_type or payload.get("run_id") != run_id:
        raise ProtocolInputError("协议帧类型或 run_id 与当前运行不一致")
    return payload


def _abandon_after_failure(coordinator: RunCoordinator, prepared: object | None, original: BaseException) -> None:
    if prepared is None:
        return
    try:
        coordinator.abandon(prepared)
    except BaseException as cleanup_error:
        if hasattr(original, "add_note"):
            original.add_note(f"运行终态清理诊断：{type(cleanup_error).__name__}: {cleanup_error}")


@dataclass
class InteractiveOfficeGate:
    """Office verifier that pauses one live process for exact per-page decisions."""

    input_stream: TextIO
    output_stream: TextIO
    renderer: object

    def __call__(self, prepared: object, artifacts: Iterable[Path]) -> OfficeEvidenceBundle:
        checks = []
        rendered_words = []
        for raw_path in artifacts:
            path = Path(raw_path).absolute()
            if path.suffix.casefold() == ".xlsx":
                role = "ledger" if path == Path(prepared.staging_ledger).absolute() else "daily"
                check = verify_excel(path, scope=prepared.office_scope, role=role)
                if not check.passed:
                    raise OfficeVerificationError(check.error or f"Excel Office 验证失败：{path}")
                checks.append(check)
            elif path.suffix.casefold() == ".docx":
                evidence_root = Path(prepared.staging_dir) / ".office-evidence"
                evidence_root.mkdir(exist_ok=True)
                assert_ordinary_path(evidence_root, require_directory=True)
                render = evidence_root / sha256(str(path).encode("utf-8")).hexdigest()[:20]
                check = verify_word(path, render, renderer=self.renderer, scope=prepared.office_scope)
                if not check.office_passed or check.blank_pages or not check.page_paths:
                    raise OfficeVerificationError(check.error or f"Word Office/PDF 渲染失败：{path}")
                rendered_words.append(check)
            else:
                raise OfficeVerificationError(f"发布证据包含非 Word/Excel 文件：{path}")

        if rendered_words:
            documents = [
                {
                    "source_path": str(check.source_path),
                    "source_sha256": check.source_sha256,
                    "pdf_path": str(check.pdf_path),
                    "pdf_sha256": check.pdf_sha256,
                    "pages": [
                        {"page_number": index, "path": str(path), "sha256": digest}
                        for index, (path, digest) in enumerate(zip(check.page_paths, check.page_sha256), start=1)
                    ],
                }
                for check in rendered_words
            ]
            _emit_frame(self.output_stream, {"type": "word_visual_review_required", "run_id": prepared.run_id, "documents": documents})
            frame = _read_frame(self.input_stream, expected_type="word_visual_decisions", run_id=prepared.run_id)
            decisions = frame.get("documents")
            if not isinstance(decisions, list) or len(decisions) != len(rendered_words):
                raise ProtocolInputError("Word 逐页决定必须精确覆盖全部文档")
            by_source = {}
            for value in decisions:
                if not isinstance(value, Mapping):
                    raise ProtocolInputError("Word 文档决定必须是对象")
                source_sha = str(value.get("source_sha256") or "")
                if not source_sha or source_sha in by_source:
                    raise ProtocolInputError("Word 文档决定的 source_sha256 缺失或重复")
                by_source[source_sha] = value
            for check in rendered_words:
                value = by_source.get(check.source_sha256)
                if value is None or str(value.get("pdf_sha256") or "") != check.pdf_sha256:
                    raise ProtocolInputError("Word 逐页决定没有绑定当前 Word/PDF 哈希")
                page_values = value.get("pages")
                if not isinstance(page_values, list):
                    raise ProtocolInputError("Word 逐页决定缺少 pages 数组")
                pages = []
                for page in page_values:
                    if not isinstance(page, Mapping) or type(page.get("approved")) is not bool:
                        raise ProtocolInputError("每页决定必须包含布尔 approved")
                    pages.append(WordPageDecision(int(page.get("page_number") or 0), str(page.get("sha256") or ""), bool(page["approved"])))
                decision = WordRenderDecision(
                    source_sha256=check.source_sha256,
                    pdf_sha256=check.pdf_sha256 or "",
                    pages=tuple(pages),
                    reviewer=str(value.get("reviewer") or ""),
                )
                approved = bind_word_visual_decision(check, decision, scope=prepared.office_scope)
                if not approved.passed:
                    raise OfficeVerificationError("Word 逐页视觉复核拒绝发布")
                checks.append(approved)
        return OfficeEvidenceBundle.from_checks(tuple(checks), scope=prepared.office_scope)


def run_interactive_protocol(
    coordinator: RunCoordinator,
    request: RunRequest,
    *,
    input_stream: TextIO = sys.stdin,
    output_stream: TextIO = sys.stdout,
) -> int:
    """Keep all Task 7/9/11 capabilities alive across both review gates."""

    prepared = None
    try:
        prepared = coordinator.prepare(request)
        packets = []
        for candidate_id, packet in sorted(request.review_packets.items()):
            value = _json_value(packet)
            if isinstance(value, Mapping):
                value = {**value, "candidate_id": candidate_id}
            packets.append(value)
        _emit_frame(output_stream, {
            "type": "review_required",
            "run_id": prepared.run_id,
            "settings_sha256": prepared.settings_sha256,
            "source_statuses": {item.platform: item.status for item in prepared.source_runs},
            "review_packets": packets,
        })
        review_frame = _read_frame(input_stream, expected_type="review_decisions", run_id=prepared.run_id)
        raw_decisions = review_frame.get("decisions")
        if not isinstance(raw_decisions, list) or any(not isinstance(value, Mapping) for value in raw_decisions):
            raise ProtocolInputError("review_decisions 必须包含对象数组 decisions")
        try:
            decisions = tuple(ReviewDecision.from_mapping(value) for value in raw_decisions)
        except (TypeError, ValueError) as exc:
            raise ProtocolInputError(f"审查决定无效：{exc}") from exc
        required_ids = set(request.review_packets)
        supplied_ids = [decision.candidate_id for decision in decisions]
        if len(supplied_ids) != len(set(supplied_ids)) or set(supplied_ids) != required_ids:
            raise ProtocolInputError("审查决定必须按 candidate_id 精确覆盖全部 ReviewPacket，且不得重复或新增")
        reviews = coordinator.apply_reviews(prepared, decisions)
        summary = coordinator.finalize(prepared, reviews)
        if summary.blocked:
            raise CliOperationalError("全部来源失败，本轮未发布业务变化")
        _emit_frame(output_stream, {
            "type": "run_complete",
            "run_id": summary.run_id,
            "source_statuses": summary.source_statuses,
            "published_ledger": summary.published_ledger,
            "output_generation": summary.output_generation,
            "warnings": summary.warnings,
        })
        return SUCCESS
    except LockUnavailable as exc:
        _emit_frame(output_stream, {"type": "run_noop", "error": str(exc)})
        return SAFE_NOOP
    except ProtocolInputError as exc:
        _abandon_after_failure(coordinator, prepared, exc)
        _emit_frame(output_stream, {"type": "run_failed", "run_id": getattr(prepared, "run_id", None), "error": str(exc)})
        return INVALID_INPUT
    except (ProtocolEOF, CliOperationalError, CoordinatorError, OfficeVerificationError, OSError, ValueError) as exc:
        _abandon_after_failure(coordinator, prepared, exc)
        _emit_frame(output_stream, {"type": "run_failed", "run_id": getattr(prepared, "run_id", None), "error": str(exc)})
        return OPERATIONAL_FAILURE
    except BaseException as exc:
        _abandon_after_failure(coordinator, prepared, exc)
        raise


def _latest_success(rows: Iterable[Mapping[str, object]]) -> datetime | None:
    values = []
    for row in rows:
        value = row.get("成功完成时间")
        if isinstance(value, datetime):
            values.append(value.replace(tzinfo=value.tzinfo or timezone.utc))
        elif isinstance(value, str) and value.strip():
            try:
                parsed = datetime.fromisoformat(value)
                values.append(parsed.replace(tzinfo=parsed.tzinfo or timezone.utc))
            except ValueError:
                continue
    return max(values, default=None)


def status_project(
    project_root: str | Path,
    *,
    environment: DoctorEnvironment | object | None = None,
) -> dict[str, object]:
    project = _project_root(project_root)
    workflow = _workflow_root(project)
    settings = load_settings(_ordinary_file(workflow / "workflow-settings.toml", suffix=".toml"))
    ledger = LedgerStore.load(_ordinary_file(workflow / "ledger" / "Skills主台账.xlsx", suffix=".xlsx"))
    try:
        errors = ledger.validate()
        if errors:
            raise CliOperationalError("主台账无效：" + "；".join(errors))
        records = ledger.rows("运行记录")
    finally:
        ledger.workbook.close()
    next_run = next_run_at(settings, datetime.now(timezone.utc), _latest_success(records))
    diagnostic = doctor_project(project, environment=environment)
    successful = next((row for row in reversed(records) if row.get("状态") == "成功"), None)
    latest_output = None
    output_error = None
    if successful is None:
        output_error = "没有可验证的成功运行记录；未采用任意 generation 目录"
    else:
        verified = _verified_success_records(workflow, (successful,))
        if verified:
            latest_output = verified[0][1]
        else:
            output_error = "最后成功运行记录的发布代次、manifest 或 delivery 复验失败"
    return {
        "preview": schedule_preview(settings),
        "next_run_at": next_run,
        "latest_run": records[-1] if records else None,
        "latest_output": latest_output,
        "output_error": output_error,
        "production_ready": diagnostic.production_ready,
        "production_driver": _production_driver_status(),
        "doctor": diagnostic,
    }


def _add_project_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-root", required=True, type=Path, help="高校 AI 工作台项目的绝对根目录")


def build_parser() -> argparse.ArgumentParser:
    """Build the exact public and internal command surface."""

    parser = argparse.ArgumentParser(prog="skill-maintainer")
    subparsers = parser.add_subparsers(dest="command")
    for command in COMMANDS:
        subparser = subparsers.add_parser(command)
        _add_project_root(subparser)
        subparser.set_defaults(handler=_handle_stage_refusal if command in {"prepare", "apply-reviews", "finalize"} else None)
        if command == "setup":
            subparser.add_argument("--codex-skills-root", type=Path)
            subparser.set_defaults(handler=_handle_setup)
        elif command == "import-existing":
            subparser.add_argument("--inventory-only", action="store_true")
            subparser.add_argument("--output", type=Path)
            subparser.set_defaults(handler=_handle_import)
        elif command == "doctor":
            subparser.add_argument("--loader-output")
            subparser.add_argument("--network", action="store_true")
            subparser.set_defaults(handler=_handle_doctor)
        elif command == "edit-settings":
            subparser.set_defaults(handler=_handle_edit_settings)
        elif command == "apply-settings":
            subparser.add_argument("--loader-output")
            subparser.set_defaults(handler=_handle_apply_settings)
        elif command in {"run-now", "scheduled-run"}:
            subparser.add_argument("--loader-output")
            subparser.add_argument("--expected-config-sha")
            subparser.set_defaults(handler=_handle_run)
        elif command == "status":
            subparser.add_argument("--loader-output")
            subparser.set_defaults(handler=_handle_status)
        elif command == "repair-ledger":
            subparser.add_argument("--backup", type=Path)
            subparser.set_defaults(handler=_handle_repair)
        elif command == "rebuild-report":
            subparser.add_argument("--output", type=Path)
            subparser.set_defaults(handler=_handle_rebuild)
    return parser


def _print_json(value: object) -> None:
    print(json.dumps(_json_value(value), ensure_ascii=False, separators=(",", ":")))


def _handle_setup(args: argparse.Namespace) -> int:
    result = setup_project(args.project_root, source_workflow=_workflow_root(args.project_root), codex_skills_root=args.codex_skills_root)
    _print_json(result)
    return result.exit_code


def _handle_import(args: argparse.Namespace) -> int:
    project = _project_root(args.project_root)
    _read_authority_files(project)
    inventory = scan_existing_deliveries(project / "05_交付物")
    payload: dict[str, object] = {
        "excel_files": len(inventory.excel_files), "word_files": len(inventory.word_files),
        "excel_records": inventory.excel_skill_count, "word_records": inventory.word_skill_count,
        "duplicate_groups": inventory.duplicate_group_count, "ambiguous_records": inventory.ambiguous_record_count,
        "word_uncertainties": inventory.word_uncertainty_count,
        "word_excel_mismatch": inventory.word_excel_count_mismatch,
    }
    if args.output is not None:
        output = Path(args.output).absolute()
        ledger_root = _ordinary_directory(_workflow_root(project) / "ledger")
        staging_root = ledger_root / "staging"
        try:
            output.relative_to(staging_root.absolute())
        except ValueError as exc:
            raise CliInputError("首次导入输出必须位于 07_自动维护工作流/ledger/staging 内") from exc
        assert_ordinary_path(output)
        if output.exists() or output.is_symlink():
            raise CliOperationalError("首次导入输出已存在，拒绝覆盖")
        _create_contained_directories(ledger_root, output.parent)
        payload["import"] = build_initial_ledger(inventory, output)
    elif not args.inventory_only:
        payload["note"] = "首次必须先使用 --inventory-only；未写入任何台账"
        _print_json(payload)
        return SAFE_NOOP
    _print_json(payload)
    return SUCCESS


def _handle_doctor(args: argparse.Namespace) -> int:
    if args.network:
        raise CliOperationalError("Task 14 验收前 doctor --network 尚未接通；未发出任何网络请求")
    report = doctor_project(args.project_root, environment=current_doctor_environment(loader_output=args.loader_output))
    _print_json(report)
    return report.exit_code


def _handle_edit_settings(args: argparse.Namespace) -> int:
    workflow = _workflow_root(args.project_root)
    script = _ordinary_file(workflow / "edit-settings.ps1", suffix=".ps1")
    settings = _ordinary_file(workflow / "workflow-settings.toml", suffix=".toml")
    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if not powershell:
        raise CliOperationalError("未找到 PowerShell，无法打开中文设置表单")
    result = subprocess.run([powershell, "-NoProfile", "-File", str(script), "-SettingsPath", str(settings)], check=False)
    return SUCCESS if result.returncode == 0 else OPERATIONAL_FAILURE


def _handle_apply_settings(args: argparse.Namespace) -> int:
    plan = build_apply_settings_plan(
        args.project_root,
        environment=current_doctor_environment(loader_output=args.loader_output),
    )
    _print_json(plan)
    if plan["automation_action"] == "upsert" and not plan["production_ready"]:
        return OPERATIONAL_FAILURE
    return SUCCESS


def _handle_run(args: argparse.Namespace) -> int:
    if not _production_driver_ready():
        _print_json({"type": "run_failed", "error": "生产发现驱动未配置；prepare 前停止，未联网、未创建暂存运行"})
        return OPERATIONAL_FAILURE
    assert PRODUCTION_DRIVER_FACTORY is not None
    coordinator, request = PRODUCTION_DRIVER_FACTORY(
        project_root=Path(args.project_root).absolute(), command=args.command,
        loader_output=args.loader_output, expected_config_sha=args.expected_config_sha,
        input_stream=sys.stdin, output_stream=sys.stdout,
    )
    return run_interactive_protocol(coordinator, request)


def _handle_status(args: argparse.Namespace) -> int:
    _print_json(status_project(
        args.project_root,
        environment=current_doctor_environment(loader_output=args.loader_output),
    ))
    return SUCCESS


def _handle_repair(args: argparse.Namespace) -> int:
    result = repair_ledger(args.project_root, backup=args.backup)
    _print_json(result)
    return result.exit_code


def _handle_rebuild(args: argparse.Namespace) -> int:
    result = rebuild_reports(args.project_root, output=args.output)
    _print_json(result)
    return result.exit_code


def _handle_stage_refusal(args: argparse.Namespace) -> int:
    _print_json({
        "type": "run_failed",
        "error": f"{args.command} 只能作为 run-now/scheduled-run 同一长驻进程内的受信阶段；拒绝跨进程重建 capability",
    })
    return OPERATIONAL_FAILURE


def main(argv: list[str] | None = None) -> int:
    """Run one command and keep the 0/1/2/3 exit contract stable."""

    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return INVALID_INPUT
    try:
        return int(handler(args))
    except (SettingsError, CliInputError, ProtocolInputError, argparse.ArgumentTypeError) as exc:
        _print_json({"error": str(exc), "exit_code": INVALID_INPUT})
        return INVALID_INPUT
    except (CliOperationalError, CoordinatorError, OfficeVerificationError, OSError, ValueError) as exc:
        _print_json({"error": str(exc), "exit_code": OPERATIONAL_FAILURE})
        return OPERATIONAL_FAILURE


if __name__ == "__main__":
    raise SystemExit(main())
