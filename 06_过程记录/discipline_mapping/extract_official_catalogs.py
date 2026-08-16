from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

import pdfplumber
from lxml import html as lxml_html


HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / "source_manifest.json"
CATALOG_DIR = HERE / "catalogs"
PAGE_MARKER = "[[PAGE {page}]]"


class ParsedRecords(list[dict[str, Any]]):
    """A list-compatible parse result carrying rejected source rows."""

    def __init__(
        self,
        records: Iterable[dict[str, Any]] = (),
        exceptions: Iterable[dict[str, Any]] = (),
    ) -> None:
        super().__init__(records)
        self.exceptions = list(exceptions)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u3000", " ")).strip()


def pdf_text(path: Path) -> str:
    """Extract text with explicit, stable page boundaries."""

    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages, 1):
            pages.append(
                f"{PAGE_MARKER.format(page=page_number)}\n{page.extract_text() or ''}"
            )
    return "\n\f\n".join(pages)


def _pages(text: str) -> Iterable[tuple[int, list[str]]]:
    for block in text.split("\f"):
        lines = block.strip().splitlines()
        if not lines:
            continue
        marker = re.fullmatch(r"\[\[PAGE (\d+)\]\]", lines[0].strip())
        if marker:
            yield int(marker.group(1)), lines[1:]
        else:
            yield 1, lines


def _logical_catalog_lines(
    text: str,
    record_pattern: re.Pattern[str],
    header_patterns: tuple[re.Pattern[str], ...],
) -> Iterable[tuple[int, str]]:
    """Join wrapped annotations while preserving the first line's page."""

    for page_number, lines in _pages(text):
        pending: str | None = None
        for raw in lines:
            line = normalize_text(raw)
            if not line or re.fullmatch(r"[—-]\s*\d+\s*[—-]", line):
                continue
            if record_pattern.match(line):
                if pending is not None:
                    yield page_number, pending
                pending = line
                continue
            if any(pattern.match(line) for pattern in header_patterns):
                if pending is not None:
                    yield page_number, pending
                    pending = None
                yield page_number, line
                continue
            if re.match(r"^\d", line):
                if pending is not None:
                    yield page_number, pending
                    pending = None
                yield page_number, line
                continue
            if pending is not None:
                pending = normalize_text(f"{pending} {line}")
        if pending is not None:
            yield page_number, pending


def _split_name_note(value: str) -> tuple[str, str | None]:
    value = normalize_text(value)
    if "（" not in value:
        return value.rstrip("* "), None
    name, note = value.split("（", 1)
    return normalize_text(name).rstrip("* "), normalize_text(note.rstrip("）"))


def _undergraduate_degrees(category_name: str, note: str | None) -> list[str]:
    if note:
        match = re.search(r"(?:可授|授予)(.+?)学士学位", note)
        if match:
            degrees = [
                normalize_text(item)
                for item in re.split(r"或|、", match.group(1))
                if normalize_text(item)
            ]
            if degrees:
                return degrees
    return [] if category_name == "交叉学科" else [category_name]


def parse_undergraduate(text: str) -> list[dict]:
    major_pattern = re.compile(r"^(\d{6,7}(?:TK|KT|T|K)?)\s+(.+)$")
    category_pattern = re.compile(r"^(\d{2})\s+学科门类：(.+)$")
    class_pattern = re.compile(r"^(\d{4})\s+(.+类)$")
    records: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []
    category: tuple[str, str] | None = None
    professional_class: tuple[str, str] | None = None

    for page, line in _logical_catalog_lines(
        text, major_pattern, (category_pattern, class_pattern)
    ):
        category_match = category_pattern.match(line)
        if category_match:
            category = (category_match.group(1), normalize_text(category_match.group(2)))
            professional_class = None
            continue
        class_match = class_pattern.match(line)
        if class_match:
            professional_class = (
                class_match.group(1),
                normalize_text(class_match.group(2)),
            )
            continue
        major_match = major_pattern.match(line)
        if not major_match:
            if category is not None and line[:1].isdigit():
                exceptions.append(
                    {
                        "page": page,
                        "raw_line": line,
                        "reason": "unparseable digit-leading catalog line",
                    }
                )
            continue
        code, value = major_match.groups()
        name, note = _split_name_note(value)
        if (
            not name
            or category is None
            or (professional_class is None and category[0] != "14")
            or not code.startswith(category[0])
        ):
            exceptions.append({"page": page, "raw_line": line})
            continue
        attributes: list[str] = []
        if "T" in code:
            attributes.append("特设专业")
        if "K" in code:
            attributes.append("国家控制布点专业")
        if category[0] == "14":
            attributes.append("目录未设专业类")
        records.append(
            {
                "category_code": category[0],
                "category_name": category[1],
                "class_code": professional_class[0] if professional_class else None,
                "class_name": professional_class[1] if professional_class else None,
                "major_code": code,
                "major_name": name,
                "attributes": attributes,
                "degree_categories": _undergraduate_degrees(category[1], note),
                "duration": None,
                "source_id": "undergraduate_2026_pdf",
            }
        )

    return ParsedRecords(records, exceptions)


