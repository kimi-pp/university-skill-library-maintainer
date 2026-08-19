# Algorithm Kernel Library (zero-basis + practitioner) / 算法内核库（0 基础 + 从业者）

> **Cluster / 集群**: E (Data & AI 50+ scenarios) + K (AI governance) + I (money)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Algorithm *logic* is stable; vendor/feature claims 🔄 re-verify via `tools/04`; bias/regulation notes re-verify via `tools/05`.
> **Cross-references / 交叉引用**: `references/04-ai-application-landscape.md`, `references/13-data-and-llm-engine.md` (K), `data/03#vendor-ai`, `data/15-procurement-and-cost-benchmark.md` (ROI), `tools/06-roi-three-scenario.md`, `tools/09-ai-adversarial-consensus-gate.md`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## How to read each kernel / 每个内核怎么读 {#how-to-use}

Every kernel has **two layers**: / 每个内核有**两层**：

- **Zero-basis / 0 基础**: plain words + when to *buy not build*. / 说人话 + 何时"买不自己写"。
- **Practitioner / 从业者**: problem · data · method · eval · failure modes. / 问题·数据·方法·评估·失败模式。

Each ends with a **build-vs-buy verdict by FDMM level** and a **minimum-data honesty note**.
每个结尾给"按 FDMM 等级的 build-vs-buy 判定"与"最小数据量诚实注记"。

> **Honesty red line / 诚实红线**: "<500 members = use rules, not ML." Small clubs do not have enough signal; a simple rule (e.g. "no visit in 21 days → nudge") beats a fragile model (Iron Law 10).
> "会员 <500 = 用规则，别上 ML。" 小馆信号不足；简单规则（如"21 天没来→提醒"）胜过脆弱模型（铁律10）。

---

## 1. Churn prediction / 流失预测 {#algo-churn}

**Zero-basis / 0 基础**: Churn = a member who stops coming and won't renew. You can predict it with simple rules before any AI: if someone who used to visit 3×/week now visits 0× in 3 weeks, they are at risk. AI just does this automatically across thousands of members.
流失=会员不来且不续费。上 AI 前用简单规则就能做：原本每周来 3 次、现在 3 周 0 次=危险。AI 只是对上千人自动做这件事。

**Practitioner / 从业者**:
- Problem / 问题: rank members by renewal risk. / 给会员按续费风险排序。
- Data / 数据: visit frequency & decay, booking gaps, payment-fail count, class-drop, last-visit gap. / 到访频率与衰减、约课间隔、扣费失败次数、停课、最后到访间隔。
- Method / 方法: logistic regression → gradient-boosted trees (XGBoost/LightGBM); feature importance for action. / 逻辑回归→梯度提升树；特征重要度驱动动作。
- Eval / 评估: AUC/ROC (target ≥0.75 on holdout) + precision@k for outreach budget. / AUC（留存集≥0.75）+ precision@k 用于触达预算。
- Bias audit / 偏见审查: per HI-7/K, never punish protected groups (age/gender/minor); check score parity across segments. / 按 HI-7/K，绝不惩罚受保护群体（年龄/性别/未成年）；跨段查分数公平性。
- Failure modes / 失败: sparse data → noise; leaky labels (using renewal itself as feature); no action playbook → scores sit unused. / 数据稀→噪声；标签泄漏（用续费本身当特征）；无动作规程→分数闲置。
- Action playbook / 动作规程: score → segment → trigger SCRM nudge (consent-led, HI-7) → coach call. / 打分→分群→触发 SCRM 提醒（同意制 HI-7）→教练致电。

**Build-vs-buy / 建还是买**: L1–L2 = buy (MMS-built-in module). L3+ with ≥2k members = build if you have a data engineer, else buy. / L1–L2 买（MMS 内置）；L3+ 且 ≥2k 会员且有数据工程师才自建，否则买。
**Min data / 最小数据**: <500 members → rules. ≥2k members × 6 months history → model viable. / <500 用规则；≥2k 会员×6 月历史才可建模。

