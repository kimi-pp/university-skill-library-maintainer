from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MODULE_ROOT = Path(__file__).resolve().parent
if str(MODULE_ROOT) not in sys.path:
    sys.path.insert(0, str(MODULE_ROOT))

from economics_contract import CLASS_COUNTS, CLASS_ORDER, PROJECT_ROOT, RUN_ROOT, write_json


CATALOG_PATH = (
    PROJECT_ROOT
    / "06_过程记录"
    / "discipline_mapping"
    / "catalogs"
    / "undergraduate_2026.json"
)
SOURCE_MANIFEST_PATH = (
    PROJECT_ROOT
    / "06_过程记录"
    / "discipline_mapping"
    / "source_manifest.json"
)
CATEGORY_PATH = (
    PROJECT_ROOT
    / "02_知识库"
    / "discipline_catalog"
    / "categories"
    / "02_经济学.md"
)
INDEX_PATH = PROJECT_ROOT / "02_知识库" / "discipline_catalog" / "INDEX.md"
SOURCE_METHOD_PATH = (
    PROJECT_ROOT
    / "02_知识库"
    / "discipline_catalog"
    / "SOURCE_AND_METHOD.md"
)


def load_economics_scope(catalog_path: Path) -> dict[str, Any]:
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    selected = [row for row in payload["records"] if row["category_code"] == "02"]
    classes: list[dict[str, Any]] = []
    for class_code in CLASS_ORDER:
        rows = sorted(
            (row for row in selected if row["class_code"] == class_code),
            key=lambda row: row["major_code"],
        )
        expected = CLASS_COUNTS[class_code]
        if len(rows) != expected:
            raise ValueError(f"{class_code} count mismatch: {len(rows)} != {expected}")
        if not rows:
            raise ValueError(f"{class_code} is empty")
        classes.append(
            {
                "class_code": class_code,
                "class_name": rows[0]["class_name"],
                "major_count": len(rows),
                "majors": rows,
            }
        )
    codes = [major["major_code"] for row in classes for major in row["majors"]]
    if len(codes) != 30 or len(set(codes)) != 30:
        raise ValueError("economics scope must contain 30 unique major codes")
    return {
        "category_code": "02",
        "category_name": "经济学",
        "class_count": len(classes),
        "major_count": len(codes),
        "source_id": "undergraduate_2026_pdf",
        "classes": classes,
    }


def load_source_meta(manifest_path: Path) -> dict[str, Any]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    for row in payload["sources"]:
        if row["id"] == "undergraduate_2026_pdf":
            return row
    raise ValueError("undergraduate_2026_pdf source is missing")


def render_category(scope: dict[str, Any], source: dict[str, Any]) -> str:
    lines = [
        "# 02 经济学",
        "",
        "- 现行专业类：4 个",
        "- 现行本科专业：30 个",
        f"- 现行依据：教育部《{source['title']}》（{source['publication_date']}发布）",
        f"- 公开地址：{source['url']}",
        f"- 本地快照：`06_过程记录/discipline_mapping/{source['local_path']}`",
        f"- 快照 SHA-256：`{source['sha256']}`",
        f"- 目录访问日期：{source['accessed_at']}",
        "- 历史口径：原项目索引为4类20专业，现仅作为差异追溯，不再作为经济学现行范围。",
        "",
    ]
    for class_row in scope["classes"]:
        lines.extend(
            [
                f"## {class_row['class_code']} {class_row['class_name']}",
                "",
                f"专业数：{class_row['major_count']}",
                "",
                "| 专业代码 | 专业名称 | 授予学位门类 |",
                "|---|---|---|",
            ]
        )
        for major in class_row["majors"]:
            degrees = "、".join(major.get("degree_categories") or []) or "未列明"
            lines.append(f"| {major['major_code']} | {major['major_name']} | {degrees} |")
        lines.append("")
    lines.extend(
        [
            "## 版本说明",
            "",
            "- 本页已按教育部2026年现行本科专业目录校订。",
            "- 旧工作簿中的代码顺序不得继续用于经济学新调研或交付。",
            "- 旧版与现行版差异保存在 `06_过程记录/economics_2026-08-19/catalog_diff.json`。",
            "",
            "[返回学科分类总索引](../INDEX.md)",
            "",
        ]
    )
    return "\n".join(lines)


