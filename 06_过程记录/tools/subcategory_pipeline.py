"""Read and validate the immutable source catalog's subcategory ledger."""

import json
from pathlib import Path


def load_source_records(data_dir: Path) -> list[dict]:
    """Load the five approved source-category files in stable code order."""
    records: list[dict] = []
    for category_code in range(1, 6):
        source_path = data_dir / f"category_{category_code:02d}.json"
        with source_path.open(encoding="utf-8") as source_file:
            payload = json.load(source_file)
        records.extend(payload["records"])
    return records


def load_assignment_file(path: Path) -> dict:
    """Load the standalone, reviewable Skill-ID-to-subcategory ledger."""
    with path.open(encoding="utf-8") as assignment_file:
        return json.load(assignment_file)


def validate_assignments(records: list[dict], assignment_data: dict) -> None:
    """Reject incomplete, unknown, or cross-big-category assignments."""
    source_ids = {row["id"] for row in records}
    assignments = assignment_data["assignments"]
    taxonomy = {item["code"]: item for item in assignment_data["taxonomy"]}

    if len(source_ids) != len(records):
        raise ValueError("原始数据包含重复 Skill ID")
    if len(taxonomy) != len(assignment_data["taxonomy"]):
        raise ValueError("小分类代码重复")
    if set(assignments) != source_ids:
        missing = sorted(source_ids - set(assignments))
        extra = sorted(set(assignments) - source_ids)
        raise ValueError(f"小分类归属不完整: missing={missing}, extra={extra}")
    for skill_id, subcategory_code in assignments.items():
        if subcategory_code not in taxonomy:
            raise ValueError(f"{skill_id} 使用未知小分类 {subcategory_code}")
        if not skill_id.startswith(f"GH-{subcategory_code[:2]}-"):
            raise ValueError(f"{skill_id} 与 {subcategory_code} 的大分类不一致")


def enrich_with_subcategory(records: list[dict], assignment_data: dict) -> list[dict]:
    """Return copies of source records annotated from a validated ledger."""
    validate_assignments(records, assignment_data)
    taxonomy = {item["code"]: item for item in assignment_data["taxonomy"]}
    decision_notes = assignment_data.get("decision_notes", {})
    enriched_records: list[dict] = []
    for record in records:
        subcategory_code = assignment_data["assignments"][record["id"]]
        enriched_record = {
            **record,
            "subcategory_code": subcategory_code,
            "subcategory_name": taxonomy[subcategory_code]["name"],
        }
        if record["id"] in decision_notes:
            enriched_record["decision_note"] = decision_notes[record["id"]]
        enriched_records.append(enriched_record)
    return enriched_records
