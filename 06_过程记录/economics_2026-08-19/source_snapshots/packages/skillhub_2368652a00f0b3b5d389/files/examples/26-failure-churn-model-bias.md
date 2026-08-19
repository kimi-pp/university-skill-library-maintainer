# Failure Autopsy — The Churn Model That Discriminated / 失败解剖——搞歧视的流失模型

> **Cluster / 集群**: E (Data & AI) · K (AI Governance) · V (Meta)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: AI bias law is volatile 🔄 — re-verify via `tools/05`; model behavior must be re-audited per `templates/24`.
> **Cross-references / 交叉引用**: `data/09-algorithm-kernel-library.md` · `data/21-anti-pattern-library.md` · `templates/24-churn-prediction-project.md` · `tools/05-regulation-traceability-verification.md` · SKILL.md HI-6, HI-8
> **Retrieval note / 检索提示**: Bias-audit is mandatory; facts marked 🔄 run `tools/04`/`tools/05`.

---

## Honesty Preamble / 诚实序言

> Archetypal composite case for teaching, not a claimed real company or incident; numbers are directional. Discriminatory models are both a legal and a brand catastrophe — rehearse the audit.
> 用于教学的原型复合案例，非真实公司或事件；数字方向性。歧视性模型是法律与品牌双重灾难——请演练审计。

---

## ① The Setup / 事发前情

A 20-club chain (FDMM L3) deployed a churn-prediction model to target retention offers. The data team, eager to ship, trained on whatever features were handy: age, visit-hour, and a "life-stage" proxy built from profile fields. No bias audit was run (`templates/24-churn-prediction-project.md` mandatory section skipped). The GM cheered: "Finally, AI tells us who to save."

一家 20 店连锁（FDMM L3）上线流失预测模型来定向发挽留优惠。数据团队急于交付，用随手可得的特征训练：年龄、到店时段，以及一个用档案字段拼出的"人生阶段"代理变量。没做偏见审计（`templates/24` 强制段落被跳过）。店总欢呼：「终于有 AI 告诉我们要留住谁。」

What the data lead felt: "We hit the deadline." He confused shipping on-time with shipping safe.

数据负责人的感受：「我们赶上了 deadline。」他把准时交付错当成了安全交付。

---

## ② Timeline of Doom / 崩塌时间线

- **Month 0 / 第0月**: Model trained on biased features (age, life-stage proxy). Red flag: proxy for pregnancy/postpartum hidden in "life-stage." / 用偏见特征（年龄、人生阶段代理）训练。红旗："人生阶段"里藏着孕产代理。
- **Month 1 / 第1月**: Retention offers auto-targeted by score; older members + postpartum women systematically deprioritized. / 挽留优惠按分会自动定向；老年人 + 产后女性被系统性低优先级。
- **Month 2 / 第2月**: A postpartum member's offer vanishes; she notices peers still get promos. / 一位产后会员的优惠消失；她发现同伴仍有促销。
- **Month 3 / 第3月**: She posts: "the club stopped caring the moment I had a baby." / 她发帖：「我一生娃俱乐部就不关心我了。」
- **Month 4 / 第4月**: Complaint escalates; a journalist asks about "algorithmic discrimination." / 投诉升级；记者问"算法歧视"。
- **Month 5 / 第5月**: Internal review finds the model's offer-rate for the two groups is ¥-range lower. / 内部复查发现这两类群体的优惠触达率低一个区间。

---

## ③ The Blow-Up / 爆雷后果（方向性区间）

| Dimension / 维度 | Directional range / 方向性区间 |
|---|---|
| Lost retention value / 流失的留存价值 | Hundreds of thousands (¥) directional / 数十万（¥）方向性 |
| Remediation / 整改 | Re-train + bias audit + back-offers / 重训 + 偏见审计 + 补发优惠 |
| Legal / 法律 | Equality/consumer-law exposure (¥-range penalty) / 平等消保暴露（区间罚款） |
| Brand / 品牌 | "Club penalizes new mothers" narrative (HI-6-adjacent) / "场馆惩罚新手妈妈"叙事（邻接 HI-6） |

The member's worst moment: reading the model had quietly ranked her as "not worth saving" the week after she gave birth.

会员最难的时刻：读到模型在她生产后那周悄悄把她标为"不值得挽留"。

---