def _graduate_record(
    category: tuple[str, str],
    code: str,
    name: str,
    object_type: str,
    degree_levels: list[str],
    notes: list[str],
) -> dict[str, Any]:
    return {
        "category_code": category[0],
        "category_name": category[1],
        "object_code": code,
        "object_name": name,
        "object_type": object_type,
        "degree_levels": degree_levels,
        "notes": notes,
        "status": "current",
        "source_ids": ["graduate_2022_pdf"],
        "previous_names": [],
    }


def parse_graduate_base(text: str) -> list[dict]:
    object_pattern = re.compile(r"^(\d{4})\s+(.+)$")
    category_pattern = re.compile(r"^(\d{2})\s+(.+)$")
    records: list[tuple[dict[str, Any], int, str]] = []
    exceptions: list[dict[str, Any]] = []
    category: tuple[str, str] | None = None

    for page, line in _logical_catalog_lines(
        text, object_pattern, (category_pattern,)
    ):
        category_match = category_pattern.match(line)
        if category_match:
            category = (category_match.group(1), normalize_text(category_match.group(2)))
            continue
        match = object_pattern.match(line)
        if not match:
            if category is not None and line[:1].isdigit():
                exceptions.append(
                    {
                        "page": page,
                        "raw_line": line,
                        "reason": "unparseable digit-leading catalog line",
                    }
                )
            continue
        code, value = match.groups()
        name, note = _split_name_note(value)
        if not name or category is None or not code.startswith(category[0]):
            exceptions.append({"page": page, "raw_line": line})
            continue

        is_professional = int(code[-2:]) >= 50
        object_type = "专业学位类别" if is_professional else "学术学位一级学科"
        master_only = "*" in value
        notes = [note] if note else []
        if master_only:
            notes.append("仅授硕士专业学位")
        records.append(
            (
                _graduate_record(
                    category,
                    code,
                    name,
                    object_type,
                    ["硕士"] if master_only else ["博士", "硕士"],
                    notes,
                ),
                page,
                line,
            )
        )

        if note:
            implied = re.search(r"同时设专业学位类别，\s*代码为\s*(\d{4})", note)
            if implied:
                implied_code = implied.group(1)
                records.append(
                    (
                        _graduate_record(
                            category,
                            implied_code,
                            name,
                            "专业学位类别",
                            ["博士", "硕士"],
                            [f"由{code}条目注释明确列出"],
                        ),
                        page,
                        line,
                    )
                )

    deduplicated: dict[tuple[str, str], dict[str, Any]] = {}
    for record, page, raw_line in records:
        key = (record["object_type"], record["object_code"])
        existing = deduplicated.get(key)
        if existing is None:
            deduplicated[key] = record
            continue
        if (
            existing["object_name"] != record["object_name"]
            or existing["category_code"] != record["category_code"]
        ):
            exceptions.append(
                {
                    "page": page,
                    "raw_line": raw_line,
                    "reason": "duplicate code has conflicting current identity",
                }
            )
            continue
        existing["degree_levels"] = sorted(
            set(existing["degree_levels"]) | set(record["degree_levels"]),
            key=("博士", "硕士").index,
        )
        existing["notes"] = list(dict.fromkeys(existing["notes"] + record["notes"]))

    return ParsedRecords(deduplicated.values(), exceptions)


