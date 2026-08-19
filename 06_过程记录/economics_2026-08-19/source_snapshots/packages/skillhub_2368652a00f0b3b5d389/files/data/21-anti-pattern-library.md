# Anti-Pattern Library / 反模式库

> **Cluster / 集群**: V (Skill meta-capabilities)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify vendor/legal/pricing facts every 180 days via `tools/04`; regulation-linked items must pass `tools/05` before citing.
> **Cross-references / 交叉引用**: SKILL.md (HI-1~HI-8, Clusters O/R/T/F/M), `data/20-micro-details-ledger.md`, `data/02-regulation-traceability-index.md`, `references/13-data-and-llm-engine.md`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.

---

## Preamble — Honesty Red Line / 前言·诚实红线

> The "failure story" sketches below are **archetypal patterns**, not claimed real cases. They describe the typical way an anti-pattern blows up in production, drawn from common industry experience, not from any specific named club or incident. Use them as cautionary patterns to pre-empt — never as citations of real events.
> 下列"翻车故事"均为**原型模式**，并非声称的真实案例。它们描述的是某类反模式在真实运营中"如何爆雷"的典型形态，来自行业常见经验，不指向任何具名场馆或事件。请将其视为用于提前防范的警示模式，而非真实事件引用。

> Every entry is bilingual (English first, Chinese below) and carries five parts: Anti-pattern / 反模式, Why tempting / 诱因为何, What actually happens / 实际后果, Correct pattern / 正确做法 (+ anchor), Severity / 严重度.
> 每条均为双语（英文在上、中文在下），含五部分：反模式、诱因为何、实际后果、正确做法（+锚点）、严重度。

> Severity legend / 严重度图例: 💀 fatal (club-ending / 关店级) · 🔥 costly (major money or trust loss / 重大资金或信任损失) · ⚠️ painful (chronic friction / 长期摩擦).

---

## Top-10 Deadliest Anti-Patterns / 十大最致命反模式

| # | Anti-pattern / 反模式 | Severity / 严重度 | Anchor / 锚点 |
|---|---|---|---|
| 1 | Coaches collect fees via personal QR / 教练用个人码收款 | 💀 | `#ap-001-coach-personal-qr` |
| 2 | Membership system with no data-export clause / 会员系统无导出条款 | 💀 | `#ap-002-no-data-export` |
| 3 | Face-entry with no non-biometric alternative / 人脸入场无替代 | 💀 | `#ap-005-face-entry-no-alt` |
| 4 | Cameras in changing rooms "for safety" / 更衣室装监控"为安全" | 💀 | `#ap-006-camera-changing-room` |
| 5 | IT integrations control the fire system / IT 联动控消防 | 💀 | `#ap-007-fire-system-it-control` |
| 6 | Card numbers stored in spreadsheets / 卡号存表格 | 💀 | `#ap-008-card-numbers-spreadsheet` |
| 7 | AI outbound calls without opt-in / DNC / AI 外呼无同意 | 💀 | `#ap-011-ai-outbound-no-consent` |
| 8 | Trust sensors over lifeguard for pool safety / 泳池信传感器不信人 | 💀 | `#ap-012-sensor-over-lifeguard` |
| 9 | Churn model auto-cancels memberships / 流失模型自动退会 | 💀 | `#ap-014-churn-autocancel` |
| 10 | Member-facing AI with no kill switch / 会员 AI 无熔断 | 💀 | `#ap-027-ai-no-kill-switch` |

---

## 1. Money, Funds & Fraud / 资金、预付与欺诈

### AP-001 Coaches collect class fees via personal QR / 教练用个人码收课费 {#ap-001-coach-personal-qr}

**Anti-pattern / 反模式**: Letting coaches receive class or top-up fees through their personal WeChat/Venmo-type QR instead of the club's merchant account. 让教练用个人微信/转账类二维码收课费或储值，而非进场馆商户号。

**Why tempting / 诱因为何**: It feels "convenient" — the coach is already on the phone with the member and "just collects it." 看起来"方便"——教练本就在跟会员聊，顺手就收了。

**What actually happens / 实际后果**: The coach leaves owing tens of thousands in "collected" fees never booked; members sue the club, which can't trace the money. 教练离职时欠着数万元"已收"费用从未入账；会员告场馆，场馆追不回钱。

**Correct pattern / 正确做法**: All member payments land only in the club's verified merchant account; coach devices are pay-NONE. 所有会员付款只进场馆认证商户号；教练设备零收款权限。 → `#md-035-personal-qr-topup` (PAY-05), SKILL.md HI-3.

**Severity / 严重度**: 💀 fatal.

### AP-002 Buy a membership system without a data-export clause / 会员系统无导出条款 {#ap-002-no-data-export}

**Anti-pattern / 反模式**: Signing the membership-SaaS contract with no data-export clause (format, timeline, cost). 签会员 SaaS 合同却无数据导出条款（格式/时限/费用）。

**Why tempting / 诱因为何**: The salesperson says "of course you can export anytime" — verbally — and you skip the paper. 销售口头说"当然随时能导出"，你便没写进纸面。

**What actually happens / 实际后果**: When you switch vendors, the old one quotes ¥80k + 60 days for export, or refuses; you're locked or pay the lock-in squeeze. 换供应商时旧的报"8万+60天"或干脆拒绝；你被锁死或付高额解锁费。

**Correct pattern / 正确做法**: Contractual export: CSV/API, ≤30 days, fixed/zero fee, signed before ink. 合同导出：CSV/API、≤30天、固定/零费用，签约前落字。 → `#md-108-no-export-clause` (VEN-08), SKILL.md Iron Law 8.

**Severity / 严重度**: 💀 fatal.

### AP-003 Do cabling only after renovation finishes / 装修完才布线 {#ap-003-cabling-after-renovation}

**Anti-pattern / 反模式**: Treating network/security cabling as a post-renovation afterthought instead of a rough-in during the build. 把网络/安防布线当成装修后的"补做"，而非施工期的预埋。

**Why tempting / 诱因为何**: Renovation budgets are tight; "we'll just run cables on the surface later" saves the rough-in cost now. 装修预算紧；"以后明装走线就行"省了当下预埋钱。

**What actually happens / 实际后果**: Surface cables get damaged by cleaners/equipment, look unprofessional, and a single severed line kills the gate for a day. 明装线被保洁/器械弄坏、观感差，一根断了就让闸机瘫一天。

**Correct pattern / 正确做法**: Conduit + rough-in during renovation; label both ends (see `#md-001-cable-label-both-ends`). 装修期就预埋线管+两端贴标（见 `#md-001`）。

**Severity / 严重度**: 🔥 costly.

### AP-004 Sell all prime-time slots to aggregator platforms / 把黄金时段全卖给聚合平台 {#ap-004-sell-prime-to-aggregator}

**Anti-pattern / 反模式**: Handing 100% of prime-time (evenings/weekends) to group-buy/aggregator platforms for quick cash. 把黄金时段（晚/周末）100% 卖给团购/聚合平台换快钱。

**Why tempting / 诱因为何**: Aggregators guarantee volume and fill classes instantly; the GM hits their acquisition number this quarter. 聚合平台保量、瞬间填满课；店长本季获客数字达标。

**What actually happens / 实际后果**: Your own members can't book prime time, churn, and the club becomes a discount shell of someone else's brand. 自家会员抢不到黄金时段而流失，场馆变成别人品牌的折扣壳。

