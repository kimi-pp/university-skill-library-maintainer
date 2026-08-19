# Case 04 · Yoga & Pilates Chain (3 Sites) — Booking-First & Quiet UX / 案例04 · 瑜伽普拉提三店连锁：约课优先与安静体验

> **Cluster / 集群**: A (formats) · M (messaging) · G (lifecycle)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: DST/timezone & cross-state rules pass `tools/05`; messaging cadence passes `tools/04`.
> **Cross-references / 交叉引用**: `references/02-club-formats-and-zones.md#format-yogapilates` · `references/15-lifecycle-scenarios.md` · `references/17-omnichannel-messaging.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: 🔄 AU state-level SPAM/anti-scams rules differ — verify via `tools/05` before messaging. / 标注 🔄 的澳洲州级反垃圾规则不同——发消息前经 `tools/05` 核验。

> **Honesty preamble / 诚实声明**: This is an archetypal composite case built from common industry patterns for teaching purposes — not a claimed real company. Numbers are directional. / 本案例为教学用途的原型合成案例，非真实公司；数字为方向性参考。

---

## ① Context card / 背景卡 {#case-04-context}

- **Format / 业态**: Yoga & Pilates chain, 3 sites (~200 sqm each), ~900 members total. / 瑜伽普拉提连锁，3 店（各约 200 平），共约 900 会员。
- **Market / 市场**: Australia (multi-state: NSW + VIC + QLD). / 澳大利亚（跨州：新州 + 维州 + 昆州）。
- **FDMM start / 起点等级**: L2, booking-first; AI optional. / L2，约课优先；AI 可选。
- **Team / 团队**: founder + 3 studio leads + 9 teachers (casual). / 创始人 + 3 店长 + 9 名兼职老师。
- **Annual IT envelope / 年 IT 预算带**: directional A$25k–A$55k opex; no capex. / 方向性经营支出 2.5–5.5 万澳元；无资本开支。
- **Why this case / 为何选它**: Very light stack per `references/02#format-yogapilates`; the "waitlist psychology + quiet-hours etiquette + DST double-booking" case. / 按 `references/02#format-yogapilates` 极轻栈；是「候补心理 + 安静时段礼仪 + DST 重复预约」案例。

---

## ② The starting mess / 起初的一团乱 {#case-04-mess}

- Each site ran its own booking sheet; a member booked the "same" 7am class at two sites because the clocks were in different timezones during DST transition — and got charged twice. / 三店各用各的预约表；一名会员在 DST 切换时因时区不同，把「同一个」早 7 点课在两店都约了——还被扣了两次费。
- Teachers were paid by handwritten class count; payroll took 3 days and erred often, causing monthly arguments. / 老师按手写课时数算薪；工资核算花 3 天且常出错，引发每月争吵。
- Win-back emails blasted lapsed members 3×/week; unsubscribes spiked and a few marked spam to the carrier. / 召回邮件每周狂轰 3 次；退订激增，有人向运营商标垃圾。
- Underlying cause / 根因: three independent site sheets with wall-clock time storage, no shared system — a classic Iron Law 1 zone-mismatch across states. / 根因：三店独立表 + 挂钟时间存储、无共享系统——跨州铁律 1 区域错配的典型。

---

## ③ The journey (phase-by-phase) / 转型之路（分阶段） {#case-04-journey}

### Phase 1 — Unified booking + single timezone (Month 0–2) / 统一约课 + 单一时区 {#case-04-journey-p1}
- `references/02#format-yogapilates` + `references/15-lifecycle-scenarios.md`: one booking SaaS, all sites on UTC-store + local display to kill DST drift. / `references/02#format-yogapilates` + `references/15`：统一约课 SaaS，全店 UTC 存、本地显，根除 DST 漂移。
- Reasoning / 理由: Iron Law 1 — yoga/pilates is booking-UX-first, not hardware-first; multi-state demands one clock. / 铁律 1——瑜伽普拉提是约课体验优先，非硬件优先；跨州须统一时钟。
- Library used / 用到的库: `references/02#format-yogapilates` · `references/15` (lifecycle) · `templates/09-mms-selection-scorecard.md`. / 用到的库：`references/02#format-yogapilates` · `references/15`（生命周期）· `templates/09`（选型）。

### Phase 2 — Waitlist psychology (Month 2–5) / 候补心理 {#case-04-journey-p2}
- Auto-waitlist with transparent position + polite "you're #2, we'll ping on open" copy per `references/17-omnichannel-messaging.md`. / 自动候补 + 透明位次 + 礼貌文案「您排第 2，有位秒通知」，按 `references/17`。
- Kept quiet-hours etiquette: no messages 9pm–8am local (member-respect, not just compliance). / 守安静时段礼仪：本地时间晚 9 至早 8 不发消息（尊重会员，不止合规）。
- Library used / 用到的库: `references/17` (messaging) · `data/01-kpi-benchmark-library.md` (waitlist convert). / 用到的库：`references/17`（消息）· `data/01`（候补转化）。

### Phase 3 — Teacher payroll automation (Month 4–8) / 老师工资自动化 {#case-04-journey-p3}
- Class check-in fed payroll automatically; teacher portal showed confirmed hours; dispute window 48h. / 上课签到自动喂工资；老师端口可见已确认课时；申诉窗口 48 小时。
- Reduced payroll from 3 days to same-day draft; errors dropped. / 工资核算从 3 天缩到当日出稿；错误下降。
- Library used / 用到的库: `data/20-micro-details-ledger.md` (payroll keys) · `references/05-methodology-library.md` (process). / 用到的库：`data/20`（工资键）· `references/05`（流程）。

