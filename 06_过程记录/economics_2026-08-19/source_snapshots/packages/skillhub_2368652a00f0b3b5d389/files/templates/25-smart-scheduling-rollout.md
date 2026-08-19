# Smart Class Scheduling Rollout / 智能排课上线方案

> **Cluster / 集群**: E (Data & AI) + P (people & org)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Labour-law and coach-employment rules re-verify via `tools/05`; vendor scheduling-module claims 🔄 via `tools/04`.
> **Cross-references / 交叉引用**: `data/09-algorithm-kernel-library.md#algo-scheduling` · `references/04-ai-application-landscape.md#ai-05-smart-scheduling` · `references/13-data-and-llm-engine.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.

---

## ① Purpose & when to use / 用途与适用时机

**Use this template to plan, pilot, and govern an AI-assisted class-scheduling system** that recommends times, rooms, and coach assignments from historical demand — to lift fill-rate and coach utilization without overloading anyone.
**用本模板规划、试点并治理「AI 辅助排课系统」**——基于历史需求推荐时段、教室与教练排班，提升满课率与教练利用率，又不压垮任何人。

> **FDMM gate / FDMM 门槛**: Requires **FDMM ≥ L2** with booking + attendance history in one system. Minimum **≥ 3 months of attendance** (`data/09#algo-scheduling`).
> **FDMM 门槛**：需 **FDMM ≥ L2** 且预约+出勤历史归一系统。最小 **≥ 3 月出勤**（`data/09#algo-scheduling`）。

> **If below the gate / 若未达门槛**: keep manual scheduling in a spreadsheet; the AI only adds value once you have enough history to know *when people actually come*. Do not buy a scheduler you cannot feed.
> **若未达门槛**：继续表格手工排课；只有历史足够、知道*大家真什么时候来*，AI 才增值。别买喂不饱的排课器。

---

## ② Prerequisites checklist / 前置条件清单

- [ ] **Booking + attendance in one system** (not two spreadsheets). / 预约+出勤归一系统（非两份表）。
- [ ] **≥ 3 months attendance by timeslot / coach / room.** / ≥ 3 月各时段/教练/教室出勤。
- [ ] **Coach availability feed** (working days, blackout, max hours). / 教练可用源（工作天、禁排、最高工时）。
- [ ] **Room capacity master** (studio sizes, equipment). / 教室容量主表（操房大小、设备）。
- [ ] **Labour-rule acknowledgement** per market (rest, overtime). / 各市场劳工规则确认（休息、加班）。
- [ ] **A human scheduler owner** who can override any AI suggestion. / 可否决任何 AI 建议的人工排课负责人。
- [ ] **Member-preference signal** available (waitlist, popular slots). / 会员偏好信号可用（候补、热门时段）。

---

## ③ THE TEMPLATE / 模板

### 3.1 Demand baseline capture sheet / 需求基线采集表 {#s1-demand-baseline}

> Capture this BEFORE turning on any optimisation — it is your "before" picture and your ground truth.
> 开启任何优化**前**先采集——这是你的「前」照片与基准真相。

| Timeslot / 时段 | Avg attendance / 平均出勤 | Capacity / 容量 | Fill-rate / 满课率 | Popular? / 热门? | Coach assigned / 教练 |
|---|---|---|---|---|---|
| Mon 07:00 | ___ | ___ | ___% | ☐ | |
| Mon 19:00 | ___ | ___ | ___% | ☐ | |
| Sat 10:00 | ___ | ___ | ___% | ☐ | |
| … | | | | | |

> Micro-example / 微例: a studio shows 19:00 at 95% fill (overbooked waitlist) while 20:00 sits at 30%. The baseline exposes the mismatch the AI should fix.
> 某操房 19:00 满课率 95%（候补爆满）、20:00 仅 30%——基线暴露错配，正是 AI 该修的。

### 3.2 Constraint inventory / 约束清单 {#s2-constraints}

```
Hard constraints (AI must never violate) / 硬约束（AI 绝不可违反）:
- Coach A unavailable Mon/Wed AM  / 教练A 周一三上午不可排
- Room B max 20 pax, no weights    / B房最多20人、无器械
- No coach > X hrs/week (labour law)/ 教练周工时≤X（劳工法）
Soft constraints (optimise toward) / 软约束（尽量优化）:
- Member preference for evening     / 会员偏好晚间
- Coach skill match per class type  / 教练技能匹配课型
```

| Constraint type / 约束类 | Source / 来源 | Owner / 负责人 |
|---|---|---|
| Instructor availability / 教练可用 | coach roster / 排班表 | studio lead |
| Rooms / 教室 | capacity master / 容量主表 | ops |
| Member preference / 会员偏好 | waitlist + survey / 候补+调研 | CS |
| Labour rules / 劳工规则 | market law / 市场法 | HR/legal |

### 3.3 Pilot design (2 studios × 6 weeks) / 试点设计（2 店 × 6 周） {#s3-pilot}

> Pilot before chain-wide rollout — two studios with different member mixes de-risk the model.
> 全连锁铺开前先试点——两家会员结构不同的店可降风险。

| Week / 周 | Activity / 动作 | Success signal / 成功信号 |
|---|---|---|
| 1–2 | Baseline + shadow mode (AI suggests, human decides) / 基线+影子模式（AI 建议、人决定） | human accepts ≥60% of suggestions / 人采纳≥60%建议 |
| 3–4 | Assisted mode (AI auto-draft, human edits) / 辅助模式（AI 起草、人改） | fill-rate +5pp vs baseline / 满课率较基线+5pp |
| 5–6 | Measure + fairness review / 度量+公平复核 | no coach-overload complaints / 无教练过载投诉 |

