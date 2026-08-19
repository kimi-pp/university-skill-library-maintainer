# Franchise Digitalization Kit / 加盟数字化工具包

> **Cluster / 集群**: I (IT governance & money) + G (governance, HQ/franchise)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Vendor stack pricing & ISP SLA 🔄 via `tools/04`; compliance four-pack per market via `tools/05` before citing (`references/10`, `references/11`).
> **Cross-references / 交叉引用**: `data/21-anti-pattern-library.md#ap-002-no-data-export`, `data/07-apac-regional-differences.md`, `tools/05-regulation-traceability-verification.md`, `templates/43` (site selection), `templates/46` (HQ NOC).
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this kit when a franchisor wants to **standardize the digital stack across franchisees** while keeping brand consistency, member-data integrity, and HQ visibility — without over-claiming control over a franchisee's own business.
本工具包用于加盟商体系**统一数字化栈**，兼顾品牌一致、会员数据完整与 HQ 可见，同时不越界控制加盟商自有经营。

- **FDMM gate / 等级闸门**: L2+ chains with ≥3 franchise clubs; HQ IT owns the mandatory stack, franchisee owns local ops.
  L2+ 且 ≥3 家加盟店；HQ IT 管强制栈，加盟商管本地运营。
- **Trigger / 触发**: New franchisee signing, or franchisee "using their own spreadsheet" drift detected.
  新加盟签约，或发现加盟商用自有表格"跑偏"。

---

## ② Prerequisites checklist / 前置清单

- [ ] Franchise agreement clauses covering systems & data signed (`data/21#ap-002-no-data-export`). / 加盟合同含系统&数据条款并已签。
- [ ] HQ-selected mandatory stack vendors contracted (see §3.1). / HQ 选定强制栈供应商已签约（见 §3.1）。
- [ ] Compliance per market verified via `tools/05`. / 各市场合规经 tools/05 核验。
- [ ] Chargeback & support model approved by finance. / 分摊与支撑模式经财务批准。
- [ ] Exit/termination data clause drafted (see §3.7). / 退出/终止数据条款已拟（见 §3.7）。
- [ ] Brand asset library centralized & versioned. / 品牌资产库已集中且版本化。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Mandatory-stack vs free-choice split / 强制栈与自选分界

Define what franchisees **MUST** use (brand/data consistency) vs what they may choose.
界定加盟商**必须**用（品牌/数据一致）与可自选。

| Layer / 层 | Mandatory (HQ-set) 强制 | Free-choice 自选 |
|---|---|---|
| Membership & CRM 会员系统 | `____` (single source of truth) | — |
| Branding & pricing 品牌定价 | HQ template/engine | local promo copy only |
| Central BI dashboard 总部看板 | `____` | — |
| Club access control 门禁 | `____` approved list | model within list |
| Local marketing 本地营销 | brand assets only | channel & agency |
| Cleaning/IoT 清洁/IoT | recommended 推荐 | vendor |
| Finance/accounting 财务 | reporting format 报表格式 | local tool |

> **What good looks like / 合格样**: A franchisee can swap their cleaning vendor but never their membership DB. HQ sees every club's heartbeat from day one.
> 好样：加盟商可换清洁商，但换不了会员库；HQ 从第一天看见每家店心跳。
> **Red flag / 红线**: "Franchisees use whatever they want" → no data, no brand control, no recall path.
> 红线："随便用"→无数据、无品牌控制、无召回路径。

### 3.2 New-franchisee onboarding sequence / 新加盟商上线序列

Day-by-day systems provisioning (adjust to contract).
逐日系统开通（按合同调整）。

| Day / 天 | Action / 动作 | Owner / 责任 |
|---|---|---|
| D-14 | Contract + data clause sign 合同&数据条款签 | Franchise mgr |
| D-7 | HQ provisions tenant in membership system 总部开租户 | HQ IT |
| D-5 | Access-control devices ordered from approved list 门禁设备按清单订 | Franchisee |
| D-3 | Access-control & POS credentials issued 门禁&POS 凭证发 | HQ IT |
| D-1 | BI dashboard access + brand kit delivered 看板权限+品牌包 | HQ Mktg |
| D0 | Go-live checklist pass 上线清单过 | Joint |
| D+1 | First member scan test 首客扫码测 | Club staff |
| D+7 | First weekly ops review 首次周运营复盘 | HQ Ops |

