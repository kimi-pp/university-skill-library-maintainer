# Growth & Ops Experiment Log / 增长与运营实验看板

> **Cluster / 集群**: W (Growth & sales stack · W12 experimentation)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Sample-size calculators, stats tooling and platform experiment features change — re-verify tooling via `tools/04`; pricing/compliance facts via `tools/05`. / 样本量计算器、统计工具、平台实验功能会变——经 `tools/04` 核工具；定价/合规经 `tools/05` 核。
> **Cross-references / 交叉引用**: `references/19-growth-and-sales-stack.md#W12-experimentation` · `data/21-anti-pattern-library.md` · `data/20-micro-details-ledger.md` · `templates/47-growth-campaign-brief.md` · `references/17-omnichannel-messaging.md` (HI-7 test messaging)
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## 1. Purpose & when to use / ① 用途与使用时机

**English / 英文**: A lightweight, running log that turns growth and operations guesses into recorded learning. It operationalizes `references/19#W12-experimentation`: one hypothesis card per idea, a registry table to track every test, honest minimum-sample rules for small clubs, an ethics warning on pricing tests, a quarterly review agenda, and a "what we know now" learning library.

**中文 / 中文**: 一份轻量、持续更新的看板，把增长与运营的"猜测"变成"有记录的学习"。它落地 `references/19#W12-experimentation`：每个想法一张假设卡、用注册表追踪每个实验、为小场馆给出诚实的最小样本规则、定价实验的伦理警告、季度复盘议程，以及"我们现在知道什么"的学习库。

> **Use this log when / 用本看板当**:
> - You want to test a change (pricing, message, class time, onboarding flow) instead of guessing. / 想测一个改动（定价、话术、排课、引导流程）而非拍脑袋。
> - You run a weekly growth meeting (`references/19#W23-review-agenda`). / 开周增长例会（`references/19#W23-review-agenda`）。
> - You need an audit trail of what was tried and decided (ship/kill/iterate). / 需要"试过什么、怎么决策"的审计轨迹。

---

## 2. Prerequisites / ② 前置条件

- [ ] **North-star + guardrails defined / 北极星与护栏已定**: from `references/19#W12-experimentation` (one north-star, guardrails must not break). / 北极星+护栏已定，护栏不得破。
- [ ] **Baseline metrics known / 基线指标已知**: current conversion/visit/churn before any test. / 实验前当前转化/到店/流失。
- [ ] **Consent for test messaging / 测试触达已同意**: any message variant still needs opt-in (HI-7); no A/B on health claims (HI-6). / 任何消息变体仍需 Opt-in（HI-7）；医疗宣称不做 A/B（HI-6）。
- [ ] **Analytics connected / 分析已接通**: UTM + CAPI + offline upload per `templates/47-growth-campaign-brief.md#tracking-plan`. / 追踪方案见 `templates/47#tracking-plan`。
- [ ] **Decision rule agreed / 决策规则已谈妥**: what % move = ship, what = kill, what = iterate. / 何种幅度=上线/砍掉/迭代。

---

## 3. THE TEMPLATE / ③ 模板（填空式）

### 3.1 Hypothesis card format / 假设卡格式 {#hypothesis-card}
> **Format / 格式**: "We believe **[assumption]**. We'll test **[change]**. Success = **[metric]** moves **[N%]** without breaking guardrail **[G]**."
> "我们相信 **[假设]**。我们将测试 **[改动]**。成功 = **[指标]** 变动 **[N%]** 且不破护栏 **[G]**。"

- **We believe / 我们相信**: `____` (the assumption, e.g. "lapsed members re-engage if we send a 30-day-silent win-back voucher")
- **We'll test / 我们测试**: `____` (ONE variable only — change 5 things and you learn nothing, AP-W12)
- **Success metric / 成功指标**: `____` · **Target move / 目标变动**: `____%`
- **Guardrail / 护栏**: `____` (must NOT breach: churn / complaint / margin)

### 3.2 Experiment registry table / 实验注册表 {#experiment-registry}
| ID | Owner | Start | End | Variant / 变体 | Sample / 样本 | Result / 结果 | Decision / 决策 |
|---|---|---|---|---|---|---|---|
| `EXP-__ ` | `____` | `____` | `____` | A vs B | `____` | `____` | ship / kill / iterate |

> **Guidance / 指引**: One row per experiment. Decision MUST be recorded even for "inconclusive" — inconclusive is a valid, logged outcome, not a blank. / 一实验一行；"无结论"也是合法、留痕的结果，不可留空。

