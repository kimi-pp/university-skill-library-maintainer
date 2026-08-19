# Market Deep-Case — Taiwan (China) / 市场深挖案例·中国台湾

> **Cluster / 集群**: P4-Examples (East Asia & Oceania, batch 1)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: re-verify every 180 days; 個资法 & 定型化契約 & payment facts carry 🔄 hooks — run `tools/05` for articles, `tools/04` for platform facts.
> **Cross-references / 交叉引用**: `references/10` (four-pack) · `references/12` (biometrics) · `data/07` (regional differences) · `references/17` (messaging)
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04`/`tools/05` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04`/`tools/05` 动态情报检索。

> **HONESTY PREAMBLE / 诚实声明**: This is an archetypal composite case built from common operating patterns — **not** a real, named company. All figures are **directional illustrations**, not audited data. Regulations are time-sensitive; verify every article number, threshold and penalty via `tools/05` before acting. Vendor names illustrate typical categories only.
> **诚实声明**：本案例为基于常见运营模式的「典型复合案例」——**非**真实具名企业。所有数字均为**方向性示例**，非审计数据。法规具时效性，行动前请经 `tools/05` 核验每条条款、阈值与罚则。供应商名称仅作类别示例。

---

## ① Context Card / ① 场景卡

**Scenario / 场景**: "FormoStudio 瑜伽· Pilates 工作室连锁"（化名）在台北与台中运营 9 家精品工作室，主打女性客群与小班课，正统一会员系统并强化合规。

**Scenario / 场景 (EN)**: "FormoStudio yoga·Pilates chain" (pseudonym) runs 9 boutique studios in Taipei and Taichung, female-skewed clientele and small-group classes, unifying its membership system and hardening compliance.

**Operator profile / 运营者画像**: 会员约 14,000，月新增 1,600；IT 偏轻量，依赖本地 SaaS；团队关注个资法与定型化契约风险。

**Operator profile / 运营者画像 (EN)**: ~14k members, 1,600 new/month; light IT leaning on local SaaS; team focused on PDPA and model-contract risk.

**Why distinctive / 为何特殊**: 個资法对敏感资料（健康、生物识别）要求 explicit 同意；健身中心定型化契約强制冷静期、退费公式、终止权并禁用「不得记载」条款；LINE 是第一会员通道；支付以信用卡 + LINE Pay + 街口为主；统一发票电子化为强制常态；电压 110V。

**Why distinctive / 为何特殊 (EN)**: PDPA requires explicit consent for sensitive data (health, biometric); the model gym contract mandates cooling-off, refund formula, termination and bans "不得記載" clauses; LINE is the primary member channel; payments cards + LINE Pay + JKOPAY; e-invoice (統一發票) is standard; 110V.

---

## ② The Market's Distinctive Digital Reality / ② 本市场独特数字现实

**Payments / 支付**: 信用卡、LINE Pay、街口支付（JKOPAY）为主，现金仍常见；统一发票（統一發票）电子化为开票常态。🔄

**Payments / 支付 (EN)**: Cards, LINE Pay and JKOPAY dominate, cash still common; e-invoice (統一發票) is the standard issuance mode. 🔄

**Messaging / 消息**: LINE 官方账号是第一会员旅程通道（购票、约课、到期、关怀）；LINE 内营销须 Opt-in（個资法 + 反垃圾）。

**Messaging / 消息 (EN)**: LINE Official Account is the primary member journey channel (purchase, booking, renewal, care); LINE marketing requires opt-in (PDPA + anti-spam).

**Compliance four-pack highlights (`references/10`) / 四件套要点**:
- ① 個資法（PDPA）：敏感资料 explicit 同意；资料清册；跨区域传输审慎。🔄
- ② 生物识别：入场须非生物识别替代；监控标识；更衣室绝对禁区（HI-5）。
- ③ 健身中心定型化契約：强制披露 + 禁用不公平条款（如没收退费）。
- ④ 消费者保护：法定冷静期/终止权；营销同意依個资法。

