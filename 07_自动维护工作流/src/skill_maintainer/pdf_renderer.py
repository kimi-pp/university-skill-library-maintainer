"""Portable project entrypoint for Task 11 PDF page evidence."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Any


class PdfRendererError(RuntimeError):
    """The renderer input, dependency, or output violates its contract."""


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise PdfRendererError(message)


def render(argv: list[str] | None = None) -> dict[str, list[dict[str, Any]]]:
    """Render an ordinary absolute PDF into an existing empty ordinary directory."""
    parser = _Parser(add_help=False)
    parser.add_argument("--python-packages", required=True)
    parser.add_argument("--pdftoppm", required=True)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args(argv)

    packages = _ordinary_directory(_absolute(args.python_packages, "python-packages"), "python-packages")
    pdftoppm = _ordinary_file(_absolute(args.pdftoppm, "pdftoppm"), "pdftoppm")
    if pdftoppm.name.lower() != "pdftoppm.exe":
        raise PdfRendererError("pdftoppm 必须是显式 .exe 文件")
    _ordinary_file(pdftoppm.with_name("pdfinfo.exe"), "pdfinfo")
    pdf = _ordinary_file(_absolute(args.pdf, "pdf"), "pdf")
    if pdf.suffix.lower() != ".pdf":
        raise PdfRendererError("输入文件扩展名必须为 .pdf")
    output = _ordinary_directory(_absolute(args.output_dir, "output-dir"), "output-dir")
    if any(output.iterdir()):
        raise PdfRendererError("输出目录必须为空")

    _extend_package_path(packages)
    try:
        from pdf2image import convert_from_path
        from PIL import Image, ImageChops
    except ImportError as exc:
        raise PdfRendererError("加载器 Python 环境缺少 pdf2image 或 Pillow") from exc

    work = output / ".rendering"
    work.mkdir(exist_ok=False)
    _ordinary_directory(work, "render work directory")
    moved: list[Path] = []
    try:
        images = convert_from_path(
            str(pdf),
            dpi=150,
            fmt="png",
            thread_count=1,
            poppler_path=str(pdftoppm.parent),
            use_pdftocairo=False,
        )
        if not images:
            raise PdfRendererError("PDF 没有可渲染页面")
        rows: list[dict[str, Any]] = []
        staged: list[Path] = []
        for index, image in enumerate(images, start=1):
            target = work / f"page-{index}.png"
            rgb = image.convert("RGB")
            rgb.save(target, "PNG")
            _ordinary_file(target, f"page-{index}")
            top = max(1, int(rgb.height * 0.10))
            bottom = min(rgb.height, int(rgb.height * 0.90))
            body = rgb.crop((0, top, rgb.width, bottom))
            white = Image.new("RGB", body.size, (255, 255, 255))
            difference = ImageChops.difference(body, white).convert("L")
            pixels = sum(difference.histogram()[1:])
            rows.append({"path": target.name, "body_nonwhite_pixels": pixels})
            staged.append(target)
        for source in staged:
            destination = output / source.name
            os.replace(source, destination)
            _ordinary_file(destination, source.name)
            moved.append(destination)
        work.rmdir()
        return {"pages": rows}
    except Exception:
        for page in moved:
            if page.exists() and page.parent == output and not _is_link_or_reparse(page):
                page.unlink()
        _clean_owned_work_directory(work)
        raise


def _extend_package_path(packages: Path) -> None:
    candidates = (packages, packages / "Lib" / "site-packages")
    for candidate in reversed(candidates):
        if candidate.is_dir() and not _is_link_or_reparse(candidate):
            sys.path.insert(0, str(candidate))


def _absolute(value: str, label: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise PdfRendererError(f"{label} 必须为绝对路径")
    return path.absolute()


def _ordinary_file(path: Path, label: str) -> Path:
    _assert_ordinary_chain(path)
    if not path.is_file() or _is_link_or_reparse(path):
        raise PdfRendererError(f"{label} 不是普通文件")
    return path.resolve(strict=True)


def _ordinary_directory(path: Path, label: str) -> Path:
    _assert_ordinary_chain(path)
    if not path.is_dir() or _is_link_or_reparse(path):
        raise PdfRendererError(f"{label} 不是普通目录")
    return path.resolve(strict=True)


def _assert_ordinary_chain(path: Path) -> None:
    for current in (path, *path.parents):
        if (current.exists() or current.is_symlink()) and _is_link_or_reparse(current):
            raise PdfRendererError(f"路径包含链接或重解析点：{current}")


def _is_link_or_reparse(path: Path) -> bool:
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return False
    return path.is_symlink() or bool(getattr(stat, "st_file_attributes", 0) & 0x400)


def _clean_owned_work_directory(work: Path) -> None:
    if not work.exists() or _is_link_or_reparse(work):
        return
    for child in tuple(work.iterdir()):
        if child.is_file() and not _is_link_or_reparse(child):
            child.unlink()
        elif child.is_dir() and not _is_link_or_reparse(child):
            shutil.rmtree(child)
    try:
        work.rmdir()
    except OSError:
        pass


def main(argv: list[str] | None = None) -> int:
    try:
        payload = render(argv)
    except Exception as exc:
        print(f"renderer-error:{exc}", file=sys.stderr)
        return 2
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
