"""Build a PDF renderer command only from Codex loader-bound paths."""

from __future__ import annotations

import os
from pathlib import Path
import re

from .office import RendererCommand
from .paths import assert_ordinary_path, is_link_or_reparse


class WorkspaceRendererError(ValueError):
    """Workspace dependency data cannot produce a trusted renderer command."""


_FIELDS = {
    "Python executable": "python",
    "Python packages": "packages",
    "Override binaries": "override",
    "Fallback binaries": "fallback",
}
_LOADER_LINE = re.compile(r"^- (?P<label>[^:]+): `(?P<value>[^`]+)`$")
_WRAPPER_TARGET = re.compile(
    r'^\s*(?:call\s+)?"(?:%SCRIPT_DIR%|%~dp0)(?P<relative>[^"%]+pdftoppm\.(?:cmd|exe))"',
    re.IGNORECASE | re.MULTILINE,
)
_SCRIPT_DIR = re.compile(
    r'^\s*set\s+"SCRIPT_DIR=%~dp0"\s*$', re.IGNORECASE | re.MULTILINE
)


def build_workspace_renderer_command(
    loader_output: str,
    project_root: str | Path,
) -> RendererCommand:
    """Construct Task 11's command from the actual loader text and project root."""
    paths = _parse_loader_output(loader_output)
    python = _ordinary_file(paths["python"], "Python executable")
    if python.name.lower() not in {"python.exe", "python"}:
        raise WorkspaceRendererError("工作区 Python 可执行文件名称无效。")
    packages = _ordinary_directory(paths["packages"], "Python packages")
    override = _ordinary_directory(paths["override"], "Override binaries")
    fallback = _ordinary_directory(paths["fallback"], "Fallback binaries")
    runtime_root = _common_runtime_root((python, packages, override, fallback))

    project_path = Path(project_root)
    if not project_path.is_absolute():
        raise WorkspaceRendererError("project root 必须为绝对路径。")
    project = _ordinary_directory(project_path, "project root")
    entrypoint = _ordinary_file(
        project
        / "07_自动维护工作流"
        / "src"
        / "skill_maintainer"
        / "pdf_renderer.py",
        "project PDF renderer",
    )
    try:
        entrypoint.relative_to(project)
    except ValueError as exc:
        raise WorkspaceRendererError("项目 PDF 渲染入口越出项目根。") from exc

    pdftoppm = _resolve_pdftoppm(override, fallback, runtime_root)
    return RendererCommand(
        (
            str(python),
            str(entrypoint),
            "--python-packages",
            str(packages),
            "--pdftoppm",
            str(pdftoppm),
        )
    )


def _parse_loader_output(loader_output: str) -> dict[str, Path]:
    if type(loader_output) is not str or not loader_output.strip():
        raise WorkspaceRendererError("工作区依赖加载器没有返回文本。")
    found: dict[str, Path] = {}
    for line in loader_output.splitlines():
        match = _LOADER_LINE.fullmatch(line.strip())
        if match is None or match.group("label") not in _FIELDS:
            continue
        key = _FIELDS[match.group("label")]
        if key in found:
            raise WorkspaceRendererError(f"工作区依赖字段重复：{match.group('label')}")
        value = Path(match.group("value"))
        if not value.is_absolute():
            raise WorkspaceRendererError(f"工作区依赖路径不是绝对路径：{match.group('label')}")
        found[key] = value
    missing = tuple(key for key in _FIELDS.values() if key not in found)
    if missing:
        raise WorkspaceRendererError(f"工作区依赖字段缺失：{','.join(missing)}")
    return found


def _ordinary_file(path: Path, label: str) -> Path:
    absolute = path.absolute()
    try:
        assert_ordinary_path(absolute)
    except ValueError as exc:
        raise WorkspaceRendererError(f"{label} 包含链接或重解析点。") from exc
    if not absolute.is_file() or is_link_or_reparse(absolute):
        raise WorkspaceRendererError(f"{label} 不是普通文件。")
    return absolute.resolve(strict=True)


def _ordinary_directory(path: Path, label: str) -> Path:
    absolute = path.absolute()
    try:
        assert_ordinary_path(absolute, require_directory=True)
    except ValueError as exc:
        raise WorkspaceRendererError(f"{label} 不是普通目录。") from exc
    return absolute.resolve(strict=True)


def _common_runtime_root(paths: tuple[Path, ...]) -> Path:
    try:
        root = Path(os.path.commonpath(tuple(map(str, paths))))
    except ValueError as exc:
        raise WorkspaceRendererError("工作区依赖不属于同一运行时根。") from exc
    root = _ordinary_directory(root, "workspace runtime root")
    if root == Path(root.anchor):
        raise WorkspaceRendererError("工作区依赖的共同根过宽。")
    for path in paths:
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise WorkspaceRendererError("工作区依赖越出共同运行时根。") from exc
    return root


def _resolve_pdftoppm(override: Path, fallback: Path, runtime_root: Path) -> Path:
    candidates = (
        override / "pdftoppm.exe",
        override / "pdftoppm.cmd",
        fallback / "pdftoppm.exe",
        fallback / "pdftoppm.cmd",
    )
    start = next((path for path in candidates if path.exists() or path.is_symlink()), None)
    if start is None:
        raise WorkspaceRendererError("加载器返回的二进制目录中缺少 pdftoppm。")
    current = _ordinary_file(start, "pdftoppm loader entry")
    seen: set[Path] = set()
    for _ in range(4):
        if current in seen:
            raise WorkspaceRendererError("pdftoppm 包装器形成循环。")
        seen.add(current)
        _require_runtime_containment(current, runtime_root)
        if current.suffix.lower() == ".exe":
            if current.name.lower() != "pdftoppm.exe":
                raise WorkspaceRendererError("Poppler 可执行文件名称无效。")
            pdfinfo = _ordinary_file(current.with_name("pdfinfo.exe"), "pdfinfo executable")
            _require_runtime_containment(pdfinfo, runtime_root)
            return current
        if current.suffix.lower() != ".cmd":
            raise WorkspaceRendererError("pdftoppm 入口不是受支持的文件类型。")
        current = _read_wrapper_target(current, runtime_root)
    raise WorkspaceRendererError("pdftoppm 包装器层级过深。")


def _read_wrapper_target(wrapper: Path, runtime_root: Path) -> Path:
    try:
        if wrapper.stat().st_size > 4096:
            raise WorkspaceRendererError("pdftoppm 包装器过大。")
        text = wrapper.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise WorkspaceRendererError("无法读取 pdftoppm 包装器。") from exc
    matches = tuple(_WRAPPER_TARGET.finditer(text))
    if len(matches) != 1:
        raise WorkspaceRendererError("pdftoppm 包装器没有唯一静态目标。")
    target_text = matches[0].group(0)
    if "%SCRIPT_DIR%" in target_text and _SCRIPT_DIR.search(text) is None:
        raise WorkspaceRendererError("pdftoppm 包装器的 SCRIPT_DIR 未固定。")
    relative = Path(matches[0].group("relative"))
    if relative.is_absolute() or "%" in str(relative):
        raise WorkspaceRendererError("pdftoppm 包装器目标不是静态相对路径。")
    target = _ordinary_file(wrapper.parent / relative, "pdftoppm wrapper target")
    _require_runtime_containment(target, runtime_root)
    return target


def _require_runtime_containment(path: Path, runtime_root: Path) -> None:
    try:
        path.relative_to(runtime_root)
    except ValueError as exc:
        raise WorkspaceRendererError("Poppler 入口越出加载器运行时根。") from exc