## ④ Root-Cause Analysis / 根因分析

**5-Whys / 五问法**

| # | Why / 为何 | Answer / 答 |
|---|---|---|
| 1 | Why discrimination? / 为何歧视？ | Biased features drove offers / 偏见特征驱动了优惠 |
| 2 | Why biased features? / 为何偏见特征？ | No bias audit before ship / 上线前无偏见审计 |
| 3 | Why no audit? / 为何无审计？ | `templates/24` mandatory section skipped / `templates/24` 强制段落跳过 |
| 4 | Why skipped? / 为何跳过？ | "Ship fast" pressure over governance / "快交付"压过治理 |
| 5 | Why no gate? / 为何无闸？ | HI-6/AI-risk control (G7) not enforced / HI-6/AI 风险闸（G7）未执行 |

**Anti-patterns violated / 违反的反模式**: `#ap-014-churn-autocancel` (spirit: model silently decides member fate) · `#ap-043-churn-train-promo` (spirit: unexamined training data). Core: **no `templates/24` bias audit**.
**HI invariant / 硬不变量**: **HI-6** (dignity / no unfair treatment adjacent) + **HI-8** (minimization — proxies shouldn't infer protected traits). Strained/violated in spirit.

---

## ⑤ The Counterfactual — Library-Guided Path / 反事实——按本库走的路

| Step / 步 | Library action / 本库动作 | Anchor / 锚点 |
|---|---|---|
| 1 | Use bias-audited churn recipe; drop protected/proxy features / 用经审计流失配方；去掉受保护/代理特征 | `data/09#algo-churn` |
| 2 | Run MANDATORY bias-audit parity check before launch / 上线前跑强制偏见审计公平性核查 | `templates/24` |
| 3 | Flag high-risk model with bias/drift/human-in-loop (G7) / 标高风险模型含偏见/漂移/人在回路（G7） | G7 |
| 4 | Model only TRIGGERS human-led save-play, never auto-decides / 模型只触发人工挽留，绝不自动定 | `data/21#md-077` |
| 5 | `tools/05` equality/consumer-law scan pre-deploy / 部署前 `tools/05` 查平等/消保法 | `tools/05` |

---

## ⑥ Early-Warning Checklist (10 signals) / 预警清单

1. Model trained on age / life-stage / proxy features. / 模型用年龄/人生阶段/代理特征训练。
2. No bias-audit section completed (`templates/24`). / 没完成偏见审计段落（`templates/24`）。
3. Offers auto-targeted with no human review. / 优惠自动定向、无人工复核。
4. No per-group parity metric tracked. / 无分组公平性指标。
5. "Ship fast" cited as reason to skip governance. / 以"快交付"为由跳过治理。
6. Protected traits inferable from inputs. / 输入可推知受保护属性。
7. No drift monitoring post-launch. / 上线后无漂移监控。
8. No kill switch on the offer engine (`AP-027`). / 优惠引擎无熔断（`AP-027`）。
9. Members complain of being "forgotten." / 会员抱怨"被遗忘"。
10. No `tools/05` equality-law check. / 未经 `tools/05` 平等法核查。

> One-line takeaway / 一句话: An algorithm must never quietly rank a member as unworthy.
> 算法绝不可悄悄把一个会员标为"不值得"。

---

## ⑦ Related Files / 相关文件

`data/09-algorithm-kernel-library.md` (#algo-churn) · `data/21-anti-pattern-library.md` (#ap-014, #ap-043) · `templates/24-churn-prediction-project.md` · `tools/05` · SKILL.md HI-6, HI-8, G7.

---

## ⑧ G13 Note / G13 注记

- **Architect / 架构师**: fairness is a design constraint; drop proxy features and audit (HI-6/8).
- **Operator / 运营者**: the human-led save-play is the safe path; the model only flags.
- **Member / 会员**: dignity — no one is silently deprioritized by an algorithm. No orphan touchpoint.
- **会员**：尊严——无人被算法悄悄低优先级。无孤儿触点。

> Honesty note / 诚实注记: Archetypal composite; cost figures directional. AI bias law is volatile — verify via `tools/05` and run `templates/24` before any churn-AI deploy.
> 原型复合；成本为方向性。AI 偏见法易变——任何流失 AI 部署前经 `tools/05` 核验并跑 `templates/24`。
