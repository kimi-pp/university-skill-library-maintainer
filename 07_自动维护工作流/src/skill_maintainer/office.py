"""Microsoft Office read-only verification and hash-bound visual evidence."""

from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
from typing import Any, Iterable

from .paths import assert_ordinary_path, is_link_or_reparse


class OfficeVerificationError(RuntimeError):
    """Office or render evidence is missing, stale, or unsafe."""


@dataclass(frozen=True)
class RendererCommand:
    """Explicit loader-supplied PDF renderer command.

    The command receives ``--pdf ABSOLUTE`` and ``--output-dir ABSOLUTE`` and
    prints one JSON object with ordered page paths and body-pixel counts.
    """

    argv: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.argv or any(not str(part) for part in self.argv):
            raise OfficeVerificationError("PDF 渲染器命令不能为空。")

    def render(self, pdf: Path, output_dir: Path) -> tuple[tuple[Path, ...], tuple[int, ...]]:
        completed = subprocess.run(
            [*self.argv, "--pdf", str(pdf), "--output-dir", str(output_dir)],
            check=False, capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        stdout = completed.stdout.strip().lstrip("\ufeff")
        lines = [line for line in stdout.splitlines() if line.strip()]
        if completed.returncode != 0 or len(lines) != 1:
            detail = completed.stderr.strip() or stdout or f"exit={completed.returncode}"
            raise OfficeVerificationError(f"显式 PDF 渲染器失败：{detail}")
        try:
            payload = json.loads(lines[0])
        except json.JSONDecodeError as exc:
            raise OfficeVerificationError("显式 PDF 渲染器返回无效 JSON。") from exc
        rows = payload.get("pages") if isinstance(payload, dict) else None
        if not isinstance(rows, list) or not rows:
            raise OfficeVerificationError("显式 PDF 渲染器没有返回页面。")
        paths: list[Path] = []
        body_pixels: list[int] = []
        for index, row in enumerate(rows, start=1):
            if not isinstance(row, dict):
                raise OfficeVerificationError("显式 PDF 渲染器页面记录无效。")
            relative = Path(str(row.get("path") or ""))
            if relative.is_absolute() or relative.parts != (f"page-{index}.png",):
                raise OfficeVerificationError("显式 PDF 渲染器页面路径或顺序不符合契约。")
            page = output_dir / relative
            if not page.is_file() or is_link_or_reparse(page):
                raise OfficeVerificationError("显式 PDF 渲染器页面缺失或不是普通文件。")
            assert_ordinary_path(page)
            try:
                count = int(row["body_nonwhite_pixels"])
            except (KeyError, TypeError, ValueError) as exc:
                raise OfficeVerificationError("显式 PDF 渲染器缺少正文区域像素判定。") from exc
            if count < 0:
                raise OfficeVerificationError("显式 PDF 渲染器正文区域像素判定无效。")
            paths.append(page)
            body_pixels.append(count)
        return tuple(paths), tuple(body_pixels)


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
    body_nonwhite_pixels: tuple[int, ...] = ()
    blank_pages: tuple[int, ...] = ()
    visual_reviewed: bool = False
    page_approved: tuple[bool, ...] = ()
    visual_reviewer: str | None = None
    process_count_before: int = 0
    process_count_after: int = 0
    error: str | None = None

    def __bool__(self) -> bool:
        return self.passed


@dataclass(frozen=True)
class WordPageDecision:
    page_number: int
    sha256: str
    approved: bool


@dataclass(frozen=True)
class WordRenderDecision:
    source_sha256: str
    pdf_sha256: str
    pages: tuple[WordPageDecision, ...]
    reviewer: str

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
        rejected = set(rejected_pages)
        if any(page < 1 or page > len(check.page_sha256) for page in rejected):
            raise OfficeVerificationError("视觉驳回页码越出当前渲染范围。")
        return cls(
            check.source_sha256,
            check.pdf_sha256,
            tuple(
                WordPageDecision(index, digest, approved and index not in rejected)
                for index, digest in enumerate(check.page_sha256, start=1)
            ),
            reviewer.strip(),
        )


@dataclass(frozen=True)
class OfficeEvidenceBundle:
    """Exact Office evidence for every Word/Excel artifact in a commit."""

    checks: tuple[OfficeCheck, ...]
    sha256: str

    @classmethod
    def from_checks(cls, checks: Iterable[OfficeCheck]) -> "OfficeEvidenceBundle":
        frozen = tuple(checks)
        seen: set[Path] = set()
        records: list[dict[str, object]] = []
        for check in frozen:
            source = check.source_path.absolute()
            if source in seen:
                raise OfficeVerificationError(f"Office 证据重复绑定同一文件：{source}")
            seen.add(source)
            _validate_check(check)
            records.append({
                "kind": check.kind, "source_path": str(source),
                "source_sha256": check.source_sha256, "pdf_sha256": check.pdf_sha256,
                "page_sha256": list(check.page_sha256),
                "body_nonwhite_pixels": list(check.body_nonwhite_pixels),
                "visual_reviewed": check.visual_reviewed,
                "page_approved": list(check.page_approved),
                "visual_reviewer": check.visual_reviewer,
                "process_count_before": check.process_count_before,
                "process_count_after": check.process_count_after,
            })
        encoded = json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return cls(frozen, sha256(encoded).hexdigest())

    def assert_covers(self, paths: Iterable[str | Path]) -> None:
        rebuilt = type(self).from_checks(self.checks)
        if rebuilt.sha256 != self.sha256:
            raise OfficeVerificationError("Office 证据摘要与逐项证据不一致。")
        required = {
            Path(path).absolute()
            for path in paths
            if Path(path).suffix.casefold() in {".xlsx", ".docx"}
        }
        supplied = {check.source_path.absolute() for check in self.checks}
        if required != supplied:
            missing = sorted(str(path) for path in required - supplied)
            extra = sorted(str(path) for path in supplied - required)
            raise OfficeVerificationError(f"Office 证据未精确覆盖发布文件；缺失={missing}；多余={extra}")
        for check in self.checks:
            _validate_check(check)


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_check(check: OfficeCheck) -> None:
    source = check.source_path.absolute()
    if check.kind not in {"excel", "word"}:
        raise OfficeVerificationError("Office 证据类型必须是 excel 或 word。")
    if not check.passed or not check.office_passed or not check.office_opened or not check.read_only:
        raise OfficeVerificationError(f"Office 证据未完整通过：{source}")
    if check.process_count_before != check.process_count_after:
        raise OfficeVerificationError(f"Office 进程未精确返回基线：{source}")
    if not source.is_file() or is_link_or_reparse(source) or _sha256(source) != check.source_sha256:
        raise OfficeVerificationError(f"Office 源文件缺失或哈希已变化：{source}")
    if check.kind == "word":
        if not check.visual_reviewed or check.blank_pages:
            raise OfficeVerificationError(f"Word 未完成逐页视觉批准：{source}")
        if not check.pdf_path or not check.pdf_sha256 or not check.page_paths:
            raise OfficeVerificationError(f"Word PDF/逐页证据不完整：{source}")
        if len(check.page_paths) != len(check.page_sha256):
            raise OfficeVerificationError(f"Word 逐页证据数量不一致：{source}")
        if check.page_approved != (True,) * len(check.page_sha256) or not (check.visual_reviewer or "").strip():
            raise OfficeVerificationError(f"Word 逐页批准枚举或复核者证据不完整：{source}")
        evidence = ((check.pdf_path, check.pdf_sha256), *zip(check.page_paths, check.page_sha256))
        for path, digest in evidence:
            if not path.is_file() or is_link_or_reparse(path) or _sha256(path) != digest:
                raise OfficeVerificationError(f"Word PDF/逐页证据缺失或哈希已变化：{path}")


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
    before = int(result.get("process_count_before") or 0)
    after = int(result.get("process_count_after") or 0)
    exact_baseline = before == after
    passed = bool(result.get("passed")) and exact_baseline
    error = _friendly_error(result.get("error"))
    if not exact_baseline:
        error = "Excel COM 进程未精确返回验证前基线。"
    return OfficeCheck(
        kind="excel", source_path=source, source_sha256=source_hash,
        passed=passed, office_passed=passed,
        office_opened=bool(result.get("office_opened")), read_only=bool(result.get("read_only")),
        key_sheet=_optional_text(result.get("key_sheet")), last_row=_optional_int(result.get("last_row")),
        last_column=_optional_int(result.get("last_column")), last_value=_optional_text(result.get("last_value")),
        process_count_before=before, process_count_after=after, error=error,
    )


def verify_word(path: str | Path, render_dir: str | Path, *, renderer: RendererCommand) -> OfficeCheck:
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
    before = int(result.get("process_count_before") or 0)
    after = int(result.get("process_count_after") or 0)
    exact_baseline = before == after
    office_passed = bool(result.get("passed")) and exact_baseline
    pdf_text = _optional_text(result.get("pdf_path"))
    if not office_passed or not pdf_text:
        error = _friendly_error(result.get("error")) or "Word Office 复读失败。"
        if not exact_baseline:
            error = "Word COM 进程未精确返回验证前基线。"
        return OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=False, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")), process_count_before=before,
            process_count_after=after, error=error,
        )
    pdf = Path(pdf_text).absolute()
    try:
        pdf.relative_to(render)
        if not pdf.is_file() or is_link_or_reparse(pdf):
            raise OfficeVerificationError("Word PDF 不是渲染目录内的普通文件。")
        pages, body_pixels = renderer.render(pdf, render)
        page_hashes = tuple(_sha256(page) for page in pages)
        blank_pages = tuple(index for index, count in enumerate(body_pixels, start=1) if count == 0)
        reported_pages = int(result.get("page_count") or 0)
        if not pages or (reported_pages and len(pages) != reported_pages):
            raise OfficeVerificationError("Word 报告页数与逐页图像不一致或没有页面。")
        error = "逐页图像已生成；必须绑定外部视觉复核通过判定后方可发布。"
        if blank_pages:
            error = f"逐页渲染检测到无正文页面：{','.join(map(str, blank_pages))}"
        return OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=True, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")), pdf_path=pdf, pdf_sha256=_sha256(pdf),
            page_paths=pages, page_sha256=page_hashes, body_nonwhite_pixels=body_pixels,
            blank_pages=blank_pages, process_count_before=before, process_count_after=after,
            error=error,
        )
    except OfficeVerificationError as exc:
        return OfficeCheck(
            kind="word", source_path=source, source_sha256=source_hash,
            passed=False, office_passed=False, office_opened=bool(result.get("office_opened")),
            read_only=bool(result.get("read_only")), pdf_path=pdf if pdf.is_file() else None,
            pdf_sha256=_sha256(pdf) if pdf.is_file() else None,
            process_count_before=before, process_count_after=after, error=str(exc),
        )


