# Digitalization Charter & Stage-Gate / 数字化章程与阶段门

> **Cluster / 集群**: I (governance & money), X (methodology)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: regulation red lines re-verify via `tools/05` before each investment gate; vendor decision rights fixed at charter sign but reviewed annually. / 合规红线在每个投资门前经 `tools/05` 复核；供应商决策权于章程签署时固定、年度复审。
> **Cross-references / 交叉引用**: `tools/07-chief-orchestrator.md` (S1–S8 pipeline) · `references/05-methodology-library.md` §2 · `templates/02-annual-it-budget.md` (approval) · `templates/07-roi-business-case.md` (investment gate) · `SKILL.md` HI-1~HI-8
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04`。

---

## ① Purpose & When to Use / 用途与使用时机 {#purpose}

Write this one-page charter BEFORE any digital purchase, and attach the S1–S8 Stage-Gate definitions so every project follows the same lifecycle. It is the guardrail against ad-hoc, skip-stage IT failure (Iron Law 5).
在任何数字化采购前写这份一页章程，并附 S1–S8 阶段门定义，让每个项目走同一生命周期。它是防止临时起意、跳阶段 IT 失败（铁律 5）的护栏。

> **FDMM level gate / 成熟度闸口**: **Any level — write it at L1 before the first SaaS.** The charter is the cheapest insurance you will ever buy. It only grows in detail as you scale.
> **FDMM 等级闸口**：**任何等级——L1 首套 SaaS 前就写**。章程是你买过最便宜的保险，仅随规模增细。

> **What good looks like / 好答案长什么样**: the charter names what you will NOT do (HI red lines + no surveillance in lockers + no diagnosis), who approves which spend tier, and the S1–S8 gates each carry an explicit exit checklist.
> **好答案长什么样**：章程写明绝不做什么（HI 红线+更衣室不监控+不做诊断）、谁批哪档支出、且 S1–S8 每门带明确退出清单。

> **Red flag / 红旗**: a charter with "approver: whoever is free" or missing HI-5/HI-6 → reject. See `data/21-anti-pattern-library.md#ap-006`, `#ap-007`. / 审批人写「谁有空谁批」或漏 HI-5/HI-6 → 驳回。见 `data/21#ap-006`、`#ap-007`。

---

## ② Prerequisites & Inputs Checklist / 前置条件与输入清单 {#prerequisites}

- [ ] Confirmed club format + target market(s). / 已确认业态 + 目标市场。
- [ ] HI-1~HI-8 red lines pasted from `SKILL.md`. / 从 `SKILL.md` 粘贴 HI-1~HI-8 红线。
- [ ] Current FDMM level via `tools/01`. / 经 `tools/01` 知当前 FDMM 等级。
- [ ] Named people for owner / approver / esc creator. / 具名负责人/审批人/升级触发人。
- [ ] `templates/02` ready for the approval thresholds. / `templates/02` 备好审批阈值。

---

## ③ The Template / 模板正文 {#template}

### 3.1 Charter — Scope & Red Lines / 章程：范围与红线 {#s-charter}

| Field / 字段 | Fill-in / 填写 |
|---|---|
| Why we digitize / 数字化目的 | ___ (member value + business resilience, not hype) |
| In scope / 范围内 | ___ |
| Out of scope — NEVER / 范围外（绝不） | no imaging in changing rooms (HI-5); no health diagnosis (HI-6); no IT control of fire (HI-4) |
| Data principle / 数据原则 | minimization + local-first biometric (HI-1, HI-8, HI-9) |
| Comms principle / 触达原则 | opt-in only, anti-spam law (HI-7) |

### 3.2 Decision Rights — Who Approves What Spend / 决策权：谁批哪档支出 {#s-rights}

| Spend tier / 支出档 | Examples / 例 | Approver / 审批人 |
|---|---|---|
| < ¥__ (small) / 小 | cable, mouse, SaaS add-on / 线、鼠标、SaaS 增项 | One-person IT / 一人 IT |
| ¥__–¥__ (mid) / 中 | POS refresh, locker bank / POS 换新、柜组 | Club owner / 老板 |
| > market ¥100k equiv / 大 | gates, SD-WAN, AI platform / 闸机、SD-WAN、AI 平台 | Board + ROI (`templates/07`) / 董事会+ROI |

