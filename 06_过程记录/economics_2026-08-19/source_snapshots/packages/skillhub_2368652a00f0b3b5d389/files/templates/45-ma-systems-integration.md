# M&A Systems Integration Plan / 并购系统整合计划

> **Cluster / 集群**: I (IT governance & money) + G (governance) + B (software)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Consent-validity law 🔄 via `tools/05`; target systems contracts & lock-ins 🔄 via `tools/04`; old-system sunset link `templates/22`.
> **Cross-references / 交叉引用**: `tools/05-regulation-traceability-verification.md`, `data/21-anti-pattern-library.md#ap-002-no-data-export`, `templates/22-data-migration-plan.md`, `templates/42` (franchise data), `references/18-integration-and-data-plumbing.md`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this plan to **integrate the IT & data of an acquired club group** without losing members, breaking compliance, or inheriting locked-in contracts blindly.
本计划用于**整合被并购俱乐部集团的 IT 与数据**，不丢会员、不破合规、不盲继锁定合同。

- **FDMM gate / 等级闸门**: L2+ acquirer; any deal with ≥1 club & member DB.
  L2+ 收购方；凡 ≥1 店且含会员库。
- **Trigger / 触发**: LOI signed; run diligence before close.
  签意向书；交割前跑尽调。

---

## ② Prerequisites checklist / 前置清单

- [ ] Target system inventory requested. / 目标系统清单已索。
- [ ] Data-quality sample audit scoped. / 数据质量抽样审计已定。
- [ ] Compliance liabilities check started (`tools/05`). / 合规负债核查已启。
- [ ] Day-1 access plan drafted. / Day-1 权限方案已拟。
- [ ] Sunset plan linked to `templates/22`. / 退役方案链 templates/22。
- [ ] Integration RACI named. / 整合 RACI 已定。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Due-diligence IT & data checklist / 尽调 IT 与数据清单

| Item / 项 | Finding / 发现 | Risk / 风险 |
|---|---|---|
| Systems list 系统清单 | `____` | `____` |
| Contracts & lock-ins 合同锁定 | `____` | `____` |
| Data-quality sample 数据质量样 | `____`% valid | `____` |
| Compliance liabilities 合规负债 | `____` | `____` |
| Consent validity 同意有效性 | `____` | `____` |
| Cyber posture 网安态势 | `____` | `____` |

> **Stop-line / 停手线**: Undisclosed lock-in or invalid consent = reprice or walk.
> 停手线：隐瞒锁定或同意无效→重新定价或退出。

### 3.2 Day-1 requirements / Day-1 要求

- [ ] Access control to target systems granted to acquirer IT. / 收购方 IT 获目标系统权限。
- [ ] Payroll & staff comms continuity. / 薪资与员工沟通不断。
- [ ] Member comms template approved (no surprise "we sold you"). / 会员沟通模板已批（别惊现"我们卖了你"）。
- [ ] Emergency contact routing known. / 应急联络路由已知。
- [ ] Parallel-run window defined (`____` days). / 并行运行窗口已定。

### 3.3 Membership-system merge workbook / 会员系统合并手册

| Step / 步 | Action / 动作 |
|---|---|
| Dedup rules 去重 | match by `____` (phone+email), keep `____` |
| Balance reconcile 余额核对 | source vs target diff `____` |
| Consent RE-CAPTURE 同意重获 | cannot inherit — plan `____` |
| Communications 沟通 | notify + re-opt-in within `____` days |
| Loyalty merge 积分合并 | map `____` to `____` |

:::dynamic-hook topic="consent-inheritance-rule" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07: acquired consent is generally NOT inherited — re-capture required per market (`tools/05`). Verify exact rule.
截至 2026-07：并购所得同意一般不可继承——须按市场重获（tools/05）。具体规则核验。
:::

> **Red flag / 红线**: "We'll just copy the old DB and keep mailing" → breach.
> 红线："直接拷旧库继续发"→违规。

### 3.4 Integration sequencing & RACI / 整合时序与 RACI

| Phase / 阶段 | Owner / 责 | Exit crit / 退出标准 |
|---|---|---|
| Day-1 access & payroll 权限薪资 | Acq IT | access live |
| Data migration (templates/22) 数据迁移 | Data lead | reconciliation pass |
| Consent re-capture 同意重获 | Mktg/Legal | `____`% re-opt |
| Cutover & de-dupe 切换去重 | Ops | zero dup |
| Sunset old 退役旧 | IT | contract closed |

> **Guidance / 指引**: Parallel-run before cutover catches balance mismatches without member impact.
> 指引：切换前并行跑可抓余额差且不伤会员。

### 3.5 Old-system sunset plan / 旧系统退役方案

- Link to `templates/22-data-migration-plan.md` for migration detail. / 迁移细节链 templates/22。
- [ ] Final extract + archive (export clause honored, `data/21#ap-002-no-data-export`). / 末次抽取+归档（守导出条款）。
- [ ] Vendor contract terminated or transferred. / 厂商合同终止或转。
- [ ] Credentials revoked. / 凭证吊销。
- [ ] Retention period logged. / 留存期已记。
- [ ] Final cost reconciliation (stop double-pay). / 末次费用核（止双付）。

