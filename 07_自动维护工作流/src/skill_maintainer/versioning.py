"""固定版本变化判定与受信 Task 7 审批绑定的原子写入。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from hashlib import sha256
from io import BytesIO
import re
from typing import Any, Mapping

from openpyxl import load_workbook

from .review import AppliedReview, consume_applied_review, validate_applied_review


_SHA256 = re.compile(r"[0-9a-f]{64}", re.IGNORECASE)
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
    applied_review: AppliedReview | None = None

    @classmethod
    def from_change(cls, change: VersionChange, *, outcome: str, review_date: str = "", conclusion_change: str = "", evidence_paths: tuple[str, ...] | None = None) -> "VersionDecision":
        if outcome == "accepted" and change.requires_full_review:
            raise ValueError("changed content accepted version requires a trusted review receipt")
        paths = evidence_paths if evidence_paths is not None else tuple(change.observed.get("evidence_paths", ()))
        return cls(change, outcome, review_date, conclusion_change, tuple(str(item) for item in paths))

    @classmethod
    def accept_from_applied_review(cls, change: VersionChange, receipt: object, *, review_date: str, conclusion_change: str) -> "VersionDecision":
        if not change.requires_full_review:
            raise ValueError("review receipt can only accept changed content")
        return cls(change, "accepted", review_date, conclusion_change, (), {}, validate_applied_review(receipt))


def compare_version(current: Mapping[str, Any], observed: Mapping[str, Any]) -> VersionChange:
    current_row, observed_row = dict(current), dict(observed)
    if str(observed_row.get("availability", "")).strip().casefold() in {"deleted", "unavailable"}:
        return VersionChange("attention_required", current_row, observed_row, False)
    old_hash, new_hash = _current_hash(current_row), _observed_hash(observed_row)
    if not old_hash or not new_hash:
        raise ValueError("固定版本内容指纹必须为精确 64 位十六进制 SHA-256")
    old_version, new_version = _observed_version(current_row), _observed_version(observed_row)
    if old_hash == new_hash:
        return VersionChange("unchanged" if not new_version or old_version == new_version else "alias_observation", current_row, observed_row, False)
    return VersionChange("full_review_required", current_row, observed_row, True)


def apply_approved_version(ledger: object, decision: VersionDecision) -> None:
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
        if change.status == "alias_observation" and _observed_version(change.observed):
            _append_version_alias_once(ledger, change)
        return
    persisted = _persisted_current(ledger, change)
    receipt = _validate_accepted_review(decision, persisted)
    history = _history_row(change, decision)
    existing_history = {str(row.get("版本记录标识") or "") for row in ledger.rows("版本历史")}
    if history["版本记录标识"] in existing_history:
        if _observed_version(persisted) == _observed_version(change.observed) and _current_hash(persisted) == _observed_hash(change.observed):
            return
        raise ValueError("版本历史标识已存在，但当前Skill 未处于该已接受版本")
    _apply_transactionally(ledger, history, change, persisted)
    consume_applied_review(receipt)


def _persisted_current(ledger: object, change: VersionChange) -> Mapping[str, Any]:
    stable_id = str(change.current.get("内部标识") or "").strip()
    rows = [row for row in ledger.rows("当前Skill") if str(row.get("内部标识") or "").strip() == stable_id]
    if len(rows) != 1:
        raise ValueError("当前Skill 必须存在唯一的稳定标识")
    persisted = rows[0]
    if dict(persisted) != dict(change.current):
        if not (_observed_version(persisted) == _observed_version(change.observed) and _current_hash(persisted) == _observed_hash(change.observed)):
            raise ValueError("当前Skill 与版本决定的完整持久化行不一致")
    if not _current_hash(persisted) or not _observed_version(change.observed) or not _observed_hash(change.observed):
        raise ValueError("新固定版本和固定版本内容指纹必须有效")
    return persisted


def _validate_accepted_review(decision: VersionDecision, persisted: Mapping[str, Any]) -> AppliedReview:
    receipt = validate_applied_review(decision.applied_review)
    observed = decision.change.observed
    expected = (
        str(persisted.get("内部标识") or ""), _observed_version(observed),
        str(persisted.get("Canonical source") or ""), str(persisted.get("许可证") or ""),
        str(persisted.get("安全等级") or ""), tuple(str(item) for item in observed.get("evidence_paths", ())), _observed_hash(observed),
    )
    actual = (
        receipt.candidate_id, receipt.fixed_version, receipt.canonical_source, receipt.license,
        receipt.security_grade, receipt.evidence_paths, receipt.fixed_content_hash,
    )
    if actual != expected:
        raise ValueError("Task 7 review 与当前Skill/观察版本不精确绑定")
    return receipt


def _apply_transactionally(ledger: object, history: Mapping[str, Any], change: VersionChange, persisted: Mapping[str, Any]) -> None:
    before = _workbook_bytes(ledger.workbook)
    staged_workbook = load_workbook(BytesIO(before), data_only=False)
    staged_ledger = ledger.__class__(staged_workbook, getattr(ledger, "source_path", None))
    try:
        staged_ledger.append_rows("版本历史", [history])
        updated = dict(persisted)
        updated["固定版本"], updated["固定版本内容指纹"] = _observed_version(change.observed), _observed_hash(change.observed)
        staged_ledger.upsert_skill(updated)
    except Exception:
        staged_workbook.close()
        raise
    previous = ledger.workbook
    ledger.workbook = staged_workbook
    previous.close()


def _workbook_bytes(workbook: object) -> bytes:
    """创建影子工作簿；失败路径从不替换调用者拥有的原对象。"""
    payload = BytesIO()
    workbook.save(payload)
    return payload.getvalue()


def _history_row(change: VersionChange, decision: VersionDecision) -> dict[str, Any]:
    old_version, new_version = _observed_version(change.current), _observed_version(change.observed)
    old_hash, new_hash = _current_hash(change.current), _observed_hash(change.observed)
    if not all((old_version, new_version, old_hash, new_hash)):
        raise ValueError("版本历史缺少旧/新版本或旧/新固定版本内容指纹")
    stable_id = str(change.current.get("内部标识") or "").strip()
    material = "|".join((stable_id, old_version, new_version, old_hash, new_hash))
    evidence = tuple(change.observed.get("evidence_paths", ()))
    return {"版本记录标识": f"version-{sha256(material.encode('utf-8')).hexdigest()[:20]}", "内部标识": stable_id,
            "固定版本": new_version, "变更日期": decision.review_date or date.today().isoformat(),
            "变更摘要": f"旧版本={old_version}；新版本={new_version}；旧哈希={old_hash}；新哈希={new_hash}；结论变化={decision.conclusion_change or '完整复审后接受'}",
            "证据位置": "；".join(str(path) for path in evidence)}


def _append_version_alias_once(ledger: object, change: VersionChange) -> None:
    stable_id, version = str(change.current.get("内部标识") or "").strip(), _observed_version(change.observed)
    if not version:
        return
    source_url = str(change.observed.get("source_url") or change.observed.get("canonical_source") or "").strip()
    alias_id = f"version-alias-{sha256('|'.join((stable_id, version, source_url)).encode('utf-8')).hexdigest()[:16]}"
    if alias_id in {str(row.get("别名标识") or "") for row in ledger.rows("来源别名")}:
        return
    ledger.append_rows("来源别名", [{"别名标识": alias_id, "内部标识": stable_id,
        "来源平台": str(change.observed.get("platform") or change.current.get("来源平台") or ""), "来源地址": source_url,
        "Canonical source": str(change.current.get("Canonical source") or ""), "关系类型": "版本别名观察",
        "去重依据": "固定版本内容指纹一致；仅新增版本标签", "记录日期": str(change.observed.get("observed_on") or date.today().isoformat())}])


def _append_attention_once(ledger: object, change: VersionChange) -> None:
    stable_id, source = str(change.current.get("内部标识") or "").strip(), str(change.current.get("Canonical source") or "").strip()
    observation_id = f"attention-{sha256('|'.join((stable_id, source, 'attention_required')).encode('utf-8')).hexdigest()[:16]}"
    if observation_id in {str(row.get("观察标识") or "") for row in ledger.rows("候选观察")}:
        return
    ledger.append_rows("候选观察", [{"观察标识": observation_id, "候选名称": str(change.current.get("Skill名称") or ""),
        "Canonical source": source, "观察状态": "attention_required", "许可证": str(change.current.get("许可证") or "待确认"),
        "记录日期": str(change.observed.get("observed_on") or date.today().isoformat()), "原因": "上游已删除或不可用；保留既有当前版本和固定快照"}])


def _current_hash(row: Mapping[str, Any]) -> str:
    return _valid_hash(str(row.get("固定版本内容指纹") or ""))


def _observed_hash(row: Mapping[str, Any]) -> str:
    return _valid_hash(str(row.get("content_hash") or row.get("固定版本内容指纹") or ""))


def _observed_version(row: Mapping[str, Any]) -> str:
    return str(row.get("fixed_version") or row.get("固定版本") or "").strip()


def _valid_hash(value: str) -> str:
    return value.casefold() if _SHA256.fullmatch(value.strip()) else ""