**Correct pattern / 正确做法**: Cap aggregator share (e.g., ≤20% of prime slots); protect core-member access. 聚合占比设上限（如黄金时段≤20%）；保核心会员权益。 → SKILL.md Cluster W.

**Severity / 严重度**: 🔥 costly.

### AP-005 Run face-entry without a non-biometric alternative / 人脸入场无替代 {#ap-005-face-entry-no-alt}

**Anti-pattern / 反模式**: Deploying face-gate as the ONLY entry method, with no card/QR fallback. 只部署人脸闸机，无卡/码兜底。

**Why tempting / 诱因为何**: "Frictionless, members love it, and it looks high-tech." 「无感通行，会员爱用，还显科技感。」

**What actually happens / 实际后果**: A member with a medical mask/cast, a child, or a face-match failure is locked out publicly; biometric-only also breaches HI-1 in several markets. 戴口罩/打石膏的会员、儿童或识别失败者当众被拦；纯生物识别在多个市场还违反 HI-1。

**Correct pattern / 正确做法**: Face is convenience only; card/QR is the guaranteed path; explicit separate biometric consent. 人脸仅便民；卡/码为保底通路；生物识别单独明确同意。 → `#md-092-biometric-consent-separate` (CMP-04), SKILL.md HI-1.

**Severity / 严重度**: 💀 fatal.

### AP-006 Put cameras in changing areas "for safety" / 更衣室装监控"为安全" {#ap-006-camera-changing-room}

**Anti-pattern / 反模式**: Installing any imaging device in changing rooms/showers, rationalized as "member safety." 以"会员安全"为由在更衣室/淋浴区装任何影像设备。

**Why tempting / 诱因为何**: "We just want to prevent theft in the lockers." 「我们只是想防储物柜失窃。」

**What actually happens / 实际后果**: This is an absolute no-go (HI-5); discovery triggers a criminal-exposure investigation and possible club closure. 这是绝对禁区（HI-5）；一旦被发现触发刑事暴露调查，甚至可能关店。

**Correct pattern / 正确做法**: Zero optics in changing/shower zones; use non-imaging motion sensors if "safety" is needed. 更衣/淋浴区零光学设备；若需"安全"用非成像存在传感器。 → `#md-093-camera-changing-room` (CMP-05), SKILL.md HI-5.

**Severity / 严重度**: 💀 fatal.

### AP-007 Let the fire system be controlled by your IT integrations / IT 联动控消防 {#ap-007-fire-system-it-control}

**Anti-pattern / 反模式**: Wiring fire-safety devices so your business/IT systems can command them (e.g., IT closes a fire door, IT silences an alarm). 把消防设备接成可被业务/IT 系统指挥（如 IT 关门、IT 静音）。

**Why tempting / 诱因为何**: "One dashboard to rule them all" feels efficient for the facilities manager. 「一块大屏统管一切」对工程经理显得高效。

**What actually happens / 实际后果**: A software bug or cyber event disables a fire control; lives at risk — HI-4 hard red line. 软件 bug 或网络事件让消防控制失效；危及生命——踩 HI-4 硬红线。

**Correct pattern / 正确做法**: Fire integration is MONITOR-ONLY; business systems never command fire devices. 消防联动只监不控；业务系统绝不指挥消防设备。 → SKILL.md HI-4, `#md-013-exit-gate-fail-open` (FACILITY-13).

**Severity / 严重度**: 💀 fatal.

### AP-008 Store card numbers in spreadsheets / 卡号存表格 {#ap-008-card-numbers-spreadsheet}

**Anti-pattern / 反模式**: Keeping member credit-card numbers / CVV in Excel "for recurring billing." 为"循环扣费"把会员卡号/CVV 存进 Excel。

**Why tempting / 诱因为何**: The old billing tool can't tokenize; a sheet is the "quick fix." 旧扣费工具不能令牌化；表格是"快解"。

**What actually happens / 实际后果**: One leaked laptop = full PAN breach = PCI violation, fines, and member-trust collapse. 一台笔记本泄露=完整卡号外泄=PCI 违规、罚款、会员信任崩塌。

**Correct pattern / 正确做法**: Use a PCI-DSS tokenizing processor; never store PAN/CVV; you hold only a token. 用 PCI-DSS 令牌化收单；绝不存 PAN/CVV；你只持有令牌。 → SKILL.md Cluster R.

**Severity / 严重度**: 💀 fatal.

### AP-009 Use one shared admin login for all staff / 全员共用管理员账号 {#ap-009-shared-admin-login}

**Anti-pattern / 反模式**: Every staff member logs into the admin console as "admin / admin123." 全体员工用 "admin/admin123" 登管理后台。

**Why tempting / 诱因为何**: Faster onboarding, no license seats to manage. 入职快，还省账号许可。

**What actually happens / 实际后果**: A ¥5k fraudulent refund is pushed; the log shows only "admin" — no one is accountable, and the insurer rejects the claim. 一笔5千元欺诈退款发出；日志只显示"admin"——无人可责，保险拒赔。

**Correct pattern / 正确做法**: Per-user accounts with role-based access; every action attributable; SSO where possible. 按人建账号+角色权限；每动作可溯源；可行则用 SSO。 → `#md-038-refund-intern-login` (PAY-08), SKILL.md Cluster I.

**Severity / 严重度**: 🔥 costly.

### AP-010 Skip the UPS to save money / 为省钱不买 UPS {#ap-010-skip-ups}

**Anti-pattern / 反模式**: Running the network rack and gate controller straight off mains with no UPS "to save ¥2k." 网络机柜与闸机控制器直连市电，不配 UPS，"省两千块"。

**Why tempting / 诱因为何**: Power is "reliable enough"; the UPS line item gets cut in budgeting. 电"够稳"；预算里 UPS 这一项被砍。

**What actually happens / 实际后果**: A 4-hour neighborhood outage kills the gate on a Saturday; you manually buzz 400 members and lose a full day of revenue + trust. 周六片区停4小时，闸机死；你手动放行400人，赔掉一整天营收+信任。

**Correct pattern / 正确做法**: UPS sized for ≥ the longest realistic outage on battery-backed outlets only. UPS 按"最长合理断网"配，且只接电池后备口。 → `#md-006-ups-vs-surge-outlets` (FACILITY-06), `#md-003-server-closet-lock-temp` (FACILITY-03).

**Severity / 严重度**: 🔥 costly.

### AP-011 Launch AI outbound calls without opt-in and DNC checks / AI 外呼无同意 {#ap-011-ai-outbound-no-consent}

**Anti-pattern / 反模式**: Turning on an AI voice-bot that dials members for renewals without consent and without checking the Do-Not-Contact list. 上线 AI 语音机器人给会员打续费电话，既无同意也不查免联系名单。

**Why tempting / 诱因为何**: "It's just a reminder call, not really marketing." 「这只是提醒电话，不算营销。」

**What actually happens / 实际后果**: The bot calls an opted-out member who records it and files a spam complaint; regulator fines and kills the campaign — HI-7 violation. 机器人打给已退订会员，对方录音并向监管举报；被罚款且活动腰斩——违反 HI-7。

**Correct pattern / 正确做法**: Pre-dial DNC + consent gate; log every call; human-supervised. 拨前查免联系+同意闸门；记每通电话；人工监督。 → `#md-085-voicebot-no-dnc` (AI-09), SKILL.md HI-7.

**Severity / 严重度**: 💀 fatal.

### AP-012 Trust sensor readings over lifeguard / manual checks for pool safety / 泳池信传感器不信人 {#ap-012-sensor-over-lifeguard}

