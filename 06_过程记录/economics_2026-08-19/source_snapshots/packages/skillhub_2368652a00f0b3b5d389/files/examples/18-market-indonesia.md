# Market Deep-Case · Indonesia / 市场深度案例·印度尼西亚

> **Cluster / 集群**: F (South & SE Asia compliance) · Example / 例证 18 of 34
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: re-verify every 180 days; PDP implementing regulations (PP71 residency) are 🔄 — run `tools/05` before citing; platform facts via `tools/04`.
> **Cross-references / 交叉引用**: `references/11` (four-pack) · `references/13` (#k-63-indonesia, PP71) · `data/07` (regional differences) · `data/14` (SLA) · `references/12`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

> **HONESTY PREAMBLE / 诚实声明**: This is an **archetypal composite case**, not a real company. Figures are **directional**, not audited. Regulations are time-sensitive — verify PDP Law 27/2022 implementing rules and PP71 scope via `tools/05`. No article numbers or penalty figures are invented.
> **诚实声明**：本案为**原型复合案例**，非真实企业。数据仅为**方向性**参考。法规具时效性——PDP 27/2022 细则与 PP71 范围请经 `tools/05` 核验。不编造条款号或罚款数值。

---

## ① Context Card / 背景卡 {#id-context}

**Operator / 运营方**: "Senayan Boutique Collective" — a 4-club boutique chain in Jakarta (Senayan, Kemang, SCBD, Kelapa Gading), ~5,400 members, FDMM L2→L3, heavy WhatsApp engagement, Android-first member app.
**运营方**：「史纳延精品集合」——雅加达 4 店精品连锁，约 5,400 会员，FDMM L2→L3，WhatsApp 重度、会员 App 安卓优先。

**Why Indonesia is special / 印尼特殊之处**: PDP Law 27/2022 is the first comprehensive law with phasing PP; QRIS unifies wallets; WhatsApp scales as the member channel; prayer times and Jakarta traffic shape demand; Android-first device reality; PP71 raises an in-country data question.
**特殊之处**：PDP 27/2022 为首部综合法、PP 分阶段；QRIS 统一钱包；WhatsApp 规模化为主渠道；祷告时间与雅加达拥堵塑需求；安卓优先设备现实；PP71 提出境内数据问题。

| Dimension / 维度 | Value / 数值 | Note / 备注 |
|---|---|---|
| Clubs / 门店 | 4 | Jakarta clusters / 雅加达片区 |
| Members / 会员 | ≈5,400 | boutique, community-led / 精品、社群驱动 |
| FDMM | L2→L3 | MMS + WhatsApp + BI / 会员系统+WhatsApp+看板 |
| Channels / 渠道 | WhatsApp Business at scale | Android-first app / 安卓优先 |

---

## ② The Market's Distinctive Digital Reality / 市场独有的数字现实 {#id-digital-reality}

**Payments / 支付** (anchor `data/07` §①): QRIS is the national interoperable QR; GoPay, OVO, DANA ride on top; cards at desk. 🔄
**支付**：QRIS 为国家互操作二维码；GoPay、OVO、DANA 叠加；前台刷卡。

**Messaging / 消息** (anchor `data/07` §②): WhatsApp is the workhorse; Indonesian-language templates primary, EN for expats.
**消息**：WhatsApp 为主力；印尼语模板为主，英文接外侨。

**Compliance four-pack / 合规四件套** (anchor `references/11` Indonesia):

- **① Privacy — PDP Law 27/2022**: consent + purpose limitation; breach notification per law's mechanism; Kominfo enforcement; PP phasing in. 🔄 Penalty ≈ statutory ceiling + criminal (verify via `tools/05`).
  ① 隐私 — PDP 27/2022：同意 + 目的限制；依机制通报泄露；Kominfo 执法；PP 分阶段。罚则≈法定上限+刑（经 tools/05 核验）。
- **② Biometric & CCTV**: consent + alternative for face; signage + retention; changing-room ban (HI-5).
  ② 生物识别与监控：人脸须同意 + 替代；标识 + 留存；更衣室禁（HI-5）。
- **③ Payments & prepaid**: clear contract; fair cancellation/refund; segregate prepaid float (HI-3).
  ③ 支付与预付：清晰合同；公平退会/退费；隔离预收款项（HI-3）。
- **④ Industry — localization (PP71)**: government/strategic + some private data may need in-country processing; private gym data lower risk but confirm scope. 🔄 Keep member DB in-country unless a transfer basis exists.
  ④ 行业 — 本地化（PP71）：政府/战略及部分私人数据或需境内处理；私营健身房风险较低但须确认范围。会员库驻留境内，除非有传输依据。

:::dynamic-hook
topic: Indonesia PDP Law implementing regulations (PP) + PP71 residency scope / 印尼 PDP 法细则与 PP71 驻留范围
stored-value: PP detailing breach notice, DPO, cross-border & localization rolling out post-2022; private gym data typically lower residency risk but scope must be confirmed (stored 2026-07)
staleness: HIGH — implementing rules still emerging / 高——细则仍在出台
action: retrieve Kominfo / official gazette before finalizing cloud & transfer design
fallback: if retrieval fails, present stored value + "as of 2026-07, verify before use"
:::

---

**Consumer habits that shape the build / 塑造系统的消费习惯** (anchor `data/07` §①, §④, §⑭): Indonesian members are WhatsApp-native and Android-first; they expect one QR (QRIS) to pay anything; prayer times and Jakarta traffic dictate when they train; boutique communities value personal touch over automation.
**消费习惯**：会员 WhatsApp 原生、安卓优先；期待一码（QRIS）通付；祷告时间与雅加达拥堵决定训练时段；精品社群重人情甚于自动化。

| Habit / 习惯 | Implication / 含义 |
|---|---|
| Android-first / 安卓优先 | lightweight PWA / 轻量 PWA |
| QRIS expectation / 期待 QRIS | one-QR payments / 一码付 |
| Prayer-time rhythm / 祷告节奏 | schedule inputs / 排课输入 |
| Traffic windows / 拥堵时段 | off-peak pricing / 非高峰定价 |

## ③ The Real Assembly / 真实组装 {#id-assembly}

**MMS choice logic — local vs global 🔄 / 会员系统选型（本地 vs 全球）**: A global MMS lacked QRIS unification and Indonesian tax-invoice (faktur pajak) output. A regional APAC MMS with QRIS, GoPay/OVO, and id-ID locale was chosen; cloud region set in-country per PP71 caution. 🔄
**选型逻辑**：全球 MMS 缺 QRIS 统一与印尼税务发票输出；选含 QRIS、GoPay/OVO、id-ID 区域设定的区域 APAC MMS；云区域按 PP71 谨慎设境内。

**Payment wiring / 支付接线**: QRIS (one QR for all wallets) → GoPay/OVO/DANA → cards. Prepaid float segregated (HI-3). All settlements reconcile to local tax-invoice type.
**支付接线**：QRIS（一码通所有钱包）→ GoPay/OVO/DANA → 卡。预收款项隔离（HI-3）。所有结算对接本地税务发票类型。

**Cloud & residency decision / 云与驻留决策**: per `references/13` #k-63-indonesia, member PII DB placed in an in-country cloud region; cross-border transfers (if any analytics export) use a documented transfer basis. Confirmed private-gym scope is lower-risk but kept in-country by default.
**云与驻留决策**：按 references/13 #k-63，会员 PII 库置境内云区域；跨境传输（如有分析导出）用书面传输依据。确认私营健身房范围风险较低，但默认留境内。

**Messaging setup / 消息设置**: WhatsApp Business API at scale — booking, reminder, prayer-time-aware class nudges, opt-in promo in id-ID. Consent captured in-channel (HI-7).
**消息设置**：WhatsApp Business API 规模化——约课、提醒、祷告时间感知课程轻推、id-ID Opt-in 促销。渠道内取同意（HI-7）。

**Compliance actions / 合规动作**: Indonesian-language privacy notice; DPO-style contact; non-biometric entry live; breach-notification runbook; prayer-time scheduling inputs; Android-first lightweight app.

**Local vs global MMS scorecard / 本地 vs 全球 MMS 评分卡**:

| Criterion / 维度 | Global MMS / 全球 | Regional APAC MMS / 区域 | Chosen / 选用 |
|---|---|---|---|
| QRIS unification / 统一 | weak / 弱 | native / 原生 | regional / 区域 |
| id-ID + faktur pajak / 税务 | no / 无 | full / 完整 | regional / 区域 |
| In-country cloud / 境内云 | offshore / 离岸 | selectable / 可选 | regional / 区域 |
| Android-first app / 安卓优先 | iOS-heavy / 重iOS | PWA / 轻量 | regional / 区域 |

**Payment-mix & messaging wiring / 支付占比与消息接线**:

| Layer / 层 | Stack / 栈 | Note / 备注 |
|---|---|---|
| Pay / 支付 | QRIS → GoPay/OVO/DANA → card | one QR / 一码 |
| Message / 消息 | WhatsApp Business | id-ID / 印尼语 |
| Compliance / 合规 | PDP 27/2022 + PP71 | in-country PII / 境内 |

**Preparedness note / 备战注**: PP71 caution pushed the raw PII store in-country by default; cross-border analytics was redesigned to use anonymized aggregates, which also simplified the consent story.
**备战注**：PP71 谨慎使原始 PII 默认留境内；跨境分析改匿名聚合，也简化了同意叙事。
**合规动作**：印尼语隐私告知；DPO 式联络；非生物识别入场在线；泄露通报 runbook；祷告时间排课输入；安卓优先轻量 App。

---

## ④ Two Market-Specific Incidents & Resolutions / 两起本地事件与处置 {#id-incidents}

### Incident A — Traffic-driven off-peak pilot / 事件 A — 拥堵驱动非高峰试点 {#id-incident-1}
**What happened / 事件**: Jakarta's rush-hour gridlock emptied 5–7pm classes but left 10am–12pm underused; a dynamic-pricing pilot aimed to fill off-peak.
**经过**：雅加达晚高峰拥堵致 5–7 点课空、10–12 点闲置；动态定价试点欲填非高峰。

**Resolution / 处置**: launched off-peak credit bonuses + lower drop-in price for 10am–12pm via WhatsApp nudges; monitored fairness (no discrimination) and POS rules in sandbox first.
**处置**：经 WhatsApp 轻推对 10–12 点发非高峰积分加成 + 更低临门价；先沙箱监公平性（无歧视）与 POS 规则。

### Incident B — Cross-border export slip / 事件 B — 跨境导出疏漏 {#id-incident-2}
**What happened / 事件**: a global BI tool auto-exported member PII to an offshore region for "headquarters analytics" without a transfer basis — PP71/Decree concern.
**经过**：全球 BI 工具将会员 PII 自动导出境外供「总部分析」，无传输依据——触 PP71/法令关切。

**Resolution / 处置**: halted auto-export; anonymized/aggregated before any cross-border flow; documented transfer basis per `references/13` #k-63; kept raw PII in-country.
**处置**：停自动导出；任何跨境前先匿名/聚合；按 references/13 #k-63 备书面传输依据；原始 PII 留境内。

---

## ⑤ Outcomes & Surprises / 成效与意外 {#id-outcomes}

- QRIS unification removed 3 separate wallet integrations and cut payment-support tickets ≈40%.
  QRIS 统一免去 3 套独立钱包对接，支付工单降约 40%。
- Prayer-time-aware nudges lifted mid-day class fill without alienating members.
  祷告时间感知轻推提升日间课填充，且不冒犯会员。
- **Surprise / 意外**: Android-first lightweight PWA outperformed the planned native iOS-heavy app on engagement and cost — device reality beat aspiration.
  **意外**：安卓优先轻量 PWA 在参与度与成本上胜过原计划原生 iOS 重 App——设备现实胜过理想。

---

## ⑥ 10-Item Transferable Market-Entry Checklist / 10 项可迁移入市清单 {#id-checklist}

1. Choose an MMS with QRIS unification + GoPay/OVO + id-ID locale + faktur pajak. / 选含 QRIS 统一 + GoPay/OVO + id-ID + 税务发票的 MMS。
2. Decide cloud region in-country per PP71 caution; document any cross-border transfer basis. 🔄 / 按 PP71 谨慎定云区域境内；任何跨境备书面依据。
3. Keep raw member PII in-country; aggregate/anonymize before export. / 原始会员 PII 留境内；导出前先聚合/匿名。
4. Make WhatsApp the scaled member channel with id-ID templates. / 以 WhatsApp 为规模化会员渠道，配 id-ID 模板。
5. Feed prayer times into class scheduling + nudge logic. / 将祷告时间喂入排课 + 轻推逻辑。
6. Pilot traffic-driven off-peak dynamic pricing only after sandbox fairness check. / 拥堵驱动非高峰动态定价仅于沙箱公平性校验后试点。
7. Segregate prepaid float; fair cancellation/refund in contract (HI-3). / 隔离预收款项；合同写公平退会/退费（HI-3）。
8. Ship an Android-first lightweight app/PWA; don't over-invest iOS-first. / 发安卓优先轻量 App/PWA；勿过度投 iOS 优先。
9. Keep a non-biometric entry alternative live (HI-1/face). / 非生物识别入场替代常在线（HI-1/人脸）。
10. Run `tools/05` to confirm PP71 scope for private gyms before go-live. 🔄 / 上线前跑 tools/05 确认私营健身房 PP71 范围。

---

## ⑦ Related Files / 相关文件 {#id-related}

- `references/11-apac-compliance-south-southeast-asia.md` (Indonesia four-pack + PP71)
- `references/13-data-and-llm-engine.md` #k-63-indonesia (PP71 residency)
- `data/07-apac-regional-differences.md` §① payments, §② messaging, §⑭ Android-first
- `references/12-biometrics-and-cctv.md` (face-entry consent)
- `data/14-repair-scripts-and-sla-library.md` (SLA + market localization)
- `tools/05-regulation-traceability-verification.md`

---

## ⑧ G13 Tri-Perspective Note / G13 三视角注记 {#id-g13}

**Architect / 架构师**: QRIS-first payments; in-country cloud for PII per PP71; WhatsApp-at-scale with id-ID; prayer-time + traffic scheduling inputs; Android-first app.
**架构师**：QRIS 优先支付；按 PP71 境内云存 PII；WhatsApp 规模化配 id-ID；祷告时间 + 拥堵排课输入；安卓优先 App。

**Operator / 运营者**: one SOP for id-ID notice, refund, opt-in, residency handling, and off-peak pricing fairness; confirm PP71 scope with legal.
**运营者**：一套 SOP 管 id-ID 告知、退费、Opt-in、驻留处理、非高峰定价公平；与法务确认 PP71 范围。

**Member / 会员**: gets Indonesian-language consent, a face-entry alternative, fair refund, and a schedule that respects prayer times and Jakarta's traffic.
**会员**：获印尼语同意、人脸替代、公平退费，以及尊重祷告时间与雅加达拥堵的排课。
