# Growth Campaign Brief & Pre-flight / 增长活动简报与起飞前检查

> **Cluster / 集群**: W (Growth & sales stack)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Ad-platform APIs, CAPI/pixel policy, group-buy commission, BNPL availability, prepaid thresholds and anti-spam quiet-hours change constantly — re-verify via `tools/04`/`tools/05` before each launch. / 广告平台 API、CAPI/像素政策、团购佣金、BNPL 可用性、预付阈值、反垃圾静默时段持续变——每次上线前经 `tools/04`/`tools/05` 复核。
> **Cross-references / 交叉引用**: `references/19-growth-and-sales-stack.md` (W1–W12) · `references/17-omnichannel-messaging.md` (M · channel map) · `references/10`+`references/11` (F · HI-3/HI-7) · `templates/40-consent-ledger.md` (planned) · `data/20-micro-details-ledger.md` (capacity) · `data/21-anti-pattern-library.md` · `tools/05-regulation-traceability-verification.md` · `tools/06-roi-three-scenario.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## 1. Purpose & when to use / ① 用途与使用时机

**English / 英文**: A single, fill-in-the-blank brief you complete *before* any growth campaign goes live — paid (W1/W6/W9), group-buy (W2/W8), private-domain (W3), outbound (W4), referral (W5), or a mix. It forces nine checks that prevent the most common, most expensive failures: a campaign that burns budget blind, sends to non-consented lists, breaches prepaid rules, or floods a club that cannot absorb the leads.

**中文 / 中文**: 一份上线前必填的填空式简报——付费投放（W1/W6/W9）、团购（W2/W8）、私域（W3）、外呼（W4）、裂变（W5）或组合。它强制 9 项检查，规避最常见也最贵的失败：盲烧预算、发给未同意名单、触犯预付规则、或把超出承接能力的线索灌进场馆。

> **Use this brief when / 用本简报当**:
> - Launching any new acquisition campaign, or scaling an existing one. / 启动任何新获客活动，或扩量现有活动。
> - The offer touches stored value / prepaid (HI-3 territory). / 优惠涉及储值/预付（HI-3 范畴）。
> - Messaging goes to a list you did not build with opt-in (HI-7 territory). / 触达非 Opt-in 自建名单（HI-7 范畴）。
> - FDMM L2+ and spend exceeds ¥100k-equivalent (triggers ROI three-scenario `tools/06`). / FDMM L2+ 且花费超 10 万元等值（触发 ROI 三情景 `tools/06`）。

---

## 2. Prerequisites / ② 前置条件

- [ ] **FDMM level known / FDMM 等级已知**: L1 may run owned/organic (W3/W5 light); paid media + BNPL need L2+ and cash flow (`references/19#W19-first-30-days`). / L1 可做自有/自然（W3/W5 轻量）；付费+BNPL 需 L2+ 与现金流。
- [ ] **Consent ledger live / 同意台账已上线**: `templates/40-consent-ledger.md` (planned) captures per-member opt-in per channel before any send. / 每会员每通道 Opt-in 已落台账，方可发送。
- [ ] **Channel accounts claimed / 通道账号已认领**: per-market accounts from `references/17-omnichannel-messaging.md#M1` (WeChat/LINE/WhatsApp/Kakao/Zalo/OA). / 按 `references/17#M1` 认领各市场账号。
- [ ] **Prepaid rule verified / 预付规则已核验**: target market's stored-value cap, escrow, cooling-off, refund via `tools/05` (HI-3). / 目标市场储值上限/托管/冷静期/退款经 `tools/05` 核验（HI-3）。
- [ ] **LTV baseline known / LTV 基准已知**: from `data/01-kpi-benchmark-library.md` (use YOUR club's number, not a generic benchmark). / 用本馆数据，非通用基准。
- [ ] **Capacity headroom known / 承接余量已知**: booking/PT/door capacity & rate-limit headroom from `data/20-micro-details-ledger.md`. / 预约/私教/入场余量与限流余量见 `data/20`。

---

## 3. THE TEMPLATE / ③ 模板（填空式）

> **Guidance / 指引**: Fill every block. A blank block = a risk you have not thought through. Do not launch with blanks. / 每块必填；留空=未想清的风险，不得带空上线。

### 3.1 Campaign ID & owner / 活动编号与负责人
- **Campaign ID / 活动编号**: `____` (e.g. SG-BOUTIQUE-WA-TRIAL-2026Q3)
- **Owner / 负责人**: `____` · **Markets / 市场**: `____` · **Cluster / 模块**: W__ (W1/W2/W3/W4/W5/W6/W8/W9)
- **Launch date / 上线日**: `____` · **End date / 结束日**: `____`

### 3.2 Objective & north-star link / 目标与北极星挂钩 {#objective-north-star}
- **Business objective / 经营目标**: `____` (e.g. "acquire 60 trial members in 4 weeks")
- **North-star metric / 北极星指标** (from `references/19#W12-experimentation`): `____` (pick ONE: weekly active visits / new-member LTV / trial→member rate)
- **Guardrail that must NOT break / 不得破的护栏**: `____` (churn / complaint rate / margin % — see `references/19#W12-experimentation`)

> **Why / 为何**: A campaign with no north-star is a vanity spend; a campaign that breaks a guardrail (e.g. margin) "wins" expensively. / 无北极星=虚荣花费；破了护栏（如毛利）"赢了也贵"。

### 3.3 Audience & consent pre-flight (HI-7) / 受众与同意起飞检查（HI-7） {#audience-consent-preflight}
- **Target segment / 目标分群**: `____` (new movers / lapsed members / class-type X lovers)
- **Source list / 名单来源**: `____` — MUST be opted-in only. No opt-in, no send. / **仅限已 Opt-in 名单。无同意不发送。**
- **Consent ledger ref / 同意台账引用**: `templates/40-consent-ledger.md#____` (record purpose + channel + timestamp + withdraw path)
- **Market anti-spam law / 市场反垃圾法**: `____` (see `references/17-omnichannel-messaging.md#M10`; verify exact article via `tools/05`)
- **Unsubscribe mechanism / 退订机制**: `____` (every message carries STOP/退订; enforced ≤72h)

> **Hard line / 红线**: HI-7 is a one-vote veto. If the list is scraped, bought, or stale-consent, STOP the campaign. Fine risk is real across SG Spam Control Act / AU Spam Act / JP 特定電子メール法 / KR 情報通信網法. / HI-7 一票否决；名单爬虫/购买/同意过期即停。各市场罚款真实存在。

### 3.4 Channel plan per market / 分市场通道计划 {#channel-plan}
| Market / 市场 | Channel / 通道 | Message type / 类型 | Quiet hours / 静默时段 | Marketing cap / 上限 |
|---|---|---|---|---|
| `____` | `____` | transactional / marketing | `references/17#M9b` baseline | `references/17#M9b` |

> **Guidance / 指引**: Copy the quiet-hours & frequency baseline from `references/17-omnichannel-messaging.md#M9b`; verify exact windows via `tools/05`. Transactional (booking/OTP/renewal) may send anytime; marketing obeys quiet hours. / 静默时段与频控基线取自 `references/17#M9b`，具体窗口经 `tools/05` 核验。事务类随时，营销守静默。

### 3.5 Offer & prepaid-compliance check (HI-3) / 优惠与预付合规检查（HI-3） {#offer-prepaid-check}
- **Offer description / 优惠描述**: `____`
- **Is it stored value / 是否储值**: ☐ Yes  ☐ No
- **If YES — prepaid check / 若是，预付检查**:
  - Stored-value cap per market / 市场储值上限: `____` (verify via `tools/05`, reference `references/10`/`references/11`)
  - Fund supervision / escrow / 资金监管/托管: `____` (mandatory where required)
  - Expiry & refund clarity / 过期与退款清晰: `____`
  - Cooling-off / 冷静期: `____` (W9)

:::dynamic-hook topic="apac-prepaid-stored-value-threshold" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07: prepaid/stored-value thresholds, escrow obligation and cooling-off periods differ sharply across the 12 markets (e.g. CN 单用途预付卡 rules, SG/other PDPA-adjacent consumer regimes). Exact caps change — verify the precise article + threshold for YOUR market via tools/05 before selling any stored-value offer. / 截至 2026-07：12 市场预付/储值上限、托管义务、冷静期差异极大（如大陆单用途预付卡规则、新加坡等消保机制）。具体上限会变——售卖任何储值优惠前经 tools/05 核精确条款+阈值。
:::

> **Hard line / 红线**: HI-3 is a one-vote veto. A stored-value offer that violates local fund supervision = prepaid scandal risk (`references/19#W7-loyalty` AP-W7). Verify before launch, not after. / HI-3 一票否决；储值优惠违当地资金监管=预付暴雷风险。上线前核验，而非事后。

### 3.6 Tracking plan / 追踪方案 {#tracking-plan}
- **UTM discipline / UTM 纪律**: every link `?utm_source=__&utm_medium=__&utm_campaign=__&utm_content=__`; one spreadsheet = single source of truth. / 每链接带参；一张表作唯一真相。
- **CAPI / pixel events / CAPI 与像素事件**: `____` (Meta CAPI / Google Enhanced Conversions / TikTok-Douyin Events API — server-side preferred). 🔄
- **Offline conversion upload / 离线转化回传**: closed deals pushed back to platform with hashed PII + LTV. / 成交以哈希 PII+LTV 回传平台。
- **Promo-code attribution / 优惠码归因**: unique code per channel/variant → `____`.

> **Anti-pattern guard / 反模式护栏**: "pixel-only, no offline upload" (AP-W1, `data/21`) hides which ad actually closed. Always wire offline upload. / 仅像素无回传（AP-W1）看不见哪条广告成交，务必接回传。

### 3.7 Budget & CAC guardrails / 预算与 CAC 护栏 {#budget-cac}
- **Total budget / 总预算**: `____` · **Per-channel split / 分渠道**: `____`
- **Max acceptable CAC / CAC 上限** = function of your LTV: `CAC_cap = LTV (data/01) × target_CAC/LTV_ratio`. If actual CAC > 12-month member contribution → cut. 🔄
- **Cut rule / 砍量规则**: `____` (e.g. pause channel if CAC > cap for 7 consecutive days)

> **Rule / 守则**: owned channels (W3) are the cheapest retention lever — protect their budget even when paid scales (`references/19#W12-budget`). / 自有通道（W3）最便宜留存杠杆——付费扩量也保其预算。

### 3.8 Capacity check / 承接能力检查 {#capacity-check}
- **Max leads/week the club can absorb / 场馆周可承接线索上限**: `____` (booking slots + PT capacity + front-desk bandwidth). See `data/20-micro-details-ledger.md` rate-limit headroom. / 预约位+私教产能+前台人力；限流余量见 `data/20`。
- **Rate-limit headroom / 限流余量**: `____` (if demand > headroom, throttle acquisition or add slots)
- **Peak-inventory protection / 黄金时段保护**: platforms/aggregators get OFF-peak only (`references/19#W2-group-buy`, `references/19#W8-aggregators`).

### 3.9 Campaign timeline with quiet hours / 含静默时段的活动时间表 {#campaign-timeline}
| Date / 日期 | Action / 动作 | Market / 市场 | Send window / 发送窗 (local) |
|---|---|---|---|
| `____` | `____` | `____` | within `references/17#M9b` quiet-hours rule |

### 3.10 Post-campaign report sheet / 活动后报告表 {#post-campaign-report}
| Metric / 指标 | Planned / 计划 | Actual / 实际 | Variance / 差异 | Read / 解读 |
|---|---|---|---|---|
| Spend / 花费 | `____` | `____` | `____` | `____` |
| Leads / 线索 | `____` | `____` | `____` | `____` |
| Trials / 体验 | `____` | `____` | `____` | `____` |
| Members / 会员 | `____` | `____` | `____` | `____` |
| CAC / 获客成本 | `____` | `____` | `____` | `____` |
| ROAS / 广告回报 | `____` | `____` | `____` | `____` |

> **Micro-example (illustrative numbers only, not benchmarks) / 微例（仅演示，非基准）**: SG boutique, WhatsApp trial campaign, budget S$1,500, planned 40 trials, actual 52 trials → 18 members, actual CAC S$83 vs LTV S$1,800 → healthy, scale. Numbers here are placeholders to show the table shape — replace with your real data. / 新加坡精品馆 WhatsApp 体验活动，预算 S$1,500，计划 40 体验，实际 52→18 会员，实际 CAC S$83 对 LTV S$1,800→健康可扩量。表中为占位演示，请填真实数据。

### 3.11 Pre-flight sign-off (gate before launch) / 起飞前签字（上线闸） {#preflight-signoff}
> **Gate / 闸**: Do not launch until every box is ticked. A blank = a risk unmanaged. / 每框勾完才上线；留空=风险未管。

| Check / 检查项 | Owner sign / 负责人 | OK? / 通过? |
|---|---|---|
| Objective tied to north-star + guardrail | `____` | ☐ |
| List is opted-in only (HI-7) | `____` | ☐ |
| Prepaid offer verified via `tools/05` (HI-3) | `____` | ☐ |
| UTM + CAPI + offline upload wired | `____` | ☐ |
| CAC cap set vs LTV (`data/01`) | `____` | ☐ |
| Capacity headroom confirmed (`data/20`) | `____` | ☐ |
| Quiet hours per market respected (`references/17#M9b`) | `____` | ☐ |
| Unsubscribe on every message | `____` | ☐ |

### 3.12 Multi-market campaign note / 多市场活动注记 {#multi-market-note}
> **Guidance / 指引**: If one campaign spans ≥2 markets, clone §3.3–§3.4 and §3.9 per market — consent law, prepaid cap and quiet hours differ by market (`references/10`/`references/11` vs `references/17#M9b`). One global setting is the #1 cross-market compliance bug. / 若活动跨 ≥2 市场，按市场复制 §3.3–§3.4 与 §3.9——同意法、预付上限、静默时段因市场而异；单一全局设置是头号跨市场合规 bug。

### 3.13 Field glossary / 字段术语 {#field-glossary}
- **North-star / 北极星**: the single metric the whole club optimizes (W12). / 全馆唯一优化指标。
- **Guardrail / 护栏**: a metric that must NOT worsen even if north-star improves. / 即便北极星提升也不得恶化的指标。
- **CAPI / CAPI**: server-side conversion API (more durable than pixel). / 服务端转化 API，比像素更稳。
- **Rate-limit headroom / 限流余量**: spare booking/PT/door capacity before the club saturates. / 场馆饱和前的预约/私教/入场余量。
- **ROAS / 广告回报**: revenue ÷ ad spend. / 营收÷广告花费。

### 3.14 Pause & escalation rule / 暂停与升级规则 {#pause-rule}
> **Guidance / 指引**: Define the kill switch BEFORE launch, not during the panic. / 杀开关上线前定，别等慌了再定。

- **Auto-pause trigger / 自动暂停触发**: CAC > cap for `____` consecutive days, OR complaint spike `____`, OR any HI-3/HI-7 breach. / CAC 超上限连续 `____` 天，或投诉尖峰 `____`，或任何 HI-3/HI-7 违。
- **Escalation path / 升级路径**: operator → owner → (if compliance) legal via `tools/05`. / 运营→老板→（合规）经 `tools/05` 交法务。
- **Post-pause action / 暂停后动作**: log in `data/21` if an anti-pattern triggered; document root cause in the post-campaign report §3.10. / 若触发反模式记 `data/21`；根因写进 §3.10 报告。

---

## 4. Common mistakes / ④ 常见错误

Link the full remedy library: `data/21-anti-pattern-library.md`. Most campaign failures map to these anti-patterns:
常见错误完整对策见 `data/21`；多数活动失败对应以下反模式：
- **AP-W1** Pixel-only, no offline upload → blind attribution. / 仅像素无回传→盲归因。
- **AP-W2 / AP-W8** Giving peak inventory to aggregators → margin death / cannibalization. / 黄金时段给平台→毛利死/蚕食。
- **AP-W3** Daily blast to all contacts → block + unsubscribe (HI-7 breach). / 每日群发→被屏蔽退订。
- **AP-W6** Live price undercuts front desk → channel war. / 直播破价→渠道内战。
- **AP-W7** Huge stored value, no escrow → prepaid scandal (HI-3 breach). / 大储值无托管→预付暴雷。
- **AP-W9** BNPL with no chargeback reserve → bad-debt blowup. / 无拒付准备金→坏账爆雷。
- **AP-W12** Changing 5 things at once → no learning. / 一次改 5 样→无学习。

---

## 5. Related files / ⑤ 相关文件
- `references/19-growth-and-sales-stack.md` — W1–W12 full playbook. / W1–W12 全玩法。
- `references/17-omnichannel-messaging.md` — channel map, quiet hours, consent. / 通道图、静默时段、同意。
- `references/10` + `references/11` — 12-market prepaid & anti-spam law. / 12 市场预付与反垃圾法。
- `templates/40-consent-ledger.md` (planned) — opt-in ledger you can prove. / 可举证的 Opt-in 台账。
- `data/20-micro-details-ledger.md` — capacity & rate-limit headroom. / 承接与限流余量。
- `data/21-anti-pattern-library.md` — remedies for AP-W1~W12. / AP-W1~W12 对策。
- `tools/05` — prepaid/anti-spam verification. / 预付/反垃圾核验。
- `tools/06-roi-three-scenario.md` — required if spend > ¥100k-equiv. / 花费超 10 万等值必跑。

---

## 6. G13 tri-perspective note / ⑥ G13 三视角覆盖注记

**Architect / 架构师**: The brief enforces FDMM-fit (L1 owned vs L2+ paid), compliance gates (HI-3/HI-7) and a tracking architecture (UTM + CAPI + offline upload) so attribution is auditable, not presumed. / 简报强制 FDMM 适配、合规闸（HI-3/HI-7）与可审计的归因架构（UTM+CAPI+离线回传）。
**Operator / 运营者**: Fill-in-blank blocks + capacity & quiet-hours checks give a front-desk or advisor a same-day, court-defensible launch checklist. / 填空块+承接与静默检查，给前台/顾问当日起草、可举证的上线清单。
**Member / 会员**: HI-7 opt-in + unsubscribe and HI-3 prepaid protection keep acquisition honest and non-intrusive — members hear only what they agreed to, and stored value is supervised. / HI-7 Opt-in+退订、HI-3 储值保护，保证获客诚实不侵扰——会员只收到已同意的内容，储值受监管。