---

### 3.6 Member communications template (re-opt-in) / 会员沟通模板（重获同意）

Send within `____` days of close; plain language, no dark patterns.
交割后 `____` 天内发；白话、无暗黑模式。

> "Hi `____`, `____` has joined the `____` group. To keep your membership, please re-confirm your consent at `____`. Your balance `____` is safe. You can opt out anytime."
> "您好 `____`，`____` 已加入 `____` 集团。为保留会籍请于 `____` 重新确认同意。您的余额 `____` 安全。可随时退出。"

### 3.7 Data-quality remediation plan / 数据质量修复方案

- [ ] Invalid emails/phones quarantined, not migrated blind. / 无效邮箱手机隔离，不盲迁。
- [ ] Duplicate households merged with rule in §3.3. / 重复家庭按 §3.3 合并。
- [ ] Orphan records (no consent) excluded from comms. / 孤儿记录（无同意）排除出沟通。
- [ ] Pre/post migration counts reconciled. / 迁移前后计数已核对。

### 3.8 Integration risk register / 整合风险登记

| Risk / 风险 | Likelihood 可能 | Impact 影响 | Mitigation 缓解 |
|---|---|---|---|
| Consent invalid 同意无效 | `____` | High 高 | §3.3 re-capture |
| Balance mismatch 余额差 | `____` | High 高 | §3.4 parallel-run |
| Lock-in cost 锁定费 | `____` | Med 中 | §3.1 diligence |
| Staff churn 员工流失 | `____` | Med 中 | §3.2 continuity |

> **Guidance / 指引**: Register reviewed at every integration gate; close before cutover.
> 指引：风险登记每整合闸复看；切换前清零。

### 3.9 Integration cost tracker / 整合成本追踪

| Cost / 成本 | Budget 预算 | Actual 实际 |
|---|---|---|
| Migration run (templates/22) 迁移 | `____` | `____` |
| Consent re-capture campaign 重获 | `____` | `____` |
| Parallel-run overlap 并行重叠 | `____` | `____` |
| Sunset/termination 退役终止 | `____` | `____` |
| **Total 合计** | `____` | `____` |

> **Rule / 规则**: Track double-pay window (old+new running) explicitly — it is the stealth cost.
> 规则：显式追"双跑"窗口——那是隐性成本。

### 3.10 Day-100 integration health check / 整合百日健康检查

| Check / 查 | Target / 目标 | Status / 态 |
|---|---|---|
| Re-opt-in rate 重获率 | ≥ `____`% | `____` |
| Dup complaints 重复投诉 | 0 | `____` |
| Old system cost 旧系统费 | €0 double-pay | `____` |
| Member churn 会员流失 | < `____`% | `____` |

> **Rule / 规则**: If re-opt-in < target, pause marketing until legal clears the gap.
> 规则：重获率不达标，暂停营销待法务清缺口。

### 3.11 Lessons capture / 经验回收

- What broke during migration & fix. / 迁移中坏啥、咋修。
- Consent re-capture rate by market. / 各市场重获率。
- Feed into next deal diligence checklist. / 回灌下笔尽调清单。

## ④ Common mistakes / 常见错误

1. Inheriting consent blindly → breach. / 盲继同意→违规。→ §3.3 (`tools/05`)
2. No data-export clause at diligence → stranded. / 尽调无导出条款→滞留。→ `data/21#ap-002-no-data-export`
3. Hidden lock-in discovered post-close. / 交割后才现隐藏锁定。→ §3.1
4. Poor dedup → double-charge members. / 去重差→会员重复扣费。→ §3.3
5. No sunset plan → paying two systems. / 无退役方案→双系统付费。→ §3.5
6. No parallel-run → silent balance loss. / 无并行跑→余额静默丢。→ §3.4

---

## ⑤ Related files / 相关文件

- `templates/22-data-migration-plan.md` — migration & sunset detail / 迁移与退役细节
- `data/21-anti-pattern-library.md` — export & lock-in anti-patterns / 导出与锁定反模式
- `tools/05-regulation-traceability-verification.md` — consent validity verify / 同意有效性核验
- `references/18-integration-and-data-plumbing.md` — plumbing patterns / 管道模式
- `templates/42-franchise-digital-kit.md` — data return on exit / 退出数据返还

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (system inventory + merge workbook + sunset sequencing), **Operator** (Day-1 continuity + integration sequencing that avoids double-running), and **Member** (no lost balance, no surprise breach, clear re-opt-in); the consent re-capture rule is the hard compliance line that separates a clean deal from a liability.
本模板覆盖**架构师**（系统清单+合并手册+退役时序）、**运营者**（Day-1 连续+整合时序免双跑）、**会员**（余额不丢、无惊爆违规、清晰重获）；同意重获规则是区分干净交易与负债的硬合规线。