### 3.3 Minimum-sample rules of thumb (honesty) / 最小样本经验法则（诚实） {#minimum-sample}
> **Honesty rule / 诚实规则**: Small clubs often CANNOT reach statistical significance in a 2-week window. Do not fake a "winner." Use directional reads + longer windows. / 小场馆往往 2 周窗口内**无法达到统计显著**。不要假装"胜出"；用方向性解读+更长窗口。

- **Compute, don't guess / 算而非猜**: use a sample-size calculator with YOUR base rate + minimum detectable effect; do not apply a borrowed number. 🔄
- **Rule of thumb / 经验法则** (illustrative, verify for your base rate / 演示用，按你的基线核): if your weekly visits < a few hundred per variant, extend the window to 4–8 weeks or read the result as *directional only*. / 若每变体周访问不足数百，延窗至 4–8 周，或仅作*方向性*解读。
- **Directional read format / 方向性读法**: "B trended +X% vs A but below significance threshold (n=__); extend window or iterate." / "B 较 A 趋势 +X% 但未达显著（n=__）；延窗或迭代。"
- **Guardrail override / 护栏优先**: even a "significant" win is KILLED if it breaches a guardrail (complaint spike, margin drop). / 即便"显著"，破护栏也砍。

:::dynamic-hook topic="stats-sample-size-tooling-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07: sample-size calculators, A/B platforms' built-in significance tests and stats libraries differ in default settings (one-tailed vs two-tailed, power) — verify the tool's assumptions before trusting its n. Prefer computing your own with stated base rate + MDE. / 截至 2026-07：样本量计算器、A/B 平台内置显著性检验、统计库的默认设定（单尾/双尾、power）各异——信其 n 前先核工具假设；建议用你的基线率+最小可检效应自算。
:::

### 3.4 Pricing-test ethics warning / 定价实验伦理警告 {#pricing-ethics}
> ⚠️ **Ethics warning / 伦理警告**: Pricing and offer tests on *existing* members touch trust — the asset hardest to rebuild (`references/19#W7-loyalty`). Mishandled, a test erodes retention more than it teaches. / 对*存量*会员做定价/优惠实验，触碰的是最难重建的信任资产。处理不当，实验对留存的伤害大于教益。
- Do NOT silently split existing members into price tiers they can compare. / 不得静默把存量会员拆成可互相比价的档位。
- Prefer new-acquisition or geo/cluster holdouts over in-club existing-member splits. / 优先新客或门店/分群对照，而非店内存量拆分。
- Any price change must keep cooling-off / refund fairness (HI-3) — no surprise fees (AP-W10). / 任何变价须保冷静期/退款公平（HI-3），不突袭收费（AP-W10）。
- Log the test in `data/21-anti-pattern-library.md` if it produced a trust incident. / 若引发信任事件，记 `data/21`。

**Pricing-test decision checklist (answer before you start) / 定价实验决策清单（开测前回答）**:
**定价实验决策清单（开测前回答）**:
- [ ] Are we testing on NEW acquisition only, not existing members? / 是否仅测新客而非存量？
- [ ] Can members in different arms NOT compare prices easily (geo/cluster split)? / 各臂会员是否难互相比价（门店/分群隔离）？
- [ ] Does the change keep cooling-off + refund fairness (HI-3)? / 变价是否保冷静期+退款公平（HI-3）？
- [ ] Is a guardrail (retention/complaint) explicitly armed to auto-kill? / 是否明确设护栏（留存/投诉）自动叫停？
- [ ] If ANY box is No → do NOT run on existing members; redesign or skip. / 任一"否"→不对存量会员跑，重设或放弃。

### 3.5 Quarterly experiment review agenda / 季度实验复盘议程 {#quarterly-review}
A 30-minute template (owner + operator + advisor): / 老板+运营+顾问 30 分钟模板：
1. **Volume / 数量** (5m): experiments run, win rate, inconclusive rate. / 实验数、胜率、无结论率。
2. **North-star trend / 北极星趋势** (5m): did the metric move vs `references/19#W12-experimentation` baseline? / 指标对基线动了没？
3. **Guardrail breaches / 护栏破项** (5m): any complaint/margin/churn spikes? / 投诉/毛利/流失有无尖峰？
4. **Decisions audit / 决策审计** (10m): ship/kill/iterate log reviewed; reverse any bad call. / 审 ship/kill/iterate，撤销错误决策。
5. **Next quarter / 下季** (5m): top 3 hypotheses to test. / 下季三大假设。

