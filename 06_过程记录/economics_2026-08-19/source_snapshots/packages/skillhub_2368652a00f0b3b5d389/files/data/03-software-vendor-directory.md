# Software Vendor Directory (APAC Landscape) / 软件供应商名录（亚太格局）

> **Cluster / 集群**: B (Software systems ×26) + H (Digital assets & online presence) + W (Growth & sales stack)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Vendor landscape, pricing tiers and feature sets re-verify every 90 days via `tools/04`; every vendor cell here carries 🔄 meaning "example, not endorsement, verify before contract".
> **Cross-references / 交叉引用**: `references/06-software-landscape-apac-vendors.md` (narrative guide), `references/19-growth-and-sales-stack.md` (W11 MarTech link), `data/04-hardware-vendor-directory.md`, `data/21-anti-pattern-library.md`, `data/15-procurement-and-cost-benchmark.md`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## How to use this directory / 本名录使用说明

This is a **structured landscape map**, not a buyer's recommendation. It groups software by class and market so you can (a) know what category exists, (b) see 3+ example vendors per class including a local-market option, and (c) check the deployment / pricing / data-export / integration columns before talking to sales.
本名录是**结构化格局地图**，不是采购推荐。它按类别与市场归类，让你能（a）知道存在哪类软件、（b）每类看到 3 个以上示例供应商（含本地选项）、（c）谈销售前先核对部署/定价/数据导出/集成四列。

**Honesty preamble / 诚实前置**: The APAC fitness-software landscape shifts roughly **quarterly** — vendors merge, re-price, change API policy, enter/exit markets. Treat every vendor name 🔄 as a *pointer to investigate*, never as a verified current fact. Always run `tools/04` and ask for a written data-export clause before signing (Iron Law 8 / FDMM L1+).
**格局约每季度一变**——厂商合并、调价、改 API 政策、进出市场。把每个 🔄 厂商名当作"待查线索"，而非已核实事实。签约前务必跑 `tools/04` 并索要书面数据导出条款（铁律8）。

> **Golden rule / 黄金铁律**: No data-export clause in writing → no signature. See `data/21#ap-021-no-export-clause`.
> 无书面数据导出条款 → 不签字。见 `data/21#ap-021-no-export-clause`。

**Column legend / 列说明**: class = 类别 · vendor examples 🔄 = 示例非背书 · primary markets = 主市场 · deployment = 部署(SaaS/on-prem) · pricing model = 定价模式(区间非单价) · data-export = 数据导出能力注记 · integration = 集成生态注记.

---

## 1. Membership Management System (MMS) / 会籍管理系统

The spine system of record for members, contracts, check-ins, renewals, billing. Everything else plugs into it.
会籍系统是会会员/合同/入场/续费/扣费的记录中枢，其他系统都接入它。

### 1.1 China market / 中国市场 {#vendor-mms-cn}

| Vendor 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration ecosystem |
|---|---|---|---|---|---|
| 三体云动 (SanTi) | China Tier1–3 | SaaS (cloud) | per-club/mo subscription, tiered by member count / 按店月订，按会员量分级 | open CSV/API claimed / 宣称支持开放导出 | WeChat mini-program, Alipay, 本地支付, 门禁 |
| 青橙 (QingCheng) | China | SaaS | per-club/mo + module add-ons / 按店月订+模块叠加 | API + CSV / 开放 | 小程序, 储值合规, 体测仪 |
| 勾股健身 (GouGu) | China | SaaS | per-club/mo / 按店月订 | CSV export / CSV 导出 | 本地支付, 门禁 |
| 菲特 / 勤鸟 | China SMB | SaaS | low-cost per-club/mo / 低价按店月订 | basic CSV / 基础 CSV | 微信, 基础门禁 |

:::dynamic-hook topic="cn-mms-vendor-share-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07 the China MMS market is led by 三体云动/青橙-class SaaS with strong WeChat mini-program integration; exact market share is volatile — verify via tools/04 before citing a leader.
截至 2026-07 中国市场以三体云动/青橙类 SaaS 为主，微信小程序集成强；确切份额易变——引用"龙头"前经 tools/04 核验。
:::

### 1.2 Global / APAC-international {#vendor-mms-global}