---

## 2. Class scheduling optimization / 排课优化 {#algo-scheduling}

**Zero-basis / 0 基础**: Don't let a room sit empty at 7pm while another class is overbooked. Scheduling optimization just balances demand (when do people come?) against constraints (which coach, which room, no clash).
别让 19 点空房、另一节课爆满。排课优化只是把需求（大家啥时候来？）与约束（哪个教练、哪个房、不冲突）做平衡。

**Practitioner / 从业者**:
- Data / 数据: historical attendance by timeslot/coach/room, coach availability, capacity. / 历史各时段/教练/房出勤、教练可用、容量。
- Method / 方法: demand forecast (time series) + constraint solver (ILP/CP-SAT) for assignment. / 需求预测（时序）+ 约束求解（ILP/CP-SAT）分配。
- Eval / 评估: fill-rate uplift, idle-room hours down, coach utilization. / 满课率提升、空房小时降、教练利用率。
- Failure / 失败: over-fitting to last month's anomaly (holiday); ignoring coach preference → turnover. / 过拟合上月异常（假期）；忽视教练偏好→流失。

**Build-vs-buy / 建还是买**: L2 = MMS-built-in. L3+ boutique with complex roster = buy scheduler add-on. / L2 用 MMS 内置；L3+ 精品复杂排班=买排课插件。
**Min data / 最小数据**: ≥3 months attendance. / ≥3 月出勤。

---

## 3. Dynamic pricing guardrails / 动态定价护栏 {#algo-dynamic-pricing}

**Zero-basis / 0 基础**: Raising prices when demand peaks (like airlines) can fill classes — but a gym that surprises members with surge pricing breaks trust and may break prepaid/consumer law. So dynamic pricing for fitness needs strict guardrails.
需求高峰涨价（像航司）能填满课——但健身房突然对会员涨价会毁信任，也可能违预付/消保法。故健身动态定价须严格护栏。

**Practitioner / 从业者**:
- Method / 方法: price elasticity model, but only on *new* flexible inventory (drop-in, off-peak), never on committed members. / 弹性模型，但只用于*新*弹性库存（次卡、非高峰），绝不对已承诺会员。
- Fairness flags / 公平标志: cap surge %, exempt prepaid/contract holders, transparent notice. / 限涨价幅度、豁免预付/合约会员、透明告知。
- Regulation / 合规: prepaid/consumer-protection law varies (HI-3); verify via `tools/05`. / 预付/消保法因市场而异（HI-3）；经 tools/05 核验。
- Failure / 失败: backlash, churn spike, regulatory complaint. / 反噬、流失飙升、监管投诉。

**Build-vs-buy / 建还是买**: L1–L3 = do NOT use dynamic pricing on members; use off-peak promos only. L4+ with legal sign-off = controlled experiment. / L1–L3 不对会员用动态价，仅非高峰促销；L4+ 法务签字才受控实验。
**Min data / 最小数据**: not advised below L4. / L4 以下不建议。

---

## 4. Lead scoring / 线索评分 {#algo-lead-scoring}

**Zero-basis / 0 基础**: Not every inquiry becomes a member. Lead scoring ranks enquiries so your front desk calls the hot ones first (visited pricing page, asked about PT, came from referral).
不是每个咨询都成会员。线索评分给咨询排序，让前台先打"热的"（看了价目、问私教、转介绍来的）。

**Practitioner / 从业者**:
- Data / 数据: channel, page views, event (trial booked), source (referral/paid). / 渠道、页面浏览、事件（约体验）、来源（转介/付费）。
- Method / 方法: logistic regression or simple rule-score; route to SCRM. / 逻辑回归或简单规则分；路由 SCRM。
- Eval / 评估: conversion lift, sales-cycle shorten. / 转化提升、销售周期缩短。
- Failure / 失败: biased toward paid channel → undervalues referrals. / 偏向付费渠道→低估转介。

