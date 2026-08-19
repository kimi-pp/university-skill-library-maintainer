# Market Deep-Case — China Mainland / 市场深挖案例·中国内地

> **Cluster / 集群**: P4-Examples (East Asia & Oceania, batch 1)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: re-verify every 180 days; law thresholds & platform policies carry 🔄 hooks — run `tools/05` before citing exact articles, `tools/04` for platform facts.
> **Cross-references / 交叉引用**: `references/10` (four-pack) · `references/12` (biometrics) · `data/07` (regional differences) · `references/17` (messaging)
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04`/`tools/05` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04`/`tools/05` 动态情报检索。

> **HONESTY PREAMBLE / 诚实声明**: This is an archetypal composite case built from common operating patterns — **not** a real, named company. All figures (member counts, ARPU, conversion rates) are **directional illustrations**, not audited data. Regulations are time-sensitive; verify every article number, threshold and penalty via `tools/05` before acting. Vendor names illustrate typical categories only.
> **诚实声明**：本案例为基于常见运营模式的「典型复合案例」——**非**真实具名企业。所有数字（会员数、ARPU、转化率）均为**方向性示例**，非审计数据。法规具时效性，行动前请经 `tools/05` 核验每条条款、阈值与罚则。供应商名称仅作类别示例。

---

## ① Context Card / ① 场景卡

**Scenario / 场景**: "FitTier 健身"（化名）是一家在中国内地二线城市运营 14 家中型门店的连锁品牌，正将 11 家直营店与一个加盟试点统一到一套数字化会员与营销中台。

**Scenario / 场景 (EN)**: "FitTier Fitness" (pseudonym) runs 14 mid-size clubs across a tier-2 mainland city cluster, consolidating 11 directly-operated sites and one franchise pilot onto one digital membership and marketing mid-platform.

**Operator profile / 运营者画像**: 门店平均 1,200㎡，含团课教室与泳池；会员约 6.8 万，月新增 2,800；数字化负责人 1 名 + 外包实施团队。

**Operator profile / 运营者画像 (EN)**: ~1,200㎡ avg floor with group-class rooms and a pool; ~68k members, 2,800 new/month; one digital lead plus an outsourced implementation team.

**Why this market is distinctive / 为何此市场特殊**: 微信生态是第一入口；预付卡受单用途预付卡监管；生物识别属敏感个人信息须单独同意并提供替代；抖音本地生活是重要获客渠道。

**Why distinctive / 为何特殊 (EN)**: WeChat ecosystem is the primary front door; prepaid cards are supervised as single-purpose prepaid cards; biometrics are sensitive PI needing separate consent and an alternative; Douyin local-life is a major acquisition channel.

---

## ② The Market's Distinctive Digital Reality / ② 本市场独特数字现实

**Payments / 支付**: 微信支付与支付宝主导城市交易，现金边缘化。收银/POS 必须接入两者；会员 App 不能用 Google Play/FCM 推送，须接国产厂商推送通道。🔄

**Payments / 支付 (EN)**: WeChat Pay and Alipay dominate urban transactions; cash is marginal. POS must plug both rails; the member app cannot rely on Google Play/FCM push and must integrate domestic OEM push channels. 🔄

**Messaging / 消息**: 企业微信（WeCom）SCRM + 短信 + 小程序是会员沟通主轴；抖音/小红书/大众点评是获客三件套。营销短信须 Opt-in（反骚扰）。

**Messaging / 消息 (EN)**: WeCom SCRM + SMS + Mini-program are the member-comms backbone; Douyin/Xiaohongshu/Dianping are the acquisition trio. Promotional SMS requires opt-in (anti-harassment).

**Compliance four-pack highlights (from `references/10`) / 四件套要点**:
- ① PIPL+DSL+CSL：敏感信息单独同意、最小必要、处理记录台账。🔄
- ② 生物识别：敏感个人信息，须单独同意 + 非生物识别替代（绝不可仅人脸）。
- ③ 单用途预付卡：超地方阈值须备案 + 银行资金存管。🔄
- ④ 行业特有：短信营销同意、AIGC 内容标识、泳池 AED/急救冗余（HI-2）。🔄

**Four-pack (EN)**: ① PIPL+DSL+CSL separate consent & minimization; ② biometrics = sensitive PI, separate consent + non-biometric alternative; ③ single-purpose prepaid card filing + bank custody; ④ SMS consent, AIGC labeling, pool AED redundancy.

