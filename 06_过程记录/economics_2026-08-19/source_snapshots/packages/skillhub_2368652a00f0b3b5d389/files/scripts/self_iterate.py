#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fitness-club-digital-ai-expert · Self-Iteration Engine runtime
健身俱乐部数字化 AI 专家 · 自迭代引擎运行时

==================================================================================
This script is the DETERMINISTIC, AUDIT-BEARING layer of the zero-human-intervention
self-iteration engine described in `playbooks/11-self-iteration-sop.md` and gated by
`tools/09-ai-adversarial-consensus-gate.md`. It executes the canonical 7-step pipeline
(Step 1 parse → Step 2 staleness → Step 3 retrieval plan → Step 4 diff proposal →
Step 5 gate → Step 6 apply-or-quarantine → Step 7 hash-chain audit) in DRY-RUN-BY-DEFAULT
mode. Cognitive/retrieval steps (actual web fetch, council deliberation, golden-QA scoring)
are delegated to the Agent; this script enforces the *mechanically checkable* red lines:
hash-chain integrity, change-level classification (L0–L4), HI-1~HI-8 quarantine routing,
confidence threshold, and reversible snapshots.

本脚本是 `playbooks/11` 与 `tools/09` 中「零人为干预自迭代引擎」的**确定性审计层**。
它在 DRY-RUN-BY-DEFAULT 下执行规范七步流水线；需要认知/检索的步骤（真实联网、理事会审议、
黄金问答评分）交由 Agent。本脚本只把可机械判定的红线守死并留痕：哈希链完整、变更级
L0–L4 分类、HI-1~8 隔离路由、置信阈值、可逆快照。

Design boundaries (honesty) / 诚实边界:
  * Stdlib only (Python 3.9+), no network calls — the engine PREPARES the worklist,
    it never fetches the internet itself.  / 仅标准库，不联网——只备工单，不自取。
  * Never touches content `.md` files unless `--apply` is explicitly passed.
    / 除非显式 `--apply`，绝不改内容文件。
  * Never writes outside the skill root.  / 绝不写出 skill 根目录之外。
  * Refuses to run if the skill root cannot be confidently located.
    / 若无法可靠定位 skill 根目录，拒绝运行。

Usage / 用法:
  python3 scripts/self_iterate.py scan                      # read-only 7-step (Steps 1-3)
  python3 scripts/self_iterate.py propose --proposals P.json   # validate + plan (Step 4)
  python3 scripts/self_iterate.py apply   --proposals P.json [--apply] [--consensus-token T]
  python3 scripts/self_iterate.py verify-chain              # validate hash_chain.jsonl
  python3 scripts/self_iterate.py golden-qa                 # emit agent checklist stub
  python3 scripts/self_iterate.py rollback <run_id>         # restore backup snapshot

Author: generated for the fitness-club-digital-ai-expert skill.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# ---------------------------------------------------------------------------
# Paths / 路径（全部派生自 __file__，不依赖 CWD）
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
SCRIPTS_DIR = SCRIPT_PATH.parent                 # <skill>/scripts
SKILL_ROOT = SCRIPTS_DIR.parent                  # <skill> 根
DATA_DIR = SKILL_ROOT / "data"
BACKUPS_DIR = SKILL_ROOT / "backups"
QUARANTINE_DIR = SKILL_ROOT / "quarantine"
HASH_CHAIN = SCRIPTS_DIR / "hash_chain.jsonl"
FRESHNESS_STATE = SCRIPTS_DIR / "freshness_state.json"
GOLDEN_QA = DATA_DIR / "19-golden-qa-benchmark.md"
FRESHNESS_LEDGER = DATA_DIR / "16-freshness-ledger.md"

ENGINE_VERSION = "1.0.0"
GENESIS_HASH = "0" * 64                          # 哈希链创世前哈希

# Skip runtime dirs when parsing content / 解析内容时跳过的运行时目录
SKIP_DIRS = {"backups", "quarantine"}

# Staleness tier → days / 时效级 → 天数（对齐 data/16 §2）
TIER_DAYS = {
    "HIGH": 30, "H": 30, "MED": 90, "MEDIUM": 90, "M": 90,
    "LOW": 180, "L": 180,
}
DEFAULT_STALENESS_DAYS = 90

# HI-adjacent carrier files get a priority flag in the staleness report.
# HI 相邻承载文件在保鲜报告中获优先标记。
PRIORITY_PREFIXES = ("references/10", "references/11", "references/12", "data/02")

# Hard-invariant / compliance keyword signals (for L3+ / L4 routing).
# 硬不变量 / 合规关键词信号（用于 L3+ / L4 路由）。
HI_KEYWORDS = [
    "biometric", "生物识别", "minor", "未成年人", "prepaid", "预付",
    "fire", "消防", "changing room", "更衣室", "shower", "淋", "medical",
    "医疗", "opt-in", "授权", "consent", "同意", "cctv", "监控",
    "surveillance", "data minimization", "数据最小化", "hi-1", "hi-2",
    "hi-3", "hi-4", "hi-5", "hi-6", "hi-7", "hi-8",
]
# Vendor / pricing signals → L1–L2. 供应商/价格信号。
VENDOR_PRICING_KEYWORDS = [
    "vendor", "供应商", "pricing", "价格", "price", "cost", "成本", "fee",
    "费率", "benchmark", "基准", "saas", "procurement", "采购", "quotas",
    "配额", "subscription", "订阅",
]
# Typo / format signals → L0. 错字/格式信号。
TYPO_FORMAT_KEYWORDS = [
    "typo", "错字", "spelling", "拼写", "format", "格式", "punctuation",
    "标点", "whitespace", "空格", "broken link", "断链",
]

