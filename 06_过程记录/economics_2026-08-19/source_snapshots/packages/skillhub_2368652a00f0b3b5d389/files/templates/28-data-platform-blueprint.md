# Data Platform / Mid-Office Blueprint / 数据平台与中台蓝图

> **Cluster / 集群**: K (AI governance & cloud sovereignty) + N (integration) + E (data)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Cloud-region & cost benchmarks 🔄 re-verify via `tools/04`; data-residency rules via `tools/05`.
> **Cross-references / 交叉引用**: `references/13-data-and-llm-engine.md#k-32-member-360` · `references/18-integration-and-data-plumbing.md` · `references/13-data-and-llm-engine.md#k-14-reference-architecture` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04`/`tools/05` before relying on them.

---

## ① Purpose & when to use / 用途与适用时机

**Use this blueprint to plan a club's data foundation — from a spreadsheet master to a CDP** — and to avoid the #1 data mistake: building a warehouse before the systems are integrated.
**用本蓝图规划场馆数据底座——从表格主表到 CDP**——并避免头号数据错误：系统未打通就建数仓。

> **FDMM gate / FDMM 门槛**: A **full data platform/warehouse is an FDMM L3–L5 investment**. Most AI use cases need FDMM ≥ L3 data readiness (`references/13#k-13-bi-dashboards`).
> **FDMM 门槛**：**完整数据平台/数仓是 FDMM L3–L5 投资**。多数 AI 用例需 FDMM ≥ L3 数据就绪（`references/13#k-13-bi-dashboards`）。

> **If below the gate / 若未达门槛**: do NOT build a platform. At L1–L2 use a spreadsheet master + your membership SaaS reports + basic BI (`references/13#k-11-spreadsheets`). Collect data only when a `references/04` use case demands it — data for data's sake is HI-8.
> **若未达门槛**：勿建平台。L1–L2 用表格主表+会籍 SaaS 报表+基础 BI（`references/13#k-11-spreadsheets`）。仅当 `references/04` 某用例需要才采集——为数据而数据是 HI-8。

---

## ② Prerequisites checklist / 前置条件清单

- [ ] **Membership SaaS live** with exportable data (L1→L2 gate). / 会籍 SaaS 上线且可导出（L1→L2 门槛）。
- [ ] **Stable primary key** per member (phone/email). / 每会员稳定主键（手机/邮箱）。
- [ ] **≥3 systems identified** for L3 integration target. / L3 集成目标已定 ≥3 系统。
- [ ] **Consent captured at signup** (marketing/biometric/health separate). / 注册时采集同意（营销/生物/健康分开）。
- [ ] **A named data owner** (even part-time at L3). / 已指定数据负责人（L3 可兼职）。
- [ ] **Residency expectation** known per market (§3.6). / 各市场驻留预期已知（§3.6）。

---

## ③ THE TEMPLATE / 模板

### 3.1 Current data-source inventory grid / 当前数据源清单网格 {#d1-source-inventory}

> Map what you have today before designing what to build.
> 设计前先盘点现有。

| Source / 源 | Data / 数据 | Format / 格式 | Owner / 负责人 | Exportable? / 可导出? |
|---|---|---|---|---|
| Membership SaaS / 会籍SaaS | profile, tier / 档案档位 | API/CSV | CS | ☐Y ☐N |
| POS / 收银 | payments / 支付 | CSV | finance | ☐Y ☐N |
| Gate / 闸机 | entries / 进场 | webhook | ops | ☐Y ☐N |
| Booking / 约课 | attendance / 出勤 | API | ops | ☐Y ☐N |
| Wearable / 可穿戴 | activity / 活动 | API | coach | ☐Y ☐N |
| Survey / 调研 | NPS/CSAT | export | CS | ☐Y ☐N |

### 3.2 Member-360 canonical model worksheet / 会员360 标准模型工作表 {#d2-member-360}

> Grow into this minimal schema (`references/13#k-32-member-360`). Fill which fields you have today.
> 渐进落地此极简 schema（`references/13#k-32-member-360`）。填你今天有哪些字段。