> Decision rights MUST align with `templates/02` §3.5. No tier without a named approver.
> 决策权须与 `templates/02` §3.5 对齐。任何档都须具名审批人。

### 3.3 Stage-Gate S1–S8 Definitions / 阶段门 S1–S8 定义 {#s-gates}

> Aligned with `tools/07` pipeline: Diagnose → Strategy → Selection → Investment → Implementation → Go-live → Operations → Retrospective.
> 与 `tools/07` 流水线一致：诊断→战略→选型→投资→实施→上线→运营→复盘。

| Gate / 门 | Name / 名 | Entry / 入口 | Exit checklist (all ✓ to pass) / 退出清单（全 ✓ 才过） |
|---|---|---|---|
| S1 | Diagnose / 诊断 | symptom or goal / 症状或目标 | FDMM scored (`tools/01`); gap listed / 已评分；缺口列 |
| S2 | Strategy / 战略 | FDMM + goal / 等级+目标 | initiative mapped to horizon; envelope sized / 举措挂时区；投资包定量 |
| S3 | Selection / 选型 | shortlist / 候选 | ≥3 options, data-export checked (Iron Law 8) / ≥3 选项，导出已查 |
| S4 | Investment / 投资 | vendor quote / 报价 | ROI 3-scenario (`templates/07`); HI scan clean / ROI 三情景；HI 干净 |
| S5 | Implementation / 实施 | signed / 已签约 | plan + owner + rollback; CCTV zone check / 计划+负责人+回滚；禁区核 |
| S6 | Go-live / 上线 | built / 建成 | pilot passed (`templates/08`); training done / 试点过；培训完 |
| S7 | Operations / 运营 | live / 已上线 | RACI active (`templates/06`); monitoring on / RACI 生效；监控开 |
| S8 | Retrospective / 复盘 | quarter end / 季末 | ROI realized vs promised; lessons logged / 实现 vs 承诺；教训记 |

> **Red flag / 红旗**: skipping S4 (no ROI) for a >¥100k buy → Iron Law 6 breach. Send back to S3/S4.
> **红旗**：>10 万采购跳过 S4（无 ROI）→ 违反铁律 6。退回 S3/S4。

### Exit Criteria Quick-Check / 退出清单速查 {#s-exit}

> Use this at every gate review meeting. Tick all before proceeding.
> 每门评审会用。全勾才前进。

- [ ] S1 FDMM evidence attached? / S1 附 FDMM 证据？
- [ ] S2 horizon map updated? / S2 时区地图更新？
- [ ] S3 ≥3 vendors, export clause? / S3 ≥3 供应商、导出条款？
- [ ] S4 ROI 3-scenario signed? / S4 ROI 三情景签字？
- [ ] S5 rollback plan exists? / S5 回滚计划存在？
- [ ] S6 pilot + training done? / S6 试点+培训完成？
- [ ] S7 RACI + monitoring live? / S7 RACI+监控在线？
- [ ] S8 lessons fed to next S1? / S8 教训喂回下轮 S1？

### 3.4 Escalation Paths / 升级路径 {#s-escalation}

| Trigger / 触发 | Escalate to / 升级至 | Within / 时限 |
|---|---|---|
| HI-1~HI-8 breach suspected / 疑触红线 | Owner + counsel / 老板+法务 | 24h |
| Spend > approved tier / 超批档 | Board / 董事会 | immediate / 立即 |
| Vendor refuses data export / 供应商拒导出 | Charter owner + switch plan / 章程主+切换预案 | 48h |

---

### 3.5 Charter Sign-Off Checklist / 章程签署清单 {#s-signoff}

> Do not purchase anything until every box is ticked. The charter is signed once and reviewed annually.
> 勾满前不采购。章程签一次、年度复审。

