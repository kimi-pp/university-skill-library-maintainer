"""把规范候选数据转换为知识库和交付物共用的中间数据。"""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "name",
    "cn",
    "cat",
    "repo",
    "path",
    "ecosystem",
    "form",
    "tags",
    "summary",
    "detail",
    "roles",
    "scenario",
    "compat",
    "adapt",
    "deps",
    "risk",
    "verify",
    "priority",
    "related",
}


def validate_catalog(records, categories, repositories):
    """检查 ID、分类、仓库和交付字段，拒绝落选状态进入共用数据。"""
    ids = [row.get("id") for row in records]
    if len(ids) != len(set(ids)):
        raise ValueError("发现重复 ID")
    for row in records:
        missing = REQUIRED_FIELDS.difference(row)
        if missing:
            raise ValueError(f"{row.get('id', '<unknown>')} 缺少字段: {sorted(missing)}")
        if row["cat"] not in categories:
            raise ValueError(f"{row['id']} 的分类不在本轮范围")
        if row["repo"] not in repositories:
            raise ValueError(f"{row['id']} 缺少仓库元数据")
        if row["compat"] == "X":
            raise ValueError(f"{row['id']} 为落选状态，不能进入交付数据")


def records_for_category(records, category):
    """返回单一功能分类的记录，保持 ID 稳定排序。"""
    return sorted((row for row in records if row["cat"] == category), key=lambda row: row["id"])


def build_manifest(categories):
    """定义各功能分类独立的 XLSX 与 DOCX 交付物。"""
    manifest = []
    for category, name in categories.items():
        stem = f"{category}_{name}_GitHub技能调研"
        for output_format in ("xlsx", "docx"):
            manifest.append(
                {
                    "category": category,
                    "category_name": name,
                    "format": output_format,
                    "path": f"{stem}.{output_format}",
                }
            )
    return manifest


def write_research_data(output_dir, records, categories, repositories):
    """写出生成器共用的 JSON、JSONL 与交付清单。"""
    validate_catalog(records, categories, repositories)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    enriched = []
    for row in records:
        repo_meta = repositories[row["repo"]]
        item = dict(row)
        item["repo_url"] = f"https://github.com/{row['repo']}"
        item["skill_url"] = (
            f"https://github.com/{row['repo']}/blob/{repo_meta['branch']}/{row['path']}"
        )
        item["stars"] = repo_meta["stars"]
        item["repo_pushed"] = repo_meta["pushed"]
        item["license"] = repo_meta["license"]
        enriched.append(item)

    for category, category_name in categories.items():
        payload = {
            "category": category,
            "category_name": category_name,
            "records": records_for_category(enriched, category),
        }
        (output_dir / f"category_{category}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    (output_dir / "skills.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in enriched) + "\n",
        encoding="utf-8",
    )
    (output_dir / "repositories.json").write_text(
        json.dumps(repositories, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_dir / "manifest.json").write_text(
        json.dumps(build_manifest(categories), ensure_ascii=False, indent=2), encoding="utf-8"
    )