```
member_id (PK)                     [ have? ☐ ]
├─ identity: phone, email, im_ids[], card_id, face_template_ref?
├─ consents: marketing(opt-in+date), biometric(legal_basis), health(only_if_given)
├─ profile: age_band, gender, goals[], join_date, home_club
├─ behavior: visit_count_30d, class_attendance[], last_visit, app_opens_30d
├─ commerce: tier, mrr, ltv, stored_value_balance, pt_sessions_left
├─ risk: churn_score?, at_risk_flag?
└─ feedback: nps?, csat?, review_sentiment?
```

- **Sensitive-tag ban list (K3)**: no health-diagnosis tag, no pregnancy inference, no medical inference without explicit consent. / 敏感标签禁单（K3）：禁健康诊断标签、禁孕产推断、禁医疗推断（无明确同意）。
- Store `face_template_ref` (reference), never raw biometric; local-first where market demands (HI-8/HI-1). / 存「模板引用」非原始生物特征；按市场本地优先（HI-8/HI-1）。

### 3.3 ID-mapping strategy (one member, five IDs) / 身份归一策略（一人五 ID） {#d3-id-mapping}

> The "one member, five IDs" problem: the same person appears as phone, email, WeChat unionid, membership card, and face template — fragmented journeys and duplicate churn scores.
> 「一人五 ID」问题：同一人分散为手机、邮箱、微信 unionid、会员卡、人脸模板——旅程断裂、流失分重复。

- **Strategy / 策略**: pick ONE stable primary key; map every other ID to it (ID-resolution, `references/18-integration-and-data-plumbing.md`).
- **Rule / 规则**: merge duplicates (same person, two phones); never profile a member from fragmented IDs.
- **HI-8**: map only what the purpose needs; do not collect IDs "just in case". / 仅映射目的所需；勿「以防万一」采集 ID。

### 3.4 Dashboard requirement cards per role / 按角色的看板需求卡 {#d4-dashboards}

| Role / 角色 | Top question / 核心问题 | Must-show / 必显指标 | Cadence / 频率 |
|---|---|---|---|
| Owner / 老板 | "Am I growing?" / 在增长吗 | MRR, churn%, LTV, CAC / 月经常性收入、流失%、LTV、CAC | weekly / 周 |
| Store manager / 店长 | "Is today healthy?" / 今天健康吗 | attendance, no-show, fill-rate, complaints / 出勤、爽约、满课率、投诉 | daily / 日 |
| Coach lead / 教练主管 | "Are my clients retained?" / 学员留住吗 | per-coach attendance, pt renewal / 各教练出勤、私教续费 | weekly / 周 |
| HQ / 总部 | "Which store lags?" / 哪家掉队 | cross-store benchmark, funnel / 跨店基准、漏斗 | monthly / 月 |

> Lock a metric dictionary (churn definition!) before building — inconsistency across stores is the silent killer (`references/13#k-91-quality-dimensions`). / 建前先锁指标口径（含流失定义！）——各店口径不一为隐形杀手。

### 3.5 Build sequence by FDMM level / 按 FDMM 等级的构建顺序 {#d5-build-sequence}

| FDMM / 等级 | Build / 构建 | Do NOT / 勿做 |
|---|---|---|
| L1 | spreadsheet master + weekly POS↔gate reconciliation / 表格主表+每周 POS↔闸机对账 | no cloud yet / 暂不需云 |
| L2 | membership SaaS + basic BI + consent capture / 会籍SaaS+基础BI+注册采同意 | no siloed CSVs / 无孤岛CSV |
| L3 | light warehouse + event tracking + 1 production AI + registry / 轻量数仓+事件埋点+1个量产AI+注册表 | no warehouse before 3 systems / 未打通先不建仓 |
| L4 | CDP + model monitoring + residency ledger / CDP+模型监控+驻留账 | no untracked model / 无追踪模型 |
| L5 | group data platform + automated activation + quarterly governance / 集团数据平台+自动激活+季度治理 | no purpose-less collection / 无目的采集 |

