# 10 · Member App / Mini-Program Requirements (PRD-lite) / 会员 App / 小程序 需求模板（轻量 PRD）

> **Cluster / 集群**: B (Software) + H (Digital assets) · Template / 模板 · System-Building tier (FDMM L2→L3)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: App-store & mini-program policies re-verify every 90 days via `tools/04`; platform rules (IAP, WeChat/Alipay mini-program) are volatile.
> **Cross-references / 交叉引用**: `references/06-software-landscape-apac-vendors.md` (§7 Member App) · `references/17-omnichannel-messaging.md` · `data/21-anti-pattern-library.md#ap-011-ai-outbound-no-consent` · `tools/05-regulation-traceability-verification.md` · `data/07-apac-regional-differences.md#payment-method-landscape`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用（FDMM 闸门）

**Purpose / 用途**: A PRD-lite template to scope a member app or mini-program (WeChat / Alipay / LINE / Kakao) — the member's pocket front door for booking, entry, history and store.
**用途 / 中文**：轻量 PRD 模板，用于界定会员 App 或小程序（微信/支付宝/LINE/Kakao）——会员口袋里的门面：约课、入场、记录、商城。

**When to use / 适用场景**:
- MMS already chosen (FDMM L2) and you want a member-facing layer. / MMS 已选定（L2），要上层会员界面。
- Member base > 300 and retention is now a managed process. / 会员 >300 且留存需被管理。
- **FDMM gate / 闸门**: App must be MMS-backed (single source of truth, no separate member DB). Skip native app if <300 members on L1. / App 必须由 MMS 支撑（单一真相源，不另建库）；L1 且 <300 人暂缓原生 App。
- **Consent gate (HI-7) / 同意闸门**: every push/notification needs opt-in; no consent, no send. / 每条推送需 Opt-in；无同意不发送。

---

## ② Prerequisites checklist / 前置清单

- [ ] MMS selected with open API (`templates/09`). / 已选带开放 API 的 MMS。
- [ ] Target market(s) & their app-store / mini-program rules known (🔄 `tools/04`). / 已知目标市场商店/小程序规则。
- [ ] Consent policy drafted (HI-7) and quiet-hours per market set. / 已拟同意政策（HI-7）并设分市场静默时段。
- [ ] Brand assets (logo, colors) and content owner assigned. / 品牌素材与内容负责人已定。
- [ ] Payment methods mapped per market (`data/07#payment-method-landscape`). / 按市场映射支付方式。
- [ ] Offline-QR entry fallback designed for poor-signal zones. / 为弱信号区设计离线二维码入场兜底。

---

## ③ The template / 模板正文

### 3.1 User stories by persona / 分角色用户故事

> **What good looks like / 合格标准**: Every story has an acceptance sentence; no story lacks a persona. / 每个故事都有验收句；无无角色的故事。
> **Red flag / 红旗**: Writing features with no persona → you build for nobody. / 无角色堆功能 → 为无人而建。

**Member / 会员**
- As a member, I want to book a class and scan to enter, so I skip the front desk. / 作为会员，我要约课并扫码入场，免去前台。
  - Accept / 验收: booking reflects in MMS within 5s; gate opens on scan. / 5 秒内约课入 MMS，扫码开闸。
- As a member, I want to see my body-test trend, so I feel progress. / 作为会员，我要看体测趋势，感知进步。
- As a member, I want to pause marketing pushes, so I am not spammed. / 作为会员，我要能关营销推送，免被打扰。

**Coach / 教练**
- As a coach, I want the class roster on my phone, so I check-in fast. / 作为教练，我要手机看名单，快速签到。
- As a coach, I want to log a PT session, so commission is accurate. / 作为教练，我要记私教课时，提成准确。

**Front desk / 前台**
- As front desk, I want to issue a day-pass from the app, so walk-ins convert. / 作为前台，我要从 App 发次卡，转化散客。
- As front desk, I want a refund button with reason code, so audit is clean. / 作为前台，我要带原因码的退款键，审计干净。

