# FDMM Assessment Worksheet / FDMM 成熟度评估工作表

> **Cluster / 集群**: I (governance & money), X (methodology)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: re-assess every 90–180 days; re-verify regulation red lines via `tools/05` before each round. / 每 90–180 天复评；每轮前经 `tools/05` 复核实红线。
> **Cross-references / 交叉引用**: `tools/01-fdmm-maturity-assessment.md` (model + anchors) · `references/05-methodology-library.md` §1 · `templates/01-three-year-digital-strategy.md` (uses snapshot) · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04`。

---

## ① Purpose & When to Use / 用途与使用时机 {#purpose}

The operational companion to `tools/01`: a fill-in sheet to score your club across six dimensions × five levels, collect evidence, plot a radar, and list gap-to-target actions. Run it as your entry diagnostic — and again every quarter.
`tools/01` 的可操作配套：一张填写表，把场馆按六维度×五级打分、采集证据、画雷达、列差距行动。作为入场诊断跑——之后每季度再跑。

> **FDMM level gate / 成熟度闸口**: **Any level — this is the starting point.** Even an L1 paper-club completes it (the result will simply be "L1 everywhere", which is the honest baseline).
> **FDMM 等级闸口**：**任何等级——这是起点**。L1 纸表馆也跑（结果就是「处处 L1」，即诚实基线）。

> **What good looks like / 好答案长什么样**: each dimension gets one level with a cited evidence note; the radar shows the lopsided shape; gap rows name the next level's entry criterion as the action.
> **好答案长什么样**：每维度取一级并附证据；雷达显出偏科形状；差距行把下一级准入条件列为行动。

> **Red flag / 红旗**: "we're L4" with no evidence note on any dimension → self-grade inflation. Force evidence or drop a level. / 无任何维度证据的「我们是 L4」→ 自评虚高。强制补证据或降级。

---

## ② Prerequisites & Inputs Checklist / 前置条件与输入清单 {#prerequisites}

- [ ] List of systems actually live (not "planned"). / 实际在线的系统清单（非「计划」）。
- [ ] Last 90 days of ops data if any (attendance, complaints). / 近 90 天运营数据（如有）。
- [ ] `tools/01` open for the model + level anchors. / 打开 `tools/01` 看模型与等级锚点。
- [ ] A quiet 60 minutes and a honest colleague. / 安静 60 分钟 + 一位诚实同事。

---

## ③ The Template / 模板正文 {#template}

### 3.1 Six-Dimension × Five-Level Scoring Grid / 六维×五级评分网格 {#s-grid}

> Circle ONE level per dimension. Descriptors are bilingual; pick the highest level where ALL bullets in that cell are true.
> 每维度圈一级。描述为双语；选「该格所有要点都为真」的最高等级。

| Dimension / 维度 | L1 / 纸表 | L2 / 单系统在线 | L3 / 集成数据驱动 | L4 / AI 增强 | L5 / 自主连锁 |
|---|---|---|---|---|---|
| **Member / 会员** | Paper sign-in, Excel list / 纸质签到、Excel 名单 | CRM + QR entry / CRM+扫码入场 | CRM+app+gate integrated / CRM+App+闸机打通 | Churn-AI in use / 流失 AI 在用 | Self-optimizing journeys / 自优化旅程 |
| **Operations / 运营** | Manual rosters / 手工排班 | Daily digital report / 数据日报 | Dashboard + alerts / 看板+告警 | Smart scheduling / 智能排课 | Autonomous ops periods / 自主运营时段 |
| **Infrastructure / 基础设施** | Home Wi-Fi / 家用 Wi-Fi | Dedicated network + UPS / 专用网+UPS | VLAN + SD-WAN multi-site / VLAN+多店 SD-WAN | Redundant core / 冗余核心 | Self-healing fabric / 自愈合架构 |
| **Data / 数据** | Scattered files / 散文件 | One member DB / 单一会员库 | Integrated warehouse / 集成数仓 | Clean single-source / 干净唯一口径 | Group brain / 集团大脑 |
| **AI / AI** | None / 无 | None / 无 | ≥2 prod use cases w/ ROI / ≥2 量产场景有 ROI | Churn+CV+agent / 流失+CV+Agent | Self-learning loop / 自学习闭环 |
| **Governance / 治理** | No charter / 无章程 | Ad-hoc approval / 临时审批 | Charter + budget / 章程+预算 | Stage-Gate S1–S8 / 阶段门全跑 | Continuous audit / 持续审计 |

### 3.2 Score Capture & Evidence / 评分与证据 {#s-evidence}

| Dimension / 维度 | My level / 我的级 | Evidence note / 证据 | Source / 来源 |
|---|---|---|---|
| Member / 会员 | L__ | ___ | ___ |
| Operations / 运营 | L__ | ___ | ___ |
| Infrastructure / 基础设施 | L__ | ___ | ___ |
| Data / 数据 | L__ | ___ | ___ |
| AI / AI | L__ | ___ | ___ |
| Governance / 治理 | L__ | ___ | ___ |

> **Evidence-collection prompts / 证据采集提示**: "Show me the system login." / 给我看系统登录。"Export one week of attendance." / 导出一周考勤。"Name the approver of last purchase." / 说出上次采购的审批人。No artifact = level too high. / 拿不出物证 = 等级虚高。

### 3.3 Radar-Chart Data Table / 雷达图数据表 {#s-radar}

> Score each dimension 1–5 (L1=1 … L5=5). Plot in any radar tool; the shape reveals imbalance.
> 每维度打 1–5 分（L1=1…L5=5）。用任意雷达工具绘；形状显偏科。

| Axis / 轴 | Score 1–5 / 分 | Target in 1 yr / 一年目标 |
|---|---|---|
| Member / 会员 | __ | __ |
| Operations / 运营 | __ | __ |
| Infrastructure / 基础设施 | __ | __ |
| Data / 数据 | __ | __ |
| AI / AI | __ | __ |
| Governance / 治理 | __ | __ |

### 3.4 Gap-to-Target Action Rows / 差距行动行 {#s-gap}

> For each dimension below target, write the NEXT level's entry criterion as the action (from `SKILL.md` FDMM table).
> 对每个低于目标的维度，把「下一级准入条件」写成行动（取自 `SKILL.md` FDMM 表）。

| Dimension / 维度 | Current→Target / 当前→目标 | Action (next-level entry) / 行动（下一级准入） | Owner / 负责人 |
|---|---|---|---|
| ___ | L__→L__ | e.g. "integrate ≥3 systems, unify ID" / 集成≥3系统、身份归一 | ___ |
| ___ | | | |

> **Worked micro-example / 微例**: Infrastructure L1→L2 action = "install dedicated club network + UPS; retire home Wi-Fi" (addresses `data/21-anti-pattern-library.md#ap-010`). / 基础设施 L1→L2 行动 =「装专用馆网+UPS，退家用 Wi-Fi」（对应 `data/21#ap-010`）。

