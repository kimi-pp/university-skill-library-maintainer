# Semantic Consistency Scan / 语义一致性扫描（矛盾检测台账）
> **Cluster / 集群**: P4 engine · feeds / 供给: `tools/09` (consensus gate) · `data/06` (term canon) · `data/02` (compliance truth) · `scripts/self_iterate.py`
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: scan runs monthly (P4) + on event; Tier-1 every run; findings re-checked after every L2/L3 apply.
> **Cross-references / 交叉引用**: `data/06` (canon) · `data/16` (freshness) · `data/19` (golden QA) · `tools/09`
> **Retrieval note / 检索提示**: scan surfaces conflicts only — resolution always routes to `tools/05`/`tools/09`, never auto-decided here.
> 本扫描只暴露冲突——解决一律走 `tools/05`/`tools/09`，本文件绝不自作裁决。

---

## 1 · Purpose / 用途
The library is large and multi-authored (auto-generated patches land via `scripts/self_iterate.py`). Over time, two files can drift into contradiction — e.g. one says "face-entry is permitted in market X", another says "face-entry is banned there". This ledger records the **embedding-based cross-library scan** that finds such contradicting statements before a member or operator is misled.
库体量大、多源生成（自动补丁经 `scripts/self_iterate.py` 落库）。时间一长，两份文件可能自相矛盾——如一份说「市场 X 允许人脸入场」，另一份说「该市场禁用人脸」。本台账记录**基于向量的跨库扫描**，在误导会员/运营者前找出这类矛盾。

> **Honesty red line / 诚实红线**: A contradiction finding is a QUESTION, not a verdict. The scan never picks which side is right on HI-adjacent topics; it quarantines and routes to `tools/05` + `tools/09`.
> 诚实红线：矛盾发现是「疑问」而非「裁决」。扫描绝不替 HI 相关主题选边，只隔离并送 `tools/05`+`tools/09`。

---

## 2 · Method Spec / 方法规范
The scan is a deterministic pipeline (run by `scripts/self_iterate.py`, P4):
扫描是确定性流水线（由 `scripts/self_iterate.py` P4 运行）：

1. **Chunk / 切片**: Split every `data/` & `references/` file into 200–400 token chunks; preserve `file#anchor` provenance per chunk. / 把每个 `data/`·`references/` 文件切成 200–400 token 块，每块保留 `文件#锚点` 出处。
2. **Embed / 向量化**: Encode each chunk into a vector via the library embedding model. / 用库内向量模型把每块编成向量。
3. **Nearest-neighbor cross-file pairs / 跨文件近邻配对**: For each chunk, find the top-K most similar chunks that live in a *different* file. / 对每块找跨**不同文件**的最相似 Top-K 块。
4. **Contradiction classifier / 矛盾分类器**: A prompt-classifier scores each cross-file pair for contradiction (0–1) across types: factual, compliance, safety, numeric, terminology. / 用提示分类器对每对跨文件块判矛盾（0–1），分事实/合规/安全/数值/术语类。
5. **Human-readable report / 可读报告**: Emit a finding per pair above threshold (template in §4). / 对超阈值的每对生成发现（模板见 §4）。
6. **Route / 路由**: Per `severity` → gate route (§4) and resolution rules (§5). / 按严重度→闸门路由（§4）与解决规则（§5）。

> Scope canons: Tier-3 uses `data/06` as the authoritative vocabulary; any term not in `data/06` used inconsistently is flagged as terminology drift.
> 范围准则：Tier-3 以 `data/06` 为权威词表；未在 `data/06` 中、却用法不一致的术语标为术语漂移。

---

## 3 · Scan Scope Tiers / 扫描范围分层
| Tier / 层 | Scope / 范围 | Cadence / 频次 | Canon / 权威源 | Auto-route / 自动路由 |
|---|---|---|---|---|
| Tier-1 | Compliance & safety claims (HI-1~HI-8, face-entry, CCTV, minors, prepaid, fire, pool/sauna) / 合规与安全论断 | **Every run** (monthly + event) | `data/02` + `tools/05` | Quarantine + `tools/09` (never auto-pick) |
| Tier-2 | Vendor / pricing / benchmark claims 🔄 / 供应商·价格·基准论断 | Monthly / 月 | `data/03`·`04`·`15` + `tools/04` | DG4 write-back if agreed |
| Tier-3 | Style / terminology drift / 风格·术语漂移 | Quarterly / 季 | `data/06` glossary | Patch to `data/06`; non-HI |

Tier-1 contradictions on HI-adjacent topics are **never auto-resolved** — they park in `quarantine/` pending `tools/05` verification, then `tools/09` consensus.
Tier-1 在 HI 相关主题上的矛盾**绝不自动解决**——先停放 `quarantine/` 待 `tools/05` 核验，再走 `tools/09` 共识。

---

## 4 · Report Format Template / 报告格式模板
Every finding is one row in the scan log (§6) and follows:
每个发现即 §6 扫描日志的一行，遵循：

