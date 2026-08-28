"""Microsoft Office read-only verification with hash-bound Word render review."""

from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

from .paths import assert_ordinary_path, is_link_or_reparse


class OfficeVerificationError(RuntimeError):
    """Office or render evidence is missing, stale, or unsafe."""


@dataclass(frozen=True)
class OfficeCheck:
    kind: str
    source_path: Path
    source_sha256: str
    passed: bool
    office_passed: bool
    office_opened: bool
    read_only: bool
    key_sheet: str | None = None
    last_row: int | None = None
    last_column: int | None = None
    last_value: str | None = None
    pdf_path: Path | None = None
    pdf_sha256: str | None = None
    page_paths: tuple[Path, ...] = ()
    page_sha256: tuple[str, ...] = ()
    blank_pages: tuple[int, ...] = ()
    visual_reviewed: bool = False
    process_count_before: int = 0
    process_count_after: int = 0
    error: str | None = None

    def __bool__(self) -> bool:
        return self.passed


@dataclass(frozen=True)
class WordRenderDecision:
    source_sha256: str
    pdf_sha256: str
    page_sha256: tuple[str, ...]
    approved: bool
    reviewer: str
    rejected_pages: tuple[int, ...] = ()

    @classmethod
    def from_check(
        cls,
        check: OfficeCheck,
        *,
        approved: bool,
        reviewer: str,
        rejected_pages: tuple[int, ...] = (),
    ) -> "WordRenderDecision":
        if check.kind != "word" or not check.pdf_sha256 or not check.page_sha256:
            raise OfficeVerificationError("Word 渲染证据不完整，不能形成视觉判定。")
        if not reviewer.strip():
            raise OfficeVerificationError("逐页视觉判定必须记录复核者。")
        return cls(
            source_sha256=check.source_sha256,
            pdf_sha256=check.pdf_sha256,
            page_sha256=check.page_sha256,
            approved=approved,
            reviewer=reviewer.strip(),
            rejected_pages=tuple(sorted(set(rejected_pages))),
        )


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ordinary_file(path: str | Path, suffix: str) -> Path:
    target = Path(path).absolute()
    if target.suffix.casefold() != suffix or not target.is_file() or is_link_or_reparse(target):
        raise OfficeVerificationError(f"必须提供普通 {suffix} 文件：{target}")
    assert_ordinary_path(target)
    return target


def _powershell() -> str:
    executable = shutil.which("powershell.exe") or shutil.which("powershell")
    if not executable:
        raise OfficeVerificationError("未找到 Windows PowerShell，无法执行 Office COM 复读。")
    return executable


def _script_path() -> Path:
    path = Path(__file__).resolve().parents[2] / "verify_office.ps1"
    if not path.is_file():
        raise OfficeVerificationError(f"缺少 Office 验证脚本：{path}")
    return path


def _run_office(*arguments: str) -> dict[str, Any]:
    if os.name != "nt":
        raise OfficeVerificationError("Microsoft Office COM 验证只支持 Windows。")
    command = [
        _powershell(), "-NoLogo", "-NoProfile", "-NonInteractive",
        "-ExecutionPolicy", "Bypass", "-File", str(_script_path()), *arguments,
    ]
    completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8", errors="replace")
    stdout = completed.stdout.strip().lstrip("\ufeff")
    lines = [line for line in stdout.splitlines() if line.strip()]
    if completed.returncode != 0 or len(lines) != 1:
        detail = completed.stderr.strip() or stdout or f"exit={completed.returncode}"
        raise OfficeVerificationError(f"Office 验证脚本没有返回唯一 JSON 结果：{detail}")
    try:
        result = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise OfficeVerificationError("Office 验证脚本返回了无效 JSON。") from exc
    if not isinstance(result, dict):
        raise OfficeVerificationError("Office 验证脚本结果必须是对象。")
    return result