| Vendor 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration ecosystem |
|---|---|---|---|---|---|
| Mindbody | US, AU, SG, global | SaaS | per-location/mo + per-member overage / 按点月订+超额按人 | API + export / 开放 | ClassPass, 支付, app |
| Glofox (ABC) | UK, AU, SG, global | SaaS | per-location/mo / 按点月订 | API / 开放 | 支付, 门禁, 营销 |
| Hapana | ANZ, SEA, enterprise | SaaS | per-location/mo, enterprise | API / 开放 | BI, 多店 |
| Perfect Gym | Europe, MEA, APAC | SaaS / on-prem opt | per-location/mo / 按点月订 | API / 开放 | 门禁, 支付 |
| Xplor (Mariana Tek) | UK, AU | SaaS | per-location/mo / 按点月订 | API / 开放 | 穿戴, 营销 |
| bsport | Europe, boutique | SaaS | per-location/mo / 按点月订 | API / 开放 | 支付, app |
| TeamUp | UK, boutique, class-only | SaaS | per-booking or per-mo / 按约或按月 | CSV/API / 开放 | 支付, calendar |

### 1.3 Japan / 日本 {#vendor-mms-jp}

| Vendor 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration ecosystem |
|---|---|---|---|---|---|
| hacomona (ハコモナ) | Japan | SaaS | per-club/mo, 日本本地合规 | API + CSV / 开放 | LINE, 本地支付, 门禁, 体测 |
| 其他日系 MMS | Japan | SaaS / on-prem | per-club/mo / 按店月订 | varies / 不一 | 本地生态为主 |

> **Note / 注**: Japan demands **kaiin (会員) data residency** and local receipt/tax fields; verify residency + インボイス (invoice) compliance via `tools/05` before selecting.
> 日本要求会员数据本地驻留及本地收据/税务字段；选型前经 `tools/05` 核验驻留与发票合规。

### 1.4 Korea / 韩国 {#vendor-mms-kr}

| Vendor 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration ecosystem |
|---|---|---|---|---|---|
| 韩国本地 MMS (예: 피트니스 특화 SaaS) | Korea | SaaS | per-club/mo / 按店月订 | varies / 不一 | KakaoTalk, 本地支付, 门禁 |
| Global SaaS localized | Korea | SaaS | per-location/mo / 按点月订 | API / 开放 | Kakao, 本地支付 |

> **Note / 注**: Korea market has strong local players; global SaaS often needs Korean-language support + KakaoTalk integration. Verify current leaders via `tools/04`.
> 韩国本地厂商强；国际 SaaS 常需韩文支持与 KakaoTalk 集成。当前龙头经 tools/04 核验。

---

## 2. Booking & Class Scheduling / 约课与排课 {#class-booking}

| Vendor examples 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration ecosystem |
|---|---|---|---|---|---|
| MMS-built-in (三体云动/青橙/ Mindbody/ Glofox) | all | bundled in MMS | usually included / 多随 MMS 捆绑 | via MMS API | MMS, calendar, access |
| 乐刻 / 超级猩猩 class engines | China | SaaS | module / 模块 | via MMS | MMS, app |
| standalone schedulers (예: 排课独立 SaaS) | global | SaaS | ¥200–¥2,000/mo 🔄 | CSV/API | calendar, access |

> **Buy guidance / 选购**: Most clubs should use the MMS-built-in booking to avoid a second database. Standalone only if MMS booking is weak. (FDMM L2)
> 多数场馆应用 MMS 内置约课，避免第二个库。仅当 MMS 约课弱时才独立采购（FDMM L2）。

---

## 3. POS & Payments / 收银与支付 {#class-pos-payments}

| Layer / 层 | Vendor examples 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Note / 注记 |
|---|---|---|---|---|---|---|
| Payment gateway / 支付网关 | Stripe | Global, SG, AU, JP | SaaS/API | % per txn / 按笔费率 | API | needs local entity / 需本地主体 |
| Payment gateway / 支付网关 | Adyen | Global, enterprise | SaaS/API | % + fixed / 费率+固定 | API | omnichannel / 全渠道 |
| Payment gateway / 支付网关 | GMO Payment | Japan | SaaS/API | % per txn / 按笔费率 | API | 日本本地必接之一 |
| Payment gateway / 支付网关 | Razorpay | India | SaaS/API | % per txn / 按笔费率 | API | 印度主流 |
| Payment gateway / 支付网关 | Xendit | Indonesia, PH, SEA | SaaS/API | % per txn / 按笔费率 | API | 东南亚主流 |
| Payment gateway / 支付网关 | 2C2P | TH, MY, SEA | SaaS/API | % per txn / 按笔费率 | API | 东南亚主流 |
| POS software / 收银软件 | 拉卡拉 / 收钱吧 | China | SaaS + terminal | % + terminal rental / 费率+终端租 | CSV/API | 本地支付 |
| POS software / 收银软件 | Square | US, AU, JP | SaaS + terminal | % + rental / 费率+租 | API | 一体易用 |
| POS terminal / 收银终端 | Verifone / 商米 / 新大陆 | all | on-prem/hardware | one-off + rental / 一次性+租 | n/a | see `data/04#cat-pos-terminal` |

