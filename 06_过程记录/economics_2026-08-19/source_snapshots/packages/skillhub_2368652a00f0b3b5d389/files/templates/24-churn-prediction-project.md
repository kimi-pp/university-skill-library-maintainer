# Churn Prediction Project Charter / 流失预测项目章程

> **Cluster / 集群**: E (Data & AI) + K (AI governance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Bias/protected-group and prepaid rules re-verify via `tools/05` before citing; vendor churn-module claims 🔄 re-verify via `tools/04`.
> **Cross-references / 交叉引用**: `data/09-algorithm-kernel-library.md#algo-churn` · `references/13-data-and-llm-engine.md#k-53-bias-audit` · `references/04-ai-application-landscape.md#ai-04-churn-prediction` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.

---

## ① Purpose & when to use / 用途与适用时机

**Use this charter to scope, build-govern, and operate a member churn (non-renewal) prediction model — from problem framing to monitoring.** It is the #1 AI use case for retention ROI, but also the #1 failure when "churn" is never defined.
**用本章程界定、治理并运营「会员流失（不续费）预测模型」——从问题定义到上线监控。** 它是留存 ROI 第一的 AI 用例，但也是「从没定义过流失」时失败率第一的用例。

> **FDMM gate / FDMM 门槛**: Churn modelling requires **FDMM ≥ L3** (≥3 systems integrated, identity unified, data platform live). It also needs **≥2,000 active members × ≥6 months of behaviour + renewal history** (`data/09#algo-churn`).
> **FDMM 门槛**：流失建模要求 **FDMM ≥ L3**（≥3 系统打通、身份归一、数据中台在线），且需 **≥2,000 活跃会员 × ≥6 月行为+续费历史**（`data/09#algo-churn`）。

> **If you are below the gate / 若未达门槛**: Do NOT build a model. Use a transparent **rule** instead — "no visit in 21 days → coach nudge" — which is honest, free, and often beats a fragile model on small data (Iron Law 10). Revisit modelling only after crossing the data floor.
> **若未达门槛**：不要建模。改用透明**规则**——「21 天没来 → 教练提醒」——它诚实、免费，且在小数据上常胜过脆弱模型（铁律10）。跨过数据底线后再考虑建模。

---

## ② Prerequisites checklist / 前置条件清单

- [ ] **Member count ≥ 2,000 active** (else → rules, not ML). / 活跃会员 ≥ 2,000（否则用规则非 ML）。
- [ ] **Behaviour history ≥ 6 months** exportable per member (visits, bookings, app opens, payments). / 每会员可导出 ≥6 月行为历史（到店、约课、App 打开、缴费）。
- [ ] **Renewal/cancel outcome label** exists and is consistent across stores. / 续费/退会结果标签存在且各店口径一致。
- [ ] **Stable primary key** so one member is never duplicated (ID resolution done, `references/13#k-32-member-360`). / 稳定主键，会员不重复（身份归一完成）。
- [ ] **Marketing consent captured per member** (churn-save outreach needs it — HI-7). / 每会员已采集营销同意（挽留触达需要，HI-7）。
- [ ] **A named model owner** assigned (never "the system", `references/13#k-51-model-registry`). / 已指定模型负责人（绝不说「系统」）。
- [ ] **Protected-group attributes** inventoried for the bias audit (see §3.6). / 已盘点受保护群体属性供偏见审计（见 §3.6）。

> **Data-volume honesty / 数据量诚实**: "<500 members = use rules, not ML" — a model on 300 members will memorize noise and lie to you. This is not a limitation to hide; it is the honest floor.
> **数据量诚实**：「会员 <500 用规则别上 ML」——300 人的模型只会记噪声、骗你。这不是要掩盖的限制，而是诚实底线。

---

## ③ THE TEMPLATE / 模板

### 3.1 Problem framing & churn definition worksheet / 问题框定与流失定义工作表 {#c1-problem-framing}

> **The #1 failure / 头号失败**: teams build a model before agreeing what "churn" means. Fill this FIRST; every later number depends on it.
> **头号失败**：团队先建模、却没对齐「流失」定义。先填这张；后面所有数字都取决于它。

| Field / 字段 | Fill in / 填写 | Example / 示例 |
|---|---|---|
| Churn event = / 流失事件 = | member status at date X / X 日会员状态 | `renewal_not_paid` within 30d of expiry / 到期 30 天内未续费 |
| Observation window / 观察窗 | days of history used / 用多少天历史 | 180 days / 180 天 |
| Prediction horizon / 预测前瞻 | how far ahead we score / 提前多久打分 | 30–60 days before expiry / 到期前 30–60 天 |
| Label source / 标签来源 | system field / 系统字段 | `membership.status` + `renewal_date` / 会籍状态+续费日 |
| Exclusions / 排除项 | who is NOT in scope / 谁不在范围 | frozen/paused, corporate bulk, <30d tenure / 冻结、企业团单、会龄<30天 |
| Churn rate (baseline) / 流失率基线 | % per period / 每期% | ___% (compute from last 4 cohorts) / 近 4 期计算 |

> **Micro-example / 微例**: "Churn = a paying member whose `renewal_date` passed with `status≠active` and no new contract in 30 days, excluding medical freezes." Without the exclusion, a maternity pause looks like churn and poisons the label.
> **微例**：「流失 = 付费会员 `renewal_date` 已过且 `status≠active`、30 天内无新合同，排除医疗冻结。」不写排除项，孕产暂停会被当成流失，毒化标签。

### 3.2 Data audit checklist / 数据审计清单 {#c2-data-audit}

| Data domain / 数据域 | Available? / 有? | Quality OK? / 质量OK? | Owner / 负责人 | Note / 备注 |
|---|---|---|---|---|
| Visit frequency & decay / 到访频率与衰减 | ☐Y ☐N | ☐Y ☐N | | |
| Booking gaps / 约课间隔 | ☐Y ☐N | ☐Y ☐N | | |
| Payment-fail count / 扣费失败次数 | ☐Y ☐N | ☐Y ☐N | | |
| Class attendance series / 出勤序列 | ☐Y ☐N | ☐Y ☐N | | |
| Last-visit gap / 最后到访间隔 | ☐Y ☐N | ☐Y ☐N | | |
| App / wearable engagement / App/可穿戴互动 | ☐Y ☐N | ☐Y ☐N | | |

> **Leakage warning / 泄漏警告**: never use `renewal_date` or "renewed?" as a feature — that is the label. Using it = cheating the score (see `data/09#algo-churn` failure modes).
> **泄漏警告**：绝不能用 `renewal_date` 或「续费了？」当特征——那是标签。用它=作弊分数（见 `data/09#algo-churn` 失败模式）。

### 3.3 Feature candidate list / 特征候选清单 {#c3-feature-candidates}

```
Candidate features (score each for actionability + leakage risk):
候选特征（为每个评估"可行动性 + 泄漏风险"）：
1. visit_count_30d            actionability: HIGH  leakage: NONE
2. visit_count_30d vs 90d avg (decay ratio)   actionability: HIGH  leakage: NONE
3. days_since_last_visit      actionability: HIGH  leakage: NONE
4. class_booking_gap_days     actionability: MED   leakage: NONE
5. payment_fail_count_90d     actionability: MED   leakage: NONE
6. app_opens_30d              actionability: LOW   leakage: NONE
-- PROTECTED: do NOT use as features (bias audit, §3.6) --
受保护：不得作特征（偏见审计 §3.6）
   gender, age_band (if proxy), health_flag, maternity/pause_reason
```

> Full method + eval detail: `data/09-algorithm-kernel-library.md#algo-churn`.
> 完整方法+评估：见 `data/09-algorithm-kernel-library.md#algo-churn`。

### 3.4 Build-vs-buy decision / 自建还是采购决策 {#c4-build-vs-buy}

| Your situation / 你的情况 | Verdict / 结论 |
|---|---|
| L1–L2, any size / 任意规模 | **Buy** MMS-built-in churn module (Iron Law 8: ≥3 options). / 买 MMS 内置流失模块（铁律8：≥3 选项）。 |
| L3+, ≥2k members, has data engineer / 有数据工程师 | Build viable; else **buy**. / 可自建；否则买。 |
| L3+, <2k members / 会员<2k | **Rules**, not ML. / 用规则非 ML。 |

- Vendor lock-in check / 锁定风险: confirm data-export clause (HI-9) before signing. / 签约前确认数据导出条款（HI-9）。
- ≥3 options incl. one local-market + one low-cost/open option. / ≥3 选项，含本地市场与低成本/开源各一。

### 3.5 Evaluation plan / 评估计划 {#c5-evaluation}

| Metric / 指标 | Floor / 底线 | How measured / 怎么测 |
|---|---|---|
| AUC / ROC | **≥ 0.75 on holdout** / 留存集≥0.75 | stratified split, never on training data / 分层切分，绝不在训练集 |
| Calibration / 校准 | predicted prob ≈ actual rate / 预测概率≈实际率 | reliability curve by decile / 按十分位可靠曲线 |
| Precision@k / 前k精确率 | budget-driven / 由预算定 | of flagged k, true churners / 标记 k 人中真流失 |

> **Honesty red line / 诚实红线**: We do NOT promise "X% accuracy." AUC 0.75 means "ranks risk better than coin-flip" — it is a ranking aid, not a verdict. State ranges, not single points (G8).
> **诚实红线**：我们不承诺「X% 准确率」。AUC 0.75 意为「排序风险优于抛币」——是排序辅助，非定论。给区间非单点（G8）。

### 3.6 BIAS AUDIT (mandatory) / 偏见审计（强制） {#c6-bias-audit}

> **Mandatory section — a churn model without a bias audit is not production-ready (HI-7 / K).** A model trained on history may learn "paused-for-medical/maternity cancel more" and silently down-score protected groups.
> **强制章节——未经偏见审计的流失模型不得量产（HI-7 / K）。** 按历史训练的模型可能学出「医疗/孕产暂停者更易退会」并静默降权受保护群体。

| Protected group / 受保护群体 | Attribute / 属性 | Check / 检查 | Result / 结果 |
|---|---|---|---|
| Gender / 性别 | gender | score parity across segments / 跨段分数公平 | ☐ pass ☐ fail |
| Age band / 年龄段 | age_band (proxy) | recall not lower for seniors / 老年召回不更低 | ☐ pass ☐ fail |
| Minors / 未成年 | is_minor | excluded from scoring / 排除出打分 | ☐ pass ☐ fail |
| Health / 健康 | health_flag | **never a feature** / 绝不作特征 | ☐ pass ☐ fail |

:::dynamic-hook topic="protected-attributes-per-market" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07: protected attributes vary by market (e.g. age/gender/disability under various APAC privacy & anti-discrimination laws) — verify the exact protected-class list for your market via tools/05 before the audit. / 截至 2026-07：受保护属性因市场而异（如各亚太隐私与反歧视法下的年龄/性别/残障）——审计前经 tools/05 核验你市场的确切受保护类清单。
:::

### 3.7 Action-playbook design (what staff DO with scores) / 动作规程设计（员工拿分数做什么） {#c7-action-playbook}

> A score with no playbook sits unused — the most common "successful model, zero impact" trap.
> 有分数无规程=闲置——最常见的「模型成功、影响为零」陷阱。

| Score band / 分数段 | Trigger / 触发 | Who acts / 谁执行 | Action / 动作 |
|---|---|---|---|
| High risk (top 10%) / 高危 | weekly export / 周导出 | Advisor / 顾问 | consent-led SCRM nudge → coach call (HI-7) / 同意制提醒→教练致电 |
| Medium / 中危 | monthly / 月 | Front desk / 前台 | personalised class invite / 个性化约课邀请 |
| Low / 低危 | — | — | no action / 不动作 |

> HI-7: every save outreach needs opt-in consent; honour unsubscribe. / HI-7：每次挽留触达需 Opt-in 同意；尊重退订。

### 3.8 Monitoring & retraining schedule / 监控与重训排期 {#c8-monitoring}

| Cadence / 频率 | Signal / 信号 | Action / 动作 | Owner / 负责人 |
|---|---|---|---|
| Weekly / 周 | score-distribution shift / 分数分布偏移 | investigate / 查因 | data owner |
| Monthly / 月 | bias metric / 偏见指标 | registry note / 注册表记 | governance |
| Quarterly / 季 | full retrain / 全量重训 | champion/challenger 30d / 新旧对照30天 | data owner |

> **⚠ Promo-month contamination warning / 促销月污染警告**: during promo months (New-Year, double-month deals, freeze campaigns) the churn label gets corrupted — members who "lapsed" were actually on a paid pause. **Exclude promo windows from training labels and annotate them**, or the model will learn wrong churn signals. Re-baseline after each promo season.
> **⚠ 促销月污染警告**：促销月（新年、双月特惠、冻结活动）流失标签会被污染——「流失」的会员其实在付费暂停。**从训练标签排除促销窗口并标注**，否则模型会学错流失信号。每促销季后重基线。

---

## ④ Common mistakes / 常见误区

- **Undefined churn** → everything downstream is wrong (see `data/21-anti-pattern-library.md`). / 流失未定义→下游全错。
- **Leaky label** (using renewal as feature) → inflated, fake AUC. / 标签泄漏→虚高假 AUC。
- **Modelling <2k members** → noise memorisation, not prediction. / <2k 建模→记噪声非预测。
- **No bias audit** → silent discrimination, compliance liability. / 无偏见审计→静默歧视、合规负债。
- **Score with no playbook** → zero business impact. / 有分数无规程→零业务影响。
- **Promo-month contamination** → model learns pause as churn. / 促销月污染→模型把暂停当流失。

> Full remedy catalogue: `data/21-anti-pattern-library.md`.
> 完整对策：见 `data/21-anti-pattern-library.md`。

---

## ⑤ Related files / 相关文件

- `data/09-algorithm-kernel-library.md#algo-churn` — method, eval, build-vs-buy, min-data. / 方法、评估、建买、最小数据。
- `references/13-data-and-llm-engine.md#k-53-bias-audit` — bias audit case & mitigation. / 偏见审计案例与缓解。
- `references/13-data-and-llm-engine.md#k-51-model-registry` — model ownership. / 模型归属。
- `references/04-ai-application-landscape.md#ai-04-churn-prediction` — use-case scope & flags. / 用例范围与标记。
- `tools/06-roi-three-scenario.md` — retention ROI three scenarios. / 留存 ROI 三情景。

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: FDMM L3 gate + ≥2k×6mo data floor + AUC 0.75 + mandatory bias audit + model registry entry — no L4 solution prescribed to an L1 club (Iron Law 7).
- **Operator / 运营者**: churn-definition worksheet, rule fallback below gate, action playbook so scores convert to retained members, promo-month guard.
- **Member / 会员**: protected-group fairness (HI-7/K), consent-led save outreach (HI-7), no discrimination by health/gender/age, transparent ranking not verdict.
本文件覆盖架构师（FDMM L3 门槛+≥2k×6月底线+AUC0.75+强制偏见审计+注册表；绝不给 L1 馆上 L4 方案，铁律7）、运营者（流失定义工作表、门槛下规则兜底、动作规程把分数变留存、促销月护栏）、会员（受保护群体公平 HI-7/K、同意制挽留 HI-7、不因健康/性别/年龄歧视、透明排序非定论）。
