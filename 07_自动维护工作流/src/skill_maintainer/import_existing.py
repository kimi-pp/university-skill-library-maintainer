"""保守地清点历史交付物，并在可对账时写入 Excel 主台账。"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Mapping
from zipfile import BadZipFile, ZipFile

from .ledger import validate_current_skill_row
from .ledger_schema import CURRENT_SKILL_COLUMNS, CURRENT_SKILL_OPTIONAL_COLUMNS

if TYPE_CHECKING:
    from .ledger import LedgerStore


HEADER_ALIASES = {
    "内部标识": {"内部标识", "内部编号", "Skill ID", "stable_id", "skill_id"},
    "Skill名称": {"Skill名称", "原始名称", "name"},
    "来源地址": {"来源地址", "Skill地址", "canonical_url", "GitHub仓库地址"},
    "固定版本": {"固定版本", "审查版本", "fixed_version"},
}

_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_DOCX = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_PACKAGE_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
_API_COMBINED = "API 或外部服务"


@dataclass(frozen=True)
class ImportedRecord:
    source_path: Path
    source_row: int
    values: Mapping[str, str]

    @property
    def canonical_source(self) -> str:
        return _first(self.values, "Canonical source", "来源地址")

    @property
    def skill_name(self) -> str:
        return _first(self.values, "Skill名称")


@dataclass(frozen=True)
class WordUncertainty:
    source_path: Path
    reason: str


@dataclass(frozen=True)
class ImportInventory:
    root: Path
    records: tuple[ImportedRecord, ...]
    source_hashes: dict[Path, str]
    excel_files: tuple[Path, ...]
    word_files: tuple[Path, ...]
    excel_skill_count: int
    word_skill_count: int
    duplicate_group_count: int
    ambiguous_record_count: int
    word_excel_count_mismatch: bool
    word_uncertainties: tuple[WordUncertainty, ...] = ()

    @property
    def word_uncertainty_count(self) -> int:
        return len(self.word_uncertainties)


@dataclass(frozen=True)
class ImportSummary:
    output: Path
    written: bool
    current_skill_count: int
    source_alias_count: int
    candidate_observation_count: int
    stable_ids: tuple[str, ...]


def scan_existing_deliveries(root: Path) -> ImportInventory:
    """只读扫描 ``05_交付物``；不改变源文件、暂存台账或主台账。"""
    resolved = Path(root).resolve()
    source_hashes: dict[Path, str] = {}
    excel_files = tuple(sorted(resolved.rglob("*.xlsx")))
    word_files = tuple(sorted(resolved.rglob("*.docx")))
    records: list[ImportedRecord] = []
    word_skill_count = 0
    word_uncertainties: list[WordUncertainty] = []
    for path in (*excel_files, *word_files):
        source_hashes[path.relative_to(resolved)] = hashlib.sha256(path.read_bytes()).hexdigest()
    for path in excel_files:
        records.extend(_read_xlsx_records(path))
    for path in word_files:
        count, uncertainty = _inspect_docx_skill_rows(path)
        word_skill_count += count
        if uncertainty:
            word_uncertainties.append(WordUncertainty(path, uncertainty))
    duplicate_group_count = sum(1 for group in _groups(records).values() if len(group) > 1)
    ambiguous_record_count = sum(1 for record in records if _is_ambiguous(record))
    return ImportInventory(
        root=resolved,
        records=tuple(records),
        source_hashes=source_hashes,
        excel_files=excel_files,
        word_files=word_files,
        excel_skill_count=len(records),
        word_skill_count=word_skill_count,
        duplicate_group_count=duplicate_group_count,
        ambiguous_record_count=ambiguous_record_count,
        word_excel_count_mismatch=bool(word_files) and word_skill_count != len(records),
        word_uncertainties=tuple(word_uncertainties),
    )


def build_initial_ledger(inventory: ImportInventory, output: Path) -> ImportSummary:
    """把可证明为正式条目的历史记录写入新的暂存 Excel 主台账。"""
    if inventory.word_uncertainties:
        raise ValueError("Word 结构无法确定，阻断自动正式导入")
    if inventory.word_excel_count_mismatch:
        raise ValueError("Word/Excel 数量不一致，阻断自动正式导入")
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    current_rows: list[dict[str, object]] = []
    alias_rows: list[dict[str, object]] = []
    observation_rows: list[dict[str, object]] = []
    from .ledger import LedgerStore
    for _, group in sorted(_groups(inventory.records).items()):
        if any(_is_ambiguous(record) for record in group):
            for record in group:
                observation_rows.append(_observation_row(record, "同一身份组含历史字段“API 或外部服务”，所有来源均需人工对账；不得推断为远程 API"))
            continue
        formal = next((record for record in group if _is_formal_record(record)), None)
        if formal is None:
            for record in group:
                observation_rows.append(_observation_row(record, "历史字段不足，需人工对账后才可进入正式台账"))
            continue
        stable_id = _stable_id(formal, _group_stable_id(group), formal.canonical_source)
        current_rows.append(_formal_row(formal, stable_id))
        alias_rows.extend(_alias_row(record, stable_id, formal) for record in group)
    with tempfile.TemporaryDirectory(prefix="ledger-import-", dir=output.parent) as directory:
        scratch = Path(directory) / "building.xlsx"
        candidate = Path(directory) / "validated.xlsx"
        store = LedgerStore.create(scratch)
        store.append_rows("当前Skill", current_rows)
        store.append_rows("来源别名", alias_rows)
        store.append_rows("候选观察", observation_rows)
        errors = store.validate()
        if errors:
            raise ValueError("初始台账预校验失败：" + "；".join(errors))
        store.save_staged(candidate)
        os.replace(candidate, output)
    return ImportSummary(
        output=output,
        written=True,
        current_skill_count=len(current_rows),
        source_alias_count=len(alias_rows),
        candidate_observation_count=len(observation_rows),
        stable_ids=tuple(row["内部标识"] for row in current_rows),
    )


def _read_xlsx_records(path: Path) -> list[ImportedRecord]:
    try:
        with ZipFile(path) as archive:
            shared = _shared_strings(archive)
            relationships = _workbook_relationships(archive)
            workbook = ET.fromstring(archive.read("xl/workbook.xml"))
            records: list[ImportedRecord] = []
            for sheet in workbook.findall(f"{_MAIN}sheets/{_MAIN}sheet"):
                relationship_id = sheet.attrib.get(f"{_REL}id", "")
                target = relationships.get(relationship_id)
                if not target:
                    continue
                rows = _worksheet_rows(archive.read(target), shared)
                records.extend(_records_from_rows(path, rows))
            return records
    except (BadZipFile, KeyError, ET.ParseError):
        return []


def _shared_strings(archive: ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(node.itertext()) for node in root.findall(f"{_MAIN}si")]


def _workbook_relationships(archive: ZipFile) -> dict[str, str]:
    root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    result: dict[str, str] = {}
    for relation in root.findall(f"{_PACKAGE_REL}Relationship"):
        target = relation.attrib.get("Target", "")
        if target.startswith("/"):
            result[relation.attrib["Id"]] = target.lstrip("/")
        else:
            result[relation.attrib["Id"]] = f"xl/{target}".replace("xl/../", "")
    return result


def _worksheet_rows(payload: bytes, shared: list[str]) -> list[tuple[int, dict[int, str]]]:
    root = ET.fromstring(payload)
    result: list[tuple[int, dict[int, str]]] = []
    for row in root.findall(f"{_MAIN}sheetData/{_MAIN}row"):
        values: dict[int, str] = {}
        for cell in row.findall(f"{_MAIN}c"):
            reference = cell.attrib.get("r", "A1")
            column = _column_number(re.sub(r"\d", "", reference))
            type_name = cell.attrib.get("t")
            if type_name == "inlineStr":
                value = "".join(cell.itertext())
            else:
                value_node = cell.find(f"{_MAIN}v")
                value = "" if value_node is None else value_node.text or ""
                if type_name == "s" and value.isdigit() and int(value) < len(shared):
                    value = shared[int(value)]
            values[column] = value.strip()
        if values:
            result.append((int(row.attrib.get("r", len(result) + 1)), values))
    return result


def _records_from_rows(path: Path, rows: list[tuple[int, dict[int, str]]]) -> list[ImportedRecord]:
    if not rows:
        return []
    header_index = next(
        (index for index, (_, values) in enumerate(rows) if "Skill名称" in {_canonical_header(value) for value in values.values()}),
        None,
    )
    if header_index is None:
        return []
    header_row, header_values = rows[header_index]
    headers = {column: _canonical_header(value) for column, value in header_values.items()}
    if "Skill名称" not in headers.values():
        return []
    records: list[ImportedRecord] = []
    for row_number, values in rows[header_index + 1:]:
        record = {headers[column]: value for column, value in values.items() if headers.get(column) and value}
        if record.get("Skill名称"):
            records.append(ImportedRecord(path, row_number, record))
    return records


def _canonical_header(header: str) -> str:
    normalized = header.strip()
    for target, aliases in HEADER_ALIASES.items():
        if normalized in aliases:
            return target
    if normalized in CURRENT_SKILL_COLUMNS or normalized in {"Canonical source", "来源平台", "API 或外部服务"}:
        return normalized
    return normalized


def _inspect_docx_skill_rows(path: Path) -> tuple[int, str | None]:
    try:
        with ZipFile(path) as archive:
            root = ET.fromstring(archive.read("word/document.xml"))
    except (BadZipFile, KeyError, ET.ParseError):
        return 0, "无法读取 Word 文档结构"
    count = 0
    found_recognized_table = False
    for table in root.findall(f".//{_DOCX}tbl"):
        rows = table.findall(f"{_DOCX}tr")
        if not rows:
            continue
        header_cells = ["".join(cell.itertext()).strip() for cell in rows[0].findall(f"{_DOCX}tc")]
        if "Skill名称" not in {_canonical_header(header) for header in header_cells}:
            continue
        found_recognized_table = True
        count += sum(1 for row in rows[1:] if "".join(row.itertext()).strip())
    if found_recognized_table:
        return count, None
    return 0, "未发现可确定的 Skill名称 表头"


def _groups(records: Iterable[ImportedRecord]) -> dict[str, list[ImportedRecord]]:
    items = list(records)
    parents = list(range(len(items)))

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(first: int, second: int) -> None:
        first_root, second_root = find(first), find(second)
        if first_root != second_root:
            parents[second_root] = first_root

    canonical_seen: dict[str, int] = {}
    validated_ids = {
        _first(record.values, "内部标识")
        for record in items
        if _is_validated_historical_record(record) and _first(record.values, "内部标识")
    }
    stable_seen: dict[str, int] = {}
    for index, record in enumerate(items):
        canonical = record.canonical_source
        if canonical:
            if canonical in canonical_seen:
                union(index, canonical_seen[canonical])
            else:
                canonical_seen[canonical] = index
        stable_id = _first(record.values, "内部标识")
        if stable_id and stable_id in validated_ids:
            if stable_id in stable_seen:
                union(index, stable_seen[stable_id])
            else:
                stable_seen[stable_id] = index
    result: dict[str, list[ImportedRecord]] = {}
    for index, record in enumerate(items):
        root = find(index)
        result.setdefault(f"group-{root:06d}", []).append(record)
    return result


def _is_ambiguous(record: ImportedRecord) -> bool:
    return bool(record.values.get(_API_COMBINED, "").strip())


def _is_formal_record(record: ImportedRecord) -> bool:
    values = record.values
    if values.get("入库层级") != "正式":
        return False
    return all(
        values.get(column, "").strip()
        for column in CURRENT_SKILL_COLUMNS
        if column not in CURRENT_SKILL_OPTIONAL_COLUMNS and column != "内部标识"
    )


def _group_stable_id(group: Iterable[ImportedRecord]) -> str:
    for record in group:
        stable_id = _first(record.values, "内部标识")
        if stable_id and _is_validated_historical_record(record):
            return stable_id
    return ""


def _is_validated_historical_record(record: ImportedRecord) -> bool:
    stable_id = _first(record.values, "内部标识")
    return bool(stable_id) and not validate_current_skill_row(_formal_row(record, stable_id))


def _stable_id(record: ImportedRecord, existing: str, canonical_source: str) -> str:
    if existing:
        return existing
    category = record.values.get("功能一级分类", "IMP").strip() or "IMP"
    digest = hashlib.sha256(canonical_source.encode("utf-8")).hexdigest()[:12].upper()
    return f"IMP-{category}-{digest}"


def _formal_row(record: ImportedRecord, stable_id: str) -> dict[str, object]:
    row: dict[str, object] = {column: "" for column in CURRENT_SKILL_COLUMNS}
    row.update(record.values)
    row["内部标识"] = stable_id
    row["Canonical source"] = record.canonical_source
    quality_score = row.get("质量评分")
    if isinstance(quality_score, str) and quality_score.strip().isdigit():
        row["质量评分"] = int(quality_score.strip())
    return row


def _alias_row(record: ImportedRecord, stable_id: str, formal: ImportedRecord) -> dict[str, object]:
    source_url = _first(record.values, "来源地址", "发现地址", "Canonical source")
    material = f"{stable_id}|{record.source_path}|{record.source_row}|{source_url}"
    return {
        "别名标识": f"alias-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}",
        "内部标识": stable_id,
        "来源平台": record.values.get("来源平台", formal.values.get("来源平台", "")),
        "来源地址": source_url,
        "Canonical source": formal.canonical_source,
        "关系类型": "规范来源" if record is formal else "跨平台别名",
        "去重依据": "Canonical source 一致",
        "记录日期": _first(record.values, "收集日期") or _first(formal.values, "收集日期"),
    }


def _observation_row(record: ImportedRecord, reason: str | None = None) -> dict[str, object]:
    material = f"{record.source_path}|{record.source_row}|{record.canonical_source}|{record.skill_name}"
    detail = reason or "历史字段“API 或外部服务”无法区分本地软件、插件接口与远程服务；不得推断为远程 API，需人工对账"
    return {
        "观察标识": f"obs-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:16]}",
        "候选名称": record.skill_name,
        "Canonical source": record.canonical_source,
        "观察状态": "需人工对账",
        "许可证": record.values.get("许可证", "待确认"),
        "记录日期": _valid_observation_date(_first(record.values, "收集日期")),
        "原因": detail,
    }


def _valid_observation_date(value: str) -> str:
    """保留可信历史日期；缺失或非法时记录本次导入日期。"""
    try:
        return date.fromisoformat(value).isoformat()
    except (TypeError, ValueError):
        return date.today().isoformat()


def _first(values: Mapping[str, str], *names: str) -> str:
    for name in names:
        if values.get(name, "").strip():
            return values[name].strip()
    return ""


def _column_number(name: str) -> int:
    value = 0
    for character in name:
        value = value * 26 + ord(character.upper()) - 64
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="只读清点历史 Word/Excel 交付物")
    parser.add_argument("root", type=Path)
    parser.add_argument("--inventory-only", action="store_true")
    args = parser.parse_args()
    inventory = scan_existing_deliveries(args.root)
    print(
        "Excel文件={}; Word文件={}; Excel记录={}; Word记录={}; 重复组={}; 歧义记录={}; Word不确定文件={}; Word/Excel不一致={}".format(
            len(inventory.excel_files),
            len(inventory.word_files),
            inventory.excel_skill_count,
            inventory.word_skill_count,
            inventory.duplicate_group_count,
            inventory.ambiguous_record_count,
            inventory.word_uncertainty_count,
            "是" if inventory.word_excel_count_mismatch else "否",
        )
    )
    if not args.inventory_only:
        parser.error("为保护历史交付物，首次运行必须指定 --inventory-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