:::dynamic-hook topic="apac-payment-gateway-fees-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
APAC card/QR fees range roughly 0.3%–3% per market and per instrument (Alipay/WeChat/Paytm/LINE Pay/EFTPOS); acquirer-tied nuances change yearly — verify exact rate via tools/04 before forecasting opex.
亚太刷卡/扫码费率约 0.3%–3%（因市场与工具而异）；收单绑定细则每年变——预测运营支出前经 tools/04 核验。
:::

---

## 4. SCRM / MarTech Sub-directory / 私域与营销科技子目录 {#scrm-martech}

China SCRM lives on WeCom (企业微信); global MarTech uses Braze/CleverTap-class engagement; Japan/Thai/TW use LINE tools. All must respect opt-in (HI-7).
中国私域在企微；国际用 Braze/CleverTap 类；日本/泰国/中国台湾用 LINE 工具。均须守 Opt-in（HI-7）。

| Sub-class / 子类 | Vendor examples 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration |
|---|---|---|---|---|---|---|
| WeCom SCRM / 企微SCRM | 微盛, 卫瓴, 探马 | China | SaaS | ¥0–¥3,000/mo SMB / 中小档 | contact+tag export | WeCom, MMS |
| Global engagement / 国际互动 | Braze, CleverTap, MoEngage, WebEngage | Global, IN, SEA | SaaS | by MAU / 按活跃用户 | event export | CRM, ads CAPI |
| LINE tools / LINE工具 | LINE Official Account, 本土 LINE 代运营 | Japan, TW, TH | SaaS | per-follower / 按粉丝 | API | LINE, CRM |
| Marketing automation / 营销自动化 | 有赞, 微盟, HubSpot | China/global | SaaS | ¥500–¥10,000/mo 🔄 | segment export | CRM, ads |
| Channel commerce / 渠道电商 | 抖音/小红书, 美团 | China | platform | commission / 佣金 | order API | MMS |

### 4.1 MarTech mini-book / 营销科技小册 {#martech-mini-book}

Per the charter (W11 link → `references/19-growth-and-sales-stack.md`), the MarTech mini-book covers the full private-domain → paid-ads → group-buy → live-commerce loop. This directory only lists the **vendor landscape**; the playbook (journeys, consent model, attribution, CAPI wiring) lives in `references/19`. 
依规划书（W11 链接 → `references/19-growth-and-sales-stack.md`），营销科技小册覆盖"私域→付费广告→团购→直播带货"全闭环。本名录只列**供应商格局**；旅程/同意模型/归因/CAPI 接线等打法见 `references/19`。

> **Consent red line / 同意红线**: No marketing send without opt-in per HI-7 and the market's anti-spam law (e.g. 中国《个人信息保护法》, 日本 Act on Specified Commercial Transactions, 韩国 ISMS, SG PDPA + spam rules). Verify exact rule via `tools/05`.
> 无 Opt-in 不发送（HI-7 + 当地反垃圾法：中国 PIPL、日本特定商取引法、韩国 ISMS、新加坡 PDPA）。具体规则经 tools/05 核验。

---

## 5. BI / Dashboards / 经营看板 {#class-bi}

| Vendor examples 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration ecosystem |
|---|---|---|---|---|---|
| 帆软 / 观远 | China enterprise | on-prem / SaaS | ¥0–¥5,000+/mo 🔄 | query+snapshot export | connector library |
| Power BI / Tableau | Global | SaaS / on-prem | per-user/mo / 按人月 | export | MS / broad |
| Metabase / Looker Studio | Global, SMB | SaaS / OSS | ¥0–¥mid 🔄 | SQL export | broad connectors |

> **When / 何时**: L3 only, after ≥3 systems integrated (see `references/18`). Premature BI = dashboard with no data.
> L3 才上，且 ≥3 系统打通后（见 `references/18`）。过早上 BI = 没数据的空看板。

---

## 6. HR / Rostering / 人事与排班 {#class-hr-rostering}

| Vendor examples 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration |
|---|---|---|---|---|---|
| 钉钉 / 企业微信 / 飞书 | China | SaaS | ¥0–¥50/user/mo 🔄 | schedule export | payroll, access |
| Deputy / Humanity / 盖雅 | Global / China | SaaS | per-user/mo / 按人月 | export | payroll, MMS |

---

## 7. Helpdesk / Ticketing / 工单客服台 {#class-helpdesk}