**Anti-pattern / 反模式**: Relying on CV/water sensors alone for drowning detection and removing the human lifeguard. 防溺水只靠 CV/水感传感器，撤掉人工救生员。

**Why tempting / 诱因为何**: "24h unmanned pool saves payroll" and the AI demo looked impressive. 「24h 无人泳池省人力」，且 AI demo 看着唬人。

**What actually happens / 实际后果**: The model misses a rare pose; a drowning goes undetected — HI-2 life-safety violation and tragedy. 模型漏掉罕见姿态；溺水未被发现——违反 HI-2 人身安全，酿成悲剧。

**Correct pattern / 正确做法**: AI is a SECONDARY alarm only; a human lifeguard is mandatory on duty; fail-safe design. AI 仅作次级告警；救生员在岗强制；故障安全设计。 → `#md-131-pool-ai-over-lifeguard` (POOL-03), SKILL.md HI-2.

**Severity / 严重度**: 💀 fatal.

### AP-014 Let the churn model auto-cancel memberships / 流失模型自动退会 {#ap-014-churn-autocancel}

**Anti-pattern / 反模式**: Wiring the churn-prediction model to automatically cancel or freeze "high-risk" members to "save ops cost." 把流失预测模型接成自动取消/冻结"高风险"会员以"省运营成本"。

**Why tempting / 诱因为何**: "Why pay to keep members who'll leave anyway?" 「何必留那些反正要走的会员？」

**What actually happens / 实际后果**: A model glitch flags 300 loyal members as churn; they're auto-cancelled overnight; lawsuits + brand ruin. 模型故障把300名忠诚会员标为流失；一夜之间被自动退会；诉讼+品牌毁灭。

**Correct pattern / 正确做法**: Churn model only TRIGGERS a human-led save-play; never auto-terminates a membership. 流失模型只"触发"人工挽留动作；绝不自动终止会籍。 → `#md-077-churn-promo-retrain` (AI-01), SKILL.md Cluster E.

**Severity / 严重度**: 💀 fatal.

### AP-015 Prepay 3+ years of SaaS for a discount before a pilot / 试点前预付3年SaaS {#ap-015-prepaid-3yr-saas}

**Anti-pattern / 反模式**: Paying 3+ years upfront for a "discount" on a system you haven't piloted. 为折扣把未试点的系统预付3年以上。

**Why tempting / 诱因为何**: The discount is large (e.g., 40% off) and the CFO likes the one-time saving. 折扣大（如4折），CFO 喜欢一次性省。

**What actually happens / 实际后果**: After 4 months it doesn't fit; you're stuck with 32 non-refundable months and a tool nobody uses. 4个月后证明不适配；被32个月预付绑死且工具无人用。

**Correct pattern / 正确做法**: Pilot first; cap prepay at 12 months until proven; review clause. 先试点；证实前预付封顶12个月；留复核条款。 → `#md-104-prepaid-3yr-pre-pilot` (VEN-04), SKILL.md Iron Law 8.

**Severity / 严重度**: 🔥 costly.

### AP-017 Give the marketing agency direct database access / 给营销代理直达数据库 {#ap-017-agency-db-access}

**Anti-pattern / 反模式**: Handing the external marketing agency read/write access to the live member database "so they can run campaigns." 把外部营销代理对会员生产库的读写权限"方便他们做活动"。

**Why tempting / 诱因为何**: "They need the data to target; exporting per-list is slow." 「他们要数据才能定向；每次导表太慢。」

**What actually happens / 实际后果**: The agency's weak credentials leak; 50k member records hit the dark web; PDPA/PIPL breach + class action. 代理弱口令泄露；5万会员记录上暗网；PIPL/PDPA 违规+集体诉讼。

**Correct pattern / 正确做法**: Agency gets a scoped, tokenized, read-only API per campaign; no raw DB; DPA signed. 代理只拿按活动限定、令牌化、只读 API；无原始库直连；签 DPA。 → `#md-081-ai-pii-prompt-store` (AI-05), SKILL.md HI-8.

**Severity / 严重度**: 💀 fatal.

### AP-025 Let BNPL chargebacks surprise finance / BNPL 拒付吓坏财务 {#ap-025-bnpl-chargeback-surprise}

**Anti-pattern / 反模式**: Offering buy-now-pay-later without modeling default risk into the P&L. 上线先买后付却不把违约风险建模进利润表。

**Why tempting / 诱因为何**: BNPL inflates top-line sales immediately and looks like growth. BNPL 立刻吹大营收，看着像增长。

**What actually happens / 实际后果**: Chargebacks land 6–9 months later with no reserve; a profitable quarter flips to a loss. 拒付在6–9个月后无准备地到来；盈利季翻成亏损。

**Correct pattern / 正确做法**: Reserve BNPL defaults as contra-revenue; report deferred + risk together. 把 BNPL 违约计提为收入备抵；递延与风险合并报。 → `#md-113-bnpl-chargeback-surprise` (FIN-03), SKILL.md HI-3.

**Severity / 严重度**: 🔥 costly.

### AP-026 A/B test pricing on existing members carelessly / 对老会员乱做价格A/B {#ap-026-ab-price-test-members}

**Anti-pattern / 反模式**: Running price A/B tests by showing different renewal prices to existing members without care. 对现有会员展示不同续费价做价格 A/B，毫不谨慎。

**Why tempting / 诱因为何**: "We can optimize price with a quick experiment." 「快速实验就能优化定价。」

**What actually happens / 实际后果**: Members compare screenshots in the group chat; "you charged me more" fury; trust damage that outlasts the test. 会员在群里对截图；"你对我收更贵"的暴怒；信任损伤久过实验本身。

**Correct pattern / 正确做法**: Test pricing only on NEW cohorts or geo-segmented prospects; never split existing members. 价格测试只对新客群或地理分群；绝不拆现有会员。 → SKILL.md Cluster W.

**Severity / 严重度**: 🔥 costly.

### AP-032 Refund cash for a digital payment / 数字支付发现金退款 {#ap-032-cash-refund-digital}

**Anti-pattern / 反模式**: Refunding a WeChat/Alipay/card payment in cash. 把微信/支付宝/银行卡付款用现金退。

**Why tempting / 诱因为何**: "The member is here, just give them cash and close the ticket." 「会员在眼前，直接发现金销单。」

**What actually happens / 实际后果**: The member disputes the original charge with the bank AND keeps your cash — you lose twice; acquirer fines you. 会员就原卡交易发起争议又拿了你的现金——赔两次；收单机构罚款。

**Correct pattern / 正确做法**: Refunds only to the original method; system-enforced, no cash button. 仅原路退；系统强制，禁用现金退款按钮。 → `#md-032-no-cash-refund-digital` (PAY-02), SKILL.md HI-3.

**Severity / 严重度**: 💀 fatal.

### AP-041 Mix prepaid member funds with the operating account / 预付金混进运营户 {#ap-041-prepaid-mixed-account}

**Anti-pattern / 反模式**: Parking prepaid member funds in the same operating account as daily revenue. 把会员预付金与日常营收放在同一运营账户。

**Why tempting / 诱因为何**: "It's all our money anyway; simpler to keep together." 「反正都是我们的钱，放一起省事。」

**What actually happens / 实际后果**: You spend prepaid funds on payroll; a dip in new sales leaves you unable to refund — fund-supervision violation + insolvency scandal. 你把预付金挪发工资；新售下滑后无力退款——违反资金监管+破产丑闻。