# Market → detection keywords (for channel-map lookup in Step 3).
# 市场 → 检测关键词（步骤3通道地图匹配）。
MARKET_KEYWORDS: Dict[str, List[str]] = {
    "cn": ["cn", "china", "中国", "中国大陆"],
    "hk": ["hk", "hong kong", "香港"],
    "tw": ["tw", "taiwan", "台湾"],
    "jp": ["jp", "japan", "日本"],
    "kr": ["kr", "korea", "韩国"],
    "au": ["au", "australia", "澳大利亚"],
    "nz": ["nz", "new zealand", "新西兰"],
    "sg": ["sg", "singapore", "新加坡"],
    "th": ["th", "thailand", "泰国"],
    "my": ["my", "malaysia", "马来西亚"],
    "id": ["id", "indonesia", "印尼"],
    "vn": ["vn", "vietnam", "越南"],
    "in": ["in", "india", "印度"],
}

CONFIDENCE_THRESHOLD = 0.6                       # tools/09 通过阈值


# ---------------------------------------------------------------------------
# Data model / 数据模型
# ---------------------------------------------------------------------------
@dataclass
class Hook:
    """A parsed :::dynamic-hook block. / 一个解析后的动态钩子块。"""
    file: str
    line: int
    topic: str
    stored_value: str = ""
    last_verified: Optional[str] = None          # ISO-ish, may be None
    staleness_raw: str = ""
    staleness_days: int = DEFAULT_STALENESS_DAYS
    action: str = ""
    fallback: str = ""
    body: str = ""
    malformed: bool = False
    warnings: List[str] = field(default_factory=list)

    @property
    def overdue(self) -> Optional[bool]:
        """Return True if past last-verified + staleness_days. None if unknown."""
        if not self.last_verified:
            return None
        d = parse_date(self.last_verified)
        if d is None:
            return None
        due = d + timedelta(days=self.staleness_days)
        return date.today() > due