| Vendor examples 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration |
|---|---|---|---|---|---|
| 飞书服务台 / 企业微信工单 | China | SaaS | ¥0–¥200/agent/mo 🔄 | ticket export | MMS, messaging |
| Zendesk / Freshdesk / 美洽 | Global / China | SaaS | per-agent/mo / 按坐席月 | export | CRM, asset |

---

## 8. E-sign / 电子签 {#class-esign}

| Vendor examples 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration |
|---|---|---|---|---|---|
| 法大大 / 上上签 / 信任签 | China | SaaS | ¥0.5–¥10/view or ¥200–¥2,000/mo 🔄 | signed PDF + hash | MMS, accounting |
| DocuSign / Adobe Sign | Global | SaaS | per-doc / per-mo / 按份或月 | export | MMS |

> **Compliance / 合规**: Verify the e-sign is legally recognized in your market (CA cert / 电子签名法) before relying on it for prepaid contracts (HI-3).
> 用于预售合同前，先核验电签在本地法律效力（CA 证书/电子签名法）（HI-3）。

---

## 9. AI Vendors (churn / CV / chatbot) / AI 供应商（流失/CV/客服）{#vendor-ai}

| AI use-case / 场景 | Vendor examples 🔄 | Primary markets | Deployment | Pricing model pattern | Data-export | Integration |
|---|---|---|---|---|---|---|
| Churn prediction / 流失预测 | MMS-built-in AI modules, 独立 AI SaaS | all | SaaS / API | per-member or module / 按人或模块 | score export | MMS, CRM |
| CV posture / 体态CV | 姿动-type, 国际 CV SaaS | China/global | SaaS/edge | per-camera or module / 按摄像头或模块 | event export | MMS, app |
| Chatbot / CS / 客服机器人 | 大模型客服 SaaS, 国际对话平台 | all | SaaS | per-session or per-mo / 按会话或月 | log export | messaging, helpdesk |

:::dynamic-hook topic="apac-fitness-ai-vendor-landscape-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
The fitness-AI vendor field is the fastest-moving class (churn/CV/chatbot). Many MMS now bundle AI modules; standalone AI SaaS appear monthly. Verify current capability + bias controls via tools/04 and `data/09#algo-churn` before buying.
健身 AI 是变动最快的类别（流失/CV/客服）。许多 MMS 现已捆绑 AI 模块；独立 AI SaaS 每月涌现。采购前经 tools/04 与 `data/09#algo-churn` 核验能力与偏见控制。
:::

---

## 10. Cross-class integration map / 跨类集成图

```
MMS (spine) ──→ Booking ──→ Access control
   │              │
   ├──→ POS/Payments ──→ Accounting (deferred revenue)
   ├──→ SCRM/MarTech (consent-led)
   ├──→ BI ← pulls MMS/POS/Booking/Access
   └──→ E-sign (attach contract to member)
```
All arrows require a written data-export + webhook/retry (idempotency key) clause. See `references/18-integration-and-data-plumbing.md`.
所有箭头都需书面"数据导出 + webhook/重试（幂等键）"条款。见 `references/18`。

---

## 10. Selection top-5 by class / 各类选型 5 条

Condensed from `references/06`; use as a pre-demo checklist so sales talk doesn't drown the must-haves.
摘编自 `references/06`；用作演示前清单，免得销售话术淹了必选项。

### 10.1 MMS top-5 / 会籍系统 5 条
1. Data export (CSV/API) on demand, no lock-in. / 随时可导出（CSV/API），无锁定。
2. Local payment gateways & prepaid-fund compliance for your market. / 本地支付通道与储值合规。
3. Native booking + access-control connectors. / 原生约课与门禁对接。
4. Multi-club & multi-role permissions. / 多店多角色权限。
5. Local-language staff UI. / 本地语言后台。

### 10.2 Booking / POS / SCRM / BI / HR 速览
| Class / 类 | Top-5 one-liner / 5条一句话 |
|---|---|
| Booking / 约课 | real-time availability, waitlist, clash rules, coach sync, no-show penalty. / 实时余位、候补、冲突规则、教练同步、爽约扣罚。 |
| POS / 收银 | local pay methods, receipt fields, refund-to-source, offline mode, recon export. / 本地支付、小票字段、原路退、离线、对账导出。 |
| SCRM / 私域 | tag model, consent tracking (HI-7), journey builder, unified inbox, MMS sync. / 标签、同意追踪(HI-7)、旅程、统一收件箱、MMS 同步。 |
| BI / 看板 | connector library, refresh cadence, role dashboards, alert thresholds, export. / 连接器、刷新频率、分角色、告警阈值、导出。 |
| HR / 人事 | shift templates, leave accrual, mobile clock-in, labor-cost view, MMS link. / 班次模板、请假、移动打卡、人力成本、MMS 关联。 |