def verify_excel(path: str | Path) -> OfficeCheck:
    source = _ordinary_file(path, ".xlsx")
    source_hash = _sha256(source)
    result = _run_office("-Excel", str(source))
    return OfficeCheck(
        kind="excel", source_path=source, source_sha256=source_hash,
        passed=bool(result.get("passed")), office_passed=bool(result.get("passed")),
        office_opened=bool(result.get("office_opened")), read_only=bool(result.get("read_only")),
        key_sheet=_optional_text(result.get("key_sheet")), last_row=_optional_int(result.get("last_row")),
        last_column=_optional_int(result.get("last_column")), last_value=_optional_text(result.get("last_value")),
        process_count_before=int(result.get("process_count_before") or 0),
        process_count_after=int(result.get("process_count_after") or 0),
        error=_friendly_error(result.get("error")),
    )


def verify_word(path: str | Path, render_dir: str | Path) -> OfficeCheck:
    source = _ordinary_file(path, ".docx")
    source_hash = _sha256(source)
    render = Path(render_dir).absolute()
    if render.exists():
        assert_ordinary_path(render, require_directory=True)
        if any(render.iterdir()):
            raise OfficeVerificationError("Word 逐页渲染目录必须是空目录，拒绝覆盖既有文件。")
    else:
        render.mkdir(parents=True, exist_ok=False)
        assert_ordinary_path(render, require_directory=True)
    result = _run_office("-Word", str(source), "-RenderDirectory", str(render))
    office_passed = bool(result.get("passed"))
    pdf_text = _optional_text(result.get("pdf_path"))
    if not office_passed or not pdf_text:
        return OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=False, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")),
            process_count_before=int(result.get("process_count_before") or 0),
            process_count_after=int(result.get("process_count_after") or 0),
            error=_friendly_error(result.get("error")) or "Word Office 复读失败。",
        )
    pdf = Path(pdf_text).absolute()
    try:
        pdf.relative_to(render)
        if not pdf.is_file() or is_link_or_reparse(pdf):
            raise OfficeVerificationError("Word PDF 不是渲染目录内的普通文件。")
        pages, blank_pages = _render_pdf_pages(pdf, render)
        page_hashes = tuple(_sha256(page) for page in pages)
        reported_pages = int(result.get("page_count") or 0)
        if not pages or (reported_pages and len(pages) != reported_pages):
            raise OfficeVerificationError("Word 报告页数与逐页图像不一致或没有页面。")
        error = "逐页图像已生成；必须绑定外部视觉复核通过判定后方可发布。"
        if blank_pages:
            error = f"逐页渲染检测到空白页：{','.join(map(str, blank_pages))}"
        return OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=True, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")), pdf_path=pdf, pdf_sha256=_sha256(pdf),
            page_paths=pages, page_sha256=page_hashes, blank_pages=blank_pages,
            process_count_before=int(result.get("process_count_before") or 0),
            process_count_after=int(result.get("process_count_after") or 0), error=error,
        )
    except OfficeVerificationError as exc:
        return OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=False, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")), pdf_path=pdf if pdf.is_file() else None,
            pdf_sha256=_sha256(pdf) if pdf.is_file() else None,
            process_count_before=int(result.get("process_count_before") or 0),
            process_count_after=int(result.get("process_count_after") or 0), error=str(exc),
        )


