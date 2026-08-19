# Case 07 · Corporate / Office-Building Gym — B2B Eligibility & Privacy Split / 案例07 · 企业/写字楼健身房：B2B 资格与隐私边界

> **Cluster / 集群**: A (formats) · N (integration) · F (compliance) · Q (B2B)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: employer-data boundary passes `tools/05`; SSO/HRIS integration passes `tools/04`.
> **Cross-references / 交叉引用**: `references/02-club-formats-and-zones.md#format-corporate` · `references/18-integration-and-data-plumbing.md` · `tools/05-regulation-traceability-verification.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: 🔄 HRIS/SSO API policies shift — verify integration scope via `tools/04` before build. / 标注 🔄 的 HRIS/SSO API 政策会变——建设前经 `tools/04` 核验集成范围。

> **Honesty preamble / 诚实声明**: This is an archetypal composite case built from common industry patterns for teaching purposes — not a claimed real company. Numbers are directional. / 本案例为教学用途的原型合成案例，非真实公司；数字为方向性参考。

---

## ① Context card / 背景卡 {#case-07-context}

- **Format / 业态**: Corporate gym in an office tower, 350 sqm, operated for one enterprise client, ~1,200 eligible employees. / 写字楼内企业健身房，350 平米，为单一企业客户运营，约 1200 名合格员工。
- **Market / 市场**: Hong Kong (China). / 中国香港。
- **FDMM start / 起点等级**: L2, integration-heavy not AI-heavy. / L2，重集成轻 AI。
- **Team / 团队**: operator GM + 1 club supervisor + client HR liaison. / 运营方总经理 + 1 店长 + 客户 HR 对接。
- **Annual IT envelope / 年 IT 预算带**: directional HK$200k–HK$450k opex (integration + reporting); capex minor (badge readers). / 方向性经营支出 20–45 万港元（集成+报表）；资本开支小（工牌读头）。
- **Why this case / 为何选它**: B2B eligibility via HR system + badge access + utilization reporting + the privacy split the employer may NOT see. / B2B 资格走 HR 系统 + 工牌门禁 + 用量报表 + 雇主「不得看」的隐私边界。

---

## ② The starting mess / 起初的一团乱 {#case-07-mess}

- Eligibility was a monthly CSV from HR, pasted into the gym CRM by hand; leavers kept accessing for weeks. / 资格是 HR 每月给的 CSV，手工粘进场馆 CRM；离职者还能进好几周。
- The client HR director asked for "individual attendance of our staff" — which would expose who exercises and when to their employer. / 客户 HR 总监要「员工个人考勤」——等于把谁锻炼、何时锻炼暴露给雇主。
- SSO to the booking app stalled because the client's IT required a 3-month security review with no clear scope. / 预约 App 的 SSO 卡住，因为客户 IT 要求 3 个月安全审查却无明确范围。
- Underlying cause / 根因: the operator treated B2B as "just a big membership" and never designed the privacy split — an HI-1/HI-7 blind spot. / 根因：运营方把 B2B 当「只是个大会员」、从没设计隐私拆分——HI-1/HI-7 盲点。

---

## ③ The journey (phase-by-phase) / 转型之路（分阶段） {#case-07-journey}

### Phase 1 — Eligibility integration & badge access (Month 0–3) / 资格集成与工牌门禁 {#case-07-journey-p1}
- `references/02#format-corporate` + `references/18-integration-and-data-plumbing.md`: nightly HRIS eligibility sync → badge/QR access; leavers auto-revoked within 24h. / `references/02#format-corporate` + `references/18`：HRIS 夜间资格同步 → 工牌/二维码门禁；离职 24 小时内自动撤销。
- Reasoning / 理由: Iron Law 1 — corporate gym is integration-first, privacy-split is the core design, not an add-on. / 铁律 1——企业健身房是集成优先，隐私拆分是核心设计而非附加。
- Library used / 用到的库: `references/02#format-corporate` · `references/18` (integration) · `templates/09-mms-selection-scorecard.md`. / 用到的库：`references/02#format-corporate` · `references/18`（集成）· `templates/09`（选型）。

### Phase 2 — Privacy boundary definition (Month 1–4) / 隐私边界定义 {#case-07-journey-p2}
- Wrote a data-sharing contract: operator holds individual records; client gets AGGREGATE utilization only (no individual). Per `tools/05` + HI-7/HI-1. / 写数据共享合同：运营方持个人记录；客户仅得「聚合用量」（无个人）。按 `tools/05` + HI-7/HI-1。
- Individual attendance = member-private; employer may NOT see (pushed back, see setbacks). / 个人考勤 = 会员隐私；雇主不得看（已回推，见挫折）。
- Library used / 用到的库: `tools/05` (boundary law) · `references/10-apac-compliance-east-asia-oceania.md` (PDPO). / 用到的库：`tools/05`（边界法）· `references/10`（PDPO 合规）。

### Phase 3 — Utilization reporting to client (Month 3–6) / 给客户的用量报表 {#case-07-journey-p3}
- Dashboard: headcount, peak hours, class fill, aggregate demographics — never individual rows. / 看板：人数、高峰、满课率、聚合画像——绝不含个人行。
- ROI to client shown as "utilization & wellbeing signal", not surveillance. / 给客户的 ROI 呈现为「利用率与福祉信号」，而非监控。
- Library used / 用到的库: `data/01-kpi-benchmark-library.md` (utilization) · `references/19-growth-and-sales-stack.md` (Q/B2B). / 用到的库：`data/01`（利用率）· `references/19`（Q/B2B）。