**Correct pattern / 正确做法**: Segregated supervised account; reconcile to the deferred schedule regularly. 隔离监管账户；定期与递延排程对账。 → `#md-118-prepaid-mixed-account` (FIN-08), SKILL.md HI-3.

**Severity / 严重度**: 💀 fatal.

---

## 2. Systems, Data & Architecture / 系统、数据与架构

### AP-013 Migrate systems during peak season / 旺季做系统迁移 {#ap-013-migrate-peak}

**Anti-pattern / 反模式**: Scheduling the membership/CRM migration for December–January (peak season) to "get it done." 把会员/CRM 迁移排到12–1月（旺季）"一口气做完"。

**Why tempting / 诱因为何**: "We'll have more staff over the holidays to help." 「假期人多好帮忙。」

**What actually happens / 实际后果**: A data-mapping bug blocks check-ins on January 2; the year's biggest week is a front-desk nightmare. 数据映射 bug 在1月2日卡住签到；全年最大周变成前台噩梦。

**Correct pattern / 正确做法**: Migrate in the lowest-traffic window; parallel-run; keep the old system warm. 在最低谷窗口迁移；并行运行；旧系统保温。 → `#md-042-bank-change-no-dr` (PAY-12), SKILL.md Iron Law 5.

**Severity / 严重度**: 🔥 costly.

### AP-020 Treat "the vendor demo worked" as acceptance / 把demo当验收 {#ap-020-demo-not-acceptance}

**Anti-pattern / 反模式**: Signing off the project because "the demo looked great" instead of a production-scale UAT. 因"demo 很棒"就签字验收，而非做生产级 UAT。

**Why tempting / 诱因为何**: The demo was smooth and everyone wants to go live. demo 流畅，大家都想上线。

**What actually happens / 实际后果**: On your 8k-member load the "instant" search takes 9s; adoption fails and blame lands on the club. 在你8千会员负载下"秒搜"变9秒；采纳失败，锅甩给场馆。

**Correct pattern / 正确做法**: UAT on production-scale data + real devices; measure latency/throughput SLAs before sign-off. 用生产级数据+真机做 UAT；签字前测延迟/吞吐 SLA。 → `#md-101-demo-faster-than-prod` (VEN-01).

**Severity / 严重度**: 🔥 costly.

### AP-021 Skip restore tests ("backup theater") / 只备份不演练 {#ap-021-backup-theater}

**Anti-pattern / 反模式**: Backing up nightly but never restoring, assuming "the backup exists so we're safe." 每晚备份却从不恢复，以为"备份在就安全"。

**Why tempting / 诱因为何**: Backups run green; nobody wants to spend a weekend on a restore drill. 备份跑得全绿；没人愿周末做恢复演练。

**What actually happens / 实际后果**: The DB corrupts; the "backup" is silently incomplete; you lose a month of member data. 库损坏；"备份"其实悄悄不全；丢了一个月会员数据。

**Correct pattern / 正确做法**: Quarterly restore drill to a sandbox; verify row counts + spot-check records. 每季度恢复到沙箱演练；核对行数+抽査记录。 → SKILL.md Cluster K.

**Severity / 严重度**: 💀 fatal.

### AP-022 Digitize a broken process / 把坏流程数字化 {#ap-022-digitize-broken-process}

**Anti-pattern / 反模式**: Automating a chaotic, undocumented workflow 1:1 instead of fixing it first. 先把混乱、无文档的流程1:1自动化，而非先修。

**Why tempting / 诱因为何**: "Software will enforce discipline for us." 「软件会替我们立规矩。」

**What actually happens / 实际后果**: You get "garbage in, faster garbage out" — the system just makes the chaos scale and auditable-as-broken. 结果是"垃圾进、更快垃圾出"——系统只是让混乱规模化且可被追责为混乱。

**Correct pattern / 正确做法**: Map + simplify the process on paper/Excel first; then digitize the improved version. 先在纸/Excel 上梳理并简化流程；再数字化改进版。 → SKILL.md Iron Law 5 (stage-gate).

**Severity / 严重度**: ⚠️ painful.

### AP-023 Install a system the front desk wasn't trained on, week of a promo / 促销周上新系统前台没训 {#ap-023-untrained-system-promo}

**Anti-pattern / 反模式**: Go-live on new POS/CRM the same week as a big acquisition promo, with no staff training. 大促获客周同时上新 POS/CRM，员工没培训。

**Why tempting / 诱因为何**: "The promo drives traffic; we'll learn on the job." 「促销带客流；边干边学。」

**What actually happens / 实际后果**: Front-desk fumbles every check-in; the promo's flood of new members gets a broken first impression and churns. 前台每个签到都卡；促销涌来的新会员首印象崩坏而流失。

**Correct pattern / 正确做法**: Train + dry-run 2 weeks before any promo; hold the launch if training slips. 大促前2周培训+空跑；培训没到位就推迟上线。 → SKILL.md Cluster L1.

**Severity / 严重度**: 🔥 costly.

### AP-024 Ignore the offboarding checklist (ex-staff still had gate access) / 忽视离职清单（前员工仍有门禁） {#ap-024-offboarding-checklist}

**Anti-pattern / 反模式**: Letting staff leave without revoking app/gate/credential access the same day. 员工离职当天不撤销 App/闸机/凭证访问。

**Why tempting / 诱因为何**: "They were a good employee; we'll clean up next week." 「他是个好员工；下周再清理。」

**What actually happens / 实际后果**: The ex-staff member's app still opens the back gate; they enter at night "to collect things" — theft + liability. 前员工 App 仍能开后门；夜里进来"拿东西"——盗窃+责任。

**Correct pattern / 正确做法**: Same-day revoke of ALL digital + physical access; signed offboarding checklist. 当日撤销全部数字+实体访问；离职清单签字。 → `#md-128-offboarding-gate-access` (UNM-10), `#md-011-spare-key-orphan` (FACILITY-11).

**Severity / 严重度**: 💀 fatal.

### AP-028 Put the only NVR backhaul on Wi-Fi / 录像机只走Wi-Fi回传 {#ap-028-nvr-wifi-backhaul}

**Anti-pattern / 反模式**: Backhauling security cameras over Wi-Fi as the only path. 安防摄像头只走 Wi-Fi 回传，别无他路。

**Why tempting / 诱因为何**: "Running cable to the roof is expensive; Wi-Fi is fine." 「拉线到顶贵；Wi-Fi 就行。」

**What actually happens / 实际后果**: An AP reboot during a break-in drops all footage exactly when you need it; insurance denies the claim. AP 在破门时重启，恰好丢光录像；保险拒赔。

**Correct pattern / 正确做法**: PoE wired backbone for cameras; Wi-Fi only as redundant. 摄像头用 PoE 有线主干；Wi-Fi 仅冗余。 → `#md-124-wifi-only-camera-backhaul` (UNM-06).

**Severity / 严重度**: 🔥 costly.

### AP-029 Auto-delete inactive members with no archive / 无归档自动删沉默会员 {#ap-029-autodelete-inactive}

**Anti-pattern / 反模式**: A script that hard-deletes "inactive >2yr" members. 脚本硬删"沉默超2年"会员。

**Why tempting / 诱因为何**: "Old records bloat the DB and GDPR says minimize." 「旧记录撑大库，且法规说最小化。」

**What actually happens / 实际后果**: A 3-year consumer dispute arrives; the member was purged and you can't defend — unlawful deletion penalty. 三年后消费争议来了；会员已被删，你无法自证——违法删除被罚。

