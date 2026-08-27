"""保守的跨平台 Skill 去重；名称相似永不构成自动合并依据。"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from difflib import SequenceMatcher
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class DedupResult:
    """去重结果仅描述可写入的行，实际写入仍由单写入协调器完成。"""

    skills: tuple[dict[str, Any], ...]
    aliases: tuple[dict[str, Any], ...]
    manual_review: tuple[dict[str, Any], ...]

    @property
    def product_count(self) -> int:
        return len(self.skills)


def canonical_key(candidate: object) -> str:
    """按 canonical source、上游身份+入口和内容指纹的保守顺序构造键。"""
    canonical = _normalized_url(_value(candidate, "canonical_source", "Canonical source"))
    if canonical:
        return f"source:{canonical}"
    upstream = _normalized_text(_value(candidate, "upstream_identity", "上游项目地址", "upstream_project"))
    entry_path = _normalized_path(_value(candidate, "entry_path", "Skill入口路径"))
    if upstream and entry_path:
        return f"upstream:{upstream}|entry:{entry_path}"
    content_hash = _normalized_text(_value(candidate, "content_hash", "固定版本内容指纹"))
    if content_hash:
        return f"hash:{content_hash}"
    source_url = _normalized_url(_value(candidate, "source_url", "来源地址", "发现地址"))
    name = _normalized_text(_value(candidate, "name", "Skill名称"))
    function = _normalized_text(_value(candidate, "function", "简要功能", "详细功能摘要"))
    material = "|".join((source_url, name, function))
    return f"unproven:{sha256(material.encode('utf-8')).hexdigest()}"


def deduplicate(candidates: Sequence[object], ledger: object | None) -> DedupResult:
    """仅在可验证的关系证据下合并；其它相似项进入人工复核。"""
    normalized = [dict(_as_mapping(item)) for item in candidates]
    parents = list(range(len(normalized)))

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(first: int, second: int) -> None:
        first_root, second_root = find(first), find(second)
        if first_root != second_root:
            parents[second_root] = first_root

    evidence: dict[tuple[int, int], str] = {}
    for first in range(len(normalized)):
        for second in range(first):
            reason = _merge_reason(normalized[second], normalized[first])
            if reason:
                union(first, second)
                evidence[(second, first)] = reason

    groups: dict[int, list[int]] = {}
    for index in range(len(normalized)):
        groups.setdefault(find(index), []).append(index)
    existing_ids = _existing_stable_ids(ledger)
    existing_alias_ids = _existing_alias_ids(ledger)
    skills: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    group_by_index: dict[int, int] = {}
    for group_number, indexes in enumerate(groups.values()):
        representative = normalized[indexes[0]]
        stable_id = _stable_id(indexes, normalized, existing_ids)
        canonical = _normalized_url(_value(representative, "canonical_source", "Canonical source"))
        skill = dict(representative)
        skill["内部标识"] = stable_id
        skill["Canonical source"] = canonical
        skills.append(skill)
        for index in indexes:
            group_by_index[index] = group_number
            candidate = normalized[index]
            alias = _alias_row(candidate, stable_id, canonical, _reason_for(index, indexes, normalized, evidence))
            if alias["别名标识"] not in existing_alias_ids and not any(item["别名标识"] == alias["别名标识"] for item in aliases):
                aliases.append(alias)

    manual_review = _manual_reviews(normalized, group_by_index)
    return DedupResult(tuple(skills), tuple(aliases), tuple(manual_review))


def _merge_reason(first: Mapping[str, Any], second: Mapping[str, Any]) -> str:
    first_source = _normalized_url(_value(first, "canonical_source", "Canonical source"))
    second_source = _normalized_url(_value(second, "canonical_source", "Canonical source"))
    if first_source and first_source == second_source:
        return "Canonical source 一致"
    first_upstream = _normalized_text(_value(first, "upstream_identity", "上游项目地址", "upstream_project"))
    second_upstream = _normalized_text(_value(second, "upstream_identity", "上游项目地址", "upstream_project"))
    first_entry = _normalized_path(_value(first, "entry_path", "Skill入口路径"))
    second_entry = _normalized_path(_value(second, "entry_path", "Skill入口路径"))
    if first_upstream and first_entry and (first_upstream, first_entry) == (second_upstream, second_entry):
        return "上游身份与 Skill 入口路径一致"
    # 内容指纹只是缺少更强身份时的最后回退证据；不得推翻已知的不同
    # canonical source，或不同的上游/入口组合。
    has_conflicting_source = bool(first_source and second_source and first_source != second_source)
    first_identity = (first_upstream, first_entry) if first_upstream and first_entry else None
    second_identity = (second_upstream, second_entry) if second_upstream and second_entry else None
    has_conflicting_identity = bool(first_identity and second_identity and first_identity != second_identity)
    first_hash = _normalized_text(_value(first, "content_hash", "固定版本内容指纹"))
    second_hash = _normalized_text(_value(second, "content_hash", "固定版本内容指纹"))
    if not has_conflicting_source and not has_conflicting_identity and first_hash and first_hash == second_hash:
        return "固定版本内容指纹一致"
    return ""


def _reason_for(index: int, indexes: list[int], candidates: list[Mapping[str, Any]], evidence: Mapping[tuple[int, int], str]) -> str:
    if index == indexes[0]:
        return "规范来源"
    for other in indexes:
        pair = (min(other, index), max(other, index))
        if pair in evidence:
            return evidence[pair]
    return "已验证关联关系"


def _manual_reviews(candidates: list[Mapping[str, Any]], group_by_index: Mapping[int, int]) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    reviewed: set[tuple[int, int]] = set()
    for first in range(len(candidates)):
        for second in range(first):
            if group_by_index[first] == group_by_index[second]:
                continue
            pair = (second, first)
            if pair in reviewed or not _possible_duplicate(candidates[second], candidates[first]):
                continue
            reviewed.add(pair)
            material = "|".join(sorted((_candidate_identity(candidates[second]), _candidate_identity(candidates[first]))))
            reviews.append({
                "观察标识": f"possible-duplicate-{sha256(material.encode('utf-8')).hexdigest()[:16]}",
                "候选名称": _value(candidates[first], "name", "Skill名称"),
                "Canonical source": _normalized_url(_value(candidates[first], "canonical_source", "Canonical source")),
                "观察状态": "manual_review",
                "许可证": _value(candidates[first], "license", "许可证") or "待确认",
                "记录日期": _value(candidates[first], "observed_on", "收集日期"),
                "原因": "possible_duplicate",
            })
    return reviews


def _possible_duplicate(first: Mapping[str, Any], second: Mapping[str, Any]) -> bool:
    first_name = _normalized_text(_value(first, "name", "Skill名称"))
    second_name = _normalized_text(_value(second, "name", "Skill名称"))
    if not first_name or not second_name or first_name == second_name:
        return False
    first_function = _normalized_text(_value(first, "function", "简要功能", "详细功能摘要"))
    second_function = _normalized_text(_value(second, "function", "简要功能", "详细功能摘要"))
    if first_function and second_function and first_function != second_function:
        return False
    return SequenceMatcher(a=first_name, b=second_name).ratio() >= 0.65


def _stable_id(indexes: list[int], candidates: list[Mapping[str, Any]], existing_ids: Mapping[str, str]) -> str:
    for index in indexes:
        candidate = candidates[index]
        source = _normalized_url(_value(candidate, "canonical_source", "Canonical source"))
        if source and source in existing_ids:
            return existing_ids[source]
        existing = _value(candidate, "内部标识", "stable_id")
        if existing:
            return existing
    material = canonical_key(candidates[indexes[0]])
    return f"SK-{sha256(material.encode('utf-8')).hexdigest()[:16].upper()}"


def _alias_row(candidate: Mapping[str, Any], stable_id: str, canonical: str, reason: str) -> dict[str, Any]:
    platform = _value(candidate, "platform", "来源平台")
    source = _normalized_url(_value(candidate, "source_url", "来源地址", "发现地址"))
    material = "|".join((stable_id, platform, source))
    return {
        "别名标识": f"alias-{sha256(material.encode('utf-8')).hexdigest()[:16]}",
        "内部标识": stable_id,
        "来源平台": platform,
        "来源地址": source,
        "Canonical source": canonical,
        "关系类型": "规范来源" if reason == "规范来源" else "跨平台别名",
        "去重依据": reason,
        "记录日期": _value(candidate, "observed_on", "收集日期"),
    }


def _existing_stable_ids(ledger: object | None) -> dict[str, str]:
    if ledger is None or not hasattr(ledger, "rows"):
        return {}
    return {
        _normalized_url(str(row.get("Canonical source") or "")): str(row.get("内部标识") or "")
        for row in ledger.rows("当前Skill")
        if _normalized_url(str(row.get("Canonical source") or "")) and str(row.get("内部标识") or "")
    }


def _existing_alias_ids(ledger: object | None) -> set[str]:
    if ledger is None or not hasattr(ledger, "rows"):
        return set()
    return {str(row.get("别名标识") or "") for row in ledger.rows("来源别名")}


def _candidate_identity(candidate: Mapping[str, Any]) -> str:
    return canonical_key(candidate) + "|" + _normalized_url(_value(candidate, "source_url", "来源地址", "发现地址"))


def _as_mapping(candidate: object) -> Mapping[str, Any]:
    if isinstance(candidate, Mapping):
        return candidate
    return vars(candidate)


def _value(candidate: object, *names: str) -> str:
    if isinstance(candidate, Mapping):
        for name in names:
            value = candidate.get(name)
            if value not in (None, ""):
                return str(value).strip()
        return ""
    for name in names:
        value = getattr(candidate, name, None)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def _normalized_text(value: str) -> str:
    return " ".join(value.strip().casefold().split())


def _normalized_path(value: str) -> str:
    return value.replace("\\", "/").strip(" /").casefold()


def _normalized_url(value: str) -> str:
    if not value:
        return ""
    parsed = urlsplit(value.strip())
    if not parsed.scheme or not parsed.netloc:
        return ""
    path = parsed.path.rstrip("/")
    if path.casefold().endswith(".git"):
        path = path[:-4]
    return urlunsplit((parsed.scheme.casefold(), parsed.netloc.casefold(), path, "", ""))