**Four-pack (EN)**: ① PDPA explicit consent for sensitive data; data inventory; careful mainland–Taiwan-region transfer; ② non-biometric entry alternative; ③ model gym contract mandatory disclosures & banned clauses; ④ statutory cooling-off/termination; marketing consent under PDPA.

**Consumer habits / 消费习惯**: 会员高度依赖 LINE；重视个资与退费权益；女性客群对隐私与体测数据敏感。

**Consumer habits (EN)**: Members heavily rely on LINE; value data privacy and refund rights; female clientele sensitive to privacy and body-metric data.

---

### Market quick-facts (from `data/07`) / 市场速览（出自 data/07）

| Dimension / 维度 | Fact / 事实 |
|---|---|
| Payment / 支付 | Cards + LINE Pay + JKOPAY; cash still common 🔄 |
| Messaging / 消息 | LINE (first channel) |
| Locale / 区域 | zh-TW traditional; family+given; smallest→largest |
| Voltage / 电压 | 110V 60Hz; step-down for 220V gear |
| Peak holiday / 旺季 | CNY; earthquake + typhoon belt |
| Resilience / 韧性 | UPS + generator; offline POS; seismic-rated racking |

**Quick-facts (EN)**: Cards/LINE Pay/JKOPAY; LINE first; zh-TW; 110V step-down; CNY + quake/typhoon; UPS + offline POS.

## ③ The Real Assembly / ③ 真实拼装

### Four-pack → control scorecard / 四件套→控制记分卡

| Pack / 件套 | Control implemented / 落实控制 |
|---|---|
| ① Privacy & data | 個資法 explicit consent + inventory 🔄 |
| ② Biometric & CCTV | RFID+QR; CCTV signage (HI-5) |
| ③ Payments & prepaid | model-contract refund + segregation (HI-3) |
| ④ Industry-specific | cooling-off/termination; anti-spam (HI-7) |

**Scorecard (EN)**: PDPA explicit consent + inventory; non-face entry + CCTV; model-contract refund + segregation; cooling-off + anti-spam.

### MMS choice logic / MMS 选型逻辑
**Local vs global vendor 🔄**: 选本地 MMS（原生 LINE OA、統一發票、個資法同意管理、110V 设备兼容）；海外 MMS 常缺 LINE 深度集成与发票模块。

**Local vs global 🔄 (EN)**: Chose a local MMS (native LINE OA, 統一發票, PDPA consent management, 110V-compatible); global MMS often lacks deep LINE integration and invoice modules.

### Payment stack wiring / 支付链路接线
信用卡 + LINE Pay + 街口聚合；月费自动扣缴；预收款项隔离（HI-3）；统一发票自动开立并对接政府整合服务平台。🔄

**Payment (EN)**: Aggregated cards + LINE Pay + JKOPAY; auto-debit monthly; prepaid float segregated (HI-3); e-invoice auto-issued and reconciled to the government platform. 🔄

### Messaging channel setup / 消息通道搭建
LINE 官方账号承载旅程（欢迎、约课提醒、续费、流失召回、关怀）；Opt-in 在 LINE 内取得（HI-7）；体测/健康资料与营销分别同意。

**Messaging (EN)**: LINE OA drives the journey (welcome, class reminders, renewal, win-back, care); opt-in captured in LINE (HI-7); health metrics & marketing consented separately.

### Compliance actions taken / 已落实的合规动作
- **定型化契約配置** (`#tw-model-contract`): 会员系统内置定型化契約强制条款——冷静期、退费公式、终止权；剔除所有「不得記載」禁用条款（如不公平没收退费）。
- **個资法同意管理** (`#tw-pdpa-consent`): 注册页发布隐私政策，体测健康数据、生物识别门禁、营销分别 explicit 同意；建资料清册。
- **非人脸入场** (`#tw-non-face-entry`): 采用 RFID 手环 + APP 二维码；CCTV 入口标识 + 留存上限，更衣室零摄像头（HI-5）。
- **统一发票整合** (`#tw-einvoice`): 对接财政整合服务平台，续费/购课自动开統一發票；会员后台可查。
- **大陆与台湾地区间传输审慎** (`#tw-mainland–Taiwan-region`): 若有跨区域资料传输，依個資法及有关规定评估并设保障。🔄