**Correct pattern / 正确做法**: Anonymize, don't delete; keep a frozen archive per the retention schedule. 做匿名化而非删除；按留存期留冻结归档。 → `#md-050-inactive-autodelete` (MEM-08), SKILL.md HI-8.

**Severity / 严重度**: 🔥 costly.

### AP-030 Make face-match the ONLY gate path / 把人脸当唯一闸机通路 {#ap-030-face-only-gate}

**Anti-pattern / 反模式**: Configuring the gate so a failed face-match hard-blocks entry with no card/QR escape. 把闸机配成"人脸失败即硬拦"，无卡/码退路。

**Why tempting / 诱因为何**: "Face is the future; cards are legacy." 「人脸是未来；卡是过时的。」

**What actually happens / 实际后果**: A 5-year member with a 5-year-old photo is falsely rejected in front of a queue; public argument, trust hit, and a HI-1 exposure. 照片5年没更新的老会员在队伍前被误拒；当众争执、信任受损，还踩 HI-1。

**Correct pattern / 正确做法**: Always a non-biometric fallback; refresh photos; desk override with logging. 永远有非生物识别兜底；刷新照片；前台可留痕放行。 → `#md-026-crm-photo-stale` (GATES-08), SKILL.md HI-1.

**Severity / 严重度**: 💀 fatal.

### AP-042 Use phone number as the unique member ID / 用手机号当唯一会员ID {#ap-042-phone-as-unique-id}

**Anti-pattern / 反模式**: Keying the member record on the mobile number as the primary key. 用手机号作主键锁会员档案。

**Why tempting / 诱因为何**: "Everyone has a phone; it's the natural ID." 「人人有手机；天然就是ID。」

**What actually happens / 实际后果**: Two sisters share a number; one's check-ins merge into the other's attendance and churn score — analytics and billing both corrupt. 两姐妹共用号；一人打卡并入了另一人的出勤与流失分——分析与账单双双失真。

**Correct pattern / 正确做法**: System-assigned member_id is the key; phone is an attribute; allow multi-member per phone. 系统分配 member_id 作主键；手机只是属性；同号允许多会员。 → `#md-043-phone-not-unique` (MEM-01).

**Severity / 严重度**: 🔥 costly.

### AP-043 Train the churn model on a promo month / 用促销月训练流失模型 {#ap-043-churn-train-promo}

**Anti-pattern / 反模式**: Retraining the churn model on a month that had a huge acquisition promo. 在含大额获客促销的月份重训流失模型。

**Why tempting / 诱因为何**: "Use the most recent data; it's the most relevant." 「用最近的数据，最相关。」

**What actually happens / 实际后果**: The model bakes promo behavior in as "normal"; post-promo it flags 40% of new members as high-churn and you discount them all — margin evaporates. 模型把促销行为学成"正常"；促销后把40%新会员标高流失，你全给打折——利润蒸发。

**Correct pattern / 正确做法**: Tag promo cohorts; train only on steady-state windows; backtest on a clean holdout. 给促销群打标；只在稳态窗口训练；干净留存集回测。 → `#md-077-churn-promo-retrain` (AI-01).

**Severity / 严重度**: 🔥 costly.

### AP-044 Let the chatbot loop without handoff / 机器人死循环不转人工 {#ap-044-bot-no-handoff}

**Anti-pattern / 反模式**: A member-facing bot that endlessly asks "please elaborate" instead of escalating. 面向会员的机器人不停问"请详述"而不升级。

**Why tempting / 诱因为何**: "Automation should resolve everything to save labor." 「自动化该包揽一切以省人力。」

**What actually happens / 实际后果**: A member asks about a refund 5 times, the bot repeats, they rage-quit and don't renew. 会员问退款5次，机器人复读，他气到退出且不续费。

**Correct pattern / 正确做法**: Escalate to human after 2 fails or <0.6 confidence, with context. 2次失败或置信<0.6即带上下文转人工。 → `#md-078-bot-handoff-2fails` (AI-02).

**Severity / 严重度**: ⚠️ painful.

### AP-048 Assume an "unlimited" plan is truly unlimited / 以为"无限"真无限 {#ap-048-unlimited-not-unlimited}

**Anti-pattern / 反模式**: Buying "unlimited" SMS/API/push and sending at will, ignoring fair-use clauses. 买"无限"短信/API/推送便随意发，无视公平使用条款。

**Why tempting / 诱因为何**: The word "unlimited" is on the price sheet. 价目表上写着"无限"。

**What actually happens / 实际后果**: Your promo sends 200k messages; the plan throttles to 1k/hr; the campaign dies mid-launch. 促销发20万条；套餐限到1千/时；活动在半路死掉。

**Correct pattern / 正确做法**: Negotiate a committed throughput in writing; model at 3× volume. 书面谈下承诺吞吐；按3倍量建模。 → `#md-102-unlimited-fairuse` (VEN-02), `#md-018-promo-no-headroom` (see AP-018).

**Severity / 严重度**: 🔥 costly.

### AP-049 Ship sandbox API keys to production / 把沙箱密钥上生产 {#ap-049-sandbox-keys-prod}

**Anti-pattern / 反模式**: Deploying with test/sandbox API keys still in the production config. 生产配置里还留着测试/沙箱 API 密钥就上线。

**Why tempting / 诱因为何**: "It's just a key; we'll swap it later." 「只是个密钥，以后换。」

**What actually happens / 实际后果**: Messages "send" but nobody receives for a week — silent failure, unnoticed until a member asks. 消息"已发"却无人收到，持续一周——静默失败，会员来问才发现。

**Correct pattern / 正确做法**: Separate keys per env; deploy fails if prod uses a sandbox key; post-deploy smoke test. 按环境分密钥；生产用沙箱密钥则发布失败；发布后冒烟测。 → `#md-103-sandbox-keys-prod` (VEN-03).

**Severity / 严重度**: 💀 fatal.

---

## 3. Compliance, Privacy & Safety / 合规、隐私与安全

### AP-034 Let the bot answer medical / injury questions / 让机器人答医疗问题 {#ap-034-bot-medical-answer}

**Anti-pattern / 反模式**: Allowing the AI coach/bot to diagnose injuries or give medical advice. 让 AI 教练/机器人诊断伤情或给医疗建议。

**Why tempting / 诱因为何**: "Members ask health questions; the bot should help." 「会员问健康，机器人该帮。」

**What actually happens / 实际后果**: A member asks about knee pain; the bot says "light squats are fine"; they injure further and sue — HI-6 violation. 会员问膝盖疼；机器人说"轻蹲没事"；伤加重并起诉——违反 HI-6。

**Correct pattern / 正确做法**: Detect medical intent → "consult a qualified professional" + disclaimer, never advice. 识别医疗意图→回"请咨询专业人士"+免责，绝不给建议。 → `#md-079-ai-no-medical` (AI-03), SKILL.md HI-6.

**Severity / 严重度**: 💀 fatal.

### AP-035 Let AI set pricing autonomously with no floor / AI 自主定价无下限 {#ap-035-ai-autonomous-pricing}

**Anti-pattern / 反模式**: An autonomous promo/pricing bot that can fire deep discounts with no human floor. 自主促销/定价机器人能打深折，无人工下限。

**Why tempting / 诱因为何**: "AI will optimize revenue better than us." 「AI 比我们更会优化营收。」

**What actually happens / 实际后果**: The bot drops New-Year premium slots to 50% "to fill" a 95%-full window; ¥200k margin lost in a weekend. 机器人把本已95%满的元旦 premium 时段打到5折"填满"；一个周末亏20万毛利。

