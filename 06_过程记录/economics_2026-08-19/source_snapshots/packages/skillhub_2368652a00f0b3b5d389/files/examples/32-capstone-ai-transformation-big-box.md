# 32 · Capstone: AI Transformation of an 8000-Member Big-Box Flagship / 案例 32：8000 会员大型旗舰馆 AI 转型

> **Cluster / 集群**: E (data & AI) · K (AI governance) · B (software) · I (governance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: vendor/AI-model status 🔄 via `tools/04`; ROI scenarios per `tools/06`; bias/drift controls per `references/13`; compliance per `tools/05` every 90d.
> **Cross-references / 交叉引用**: `templates/27-ai-customer-service-launch.md` · `templates/08-pilot-validation-plan.md` · `references/04-ai-application-landscape.md` · `references/13-data-and-llm-engine.md` · `tools/06-roi-three-scenario.md` · `data/09-algorithm-kernel-library.md` · `playbooks/05` (governance)
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## Honesty Preamble / 诚实前言

> Archetypal composite case for teaching — an amalgam of big-box AI programs observed across APAC. **Not** a claimed real club. Figures are directional; model names and prices are ranges with confidence notes, not quotes.
> 典型复合教学案例——糅合亚太大型馆 AI 项目常见模式。**非**真实场馆。数字方向性；模型名与价为带置信区间的示意，非报价。

> AI use cases touching churn, posture (CV), pricing and health inference are HIGH-RISK (G7): each carries bias/drift/human-in-loop controls. Where a use case failed the HI-1 gate, it was PAUSED — documented below, not hidden.
> 涉流失、体态(CV)、定价、健康推断的 AI 为高险（G7）：各带偏见/漂移/人在回路控制。未过 HI-1 闸的用例即**暂停**——下文明示非藏。

---

## ① Context Card / 情境卡

| Field / 字段 | Value / 值 |
|---|---|
| Archetype / 原型 | 8000-member big-box flagship, single market / 8000 会员大型旗舰，单市场 |
| Starting FDMM / 起点 | L2 (membership SaaS + QR entry) / L2（会籍 SaaS+扫码） |
| Target FDMM / 目标 | L4 (AI-augmented) in 24 months / 24 个月达 L4（AI 增强） |
| Timeline / 周期 | 24 months / 24 个月 |
| AI ladder / AI 阶梯 | churn → scheduling → LLM CS → CV posture → AIGC → energy / 流失→排课→客服→体态→内容→能效 |
| Honesty scope / 诚实范围 | composite; directional ranges; 1 use case killed at pilot / 复合；方向性；1 用例试点被砍 |

### Key Numbers at a Glance / 关键数字一览

| Metric / 指标 | Value / 值 |
|---|---|
| Members / 会员 | 8000 |
| Duration / 周期 | 24 months / 24 月 |
| AI use cases shipped / 量产AI | 5 of 7 scoped / 7定中5 |
| Use cases paused/killed / 暂停/砍 | 2 (CV @HI-1, dynamic pricing @trust) / 2 |
| FDMM L2 → L4 | yes, with measured ROI / 是，ROI可测 |
| Investment / 投资 | ¥6–9M directional / 方向性 600–900万 |

These are directional illustrations, not audited figures — re-estimate per `tools/06` before any real business case.
**均为方向性示意非审计数**——真实立项前按 tools/06 重估。

---

## ② Multi-Phase Journey / 多阶段旅程（24 个月）

### Phase 1 — The Unglamorous 6 Months: Data Cleanup (M1–6) / 阶段一 不起眼的 6 个月：数据清洗

**Situation / 形势**: The club had 8000 members but 31% duplicate/garbage records, no unified ID, and 3 systems that disagreed on "active." AI on this data would have been confident and wrong.
**形势**：8000 会员却有 31% 重复/脏记录，无统一 ID，3 套系统对「活跃」定义不一。在此数据上跑 AI 会自信地错。

**Decision forks considered / 决策分叉**:
- *Fork — buy AI now vs clean first.* Rejected "buy AI now": garbage-in-garbage-out; chose **6-month cleanup first** (Iron Law 7 evolvable architecture — earn L3 before L4).
  *分叉 — 现在买 AI vs 先洗。否决「现在买」：垃圾进垃圾出；选**先洗 6 个月**（铁律7 可演进——先 L3 再 L4）。*
- *Fork — full re-platform vs reconcile in place.* Chose **reconcile + unified ID** (cheaper, faster), deferring re-platform.
  *分叉 — 全重铸 vs 就地对账。选**对账+统一 ID**（更省更快），重铸暂缓。*

**Library artifacts used / 引用库工件**: `references/04` §data-foundation · `data/09-algorithm-kernel-library.md` (dedupe kernel) · `references/13` §K data governance.
**Outcome / 结果**: Duplicate rate to 4%; unified member ID; daily dashboard live — club reached L3 at M6, the gate to touch AI.
**结果**：重复率降至 4%；会员 ID 统一；日看板上线——M6 达 L3，触 AI 的闸门。

**Data cleanup detail (the unglamorous 6 months) / 清洗明细（不起眼 6 月）**:

| Step / 步 | Action / 动作 | Result / 结果 |
|---|---|---|
| Dedupe / 去重 | `data/09` kernel on phone+name / 按手机+名 | 31%→4% dup / 31→4%重复 |
| Unify ID / 统一ID | map 3 systems to 1 key / 3系统映1键 | single member record / 单一档案 |
| Validate / 校验 | schema + boundary check / 结构+边界查 | bad rows quarantined / 坏行隔离 |
| Dashboard / 看板 | daily automated pull / 日自动拉 | L3 reached / 达L3 |

This is the part no one photographs — and the part that decided whether every later AI number was real or a mirage.
**这是无人拍照的部分**——却决定了后续每个 AI 数是真还是幻。

### Phase 2 — Churn Model with Bias Audit (M6–12) / 阶段二 带偏见审计的流失模型

**Situation / 形势**: First production AI use case. Model predicted churn at 0.78 AUC but a bias audit flagged older-female members systematically under-scored.
**形势**：首个量产 AI 用例。模型 AUC 0.78，但偏见审计发现年长女性会员被系统性低估。

**Decision forks considered / 决策分叉**:
- *Fork — ship as-is vs re-weight.* Rejected "ship as-is": G7 + HI-8 minimization; chose **re-weight + fairness slice test** before go-live.
  *分叉 — 原样上 vs 重加权。否决「原样上」：G7+HI-8 最小化；选**重加权+公平性切片测试**后再上。*
- *Fork — black-box vs explainable.* Chose **explainable** output so coaches could act, not just score.
  *分叉 — 黑盒 vs 可解释。选**可解释**输出，教练能行动非仅打分。*

**Library artifacts used / 引用库工件**: `references/04` §churn-AI · `references/13` §K bias/drift · `data/09` (fairness kernel) · G7 gate.
**Outcome / 结果**: Bias gap closed to <2pp; churn intervention ran; retention +2.4pp in pilot cohort.
**结果**：偏见差收至 <2pp；流失干预运行；试点群留存 +2.4pp。

### Phase 3 — Smart Scheduling + AI Customer Service w/ Kill-Switch (M12–18) / 阶段三 智能排课 + 带急停的大模型客服

**Situation / 形势**: Two parallel builds — class-demand scheduling optimizer, and an LLM customer-service agent for FAQs.
**形势**：两并行建设——课程需求排课优化器，与 FAQ 大模型客服 Agent。

**Decision forks considered / 决策分叉**:
- *Fork — AI CS fully autonomous vs supervised with kill-switch.* Rejected "fully autonomous": member-trust + HI-7 consent risk. Chose **LLM CS behind a kill-switch** per `templates/27` — human can flip it off in one click; escalates to human on low-confidence.
  *分叉 — 客服全自主 vs 监督+急停。否决「全自主」：会员信任+HI-7 同意风险。选**大模型客服带急停**（templates/27）——人工一键关；低置信转人工。*
- *Fork — scheduling auto-publish vs recommend.* Chose **recommend + manager approve** for first 2 months, then auto.
  *分叉 — 排课自动发 vs 推荐。选**推荐+店长批**前 2 月，后转自动。*

**Library artifacts used / 引用库工件**: `templates/27-ai-customer-service-launch.md` · `references/04` §smart-scheduling · `references/17` (channel consent, HI-7).
**Outcome / 结果**: CS deflection 38% of tickets; kill-switch exercised once in drill (clean handoff). Scheduling no-show down 11%.
**结果**：客服拦截 38% 工单；急停演练用过一次（交接干净）。排课爽约降 11%。

### Phase 3.5 — Member-Trust Instrumentation / 阶段 3.5 会员信任仪表

**Goal / 目标**: Before any customer-facing AI shipped, the club stood up a lightweight trust signal panel — because the Skill's Iron Law 12 says "to the member, respect opt-in" and HI-7 forbids send-without-consent. This is what later killed dynamic pricing.
**目标**：任何面向会员的 AI 上线前，场馆立轻量信任信号面板——因铁律12「对会员守 Opt-in」、HI-7 禁无同意发送。此即后来砍动态定价之据。

**Trust signals tracked / 追踪的信任信号**:

| Signal / 信号 | How measured / 量法 | Threshold / 阈值 |
|---|---|---|
| CS opt-out rate / 客服退订率 | unsubscribe after AI reply / AI回复后退订 | >3% → review / 超3%复审 |
| Pricing complaint sentiment / 定价投诉情绪 | survey + social scan / 调研+社媒扫 | red → kill pilot / 红砍试点 |
| Consent freshness / 同意新鲜度 | re-opt-in every 12mo / 每12月重Opt-in | lapse = stop / 失效即停 |
| Explainability rating / 可解释评分 | coach feedback / 教练反馈 | <3/5 → tune / 低于调 |

The panel was the early-warning system: dynamic pricing lit the "pricing complaint sentiment" signal red in week 2 of pilot — the kill switch for that use case, applied before any member was actually over-charged.
**此面板即预警**：动态定价试点第 2 周亮「定价投诉情绪」红——该用例急停，先于任何会员真被多收。

### Phase 4 — CV Posture Pilot PAUSED at HI-1 Gate (M18–21) / 阶段四 CV 体态试点在 HI-1 闸暂停

**Situation / 形势**: A computer-vision posture-assessment pilot on the gym floor. It needed camera coverage that, in one market's reading, risked capturing minors and changing-room approaches.
**形势**：训练区计算机视觉体态评估试点。需摄像头覆盖，按某市场解读，有拍到未成年人、逼近更衣室之险。

**Decision forks considered / 决策分叉**:
- *Fork — continue pilot vs pause.* Rejected "continue": **HI-1 (minors' data basis) + HI-5 (no camera in changing room) unresolved** in that market. Chose **PAUSE** at the gate — no biometric/minors data without legal basis.
  *分叉 — 续试点 vs 暂停。否决「续」：**HI-1（未成年人数据依据）+HI-5（更衣室禁摄像）在该市场未解**。选**闸口暂停**——无法律依据不采生物/未成年人数据。*
- *Fork — blur faces vs delay.* Chose **delay + re-scope to consenting adults in a fenced zone** with local template storage; revisit after `tools/05` clearance.
  *分叉 — 人脸模糊 vs 延。选**延+重划至同意成年人封闭区**+本地模板存储；tools/05 清关后复审。*

**Library artifacts used / 引用库工件**: HI-1 / HI-5 hard invariants · `tools/05` (minor+biometric basis) · `references/12-biometrics-and-cctv.md` · `templates/08-pilot-validation-plan.md` (go/no-go gate).
**Outcome / 结果**: Pilot formally PAUSED; documented as a discipline win, not a failure. Saved the club from a likely compliance breach and a member-trust hit.
**结果**：试点正式暂停；记为纪律性胜利非失败。使场馆免于一桩可能合规破防与会员信任重挫。

### Phase 5 — AIGC Content Workbench + Energy AI (M21–24) / 阶段五 AIGC 内容工作台 + 能效 AI

**Situation / 形势**: Marketing team drowned in post production; building HVAC ran on fixed timers.
**形势**：市场部淹没在内容生产；楼宇 HVAC 走固定定时。

**Decision forks considered / 决策分叉**:
- *Fork — buy content agency vs AIGC workbench.* Chose **AIGC workbench** (brand-safe templates, human approves) — cut production time ~50%.
  *分叉 — 买外包 vs AIGC 工作台。选**AIGC 工作台**（品牌安全模板、人审）——生产时省约 50%。*
- *Fork — energy AI vs fixed schedule.* Chose **occupancy-driven energy AI** (fail-safe, human override) — est. 8–14% saving.
  *分叉 — 能效 AI vs 固定表。选** occupancy 驱动能效 AI**（故障安全、人可覆）——估省 8–14%。*

**Library artifacts used / 引用库工件**: `references/04` §AIGC · `references/13` §K (human-in-loop) · `references/16` §R (energy, fail-safe).
**Outcome / 结果**: At M24 the club hit L4 — ≥2 AI use cases in production with measured ROI; replicated playbook drafted.
**结果**：M24 达 L4——≥2 AI 量产且 ROI 可测；复制打法草拟。

### Phase 5.5 — AI Use-Case Scorecard (go/no-go log) / 阶段 5.5 AI 用例记分卡（go/no-go 日志）

**Goal / 目标**: Every AI idea was scored against the FDMM ladder, G7 risk, and HI-1~HI-8 before build. This is the honest log — including the two that did NOT ship.
**目标**：每 AI 创意建前按 FDMM 阶梯、G7 风险、HI-1~HI-8 打分。此即诚实日志——含两个未上的。

| Use case / 用例 | Risk / 风险 | Gate / 闸门 | Decision / 决策 |
|---|---|---|---|
| Churn model / 流失模型 | Medium (G7) | bias audit pass / 过偏见审 | GO (re-weighted) / 上(重加权) |
| Smart scheduling / 智能排课 | Low | manager approve / 店长批 | GO / 上 |
| LLM CS / 大模型客服 | Medium (HI-7) | kill-switch / 急停 | GO (`templates/27`) / 上 |
| CV posture / CV体态 | High (HI-1/HI-5) | legal basis missing / 缺依据 | **PAUSE** at HI-1 / HI-1闸暂停 |
| AIGC workbench / AIGC台 | Low | human approve / 人审 | GO / 上 |
| Energy AI / 能效AI | Low (fail-safe) | human override / 人可覆 | GO / 上 |
| Dynamic pricing / 动态定价 | High (trust) | member signal red / 信任红 | **KILL** at pilot / 试点砍 |

The scorecard is the discipline artifact — it makes "we paused" and "we killed" visible, not buried. `references/04` §U lists the full 50+ landscape; this club shipped 5 of them.
**记分卡即纪律工件**——使「暂停」「砍掉」可见非埋。references/04 §U 列 50+ 全景；本馆量产其中 5 个。

---

## ③ Three Major Setbacks & Recovery / 三大挫折与复原

**Setback 1 — Garbage data nearly shipped AI / 挫折一 脏数据险些上线 AI**: At M2 the churn model trained on un-cleaned data showed 0.81 AUC — a mirage. Recovery: forced the 6-month cleanup gate; re-baselined. Lesson: maturity gate is non-negotiable (Iron Law 7).
**挫折一**：M2 流失模型用未洗数据显 0.81 AUC——海市蜃楼。复原：强推 6 月清洗闸；重基线。教训：成熟度闸不可谈（铁律7）。

**Setback 2 — Bias audit flagged unfairness / 挫折二 偏见审计亮不公**: Older-female members under-scored. Recovery: re-weight + fairness slice; 3-week delay. Lesson: G7 bias control is a ship gate, not a post-mortem.
**挫折二**：年长女性被低估。复原：重加权+公平切片；延 3 周。教训：G7 偏见控制是上线闸非事后查。

**Setback 3 — CV pilot hit HI-1/HI-5 wall / 挫折三 CV 试点撞 HI-1/HI-5 墙**: Could not clear minors/changing-room basis. Recovery: PAUSED, re-scoped to consenting adults. Lesson: go/no-go discipline at `templates/08` gate protects the brand. **Dynamic pricing killed at pilot — member trust signal**: a dynamic class-pricing test read as "nickel-and-diming" in surveys; killed at pilot (HI-3/prepaid-trust). Lesson: not every AI that works technically earns member trust.
**挫折三**：清不掉未成年/更衣室依据。复原：暂停+重划同意成人。教训：templates/08 闸的 go/no-go 护品牌。**动态定价试点被砍——会员信任信号**：动态课时定价在调研中被读成「薅羊毛」；试点即砍（HI-3/预付信任）。教训：技术上跑得通的 AI 未必赢得会员信任。

---

## ④ Financials View (Directional) / 财务视角（方向性）

**Investment envelope / 投资带**: directional ¥6–9M over 24 months — data cleanup 15%, churn+scheduling 25%, AI CS+kill-switch 20%, CV pilot (written off partially) 10%, AIGC+energy 20%, governance/bias audit 10%.
**投资带**：24 个月 600–900 万元——清洗 15%、流失+排课 25%、客服+急停 20%、CV 试点（部分核销）10%、AIGC+能效 20%、治理/偏见审 10%。

**Payback narrative / 回收叙事**: Levers — churn retention (+2.4pp ≈ ¥X saved), CS deflection (38% tickets ≈ headcount avoid), no-show cut (11% ≈ capacity recovered), energy (8–14%). Directional payback 20–30 months.
**回收叙事**：杠杆——留存(+2.4pp≈省 X)、客服拦截(38%≈免人)、爽约降(11%≈产能回)、能效(8–14%)。方向性回收 20–30 月。

**Three-scenario retrospective per `tools/06` / 三情景复盘（按 tools/06）**:

| Scenario / 情景 | Assumed / 假设 | Landed? / 落点 |
|---|---|---|
| Base / 基准 | 2 use cases live, payback 28mo / 2 用例、回收 28 月 | Landed / 落点 |
| Expected / 预期 | churn -3pp, CS 40%, energy 12% / 流失-3pp、客服40%、能效12% | **Beat on CS (38% vs 40% near) + energy (≈12%); missed churn (-2.4pp)** / 客服近达标、能效达标；流失未达(-2.4pp) |
| Pessimistic / 悲观 | CV ships, breach fine / CV 上线、违规罚 | **Avoided** — CV paused at HI-1, no fine / 规避——CV 于 HI-1 暂停，无罚 |

**Did expected case land? / 预期是否落地？**: Mostly. The CV pause and dynamic-pricing kill were "losses" on paper but **risk-avoided wins** — no fine, no trust breach. Net ROI positive, slightly below expected midpoint due to churn lag.
**预期是否落地？**：大体是。CV 暂停与定价被砍账面是「亏」，实为**避险赢**——无罚无信任破。净 ROI 正，因流失滞后略低于预期中值。

**Savings-lever detail (directional) / 节支杠杆明细（方向性）**:

| Lever / 杠杆 | Expected / 预期 | Landed / 落点 |
|---|---|---|
| Retention (+churn) / 留存 | +3pp | +2.4pp (miss) |
| CS deflection / 客服拦截 | 40% | 38% (near) |
| No-show cut / 爽约降 | — | 11% (beat) |
| Energy save / 能效 | 12% | ~12% (beat) |
| AIGC time cut / AIGC省时 | 50% | ~50% (beat) |
| Risk avoided (CV/pricing) / 避险 | — | fine + trust breach avoided / 免罚+免破信 |

**What we would redo / 重做之处**: (1) Run the bias audit in parallel with model build, not after — saved 3 weeks; (2) test dynamic pricing as a member-survey FIRST, not a live pilot; (3) scope CV to consenting adults from day one to clear HI-1 faster.
**重做之处**：(1) 偏见审计与建模并行非事后——省 3 周；(2) 动态定价先会员调研非现场试点；(3) CV 首日即划同意成人以快清 HI-1。

---

## ⑤ Org & People Evolution / 组织与人才演进

- **M1**: 1 data analyst, no AI owner. / 1 数据分析，无 AI 负责人。
- **M6**: AI product owner hired; bias-review routine stood up. / 设 AI 产品负责人；偏见复审例程立。
- **M12**: coaches trained to read explainable churn scores. / 教练受训读可解释流失分。
- **M18**: CS kill-switch drill in runbook; on-call human escalator named. / 客服急停演练入手册；人工升级岗点名。
- **M24**: AI council (4 roles per `references/13`) reviews new use cases against HI-1~HI-8.
**M24**：AI 理事会（references/13 四角色）按 HI-1~HI-8 审新用例。

The shift: from **"AI = magic"** to **"AI = use case with a gate."** The kill-switch drill made the board comfortable; the HI-1 pause made members safe.
**转变**：从「AI=魔法」到「AI=带闸的用例」。急停演练安了董事会心；HI-1 暂停护了会员安。

**AI governance table (the 4-role council) / AI 治理表（四角色理事会）**:

| Role / 角色 | Who / 谁 | Duty / 职责 |
|---|---|---|
| Proposer / 提议 | AI product owner / AI产品负责人 | scope + ROI / 范围+ROI |
| Verifier / 核验 | Data scientist / 数据科学家 | G7 bias/drift check / G7偏见漂移查 |
| Adversary / 对抗 | Compliance lead / 合规负责人 | HI-1~HI-8 challenge / HI-1~HI-8挑刺 |
| Arbiter / 裁决 | GM + owner / 总经理+老板 | go/no-go sign / 准驳签 |

This mirrors `references/13` §K council model; it is what turned a scary "AI" word into a weekly 30-minute review.
**此即 references/13 §K 理事会模型**；它把吓人的「AI」词变每周 30 分评审。

---

## ⑥ Ten Transferable Lessons / 十条可迁移经验

1. **Earn L3 before L4** — 6 months of cleanup was the unglamorous key. / 先 L3 再 L4——6 月清洗是不起眼钥匙。
2. **Bias audit is a ship gate, not post-mortem** — G7 forced fairness before go-live. / 偏见审计是上线闸非事后——G7 逼出上线前公平。
3. **Kill-switch is non-negotiable for AI CS** — `templates/27` one-click off. / 客服急停不可谈——templates/27 一键关。
4. **HI-1/HI-5 are hard walls** — CV paused, no apology needed. / HI-1/HI-5 是硬墙——CV 暂停无需歉。
5. **Technical win ≠ trust win** — dynamic pricing killed on member signal. / 技术赢≠信任赢——动态定价因会员信号被砍。
6. **Explainable > black-box** — coaches acted on scores. / 可解释>黑盒——教练据分行动。
7. **Reconcile before re-platform** — cheaper, faster path to unified ID. / 先对账再重铸——统一 ID 更省更快。
8. **Energy AI pays fail-safe** — 8–14% saving with human override. / 能效 AI 带故障安全——省 8–14% 且人可覆。
9. **AIGC workbench needs human approve** — brand-safe, 50% time cut. / AIGC 工作台需人审——品牌安全、省时 50%。
10. **Document the pause** — a paused pilot is a discipline win, not a failure. / 记下暂停——暂停是纪律胜利非失败。

---

## ⑦ Related Files / 相关文件

- `templates/27-ai-customer-service-launch.md` — the kill-switch spec. / 急停规范。
- `templates/08-pilot-validation-plan.md` — go/no-go gate. / go/no-go 闸。
- `references/04-ai-application-landscape.md` — 50+ AI scenarios. / 50+ AI 场景。
- `references/13-data-and-llm-engine.md` — bias/drift/human-in-loop. / 偏见/漂移/人在回路。
- `tools/06-roi-three-scenario.md` — ROI framing. / ROI 框架。
- `references/12-biometrics-and-cctv.md` · `tools/05` — HI-1/HI-5 basis. / HI-1/HI-5 依据。
- `data/09-algorithm-kernel-library.md` — dedupe/fairness kernels. / 去重/公平核。

---

## ⑧ G13 Note / G13 注记

**Architect / 架构师**: FDMM gate (L3 before L4), G7 bias/drift controls, HI-1/HI-5 hard walls, kill-switch in the AI CS design, UTC-free local data minimization. Every use case carries a go/no-go gate (`templates/08`).
**架构师**：FDMM 闸（先 L3 再 L4）、G7 偏见/漂移控制、HI-1/HI-5 硬墙、客服急停设计、本地数据最小化。每用例带 go/no-go 闸（templates/08）。

**Operator / 运营者**: The kill-switch drill + human escalator meant a bad AI answer never reached a member unattended. Coaches got explainable scores, not black-box orders.
**运营者**：急停演练+人工升级岗=坏 AI 答案绝不无人经手到会员。教练拿可解释分非黑盒令。

**Member / 会员**: No camera in the changing room; no minors' biometric taken without basis; FAQ answers come from a supervised agent that a human can switch off; pricing stayed fair and predictable (dynamic pricing killed on trust signal).
**会员**：更衣室无摄像；无依据不采未成年生物数据；FAQ 来自受监督、可一键关的 Agent；定价保持公平可预期（动态定价因信任信号被砍）。

> **G13 coverage confirmed / 三视角覆盖确认**: Architect × Operator × Member all承接, no orphan touchpoint. / 三视角均已承接，无孤儿触点。