### 3.2 Feature priority — MoSCoW / 功能优先级（MoSCoW）

| Feature / 功能 | Persona / 角色 | MoSCoW | Notes (En / 中文) |
|---|---|---|---|
| QR / band entry | Member | Must | Scan-to-open gate / 扫码开闸 |
| Class booking + waitlist | Member | Must | Real-time slots / 实时余位 |
| Payment & top-up | Member | Must | Local methods per market / 按市场本地支付 |
| Push consent center | Member | Must | HI-7 opt-in toggle / HI-7 同意开关 |
| Body-test trend chart | Member | Should | From MMS / 取自 MMS |
| Coach roster & check-in | Coach | Must | Sync MMS / 同步 MMS |
| PT session logging | Coach | Should | Commission link / 关联提成 |
| Day-pass issuance | Front desk | Should | Walk-in convert / 散客转化 |
| Social / leaderboard | Member | Could | Opt-in only (HI-7) / 仅 Opt-in |
| In-app live commerce | Member | Won't (now) | Later phase / 后续阶段 |

> **Red flag / 红旗**: "Could/Won't" slipping into Must inflates build cost and delays go-live. / 把 Could/Won't 混进 Must 会抬高成本拖上线。

### 3.3 Booking & payment flows / 约课与支付流程

**Booking flow / 约课流程**
1. Open app → tap Class → see real-time slots. / 开 App → 点课程 → 看实时余位。
2. Tap Book → MMS reserves seat (idempotent). / 点预约 → MMS 锁位（幂等）。
3. Waitlist auto-fill on cancel notifies next member. / 取消时候补自动补位并通知。
4. At club: scan QR at gate → access log written. / 到店扫码 → 写门禁日志。

**Payment flow / 支付流程**
1. Cart (membership / PT / retail) → choose local tender. / 购物车（会籍/私教/零售）→ 选本地支付方式。
2. Pay → webhook updates MMS ledger (idempotency key). / 支付 → webhook 更新 MMS 台账（幂等键）。
3. Receipt pushed + stored in MMS transaction log. / 推送小票并存 MMS 流水。
4. Refund → refund-to-source with reason code. / 退款 → 原路退含原因码。

### 3.4 Push / notification consent matrix (HI-7) / 推送同意矩阵（HI-7）

> **Rule / 规则**: Each row needs explicit opt-in before any send; quiet-hours per market enforced. / 每行发送前需明确 Opt-in；按市场执行静默时段。

| Channel / 通道 | Type / 类型 | Opt-in required? / 需同意? | Quiet-hours / 静默 | Legal basis / 依据 |
|---|---|---|---|---|
| Booking reminder / 约课提醒 | Transactional | No (contractual) / 否（合同内） | No / 否 | Contract / 合同 |
| Class cancel alert / 停课通知 | Transactional | No / 否 | No / 否 | Safety / 安全 |
| Promo blast / 促销群发 | Marketing | YES / 是 | Per market / 按市场 | HI-7 |
| Birthday offer / 生日礼 | Marketing | YES / 是 | Per market / 按市场 | HI-7 |
| Churn-winback / 流失挽回 | Marketing | YES / 是 | Per market / 按市场 | HI-7 |

> **Red flag / 红旗**: see `data/21#ap-011-ai-outbound-no-consent` and `data/21#ap-019-whatsapp-blast-cold` — sending marketing without consent is an anti-pattern and may breach anti-spam law. / 无同意发营销是反模式且可能违法（见锚点）。

### 3.5 App-store & mini-program submission checklist per market (🔄) / 分市场上架清单

:::dynamic-hook topic="apac-appstore-miniprogram-policy-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07: China needs ICP + mini-program subject verification; Apple App Store forbids forcing mini-program as app substitute and restricts IAP for digital goods; Japan/Korea use App Store + LINE/Kakao mini-program; SEA/ANZ use App Store/Play + regional wallets. Verify current policy via tools/04.
截至 2026-07：中国需 ICP+小程序主体核验；App Store 禁以小程序替代 App 并对数字商品限 IAP；日韩用 App Store+LINE/Kakao 小程序；东南亚/澳新用双商店+区域钱包。当前政策经 tools/04 核验。
:::

