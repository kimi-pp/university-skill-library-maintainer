# RFP / Tender Technical Specification Skeleton / 招标技术规格书骨架

> **Cluster / 集群**: I (IT governance & money) + B (software)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Vendor/price 🔄 via `tools/04`; data-residency & procurement law via `tools/05`; re-verify before each tender.
> **Cross-references / 交叉引用**: `data/21#ap-002-no-data-export`, `data/21#ap-020-demo-not-acceptance`, `references/05` (methodology §11), `templates/21` (vendor eval), `templates/22` (migration).
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this skeleton to write a **technical specification** for a tender (membership SaaS, POS, gate system, network MSP, etc.) so vendors bid on the SAME scope — enabling comparable quotes and a clean evaluation.
本骨架用于编写**招标技术规格书**（会籍 SaaS、POS、闸机、网络 MSP 等），让供应商在同一范围报价——便于比价与干净评审。

- **FDMM gate / 等级闸门**: L1+ for any outsourced system. Early L1 may use a lighter version; do not require L4 multi-site clauses for a single studio.
  L1+ 凡外包系统。早期 L1 可用精简版；单店别强塞 L4 多店条款。
- **Trigger / 触发**: buying/replacing a core system, or ≥3 vendors to compare.
  采购/替换核心系统，或需 ≥3 家比选。

---

## ② Prerequisites checklist / 前置清单

- [ ] Business requirements clear (who/what/why). / 业务需求清晰（谁/做什么/为什么）。
- [ ] Current-state documented (see §3.1 annex). / 现状已记录（见 §3.1 附录）。
- [ ] At least 3 vendors shortlisted, ≥1 local + ≥1 low-cost (`SKILL.md` Iron Law 8). / 至少 3 家入围，含本地+低成本（铁律8）。
- [ ] Data-export clause reviewed BEFORE issuing (`data/21#ap-002-no-data-export`). / 发标前已审数据导出条款。
- [ ] Budget ranges confirmed via `tools/04` 🔄. / 预算区间经 `tools/04` 确认。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Scope & current-state annex / 范围与现状附录

- **In scope / 范围内**: `____` (systems, sites, users). / 含：`____`（系统、门店、用户）。
- **Out of scope / 范围外**: `____`. / 不含：`____`。
- **Current state / 现状**: existing vendor `____`, contract ends `____`, data volume `____` records. / 现有供应商 `____`，合同止 `____`，数据量 `____` 条。
- **Mandatory exit readiness / 强制退出准备**: confirm old system's data-export capability NOW (`templates/22`). / 现在就确认旧系统导出能力。

### 3.2 Functional requirements table (MUST / SHOULD / NICE) / 功能需求表（必须/应当/可选）

| ID | Requirement / 需求 | Priority / 优先级 | Acceptance / 验收 |
|---|---|---|---|
| F-01 | Member check-in via QR + face fallback 扫码入场+人脸兜底 | MUST | opens within 2 s |
| F-02 | Offline mode on WAN loss 断网离线模式 | MUST | gate + POS offline |
| F-03 | Role-based access 角色权限 | SHOULD | 4 roles min |
| F-04 | Open API / webhook 开放接口 | SHOULD | idempotent retry |
| F-05 | AI churn dashboard AI 流失看板 | NICE | — |

> **Guidance / 指引**: MUST = contract-breaking if missing. NICE = scored, not gating. This prevents "demo passed" being called done (`data/21#ap-020-demo-not-acceptance`).
> MUST=缺即违约。NICE=计分不卡关。防"demo 过=完成"。

### 3.3 Non-functional requirements / 非功能需求

- **Uptime / 可用性**: `____` % (e.g. 99.5% for L2). / 如 L2 取 99.5%。
- **Support hours / 支持时段**: `____` (e.g. 08:00–22:00 local + on-call). / 如本地 8–22 加值班。
- **Data residency 🔄**: where member data (esp. biometric & health) is stored, whether it crosses borders, local residency requirement per market (`SKILL.md` HI-9). Verify mechanism via `tools/05`. / 会员数据（尤其生物识别/健康）存储地、是否出境、本地驻留要求；机制经 `tools/05` 核验。
- **Security / 安全**: encryption at rest+transit, audit log, no shared admin (`data/21#ap-009-shared-admin-login`). / 静态+传输加密、审计日志、禁共用管理员。