---

## 11. Directory index to all 26 software classes / 26 类软件目录索引

This directory details the high-spend classes above. The remaining classes are catalogued with full selection top-5 + vendors in `references/06-software-landscape-apac-vendors.md` §1–§26. Use that file for deep selection; use this file for the cross-market vendor landscape at a glance.
本名录详述上述高支出类别。其余类别完整选型5条+供应商见 `references/06` §1–§26。深度选型看那篇，跨市场格局看本篇。

| Class / 类 | Landmark vendors 🔄 | See / 见 |
|---|---|---|
| Member App / 会员App | MMS-built-in, 微盟小程序, Glide | references/06 §7 |
| PT management / 私教 | MMS-built-in, 青橙, Mindbody | references/06 §8 |
| Body-assessment / 体测 | InBody, 体脂康, 姿动 | references/06 §9 |
| Accounting / ERP-lite | 金蝶, Xero, MYOB | references/06 §11 |
| Payroll / 薪酬 | 金蝶薪资, ADP, Gusto | references/06 §13 |
| Inventory / 库存 | 管家婆, Square Retail | references/06 §16 |
| Signage CMS | 视达, Yodeck, NoviSign | references/06 §17 |
| VMS | 海康 iVMS, Milestone | references/06 §18 |
| Wi-Fi captive | 锐捷, UniFi | references/06 §19 |
| Energy | 安科瑞, Schneider | references/06 §20 |
| Survey/NPS | 问卷星, Qualtrics | references/06 §21 |
| LMS | 腾讯乐享, Moodle | references/06 §22 |
| Doc-cloud | 腾讯文档, Google Workspace | references/06 §23 |
| Password / 密码 | 1Password, Bitwarden | references/06 §24 |
| Backup / 备份 | Veeam, Acronis | references/06 §25 |
| Endpoint / 终端安全 | 360, CrowdStrike | references/06 §26 |

---

## 12. Deployment & pricing glossary / 部署与定价术语

- **SaaS** = cloud subscription, vendor hosts, you log in. / 云订阅，厂商托管，你登录。
- **on-prem** = software on your server, you operate. / 软件装你服务器，你运维。
- **per-location** = priced by club/site. / 按门店计价。
- **per-member** = priced by active member count. / 按活跃会员计价。
- **transaction %** = payment cut per sale. / 每笔销售抽成。

> **Anti-pattern / 反模式**: Vendor lock-in without export → `data/21#ap-021-no-export-clause`. "Free" module that traps data → `data/21#ap-022-free-trap`.
> 无导出锁定 → `data/21#ap-021-no-export-clause`；"免费"模块困数据 → `data/21#ap-022-free-trap`。

---

## 13. MMS market-coverage matrix / 会籍系统市场覆盖矩阵

Quick grid: which vendor classes serve which market (examples 🔄, verify via tools/04). / 速查网格：哪类厂商服务哪市场（示例🔄，经 tools/04 核验）。

| Market / 市场 | China MMS 🔄 | Global MMS 🔄 | Local SCRM 🔄 | Payment gateway 🔄 |
|---|---|---|---|---|
| China 大陆 | 三体云动/青橙 | Mindbody (expats) | 企微 SCRM | 支付宝/微信/拉卡拉 |
| Japan 日本 | hacomona | Mindbody/Glofox | LINE | GMO/Stripe |
| Korea 韩国 | 本地 SaaS | Glofox | KakaoTalk | Kakao/本土 |
| SG/ANZ | — | Mindbody/Glofox/Xplor | Braze-class | Stripe/Adyen/EFTPOS |
| India | — | Glofox | WebEngage | Razorpay |
| SEA | — | Glofox/bsport | LINE/ Braze | Xendit/2C2P/Adyen |

> Every cell re-verify every 90 days; a vendor strong in one market may be absent next door.
> 每格每 90 天重核；某市场强的厂商隔壁可能缺席。

---

## G13 Tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: selection matrix + integration spine above; every class has ≥3 vendor options incl. a local one (Iron Law 8).
- **Operator / 运营者**: pricing *patterns* + data-export red line + "verify via tools/04" before contract.
- **Member / 会员**: consent-led MarTech (HI-7), portable data-export, no lock-in surprise. No touchpoint is orphaned — the MMS spine connects all.
本文件覆盖架构师（选型矩阵+集成中枢）、运营者（定价模式+导出红线+签约前核验）、会员（同意制营销 HI-7、可携数据、无锁定惊吓）三视角；会籍系统中枢承接所有触点，无孤儿触点。