- [ ] China / 中国: ICP filing + WeChat/Alipay mini-program subject verification. / ICP 备案 + 微信/支付宝小程序主体核验。
- [ ] Apple App Store: no IAP bypass for digital goods; privacy nutrition label filled. / 数字商品不绕 IAP；填隐私营养标签。
- [ ] Google Play: data-safety form; restricted API declaration. / 数据安全表单；受限 API 申报。
- [ ] Japan / Korea: LINE/Kakao mini-program review + native app store listing. / LINE/Kakao 小程序审核 + 原生商店上架。
- [ ] Privacy policy URL + consent language in local language. / 隐私政策链接 + 本地语言同意文案。

### 3.6 Acceptance criteria / 验收标准

- [ ] Every Must feature passes UAT with real members (≥20 testers). / 每个 Must 功能经 ≥20 真实会员 UAT。
- [ ] Opt-out of marketing takes effect < 24h (HI-7). / 营销退订 <24h 生效。
- [ ] Entry works on offline QR when network drops. / 断网时离线二维码可入场。
- [ ] All data flows tag back to MMS (no orphan DB). / 所有数据回流 MMS（无孤儿库）。
- [ ] Crash-free session rate ≥ 99% in beta week. /  Beta 周无崩溃会话率 ≥99%。

---

### 3.7 Worked example (mini-program, China) / 实例（中国小程序）

- Market / 市场: China / 中国 → WeChat mini-program, ICP filed, subject verified. / 微信小程序，已 ICP 备案与主体核验。
- Must features shipped / 上线 Must: QR entry, booking + waitlist, payment (WeChat Pay), consent center. / 扫码入场、约课候补、支付（微信）、同意中心。
- Consent center / 同意中心: member toggles promo off → takes effect < 24h (HI-7). / 会员关促销 → <24h 生效。
- Result / 结果: front-desk walk-ins down 30%; zero spam complaints in 4-week beta. / 前台散客降 30%；4 周 Beta 零骚扰投诉。
- Lesson / 教训: skipping the consent center would have breached HI-7 on day one. / 教训：省掉同意中心首日即违反 HI-7。

## ④ Common mistakes (anti-patterns) / 常见错误（反模式）

- `data/21#ap-011-ai-outbound-no-consent` — outbound without consent. / 无同意外呼外推。
- `data/21#ap-019-whatsapp-blast-cold` — cold blast on WhatsApp. / WhatsApp 冷启动群发。
- `data/21#ap-023-untrained-system-promo` — promoting an app staff can't support. / 推一个员工不会用的 App。
- `data/21#ap-002-no-data-export` — app holds member data the operator cannot export. / App 持有运营者无法导出的会员数据。

---

## ⑤ Related files / 相关文件

- `references/06-software-landscape-apac-vendors.md` (§7) — app vs mini-program cost. / App 与小程序成本。
- `references/17-omnichannel-messaging.md` — channel & consent map. / 通道与同意图。
- `templates/09-mms-selection-scorecard.md` — MMS is the backing system. / MMS 是支撑系统。
- `tools/05-regulation-traceability-verification.md` — privacy & anti-spam per market. / 各市场隐私与反垃圾法。

---

## ⑥ G13 tri-perspective note / G13 三视角覆盖说明

This template serves **Architect** (MoSCoW + MMS-backed architecture), **Operator** (submission checklist + acceptance UAT), and **Member** (consent center, offline entry, data portability); the HI-7 consent matrix is the gate that protects the member from spam and the operator from anti-spam liability — no orphaned touchpoint.
本模板覆盖**架构师**（MoSCoW+ MMS 支撑架构）、**运营者**（上架清单+验收 UAT）、**会员**（同意中心、离线入场、数据可携）；HI-7 同意矩阵是保护会员免骚扰、保护运营者免违法的闸门——无孤儿触点。