def bind_word_visual_decision(check: OfficeCheck, decision: WordRenderDecision) -> OfficeCheck:
    if check.kind != "word" or not check.office_passed:
        raise OfficeVerificationError("只有完成 Word Office/PDF/逐页渲染的结果可以绑定视觉判定。")
    if check.process_count_before != check.process_count_after:
        raise OfficeVerificationError("Word COM 进程未精确返回验证前基线。")
    if check.blank_pages:
        raise OfficeVerificationError("Word 逐页图像包含空白正文页，不能批准发布。")
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
    expected = tuple((index, digest) for index, digest in enumerate(check.page_sha256, start=1))
    actual = tuple((page.page_number, page.sha256) for page in decision.pages)
    if decision.source_sha256 != check.source_sha256 or decision.pdf_sha256 != check.pdf_sha256:
        raise OfficeVerificationError("外部视觉判定未绑定当前 Word/PDF 哈希。")
    if actual != expected:
        raise OfficeVerificationError("外部视觉判定必须逐页枚举并绑定每一页精确哈希。")
    approved = bool(decision.pages) and all(page.approved for page in decision.pages)
    return replace(
        check,
        passed=approved,
        visual_reviewed=True,
        page_approved=tuple(page.approved for page in decision.pages),
        visual_reviewer=decision.reviewer,
        error=None if approved else "外部逐页视觉复核未通过。",
    )


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
        "excel-process-leak": "Excel COM 进程未精确返回验证前基线。",
        "word-not-read-only": "Word 未以只读方式打开。",
        "word-pdf-empty-or-missing": "Word PDF 导出为空或缺失。",
        "word-pdf-target-exists": "Word PDF 目标在验证期间已存在，拒绝覆盖。",
        "word-process-leak": "Word COM 进程未精确返回验证前基线。",
    }
    return messages.get(text, text)