def bind_word_visual_decision(check: OfficeCheck, decision: WordRenderDecision) -> OfficeCheck:
    if check.kind != "word" or not check.office_passed:
        raise OfficeVerificationError("只有完成 Word Office/PDF/逐页渲染的结果可以绑定视觉判定。")
    if check.blank_pages:
        raise OfficeVerificationError("Word 逐页图像包含空白页，不能批准发布。")
    if not check.pdf_path or not check.page_paths or len(check.page_paths) != len(check.page_sha256):
        raise OfficeVerificationError("Word PDF 或逐页图像证据缺失。")
    evidence_paths = (check.source_path, check.pdf_path, *check.page_paths)
    if any(not path.is_file() or is_link_or_reparse(path) for path in evidence_paths):
        raise OfficeVerificationError("Word 源文档、PDF 或逐页图像证据缺失。")
    if check.source_sha256 != _sha256(check.source_path):
        raise OfficeVerificationError("Word 源文档哈希已变化。")
    if check.pdf_sha256 != _sha256(check.pdf_path):
        raise OfficeVerificationError("Word PDF 哈希已变化。")
    current_page_hashes = tuple(_sha256(path) for path in check.page_paths)
    if current_page_hashes != check.page_sha256:
        raise OfficeVerificationError("Word 逐页图像哈希已变化。")
    if (
        decision.source_sha256 != check.source_sha256
        or decision.pdf_sha256 != check.pdf_sha256
        or decision.page_sha256 != check.page_sha256
    ):
        raise OfficeVerificationError("外部视觉判定未绑定当前 Word/PDF/逐页图像哈希。")
    if decision.rejected_pages and any(page < 1 or page > len(check.page_paths) for page in decision.rejected_pages):
        raise OfficeVerificationError("视觉驳回页码越出当前渲染范围。")
    approved = decision.approved and not decision.rejected_pages
    return replace(
        check,
        passed=approved,
        visual_reviewed=True,
        error=None if approved else "外部逐页视觉复核未通过。",
    )


def _render_pdf_pages(pdf: Path, render_dir: Path) -> tuple[tuple[Path, ...], tuple[int, ...]]:
    try:
        from pdf2image import convert_from_path
        from PIL import ImageChops
    except ImportError as exc:
        raise OfficeVerificationError("Codex 打包 PDF 渲染依赖不可用。") from exc
    with tempfile.TemporaryDirectory(prefix="word-pages-", dir=render_dir) as temporary:
        try:
            images = convert_from_path(str(pdf), dpi=150, fmt="png", thread_count=1)
        except Exception as exc:
            raise OfficeVerificationError(f"Word PDF 逐页渲染失败：{exc}") from exc
        if not images:
            raise OfficeVerificationError("Word PDF 没有可渲染页面。")
        temporary_root = Path(temporary)
        generated: list[Path] = []
        blank: list[int] = []
        for index, image in enumerate(images, start=1):
            page = temporary_root / f"page-{index}.png"
            image.save(page, "PNG")
            rgb = image.convert("RGB")
            # Compare to a same-sized white canvas; one non-white pixel makes the page nonblank.
            white = rgb.copy()
            white.paste((255, 255, 255), (0, 0, white.width, white.height))
            difference = ImageChops.difference(rgb, white)
            if difference.getbbox() is None:
                blank.append(index)
            generated.append(page)
        final_pages: list[Path] = []
        for index, page in enumerate(generated, start=1):
            destination = render_dir / f"page-{index}.png"
            try:
                with page.open("rb") as source, destination.open("xb") as target:
                    shutil.copyfileobj(source, target)
            except FileExistsError as exc:
                raise OfficeVerificationError("渲染目录在生成期间出现同名页面文件，拒绝覆盖。") from exc
            final_pages.append(destination)
        return tuple(final_pages), tuple(blank)


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    return int(value)


def _friendly_error(value: object) -> str | None:
    text = _optional_text(value)
    if text is None:
        return None
    messages = {
        "excel-not-read-only": "Excel 未以只读方式打开。",
        "excel-no-data-row": "关键工作表没有非空数据行或末尾数据单元格为空。",
        "excel-process-leak": "Excel COM 进程未回到验证前基线。",
        "word-not-read-only": "Word 未以只读方式打开。",
        "word-pdf-empty-or-missing": "Word PDF 导出为空或缺失。",
        "word-pdf-target-exists": "Word PDF 目标在验证期间已存在，拒绝覆盖。",
        "word-process-leak": "Word COM 进程未回到验证前基线。",
    }
    return messages.get(text, text)
