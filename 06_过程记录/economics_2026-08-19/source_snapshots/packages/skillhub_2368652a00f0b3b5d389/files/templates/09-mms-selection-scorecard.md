# 09 · Membership Management System Selection Scorecard / 会籍管理系统选型评分卡

> **Cluster / 集群**: B (Software systems) · Template / 模板 · System-Building tier (FDMM L2)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Vendor pricing, feature lists & contract terms re-verify every 90 days via `tools/04`; all vendor mentions carry 🔄 and are examples, not endorsements.
> **Cross-references / 交叉引用**: `references/06-software-landscape-apac-vendors.md` (§1 MMS) · `data/21-anti-pattern-library.md#ap-002-no-data-export` · `data/07-apac-regional-differences.md#payment-method-landscape` · `tools/05-regulation-traceability-verification.md` · `references/02-club-formats-and-zones.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用（FDMM 闸门）

**Purpose / 用途**: A fill-in scorecard to select a Membership Management System (MMS) — the club's system of record for members, contracts, check-ins, renewals and billing. It is the spine every other system plugs into.
**用途 / 中文**：填入式评分卡，用于选型「会籍管理系统（MMS）」——会员、合同、入场、续费、扣费的唯一记录系统，是所有其他系统的中枢。

**When to use / 适用场景**:
- You run on paper + Excel (FDMM L1) and are buying your first SaaS → L1→L2 transition. / 还在纸质+Excel（L1），要买第一套 SaaS → L1→L2。
- You are replacing an MMS that locks your data or lacks local payment methods. / 正在替换一个锁定数据或缺少本地支付通道的 MMS。
- **FDMM gate / 闸门**: Do NOT buy any MMS without a data-export clause reviewed BEFORE signing — see `data/21#ap-002-no-data-export`. / 签约前未审查数据导出条款，绝不开买（见 `data/21#ap-002-no-data-export`）。
- **Vendor-neutrality rule (Iron Law 8) / 供应商中立（铁律8）**: shortlist ≥3 vendors, including ≥1 local-market option and, where viable, ≥1 open-source/low-cost option. / 短名单 ≥3 家，含 ≥1 本地市场选项与可行的开源/低成本选项。

---

## ② Prerequisites checklist / 前置清单

- [ ] Member headcount & growth plan known (current / 12-month / 36-month). / 已知会员数与增长计划（当前/12月/36月）。
- [ ] Target market(s) and their prepaid/stored-value consumer-protection rules confirmed via `tools/05`. / 目标市场及其预付费消保规则经 `tools/05` 确认。
- [ ] Local payment methods listed per market (`data/07#payment-method-landscape`). / 按市场列出本地支付方式。
- [ ] Current data exported to CSV as a migration sample. / 现有数据已导出为 CSV 作为迁移样本。
- [ ] Budget band set (see ranges below 🔄). / 已设定预算区间（见下方区间 🔄）。
- [ ] At least 3 vendors shortlisted (Iron Law 8). / 已短列 ≥3 家（铁律8）。
- [ ] A staff member assigned as "data-export clause owner" before contract review. / 已指定「数据导出条款负责人」参与合同审查。

:::dynamic-hook topic="apac-mms-pricing-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07: China SaaS roughly ¥500–¥8,000/club/mo; global US$100–US$1,500/club/mo. Ranges are order-of-magnitude; verify current pricing via tools/04 before budgeting.
截至 2026-07：中国约 ¥500–¥8,000/店/月；国际 US$100–US$1,500/店/月。区间仅为量级；预算前经 tools/04 核验当前价。
:::

---

## ③ The template / 模板正文

### 3.1 Requirements checklist (60+ line items) / 需求清单（60+ 项）

> **How to use / 用法**: Mark Must (M) or Should (S) per line; leave Vendor A/B/C score columns for §3.2. / 每行标 M（必须）或 S（应有）；供应商 A/B/C 评分列留给 §3.2。
> **What good looks like / 合格标准**: ≥90% of "Must" items covered by your winning vendor; every "Must" gap has a written workaround. / 中标供应商覆盖 ≥90% 的「必须」项；每个「必须」缺口都有书面替代方案。
> **Red flag / 红旗**: A vendor that cannot tick the Data-Export group (§3.1.7) is auto-disqualified — no exceptions. / 勾不出「数据导出组」（§3.1.7）的供应商一票否决，无例外。