**Correct pattern / 正确做法**: Discount floor + holiday blackout list + kill switch; human approval above floor. 折扣下限+假日禁促清单+熔断；超下限须人工批。 → `#md-088-smart-pricing-holiday` (AI-12), AP-027.

**Severity / 严重度**: 💀 fatal.

### AP-036 Leak PII into a third-party LLM prompt store / 把PII泄进第三方LLM库 {#ap-036-pii-llm-prompt-store}

**Anti-pattern / 反模式**: Feeding member names/health notes into a third-party LLM prompt store unredacted. 把会员姓名/健康备注未脱敏地喂进第三方 LLM 提示库。

**Why tempting / 诱因为何**: "The bot needs context to help the member." 「机器人需要上下文才能帮会员。」

**What actually happens / 实际后果**: A support bot logs "Member Zhang, knee surgery, wants refund" to the vendor's store — cross-border PII breach finding. 客服机器人把"会员张，膝盖手术，要退款"记进供应商库——跨境 PII 泄露认定。

**Correct pattern / 正确做法**: Pseudonymize IDs; strip free-text health before any external call; self-host where possible. 假名化 ID；外呼前剥离健康自由文本；可行则自托管。 → `#md-081-ai-pii-prompt-store` (AI-05), SKILL.md HI-8.

**Severity / 严重度**: 💀 fatal.

### AP-037 Leave the spare server-closet key with an ex-staff member / 备用机房钥匙留前员工 {#ap-037-spare-key-ex-staff}

**Anti-pattern / 反模式**: Never recovering the only spare closet key from a departed manager. 离职经理手里的唯一备用机房钥匙从不收回。

**Why tempting / 诱因为何**: "He returned his badge; the key is probably fine." 「工牌还了；钥匙应该没事。」

**What actually happens / 实际后果**: The ex-staff enters at night and reboots the NVR "as a prank" — an inside job you enabled. 前员工夜里进来把录像机"当恶作剧"重启——你亲手留的内鬼通道。

**Correct pattern / 正确做法**: Rekey on every offboarding; log physical keys like credentials; prefer electronic revocable locks. 每次离职换锁芯；实体钥匙按凭证登记；优先可撤销电子锁。 → `#md-011-spare-key-orphan` (FACILITY-11), AP-024.

**Severity / 严重度**: 💀 fatal.

### AP-038 Skip monthly deferred-revenue reconciliation / 漏做月度递延对账 {#ap-038-deferred-no-reconcile}

**Anti-pattern / 反模式**: Keeping deferred revenue in a spreadsheet that never reconciles with the membership system. 递延收入只留表格，从不与会员系统对账。

**Why tempting / 诱因为何**: "The numbers are close enough; month-end is busy." 「数字差不多；月底忙。」

**What actually happens / 实际后果**: Year-end shows ¥300k off vs the MMS; the auditor flags a material misstatement and penalties follow. 年末与会员系统差30万；审计标定重大错报并罚款。

**Correct pattern / 正确做法**: Monthly auto-reconcile; alert on >0.5% variance; system of record drives the schedule. 每月自动对账；差异>0.5%即告警；以源系统驱动排程。 → `#md-111-deferred-revenue-reconcile` (FIN-01).

**Severity / 严重度**: 🔥 costly.

### AP-039 Configure the refund policy AFTER the first request / 首个退款后才配政策 {#ap-039-refund-policy-late}

**Anti-pattern / 反模式**: Having no refund logic in the system until a member actually asks for one. 系统里毫无退款逻辑，直到真有会员来要退。

**Why tempting / 诱因为何**: "We'll handle refunds case by case." 「退款我们case by case 处理。」

**What actually happens / 实际后果**: The first big refund gets two different answers from two staff; the member records both and complains of unfairness. 首笔大额退款两员工给两种说法；会员录下并投诉不公。

**Correct pattern / 正确做法**: Pre-load the refund policy in the system before go-live; train staff; log overrides. 上线前把退款政策配进系统；培训员工；覆盖留痕。 → `#md-112-refund-policy-preloaded` (FIN-02).

**Severity / 严重度**: 🔥 costly.

### AP-040 Run e-KYC-only unmanned entry with no fallback / 无人店只靠e-KYC无兜底 {#ap-040-ekyc-no-fallback}

**Anti-pattern / 反模式**: An unmanned club whose ONLY entry is e-KYC, with no manual fallback for foreigners/edge cases. 无人场馆唯一入场方式是 e-KYC，外籍/边缘情形毫无兜底。

**Why tempting / 诱因为何**: "e-KYC is instant and needs no staff." 「e-KYC 秒过且无需员工。」

**What actually happens / 实际后果**: A tourist fails e-KYC at 11pm; the unmanned club denies entry with no human to help — bad review, lost sale, accessibility issue. 游客晚11点过不了 e-KYC；无人场馆拒入且无人可求助——差评+丢单+无障碍问题。

**Correct pattern / 正确做法**: Manual fallback (staff video-verify / pre-clear) for e-KYC failures; log exceptions. e-KYC 失败有手动兜底（员工视频核/预先放行）；记异常。 → `#md-119-ekyc-foreign-fallback` (UNM-01), SKILL.md HI-1.

**Severity / 严重度**: 💀 fatal.

### AP-045 Post class recordings with minors, no consent / 无同意发含未成年人课程录像 {#ap-045-class-recording-minors}

**Anti-pattern / 反模式**: Publishing class livestreams/recordings that include minors without parental consent. 发布含未成年人的课程直播/录像，无家长同意。

**Why tempting / 诱因为何**: "It's great marketing content; the kids are just in the background." 「是很棒的营销素材；孩子只在背景里。」

**What actually happens / 实际后果**: A parent spots their child in a public video; regulatory complaint; possible takedown + fine — HI-1/HI-5 exposure. 家长看到孩子出现在公开视频；监管投诉；可能下架+罚款——踩 HI-1/HI-5。

**Correct pattern / 正确做法**: Minor-exclusion policy in the filming SOP; written guardian consent per minor. 拍摄 SOP 含未成年人排除政策；每位监护人单独书面同意。 → `#md-075-class-recording-minors` (CLS-09), SKILL.md HI-1/HI-5.

**Severity / 严重度**: 💀 fatal.

### AP-046 Aim a security camera at the public street without signage / 监控无标识对准公共街道 {#ap-046-camera-public-street}

**Anti-pattern / 反模式**: Pointing an externally-facing camera so it sweeps passers-by on a public street, with no notice. 把朝外摄像头瞄到扫到公共街道路人，且无告知。

**Why tempting / 诱因为何**: "We just want to cover our own entrance." 「我们只想覆盖自家入口。」

**What actually happens / 实际后果**: A neighbor complains of mass surveillance; regulator orders re-aim and signage; community friction. 邻居投诉大规模监控；监管令调角+贴标识；社区摩擦。

**Correct pattern / 正确做法**: Narrow FOV on your entrance only; post public CCTV signage; document rationale. 视角只收窄对准自家入口；贴公共监控标识；记录理由。 → `#md-099-camera-public-street` (CMP-11).

**Severity / 严重度**: ⚠️ painful.

### AP-047 Bundle biometric consent inside the general T&Cs / 生物识别同意埋进总条款 {#ap-047-biometric-consent-bundled}

**Anti-pattern / 反模式**: Hiding face/vein/fingerprint consent inside the general signup terms instead of a separate opt-in. 把人脸/静脉/指纹同意埋进注册总条款，而非独立 opt-in。

**Why tempting / 诱因为何**: "One checkbox is simpler for the member." 「一个勾选框对会员更简单。」