**Compliance (EN)**: Model-contract clauses encoded (cooling-off, refund formula, termination; banned clauses removed); PDPA separate explicit consents + inventory; RFID+QR non-face entry; e-invoice integration; careful mainland–Taiwan-region transfer assessment. 🔄

:::dynamic-hook
topic: Taiwan 個資法 mainland–Taiwan-region transfer & model gym-contract enforcement / 中国台湾个资法大陆与台湾地区间传输与定型化契约执法
stored-value: PDPA and applicable regulations govern mainland–Taiwan-region transfer with care; model gym contract enforced by fair-trade/consumer bodies (stored 2026-07)
staleness: MED — enforcement guidance active / 中——执法指引活跃
action: retrieve latest PDPA guidance + model contract before launch
fallback: if retrieval fails, present stored value + "as of 2026-07, verify before use"
:::

---

### Assembled stack at a glance / 拼装后技术栈一览

| Layer / 层 | Choice / 选型 | Why / 缘由 |
|---|---|---|
| MMS / 会员系统 | 本地 LINE OA SaaS | 原生 LINE、統一發票、個資法同意 🔄 |
| Payment / 支付 | 信用卡 + LINE Pay + 街口 | 现金仍常见 🔄 |
| Entry / 入场 | RFID 手环 + APP 二维码 | 非人脸替代 |
| Comms / 沟通 | LINE 官方账号 | 第一通道，Opt-in (HI-7) |
| Invoice / 发票 | 統一發票电子化 | 政府平台对接 |
| Resilience / 韧性 | 110V 兼容 + UPS | 降压与认证 |

**Stack (EN)**: Local LINE-OA MMS; cards + LINE Pay + JKOPAY; RFID + app QR entry; LINE OA comms; e-invoice to government platform; 110V-compatible + UPS.

## ④ Two Market-Specific Incidents & Resolutions / ④ 两起市场特有事件与处置

**Incident A — 退费公式争议 (`#tw-incident-refund`)**: 一名会员引用定型化契約主张按比例退费，门店原条款含「不得記載」的没收条款。
**Resolution / 处置**: 立即下架违规条款，按法定退费公式补退差额；会员系统永久锁定禁用条款校验；零裁罚。

**Incident A (EN)**: A member invoked the model contract for pro-rata refund; the store's clause contained a banned forfeiture ("不得記載") term. Resolved by removing the clause, refunding the difference per the statutory formula, and hard-blocking banned clauses in the system; no penalty.

**Incident B — LINE 营销未取 Opt-in (`#tw-incident-line-optin`)**: 新 campaign 在未单独同意下推送 LINE 促销，遭个资法质疑。
**Resolution / 处置**: 补发同意征集、对未同意者停止推送；建立「先同意后推送」闸门（HI-7）；留存同意记录备查。

**Incident B (EN)**: A campaign pushed LINE promos without separate consent, raising PDPA concern. Resolved by re-collecting consent, stopping sends to non-consenters, and adding a "consent-before-send" gate (HI-7); retained consent logs.

**Preventive controls / 预防控制**:
- 会员系统硬编码禁用「不得記載」条款校验。 / System hard-validates banned "不得記載" clauses.
- LINE 推送前强制同意闸门，留存同意日志。 / Mandatory consent gate before LINE send; retain logs.
- 进口 220V 设备统一降压与认证清单。 / Unified step-down + certification list for 220V imports.

---

## ⑤ Outcomes & What Surprised the Operator / ⑤ 结果与被意外之处

**Outcomes / 结果**: LINE 旅程使续费提醒打开率方向性 ~68%；定型化契約内置使退费争议方向性 −50%；统一发票自动化使财务对账工时方向性 −45%；非人脸方案降低个资投诉。

**Outcomes (EN)**: LINE journey lifted renewal open rate ~68%; encoded model contract cut refund disputes ~50%; e-invoice automation cut reconciliation ~45%; non-face entry lowered privacy complaints.

