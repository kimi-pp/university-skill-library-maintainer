# Annual IT Budget Worksheet / 年度 IT 预算工作表

> **Cluster / 集群**: I (IT governance & money)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: budget % of revenue re-verify every 90 days via 🔄 hook → `data/15-procurement-and-cost-benchmark.md`; vendor unit prices pass `tools/04`. / 预算占营收比每 90 天经 🔄 钩复核 → `data/15`；供应商单价过 `tools/04`。
> **Cross-references / 交叉引用**: `references/05-methodology-library.md` §3 (IT budgeting) · `data/15-procurement-and-cost-benchmark.md` (#cost-structure, #cost-fitout) · `tools/04-dynamic-intelligence-retrieval.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04`。

---

## ① Purpose & When to Use / 用途与使用时机 {#purpose}

Use this worksheet to plan and approve one club (or one chain's) annual IT spend — capex vs opex, per-category lines, a revenue-sanity check, monthly phasing, and an approval trail.
用本工作表规划并审批单店（或单条连锁）的年度 IT 支出——资本 vs 经营、分科目明细、营收合理性校验、月度排程与审批留痕。

> **FDMM level gate / 成熟度闸口**: For **FDMM L2 and above**. An L1 paper-club should NOT use this full sheet yet — start with a one-page opex tracker (SaaS + connectivity + MSP only) and graduate to this sheet once a second system goes live.
> **FDMM 等级闸口**：适用于 **FDMM L2 及以上**。L1 纸表馆暂勿用整表——先用一页经营支出追踪（仅 SaaS+网络+外包），待第二套系统上线再升级到本表。

> **What good looks like / 好答案长什么样**: every line is a range with a source note; capex and opex are separated; the % of revenue lands inside the sanity band; contingency is 10–15%; approval signatures exist.
> **好答案长什么样**：每行为带来源说明的区间；资本与经营分开；占营收落在合理带； contingency 10–15%；有审批签字。

> **Red flag / 红旗**: a budget with single-point "exact" prices, or 0% contingency, or no approval row → reject. See `data/21-anti-pattern-library.md#ap-010` (cutting resilience to save cost).
> **红旗**：预算是单点「精确」价、或 contingency 为 0%、或无审批行 → 驳回。见 `data/21#ap-010`（为省钱砍韧性）。

---

## ② Prerequisites & Inputs Checklist / 前置条件与输入清单 {#prerequisites}

- [ ] Club count and format known (big-box / boutique / 24h / corporate). / 已知门店数与业态（综合/精品/无人/企业）。
- [ ] Prior-year actuals (if any) for baseline. / 上年实际数（如有）作基线。
- [ ] Projected revenue for the year (range). / 当年预测营收（区间）。
- [ ] `data/15` open for cost ranges. / 已打开 `data/15` 取成本区间。
- [ ] FDMM level from `tools/01` (drives automation weight). / 已知 `tools/01` 的 FDMM 等级（决定自动化权重）。
- [ ] Named approver(s) per `templates/04` decision rights. / 按 `templates/04` 决策权已具名审批人。

---

## ③ The Template / 模板正文 {#template}

### 3.1 Capex vs Opex split / 资本性与经营性拆分 {#s-split}

| Type / 类型 | Definition / 定义 | Examples / 例 |
|---|---|---|
| Capex / 资本性 | one-time, amortized 3–5 yrs / 一次性，3–5 年摊销 | gates, POS, servers, cabling, screens / 闸机、POS、服务器、布线、屏 |
| Opex / 经营性 | recurring / 经常性 | SaaS, connectivity, MSP, cloud, support / SaaS、网络、外包、云、支持 |

### 3.2 Per-Category Lines / 分科目明细 {#s-lines}

> Fill each as a range 🔄; replace with `data/15` actuals once quoted. Sum capex and opex separately.
> 每行填区间 🔄；有报价后替 `data/15` 实际值。资本与经营分别求和。

| # | Category / 科目 | Type / 类型 | Annual range 🔄 / 年度区间 | Basis / 依据 | Note / 说明 |
|---|---|---|---|---|---|
| 1 | Software SaaS (CRM/booking/app) / 软件 SaaS | Opex | __–__ | `data/15#cost-mms` | per club / 每店 |
| 2 | Hardware refresh (gate/POS/locker) / 硬件换新 | Capex | __–__ | `data/15#cost-gate-lane` | amortize / 摊销 |
| 3 | Network & SD-WAN / 网络 | Opex+Capex | __–__ | `data/15#cost-network-sqm` | per club / 每店 |
| 4 | Security & CCTV / 安全监控 | Capex+Opex | __–__ | `data/15#cost-cctv-camera` | HI-5 zone check / 禁区核 |
| 5 | AI experiments (pilot budget) / AI 实验 | Opex | __–__ | `templates/07` | ring-fenced / 专款 |
| 6 | Training & change / 培训变革 | Opex | __–__ | `playbooks/13-90day-onboarding` | micro-learning / 微课 |
| 7 | Contingency 10–15% / 应急 | Opex | __–__ | see §3.4 / 见 §3.4 | mandatory / 必填 |
| | **Total / 合计** | | **__–__** | | |

### 3.3 % of Revenue Sanity Check / 占营收比合理性校验 {#s-sanity}

:::dynamic-hook topic="it-spend-percent-of-revenue" staleness="90d" action="tools/04" fallback="treat as unverified"
As of 2026-07, club IT spend (capex amortized + opex) commonly sits in a RANGE of roughly 2%–6% of revenue by format & FDMM level; verify current benchmarks via `tools/04` and compare against `data/15`.
截至 2026-07，场馆 IT 支出（资本摊销+经营）通常约 2%–6% 营收，随业态与 FDMM 等级浮动；经 `tools/04` 核验并与 `data/15` 对照。
:::

| Check / 校验项 | Value / 数值 | Pass? / 通过? |
|---|---|---|
| Total IT / revenue / IT 合计 ÷ 营收 | __% | in 2%–6% band? / 在带内? 🔄 |
| Contingency ≥ 10% / 应急 ≥10% | __% | yes / 否 |
| AI experiment ring-fenced / AI 专款 | __ | yes / 否 |

> **Red flag / 红旗**: total > 8% of revenue with no staged pilot explanation → over-build risk (Iron Law 6). / 总比 >8% 且无分阶段试点说明 → 过度建设风险（铁律 6）。

### 3.4 Monthly Phasing / 月度排程 {#s-phasing}

| Month / 月 | Capex / 资本 | Opex / 经营 | Milestone / 里程碑 |
|---|---|---|---|
| M1–M3 | __ | __ | assess / 诊断 |
| M4–M6 | __ | __ | procure / 采购 |
| M7–M9 | __ | __ | implement / 实施 |
| M10–M12 | __ | __ | optimize / 优化 |

### 3.5 Approval Workflow / 审批流程 {#s-approval}

| Step / 步 | Role / 角色 | Threshold / 阈值 | Sign / 签字 |
|---|---|---|---|
| Prepare / 编制 | One-person IT / 一人 IT | all / 全部 | ___ |
| Review / 复核 | Club owner / 老板 | >¥__ | ___ |
| Approve / 批准 | Board (if L4+) / 董事会 | >market ¥100k equiv | ___ |

> Decision rights must align with `templates/04` charter. No signature = no spend.
> 决策权须与 `templates/04` 章程对齐。无签字 = 不花钱。

---

### 3.6 Worked Example — Single Big-Box Club / 实例：单家综合馆 {#s-example}

> Illustrative ranges 🔄 only — replace with `data/15` quotes and `tools/04` verification before committing.
> 仅示意区间 🔄——承诺前替 `data/15` 报价并经 `tools/04` 核验。

| # | Category / 科目 | Type / 类型 | Annual range 🔄 / 年区间 | Basis / 依据 |
|---|---|---|---|---|
| 1 | Membership SaaS / 会籍 SaaS | Opex | ¥60k–¥120k | `data/15#cost-mms` |
| 2 | Hardware refresh / 硬件换新 | Capex | ¥80k–¥150k | `data/15#cost-gate-lane` |
| 3 | Network & SD-WAN / 网络 | Opex+Capex | ¥30k–¥60k | `data/15#cost-network-sqm` |
| 4 | Security & CCTV / 安全监控 | Capex+Opex | ¥40k–¥80k | `data/15#cost-cctv-camera` |
| 5 | AI experiments / AI 实验 | Opex | ¥20k–¥40k | `templates/07` |
| 6 | Training & change / 培训变革 | Opex | ¥15k–¥30k | `playbooks/13` |
| 7 | Contingency 12% / 应急 12% | Opex | ¥30k–¥60k | §3.4 / 见 §3.4 |
| | **Total / 合计** | | **¥275k–¥540k** | |

Assume revenue ¥6M → IT = 4.6%–9.0% of revenue. The upper end exceeds the 2%–6% sanity band → flag for staged pilot justification (Iron Law 6).
假定营收 ¥600 万 → IT 占 4.6%–9.0%。上限超 2%–6% 合理带 → 标需分阶段试点论证（铁律 6）。

> **What good looks like / 好答案长什么样**: the example above still forces a contingency line, separates capex/opex, and triggers the sanity check. A "complete" budget missing any of these three is not complete.
> **好答案长什么样**：上例仍强制 contingency 行、分开资本/经营、触发合理性校验。缺这三样的「完整」预算不算完整。

### 3.7 Format Weight Note / 业态权重说明 {#s-format}

> Total IT weight by format (qualitative; quantify via `data/15` + 🔄 `tools/04`): / 按业态 IT 权重（定性；经 `data/15`+🔄`tools/04` 定量）：

| Format / 业态 | Weight / 权重 | Driver / 驱动 |
|---|---|---|
| Big-box / 综合馆 | highest / 最高 | full stack, many systems / 全栈多系统 |
| 24h unmanned / 无人 | high automation / 自动化高 | lower staff IT, more sensors / 少人IT多传感 |
| Boutique / 精品 | low / 低 | booking + community heavy / 约课+社群重 |
| Corporate / 企业 | low / 低 | integration heavy / 集成重 |

> Use this to sanity-check the §3.3 % band: a boutique club at 5% of revenue is likely over-built; a 24h unmanned at 3% may be under-funded on resilience. / 用此校验 §3.3 占比带：精品馆占 5% 可能过度建设；无人馆占 3% 韧性或投入不足。

## ④ Common Mistakes / 常见错误 {#mistakes}

- **Zero contingency** → a single hardware failure blows the year. See `data/21-anti-pattern-library.md#ap-010`. / 零应急 → 一次硬件故障击穿全年。见 `data/21#ap-010`。
- **No data-export line in SaaS buys** → lock-in discovered at renewal. See `data/21-anti-pattern-library.md#ap-002`. / SaaS 采购无数据导出项 → 续约才发现锁定。见 `data/21#ap-002`。
- **Single-point "exact" prices** → violates G8 ranges. Use 🔄 hook to `tools/04`. / 单点「精确」价 → 违反 G8 区间。用 🔄 钩接 `tools/04`。
- **Cabling budgeted after renovation** → rework cost. See `data/21-anti-pattern-library.md#ap-003`. / 装修后才列布线预算 → 返工费。见 `data/21#ap-003`。

---

## ⑤ Related Files / 相关文件 {#related}

- `references/05-methodology-library.md` §3 — budgeting method. / 预算方法。
- `data/15-procurement-and-cost-benchmark.md` — cost ranges. / 成本区间。
- `tools/04-dynamic-intelligence-retrieval.md` — price verification. / 价格核验。
- `templates/01-three-year-digital-strategy.md` — 3-yr envelope. / 三年投资包。
- `templates/04-digital-charter-and-stage-gate.md` — approval rights. / 审批权。
- `templates/07-roi-business-case.md` — AI experiment justification. / AI 实验论证。

---

## ⑥ G13 Tri-Perspective Note / 三视角覆盖备注 {#g13}

> **Architect** (capex/opex + sanity band frame a fundable plan) × **Operator** (monthly phasing + approval trail give the solo steward control) × **Member** (contingency + security line protect uptime & safety so member experience is never the cut line). / **架构**（资本/经营+合理带框出可注资计划）× **商家**（月度排程+审批留痕给一人总管掌控）× **会员**（应急+安全线保障可用与安全，会员体验永不被砍）。
