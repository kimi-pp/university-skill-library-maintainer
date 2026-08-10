#!/usr/bin/env python3
"""Build compact contact sheets for visual QA of every FD06 workbook render."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent / "fd06_artifacts" / "xlsx_renders"
OUT = Path(__file__).resolve().parent / "fd06_artifacts" / "xlsx_contact_sheets"
OUT.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.load_default()
PREFIXES = ["00"] + [f"06_{index:02d}" for index in range(1, 13)]


def fit(image: Image.Image, width: int) -> Image.Image:
    if image.width <= width:
        return image.copy()
    ratio = width / image.width
    return image.resize((width, max(1, round(image.height * ratio))), Image.Resampling.LANCZOS)


for prefix in PREFIXES:
    panels: list[tuple[str, Image.Image]] = []
    for sheet, label in [("使用说明", "Guide"), ("分类统计", "Statistics"), ("来源清单", "Sources")]:
        image = Image.open(ROOT / f"{prefix}_{sheet}.png").convert("RGB")
        panels.append((label, fit(image, 1450)))

    skill = Image.open(ROOT / f"{prefix}_AI技能清单.png").convert("RGB")
    if skill.height > 4000:
        crop_height = min(1200, skill.height // 3)
        starts = [0, (skill.height - crop_height) // 2, skill.height - crop_height]
        labels = ["Skill list - top", "Skill list - middle", "Skill list - bottom"]
        for label, start in zip(labels, starts):
            panels.append((label, fit(skill.crop((0, start, skill.width, start + crop_height)), 1450)))
    else:
        panels.append(("Skill list", fit(skill, 1450)))

    label_height = 34
    gap = 18
    height = 24 + sum(label_height + panel.height + gap for _, panel in panels)
    canvas = Image.new("RGB", (1500, height), "#D7DEE5")
    draw = ImageDraw.Draw(canvas)
    y = 16
    for label, panel in panels:
        draw.rectangle((12, y, 1488, y + label_height - 4), fill="#17324D")
        draw.text((24, y + 8), f"{prefix} {label}", fill="white", font=FONT)
        y += label_height
        canvas.paste(panel, ((1500 - panel.width) // 2, y))
        y += panel.height + gap
    canvas.save(OUT / f"{prefix}_contact.png", optimize=True)

print(f"contact_sheets={len(list(OUT.glob('*_contact.png')))}")
