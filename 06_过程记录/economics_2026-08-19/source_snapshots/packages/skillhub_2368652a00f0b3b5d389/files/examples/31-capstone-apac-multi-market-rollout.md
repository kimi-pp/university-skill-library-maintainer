# 31 · Capstone: APAC Multi-Market Rollout / 案例 31：亚太多市场扩张旗舰战例

> **Cluster / 集群**: F (compliance) · B (software) · M (messaging) · I (governance) · L (architecture)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: compliance four-pack per market via `tools/05` every 90 days; payment & messaging localization 🔄 via `tools/04`; micro-details via `data/20`.
> **Cross-references / 交叉引用**: `templates/44-multi-market-rollout-plan.md` · `references/10-apac-compliance-east-asia-oceania.md` · `references/11-apac-compliance-south-southeast-asia.md` · `references/17-omnichannel-messaging.md` · `data/07-apac-regional-differences.md` · `data/20-micro-details-ledger.md` · `tools/05-regulation-traceability-verification.md` · `playbooks/05-apac-multi-market-expansion.md` · `playbooks/08-emergency-runbooks.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## Honesty Preamble / 诚实前言

> This is an **archetypal composite case** built for teaching — an amalgam of patterns observed across APAC fitness chains. It is **not** a claimed real company; names, clubs and figures are directional illustrations, not audited financials.
> 本案例为**典型复合教学案例**——糅合亚太健身连锁常见模式而成，**并非**宣称某家真实企业；名称、门店与数字均为方向性示意，非审计财报。

> No market's compliance status is asserted as final. Every four-pack item below carries a retrieval date and must be re-verified via `tools/05` before any real deployment.
> 任何市场的合规状态均非定论。下列四件套条目均带检索日期，真实落地前须经 `tools/05` 重新核验。

---

## ① Context Card / 情境卡

| Field / 字段 | Value / 值 |
|---|---|
| Archetype / 原型 | 15-club group, HQ Singapore, home market L3 / 15 店集团，总部新加坡，本土 L3 |
| Markets entered / 进入市场 | Japan (M6–14) · Thailand (M14–22) · Australia (M22–30) / 日本 · 泰国 · 澳大利亚 |
| Market deferred / 暂缓市场 | Hong Kong (China) — compliance-risk weighted hold / 中国香港——合规风险加权暂缓 |
| Timeline / 周期 | 30 months / 30 个月 |
| FDMM entry → target / 起点→目标 | L3 (home) → L4 (multi-site group) / L3（本土）→ L4（多店集团） |
| Investment envelope / 投资带 | directional S$8–12M over 30 months / 方向性 30 个月 800–1200 万新元 |
| Honesty scope / 诚实范围 | composite; directional ranges only / 复合案例；仅方向性区间 |

---

## ② Multi-Phase Journey / 多阶段旅程（30 个月）

### Phase 1 — Market Sequencing & HQ Consolidation (M1–6) / 阶段一 市场排序与总部整合

**Situation / 形势**: The group ran 15 clubs across Singapore & Malaysia at L3 (CRM+POS+gates integrated, daily dashboard). Board wanted APAC scale but lacked a repeatable cross-border playbook.
**形势**：集团在新马共 15 店，已达 L3（会籍+收银+闸机打通、日看板）。董事会想做亚太规模，但缺可复制的跨境打法。

**Decision forks considered / 决策分叉（含被否选项与理由）**:
- *Fork A — enter 3 markets at once vs one at a time.* Rejected "3 at once": violates `playbooks/05` §Phase 1 common trap (`data/21#market-overreach`) — each gets 1/3 attention, all stall. Chose **one at a time**, ranked by `templates/44`.
  *分叉 A — 同时进 3 市场 vs 逐次进。否决「三箭齐发」：违反 playbooks/05 阶段一陷阱（market-overreach）——每市场仅 1/3 注意力，全搁浅。选**逐次进**，按 templates/44 排序。*
