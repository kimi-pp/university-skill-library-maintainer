from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


PLATFORM_ORDER = {"GitHub": 0, "SkillHub": 1, "ClawHub": 2, "Hugging Face Spaces": 3}


def _norm(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    text = re.sub(r"[\"'`*_>|]+", " ", text)
    text = re.sub(r"[^0-9a-z\u3400-\u9fff]+", " ", text)
    return " ".join(text.split())


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"(?mi)^{re.escape(key)}\s*:\s*(.*)$", text)
    if not match:
        return ""
    value = match.group(1).strip().strip("\"'")
    if value not in {"|", "|-", ">", ">-", ""}:
        return value
    lines: list[str] = []
    for line in text[match.end() :].splitlines():
        if re.match(r"^[A-Za-z][A-Za-z0-9_-]*\s*:", line):
            break
        if line.strip():
            lines.append(line.strip())
        elif lines:
            break
    return " ".join(lines)


def extract_skill_identity(text: str, fallback_path: str = "") -> tuple[str, str]:
    name = _frontmatter_value(text, "name")
    description = _frontmatter_value(text, "description")
    if not name:
        heading = re.search(r"(?m)^#\s+(.+?)\s*$", text)
        name = heading.group(1).strip() if heading else PurePosixPath(fallback_path).parent.name
    if not description:
        body = re.sub(r"(?s)^---.*?---", "", text, count=1)
        paragraphs = [re.sub(r"\s+", " ", p).strip(" #\t") for p in re.split(r"\n\s*\n", body)]
        description = next((p for p in paragraphs if len(p) >= 40 and not p.startswith("#")), "")
    return name.strip().strip("\"'"), description.strip().strip("\"'")


def canonical_source_key(row: dict[str, Any]) -> str:
    upstream = str(row.get("upstream_url") or "")
    github = re.search(r"github\.com/([^/]+)/([^/#]+)(?:/(?:tree|blob)/[^/]+/(.+))?", upstream, re.I)
    if github:
        owner, repo, path = github.group(1), github.group(2).removesuffix(".git"), github.group(3) or "skill.md"
        return f"github:{owner.casefold()}/{repo.casefold()}:{PurePosixPath(path).as_posix().casefold()}"

    platform = str(row.get("platform") or "")
    repository = str(row.get("repository") or "")
    path = PurePosixPath(str(row.get("skill_path") or "skill.md")).as_posix()
    mirror = re.search(r"(?:^|/)mirrors/repos/([^/@]+)@([^/]+)/(.+)$", path, re.I)
    if mirror:
        repository = f"{mirror.group(1)}/{mirror.group(2)}"
        path = mirror.group(3)
    if platform == "GitHub" and repository:
        return f"github:{repository.casefold()}:{path.casefold()}"
    native = str(row.get("candidate_native_id") or row.get("canonical_url") or row.get("candidate_key") or "")
    return f"{_norm(platform).replace(' ', '-') or 'unknown'}:{_norm(native).replace(' ', ':')}"


def function_fingerprint(row: dict[str, Any]) -> str:
    name = _norm(row.get("skill_name"))
    description = _norm(row.get("skill_description"))
    if not description:
        description = _norm(str(row.get("skill_text") or "")[:1600])
    return _sha(f"{name}\n{description}")


def _skill_path(row: dict[str, Any]) -> Path | None:
    for value in row.get("evidence_paths", []):
        path = Path(value)
        if path.name.casefold() == "skill.md" and path.exists():
            return path
    return None