| # | Group / 分组 | Requirement (En / 中文) | M/S | A | B | C |
|---|---|---|---|---|---|---|
| 1 | Membership / 会员 | Multi-tier membership types (single / multi-club / corporate) / 多层级会员类型（单店/多店/企业） | M | | | |
| 2 | Membership | Member profile with photo, emergency contact, minor-flag / 会员档案含照片、紧急联系人、未成年标识 | M | | | |
| 3 | Membership | Freeze / hold with reason & date range / 冻结/暂停含原因与日期区间 | M | | | |
| 4 | Membership | Ban / blacklist with audit log / 拉黑含审计日志 | M | | | |
| 5 | Membership | Multi-club & multi-role permission matrix / 多店多角色权限矩阵 | M | | | |
| 6 | Membership | Transfer / upgrade membership workflow / 转会/升级流程 | S | | | |
| 7 | Membership | Guest / day-pass issuance / 访客/次卡发放 | S | | | |
| 8 | Membership | Local-language staff UI (zh/en/ja/ko…) / 本地语言后台 | M | | | |
| 9 | Membership | Duplicate-member detection / 重复会员查重 | S | | | |
| 10 | Membership | Consent ledger for marketing (HI-7) / 营销同意台账（HI-7） | M | | | |
| 11 | Billing / 计费 | Recurring membership fee auto-debit / 会费定期自动扣款 | M | | | |
| 12 | Billing | Local payment methods (Alipay/WeChat/Paytm/LINE Pay/EFTPOS…) / 本地支付方式 | M | | | |
| 13 | Billing | Prepaid/stored-value balance & deferred-revenue tracking / 储值余额与递延收入跟踪 | M | | | |
| 14 | Billing | Proration on upgrade / downgrade / 升降级按比例计费 | S | | | |
| 15 | Billing | Refund-to-source with reason code / 原路退款含原因码 | M | | | |
| 16 | Billing | Failed-payment retry & dunning flow / 扣款失败重试与催缴 | M | | | |
| 17 | Billing | Invoice / receipt fields per market (🔄 verify) / 按市场小票字段 | M | | | |
| 18 | Billing | Tax / fapiao compliance fields per market (🔄) / 税务/发票字段 | S | | | |
| 19 | Billing | Coupon / promo engine with cap / 优惠券引擎含上限 | S | | | |
| 20 | Billing | Commission settlement to coach (PT) / 教练提成结算 | S | | | |
| 21 | Booking / 约课 | Real-time class capacity & remaining slots / 实时余位 | M | | | |
| 22 | Booking | Waitlist auto-fill on cancel / 候补自动补位 | M | | | |
| 23 | Booking | Coach-calendar sync / 教练日历同步 | M | | | |
| 24 | Booking | No-show / late-cancel penalty rules / 爽约/迟到扣罚规则 | S | | | |
| 25 | Booking | Court / PT 1:1 slot booking / 场地/私教 1:1 预约 | S | | | |
| 26 | Booking | Capacity & clash rules / 容量与冲突规则 | M | | | |
| 27 | Booking | QR / band scan-to-enter for booked class / 扫码/手环入场约课 | M | | | |
| 28 | Booking | Class check-in history per member / 会员上课记录 | M | | | |
| 29 | Booking | Recurring booking (e.g. weekly) / 周期预约 | S | | | |
| 30 | Booking | Overbooking headroom control / 超售余量控制 | S | | | |
| 31 | Access-int / 门禁集成 | Real-time member-status sync from MMS to gate / 与闸机实时同步会员状态 | M | | | |
| 32 | Access-int | Fail-open / fail-closed policy configurable / 可配置断电开/关策略 | M | | | |
| 33 | Access-int | Offline credential cache at gate / 闸机离线凭证缓存 | M | | | |
| 34 | Access-int | Credential types: QR / RFID / face* / 凭证类型：二维码/RFID/人脸* | M | | | |
| 35 | Access-int | Access-event log export / 门禁事件日志导出 | M | | | |
| 36 | Access-int | Multi-gate map & zone rules / 多闸地图与分区规则 | S | | | |
| 37 | Access-int | Tailgating alert hook to CCTV / 防尾随联动监控 | S | | | |
| 38 | Access-int | Locker assignment from MMS / 由 MMS 分配柜 | S | | | |
| 39 | Access-int | 24h-unmanned mode support / 24h 无人模式支持 | S | | | |
| 40 | Reporting / 报表 | Daily revenue & attendance dashboard / 每日营收到场看板 | M | | | |
| 41 | Reporting | Churn / retention cohort report / 流失/留存 cohort 报表 | S | | | |
| 42 | Reporting | Class fill-rate report / 满课率报表 | M | | | |
| 43 | Reporting | ARPU / LTV estimate / 客单价/生命周期价值估算 | S | | | |
| 44 | Reporting | Prepaid liability (deferred revenue) report / 预售负债报表 | M | | | |
| 45 | Reporting | Custom report builder / 自定义报表构建 | S | | | |
| 46 | Reporting | Scheduled email/export of reports / 报表定时邮件/导出 | S | | | |
| 47 | Reporting | Role-based dashboard views / 分角色看板 | S | | | |
| 48 | Reporting | Drill-down to transaction level / 下钻到交易级 | M | | | |
| 49 | API / 接口 | Open REST API documented / 有文档的开放 REST API | M | | | |
| 50 | API | Webhook with idempotency key / 带幂等键的 webhook | M | | | |
| 51 | API | Webhook retry & dead-letter / webhook 重试与死信 | S | | | |
| 52 | API | Sandbox / test environment / 沙箱环境 | S | | | |
| 53 | API | Rate-limit transparency / 限流透明 | S | | | |
| 54 | API | SSO / SAML or OIDC for staff / 员工 SSO | S | | | |
| 55 | API | BI connector (or raw export) / BI 连接器或原始导出 | M | | | |
| 56 | Data-export (MANDATORY) / 数据导出（强制） | Full member + contract export in open format (CSV/JSON) / 全套会员+合同开放格式导出 | M | | | |
| 57 | Data-export | Transaction log export with tender type / 含支付方式的交易流水导出 | M | | | |
| 58 | Data-export | Export timeline & cost stated IN CONTRACT / 导出时限与费用写进合同 | M | | | |
| 59 | Data-export | No lock-in: export on demand, not only at exit / 可随时导出，非仅退网时 | M | | | |
| 60 | Data-export | Booking & access-event history export / 约课与门禁历史导出 | M | | | |
| 61 | Data-export | PT session & commission balance export / 课时与提成余额导出 | S | | | |
| 62 | Data-export | Data residency stated per market (HI-9) / 按市场声明数据驻留 | M | | | |
| 63 | Data-export | Deletion / right-to-be-forgotten support / 删除/被遗忘权支持 | M | | | |