**Consumer habits / 消费习惯**: 私域运营（企微社群）转化高；抖音团购引流到店体验；会员习惯小程序自助约课与扫码进场。

**Consumer habits (EN)**: Private-domain ops (WeCom groups) convert well; Douyin group-buy drives trial visits; members expect self-service booking and scan-to-enter via Mini-program.

---

### Market quick-facts (from `data/07`) / 市场速览（出自 data/07）

| Dimension / 维度 | Fact / 事实 |
|---|---|
| Payment / 支付 | WeChat Pay + Alipay dominate; cash marginal in cities 🔄 |
| Messaging / 消息 | WeCom + SMS + Mini-program |
| Locale / 区域 | zh-CN simplified; family+given; smallest→largest |
| Voltage / 电压 | 220V 50Hz, CCC mark |
| Peak holiday / 旺季 | CNY + October Golden Week booking spikes |
| Resilience / 韧性 | SD-WAN multi-link; public servers need ICP 备案 |

**Quick-facts (EN)**: Wallets dominate; WeCom/SMS/Mini-program; zh-CN; 220V CCC; CNY + Golden Week peaks; SD-WAN + ICP filing.

## ③ The Real Assembly / ③ 真实拼装

### Four-pack → control scorecard / 四件套→控制记分卡

| Pack / 件套 | Control implemented / 落实控制 |
|---|---|
| ① Privacy & data | PIPL notice + separate consent + processing log |
| ② Biometric & CCTV | QR+RFID alternative; CCTV signage + retention |
| ③ Payments & prepaid | 单用途预付卡 filing + bank custody (HI-3) 🔄 |
| ④ Industry-specific | SMS opt-in (HI-7); AIGC label; fapiao; AED (HI-2) |

**Scorecard (EN)**: PIPL notice+consent+log; non-face alternative + CCTV signage; prepaid filing+custody; SMS opt-in, AIGC label, fapiao, AED.

### MMS choice logic / MMS 选型逻辑
**Local vs global vendor 🔄**: 选国产会员管理 SaaS（支持微信生态、企微 SCRM、单用途预付卡台账与本地发票），而非海外 MMS——后者不原生支持微信/支付宝、企微与增值税专票。

**Local vs global 🔄 (EN)**: Chose a domestic MMS (WeChat-native, WeCom SCRM, prepaid-card ledger, local VAT invoice) over a global MMS that lacks native WeChat/Alipay, WeCom and fapiao support.

### Payment stack wiring / 支付链路接线
微信支付 + 支付宝聚合收银；会员储值走单用途预付卡资金存管账户，与运营现金隔离（HI-3）；小程序内购课与续费直连支付。🔄

**Payment (EN)**: Aggregated WeChat Pay + Alipay checkout; membership stored-value routed to a bank-custodied single-purpose prepaid account, segregated from operating cash (HI-3); in-Mini-program class purchase and renewal link directly. 🔄

### Messaging channel setup / 消息通道搭建
企微 SCRM 做会员旅程（欢迎、约课提醒、到期续费、流失召回）；短信仅作验证码与法定通知；抖音团购券核销同步企微。营销短信前获取 Opt-in（HI-7）。

**Messaging (EN)**: WeCom SCRM drives the member journey (welcome, class reminders, renewal, win-back); SMS reserved for OTP and statutory notices; Douyin voucher redemption syncs to WeCom. Opt-in captured before any promo SMS (HI-7).

### Compliance actions taken / 已落实的合规动作
- **Face-entry decision → chose QR+RFID** (`#cn-face-entry-decision`): 经 PIPL 生物识别影响评估，认定人脸为敏感个人信息风险高，最终采用「小程序二维码 + RFID 手环」双替代，默认不开通人脸；更衣室/淋浴绝对禁摄像头（HI-5）。
- **单用途预付卡备案与存管** (`#cn-single-purpose-card`): 按门店所在地商务主管部门阈值备案，预收资金进银行存管账户，留存发卡与退费记录。🔄
- **隐私政策与单独同意弹窗**: 注册页发布隐私政策，体测健康数据、营销短信分别单独同意。
- **AIGC 内容标识** (`#cn-aigc-label`): AI 生成的训练计划/虚拟教练文案按生成式 AI 规定打标。🔄
- **发票数字化** (`#cn-fapiao-digital`): 对接增值税电子发票/数电票，续费自动开票，减少纸质票。
- **CCTV 标识与留存**: 公共区摄像头入口提示，限制留存期，访问受限。

