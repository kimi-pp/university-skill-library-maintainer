# Pilot Validation Plan / 试点验证计划

> **Cluster / 集群**: I (governance & money), X (methodology)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: baseline metrics are point-in-time → capture & date them before launch; benchmark ranges re-verify via `tools/04`. / 基线为时点值 → 上线前采集并标注日期；基准区间经 `tools/04` 复核。
> **Cross-references / 交叉引用**: `templates/07-roi-business-case.md` (pilot trigger) · `templates/04-digital-charter-and-stage-gate.md` (S6 gate) · `references/05-methodology-library.md` §9 · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04`。

---

## ① Purpose & When to Use / 用途与使用时机 {#purpose}

Design a real pilot before scaling any system or AI feature — capture baseline first, define success metrics, sample, duration, control, and a go/no-go review. This is the S6 Go-live gate's evidence base.
在扩大任何系统或 AI 功能前设计真试点——先采基线、定义成功指标、样本、时长、对照与 go/no-go 评审。这是 S6 上线门的证据基。

> **FDMM level gate / 成熟度闸口**: **FDMM L2 and above**, and mandatory whenever `templates/07` pessimistic says "pilot first", or any AI/high-change feature rolls out. L1 clubs pilot only single-system swaps with owner as the sole tester.
> **FDMM 等级闸口**：**FDMM L2 及以上**，且凡 `templates/07` 悲观指「先试点」或任何 AI/高变更功能上线都强制。L1 仅做单系统切换、老板为唯一测试者。

> **What good looks like / 好答案长什么样**: a one-line hypothesis; baseline captured BEFORE launch with dates; metrics tied to the ROI case; defined control (or honest reason none); fixed duration; a go/no-go scorecard with pre-agreed thresholds.
> **好答案长什么样**：一句话假设；上线前带日期采基线；指标挂钩 ROI 案；定义对照（或无对照的诚实理由）；固定时长；带预设阈值的 go/no-go 评分卡。

> **Red flag — Pilot Theater / 红旗：试点作秀**: a "pilot" with no baseline, no control, success predefined, or run only on the champion club by enthusiasts. That proves nothing. See `data/21` failure pattern; design against it below. / 无基线、无对照、成功预设、只在发烧友旗舰店跑的「试点」证明不了任何事。见 `data/21`；按下文反设计。

---

## ② Prerequisites & Inputs Checklist / 前置条件与输入清单 {#prerequisites}

- [ ] Hypothesis + expected effect from `templates/07`. / `templates/07` 的假设与预期效果。
- [ ] Baseline data source accessible (last 90 days). / 基线数据源可查（近 90 天）。
- [ ] Pilot scope: which clubs/members, how many. / 试点范围：哪些店/会员、多少。
- [ ] Owner + measurer (not the same enthusiast). / 负责人+测量人（非同一发烧友）。
- [ ] Pre-agreed go/no-go thresholds. / 预设 go/no-go 阈值。

---

## ③ The Template / 模板正文 {#template}

### 3.1 Hypothesis Card / 假设卡 {#s-hypothesis}

| Field / 字段 | Fill-in / 填写 |
|---|---|
| Hypothesis / 假设 | "If we __, then __ will change by __." / 「若我们__，则__将变化__。」 |
| Why now / 为何现在 | ___ |
| Linked ROI line / 挂钩 ROI 行 | from `templates/07` §3.2 / 取自 §3.2 |
| Owner / 负责人 | ___ |
| Non-negotiable / 不可让 | HI-1~HI-8 must hold / HI 红线须守 |

### 3.2 Baseline Capture — BEFORE Pilot / 基线采集：试点前 {#s-baseline}

> Capture these on __ (date) BEFORE any change. No baseline = no pilot, just theater.
> 在 __（日期）任何改动前采集。无基线 = 非试点，只是作秀。

| Metric / 指标 | Baseline value / 基线值 | Date captured / 采集日 | Source / 来源 |
|---|---|---|---|
| e.g. churn rate / 流失率 | __% | ___ | CRM |
| e.g. check-in time / 入场耗时 | __s | ___ | gate log / 闸机日志 |
| e.g. complaint/incident / 投诉事故 | __/mo | ___ | log / 台账 |

### 3.3 Success Metrics & Thresholds / 成功指标与阈值 {#s-metrics}

| Metric / 指标 | Baseline / 基线 | Target / 目标 | Go threshold / 过阈 | No-go threshold / 否阈 |
|---|---|---|---|---|
| ___ | __ | __ | ≥__ | <__ |
| ___ | __ | __ | ≥__ | <__ |

> Tie every metric to the ROI benefit class it proves (revenue/cost/compliance/member-exp). / 每指标挂钩它要证明的 ROI 收益类。

### 3.4 Sample & Duration Rules of Thumb / 样本与时长经验规则 {#s-sample}

- **Sample / 样本**: enough to see the effect — rule of thumb ≥ 1 club or ≥ 200 members for behavioral metrics; smaller only for pure tech uptime. / 足以看到效果——经验：行为类 ≥1 店或 ≥200 会员；纯技术可用性可更小。
- **Duration / 时长**: ≥ 1 full cycle (e.g. 4 weeks membership billing cycle) so seasonality doesn't fake the result. / ≥ 一个完整周期（如 4 周会籍计费周期），避免季节性造假。
- **Representativeness / 代表性**: pick a TYPICAL club, not the flagship enthusiast club. / 选典型店，非发烧友旗舰店。

### 3.5 Control Considerations / 对照考量 {#s-control}

| Option / 选项 | When / 何时 | Note / 说明 |
|---|---|---|
| A/B split / 分组对照 | enough volume / 量够 | compare pilot vs matched non-pilot club / 试点 vs 匹配非试点店 |
| Before/after / 前后对照 | single club / 单店 | relies on stable baseline; weaker / 靠稳定基线，较弱 |
| No control / 无对照 | never recommended / 不推荐 | only if HI/legal blocks comparison; state why / 仅 HI/法律阻比对时；写理由 |

> **Red flag / 红旗**: claiming success with no control AND no baseline = pilot theater. Reject the conclusion. / 无对照且无基线却宣称成功 = 试点作秀。拒结论。

### 3.6 Go / No-Go Review Template / Go/No-Go 评审模板 {#s-gonogo}

| Criterion / 判据 | Result / 结果 | Verdict / 结论 |
|---|---|---|
| Baseline existed pre-launch / 上线前有基线 | yes/no | |
| Target met / 达目标 | __ vs __ | |
| No HI breach / 无 HI 违 | yes/no | |
| ROI case still holds / ROI 案仍立 | yes/no | |
| **Decision / 决策** | **Go / Iterate / Kill** | |

### 3.7 Pilot-Theater Anti-Pattern Warning / 试点作秀反模式警示 {#s-theater}

> **Pilot theater / 试点作秀** = a pilot designed to confirm, not to test: no baseline, no control, enthusiasts-only, success pre-declared, duration too short to see anything. It manufactures false confidence and leads to chain-wide rollout of a dud (Iron Law 10 honesty breach).
> **试点作秀** = 为证实而非验证而设计的试点：无基线、无对照、只发烧友、成功预设、时长过短啥也看不出。它制造虚假信心，导致全连锁铺开一个废功能（违反铁律 10 诚实）。

Checklist to AVOID theater / 避作秀清单:
- [ ] Baseline dated & captured before any change? / 改动前带日期采基线？
- [ ] Typical (not flagship) club? / 典型（非旗舰）店？
- [ ] Independent measurer (not owner of hypothesis)? / 独立测量人（非假设提出者）？
- [ ] Pre-agreed go/no-go thresholds? / 预设 go/no-go 阈值？
- [ ] Duration covers ≥1 full cycle? / 时长覆盖 ≥1 完整周期？

---

### 3.8 Worked Example — Churn-AI Pilot / 实例：流失 AI 试点 {#s-example}

| Field / 字段 | Value / 值 |
|---|---|
| Hypothesis / 假设 | "If coaches use AI churn alerts, monthly churn drops by ≥2pp." / 「若教练用 AI 流失提醒，月流失降 ≥2 点。」 |
| Baseline (captured 2026-07-01) / 基线 | 12% annual churn, 600 lost/yr, no alerts in use / 年流失 12%、年失 600、无提醒 |
| Scope / 范围 | 1 typical 2-club operator, 300 members, NOT the flagship / 1 典型 2 店、300 会员、非旗舰 |
| Duration / 时长 | 8 weeks (2 billing cycles) / 8 周（2 计费周期） |
| Control / 对照 | Before/after on same club (volume too small for clean A/B) / 同店前后（量小难干净 A/B） |
| Go threshold / 过阈 | churn ≤ 10% annualized by week 8 / 第 8 周日化年流失 ≤10% |
| Measurer / 测量人 | Duty manager (independent of hypothesis owner) / 店长（独立于假设提出者） |

> Result / 结果: at week 8, annualized churn = 10.5% → missed go threshold by 0.5pp → decision **Iterate** (extend 4 weeks, coach training refresh) rather than full rollout. This honest "near-miss" is the opposite of pilot theater. / 第 8 周日化年流失 10.5% → 差 0.5 点未过阈 → 决策**迭代**（延 4 周、补教练培训）而非全铺。此诚实「擦肩」正与试点作秀相反。

### 3.9 One-Line Memory Aid / 口诀 {#s-aid}

> **Baseline before, control beside, threshold decided, typical club, independent eye — or it's theater.** / **先基线、旁对照、阈预设、典型店、独立眼——否则即作秀。**

Repeat this before approving any pilot. If any word is missing, the pilot is not ready to fund. / 批任何试点前默念。缺一即未_ready 注资。

### 3.10 Volatile-Fact Hook / 易变事实钩子 {#s-hook}

:::dynamic-hook topic="pilot-benchmark-ranges" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07, pilot sample-size and duration rules of thumb vary by club size, member volume and metric type (behavioral vs pure-uptime); verify the fit-for-purpose minimum via `tools/04` rather than copying a generic "2-week pilot" from another industry.
截至 2026-07，试点样本量与时长经验规则随门店规模、会员量与指标类型（行为 vs 纯可用性）浮动；经 `tools/04` 核验合身最小值，勿照搬他行业「2 周试点」。
:::

## ④ Common Mistakes / 常见错误 {#mistakes}

- **Pilot theater** → false confidence, bad rollout. Fight with §3.7 checklist. / 试点作秀 → 虚假信心、烂铺开。用 §3.7 清单对抗。
- **No baseline** → can't prove anything moved. Capture in §3.2. / 无基线 → 无法证变动。用 §3.2 采。
- **Flagship-only** → selection bias, won't generalize. Pick typical. / 只旗舰 → 选择偏误、不普适。选典型。
- **Roll out before go/no-go** → skips S6. Hold the review in §3.6. / 评审前就铺开 → 跳 S6。先跑 §3.6。

---

## ⑤ Related Files / 相关文件 {#related}

- `templates/07-roi-business-case.md` — pilot trigger. / 试点触发。
- `templates/04-digital-charter-and-stage-gate.md` — S6 gate. / S6 门。
- `references/05-methodology-library.md` §9 — change mgmt. / 变革管理。
- `data/21-anti-pattern-library.md` — failure patterns. / 失败模式。
- `tools/01-fdmm-maturity-assessment.md` — level fit. / 等级适配。

---

## ⑥ G13 Tri-Perspective Note / 三视角覆盖备注 {#g13}

> **Architect** (hypothesis + control + thresholds enforce scientific validation) × **Operator** (sample/duration rules + go/no-go give the solo steward a runnable, defensible pilot) × **Member** (baseline + HI guard in pilot protect members from unproven features rolled out at scale). / **架构**（假设+对照+阈值强制科学验证）× **商家**（样本/时长规则+go-no-go 给一人总管可跑可辩的试点）× **会员**（试点内基线+HI 护栏保护会员不被未证功能大规模铺开伤害）。