> **Red flag / 红旗**: If a salesperson says "export is available" but the contract is silent on format, timeline and cost → that is `data/21#ap-002-no-data-export` in the making. Walk away or get it in writing. / 销售说"能导出"但合同不写格式/时限/费用 → 正是 `data/21#ap-002-no-data-export` 的苗头。离场或写进合同。

### 3.2 Weighted scoring matrix / 加权评分矩阵

> **Method / 方法**: Score each vendor 1–5 per row; Weighted = (Weight ÷ 5) × Score. Total must equal Σ Weight = 100. Pick highest weighted total. / 每家供应商每行打 1–5 分；加权 =（权重÷5）×得分；权重合计=100；取加权总分最高者。
> **What good looks like / 合格标准**: Winner scores ≥4 on every "Must" group average and beats runners-up by a margin wider than price difference. / 中标者在每个「必须」组平均 ≥4 分，且优势超过价差。
> **Red flag / 红旗**: Choosing on price alone while the winner fails Data-Export or Access-integration "Must" rows. / 仅凭价格选，却输了数据导出或门禁集成的「必须」项。

| Criterion / 标准 | Weight / 权重 | Vendor A (1–5) | Vendor B (1–5) | Vendor C (1–5) |
|---|---|---|---|---|
| Membership & billing fit / 会员计费契合 | 20 | | | |
| Booking & access integration / 约课门禁集成 | 20 | | | |
| Local payment & prepaid compliance / 本地支付与预售合规 | 15 | | | |
| Reporting & API / 报表与接口 | 15 | | | |
| Data-export & exit / 数据导出与退出 | 20 | | | |
| Price vs TCO / 价格与总拥有成本 | 10 | | | |
| **Total weighted / 加权合计** | **100** | | | |

