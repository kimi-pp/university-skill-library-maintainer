# Failure Autopsy — The Prepaid-Heavy Chain That Collapsed / 失败解剖——重预付连锁的崩塌

> **Cluster / 集群**: I (IT Governance & Money) · R (Finance) · F (Compliance) · V (Meta)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify fund-supervision regulation every 90 days via `tools/05`; prepaid rules are market-specific and volatile.
> **Cross-references / 交叉引用**: `data/01-kpi-benchmark-library.md` · `data/21-anti-pattern-library.md` · `references/16-security-operations-and-emergency.md` · `tools/05-regulation-traceability-verification.md` · SKILL.md HI-3
> **Retrieval note / 检索提示**: Prepaid/consumer-protection law is volatile 🔄 — run `tools/05` before any conclusion.

---

## Honesty Preamble / 诚实序言

> Archetypal composite case for teaching, not a claimed real company or incident; numbers are directional ranges, not exact losses. Prepaid failures are emotionally and legally severe — rehearse the safeguards.
> 用于教学的原型复合案例，非真实公司或事件；数字为方向性区间，非精确损失。预付暴雷在情感与法律上都很重——请演练防范。

---

## ① The Setup / 事发前情

A 12-club regional chain (FDMM L2) chasing aggressive growth. The GM's playbook: sell huge stored-value packages — "recharge ¥5,000 get ¥7,000" — and fund new-club fit-out from the cash inflow. On paper, the balance sheet looked like a war chest. The deferred-revenue ledger was a spreadsheet that "looked close enough" to the membership system (`data/01-kpi-benchmark-library.md#kpi-deferred-revenue`). Nobody reconciled it monthly. Prepaid funds sat in the operating account, mixed with daily revenue (`data/21#ap-041-prepaid-mixed-account`).

一家 12 店区域连锁（FDMM L2）拼命冲规模。店总打法：狂卖储值卡——"充 5000 送 2000"——再用流入的现金去装修新店。账面上看像有了金库。递延收入账是张"差不多对了"的表，从没和会员系统月月对账（`data/01#kpi-deferred-revenue`）。预付金混在日常营收的运营户里（`data/21#ap-041`）。

The owner told the board: "Prepaid is just cash we already earned." That sentence is the seed of the collapse — it mistakes a liability for revenue.

老板对董事会说：「预付不过是我们已经赚到的现金。」这句话就是崩塌的种子——把负债当成了收入。

---

## ② Timeline of Doom / 崩塌时间线（决策逐条，红旗可见）

- **Month 0 / 第0月**: Launch 3× stored-value promos. Red flag ignored: selling future obligations faster than delivering them. / 上 3 轮储值大促。被忽略的红旗：卖未来义务比交付快。
- **Month 2 / 第2月**: Deferred ledger already drifts from the MMS but nobody notices. Red flag: no reconciliation habit. / 递延账已偏离会员系统但无人察觉。红旗：无对账习惯。
- **Month 3 / 第3月**: Use ¥-range of prepaid float to fit out Club #13. Red flag: spending member money as if it were profit (`AP-041`). / 拿一笔预付浮存装修 13 店。红旗：把会员的钱当利润花（`AP-041`）。
- **Month 5 / 第5月**: New-member sales dip (market saturation). Red flag: the float that hid the gap is now shrinking. / 新会员销售下滑（市场饱和）。红旗：掩盖缺口的浮存正在缩水。
- **Month 6 / 第6月**: Deferred ledger is ¥-range OFF vs the MMS; still not reconciled (`AP-038`). / 递延账与会员系统差一笔区间；仍不核对（`AP-038`）。
- **Month 8 / 第8月**: A local consumer-protection probe opens on prepaid complaints. Red flag: fund-supervision non-compliance exposed. / 当地消保因预付投诉立案。红旗：资金监管不合规曝光。
- **Month 9 / 第9月**: Trigger event — a social post about "can't get refund" goes local-viral. A run on refunds begins. / 触发事件——"退不了款"的帖本地刷屏，挤兑式退款开始。
- **Month 10 / 第10月**: Float gone, refunds unpayable, clubs suspended. / 浮存耗尽，退款无力兑付，门店被责令停业。

---

## ③ The Blow-Up / 爆雷后果（方向性区间）

| Dimension / 维度 | Directional range / 方向性区间 |
|---|---|
| Refund run / 退款挤兑 | Low millions to tens of millions (¥) / 低百万到数千万（¥） |
| Members affected / 受影响会员 | Thousands with disputed balances / 数千名会员余额争议 |
| Legal exposure / 法律暴露 | Regulatory penalty + possible principal liability / 监管罚款 + 可能的主体责任 |
| Club fate / 门店命运 | Multiple clubs suspended; chain effectively ends / 多店停业；连锁实质终结 |

The human cost is the worst part: members who prepaid for a year of fitness lost both the money and the trust. Several elderly members, who had paid annual in advance, were locked out.