### 3.6 Learning library format ("what we know now" cards) / 学习库格式（"我们现在知道"卡片） {#learning-library}
> **Card template / 卡片模板**:
> - **Date / 日期**: `____` · **Source exp / 来源实验**: `EXP-__`
> - **We learned / 我们学到**: `____` (one sentence, falsifiable)
> - **Applies to / 适用**: `____` (market / format / FDMM level)
> - **Confidence / 置信**: high / medium / low (low = directional only)
> - **Related guardrail / 相关护栏**: `____`

> **Micro-example (illustrative) / 微例（演示）**: "2026-Q3, EXP-14, SG boutique: a 30-day-silent win-back voucher lifted recommit rate directionally (+6%) but n=48 → low confidence, extend window." Numbers illustrative. / "2026-Q3，EXP-14，新加坡精品馆：静默30天召回券方向性提升续约+6%，但 n=48→低置信，延窗。"数值演示。

### 3.7 Worked hypothesis cards (3 examples) / 三个已填假设卡 {#worked-cards}
> **Growth / 增长**: We believe lapsed members re-engage with a 30-day-silent win-back voucher. We'll test voucher vs no-voucher on new lapses. Success = recommit rate +5% without churn guardrail breach. / 我们相信静默30天召回券能唤回流失会员；测"有券 vs 无券"；成功=续约率+5%且不破流失护栏。
> **Ops / 运营**: We believe moving the 18:00 class 30 min later fills a dead slot. We'll test new time for 4 weeks. Success = that slot utilization +15% without complaint guardrail breach. / 我们相信18点课改晚30分填满闲置段；测新时段4周；成功=该时段利用率+15%且不破投诉护栏。
> **Pricing (ethics-gated) / 定价（伦理护栏）**: We believe a new-acquisition intro price lifts trials. We'll test on NEW walk-ins only (not existing members, per §3.4). Success = trial rate +10% without margin guardrail breach. / 我们相信新客体验价提升体验量；仅对新到店测（非存量，见§3.4）；成功=体验率+10%且不破毛利护栏。

### 3.8 Sample-size, worked (qualitative) / 样本量实战（定性） {#sample-worked}
> **Honesty rule / 诚实规则**: below is a reasoning shape, NOT a number to copy. Compute with your base rate. / 以下是推理框架，非可抄数字；按你的基线算。

- Step 1 / 第1步: find your current base rate (e.g. trial→member = 20%). / 取当前基线率（如体验→会员=20%）。
- Step 2 / 第2步: decide minimum detectable effect (e.g. +5pp). / 定最小可检效应（如+5pp）。
- Step 3 / 第3步: feed both + confidence (80–95%) into a sample-size calculator. 🔄 / 两者+置信度喂计算器。
- Step 4 / 第4步: if required n > your reachable volume in 2 weeks → extend window or read directional. / 若所需 n>2周可触量→延窗或方向性读。

### 3.9 Log upkeep cadence / 看板维护节奏 {#upkeep}
- **Weekly / 周**: add new experiments, update registry results, run `references/19#W23-review-agenda`. / 加新实验、更注册表、跑周例会。
- **Quarterly / 季**: §3.5 review; archive shipped experiments into learning library §3.6. / 季度复盘；把上线实验归档学习库。
- **Retire a card / 卡片退役**: when a "what we know now" card is overturned by new evidence, mark it superseded with date + new card ID — never delete (audit trail). / 被新证据推翻时标"已替代"+日期+新卡号，勿删（留痕）。

### 3.10 Copy-paste blank templates / 可复制空白模板 {#copy-paste}
**Hypothesis card / 假设卡** (copy per idea):
**假设卡**（每想法复制）：
```
We believe: ____
We'll test: ____ (ONE variable)
Success = ____ moves ____% without breaking guardrail ____
Owner: ____  Start: ____  End: ____
```
**Registry row / 注册表行** (copy per experiment):
**注册表行**（每实验复制）：
```
| EXP-__ | ____ | ____ | ____ | A vs B | n=__ | ____ | ship/kill/iterate |
```
> **Tip / 提示**: Keep this file as the single living log; paste new rows at top so the latest is first. / 本文件作唯一活看板；新行贴顶部，最新在前。

### 3.11 Decision rules (how to read the registry) / 决策规则（如何读注册表） {#decision-rules}
- **Ship / 上线**: target move reached (or directional + strong) AND no guardrail breach. / 达标（或方向性强）且不破护栏。
- **Kill / 砍**: no move AND/OR guardrail breach. / 无动且/或破护栏。
- **Iterate / 迭代**: move in right direction but below target → change ONE variable, re-test. / 方向对但不足→改一变量重测。
- **Inconclusive / 无结论**: n below threshold → extend window, do NOT declare winner. / n 不足→延窗，勿宣胜。

