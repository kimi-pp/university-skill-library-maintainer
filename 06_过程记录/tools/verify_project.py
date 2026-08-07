"""最终项目级一致性检查。"""

from __future__ import annotations

import json
import re
from pathlib import Path


project_root = Path(__file__).resolve().parents[2]
data_dir = project_root / "03_候选池" / "deduplicated"
manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
expected_counts = {"01": 20, "02": 22, "03": 31, "04": 29, "05": 55}

all_ids = []
for category, expected_count in expected_counts.items():
    payload = json.loads((data_dir / f"category_{category}.json").read_text(encoding="utf-8"))
    assert len(payload["records"]) == expected_count, f"{category}: 规范数据数量错误"
    all_ids.extend(row["id"] for row in payload["records"])
expected_total = sum(expected_counts.values())
assert len(all_ids) == expected_total and len(set(all_ids)) == expected_total, "Skill ID 总数或唯一性错误"

domain_dirs = {
    "01": project_root / "02_知识库" / "functional_domains" / "01_学术写作引用与出版" / "skills",
    "02": project_root / "02_知识库" / "functional_domains" / "02_文档表格演示文稿与办公自动化" / "skills",
    "03": project_root / "02_知识库" / "functional_domains" / "03_文献检索与学术研究" / "skills",
    "04": project_root / "02_知识库" / "functional_domains" / "04_图书馆与信息素养" / "skills",
    "05": project_root / "02_知识库" / "functional_domains" / "05_编程数学数据分析和可视化" / "skills",
}
for category, skill_dir in domain_dirs.items():
    assert len(list(skill_dir.glob("GH-*.md"))) == expected_counts[category], f"{category}: 知识库条目数错误"

deliverable_dir = project_root / "05_交付物"
actual_deliverables = sorted(
    item.name for item in deliverable_dir.iterdir()
    if item.is_file() and not item.name.startswith("~$")
)
expected_deliverables = sorted(item["path"] for item in manifest)
assert actual_deliverables == expected_deliverables, "交付目录与清单定义不一致"
assert all((deliverable_dir / name).stat().st_size > 0 for name in expected_deliverables), "存在空交付文件"

page_counts = {
    category: len(list((project_root / "06_过程记录" / "renders" / "docx_final" / category).glob("page-*.png")))
    for category in expected_counts
}

broken_links = []
for markdown_path in project_root.rglob("*.md"):
    if "node_modules" in markdown_path.parts:
        continue
    text = markdown_path.read_text(encoding="utf-8")
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = match.group(1).split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (markdown_path.parent / target).resolve()
        if not resolved.exists():
            broken_links.append(f"{markdown_path}: {target}")
assert not broken_links, "Markdown 入口存在失效链接:\n" + "\n".join(broken_links)

print(
    f"catalog={expected_total} unique; knowledge_md={expected_total}; "
    f"deliverables={len(expected_deliverables)}; docx_pages={page_counts}; markdown_links=OK"
)
