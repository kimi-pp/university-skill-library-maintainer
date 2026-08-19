from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


ECONOMIC_MARKERS = (
    "econom", "econometric", "causal inference", "policy evaluation", "input-output", "cge", "productivity",
    "macroeconomic", "microeconomic", "financial", "finance", "fiscal", "tax", "trade", "tariff", "banking",
    "monetary", "investment", "capital market", "stock", "insurance", "actuar", "credit", "fintech", "labor",
    "energy economics", "environmental economics", "经济", "计量", "因果推断", "政策评估", "财政", "税收", "金融",
    "贸易", "关税", "投资", "资本市场", "银行", "货币政策", "保险", "精算", "信用", "劳动经济", "能源经济",
    "资源环境", "投入产出", "经济统计", "金融审计", "数字贸易", "数字金融",
)
GENERIC_ONLY = (
    "meeting note", "action item", "generic summary", "ppt template", "mobile app design", "career planning",
    "swiss template", "slide template", "会议纪要", "通用办公", "界面设计", "职业规划",
)
HIGHER_ED_MARKERS = ("university", "student", "teacher", "course", "research", "paper", "journal", "thesis", "教学", "科研", "课程", "论文", "期刊")
OFFICIAL_MARKERS = ("openai", "anthropic", "microsoft", "university", "academy", "institute", "大学", "学院", "研究院", "学会")

MAJOR_MARKERS: dict[str, tuple[str, ...]] = {
    "020101": ("business economics", "empirical economics", "econometrics", "economic model", "economic policy", "微观经济", "宏观经济", "计量经济", "经济模型", "经济政策", "经济学实证"),
    "020102": ("economic statistics", "economic indicator", "national accounts", "time series", "statistical figures", "event-study", "causal dag", "经济统计", "国民经济核算", "经济指标", "时间序列", "统计图表"),
    "020103T": ("national economy", "macroeconomic management", "industrial policy", "国民经济管理", "宏观调控", "产业政策"),
    "020104T": ("environmental economics", "resource economics", "carbon pricing", "natural resource", "资源与环境经济", "环境经济", "资源经济", "碳定价"),
    "020105T": ("business economics", "market demand", "pricing strategy", "industrial organization", "商务经济", "市场需求", "定价策略", "产业组织"),
    "020106T": ("energy economics", "energy market", "electricity market", "能源经济", "能源市场", "电力市场"),
    "020107T": ("labor economics", "labour economics", "wage inequality", "employment data", "劳动经济", "工资差距", "就业数据"),
    "020108T": ("quantitative economics", "econometric methods", "input-output", "cge", "forecasting", "dea", "sfa", "productivity measurement", "数量经济", "经济工程", "投入产出", "计量方法", "经济预测", "生产率"),
    "020109T": ("digital economy", "platform economy", "digital industrial", "数字经济", "平台经济", "产业数字化"),
    "020110TK": ("low-altitude economy", "low altitude economy", "aviation economy", "低空经济", "通用航空经济"),
    "020111T": ("environmental audit", "resource audit", "carbon audit", "资源环境审计", "自然资源审计", "碳审计"),
    "020201K": ("public finance", "fiscal policy", "government budget", "public expenditure", "tax incidence", "财政学", "财政政策", "政府预算", "公共支出", "税收归宿"),
    "020202": ("taxation", "tax policy", "tax incidence", "tax compliance", "税收学", "税收政策", "税负", "纳税合规"),
    "020203TK": ("international tax", "cross-border tax", "transfer pricing", "tax treaty", "国际税收", "跨境税收", "转让定价", "税收协定"),
    "020301K": ("financial economics", "monetary policy", "banking", "capital market", "corporate finance", "金融学", "货币政策", "银行业", "资本市场", "公司金融"),
    "020302": ("financial engineering", "derivative pricing", "quantitative finance", "risk-neutral", "金融工程", "衍生品定价", "量化金融"),
    "020303": ("underwriting", "insurance pricing", "insurance claim", "claims analysis", "insurance capital", "insurance financial", "insurance regulatory", "insurance fraud", "insurance product", "premium pricing", "loss reserve", "coverage analysis", "insurance needs analysis", "保险学", "承保", "保险定价", "保险理赔", "寿险理赔", "准备金"),
    "020304": ("investment analysis", "investment memo", "portfolio analysis", "security analysis", "asset pricing", "valuation", "投资分析", "投资组合", "证券分析", "资产定价", "估值"),
    "020305T": ("financial mathematics", "stochastic finance", "option pricing", "mathematical finance", "金融数学", "随机金融", "期权定价"),
    "020306T": ("credit risk", "credit scoring", "credit management", "default prediction", "信用风险", "信用评分", "信用管理", "违约预测"),
    "020307T": ("economics and finance", "financial economics", "macro-finance", "经济与金融", "金融经济"),
    "020308T": ("actuarial", "life contingency", "loss model", "solvency", "精算", "寿险精算", "损失模型", "偿付能力"),
    "020309T": ("internet finance", "online lending", "crowdfunding", "digital payment", "互联网金融", "网络借贷", "众筹", "数字支付"),
    "020310T": ("financial technology", "fintech", "regtech", "digital payment", "blockchain finance", "金融科技", "监管科技", "数字支付", "区块链金融"),
    "020311TK": ("financial audit", "bank audit", "securities audit", "金融审计", "银行审计", "证券审计"),
    "020312TK": ("digital finance", "inclusive digital finance", "digital currency", "数字金融", "数字普惠金融", "数字货币"),
    "020401": ("international trade", "trade policy", "customs", "global value chain", "国际经济与贸易", "国际贸易", "贸易政策", "海关", "全球价值链"),
    "020402": ("trade economics", "domestic trade", "circulation economy", "supply chain trade", "贸易经济", "国内贸易", "流通经济"),
    "020403T": ("development cooperation", "development finance", "foreign aid", "international development", "国际经济发展合作", "发展援助", "发展融资", "国际发展"),
    "020404TK": ("digital trade", "cross-border e-commerce", "trade digitalization", "数字贸易", "跨境电商", "贸易数字化"),
}