# ---------------------------------------------------------------------------
# Date parsing / 日期解析
# ---------------------------------------------------------------------------
def parse_date(s: str) -> Optional[date]:
    """Parse several date formats; 'YYYY-MM' is treated as the 1st of the month.
    支持多种格式；'YYYY-MM' 视为当月 1 号（保守：更早到期）。"""
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m", "%Y/%m", "%Y"):
        try:
            d = datetime.strptime(s, fmt).date()
            if fmt in ("%Y-%m", "%Y/%m"):
                return d.replace(day=1)
            if fmt == "%Y":
                return d.replace(month=1, day=1)
            return d
        except ValueError:
            continue
    m = re.search(r"(\d{4})\D+(\d{1,2})\D+(\d{1,2})", s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None


# ---------------------------------------------------------------------------
# Skill-root safety / 根目录安全
# ---------------------------------------------------------------------------
def ensure_skill_root() -> None:
    """Refuse to run if the skill root cannot be confidently located.
    若无法可靠定位 skill 根目录则拒绝运行。"""
    if not SKILL_ROOT.is_dir():
        sys.exit(f"[FATAL] skill root not found / 找不到 skill 根目录: {SKILL_ROOT}")
    if not (DATA_DIR.is_dir() and SCRIPTS_DIR.is_dir()):
        sys.exit(
            "[FATAL] skill root structure unexpected / skill 根目录结构异常 "
            f"(expected {DATA_DIR} and {SCRIPTS_DIR})"
        )


def safe_rel(path: Path) -> str:
    """Return a posix rel-path guaranteed to be inside SKILL_ROOT, else abort.
    返回保证在 SKILL_ROOT 内的相对路径，否则中止。"""
    try:
        rel = path.resolve().relative_to(SKILL_ROOT.resolve())
    except ValueError:
        sys.exit(f"[FATAL] path escapes skill root / 路径逸出根目录: {path}")
    return rel.as_posix()


def within_root(path: Path) -> bool:
    """True if resolved path is inside SKILL_ROOT. / 路径是否在根内。"""
    try:
        path.resolve().relative_to(SKILL_ROOT.resolve())
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Step 1 · Parse hooks / 解析钩子
# ---------------------------------------------------------------------------
HEADER_DATE_RE = re.compile(
    r"Last verified[^:\n]*:\s*(\d{4}[-/]\d{2}(?:[-/]\d{2})?)", re.IGNORECASE)
BLOCK_RE = re.compile(r":::dynamic-hook\b([^\n]*)\n(.*?):::", re.DOTALL)
INLINE_ATTR_RE = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
LINE_KV_RE = re.compile(r"^\s*([\w-]+)\s*[:：]\s*(.+?)\s*$")
STALENESS_FIELD_RE = re.compile(r"(\d+)\s*d\b", re.IGNORECASE)


def parse_header_date(content: str) -> Optional[str]:
    """Extract the file-level 'Last verified' date (first match)."""
    m = HEADER_DATE_RE.search(content)
    return m.group(1) if m else None


def _extract_fields(opening: str, body_lines: List[str]) -> Dict[str, str]:
    """Pull topic/stored-value/last-verified/staleness/action/fallback from
    either inline attributes OR `key: value` lines. Supports BOTH the canonical
    spec format (field-per-line) and the actual inline-attribute format.
    同时支持规范（逐行字段）与真实（行内属性）两种钩子写法。"""
    fields: Dict[str, str] = {}
    # 1) inline attributes on the opening line / 行内属性
    for k, v in INLINE_ATTR_RE.findall(opening):
        fields[k.lower()] = v
    # 2) key: value lines inside the block / 块内逐行字段
    remaining: List[str] = []
    for ln in body_lines:
        m = LINE_KV_RE.match(ln)
        if m:
            key = m.group(1).lower().replace(" ", "-")
            fields.setdefault(key, m.group(2).strip())
            # do not keep recognised field lines in the description body
            if key in ("topic", "stored-value", "stored_value", "last-verified",
                       "last_verified", "staleness", "staleness-days",
                       "staleness_days", "action", "fallback"):
                continue
        remaining.append(ln)
    return fields, remaining


def parse_dynamic_hooks(content: str, rel_file: str) -> Tuple[List[Hook], List[str]]:
    """Walk all :::dynamic-hook blocks in one file. Gracefully skips malformed
    blocks (logs a warning, never crashes). / 解析单文件全部钩子，坏块优雅跳过。"""
    hooks: List[Hook] = []
    warnings: List[str] = []
    for m in BLOCK_RE.finditer(content):
        opening = m.group(1)
        inner = m.group(2)
        start_line = content.count("\n", 0, m.start()) + 1
        body_lines = inner.splitlines()
        try:
            fields, remaining = _extract_fields(opening, body_lines)
        except Exception as exc:  # defensive: never crash on a weird block
            warnings.append(f"{rel_file}:{start_line} malformed block skipped ({exc})")
            continue

        topic = fields.get("topic", "").strip()
        h = Hook(
            file=rel_file,
            line=start_line,
            topic=topic,
            stored_value=fields.get("stored-value", fields.get("stored_value", "")).strip(),
            last_verified=fields.get("last-verified", fields.get("last_verified", "")).strip() or None,
            staleness_raw=fields.get("staleness", "").strip(),
            action=fields.get("action", "").strip(),
            fallback=fields.get("fallback", "").strip(),
            body="\n".join(remaining).strip(),
        )
        if not topic:
            h.malformed = True
            h.warnings.append("missing 'topic' field")
            warnings.append(f"{rel_file}:{start_line} hook missing topic (skipped)")
            continue

        # resolve staleness_days / 解析时效天数
        explicit_days = fields.get("staleness-days", fields.get("staleness_days", "")).strip()
        raw = h.staleness_raw
        if explicit_days:
            try:
                h.staleness_days = int(explicit_days)
            except ValueError:
                h.staleness_days = DEFAULT_STALENESS_DAYS
                h.warnings.append(f"bad staleness-days '{explicit_days}' -> default {DEFAULT_STALENESS_DAYS}")
        elif raw:
            dm = STALENESS_FIELD_RE.search(raw)
            if dm:
                h.staleness_days = int(dm.group(1))
            elif raw.upper() in TIER_DAYS:
                h.staleness_days = TIER_DAYS[raw.upper()]
            else:
                h.staleness_days = DEFAULT_STALENESS_DAYS
                h.warnings.append(f"unknown staleness '{raw}' -> default {DEFAULT_STALENESS_DAYS}")
        else:
            h.staleness_days = DEFAULT_STALENESS_DAYS
            h.warnings.append("no staleness field -> default 90d")
        hooks.append(h)
    return hooks, warnings


def iter_md_files() -> List[Path]:
    """All .md content files under SKILL_ROOT, skipping runtime dirs.
    遍历全部内容 .md，跳过运行时目录。"""
    out: List[Path] = []
    for p in SKILL_ROOT.rglob("*.md"):
        if p.is_dir():
            continue
        rel_parts = p.relative_to(SKILL_ROOT).parts
        if rel_parts and rel_parts[0] in SKIP_DIRS:
            continue
        out.append(p)
    return out


def parse_all() -> Tuple[List[Hook], Dict[str, str], int, List[str]]:
    """Run Step 1 across the library. Returns (hooks, file_dates, volatile_count, warnings).
    全库执行步骤1。返回（钩子, 文件级日期, 🔄计数, 告警）。"""
    hooks: List[Hook] = []
    file_dates: Dict[str, str] = {}
    warnings: List[str] = []
    volatile = 0
    for p in iter_md_files():
        rel = safe_rel(p)
        try:
            content = p.read_text(encoding="utf-8")
        except Exception as exc:
            warnings.append(f"{rel}: read error ({exc})")
            continue
        volatile += content.count("🔄")
        hd = parse_header_date(content)
        if hd:
            file_dates[rel] = hd
        fh, fw = parse_dynamic_hooks(content, rel)
        hooks.extend(fh)
        warnings.extend(fw)
    # backfill per-hook last-verified from the file header / 用文件头回填空缺的末核
    for h in hooks:
        if not h.last_verified and h.file in file_dates:
            h.last_verified = file_dates[h.file]
    return hooks, file_dates, volatile, warnings


# ---------------------------------------------------------------------------
# Step 2 · Staleness scan / 保鲜扫描
# ---------------------------------------------------------------------------
def severity_key(h: Hook) -> Tuple[int, int, int, str]:
    """Sort key: priority files first, overdue first, shorter window first.
    排序键：优先文件在前、逾期在前、时效窗更短（更急）在前。"""
    priority = 0 if h.file.startswith(PRIORITY_PREFIXES) else 1
    od = h.overdue
    overdue_flag = 0 if od is True else (1 if od is False else 2)
    return (priority, overdue_flag, h.staleness_days, h.file)


def staleness_scan(hooks: List[Hook]) -> List[Hook]:
    """Compute overdue set and return hooks sorted by severity.
    计算逾期集并按严重度排序。"""
    return sorted(hooks, key=severity_key)


# ---------------------------------------------------------------------------
# Step 3 · Retrieval plan / 检索计划（不联网，只备工单）
# ---------------------------------------------------------------------------
CHANNEL_ROW_RE = re.compile(r"^\|\s*([a-z]{2})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)
MARKET_DOMAINS: Dict[str, Dict[str, Any]] = {}


def load_channel_map() -> Dict[str, Dict[str, Any]]:
    """Parse data/16 §3.1 per-market official regulator domains (best-effort).
    尽力解析 data/16 §3.1 各市场官方监管域名。"""
    if MARKET_DOMAINS:
        return MARKET_DOMAINS
    if not FRESHNESS_LEDGER.exists():
        return MARKET_DOMAINS
    try:
        text = FRESHNESS_LEDGER.read_text(encoding="utf-8")
    except Exception:
        return MARKET_DOMAINS
    # limit to the §3.1 section for precision
    sec = text
    m = re.search(r"### 3\.1.*?(?=\n###|\Z)", text, re.DOTALL)
    if m:
        sec = m.group(0)
    for rm in CHANNEL_ROW_RE.finditer(sec):
        market = rm.group(1)
        domains = [d.strip() for d in re.split(r"[·•\n]", rm.group(2)) if d.strip()]
        queries = re.findall(r'"([^"]+)"', rm.group(3))
        MARKET_DOMAINS[market] = {"domains": domains, "queries": queries}
    return MARKET_DOMAINS


def detect_market(text: str) -> Optional[str]:
    """Best-effort market detection from free text. / 从文本尽力识别市场。"""
    low = text.lower()
    for market, kws in MARKET_KEYWORDS.items():
        if any(kw in low for kw in kws):
            return market
    return None


def build_retrieval_plan(overdue: List[Hook]) -> List[Dict[str, Any]]:
    """Emit a verification task per overdue hook (topic + suggested query +
    official-source domain from data/16 channel map if parseable).
    为每个逾期钩子生成核验任务（含建议检索式与官方域名，可解析才填）。"""
    cmap = load_channel_map()
    plan: List[Dict[str, Any]] = []
    for h in overdue:
        blob = f"{h.topic} {h.body} {h.file}"
        market = detect_market(blob)
        if market and market in cmap:
            domains = cmap[market]["domains"]
            queries = cmap[market]["queries"] or [h.topic]
        else:
            domains = []
            queries = [h.topic]
        plan.append({
            "topic": h.topic,
            "file": h.file,
            "staleness_days": h.staleness_days,
            "suggested_query": " ".join(queries[:2]) or h.topic,
            "official_domains": domains,
            "action": h.action,
            "fallback": h.fallback,
            "market_detected": market or "n/a",
        })
    return plan


# ---------------------------------------------------------------------------
# Step 4 · Diff proposal schema validation / 差异提案校验
# ---------------------------------------------------------------------------
PROPOSAL_REQUIRED = {"file": str, "old_text": str, "new_text": str, "confidence": (int, float)}
PROPOSAL_OPTIONAL = {"anchor": str, "evidence_url": str, "topic": str}


def validate_proposals(data: Any) -> List[Dict[str, Any]]:
    """Validate the --proposals JSON schema. Raises ValueError on first failure.
    校验提案 JSON schema；首个错误即抛 ValueError。"""
    if not isinstance(data, list):
        raise ValueError("proposals JSON must be a list / 提案须为数组")
    cleaned: List[Dict[str, Any]] = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"proposal[{i}] is not an object")
        for key, typ in PROPOSAL_REQUIRED.items():
            if key not in item:
                raise ValueError(f"proposal[{i}] missing required field '{key}'")
            if not isinstance(item[key], typ):
                raise ValueError(f"proposal[{i}].{key} has wrong type")
        for key, typ in PROPOSAL_OPTIONAL.items():
            if key in item and not isinstance(item[key], typ):
                raise ValueError(f"proposal[{i}].{key} has wrong type")
        conf = float(item["confidence"])
        if not (0.0 <= conf <= 1.0):
            raise ValueError(f"proposal[{i}].confidence out of range [0,1]")
        cleaned.append(item)
    return cleaned


# ---------------------------------------------------------------------------
# Step 5 · Gate classification (L0–L4 heuristic) / 对抗共识门级别判定
# ---------------------------------------------------------------------------
def classify_gate(prop: Dict[str, Any]) -> Tuple[str, List[str], bool]:
    """Keyword-based L0–L4 classification per tools/09. Returns
    (level, reasons, auto_quarantine). Confidence < 0.6 → quarantine.
    按 tools/09 关键词启发式判 L0–L4，返回（级别, 理据, 是否自动隔离）。"""
    reasons: List[str] = []
    topic = str(prop.get("topic", "")).lower()
    fname = str(prop.get("file", "")).lower()
    new_text = str(prop.get("new_text", "")).lower()
    blob = f"{topic} {fname} {new_text}"

    confidence = float(prop.get("confidence", 0.0))
    if confidence < CONFIDENCE_THRESHOLD:
        reasons.append(f"confidence {confidence} < {CONFIDENCE_THRESHOLD} → quarantine")

    # L4: anything touching SKILL.md invariants / mechanism.
    # L4：触及 SKILL.md 不变量或机制。
    if fname.endswith("skill.md"):
        reasons.append("touches SKILL.md → L4 (human-mandatory)")
        return "L4", reasons, True

    # L3+: HI-1~HI-8 topics / compliance carrier files.
    # L3+：HI 关键词或合规承载文件。
    compliance_file = (
        fname.startswith("data/02") or fname.startswith("references/10")
        or fname.startswith("references/11") or fname.startswith("references/12")
    )
    hi_hit = any(k in blob for k in HI_KEYWORDS)
    if compliance_file or hi_hit:
        level = "L3"
        reasons.append("HI/compliance signal → L3 (needs consensus + golden-QA)")
        return level, reasons, confidence < CONFIDENCE_THRESHOLD

    # L1–L2: vendor / pricing.
    # L1–L2：供应商/价格。
    if any(k in blob for k in VENDOR_PRICING_KEYWORDS):
        level = "L2"
        reasons.append("vendor/pricing signal → L2")
        return level, reasons, confidence < CONFIDENCE_THRESHOLD

    # L0: typo / format only.
    # L0：仅错字/格式。
    if any(k in blob for k in TYPO_FORMAT_KEYWORDS):
        level = "L0"
        reasons.append("typo/format signal → L0")
        return level, reasons, confidence < CONFIDENCE_THRESHOLD

    # default → L1 (fact refresh inside a hook).
    level = "L1"
    reasons.append("default → L1 (fact refresh)")
    return level, reasons, confidence < CONFIDENCE_THRESHOLD


# ---------------------------------------------------------------------------
# Step 6 · Apply or quarantine / 应用或隔离
# ---------------------------------------------------------------------------
def snapshot(affected: List[Path], run_id: str, reason: str) -> Path:
    """Copy only the affected files into backups/<run_id>/ + manifest.json.
    仅复制受影响文件到 backups/<run_id>/ 并写 manifest.json。"""
    dest = BACKUPS_DIR / run_id
    dest.mkdir(parents=True, exist_ok=True)
    manifest = {
        "run_id": run_id,
        "created": datetime.now().isoformat(timespec="seconds"),
        "reason": reason,
        "files": [],
    }
    for f in affected:
        rel = safe_rel(f)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)
        manifest["files"].append(rel)
    (dest / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def apply_proposal(prop: Dict[str, Any]) -> Tuple[bool, str]:
    """Apply one proposal by exact old_text → new_text replacement.
    通过精确 old_text→new_text 替换应用单个提案。"""
    rel = str(prop["file"])
    target = SKILL_ROOT / rel
    if not within_root(target):
        return False, "path escapes skill root"
    if not target.exists():
        return False, f"target file missing: {rel}"
    content = target.read_text(encoding="utf-8")
    old = prop["old_text"]
    new = prop["new_text"]
    if old not in content:
        return False, "old_text not found in target file"
    content = content.replace(old, new, 1)
    target.write_text(content, encoding="utf-8")
    return True, ""


def write_quarantine(prop: Dict[str, Any], level: str, reasons: List[str],
                     status: str, run_id: str) -> Path:
    """Park a rejected/unresolved proposal in quarantine/ as a dated .json.
    将未过闸/未决提案停放 quarantine/ 为带日期 .json。"""
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", str(prop.get("topic", "item")).lower()).strip("-") or "item"
    ts = datetime.now().strftime("%Y%m%d")
    rec = {
        "id": f"{ts}-{slug}",
        "created": datetime.now().isoformat(timespec="seconds"),
        "run_id": run_id,
        "level": level,
        "status": status,                    # pending-human | quarantined-low-confidence | quarantined-needs-consensus | failed-apply
        "gate_reasons": reasons,
        "proposal": {
            "file": prop.get("file"),
            "anchor": prop.get("anchor"),
            "old_text": prop.get("old_text"),
            "new_text": prop.get("new_text"),
            "evidence_url": prop.get("evidence_url"),
            "confidence": prop.get("confidence"),
            "topic": prop.get("topic"),
        },
    }
    out = QUARANTINE_DIR / f"{rec['id']}.json"
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Step 7 · Hash-chain audit / 哈希链审计
# ---------------------------------------------------------------------------
def _record_hash(rec: Dict[str, Any]) -> str:
    """Canonical hash of a chain record (excludes its own _hash).
    记录规范化哈希（排除自身 _hash）。"""
    canon = {
        "timestamp": rec.get("timestamp"),
        "action": rec.get("action"),
        "files_changed": rec.get("files_changed"),
        "sha256": rec.get("sha256"),
        "prev_record_hash": rec.get("prev_record_hash"),
        "run_id": rec.get("run_id"),
    }
    blob = json.dumps(canon, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_chain_record(action: str, files_changed: List[str],
                         run_id: str) -> Dict[str, Any]:
    """Append a tamper-evident record and return it. / 追加防篡改记录并返回。"""
    prev_hash = GENESIS_HASH
    if HASH_CHAIN.exists():
        try:
            last = HASH_CHAIN.read_text(encoding="utf-8").strip().splitlines()[-1]
            prev_hash = json.loads(last).get("_hash", GENESIS_HASH)
        except Exception:
            prev_hash = GENESIS_HASH
    sha_map = {}
    for rel in files_changed:
        p = SKILL_ROOT / rel
        if p.exists():
            sha_map[rel] = _file_sha(p)
    rec = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "action": action,
        "files_changed": files_changed,
        "sha256": sha_map,
        "prev_record_hash": prev_hash,
        "run_id": run_id,
    }
    rec["_hash"] = _record_hash(rec)
    with HASH_CHAIN.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def verify_chain() -> Tuple[bool, List[str]]:
    """Validate the whole hash chain end-to-end. / 端到端校验哈希链。"""
    if not HASH_CHAIN.exists():
        return True, ["hash chain empty / 哈希链为空（视为有效）"]
    errors: List[str] = []
    prev_hash = GENESIS_HASH
    for ln in HASH_CHAIN.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            rec = json.loads(ln)
        except Exception as exc:
            errors.append(f"unparseable line / 无法解析行: {exc}")
            continue
        if rec.get("prev_record_hash") != prev_hash:
            errors.append(f"{rec.get('run_id','?')} prev link broken / 前链断裂 "
                          f"(got {rec.get('prev_record_hash')}, want {prev_hash})")
        computed = _record_hash(rec)
        if rec.get("_hash") != computed:
            errors.append(f"{rec.get('run_id','?')} record hash mismatch / 记录哈希失配")
        prev_hash = rec.get("_hash", prev_hash)
    return (len(errors) == 0), errors


# ---------------------------------------------------------------------------
# freshness_state.json / 运行时状态
# ---------------------------------------------------------------------------
def update_freshness_state(overdue_count: Optional[int] = None,
                           hook_count: Optional[int] = None) -> Dict[str, Any]:
    """Update scripts/freshness_state.json on every run. / 每次运行更新状态。"""
    state: Dict[str, Any] = {
        "last_run": None, "next_due": None, "schedule": "RRULE:FREQ=MONTHLY;BYMONTHDAY=27",
        "overdue_count": 0, "quarantine_count": 0, "hook_count_at_last_scan": None,
        "engine_version": ENGINE_VERSION,
    }
    if FRESHNESS_STATE.exists():
        try:
            state.update(json.loads(FRESHNESS_STATE.read_text(encoding="utf-8")))
        except Exception:
            pass
    today = date.today()
    state["last_run"] = today.isoformat()
    state["next_due"] = (today + timedelta(days=30)).isoformat()
    state["engine_version"] = ENGINE_VERSION
    # quarantine count = .json entries excluding README
    qc = 0
    if QUARANTINE_DIR.is_dir():
        qc = sum(1 for p in QUARANTINE_DIR.glob("*.json")
                 if p.name != "README.md")
    state["quarantine_count"] = qc
    if overdue_count is not None:
        state["overdue_count"] = overdue_count
    if hook_count is not None:
        state["hook_count_at_last_scan"] = hook_count
    FRESHNESS_STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2),
                               encoding="utf-8")
    return state