**What actually happens / 实际后果**: A member objects; the regulator says the consent is invalid; you're forced to re-consent and may be fined — HI-1 breach. 会员反对；监管认定同意无效；被迫重新征同意并可能罚款——违反 HI-1。

**Correct pattern / 正确做法**: Standalone explicit biometric opt-in + non-biometric alternative always offered. 独立明确生物识别 opt-in，且永远提供非生物识别替代。 → `#md-092-biometric-consent-separate` (CMP-04), SKILL.md HI-1.

**Severity / 严重度**: 💀 fatal.

### AP-050 Blast WhatsApp without a working unsubscribe / WhatsApp无可用退订就群发 {#ap-050-whatsapp-no-unsubscribe}

**Anti-pattern / 反模式**: Sending a WhatsApp campaign whose unsubscribe link is dead or untested. 发 WhatsApp 活动，退订链接却是死链或未测过。

**Why tempting / 诱因为何**: "We'll fix the link after; the send is time-sensitive." 「链接事后修；发送赶时间。」

**What actually happens / 实际后果**: 20k messages go out; the link 404s; members report spam en masse; sender reputation dies overnight — HI-7. 发2万条；链接404；会员集体举报垃圾；发送信誉一夜归零——违反 HI-7。

**Correct pattern / 正确做法**: Pre-send checklist includes clicking the unsub link on 3 devices; monitor unsub latency <5 min. 发前清单含在3种设备点过退订；监控退订生效<5分钟。 → `#md-058-unsubscribe-pre-send` (MSG-04), SKILL.md HI-7.

**Severity / 严重度**: 💀 fatal.

### AP-051 Let the AI trainer auto-prescribe load progressions / AI私教自动开负荷 {#ap-051-ai-trainer-load}

**Anti-pattern / 反模式**: An AI posture coach that also "recommends" weight increases, pushing unsafe loads. 只做姿态提示的 AI 私教却又"建议"加重，推不安全负荷。

**Why tempting / 诱因为何**: "Personalized progression sells the product." 「个性化进阶才好卖。」

**What actually happens / 实际后果**: The AI tells a member with poor form to "add 5kg"; they injure a shoulder — HI-2/HI-6 liability. AI 对姿态差者说"加5公斤"；肩伤——违反 HI-2/HI-6 担责。

**Correct pattern / 正确做法**: Constrain AI to form cues only; flag "consult coach" for any progression; human-in-loop. 限制 AI 只做姿态提示；进阶标"请咨询教练"；人在回路。 → `#md-082-ai-trainer-load` (AI-06), SKILL.md HI-2/HI-6.

**Severity / 严重度**: 💀 fatal.

### AP-055 Log member MAC addresses on "free WiFi" without notice / 免费WiFi无告知记MAC {#ap-055-wifi-mac-no-notice}

**Anti-pattern / 反模式**: A captive-portal WiFi that silently fingerprints every device's MAC with no notice or consent. 捕获门户 WiFi 在会员无告知无同意下静默给每台设备建档（MAC）。

**Why tempting / 诱因为何**: "We just need to manage bandwidth; it's harmless." 「我们只是要管带宽；无害。」

**What actually happens / 实际后果**: A privacy researcher flags covert tracking; bad press and a HI-8 minimization breach. 隐私研究者曝光隐性追踪；负面舆情+违反 HI-8 最小化。

**Correct pattern / 正确做法**: Consent screen on connect; log session only, not perpetual MAC; delete on disconnect. 连接时 consent 屏；只记会话不永久存 MAC；断开即删。 → `#md-100-wifi-mac-logging` (CMP-12), SKILL.md HI-8.

**Severity / 严重度**: ⚠️ painful.

---

## 4. Operations, Scheduling & Physical Safety / 运营、排期与物理安全

### AP-018 Run promos without rate-limit headroom / 无速率余量就做促销 {#ap-018-promo-no-headroom}

**Anti-pattern / 反模式**: Launching a big campaign without confirming the messaging/API/network can handle the peak send rate. 大活动上线前不确认消息/API/网络能否扛峰值发送率。

**Why tempting / 诱因为何**: "The platform says unlimited; we're good." 「平台说无限；稳了。」

**What actually happens / 实际后果**: The send throttles mid-campaign; half the members never get the offer; the promo flops. 发送在活动半路被限流；半数会员没收到优惠；促销扑街。

**Correct pattern / 正确做法**: Load-test to 3× expected peak; negotiate committed throughput; stagger sends. 按预期峰值3倍压测；谈承诺吞吐；分批发送。 → `#md-102-unlimited-fairuse` (VEN-02), AP-048.

**Severity / 严重度**: 🔥 costly.

### AP-019 Let WhatsApp quality rating tank by blasting cold lists / 群发冷名单拖垮WhatsApp质量 {#ap-019-whatsapp-blast-cold}

**Anti-pattern / 反模式**: Importing a bought/cold list and blasting templated promos in service conversations. 导入购买/冷名单并在服务会话里群发模板促销。

**Why tempting / 诱因为何**: "More contacts = more reach, fast." 「名单越多=触达越快。」

**What actually happens / 实际后果**: Meta's quality rating drops to "low"; all templates are throttled for 7 days mid-promo — launch implodes. Meta 质量评分跌"低"；所有模板在促销中途限流7天——活动崩盘。

**Correct pattern / 正确做法**: Opt-in only; respect conversation types; watch the quality dashboard daily in campaign weeks. 仅 opt-in；区分会话类型；活动周每日盯质量看板。 → `#md-063-whatsapp-quality-quickreply` (MSG-09), SKILL.md HI-7.

**Severity / 严重度**: 💀 fatal.

### AP-027 Deploy member-facing AI without a kill switch / 会员AI无熔断开关 {#ap-027-ai-no-kill-switch}

**Anti-pattern / 反模式**: Shipping a member-facing AI (bot, pricing, recommender) with no instant off-switch. 上线面向会员的 AI（机器人/定价/推荐）却无一键关停。

**Why tempting / 诱因为何**: "We tested it; it's safe." 「我们测过了，安全。」

**What actually happens / 实际后果**: A prompt-injection or model bug starts quoting wrong prices or offensive text to members; you can't stop it for hours. 提示注入或模型 bug 开始给会员报错价或冒犯话术；你几小时都停不下来。

**Correct pattern / 正确做法**: Every member-facing AI has a one-click kill switch + human-monitored fallback. 每个会员 AI 都有一键熔断+人工监控兜底。 → `#md-088-smart-pricing-holiday` (AI-12), AP-035.

**Severity / 严重度**: 💀 fatal.

### AP-052 Use a DST-naive scheduler (AU/NZ double-book) / 用无视夏令时的排期器 {#ap-052-dst-naive-scheduler}

**Anti-pattern / 反模式**: Scheduling classes in local time without daylight-saving handling in AU/NZ. 在澳/新用本地时间排课却不管夏令时。

**Why tempting / 诱因为何**: "Local time is local time; the calendar handles it." 「本地时间就是本地时间；日历会处理。」

**What actually happens / 实际后果**: On DST day the 7am yoga appears twice; 20 members double-book, 10 are turned away — refunds + rage. 夏令日早7瑜伽出现两次；20人重复约、10人被拒——退款+暴怒。

**Correct pattern / 正确做法**: Store class times in UTC + market tz; test the DST boundary yearly; freeze edits on transition days. 课程时间存 UTC+市场时区；每年测 DST 边界；切换日冻结改期。 → `#md-067-dst-double-book` (CLS-01).