**Build-vs-buy / 建还是买**: L2 = MMS/CRM built-in. L3 = buy MarTech lead module. / L2 用 MMS/CRM 内置；L3 买 MarTech 线索模块。
**Min data / 最小数据**: ≥200 leads history. / ≥200 条线索历史。

---

## 5. Site selection / 选址 {#algo-site-selection}

**Zero-basis / 0 基础**: Where should the next club go? Use a trade-area gravity model: count how many target customers live within 15 minutes, weigh by income, subtract competitor pull. POI data (subways, offices, apartments) feeds it.
下一家开哪？用商圈引力模型：15 分钟内有多少目标客、按收入加权、减去竞品拉力。POI 数据（地铁/写字楼/小区）喂进去。

**Practitioner / 从业者**:
- Data / 数据: POI, residential density, income, competitor locations, transit. / POI、居住密度、收入、竞品位置、交通。
- Method / 方法: Huff/gravity model + catchment radius; GIS overlay. / Huff/引力模型+ catchment 半径；GIS 叠加。
- Eval / 评估: predicted vs actual membership draw (back-test). / 预测 vs 实际吸客（回测）。
- Failure / 失败: stale POI, ignoring local regulation (zoning/gym license). / POI 过期、忽视本地法规（ zoning/健身许可）。

**Build-vs-buy / 建还是买**: L4 expansion = buy GIS/site tool or consultant; do not hand-guess. / L4 扩张=买 GIS/选址工具或顾问；别拍脑袋。
**Min data / 最小数据**: city POI + ≥3 existing clubs for calibration. / 城市 POI + ≥3 家现有店校准。

---

## 6. Staff rostering optimization / 排班优化 {#algo-rostering}

**Zero-basis / 0 基础**: Match staff to when members come (busy 6–9pm, quiet 2pm) without breaking labor law or burning out coaches.
把员工排到会员来的时段（晚 6–9 忙、下午 2 点闲），又不破劳动法、不累垮教练。

**Practitioner / 从业者**:
- Data / 数据: footfall by hour, labor rules per market, coach skills. / 各时段人流、各地劳工规则、教练技能。
- Method / 方法: constraint optimization (shift coverage ≥ demand, rest rules). / 约束优化（覆盖≥需求、休息规则）。
- Eval / 评估: labor cost %, coverage gaps, turnover. / 人力成本%、覆盖缺口、流失。
- Failure / 失败: illegal overtime, ignored rest law → fine. / 违法加班、忽视休息法→罚款。

**Build-vs-buy / 建还是买**: L2 = HR SaaS rostering. L3 = buy optimizer. / L2 用 HR SaaS 排班；L3 买优化器。
**Min data / 最小数据**: ≥4 weeks footfall. / ≥4 周人流。

---

## 7. Energy optimization (rules-first) / 能源优化（规则优先）{#algo-energy}

**Zero-basis / 0 基础**: The cheapest "AI" for energy is rules: HVAC off at 11pm, pool pump on timer, lights on occupancy sensor. Rules-first; add ML only if bills stay >5% of opex.
最便宜的能源"AI"是规则：空调 23 点关、水泵定时、灯随人感。规则优先；只有电费仍占运营成本 >5% 才加 ML。

**Practitioner / 从业者**:
- Method / 方法: rule engine (schedule + threshold) → if still high, RL/forecast on sub-meter data. / 规则引擎（排程+阈值）→ 仍高则对分项电表用 RL/预测。
- Eval / 评估: kWh drop vs baseline, payback months. / 较基线省电、回收月数。
- Failure / 失败: over-automation → member discomfort complaints. / 过度自动化→会员不适投诉。

**Build-vs-buy / 建还是买**: L1–L3 = rules + smart switches. L3+ = buy EMS. / L1–L3 规则+智能开关；L3+ 买 EMS。
**Min data / 最小数据**: ≥1 month sub-meter series. / ≥1 月分项电表时序。

---

## 8. Demand forecasting (seasonality) / 需求预测（季节性）{#algo-demand-forecast}

