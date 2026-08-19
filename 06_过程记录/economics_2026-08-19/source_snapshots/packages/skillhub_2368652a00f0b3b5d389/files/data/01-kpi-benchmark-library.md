# KPI Benchmark Library / KPI 基准库

> **Cluster / 集群**: U (Market intel & member UX) · carrier of commercial/ops/digital/IT/energy/AI benchmarks
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: All ranges are DIRECTIONAL and decay with market/format/era — re-verify any number you act on via `tools/04` before budgeting; re-baseline your own club every 90 days.
> **Cross-references / 交叉引用**: `references/17-omnichannel-messaging.md` (campaign CTR channels) · `references/19-growth-and-sales-stack.md` (CAC/LTV context) · `references/04-ai-application-landscape.md` (AI KPIs) · `data/02-regulation-traceability-index.md` · `tools/04-dynamic-intelligence-retrieval.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

> **Read this first / 先读这段**: Every figure below is a RANGE, not a fact. It is a directional benchmark to sanity-check your own numbers — never a target to copy blindly, and never proof of "the market average." Mark any number you quote with the retrieval date.
> 以下每个数值都是**区间**而非事实，是给你自查的方向性基准——绝非可盲抄的目标，也非「市场平均」的证据。引用任何数字务必标注检索日。

---

## How to Use Benchmarks Without Fooling Yourself / 如何不被基准骗

Two traps sink most benchmark exercises. Name them before you compare.
两个陷阱毁掉多数基准对标，比较前先点名。

1. **Survivorship bias / 幸存者偏差**: Published "benchmarks" come from clubs that survived and reported — struggling clubs are silent, so the number looks better than reality. Your true peer median is lower. 公开的「基准」来自存活且愿意上报的场馆——挣扎者沉默，故数字偏优。你真实同业中位数更低。
2. **Definition mismatch / 定义错位**: "Churn" to one analyst means non-renewal at term-end; to another, any 30-day lapse. "LTV" may or may not include PT and F&B. Compare only like-for-like; if definitions differ, the gap is noise. 「流失」有人指到期不续，有人指任意 30 天断档；「LTV」可能含或不含私教餐饮。只比对口径一致者，定义不同则差是噪声。

**Rule / 规则**: Use benchmarks to spot the *direction* and *order of magnitude* of a gap, then investigate YOUR cause. A number 10 points off benchmark is a question, not a verdict. 用基准看差距的*方向*与*量级*，再查*你的*原因。偏离 10 个点只是问题，不是判决。

:::dynamic-hook topic="kpi-benchmark-ranges-apac" staleness="MED" action="tools/04" fallback="treat all ranges as directional, re-verify before budgeting"
All numeric ranges in this file are directional stored values as of 2026-07, assembled from experience, not measured market averages; re-retrieve per market/format before any budget or board use. / 本文件所有数值区间均为 2026-07 的方向性存值，来自经验而非测得市场平均；任何预算或董事会用途前按市场/业态重新检索。
:::

---

### #kpi-definitions KPI Definition Quick-Reference / KPI 定义速查

One-line formula per KPI so comparisons never drift on definition (trap #2).
每个 KPI 一行公式，避免定义漂移（陷阱 #2）。

| KPI / 指标 | Formula / 公式 |
|---|---|
| Revenue per sqm / 坪效 | Monthly revenue ÷ usable area |
| LTV | Sum of member gross margin over active life (scope PT/F&B per definition) |
| CAC | Total acquisition cost ÷ new paying members |
| LTV:CAC | LTV ÷ CAC |
| Monthly churn | Members lost in month ÷ members at month start |
| Lead→Trial | Trials ÷ leads |
| Trial→Join | Joins ÷ trials |
| PT attach | Members with ≥1 PT in period ÷ active members |
| ARPU | Period revenue ÷ active members |
| Prepaid balance ratio | Outstanding deferred ÷ monthly recognized revenue |
| Class fill | Check-ins ÷ bookable seats |
| No-show | Booked-not-attended ÷ bookings |
| Peak utilization | Present at peak ÷ zone capacity |
| Gate throughput | Members cleared/min at peak |
| Staff:member | Front-line staff ÷ active members |
| App adoption | Active app users ÷ active members (30d) |
| Online booking share | Online bookings ÷ total bookings |
| Self-service rate | Staff-free actions ÷ total actions |
| CAPI match | Matched conversions ÷ total conversions |
| System uptime | Operational time ÷ total time |
| Backup success | Successful backups ÷ scheduled |
| kWh/sqm | Energy ÷ area |
| Churn AUC | Model discrimination on holdout |
| Bot deflection | Bot-resolved ÷ total queries |
| Forecast MAPE | Mean abs % error of forecast vs actual |

Lock these definitions club-wide before benchmarking; if a vendor reports a KPI with a different formula, relabel it, don't compare it. 对标前全馆锁定这些定义；若供应商用不同公式报 KPI，重命名而非直接比。

## 1. Commercial KPIs / 商业 KPI

### #kpi-revenue-per-sqm Revenue per Sqm (坪效) / 每平米营收（坪效）

Total monthly revenue ÷ usable floor area. The core efficiency ratio for physical clubs.
月总营收 ÷ 可用面积。实体场馆核心效率比。

- Typical directional range / 方向性区间: varies widely by format and city-tier — treat any single figure as market-specific; verify per market via `tools/04`. 随业态与城市能级差异极大，任何单点值都仅限特定市场；按市场经 `tools/04` 核验。
- Compare like-for-like / 同口径比: include or exclude pool/F&B consistently or the ratio lies. 泳池/餐饮须一致计入或剔除，否则失真。

### #kpi-ltv Lifetime Value (LTV) / 客户终身价值

Total gross margin a member generates over their active life, including membership + PT + F&B where defined.
会员活跃期内产生的总毛利，按定义含会籍 + 私教 + 餐饮。

- Directional range / 方向性区间: highly format-dependent; boutique and PT-heavy clubs run higher than low-price 24h. Verify per market via `tools/04`. 高度依赖业态；精品与私教重的场馆高于低价 24h。按市场经 `tools/04` 核验。
- Definition caveat / 定义提示: state whether PT/F&B are inside LTV before comparing. 比较前声明私教/餐饮是否计入 LTV。

### #kpi-cac Customer Acquisition Cost (CAC) / 获客成本

Fully-loaded cost to win one paying member: ads + commissions + promo + allocated overhead, ÷ new joins.
赢得一名付费会员的全口径成本：广告 + 佣金 + 促销 + 分摊 overhead，÷ 新入会数。

- Directional range / 方向性区间: spread is enormous across channels (referral ≈ near-zero to paid-social high); verify per market/channel via `tools/04`. 渠道间跨度极大（转介≈近零至付费社交高）；按市场/渠道经 `tools/04` 核验。

### #kpi-ltv-cac-ratio LTV : CAC Ratio / 终身价值与获客成本比

LTV ÷ CAC. The survival threshold for any club model.
LTV ÷ CAC。任何场馆模式的存活门槛。

- Directional floor / 方向性下限: a ratio below a modest threshold signals the model is unprofitable per member; healthy clubs sit materially above it — exact band verify via `tools/04`. 低于温和阈值即单客模型亏损；健康场馆显著高于此，精确带经 `tools/04` 核验。
- Watch / 注意: a high ratio from cheap CAC can mean under-investing in growth, not efficiency. 高比可能因 CAC 过低（增长投入不足）而非高效。

### #kpi-churn-rate Monthly Churn / Attrition (by format) / 月度流失率（按业态）

Active members lost in a month ÷ active members at month start. Format changes everything.
当月流失活跃会员 ÷ 月初活跃会员。业态决定一切。

| Format / 业态 | Directional monthly churn / 方向性月流失 | Note / 说明 |
|---|---|---|
| Big-box / 大型综合 | lower-to-mid band | Longer contracts smooth churn / 长合约平滑流失 |
| Boutique studio / 精品工作室 | mid band | Community binds, price sensitive / 社群黏性但价格敏感 |
| 24h unmanned / 24h 无人 | mid-to-higher band | Low touch, easy lapse / 低接触易断档 |

- All bands are directional; re-baseline your own after 90 days and compare your trend, not the table. 以上均为方向性；90 天后建自身基线，比趋势而非比表。
- Definition / 定义: decide term-end non-renewal vs any-lapse and stick to it. 选定「到期不续」或「任意断档」并固定。

### #kpi-lead-trial-join Lead → Trial → Join Conversion / 潜客→体验→入会转化

Two-stage funnel: (lead→trial) then (trial→join). The second stage is where clubs leak most.
两段漏斗：潜客→体验，再体验→入会。第二段漏得最多。

- Directional ranges / 方向性区间: lead→trial varies by channel; trial→join varies by offer and follow-up discipline. Verify per market via `tools/04`. 潜客→体验随渠道变；体验→入会随优惠与跟进纪律变。按市场经 `tools/04` 核验。
- Lever / 杠杆: speed-to-first-contact after a lead is the top predictor — measure it. 留资后首次联系速度是最强预测因子，须测量。

### #kpi-pt-attach-rate PT Attach Rate / 私教渗透率

Share of active members buying ≥1 PT session in a period.
某时段内购买 ≥1 次私教的活跃会员占比。

- Directional range / 方向性区间: boutique/PT-led clubs higher; low-price 24h lower. Verify per market via `tools/04`. 精品/私教主导高，低价 24h 低。按市场经 `tools/04` 核验。
- Why it matters / 为何重要: PT is the main margin expander beyond dues; attach rate tracks revenue health. 私教是会费外主要利润扩张点，渗透率反映营收健康。

### #kpi-arpu ARPU (Average Revenue per User) / 每用户平均营收

Total revenue in period ÷ active members. Blends dues + ancillary.
时段总营收 ÷ 活跃会员。混合会费 + 附加。

- Directional range / 方向性区间: format- and city-driven; verify per market via `tools/04`. 随业态与城市，按市场经 `tools/04` 核验。

### #kpi-prepaid-balance-ratio Prepaid Balance Ratio / 预付余额比

Outstanding deferred (unearned) member balance ÷ monthly recognized revenue. A liquidity & risk gauge.
未确认（递延）会员余额 ÷ 月度确认收入。流动性与风险指标。

- Directional range / 方向性区间: higher in annual-prepaid-heavy clubs; watch the HI-3 fund-supervision link. Verify per market via `tools/04`. 年付重的场馆更高；注意与 HI-3 资金监管关联。按市场经 `tools/04` 核验。

---

## 2. Operations KPIs / 运营 KPI

### #kpi-class-fill-rate Class Fill Rate / 课程满座率

Checked-in attendees ÷ bookable seats per class.
实到 ÷ 可约座位。

- Directional range / 方向性区间: popular time-slots far above off-peak; verify per format via `tools/04`. 热门时段远高于平峰；按业态经 `tools/04` 核验。
- Use / 用途: low fill = schedule or demand mismatch, not just "bad class." 低满座=排课或需求错配，非仅「课差」。

### #kpi-no-show-rate Booking No-Show Rate / 预约爽约率

Booked-but-not-attended ÷ total bookings.
约而未到 ÷ 总预约。

- Directional range / 方向性区间: varies with penalty policy; clubs with no-show fees lower. Verify per market via `tools/04`. 随违约惩罚政策变；有爽约费者低。按市场经 `tools/04` 核验。
- Lever / 杠杆: a small no-show credit or waitlist auto-fill cuts wasted capacity. 小额爽约扣费或候补自动补位可减少浪费产能。

### #kpi-peak-utilization Peak-Hour Utilization / 高峰时段利用率

Members present during peak window ÷ designed capacity of that zone.
高峰窗口在场会员 ÷ 该区设计容量。

- Directional range / 方向性区间: well-run clubs peak near design capacity at 2–3 daily windows; verify per format via `tools/04`. 运营好者每日 2–3 个高峰近设计容量。按业态经 `tools/04` 核验。
- Risk / 风险: sustained > capacity = safety & experience problem; sustained < capacity = over-built. 持续超载=安全与体验问题；持续不足=过度建设。

### #kpi-gate-throughput Gate Throughput / 闸机吞吐

Members cleared through entry per minute at peak.
高峰每分钟过闸会员数。

- Directional range / 方向性区间: depends on auth method (face > QR > card tap); verify per hardware via `tools/04`. 取决于认证方式（人脸>二维码>刷卡）；按硬件经 `tools/04` 核验。
- Fail flag / 故障信号: queue at open/peak = lost sessions & complaints; size gates to peak, not average. 开门/高峰排长队=丢课时与投诉；闸机按高峰而非均值配。

### #kpi-staff-member-ratio Staff-to-Member Ratio / 员工会员比

Front-line staff (incl. coaches, excl. back-office) ÷ active members.
一线员工（含教练，不含后台）÷ 活跃会员。

- Directional range / 方向性区间: boutique higher touch; 24h unmanned near-zero on-site. Verify per format via `tools/04`. 精品高接触；24h 无人现场近零。按业态经 `tools/04` 核验。

---

## 3. Digital KPIs / 数字化 KPI

### #kpi-app-adoption App Adoption % / App 渗透率

Active app users ÷ active members (measured over a 30-day window).
活跃 App 用户 ÷ 活跃会员（30 天窗口）。

- Directional range / 方向性区间: L2+ clubs target a meaningful majority; verify per market via `tools/04`. L2+ 场馆目标为可观多数。按市场经 `tools/04` 核验。

### #kpi-online-booking-share Online Booking Share / 线上预约占比

Online/class-app bookings ÷ total bookings.
线上/App 预约 ÷ 总预约。

- Directional range / 方向性区间: rises with digital maturity; verify per format via `tools/04`. 随数字化成熟度升。按业态经 `tools/04` 核验。

### #kpi-self-service-rate Self-Service Rate / 自助服务率

Member actions done without staff (entry, booking, plan change, FAQ bot) ÷ total actions.
无需员工的会员动作（入场、约课、改套餐、FAQ 机器人）÷ 总动作。

- Directional range / 方向性区间: 24h/unmanned models push this high; verify per format via `tools/04`. 24h/无人模式推高。按业态经 `tools/04` 核验。

### #kpi-campaign-ctr Campaign Open / CTR by Channel / 各渠道营销打开率与点击率

Email / SMS / WhatsApp / LINE / WeChat / Douyin open & click ranges. Detail + channel rules in `references/17-omnichannel-messaging.md`.
邮件/短信/WhatsApp/LINE/微信/抖音的打开与点击区间。细节与渠道规则见 `references/17`。

- Directional ranges / 方向性区间: opt-in quality beats channel — a clean consent list outperforms a bought list on any platform; verify per market via `tools/04`. 同意质量胜过渠道——干净同意名单在任何平台优于购买名单。按市场经 `tools/04` 核验。
- HI-7 / 反垃圾: only measured on opt-in lists; no consent, no send. 仅在 Opt-in 名单上测量；无同意不发送。

### #kpi-capi-match-rate CAPI Match Rate / 转化 API 匹配率

Share of offline conversions (joins, PT sales) correctly matched back to ad-platform click IDs via Conversions API.
线下转化（入会、私教销售）经转化 API 正确回匹配广告平台点击 ID 的比例。

- Directional range / 方向性区间: low match = wasted ad spend & broken attribution; improve with server-side CAPI + hashed PII; verify per platform via `tools/04`. 匹配低=广告费浪费与归因断裂；用服务端 CAPI + 哈希 PII 提升。按平台经 `tools/04` 核验。
- 🔄 Platform APIs and match methodology change frequently — re-verify before a campaign. 平台 API 与匹配方法常变——投放前重新核验。

---

## 4. IT KPIs / IT 运维 KPI

### #kpi-system-uptime System Uptime Target / 系统可用率目标

Share of time core systems (CRM/POS/gate/network) are operational.
核心系统（会籍/收银/闸机/网络）可用时间占比。

- Directional target / 方向性目标: critical entry/POS near-continuous expected; verify SLA per vendor via `tools/04`. 关键入场/收银须近持续；按供应商经 `tools/04` 核验 SLA。
- Gate uptime is life-safety-adjacent at unmanned sites — fail-open or staffed fallback required (HI-2). 无人场闸机可用率涉人身安全，须故障开放或有人兜底（HI-2）。

### #kpi-ticket-sla Ticket First-Response / Resolution SLA / 工单首响与解决 SLA

Median time to first response and to resolution for logged incidents.
已记录事件的首响中位时与解决中位时。

- Directional ranges / 方向性区间: L0 trivial faults (printer, Wi-Fi) faster than L2 integrations; verify per club size via `tools/04`. L0 琐事（打印机、Wi-Fi）快于 L2 集成。按场馆规模经 `tools/04` 核验。

### #kpi-backup-success-rate Backup Success Rate / 备份成功率

Successful automated backups ÷ scheduled backups.
成功自动备份 ÷ 计划备份。

- Directional target / 方向性目标: near-perfect expected; a single failed backup below target triggers same-day fix. 期望近完美；一次失败低于目标即当日修。
- Pair with restore test (#j-backup-3-2-1) — success rate alone lies if restores fail. 配合恢复实测——恢复失败则成功率失真。

### #kpi-wifi-satisfaction Wi-Fi Satisfaction / 无线满意度

Member-reported Wi-Fi quality (simple survey or app rating).
会员上报的无线质量（简答或 App 评分）。

- Directional range / 方向性区间: a member-experience proxy more than a tech metric; verify method via `tools/04`. 更偏会员体验代理指标而非技术指标。方法经 `tools/04` 核验。

---

## 5. Energy KPIs / 能耗 KPI

### #kpi-kwh-per-sqm kWh per Sqm / 每平米耗电

Monthly energy consumption ÷ floor area. HVAC and pools dominate.
月能耗 ÷ 面积。暖通与泳池为主。

- Directional ranges / 方向性区间: pool & sauna clubs materially above dry gyms; climate drives bands; 🔄 verify current efficiency norms per market via `tools/04`. 泳池桑拿馆远高于干区馆；气候决定区间；🔄 按市场经 `tools/04` 核验当前能效基准。
- Lever / 杠杆: schedule HVAC to occupancy; pool covers cut evaporation loss — biggest quick wins. 暖通按 occupancy 排程；泳池加盖降蒸发——最大速赢。

---

## 6. AI KPIs / AI 能力 KPI

> These are model-quality floors, not business targets. See `references/04-ai-application-landscape.md` for use cases.
> 以下为模型质量下限，非经营目标。场景见 `references/04`。

### #kpi-churn-auc Churn-Model AUC Floor / 流失模型 AUC 下限

AUC (discrimination) of a churn-prediction model on holdout data. Higher = better separation of leavers/stayers.
流失预测模型在留出集上的 AUC（区分度）。越高=离留区分越好。

- Directional floor / 方向性下限: a model near random is useless; a meaningful floor is expected before any production use — exact floor verify via `tools/04`. 近随机的模型无用；量产使用前须达有意义下限，精确下限经 `tools/04` 核验。
- Governance / 治理: churn scoring touches retention offers — keep human-in-loop, watch bias (HI-7 adjacent). 流失评分触及留存优惠——保持人在回路、防偏见（邻 HI-7）。

### #kpi-bot-deflection Bot Deflection Rate / 机器人偏转率

Member queries resolved by bot without human handoff ÷ total queries.
机器人无需转人工即解决 ÷ 总咨询。

- Directional range / 方向性区间: rises with knowledge-base quality; verify per deployment via `tools/04`. 随知识库质量升。按部署经 `tools/04` 核验。
- Guardrail / 护栏: health/medical questions must route to human or referral (HI-6) — never let the bot "diagnose." 健康/医疗问题须转人工或转介（HI-6），勿让机器人「诊断」。

### #kpi-forecast-mape Forecast MAPE / 预测 MAPE

Mean Absolute Percentage Error of demand/attendance forecasts vs actual.
需求/到场预测对实际的 MAPE（平均绝对百分比误差）。

- Directional floor / 方向性下限: lower is better; a high MAPE means the forecast isn't trusted operationally — exact acceptable band verify via `tools/04`. 越低越好；高 MAPE 意味着预测不被运营信任，可接受带经 `tools/04` 核验。
- Use / 用途: good MAPE enables smart scheduling & staffing; bad MAPE just adds noise. 好 MAPE 支撑智能排课排班；差 MAPE 只添噪声。

---

### #kpi-fdmm-ladder FDMM KPI Ladder / FDMM 的 KPI 阶梯

Don't track everything at once. The ladder says which KPIs earn their place at your level.
勿一次全盯。阶梯告诉你当前等级该配哪些 KPI。

| Level / 等级 | KPIs that matter first / 优先 KPI |
|---|---|
| L1 Paper & spreadsheet / 纸表 | #kpi-churn-rate · #kpi-arpu · #kpi-pos-reconciliation-adjacent cash · #kpi-lead-trial-join |
| L2 Single-system online / 单系统在线 | + #kpi-app-adoption · #kpi-online-booking-share · #kpi-gate-throughput |
| L3 Integrated & data-driven / 集成数据驱动 | + #kpi-ltv-cac-ratio · #kpi-class-fill-rate · #kpi-no-show-rate · #kpi-system-uptime · #kpi-backup-success-rate |
| L4 AI-augmented / AI 增强 | + #kpi-churn-auc · #kpi-bot-deflection · #kpi-forecast-mape · #kpi-capi-match-rate |
| L5 Autonomous chain / 自主连锁 | + #kpi-self-service-rate · #kpi-kwh-per-sqm · group-comparison across sites |

Add the next row only when the current one is stable — a shaky L1 tracking 30 KPIs helps no one. 当前行稳了才加下一行——L1 不稳却盯 30 个 KPI 毫无助益。

### #kpi-worksheet Benchmark Worksheet (copy-paste) / 基准工作表（可复制）

Use this every 90 days. Fill "my number", then "directional band" from above, then "gap direction".
每 90 天用一次。填「我的数值」，再从上文取「方向性区间」，再填「偏差方向」。

```
KPI / 指标        | My number / 我的值 | Directional band / 方向带 | Gap direction / 偏差方向 | My cause / 我的原因
-----------------|-------------------|--------------------------|------------------------|------------------
Churn / 流失     |                   |                          |                        |
LTV:CAC          |                   |                          |                        |
Fill rate / 满座 |                   |                          |                        |
App adoption     |                   |                          |                        |
Backup success   |                   |                          |                        |
```

Rule / 规则: a gap is only actionable after you write "my cause" — benchmarking without a cause is astrology. 除非写出「我的原因」，否则偏差不可行动——无原因的基准是对齐占星。

### #kpi-pitfalls Common Benchmark Pitfalls / 常见基准陷阱

- **Averaging across formats / 跨业态取平均**: A big-box and a boutique should never share one "average" — the spread dwarfs the signal. 大型综合与精品绝不可共享一个「平均」——离散盖过信号。
- **One month snapshot / 单月快照**: Seasonality (January join surge, summer dip) distorts; use rolling 3–6 months. 季节性（1 月入会高峰、夏季低谷）失真；用滚动 3–6 月。
- **Vanity vs leverage / 虚荣 vs 杠杆**: App adoption feels good but LTV:CAC pays the rent — weight by impact. App 渗透好看但 LTV:CAC 才付房租——按影响加权。
- **Copying a competitor's number / 抄竞对数字**: Their cost base, lease and city differ; their "good" may be your "loss." 其成本、租金、城市不同；其「好」或是你「亏」。
- **Gaming the metric / 刷指标**: Cutting churn by locking members into brutal contracts hurts experience and future joins — HI-3/ member-trust cost. 用苛刻合约压流失伤体验与未来入会——损 HI-3/会员信任。

### #kpi-worked-example Worked Directional Example (LTV:CAC) / 方向性算例（LTV:CAC）

Uses illustrative ranges only — replace with your own verified numbers; do NOT treat the example as a market fact.
仅用示意区间——换成你自核的数值，勿将示例当市场事实。

- Suppose / 假设: monthly dues margin per member = a moderate amount; average active life = a moderate number of months; PT/F&B lift = a modest %. Then LTV ≈ dues-margin × life + ancillary. 月会费毛利=中等额；平均活跃期=中等月数；私教餐饮加成=小 %。则 LTV ≈ 会费毛利×活跃期 + 附加。
- Suppose / 假设: CAC = a moderate amount from blended channels. Then LTV:CAC = LTV ÷ CAC. If the ratio lands below the directional floor, the per-member model loses money regardless of top-line growth. 若 CAC=中等额（混合渠道），则 LTV:CAC = LTV÷CAC。若低于方向性下限，单客模型亏损，与营收规模无关。
- Lesson / 启示: growth that buys members below the LTV:CAC floor is buying losses — benchmarks exist to stop that, not to brag. 低于 LTV:CAC 下限买会员是在买亏损——基准的意义在止损而非炫耀。

### #kpi-monthly-review Monthly KPI Review Agenda / 月度 KPI 复盘议程

A 30-minute monthly loop keeps benchmarks useful. Copy this.
30 分钟月度循环让基准有用。直接复制。

1. Pull the ≤10 KPIs for your FDMM level from the dashboard. 从看板取你 FDMM 等级的 ≤10 个 KPI。
2. Compare each to its directional band + your own 90-day trend. 各自比对方向性区间 + 自身 90 天趋势。
3. Write "my cause" for every gap beyond a band you set. 对超自定带的每个偏差写「我的原因」。
4. Pick ONE KPI to act on next month; ignore the rest. 选 ONE 个下月行动，其余忽略。
5. Note any number older than 180 days as "TO VERIFY" and trigger `tools/04`. 超 180 天数值标「待复核」并触发 `tools/04`。

### #kpi-honesty Honesty Note on These Numbers / 关于这些数值的诚实声明

No figure in this file is a measured market average. Each is a DIRECTIONAL range assembled from experience and must be re-verified per market/format/era via `tools/04` before it informs a budget or a board slide. Citing any of them as "the industry average" would violate Iron Law 10.
本文件无任何「测得的市场平均」。每个都是经验汇总的方向性区间，在影响预算或董事会材料前须按市场/业态/时代经 `tools/04` 重新核验。将其称为「行业平均」即违反铁律 10。

> **G13 tri-perspective note / 三视角注记**: Architect — KPIs are the measurement layer of the FDMM; pick ≤10 that match your level, not all 30. Operator — track a small dashboard weekly; a number is a question, not a verdict. Member — behind every KPI (churn, fill, no-show) is a person's experience; optimize the metric by improving the experience, never by gaming it.
> **G13 三视角注记**：架构师——KPI 是 FDMM 的度量层，按等级选 ≤10 个而非全 30。运营者——每周盯小看板，数字是问题不是判决。会员——每个 KPI（流失、满座、爽约）背后都是人的体验；靠改善体验而非刷数据来优化指标。