**Compliance (EN)**: Face-entry assessed under PIPL and replaced by QR+RFID; prepaid-card filing + custody per local commerce bureau; privacy notice with separate consents; AIGC labeling; digital fapiao; CCTV signage + retention limits.

:::dynamic-hook
topic: China mainland 单用途预付卡 filing thresholds & fund custody / 中国内地单用途预付卡备案阈值与存管
stored-value: thresholds and custody % set by provincial commerce bureaus; 2024–2025 stricter local enforcement (stored 2026-07)
staleness: MED — local rules differ by province / 中——各省细则不一
action: retrieve host province's commerce-bureau prepaid-card rules before launch
fallback: if retrieval fails, present stored value + "as of 2026-07, verify before use"
:::

### Assembled stack at a glance / 拼装后技术栈一览

| Layer / 层 | Choice / 选型 | Why / 缘由 |
|---|---|---|
| MMS / 会员系统 | 国产微信原生 SaaS | 原生企微、单用途预付卡台账、数电票 🔄 |
| Payment / 支付 | 微信支付 + 支付宝聚合 | 城市主导，现金边缘化 🔄 |
| Entry / 入场 | 小程序二维码 + RFID 手环 | PIPL 生物识别评估后弃人脸替代 |
| Comms / 沟通 | 企微 SCRM + 短信(OTP) | 私域转化高，短信仅事务 |
| Acquisition / 获客 | 抖音/小红书/大众点评 | 本地生活团购引流 |
| Invoice / 发票 | 增值税数电票对接 | 续费自动开票 |
| Resilience / 韧性 | 双运营商 SD-WAN + UPS | 抗断网，保闸门监控 |

**Stack (EN)**: Domestic WeChat-native MMS; aggregated WeChat Pay + Alipay; QR+RFID entry (post-PIPL biometric assessment); WeCom SCRM + SMS-OTP; Douyin/Xiaohongshu/Dianping acquisition; digital VAT fapiao; dual-carrier SD-WAN + UPS.

### Douyin local-life operations / 抖音本地生活运营
搭建本地生活团购（体验周卡/私教体验），券码核销进企微与 MMS；直播间挂载门店 POI，到店转化追踪（抖音→企微→小程序）。🔄

**Douyin (EN)**: Built local-life group-buy (trial week-PASS/PT trial), voucher redemption feeds WeCom + MMS; livestream mounts store POI with visit-conversion tracking (Douyin→WeCom→Mini-program). 🔄

---

## ④ Two Market-Specific Incidents & Resolutions / ④ 两起市场特有事件与处置

**Incident A — 人脸门禁合规问询 (`#cn-incident-face-inquiry`)**: 市场监管与网信条线联合询问某新店拟上「仅人脸」进场方案。
**Resolution / 处置**: 出示 PIPL 生物识别影响评估与「二维码+RFID」替代方案，撤回仅人脸计划，加贴单独同意弹窗；事件零处罚。

**Incident A (EN)**: A new site proposed face-only entry; regulators inquired. Resolved by presenting the PIPL biometric impact assessment and the QR+RFID alternative, withdrawing face-only, adding a separate-consent pop-up; no penalty.

**Incident B — 预付卡资金混同自查 (`#cn-incident-fund-comingling`)**: 审计发现加盟试点把预收会费并入运营账户支付工资。
**Resolution / 处置**: 立即开设银行存管账户迁移预收资金，补齐备案材料，修订财务 SOP 隔离（HI-3）；对会员公示资金安全说明。

**Incident B (EN)**: An audit found the franchise pilot co-mingled prepaid fees with operating cash for payroll. Resolved by opening a custody account, migrating funds, back-filing, and revising finance SOPs (HI-3); published a member fund-safety notice.

**Preventive controls / 预防控制**:
- 会员储值账户与运营账户物理隔离，财务系统双签校验。 / Member-float vs operating account physically separated; dual-sign finance check.
- 每月自动跑单用途预付卡备案阈值自检脚本。 / Monthly auto self-check of prepaid filing threshold. 🔄
- 人脸方案上线前强制 PIPL 生物识别影响评估关卡。 / Mandatory PIPL biometric impact-assessment gate before any face plan.

---

## ⑤ Outcomes & What Surprised the Operator / ⑤ 结果与被意外之处

**Outcomes / 结果**: 私域企微会员 90 日留存提升方向性 +18%；抖音团购到店转化率方向性 ~12%；因取消人脸，进场速度略降但投诉率下降；发票数字化使财务对账工时方向性 −40%。