**Severity / 严重度**: 🔥 costly.

### AP-053 Deploy smart lockers with no remote release / 智能储物柜无远程开 {#ap-053-smart-locker-no-release}

**Anti-pattern / 反模式**: Installing smart lockers in an unmanned club with no remote or physical override. 无人场馆装智能储物柜却无远程或物理应急开。

**Why tempting / 诱因为何**: "They rarely jam; override adds cost." 「很少卡；应急开多花钱。」

**What actually happens / 实际后果**: A locker jams at midnight; a member's laptop is locked in; no staff; police called — reputation + possible claim. 储物柜半夜卡死；会员电脑锁里；无员工；报警——口碑+可能索赔。

**Correct pattern / 正确做法**: Remote-release API + a sealed physical master key on-site; daily self-test. 远程开 API+现场封存物理总钥匙；每日自检。 → `#md-122-smart-locker-jam` (UNM-04).

**Severity / 严重度**: 🔥 costly.

### AP-054 Show "pool open" when no lifeguard is on duty / 无救生员却显示泳池开放 {#ap-054-pool-open-no-lifeguard}

**Anti-pattern / 反模式**: The app/pool status shows "open" while the lifeguard called in sick and no replacement is on duty. App/泳池状态显示"开放"，但救生员请病假且无人替。

**Why tempting / 诱因为何**: "The water's fine; members can swim." 「水没问题；会员能游。」

**What actually happens / 实际后果**: A member swims solo; a cramp becomes an emergency with no one watching — HI-2 life-safety failure. 会员独自游；抽筋成急救却无人盯——违反 HI-2 人身安全。

**Correct pattern / 正确做法**: Pool status = lifeguard-on-duty status; auto-close on guard absence; sync on guard check-in. 泳池状态=救生员在岗状态；缺岗自动关闭；救生员签到即同步。 → `#md-138-pool-open-no-lifeguard` (POOL-10), SKILL.md HI-2.

**Severity / 严重度**: 💀 fatal.

### AP-056 Dim emergency lighting with the ambiance scene / 应急灯随氛围调暗 {#ap-056-emergency-light-dimming}

**Anti-pattern / 反模式**: Smart lighting that "dims for ambiance" also dims the emergency exit lights below code. 为氛围"调暗"的智能照明把应急出口灯也调到不合规亮度。

**Why tempting / 诱因为何**: "One lighting system, one scene controller." 「一套照明、一个场景控制器。」

**What actually happens / 实际后果**: A power dip triggers the dimmed "emergency" lights too faint to see; evacuation slows — life-safety code breach. 断电时调暗的"应急"灯太暗看不见；疏散变慢——违反人身安全规范。

**Correct pattern / 正确做法**: Emergency lights on a separate, non-dimmable circuit; monthly 90-min battery test. 应急灯走独立、不可调光回路；每月90分钟电池测。 → `#md-127-emergency-light-dimming` (UNM-09), `#md-013-exit-gate-fail-open` (FACILITY-13).

**Severity / 严重度**: 💀 fatal.

### AP-016 Buy gray-import equipment for mission-critical lanes / 关键链路买水货设备 {#ap-016-gray-import-critical}

**Anti-pattern / 反模式**: Purchasing gray-import gate/network gear for mission-critical paths to save cost. 为省钱在关键链路买水货闸机/网络设备。

**Why tempting / 诱因为何**: "It's the same model, 30% cheaper." 「同型号，便宜30%。」

**What actually happens / 实际后果**: The gray-import gate dies on a Saturday; no local RMA; the club runs manual for a week — revenue + experience loss. 水货闸机周六坏；无本地返修；手动放行一周——营收+体验双损。

**Correct pattern / 正确做法**: Locally-supported SKUs with warranty + SLA for critical gear; validate serial region. 关键设备买本地支持型号（含保修+SLA）；核序列号区域。 → `#md-105-gray-import-critical` (VEN-05).

**Severity / 严重度**: 🔥 costly.

### AP-031 Send a personal payment link in a member group chat / 在会员群发个人支付链接 {#ap-031-payment-link-groupchat}

**Anti-pattern / 反模式**: Posting a member's personal payment link in a WeChat group, exposing their pending amount to others. 在微信群里发某会员的个人支付链接，让其待付金额被他人看见。

**Why tempting / 诱因为何**: "It's faster than a DM." 「比私信快。」

**What actually happens / 实际后果**: A member's ¥8,000 renewal link is visible to the whole group; they feel exposed and complain. 某会员8千元续费链接被全群看见；他觉得被曝光而投诉。

**Correct pattern / 正确做法**: Send payment links 1:1 via the official channel only; never in groups. 支付链接只走官方渠道一对一发；绝不进群。 → `#md-041-payment-link-groupchat` (PAY-11), SKILL.md HI-8.

**Severity / 严重度**: ⚠️ painful.

### AP-033 Leave CCTV retention unverified (over- or under-retain) / 监控留存不核验 {#ap-033-cctv-retention-unverified}

**Anti-pattern / 反模式**: Setting the NVR retention once and never verifying it against the legal period. 录像机留存期设一次后从不按法定期限核验。

**Why tempting / 诱因为何**: "90 days is safe; set and forget." 「90天稳妥；设完不管。」

**What actually happens / 实际后果**: The law says 30 days but you kept 90 — a breach exposes 3× footage; or you kept 10 and lost evidence. 法定30天你存了90——违规曝光3倍时长；或只存10天丢了证据。

**Correct pattern / 正确做法**: Per-market retention config; monthly delete-log review; alert on deviation. 按市场配置留存期；每月查删除日志；偏差即告警。 → `#md-090-cctv-retention-verify` (CMP-02), SKILL.md HI-5.

**Severity / 严重度**: 🔥 costly.

---

## G13 Tri-Perspective Coverage / G13 三视角覆盖矩阵

> This library was authored so each anti-pattern maps to an Architect × Operator × Member touchpoint and none is an orphan.
> 本库每条反模式都映射到「架构师 × 运营者 × 会员」触点，无孤儿项。

- **Architect / 架构师**: Vendor lock-in, data-export clauses, UPS/network design, AI guardrails + kill switch, fire monitor-only, biometric consent architecture, pool safety architecture, retention config — the "design the boundaries" layer (AP-002, AP-007, AP-008, AP-010, AP-021, AP-027, AP-030, AP-035, AP-036, AP-047, AP-054, AP-056).
- **Operator / 运营者**: Offboarding, refund policy, reconciliation hour, DST scheduling, deferred revenue, promo headroom, restore drills, locker override, panic readiness — the "run it without blowing up" layer (AP-013, AP-018, AP-019, AP-023, AP-024, AP-037, AP-038, AP-039, AP-052, AP-053, AP-033).
- **Member / 会员**: No surprise charges, dignified access, privacy of PII/photo, safe environment, honest "open" status, reachable human help, no spam — the "trust & safety" layer (AP-001, AP-005, AP-006, AP-011, AP-014, AP-017, AP-032, AP-040, AP-045, AP-050, AP-055, AP-031).

> **Honesty note / 诚实注记**: Every "failure story" above is an archetypal pattern, not a claimed real incident. Verify market-specific regulations via `tools/05` and volatile vendor/pricing facts via `tools/04` before acting. Severity tags are relative guidance, not legal/risk advice.
> 上述每个"翻车故事"均为原型模式，非声称的真实事件。行动前请经 `tools/05` 核验市场法规、经 `tools/04` 核验易变供应商/价格事实。严重度标签为相对指引，非法律/风险意见。