# ---------------------------------------------------------------------------
# Subcommand implementations / 子命令
# ---------------------------------------------------------------------------
def cmd_scan(args: argparse.Namespace) -> int:
    """Steps 1–3 (read-only). Prints a staleness report + retrieval plan.
    步骤1–3（只读）。打印保鲜报告与检索计划。"""
    print("=== SELF-ITERATION SCAN · 自迭代巡检（read-only / 只读）===")
    hooks, file_dates, volatile, warnings = parse_all()
    ranked = staleness_scan(hooks)
    overdue = [h for h in ranked if h.overdue is True]

    print(f"\n[Step 1] Parsed {len(hooks)} dynamic hooks across "
          f"{len(file_dates)} files · 🔄 volatile markers: {volatile}")
    if warnings:
        print(f"  ⚠ warnings / 告警 ({len(warnings)}):")
        for w in warnings[:20]:
            print(f"    - {w}")
        if len(warnings) > 20:
            print(f"    … +{len(warnings) - 20} more")

    print(f"\n[Step 2] Staleness scan / 保鲜扫描 — OVERDUE: {len(overdue)}")
    print("  priority files (HI-adjacent): " + ", ".join(PRIORITY_PREFIXES))
    if overdue:
        print("  --- OVERDUE / 逾期 ---")
        for h in overdue:
            pri = " [PRIORITY]" if h.file.startswith(PRIORITY_PREFIXES) else ""
            print(f"  🔴 {h.file}:{h.line}  {h.topic}  "
                  f"(last {h.last_verified}, +{h.staleness_days}d){pri}")
    fresh = [h for h in ranked if h.overdue is False]
    unknown = [h for h in ranked if h.overdue is None]
    print(f"  ✅ fresh / 新鲜: {len(fresh)}   "
          f"❓ unknown (no date) / 无日期: {len(unknown)}")

    plan = build_retrieval_plan(overdue)
    print(f"\n[Step 3] Retrieval plan / 检索计划 — {len(plan)} verification tasks "
          f"(engine does NOT fetch; this is the Agent worklist):")
    for t in plan:
        dom = ", ".join(t["official_domains"]) if t["official_domains"] else "n/a (use tools/04 general)"
        print(f"  · {t['topic']}")
        print(f"      query / 检索式: {t['suggested_query']}")
        print(f"      market / 市场: {t['market_detected']}  domains / 域名: {dom}")

    # update runtime state (allowed side-effect; no content touched)
    update_freshness_state(overdue_count=len(overdue), hook_count=len(hooks))
    print(f"\n[state] wrote scripts/freshness_state.json · overdue={len(overdue)} "
          f"· hooks={len(hooks)} · quarantine={_quarantine_count()}")
    print("SCAN complete / 巡检完成（read-only，未改动任何内容文件）。")
    return 0