def quality_score(row: dict[str, Any]) -> int:
    if not row.get("admission_pass"):
        return 0
    return min(5, 1 + sum(bool(flag) for flag in row.get("bonus_flags", [])))


def _read_skill_text(row: dict[str, Any]) -> str:
    if row.get("skill_text"):
        return str(row["skill_text"])
    for value in row.get("evidence_paths", []):
        path = Path(value)
        if path.name.casefold() == "skill.md" and path.exists():
            try:
                return path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                return ""
    return ""


def _profile_terms(profile: dict[str, Any]) -> list[str]:
    values: list[str] = [str(profile.get("major_name") or "")]
    for field in ("core_learning_domains", "typical_tasks", "inclusion_rules"):
        values.extend(str(value) for value in profile.get(field, []))
    for values_by_language in profile.get("search_terms", {}).values():
        values.extend(str(value) for value in values_by_language)
    terms: set[str] = set()
    for value in values:
        normalized = value.casefold().strip()
        if len(normalized) >= 3:
            terms.add(normalized)
        for token in re.findall(r"[a-z][a-z-]{3,}|[\u3400-\u9fff]{2,8}", normalized):
            if token not in {"analysis", "research", "management", "skills", "数据分析", "政策分析", "专业", "管理"}:
                terms.add(token)
    return sorted(terms, key=lambda term: (-len(term), term))


def _major_match(text: str, profile: dict[str, Any]) -> tuple[int, list[str]]:
    normalized = text.casefold()
    matches = [term for term in _profile_terms(profile) if term in normalized]
    score = sum(3 if " " in term or re.fullmatch(r"[\u3400-\u9fff]{4,}", term) else 1 for term in matches)
    return score, matches[:12]


def _specialized_major_match(identity_text: str, profile: dict[str, Any], discovered: bool) -> tuple[int, list[str]]:
    normalized = identity_text.casefold()
    markers = [marker for marker in MAJOR_MARKERS.get(profile["major_code"], ()) if _marker_present(normalized, marker)]
    if not markers:
        return 0, []
    profile_score, profile_terms = _major_match(identity_text, profile)
    score = 10 * len(markers) + profile_score + (20 if discovered else 0)
    return score, list(dict.fromkeys(markers + profile_terms))[:12]


def _marker_present(normalized: str, marker: str) -> bool:
    if re.search(r"[\u3400-\u9fff]", marker):
        return marker in normalized
    pattern = r"(?<![a-z0-9])" + re.escape(marker) + r"(?![a-z0-9])"
    return bool(re.search(pattern, normalized))


