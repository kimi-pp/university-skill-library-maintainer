# 3-Year Digital & AI Strategy Document / 三年数字化与 AI 战略文档

> **Cluster / 集群**: I (IT governance & money), L5 (strategy & governance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: IT-spend % of revenue re-verify every 90 days via 🔄 hook; regulation citations pass `tools/05`; vendor/roadmap facts pass `tools/04`. / IT 支出占营收比每 90 天经 🔄 钩复核；法规过 `tools/05`；供应商/路线事实过 `tools/04`。
> **Cross-references / 交叉引用**: `tools/01-fdmm-maturity-assessment.md` (current state) · `tools/07-chief-orchestrator.md` (S1–S8) · `references/05-methodology-library.md` §I · `data/15-procurement-and-cost-benchmark.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04`。

---

## ① Purpose & When to Use / 用途与使用时机 {#purpose}

Use this template to write the club chain's 3-year digital & AI strategy narrative — the single document the board, investors, and the internal digital team align on.
用本模板撰写连锁场馆的三年数字化与 AI 战略叙事——董事会、投资人与内部数字化团队对齐的唯一文档。

> **FDMM level gate / 成熟度闸口**: **Do NOT use this template before FDMM L4** unless the board has explicitly commissioned a forward strategy. An L1–L3 club should first complete `templates/05-fdmm-assessment-worksheet.md` + `templates/02-annual-it-budget.md` and reach a stable L3 (≥2 AI use cases in production with measured ROI) before attempting a 3-year narrative.
> **FDMM 等级闸口**：**FDMM L4 以下不要使用本模板**，除非董事会明确委托前瞻战略。L1–L3 场馆应先完成 `templates/05` + `templates/02`，并稳定达到 L3（≥2 个量产且 ROI 可测的 AI 场景）再谈三年叙事。

> **What good looks like / 好答案长什么样**: the doc names a current FDMM level with evidence, a target level per year, 3–6 initiatives mapped to horizons, a total investment envelope as a % of revenue range, and a governance cadence. No buzzword salad.
> **好答案长什么样**：文档给出带证据的当前 FDMM 等级、逐年目标等级、映射到时区的 3–6 个举措、作为营收占比区间的总投资包、以及治理节奏。无 buzzword 沙拉。

> **Red flag / 红旗**: if the doc says "become an AI-native unmanned chain by year 1" for a paper-club today, it violates Iron Law 7 (evolvable architecture). Send it back.
> **红旗**：若文档对今天的纸表馆写「第一年成为 AI 原生无人连锁」，违反铁律 7（可演进架构）。打回。

---

## ② Prerequisites & Inputs Checklist / 前置条件与输入清单 {#prerequisites}

- [ ] Current FDMM snapshot completed via `tools/01` (six dimensions × L1–L5). / 经 `tools/01` 完成当前 FDMM 快照（六维 × L1–L5）。
- [ ] At least one full annual IT budget (`templates/02`) for baseline spend. / 至少一份完整年度 IT 预算（`templates/02`）作支出基线。
- [ ] Target market list (which of the 12 APAC markets) and club-count projection. / 目标市场清单（12 个亚太市场中哪些）与门店数预测。
- [ ] Compliance red lines acknowledged: HI-1~HI-8 from `SKILL.md`. / 已确认合规红线：见 `SKILL.md` HI-1~HI-8。
- [ ] Board's risk appetite stated in writing (conservative / balanced / aggressive). / 董事会风险偏好书面确认（保守/平衡/激进）。
- [ ] Access to `data/15` for cost ranges and `tools/04` for live vendor/regulation facts. / 可查 `data/15` 成本区间、`tools/04` 实时供应商/法规事实。

---

## ③ The Template / 模板正文 {#template}

### 3.1 Executive Summary / 执行摘要 {#s-exec}

| Field / 字段 | Fill-in / 填写 |
|---|---|
| One-line vision / 一句话愿景 | ___ |
| Current FDMM level / 当前 FDMM 等级 | L__ (evidence: ___) |
| Target FDMM by Y1 / Y1 目标 | L__ |
| Target FDMM by Y2 / Y2 目标 | L__ |
| Target FDMM by Y3 / Y3 目标 | L__ |
| Total 3-yr envelope / 三年总包 | __%–__% of revenue (range) / 占营收区间 |

> **Guidance / 指引**: keep the summary to 8 lines. A board member should understand the bet in 60 seconds.
> **指引**：摘要控制在 8 行内。董事会成员 60 秒读懂下注。

### 3.2 Current-State FDMM Snapshot / 当前状态 FDMM 快照 {#s-current}

> Copy the per-dimension scores from `tools/01`. Do not re-invent ratings here.
> 从 `tools/01` 抄录各维度评分，勿在此重新发明评级。

| Dimension / 维度 | Current / 当前 | Ceiling evidence / 封顶证据 | Biggest gap / 最大缺口 |
|---|---|---|---|
| Member / 会员 | L__ | ___ | ___ |
| Operations / 运营 | L__ | ___ | ___ |
| Infrastructure / 基础设施 | L__ | ___ | ___ |
| Data / 数据 | L__ | ___ | ___ |
| AI / AI | L__ | ___ | ___ |
| Governance / 治理 | L__ | ___ | ___ |

### 3.3 Vision & North-Star Metrics / 愿景与北极星指标 {#s-vision}

- **Vision statement / 愿景陈述**: ___ (one paragraph, format + market specific).
- **North-star metric / 北极星指标** (pick 1–2, not ten):

| Metric / 指标 | Baseline / 基线 | Y1 / 第一年 | Y3 / 第三年 | Source / 来源 |
|---|---|---|---|---|
| e.g. Member retention / 会员留存 | __% | __% | __% | `data/01` |
| e.g. IT cost / revenue / IT 占营收 | __% | __% | __% | `templates/02` |

> **Red flag / 红旗**: more than 3 north-star metrics = none is a north star. Cut.
> **红旗**：北极星指标超过 3 个 = 没有北极星。砍。

### 3.4 Three-Horizon Initiative Map / 三时区举措地图 {#s-horizons}

Map initiatives to horizons: H1 (0–12m, foundation) · H2 (12–24m, scale) · H3 (24–36m, transform).
把举措映射到时区：H1（0–12 月，打底）· H2（12–24 月，扩张）· H3（24–36 月，转型）。

| # | Initiative / 举措 | Horizon / 时区 | FDMM lift / 等级跃升 | Owner / 负责人 | Depends on / 前置 |
|---|---|---|---|---|---|
| 1 | ___ | H1/H2/H3 | L__→L__ | ___ | ___ |
| 2 | ___ | | | | |
| 3 | ___ | | | | |

> **Worked micro-example / 微例**: H1 "Unify member ID across CRM+gate+POS" (L2→L3 foundation). H2 "Churn-AI pilot on retained data" (L3→L4). H3 "Unmanned overnight at 5 low-risk clubs" (L4→L5, only after HI-2 redundancy proven).
> **微例**：H1「CRM+闸机+POS 会员 ID 归一」（L2→L3 打底）。H2「在留存数据上试点流失 AI」（L3→L4）。H3「5 家低风险馆夜间无人」（L4→L5，须先验证 HI-2 冗余）。

### 3.5 Investment Envelope / 投资包 {#s-investment}

:::dynamic-hook topic="it-spend-percent-of-revenue" staleness="90d" action="tools/04" fallback="treat as unverified"
As of 2026-07, total club IT spend commonly ranges ~2%–6% of revenue; a 3-year transformation program may temporarily sit above this band during heavy build years. Treat as a planning anchor; verify current benchmarks via `tools/04` and compare against `data/15`.
截至 2026-07，场馆 IT 总支出常见约 2%–6% 营收；三年转型在重建设年份可能临时高于此带。视作规划锚点；经 `tools/04` 核验并与 `data/15` 对照。
:::

| Year / 年 | Capex / 资本 | Opex / 经营 | % of revenue 🔄 / 占营收 | Notes / 说明 |
|---|---|---|---|---|
| Y1 | __ | __ | __% | foundation / 打底 |
| Y2 | __ | __ | __% | scale / 扩张 |
| Y3 | __ | __ | __% | transform / 转型 |

> **Red flag / 红旗**: a single year >10% of revenue with no staged pilot = likely over-build. Re-check against Iron Law 6 (ROI first).
> **红旗**：单年 >10% 营收且无分阶段试点 = 大概率过度建设。按铁律 6（ROI 先行）复核。

### 3.6 Risk & Compliance Register / 风险与合规登记表 {#s-risk}

| Risk / 风险 | Market / 市场 | HI ref / 红线 | Likelihood / 可能 | Mitigation / 缓解 |
|---|---|---|---|---|
| Biometric storage cross-border / 生物识别跨境 | ___ | HI-1 | ___ | ___ |
| Unmanned lone-exerciser safety / 无人独练安全 | ___ | HI-2 | ___ | ___ |
| Prepaid fund supervision / 预付资金监管 | ___ | HI-3 | ___ | ___ |

> Every row touching HI-1~HI-8 MUST carry a named mitigation. No "TBD".
> 凡触及 HI-1~HI-8 的行必须带具名缓解措施。不得「待定」。

### 3.7 Governance Cadence / 治理节奏 {#s-governance}

- Monthly: digital ops review (RACI owner + FDMM tracker). / 月度：数字化运营复盘（RACI 负责人 + FDMM 追踪）。
- Quarterly: board KPI dashboard + initiative RAG review (`templates/03`). / 季度：董事会 KPI 看板 + 举措 RAG 复盘（`templates/03`）。
- Annual: FDMM re-assessment + budget reset (`templates/02`, `templates/05`). / 年度：FDMM 复评 + 预算重设（`templates/02`、`templates/05`）。

---

## ④ Common Mistakes / 常见错误 {#mistakes}

- **Skipping FDMM diagnosis** → Strategy built on a vibe, not a level. See `data/21-anti-pattern-library.md#ap-002` spirit (decide before you measure). / 跳过 FDMM 诊断 → 战略建在感觉而非等级上。
- **Buzzword-first roadmap** ("AI everything") → violates Iron Law 7. / 「AI 一切」优先路线 → 违反铁律 7。
- **No compliance register** → HI-1~HI-8 blind spots surface at go-live. / 无合规登记表 → HI-1~HI-8 盲区在上线爆发。
- **Single-point forecasts** → violates G8 (ranges only). Use `templates/07` for ROI ranges. / 单点预测 → 违反 G8（只用区间）。ROI 区间用 `templates/07`。

---

## ⑤ Related Files / 相关文件 {#related}

- `tools/01-fdmm-maturity-assessment.md` — current-state scoring. / 当前状态评分。
- `tools/07-chief-orchestrator.md` — S1–S8 execution. / S1–S8 执行。
- `templates/02-annual-it-budget.md` — envelope detail. / 投资包明细。
- `templates/03-board-report-deck-outline.md` — board narrative. / 董事会叙事。
- `templates/05-fdmm-assessment-worksheet.md` — diagnostic. / 诊断表。
- `references/05-methodology-library.md` §I — governance method. / 治理方法。
- `data/15-procurement-and-cost-benchmark.md` — cost ranges. / 成本区间。
- `data/21-anti-pattern-library.md` — failure patterns. / 失败模式。

---

## ⑥ G13 Tri-Perspective Note / 三视角覆盖备注 {#g13}

> **Architect** (this doc frames the 3-year build discipline via FDMM + horizons) × **Operator** (cadence + RACI give the solo steward a runnable plan) × **Member** (north-star retention + HI red lines keep member value & safety funded, not traded for hype). / **架构**（本文件以 FDMM+时区框定三年建设纪律）× **商家**（节奏+RACI 给一人总管可跑计划）× **会员**（北极星留存+HI 红线让会员价值与安全被注资，而非为噱头让渡）。