### Phase 4 — Gentle win-back (Month 8–12) / 温和召回 {#case-04-journey-p4}
- Replaced blasts with behavior-triggered, capped 1×/week win-back (HI-7 opt-in respect); easy opt-out in every footer. / 把狂轰换成行为触发、封顶每周 1 次的召回（尊重 HI-7 Opt-in）；每封页脚易退订。
- Library used / 用到的库: `references/17` · `tools/05` (anti-spam). / 用到的库：`references/17` · `tools/05`（反垃圾）。

:::dynamic-hook topic="au-state-spam-cadence-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
AU state-level anti-spam / SMS rules (NSW/VIC/QLD) and the federal Spam Act interplay shift; verify messaging cadence & consent via `tools/05` before campaigns. / 澳洲州级反垃圾 / SMS 规则（新州/维州/昆州）与联邦《反垃圾法》的交叉会变动；活动前经 `tools/05` 核验发送节奏与同意。
:::

---

## ④ What went wrong / 踩过的坑 {#case-04-setbacks}

### Setback 1 — DST double-booking across states (AU) / 跨州 DST 重复预约
- During DST change, two sites in different states showed the "same" wall-clock class; member booked both, charged twice, complained to fair-trading. / DST 切换时，两店在不同时州显示「同一」挂钟课；会员两店都约、扣两次费、投诉到消协。
- Fix / 修复: moved all stored times to UTC with local display; added cross-site clash check at book time. / 全部存 UTC、本地显示；约课时加跨店冲突校验。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-dst-double-book` (wall-clock storage). / 对应反模式：挂钟时间存储。

### Setback 2 — Over-aggressive win-back caused unsubscribes / 过度召回致退订
- 3×/week blasts pushed lapsed-member unsubscribe rate up directional 2×; some flagged spam, risking sender reputation. / 每周 3 次狂轰让流失会员退订率方向性翻倍；有人标垃圾，危及发信声誉。
- Fix / 修复: capped 1×/week, behavior-triggered only, added easy opt-out; unsubscribe rate returned to baseline within 6 weeks. / 封顶每周 1 次、仅行为触发、加易退订；6 周内退订率回到基线。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-over-aggressive-winback` (spam cadence). / 对应反模式：垃圾节奏。

---

## ⑤ Outcomes (6–18 months later, directional) / 结果（方向性） {#case-04-outcomes}

- Double-booking complaints: from several/month to ~0 after UTC store. / 重复预约投诉：每月数次 → UTC 存储后约 0。
- Payroll: 3 days → same-day draft; error rate down directional 60–80%; teacher disputes near-zero. / 工资：3 天 → 当日稿；错误率方向性降 60–80%；教练纠纷近零。
- Win-back unsubscribe: returned to baseline; reactivation directional +2 to +4 pp. / 召回退订：回基线；激活率方向性 +2 至 +4 个百分点。
- Waitlist convert: transparent position lifted off-waitlist conversion directional +5 to +12 pp. / 候补转化：透明位次让离候补转化方向性 +5 至 +12 个百分点。
- Honest caveat / 诚实提示: quiet-hours etiquette is a brand choice, but consent law (HI-7) is a floor, not a ceiling. / 安静时段礼仪是品牌选择，但同意法（HI-7）是底线非上限。

---

## ⑥ Transferable lessons / 可迁移经验 {#case-04-lessons}

- Store times in UTC, display local — kills DST drift for multi-state chains. / 时间存 UTC、显本地——根除跨州连锁的 DST 漂移。
- Waitlist transparency builds trust; silence ("you're #2") beats pressure. / 候补透明建信任；「您排第 2」的安静感胜过压迫感。
- Automate casual-teacher payroll from check-in; hand-count errs. / 从签到自动算兼职老师工资；手数必错。
- Messaging cadence is a retention lever AND a compliance line (HI-7). / 发送节奏既是留存杠杆也是合规线（HI-7）。
- Quiet-hours etiquette is member-respect, not just law. / 安静时段礼仪是尊重会员，不止守法。
- One booking SaaS across sites beats three sheets — integration even at L2. / 跨店统一约课 SaaS 胜三张表——L2 也要集成。
- Payroll dispute window (48h) prevents month-end arguments. / 工资申诉窗口（48h）避免月底争吵。
- Verify state-level spam rules before any cross-state campaign (`tools/05`). / 任何跨州活动前经 `tools/05` 核验州级反垃圾规则。

---

## ⑦ Related files / 相关文件 {#case-04-related}

- `references/02-club-formats-and-zones.md#format-yogapilates` · `#zone-groupclass` · `#zone-pt`
- `references/15-lifecycle-scenarios.md` · `references/17-omnichannel-messaging.md` · `references/05-methodology-library.md`
- `tools/05-regulation-traceability-verification.md` (AU Spam Act, state rules) · `templates/09-mms-selection-scorecard.md`
- `data/21-anti-pattern-library.md#ap-dst-double-book` · `#ap-over-aggressive-winback`
- `data/01-kpi-benchmark-library.md` (unsubscribe / reactivation / waitlist baselines) · `data/20-micro-details-ledger.md`

---

## ⑧ G13 tri-perspective note / G13 三视角覆盖说明 {#case-04-g13}

**Architect / 架构**: one booking SaaS, UTC storage, payroll fed from check-in — light stack done right. / 统一约课 SaaS、UTC 存储、工资从签到喂——轻栈做对。
**Operator / 商家**: 3 studio leads run 3 sites without double-entry; payroll same-day. / 3 店长无重复录入运营 3 店；工资当日出。
**Member / 会员**: no double-charge, transparent waitlist, quiet-hours respect, no spam. / 不重复扣费、候补透明、守安静时段、无骚扰。
No orphan touchpoint — booking + payroll + messaging all converge on the member experience. / 无孤儿触点——约课 + 工资 + 消息全部汇于会员体验。