---

### 3.5 Per-Dimension Evidence Prompts / 逐维证据提示 {#s-prompts}

| Dimension / 维度 | Ask yourself / 自问 | Artifact if true / 若为真的物证 |
|---|---|---|
| Member / 会员 | Can a member book & enter without paper? / 会员能无纸约课入场？ | App + QR logs / App+扫码日志 |
| Operations / 运营 | Do you get a daily digital report? / 有每日数据报告？ | Dashboard screenshot / 看板截图 |
| Infrastructure / 基础设施 | Is the network dedicated, not home Wi-Fi? / 网络专用非家用？ | Topology + UPS invoice / 拓扑+UPS 发票 |
| Data / 数据 | Is there one member database? / 有单一会员库？ | DB schema / 库结构 |
| AI / AI | Any AI in production with measured ROI? / 有量产且 ROI 可测的 AI？ | ROI case (`templates/07`) / ROI 案 |
| Governance / 治理 | Is there a signed charter? / 有签署章程？ | `templates/04` signed / 已签章程 |

> No artifact = the level claim is unsupported; score one level lower. / 无物证 = 等级主张无支撑；降一级。

### 3.6 Worked Scoring Example / 评分实例 {#s-example}

> A 2-club L2 operator's realistic self-grade: / 某 2 店 L2 运营者的真实自评：

