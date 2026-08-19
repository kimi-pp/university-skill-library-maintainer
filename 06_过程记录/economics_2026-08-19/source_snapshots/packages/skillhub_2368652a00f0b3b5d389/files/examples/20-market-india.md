# Market Deep-Case · India / 市场深度案例·印度

> **Cluster / 集群**: F (South & SE Asia compliance) · Example / 例证 20 of 34
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: re-verify every 180 days; DPDP Rules rollout is 🔄 — run `tools/05` before citing; platform facts via `tools/04`.
> **Cross-references / 交叉引用**: `references/11` (four-pack) · `data/07` (regional differences) · `references/19` (#w9-online-sales-bnpl) · `playbooks/15-peak-season-and-promo-protection.md` · `data/14` (SLA) · `references/13` (#k-64-india)
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

> **HONESTY PREAMBLE / 诚实声明**: This is an **archetypal composite case**, not a real company. Figures are **directional**, not audited. Regulations are time-sensitive — verify DPDP Act 2023 Rules status and every threshold via `tools/05`. No article numbers or penalty figures are invented.
> **诚实声明**：本案为**原型复合案例**，非真实企业。数据仅为**方向性**参考。法规具时效性——DPDP 2023 细则状态与每项阈值请经 `tools/05` 核验。不编造条款号或罚款数值。

---

## ① Context Card / 背景卡 {#in-context}

**Operator / 运营方**: "Urban Peak" — a 7-club premium chain across Mumbai (BKC, Lower Parel, Andheri) and Bangalore (Indiranagar, Koramangala, Whitefield, Electronic City), ~14,500 members, FDMM L3, WhatsApp-first, UPI-everything.
**运营方**：「都市之巅」——孟买（BKC、Lower Parel、Andheri）与班加罗尔（Indiranagar、Koramangala、Whitefield、Electronic City）7 店高端连锁，约 14,500 会员，FDMM L3，WhatsApp 优先、UPI 万能。

**Why India is special / 印度特殊之处**: DPDP Act 2023 with Rules rolling out through 2024–2025 🔄; UPI dominates small payments; it is the world's largest WhatsApp market; TRAI DND/DNC governs promo SMS/calls; Aadhaar-adjacent KYC needs caution; festival season (Diwali/New Year) spikes promo load; price-sensitive tiering + BNPL risk.
**特殊之处**：DPDP 2023 法 + 细则 2024–2025 陆续落地 🔄；UPI 主导小额；全球最大 WhatsApp 市场；TRAI DND/DNC 管促销短信/电话；Aadhaar 邻接 KYC 须谨慎；节庆（排灯/新年）促销负载峰；价格敏感分层 + BNPL 风险。

| Dimension / 维度 | Value / 数值 | Note / 备注 |
|---|---|---|
| Clubs / 门店 | 7 | Mumbai + Bangalore / 双城 |
| Members / 会员 | ≈14,500 | premium, price-sensitive tiers / 高端但价格敏感分层 |
| FDMM | L3 | MMS + WhatsApp + BI / 会员系统+WhatsApp+看板 |
| Channels / 渠道 | WhatsApp-first + DND-aware SMS | UPI payments / UPI 支付 |

---

## ② The Market's Distinctive Digital Reality / 市场独有的数字现实 {#in-digital-reality}

**Payments / 支付** (anchor `data/07` §①): UPI (PhonePe/Google Pay) dominates small/recurring; cards at desk; BNPL emerging. 🔄
**支付**：UPI（PhonePe/GPay）主导小额/循环；前台刷卡；BNPL 兴起。

**Messaging / 消息** (anchor `data/07` §②): WhatsApp is primary (largest market); SMS only DND-aware for transactional/promo.
**消息**：WhatsApp 为主（最大市场）；短信仅 DND 感知用于交易/促销。

**Compliance four-pack / 合规四件套** (anchor `references/11` India):

- **① Privacy — DPDP Act 2023 + Rules**: verifiable consent (multilingual notice); report breaches to the Data Protection Board per Rules. 🔄 Penalty ≈ INR 250 crore cap for certain breaches (verify via `tools/05`).
  ① 隐私 — DPDP 2023 + 细则：可验证同意（多语种告知）；依细则向数据保护委员会报泄露。罚则≈特定违规上限 2.5 亿卢比（经 tools/05 核验）。
- **② Biometric & CCTV**: consent + alternative for face; signage + retention; changing-room ban (HI-5).
  ② 生物识别与监控：人脸须同意 + 替代；标识 + 留存；更衣室禁（HI-5）。
- **③ Payments & prepaid**: clear contract; fair cancellation/refund; segregate prepaid float (HI-3).
  ③ 支付与预付：清晰合同；公平退会/退费；隔离预收款项（HI-3）。
- **④ Industry — DNC / TRAI**: honor DND registry; opt-in + registration before promotional SMS/calls (HI-7); AED/pool supervision (HI-2).
  ④ 行业 — DND/TRAI：守 DND 名录；促销短信/电话前 Opt-in + 登记（HI-7）；泳池/AED 监管（HI-2）。

:::dynamic-hook
topic: India DPDP Rules 2024/2025 notification status / 印度 DPDP 细则通知状态
stored-value: Rules finalized & notified across 2024–2025 with phased compliance; penalty amounts & consent-manager regime active (stored 2026-07)
staleness: HIGH — rules bedding in, penalties live / 高——细则落地，罚则生效
action: retrieve MeitY + Data Protection Board notifications before design
fallback: if retrieval fails, present stored value + "as of 2026-07, verify before use"
:::

---

## ③ The Real Assembly / 真实组装 {#in-assembly}

**MMS choice logic — local vs global 🔄 / 会员系统选型（本地 vs 全球）**: A global MMS lacked UPI deep-links, India GST e-invoice, and DND-list screening. A regional APAC MMS with UPI, WhatsApp, and en-IN + local-language fields was chosen; DND screening built into every promo audience. 🔄
**选型逻辑**：全球 MMS 缺 UPI 深链、印度 GST 电子发票、DND 筛检；选含 UPI、WhatsApp、en-IN + 本地语字段的区域 APAC MMS；每波促销受众内建 DND 筛检。

**Payment wiring / 支付接线**: UPI (default, recurring via mandate/autopay) → cards → BNPL (guarded). Prepaid float segregated (HI-3). All settlements GST e-invoice (hóa đơn điện tử equivalent: e-invoice).
**支付接线**：UPI（默认，循环经授权/自动付）→ 卡 → BNPL（设防）。预收款项隔离（HI-3）。全部 GST 电子发票结算。

**Messaging setup / 消息设置**: WhatsApp Business API as the spine — booking, reminder, freeze/renew, opt-in promo. DND registry screened before any SMS/call (HI-7); consent captured in-channel; multilingual notice (en-IN + local).
**消息设置**：WhatsApp Business API 为轴——约课、提醒、冻结/续费、Opt-in 促销。任何短信/电话前筛 DND 名录（HI-7）；渠道内取同意；多语种告知（en-IN + 本地）。

**Compliance + KYC caution / 合规与 KYC 谨慎**: DPDP verifiable consent + DPO-style contact + breach runbook; Aadhaar-adjacent KYC — **do NOT store full Aadhaar numbers**; use masked reference / VID token only, with purpose limitation and short retention.
**合规与 KYC 谨慎**：DPDP 可验证同意 + DPO 式联络 + 泄露 runbook；Aadhaar 邻接 KYC——**勿存完整 Aadhaar 号**；仅用脱敏引用/VID 令牌，目的限制 + 短留存。

---

## ④ Two Market-Specific Incidents & Resolutions / 两起本地事件与处置 {#in-incidents}

### Incident A — DND violation near-miss / 事件 A — DND 违规险情 {#in-incident-1}
**What happened / 事件**: a Diwali promo SMS blast was queued before the DND filter ran; ≈3,200 DND-registered numbers were one click from exposure (TRAI penalty risk).
**经过**：排灯节促销短信群发在 DND 过滤前排队；约 3,200 个 DND 登记号一键即触（TRAI 罚险）。

**Resolution / 处置**: halted send; made DND screening a hard pre-send gate (audience ANDed with DND-opt-out + in-channel opt-in); added a dry-run audit. Per `playbooks/15` promo-rules testing in sandbox.
**处置**：停发；将 DND 筛检设为发送硬闸（受众与 DND 退订 + 渠道内 Opt-in 取交集）；增试跑审计。按 playbooks/15 沙箱促销规则测试。

### Incident B — Aadhaar over-collection / 事件 B — Aadhaar 过度采集 {#in-incident-2}
**What happened / 事件**: a KYC workflow stored full Aadhaar numbers "for convenience"; this breached purpose-limitation and Aadhaar-storage caution.
**经过**：某 KYC 流程「为方便」存完整 Aadhaar 号；违反目的限制与 Aadhaar 存储谨慎。

**Resolution / 处置**: purged stored Aadhaar; moved to masked-reference / VID token; retention capped at KYC-need window; re-educated front desk.
**处置**：清除已存 Aadhaar；转脱敏引用/VID 令牌；留存限 KYC 所需窗；重申前台培训。

---

## ⑤ Outcomes & Surprises / 成效与意外 {#in-outcomes}

- UPI autopay cut failed-renewal churn ≈22% vs card-only retries.
  UPI 自动付使续费失败流失较纯卡重试降约 22%。
- Festival load (Diwali/New Year) handled via `playbooks/15` war-room + capacity review — zero booking outages.
  节庆负载（排灯/新年）经 playbooks/15 作战室 + 容量复审——零约课宕机。
- **Surprise / 意外**: BNPL drove acquisition but lifted default-risk on low-tier plans — tiering had to price BNPL cost in, not hide it.
  **意外**：BNPL 拉动获客却抬高低档计划违约风险——分层须将 BNPL 成本计入价而非隐藏。

---

## ⑥ 10-Item Transferable Market-Entry Checklist / 10 项可迁移入市清单 {#in-checklist}

1. Choose an MMS with UPI deep-links + WhatsApp + en-IN/local fields + GST e-invoice. / 选含 UPI 深链 + WhatsApp + en-IN/本地字段 + GST 电子发票的 MMS。
2. Build DND screening as a hard pre-send gate for every SMS/call (HI-7). / 将 DND 筛检设为每波短信/电话发送硬闸（HI-7）。
3. Capture verifiable, multilingual consent; appoint DPO-style contact; breach runbook per DPDP Rules. 🔄 / 取可验证多语种同意；设 DPO 式联络；按 DPDP 细则编泄露 runbook。
4. Do NOT store full Aadhaar numbers — use masked reference / VID token only. / 勿存完整 Aadhaar 号——仅用脱敏引用/VID 令牌。
5. Wire UPI as default with autopay mandate; cards + guarded BNPL. / UPI 默认 + 自动付授权；卡 + 设防 BNPL。
6. Segregate prepaid float; fair cancellation/refund in contract (HI-3). / 隔离预收款项；合同写公平退会/退费（HI-3）。
7. Protect festival load (Diwali/New Year) via playbooks/15 war-room + capacity review. / 经 playbooks/15 作战室 + 容量复审防护节庆负载。
8. Price BNPL cost into tiering; monitor low-tier default risk. / 将 BNPL 成本计入分层；监低档违约风险（references/19 #w9）。
9. Keep a non-biometric entry alternative live (HI-1/face); AED/pool supervision (HI-2). / 非生物识别入场替代常在线（HI-1/人脸）；泳池/AED 监管（HI-2）。
10. Run `tools/05` to confirm DPDP Rules status before go-live. 🔄 / 上线前跑 tools/05 确认 DPDP 细则状态。

---

## ⑦ Related Files / 相关文件 {#in-related}

- `references/11-apac-compliance-south-southeast-asia.md` (India four-pack + DNC/TRAI)
- `references/13-data-and-llm-engine.md` #k-64-india (DPDP residency — no broad mandate)
- `data/07-apac-regional-differences.md` §① UPI, §② WhatsApp+DND, §④ Diwali
- `references/19-growth-and-sales-stack.md` #w9-online-sales-bnpl (BNPL risk)
- `playbooks/15-peak-season-and-promo-protection.md` (festival load protection)
- `data/14-repair-scripts-and-sla-library.md` (SLA + market localization)
- `tools/05-regulation-traceability-verification.md`

---

## ⑧ G13 Tri-Perspective Note / G13 三视角注记 {#in-g13}

**Architect / 架构师**: UPI + WhatsApp with en-IN/local; DND hard-gate; DPDP verifiable-consent + breach timer; no Aadhaar storage (masked/VID); cloud region per DPDP Rules (no broad localization mandate).
**架构师**：UPI + WhatsApp 配 en-IN/本地；DND 硬闸；DPDP 可验证同意 + 泄露计时；不存 Aadhaar（脱敏/VID）；云区域按 DPDP 细则（无广泛本地化强制）。

**Operator / 运营者**: one SOP for multilingual notice, refund, DND screening, Aadhaar caution, and festival war-room; tier BNPL cost transparently.
**运营者**：一套 SOP 管多语种告知、退费、DND 筛检、Aadhaar 谨慎、节庆作战室；BNPL 成本透明计入分层。

**Member / 会员**: gets clear multilingual consent, a face-entry alternative, fair refund, no DND-spam, and KYC that never hoards their Aadhaar.
**会员**：获清晰多语种同意、人脸替代、公平退费、无 DND 骚扰，以及不囤积 Aadhaar 的 KYC。
