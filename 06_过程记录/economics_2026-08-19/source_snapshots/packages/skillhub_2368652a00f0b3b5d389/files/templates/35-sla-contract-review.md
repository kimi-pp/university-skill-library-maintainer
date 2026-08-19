# SLA / Contract Review Checklist / SLA 与合同审查清单

> **Cluster / 集群**: I (IT governance & money) + J (Resilience)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify SLA norms and penalty caps every 90 days via `tools/04`/`tools/05`; align with `data/14-repair-scripts-and-sla-library.md`.
> **Cross-references / 交叉引用**: `data/14-repair-scripts-and-sla-library.md` (SLA clause library) · `references/05-methodology-library.md` (money questions) · `data/21-anti-pattern-library.md` · `references/16-security-operations-and-emergency.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: Use this BEFORE signing any vendor contract that holds member data or keeps your club running — CRM, POS, gate, network, CCTV, payments. It turns vague sales promises into contractual commitments you can claim against. Print one per vendor.
**中文**：在签署任何持有会员数据或维系场馆运转的厂商合同前用——会籍、收银、闸机、网络、监控、支付。把含糊的销售承诺变成你可主张的合同义务。每厂商打印一份。

> ⚠️ A vendor quoting only "response 4h" may never promise resolution. Always write BOTH per severity. And read the auto-renew + price-hike fine print — that's where clubs get trapped.
> ⚠️ 只报「响应4h」的厂商可能从不承诺解决。每级都写「响应+解决」二者。还要读自动续约与涨价小字——场馆常栽在这。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | The contract draft / 合同草案 | in hand / 在手 |
| 2 | Your outage log (if renewing) / 故障日志 | from `data/14` / 来自 |
| 3 | ≥3 vendor options compared / 至少3家比 | HI-8 vendor neutrality / 铁律8 |
| 4 | `data/14` SLA clause library open / 打开 | for clause intent / 条款意图 |

---

## ③ THE TEMPLATE / 模板正文

### #definitions Response vs Resolution / 响应 vs 解决

- **Response / 响应**: time to first human reply ("we got your ticket"). / 首次人工回复时间。
- **Resolution / 解决**: time to actually fix or workaround. / 真正修好或绕过的时限。
- ✅ Require BOTH defined per P1/P2/P3 (see `templates/31` severity matrix). / 每级都要二者。

### #business-hours Business-Hours Trap / 营业时间陷阱

| Vendor says / 厂商说 | Risk for a gym / 对健身房风险 | Demand / 要求 |
|---|---|---|
| "Business hours 9–6 Mon–Fri" | Sat morning outage waits till Mon / 周六早故障等周一 | 24/7 or peak coverage / 24/7或高峰覆盖 |
| "Response next business day" | class-hour downtime uncompensated / 上课时段宕机无赔 | peak-hours SLA / 高峰 SLA |

### #uptime-math Uptime % Math Table / 可用率换算表（说人话）

| Uptime / 可用率 | Down per month / 月停 | Down per year / 年停 | Plain words / 说人话 |
|---|---|---|---|
| 99.9% | ~43 min | ~8.8 h | decent / 还行 |
| **99%** | **~7 h** | **~87 h** | **a full business day lost / 丢一整个营业日** |
| 95% | ~36 h | ~18 d | unacceptable for gates/POS / 闸机收银不可接受 |

> 🔄 These are math, not vendor promises — your contracted % may differ. A gym with 99% on the gate means ~7h/month a member may be stuck. Negotiate ≥99.5% for revenue systems (→ `references/18#n12`).
> 🔄 这是数学非厂商承诺——你签的百分比可能不同。闸机只 99% = 月均约7小时会员可能被卡。营收系统谈 ≥99.5%（→ `references/18#n12`）。

### #clause-checklist Clause Checklist (tick each found) / 条款清单