def hydrate(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    text = str(result.get("skill_text") or "")
    path = _skill_path(result)
    if not text and path:
        text = path.read_text(encoding="utf-8", errors="replace")
    name, description = extract_skill_identity(text, str(result.get("skill_path") or ""))
    content_sha = str(result.get("skill_content_sha256") or "")
    if not content_sha:
        inventory = result.get("file_inventory", [])
        skill = next((f for f in inventory if PurePosixPath(str(f.get("path", ""))).name.casefold() == "skill.md"), None)
        content_sha = str((skill or {}).get("sha256") or (_sha(text) if text else ""))
    result.update(
        {
            "skill_name": name,
            "skill_description": description,
            "skill_content_sha256": content_sha,
            "canonical_source_key": canonical_source_key(result),
            "function_fingerprint": function_fingerprint({"skill_name": name, "skill_description": description, "skill_text": text}),
            "_skill_text": text,
        }
    )
    return result


class _UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[b] = a


def _representative_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        not bool(row.get("formal_eligible")),
        PLATFORM_ORDER.get(str(row.get("platform")), 9),
        -int(row.get("repository_stars") or 0),
        str(row.get("candidate_key") or ""),
    )


def deduplicate(rows: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    hydrated = [hydrate(row) for row in rows]
    uf = _UnionFind(len(hydrated))
    indexes: dict[tuple[str, str], int] = {}
    for idx, row in enumerate(hydrated):
        keys = [
            ("source", row["canonical_source_key"]),
            ("content", row["skill_content_sha256"]),
        ]
        name = _norm(row.get("skill_name"))
        description = _norm(row.get("skill_description"))
        if len(name) >= 4 and len(description) >= 20:
            keys.append(("function", row["function_fingerprint"]))
        for key in keys:
            if not key[1]:
                continue
            if key in indexes:
                uf.union(idx, indexes[key])
            else:
                indexes[key] = idx

    groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for idx, row in enumerate(hydrated):
        groups[uf.find(idx)].append(row)

    unique: list[dict[str, Any]] = []
    relations: list[dict[str, Any]] = []
    for members in groups.values():
        members.sort(key=_representative_key)
        representative = dict(members[0])
        member_keys = sorted(str(row.get("candidate_key") or "") for row in members)
        platforms = sorted({str(row.get("platform") or "") for row in members}, key=lambda p: PLATFORM_ORDER.get(p, 9))
        major_codes = sorted({code for row in members for code in row.get("major_codes", [])})
        query_ids = sorted({qid for row in members for qid in row.get("query_ids", [])})
        representative["candidate_uid"] = _sha("\n".join(member_keys))
        representative["discovery_platforms"] = platforms
        representative["major_codes"] = major_codes
        representative["query_ids"] = query_ids
        representative["duplicate_member_keys"] = member_keys
        representative["duplicate_count"] = len(members) - 1
        representative["source_candidates"] = [
            {
                "candidate_key": row.get("candidate_key"),
                "platform": row.get("platform"),
                "canonical_url": row.get("canonical_url"),
                "canonical_source_key": row.get("canonical_source_key"),
            }
            for row in members
        ]
        representative.pop("_skill_text", None)
        unique.append(representative)
        if len(members) > 1:
            same_content = len({row["skill_content_sha256"] for row in members}) == 1
            same_source = len({row["canonical_source_key"] for row in members}) == 1
            reason = "same_content" if same_content else "same_upstream" if same_source else "same_function"
            relations.append(
                {
                    "representative_candidate_key": representative.get("candidate_key"),
                    "member_candidate_keys": member_keys,
                    "discovery_sources": platforms,
                    "reason": reason,
                }
            )
    unique.sort(key=lambda row: (row.get("skill_name", "").casefold(), row.get("candidate_uid", "")))
    relations.sort(key=lambda row: str(row.get("representative_candidate_key")))
    return unique, relations


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audits", type=Path, required=True)
    parser.add_argument("--unique", type=Path, required=True)
    parser.add_argument("--relations", type=Path, required=True)
    args = parser.parse_args()
    unique, relations = deduplicate(_read_jsonl(args.audits))
    args.unique.write_text(json.dumps(unique, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.relations.write_text(json.dumps(relations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_rows": len(_read_jsonl(args.audits)), "unique_candidates": len(unique), "duplicate_groups": len(relations)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