### 3.3 Demo script — force vendors to SHOW LIVE / 演示脚本（逼供应商现场演示）

> **Rule / 规则**: No PowerPoint screenshots count. Make them log in and do it. / 不接受 PPT 截图，必须登录现场操作。

- [ ] **Live data export**: trigger a member+contract CSV export in front of you. / 现场触发会员+合同 CSV 导出。
- [ ] **Freeze a member** then show the gate rejects entry within 1 minute. / 冻结一名会员，1 分钟内闸机拒入。
- [ ] **Refund-to-source** on a test transaction; show money path. / 测试交易原路退款，展示资金路径。
- [ ] **Offline mode**: cut the network at the gate simulator; show cached credential still opens. / 断网模拟闸机，缓存凭证仍能开。
- [ ] **Multi-club**: move a member across clubs; show permission & balance sync. / 跨店迁移会员，展示权限与余额同步。
- [ ] **Consent toggle**: show marketing opt-in recorded with timestamp (HI-7). / 展示营销同意带时间戳记录。

### 3.4 Reference-call question list (talk to 2 live customers) / 客户背调问题清单（找 2 家在用客户）

- "How long from contract sign to go-live, realistically?" / 签约到上线实际多久？
- "Did you ever export ALL data? How long and what did it cost?" / 是否曾导出全部数据？多久、花多少？
- "What broke in the first 90 days, and how fast was support?" / 头 90 天出过什么故障，支持多快？
- "Any unplanned price increase at renewal?" / 续约时有无计划外涨价？
- "Does the gate/MMS sync ever drift, and how do you catch it?" / 门禁/MMS 同步会漂移吗，怎么发现？
- "Were local payment methods added without extra fee?" / 本地支付通道是否免额外费接入？

### 3.5 Red flags at contract stage / 合同阶段红旗

> **Red flag / 红旗**: "Source code escrow", "per-seat penalty", "export only at termination with 30-day SLA", "API extra paid" → negotiate or flag. / 源码托管、按坐席罚、仅退网时导出且 30 天 SLA、API 另收费 → 谈判或标红。

---

## ④ Common mistakes (anti-patterns) / 常见错误（反模式）

- `data/21#ap-002-no-data-export` — buying MMS with no data-export clause. / 买无导出条款的 MMS。
- `data/21#ap-022-digitize-broken-process` — digitizing a broken manual process instead of fixing it. / 把坏流程直接数字化而非先修。
- `data/21#ap-023-untrained-system-promo` — promoting a system the front desk was never trained on. / 推一个前台从未受训的系统。
- `data/21#ap-008-card-numbers-spreadsheet` — storing member card numbers in a plain spreadsheet. / 会员卡号存明文表格。
- `data/21#ap-009-shared-admin-login` — one shared admin login for all staff. / 全员共用管理员账号。

---

## ⑤ Related files / 相关文件

- `references/06-software-landscape-apac-vendors.md` (§1 MMS selection top-5) / MMS 选型五条。
- `references/07-hardware-landscape-and-vendors.md` (C2 gates, C12 wearables) / 闸机与穿戴硬件。
- `data/21-anti-pattern-library.md` (anti-pattern anchors) / 反模式锚点。
- `tools/06-roi-three-scenario.md` — if MMS cost >¥100k equivalent, attach 3-scenario ROI. / 若 MMS 投入超等值 10 万，附 ROI 三情景。
- `templates/12-access-control-gate-spec.md` — gate integration spec downstream. / 下游闸机集成规格。

---

## ⑥ G13 tri-perspective note / G13 三视角覆盖说明

This template serves **Architect** (weighted matrix + integration must-haves), **Operator** (demo script + reference-call script + contract red flags), and **Member** (consent ledger, reliable entry, data-portability rights); the data-export group is the non-negotiable spine that keeps the member's data sovereign and the operator non-locked-in — no orphaned touchpoint.
本模板覆盖**架构师**（加权矩阵+集成必接）、**运营者**（演示脚本+背调脚本+合同红旗）、**会员**（同意台账、可靠入场、数据可携权）；数据导出组是不可妥协的中枢，保障会员数据主权与运营者不被锁定——无孤儿触点。