**Zero-basis / 0 基础**: January spikes (New-Year resolutions), CNY dips, Ramadan shifts evening traffic, Obon/summer in JP. Forecast lets you stock staff and avoid empty classes in slow weeks.
1 月高峰（新年决心）、春节跌、斋月改晚间、日本暑期/Obon。预测让你配人手、淡季不空课。

**Practitioner / 从业者**:
- Data / 数据: 12–24 months history + calendar flags (CNY/Ramadan/NY). / 12–24 月历史+日历标记（春节/斋月/新年）。
- Method / 方法: seasonal decomposition (STL) + holiday regressors. / 季节分解（STL）+ 节假日回归量。
- Eval / 评估: MAPE by week; flag Ramadan/CNY specially. / 周 MAPE；春节/斋月单独标。
- Failure / 失败: ignoring local holiday → big miss. / 忽视本地节日→大偏。

**Build-vs-buy / 建还是买**: L2 = spreadsheet + calendar. L3 = BI forecast. / L2 表格+日历；L3 BI 预测。
**Min data / 最小数据**: ≥12 months. / ≥12 月。

---

## 9. Recommendation (next-best-class) / 推荐（下一节最佳课）{#algo-recommendation}

**Zero-basis / 0 基础**: "Members who liked Monday yoga also liked Wednesday Pilates." Simple co-visitation recommendation in the app nudges attendance.
"喜欢周一瑜伽的也喜欢周三普拉提。" App 里简单共现推荐，轻轻推一把到场。

**Practitioner / 从业者**:
- Data / 数据: booking co-occurrence, member tags. / 约课共现、会员标签。
- Method / 方法: item-item CF or rule-based "frequently booked together". / 物品协同过滤或"常一起约"规则。
- Eval / 评估: CTR on recommendation, attendance uplift. / 推荐点击率、到场提升。
- Failure / 失败: cold start for new members → default to popular. / 新会员冷启动→默认推热门。

**Build-vs-buy / 建还是买**: L2 = MMS app built-in. L3 = buy recommend add-on. / L2 用 MMS App 内置；L3 买推荐插件。
**Min data / 最小数据**: ≥1k bookings. / ≥1k 条约课。

---

## 10. CV rep counting & posture / CV 计数与体态 {#algo-cv-posture}

**Zero-basis / 0 基础**: Cameras + AI can count your reps and warn on bad posture. But "98% accurate" lab claims drop in a real loud, crowded gym. Treat CV as *assist*, not coach replacement (HI-2/6).
摄像头+AI 能数你的次数、提醒姿势差。但实验室"98% 准"在真实吵闹拥挤的馆会掉。把 CV 当*辅助*，不是教练替代（HI-2/6）。

**Practitioner / 从业者**:
- Data / 数据: labeled video per exercise, diverse body types. / 各动作标注视频、多样体型。
- Method / 方法: pose estimation (OpenPose/MediaPipe) + rep state machine. / 姿态估计+次数状态机。
- Eval / 评估: per-exercise precision/recall on *your* footage, not vendor demo. / 在*你的*视频上评各动作精确率/召回，而非厂商 demo。
- Traps / 陷阱: demo-only eval, no occlusion handling, bias across body types. / 仅 demo 评估、无遮挡处理、跨体型偏见。