def _expanded_rows(table: Any) -> list[list[str]]:
    pending: dict[int, tuple[str, int]] = {}
    expanded: list[list[str]] = []
    for tr in table.xpath(".//tr"):
        row: list[str] = []
        column = 0
        cells = tr.xpath("./th|./td")
        cell_index = 0
        while cell_index < len(cells) or pending:
            while column in pending:
                value, remaining = pending[column]
                row.append(value)
                if remaining == 1:
                    del pending[column]
                else:
                    pending[column] = (value, remaining - 1)
                column += 1
            if cell_index >= len(cells):
                break
            cell = cells[cell_index]
            cell_index += 1
            value = normalize_text("".join(cell.itertext()))
            colspan = int(cell.get("colspan", "1"))
            rowspan = int(cell.get("rowspan", "1"))
            for _ in range(colspan):
                row.append(value)
                if rowspan > 1:
                    pending[column] = (value, rowspan - 1)
                column += 1
        expanded.append(row)
    return expanded


def _identity_name(value: str) -> tuple[str, str | None]:
    return _split_name_note(value)


def parse_correspondence(html: str) -> list[dict]:
    document = lxml_html.fromstring(html)
    target = None
    for table in document.xpath("//table"):
        first_row = normalize_text("".join(table.xpath(".//tr[1]//text()")))
        if "研究生教育学科专业目录（2022年）" in first_row:
            target = table
            break
    if target is None:
        return ParsedRecords(
            [],
            [{"page": None, "raw_line": "", "reason": "correspondence table not found"}],
        )

    raw_records: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []
    code_pattern = re.compile(r"^\d{4,6}$")
    for row_number, row in enumerate(_expanded_rows(target)[2:], 3):
        if len(row) < 6:
            exceptions.append(
                {"page": None, "raw_line": " | ".join(row), "row": row_number}
            )
            continue
        current_category, current_code, current_value = row[:3]
        previous_category, previous_code, previous_name = row[3:6]
        current_name, current_note = _identity_name(current_value)
        required = (current_code, current_name, previous_code, previous_name)
        if (
            not all(required)
            or not code_pattern.fullmatch(current_code)
            or not code_pattern.fullmatch(previous_code)
        ):
            exceptions.append(
                {"page": None, "raw_line": " | ".join(row), "row": row_number}
            )
            continue
        raw_records.append(
            {
                "current_category_name": current_category,
                "current_object_code": current_code,
                "current_object_name": current_name,
                "current_object_type": (
                    "专业学位类别"
                    if int(current_code[-2:]) >= 50
                    else "学术学位一级学科"
                ),
                "previous_category_name": previous_category,
                "previous_code": previous_code,
                "previous_name": previous_name,
                "relation_type": "",
                "notes": [current_note] if current_note else [],
                "source_id": "graduate_2025_correspondence",
            }
        )

    current_to_previous: dict[tuple[str, str], set[tuple[str, str]]] = {}
    previous_to_current: dict[tuple[str, str], set[tuple[str, str]]] = {}
    for record in raw_records:
        current = (record["current_object_code"], record["current_object_name"])
        previous = (record["previous_code"], record["previous_name"])
        current_to_previous.setdefault(current, set()).add(previous)
        previous_to_current.setdefault(previous, set()).add(current)
    for record in raw_records:
        current = (record["current_object_code"], record["current_object_name"])
        previous = (record["previous_code"], record["previous_name"])
        if len(current_to_previous[current]) > 1:
            relation_type = "merge"
        elif len(previous_to_current[previous]) > 1:
            relation_type = "split"
        elif (
            record["current_object_code"] == record["previous_code"]
            and re.sub(r"\s+", "", record["current_category_name"])
            == re.sub(r"\s+", "", record["previous_category_name"])
        ):
            relation_type = "rename"
        else:
            relation_type = "move"
        record["relation_type"] = relation_type

    return ParsedRecords(raw_records, exceptions)