| Dimension / 维度 | Level / 级 | Evidence / 证据 |
|---|---|---|
| Member / 会员 | L2 | CRM + QR entry live / CRM+扫码在线 |
| Operations / 运营 | L2 | daily digital report / 每日数据报告 |
| Infrastructure / 基础设施 | L2 | dedicated net + UPS / 专用网+UPS |
| Data / 数据 | L2 | one member DB / 单一会员库 |
| AI / AI | L1 | none yet / 尚无 |
| Governance / 治理 | L2 | ad-hoc approval logged / 临时审批有记录 |

> Radar shows AI + Governance as the two low axes → the gap-to-target plan prioritizes an AI pilot (L1→L2 in AI = first prod use case) and a signed charter (L2→L3 in governance). / 雷达显 AI+治理两低轴 → 差距计划优先 AI 试点（AI L1→L2=首个量产场景）与签章程（治理 L2→L3）。

### 3.7 Re-Assessment Cadence / 复评节奏 {#s-cadence}

| Trigger / 触发 | Action / 动作 |
|---|---|
| Every 90 days / 每 90 天 | re-run §3.1–§3.4, update radar / 重跑 §3.1–§3.4、更新雷达 |
| After any S4 buy / 任何 S4 采购后 | re-score affected dimension / 重评受影响维度 |
| Market/regulation shift / 市场法规变 | re-verify HI red lines via `tools/05` / 经 `tools/05` 复核 HI 红线 |

> Track movement as "L__→L__" in `templates/01` snapshot; stagnation for 2 cycles = a gap-to-target plan is not being executed. / 在 `templates/01` 快照记「L__→L__」；连续 2 周期停滞=差距计划未执行。

### 3.8 Volatile-Fact Hook / 易变事实钩子 {#s-hook}

:::dynamic-hook topic="fitness-maturity-benchmark-distribution" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07, cross-market FDMM distribution benchmarks (what % of clubs sit at L1–L5 by format) shift with market maturity; verify via `tools/04` when benchmarking your score against peers — your self-grade is the source of truth, not a peer average.
截至 2026-07，跨市场 FDMM 分布基准（各业态 L1–L5 占比）随市场成熟度浮动；对标同行时经 `tools/04` 核验——你的自评才是真相，非同行均值。
:::

## ④ Common Mistakes / 常见错误 {#mistakes}

- **Self-grade inflation** → no evidence = no level. Force `tools/01` discipline. / 自评虚高 → 无证据无等级。强制 `tools/01` 纪律。
- **Ignoring governance dimension** → charter-less clubs fail at S4. See `data/21-anti-pattern-library.md#ap-002`. / 忽略治理维度 → 无章程馆卡在 S4。
- **One score for whole club** → score per dimension; a club can be L4 in Member, L1 in AI. / 全馆一个分 → 要逐维打分；可会员 L4、AI L1。
- **No re-assessment cadence** → stale FDMM misleads strategy. Re-run quarterly. / 无复评节奏 → 过时 FDMM 误导战略。季度重跑。

---

## ⑤ Related Files / 相关文件 {#related}

- `tools/01-fdmm-maturity-assessment.md` — model + level anchors. / 模型与等级锚点。
- `templates/01-three-year-digital-strategy.md` — consumes the snapshot. / 消费快照。
- `templates/04-digital-charter-and-stage-gate.md` — governance gate. / 治理门。
- `references/05-methodology-library.md` §1 — FDMM recap. / FDMM 回顾。
- `data/21-anti-pattern-library.md` — failure patterns. / 失败模式。

---

## ⑥ G13 Tri-Perspective Note / 三视角覆盖备注 {#g13}

> **Architect** (six-dimension grid makes maturity legible & comparable) × **Operator** (evidence prompts + gap rows give the solo steward a concrete next-step list) × **Member** (honest leveling prevents over-promising features members never receive). / **架构**（六维网格让成熟度可读可比）× **商家**（证据提示+差距行给一人总管具体下一步清单）× **会员**（诚实定级避免夸大会员永远用不上的功能）。