**Outcomes (EN)**: WeCom private-domain 90-day retention up directionally +18%; Douyin group-buy visit-conversion ~12%; dropping face-entry slowed entry slightly but cut complaints; digital fapiao cut reconciliation effort ~40%.

**What surprised / 意外**: ① 会员对「非人脸」接受度高于预期，反而视其为隐私尊重；② 单用途预付卡备案比想象中更依赖地方细则，跨省扩张需逐省核验；③ AIGC 标识成本极低但显著提升品牌信任。

**Surprises (EN)**: Members welcomed the non-face alternative as privacy-respecting; prepaid filing is heavily province-specific; AIGC labeling was cheap yet boosted trust.

### Directional outcomes snapshot / 方向性成果速览

| Metric / 指标 | Before / 前 | After / 后 | Note / 备注 |
|---|---|---|---|
| WeCom 90-day retention / 企微 90 日留存 | baseline | +18% | directional / 方向性 |
| Douyin visit-conversion / 抖音到店转化 | baseline | ~12% | group-buy / 团购 |
| Reconciliation effort / 对账工时 | baseline | −40% | fapiao digital / 数电票 |
| Complaint rate / 投诉率 | baseline | lower | dropped face / 弃人脸 |

**Snapshot (EN)**: WeCom retention +18%, Douyin visit-conversion ~12%, reconciliation effort −40%, complaint rate down after dropping face entry.

---

## ⑥ Transferable Checklist (10 items) / ⑥ 可迁移清单（10 项）

1. 选型以微信生态原生为先，海外 MMS 多数不原生支持。 / Pick WeChat-native MMS; most global MMS lack native support. 🔄
2. 人脸门禁前先做 PIPL 生物识别影响评估，默认提供 QR/RFID/PIN 替代。 / Run PIPL biometric assessment before face entry; offer QR/RFID/PIN alternative by default.
3. 单用途预付卡超阈值即备案 + 银行存管，预收资金绝不运营混同（HI-3）。 / File + custody prepaid card above threshold; never co-mingle (HI-3). 🔄
4. 营销短信必须 Opt-in 并即时退订（HI-7）。 / Promo SMS opt-in + instant unsubscribe (HI-7).
5. 企微 SCRM 承载会员旅程，短信仅验证码/法定通知。 / WeCom SCRM for journey; SMS only OTP/statutory.
6. AIGC 生成内容按规打标，体测/健康数据单独同意。 / Label AIGC; separate consent for health metrics.
7. 对接增值税数电票，续费自动开票。 / Integrate digital VAT fapiao; auto-issue on renewal.
8. 抖音本地生活券核销同步 MMS，追踪到店转化。 / Sync Douyin voucher redemption to MMS; track visit conversion. 🔄
9. CCTV 入口标识 + 留存上限，更衣室/淋浴零摄像头（HI-5）。 / CCTV signage + retention cap; zero cameras in changing rooms (HI-5).
10. 上线前跑 `tools/05` 核验所有条款阈值。 / Run `tools/05` to verify all articles/thresholds pre-launch.

---

## ⑦ Related Files / ⑦ 相关文件
- `references/10-apac-compliance-east-asia-oceania.md` — four-pack for mainland. / 内地四件套。
- `references/12-biometrics-and-cctv.md` — face-entry & HI-5 red lines. / 人脸与 HI-5 红线。
- `references/17-omnichannel-messaging.md` — WeCom/SMS journey. / 企微短信旅程。
- `data/07-apac-regional-differences.md` — payment & channel facts. / 支付渠道事实。
- `data/02-regulation-traceability-index.md` — machine-checkable anchors. / 可机检锚点。

---

## ⑧ G13 Tri-Perspective Note / ⑧ G13 三视角注记

> **Architect / 架构师**: Map PIPL four-pack to system controls — separate-consent pop-ups, non-face entry fallback, prepaid custody ledger, AIGC label flags in CMS. / 将 PIPL 四件套映射为系统控制：单独同意弹窗、非人脸替代入场、预付存管台账、CMS 内 AIGC 标识位。
> **Operator / 运营者**: Embed the 10-item checklist into onboarding SOP and finance runbook; verify province-specific prepaid thresholds before each new city. / 把 10 项清单嵌入入驻 SOP 与财务手册；每进一城先核验该省预付阈值。
> **Member / 会员**: Receives a clear privacy notice, a genuine non-face alternative, transparent total price, and automatic fapiao — privacy-respecting by design. / 获得清晰隐私告知、真实非人脸替代、透明总价与自动发票——隐私友好。
