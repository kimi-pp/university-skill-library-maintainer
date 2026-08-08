from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = ROOT / "02_知识库" / "functional_domains" / "06_课程设计教学材料与教学评估"
DELIVERY_ROOT = ROOT / "05_交付物" / "06_课程设计、教学材料与教学评估_全网公开技能调研"

INDEXES = [
    ROOT / "00_索引" / "INDEX.md",
    KB_ROOT / "INDEX.md",
    KB_ROOT / "SUBCATEGORY_INDEX.md",
    KB_ROOT / "skills" / "INDEX.md",
    DELIVERY_ROOT / "INDEX.md",
    ROOT / "06_过程记录" / "2026-08-09-FD06交付物质检.md",
    *sorted((KB_ROOT / "subcategories").glob("*/INDEX.md")),
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def verify() -> tuple[int, int]:
    missing: list[str] = []
    checked_links = 0
    for index_path in INDEXES:
        if not index_path.is_file():
            missing.append(f"missing index: {index_path}")
            continue
        text = index_path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            checked_links += 1
            resolved = (index_path.parent / unquote(target)).resolve()
            if not resolved.exists():
                missing.append(f"{index_path.relative_to(ROOT)} -> {target}")
    if missing:
        raise SystemExit("Broken local links:\n" + "\n".join(missing))
    return len(INDEXES), checked_links


if __name__ == "__main__":
    index_count, link_count = verify()
    print(f"indexes={index_count}; local_links={link_count}; missing=0")
