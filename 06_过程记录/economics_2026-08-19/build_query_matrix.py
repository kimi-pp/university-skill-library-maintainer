from __future__ import annotations

import argparse
import json
import unicodedata
from pathlib import Path
from typing import Any


PLATFORMS = (
    ("SkillHub", "SH"),
    ("ClawHub", "CH"),
    ("GitHub", "GH"),
    ("Hugging Face Spaces", "HF"),
)


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", " ".join(value.split()))


def _queries(profile: dict[str, Any], platform: str) -> tuple[str, str]:
    major_name = profile["major_name"]
    zh_terms = profile["search_terms"]["zh"]
    en_terms = profile["search_terms"]["en"]
    en_name = en_terms[0]
    method_zh = zh_terms[1] if len(zh_terms) > 1 else zh_terms[0]
    method_en = en_terms[1] if len(en_terms) > 1 else en_terms[0]

    if platform == "SkillHub":
        return (
            f"{major_name} {en_name} skill SKILL.md",
            f"{method_zh} {method_en} skill agent",
        )
    if platform == "ClawHub":
        return (
            f"{major_name} {en_name} claw skill agent",
            f"{method_zh} {method_en} skill workflow",
        )
    if platform == "GitHub":
        return (
            f"filename:SKILL.md {major_name} {en_name}",
            f"filename:SKILL.md {method_zh} {method_en}",
        )
    if platform == "Hugging Face Spaces":
        return (
            f"{major_name} {en_name} space",
            f"{method_zh} {method_en} app tool",
        )
    raise ValueError(f"unsupported platform: {platform}")


def build_query_matrix(profiles: dict[str, Any]) -> dict[str, Any]:
    jobs: list[dict[str, Any]] = []
    sequence = 0
    for profile in profiles["profiles"]:
        seen_for_major: set[str] = set()
        for platform, platform_code in PLATFORMS:
            for round_number, query in enumerate(_queries(profile, platform), start=1):
                normalized_query = _nfc(query)
                dedup_key = normalized_query.casefold()
                if dedup_key in seen_for_major:
                    continue
                seen_for_major.add(dedup_key)
                sequence += 1
                jobs.append(
                    {
                        "query_id": (
                            f"ECON-{profile['major_code']}-{platform_code}-"
                            f"R{round_number}-{sequence:04d}"
                        ),
                        "major_code": profile["major_code"],
                        "major_name": profile["major_name"],
                        "class_code": profile["class_code"],
                        "class_name": profile["class_name"],
                        "platform": platform,
                        "platform_code": platform_code,
                        "round": round_number,
                        "query": normalized_query,
                        "term_types": (
                            ["professional_name", "english_domain", "structure"]
                            if round_number == 1
                            else ["method_or_task", "bilingual", "structure"]
                        ),
                    }
                )
    return {
        "schema_version": "1.0",
        "category_code": profiles["category_code"],
        "category_name": profiles["category_name"],
        "profile_count": profiles["profile_count"],
        "platforms": [row[0] for row in PLATFORMS],
        "rounds": [1, 2],
        "job_count": len(jobs),
        "jobs": jobs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="生成经济学门类四平台双语查询矩阵")
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    profiles = json.loads(args.profiles.read_text(encoding="utf-8"))
    matrix = build_query_matrix(profiles)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