> **Micro-example / 微例**: A 10-club franchisee in `____` market got tenant provisioned D-7; their first member scanned in at D0 09:02 with zero manual import, and the BI row went green before open.
> 微例：某 10 店加盟商 D-7 开通租户，D0 09:02 首客扫码入场，零手工导入，BI 行开业前即绿。

### 3.3 Data-sharing & privacy split (controller/processor in plain words) / 数据共享与隐私分（用白话讲控制者/处理者）

:::dynamic-hook topic="franchise-controller-processor-model" staleness="180d" action="tools/05" fallback="treat as unverified"
Stored baseline as of 2026-07: HQ usually acts as **joint controller** for member identity & billing; franchisee as **controller** for local CCTV/HR; both use processors (the SaaS vendors). Verify exact role per market law.
截至 2026-07 基线：HQ 通常为会员身份与账单的**共同控制者**；加盟商为本地监控/人事的**控制者**；SaaS 厂商为**处理者**。具体角色按各市场法核验。
:::

- [ ] Identified who is controller for: member PII `____`, CCTV `____`, staff `____`. / 已界定控制者：会员PII、监控、员工。
- [ ] Processor list (vendors) with DPA signed. / 处理者清单（厂商）且 DPA 已签。
- [ ] Cross-border transfer lawful basis noted (`tools/05`). / 跨境传输合法依据已注。
- [ ] Breach-notification responsibility assigned. / 泄露通知责任已分。

> **Red flag / 红线**: Assuming HQ can read franchisee CCTV "because brand". Confirm lawful basis or exclude it.
> 红线：想当然"为品牌 HQ 能看加盟商监控"。须确认依据，否则排除。

### 3.4 Brand-asset & pricing governance in systems / 品牌资产与定价系统治理

- Brand kit pushed to all club signage/UI from HQ. / 品牌包由 HQ 推至所有门店标识/界面。
- Pricing engine: HQ sets floor & ceilings; franchisee picks within band. / 定价引擎：HQ 定上下限，加盟商区间内选。
- Any deviation needs HQ approval flag in system. / 任何偏离需系统内 HQ 审批标记。
- Promo copy uses approved templates only; local slang allowed in defined slot. / 促销文案仅用审批模板；方言限定义槽位。

### 3.5 Franchisee scorecard dashboard spec / 加盟商记分卡看板规格

| KPI / 指标 | Target / 目标 | Source / 源 |
|---|---|---|
| Digital adoption % 数字化采用率 | ≥ `____`% | membership sys |
| Data sync latency 数据同步延迟 | < `____` min | BI |
| Brand compliance 品牌合规 | 100% | audit |
| Member NPS 会员NPS | ≥ `____` | survey |
| Backup success 备份成功率 | ≥ `____`% | NOC |

> **Guidance / 指引**: Scorecard is coaching, not punishment — review trends monthly, not single blips.
> 指引：记分卡是辅导非惩罚——看月度趋势，非单次波动。

### 3.6 HQ IT support model & chargeback / HQ IT 支撑模式与分摊

- Tiered support: L1 franchisee self, L2 HQ shared, L3 vendor. / 分级支撑：L1 加盟商自，L2 HQ 共，L3 厂商。
- Chargeback: per-club monthly `____` (range, verify `tools/04`). / 分摊：每店每月 `____`（区间，tools/04 核）。
- SLA: L2 response `____` h, L3 per vendor contract. / SLA：L2 响应 `____` 小时，L3 按厂商合同。
- :::dynamic-hook topic="managed-services-price-band" staleness="180d" action="tools/04" fallback="treat as unverified"
  As of 2026-07 managed-services per club roughly `____`–`____`/mo; confirm current band.
  截至 2026-07 托管服务每店约 `____`–`____`/月；请核当前区间。
  :::