- *Fork B — include Hong Kong (China) in wave 1 vs defer.* Rejected immediate entry: the four-pack pre-scan showed a **higher weighted compliance-risk** (cross-border data basis + prepaid supervision uncertainty) vs the other three. Chose **defer to a later wave** with a RED hold, not a failure.
  *分叉 B — 中国香港首波 vs 暂缓。否决立即进：四件套预审显示其**合规风险加权更高**（跨境数据依据+预付监管不确定性）高于其余三者。选**暂缓至后续波次**，标红而非失败。*
- *Fork C — global single-stack vs global core + local adapters.* Chose **global MMS + local payment/messaging adapters** (see `playbooks/05` §Phase 4). Rejected "copy home stack verbatim": would breach data residency (`data/21#stack-copy-crossborder`).
  *分叉 C — 全球单栈 vs 全球核心+本地适配。选**全球 MMS + 本地支付/消息适配**。否决「照搬本土栈」：会破数据驻留（stack-copy-crossborder）。*

**Library artifacts used / 引用库工件**: `templates/44-multi-market-rollout-plan.md` (scoring + 90-day) · `playbooks/05` §Phase 1–2 · `tools/05` four-pack pre-scan · `references/10` / `references/11` for HK (China) hold rationale.
**Outcome / 结果**: Ranked list — JP(20) > TH(18) > AU(15) > HK(RED hold); HQ NOC blueprint sketched; investment envelope set.
**结果**：排序榜——日(20)>泰(18)>澳(15)>港(红缓)；总部 NOC 蓝图草拟；投资带锁定。

### Phase 1.5 — Compliance Four-Pack Clearance Snapshot / 阶段 1.5 合规四件套清关快照

**Goal / 目标**: Show the four-pack status per entered market before any member data was collected (per `playbooks/05` §Phase 2.5). All items verified via `tools/05` with retrieval dates; 🔄 re-verify before real use.
**目标**：示各进入市场四件套状态（采会员数据前，playbooks/05 阶段2.5）。各项经 tools/05 核验带检索日；🔄 真实使用前重核。

| Pack / 件 | Japan / 日本 | Thailand / 泰国 | Australia / 澳洲 |
|---|---|---|---|
| Privacy / 隐私 | APPI, rev. 🔄 · retrieved 2026-07 | PDPA (TH) · retrieved 2026-07 | Privacy Act, rev. 🔄 · retrieved 2026-07 |
| Biometric / 生物 | Face deferred; consent + local template / 人脸缓；同意+本地模板 | QR+fob only / 仅扫码+手环 | Opt-in face later / 后续Opt-in人脸 |
| Payment / 支付 | Prepaid escrow req. / 预付托管需 | PromptPay + escrow / PromptPay+托管 | Stored-value supervised / 储值监管 |
| Industry / 行业 | Cooling-off 7d / 冷静期7天 | Contract rule 🔄 / 合同规 | Cooling-off per state / 按州冷静期 |

Hong Kong (China) remained **RED** on the payment + cross-border-data packs — the documented reason for the deferral, not a compliance failure.
**中国香港**在支付+跨境数据包仍**红**——此即暂缓的书面理由，非合规失败。

### Phase 2 — Japan Entry: The Vendor-Culture Learning Curve (M6–14) / 阶段二 日本进场：供应商文化学习曲线

**Situation / 形势**: Japan scored top but vendors expected rigid, document-heavy integration specs; the group's "move fast" HQ habit clashed with local **shikakuken** (qualification/approval) culture.
**形势**：日本分最高，但本地供应商要严谨、重文档的对接规范；总部「快跑」习惯与本地**资格/审批文化**冲突。

**Decision forks considered / 决策分叉**:
- *Fork — hire a local SI (system integrator) vs push HQ engineers.* Rejected "HQ engineers alone": language + certification gaps would miss APPI biometric basis (`#jp-appi-biometric`). Chose **local SI as integration broker** + HQ architecture guardrail.
  *分叉 — 雇本地 SI vs 压总部工程师。否决「仅总部工程师」：语言+认证缺口会漏掉 APPI 生物识别依据（jp-appi-biometric）。选**本地 SI 作对接经纪**+总部架构护栏。*
- *Fork — face gate vs QR+fob.* Chose **QR + fob** for launch (lower biometric friction), deferring face to a later opt-in phase with local template storage (HI-1).
  *分叉 — 人脸闸 vs 扫码+手环。选**扫码+手环**首发（生物识别摩擦低），人脸留待后续 Opt-in 阶段且本地模板存储（HI-1）。*

