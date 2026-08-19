# Renewal Negotiation Prep Sheet / 续约谈判准备表

> **Cluster / 集群**: I (IT governance & money) + L (Architecture upgrades)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify market alternatives and pricing every 180 days via `tools/04`; align with `data/14` renewal section.
> **Cross-references / 交叉引用**: `data/14-repair-scripts-and-sla-library.md` (renewal via SLA log) · `references/06-software-landscape-apac-vendors.md` · `tools/04-dynamic-intelligence-retrieval.md` · `references/05-methodology-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: Fill this 2–4 weeks before any vendor renewal. It turns your `data/14` SLA log and outage history into proven leverage, scans the market for alternatives, and sets a target price plus a walk-away line — so you lead with facts, not loyalty.
**中文**：任何厂商续约前 2–4 周填。把 `data/14` 的 SLA 日志与故障史变成有据筹码，扫市场找替代，定目标价与走人线——让你带事实而非忠诚开场。

> 💡 Vendors discount proven pain more than friendly reminders. Your outage log is the leverage; loyalty is not a negotiation tactic (→ `data/14` renewal section).
> 💡 厂商对「有据的痛」比「友好的提醒」更肯降价。故障日志是筹码；忠诚不是谈判策略（→ `data/14` 续约节）。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | `data/14` ticket log (past 12 mo) / 工单日志(近12月) | outage hours, breaches / 故障时、超SLA |
| 2 | Current contract + price / 现合同+价 | renewal date marked / 标续约日 |
| 3 | `tools/04` market scan / 市场扫描 | ≥3 alternatives / ≥3替代 |
| 4 | Usage report from vendor / 厂商用量报告 | seats, API calls / 席位数、调用 |

---

## ③ THE TEMPLATE / 模板正文

### #usage-audit Usage Audit / 用量审计

| Metric / 指标 | Contracted / 签约 | Actual / 实际 | Wasting? / 浪费? |
|---|---|---|---|
| Seats / 席位 | __ | __ | Y/N |
| Locations / 门店 | __ | __ | Y/N |
| API calls/mo / 月调用 | __ | __ | Y/N |
| Features used / 用到功能 | all / 部分 | __ | unused? / 未用? |

> Paying for unused seats is the easiest money to claw back. Right-size before you ask (→ `data/21#ap-015-prepaid-3yr-saas` caution).
> 为闲置席位付费是最易追回的钱。先削再谈（→ `data/21#ap-015` 警示）。

### #market-scan Market Alternatives Scan (via tools/04) / 市场替代扫描

| Vendor / 厂商 🔄 | Fit / 适配 | Price range / 价区间 | Lock-in risk / 锁定风险 | Note / 备注 |
|---|---|---|---|---|
| Alt A | __ | ¥__–__ | low/med/high | __ |
| Alt B | __ | ¥__–__ | low/med/high | __ |
| Alt C (open) / 开源 | __ | ¥__–__ | low | __ |

> 🔄 Run `tools/04` for current APAC vendor landscape before relying on any price. Keep ≥3 options (Iron Law 8).
> 🔄 依赖任何价格前先跑 `tools/04` 核亚太厂商格局。保持 ≥3 选项（铁律8）。

### #leverage-inventory Leverage Inventory / 筹码清单

| Leverage / 筹码 | Strength / 强度 (1–5) | How to use / 怎么用 |
|---|---|---|
| Multi-year vs flexibility / 多年 vs 灵活 | __ | trade term for discount / 用期限换折扣 |
| Timing (before their quarter-end) / 时机 | __ | negotiate at their soft spot / 趁其软档谈 |
| Reference-ability / 可背书性 | __ | offer case study for price / 用案例换价 |
| Outage/SLA breaches / 故障超SLA | __ | demand credit or discount / 要求抵扣或折 |
| Repeat-fault device / 反复坏设备 | __ | demand free replace / 要求免费换 |

### #target-pricing Target / Walk-Away Pricing / 目标与走人价

| Item / 项 | Current / 现 | Target / 目标 | Walk-away / 走人线 |
|---|---|---|---|
| Annual fee / 年费 | ¥__ | ¥__ | >¥__ → leave / 超则走 |
| Seat price / 席位价 | ¥__ | ¥__ | >¥__ → leave |
| Term / 期限 | __ | __ | no auto-renew trap / 无自动续约坑 |

### #negotiation-script Bilingual Negotiation Script / 双语谈判话术

**EN**: "Based on our log, we had __ outage hours and __ SLA breaches last year. We also use only __ of __ seats. We'd like to renew at __ with a 12-month cap and a free-data-export clause, or we'll move to Alt __."
**中文**：「据日志，去年我们 __ 小时故障、超 SLA __ 次，且 __ 个席位只用 __ 个。我们希望以 __ 续约，期限封顶12月且免费导出数据，否则转向替代 __。」

> Stay factual, cite the log, never insult (→ `data/14` escalation works-vs-backfires table).
> 只讲事实、引日志、不人身攻击（→ `data/14` 管用vs反效果表）。

### #redflag-summary Red-Flag Summary / 红旗摘要

| Signal / 信号 | If present / 若出现 | Action / 动作 |
|---|---|---|
| Usage <60% of contracted / 用量<签约6成 | right-size now / 立即削量 | demand seat cut / 要求减席 |
| >3 SLA breaches/yr / 年超SLA>3次 | credit or leave / 抵扣或走 | escalate / 升级 |
| No data-export clause / 无导出条款 | walk / 走 | HI-8 red line / HI-8红线 |
| Auto-renew <60d window / 自动续约窗<60天 | mark + cap / 标+封顶 | non-negotiable / 不可让 |

### #outcome-log Outcome Log / 结果日志

| Date / 日期 | Agreed price / 成交价 | Term / 期限 | Concessions / 让步 | Signed? / 签? | Next review / 下次核 |
|---|---|---|---|---|---|
| ____ | ¥__ | __ | __ | □ | ____ |

---

## ④ Common Mistakes / 常见错误

- **Renew on loyalty alone** → overpay for unused seats. → `data/14` renewal section.
- **No SLA log** → no leverage. → `data/21#ap-024` (evidence lineage).
- **Prepay 3yr before pilot** → stuck. → `data/21#ap-015-prepaid-3yr-saas`.
- **Forget auto-renew window** → trapped again. → `data/14` contract traps.

---

## ⑤ Related Files / 相关文件

- `data/14-repair-scripts-and-sla-library.md` — renewal via SLA log. / 用 SLA 日志谈续约。
- `templates/35-sla-contract-review.md` — clauses to defend. / 要守的条款。
- `references/06-software-landscape-apac-vendors.md` — alternative vendors. / 替代厂商。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: Renewal prep is the governance gate of Cluster I — usage audit + market scan enforce Iron Law 8 (vendor neutrality) and prevent lock-in before it renews.
**运营者 / Operator**: A fill-in sheet turns the owner into a prepared negotiator; the log is the operator's shield against "it went up again" surprises.
**会员 / Member**: Right-sized, fairly-priced systems keep member-facing services stable and data portable (HI-8) — no forced migration mid-contract that disrupts check-in.
