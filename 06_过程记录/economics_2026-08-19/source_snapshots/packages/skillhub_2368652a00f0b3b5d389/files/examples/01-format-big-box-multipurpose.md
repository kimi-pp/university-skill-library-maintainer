# Case 01 · Big-Box Multi-Purpose Club — FDMM L2→L4 / 案例01 · 大型综合馆：成熟度 L2→L4

> **Cluster / 集群**: A (formats) · C (hardware) · D (network) · E (data/AI) · U (KPI)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: vendor/price ranges pass `tools/04`; benchmark % pass `data/01-kpi-benchmark-library.md`; compliance passes `tools/05`.
> **Cross-references / 交叉引用**: `references/02-club-formats-and-zones.md` · `tools/01-fdmm-maturity-assessment.md` · `tools/02-ai-use-case-rice-scorecard.md` · `tools/06-roi-three-scenario.md` · `templates/09-mms-selection-scorecard.md` · `playbooks/01-single-club-zero-to-one.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: 🔄 pricing & vendor landscape volatile — run `tools/04` before budgeting. / 标注 🔄 的价格与供应商格局易变——预算前跑 `tools/04`。

> **Honesty preamble / 诚实声明**: This is an archetypal composite case built from common industry patterns for teaching purposes — not a claimed real company. Numbers are directional. / 本案例为教学用途的原型合成案例，非真实公司；数字为方向性参考。

---

## ① Context card / 背景卡 {#case-01-context}

- **Format / 业态**: Big-box multi-purpose, 4,000 sqm, 6,000 members, 1 site. / 大型综合馆，4000 平米，6000 会员，单店。
- **Market / 市场**: Tier-1 city in Chinese Mainland. / 中国大陆一线城市。
- **FDMM start / 起点等级**: L2 (membership SaaS live, QR entry) targeting L4 in 24 months. / L2（会籍 SaaS 上线、扫码入场），目标 24 个月到 L4。
- **Team / 团队**: 1 part-time IT admin (ops manager wearing the hat), 1 external MSP, no in-house architect. / 1 名兼职 IT 管理员（运营经理兼任），1 家外部运维服务商，无内部架构师。
- **Annual IT envelope / 年 IT 预算带**: directional ¥600k–¥1.2M opex + one-off ¥800k–¥1.5M capex (gate + network + sensors). / 方向性年经营支出 60–120 万 + 一次性资本开支 80–150 万（闸机+网络+传感）。
- **Why this case / 为何选它**: Heaviest stack weight of all formats per `references/02-club-formats-and-zones.md#format-bigbox`; the canonical "integration & single source of truth" pain. / 按 `references/02` 是 IT 权重最重的业态，是「集成与唯一口径」痛点的典型。

---

## ② The starting mess / 起初的一团乱 {#case-01-mess}

- The membership system (MMS) was an aging local-server product from 2014 that crashed every Monday peak. Front desk kept a paper "overflow book" because the gate QR sync lagged 8–15 minutes, so valid members were turned away at the turnstile. / 会籍系统是一套 2014 年的本地服务器老产品，每周一高峰必崩。闸机二维码同步延迟 8–15 分钟，有效会员在闸机前被拦，前台只能备一本纸质「溢出登记簿」。
- Three systems held the "same" member record with three different spellings of the same name; BI was impossible because no one trusted the headcount. / 三套系统里同一个会员有三种不同拼写，没人敢信总人数，BI 根本做不了。
- Energy bill was a mystery: 80 cardio machines ran 16h/day but the club could not tell which zone wasted power. / 电费是笔糊涂账：80 台有氧器械每天跑 16 小时，但场馆说不清哪个区域在浪费电。
- The owner's ask was blunt: "Stop the Monday crash, tell me who is about to quit, and cut the power bill — without hiring a full IT team." / 老板的要求很直白：「周一别崩、告诉我谁要跑路、把电费砍下来——还别让我招一整支 IT 队。」
- Underlying cause / 根因: the club had bought systems one symptom at a time (gate vendor, POS vendor, MMS vendor) with zero integration plan — classic Iron Law 7 violation (no staged maturity path). / 根因：场馆是「一个症状买一套系统」（闸机商、POS 商、MMS 商）零集成规划——典型铁律 7 违例（无阶段性成熟度路径）。