def enrich_with_correspondence(
    base: list[dict], correspondence: list[dict]
) -> list[dict]:
    effective = ParsedRecords(copy.deepcopy(base), getattr(base, "exceptions", []))
    index = {
        (record["object_type"], record["object_code"]): record for record in effective
    }
    for lineage in correspondence:
        key = (lineage["current_object_type"], lineage["current_object_code"])
        current = index.get(key)
        if current is None:
            effective.exceptions.append(
                {
                    "page": None,
                    "raw_line": json.dumps(lineage, ensure_ascii=False, sort_keys=True),
                    "reason": "2022-side code is absent from the 2022 PDF",
                }
            )
            continue
        names_match = normalize_text(current["object_name"]) == normalize_text(
            lineage["current_object_name"]
        )
        categories_match = re.sub(r"\s+", "", current["category_name"]) == re.sub(
            r"\s+", "", lineage["current_category_name"]
        )
        if not names_match or not categories_match:
            effective.exceptions.append(
                {
                    "page": None,
                    "raw_line": json.dumps(lineage, ensure_ascii=False, sort_keys=True),
                    "reason": "2022-side code/name conflicts with the 2022 PDF",
                }
            )
            continue
        previous = {
            "category_name": lineage["previous_category_name"],
            "code": lineage["previous_code"],
            "name": lineage["previous_name"],
            "relation_type": lineage["relation_type"],
            "source_id": lineage["source_id"],
        }
        if previous not in current["previous_names"]:
            current["previous_names"].append(previous)
        if lineage["source_id"] not in current["source_ids"]:
            current["source_ids"].append(lineage["source_id"])
    for record in effective:
        record["previous_names"].sort(
            key=lambda item: (item["code"], item["name"], item["category_name"])
        )
    return effective


def _record_sort_key(record: dict[str, Any]) -> tuple[str, ...]:
    if "major_code" in record:
        return (record["major_code"],)
    if "object_code" in record:
        type_order = "0" if record["object_type"] == "学术学位一级学科" else "1"
        return (type_order, record["object_code"], record["object_name"])
    return (
        record.get("current_object_code", ""),
        record.get("previous_code", ""),
        record.get("previous_name", ""),
    )


def write_payload(path: Path, source_ids: list[str], records: list[dict]) -> None:
    exceptions = list(getattr(records, "exceptions", []))
    sorted_records = sorted(records, key=_record_sort_key)
    payload = {
        "metadata": {
            "source_ids": source_ids,
            "record_count": len(sorted_records),
            "exception_count": len(exceptions),
        },
        "records": sorted_records,
        "exceptions": exceptions,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _verified_sources() -> dict[str, Path]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    sources: dict[str, Path] = {}
    for source in manifest["sources"]:
        path = HERE / source["local_path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != source["sha256"]:
            raise ValueError(f"snapshot hash mismatch for {source['id']}")
        sources[source["id"]] = path
    return sources


def main() -> None:
    sources = _verified_sources()
    undergraduate = parse_undergraduate(
        pdf_text(sources["undergraduate_2026_pdf"])
    )
    graduate_base = parse_graduate_base(pdf_text(sources["graduate_2022_pdf"]))
    correspondence = parse_correspondence(
        sources["graduate_2025_correspondence"].read_text(encoding="utf-8")
    )
    graduate_effective = enrich_with_correspondence(
        graduate_base, correspondence
    )

    write_payload(
        CATALOG_DIR / "undergraduate_2026.json",
        ["undergraduate_2026_pdf"],
        undergraduate,
    )
    write_payload(
        CATALOG_DIR / "graduate_2022_base.json",
        ["graduate_2022_pdf"],
        graduate_base,
    )
    write_payload(
        CATALOG_DIR / "graduate_correspondence.json",
        ["graduate_2025_correspondence"],
        correspondence,
    )
    write_payload(
        CATALOG_DIR / "graduate_effective.json",
        ["graduate_2022_pdf", "graduate_2025_correspondence"],
        graduate_effective,
    )


if __name__ == "__main__":
    main()