### 3.7 Exit / termination data handling / 退出/终止数据处置

- [ ] Member data export to HQ or successor within `____` days. / 会员数据 `____` 天内导出至 HQ 或接手方。
- [ ] Credential revocation automated on termination. / 终止时凭证自动吊销。
- [ ] Brand assets & local config wiped. / 品牌资产与本地配置清除。
- [ ] DPA wind-down clause executed. / DPA 收尾条款执行。
- [ ] Final audit sign-off archived. / 末次审计签字归档。

> **Rule / 规则**: Never let a terminated franchisee keep the membership DB — it is HQ/brand data.
> 规则：终止加盟商绝不可保留会员库——那是 HQ/品牌数据。

### 3.8 Franchisee self-service portal (optional) / 加盟商自助门户（可选）

- Password/access self-reset reduces L2 tickets. / 自助改密降 L2 工单。
- Knowledge base of runbooks linked. / 链入 runbook 知识库。
- Request form for brand-asset deviations. / 品牌偏离申请表单。

---

### 3.9 Franchisee training & onboarding KPI / 加盟商培训与上线 KPI

| Milestone / 里程碑 | Target / 目标 | Owner / 责 |
|---|---|---|
| Systems training done 系统培训完 | by D-2 | HQ Train |
| First successful sync 首成同步 | by D0 | Club IT |
| Scorecard green 记分卡绿 | by D+30 | HQ Ops |
| Support ticket <`____` 工单 | by D+14 | HQ IT |

> **Micro-example / 微例**: Franchisee `____` hit first sync at D0 14:30 and scorecard green at D+21 after two coaching calls — not penalties.
> 微例：加盟商 `____` D0 14:30 首同步，经两次辅导 D+21 记分卡转绿——非罚款。

### 3.10 HQ governance cadence / HQ 治理节奏

- Monthly franchisee digital review. / 月度加盟商数字化复盘。
- Quarterly stack re-evaluation (pricing 🔄 via `tools/04`). / 季度栈复评（价格 tools/04）。
- Annual contract & compliance re-sign. / 年度合同与合规重签。

## ④ Common mistakes / 常见错误

1. No data-export/return clause → stranded members. / 无导出/返还条款→会员滞留。→ `data/21#ap-002-no-data-export`
2. Over-claiming controller over franchisee CCTV. / 越界自称监控控制者。→ §3.3
3. Free-choice membership system → no HQ visibility. / 会员系统自选→HQ 失明。
4. No chargeback → HQ IT unbudgeted. / 无分摊→HQ IT 无预算。→ §3.6
5. Exit plan missing → painful termination. / 缺退出方案→终止痛苦。→ §3.7
6. Brand kit not versioned → inconsistent signage. / 品牌包无版本→标识不一。→ §3.4
7. Scorecard used as a pressure tool → franchisee hides data. / 记分卡当施压工具→加盟商藏数。→ §3.5

---

## ⑤ Related files / 相关文件

- `templates/43-site-selection-scorecard.md` — new-site IT readiness / 新店 IT 就绪
- `templates/46-hq-noc-dashboard-spec.md` — multi-club visibility / 多店可见
- `data/21-anti-pattern-library.md` — lock-in & export anti-patterns / 锁定与导出反模式
- `tools/05-regulation-traceability-verification.md` — controller/processor verify / 角色核验
- `data/07-apac-regional-differences.md` — per-market rules / 各市场规则

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (mandatory-stack definition + BI spec), **Operator** (onboarding sequence + support tiers + scorecard), and **Member** (portable, brand-consistent experience + protected PII via clear controller/processor roles and a clean exit path); the privacy split prevents HQ overreach while keeping recall ability.
本模板覆盖**架构师**（强制栈+看板规格）、**运营者**（上线序列+支撑分级+记分卡）、**会员**（可携、品牌一致体验+经清晰角色与干净退出保护 PII）；隐私分界防 HQ 越界又保留召回力。