---

## ③ The journey (phase-by-phase) / 转型之路（分阶段） {#case-01-journey}

### Phase 1 — Diagnose & baseline (Month 0–1) / 诊断与基线 {#case-01-journey-p1}
- Ran the 12-question intake via `tools/00-intake-router.md` → confirmed L2, not L1 (SaaS already live). Used `tools/01-fdmm-maturity-assessment.md` worksheet to set the L2→L4 entry gates (≥3 systems integrated, ID unified before L3). / 用 `tools/00` 跑 12 问开场诊断 → 确认是 L2 而非 L1（SaaS 已上线）。用 `tools/01` 工作表设定 L2→L4 晋级准入（L3 前须 ≥3 系统打通、身份归一）。
- Reasoning / 理由: Iron Law 7 — do not leap levels; the club was already on SaaS, so the job was integration, not "escape paper". / 铁律 7——不跳级；该馆已在 SaaS 上，任务是集成而非「脱贫」。
- Library used / 用到的库: `tools/01` (assessment) · `references/02#format-bigbox` (priority zones: reception, gate, gym floor, server room). / 用到的库：`tools/01`（评估）· `references/02#format-bigbox`（必建区域：前台、闸机、器械区、机房）。

### Phase 2 — MMS replacement & master data (Month 1–5) / 换系统与主数据 {#case-01-journey-p2}
- Selected a cloud MMS via `templates/09-mms-selection-scorecard.md` against ≥3 options (one local, one open-source-low-cost) per Iron Law 8; scored on data-export clause FIRST (vendor neutrality). / 用 `templates/09` 在 ≥3 个选项（含本地与开源低成本）中按铁律 8 选型；先按「数据导出条款」打分（供应商中立）。
- Built a master-member de-dupe rule BEFORE migration (this saved Phase 4 — see setbacks). Rule: mobile > national ID > name+pinyin. / 在迁移前先建「会员主数据去重规则」（这救了第四阶段，见挫折节）。规则：手机 > 证件号 > 姓名+拼音。
- Used `playbooks/01-single-club-zero-to-one.md` Chapter 3 migration runbook (dry-run → cutover weekend → 7-day parallel). / 用 `playbooks/01` 第 3 章迁移手册（试运行 → 周末割接 → 7 天并行）。
- Library used / 用到的库: `templates/09` (selection) · `playbooks/01` (migration) · `data/20-micro-details-ledger.md` (match keys). / 用到的库：`templates/09`（选型）· `playbooks/01`（迁移）· `data/20`（匹配键）。

### Phase 3 — Gate upgrade & network split (Month 4–8) / 闸机升级与网络拆分 {#case-01-journey-p3}
- Replaced tripod gates with swing gates + QR/NFC + offline-fail-open; moved gates to business VLAN, cardio to isolated IoT VLAN per `references/02-club-formats-and-zones.md#zone-gymfloor`. / 三辊闸换摆闸 + 二维码/NFC + 离线故障开；闸机走业务 VLAN，有氧走隔离 IoT VLAN（见 `references/02#zone-gymfloor`）。
- Fire-egress release kept monitor-only (HI-4); UPS on core so gates release on power loss. / 消防释放只联不控（HI-4）；核心接 UPS，断电闸机释放。
- Library used / 用到的库: `references/02#zone-gate` · `#zone-serverroom` · `references/08-network-and-infrastructure.md` (VLAN standard). / 用到的库：`references/02#zone-gate` · `#zone-serverroom` · `references/08`（VLAN 标准）。

