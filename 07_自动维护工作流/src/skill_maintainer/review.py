"""审查包、字段级规则校验和瞬态 stdin 审查输入。"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, BinaryIO, Mapping, TextIO

from .ledger import LedgerStore
from .snapshots import SnapshotManifest


_UNKNOWN_LICENSES = frozenset({"", "待确认", "无许可证声明", "未明确", "未知", "unknown", "n/a", "none", "null", "-"})
_FINAL_STATUSES = frozenset({"全部通过（未实测）", "全部通过（已实测）"})
_LOCAL_PRODUCTS = ("abaqus", "ansys", "matlab", "autocad")


@dataclass(frozen=True)
class ObservedFacts:
    fixed_version: str
    entry_description_complete: bool
    prerequisites_clear_and_available: bool
    license: str
    canonical_source: str
    evidence_paths: tuple[str, ...]
    remote_api_call: str
    remote_endpoints: tuple[str, ...]
    local_professional_software: str
    local_script_plugin_interface: str
    security_grade: str
    verification_status: str


@dataclass(frozen=True)
class ProjectJudgments:
    record_tier: str
    display_in_product: bool
    direct_deployable: bool
    relevance_score: int
    quality_bonus_flags: tuple[bool, ...] = ()


@dataclass(frozen=True)
class DerivedFields:
    quality_score: int | None = None
    ledger_row: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class ReviewDecision:
    observed_facts: ObservedFacts
    project_judgments: ProjectJudgments
    derived_fields: DerivedFields = field(default_factory=DerivedFields)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "ReviewDecision":
        facts = payload.get("observed_facts")
        judgments = payload.get("project_judgments")
        derived = payload.get("derived_fields", {})
        if not isinstance(facts, Mapping) or not isinstance(judgments, Mapping) or not isinstance(derived, Mapping):
            raise ValueError("review decision 必须分为 observed_facts、project_judgments、derived_fields")
        evidence = facts.get("evidence_paths", ())
        endpoints = facts.get("remote_endpoints", ())
        bonuses = judgments.get("quality_bonus_flags", ())
        if isinstance(evidence, str): evidence = (evidence,)
        if isinstance(endpoints, str): endpoints = (endpoints,)
        if isinstance(bonuses, bool): bonuses = (bonuses,)
        if not isinstance(bonuses, (list, tuple)) or not all(isinstance(item, bool) for item in bonuses):
            raise ValueError("project_judgments.quality_bonus_flags 必须为布尔数组")
        return cls(
            ObservedFacts(
                str(facts.get("fixed_version", "")), _required_bool(facts, "entry_description_complete"),
                _required_bool(facts, "prerequisites_clear_and_available"), str(facts.get("license", "")),
                str(facts.get("canonical_source", "")), tuple(str(item) for item in evidence),
                str(facts.get("remote_api_call", "")), tuple(str(item) for item in endpoints),
                str(facts.get("local_professional_software", "")), str(facts.get("local_script_plugin_interface", "")),
                str(facts.get("security_grade", "")), str(facts.get("verification_status", "")),
            ),
            ProjectJudgments(
                str(judgments.get("record_tier", "")), _required_bool(judgments, "display_in_product"),
                _required_bool(judgments, "direct_deployable"), int(judgments.get("relevance_score", 0)),
                tuple(bool(item) for item in bonuses),
            ),
            DerivedFields(derived.get("quality_score"), derived.get("ledger_row")),
        )


@dataclass(frozen=True)
class ReviewPacket:
    candidate_id: str
    fixed_version: str
    rule_versions: Mapping[str, str]
    evidence_paths: tuple[str, ...]
    snapshot_files: tuple[str, ...]


def build_review_packet(candidate: object, snapshot: SnapshotManifest) -> ReviewPacket:
    candidate_id = _candidate_id(candidate) or snapshot.candidate_id
    rule_versions = {
        "SKILL_RESEARCH_WORKFLOW": "1.4 (2026-08-19)",
        "VALIDATION_PROTOCOL": "2026-08-07",
        "SECURITY_REVIEW_PROTOCOL": "2026-08-07",
        "SOURCE_POLICY": "2026-08-07",
        "DATA_DICTIONARY": "2026-08-09",
    }
    return ReviewPacket(candidate_id, snapshot.fixed_version, rule_versions,
                        tuple(dict.fromkeys((*snapshot.source_evidence_paths, *snapshot.evidence_paths))),
                        tuple(item.path for item in snapshot.files))


def validate_review(decision: ReviewDecision, packet: ReviewPacket | None = None) -> tuple[str, ...]:
    """返回稳定的字段级中文错误，决不以项目判断覆盖观测事实。"""
    facts = decision.observed_facts
    judgments = decision.project_judgments
    errors: list[str] = []
    if not facts.fixed_version.strip():
        errors.append("observed_facts.fixed_version: 必须提供固定版本")
    if facts.remote_api_call not in {"是", "否"}:
        errors.append("observed_facts.remote_api_call: 只能为是或否")
    if facts.remote_api_call == "否" and facts.remote_endpoints:
        errors.append("observed_facts.remote_endpoints: remote API 标记为否时不得填写远程端点")
    if facts.remote_api_call == "是" and not facts.remote_endpoints:
        errors.append("observed_facts.remote_endpoints: remote API 标记为是时必须填写远程端点")
    if facts.remote_api_call == "是" and any(product in endpoint.casefold() for endpoint in facts.remote_endpoints for product in _LOCAL_PRODUCTS):
        errors.append("observed_facts.remote_endpoints: 本地专业软件不得填写为远程端点")
    if judgments.record_tier == "正式" and _unknown_license(facts.license):
        errors.append("observed_facts.license: 正式条目许可证未明确")
    if judgments.display_in_product and judgments.relevance_score < 3:
        errors.append("project_judgments.display_in_product: 相关度低于 3/5 不得展示")
    if facts.verification_status == "待核验" and facts.security_grade in {"SA", "SB"}:
        errors.append("observed_facts.security_grade: 待核验不得给出 SA/SB 正式等级")
    if judgments.record_tier == "正式" and facts.verification_status not in _FINAL_STATUSES:
        errors.append("observed_facts.verification_status: 正式条目最低为全部通过（未实测）")
    if judgments.record_tier == "正式" and facts.security_grade not in {"SA", "SB"}:
        errors.append("observed_facts.security_grade: 正式条目安全等级必须为 SA 或 SB")
    if facts.security_grade == "SB-A" and judgments.direct_deployable:
        errors.append("project_judgments.direct_deployable: SB-A 原包不得直接部署")
    if decision.derived_fields.quality_score is not None and decision.derived_fields.quality_score != score_quality(decision):
        errors.append("derived_fields.quality_score: 必须由事实和项目判断重新计算")
    if packet is not None:
        if packet.fixed_version != facts.fixed_version:
            errors.append("observed_facts.fixed_version: 与审查包固定版本不一致")
        if not packet.evidence_paths:
            errors.append("review_packet.evidence_paths: 审查包缺少证据路径")
    return tuple(dict.fromkeys(errors))


def score_quality(decision: ReviewDecision) -> int:
    """四项准入齐备才有基础 1 分；安全、许可证或追溯失败不能用热度抵消。"""
    facts = decision.observed_facts
    if facts.security_grade not in {"SA", "SB"} or _unknown_license(facts.license) or not _traceable(facts):
        return 0
    admission = (
        facts.entry_description_complete,
        facts.prerequisites_clear_and_available,
        not _unknown_license(facts.license),
        _traceable(facts),
    )
    if not all(admission):
        return 0
    return min(5, 1 + sum(1 for item in decision.project_judgments.quality_bonus_flags if item))


def apply_reviews_from_stream(stream: BinaryIO | TextIO, staged_ledger: LedgerStore) -> tuple[ReviewDecision, ...]:
    """读取一次 UTF-8 stdin JSON；只在内存中校验，绝不落地审查 JSON。"""
    raw = stream.read()
    if isinstance(raw, str):
        payload_text = raw
    elif isinstance(raw, bytes):
        payload_text = raw.decode("utf-8", "strict")
    else:
        raise ValueError("审查 stdin 必须提供 UTF-8 JSON")
    payload = json.loads(payload_text)
    if not isinstance(payload, Mapping) or not isinstance(payload.get("decisions", []), list):
        raise ValueError("审查 stdin JSON 必须包含 decisions 数组")
    decisions = tuple(ReviewDecision.from_mapping(item) for item in payload["decisions"] if isinstance(item, Mapping))
    if len(decisions) != len(payload["decisions"]):
        raise ValueError("decisions 中每项必须为对象")
    errors = [error for decision in decisions for error in validate_review(decision)]
    if errors:
        raise ValueError("审查决定校验失败：" + "；".join(errors))
    for decision in decisions:
        if decision.derived_fields.ledger_row is not None:
            staged_ledger.upsert_skill(decision.derived_fields.ledger_row)
    return decisions


def _unknown_license(value: str) -> bool:
    return value.strip().casefold() in _UNKNOWN_LICENSES


def _required_bool(payload: Mapping[str, Any], field_name: str) -> bool:
    value = payload.get(field_name)
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} 必须为 JSON 布尔值")
    return value


def _traceable(facts: ObservedFacts) -> bool:
    return bool(facts.fixed_version.strip() and facts.canonical_source.strip() and facts.evidence_paths)


def _candidate_id(candidate: object) -> str:
    if isinstance(candidate, Mapping):
        return str(candidate.get("candidate_id") or candidate.get("id") or candidate.get("native_id") or "")
    return str(getattr(candidate, "candidate_id", None) or getattr(candidate, "native_id", None) or "")