### 3.4 Data-export & exit clauses (MANDATORY) / 数据导出与退出条款（强制）

> **Hard rule / 硬规则**: This section is non-negotiable. No export clause = no contract (`SKILL.md` Iron Law 8, `data/21#ap-002-no-data-export`).
> 本节不可谈。无导出条款=不签约。

- Vendor MUST provide full data export in open format (CSV/JSON) at any time, no fee beyond reasonable cost. / 供应商须随时提供开放格式（CSV/JSON）全量导出，除合理成本外不收费。
- Export includes members, balances, bookings, orders, consents. / 导出含会员、储值、预约、订单、同意记录。
- Exit: all data delivered within `____` days of termination, format specified. / 退出：终止后 `____` 天内交付，格式明确。
- Source-code escrow ONLY if custom-built; not required for SaaS. / 源码托管仅定制开发需要，SaaS 不强制。

### 3.5 Evaluation criteria & weights / 评审标准与权重

| Criterion / 标准 | Weight / 权重 | Scoring / 计分 |
|---|---|---|
| Functionality fit 功能契合 | 35% | MUST met = pass |
| Service network 服务网络 | 20% | nearest engineer test (`templates/21`) |
| Price 价格 | 20% | per §3.6 comparable |
| Integration & API 集成 | 15% | open API |
| Compliance 合规 | 10% | data-residency + consent |

> Weights sum to 100%. Adjust per project but keep functionality + service ≥ 50%.
> 权重合计 100%。可按项目调，但功能+服务 ≥50%。

### 3.6 Pricing-response format (force comparable quotes) / 报价格式（强制可比）

Vendors MUST fill this exact table — no "package pricing" lumps.
供应商须填此表——禁止"打包价"含糊。

| Cost item / 费用项 | One-time / 一次性 | Recurring / 周期 | Unit / 单位 | Note / 说明 |
|---|---|---|---|---|
| Licence 许可 | `____` | `____`/mo | per club | |
| Hardware 硬件 | `____` | — | | |
| Implementation 实施 | `____` | — | | |
| Training 培训 | `____` | — | | |
| Support 支持 | — | `____`/yr | | |
| **Total 3-yr TCO** | | `____` | | |

> **Rule / 规则**: If a vendor cannot break down TCO, disqualify — you cannot compare lumps (`data/21#ap-020-demo-not-acceptance` spirit).
> 供应商拆不开 TCO 即淘汰——含糊包价无法比。

### 3.7 Timeline & Q&A protocol / 时间表与答疑机制

- RFP issued `____`; questions by `____`; answers published to ALL bidders `____`; submission `____`; award `____`. / 发标`____`；提问`____`；统一答复所有投标人`____`；交标`____`；定标`____`。
- All Q&A published to every bidder (no side deals). / 所有答疑对全体投标人公开，禁止私相授受。

---

## ④ Common mistakes / 常见错误

1. No data-export clause → locked in forever. / 无导出条款→永久锁定。→ `data/21#ap-002-no-data-export`
2. "Demo worked" accepted as delivery. / 把 demo 当交付。→ `data/21#ap-020-demo-not-acceptance`
3. Lump-sum quotes → cannot compare. / 打包价→无法比价。→ §3.6
4. Side-deal Q&A → unfair tender. / 私下答疑→不公招标。
5. Ignoring data residency → compliance breach. / 忽视数据驻留→违规。→ §3.3 🔄

---

## ⑤ Related files / 相关文件

- `templates/21-vendor-evaluation-matrix.md` — scorecard to run post-RFP / 标后评分卡
- `templates/22-data-migration-plan.md` — exit & migration / 退出与迁移
- `references/05-methodology-library.md` — procurement §11 / 采购
- `data/21-anti-pattern-library.md#ap-002-no-data-export` — export red line / 导出红线
- `tools/05-regulation-traceability-verification.md` — data residency / 数据驻留

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (functional + non-functional spec + exit clauses), **Operator** (comparable pricing + Q&A protocol + support hours), and **Member** (data portability, privacy via residency & consent, no lock-in); the export clause is the member's safety net against vendor captivity.
本模板覆盖**架构师**（功能+非功能规格+退出条款）、**运营者**（可比报价+答疑机制+支持时段）、**会员**（数据可携、驻留与同意保隐私、不被供应商锁死）；导出条款是会员对抗供应商锁定的安全网。