**Library artifacts used / 引用库工件**: `references/10` §Japan (APPI) · `data/07` (name-order: family-first dedupe on phone) · `references/17` (LINE-dominant messaging) · `data/20#name-order` micro-detail.
**Outcome / 结果**: First Tokyo club live at M14; LINE booking notices in Japanese; member ID namespace unified at HQ; biometric deferred — RED cleared on privacy pack with consent model documented.
**结果**：东京首店 M14 开业；LINE 日文约课通知；会员 ID 命名空间总部归一；生物识别暂缓——隐私件带同意模型文档清红。

### Phase 3 — Thailand Entry: Monsoon Outage Tests BCP (M14–22) / 阶段三 泰国进场：季风断网考验 BCP

**Situation / 形势**: Bangkok club opened during monsoon season. A flood-linked ISP outage took the club offline for 9 hours; local payment rail (🔄 `tools/04`) and gate auth both depended on cloud.
**形势**：曼谷店季风季开业。洪水关联的 ISP 断网致门店离线 9 小时；本地支付通道与闸机鉴权均依赖云。

**Decision forks considered / 决策分叉**:
- *Fork — keep cloud-only auth vs add offline mode.* Rejected "cloud-only": `playbooks/05` §Phase 5 mandates offline-mode drill. Chose **local-cache auth + offline checkout** per `playbooks/08` R3 graceful degradation.
  *分叉 — 纯云鉴权 vs 加离线模式。否决「纯云」：playbooks/05 阶段五强制离线演练。选**本地缓存鉴权+离线结账**（playbooks/08 R3 优雅降级）。*
- *Fork — single ISP vs dual ISP.* Chose **dual ISP with auto-failover**; cost accepted as BCP premium.
  *分叉 — 单 ISP vs 双 ISP。选**双 ISP 自动切换**；成本作 BCP 溢价接受。*

**Library artifacts used / 引用库工件**: `playbooks/08` R3 (graceful degradation) · `references/08-network-and-infrastructure.md` · `data/20#home-schema-universal` (address/postal format fix) · `data/07` (Thai e-invoice 🔄).
**Outcome / 结果**: After fix, a simulated 6-hour outage ran with zero manual check-in bypass; recovery drill written into the playbook; BCP premium paid back in one avoided lost-day.
**结果**：修复后模拟 6 小时断网零人工签到兜底；恢复演练写入手册；BCP 溢价靠一次免损营业日回本。

### Phase 4 — Australia Entry: The DST Incident (M22–30) / 阶段四 澳大利亚进场：夏令时事故

**Situation / 形势**: Sydney club launched; HQ timestamps used SG timezone. The night "unmanned window" shifted by 1 hour at DST change, and cross-market attendance reports double-counted.
**形势**：悉尼店开业；总部时间戳用新加坡时区。DST 切换时夜间「无人窗口」偏移 1 小时，跨市场考勤报表重复计数。