def cmd_propose(args: argparse.Namespace) -> int:
    """Step 4 — validate proposals and print the prepared plan (no writes).
    步骤4 — 校验提案并打印预备计划（不写）。"""
    print("=== PROPOSE · 差异提案校验（dry / 不写）===")
    data = json.loads(Path(args.proposals).read_text(encoding="utf-8"))
    props = validate_proposals(data)
    print(f"  ✅ schema valid / 校验通过: {len(props)} proposals")
    for p in props:
        level, reasons, _ = classify_gate(p)
        print(f"  · {p.get('topic', p['file'])}  → level {level}  conf={p['confidence']}")
        for r in reasons:
            print(f"      - {r}")
    print("PROPOSE complete / 提案校验完成（未落地，待 apply --apply）。")
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    """Steps 5–6 — gate + apply-or-quarantine. Writes only with --apply.
    步骤5–6 — 闸门 + 应用/隔离。仅 --apply 时写入。"""
    print("=== APPLY · 应用或隔离 ===")
    data = json.loads(Path(args.proposals).read_text(encoding="utf-8"))
    props = validate_proposals(data)
    run_id = datetime.now().strftime("%Y-%m-%d-%H%M")

    to_apply: List[Tuple[Dict[str, Any], str]] = []
    to_quarantine: List[Tuple[Dict[str, Any], str, List[str], str]] = []

    for p in props:
        level, reasons, auto_q = classify_gate(p)
        conf = float(p["confidence"])
        if auto_q or level == "L4":
            status = "pending-human" if level == "L4" else "quarantined-low-confidence"
            to_quarantine.append((p, level, reasons, status))
        elif level == "L3":
            if args.consensus_token and conf >= CONFIDENCE_THRESHOLD:
                to_apply.append((p, level))
            else:
                to_quarantine.append((p, level, reasons, "quarantined-needs-consensus"))
        else:  # L0/L1/L2
            if conf >= CONFIDENCE_THRESHOLD:
                to_apply.append((p, level))
            else:
                to_quarantine.append((p, level, reasons, "quarantined-low-confidence"))

    print(f"  plan / 计划: apply={len(to_apply)}  quarantine={len(to_quarantine)}")
    for p, level in to_apply:
        print(f"    → APPLY {level}: {p.get('topic', p['file'])}")
    for p, level, reasons, status in to_quarantine:
        print(f"    → QUARANTINE [{status}] {level}: {p.get('topic', p['file'])}")

    if not args.apply:
        print("\n[DRY-RUN] no files written / 未写入（需 --apply 才落地）。")
        update_freshness_state()
        return 0

    # ---- actually apply / 真正落地 ----
    affected: List[Path] = []
    applied_files: List[str] = []
    failed: List[str] = []
    for p, level in to_apply:
        tgt = SKILL_ROOT / str(p["file"])
        if tgt not in affected:
            affected.append(tgt)
    if affected:
        snapshot(affected, run_id, reason=f"pre-apply snapshot for {len(to_apply)} proposal(s)")
        print(f"  📸 snapshot / 快照: backups/{run_id}/")
    for p, level in to_apply:
        ok, msg = apply_proposal(p)
        if ok:
            applied_files.append(str(p["file"]))
            print(f"    ✅ applied / 已应用: {p['file']}")
        else:
            failed.append(f"{p['file']}: {msg}")
            print(f"    ❌ failed / 失败: {p['file']} ({msg})")
            # route failed apply to quarantine
            to_quarantine.append((p, level, [f"apply failed: {msg}"], "failed-apply"))
    for p, level, reasons, status in to_quarantine:
        out = write_quarantine(p, level, reasons, status, run_id)
        print(f"    ⛔ quarantined / 隔离: {out.name}")

    if applied_files:
        append_chain_record("APPLY", applied_files, run_id)
        print(f"  🔗 hash-chain record appended / 哈希链已记: run_id={run_id}")
    if failed:
        print("  ⚠ some applies failed — see quarantine / 部分应用失败，见隔离区。")
    update_freshness_state()
    return 0