### 3.6 Cost envelope 🔄 / 成本区间 {#d6-cost}

:::dynamic-hook topic="data-platform-cost-apac" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07 (ranges, verify via tools/04; per club/month at L3): warehouse compute+storage ¥200–¥800; BI ¥0 (built-in)–¥50/seat; LLM bot tokens ¥50–¥300 low-volume; CDP (L5) ¥1,000+/mo at chain scale. Costs vary by rows, region, and vendor — treat as a planning range, not a quote. / 截至 2026-07（区间，经 tools/04 核；L3 每馆每月）：数仓算力存储 200–800；BI 0（内置）–50/席；大模型机器人 token 50–300 低量；CDP（L5）连锁级 1000+/月。随数据量、区域、供应商而变——作规划区间非报价。
:::

> Rule / 守则: data spend must tie to a use-case ROI (`tools/06`); idle warehouse = waste. / 数据支出须绑定用例 ROI（tools/06）；闲置数仓=浪费。

### 3.7 Residency ledger example row / 驻留账示例行 {#d7-residency-row}

> One row per club makes §3.6 auditable (`references/13#k-12-residency-ledger`). / 每馆一行使 §3.6 可审计（`references/13#k-12-residency-ledger`）。

```
club_id, market, cloud, region, biometric_stored, biometric_residency, xborder_mechanism, last_review, owner
C001, CN, Aliyun, cn-hangzhou, yes, onshore, PIPL-SCC, 2026-07, data-owner
C002, SG, AWS, ap-southeast-1, no, n/a, PDPA-accountability, 2026-07, data-owner
```
> 🔄 Verify available regions per provider via `tools/04` before committing residency. / 🔄 承诺驻留前经 tools/04 核各供应商可用区域。

> Keep the ledger invertible: every layer must support data export (HI-9) so you are never locked in. / 账须可逆：每层须支持数据导出（HI-9），永不锁定。

---

## ④ Common mistakes / 常见误区

- **Warehouse before 3 systems integrated** → drift, no trust. / 未打通先建仓→漂移无信任。
- **No primary key** → duplicate members, broken journeys. / 无主键→重复会员、旅程断裂。
- **Collecting before a use case** → HI-8 breach. / 无用例先采集→HI-8 违规。
- **Model in prod with no owner** → silent bias/drift. / 无主模型上线→静默偏见/漂移。
- **Ignoring residency** → cross-border violation. / 忽视驻留→跨境违规。

> Full remedy catalogue: `data/21-anti-pattern-library.md`.
> 完整对策：见 `data/21-anti-pattern-library.md`。

---

## ⑤ Related files / 相关文件

- `references/13-data-and-llm-engine.md#k-32-member-360` — canonical model + sensitive ban. / 标准模型+敏感禁单。
- `references/13-data-and-llm-engine.md#k-14-reference-architecture` — layering view. / 分层视图。
- `references/18-integration-and-data-plumbing.md` — ID resolution, ingestion. / 身份归一、接入。
- `references/13-data-and-llm-engine.md#k-12-residency-ledger` — residency ledger. / 驻留账。
- `tools/06-roi-three-scenario.md` — platform ROI. / 平台 ROI。

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: staged build by FDMM (never L4 solution to L1), member-360 canonical model, ID-resolution strategy, residency ledger, cost ranges via tools/04.
- **Operator / 运营者**: source inventory, role-based dashboards, metric dictionary lock, named data owner — prevents over-spend and drift.
- **Member / 会员**: minimisation (HI-8), sensitive-tag ban (K3), consent separation, no raw biometric stored, residency protects their data across borders.
本文件覆盖架构师（按 FDMM 分阶构建、会员360 标准模型、身份归一策略、驻留账、成本区间经 tools/04）、运营者（源清单、按角色看板、指标口径锁、数据负责人——防过度投入与漂移）、会员（最小化 HI-8、敏感标签禁单 K3、同意分离、不存原始生物特征、驻留保护跨境数据）。
