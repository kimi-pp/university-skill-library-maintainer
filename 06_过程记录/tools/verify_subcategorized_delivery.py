"""Project-level acceptance gate for the five plain-language subcategory samples.

The verifier deliberately recomputes every reported count from primary files.  It
does not generate reports, renders, or review evidence; its only write is the
explicit JSON result requested by the command line.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple
from xml.etree import ElementTree as ET


EXPECTED_BIG_COUNTS = {"01": 20, "02": 22, "03": 31, "04": 29, "05": 55}
EXPECTED_BIG_SUBCATEGORIES = {"01": 9, "02": 9, "03": 11, "04": 12, "05": 20}
EXPECTED_SUBCATEGORY_COUNTS = {
    "01-01": 2, "01-02": 5, "01-03": 1, "01-04": 1, "01-05": 3,
    "01-06": 2, "01-07": 2, "01-08": 1, "01-09": 3,
    "02-01": 2, "02-02": 4, "02-03": 5, "02-04": 2, "02-05": 1,
    "02-06": 3, "02-07": 2, "02-08": 1, "02-09": 2,
    "03-01": 5, "03-02": 7, "03-03": 1, "03-04": 2, "03-05": 3,
    "03-06": 1, "03-07": 2, "03-08": 5, "03-09": 3, "03-10": 1,
    "03-11": 1,
    "04-01": 2, "04-02": 2, "04-03": 2, "04-04": 4, "04-05": 1,
    "04-06": 2, "04-07": 2, "04-08": 2, "04-09": 4, "04-10": 2,
    "04-11": 4, "04-12": 2,
    "05-01": 1, "05-02": 2, "05-03": 2, "05-04": 4, "05-05": 5,
    "05-06": 1, "05-07": 2, "05-08": 5, "05-09": 3, "05-10": 2,
    "05-11": 3, "05-12": 2, "05-13": 2, "05-14": 3, "05-15": 5,
    "05-16": 3, "05-17": 2, "05-18": 3, "05-19": 4, "05-20": 1,
}
BIG_DIRECTORIES = {
    "01": "01_学术写作引用与出版",
    "02": "02_文档表格演示文稿与办公自动化",
    "03": "03_文献检索与学术研究",
    "04": "04_图书馆与信息素养",
    "05": "05_编程数学数据分析和可视化",
}
BIG_CATEGORY_NAMES = {
    "01": "学术写作、引用与出版",
    "02": "文档、表格、演示文稿与办公自动化",
    "03": "文献检索与学术研究",
    "04": "图书馆与信息素养",
    "05": "编程、数学、数据分析和可视化",
}
ORIGINAL_BASENAMES = {
    "01": "01_学术写作、引用与出版_GitHub技能调研",
    "02": "02_文档、表格、演示文稿与办公自动化_GitHub技能调研",
    "03": "03_文献检索与学术研究_GitHub技能调研",
    "04": "04_图书馆与信息素养_GitHub技能调研",
    "05": "05_编程、数学、数据分析和可视化_GitHub技能调研",
}
APPROVED_TAXONOMY_SHA256 = "7365b6a36376f895b490fcfce6f1ca126309a6df349dc3b395e80282e88a7224"
APPROVED_ASSIGNMENT_SHA256 = "ca2fa005329db69b4cb07e1ffd566e0c8f773a3e9bd0ca4d8a445f9ba7633082"
APPROVED_ASSIGNMENT_ORDER_SHA256 = "379bd125818f63e3a38200f41e7c5cd9221c0c2ba68f1e14991dd2a3af4a82ce"
APPROVED_OUTPUT_CONTRACT_SHA256 = "d67e83360ffbf3c51359fa99495703245f8d59dc213f4614a06625e745039b31"
PLAIN_FIELDS = (
    "plain_purpose", "plain_outputs", "plain_audience", "plain_when_to_use",
    "plain_prerequisites", "plain_limitations", "plain_integration",
    "plain_verification",
)
KNOWN_LEGACY_TEST_EXCEPTIONS = (
    "test_artifact_generator.ArtifactGeneratorTests.test_catalog_is_valid_and_has_expected_category_counts",
    "test_artifact_generator.ArtifactGeneratorTests.test_manifest_contains_six_independent_deliverables",
)


class VisualExpectations(NamedTuple):
    docx_pages: int
    worksheets: int
    segments: int
    images: int
    batches: int


FORMAL_VISUAL_EXPECTATIONS = VisualExpectations(259, 264, 20, 543, 19)


def _reject_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"重复 JSON 键: {key}")
        result[key] = value
    return result


def load_json_strict(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except FileNotFoundError as exc:
        raise ValueError(f"缺失文件: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 无效: {path}: {exc}") from exc


def _canonical_sha(payload: object) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"无法加载验证模块: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _source_records(root: Path) -> list[dict]:
    data_dir = root / "03_候选池" / "deduplicated"
    records: list[dict] = []
    for code in EXPECTED_BIG_COUNTS:
        path = data_dir / f"category_{code}.json"
        payload = load_json_strict(path)
        if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
            raise ValueError(f"源数据格式无效: {path}")
        rows = payload["records"]
        if len(rows) != EXPECTED_BIG_COUNTS[code]:
            raise ValueError(
                f"源数据 {code} 数量错误: {len(rows)} != {EXPECTED_BIG_COUNTS[code]}"
            )
        for row in rows:
            if not isinstance(row, dict) or row.get("cat") != code:
                raise ValueError(f"源数据大分类归属错误: {row}")
        records.extend(rows)
    ids = [row.get("id") for row in records]
    duplicates = sorted(value for value, count in Counter(ids).items() if count > 1)
    if len(records) != 157 or len(set(ids)) != 157:
        raise ValueError(f"源数据必须为 157 个唯一记录；重复={duplicates}")
    return records


def verify_data_contract(root: Path) -> dict:
    """Verify immutable sources, frozen mapping, and derived plain-language facts."""
    root = root.resolve()
    source_records = _source_records(root)
    source_by_id = {row["id"]: row for row in source_records}

    assignment_path = root / "03_候选池/derived/subcategory_assignments.json"
    assignment_data = load_json_strict(assignment_path)
    if not isinstance(assignment_data, dict):
        raise ValueError("taxonomy 与小分类归属文件格式无效")
    taxonomy = assignment_data.get("taxonomy")
    assignments = assignment_data.get("assignments")
    if not isinstance(taxonomy, list) or not isinstance(assignments, dict):
        raise ValueError("taxonomy 与小分类归属格式无效")
    codes = [item.get("code") for item in taxonomy if isinstance(item, dict)]
    if len(taxonomy) != 61 or len(set(codes)) != 61:
        raise ValueError("taxonomy 必须含 61 个唯一小分类")
    if Counter(str(code)[:2] for code in codes) != Counter(EXPECTED_BIG_SUBCATEGORIES):
        raise ValueError("taxonomy 各大分类小分类数量不符")
    expected_codes = [
        f"{big}-{index:02d}"
        for big, count in EXPECTED_BIG_SUBCATEGORIES.items()
        for index in range(1, count + 1)
    ]
    if codes != expected_codes:
        raise ValueError("taxonomy 小分类代码或顺序不是批准版本")
    if any(set(item) != {"code", "name", "inclusion_focus"} or not all(item.values()) for item in taxonomy):
        raise ValueError("taxonomy 小分类字段不完整")
    if _canonical_sha(taxonomy) != APPROVED_TAXONOMY_SHA256:
        raise ValueError("taxonomy 冻结摘要不一致")

    source_ids = set(source_by_id)
    if set(assignments) != source_ids:
        raise ValueError(
            f"小分类归属不完整: 缺失={sorted(source_ids-set(assignments))} "
            f"额外={sorted(set(assignments)-source_ids)}"
        )
    taxonomy_by_code = {item["code"]: item for item in taxonomy}
    for skill_id, code in assignments.items():
        if code not in taxonomy_by_code:
            raise ValueError(f"{skill_id} 使用未知小分类 {code}")
        if source_by_id[skill_id]["cat"] != code[:2]:
            raise ValueError(f"{skill_id} 小分类归属与大分类不一致")
    if _canonical_sha(assignments) != APPROVED_ASSIGNMENT_SHA256:
        raise ValueError("小分类归属冻结摘要不一致")
    if _canonical_sha(list(assignments.items())) != APPROVED_ASSIGNMENT_ORDER_SHA256:
        raise ValueError("小分类归属顺序与冻结清单不一致")
    assignment_counts = Counter(assignments.values())
    if dict(sorted(assignment_counts.items())) != EXPECTED_SUBCATEGORY_COUNTS:
        raise ValueError("冻结小分类成员数量不一致")

    output_data = load_json_strict(root / "03_候选池/derived/plain_output_contract.json")
    if not isinstance(output_data, dict) or output_data.get("version") != 1:
        raise ValueError("逐项产出契约格式无效")
    output_contract = output_data.get("records")
    if not isinstance(output_contract, dict) or set(output_contract) != source_ids:
        raise ValueError("逐项产出契约未精确覆盖 157 个源记录")
    if _canonical_sha(output_contract) != APPROVED_OUTPUT_CONTRACT_SHA256:
        raise ValueError("逐项产出契约冻结摘要不一致")

    catalog = load_json_strict(root / "03_候选池/derived/plain_language_catalog.json")
    if not isinstance(catalog, list) or len(catalog) != 157:
        raise ValueError("通俗目录必须恰好含 157 条记录")
    catalog_ids = [row.get("id") for row in catalog if isinstance(row, dict)]
    if set(catalog_ids) != source_ids or len(set(catalog_ids)) != 157:
        raise ValueError("通俗目录 Skill ID 缺失或重复")

    pipeline = _load_module(
        "task9_subcategory_pipeline",
        Path(__file__).resolve().parent / "subcategory_pipeline.py",
    )
    fact_drift: list[str] = []
    readability: list[str] = []
    output_issues: list[str] = []
    for row in catalog:
        source = source_by_id[row["id"]]
        for field, value in source.items():
            if field not in row or row[field] != value:
                fact_drift.append(f"{row['id']}:{field}")
        code = assignments[row["id"]]
        if row.get("subcategory_code") != code:
            fact_drift.append(f"{row['id']}:subcategory_code")
        if row.get("subcategory_name") != taxonomy_by_code[code]["name"]:
            fact_drift.append(f"{row['id']}:subcategory_name")
        if any(not isinstance(row.get(field), str) or not row[field].strip() for field in PLAIN_FIELDS):
            readability.append(f"{row['id']}:通俗字段为空")
        readability.extend(pipeline.readability_issues(row))
        output_issues.extend(pipeline.output_contract_issues(row, output_contract))
    if fact_drift:
        raise ValueError(f"通俗目录发生源事实漂移: {fact_drift[:10]}")
    if readability:
        raise ValueError(f"通俗目录可读性问题: {readability[:10]}")
    if output_issues:
        raise ValueError(f"通俗目录产出事实问题: {output_issues[:10]}")
    return {
        "source_records": len(source_records),
        "subcategories": len(taxonomy),
        "big_category_records": dict(Counter(row["cat"] for row in source_records)),
        "big_category_subcategories": dict(Counter(code[:2] for code in codes)),
        "assignments": len(assignments),
        "plain_records": len(catalog),
        "fact_drift": 0,
        "readability_issues": 0,
        "taxonomy": taxonomy,
        "assignments_data": assignments,
        "decision_note_ids": sorted(assignment_data.get("decision_notes", {})),
        "catalog": catalog,
    }


def expected_manifest(taxonomy: list[dict]) -> list[dict]:
    items: list[dict] = []
    for big, directory in BIG_DIRECTORIES.items():
        base = f"05_交付物/通俗细分版_2026-08-07/{directory}"
        for suffix in ("docx", "xlsx"):
            items.append({
                "path": f"{base}/00_大分类总览.{suffix}",
                "format": suffix,
                "scope": "overview",
                "big_category_code": big,
            })
    for big, directory in BIG_DIRECTORIES.items():
        base = f"05_交付物/通俗细分版_2026-08-07/{directory}"
        for subcategory in [row for row in taxonomy if row["code"].startswith(f"{big}-")]:
            code, name = subcategory["code"], subcategory["name"]
            for suffix in ("docx", "xlsx"):
                items.append({
                    "path": f"{base}/{code}_{name}/{code}_{name}_GitHub技能调研.{suffix}",
                    "format": suffix,
                    "scope": "subcategory",
                    "big_category_code": big,
                    "subcategory_code": code,
                    "subcategory_name": name,
                })
    return items


def verify_manifest_and_delivery(root: Path, taxonomy: list[dict]) -> dict:
    root = root.resolve()
    manifest = load_json_strict(root / "03_候选池/derived/subcategory_manifest.json")
    expected = expected_manifest(taxonomy)
    if not isinstance(manifest, list) or manifest != expected or len(manifest) != 132:
        raise ValueError("manifest 不是批准的 132 文件精确清单")
    paths = [item["path"] for item in manifest]
    if len(set(paths)) != 132:
        raise ValueError("manifest 含重复交付路径")
    pairs = defaultdict(set)
    for item in manifest:
        key = item.get("subcategory_code", f"{item['big_category_code']}-overview")
        pairs[key].add(item["format"])
    if len(pairs) != 66 or any(formats != {"docx", "xlsx"} for formats in pairs.values()):
        raise ValueError("manifest 必须为 66 组 DOCX/XLSX 精确配对")
    expected_paths = {(root / Path(*path.split("/"))).resolve() for path in paths}
    delivery_root = root / "05_交付物/通俗细分版_2026-08-07"
    actual_paths = {path.resolve() for path in delivery_root.rglob("*") if path.is_file()}
    missing = sorted(path.name for path in expected_paths - actual_paths)
    extra = sorted(path.name for path in actual_paths - expected_paths)
    if missing or extra:
        raise ValueError(f"交付文件集合与 manifest 不一致: 缺失={missing} 额外={extra}")
    empty = sorted(path.name for path in expected_paths if path.stat().st_size == 0)
    if empty:
        raise ValueError(f"交付中存在空文件: {empty}")
    expected_directories: set[Path] = set()
    for path in expected_paths:
        parent = path.parent
        while parent != delivery_root.resolve():
            expected_directories.add(parent)
            parent = parent.parent
    actual_directories = {path.resolve() for path in delivery_root.rglob("*") if path.is_dir()}
    missing_directories = sorted(path.name for path in expected_directories - actual_directories)
    extra_directories = sorted(path.name for path in actual_directories - expected_directories)
    if missing_directories or extra_directories:
        raise ValueError(
            f"交付目录树与 manifest 不一致: 缺失={missing_directories} 额外={extra_directories}"
        )
    residue = sorted(
        path.name for path in delivery_root.rglob("*")
        if path.name.endswith((".tmp", ".part", ".bak")) or path.name.startswith(("~$", ".~"))
    )
    if residue:
        raise ValueError(f"交付目录存在事务残留: {residue}")
    return {
        "manifest": manifest,
        "delivery_files": len(actual_paths),
        "document_files": sum(item["format"] == "docx" for item in manifest),
        "spreadsheet_files": sum(item["format"] == "xlsx" for item in manifest),
        "artifact_pairs": len(pairs),
    }


def verify_originals_and_archive(root: Path) -> dict:
    root = root.resolve()
    delivery = root / "05_交付物"
    archive = delivery / "原始版_2026-08-06"
    approved_names = {
        f"{basename}.{suffix}"
        for basename in ORIGINAL_BASENAMES.values()
        for suffix in ("docx", "xlsx")
    }
    originals = sorted(path for path in delivery.iterdir() if path.is_file() and path.name in approved_names)
    archived = sorted(path for path in archive.iterdir() if path.is_file()) if archive.is_dir() else []
    if {path.name for path in originals} != approved_names:
        raise ValueError("原位置五类报告不符合 10 个批准文件名")
    if {path.name for path in archived} != approved_names:
        raise ValueError("原始版归档文件集合必须精确对应 10 个批准文件名")
    for original in originals:
        copy = archive / original.name
        if original.stat().st_size != copy.stat().st_size or _file_sha(original) != _file_sha(copy):
            raise ValueError(f"原始版归档 SHA 不一致: {original.name}")
    pilot_names = {f"0809_计算机类_跨平台技能调研.{suffix}" for suffix in ("docx", "xlsx")}
    pilots = [delivery / name for name in pilot_names]
    if any(not path.is_file() or path.stat().st_size == 0 for path in pilots):
        raise ValueError("0809 计算机类交付对缺失或为空")
    if pilot_names & {path.name for path in archived}:
        raise ValueError("0809 文件不得进入五类原始版归档")
    return {"originals": len(originals), "archived": len(archived), "pilot_files": len(pilots)}


_MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
_REFERENCE_DEFINITION_RE = re.compile(
    r"(?m)^ {0,3}\[([^\]\n]+)\]:\s*(<[^>]+>|\S+)"
)
_REFERENCE_USAGE_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\[([^\]\n]*)\]")
_IMAGE_REFERENCE_USAGE_RE = re.compile(r"!\[([^\]\n]*)\]\[([^\]\n]*)\]")
_SHORTCUT_REFERENCE_RE = re.compile(r"(?<!!)(?<!\])\[([^\]\n]+)\](?![\[\(:])")
_INTERNAL_MARKDOWN_PARTS = frozenset({".git", ".superpowers", ".worktrees"})


def _inside_nested_repository(root: Path, path: Path) -> bool:
    for parent in path.parents:
        if parent == root:
            return False
        if (parent / ".git").exists():
            return True
    return False


def _reference_label(value: str) -> str:
    return " ".join(value.strip().casefold().split())


def _check_markdown_target(root: Path, page: Path, raw: str) -> bool:
    raw = raw.strip()
    if raw.startswith("<") and raw.endswith(">"):
        target = raw[1:-1]
    else:
        if any(character.isspace() for character in raw):
            raise ValueError(f"CommonMark 链接目标含未包裹空格: {page}: {raw}")
        target = raw
    if re.match(r"^(?:https?|mailto):", target, re.IGNORECASE) or target.startswith("#"):
        return False
    decoded = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not decoded:
        return False
    candidate = (page.parent / Path(decoded)).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"CommonMark 链接越出项目目录: {page}: {target}")
    if not candidate.exists():
        raise ValueError(f"Markdown 坏链: {page}: {target}")
    return True


def verify_markdown_links(root: Path, paths: list[Path]) -> dict:
    root = root.resolve()
    checked = 0
    local = 0
    for page in paths:
        text = page.read_text(encoding="utf-8")
        definitions: dict[str, str] = {}
        for definition in _REFERENCE_DEFINITION_RE.finditer(text):
            definitions.setdefault(_reference_label(definition.group(1)), definition.group(2))
        for match in _MARKDOWN_LINK_RE.finditer(text):
            checked += 1
            local += int(_check_markdown_target(root, page, match.group(1)))
        for pattern in (_REFERENCE_USAGE_RE, _IMAGE_REFERENCE_USAGE_RE):
            for usage in pattern.finditer(text):
                label = _reference_label(usage.group(2) or usage.group(1))
                if label not in definitions:
                    raise ValueError(f"Markdown 引用式链接缺少定义: {page}: {label}")
                checked += 1
                local += int(_check_markdown_target(root, page, definitions[label]))
        for usage in _SHORTCUT_REFERENCE_RE.finditer(text):
            label = _reference_label(usage.group(1))
            if label in definitions:
                checked += 1
                local += int(_check_markdown_target(root, page, definitions[label]))
    return {"markdown_files": len(paths), "links": checked, "local_links": local}


def _tracked_markdown(root: Path) -> list[Path]:
    root = root.resolve()
    discovered: set[Path] = set()
    for path in root.rglob("*.md"):
        relative_parts = path.relative_to(root).parts
        if any(part in _INTERNAL_MARKDOWN_PARTS for part in relative_parts):
            continue
        resolved = path.resolve()
        if (resolved == root or root in resolved.parents) and not _inside_nested_repository(root, resolved):
            discovered.add(resolved)
    try:
        result = subprocess.run(
            ["git", "-c", "core.quotepath=false", "ls-files", "-z", "--", "*.md"],
            cwd=root, check=True, capture_output=True,
        )
        names = [name for name in result.stdout.decode("utf-8").split("\0") if name]
        for name in names:
            if any(part in _INTERNAL_MARKDOWN_PARTS for part in Path(name).parts):
                continue
            resolved = (root / Path(name)).resolve()
            if (resolved == root or root in resolved.parents) and not _inside_nested_repository(root, resolved):
                discovered.add(resolved)
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        pass
    return sorted(discovered)


def _marked_block(text: str, start: str, end: str, *, source: Path) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"导航标记缺失或重复: {source}")
    start_at = text.index(start)
    end_at = text.index(end, start_at) + len(end)
    return text[start_at:end_at]


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", "<br>").strip()


def _markdown_link(label: str, target: str) -> str:
    return f"[{label}](<{target}>)"


def _expected_leaf_page(category: dict, records: list[dict]) -> str:
    code, name = category["code"], category["name"]
    lines = [
        f"# {code} {name}", "", "## 这类工具是做什么的", "",
        category["inclusion_focus"].strip(), "", "## 收录数量", "",
        f"共 {len(records)} 项 Skill。", "", "## 收录条目", "",
        "| 内部编号 | 中文名称 | 主要用途 | 推荐程度 | 条目链接 |",
        "|---|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            "| {id} | {cn} | {purpose} | {priority} | {link} |".format(
                id=_markdown_cell(record["id"]),
                cn=_markdown_cell(record["cn"]),
                purpose=_markdown_cell(record["plain_purpose"]),
                priority=_markdown_cell(record["priority"]),
                link=_markdown_link(
                    "查看", f"../../skills/{record['id']}_{record['name']}.md"
                ),
            )
        )
    return "\n".join(lines) + "\n"


def _manifest_views(manifest: list[dict]) -> tuple[dict, dict]:
    leaves: dict[str, dict[str, str]] = defaultdict(dict)
    overviews: dict[str, dict[str, str]] = defaultdict(dict)
    for item in manifest:
        if item["scope"] == "subcategory":
            leaves[item["subcategory_code"]][item["format"]] = item["path"]
        elif item["scope"] == "overview":
            overviews[item["big_category_code"]][item["format"]] = item["path"]
    return dict(leaves), dict(overviews)


def _expected_domain_navigation(
    categories: list[dict], grouped: dict[str, list[dict]], leaf_paths: dict
) -> str:
    lines = [
        "<!-- SUBCATEGORY_NAVIGATION_START -->", "## 小分类导航", "",
        "| 小分类代码 | 小分类名称 | 成员数 | 知识库 | Word | Excel |",
        "|---|---|---:|---|---|---|",
    ]
    for category in categories:
        code, name = category["code"], category["name"]
        delivery = leaf_paths.get(code, {})
        if set(delivery) != {"docx", "xlsx"}:
            raise ValueError(f"{code} 的 Word/XLSX 导航配对不完整")
        lines.append(
            "| {code} | {name} | {count} | {kb} | {word} | {excel} |".format(
                code=code,
                name=name,
                count=len(grouped[code]),
                kb=_markdown_link("进入", f"subcategories/{code}_{name}/INDEX.md"),
                word=_markdown_link("打开", f"../../../{delivery['docx']}"),
                excel=_markdown_link("打开", f"../../../{delivery['xlsx']}"),
            )
        )
    return "\n".join(lines + ["", "<!-- SUBCATEGORY_NAVIGATION_END -->"])


def _expected_total_navigation(
    categories: list[dict], grouped: dict[str, list[dict]], manifest: list[dict], overviews: dict
) -> str:
    format_counts = Counter(item["format"] for item in manifest)
    record_count = sum(len(rows) for rows in grouped.values())
    lines = [
        "<!-- SUBCATEGORY_OVERVIEW_START -->",
        "## 通俗细分版（五类样板）", "",
        f"本轮从 13 个通用大分类中选择已完成调研的五类先做样板，只按任务用途细分，不涉及专业或学科分类。{record_count} 项 Skill 已唯一归入 {len(categories)} 个小分类；每项只有一个主小分类，跨用途能力继续用辅助标签说明。",
        "",
        f"最终通俗细分版共有 {len(manifest)} 个文件，包括 {format_counts['docx']} 份 Word 和 {format_counts['xlsx']} 份 Excel。原始五类 Word 与 Excel 报告仍保留在原位置，并另存一份原样副本。候选 Skill 本次只核对说明或包内容，未安装、未运行。",
        "",
        f"- {_markdown_link('通俗细分版交付目录', '../05_交付物/通俗细分版_2026-08-07/')}",
        f"- {_markdown_link('原始版存档', '../05_交付物/原始版_2026-08-06/')}",
        "", "### 五个大类入口", "",
        "| 大分类 | Skill 数 | 小分类数 | 大类导航 | Word 概览 | Excel 概览 |",
        "|---|---:|---:|---|---|---|",
    ]
    for big, directory in BIG_DIRECTORIES.items():
        overview = overviews.get(big, {})
        if set(overview) != {"docx", "xlsx"}:
            raise ValueError(f"{big} 的 Word/XLSX 概览配对不完整")
        big_categories = [item for item in categories if item["code"].startswith(f"{big}-")]
        lines.append(
            "| {category} | {skills} | {subcategories} | {navigation} | {word} | {excel} |".format(
                category=f"{big} {BIG_CATEGORY_NAMES[big]}",
                skills=sum(len(grouped[item["code"]]) for item in big_categories),
                subcategories=len(big_categories),
                navigation=_markdown_link(
                    "进入", f"../02_知识库/functional_domains/{directory}/INDEX.md"
                ),
                word=_markdown_link("打开", f"../{overview['docx']}"),
                excel=_markdown_link("打开", f"../{overview['xlsx']}"),
            )
        )
    lines.extend([
        "", f"### {len(categories)} 个小分类知识库入口", "",
        "| 小分类代码 | 小分类名称 | 知识库入口 |", "|---|---|---|",
    ])
    for category in categories:
        code, name = category["code"], category["name"]
        lines.append(
            f"| {code} | {name} | "
            + _markdown_link(
                "进入",
                f"../02_知识库/functional_domains/{BIG_DIRECTORIES[code[:2]]}/subcategories/{code}_{name}/INDEX.md",
            )
            + " |"
        )
    return "\n".join(lines + ["", "<!-- SUBCATEGORY_OVERVIEW_END -->"])


def verify_navigation(
    root: Path,
    taxonomy: list[dict],
    assignments: dict[str, str],
    *,
    catalog: list[dict],
    manifest: list[dict],
) -> dict:
    functional = root / "02_知识库/functional_domains"
    domain_indexes = [functional / directory / "INDEX.md" for directory in BIG_DIRECTORIES.values()]
    leaf_indexes: list[Path] = []
    for item in taxonomy:
        directory = BIG_DIRECTORIES[item["code"][:2]]
        leaf_indexes.append(
            functional / directory / "subcategories" / f"{item['code']}_{item['name']}" / "INDEX.md"
        )
    if len(leaf_indexes) != 61 or any(not path.is_file() for path in leaf_indexes):
        raise ValueError("知识库必须含 61 个小分类页面")
    if any(not path.is_file() for path in domain_indexes):
        raise ValueError("五个大分类导航页不完整")
    total_index = root / "00_索引/INDEX.md"
    if not total_index.is_file():
        raise ValueError("总索引缺失")
    categories = sorted((dict(item) for item in taxonomy), key=lambda item: item["code"])
    grouped: dict[str, list[dict]] = defaultdict(list)
    seen_ids: set[str] = set()
    for record in catalog:
        if record["id"] in seen_ids:
            raise ValueError(f"知识库目录含重复 ID: {record['id']}")
        seen_ids.add(record["id"])
        grouped[record["subcategory_code"]].append(record)
    grouped = {code: sorted(rows, key=lambda row: row["id"]) for code, rows in grouped.items()}
    if set(grouped) != {item["code"] for item in categories}:
        raise ValueError("知识库分组未精确覆盖 taxonomy")
    leaf_paths, overview_paths = _manifest_views(manifest)
    for item, path in zip(categories, leaf_indexes):
        expected_text = _expected_leaf_page(item, grouped[item["code"]])
        if path.read_text(encoding="utf-8") != expected_text:
            raise ValueError(f"{item['code']} 知识库页面逐行不一致")
        expected_ids = sorted(skill_id for skill_id, code in assignments.items() if code == item["code"])
        if [row["id"] for row in grouped[item["code"]]] != expected_ids:
            raise ValueError(f"{item['code']} 知识库成员与冻结归属不一致")
    for big, path in zip(BIG_DIRECTORIES, domain_indexes):
        expected_block = _expected_domain_navigation(
            [item for item in categories if item["code"].startswith(f"{big}-")],
            grouped,
            leaf_paths,
        )
        actual_block = _marked_block(
            path.read_text(encoding="utf-8"),
            "<!-- SUBCATEGORY_NAVIGATION_START -->",
            "<!-- SUBCATEGORY_NAVIGATION_END -->",
            source=path,
        )
        if actual_block != expected_block:
            raise ValueError(f"{big} 大分类导航逐行不一致")
    total_text = total_index.read_text(encoding="utf-8")
    expected_total = _expected_total_navigation(
        categories, grouped, manifest, overview_paths
    )
    actual_total = _marked_block(
        total_text,
        "<!-- SUBCATEGORY_OVERVIEW_START -->",
        "<!-- SUBCATEGORY_OVERVIEW_END -->",
        source=total_index,
    )
    if actual_total != expected_total:
        raise ValueError("总索引五类与 61 小分类导航逐行不一致")
    links = verify_markdown_links(root, _tracked_markdown(root))
    return {"leaf_pages": len(leaf_indexes), "domain_indexes": len(domain_indexes), "total_indexes": 1, **links}


def load_visual_module(root: Path):
    module = _load_module(
        f"task9_visual_{hash(root.resolve()) & 0xffffffff:x}",
        Path(__file__).resolve().parent / "make_subcategorized_contact_sheets.py",
    )
    module.PROJECT_ROOT = root.resolve()
    return module


def verify_visual_evidence(
    root: Path,
    manifest: list[dict],
    catalog: list[dict],
    expectations: VisualExpectations = FORMAL_VISUAL_EXPECTATIONS,
) -> dict:
    root = root.resolve()
    visual = load_visual_module(root)
    visual.validate_delivery_tree(root, manifest)
    docx = visual.collect_docx_render_inventory(
        root / "06_过程记录/renders/subcategorized_docx", manifest
    )
    xlsx = visual.collect_xlsx_render_inventory(
        root / "06_过程记录/renders/subcategorized_xlsx",
        manifest,
        required_segment_keys=visual.required_segment_keys(catalog),
    )
    worksheets = sum(row.get("render_kind") == "worksheet" for row in xlsx)
    segments = sum(row.get("render_kind") == "segment" for row in xlsx)
    observed = (len(docx), worksheets, segments, len(docx) + len(xlsx))
    expected = (
        expectations.docx_pages, expectations.worksheets,
        expectations.segments, expectations.images,
    )
    if observed != expected:
        raise ValueError(f"渲染图数量与预期集合不一致: observed={observed} expected={expected}")
    recomputed_inventory = visual.build_inventory_document(docx + xlsx)
    inventory_path = root / "06_过程记录/visual_review/task-7-inventory.json"
    stored_inventory = load_json_strict(inventory_path)
    if stored_inventory != recomputed_inventory:
        raise ValueError("库存 inventory digest/hash/尺寸与原始渲染图不一致")
    review_path = root / "06_过程记录/visual_review/task-7-review-log.jsonl"
    review_records = visual.load_review_log(review_path)
    recomputed_finalized = visual.finalize_review_inventory(
        root, stored_inventory, review_records, review_log_sha256=_file_sha(review_path)
    )
    stored_finalized = load_json_strict(
        root / "06_过程记录/visual_review/task-7-finalized.json"
    )
    if stored_finalized != recomputed_finalized:
        raise ValueError("finalized 完成声明与库存或 review log 不一致")
    summary = recomputed_finalized.get("summary", {})
    if (
        summary.get("images") != expectations.images
        or summary.get("batches") != expectations.batches
        or summary.get("pass") != expectations.images
        or summary.get("nonpass") != 0
        or recomputed_finalized.get("review_complete") is not True
    ):
        raise ValueError(f"人工复核完成计数不符: {summary}")
    return {
        "docx_pages": len(docx), "worksheets": worksheets, "segments": segments,
        "review_images": summary["images"], "review_batches": summary["batches"],
        "review_pass": summary["pass"], "review_nonpass": summary["nonpass"],
        "inventory_digest": recomputed_inventory["inventory_digest"],
    }


_PLACEHOLDER_RE = re.compile(
    r"(?i)(?:\bTODO\b|\bTBD\b|\bFIXME\b|\bPLACEHOLDER\b|\bTEMPLATE\b|待填|占位文本|模板占位|模板标记|示例模板)"
)
_INTERNAL_RE = re.compile(
    r"(?i)(?:(?<![A-Za-z])[A-Za-z]:\\|/Users/|/home/|/tmp/|\.codex|\.superpowers|06_过程记录[/\\]tools[/\\]"
    r"|verify_subcategorized_|build_subcategorized_|render_subcategorized_)"
)
_SUCCESS_RE = re.compile(
    r"(?:已经|已)(?:完成)?(?:安装|运行|部署|验证成功|验证可用|证明有效|通过实际测试)"
    r"|(?:安装|运行)(?:已经|已)?成功"
    r"|经验证(?:可以|可)?正常使用|测试通过(?:可以|可)?正常运行"
)
_NEGATION_RE = re.compile(
    r"(?:未|没有|尚未|不曾)(?:进行|完成)?(?:安装|运行|部署|实际测试)"
    r"|(?:不代表|不等于|不得|不能|不可)[^。；\n]{0,30}(?:安装|运行|部署|验证成功|验证可用|证明有效|实际测试)"
    r"|不把[^。；\n]{0,40}(?:写成|视为)(?:已|已经)(?:安装|运行|部署)"
    r"|(?:没有|未|不曾)(?:被)?(?:写成|视为)(?:已|已经)(?:安装|运行|部署|验证可用|证明有效)"
)
_DISCIPLINE_RE = re.compile(r"(?:按照|依照|基于|采用|属于|细分)(?:专业或)?学科分类|学科分类(?:建立|划分|细分|作为)")
_DISCIPLINE_NEGATION_RE = re.compile(r"(?:不涉及|不是|不采用|未按|不按|不细分|不用于细分)(?:专业或)?学科分类")


def text_quality_issues(text: str, *, source: str) -> list[str]:
    issues: list[str] = []
    clauses = [
        clause.strip()
        for clause in re.split(
            r"[\n。；;！？|，,]+|(?<!不)但(?:是)?|然而|不过",
            str(text),
        )
        if clause.strip()
    ]
    for clause_number, clause in enumerate(clauses, 1):
        if _PLACEHOLDER_RE.search(clause):
            issues.append(f"{source}:分句{clause_number}:占位或模板标记")
        if _INTERNAL_RE.search(clause):
            issues.append(f"{source}:分句{clause_number}:内部或临时路径/脚本名")
        if _SUCCESS_RE.search(clause) and not _NEGATION_RE.search(clause):
            issues.append(f"{source}:分句{clause_number}:把静态核验夸大为安装或运行成功")
        if _DISCIPLINE_RE.search(clause) and not _DISCIPLINE_NEGATION_RE.search(clause):
            issues.append(f"{source}:分句{clause_number}:误述为学科分类")
    return issues


def _docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        parts: list[str] = []
        for name in archive.namelist():
            if not re.match(r"word/(?:document|header\d+|footer\d+)\.xml$", name):
                continue
            root = ET.fromstring(archive.read(name))
            for paragraph in (node for node in root.iter() if node.tag.endswith("}p")):
                text = "".join(
                    node.text or "" for node in paragraph.iter() if node.tag.endswith("}t")
                )
                if text:
                    parts.append(text)
        return "\n".join(parts)


def _xlsx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in (node for node in root.iter() if node.tag.endswith("}si")):
                shared.append(
                    "".join(node.text or "" for node in item.iter() if node.tag.endswith("}t"))
                )
        parts: list[str] = []
        for name in sorted(archive.namelist()):
            if not re.match(r"xl/worksheets/sheet\d+\.xml$", name):
                continue
            root = ET.fromstring(archive.read(name))
            for cell in (node for node in root.iter() if node.tag.endswith("}c")):
                cell_type = cell.get("t")
                if cell_type == "inlineStr":
                    value = "".join(
                        node.text or "" for node in cell.iter() if node.tag.endswith("}t")
                    )
                else:
                    value_node = next(
                        (node for node in cell if node.tag.endswith("}v")), None
                    )
                    value = value_node.text if value_node is not None and value_node.text else ""
                    if cell_type == "s" and value:
                        try:
                            value = shared[int(value)]
                        except (ValueError, IndexError) as exc:
                            raise ValueError(f"XLSX shared string 索引无效: {path}") from exc
                if value:
                    parts.append(value)
        return "\n".join(parts)


def _all_string_values(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _all_string_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _all_string_values(item)


def verify_visible_text(root: Path, manifest: list[dict], catalog: list[dict]) -> dict:
    checked = 0
    issues: list[str] = []
    functional = root / "02_知识库/functional_domains"
    markdown_paths = [
        root / "00_索引/INDEX.md",
        root / "01_规则/TAXONOMY.md",
        root / "01_规则/DATA_DICTIONARY.md",
        root / "01_规则/REPORTING_STANDARD.md",
        root / "06_过程记录/DECISION_LOG.md",
        root / "06_过程记录/RESEARCH_LOG.md",
    ]
    markdown_paths.extend(functional / directory / "INDEX.md" for directory in BIG_DIRECTORIES.values())
    markdown_paths.extend(
        path
        for directory in BIG_DIRECTORIES.values()
        for path in sorted((functional / directory / "subcategories").glob("*/INDEX.md"))
    )
    skill_paths = [
        path
        for directory in BIG_DIRECTORIES.values()
        for path in sorted((functional / directory / "skills").glob("*.md"))
    ]
    if len(skill_paths) != 157:
        raise ValueError(f"用户可见 Skill Markdown 范围不完整: {len(skill_paths)} != 157")
    markdown_paths.extend(skill_paths)
    if len(markdown_paths) != 229 or any(not path.is_file() for path in markdown_paths):
        raise ValueError("用户可见 Markdown 终检范围不完整（预期 229 份）")
    for path in markdown_paths:
        checked += 1
        issues.extend(text_quality_issues(path.read_text(encoding="utf-8"), source=path.relative_to(root).as_posix()))
    for row in catalog:
        checked += 1
        text = "\n".join(_all_string_values(row))
        issues.extend(text_quality_issues(text, source=f"plain:{row['id']}"))
    for item in manifest:
        path = root / Path(*item["path"].split("/"))
        checked += 1
        text = _docx_text(path) if item["format"] == "docx" else _xlsx_text(path)
        issues.extend(text_quality_issues(text, source=item["path"]))
    if issues:
        raise ValueError(f"可见文本风险扫描失败（{len(issues)} 项）: {issues[:20]}")
    return {"text_sources": checked, "text_issues": 0}


def verify_office_structure(
    root: Path, catalog: list[dict], taxonomy: list[dict], assignments: dict, manifest: list[dict]
) -> dict:
    tools_dir = root / "06_过程记录/tools"
    documents = _load_module("task9_document_verifier", tools_dir / "verify_subcategorized_documents.py")
    repositories = load_json_strict(root / "03_候选池/deduplicated/repositories.json")
    results = documents.verify_selected_documents(
        catalog, manifest, root, taxonomy=taxonomy, assignments=assignments,
        repositories=repositories, expected_total=157, source_project_root=root,
    )
    failed = {key: value for key, value in results.items() if value}
    if len(results) != 66 or failed:
        raise ValueError(f"DOCX 结构验收失败: verified={len(results)} issues={failed}")
    node = shutil.which("node")
    if node is None:
        raise ValueError("XLSX 结构验收所需 Node.js 不可用")
    env = os.environ.copy()
    env["SUBCATEGORY_OUTPUT_ROOT"] = str(root)
    completed = subprocess.run(
        [node, str(tools_dir / "verify_subcategorized_spreadsheets.mjs")],
        cwd=root, env=env, text=True, encoding="utf-8", errors="replace",
        capture_output=True,
    )
    output = (completed.stdout + "\n" + completed.stderr).strip()
    if completed.returncode != 0 or not re.search(r"xlsx=66\s+sheets=264", output):
        raise ValueError(f"XLSX 结构验收失败: {output}")
    return {"docx_verified": len(results), "xlsx_verified": 66, "worksheets_verified": 264}


def semantic_result_digest(payload: dict) -> str:
    stable = dict(payload)
    stable.pop("checked_at", None)
    stable.pop("semantic_digest", None)
    return _canonical_sha(stable)


def _public_summary(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: _public_summary(item)
            for key, item in value.items()
            if key not in {"taxonomy", "assignments_data", "catalog", "manifest"}
        }
    if isinstance(value, list):
        return [_public_summary(item) for item in value]
    return value


def _manual_review_payload(data: dict | None) -> dict:
    if not data:
        return {
            "category_spot_check_ids": {},
            "decision_boundary_ids": [],
            "technical_term_checks": [],
            "boundary": "数据门禁失败，无法形成有效人工抽查清单。",
        }
    catalog = data["catalog"]
    category_spots: dict[str, list[str]] = {}
    for big in EXPECTED_BIG_COUNTS:
        ids = sorted(row["id"] for row in catalog if row["cat"] == big)
        category_spots[big] = [ids[0], ids[-1]]
    technical_terms = ("API", "CLI", "JSON", "DOI", "GPU", "SQL", "UMAP", "PRISMA", "BibTeX", "LaTeX")
    term_checks: list[dict] = []
    for term in technical_terms:
        source = next(
            (
                row["id"]
                for row in catalog
                if any(term in value for value in _all_string_values(row))
            ),
            None,
        )
        if source:
            term_checks.append(
                {
                    "term": term,
                    "source_id": source,
                    "human_question": "首次出现处的中文解释是否足以让非技术读者理解，且没有改变原事实？",
                }
            )
    return {
        "category_spot_check_ids": category_spots,
        "decision_boundary_ids": data["decision_note_ids"],
        "technical_term_checks": term_checks,
        "boundary": "自动检查可核对结构、事实锚点、已管理术语和已知风险措辞；术语解释对不同读者是否足够自然仍需按本清单人工抽查。",
    }


def verify_project(root: Path) -> dict:
    root = root.resolve()
    gates: dict[str, dict] = {}
    state: dict[str, object] = {}

    def run_gate(name: str, action):
        try:
            result = action()
            state[name] = result
            gates[name] = {"status": "pass", "summary": _public_summary(result)}
            return result
        except Exception as exc:  # aggregate all independently inspectable gates
            gates[name] = {"status": "fail", "errors": [f"{type(exc).__name__}: {exc}"]}
            return None

    data = run_gate("data_contract", lambda: verify_data_contract(root))
    if data:
        delivery = run_gate(
            "manifest_delivery", lambda: verify_manifest_and_delivery(root, data["taxonomy"])
        )
        run_gate("original_archive", lambda: verify_originals_and_archive(root))
        if delivery:
            run_gate(
                "navigation_links",
                lambda: verify_navigation(
                    root,
                    data["taxonomy"],
                    data["assignments_data"],
                    catalog=data["catalog"],
                    manifest=delivery["manifest"],
                ),
            )
            run_gate(
                "office_structure",
                lambda: verify_office_structure(
                    root, data["catalog"], data["taxonomy"], data["assignments_data"], delivery["manifest"]
                ),
            )
            run_gate(
                "visual_evidence",
                lambda: verify_visual_evidence(root, delivery["manifest"], data["catalog"]),
            )
            run_gate(
                "visible_text",
                lambda: verify_visible_text(root, delivery["manifest"], data["catalog"]),
            )
    complete = bool(gates) and all(item["status"] == "pass" for item in gates.values())
    counts = {
        "source_records": data["source_records"] if data else None,
        "subcategories": data["subcategories"] if data else None,
        "delivery_files": state.get("manifest_delivery", {}).get("delivery_files") if isinstance(state.get("manifest_delivery"), dict) else None,
        "docx_files": state.get("manifest_delivery", {}).get("document_files") if isinstance(state.get("manifest_delivery"), dict) else None,
        "xlsx_files": state.get("manifest_delivery", {}).get("spreadsheet_files") if isinstance(state.get("manifest_delivery"), dict) else None,
        "archived_originals": state.get("original_archive", {}).get("archived") if isinstance(state.get("original_archive"), dict) else None,
        "docx_pages": state.get("visual_evidence", {}).get("docx_pages") if isinstance(state.get("visual_evidence"), dict) else None,
        "worksheets": state.get("visual_evidence", {}).get("worksheets") if isinstance(state.get("visual_evidence"), dict) else None,
        "overview_segments": state.get("visual_evidence", {}).get("segments") if isinstance(state.get("visual_evidence"), dict) else None,
        "review_images": state.get("visual_evidence", {}).get("review_images") if isinstance(state.get("visual_evidence"), dict) else None,
        "review_batches": state.get("visual_evidence", {}).get("review_batches") if isinstance(state.get("visual_evidence"), dict) else None,
    }
    result = {
        "version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "complete": complete,
        "counts": counts,
        "gates": gates,
        "known_legacy_test_exceptions": list(KNOWN_LEGACY_TEST_EXCEPTIONS),
        "manual_review": _manual_review_payload(data),
    }
    result["semantic_digest"] = semantic_result_digest(result)
    return result


def validated_output_path(root: Path, requested: Path | None) -> Path:
    root = root.resolve()
    expected = (root / "06_过程记录/verification/subcategorized_delivery_verification.json").resolve()
    if requested is None:
        return expected
    candidate = requested if requested.is_absolute() else root / requested
    candidate = candidate.resolve()
    if candidate != expected:
        raise ValueError(f"验收结果输出仅允许写入受控 JSON: {expected}")
    return candidate


def _write_result_atomic(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.task9.tmp")
    try:
        temporary.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    try:
        output = validated_output_path(root, args.output)
    except ValueError as exc:
        parser.error(str(exc))
    result = verify_project(root)
    _write_result_atomic(output, result)
    print(
        f"complete={str(result['complete']).lower()} "
        f"counts={json.dumps(result['counts'], ensure_ascii=False, sort_keys=True)} "
        f"result={output}"
    )
    if not result["complete"]:
        for name, gate in result["gates"].items():
            if gate["status"] == "fail":
                print(f"FAIL {name}: {'; '.join(gate['errors'])}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