**Build-vs-buy / 建还是买**: L3 = buy CV module (don't build). L1–L2 = not yet. / L3 买 CV 模块（别自建）；L1–L2 暂不上。
**Min data / 最小数据**: vendor must show eval on footage like yours. / 厂商须在你同类视频上展示评估。

---

## 11. Anomaly detection (fraud / sharing) / 异常检测（欺诈/共享）{#algo-anomaly-fraud}

**Zero-basis / 0 基础**: One band used 5 times in 20 minutes at different gates = shared pass. Anomaly detection flags impossible patterns automatically.
一个手环 20 分钟在 5 个不同闸刷 5 次=共享卡。异常检测自动标出不可能模式。

**Practitioner / 从业者**:
- Data / 数据: access-event log, timestamps, gate IDs. / 门禁事件日志、时间、闸 ID。
- Method / 方法: velocity/rule checks + isolation forest for odd patterns. / 速度/规则检查+孤立森林查异常。
- Eval / 评估: precision of flagged (avoid false accuse member). / 标记精确率（避免误告会员）。
- Failure / 失败: false positives → member friction; needs human review. / 误报→会员摩擦；需人工复核。

**Build-vs-buy / 建还是买**: L2 = MMS rule alerts. L3 = buy anomaly add-on. / L2 用 MMS 规则告警；L3 买异常插件。
**Min data / 最小数据**: ≥1 month access log. / ≥1 月门禁日志。

---

## 12. Waitlist overbooking math / 候补超卖数学 {#algo-waitlist}

**Zero-basis / 0 基础**: Like airlines, sell a few extra spots because some no-show. But gentler: a gym overbooking 3 spots that all show = angry members. Cap low.
像航司，多卖几个位因为有人爽约。但更温和：多卖 3 个全到=会员怒。上限要低。

**Practitioner / 从业者**:
- Data / 数据: no-show rate by class/time. / 各课/时段爽约率。
- Method / 方法: expected no-show × capacity → safe overbook = ceil(rate×cap)−buffer. / 预期爽约×容量→安全超卖=ceil(率×容)−缓冲。
- Eval / 评估: walk-in denials = 0 target; fill-rate up. / 拒入门=0 目标；满课率升。
- Failure / 失败: over-aggressive → denied members. / 过激→拒会员。

**Build-vs-buy / 建还是买**: L2 = MMS waitlist. L3 = tuned overbook rule. / L2 用 MMS 候补；L3 调超卖规则。
**Min data / 最小数据**: ≥4 weeks no-show. / ≥4 周爽约率。

---

## 13. No-show prediction / 爽约预测 {#algo-noshow}

**Zero-basis / 0 基础**: Some members book then vanish. Predict who, and overbook or send a reminder only to them — not spam everyone (HI-7).
有些会员约了不来。预测谁会爽约，只对这部分超卖或提醒——别群发骚扰所有人（HI-7）。

**Practitioner / 从业者**:
- Data / 数据: booking-to-appear history, last-minute cancels. / 约到到场历史、临时取消。
- Method / 方法: logistic on member × class features. / 会员×课程特征逻辑回归。
- Eval / 评估: AUC, precision@k for reminder budget. / AUC、precision@k 用于提醒预算。
- Failure / 失败: spammy reminders → opt-out. / 骚扰提醒→退订。

**Build-vs-buy / 建还是买**: L3 = MMS/ML module. L1–L2 = simple "reminder to all 2h before". / L3 用 MMS/ML 模块；L1–L2 简单"课前 2h 全提醒"。
**Min data / 最小数据**: ≥500 bookings. / ≥500 条约课。

---

## 14. Model monitoring & drift (HI-7 / K) / 模型监控与漂移

Every production model needs: / 每个生产模型需：
- **Drift check / 漂移检查**: feature & prediction distribution shift, monthly. / 特征与预测分布月度漂移。
- **Bias audit / 偏见审计**: score parity across protected groups (HI-7/K). / 跨受保护群体分数公平性（HI-7/K）。
- **Human-in-loop / 人在回路**: high-risk (pricing, minors, health inference) needs review before action. / 高风险（定价/未成年/健康推断）动作前需人工复核。
- **Kill switch / 熔断**: ability to fall back to rules if model misbehaves. / 模型失常可回退规则。
- **Champion/challenger /  challenger**: keep prior model as fallback for 30 days. / 旧模型留 30 天作回退。

---

## 15. Kernel summary matrix / 内核总览矩阵

| Kernel / 内核 | Min data / 最小数据 | FDMM to build / 自建等级 | Build/Buy / 建买 | HI guard / 守卫 |
|---|---|---|---|---|
| Churn / 流失 | ≥2k×6mo | L3+ | buy L1–L2 | HI-7, HI-8 |
| Scheduling / 排课 | ≥3mo | L3 | buy | — |
| Dynamic pricing / 动态价 | n/a | L4+ | cautious / 谨慎 | HI-3 |
| Lead scoring / 线索 | ≥200 | L3 | buy | HI-7 |
| Site selection / 选址 | ≥3 clubs | L4 | buy/consult | — |
| Rostering / 排班 | ≥4wk | L3 | buy | labor law |
| Energy / 能源 | ≥1mo | L3 | rules-first | — |
| Demand forecast / 需求 | ≥12mo | L3 | buy | — |
| Recommendation / 推荐 | ≥1k | L3 | buy | HI-7 |
| CV posture / CV体态 | vendor eval | L3 | buy | HI-2, HI-6 |
| Anomaly / 异常 | ≥1mo log | L3 | buy | HI-7 |
| Waitlist / 候补 | ≥4wk | L3 | rule | HI-7 |
| No-show / 爽约 | ≥500 | L3 | buy | HI-7 |

> **Rule / 规则**: Below the min-data row → use rules, not ML (Iron Law 10). Above L4 dynamic pricing only with legal sign-off.
> 低于最小数据行→用规则别上 ML（铁律10）。L4 以上动态定价仅法务签字后。

---

## 16. ML glossary (plain words) / 机器学习词汇（说人话）

- **AUC/ROC** = how well the model ranks risk (1.0 perfect, 0.5 coin-flip). / 模型排序风险的能力（1完美，0.5 抛币）。
- **Precision@k** = of the k members you flag, how many truly churn. / 你标记的 k 人里真流失的比例。
- **Leakage** = using future info as a feature (cheats the score). / 用未来信息当特征（作弊分数）。
- **Drift** = the world changed, model stale. / 世界变了，模型过时。
- **Cold start** = new member, no history to recommend from. / 新会员无历史可推荐。

---

## 17. Adoption roadmap by FDMM / 按 FDMM 的采用路线图

Do not jump levels — each kernel has an entry gate (Iron Law 7). / 别跳级——每个内核有准入（铁律7）。

| FDMM | AI kernels that go live / 可量产内核 | Gate / 准入 |
|---|---|---|
| L1 Paper | none (rules only) / 仅规则 | first SaaS live / 首套SaaS上线 |
| L2 Online | recommendation (app), anomaly alerts | ≥1 system integrated / ≥1系统打通 |
| L3 Integrated | churn, scheduling, lead, roster, demand, no-show, CV | ≥3 systems + data platform / ≥3系统+数据中台 |
| L4 AI-aug | dynamic pricing (guarded), site selection | legal sign-off + human-in-loop / 法务签字+人在回路 |
| L5 Autonomous | self-optimizing ops | proven multi-site playbook / 多店打法验证 |

> **Rule / 规则**: A beginner on L1 asking for "AI churn model" gets rules first (21-day nudge), not a model. Match the kernel to the level.
> L1 新手要"AI 流失模型"，先给规则（21天提醒），不是模型。内核对等级。

---

## G13 Tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: method + eval + build-vs-buy by FDMM; no L4 solution prescribed to L1 clubs (Iron Law 7).
- **Operator / 运营者**: minimum-data honesty ("<500 members = rules"), failure modes, action playbooks (churn→SCRM nudge).
- **Member / 会员**: bias/fairness guards (HI-7/K), CV as assist not replacement (HI-2/6), no spam (HI-7). Every AI kernel is governed, not a black box.
本文件覆盖架构师（方法+评估+按 FDMM 的建买判定；绝不给 L1 馆上 L4 方案，铁律7）、运营者（最小数据诚实注记、失败模式、动作规程）、会员（偏见/公平护栏 HI-7/K、CV 辅助非替代 HI-2/6、不骚扰 HI-7）。每个 AI 内核受治理，非黑箱。