def _domain_workflow_pass(major_code: str, skill_name: str, identity_text: str) -> bool:
    name = skill_name.casefold()
    text = identity_text.casefold()
    if major_code == "020303":
        if any(term in name for term in ("seo", "bureaucracy", "dsm", "epic-note", "logistics", "vendor", "lease", "collection", "settlement agreement", "new-baby", "staff-mapping", "stormproof")):
            return False
        insurance_context = any(term in text for term in ("insurance", "保险", "actuarial", "精算"))
        return insurance_context and any(_marker_present(text, marker) for marker in MAJOR_MARKERS[major_code])
    if major_code == "020311TK":
        return "audit" in name and any(term in text for term in ("financial audit", "bank audit", "securities audit", "金融审计", "银行审计", "证券审计"))
    if major_code == "020109T":
        return any(term in text for term in ("digital economy", "platform economy", "数字经济", "平台经济", "产业数字化"))
    if major_code == "020310T":
        if any(term in name for term in ("content", "template", "ppt", "presales")):
            return False
        return ("fintech" in text or "financial technology" in text or "金融科技" in text) and any(
            term in text for term in ("regulation", "compliance", "payment", "blockchain", "risk", "data", "model", "监管", "合规", "支付", "区块链", "风控", "数据")
        )
    if major_code == "020302":
        return not any(term in name for term in ("interview", "career", "persona"))
    if major_code == "020304":
        return not any(term in name for term in ("career", "agreement", "legal review", "collection"))
    if major_code == "020308T":
        if "ux" in name:
            return False
        return any(term in text for term in ("actuarial", "精算", "life conting", "loss reserve", "loss model", "premium pricing", "寿险", "准备金", "保费定价"))
    return True


def _has_economics_marker(text: str) -> bool:
    normalized = text.casefold()
    return any(marker in normalized for marker in ECONOMIC_MARKERS)


def _description_complete(text: str, description: str) -> bool:
    if len(text.strip()) < 200:
        return False
    normalized = f"{description}\n{text}".casefold()
    goal = bool(description.strip()) or any(token in normalized for token in ("purpose", "goal", "用于", "use when"))
    steps = any(token in normalized for token in ("step", "workflow", "procedure", "步骤", "流程", "method"))
    io = any(token in normalized for token in ("input", "output", "deliverable", "输入", "输出", "report", "dataset", "data"))
    return goal and steps and io


def _active_within_six_months(value: str) -> bool:
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    cutoff = datetime(2026, 2, 19, tzinfo=timezone.utc)
    return moment >= cutoff


def _older_than_eighteen_months(value: str) -> bool:
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    cutoff = datetime(2025, 2, 19, tzinfo=timezone.utc)
    return moment < cutoff


