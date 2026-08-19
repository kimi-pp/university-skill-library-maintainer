# ROI Business Case / 投资回报商业论证

> **Cluster / 集群**: I (governance & money)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: vendor price inputs verify via `tools/04` (🔄); regulation benefit (e.g. penalty avoided) confirm via `tools/05`; re-run if >90 days old. / 供应商价经 `tools/04` 复核（🔄）；合规收益（如免罚）经 `tools/05` 确认；超 90 天重跑。
> **Cross-references / 交叉引用**: `tools/06-roi-three-scenario.md` (method + multipliers) · `references/05-methodology-library.md` §6 · `templates/04-digital-charter-and-stage-gate.md` (S4 input) · `data/15-procurement-and-cost-benchmark.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04`。

---

## ① Purpose & When to Use / 用途与使用时机 {#purpose}

Build the mandatory three-scenario ROI case for any digital/AI investment above market ¥100k equivalent (Iron Law 6 / G6). It feeds the S4 Investment gate in `templates/04`.
为任何超当地等值 10 万元的数字化/AI 投资建强制三情景 ROI（铁律 6/G6）。它喂给 `templates/04` 的 S4 投资门。

> **FDMM level gate / 成熟度闸口**: **FDMM L2 and above** for anything material. Below L2, keep to opex-only pilots (<¥100k) justified by a one-paragraph rationale, not a full case.
> **FDMM 等级闸口**：**FDMM L2 及以上**对任何重大项。L2 以下只做经营支出试点（<10 万），一段理由即可，不用整案。

> **What good looks like / 好答案长什么样**: four benefit classes separated (never blended); three scenarios with mandated multipliers; pessimistic includes "no adoption" + "vendor fails" tails; kill criteria explicit; decision logged with names.
> **好答案长什么样**：四类收益分开（绝不混）；三情景带强制乘数；悲观含「没人用」+「供应商破产」尾；止损判据明确；决策留名。

> **Red flag / 红旗**: a case where "pessimistic" is still wildly positive → multipliers ignored, optimism bias. See `data/21` over-claim pattern; force `tools/06` multipliers. / 「悲观」仍暴赚 → 忽略乘数、乐观偏误。强制 `tools/06` 乘数。

---

## ② Prerequisites & Inputs Checklist / 前置条件与输入清单 {#prerequisites}

- [ ] Investment amount and category known. / 已知投资金额与类别。
- [ ] `tools/06` open for the four benefit classes + multipliers. / 打开 `tools/06` 看四类收益+乘数。
- [ ] Cost ranges from `data/15` (🔄 verify `tools/04`). / `data/15` 成本区间（🔄 经 `tools/04` 核验）。
- [ ] Baseline metrics (current churn, labor hours, incident cost). / 基线指标（当前流失、工时、事故成本）。
- [ ] `templates/04` S4 gate context. / `templates/04` S4 门上下文。

---

## ③ The Template / 模板正文 {#template}

### 3.1 Benefit Classes Worksheet / 四类收益工作表 {#s-benefits}

> Separate the four classes — blending them hides which benefit actually pays. Count each in its own unit, then convert to ¥.
> 分开四类——混算会掩盖到底哪项真回本。各自计数再折人民币。

| Class / 类 | Benefit / 收益 | Unit / 单位 | Annual qty / 年量 | Unit value 🔄 / 单价 | ¥/yr / 年额 |
|---|---|---|---|---|---|
| Revenue / 营收 | e.g. churn↓→retention↑ / 流失↓留存↑ | members retained / 留存会员 | __ | __ | __ |
| Cost / 成本 | e.g. labor hrs saved / 省工时 | hours/mo / 小时月 | __ | __ | __ |
| Compliance / 合规 | e.g. penalty avoided / 免罚 | incidents avoided / 免事故 | __ | __ | __ |
| Member-exp / 会员体验 | e.g. NPS↑→referral / NPS↑转介绍 | referrals / 转介绍 | __ | __ | __ |

### 3.2 Three-Scenario Table (mandated multipliers) / 三情景表（强制乘数） {#s-scenarios}

