import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source_snapshots" / "vocational_effective_2026_07.docx"
OUTPUT = ROOT / "catalogs" / "vocational_effective_2026.json"

CATEGORY_RE = re.compile(r"^([45]\d)(.+大类)$")
CLASS_RE = re.compile(r"^([45]\d{3})(.+类)$")
MAJOR_RE = re.compile(r"^[45]\d{5}K?$")

NEW_2026_NAMES = {
    "储能材料装备智能运维技术",
    "海洋智能机器人应用技术",
    "高原铁路智能建造与运维",
    "智能体通信技术",
    "车联网通信技术",
    "旅居康养运营与管理",
    "剧装戏具设计与制作",
    "婴幼儿家庭养育与指导",
    "老年教育服务与管理",
}


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u3000", " ")).strip()


def docx_table_rows(path: Path) -> list[list[str]]:
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))

    rows: list[list[str]] = []
    for table_row in document.iterfind(".//{*}tr"):
        cells: list[str] = []
        for table_cell in table_row.findall("./{*}tc"):
            text = "".join(node.text or "" for node in table_cell.iterfind(".//{*}t"))
            cells.append(normalize_text(text))
        if any(cells):
            rows.append(cells)
    return rows


def parse_effective_high_voc(
    rows: list[list[str]],
) -> tuple[list[dict], list[dict]]:
    current_category: tuple[str, str] | None = None
    current_class: tuple[str, str] | None = None
    records: list[dict] = []
    exceptions: list[dict] = []

    for row_number, cells in enumerate(rows, start=1):
        compact = "".join(cells)
        category_match = CATEGORY_RE.fullmatch(compact)
        if category_match:
            current_category = (category_match.group(1), category_match.group(2))
            current_class = None
            continue

        class_match = CLASS_RE.fullmatch(compact)
        if class_match:
            current_class = (class_match.group(1), class_match.group(2))
            continue

        code = next((cell for cell in cells if MAJOR_RE.fullmatch(cell)), None)
        if code is None:
            continue

        code_index = cells.index(code)
        name = normalize_text(cells[code_index + 1]) if code_index + 1 < len(cells) else ""
        if current_category is None or current_class is None or not name:
            exceptions.append(
                {
                    "row_number": row_number,
                    "raw_cells": cells,
                    "reason": "专业代码缺少可解析的专业大类、专业类或专业名称",
                }
            )
            continue

        source_ids = ["vocational_effective_2026_07"]
        enrollment_effective = "2026及以前"
        if name in NEW_2026_NAMES:
            source_ids.append("vocational_2026_release")
            enrollment_effective = "2027"

        records.append(
            {
                "category_code": current_category[0],
                "category_name": current_category[1],
                "class_code": current_class[0],
                "class_name": current_class[1],
                "major_code": code,
                "major_name": name,
                "is_national_control": code.endswith("K"),
                "catalog_status": "现行",
                "catalog_version": "职业教育专业目录（2021年）（更新时间：2026年7月）",
                "enrollment_effective": enrollment_effective,
                "source_ids": source_ids,
            }
        )

    records.sort(key=lambda item: item["major_code"])
    return records, exceptions


def validate_records(records: list[dict], exceptions: list[dict]) -> None:
    if exceptions:
        raise ValueError(f"catalog exceptions: {len(exceptions)}")
    if len(records) != 811:
        raise ValueError(f"expected 811 high-vocational majors, got {len(records)}")
    if len({row["major_code"] for row in records}) != 811:
        raise ValueError("duplicate high-vocational major codes")
    if len({row["category_code"] for row in records}) != 19:
        raise ValueError("expected 19 professional categories")
    if len({row["class_code"] for row in records}) != 97:
        raise ValueError("expected 97 professional classes")
    if sum(row["is_national_control"] for row in records) != 49:
        raise ValueError("expected 49 K-suffix national-control codes")
    if {row["major_name"] for row in records if row["enrollment_effective"] == "2027"} != NEW_2026_NAMES:
        raise ValueError("2026 supplement names do not reconcile")


def write_catalog(records: list[dict], exceptions: list[dict]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "catalog_version": "2026-07",
            "education_level": "高等职业教育专科",
            "record_count": len(records),
            "category_count": len({row["category_code"] for row in records}),
            "class_count": len({row["class_code"] for row in records}),
            "national_control_count": sum(row["is_national_control"] for row in records),
            "new_2026_count": sum(row["enrollment_effective"] == "2027" for row in records),
            "source_ids": [
                "vocational_2021_base",
                "vocational_2025_supplement",
                "vocational_effective_2026_07",
                "vocational_2026_release",
            ],
        },
        "records": records,
        "exceptions": exceptions,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    records, exceptions = parse_effective_high_voc(docx_table_rows(SOURCE))
    validate_records(records, exceptions)
    write_catalog(records, exceptions)
    print(
        f"vocational catalog: records={len(records)} "
        f"categories={len({x['category_code'] for x in records})} "
        f"classes={len({x['class_code'] for x in records})}"
    )


if __name__ == "__main__":
    main()