def patch_index(text: str, scope: dict[str, Any]) -> str:
    if scope["class_count"] != 4 or scope["major_count"] != 30:
        raise ValueError("refusing to patch index with non-current economics scope")
    updated = text.replace(
        "> 本索引只结构化 `国内大学本科专业目录.xlsx` 内已有内容；未联网、未补充、未校订，也未启动任何 skill 调研。",
        "> 本索引以历史工作簿为基础；`02 经济学`已按教育部《普通高等学校本科专业目录（2026年）》校订为现行口径，其他门类仍保留原索引口径。",
    )
    updated = updated.replace(
        "- 明细表实际数量：13 个门类、103 个一级学科、512 个专业",
        "- 历史工作簿明细：13 个门类、103 个一级学科、512 个专业；经济学现行校订后本索引展示总数为522个专业",
    )
    updated = updated.replace(
        "| 02 | 经济学 | 4 | 20 | [查看](categories/02_经济学.md) |",
        "| 02 | 经济学 | 4 | 30 | [查看](categories/02_经济学.md) |",
    )
    updated = updated.replace(
        "| 经济学 | 4 | 4 | 20 | 20 | 一致 |",
        "| 经济学 | 4 | 4 | 30（现行） | 20（旧统计） | 已按教育部2026目录校订 |",
    )
    if "| 02 | 经济学 | 4 | 30 |" not in updated:
        raise ValueError("economics entry not patched")
    return updated


def patch_source_method(text: str, source: dict[str, Any]) -> str:
    marker = "## 现行校订：02 经济学"
    if marker in text:
        return text
    addition = "\n".join(
        [
            "",
            marker,
            "",
            f"- 现行来源：教育部《{source['title']}》",
            f"- 发布日期：{source['publication_date']}",
            f"- 访问日期：{source['accessed_at']}",
            f"- 公开地址：{source['url']}",
            f"- 本地快照：`06_过程记录/discipline_mapping/{source['local_path']}`",
            f"- SHA-256：`{source['sha256']}`",
            "- 适用范围：仅将 `02 经济学`更新为4个专业类、30个专业；旧工作簿来源和其他门类原始索引继续保留。",
            "- 处理方法：按教育部目录的门类、专业类、专业代码和专业名称原样提取；旧表代码顺延不再用于经济学新任务。",
            "",
        ]
    )
    return text.rstrip() + "\n" + addition


OLD_ROW_PATTERN = re.compile(r"\|\s*(02\d{4}[A-Z]*)\s*\|\s*([^|]+?)\s*\|")


def build_catalog_diff(old_text: str, scope: dict[str, Any]) -> dict[str, Any]:
    old_rows = [
        {"major_code": match.group(1), "major_name": match.group(2).strip()}
        for match in OLD_ROW_PATTERN.finditer(old_text)
    ]
    current_rows = [
        {"major_code": major["major_code"], "major_name": major["major_name"]}
        for class_row in scope["classes"]
        for major in class_row["majors"]
    ]
    old_by_name = {row["major_name"]: row["major_code"] for row in old_rows}
    current_by_name = {row["major_name"]: row["major_code"] for row in current_rows}
    code_changes = [
        {"major_name": name, "old_code": old_by_name[name], "current_code": current_by_name[name]}
        for name in sorted(old_by_name.keys() & current_by_name.keys())
        if old_by_name[name] != current_by_name[name]
    ]
    added = [row for row in current_rows if row["major_name"] not in old_by_name]
    removed = [row for row in old_rows if row["major_name"] not in current_by_name]
    return {
        "category_code": "02",
        "old_major_count": len(old_rows),
        "current_major_count": len(current_rows),
        "net_change": len(current_rows) - len(old_rows),
        "code_changes": code_changes,
        "added_majors": added,
        "removed_majors": removed,
    }


def apply_updates() -> None:
    scope = load_economics_scope(CATALOG_PATH)
    source = load_source_meta(SOURCE_MANIFEST_PATH)
    old_category = CATEGORY_PATH.read_text(encoding="utf-8")
    write_json(RUN_ROOT / "economics_scope.json", {**scope, "source": source})
    write_json(RUN_ROOT / "catalog_diff.json", build_catalog_diff(old_category, scope))
    CATEGORY_PATH.write_text(render_category(scope, source), encoding="utf-8", newline="\n")
    INDEX_PATH.write_text(
        patch_index(INDEX_PATH.read_text(encoding="utf-8"), scope),
        encoding="utf-8",
        newline="\n",
    )
    SOURCE_METHOD_PATH.write_text(
        patch_source_method(SOURCE_METHOD_PATH.read_text(encoding="utf-8"), source),
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.apply:
        parser.error("--apply is required")
    apply_updates()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
