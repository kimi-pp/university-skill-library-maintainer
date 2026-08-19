# Market Deep-Case · Vietnam / 市场深度案例·越南

> **Cluster / 集群**: F (South & SE Asia compliance) · Example / 例证 19 of 34
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: re-verify every 180 days; PDPD 13/2023 + localization draft is 🔄 — run `tools/05` before citing; platform facts via `tools/04`.
> **Cross-references / 交叉引用**: `references/11` (four-pack) · `references/13` (#k-62-vietnam) · `data/07` (regional differences) · `data/14` (SLA enforcement) · `playbooks/13-90day-onboarding.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

> **HONESTY PREAMBLE / 诚实声明**: This is an **archetypal composite case**, not a real company. Figures are **directional**, not audited. Regulations are time-sensitive — verify Decree 13/2023 status and the localization draft via `tools/05`. No article numbers or penalty figures are invented.
> **诚实声明**：本案为**原型复合案例**，非真实企业。数据仅为**方向性**参考。法规具时效性——13/2023 议定状态与本地化草案请经 `tools/05` 核验。不编造条款号或罚款数值。

---

## ① Context Card / 背景卡 {#vn-context}

**Operator / 运营方**: "Saigon Motion" — a 5-club chain across Ho Chi Minh City (District 1, Thu Duc, Binh Thanh, Tan Binh, District 7), ~6,800 members, FDMM L2→L3, fast-growing, Zalo-led.
**运营方**：「西贡动能」——胡志明市 5 店连锁，约 6,800 会员，FDMM L2→L3，高增长，Zalo 主导。

**Why Vietnam is special / 越南特殊之处**: Decree 13/2023 is consent-centric with strict cross-border rules and a localization draft in consultation 🔄; MoMo/ZaloPay/bank-QR dominate; Zalo OA is the member channel; the market is fast-growing so vendors are immature; motorbike-parking integration is a local quirk; staff digital literacy needs investment.
**特殊之处**：13/2023 议定以同意为核心、跨境严、本地化草案征询中 🔄；MoMo/ZaloPay/银行二维码主导；Zalo OA 为会员渠道；市场高增长故供应商不成熟；摩托停车集成是本地怪；员工数字素养需投入。

| Dimension / 维度 | Value / 数值 | Note / 备注 |
|---|---|---|
| Clubs / 门店 | 5 | HCMC spread / 胡志明铺开 |
| Members / 会员 | ≈6,800 | fast-growing / 高增长 |
| FDMM | L2→L3 | MMS + Zalo OA + BI / 会员系统+Zalo OA+看板 |
| Channels / 渠道 | Zalo OA primary, WhatsApp secondary | vi-VN / 越南语 |

---

## ② The Market's Distinctive Digital Reality / 市场独有的数字现实 {#vn-digital-reality}

**Payments / 支付** (anchor `data/07` §①): MoMo + ZaloPay + Viettel Money; bank-QR rising; cards minor. 🔄
**支付**：MoMo + ZaloPay + Viettel Money；银行二维码上升；卡次要。

**Messaging / 消息** (anchor `data/07` §②): Zalo is the primary channel in VN; Zalo OA carries booking, reminders, promo (Zalo opt-in). WhatsApp for expat tails.
**消息**：越南 Zalo 为主渠道；Zalo OA 承载约课、提醒、促销（Zalo Opt-in）。WhatsApp 接外侨尾流。

**Compliance four-pack / 合规四件套** (anchor `references/11` Vietnam):

- **① Privacy — PDPD 13/2023**: explicit consent (written/electronic); Vietnamese notice; cross-border transfer needs consent + documentation. 🔄 Penalty ≈ revenue-scaled + suspension (verify via `tools/05`).
  ① 隐私 — PDPD 13/2023：明示同意（书面/电子）；越南语告知；跨境传输须同意 + 文件。罚则≈按营收分级+暂停（经 tools/05 核验）。
- **② Biometric & CCTV**: consent + alternative for face; signage + retention; changing-room ban (HI-5).
  ② 生物识别与监控：人脸须同意 + 替代；标识 + 留存；更衣室禁（HI-5）。
- **③ Payments & prepaid**: clear contract; fair refund; segregate prepaid float (HI-3).
  ③ 支付与预付：清晰合同；公平退费；隔离预收款项（HI-3）。
- **④ Industry — localization & consumer**: keep core member data in-country pending draft law. 🔄 Opt-in marketing; AED/pool supervision (HI-7, HI-2).
  ④ 行业 — 本地化与消费者：核心会员数据驻留境内（候草案）。Opt-in 营销；泳池/AED 监管（HI-7, HI-2）。

:::dynamic-hook
topic: Vietnam PDPD Decree 13 + residency/localization draft law / 越南 PDPD 13号议定与本地化草案
stored-value: Decree 13/2023 in force; a comprehensive PDP Law + data-localization draft in consultation; keep core data in-country pending law (stored 2026-07)
staleness: HIGH — draft law + localization debate active / 高——法律草案与本地化讨论活跃
action: retrieve MPS / official portal before transfer & storage design
fallback: if retrieval fails, present stored value + "as of 2026-07, verify before use"
:::

---

## ③ The Real Assembly / 真实组装 {#vn-assembly}

**MMS choice logic — local vs global 🔄 / 会员系统选型（本地 vs 全球）**: A global MMS lacked Zalo OA connector and MoMo/ZaloPay rails, and pushed an offshore data model clashing with the localization draft. A regional APAC MMS with Zalo OA, MoMo/ZaloPay, and vi-VN fields was chosen; core PII kept in-country. 🔄
**选型逻辑**：全球 MMS 缺 Zalo OA 连接器与 MoMo/ZaloPay 通道，且离岸数据模型与本地化草案冲突；选含 Zalo OA、MoMo/ZaloPay、vi-VN 字段的区域 APAC MMS；核心 PII 留境内。

**Payment wiring / 支付接线**: MoMo + ZaloPay + bank-QR (one QR aggregator) → cards minor. Prepaid float segregated (HI-3). All settlements in VND with local e-invoice (hóa đơn điện tử).
**支付接线**：MoMo + ZaloPay + 银行二维码（一码聚合）→ 卡次要。预收款项隔离（HI-3）。全部 VND 结算 + 本地电子发票。

**Messaging setup / 消息设置**: Zalo OA as the spine — booking confirmation, class reminder, freeze/renew, Zalo opt-in promo in vi-VN. Explicit consent captured in-channel (HI-7); cross-border message-platform data minimized.
**消息设置**：Zalo OA 为轴——约课确认、课程提醒、冻结/续费、vi-VN Zalo Opt-in 促销。渠道内取明示同意（HI-7）；跨境消息平台数据最小化。

**Compliance + ops actions / 合规与运营动作**: Vietnamese-language privacy notice; DPO-style contact; non-biometric entry live; in-country PII store per `references/13` #k-62-vietnam; breach + cross-border doc runbook; motorbike-parking gate tied to membership status; staff digital-literacy program adapted from `playbooks/13`.
**合规与运营动作**：越南语隐私告知；DPO 式联络；非生物识别入场在线；按 references/13 #k-62 境内存 PII；泄露 + 跨境文件 runbook；摩托停车闸机绑定会籍状态；员工数字素养计划改编自 playbooks/13。

---

## ④ Two Market-Specific Incidents & Resolutions / 两起本地事件与处置 {#vn-incidents}

### Incident A — Immature vendor SLA miss / 事件 A — 不成熟供应商 SLA 失约 {#vn-incident-1}
**What happened / 事件**: the local access-control vendor missed a 4h response SLA twice during a gate-outage; "blame triangle" with the MMS vendor stalled fixes.
**经过**：本地门禁供应商在闸机故障中两度错过 4 小时响应 SLA；与 MMS 供应商的「甩锅三角」拖慢修复。

**Resolution / 处置**: per `data/14` SLA library, invoked service-credit clause, required joint root-cause, and pre-booked standby support windows (mirrors `playbooks/15` vendor standby).
**处置**：按 data/14 SLA 条款启用服务抵扣、要求联合根因、预排待命支持窗（呼应 playbooks/15 供应商待命）。

### Incident B — Motorbike-parking integration clash / 事件 B — 摩托停车集成冲突 {#vn-incident-2}
**What happened / 事件**: parking-gate firmware tied access to a legacy member flag; a Zalo-driven freeze didn't sync, so frozen members still parked free.
**经过**：停车闸固件将通行绑旧版会员标记；Zalo 驱动的冻结未同步，致冻结会员仍免费停车。

**Resolution / 处置**: unified the membership-status event bus so freeze/reactivate propagated to both gate and parking within seconds; added a reconciliation job.
**处置**：统一会籍状态事件总线，使冻结/恢复秒级同步闸机与停车；增对账任务。

---

## ⑤ Outcomes & Surprises / 成效与意外 {#vn-outcomes}

- Zalo OA lifted booking-confirmation open rate to ≈90% vs email's ≈30%.
  Zalo OA 使约课确认打开率达约 90%，邮件仅约 30%。
- Staff digital-literacy program (playbooks/13 adapted) cut onboarding errors and vendor-escalation time.
  员工数字素养计划（改编 playbooks/13）减少入驻错误与供应商升级耗时。
- **Surprise / 意外**: vendor immaturity — not regulation — was the top delivery risk; SLA enforcement mattered more than feature breadth.
  **意外**：供应商不成熟——而非法规——才是头号交付风险；SLA 执行比功能广度更重要。

---

## ⑥ 10-Item Transferable Market-Entry Checklist / 10 项可迁移入市清单 {#vn-checklist}

1. Choose an MMS with Zalo OA connector + MoMo/ZaloPay + vi-VN fields. / 选含 Zalo OA 连接器 + MoMo/ZaloPay + vi-VN 字段的 MMS。
2. Keep core member PII in-country pending the localization draft (references/13 #k-62). 🔄 / 候本地化草案，核心 PII 留境内（references/13 #k-62）。
3. Capture explicit consent in-channel; minimize cross-border message-platform data (HI-7). / 渠道内取明示同意；最小化跨境消息平台数据（HI-7）。
4. Document any cross-border transfer per Decree 13 before it happens. / 任何跨境传输前按 13 号议定备文件。
5. Enforce SLA service-credit + joint root-cause with vendors (data/14). / 对供应商执行 SLA 服务抵扣 + 联合根因（data/14）。
6. Tie motorbike-parking gate to the unified membership-status bus. / 摩托停车闸机绑定统一会籍状态总线。
7. Run a staff digital-literacy program adapted from playbooks/13. / 运行改编自 playbooks/13 的员工数字素养计划。
8. Segregate prepaid float; fair refund in contract (HI-3). / 隔离预收款项；合同写公平退费（HI-3）。
9. Keep a non-biometric entry alternative live (HI-1/face). / 非生物识别入场替代常在线（HI-1/人脸）。
10. Run `tools/05` to confirm the localization draft's status before go-live. 🔄 / 上线前跑 tools/05 确认本地化草案状态。

---

## ⑦ Related Files / 相关文件 {#vn-related}

- `references/11-apac-compliance-south-southeast-asia.md` (Vietnam four-pack + localization)
- `references/13-data-and-llm-engine.md` #k-62-vietnam (decree residency)
- `data/07-apac-regional-differences.md` §① payments, §② messaging, §⑭ Android-first
- `data/14-repair-scripts-and-sla-library.md` (SLA clause + blame triangle)
- `playbooks/13-90day-onboarding.md` (staff digital-literacy adaptation)
- `tools/05-regulation-traceability-verification.md`

---

## ⑧ G13 Tri-Perspective Note / G13 三视角注记 {#vn-g13}

**Architect / 架构师**: Zalo OA + MoMo/ZaloPay with vi-VN; in-country PII per the draft; unified membership-status bus for gate + parking; explicit-consent capture; offline-capable POS for typhoon season.
**架构师**：Zalo OA + MoMo/ZaloPay 配 vi-VN；按草案境内存 PII；闸机+停车统一会籍状态总线；取明示同意；台风季 POS 可离线。

**Operator / 运营者**: one SOP for vi-VN notice, refund, opt-in, residency, and vendor SLA enforcement; staff-literacy drill from playbooks/13.
**运营者**：一套 SOP 管 vi-VN 告知、退费、Opt-in、驻留、供应商 SLA 执行；按 playbooks/13 做员工素养演练。

**Member / 会员**: gets Vietnamese-language consent, a face-entry alternative, fair refund, and a Zalo journey that just works — including parking.
**会员**：获越南语同意、人脸替代、公平退费，以及顺畅（含停车）的 Zalo 旅程。