### Phase 4 — BI & churn model (Month 8–16) / BI 与流失模型 {#case-01-journey-p4}
- Stood up a daily dashboard (attendance, revenue, zone load) from the now-clean single source. Benchmarked against `data/01-kpi-benchmark-library.md` (big-box churn ~4–8%/yr directional). / 用已干净的单一口径搭了每日看板（到店、营收、分区负载）。对照 `data/01` 基准（综合馆年流失约 4–8% 方向性）。
- Scored churn-AI use case with `tools/02-ai-use-case-rice-scorecard.md`; trained on 12 months of post-migration behavior (NOT promo window — see setbacks). / 用 `tools/02` 给流失 AI 用例打分；用迁移后 12 个月行为数据训练（非促销窗口——见挫折节）。
- Energy optimization: smart meters on elec/water per `references/02-club-formats-and-zones.md#zone-facade` + schedule-linked HVAC. / 能效优化：按 `references/02#zone-facade` 给电/水装智能表 + 联动空调时控。
- Library used / 用到的库: `tools/02` (RICE) · `data/01` (KPI) · `references/13-data-and-llm-engine.md` (model risk G7). / 用到的库：`tools/02`（RICE）· `data/01`（KPI）· `references/13`（模型风险 G7）。

### Phase 5 — Hardening & ROI close (Month 16–24) / 加固与 ROI 闭环 {#case-01-journey-p5}
- ROI three-scenario via `tools/06-roi-three-scenario.md` (base/expected/pessimistic), separating revenue, cost, compliance, member-experience. / 用 `tools/06` 做 ROI 三情景（基准/预期/悲观），区分营收、成本、合规、会员体验。
- Passed `tools/03-rigor-gate-checklist.md` G1–G13 (incl. G4 life-safety, G7 AI risk) before declaring L4. / 宣布 L4 前过了 `tools/03` 的 G1–G13（含 G4 人身安全、G7 AI 风险）。
- Library used / 用到的库: `tools/06` (ROI) · `tools/03` (gate). / 用到的库：`tools/06`（ROI）· `tools/03`（闸门）。

:::dynamic-hook topic="cn-bigbox-mms-pricing-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
Cloud MMS per-member-per-month SaaS list ranges vary widely by seat count and module; treat any single figure as experience-based. Verify current bands via `tools/04` before contract. / 国内大型综合馆 MMS 的「每会员每月」SaaS 标价随席位与模块浮动极大；任何单点数字均属经验性。签约前经 `tools/04` 核验当前区间。
:::

---

## ④ What went wrong / 踩过的坑 {#case-01-setbacks}

### Setback 1 — 12% duplicate members found in migration dry-run / 迁移试运行发现 12% 重复会员
- The dry-run (not the live cutover) surfaced 12% duplicate member records — same human, three spellings, three wallets. Left unhandled, this would have tripled the SMS marketing cost and split the churn label. / 试运行（不是正式割接）爆出 12% 重复会员——同一个人、三种拼写、三个钱包。不处理会导致短信营销成本三倍、流失标签分裂。
- Fix / 修复: paused cutover; ran a deterministic match (mobile > ID > name+pinyin) from `data/20-micro-details-ledger.md`; merged to one master, archived duplicates read-only, kept a merge audit log. / 暂停割接；用 `data/20` 的确定性匹配规则（手机 > 证件 > 姓名+拼音）合并为单一主档，重复档只读归档，留合并审计日志。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-duplicate-member-migration` (migrate-before-dedupe). / 对应反模式：先迁移后去重。

### Setback 2 — Churn model trained on a promo month / 流失模型用了促销月数据训练
- First model flagged "everyone churning" because training window included a 50%-off annual-card promo month that distorted visitFrequency baselines. Precision was ~0.45 — worse than a coin flip on who to call. / 初版模型「全员要跑路」，因为训练窗口含一个五折年卡促销月，把到店频率基线带歪了。精确率约 0.45——比抛硬币还差。
- Fix / 修复: excluded promo months, added a `promoFlag` feature, re-trained on 12 steady months; precision rose to a directional 0.7–0.8 range; recall held. / 剔除促销月、加 `promoFlag` 特征、用 12 个平稳月重训；精确率升到方向性 0.7–0.8 区间；召回稳住。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-promo-trained-churn` (train on biased window). / 对应反模式：用偏态窗口训练。

---

## ⑤ Outcomes (6–18 months later, directional) / 结果（6–18 个月后，方向性） {#case-01-outcomes}