- Pick **2 studios** differing in size/format (e.g. mega + boutique). / 选 **2 家**规模/业态不同的店（如综合+精品）。
- Keep a **control store** for comparison. / 留一家**对照店**比对。

### 3.4 Fairness rules for instructors / 教练公平规则 {#s4-fairness}

> An optimizer that quietly dumps all 07:00 classes on one coach will cause turnover. Fairness is a hard constraint, not a nice-to-have.
> 优化器偷偷把全部 07:00 课压给一个教练，会致流失。公平是硬约束，非锦上添花。

- [ ] Max weekly hours cap per coach (labour-law aligned). / 每教练周工时上限（对齐劳工法）。
- [ ] Rotation of unpopular slots across the team. / 冷门时段全队轮值。
- [ ] Coach skill → class-type match respected. / 教练技能→课型匹配被尊重。
- [ ] No silent reassignment; coach sees changes. / 不静默改排；教练可见变更。

### 3.5 Fill-rate & no-show KPI targets / 满课率与爽约 KPI 目标 {#s5-kpi}

| KPI / 指标 | Baseline / 基线 | Target / 目标 | Caveat / 注意 |
|---|---|---|---|
| Avg fill-rate / 平均满课率 | ___% | +5 to +10pp | not by overbooking / 非靠超卖 |
| Idle-room hours / 空房小时 | ___h | −20% | keep popular slots / 保热门 |
| Coach utilization / 教练利用率 | ___% | +5pp | within labour cap / 不超工时 |
| No-show rate / 爽约率 | ___% | −30% | see waitlist rule / 见候补规则 |

> **Honesty red line / 诚实红线**: targets are *directional ranges*, not guarantees. Overbooking to hit fill-rate hurts trust (ironically raising churn). State lift as a range measured on your pilot, not a vendor claim.
> **诚实红线**：目标为*方向性区间*，非保证。为满课率超卖会伤信任（反升流失）。提升以试点实测区间给出，非厂商宣称。

### 3.6 Override governance (human always wins) / 否决治理（人永远胜出） {#s6-override}

> **HI-2 spirit**: AI assists; the human scheduler retains final authority. Any AI suggestion can be overridden with one click and the reason logged.
> **HI-2 精神**：AI 辅助；人工排课负责人保有最终权。任何 AI 建议可一键否决并记原因。

- Every AI draft is labelled "AI suggestion — pending human confirm." / 每个 AI 草稿标「AI 建议——待人工确认」。
- Coach can flag a slot as "unavailable" and the system must respect it. / 教练可标某时段「不可排」，系统须尊重。
- Override log kept for retrospective + model improvement. / 否决日志留存供复盘+模型改进。

### 3.7 Member communication on schedule changes / 排课变更会员沟通 {#s7-communication}

> A silently moved class angers members more than a well-explained one. Communicate changes the optimizer makes.
> 静默改课比解释清楚的改课更惹怒会员。把优化器做的变更沟通出去。

- [ ] Changed slots push an IM/notification ≥ 48h ahead (HI-7 opt-in + unsubscribe). / 变更时段提前≥48h 推 IM/通知（HI-7 同意+退订）。
- [ ] Waitlisted members auto-notified of opened spots. / 候补会员自动通知空位。
- [ ] One-line "why" (e.g. "added 20:00 by demand") builds trust. / 一句话「为何」（如「按需求加 20:00」）建信任。

---

## ④ Common mistakes / 常见误区

- **No baseline** → cannot prove the AI helped. / 无基线→无法证明 AI 有用。
- **Overfitting last month's holiday anomaly** → wrong patterns. / 过拟合上月假期异常→错误模式。
- **Ignoring coach preference** → turnover, resentment. / 忽视教练偏好→流失、抵触。
- **Overbooking to hit KPI** → member anger, churn. / 为 KPI 超卖→会员怒、流失。
- **Locking the AI** with no override → unsafe, untrusted. / 锁死 AI 无否决→不安全、不获信。

> Full remedy catalogue: `data/21-anti-pattern-library.md`.
> 完整对策：见 `data/21-anti-pattern-library.md`。

---

## ⑤ Related files / 相关文件

- `data/09-algorithm-kernel-library.md#algo-scheduling` — method, eval, min-data. / 方法、评估、最小数据。
- `references/04-ai-application-landscape.md#ai-05-smart-scheduling` — use-case scope. / 用例范围。
- `references/13-data-and-llm-engine.md#k-52-human-in-loop` — human override principle. / 人工否决原则。
- `data/09-algorithm-kernel-library.md#algo-rostering` — staffing fairness link. / 排班公平联动。

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: FDMM L2 gate + ≥3mo data + hard/soft constraint split + pilot-before-rollout (Iron Law 5 stage-gate).
- **Operator / 运营者**: baseline sheet, constraint inventory, 2-studio × 6-week pilot, fairness rules, KPI dashboard, one-click override.
- **Member / 会员**: better-filled popular classes, fewer cancelled sessions, no overbooking denial; coach well-being preserved so session quality stays high.
本文件覆盖架构师（FDMM L2 门槛+≥3月数据+硬软约束分离+试点后铺开，铁律5 流程遵循）、运营者（基线表、约束清单、2店×6周试点、公平规则、KPI 看板、一键否决）、会员（热门课更满、少取消、不致超卖拒入；教练状态好故课质稳）。
