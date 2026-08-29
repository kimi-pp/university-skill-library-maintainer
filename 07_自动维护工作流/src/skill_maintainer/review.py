"""审查包、字段级规则校验和瞬态 stdin 审查输入。"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from typing import Any, BinaryIO, Mapping, TextIO
import weakref

from openpyxl import load_workbook

from .ledger import LedgerStore
from .snapshots import SnapshotManifest, clear_snapshot_run_state, consume_trusted_snapshot


_UNKNOWN_LICENSES = frozenset({"", "待确认", "无许可证声明", "未明确", "未知", "unknown", "n/a", "none", "null", "-"})
_FINAL_STATUSES = frozenset({"全部通过（未实测）", "全部通过（已实测）"})
_LOCAL_PRODUCTS = ("abaqus", "ansys", "matlab", "autocad")
_RECORD_TIERS = frozenset({"正式推荐", "条件候选", "需适配候选"})
_OUTCOMES = frozenset({"include", "exclude"})
_LEGACY_RECORD_TIERS = {"正式": "正式推荐"}
_SHA256 = re.compile(r"[0-9a-f]{64}", re.IGNORECASE)


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
    outcome: str = "include"
    exclusion_reason_code: str = ""
    exclusion_reason: str = ""


@dataclass(frozen=True)
class DerivedFields:
    quality_score: int | None = None
    ledger_row: Mapping[str, Any] | None = None
    scope_mappings: tuple[Mapping[str, Any], ...] = ()


@dataclass(frozen=True)
class ReviewDecision:
    observed_facts: ObservedFacts
    project_judgments: ProjectJudgments
    derived_fields: DerivedFields = field(default_factory=DerivedFields)
    candidate_id: str = ""

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
        scope_mappings = derived.get("scope_mappings", ())
        if isinstance(evidence, str): evidence = (evidence,)
        if isinstance(endpoints, str): endpoints = (endpoints,)
        if isinstance(bonuses, bool): bonuses = (bonuses,)
        if not isinstance(bonuses, (list, tuple)) or not all(isinstance(item, bool) for item in bonuses):
            raise ValueError("project_judgments.quality_bonus_flags 必须为布尔数组")
        if not isinstance(scope_mappings, (list, tuple)) or not all(isinstance(item, Mapping) for item in scope_mappings):
            raise ValueError("derived_fields.scope_mappings 必须为对象数组")
        candidate_id = str(payload.get("candidate_id", "")).strip()
        if not candidate_id:
            raise ValueError("review_decision.candidate_id: 必须提供非空候选标识")
        tier = str(judgments.get("record_tier", ""))
        tier = _LEGACY_RECORD_TIERS.get(tier, tier)
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
                tier, _required_bool(judgments, "display_in_product"),
                _required_bool(judgments, "direct_deployable"), int(judgments.get("relevance_score", 0)),
                tuple(bool(item) for item in bonuses), str(judgments.get("outcome", "include")),
                str(judgments.get("exclusion_reason_code", "")), str(judgments.get("exclusion_reason", "")),
            ),
            DerivedFields(
                derived.get("quality_score"), derived.get("ledger_row"),
                tuple(dict(item) for item in scope_mappings),
            ),
            candidate_id,
        )


@dataclass(frozen=True)
class ReviewPacket:
    candidate_id: str
    fixed_version: str
    canonical_source: str
    license: str
    security_grade: str
    rule_versions: Mapping[str, str]
    evidence_paths: tuple[str, ...]
    snapshot_files: tuple[str, ...]
    fixed_content_hash: str
    upstream_repository: str = ""
    skill_entry_path: str = ""
    approved_scopes: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class AppliedReview:
    """由已验证的审查应用边界签发的、单次可消费的运行时收据。"""

    candidate_id: str
    fixed_version: str
    canonical_source: str
    license: str
    security_grade: str
    evidence_paths: tuple[str, ...]
    fixed_content_hash: str
    ledger_row_sha256: str = ""


@dataclass
class _ReceiptRecord:
    receipt: weakref.ReferenceType[AppliedReview]
    facts: tuple[object, ...]


@dataclass
class _PacketRecord:
    packet: weakref.ReferenceType[ReviewPacket]
    facts: tuple[object, ...]
    owner: weakref.ReferenceType[object] | None = None


_APPLIED_REVIEW_RECEIPTS: dict[int, _ReceiptRecord] = {}
_TRUSTED_REVIEW_PACKETS: dict[int, _PacketRecord] = {}


def build_review_packet(candidate: object, snapshot: SnapshotManifest) -> ReviewPacket:
    supplied_candidate_id = _candidate_id(candidate)
    candidate_id = supplied_candidate_id or snapshot.candidate_id
    canonical_source = _candidate_value(candidate, "canonical_source", "canonical_source_hint")
    license_name = _candidate_value(candidate, "license")
    security_grade = _candidate_value(candidate, "security_grade")
    upstream_repository = _candidate_value(candidate, "upstream_repository") or canonical_source
    skill_entry_path = _candidate_value(candidate, "skill_entry_path")
    raw_scopes = candidate.get("approved_scopes", ()) if isinstance(candidate, Mapping) else getattr(candidate, "approved_scopes", ())
    approved_scopes = tuple((str(item[0]), str(item[1])) for item in raw_scopes if isinstance(item, (list, tuple)) and len(item) == 2)
    if not candidate_id.strip():
        raise ValueError("review_packet.candidate_id: 必须提供非空候选标识")
    if supplied_candidate_id and supplied_candidate_id != snapshot.candidate_id:
        raise ValueError("review_packet.candidate_id: 必须与快照候选标识一致")
    if not all((canonical_source, license_name, security_grade)):
        raise ValueError("审查包必须包含 canonical source、许可证和安全等级事实")
    rule_versions = {
        "SKILL_RESEARCH_WORKFLOW": "1.4 (2026-08-19)",
        "VALIDATION_PROTOCOL": "2026-08-07",
        "SECURITY_REVIEW_PROTOCOL": "2026-08-07",
        "SOURCE_POLICY": "2026-08-07",
        "DATA_DICTIONARY": "2026-08-09",
    }
    trusted_snapshot = consume_trusted_snapshot(snapshot)
    packet = ReviewPacket(candidate_id, trusted_snapshot.fixed_version, canonical_source, license_name, security_grade, rule_versions,
                        tuple(dict.fromkeys((*trusted_snapshot.source_evidence_paths, *trusted_snapshot.evidence_paths))),
                        tuple(item.path for item in trusted_snapshot.files), trusted_snapshot.fixed_content_hash,
                        upstream_repository, skill_entry_path, approved_scopes)
    _register_packet(packet)
    return packet


def validate_review(decision: ReviewDecision, packet: ReviewPacket | None = None) -> tuple[str, ...]:
    """返回稳定的字段级中文错误，决不以项目判断覆盖观测事实。"""
    facts = decision.observed_facts
    judgments = decision.project_judgments
    errors: list[str] = []
    if not decision.candidate_id.strip():
        errors.append("review_decision.candidate_id: 必须提供非空候选标识")
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
    excluded = judgments.outcome == "exclude"
    if judgments.outcome not in _OUTCOMES:
        errors.append("project_judgments.outcome: 只能为 include 或 exclude")
    if judgments.record_tier not in _RECORD_TIERS:
        errors.append("project_judgments.record_tier: 只能为正式推荐、条件候选或需适配候选")
    if excluded:
        if judgments.display_in_product or judgments.direct_deployable:
            errors.append("project_judgments.outcome: 排除项必须 display=false 且 direct=false")
        if not judgments.exclusion_reason_code.strip() or not judgments.exclusion_reason.strip():
            errors.append("project_judgments.exclusion_reason: 排除项必须提供结构化原因代码和中文说明")
        if judgments.exclusion_reason.strip() and not re.search(r"[\u4e00-\u9fff]", judgments.exclusion_reason):
            errors.append("project_judgments.exclusion_reason: 必须提供中文说明")
    elif facts.security_grade == "X":
        errors.append("observed_facts.security_grade: X/禁止风险只能排除")
    elif not judgments.display_in_product:
        errors.append("project_judgments.display_in_product: include 结论必须展示；非展示项应使用排除结论")
    if not excluded and judgments.record_tier == "正式推荐" and _unknown_license(facts.license):
        errors.append("observed_facts.license: 正式条目许可证未明确")
    if not excluded and judgments.display_in_product and judgments.relevance_score < 3:
        errors.append("project_judgments.display_in_product: 相关度低于 3/5 不得展示")
    if facts.verification_status == "待核验" and facts.security_grade in {"SA", "SB"}:
        errors.append("observed_facts.security_grade: 待核验不得给出 SA/SB 正式等级")
    if not excluded and judgments.record_tier == "正式推荐" and facts.verification_status not in _FINAL_STATUSES:
        errors.append("observed_facts.verification_status: 正式条目最低为全部通过（未实测）")
    if not excluded and judgments.record_tier == "正式推荐" and facts.security_grade not in {"SA", "SB"}:
        errors.append("observed_facts.security_grade: 正式条目安全等级必须为 SA 或 SB")
    if not excluded and facts.security_grade == "SB-A" and judgments.direct_deployable:
        errors.append("project_judgments.direct_deployable: SB-A 原包不得直接部署")
    if not excluded and judgments.record_tier in {"条件候选", "需适配候选"} and judgments.direct_deployable:
        errors.append("project_judgments.direct_deployable: 条件候选和需适配候选不得直接部署")
    if not excluded and judgments.record_tier == "正式推荐" and not judgments.direct_deployable:
        errors.append("project_judgments.direct_deployable: 正式推荐必须可直接部署")
    if decision.derived_fields.quality_score is not None and decision.derived_fields.quality_score != score_quality(decision):
        errors.append("derived_fields.quality_score: 必须由事实和项目判断重新计算")
    if packet is not None:
        if not packet.candidate_id.strip():
            errors.append("review_packet.candidate_id: 必须提供非空候选标识")
        if packet.candidate_id != decision.candidate_id:
            errors.append("review_packet.candidate_id: 与审查决定候选标识不一致")
        if packet.fixed_version != facts.fixed_version:
            errors.append("observed_facts.fixed_version: 与审查包固定版本不一致")
        if not _valid_hash(packet.fixed_content_hash):
            errors.append("review_packet.fixed_content_hash: 必须为精确 64 位十六进制 SHA-256")
        if not packet.evidence_paths:
            errors.append("review_packet.evidence_paths: 审查包缺少证据路径")
        if packet.canonical_source != facts.canonical_source:
            errors.append("observed_facts.canonical_source: 与审查包来源不一致")
        if packet.license != facts.license:
            errors.append("observed_facts.license: 与审查包许可证不一致")
        if packet.security_grade != facts.security_grade:
            errors.append("observed_facts.security_grade: 与审查包安全等级不一致")
        if not set(facts.evidence_paths).issubset(packet.evidence_paths):
            errors.append("observed_facts.evidence_paths: 未全部包含在审查包证据路径中")
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


def apply_reviews_from_stream(
    stream: BinaryIO | TextIO,
    staged_ledger: LedgerStore,
    review_packets: Mapping[str, ReviewPacket],
    *, packet_owner: object | None = None,
) -> tuple[AppliedReview, ...]:
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
    errors: list[str] = []
    for decision in decisions:
        packet = review_packets.get(decision.candidate_id)
        if not _trusted_review_packet(packet, owner=packet_owner):
            errors.append("review_packet: 缺少受信且匹配候选的审查包")
            continue
        errors.extend(validate_review(decision, packet))
        errors.extend(_validate_ledger_row_binding(decision, packet))
        errors.extend(_validate_scope_mappings(decision, packet))
    if errors:
        raise ValueError("审查决定校验失败：" + "；".join(errors))
    payload = BytesIO()
    staged_ledger.workbook.save(payload)
    shadow_workbook = load_workbook(BytesIO(payload.getvalue()), data_only=False)
    shadow = LedgerStore(shadow_workbook, staged_ledger.source_path)
    receipts: list[AppliedReview] = []
    try:
        for decision in decisions:
            row = decision.derived_fields.ledger_row
            if decision.project_judgments.outcome == "exclude":
                shadow.upsert_candidate_observation(_exclusion_row(decision, review_packets[decision.candidate_id]))
            elif row is not None and decision.project_judgments.record_tier == "正式推荐":
                shadow.upsert_skill(decision.derived_fields.ledger_row)
            elif row is not None:
                shadow.upsert_candidate_observation(row)
            for mapping in decision.derived_fields.scope_mappings:
                shadow.upsert_professional_task_mapping(mapping)
    except Exception:
        shadow_workbook.close()
        raise
    for decision in decisions:
        if decision.project_judgments.outcome == "include" and decision.project_judgments.record_tier == "正式推荐":
            receipts.append(_issue_applied_review(decision, review_packets[decision.candidate_id]))
    previous = staged_ledger.workbook
    staged_ledger.workbook = shadow_workbook
    previous.close()
    return tuple(receipts)


def validate_applied_review(receipt: object) -> AppliedReview:
    """验证收据确由本模块的实际应用边界签发且尚未消费。"""
    record = _APPLIED_REVIEW_RECEIPTS.get(id(receipt))
    if record is None or record.receipt() is not receipt:
        raise ValueError("trusted Task 7 review receipt is required and unused")
    if _receipt_facts(receipt) != record.facts:
        raise ValueError("trusted Task 7 review receipt has been tampered")
    return receipt


def consume_applied_review(receipt: object) -> None:
    """只应在版本影子工作簿成功替换后调用，失败重试仍可使用收据。"""
    validated = validate_applied_review(receipt)
    _APPLIED_REVIEW_RECEIPTS.pop(id(validated), None)


def clear_review_run_state(*, packets: tuple[object, ...] | None = None, receipts: tuple[object, ...] | None = None) -> None:
    """清理指定运行对象；无参数只保留给旧调用方的全局测试清理。"""
    if packets is None and receipts is None:
        _TRUSTED_REVIEW_PACKETS.clear()
        _APPLIED_REVIEW_RECEIPTS.clear()
        clear_snapshot_run_state()
        return
    for packet in packets or ():
        _TRUSTED_REVIEW_PACKETS.pop(id(packet), None)
    for receipt in receipts or ():
        _APPLIED_REVIEW_RECEIPTS.pop(id(receipt), None)


def claim_review_packets(packets: tuple[object, ...], owner: object) -> None:
    """Atomically bind trusted packets to one exact coordinator PreparedRun."""
    records: list[_PacketRecord] = []
    for packet in packets:
        record = _TRUSTED_REVIEW_PACKETS.get(id(packet))
        if record is None or record.packet() is not packet or _packet_facts(packet) != record.facts:
            raise ValueError("审查包不是当前进程构建的受信对象")
        claimed = record.owner() if record.owner is not None else None
        if record.owner is not None and claimed is not owner:
            raise ValueError("审查包已绑定另一运行或绑定运行已经终止")
        records.append(record)
    for record in records:
        if record.owner is None:
            record.owner = weakref.ref(owner)


def _issue_applied_review(decision: ReviewDecision, packet: ReviewPacket) -> AppliedReview:
    facts = decision.observed_facts
    receipt = AppliedReview(
        decision.candidate_id, facts.fixed_version, facts.canonical_source, facts.license,
        facts.security_grade, facts.evidence_paths, _valid_hash(packet.fixed_content_hash),
        _mapping_sha256(decision.derived_fields.ledger_row or {}),
    )
    _register_receipt(receipt)
    return receipt


def _receipt_facts(receipt: AppliedReview) -> tuple[object, ...]:
    return (
        receipt.candidate_id, receipt.fixed_version, receipt.canonical_source, receipt.license,
        receipt.security_grade, tuple(receipt.evidence_paths), receipt.fixed_content_hash,
        receipt.ledger_row_sha256,
    )


def _trusted_review_packet(packet: object, *, owner: object | None = None) -> bool:
    record = _TRUSTED_REVIEW_PACKETS.get(id(packet))
    if record is None or record.packet() is not packet or _packet_facts(packet) != record.facts:
        return False
    claimed = record.owner() if record.owner is not None else None
    if owner is None:
        return record.owner is None
    return claimed is owner


def _register_packet(packet: ReviewPacket) -> None:
    identity = id(packet)

    def _discard(reference: weakref.ReferenceType[ReviewPacket]) -> None:
        record = _TRUSTED_REVIEW_PACKETS.get(identity)
        if record is not None and record.packet is reference:
            _TRUSTED_REVIEW_PACKETS.pop(identity, None)

    _TRUSTED_REVIEW_PACKETS[identity] = _PacketRecord(weakref.ref(packet, _discard), _packet_facts(packet))


def _register_receipt(receipt: AppliedReview) -> None:
    identity = id(receipt)

    def _discard(reference: weakref.ReferenceType[AppliedReview]) -> None:
        record = _APPLIED_REVIEW_RECEIPTS.get(identity)
        if record is not None and record.receipt is reference:
            _APPLIED_REVIEW_RECEIPTS.pop(identity, None)

    _APPLIED_REVIEW_RECEIPTS[identity] = _ReceiptRecord(weakref.ref(receipt, _discard), _receipt_facts(receipt))


def _packet_facts(packet: ReviewPacket) -> tuple[object, ...]:
    return (
        packet.candidate_id, packet.fixed_version, packet.canonical_source, packet.license,
        packet.security_grade, tuple(packet.evidence_paths), tuple(packet.snapshot_files), packet.fixed_content_hash,
        packet.upstream_repository, packet.skill_entry_path, tuple(packet.approved_scopes),
    )


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


def _candidate_value(candidate: object, *names: str) -> str:
    if isinstance(candidate, Mapping):
        for name in names:
            if candidate.get(name):
                return str(candidate[name])
        return ""
    for name in names:
        value = getattr(candidate, name, None)
        if value:
            return str(value)
    return ""


def _valid_hash(value: str) -> str:
    return value.casefold() if _SHA256.fullmatch(value.strip()) else ""


def _mapping_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return sha256(payload.encode("utf-8")).hexdigest()


def _validate_ledger_row_binding(decision: ReviewDecision, packet: ReviewPacket) -> tuple[str, ...]:
    """派生账本行可以补充展示信息，但不得覆盖已审事实、判定或分数。"""
    row = decision.derived_fields.ledger_row
    if decision.project_judgments.outcome == "exclude":
        return () if row is None else ("derived_fields.ledger_row: 排除项不得提供产品候选行",)
    if row is None:
        return ("derived_fields.ledger_row: 展示项必须提供绑定候选身份的台账行",)
    if not isinstance(row, Mapping):
        return ("derived_fields.ledger_row: 必须为对象",)
    facts = decision.observed_facts
    tier = decision.project_judgments.record_tier
    expected = (
        {
            "内部标识": decision.candidate_id,
            "入库层级": "正式",
            "固定版本": facts.fixed_version,
            "固定版本内容指纹": packet.fixed_content_hash,
            "Canonical source": facts.canonical_source,
            "许可证": facts.license,
            "安全等级": facts.security_grade,
            "质量评分": score_quality(decision),
            "验证状态": facts.verification_status,
            "验证证据位置": "；".join(facts.evidence_paths),
            "外部联网/API 调用": facts.remote_api_call,
            "远程服务端点": "；".join(facts.remote_endpoints),
            "本地专业软件或运行时依赖": facts.local_professional_software,
            "本地脚本/插件接口": facts.local_script_plugin_interface,
            "上游项目地址": packet.upstream_repository,
            "Skill入口路径": packet.skill_entry_path,
        }
        if tier == "正式推荐"
        else {
            "观察标识": f"OBS-{decision.candidate_id}-{tier}",
            "内部标识": decision.candidate_id,
            "Canonical source": facts.canonical_source,
            "Skill入口路径": packet.skill_entry_path,
            "许可证": facts.license,
            "观察状态": tier,
            "固定版本": facts.fixed_version,
            "固定版本内容指纹": packet.fixed_content_hash,
            "验证证据位置": "；".join(facts.evidence_paths),
            "显示层级": tier,
        }
    )
    errors = [
        f"derived_fields.ledger_row.{field_name}: 必须与已审事实或判定一致"
        for field_name, value in expected.items()
        if row.get(field_name) != value
    ]
    if tier != "正式推荐":
        for field_name in ("候选名称", "原因", "记录日期"):
            if not str(row.get(field_name) or "").strip():
                errors.append(f"derived_fields.ledger_row.{field_name}: 展示候选必须填写")
        record_date = str(row.get("记录日期") or "").strip()
        if record_date:
            try:
                date.fromisoformat(record_date)
            except ValueError:
                errors.append("derived_fields.ledger_row.记录日期: 必须为 YYYY-MM-DD")
    return tuple(errors)


def _validate_scope_mappings(decision: ReviewDecision, packet: ReviewPacket) -> tuple[str, ...]:
    mappings = decision.derived_fields.scope_mappings
    if decision.project_judgments.outcome == "exclude":
        return () if not mappings else ("derived_fields.scope_mappings: 排除项不得写产品专业映射",)
    if not packet.approved_scopes:
        return ()
    if not mappings:
        return ("derived_fields.scope_mappings: 必须至少提供一个人工确认的批准专业范围映射",)
    approved = set(packet.approved_scopes)
    required = ("映射标识", "内部标识", "专业代码", "专业名称", "专业任务", "输入", "输出", "适用理由", "使用限制", "相关度")
    errors: list[str] = []
    seen: set[str] = set()
    for mapping in mappings:
        for field_name in required:
            if mapping.get(field_name) in (None, ""):
                errors.append(f"derived_fields.scope_mappings.{field_name}: 必须填写")
        stable_id = str(mapping.get("内部标识") or "")
        code = str(mapping.get("专业代码") or "")
        name = str(mapping.get("专业名称") or "")
        expected_id = f"MAP-{decision.candidate_id}-{code}"
        if stable_id != decision.candidate_id:
            errors.append("derived_fields.scope_mappings.内部标识: 必须与候选标识一致")
        if str(mapping.get("映射标识") or "") != expected_id:
            errors.append("derived_fields.scope_mappings.映射标识: 必须由候选标识和专业代码确定")
        if code.startswith("11") or (code, name) not in approved:
            errors.append("derived_fields.scope_mappings.专业代码: 必须属于固定材料批准的非军事专业范围")
        relevance = mapping.get("相关度")
        if isinstance(relevance, bool) or not isinstance(relevance, int) or relevance < 3 or relevance > 5:
            errors.append("derived_fields.scope_mappings.相关度: 必须为 3 至 5")
        if code in seen:
            errors.append("derived_fields.scope_mappings.专业代码: 同一专业范围不得重复")
        seen.add(code)
    return tuple(dict.fromkeys(errors))


def _exclusion_row(decision: ReviewDecision, packet: ReviewPacket) -> dict[str, object]:
    judgments = decision.project_judgments
    facts = decision.observed_facts
    material = "|".join((decision.candidate_id, facts.fixed_version, packet.fixed_content_hash, judgments.exclusion_reason_code))
    return {
        "观察标识": f"excluded-{sha256(material.encode('utf-8')).hexdigest()[:20]}",
        "内部标识": decision.candidate_id,
        "候选名称": "",
        "Canonical source": facts.canonical_source,
        "Skill入口路径": packet.skill_entry_path,
        "观察状态": "排除",
        "许可证": facts.license,
        "记录日期": date.today().isoformat(),
        "原因": f"{judgments.exclusion_reason_code}：{judgments.exclusion_reason}",
        "固定版本": facts.fixed_version,
        "固定版本内容指纹": packet.fixed_content_hash,
        "验证证据位置": "；".join(facts.evidence_paths),
        "原因代码": judgments.exclusion_reason_code,
        "显示层级": "不展示",
    }
