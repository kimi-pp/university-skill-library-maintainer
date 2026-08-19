# Failure Autopsy — The Nephew's Custom App / 失败解剖——侄子做的定制 App

> **Cluster / 集群**: B (Software) · N (Integration) · V (Meta)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Vendor/landscape facts volatile 🔄 — re-verify via `tools/04`; `references/06` for build-vs-buy.
> **Cross-references / 交叉引用**: `data/21-anti-pattern-library.md` · `references/06-software-landscape-apac-vendors.md` · `templates/09-mms-selection-scorecard.md` · `templates/35-sla-contract-review.md` · SKILL.md Iron Law 8
> **Retrieval note / 检索提示**: Software landscape marked 🔄 — run `tools/04` before choosing.

---

## Honesty Preamble / 诚实序言

> Archetypal composite case for teaching, not a claimed real company or incident; numbers are directional. "Build it ourselves" is the most expensive sentence in club IT — rehearse the buy-decision.
> 用于教学的原型复合案例，非真实公司或事件；数字方向性。「自己造」是场馆 IT 里最贵的句子——请演练买/造决策。

---

## ① The Setup / 事发前情

A single-club owner's nephew "is good with computers" and offered to build a custom member app + MMS "for cheap." The owner, eager to save the SaaS fee, said yes. No spec, no contract, no plan to maintain.

单店老板的侄子"懂电脑"，主动说"便宜"给做一个定制会员 App + MMS。老板想省 SaaS 月费，答应了。没需求文档、没合同、没维护计划。

---

## ② Timeline of Doom / 崩塌时间线

- **Month 0 / 第0月**: "Nephew will build it, saves the fee." Red flag: no buy-vs-build decision (`templates/09`). / "侄子来做，省月费。"红旗：没做买/造决策（`templates/09`）。
- **Month 6 / 第6月**: App half-done; features creep; still no documentation. / App 做了一半；需求蔓延；仍无文档。
- **Month 12 / 第12月**: Go-live with gaps; members confused; check-in flaky. / 带缺口上线；会员困惑；签到抽风。
- **Month 18 / 第18月**: Nephew takes a job elsewhere and leaves. No docs, no handover. / 侄子入职别处离开。无文档、无交接。
- **Month 19 / 第19月**: Security holes found (unpatched framework, weak auth); payment reconciliation chaos — records don't tie to the bank. / 发现安全漏洞（框架未打补丁、弱鉴权）；支付对账混乱——记录和银行对不上。

---

## ③ The Blow-Up / 爆雷后果（方向性区间）

- **Money / 资金**: Sunk cost ¥-range (hundreds of thousands directional over 18 months) + rescue/rebuild cost + breach-remediation. / 沉没成本数十万方向性（18 个月）+ 抢救/重建费 + 漏洞整改。
- **Members / 会员**: Check-in friction + billing errors → trust erosion, slice churns. / 签到摩擦 + 账单错误 → 信任侵蚀，部分流失。
- **Security / 安全**: Breach exposure (PII + payment) → possible PCI/PIPL finding. Verify via `tools/05`. / 泄露暴露（PII + 支付）→ 可能 PCI/PIPL 认定。经 `tools/05` 核验。
- **Operations / 运营**: No one can maintain it; club held hostage by absent dev. / 无人能维护；场馆被离场开发者卡死。

---

## ④ Root-Cause Analysis / 根因分析

**5-Whys / 五问法**

| # | Why / 为何 | Answer / 答 |
|---|---|---|
| 1 | Why hostage? / 为何被绑？ | Only the nephew understood the code / 只有侄子懂代码 |
| 2 | Why only him? / 为何只他懂？ | No documentation / 无文档 |
| 3 | Why no docs? / 为何无文档？ | Informal "favor" build / 非正式"人情"开发 |
| 4 | Why build? / 为何自造？ | "Save the fee" over buy-vs-build / "省月费"压过买/造决策 |
| 5 | Why no gate? / 为何无闸？ | `templates/09` + `references/06` ignored / 忽略 `templates/09` + `references/06` |

**Anti-patterns violated / 违反的反模式**: `#ap-008-card-numbers-spreadsheet` (spirit: amateur payment handling) · `#ap-049-sandbox-keys-prod` (spirit: no deployment discipline) · `#ap-015-prepaid-3yr-saas` (spirit: false economy). Core: no `templates/09` buy-decision.
**HI invariant / 硬不变量**: Iron Law 8 (vendor neutrality / data-export) strained — no exit clause, no export path.

---

## ⑤ The Counterfactual — Library-Guided Path / 反事实——按本库走的路

1. `references/06-software-landscape-apac-vendors.md`: principle "build ONLY what differentiates; buy the rest." A member app/MMS is NOT differentiating. / `references/06`：原则"只造差异化的，其余买"。会员 App/MMS 不差异化。
2. `templates/09-mms-selection-scorecard.md`: score build vs buy on cost, risk, maintenance, lock-in. Buy wins. / `templates/09`：从成本/风险/维护/锁定给买/造打分。买胜。
3. Pick ≥3 SaaS options with data-export clause BEFORE sign (`templates/35-sla-contract-review.md`, Iron Law 8). / 签约前选 ≥3 个带导出条款的 SaaS（`templates/35`、铁律8）。
4. Pilot first; cap any prepay at 12 months (`data/21#md-104`). / 先试点；预付封顶 12 个月（`data/21#md-104`）。
5. Contract a maintained vendor with SLA + escrow of source if custom code is ever needed. / 若确需定制，签有 SLA + 源码托管的受维护供应商。

---

## ⑥ Early-Warning Checklist (10 signals) / 预警清单

1. "A relative will build it for cheap." / "亲戚便宜给做"。
2. No written spec or contract. / 无书面需求或合同。
3. No buy-vs-build decision made (`templates/09`). / 没做买/造决策（`templates/09`）。
4. Building something non-differentiating. / 在做不差异化的东西。
5. No documentation from day one. / 从第一天起无文档。
6. Single developer, no backup. / 单一开发者，无备份。
7. Payment handled in-house amateurly. / 支付内部业余处理。
8. No data-export clause considered. / 没考虑数据导出条款。
9. "Save the fee" is the main motive. / "省月费"是主因。
10. No maintenance plan. / 无维护计划。

---

## ⑦ Related Files / 相关文件

`references/06-software-landscape-apac-vendors.md` · `data/21-anti-pattern-library.md` (#ap-008, #ap-049, #ap-015) · `templates/09-mms-selection-scorecard.md` · `templates/35-sla-contract-review.md` · SKILL.md Iron Law 8.

---

## ⑧ G13 Note / G13 注记

- **Architect / 架构师**: buy commodity systems; reserve build for true differentiation (`references/06`).
- **Operator / 运营者**: a maintained vendor with SLA beats a genius who leaves.
- **Member / 会员**: stable check-in + correct billing is the baseline promise. No orphan touchpoint.
- **会员**：稳定签到 + 准确账单是底线承诺。无孤儿触点。

> Honesty note / 诚实注记: Archetypal composite; cost figures directional. Software landscape is volatile — verify vendor options via `tools/04` before deciding.
> 原型复合；成本为方向性。软件格局易变——决策前经 `tools/04` 核验供应商选项。
