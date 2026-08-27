"""保守的跨平台 Skill 去重；名称相似永不构成自动合并依据。"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from hashlib import sha256
import re
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit


_SHA256 = re.compile(r"[0-9a-f]{64}", re.IGNORECASE)


@dataclass(frozen=True)
class DedupResult:
    skills: tuple[dict[str, Any], ...]
    aliases: tuple[dict[str, Any], ...]
    manual_review: tuple[dict[str, Any], ...]

    @property
    def product_count(self) -> int:
        return len(self.skills)


def canonical_key(candidate: object) -> str:
    """只使用已证明的身份；URL 查询和片段也是身份的一部分。"""
    canonical = _normalized_url(_value(candidate, "canonical_source", "Canonical source"))
    if canonical:
        return f"source:{canonical}"
    upstream, entry = _upstream_entry(candidate)
    if upstream and entry:
        return f"upstream:{upstream}|entry:{entry}"
    content_hash = _valid_hash(_value(candidate, "content_hash", "固定版本内容指纹"))
    if content_hash:
        return f"hash:{content_hash}"
    material = "|".join((
        _normalized_url(_value(candidate, "source_url", "来源地址", "发现地址")),
        _normalized_text(_value(candidate, "name", "Skill名称")),
        _normalized_text(_value(candidate, "function", "简要功能", "详细功能摘要")),
    ))
    return f"unproven:{sha256(material.encode('utf-8')).hexdigest()}"


def deduplicate(candidates: Sequence[object], ledger: object | None) -> DedupResult:
    """以组级强冲突检查阻止传递式误合并，并只复用台账证明的稳定 ID。"""
    normalized = [dict(_as_mapping(item)) for item in candidates]
    existing_by_identity, occupied_ids = _ledger_identity_ids(ledger)
    candidate_ids = [_matching_ledger_ids(candidate, existing_by_identity) for candidate in normalized]
    order = sorted(range(len(normalized)), key=lambda index: _candidate_sort_key(normalized[index]))
    groups: list[list[int]] = []
    for index in order:
        matches = [group for group in groups if _group_accepts(group, index, normalized, candidate_ids)]
        if not matches:
            groups.append([index])
            continue
        chosen = matches[0]
        for other in matches[1:]:
            if _groups_compatible(chosen, other, normalized, candidate_ids):
                chosen.extend(other)
                groups.remove(other)
        chosen.append(index)

    existing_alias_ids = _existing_alias_ids(ledger)
    skills: list[dict[str, Any]] = []
    aliases: list[dict[str, Any]] = []
    group_by_index: dict[int, int] = {}
    groups.sort(key=lambda group: min(_candidate_sort_key(normalized[index]) for index in group))
    for group_number, indexes in enumerate(groups):
        indexes.sort(key=lambda index: _candidate_sort_key(normalized[index]))
        representative = normalized[indexes[0]]
        stable_id = _stable_id(indexes, normalized, candidate_ids)
        canonical = _normalized_url(_value(representative, "canonical_source", "Canonical source"))
        skill = dict(representative)
        skill["内部标识"] = stable_id
        skill["Canonical source"] = canonical
        skills.append(skill)
        for index in indexes:
            group_by_index[index] = group_number
            alias = _alias_row(normalized[index], stable_id, canonical, _reason_for(index, indexes, normalized))
            if alias["别名标识"] not in existing_alias_ids and not any(item["别名标识"] == alias["别名标识"] for item in aliases):
                aliases.append(alias)

    manual_review = _manual_reviews(normalized, group_by_index)
    manual_review.extend(_untrusted_id_reviews(normalized, candidate_ids, occupied_ids))
    return DedupResult(tuple(skills), tuple(aliases), tuple(_unique_rows(manual_review, "观察标识")))


def _group_accepts(group: list[int], candidate_index: int, candidates: list[Mapping[str, Any]], ledger_ids: list[set[str]]) -> bool:
    candidate = candidates[candidate_index]
    if any(_strong_conflict(candidate, candidates[item]) for item in group):
        return False
    group_ids = set().union(*(ledger_ids[item] for item in group))
    if group_ids and ledger_ids[candidate_index] and group_ids != ledger_ids[candidate_index]:
        return False
    return any(_merge_reason(candidate, candidates[item]) for item in group)


def _groups_compatible(first: list[int], second: list[int], candidates: list[Mapping[str, Any]], ledger_ids: list[set[str]]) -> bool:
    first_ids = set().union(*(ledger_ids[item] for item in first))
    second_ids = set().union(*(ledger_ids[item] for item in second))
    if first_ids and second_ids and first_ids != second_ids:
        return False
    return not any(_strong_conflict(candidates[left], candidates[right]) for left in first for right in second)


def _merge_reason(first: Mapping[str, Any], second: Mapping[str, Any]) -> str:
    if _strong_conflict(first, second):
        return ""
    first_source = _normalized_url(_value(first, "canonical_source", "Canonical source"))
    second_source = _normalized_url(_value(second, "canonical_source", "Canonical source"))
    if first_source and first_source == second_source:
        return "Canonical source 一致"
    first_upstream, first_entry = _upstream_entry(first)
    second_upstream, second_entry = _upstream_entry(second)
    if first_upstream and first_entry and (first_upstream, first_entry) == (second_upstream, second_entry):
        return "上游身份与 Skill 入口路径一致"
    first_hash = _valid_hash(_value(first, "content_hash", "固定版本内容指纹"))
    second_hash = _valid_hash(_value(second, "content_hash", "固定版本内容指纹"))
    if first_hash and first_hash == second_hash:
        return "固定版本内容指纹一致"
    return ""


def _strong_conflict(first: Mapping[str, Any], second: Mapping[str, Any]) -> bool:
    first_source = _normalized_url(_value(first, "canonical_source", "Canonical source"))
    second_source = _normalized_url(_value(second, "canonical_source", "Canonical source"))
    if first_source and second_source and first_source != second_source:
        return True
    first_upstream, first_entry = _upstream_entry(first)
    second_upstream, second_entry = _upstream_entry(second)
    if first_upstream and first_entry and second_upstream and second_entry and (first_upstream, first_entry) != (second_upstream, second_entry):
        return True
    same_container = bool((first_source and first_source == second_source) or (first_upstream and first_upstream == second_upstream))
    if same_container and first_entry and second_entry and first_entry != second_entry:
        return True
    first_function = _normalized_text(_value(first, "function", "简要功能", "详细功能摘要"))
    second_function = _normalized_text(_value(second, "function", "简要功能", "详细功能摘要"))
    return bool(same_container and first_function and second_function and first_function != second_function)


def _reason_for(index: int, indexes: list[int], candidates: list[Mapping[str, Any]]) -> str:
    if index == indexes[0]:
        return "规范来源"
    for other in indexes:
        if other == index:
            continue
        reason = _merge_reason(candidates[index], candidates[other])
        if reason:
            return reason
    return "已验证关联关系"


def _stable_id(indexes: list[int], candidates: list[Mapping[str, Any]], ledger_ids: list[set[str]]) -> str:
    proven = set().union(*(ledger_ids[index] for index in indexes))
    if len(proven) == 1:
        return next(iter(proven))
    material = min(canonical_key(candidates[index]) for index in indexes)
    return f"SK-{sha256(material.encode('utf-8')).hexdigest()[:16].upper()}"


def _ledger_identity_ids(ledger: object | None) -> tuple[dict[str, set[str]], set[str]]:
    identities: dict[str, set[str]] = {}
    occupied: set[str] = set()
    if ledger is None or not hasattr(ledger, "rows"):
        return identities, occupied
    for sheet, fields in (("当前Skill", ("Canonical source",)), ("来源别名", ("来源地址", "Canonical source"))):
        for row in ledger.rows(sheet):
            stable_id = str(row.get("内部标识") or "").strip()
            if not stable_id:
                continue
            occupied.add(stable_id)
            for field in fields:
                value = _normalized_url(str(row.get(field) or ""))
                if value:
                    identities.setdefault(value, set()).add(stable_id)
    return identities, occupied


def _matching_ledger_ids(candidate: Mapping[str, Any], identities: Mapping[str, set[str]]) -> set[str]:
    matches: set[str] = set()
    for value in (_value(candidate, "canonical_source", "Canonical source"), _value(candidate, "source_url", "来源地址", "发现地址")):
        matches.update(identities.get(_normalized_url(value), set()))
    return matches


def _untrusted_id_reviews(candidates: list[Mapping[str, Any]], ledger_ids: list[set[str]], occupied_ids: set[str]) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        supplied = _value(candidate, "内部标识", "stable_id")
        if not supplied or supplied not in occupied_ids or ledger_ids[index] == {supplied}:
            continue
        material = f"{supplied}|{_candidate_identity(candidate)}"
        reviews.append({"观察标识": f"untrusted-id-{sha256(material.encode('utf-8')).hexdigest()[:16]}",
            "候选名称": _value(candidate, "name", "Skill名称"), "Canonical source": _normalized_url(_value(candidate, "canonical_source", "Canonical source")),
            "观察状态": "manual_review", "许可证": _value(candidate, "license", "许可证") or "待确认",
            "记录日期": _value(candidate, "observed_on", "收集日期"), "原因": "untrusted_stable_id_conflict"})
    return reviews


def _manual_reviews(candidates: list[Mapping[str, Any]], group_by_index: Mapping[int, int]) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    for first in range(len(candidates)):
        for second in range(first):
            if group_by_index[first] == group_by_index[second] or not _possible_duplicate(candidates[second], candidates[first]):
                continue
            material = "|".join(sorted((_candidate_identity(candidates[second]), _candidate_identity(candidates[first]))))
            reviews.append({"观察标识": f"possible-duplicate-{sha256(material.encode('utf-8')).hexdigest()[:16]}",
                "候选名称": _value(candidates[first], "name", "Skill名称"), "Canonical source": _normalized_url(_value(candidates[first], "canonical_source", "Canonical source")),
                "观察状态": "manual_review", "许可证": _value(candidates[first], "license", "许可证") or "待确认",
                "记录日期": _value(candidates[first], "observed_on", "收集日期"), "原因": "possible_duplicate"})
    return reviews


def _possible_duplicate(first: Mapping[str, Any], second: Mapping[str, Any]) -> bool:
    first_name, second_name = _normalized_text(_value(first, "name", "Skill名称")), _normalized_text(_value(second, "name", "Skill名称"))
    if not first_name or not second_name or first_name == second_name:
        return False
    first_function = _normalized_text(_value(first, "function", "简要功能", "详细功能摘要"))
    second_function = _normalized_text(_value(second, "function", "简要功能", "详细功能摘要"))
    return not (first_function and second_function and first_function != second_function) and SequenceMatcher(a=first_name, b=second_name).ratio() >= 0.65


def _alias_row(candidate: Mapping[str, Any], stable_id: str, canonical: str, reason: str) -> dict[str, Any]:
    platform = _value(candidate, "platform", "来源平台")
    source = _normalized_url(_value(candidate, "source_url", "来源地址", "发现地址"))
    material = "|".join((stable_id, platform, source))
    return {"别名标识": f"alias-{sha256(material.encode('utf-8')).hexdigest()[:16]}", "内部标识": stable_id,
            "来源平台": platform, "来源地址": source, "Canonical source": canonical,
            "关系类型": "规范来源" if reason == "规范来源" else "跨平台别名", "去重依据": reason,
            "记录日期": _value(candidate, "observed_on", "收集日期")}


def _existing_alias_ids(ledger: object | None) -> set[str]:
    return set() if ledger is None or not hasattr(ledger, "rows") else {str(row.get("别名标识") or "") for row in ledger.rows("来源别名")}


def _candidate_sort_key(candidate: Mapping[str, Any]) -> tuple[str, str]:
    return canonical_key(candidate), _normalized_url(_value(candidate, "source_url", "来源地址", "发现地址"))


def _candidate_identity(candidate: Mapping[str, Any]) -> str:
    return canonical_key(candidate) + "|" + _normalized_url(_value(candidate, "source_url", "来源地址", "发现地址"))


def _upstream_entry(candidate: object) -> tuple[str, str]:
    return (_normalized_text(_value(candidate, "upstream_identity", "上游项目地址", "upstream_project")), _normalized_path(_value(candidate, "entry_path", "Skill入口路径")))


def _valid_hash(value: str) -> str:
    return value.casefold() if _SHA256.fullmatch(value.strip()) else ""


def _unique_rows(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return list({row[key]: row for row in rows}.values())


def _as_mapping(candidate: object) -> Mapping[str, Any]:
    return candidate if isinstance(candidate, Mapping) else vars(candidate)


def _value(candidate: object, *names: str) -> str:
    if isinstance(candidate, Mapping):
        for name in names:
            if candidate.get(name) not in (None, ""):
                return str(candidate[name]).strip()
        return ""
    return next((str(getattr(candidate, name)).strip() for name in names if getattr(candidate, name, None) not in (None, "")), "")


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
    return urlunsplit((parsed.scheme.casefold(), parsed.netloc.casefold(), path, parsed.query, parsed.fragment))