> Mandated multipliers from `tools/06` to counter optimism bias: Base = 0.5 × Expected benefit; Expected = planned case (×1.0); Pessimistic = 0.0 × adoption benefit (assume NO behavior change) + full cost + "vendor fails" tail.
> `tools/06` 强制乘数抗乐观偏误：基准 = 0.5 × 预期收益；预期 = 计划案（×1.0）；悲观 = 0.0 × 采用收益（假定行为无改变）+ 全额成本 + 「供应商破产」尾。

| Line / 项 | Base (×0.5) / 基准 | Expected (×1.0) / 预期 | Pessimistic (×0) / 悲观 |
|---|---|---|---|
| Gross benefit / 总收益 | __ | __ | __ (adoption=0) |
| Cost (capex amort + opex) / 成本 | __ | __ | __ + switch cost |
| Net / 净额 | __ | __ | **negative** |
| Payback (yrs) / 回收期 | __ | __ | n/a (kill) |

> **Worked micro-example / 微例**: Churn-AI, ¥100k equiv. Expected: 4pp churn drop → +¥B. Base: 2pp → +¥A. Pessimistic: 0pp (coaches don't use it) + ¥C cost + vendor-switch tail → negative → if pessimistic can't recover, PILOT first (`templates/08`). / 流失 AI，等值 10 万。预期降 4 个点=+¥B；基准降 2 个点=+¥A；悲观 0 个点（教练不用）+成本¥C+切换尾=负 → 悲观收不回则先试点（`templates/08`）。

### 3.3 Sensitivity Grid / 敏感性网格 {#s-sensitivity}

| Variable / 变量 | -50% / 低 | Plan / 计划 | +50% / 高 |
|---|---|---|---|
| Adoption rate / 采用率 | net __ | net __ | net __ |
| Unit price 🔄 / 单价 | net __ | net __ | net __ |
| Cost over-run / 成本超支 | net __ | net __ | net __ |

> Vary ONE axis at a time. If any single -50% swing makes Expected negative → too fragile, pilot. / 每次只变一轴。任一 -50% 摆动让预期转负 → 太脆，试点。

### 3.4 Kill Criteria / 止损判据 {#s-kill}

- [ ] Pessimistic net negative AND payback > __ yrs. / 悲观净负且回收期 > __ 年。
- [ ] Expected sensitive to -50% adoption → negative. / 预期对 -50% 采用敏感转负。
- [ ] Any HI-1~HI-8 breach uncovered. / 任何 HI-1~HI-8 缺口未解。
- [ ] Vendor refuses data-export (Iron Law 8). / 供应商拒数据导出（铁律 8）。

### 3.5 Decision Log / 决策日志 {#s-log}

| Date / 日期 | Decision / 决策 | Approvers / 审批人 | Condition / 条件 |
|---|---|---|---|
| ___ | proceed / pilot / kill / 上/试点/砍 | ___ | ___ |

---

### 3.6 Full Worked Example — Churn-AI / 完整实例：流失 AI {#s-example}

> Market ¥100k-equiv buy. Baseline: 5,000 members, 12% annual churn = 600 lost/yr. Avg member lifetime value ¥3,000. / 等值 10 万采购。基线：5000 会员、年流失 12%=年失 600 人。会员终身价值均值 ¥3000。

**Benefit classes / 四类收益** (Expected, ×1.0):
- Revenue / 营收: 4pp churn drop → 200 members retained × ¥3,000 = **+¥600k/yr**. / 降 4 个点→留 200 人×¥3000=+¥60 万。
- Cost / 成本: 2 coach-hours/week saved on manual churn calls = **+¥30k/yr**. / 省教练每周 2 小时手动挽留=+¥3 万。
- Compliance / 合规: 0 (none claimed). / 0（未主张）。
- Member-exp / 会员体验: NPS +5 → 20 referrals × ¥3,000 = **+¥60k/yr**. / NPS+5→20 转介绍×¥3000=+¥6 万。

**Three scenarios / 三情景**:

| Line / 项 | Base (×0.5) / 基准 | Expected (×1.0) / 预期 | Pessimistic (×0) / 悲观 |
|---|---|---|---|
| Gross benefit / 总收益 | ¥345k | ¥690k | ¥0 |
| Cost (capex amort + opex) / 成本 | ¥100k | ¥100k | ¥100k + ¥20k switch |
| Net / 净额 | **+¥245k** | **+¥590k** | **−¥120k** |
| Payback / 回收期 | 0.4 yr | 0.2 yr | n/a (kill) |

> Expected recovers cost in <1 yr; even Base is positive. Pessimistic is negative — but only because adoption = 0, which the pilot (`templates/08`) de-risks. Decision: **proceed with a pilot first** to lift the pessimistic tail before full buy. / 预期 <1 年回本；基准亦正。悲观为负——仅因采用=0，由试点（`templates/08`）降险。决策：**先试点**再全买以抬悲观尾。

### 3.7 Sensitivity Reading / 敏感性读法 {#s-sensitivity-read}

> In the example, if adoption lands at 50% of Expected (2pp drop), net = +¥245k still positive → robust enough to proceed after pilot. If adoption = 0 AND cost over-runs +50%, net = −¥270k → kill. / 上例中采用率达预期 50%（降 2 点）净仍 +¥245k → 够稳健可试点后上。若采用=0 且成本超 50% → 净 −¥270k → 砍。

### 3.8 Multiplier Quick-Reference / 乘数速查 {#s-multiplier}

> Mandated to defeat optimism bias (G8 ranges, Iron Law 6). Never let a sponsor "improve" the pessimistic case into positive.
> 为击败乐观偏误强制（G8 区间、铁律 6）。绝不让赞助人把悲观案「美化」成正。

| Scenario / 情景 | Benefit multiplier / 收益乘数 | Cost treatment / 成本处理 |
|---|---|---|
| Base / 基准 | ×0.5 of Expected / 预期的 0.5 | full cost / 全额成本 |
| Expected / 预期 | ×1.0 (planned) / 计划案 | full cost / 全额成本 |
| Pessimistic / 悲观 | ×0 (no adoption) / 无采用 | full cost + switch tail / 全额+切换尾 |

> If Expected itself is fragile to a single −50% swing (§3.3), do NOT approve — pilot via `templates/08` first. / 若预期对单一 −50% 摆动即脆（§3.3），不批——先 `templates/08` 试点。

### 3.9 Volatile-Fact Hook / 易变事实钩子 {#s-hook}

:::dynamic-hook topic="it-vendor-price-trend" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07, APAC fitness SaaS/hardware pricing and packaging shift with competition and FX; any "per-member" or "% of revenue" unit value in §3.1 is a range anchor — verify current quotes via `tools/04` before committing the budget line.
截至 202/07，亚太健身 SaaS/硬件定价与套餐随竞争与汇率变动；§3.1 任何「每会员价」「占营收比」均为区间锚点——承诺预算行前经 `tools/04` 核验当前报价。
:::

## ④ Common Mistakes / 常见错误 {#mistakes}

- **Blending benefit classes** → can't tell what paid. Separate per `tools/06`. / 混算收益类 → 不知谁回本。按 `tools/06` 分。
- **No pessimistic tail** → violates G6/Iron Law 6. Always include "no adoption" + "vendor fails". / 无悲观尾 → 违反 G6/铁律 6。必含「没人用」+「供应商破产」。
- **Single-point forecast** → violates G8. Use ranges + multipliers. / 单点预测 → 违反 G8。用区间+乘数。
- **Skip ROI under ¥100k-equiv** only if truly opex-pilot; material buys need the full case. / 仅真经营试点可免整案；重大采购须整案。

---

## ⑤ Related Files / 相关文件 {#related}

- `tools/06-roi-three-scenario.md` — method + multipliers. / 方法与乘数。
- `templates/04-digital-charter-and-stage-gate.md` — S4 gate. / S4 门。
- `templates/02-annual-it-budget.md` — cost lines. / 成本行。
- `templates/08-pilot-validation-plan.md` — when pessimistic says pilot. / 悲观指试点时。
- `data/15-procurement-and-cost-benchmark.md` — cost ranges. / 成本区间。
- `data/21-anti-pattern-library.md` — failure patterns. / 失败模式。

---

## ⑥ G13 Tri-Perspective Note / 三视角覆盖备注 {#g13}

> **Architect** (four-class + multipliers enforce honest, auditable ROI) × **Operator** (sensitivity + kill criteria give the steward a defensible go/no-go) × **Member** (member-experience class + HI kill criteria ensure benefits never come at member safety/privacy cost). / **架构**（四类+乘数强制诚实可审 ROI）× **商家**（敏感性+止损给管家可辩护的 go/no-go）× **会员**（会员体验类+HI 止损确保收益不以会员安全/隐私为代价）。