| Field / 字段 | Meaning / 含义 |
|---|---|
| **Finding ID / 编号** | `SC-YYYYMM-###` (e.g. `SC-202607-001`) |
| **File A / anchor / 文件A·锚点** | `references/12#face-entry-decision` |
| **File B / anchor / 文件B·锚点** | `data/02#kr-pipa-biometric` |
| **Contradiction type / 矛盾类型** | compliance \| safety \| factual \| numeric \| terminology |
| **Severity / 严重度** | CRITICAL (HI-adjacent) \| HIGH \| MED \| LOW |
| **Proposed resolution / 建议解决** | short neutral statement of the conflict + which source decides |
| **Gate route / 闸门路由** | L0–L4 per `tools/09` (CRITICAL/HI → L4 human or quarantine→`tools/05`) |
| **Status / 状态** | OPEN \| QUARANTINED \| RESOLVED \| EXAMPLE |

---

## 5 · Resolution Rules / 解决规则
1. **Safety/compliance contradictions auto-route to quarantine** pending `tools/05` verification. The scan NEVER auto-picks a side on HI-adjacent topics (HI-1 biometric/minors, HI-2 life-safety, HI-3 prepaid, HI-4 fire, HI-5 changing-room imaging, HI-6 medical, HI-7 opt-in, HI-8 minimization).
   **安全/合规矛盾自动进隔离区**待 `tools/05` 核验。扫描在 HI 相关主题上**绝不自动选边**。
2. CRITICAL + HI-adjacent → `quarantine/` + trigger `tools/05` article-level verification + `tools/09` gate; library keeps serving the prior value + "disputed" flag (non-blocking).
   CRITICAL+HI 相关 → `quarantine/` + 触发 `tools/05` 条款级核验 + `tools/09` 闸门；库以旧值+「存疑」标继续服务（非阻塞）。
3. HIGH (non-HI) → 4-agent consensus (`tools/09` L2); on pass, apply + DG4 write-back to `data/16`.
   HIGH（非HI）→ 四 Agent 共识（`tools/09` L2）；通过则应用 + DG4 回写 `data/16`。
4. MED/LOW (vendor/pricing/style) → auto-patch at L1 (lite consensus) if both sides agree with the canon; else escalate.
   MED/LOW（供应商/价格/风格）→ 两侧与权威源一致则 L1 轻共识自动修；否则升级。
5. Terminology drift (Tier-3) → update `data/06` only; never silently rewrite a domain file's meaning.
   术语漂移（Tier-3）→ 只更新 `data/06`；绝不悄悄改写领域文件含义。
6. Every resolution appends to the hash chain (`scripts/self_iterate.py`); golden-QA (`data/19`) regression runs after any L2/L3 apply.
   每次解决追加哈希链；任何 L2/L3 应用后跑黄金问答（`data/19`）回归。

---

## 6 · Scan Log (initial) / 扫描日志（初始）
> The table below is the **initial seed**: 3 EXAMPLE rows show the shape. They are NOT real conflicts — they demonstrate the schema. The first real monthly run populates live rows.
> 下表为**初始种子**：3 个 EXAMPLE 行仅示范形态，非真实冲突。首个真实月度运行填入实行。

| Finding ID / 编号 | File A / anchor | File B / anchor | Type / 类型 | Severity / 严重度 | Proposed resolution / 建议解决 | Gate route / 路由 | Status / 状态 |
|---|---|---|---|---|---|---|---|
| SC-202607-EX1 | `references/12#face-entry-decision` | `data/02#kr-pipa-biometric` | compliance | CRITICAL | One says face-entry allowed with alt; other implies banned — verify via `tools/05` article. / 一侧说有人脸入场替代即可，另一侧暗示全禁——经 `tools/05` 条款核验。 | L4/human + quarantine→`tools/05` | EXAMPLE |
| SC-202607-EX2 | `references/07#ftms-vendors` | `data/04` (vendor row) | numeric | MED | Price range in one file wider than the other — reconcile against `tools/04` scan. / 一侧价格区间比另一侧宽——按 `tools/04` 扫描对账。 | L1 lite | EXAMPLE |
| SC-202607-EX3 | `references/06#crm-def` | `data/06#crm` | terminology | LOW | Term "CRM" used with two scopes — align to `data/06` canon. / 「CRM」两处范围不一——统一到 `data/06` 词表。 | L0 patch | EXAMPLE |

---

## 7 · Cadence & triggers / 频次与触发
- **Monthly (RRULE)**: full Tier-1 + Tier-2 pass; Tier-3 quarterly. / 月度：Tier-1+Tier-2 全过；Tier-3 季。
- **Event-triggered**: after any L2/L3 apply in `tools/09`, and on breaking-regulation alerts from `data/18`. / 事件触发：`tools/09` 任何 L2/L3 应用后，及 `data/18` 突发法规警报。
- **Pre-release**: G1–G13 gate (`tools/03`) reads this log; any OPEN/QUARANTINED HI-adjacent finding blocks release.
  发布前：`tools/03` 的 G 闸读本日志；任何 OPEN/QUARANTINED 的 HI 相关发现阻断发布。

> **G13 tri-perspective note / 三视角注记**: Architect — this scan is the library's immune system; an unreported contradiction is a G12/G13 integrity hole. Operator — treat QUARANTINED rows as "do not cite until cleared". Member — members are the ultimate victims of contradictory safety/compliance advice, so Tier-1 contradictions never reach them unverified.
> **G13 三视角**：架构师——本扫描是库的免疫系统，未报矛盾即 G12/G13 完整性漏洞；运营者——把 QUARANTINED 行当「澄清前勿引用」；会员——会员是矛盾安全/合规建议的终极受害者，故 Tier-1 矛盾绝不以未核验之姿抵达他们。