### 3.12 Worked registry example / 注册表实例 {#worked-registry}
| ID | Owner | Start | End | Variant | Sample | Result | Decision |
|---|---|---|---|---|---|---|---|
| EXP-14 | Ada | 2026-07-01 | 2026-07-28 | voucher vs none | n=48 | +6% directional | iterate (extend window) |
| EXP-15 | Ben | 2026-07-05 | 2026-08-02 | class time 18:30 | n=120 | +17% util | ship |
| EXP-16 | Cy | 2026-07-10 | 2026-07-24 | new price (new walk-ins) | n=60 | +9% trial, margin ok | ship |

> Numbers illustrative only — your registry uses YOUR real n and moves. / 仅演示；你的注册表填真实 n 与变动。

### 3.13 Loop with the campaign brief / 与活动简报的闭环 {#loop-brief}
> **Guidance / 指引**: Every growth campaign (`templates/47-growth-campaign-brief.md`) is a candidate experiment. Log the live campaign as EXP-__ so its result feeds the learning library. / 每个增长活动（`templates/47`）都可是实验；把在跑活动记为 EXP-__，结果喂学习库。

- Campaign brief §3.2 objective → becomes a hypothesis card §3.1. / 简报 §3.2 目标→变假设卡 §3.1。
- Campaign brief §3.6 tracking → supplies the registry "Result" column. / 简报 §3.6 追踪→供注册表"结果"列。
- Campaign brief §3.10 report → closes the experiment with a ship/kill/iterate. / 简报 §3.10 报告→以 ship/kill/iterate 收实验。

### 3.14 Storage & access / 存储与权限 {#storage}
> **Guidance / 指引**: Keep the log in a shared, read+write space for owner + operator + advisor; protect it from silent edits by versioning (date in filename or a changelog). / 看板放老板+运营+顾问可读写共享处；以版本（文件名带日期或变更日志）防静默篡改。

---

## 4. Common mistakes / ④ 常见错误

Full remedies in `data/21-anti-pattern-library.md`:
完整对策见 `data/21`：
- **AP-W12** Changing 5 things at once → no learning. / 一次改 5 样→无学习。
- **AP-W1** No offline attribution → can't tell which variant closed. / 无离线归因→不知哪变体成交。
- **AP-W3** Blasting test variants to non-consented lists → HI-7 breach + block. / 对非同意名单发测试变体→HI-7 违+被屏蔽。
- **Pricing-test trust loss / 定价实验信任损失**: un-flagged price splits on existing members → retention drop (see §3.4). / 对存量会员未告知拆价→流失（见 §3.4）。
- **False significance / 伪显著**: declaring a winner below sample threshold → wrong scale decision. / 样本不足即宣称胜出→错误扩量。

---

## 5. Related files / ⑤ 相关文件
- `references/19-growth-and-sales-stack.md#W12-experimentation` — W12 theory. / W12 理论。
- `templates/47-growth-campaign-brief.md` — every campaign is a candidate experiment. / 每个活动都可是实验。
- `data/20-micro-details-ledger.md` — capacity limits on how many variants you can run. / 可跑变体的产能上限。
- `data/21-anti-pattern-library.md` — log any trust/attrition incident here. / 信任/流失事件记此。
- `references/17-omnichannel-messaging.md` — HI-7 still applies to test messaging. / 测试触达仍须 HI-7。
- `tools/04` / `tools/05` — re-verify stats tooling & compliance before each test. / 每次实验前核工具与合规。

---

## 6. G13 tri-perspective note / ⑥ G13 三视角覆盖注记

**Architect / 架构师**: The log is the evidence layer of the W12 growth system — hypothesis → registry → decision → learning library forms a closed loop that compounds club knowledge instead of repeating guesses. / 看板是 W12 增长系统的证据层——假设→注册→决策→学习库形成闭环，沉淀知识而非重复猜测。
**Operator / 运营者**: Fill-in cards + registry table let a front-desk lead run a disciplined weekly test without a data scientist; directional-read rules stop small clubs from over-claiming. / 填空卡+注册表让前台主管无数据科学家也能严谨周测；方向性规则防小场馆过度宣称。
**Member / 会员**: HI-7 consent on test messaging and the pricing-ethics guard (§3.4) protect members from being unwitting test subjects and from trust-eroding price experiments. / HI-7 测试同意+定价伦理护栏（§3.4）保护会员不被当隐形实验对象，免遭伤信任的定价实验。