**Decision forks considered / 决策分叉**:
- *Fork — store local time vs UTC+local display.* Rejected "local-only": cross-market BI needs a common axis. Chose **store UTC + market-local display** (`playbooks/05` §Phase 6 war story #1).
  *分叉 — 存本地时 vs UTC+本地展示。否决「仅本地」：跨市场 BI 需公共轴。选**存 UTC + 市场本地展示**（playbooks/05 阶段六故事#1）。*
- *Fork — patch report vs fix source.* Chose **fix at source (ingest)**, not report patch — avoids silent drift.
  *分叉 — 补报表 vs 修源头。选**修源头（入库）**，非补报表——避静默漂移。*

**Library artifacts used / 引用库工件**: `playbooks/05` §Phase 6 (timezone/DST) · `data/20#dst-timestamp` · `references/16-security-operations` (incident drill).
**Outcome / 结果**: UTC ingestion fixed; DST calendar loaded; AU privacy pack (Privacy Act 🔄 `tools/04`) cleared with local counsel; 3-market group BI live at M30.
**结果**：UTC 入库修复；DST 日历载入；澳隐私件（Privacy Act，tools/04）经本地法务清关；M30 三市场集团 BI 上线。

**Cross-cutting — HQ NOC Scale-Up / 横切 — 总部 NOC 扩容**: From a 2-person SG watch (L3) to a 7-person follow-the-sun NOC (SG + Tokyo + Bangkok) by M30, running group BI, incident drill cadence, and the repeatable 90-day checklist.
**横切 — 总部 NOC 扩容**：从 2 人新加坡值班（L3）扩至 7 人「跟随太阳」NOC（新+东京+曼谷），M30 跑集团 BI、事故演练节奏与可复制 90 天清单。

### Phase 5 — Group BI & Governance Cadence (M26–30) / 阶段五 集团 BI 与治理节奏

**Situation / 形势**: With three markets live, the board wanted one number for "group health" but each market reported in local currency, tax basis, and holiday calendar — the cross-market BI was uninformable without standardization.
**形势**：三市场在线后，董事会要一个「集团健康数」，但各市场以本地币、税基、假期历上报——不标准化则跨市场 BI 不可读。

**Decision forks considered / 决策分叉**:
- *Fork — report in HQ currency vs local+FX layer.* Rejected "HQ currency only": hides local tax reality. Chose **local capture + FX layer at group BI**, stored per `references/16` §R e-invoice rule.
  *分叉 — 仅总部币 vs 本地+FX 层。否决「仅总部币」：掩本地税实。选**本地采+集团 BI 加 FX 层**（references/16 §R 电子发票规则）。*
- *Fork — monthly vs weekly cadence.* Chose **weekly automated + monthly narrative** — speed for ops, story for board.
  *分叉 — 月 vs 周节奏。选**周自动+月叙述**——运营要快、董事会要故事。*

**Library artifacts used / 引用库工件**: `references/16-security-operations` §R (e-invoice) · `data/07` (regional tax display) · `playbooks/05` §Phase 6 (holiday calendar).
**Outcome / 结果**: One group dashboard with FX-normalized revenue, per-market churn, and a DST-safe attendance axis; board got its single number at M30.
**结果**：一张 FX 归一营收、分市场流失、DST 安全考勤轴的集团看板；M30 董事会得其一数。

### Market Micro-Detail Hit-List / 各市场微细节中招清单

| Market / 市场 | Micro-detail that bit / 中招微细节 | Fix / 修复 | Anchor / 锚点 |
|---|---|---|---|
| Japan / 日本 | Family-name-first dedupe merged wrong members / 姓前去重误并 | Dedupe on phone, given+family split / 按手机去重、姓分列 | `data/20#name-order` |
| Thailand / 泰国 | Address schema rejected local format at sign-up / 地址式拒本地格式 | Per-market address schema / 按市场地址结构 | `data/20#home-schema-universal` |
| Australia / 澳洲 | DST shifted unmanned window 1h / DST 偏无人窗1时 | UTC ingest + DST calendar / UTC入库+DST历 | `data/20#dst-timestamp` |
| All / 全域 | Promo fired on local public holiday / 促销撞本地假日 | Load market holiday calendar / 载市场假期历 | `playbooks/05` §Phase 6 |

**Lesson / 教训**: The five micro-details in `playbooks/05` §Phase 6 all fired across the rollout — the "micro-details pass" in the 90-day checklist is what kept them from becoming launch-day disasters.
**教训**：playbooks/05 阶段六五项微细节全在扩张中引爆——90 天清单的「微细节检查」使其免成开业日灾难。

### Vendor Scorecard (selection discipline) / 供应商打分卡（选型纪律）

| Layer / 层 | Options considered / 候选 | Chosen / 选定 | Why / 理由 |
|---|---|---|---|
| Global MMS / 全球MMS | 3 global + 1 local / 3全球+1本地 | Global core / 全球核心 | unified ID, group BI / 统一ID、集团BI |
| Local payment / 本地支付 | PayNow·LINE Pay·PromptPay·🔄 / 多 | Per-market rail / 按市场 | `references/17` dominance / 主导App |
| Local SI (JP) / 本地SI | 2 brokers / 2经纪 | Local SI broker / 本地经纪 | APPI cert basis / APPI认证依据 |
| NOC / 运维 | HQ-only vs follow-sun / 二选 | Follow-sun / 跟随太阳 | 3am local hands / 凌晨本地手 |

Iron Law 8 honored: ≥3 options per layer, data-export clause verified before signing, lock-in risk annotated per row.
**铁律8 守**：每层 ≥3 选项，签约前数据导出条已核，锁定风险逐行注。

### Rollout Cadence Summary / 扩张节奏摘要

| Window / 窗口 | Market / 市场 | Gate cleared / 过闸 | Slip / 延宕 |
|---|---|---|---|
| M1–6 | (prep) SG HQ / 总部整备 | four-pack pre-scan / 四件套预审 | — |
| M6–14 | Japan / 日本 | APPI + local SI / APPI+本地SI | +5 wk vendor / 供应商+5周 |
| M14–22 | Thailand / 泰国 | monsoon BCP drill / 季风BCP演练 | none / 无 |
| M22–30 | Australia / 澳洲 | DST ingest fix / DST入库修 | none / 无 |

One market at a time, each with a repeatable 90-day checklist — the discipline `playbooks/05` §Phase 1 demanded and this case proved.
**一次一市场，各带可复制 90 天清单**——playbooks/05 阶段一要求的纪律，本案证之。

---

## ③ Three Major Setbacks & Recovery / 三大挫折与复原

**Setback 1 — Japan vendor refused the HQ integration spec / 挫折一 日本供应商拒收总部对接规范**: Local vendor said the spec "lacked the required certification documents" and paused. Recovery: hired local SI broker, translated spec to JP qualification format, re-submitted — 5-week slip, no data loss. Lesson: local SI is not overhead, it is the gate.
**挫折一**：本地供应商称规范「缺必备认证文档」并暂停。复原：雇本地 SI 经纪，规范译为日式资格格式重提——延 5 周，无数据损。教训：本地 SI 非开销，是闸门。

**Setback 2 — Thailand 9-hour monsoon outage / 挫折二 泰国 9 小时季风断网**: Cloud-dependent auth left the club dark. Recovery: shipped offline-cache auth + dual ISP within 3 weeks; BCP drill now mandatory pre-launch. Lesson: graceful degradation (`playbooks/08` R3) is a launch gate, not a nice-to-have.
**挫折二**：云依赖鉴权使门店停摆。复原：3 周内上线离线缓存鉴权+双 ISP；BCP 演练现成强制前置。教训：优雅降级（R3）是开业闸门，非锦上花。

**Setback 3 — Australia DST double-count / 挫折三 澳洲 DST 重复计数**: Wrong timezone shifted unmanned window, double-counted attendance. Recovery: UTC ingestion + DST calendar; backfilled reports. Lesson: timezone is a data-model decision, not a display tweak.
**挫折三**：时区错置无人窗口、重复计考勤。复原：UTC 入库+DST 日历；回填报表。教训：时区是数据模型决策，非展示微调。

**Setback 4 (honesty) — HK (China) held, not killed / 挫折四（诚实）中国香港暂缓非砍掉**: The deferred market created internal pressure ("why are we scared?"). Recovery: framed as RED hold with a re-score trigger at M30; protected the group from premature compliance exposure. Lesson: a hold is a decision, communicate it as one.
**挫折四（诚实）**：暂缓市场惹内部质疑「为何怕」。复原：定为红缓+ M30 重评触发；护集团免 premature 合规暴露。教训：暂缓是决策，按决策沟通。

---

## ④ Financials View (Directional) / 财务视角（方向性）

**Investment envelope / 投资带**: S$8–12M over 30 months — split roughly: HQ NOC + group BI 30%, local SI/adapters 25%, compliance & local counsel 20%, BCP/dual-ISP 15%, contingency 10%.
**投资带**：30 个月 800–1200 万新元——大致：总部 NOC+集团 BI 30%、本地 SI/适配 25%、合规与本地法务 20%、BCP/双 ISP 15%、预备 10%。

**Payback narrative / 回收叙事**: Payback framed on three levers — (a) centralized procurement saving ~8–12% on renewals, (b) churn reduction from unified ID + localized messaging ~2–4pp, (c) one avoided lost-day per market per year via BCP. Directional payback 26–38 months.
**回收叙事**：回收挂三杠杆——(a) 集中采购省续约约 8–12%；(b) 统一 ID+本地化消息降流失约 2–4pp；(c) BCP 每市场每年免一次损日。方向性回收 26–38 个月。

**Three-scenario retrospective per `tools/06` / 三情景复盘（按 tools/06）**:

| Scenario / 情景 | Assumed / 假设 | Landed? / 落点 |
|---|---|---|
| Base / 基准 | steady 1-market/yr cadence / 每年稳进 1 市场 | Landed near base on cost; Japan slip added ~S$0.3M / 成本近基准；日本延宕增约 30 万 |
| Expected / 预期 | churn -3pp, procurement -10% / 流失-3pp、采购-10% | **Beat** on procurement (-11%), **missed** on churn (-1.8pp, slower localization) / 采购超标(-11%)，流失未达(-1.8pp，本地化偏慢) |
| Pessimistic / 悲观 | one market RED-stop / 一市场红停 | Did not trigger; HK hold was planned, not a surprise / 未触发；中国香港缓为计划内非意外 |

**Did expected case land? / 预期情景是否落地？**: Partially. Procurement over-delivered; churn lagged because messaging localization took longer than modeled. Net: directional NPV positive but below expected midpoint.
**预期是否落地？**：部分。采购超额；流失滞后因消息本地化慢于模型。净：方向性 NPV 正但低于预期中值。

**Savings-lever detail (directional) / 节支杠杆明细（方向性）**:

| Lever / 杠杆 | Base / 基准 | Expected / 预期 | Landed / 落点 |
|---|---|---|---|
| Centralized procurement / 集中采购 | — | -10% | -11% (beat) |
| Churn (unified ID + local msg) / 流失 | — | -3pp | -1.8pp (miss) |
| BCP avoided lost-day / BCP免损日 | 0 | 1/day·market·yr | 1 realized in TH / 泰实现1 |
| FX-layer reporting overhead / FX层报表耗 | — | +2% ops | +1.5% (under) |

**What we would redo / 重做之处**: (1) Start messaging localization 2 months earlier to hit churn target; (2) load the DST + holiday calendars at HQ ingest from day one, not per market; (3) treat the local SI as a permanent gate role, not a one-off bridge.
**重做之处**：(1) 消息本地化早 2 月起步以达流失目标；(2) DST+假期历于总部入库首日即载，非逐市场；(3) 本地 SI 作永久闸门岗非一次性桥。

---

## ⑤ Org & People Evolution / 组织与人才演进

- **M1**: 2-person SG watch, all decisions centralized. / 2 人新加坡值班，决策全集中。
- **M14**: Tokyo local SI + 1 embedded NOC analyst (Japan timezone). / 东京本地 SI + 1 名嵌入 NOC 分析师（日本时区）。
- **M22**: Bangkok NOC analyst added; 90-day checklist owned by local leads. / 增曼谷 NOC 分析师；90 天清单归本地负责人。
- **M30**: 7-person follow-the-sun NOC; a "market-entry lead" role created; quarterly cross-market drill. / 7 人跟随太阳 NOC；设「市场进入负责人」岗；季度跨市场演练。

The biggest people shift: from **heroics** (HQ firefighting) to **playbooks** (local leads run the 90-day checklist). `playbooks/13` mindset migrated from single-club to multi-market.
**最大人才转变**：从**救火英雄**（总部扑火）到**手册运营**（本地负责人跑 90 天清单）。playbooks/13 心态从单店迁至多市场。

**Capability matrix (HQ vs local, by M30) / 能力矩阵（总部 vs 本地，M30）**:

| Capability / 能力 | HQ-run / 总部统管 | Local-bought / 本地采购 | Note / 注 |
|---|---|---|---|
| Member ID namespace / 会员ID命名空间 | ✔ | — | unified at HQ / 总部归一 |
| Group BI / 集团BI | ✔ | — | FX-normalized / FX归一 |
| Local payment rail / 本地支付 | — | ✔ | per `references/17` / 按参考 |
| Local counsel / 本地法务 | — | ✔ | four-pack gate / 四件套闸 |
| NOC (follow-sun) / NOC跟随太阳 | ✔ (coords) | ✔ (analyst) | hybrid / 混合 |
| Data residency / 数据驻留 | decides / 决策 | stores / 存 | HI-9 basis / HI-9依据 |

This matrix is the literal output of `playbooks/05` §Phase 4 — what runs from HQ vs what is bought locally, with data residency decided per market.
**此矩阵即 playbooks/05 阶段四的实出**——总部统管 vs 本地采购，数据驻留按市场定。

---

## ⑥ Ten Transferable Lessons / 十条可迁移经验

1. **Sequence by readiness, not hype** — `templates/44` ranking beat the board's "enter 3 now" urge. / 按就绪排序非风口——templates/44 排名胜过董事会「现在进三」冲动。
2. **A RED hold is a decision, not a failure** — HK (China) deferred with a re-score trigger. / 红缓是决策非失败——中国香港带重评触发暂缓。
3. **Local SI is the compliance gate, not overhead** — Japan proved it. / 本地 SI 是合规闸门非开销——日本为证。
4. **Global core + local adapters** beats copy-verbatim stack on data residency. / 全球核心+本地适配 胜过照搬栈（数据驻留）。
5. **Graceful degradation is a launch gate** — Thailand monsoon enforced `playbooks/08` R3. / 优雅降级是开业闸——泰国季风逼出 R3。
6. **Timezone is a data-model choice** — Australia DST fixed at ingest, not display. / 时区是数据模型选择——澳洲 DST 修于入库非展示。
7. **Micro-details sink launches** — name-order, address schema, holiday calendar (`data/20`). / 微细节沉开业——姓名序、地址式、假期历（data/20）。
8. **BCP premium pays in one avoided lost-day** — dual ISP justified fast. / BCP 溢价一次免损日即回本——双 ISP 速证。
9. **Centralized procurement > local re-negotiation** — ~11% saved at renewals. / 集中采购胜本地重谈——续约省约 11%。
10. **Playbooks scale people** — the 90-day checklist turned crossing borders into routine. / 手册放大人力——90 天清单把跨境变例行。

---

## ⑦ Related Files / 相关文件

- `playbooks/05-apac-multi-market-expansion.md` — the parent playbook. / 母手册。
- `templates/44-multi-market-rollout-plan.md` — scoring + 90-day. / 打分+90 天。
- `references/10` · `references/11` — 12-market compliance. / 12 市场合规。
- `references/17-omnichannel-messaging.md` — per-market messaging. / 各市场消息。
- `data/07-apac-regional-differences.md` · `data/20-micro-details-ledger.md` — regional & war-story detail. / 区域与实战细节。
- `tools/05-regulation-traceability-verification.md` — verify articles. / 核验条款。
- `playbooks/08-emergency-runbooks.md` — R3 graceful degradation. / R3 优雅降级。

---

## ⑧ G13 Note / G13 注记

**Architect / 架构师**: Four-pack gate per market (HI-1/3/5/9 aware) + data-residency decision built before launch; global MMS core with local adapters; UTC ingestion to kill DST drift. Cross-border data only with basis.
**架构师**：每市场四件套闸门（含 HI-1/3/5/9）+ 上线前数据驻留决策；全球 MMS 核心+本地适配；UTC 入库灭 DST 漂移。跨境数据须有依据。

**Operator / 运营者**: The 90-day checklist + local SI + dual ISP meant 3am breaks had local hands and a BCP drill already run. Follow-the-sun NOC removed the "HQ hero" bottleneck.
**运营者**：90 天清单+本地 SI+双 ISP 让凌晨出事有本地手、BCP 已演练。跟随太阳 NOC 去掉「总部英雄」瓶颈。

**Member / 会员**: Pays in LINE/PromptPay/local app, in local language, with opt-in consent; data sits where the law allows, never silently moved across a border; unmanned window actually matches local time.
**会员**：用 LINE/PromptPay/本地 App、本地语言、Opt-in 同意支付；数据落法律允许处，绝不悄跨境；无人窗口真实匹配本地时。

> **G13 coverage confirmed / 三视角覆盖确认**: Architect × Operator × Member all承接, no orphan touchpoint. / 三视角均已承接，无孤儿触点。
