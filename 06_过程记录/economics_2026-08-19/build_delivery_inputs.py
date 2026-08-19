from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CLASS_ORDER = ("0201", "0202", "0203", "0204")
SCORE_LABELS = {5: "金牌 Skill", 4: "优质 Skill", 3: "标准 Skill", 2: "可用 Skill", 1: "待观察", 0: "不纳库"}


def default_paths(root: Path) -> dict[str, Path]:
    base = root / "06_过程记录" / "economics_2026-08-19"
    return {
        "scope": base / "economics_scope.json",
        "profiles": base / "professional_profiles.json",
        "sources": base / "profile_source_ledger.jsonl",
        "formal": base / "formal_candidates.json",
        "attrition": base / "attrition_summary.json",
        "supplement": base / "zero_result_supplement.json",
    }


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_inputs(paths: dict[str, Path]) -> dict[str, Any]:
    profiles_doc = _json(paths["profiles"])
    return {
        "scope": _json(paths["scope"]),
        "profiles": profiles_doc.get("profiles", profiles_doc),
        "sources": _jsonl(paths["sources"]),
        "formal": _json(paths["formal"]),
        "attrition": _json(paths["attrition"]),
        "supplement": _json(paths["supplement"]),
    }


def _delivery_skill(row: dict[str, Any]) -> dict[str, Any]:
    no_remote = row.get("external_api") == "否"
    simple_local = row.get("local_runtime") in {"不使用", "无", ""} and row.get("local_interface") in {"不使用", "无", ""}
    difficulty = "A" if row.get("security_grade") == "SA" and no_remote and simple_local else "B"
    readiness = "可直接使用" if difficulty == "A" else "微调后可用"
    return {
        "skill_id": row["skill_id"],
        "skill_name": row.get("skill_name"),
        "skill_description": row.get("skill_description"),
        "primary_class_code": row["primary_class_code"],
        "primary_major_code": row["primary_major_code"],
        "primary_major_name": row["primary_major_name"],
        "applicable_major_codes": row.get("matched_major_codes", []),
        "quality_score": row["quality_score"],
        "quality_label": SCORE_LABELS[row["quality_score"]],
        "verification_status": row["verification_status"],
        "security_grade": row["security_grade"],
        "access_difficulty": difficulty,
        "readiness": readiness,
        "external_api": row["external_api"],
        "network_behavior": row["network_behavior"],
        "credential_behavior": row.get("credential_behavior", "无"),
        "local_runtime": row["local_runtime"],
        "local_interface": row["local_interface"],
        "file_behavior": row.get("file_behavior", "无"),
        "platforms": row.get("discovery_platforms", [row.get("platform")]),
        "canonical_url": row.get("canonical_url"),
        "fixed_version": row.get("fixed_version"),
        "license": row.get("license"),
        "maintenance_date": row.get("maintenance_date"),
        "repository_stars": row.get("repository_stars"),
        "package_manifest_sha256": row.get("package_manifest_sha256"),
        "evidence_paths": row.get("evidence_paths", []),
        "professional_relevance_evidence": row.get("professional_relevance_evidence", []),
        "deduplication_note": "已按上游、固定内容和功能指纹全局去重；本条仅在一个主专业类正式收录。",
        "usage_boundary": "仅完成固定版本静态核验，未安装、未运行；涉及真实教学科研数据时须按校内制度复核。",
    }


def build_all_payloads(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    profile_map = {profile["major_code"]: profile for profile in inputs["profiles"]}
    supplement = inputs["supplement"].get("per_major", {})
    formal_rows = [_delivery_skill(row) for row in inputs["formal"]]
    payloads: list[dict[str, Any]] = []
    for class_code in CLASS_ORDER:
        class_info = next(row for row in inputs["scope"]["classes"] if row["class_code"] == class_code)
        major_codes = [row["major_code"] for row in class_info["majors"]]
        profiles = [profile_map[code] for code in major_codes]
        class_formal = [row for row in formal_rows if row["primary_class_code"] == class_code]
        statuses = []
        for code in major_codes:
            attrition = inputs["attrition"]["per_major"][code]
            supplement_row = supplement.get(code)
            formal_count = sum(code in row["applicable_major_codes"] for row in formal_rows)
            statuses.append(
                {
                    "major_code": code,
                    "major_name": profile_map[code]["major_name"],
                    "deduplicated_candidate_count": attrition["deduplicated_candidate_count"],
                    "formal_count": formal_count,
                    "excluded_candidate_count": attrition["excluded_candidate_count"],
                    "supplement_completed": bool(supplement_row),
                    "supplement_platforms": list((supplement_row or {}).get("platforms", {}).keys()),
                    "supplement_result_counts": {
                        platform: row["result_count"] for platform, row in (supplement_row or {}).get("platforms", {}).items()
                    },
                    "zero_result_note": (
                        "已完成四平台专项补查；未发现同时通过专业相关性、固定版本、许可证和静态安全门的 Skill。"
                        if formal_count == 0 and supplement_row
                        else "首轮及补查后有正式收录项。" if formal_count else "本轮未形成正式收录项。"
                    ),
                }
            )
        sources = [row for row in inputs["sources"] if set(row.get("major_codes", [])) & set(major_codes)]
        payloads.append(
            {
                "schema_version": "economics-class-delivery-v1",
                "generated_on": "2026-08-19",
                "category_code": "02",
                "category_name": "经济学",
                "class_code": class_code,
                "class_name": class_info["class_name"],
                "major_count": len(major_codes),
                "formal_count": len(class_formal),
                "profiles": profiles,
                "formal_candidates": class_formal,
                "major_search_status": statuses,
                "profile_sources": sources,
                "attrition": {
                    "deduplicated_candidate_count": sum(row["deduplicated_candidate_count"] for row in statuses),
                    "formal_candidate_count": len(class_formal),
                    "excluded_candidate_count": sum(row["excluded_candidate_count"] for row in statuses),
                    "global_reason_counts": inputs["attrition"]["exclusion_reason_counts"],
                },
                "method_note": "四社区联网发现；固定版本静态核验；专业任务匹配；跨平台与功能级去重；评分不抵消硬门槛。",
            }
        )
    ids = [row["skill_id"] for payload in payloads for row in payload["formal_candidates"]]
    if len(ids) != len(set(ids)) or set(ids) != {row["skill_id"] for row in inputs["formal"]}:
        raise ValueError("formal skill partition is not exact")
    return payloads


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = HERE.parents[1]
    payloads = build_all_payloads(load_inputs(default_paths(root)))
    args.output.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for payload in payloads:
        path = args.output / f"{payload['class_code']}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        hashes[path.name] = _digest(path)
    manifest = {"schema_version": "economics-delivery-input-manifest-v1", "payload_count": 4, "hashes": hashes}
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"payload_count": 4, "formal_counts": {p["class_code"]: p["formal_count"] for p in payloads}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
