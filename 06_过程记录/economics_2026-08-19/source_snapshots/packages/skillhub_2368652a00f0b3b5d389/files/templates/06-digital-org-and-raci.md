# Digital Org & RACI / 数字化组织与 RACI

> **Cluster / 集群**: P (people & org), I (governance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: role sizing re-verify when club count crosses 1 / 5 / 50 thresholds; training paths track `playbooks/13-90day-onboarding`. / 门店数跨 1/5/50 阈值时复核角色配置；培训路径跟踪 `playbooks/13`。
> **Cross-references / 交叉引用**: `templates/04-digital-charter-and-stage-gate.md` (decision rights) · `references/03-value-chain-scenario-library.md` §P · `playbooks/13-90day-onboarding.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04`。

---

## ① Purpose & When to Use / 用途与使用时机 {#purpose}

Define who does what in digital ops as you scale from 1 club to 50, with role cards and a RACI matrix for 20 recurring IT activities, plus a skills matrix pointing to training.
定义从 1 店到 50 店数字化运营中谁做什么，含角色卡、20 项经常性 IT 活动的 RACI 矩阵，以及指向培训的能力矩阵。

> **FDMM level gate / 成熟度闸口**: **FDMM L2 and above** (you have ≥2 systems to operate). At L1, the owner IS the one-person IT — no matrix needed yet, just read `playbooks/01`.
> **FDMM 等级闸口**：**FDMM L2 及以上**（已有 ≥2 系统要运维）。L1 时老板就是一人 IT——暂无需矩阵，读 `playbooks/01` 即可。

> **What good looks like / 好答案长什么样**: every activity has exactly one A (Accountable); R is never "everyone"; scaling note says when HQ IT takes over an A.
> **好答案长什么样**：每项活动恰有一个 A；R 不是「全员」；扩展说明写清 HQ IT 何时接管某个 A。

> **Red flag / 红旗**: shared admin login because "no one owns access" → see `data/21-anti-pattern-library.md#ap-009`. RACI fixes ownership. / 因「没人管权限」而共用管理员账号 → 见 `data/21#ap-009`。RACI 明确归属。

---

## ② Prerequisites & Inputs Checklist / 前置条件与输入清单 {#prerequisites}

- [ ] Current club count (1 / 5 / 50 band). / 当前门店数（1/5/50 档）。- [ ] `templates/04` decision rights already set. / `templates/04` 决策权已定。
- [ ] Named people for owner / duty manager / one-person IT. / 具名老板/店长/一人IT。
- [ ] Vendor list with SLAs. / 带 SLA 的供应商清单。
- [ ] `playbooks/13` open for skill gaps. / 打开 `playbooks/13` 看技能缺口。

---

## ③ The Template / 模板正文 {#template}

### 3.1 Role Cards / 角色卡 {#s-roles}

| Role / 角色 | At 1 club / 1 店 | At 5 clubs / 5 店 | At 50 clubs / 50 店 |
|---|---|---|---|
| Owner / 老板 | A for all big spend / 大支出 A | A, delegates / A、授权 | Board-level A / 董事会级 A |
| Duty manager / 店长 | R daily ops / 日常运营 R | R per club / 单店 R | R per region / 单区 R |
| One-person IT / 一人 IT | R everything / 全包 R | R field + escalates / 现场 R+升级 | Specialized pods / 专业组 |
| HQ IT / 总部 IT | — (none) / 无 | Light (standards) / 轻量标准 | Full team (sec/net/BI) / 完整团队 |
| Vendor / 供应商 | C/R per contract / 按合同 C/R | C/R per SLA / 按 SLA C/R | C/R + QBR / C/R+季度评审 |

### 3.2 RACI Matrix — 20 Recurring IT Activities / RACI 矩阵：20 项经常性 IT 活动 {#s-raci}

> R=Responsible 执行 · A=Accountable 担责 · C=Consulted 被询 · I=Informed 知会. Exactly one A per row.
> R=执行 · A=担责 · C=被询 · I=知会。每行恰一个 A。

| # | Activity / 活动 | Owner | Duty Mgr | One-person IT | HQ IT | Vendor |
|---|---|---|---|---|---|---|
| 1 | Daily backup check / 每日备份检查 | I | I | R/A | C | C |
| 2 | Access grant/revoke / 权限开通回收 | I | C | R/A | C | I |
| 3 | Incident response / 故障响应 | I | R | A | C | C |
| 4 | Vendor renewal decision / 续约决策 | A | I | C | C | I |
| 5 | Password & license mgmt / 密码许可管理 | I | C | R/A | C | I |
| 6 | CCTV review (HI-5 bound) / 监控调阅（受 HI-5 约束） | A | C | R | C | I |
| 7 | Network health check / 网络健康检查 | I | I | R/A | C | C |
| 8 | POS/payment reconciliation / 收银对账 | I | R | A | C | C |
| 9 | Gate firmware update / 闸机固件更新 | I | C | R/A | C | C |
| 10 | Annual data-export test / 年度导出实测 | I | I | R | A | C |
| 11 | Consent ledger upkeep / 同意台账维护 | I | C | R/A | C | I |
| 12 | SLA breach escalation / SLA 违约升级 | I | I | R | A | I |
| 13 | Security patch / 安全补丁 | I | C | R/A | C | C |
| 14 | Budget preparation / 预算编制 | A | C | R | C | I |
| 15 | FDMM re-assessment / FDMM 复评 | A | C | R | C | I |
| 16 | Training rollout / 培训推行 | I | R | A | C | I |
| 17 | Compliance scan (HI) / 合规扫描 | A | I | R | C | I |
| 18 | Disaster-recovery drill / 灾备演练 | I | C | R/A | C | I |
| 19 | New-club IT onboarding / 新店 IT 入驻 | I | C | R | A | C |
| 20 | ROI review / ROI 复盘 | A | I | R | C | I |

> **Scaling note / 扩展说明**: at 5 clubs, HQ IT takes A on #10, #12, #19; at 50 clubs HQ IT also takes A on #13, #17, #18 and One-person IT splits into security/network/BI pods. / 5 店时 HQ IT 接管 #10/#12/#19 的 A；50 店时 HQ IT 再接管 #13/#17/#18 的 A，一人 IT 拆为安全/网络/BI 组。

### 3.3 Skills Matrix + Training Pointer / 能力矩阵与培训指向 {#s-skills}

| Skill / 技能 | Needed at / 需于 | Gap? / 缺口? | Training / 培训 |
|---|---|---|---|
| Network basics / 网络基础 | L2+ | __ | `playbooks/13` Ch.2 / 第2章 |
| SLA negotiation / SLA 谈判 | L3+ | __ | `references/05` §7 / 第7节 |
| Data-export testing / 导出实测 | L2+ | __ | `playbooks/13` Ch.5 / 第5章 |
| AI governance / AI 治理 | L4+ | __ | `references/13` §K / K 节 |
| Incident command / 事故指挥 | L2+ | __ | `references/16` / 第16章 |

> **Red flag / 红旗**: a role with 3+ "gap=yes" on L4 skills but asked to run AI → train or hire before S3. / 某角色 L4 技能 3+ 缺口却被要求跑 AI → S3 前先培训或招人。

---

### 3.4 Scaling Narrative / 扩展叙述 {#s-scaling}

- **At 1 club / 1 店**: the owner is A on everything; one-person IT is R on all 20 activities. No HQ IT exists. This is normal and fine — but the matrix still prevents "who owns backup?" ambiguity.
- **At 5 clubs / 5 店**: a light HQ IT appears and takes A on #10 (data-export test), #12 (SLA escalation), #19 (new-club onboarding). Duty managers become R per club; one-person IT shifts to field + escalation.
- **At 50 clubs / 50 店**: HQ IT is a full team; it also takes A on #13 (security patch), #17 (compliance scan), #18 (DR drill). One-person IT splits into security / network / BI pods, each R on its domain. Owners move to board-level A only.

> **Red flag / 红旗**: promoting the 1-club structure straight to 50 clubs (one hero IT) → single point of failure + burnout. Stand up HQ IT at the 5-club threshold. / 把 1 店结构直接用到 50 店（一个英雄 IT）→ 单点故障+过劳。5 店门槛就建 HQ IT。

### 3.5 Worked RACI Example — Incident Response / RACI 实例：故障响应 {#s-example}

> Activity #3 "Incident response" at 5 clubs: / 5 店时活动 #3「故障响应」：

| Role / 角色 | Code / 码 |
|---|---|
| Owner / 老板 | I (kept informed) |
| Duty manager / 店长 | R (first on scene) / 现场第一人 |
| One-person IT / 一人 IT | A (owns resolution) / 担责解决 |
| HQ IT / 总部 IT | C (advises, escalates) / 建议升级 |
| Vendor / 供应商 | C (per SLA) / 按 SLA |

If the same person is both R and A that is fine; if "everyone is R, no one is A" that is the failure mode `data/21-anti-pattern-library.md#ap-009` describes. / R=A 同一人可行；若「全员 R、无人 A」即 `data/21#ap-009` 所述失败态。

### 3.6 Extra Skills Rows / 补充技能行 {#s-skills-extra}

| Skill / 技能 | Needed at / 需于 | Gap? / 缺口? | Training / 培训 |
|---|---|---|---|
| RACI ownership / RACI 归属 | L2+ | __ | `references/03` §P |
| Vendor QBR facilitation / 供应商 QBR | L3+ | __ | `references/05` §7 |
| DR drill leading / 灾备演练主持 | L3+ | __ | `references/16` |
| Pilot design / 试点设计 | L2+ | __ | `templates/08` |

### 3.7 Ownership Principle / 归属原则 {#s-principle}

> One sentence to live by: **every recurring activity has exactly one A, and that A can name the last time they did it.** / 一句口诀：**每项经常性活动恰一个 A，且 A 能说出上次做它的时间。**

If you cannot name the A for "daily backup check", the matrix is unfinished — go back to §3.2 and fill it. / 若说不出「每日备份检查」的 A，矩阵未完成——回 §3.2 补。

> This single rule prevents the `data/21-anti-pattern-library.md#ap-009` failure (shared login, no owner) and the "we thought vendor handled it" gap. / 此一规则防 `data/21#ap-009` 失败（共用账号无主）与「以为供应商管了」的缺口。

### 3.8 Volatile-Fact Hook / 易变事实钩子 {#s-hook}

:::dynamic-hook topic="it-headcount-per-club" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07, IT headcount norms and role-cost benchmarks per market shift with FX and local labor rates; verify via `tools/04` before sizing HQ IT at the 5/50-club thresholds rather than copying another market's org chart.
截至 2026-07，各市场 IT 人头标准与角色成本基准随汇率与当地人力浮动；在 5/50 店门槛配置 HQ IT 前经 `tools/04` 核验，勿照搬他国组织图。
:::

## ④ Common Mistakes / 常见错误 {#mistakes}

- **Shared admin login** → no ownership, breach risk. See `data/21-anti-pattern-library.md#ap-009`. / 共用管理员账号 → 无归属、违规风险。
- **No A on an activity** → it falls through. Every row needs exactly one A. / 活动无 A → 责任落空。每行须恰一个 A。
- **One-person IT expected at 50-club scale** → burnout & single point of failure. Stand up HQ IT. / 50 店仍靠一人 IT → 过劳与单点故障。建 HQ IT。
- **Train-after-launch** → see `data/21-anti-pattern-library.md#ap-003` spirit (prepare before, not after). / 上线后才培训 → 应事前准备。

---

## ⑤ Related Files / 相关文件 {#related}

- `templates/04-digital-charter-and-stage-gate.md` — decision rights. / 决策权。
- `references/03-value-chain-scenario-library.md` §P — people method. / 人员方法。
- `playbooks/13-90day-onboarding.md` — skill building. / 技能建设。
- `references/05-methodology-library.md` §7 — vendor loop. / 供应商闭环。
- `references/16-security-operations-and-emergency.md` — incident. / 事故。
- `data/21-anti-pattern-library.md` — failure patterns. / 失败模式。

---

## ⑥ G13 Tri-Perspective Note / 三视角覆盖备注 {#g13}

> **Architect** (role cards + RACI impose clear operating structure) × **Operator** (scaling note + skills matrix give the solo steward a hire/train plan) × **Member** (access/consent/CCTV rows under named A protect member data & privacy by design). / **架构**（角色卡+RACI 强制清晰运营结构）× **商家**（扩展说明+技能矩阵给一人总管招人/培训计划）× **会员**（权限/同意/监控行归具名 A，从源头保护会员数据与隐私）。
