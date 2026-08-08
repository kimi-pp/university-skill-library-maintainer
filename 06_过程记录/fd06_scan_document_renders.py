#!/usr/bin/env python3
"""Scan every rendered FD06 Word page and build chunked contact sheets for QA."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat


ROOT = Path(__file__).resolve().parent / "fd06_artifacts"
RENDERS = ROOT / "docx_renders"
CONTACTS = ROOT / "docx_contact_sheets"
CONTACTS.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.load_default()


def page_number(path: Path) -> int:
    return int(path.stem.split("-")[-1])


def scan_page(path: Path) -> dict:
    image = Image.open(path).convert("L")
    width, height = image.size
    histogram = image.histogram()
    ink = sum(histogram[:246])
    dark = sum(histogram[:225])
    total = width * height
    mask = image.point(lambda value: 0 if value > 248 else 255)
    box = mask.getbbox()
    warnings = []
    if ink / total < 0.001:
        warnings.append("possibly_blank")
    if box is None:
        warnings.append("blank")
        margins = None
    else:
        left, top, right, bottom = box
        margins = {"left": left, "top": top, "right": width - right, "bottom": height - bottom}
        if min(margins.values()) < 20:
            warnings.append("content_near_edge")
    return {
        "file": str(path),
        "size": [width, height],
        "ink_ratio": round(ink / total, 6),
        "dark_ratio": round(dark / total, 6),
        "content_margins_px": margins,
        "warnings": warnings,
    }


def make_contacts(key: str, pages: list[Path], chunk_size: int = 16) -> list[str]:
    outputs = []
    thumb_width = 255
    columns = 4
    label_height = 22
    gap = 5
    sample = Image.open(pages[0]).convert("RGB")
    thumb_height = round(sample.height * thumb_width / sample.width)
    for chunk_index, start in enumerate(range(0, len(pages), chunk_size), 1):
        chunk = pages[start : start + chunk_size]
        rows = (len(chunk) + columns - 1) // columns
        canvas = Image.new(
            "RGB",
            (columns * (thumb_width + gap) - gap, rows * (thumb_height + label_height + gap) - gap),
            "#D7DEE5",
        )
        draw = ImageDraw.Draw(canvas)
        for index, page_path in enumerate(chunk):
            page = Image.open(page_path).convert("RGB")
            page.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            column = index % columns
            row = index // columns
            x = column * (thumb_width + gap)
            y = row * (thumb_height + label_height + gap)
            draw.rectangle((x, y, x + thumb_width, y + label_height), fill="#17324D")
            draw.text((x + 7, y + 6), f"{key} page {page_number(page_path)}", fill="white", font=FONT)
            canvas.paste(page, (x + (thumb_width - page.width) // 2, y + label_height))
        output = CONTACTS / f"{key}_contact_{chunk_index:02d}.png"
        canvas.save(output, optimize=True)
        outputs.append(str(output))
    return outputs


def main() -> None:
    reports = []
    all_warnings = []
    for directory in sorted(path for path in RENDERS.iterdir() if path.is_dir()):
        pages = sorted(directory.glob("page-*.png"), key=page_number)
        assert pages, f"no pages: {directory}"
        page_reports = [scan_page(page) for page in pages]
        for report in page_reports:
            if report["warnings"]:
                all_warnings.append(report)
        contacts = make_contacts(directory.name, pages)
        reports.append(
            {
                "key": directory.name,
                "pages": len(pages),
                "dimensions": sorted({tuple(report["size"]) for report in page_reports}),
                "warnings": sum(bool(report["warnings"]) for report in page_reports),
                "contact_sheets": contacts,
                "page_reports": page_reports,
            }
        )
    result = {
        "documents": len(reports),
        "pages": sum(report["pages"] for report in reports),
        "warning_pages": len(all_warnings),
        "reports": reports,
    }
    (ROOT / "docx_render_scan.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"documents": result["documents"], "pages": result["pages"], "warning_pages": result["warning_pages"], "contact_sheets": len(list(CONTACTS.glob('*.png')))}, ensure_ascii=False))
    if all_warnings:
        for report in all_warnings[:30]:
            print(report["file"], report["warnings"], report["content_margins_px"])


if __name__ == "__main__":
    main()