最重的是人的代价：为一年健身预付的会员丢了钱也丢了信任。几位预付年卡的老年会员被挡在门外。

---

## ④ Root-Cause Analysis / 根因分析

**5-Whys / 五问法**

| # | Why / 为何 | Answer / 答 |
|---|---|---|
| 1 | Why collapse? / 为何崩？ | A refund run with no cash to pay / 挤兑却无钱兑付 |
| 2 | Why no cash? / 为何无钱？ | Prepaid float was spent on expansion / 预付浮存花在扩张上 |
| 3 | Why spend float? / 为何花浮存？ | No segregated supervised account / 无隔离监管账户 |
| 4 | Why not segregated? / 为何不隔离？ | "It's all our money" mindset + no compliance gate / "都是我们的钱"心态 + 无合规闸 |
| 5 | Why no gate? / 为何无闸？ | HI-3 + deferred reconciliation never enforced / HI-3 + 递延对账从没执行 |

**Anti-patterns violated / 违反的反模式**: `#ap-041-prepaid-mixed-account` · `#ap-038-deferred-no-reconcile` · `#ap-015-prepaid-3yr-saas` (spirit: discounting future obligations).
**HI invariant / 硬不变量**: **HI-3** — prepaid/stored-value advice MUST NOT violate fund-supervision & consumer-protection rules. Violated in spirit and in fact.

---

## ⑤ The Counterfactual — Library-Guided Path / 反事实——按本库走的路

1. `tools/05` fund-supervision check BEFORE any promo: map the market's prepaid cap + segregated-account rule. / 任何促销前先 `tools/05` 查资金监管：映射该市场预付上限 + 隔离账户规则。
2. Segregated supervised account (`data/21#md-118-prepaid-mixed-account`): prepaid funds NEVER touch the operating account. / 隔离监管账户（`data/21#md-118`）：预付金绝不进运营户。
3. Monthly auto-reconcile (`data/21#md-111-deferred-revenue-reconcile`, `AP-038` fix): alert on >0.5% variance; the MMS is the system of record. / 月度自动对账（`data/21#md-111`、`AP-038` 修正）：差异>0.5% 即告警；以会员系统为源。
4. ROI three-scenario (`tools/06`) on every expansion: show that fit-out is funded by EQUITY, not member float. / 每笔扩张做 ROI 三情景（`tools/06`）：明示装修由股权而非会员浮存出资。
5. Pre-load refund policy (`data/21#md-112-refund-policy-preloaded`, `AP-039`): no surprise, no case-by-case. / 退款政策预置（`data/21#md-112`、`AP-039`）：不 surprises、不 case-by-case。
6. Dashboard MUST label deferred revenue as a liability, never as profit (HI-3 spirit). / 看板必须把递延收入标为负债，绝不标利润（HI-3 精神）。

---

## ⑥ Early-Warning Checklist (10 signals) / 预警清单（10 个信号）

1. Stored-value promos exceed 30% of new revenue. / 储值促销超新增营收 30%。
2. Prepaid funds sit in the operating account. / 预付金在运营户。
3. Deferred ledger not reconciled in 30+ days. / 递延账 30+ 天未对。
4. Expansion capex sourced from member float. / 扩张资本开支来自会员浮存。
5. "Deferred revenue" treated as profit on dashboards. /  dashboard 把递延收入当利润。
6. No segregated/supervised account exists. / 无隔离/监管账户。
7. Refund requests rising but policy unclear. / 退款请求升但政策不清。
8. Sales dip but obligations keep rising. / 销售降但义务续升。
9. No `tools/05` compliance scan on prepaid terms. / 预付条款未经 `tools/05` 合规扫描。
10. Consumer-complaint count ticking up on prepaid. / 预付类投诉数上升。

> One-line takeaway / 一句话: Prepaid is a promise you owe, not cash you earned.
> 预付是你欠的承诺，不是你赚的现金。

---

## ⑦ Related Files / 相关文件

`data/01-kpi-benchmark-library.md` · `data/21-anti-pattern-library.md` (#ap-041, #ap-038, #ap-015) · `references/16` §R · `tools/05` · `tools/06` · SKILL.md HI-3.

---

## ⑧ G13 Note / G13 注记

- **Architect / 架构师**: segregated-account architecture + monthly reconcile is a design requirement (HI-3).
- **Operator / 运营者**: the deferred-reconcile hour is non-negotiable; the float temptation is the trap.
- **Member / 会员**: prepaid is a promise, not free capital — their money must be protected. No orphan touchpoint.
- **会员**：预付是承诺不是免费资本——他们的钱必须被保护。无孤儿触点。

> Honesty note / 诚实注记: Archetypal composite; all money figures are directional ranges, not exact losses. Verify fund-supervision law via `tools/05` for your market before acting.
> 原型复合；所有金额均为方向性区间，非精确损失。行动前就你所在市场经 `tools/05` 核验资金监管法规。
