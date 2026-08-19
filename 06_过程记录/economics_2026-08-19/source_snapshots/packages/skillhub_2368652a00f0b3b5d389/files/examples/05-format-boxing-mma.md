# Case 05 · Boxing / MMA Gym — PT-Package Heavy & Waiver Digitization / 案例05 · 拳馆/MMA：私教课包为重与免责数字化

> **Cluster / 集群**: A (formats) · R (anti-fraud) · F (compliance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: prepaid/consumer-protection passes `tools/05`; insurance waiver rules pass `tools/05`.
> **Cross-references / 交叉引用**: `references/02-club-formats-and-zones.md#format-boxing` · `references/16-security-operations-and-emergency.md` · `data/21-anti-pattern-library.md` · `tools/05-regulation-traceability-verification.md`
> **Retrieval note / 检索提示**: 🔄 prepaid/consumer-protection rules vary by market — verify via `tools/05` before any fee flow. / 标注 🔄 的预付/消保规则各市场不同——任何收费流前经 `tools/05` 核验。

> **Honesty preamble / 诚实声明**: This is an archetypal composite case built from common industry patterns for teaching purposes — not a claimed real company. Numbers are directional. / 本案例为教学用途的原型合成案例，非真实公司；数字为方向性参考。

---

## ① Context card / 背景卡 {#case-05-context}

- **Format / 业态**: Boxing / MMA gym, 600 sqm, ~700 members, PT-package heavy (~55% revenue). / 拳馆/MMA，600 平米，约 700 会员，私教课包占比重（约 55% 营收）。
- **Market / 市场**: Thailand (Bangkok, expat + local mix). / 泰国（曼谷，外籍 + 本地混合）。
- **FDMM start / 起点等级**: L2. / L2。
- **Team / 团队**: owner + 6 coaches + 1 front desk. / 老板 + 6 教练 + 1 前台。
- **Annual IT envelope / 年 IT 预算带**: directional ฿400k–฿800k opex + ฿300k–฿600k capex (POS + e-sign + gates). / 方向性经营支出 40–80 万泰铢 + 资本开支 30–60 万（POS+电子签+闸机）。
- **Why this case / 为何选它**: Revenue concentrated in PT packages + coach commissions → fraud & waiver risk surface fast. / 营收集中在私教课包 + 教练佣金 → 欺诈与免责风险很快暴露。

---

## ② The starting mess / 起初的一团乱 {#case-05-mess}

- Coaches collected PT fees via their personal wallets (PromptPay), then "reconciled" later — owner had no real view of sold vs delivered. / 教练用个人钱包（PromptPay）收私教费，事后「对账」——老板看不到真实售/交付。
- Waivers were paper forms scanned to a shared drive; when a member got a sparring injury, the waiver PDF was unsigned and unfindable. / 免责是纸表扫到共享盘；一名会员实战受伤时，免责 PDF 既未签又找不到。
- Coach commission was a spreadsheet the owner updated by hand and distrusted; two coaches argued pay every month. / 教练佣金是老板手填的表格，自己都不信；两名教练每月为钱吵架。
- Underlying cause / 根因: money path and consent path both lived outside any system — Iron Law 10 (honesty) and HI-6 (health/liability) blind spots at once. / 根因：资金路径与同意路径都在系统外——铁律 10（诚实）与 HI-6（健康/责任）同时失明。

---

## ③ The journey (phase-by-phase) / 转型之路（分阶段） {#case-05-journey}

### Phase 1 — Kill side-wallet collection (Month 0–2) / 砍掉私账收款 {#case-05-journey-p1}
- `tools/00-intake-router.md` routed to anti-fraud `references/16-security-operations-and-emergency.md`; all PT sales forced through club POS, coach paid commission only. / `tools/00` 路由到反欺诈 `references/16`；所有私教销售强制走场馆 POS，教练只拿佣金。
- Reasoning / 理由: Iron Law 10 honesty + anti-fraud (R cluster) — money must be visible to the owner; off-book = liability. / 铁律 10 诚实 + 反欺诈（R 集群）——钱必须对老板可见；账外 = 责任。
- Library used / 用到的库: `tools/00` (router) · `references/16` (anti-fraud) · `references/02#format-boxing`. / 用到的库：`tools/00`（路由）· `references/16`（反欺诈）· `references/02#format-boxing`。

### Phase 2 — Waiver digitization (Month 1–4) / 免责数字化 {#case-05-journey-p2}
- E-sign waiver at first check-in, stored against member ID, retrievable in <30s (`tools/05` compliance + HI-6 health boundary respect). / 首次签到电子签免责，绑定会员 ID，<30 秒可调（合规 `tools/05` + 尊重 HI-6 医疗边界）。
- Insurance & waiver linked to the same record the gate reads, so entry = covered. / 保险与免责绑定到闸机读取的同一条记录，入场即已承保。
- Library used / 用到的库: `tools/05` (waiver law) · `references/12-biometrics-and-cctv.md` (consent) · `playbooks/02` (lite pattern). / 用到的库：`tools/05`（免责法）· `references/12`（同意）· `playbooks/02`（轻量范式）。

### Phase 3 — Coach commission system (Month 3–7) / 教练佣金系统 {#case-05-journey-p3}
- Commission auto-computed from DELIVERED sessions (not sold), with a 48h dispute window; coach portal shows live earned. / 佣金按「已交付课时」自动算（非售出），带 48h 申诉窗；教练端口看实时已赚。
- Equipment safety log: per-bag gloves/ wraps inspection logged per `references/16`. / 器械安全日志：每包手套/绷带检查留痕，按 `references/16`。
- Library used / 用到的库: `data/20-micro-details-ledger.md` (commission keys) · `references/16` (safety). / 用到的库：`data/20`（佣金键）· `references/16`（安全）。

### Phase 4 — Event registration (Month 6–10) / 赛事报名 {#case-05-journey-p4}
- Sparring-event sign-up with waivers re-accepted per event (not just membership); spectator consent captured. / 实战赛事报名，每场重新签免责（非仅入会时）；观众同意也采集。
- Library used / 用到的库: `templates/09-mms-selection-scorecard.md` (event tool) · `data/21` (event fraud). / 用到的库：`templates/09`（赛事工具）· `data/21`（赛事欺诈）。

:::dynamic-hook topic="th-prepaid-consumer-protection-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
Thailand's consumer-protection treatment of prepaid fitness packages and the relevant ministerial notifications are revised periodically; verify fund-handling rules via `tools/05` before any stored-value flow. / 泰国对健身预付课包的消保处理及相关部委公告会定期修订；任何储值流前经 `tools/05` 核验资金处理规则。
:::

---

## ④ What went wrong / 踩过的坑 {#case-05-setbacks}

### Setback 1 — Coach collecting fees via personal wallet (💀 anti-pattern) / 教练用私账收款（💀 反模式）
- A coach left owing ~40 unreported PT sessions; owner ate the refund and lost trust with other members. / 一名教练离职，欠约 40 节未申报私教；老板吞下退款，还丢了其他会员的信任。
- Fix / 修复: hard rule — POS-only, coach login audited; side-wallet = termination. Re-built trust via transparent commission dashboard. / 铁规——仅 POS、教练登录可审计；私账即辞退。用透明佣金看板重建信任。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-coach-side-wallet` 💀 (off-book revenue). / 对应反模式 💀：账外收入。

### Setback 2 — Waiver PDFs unsigned/unfindable during injury claim / 受伤索赔时免责 PDF 未签找不到
- Injury claim stalled because the scanned waiver was unsigned and filed under the wrong name; legal spent weeks reconstructing. / 受伤索赔卡住，因为扫描免责既未签又归错名；法务花数周重建。
- Fix / 修复: e-sign-at-check-in made waiver a gate precondition; searchable by member ID + date; legal held a tested retrieval runbook. / 电子签改为签到前置条件；按会员 ID + 日期可搜；法务持已测的调取手册。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-waiver-missing` (unfindable consent). / 对应反模式：免责不可查。

---

## ⑤ Outcomes (6–18 months later, directional) / 结果（方向性） {#case-05-outcomes}

- Off-book revenue: from material leakage to ~0 after POS-only. / 账外收入：实质性流失 → POS 仅用后约 0。
- Waiver retrievability: <30s by member ID; injury-claim prep time down directional 80–90%. / 免责可调性：按会员 ID <30 秒；受伤索赔准备时间方向性降 80–90%。
- Commission disputes: from frequent to directional <2%/month. / 佣金纠纷：频繁 → 方向性 <2%/月。
- Coach trust: transparent earned-commission portal ended monthly pay arguments. / 教练信任：透明已赚佣金端口终结了每月工资争吵。
- Honest caveat / 诚实提示: digitization reduces risk but does not remove the need for a real insurance policy and legal review. / 数字化降风险，但不替代真实保单与法律审查。

---

## ⑥ Transferable lessons / 可迁移经验 {#case-05-lessons}

- PT-heavy gyms must force all sales through club POS — side-wallets are fraud waiting to happen. / 私教重馆必须强制所有销售走场馆 POS——私账是等着发生的欺诈。
- Waiver must be e-signed at check-in and retrievable by ID in <30s; paper scans fail claims. / 免责须签到电子签、按 ID <30 秒可调；纸扫在索赔时失效。
- Commission on DELIVERED sessions, not sold — aligns coach and club. / 佣金按「已交付」而非「已售」——对齐教练与场馆。
- Equipment safety log is a liability shield, log it. / 器械安全日志是责任盾，要留痕。
- Insurance + legal review sit ABOVE any system (HI-6 respect). / 保单 + 法律审查在任何系统之上（尊重 HI-6）。
- Prepaid rules verified via `tools/05` before any stored-value flow (HI-3). / 储值流前经 `tools/05` 核验预付规则（HI-3）。
- Event waivers re-accepted per event, not just at membership. / 赛事免责每场重签，非仅入会时。
- Off-book revenue is a 💀 red line — audit coach logins weekly. / 账外收入是 💀 红线——每周审计教练登录。

---

## ⑦ Related files / 相关文件 {#case-05-related}

- `references/02-club-formats-and-zones.md#format-boxing` · `#zone-pt` · `#zone-gate` · `#zone-groupclass`
- `references/16-security-operations-and-emergency.md` (anti-fraud, safety) · `references/12-biometrics-and-cctv.md` · `tools/05-regulation-traceability-verification.md`
- `data/21-anti-pattern-library.md#ap-coach-side-wallet` 💀 · `#ap-waiver-missing`
- `data/20-micro-details-ledger.md` (waiver/commission retention detail) · `playbooks/02-boutique-studio-lite-kit.md`

---

## ⑧ G13 tri-perspective note / G13 三视角覆盖说明 {#case-05-g13}

**Architect / 架构**: POS-only money path + e-sign waiver + commission-on-delivered — fraud-resistant by design. / 仅 POS 资金路径 + 电子签免责 + 按交付计佣金——设计即抗欺诈。
**Operator / 商家**: owner sees real sold-vs-delivered; commission trusted; liability shielded. / 老板看到真实售/交付；佣金可信；责任有盾。
**Member / 会员**: clean waiver at check-in, fair commission means fair coaching, safer equipment. / 签到干净免责、公平佣金意味公平教学、器械更安全。
No orphan touchpoint — money, waiver, and safety all meet at the gate record. / 无孤儿触点——钱、免责、安全全汇于闸机记录。