**What surprised / 意外**: ① 会员对「法定退费公式」高度敏感，透明反而提升信任与续费；② 個资法 explicit 同意若做得顺滑（在 LINE 内一键）并不伤转化；③ 110V 设备采购须降压，进口 220V 器材易踩坑。

**Surprises (EN)**: Members are highly sensitive to the statutory refund formula — transparency boosted trust and renewal; smooth in-LINE explicit consent didn't hurt conversion; 110V procurement needs step-down, 220V imports trip up.

---

### Directional outcomes snapshot / 方向性成果速览

| Metric / 指标 | Before / 前 | After / 后 | Note / 备注 |
|---|---|---|---|
| LINE renewal open / 续费打开 | baseline | ~68% | journey / 旅程 |
| Refund disputes / 退费争议 | baseline | −50% | model contract / 定型化 |
| Reconciliation effort / 对账工时 | baseline | −45% | e-invoice / 統一發票 |
| Privacy complaints / 个资投诉 | baseline | lower | non-face / 非人脸 |

**Snapshot (EN)**: LINE renewal open ~68%, refund disputes −50%, reconciliation −45%, privacy complaints down via non-face entry.

---

## ⑥ Transferable Checklist (10 items) / ⑥ 可迁移清单（10 项）

1. 会员系统内置定型化契約强制条款（冷静期/退费公式/终止）。 / Encode model-contract mandatory clauses (cooling-off/refund/termination).
2. 剔除所有「不得記載」禁用条款并系统硬校验。 / Strip all banned "不得記載" clauses with hard validation.
3. 個资法 explicit 同意：健康/生物识别/营销分别取。 / PDPA explicit consent: health/biometric/marketing separate.
4. LINE 官方账号为第一通道，Opt-in 在 LINE 内取（HI-7）。 / LINE OA primary; opt-in in LINE (HI-7).
5. 支付接信用卡 + LINE Pay + 街口；統一發票自动开。 / Plug cards + LINE Pay + JKOPAY; auto e-invoice. 🔄
6. 入场用 RFID/二维码，避免人脸；更衣室零摄像头（HI-5）。 / RFID/QR entry, avoid face; zero cameras changing rooms (HI-5).
7. 预收款项隔离（HI-3）；留存发卡与退费记录。 / Segregate prepaid float (HI-3); keep issuance/refund records.
8. 110V 电压：进口设备须降压/认证。 / 110V: step-down/certify imported gear.
9. 跨区域传输依個資法及有关规定评估。 / Assess mainland–Taiwan-region transfer per PDPA and applicable regulations. 🔄
10. 上线前跑 `tools/05` 核验個資法条款与定型化契约。 / Run `tools/05` to verify PDPA articles & model contract.

---

## ⑦ Related Files / ⑦ 相关文件
- `references/10-apac-compliance-east-asia-oceania.md` — TW four-pack. / 中国台湾四件套。
- `references/12-biometrics-and-cctv.md` — non-face & HI-5. / 非人脸与 HI-5。
- `references/17-omnichannel-messaging.md` — LINE journey. / LINE 旅程。
- `data/07-apac-regional-differences.md` — payments/locale/voltage. / 支付/区域/电压。
- `data/02-regulation-traceability-index.md` — anchors. / 锚点。

---

## ⑧ G13 Tri-Perspective Note / ⑧ G13 三视角注记

> **Architect / 架构师**: Encode model-contract clauses as system invariants, separate-consent flags per PDPA, LINE-native journey, e-invoice adapter. / 将定型化契约条款设为系统不变量，按個资法设分项同意标志，LINE 原生旅程，统一发票适配器。
> **Operator / 运营者**: Embed banned-clause validation + refund formula into membership SOP; train staff on cooling-off. / 把禁用条款校验与退费公式嵌入会员 SOP；培训冷静期流程。
> **Member / 会员**: Receives statutory cooling-off & refund rights, transparent consent, non-face entry, auto e-invoice. / 获得法定冷静期与退费权、透明同意、非人脸入场、自动发票。
