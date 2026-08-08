"""Build the subcategory delivery manifest and Markdown knowledge-base entries.

This task intentionally plans future DOCX/XLSX files but does not create them.
All reader-facing Skill text comes from the approved plain-language catalog.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSIGNMENT_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_assignments.json"
PLAIN_CATALOG_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "plain_language_catalog.json"
MANIFEST_FILE = PROJECT_ROOT / "03_候选池" / "derived" / "subcategory_manifest.json"
KNOWLEDGE_BASE_ROOT = PROJECT_ROOT / "02_知识库" / "functional_domains"
DELIVERY_ROOT = Path("05_交付物") / "通俗细分版_2026-08-07"

BIG_CATEGORY_DIRECTORIES = {
    "01": "01_学术写作引用与出版",
    "02": "02_文档表格演示文稿与办公自动化",
    "03": "03_文献检索与学术研究",
    "04": "04_图书馆与信息素养",
    "05": "05_编程数学数据分析和可视化",
}

_WINDOWS_FORBIDDEN = set('<>:"|?*')
_CODE_PATTERN = re.compile(r"^\d{2}-\d{2}$")
_NAVIGATION_START = "<!-- SUBCATEGORY_NAVIGATION_START -->"
_NAVIGATION_END = "<!-- SUBCATEGORY_NAVIGATION_END -->"


def _safe_component(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}不能为空")
    if value in {".", ".."} or any(character in value for character in _WINDOWS_FORBIDDEN | {"/", "\\"}):
        raise ValueError(f"非法路径字符: {label}={value!r}")
    if value.rstrip(". ") != value:
        raise ValueError(f"非法路径字符: {label}={value!r}")
    return value


def _sorted_taxonomy(taxonomy: Iterable[dict]) -> list[dict]:
    """Validate taxonomy fields and return a stable code-ordered copy."""
    items = [dict(item) for item in taxonomy]
    seen_codes: set[str] = set()
    for item in items:
        code = item.get("code")
        name = item.get("name")
        if not isinstance(code, str) or not _CODE_PATTERN.fullmatch(code):
            raise ValueError(f"小分类代码格式错误: {code!r}")
        if code[:2] not in BIG_CATEGORY_DIRECTORIES:
            raise ValueError(f"未知大分类: {code}")
        _safe_component(code, "小分类代码")
        _safe_component(name, "小分类名称")
        if not isinstance(item.get("inclusion_focus"), str) or not item["inclusion_focus"].strip():
            raise ValueError(f"小分类白话定义不能为空: {code}")
        if code in seen_codes:
            # Duplicate codes necessarily emit the same overview/subcategory paths.
            raise ValueError(f"重复输出路径: 小分类代码 {code}")
        seen_codes.add(code)
    return sorted(items, key=lambda item: item["code"])


def _manifest_item(*, path: Path, file_format: str, scope: str, big_category_code: str, **details: str) -> dict:
    return {
        "path": path.as_posix(),
        "format": file_format,
        "scope": scope,
        "big_category_code": big_category_code,
        **details,
    }


def build_manifest(taxonomy: list[dict]) -> list[dict]:
    """Return the stable 132-path DOCX/XLSX delivery plan for a taxonomy."""
    categories = _sorted_taxonomy(taxonomy)
    manifest: list[dict] = []
    big_category_codes = sorted({item["code"][:2] for item in categories})

    for big_code in big_category_codes:
        directory = Path(BIG_CATEGORY_DIRECTORIES[big_code])
        for file_format in ("docx", "xlsx"):
            manifest.append(
                _manifest_item(
                    path=DELIVERY_ROOT / directory / f"00_大分类总览.{file_format}",
                    file_format=file_format,
                    scope="overview",
                    big_category_code=big_code,
                )
            )

    for item in categories:
        code = item["code"]
        name = item["name"]
        filename_stem = f"{code}_{name}_GitHub技能调研"
        category_directory = Path(BIG_CATEGORY_DIRECTORIES[code[:2]]) / f"{code}_{name}"
        for file_format in ("docx", "xlsx"):
            manifest.append(
                _manifest_item(
                    path=DELIVERY_ROOT / category_directory / f"{filename_stem}.{file_format}",
                    file_format=file_format,
                    scope="subcategory",
                    big_category_code=code[:2],
                    subcategory_code=code,
                    subcategory_name=name,
                )
            )

    paths = [item["path"] for item in manifest]
    if len(paths) != len(set(paths)):
        raise ValueError("重复输出路径")
    return manifest


def write_manifest(manifest: list[dict], output_path: Path) -> None:
    """Write only the JSON plan; Office files are deliberately deferred to later tasks."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def group_records(records: list[dict]) -> dict[str, list[dict]]:
    """Group plain catalog rows by approved code with deterministic Skill-ID ordering."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    seen_ids: set[str] = set()
    for record in records:
        skill_id = record.get("id")
        code = record.get("subcategory_code")
        if not isinstance(skill_id, str) or not skill_id:
            raise ValueError("Skill ID不能为空")
        if skill_id in seen_ids:
            raise ValueError(f"重复 Skill ID: {skill_id}")
        if not isinstance(code, str) or not code:
            raise ValueError(f"{skill_id} 缺少小分类代码")
        if not isinstance(record.get("plain_purpose"), str) or not record["plain_purpose"].strip():
            raise ValueError(f"{skill_id} 缺少已批准的通俗主要用途")
        seen_ids.add(skill_id)
        grouped[code].append(dict(record))
    return {code: sorted(rows, key=lambda row: row["id"]) for code, rows in sorted(grouped.items())}


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", "<br>").strip()


def _subcategory_index(category: dict, records: list[dict]) -> str:
    code = category["code"]
    name = category["name"]
    lines = [
        f"# {code} {name}",
        "",
        "## 这类工具是做什么的",
        "",
        category["inclusion_focus"].strip(),
        "",
        "## 收录数量",
        "",
        f"共 {len(records)} 项 Skill。",
        "",
        "## 收录条目",
        "",
        "| 内部编号 | 中文名称 | 主要用途 | 推荐程度 | 条目链接 |",
        "|---|---|---|---|---|",
    ]
    for record in records:
        link = f"../../skills/{record['id']}_{record['name']}.md"
        lines.append(
            "| {id} | {cn} | {purpose} | {priority} | [查看]({link}) |".format(
                id=_markdown_cell(record["id"]),
                cn=_markdown_cell(record["cn"]),
                purpose=_markdown_cell(record["plain_purpose"]),
                priority=_markdown_cell(record["priority"]),
                link=link,
            )
        )
    return "\n".join(lines) + "\n"


def _navigation_block(categories: list[dict], grouped: dict[str, list[dict]]) -> str:
    lines = [
        _NAVIGATION_START,
        "## 小分类导航",
        "",
        "| 代码与名称 | 白话定义 | Skill 数量 |",
        "|---|---|---:|",
    ]
    for category in categories:
        code, name = category["code"], category["name"]
        target = f"subcategories/{code}_{name}/INDEX.md"
        lines.append(
            f"| [{code} {name}]({target}) | {_markdown_cell(category['inclusion_focus'])} | {len(grouped[code])} |"
        )
    lines.extend(["", _NAVIGATION_END])
    return "\n".join(lines)


def _update_domain_index(index_path: Path, navigation: str) -> None:
    if index_path.exists():
        original = index_path.read_text(encoding="utf-8")
    else:
        original = f"# {index_path.parent.name}\n\n## Skill 索引\n\n"

    start = original.find(_NAVIGATION_START)
    end = original.find(_NAVIGATION_END)
    if start >= 0 and end >= start:
        original = original[:start] + original[end + len(_NAVIGATION_END):]
    elif start >= 0 or end >= 0:
        raise ValueError(f"小分类导航标记不完整: {index_path}")

    insert_before = original.find("## Skill 索引")
    if insert_before < 0:
        updated = original.rstrip() + "\n\n" + navigation + "\n"
    else:
        updated = original[:insert_before].rstrip() + "\n\n" + navigation + "\n\n" + original[insert_before:]
    index_path.write_text(updated, encoding="utf-8")


def generate_knowledge_base(records: list[dict], taxonomy: list[dict], output_root: Path) -> list[Path]:
    """Write 61 plain-language subcategory indexes and update five category navigations."""
    categories = _sorted_taxonomy(taxonomy)
    taxonomy_by_code = {item["code"]: item for item in categories}
    grouped = group_records(records)
    unknown_codes = sorted(set(grouped) - set(taxonomy_by_code))
    if unknown_codes:
        raise ValueError(f"未知小分类: {unknown_codes}")
    empty_codes = sorted(set(taxonomy_by_code) - set(grouped))
    if empty_codes:
        raise ValueError(f"空小分类: {empty_codes}")

    written: list[Path] = []
    by_big_category: dict[str, list[dict]] = defaultdict(list)
    for category in categories:
        code, name = category["code"], category["name"]
        directory = output_root / BIG_CATEGORY_DIRECTORIES[code[:2]] / "subcategories" / f"{code}_{name}"
        directory.mkdir(parents=True, exist_ok=True)
        index_path = directory / "INDEX.md"
        index_path.write_text(_subcategory_index(category, grouped[code]), encoding="utf-8")
        written.append(index_path)
        by_big_category[code[:2]].append(category)

    for big_code in sorted(by_big_category):
        domain_directory = output_root / BIG_CATEGORY_DIRECTORIES[big_code]
        domain_directory.mkdir(parents=True, exist_ok=True)
        _update_domain_index(
            domain_directory / "INDEX.md",
            _navigation_block(by_big_category[big_code], grouped),
        )
    return written


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    assignment_data = _load_json(ASSIGNMENT_FILE)
    records = _load_json(PLAIN_CATALOG_FILE)
    if not isinstance(assignment_data, dict) or not isinstance(records, list):
        raise ValueError("派生数据格式错误")
    taxonomy = assignment_data.get("taxonomy")
    assignments = assignment_data.get("assignments")
    if not isinstance(taxonomy, list) or not isinstance(assignments, dict):
        raise ValueError("小分类归属表格式错误")
    record_ids = {record.get("id") for record in records}
    if set(assignments) != record_ids or len(records) != len(record_ids):
        raise ValueError("通俗目录与归属台账的 Skill ID 不一致")
    if any(record.get("subcategory_code") != assignments[record["id"]] for record in records):
        raise ValueError("通俗目录与归属台账的小分类不一致")

    manifest = build_manifest(taxonomy)
    write_manifest(manifest, MANIFEST_FILE)
    written = generate_knowledge_base(records, taxonomy, KNOWLEDGE_BASE_ROOT)
    counts = Counter(item["format"] for item in manifest)
    print(f"manifest={len(manifest)} docx={counts['docx']} xlsx={counts['xlsx']} indexes={len(written)} records={len(records)}")


if __name__ == "__main__":
    main()