def cmd_verify_chain(args: argparse.Namespace) -> int:
    """Step 7 — validate the hash chain. / 步骤7 — 校验哈希链。"""
    print("=== VERIFY-CHAIN · 哈希链校验 ===")
    ok, errors = verify_chain()
    if ok:
        print("  ✅ chain valid / 链完整可溯源（防篡改）。")
        return 0
    print("  ❌ chain broken / 链断裂:")
    for e in errors:
        print(f"    - {e}")
    return 2


def cmd_golden_qa(args: argparse.Namespace) -> int:
    """Golden-QA stub: extract QA ids from data/19 and emit an agent checklist.
    黄金问答桩：抽取 data/19 问答 id 并产出 Agent 待填清单。"""
    print("=== GOLDEN-QA · 黄金问答回归（orchestration stub / 编排桩）===")
    if not GOLDEN_QA.exists():
        print(f"  ⚠ {GOLDEN_QA.name} missing / 缺失 — cannot extract.")
        return 1
    text = GOLDEN_QA.read_text(encoding="utf-8")
    qa_ids = re.findall(r"#(gqa-\d+)", text)
    print(f"  extracted / 抽取 {len(qa_ids)} QA ids from data/19")
    checklist = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "source": "data/19-golden-qa-benchmark.md",
        "engine_version": ENGINE_VERSION,
        "note": ("Agent fills 'agent_score' and 'pass' per tools/09 scoring rubric; "
                 "the script only orchestrates. / Agent 按 tools/09 评分规则填 agent_score 与 pass；脚本仅编排。"),
        "items": [
            {"id": qid, "question": "", "required_elements": "",
             "agent_score": None, "pass": None, "notes": ""}
            for qid in qa_ids
        ],
    }
    out = SCRIPTS_DIR / "golden_qa_checklist.json"
    out.write_text(json.dumps(checklist, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  📝 checklist emitted / 清单已生成: scripts/golden_qa_checklist.json")
    print("  (scoring is agent work; re-run after filling to trigger rollback if needed)")
    update_freshness_state()
    return 0


def cmd_rollback(args: argparse.Namespace) -> int:
    """Restore a backup snapshot by run_id. / 按 run_id 恢复备份快照。"""
    print(f"=== ROLLBACK · 回滚 → {args.run_id} ===")
    snap = BACKUPS_DIR / args.run_id
    if not snap.is_dir():
        print(f"  ❌ snapshot not found / 快照不存在: backups/{args.run_id}")
        return 1
    manifest_path = snap / "manifest.json"
    files: List[str] = []
    if manifest_path.exists():
        try:
            files = json.loads(manifest_path.read_text(encoding="utf-8")).get("files", [])
        except Exception:
            files = []
    restored: List[str] = []
    if files:
        for rel in files:
            src = snap / rel
            dst = SKILL_ROOT / rel
            if src.exists() and within_root(dst):
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                restored.append(rel)
    else:  # fall back to whatever is in the snapshot dir
        for src in snap.rglob("*"):
            if src.is_file() and src.name != "manifest.json":
                rel = safe_rel(src)
                dst = SKILL_ROOT / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                restored.append(rel)
    append_chain_record("ROLLBACK", restored, args.run_id)
    print(f"  ✅ restored / 已恢复 {len(restored)} files · hash-chain ROLLBACK recorded")
    update_freshness_state()
    return 0


def _quarantine_count() -> int:
    if not QUARANTINE_DIR.is_dir():
        return 0
    return sum(1 for p in QUARANTINE_DIR.glob("*.json") if p.name != "README.md")


# ---------------------------------------------------------------------------
# CLI / 命令行
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="self_iterate.py",
        description="Fitness-club self-iteration engine (DRY-RUN-BY-DEFAULT). "
                    "健身俱乐部自迭代引擎（默认只读）。")
    sub = ap.add_subparsers(dest="command")

    p_scan = sub.add_parser("scan", help="Steps 1-3 read-only staleness scan + retrieval plan.")
    p_scan.set_defaults(func=cmd_scan)

    p_prop = sub.add_parser("propose", help="Step 4: validate a --proposals JSON (dry).")
    p_prop.add_argument("--proposals", required=True, help="Path to proposals JSON file.")
    p_prop.set_defaults(func=cmd_propose)

    p_app = sub.add_parser("apply", help="Steps 5-6: gate + apply-or-quarantine.")
    p_app.add_argument("--proposals", required=True, help="Path to proposals JSON file.")
    p_app.add_argument("--apply", action="store_true", help="Actually write (else dry-run).")
    p_app.add_argument("--consensus-token", default=None,
                       help="AI adversarial gate approval token (required for L3 apply).")
    p_app.set_defaults(func=cmd_apply)

    p_vc = sub.add_parser("verify-chain", help="Step 7: validate the hash chain.")
    p_vc.set_defaults(func=cmd_verify_chain)

    p_gq = sub.add_parser("golden-qa", help="Emit golden-QA agent checklist stub.")
    p_gq.set_defaults(func=cmd_golden_qa)

    p_rb = sub.add_parser("rollback", help="Restore a backup snapshot by run_id.")
    p_rb.add_argument("run_id", help="Snapshot timestamp, e.g. 2026-07-28-1430.")
    p_rb.set_defaults(func=cmd_rollback)

    return ap


def main(argv: Optional[List[str]] = None) -> int:
    ensure_skill_root()
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
