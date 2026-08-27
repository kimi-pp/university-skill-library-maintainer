"""固定版本变化判定和先追加历史、后更新当前行的保守写入。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from hashlib import sha256
from typing import Any, Mapping


@dataclass(frozen=True)
class VersionChange:
    status: str
    current: Mapping[str, Any]
    observed: Mapping[str, Any]
    requires_full_review: bool


@dataclass(frozen=True)
class VersionDecision:
    change: VersionChange
    outcome: str
    review_date: str = ""
    conclusion_change: str = ""
    evidence_paths: tuple[str, ...] = ()
    history_fields: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_change(
        cls,
        change: VersionChange,
        *,
        outcome: str,
        review_date: str = "",
        conclusion_change: str = "",
        evidence_paths: tuple[str, ...] | None = None,
    ) -> "VersionDecision":
        paths = evidence_paths if evidence_paths is not None else tuple(change.observed.get("evidence_paths", ()))
        return cls(change, outcome, review_date, conclusion_change, tuple(str(item) for item in paths))


def compare_version(current: Mapping[str, Any], observed: Mapping[str, Any]) -> VersionChange:
    """内容哈希是是否升级的边界：版本标签本身不是升级理由。"""
    current_row = dict(current)
    observed_row = dict(observed)
    if str(observed_row.get("availability", "")).strip().casefold() in {"deleted", "unavailable"}:
        return VersionChange("attention_required", current_row, observed_row, False)
    old_hash = _current_hash(current_row)
    new_hash = _observed_hash(observed_row)
    if not old_hash or not new_hash:
        raise ValueError("固定版本内容指纹不得为空")
    old_version = str(current_row.get("固定版本") or "").strip()
    new_version = str(observed_row.get("fixed_version") or observed_row.get("固定版本") or "").strip()
    if old_hash == new_hash:
        return VersionChange("unchanged" if old_version == new_version else "alias_observation", current_row, observed_row, False)
    return VersionChange("full_review_required", current_row, observed_row, True)


def apply_approved_version(ledger: object, decision: VersionDecision) -> None:
    """仅接受完整复审后的变更，且历史追加成功前绝不改写当前 Skill。"""
    if decision.history_fields:
        raise ValueError("history_fields 不可信；版本历史字段只能由受信变更重新计算")
    change = decision.change
    if change.status == "attention_required":
        _append_attention_once(ledger, change)
        return
    if decision.outcome == "rejected":
        return
    if decision.outcome != "accepted":
        raise ValueError("版本决定 outcome 只能为 accepted 或 rejected")
    if not change.requires_full_review:
        if change.status == "alias_observation":
            _append_version_alias_once(ledger, change)
        return
    _assert_trusted_change(ledger, change)
    history = _history_row(change, decision)
    existing_history = {str(row.get("版本记录标识") or "") for row in ledger.rows("版本历史")}
    if history["版本记录标识"] in existing_history:
        current_rows = [
            row for row in ledger.rows("当前Skill")
            if str(row.get("内部标识") or "").strip() == history["内部标识"]
        ]
        if len(current_rows) == 1 and (
            _observed_version(current_rows[0]) == _observed_version(change.observed)
            and _current_hash(current_rows[0]) == _observed_hash(change.observed)
        ):
            return
        raise ValueError("版本历史标识已存在，但当前Skill 未处于该已接受版本")
    ledger.append_rows("版本历史", [history])
    updated = dict(change.current)
    updated["固定版本"] = _observed_version(change.observed)
    updated["固定版本内容指纹"] = _observed_hash(change.observed)
    ledger.upsert_skill(updated)


def _assert_trusted_change(ledger: object, change: VersionChange) -> None:
    stable_id = str(change.current.get("内部标识") or "").strip()
    current_rows = [row for row in ledger.rows("当前Skill") if str(row.get("内部标识") or "").strip() == stable_id]
    if len(current_rows) != 1:
        raise ValueError("当前Skill 必须存在唯一的稳定标识")
    persisted = current_rows[0]
    if _current_hash(persisted) == _observed_hash(change.observed) and _observed_version(persisted) == _observed_version(change.observed):
        return
    if _current_hash(persisted) != _current_hash(change.current) or _observed_version(persisted) != _observed_version(change.current):
        raise ValueError("当前Skill 已变化，拒绝使用过期版本决定")
    if not _observed_version(change.observed) or not _observed_hash(change.observed):
        raise ValueError("新固定版本和固定版本内容指纹不得为空")


def _history_row(change: VersionChange, decision: VersionDecision) -> dict[str, Any]:
    old_version = _observed_version(change.current)
    new_version = _observed_version(change.observed)
    old_hash = _current_hash(change.current)
    new_hash = _observed_hash(change.observed)
    if not all((old_version, new_version, old_hash, new_hash)):
        raise ValueError("版本历史缺少旧/新版本或旧/新固定版本内容指纹")
    stable_id = str(change.current.get("内部标识") or "").strip()
    material = "|".join((stable_id, old_version, new_version, old_hash, new_hash))
    review_date = decision.review_date or date.today().isoformat()
    evidence_paths = decision.evidence_paths or tuple(change.observed.get("evidence_paths", ()))
    return {
        "版本记录标识": f"version-{sha256(material.encode('utf-8')).hexdigest()[:20]}",
        "内部标识": stable_id,
        "固定版本": new_version,
        "变更日期": review_date,
        "变更摘要": f"旧版本={old_version}；新版本={new_version}；旧哈希={old_hash}；新哈希={new_hash}；结论变化={decision.conclusion_change or '完整复审后接受'}",
        "证据位置": "；".join(str(path) for path in evidence_paths),
    }


def _append_version_alias_once(ledger: object, change: VersionChange) -> None:
    stable_id = str(change.current.get("内部标识") or "").strip()
    version = _observed_version(change.observed)
    source_url = str(change.observed.get("source_url") or change.observed.get("canonical_source") or "").strip()
    material = "|".join((stable_id, version, source_url))
    alias_id = f"version-alias-{sha256(material.encode('utf-8')).hexdigest()[:16]}"
    if alias_id in {str(row.get("别名标识") or "") for row in ledger.rows("来源别名")}:
        return
    ledger.append_rows("来源别名", [{
        "别名标识": alias_id,
        "内部标识": stable_id,
        "来源平台": str(change.observed.get("platform") or change.current.get("来源平台") or ""),
        "来源地址": source_url,
        "Canonical source": str(change.current.get("Canonical source") or ""),
        "关系类型": "版本别名观察",
        "去重依据": "固定版本内容指纹一致；仅新增版本标签",
        "记录日期": str(change.observed.get("observed_on") or date.today().isoformat()),
    }])


def _append_attention_once(ledger: object, change: VersionChange) -> None:
    stable_id = str(change.current.get("内部标识") or "").strip()
    source = str(change.current.get("Canonical source") or "").strip()
    material = "|".join((stable_id, source, "attention_required"))
    observation_id = f"attention-{sha256(material.encode('utf-8')).hexdigest()[:16]}"
    if observation_id in {str(row.get("观察标识") or "") for row in ledger.rows("候选观察")}:
        return
    ledger.append_rows("候选观察", [{
        "观察标识": observation_id,
        "候选名称": str(change.current.get("Skill名称") or ""),
        "Canonical source": source,
        "观察状态": "attention_required",
        "许可证": str(change.current.get("许可证") or "待确认"),
        "记录日期": str(change.observed.get("observed_on") or date.today().isoformat()),
        "原因": "上游已删除或不可用；保留既有当前版本和固定快照",
    }])


def _current_hash(row: Mapping[str, Any]) -> str:
    return str(row.get("固定版本内容指纹") or "").strip()


def _observed_hash(row: Mapping[str, Any]) -> str:
    return str(row.get("content_hash") or row.get("固定版本内容指纹") or "").strip()


def _observed_version(row: Mapping[str, Any]) -> str:
    return str(row.get("fixed_version") or row.get("固定版本") or "").strip()