- Monday crash frequency: from ~4/month to near-zero (directional: 0–1 per quarter). / 周一崩溃：约 4 次/月 → 近乎零（方向性：0–1 次/季）。
- Gate false-reject at peak: from 8–15 min sync lag to <30s; turn-aways roughly halved. / 高峰误拒：8–15 分钟同步延迟 → <30 秒；被拦人数约减半。
- Churn-AI caught at-risk members; retention uplift directional +3 to +6 pp on contacted cohort (measured vs hold-out). / 流失 AI 锁定高风险会员；触达人群续费提升方向性 +3 至 +6 个百分点（对照 hold-out 测）。
- Energy: smart-meter + HVAC scheduling cut electricity opex a directional 8–15% on the cardio floor. / 能效：智能表 + 空调时控把有氧区电费经营支出方向性砍下 8–15%。
- Single source of truth: three spellings → one ID; weekly management meeting now runs on one dashboard. / 唯一口径：三种拼写 → 一个 ID；周例会现在跑在一张看板上。
- Honest caveat / 诚实提示: these are directional ranges from a composite; real variance depends on city, lease power rate, and discipline of daily data entry. / 这些是合成案例的方向性区间；真实差异取决于城市、租赁电价与每日录入纪律。

---

## ⑥ Transferable lessons / 可迁移经验 {#case-01-lessons}

- De-dupe master data BEFORE migration, ideally in the dry-run, not at cutover. / 迁移前去重主数据，最好在试运行阶段，而非割接时。
- Never train churn/propensity models on promo or holiday-distorted windows. / 绝不用促销或节假日畸变窗口训练流失/倾向模型。
- Split POS/business VLAN from IoT VLAN early — it contains future cardio/IoT faults. / 早把 POS/业务 VLAN 与 IoT VLAN 分开——可隔离日后器械/IoT 故障。
- Gate must fail-OPEN on power loss; fire release is monitor-only (HI-4). / 闸机断电必须故障开；消防释放只联不控（HI-4）。
- One part-time admin can run L2→L4 if the architecture is integration-first and vendor-neutral. / 一位兼职管理员也能跑完 L2→L4，前提是架构「集成优先 + 供应商中立」。
- ROI must be three-scenario before any >¥100k spend (Iron Law 6). / 任何超 10 万元投入前必须做 ROI 三情景（铁律 6）。
- BI is worthless until the single source of truth is trusted. / 在唯一口径被信任之前，BI 毫无价值。
- Score AI use cases with RICE before building — most clubs over-build, under-measure. / 建 AI 前先用 RICE 打分——多数场馆重建设、轻度量。

---

## ⑦ Related files / 相关文件 {#case-01-related}

- `references/02-club-formats-and-zones.md#format-bigbox` · `#zone-gymfloor` · `#zone-gate` · `#zone-serverroom` · `#zone-facade`
- `tools/01-fdmm-maturity-assessment.md` · `tools/02-ai-use-case-rice-scorecard.md` · `tools/03-rigor-gate-checklist.md` · `tools/06-roi-three-scenario.md`
- `templates/09-mms-selection-scorecard.md` · `playbooks/01-single-club-zero-to-one.md` · `references/08-network-and-infrastructure.md` · `references/13-data-and-llm-engine.md`
- `data/20-micro-details-ledger.md` · `data/21-anti-pattern-library.md#ap-duplicate-member-migration` · `#ap-promo-trained-churn`
- `data/01-kpi-benchmark-library.md` (churn / energy baselines)

---

## ⑧ G13 tri-perspective note / G13 三视角覆盖说明 {#case-01-g13}

**Architect / 架构**: L2→L4 roadmap with VLAN split, master-data layer, and BI/churn/energy as three stacked layers — each with explicit entry gate. / L2→L4 路线图，含 VLAN 拆分、主数据层、BI/流失/能效三层堆叠，每层有显式准入。
**Operator / 商家**: part-time admin runbook (dry-run → cutover → daily dashboard) keeps the club runnable without a full IT team. / 兼职管理员手册（试运行→割接→每日看板）让场馆无整支 IT 队也能运转。
**Member / 会员**: shorter gate queues, no false turn-aways, no duplicate-account confusion at renewal. / 闸机排队更短、不再被误拦、续费时不再有重复账户混乱。
No orphan touchpoint — all three perspectives are carried by the integration-first design. / 无孤儿触点——三视角均由「集成优先」设计承接。