| Clause / 条款 | In contract? / 在合同? | Note / 备注 |
|---|---|---|
| Penalty / service-credit / 罚则或服务抵扣 | □ | "miss SLA >X → Y days credit" / 超X赔Y天 |
| Spare-part availability / 备件可用 | □ | critical spares 24h / 关键件24h |
| EOL notice ≥90d + path / EOL通知≥90天+路径 | □ | no sudden "unsupported" / 不突然停支 |
| Data export (open format, ≤30d, free) / 数据导出 | □ | HI-8 + `data/21#ap-002` |
| Exit / data-return / 退出数据返还 | □ | parallel-run supported / 支持并行 |
| Auto-renew notice window / 自动续约通知窗 | □ | mark calendar at sign / 签约即标 |
| Price-escalation cap / 涨价上限 | □ | cap or floor / 封顶或下限 |
| Liability floor for data loss / 数据丢失责任下限 | □ | raise above 1-month fee / 高于1月费 |
| Jurisdiction / language / 管辖与语言 | □ | local for cross-border / 跨境谈本地 |

### #verdict-sheet Verdict Sheet / 裁定表

| Question / 问题 | Answer / 回答 |
|---|---|
| All critical clauses present? / 关键条款齐全? | Yes / No |
| ≥3 quotes compared? / 已比≥3家? | Yes / No |
| Data-export free & open? / 导出免费开放? | Yes / No |
| Walk-away price known? / 已知走人价? | Yes / No |
| **Verdict / 裁定** | ☐ Sign 签 ☐ Negotiate 谈 ☐ Walk 走 |

> Honesty note: if a clause is missing, write "TO VERIFY / 待复核" and do not sign until resolved. Never accept "we'll add it later" verbally (→ `data/21#ap-002-no-data-export`).
> 诚实注：缺条款即标「待复核」，解决前不签。绝不接受口头「以后补」（→ `data/21#ap-002`）。

### #signoff-block Sign-Off & Re-Verify Block / 签署与复核块

| Role / 角色 | Name / 姓名 | Date / 日期 | Confirm "all critical clauses present" / 确认「关键条款齐全」 |
|---|---|---|---|
| Reviewer / 审查 | ________ | ____ | ☐ Yes / 是 |
| Owner / 老板 | ________ | ____ | ☐ Yes / 是 |
| Legal (if >¥100k) / 法务 | ________ | ____ | ☐ Yes / 是 |

> Re-verify the contract against `tools/05` (clause-level) and `tools/04` (pricing) at every renewal — a clause valid at sign may be superseded by law later. Keep the signed copy with the exit/data-export clause highlighted.
> 每次续约用 `tools/05`（条款级）与 `tools/04`（价格）复核——签约时有效的条款日后或被法规替代。签署件留存，退出/数据导出条款高亮。

---

## ④ Common Mistakes / 常见错误

- **No data-export clause** → locked or lock-in squeezeed on switch. → `data/21#ap-002-no-data-export`.
- **Auto-renew short window** → trapped. → `data/14` contract traps.
- **Response-only SLA** → never resolved, never credited. → `data/14` SLA library.
- **Prepay 3yr before pilot** → stuck with wrong tool. → `data/21#ap-015-prepaid-3yr-saas`.

---

## ⑤ Related Files / 相关文件

- `data/14-repair-scripts-and-sla-library.md` — full SLA clause library + contract traps. / 完整 SLA 条款库+合同坑。
- `references/05-methodology-library.md` — money questions to ask. / 钱的问题。
- `templates/36-renewal-negotiation-prep.md` — use this at renewal. / 续约时用。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: The checklist is the contractual front-line of Cluster I; the exit/data-return clause is the legal shield behind HI-8 and the `#s16` STOP-LINE, and EOL + jurisdiction clauses manage lock-in risk (Iron Law 8).
**运营者 / Operator**: A tick-box review means a non-legal owner can spot the 3 clauses that matter most (export, credit, auto-renew) before signing — no lawyer on retainer needed.
**会员 / Member**: Data-export and breach clauses protect member-data portability and notification rights when switching vendors (HI-1, HI-8).