def adjudicate(row: dict[str, Any], profiles: Iterable[dict[str, Any]]) -> dict[str, Any]:
    result = dict(row)
    text = _read_skill_text(result)
    identity_text = "\n".join([str(result.get("skill_name") or ""), str(result.get("skill_description") or "")])
    combined = f"{identity_text}\n{text}"
    profile_map = {profile["major_code"]: profile for profile in profiles}
    requested = [code for code in result.get("major_codes", []) if code in profile_map]
    scored: list[tuple[int, str, list[str]]] = []
    for code in sorted(profile_map):
        score, matches = _specialized_major_match(identity_text, profile_map[code], code in requested)
        if score:
            scored.append((score, code, matches))
    scored.sort(key=lambda item: (-item[0], item[1]))

    normalized = combined.casefold()
    generic_only = any(marker in normalized for marker in GENERIC_ONLY)
    if scored:
        scored = [item for item in scored if _domain_workflow_pass(item[1], str(result.get("skill_name") or ""), identity_text)]
        scored.sort(key=lambda item: (-item[0], item[1]))
    relevance = bool(scored and not generic_only)
    matched_codes = [code for score, code, _ in scored if score >= max(10, scored[0][0] // 2)] if scored else []
    primary_code = scored[0][1] if relevance else ""
    primary_profile = profile_map.get(primary_code, {})

    description_complete = _description_complete(text, str(result.get("skill_description") or ""))
    prerequisites_clear = bool(result.get("local_runtime")) and bool(result.get("local_interface"))
    license_pass = bool(result.get("license_allowed"))
    traceable = bool(result.get("fixed_version") and result.get("canonical_source_key") and result.get("evidence_paths"))
    admission_flags = [description_complete, prerequisites_clear, license_pass, traceable]
    admission_pass = all(admission_flags)

    exclusion: list[str] = []
    if not result.get("formal_eligible"):
        exclusion.extend(str(reason) for reason in result.get("blocking_reasons", []))
    if not relevance:
        exclusion.append("professional_mismatch")
    if not description_complete:
        exclusion.append("incomplete_description")
    if not prerequisites_clear:
        exclusion.append("prerequisites_unclear")
    if not license_pass:
        exclusion.append("license_not_allowed")
    if not traceable:
        exclusion.append("source_not_traceable")
    if result.get("security_grade") not in {"SA", "SB"}:
        exclusion.append("security_grade_not_formal")
    if result.get("external_api") == "是" and result.get("network_behavior") in {"", "无", None}:
        exclusion.append("api_network_inconsistent")
    if _older_than_eighteen_months(str(result.get("maintenance_date") or "")) and int(result.get("repository_stars") or 0) < 10:
        exclusion.append("maintenance_failure")

    chinese = bool(re.search(r"[\u3400-\u9fff]", combined))
    active = _active_within_six_months(str(result.get("maintenance_date") or ""))
    stars = int(result.get("repository_stars") or 0) >= 50
    higher_ed = any(marker in normalized for marker in HIGHER_ED_MARKERS)
    publisher_text = f"{result.get('publisher', '')} {result.get('repository', '')}".casefold()
    official = any(marker in publisher_text for marker in OFFICIAL_MARKERS)
    bonus_flags = [chinese, active, stars, higher_ed, official]

    result.update(
        {
            "skill_text_sha256": result.get("skill_content_sha256"),
            "professional_relevance_pass": relevance,
            "professional_relevance_evidence": [
                {"major_code": code, "major_name": profile_map[code]["major_name"], "matched_terms": matches}
                for _, code, matches in scored[:5]
            ],
            "matched_major_codes": matched_codes if relevance else [],
            "primary_major_code": primary_code,
            "primary_major_name": str(primary_profile.get("major_name") or ""),
            "primary_class_code": str(primary_profile.get("class_code") or ""),
            "admission_flags": {
                "description_complete": description_complete,
                "prerequisites_clear": prerequisites_clear,
                "license_allowed": license_pass,
                "source_traceable": traceable,
            },
            "admission_pass": admission_pass,
            "bonus_flags": bonus_flags,
            "quality_score": 0,
            "verification_status": "全部通过（未实测）" if admission_pass and result.get("formal_eligible") else "静态核验未通过",
            "exclusion_reasons": sorted(set(exclusion)),
        }
    )
    result["quality_score"] = quality_score(result)
    result["formal_included"] = bool(
        result.get("formal_eligible")
        and relevance
        and admission_pass
        and result.get("security_grade") in {"SA", "SB"}
        and result["quality_score"] >= 2
        and not result["exclusion_reasons"]
    )
    if not result["formal_included"] and result["quality_score"] == 1:
        result["exclusion_reasons"] = sorted(set(result["exclusion_reasons"] + ["score_one_observation"]))
    return result


def adjudicate_all(rows: Iterable[dict[str, Any]], profiles: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    profile_list = list(profiles)
    reviewed = [adjudicate(row, profile_list) for row in rows]
    formal = [row for row in reviewed if row["formal_included"]]
    formal.sort(key=lambda row: (row["primary_class_code"], row["primary_major_code"], -row["quality_score"], str(row.get("skill_name") or "").casefold()))
    for index, row in enumerate(formal, start=1):
        row["skill_id"] = f"ECON-SK-{index:04d}"
    excluded = [row for row in reviewed if not row["formal_included"]]
    excluded.sort(key=lambda row: (row.get("primary_class_code", ""), str(row.get("skill_name") or "").casefold(), str(row.get("candidate_key") or "")))

    reason_counts = Counter(reason for row in excluded for reason in row.get("exclusion_reasons", []))
    per_major: dict[str, dict[str, Any]] = {}
    for profile in profile_list:
        code = profile["major_code"]
        discovered = [row for row in reviewed if code in row.get("major_codes", [])]
        included = [row for row in formal if code in row.get("matched_major_codes", [])]
        per_major[code] = {
            "major_name": profile["major_name"],
            "class_code": profile["class_code"],
            "deduplicated_candidate_count": len(discovered),
            "formal_candidate_count": len(included),
            "excluded_candidate_count": len([row for row in discovered if not row["formal_included"]]),
        }
    summary = {
        "schema_version": "economics-adjudication-v1",
        "deduplicated_candidate_count": len(reviewed),
        "formal_candidate_count": len(formal),
        "excluded_candidate_count": len(excluded),
        "exclusion_reason_counts": dict(sorted(reason_counts.items())),
        "per_major": per_major,
    }
    return formal, excluded, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unique", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--formal", type=Path, required=True)
    parser.add_argument("--excluded", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    rows = json.loads(args.unique.read_text(encoding="utf-8"))
    profile_doc = json.loads(args.profiles.read_text(encoding="utf-8"))
    profiles = profile_doc.get("profiles", profile_doc)
    formal, excluded, summary = adjudicate_all(rows, profiles)
    args.formal.write_text(json.dumps(formal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.excluded.write_text(json.dumps(excluded, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary | {"zero_formal_major_count": sum(row["formal_candidate_count"] == 0 for row in summary["per_major"].values())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