- [ ] Vision stated in member-value + resilience terms (not hype). / 愿景以会员价值+韧性表述（非噱头）。
- [ ] Out-of-scope NEVER list includes HI-4/HI-5/HI-6. / 范围外「绝不」含 HI-4/HI-5/HI-6。
- [ ] Decision rights table complete with named approvers per tier. / 决策权表各档具名审批人完整。
- [ ] S1–S8 each has an exit checklist. / S1–S8 各带退出清单。
- [ ] Escalation paths name a counsel contact for HI breaches. / 升级路径对 HI 违具名法务联系人。
- [ ] Signed & dated by owner. / 老板签字日期。

### 3.6 Worked Example — Decision Rights / 实例：决策权 {#s-example}

> A 3-club L3 operator's tiers (market ¥ equiv assumed): / 某 3 店 L3 运营者的档位（假定当地等值）：

| Spend tier / 支出档 | Examples / 例 | Approver / 审批人 |
|---|---|---|
| < ¥5k / 小 | mouse, cable, SaaS add-on / 鼠标、线、SaaS 增项 | One-person IT / 一人 IT |
| ¥5k–¥50k / 中 | POS refresh, locker bank / POS 换新、柜组 | Club owner / 老板 |
| > market ¥100k equiv / 大 | gates, SD-WAN, AI platform / 闸机、SD-WAN、AI 平台 | Board + ROI (`templates/07`) / 董事会+ROI |

> This operator once skipped the >tier sign-off on a ¥120k gate buy and later found no data-export clause — caught by `data/21-anti-pattern-library.md#ap-002`. The charter would have forced S3+S4. / 该运营者曾对 ¥120k 闸机采购跳过高档签字，后发现无数据导出条款——被 `data/21#ap-002` 抓出。章程本可强制 S3+S4。

### 3.7 Volatile-Fact Hook / 易变事实钩子 {#s-hook}

:::dynamic-hook topic="apac-fitness-regulation-amendments" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07, APAC fitness-sector regulations (biometric special rules, prepaid/consumer-protection, privacy amendments) change continuously across the 12 markets; verify the exact current articles via `tools/05` before each S4 investment gate and re-scan at charter annual review.
截至 2026-07，亚太健身业法规（生物识别特规、预付/消保、隐私修订）在 12 市场持续变动；每个 S4 投资门前经 `tools/05` 核验现行条款，章程年度复审时再扫。
:::

## ④ Common Mistakes / 常见错误 {#mistakes}

- **No charter before buying** → scope creep & lock-in. See `data/21-anti-pattern-library.md#ap-002`. / 采购前无章程 → 范围蔓延与锁定。
- **Skip S4 for big buys** → ROI blindness. See `#ap-002` + Iron Law 6. / 大采购跳 S4 → ROI 失明。
- **Camera in changing room** → HI-5 hard veto. See `data/21-anti-pattern-library.md#ap-006`. / 更衣室装监控 → HI-5 一票否决。
- **IT controls fire system** → HI-4. See `data/21-anti-pattern-library.md#ap-007`. / IT 控消防 → HI-4。

---

## ⑤ Related Files / 相关文件 {#related}

- `tools/07-chief-orchestrator.md` — S1–S8 engine. / S1–S8 引擎。
- `tools/01-fdmm-maturity-assessment.md` — S1 input. / S1 输入。
- `templates/02-annual-it-budget.md` — approval tiers. / 审批档。
- `templates/07-roi-business-case.md` — S4 input. / S4 输入。
- `templates/08-pilot-validation-plan.md` — S6 input. / S6 输入。
- `templates/06-digital-org-and-raci.md` — S7 input. / S7 输入。
- `SKILL.md` HI-1~HI-8 — red lines. / 红线。

---

## ⑥ G13 Tri-Perspective Note / 三视角覆盖备注 {#g13}

> **Architect** (charter + S1–S8 impose lifecycle discipline & HI guardrails) × **Operator** (decision rights + escalation give the solo steward clear authority & escape hatches) × **Member** (red-line clauses + opt-in principle protect member privacy & safety before any system ships). / **架构**（章程+S1–S8 强制生命周期纪律与 HI 护栏）× **商家**（决策权+升级给一人总管明确授权与退路）× **会员**（红线条款+Opt-in 原则在任何系统出货前保护会员隐私与安全）。