### Phase 4 — SSO unblock (Month 6–9) / 解封 SSO {#case-07-journey-p4}
- Met client IT review with scoped SSO (booking app only, no HR data pull); used `tools/04` to confirm API scope. / 以范围化 SSO（仅预约 App、不拉 HR 数据）过客户 IT 审查；用 `tools/04` 确认 API 范围。
- Library used / 用到的库: `tools/04` (API policy) · `references/18` (integration). / 用到的库：`tools/04`（API 政策）· `references/18`（集成）。

:::dynamic-hook topic="hk-employer-data-boundary-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
Hong Kong PDPO's stance on employer-visible employee wellness/attendance data is interpreted per current guidelines; verify the boundary (aggregate-only vs individual) via `tools/05` before any report build. / 中国香港 PDPO 对雇主可见的员工健康/考勤数据的立场按现行指南解释；建任何报表前经 `tools/05` 核验边界（仅聚合 vs 个人）。
:::

---

## ④ What went wrong / 踩过的坑 {#case-07-setbacks}

### Setback 1 — Employer demanded individual attendance data / 雇主索要个人考勤数据
- HR director pressed for a per-employee attendance export, citing "we pay for it". Legal later flagged it as a PDPO breach risk. / HR 总监以「我们出钱」施压要逐员工考勤导出；法务后将其标为 PDPO 违规风险。
- Fix / 修复: invoked privacy boundary (HI-1/HI-7) + `tools/05`; offered richer AGGREGATE reporting instead; client accepted after legal sign-off. / 援引隐私边界（HI-1/HI-7）+ `tools/05`；改供更丰富的「聚合报表」；客户法务签字后接受。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-employer-attendance-demand` (over-share individual). / 对应反模式：过度共享个人数据。

### Setback 2 — SSO integration stalled 3 months / SSO 集成卡 3 个月
- Client IT's security review had no clear scope; the project waited while members used manual badges. / 客户 IT 安全审查无明确范围；项目干等，会员用人工工牌。
- Fix / 修复: proposed scoped SSO (booking only, no HR pull) + a one-page data-flow diagram; review closed in 3 weeks. / 改提「范围化 SSO（仅预约、不拉 HR）」+ 一页数据流图；3 周走完审查。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-sso-stall` (undefined scope). / 对应反模式：范围未定义。

---

## ⑤ Outcomes (6–18 months later, directional) / 结果（方向性） {#case-07-outcomes}

- Leaver access gap: from weeks to <24h after nightly HRIS sync. / 离职准入空窗：数周 → 夜间 HRIS 同步后 <24 小时。
- Privacy incidents: 0 individual records shared with employer. / 隐私事件：0 条个人记录共享给雇主。
- Utilization reporting: client satisfied with aggregate dashboard; renewal signal positive (directional). / 用量报表：客户满意聚合看板；续约信号正向（方向性）。
- SSO: scoped login live; HR data never traversed the gym system. / SSO：范围化登录上线；HR 数据从未穿过场馆系统。
- Honest caveat / 诚实提示: the privacy split is a contract + tech joint control; tech alone cannot enforce it — the contract is the backbone. / 隐私拆分是「合同 + 技术」共同控制；单靠技术执行不了——合同是脊梁。

---

## ⑥ Transferable lessons / 可迁移经验 {#case-06-lessons}

- Corporate gym's core design is the privacy split, not the hardware. / 企业健身房的核心设计是隐私拆分，不是硬件。
- Employer pays → does NOT mean employer sees individuals (HI-1/HI-7). / 雇主出钱 ≠ 雇主看个人（HI-1/HI-7）。
- Report AGGREGATE utilization; never individual rows to the client. / 给客户报「聚合用量」；绝不含个人行。
- HRIS nightly sync auto-revokes leavers — beats monthly CSV. / HRIS 夜间同步自动撤离职者——胜过月度 CSV。
- SSO stall is solved by SCOPING, not by waiting. / SSO 卡顿靠「范围化」解，不是干等。
- Integration-first, AI-later — corporate gym needs no churn AI. / 集成优先、AI 靠后——企业健身房不需要流失 AI。
- Put the privacy split in the contract, not just the config. / 隐私拆分写进合同，而非仅写进配置。
- Confirm HRIS/SSO API scope via `tools/04` before build to avoid 3-month stalls. / 建设前经 `tools/04` 确认 HRIS/SSO API 范围，避免 3 个月卡顿。

---

## ⑦ Related files / 相关文件 {#case-07-related}

- `references/02-club-formats-and-zones.md#format-corporate` · `#zone-gate` · `#zone-staffoffice` · `#zone-reception`
- `references/18-integration-and-data-plumbing.md` · `references/10-apac-compliance-east-asia-oceania.md` (PDPO) · `tools/05-regulation-traceability-verification.md` · `tools/04-dynamic-intelligence-retrieval.md`
- `data/21-anti-pattern-library.md#ap-employer-attendance-demand` · `#ap-sso-stall`
- `data/02-regulation-traceability-index.md` (PDPO boundary) · `data/01-kpi-benchmark-library.md` · `references/19-growth-and-sales-stack.md`

---

## ⑧ G13 tri-perspective note / G13 三视角覆盖说明 {#case-07-g13}

**Architect / 架构**: HRIS sync + scoped SSO + aggregate-only reporting — privacy encoded in the data flow. / HRIS 同步 + 范围化 SSO + 仅聚合报表——隐私写进数据流。
**Operator / 商家**: GM runs eligibility automatically; client reporting is a clean aggregate dashboard. / 总经理自动跑资格；客户报表是干净的聚合看板。
**Member / 会员 (employee)**: individual attendance stays private; no employer surveillance. / 个人考勤保密；无雇主监控。
No orphan touchpoint — the privacy split is honored across architecture, operator reporting, and member right. / 无孤儿触点——隐私拆分在架构、运营报表、会员权利三处一致。
