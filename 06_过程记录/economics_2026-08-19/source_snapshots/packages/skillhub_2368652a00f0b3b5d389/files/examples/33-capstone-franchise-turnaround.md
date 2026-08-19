# 33 · Capstone: 30-Unit Franchise Network Digital Turnaround / 案例 33：30 店加盟网络数字化翻身战

> **Cluster / 集群**: B (software) · I (governance) · W (growth) · P (people) · L (architecture)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: vendor/aggregator terms 🔄 via `tools/04`; compliance per `tools/05` every 90d; ROI per `tools/06`.
> **Cross-references / 交叉引用**: `templates/42-franchise-digital-kit.md` · `references/19-growth-and-sales-stack.md` · `playbooks/05` (governance) · `data/15-procurement-and-cost-benchmark.md` · `data/21-anti-pattern-library.md` · `references/04` (churn AI)
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## Honesty Preamble / 诚实前言

> Archetypal composite case for teaching — an amalgam of franchise-network rescues observed across APAC. **Not** a claimed real franchise. Figures directional; the two exiting franchisees are illustrative, not named.
> 典型复合教学案例——糅合亚太加盟网络拯援常见模式。**非**真实加盟体系。数字方向性；退出两加盟商为示意非具名。

> Franchisee internal dynamics are real and messy; this case shows the council dynamics, not a sanitized success. Two franchisees refused and exited — that is part of the story, not a footnote.
> 加盟商内部博弈真实且 messy；本案示理事会动态非粉饰成功。两加盟商拒从退出——是故事一环非脚注。

---

## ① Context Card / 情境卡

| Field / 字段 | Value / 值 |
|---|---|
| Archetype / 原型 | 30-unit franchise network, 1 country / 30 店加盟网络，单国 |
| Starting state / 起点 | fragmented: every franchisee different stack, HQ blind / 碎片化：各加盟商栈各异、总部失明 |
| Target FDMM / 目标 | L2→L3 group (unified ID + group BI + scorecards) / L2→L3 集团（统一 ID+集团 BI+计分卡） |
| Timeline / 周期 | 18 months / 18 个月 |
| Pain / 痛点 | viral complaints, no data at HQ, aggregator over-dependence / 投诉 viral、总部无数据、过度依赖聚合平台 |
| Honesty scope / 诚实范围 | composite; directional; 2 exits / 复合；方向性；2 家退出 |

---

## ② Multi-Phase Journey / 多阶段旅程（18 个月）

### Phase 1 — Diagnose the Fragmentation (M1–3) / 阶段一 诊断碎片化

**Situation / 形势**: HQ had no consolidated view — 30 clubs ran 11 different MMS, 7 POS, and 4 booking apps. Member complaints about "double-charged" and "lost bookings" went viral on local socials.
**形势**：总部无统览——30 店跑 11 套 MMS、7 套 POS、4 套约课 App。会员「重复扣费」「约课丢失」投诉在本地社媒 viral。

**Decision forks considered / 决策分叉**:
- *Fork — mandate overnight vs negotiate.* Rejected "mandate overnight": franchise contract + trust gap would trigger mass revolt. Chose **negotiate via franchisee council** per `templates/42`.
  *分叉 — 一夜强推 vs 谈判。否决「一夜强推」：加盟合同+信任缺口会引爆集体反水。选**经加盟商理事会谈判**（templates/42）。*
- *Fork — build custom vs adopt reference stack.* Chose **adopt a reference stack** (Iron Law 8 ≥3 options) to cut cost & time.
  *分叉 — 自研 vs 用参考栈。选**采用参考栈**（铁律8 ≥3 选项）省本省时。*

**Library artifacts used / 引用库工件**: `templates/42-franchise-digital-kit.md` · `references/06-software-landscape-apac-vendors.md` · `data/21#fragmented-stack` anti-pattern.
**Outcome / 结果**: A fragmentation map (11→1 reference MMS) and a council mandate to discuss migration.
**结果**：碎片化图（11→1 参考 MMS）与理事会迁移讨论授权。

### Phase 2 — The Franchisee Council Dynamics (M3–6) / 阶段二 加盟商理事会内部博弈

**Situation / 形势**: The council split: 18 "ready" franchisees, 8 "wait-and-see", 4 "hostile" (one ran his own profitable stack and feared losing edge).
**形势**：理事会分裂：18「就绪」、8「观望」、4「敌意」（一家的自有盈利栈怕失优势）。

**Decision forks considered / 决策分叉**:
- *Fork — uniform deadline vs wave migration.* Chose **phased waves** (ready first, then wait-and-see, then holdouts) — reduces revolt risk, proves value.
  *分叉 — 统一死线 vs 波次迁移。选**分波次**（先就绪、再观望、后钉子户）——降反水险、证价值。*
- *Fork — fund HQ-only vs co-invest.* Chose **co-invest model**: HQ pays integration, franchisee pays local license — aligns incentive.
  *分叉 — 仅总部出资 vs 共投。选**共投模型**：总部付集成、加盟商付本地许可——利益对齐。*

**Library artifacts used / 引用库工件**: `templates/42` §council-dynamics · `data/15-procurement-and-cost-benchmark.md` (3-quote rule) · `references/19` §W1–W12 (growth rebuild later).
**Outcome / 结果**: Wave-1 (18 clubs) approved; hostile 4 given a 6-month observation window.
**结果**：波次一（18 店）通过；敌意 4 家获 6 月观察窗。

### Phase 3 — Phased Migration Waves + NOC & Scorecards (M6–12) / 阶段三 分波迁移 + NOC 与计分卡

**Situation / 形势**: Wave-1 migrated to unified MMS + QR entry; HQ stood up a small NOC and a franchise scorecard (attendance, complaints, SLA).
**形势**：波次一迁至统一 MMS+扫码；总部立小 NOC 与加盟计分卡（到店、投诉、SLA）。

**Decision forks considered / 决策分叉**:
- *Fork — big-bang wave-2 vs proof-first.* Chose **proof-first**: wave-1 scorecard shown to wait-and-see group before wave-2.
  *分叉 — 波次二big-bang vs 先证。选**先证**：波次一计分卡示观望群后再波次二。*
- *Fork — punish low scorers vs coach.* Chose **coach + public leaderboard** — shame-light not blame.
  *分叉 — 罚低分 vs 辅导。选**辅导+公开榜**——点名不责。*

**Library artifacts used / 引用库工件**: `playbooks/05` §NOC-scale · `data/01-kpi-benchmark-library.md` (scorecard KPIs) · `references/08` (NOC infra).
**Outcome / 结果**: Wave-2 (8 clubs) migrated by M12; complaints at HQ down 40%; unified ID reached 26/30 clubs.
**结果**：波次二（8 店）M12 迁完；总部投诉降 40%；统一 ID 达 26/30 店。

### Phase 3.5 — NOC Runbook Snapshot / 阶段 3.5 NOC 手册快照

**Goal / 目标**: The small HQ NOC needed a repeatable incident rhythm so a franchisee outage was "managed," not "panicked." This snapshot is what the scorecard ran on.
**目标**：小总部 NOC 需可复事故节奏，使加盟商宕机「受管」非「慌」。此快照即计分卡所跑。

| Cadence / 节奏 | Action / 动作 | Owner / 主 |
|---|---|---|
| Daily / 每日 | attendance + complaint scan / 到店+投诉扫 | NOC analyst / NOC分析师 |
| Weekly / 周 | scorecard to council / 计分卡送理事会 | franchise success mgr / 加盟成功经理 |
| Monthly / 月 | backup restore drill / 备恢演练 | integration PM / 集成PM |
| Quarterly / 季 | cross-club incident tabletop / 跨店事故桌面 | NOC lead / NOC负责 |

The drill discipline came straight from `playbooks/13` W5–6 (backup/restore) and `playbooks/08` R1 — a franchisee never again waited 3 hours for HQ to "look into it."
**演练纪律直承 playbooks/13 第5–6周（备恢）与 playbooks/08 R1**——加盟商再不等总部 3 小时「查查」。

**Wave migration timeline / 波次迁移时间线**:

| Wave / 波 | Clubs / 店 | Window / 窗口 | Trigger / 触发 |
|---|---|---|---|
| Wave 1 / 一波 | 18 ready / 就绪 | M6–M9 | council approved / 理事会批 |
| Wave 2 / 二波 | 8 wait-see / 观望 | M9–M12 | scorecard proof / 计分卡证 |
| Holdouts / 钉子户 | 4 → 2 exited / 退2 | M10 | 6-mo window lapsed / 观察窗过 |
| Final / 终 | 26→28 live / 在线 | M12–M18 | growth rebuild / 增长重建 |

The wave model is why the pessimistic "mass revolt" scenario never fired — each wave proved value before the next was asked to move.
**波次模型即悲观「集体反水」未燃因**——每波证价值于下一波被请动前。

### Phase 4 — Growth Stack Rebuild: Kill Aggregator Dependence (M12–18) / 阶段四 增长栈重建：斩聚合平台依赖

**Situation / 形势**: The network relied on a third-party aggregator for 60% of new leads — high CAC, zero owned data, and a term change 🔄 threatened margins.
**形势**：网络 60% 新客靠第三方聚合平台——高 CAC、零自有数据，且条款变更🔄 威胁毛利。

**Decision forks considered / 决策分叉**:
- *Fork — stay on aggregator vs build own funnel.* Rejected "stay": `references/19` W1–W12 shows owned-funnel compounding. Chose **rebuild own growth stack** (paid CAPI + SCRM private domain + group-buy + live-commerce), keeping aggregator as one channel of many.
  *分叉 — 留聚合 vs 建自有漏斗。否决「留」：references/19 W1–W12 示自有漏斗复利。选**重建增长栈**（付费 CAPI+SCRM 私域+团购+直播），聚合降为多渠道之一。*
- *Fork — hire agency vs in-house.* Chose **in-house pod + agency retainer** for speed, then insource.
  *分叉 — 雇代理 vs 自建。选**内部小队+代理 retain** 提速，后内收。*

**Library artifacts used / 引用库工件**: `references/19-growth-and-sales-stack.md` (W1–W12) · `data/21#aggregator-lockin` · `references/17` (SCRM consent, HI-7).
**Outcome / 结果**: Owned-funnel share rose 30%→55%; CAC down ~22%; first-party member data finally at HQ.
**结果**：自有漏斗占比 30%→55%；CAC 降约 22%；一手会员数据终归总部。

### Phase 4.5 — Growth Stack Mapped to W1–W12 / 阶段 4.5 增长栈映射 W1–W12

**Goal / 目标**: `references/19` covers the full W1–W12 growth stack; this network did not need all 12 at once. The map below shows what was rebuilt and when, killing aggregator over-dependence.
**目标**：references/19 覆盖完整 W1–W12 增长栈；本网络不需一次全上。下表示重建了什么、何时，斩聚合依赖。

| Wave / 波 | W-code / 码 | Rebuilt / 重建 | Killed / 斩 |
|---|---|---|---|
| W1 | W1 paid CAPI / 付费CAPI | pixel + CAPI to MMS / 像素+CAPI接MMS | blind paid spend / 盲投 |
| W2 | W4 SCRM private / 私域SCRM | WeCom/Line group + opt-in / 企微/Line群+Opt-in | aggregator-only leads / 仅聚合客 |
| W3 | W7 group-buy / 团购 | local group-buy campaign / 本地团购 | coupon spam / 优惠券骚扰 |
| W4 | W9 live-commerce / 直播 | monthly membership livestream / 月会员直播 | — |
| Cap / — | aggregator cap / 聚合封顶 | kept as 1 of many / 作多渠之一 | 60%→40% share / 占比60→40% |

HI-7 consent enforced at every W-step: no opt-in, no message. The aggregator became a channel, not the customer relationship.
**每 W 步守 HI-7 Opt-in**：无同意不发送。聚合成渠道非客户关系。

### Council Meeting Dynamics (honest excerpt) / 理事会动态（诚实节选）

The hostile franchisee #1 opened M4 with: *"You're forcing my stack out so HQ can spy."* The facilitator (per `templates/42` §council-dynamics) reframed: **"Unified ID means a member can freeze their own account across all clubs if they move — that protects your customers too."** He went silent, then asked about the data-export clause. That question was the turning point — he was negotiating, not revolting.
**敌意加盟商#1 在 M4 开场**：「你们逼我弃栈是要总部监视。」协调人（templates/42 §理事会动态）重框：**「统一 ID 意味着会员搬家可跨店冻结自身账户——也护你客户。」**他沉默后问数据导出条。那问是转折点——他在谈非反。

---

## ③ Three Major Setbacks & Recovery / 三大挫折与复原

**Setback 1 — Hostile franchisee #1 threatened to sue / 挫折一 敌意加盟商#1 扬言起诉**: Feared losing his custom stack edge. Recovery: gave him the 6-month window + co-invest cap; he later joined wave-2 voluntarily after seeing scorecard gains. Lesson: observation window beats litigation.
**挫折一**：怕失自有栈优势。复原：给 6 月窗+共投上限；见计分卡增益后自愿入波次二。教训：观察窗胜诉讼。

**Setback 2 — Migration data loss in wave-1 / 挫折二 波次一迁移数据丢失**: A botched CSV import dropped 600 member records. Recovery: restore from pre-migration backup (`templates/34` discipline from `playbooks/13`), re-import with validation; SLA credit issued. Lesson: tested backup is the only backup.
**挫折二**：CSV 导入失误丢 600 会员记录。复原：从迁移前备恢复（playbooks/13 的 templates/34 纪律）、校验重导；发 SLA 补偿。教训：测过的备份才是备份。

**Setback 3 — Aggregator term change shock / 挫折三 聚合平台条款变脸**: 🔄 Mid-program the aggregator raised take-rate 4pp. Recovery: already building owned funnel; accelerated it, capped aggregator at 40%. Lesson: `references/19` owned-funnel is insurance.
**挫折三**：🔄 聚合中途抽成涨 4pp。复原：自有漏斗已在建；加速、聚合封顶 40%。教训：references/19 自有漏斗即保险。

**Setback 4 (honesty) — 2 franchisees exited / 挫折四（诚实）2 家加盟商退出**: Two refused migration (one hostile, one indifferent) and exited at M10. Recovery: their clubs de-branded; remaining 28 stronger. Lesson: 100% adoption is a myth; a clean exit is a valid outcome.
**挫折四（诚实）**：2 家拒迁（一敌意一中立）M10 退出。复原：门店去品牌；余 28 家更强。教训：100% 采纳是神话；干净退出是有效结局。

---

## ④ Financials View (Directional) / 财务视角（方向性）

**Investment envelope / 投资带**: directional ¥4–7M over 18 months — integration (HQ-paid) 40%, local licenses (franchisee-paid) 25%, NOC+scorecard 15%, growth-stack rebuild 20%.
**投资带**：18 个月 400–700 万元——集成(总部付)40%、本地许可(加盟商付)25%、NOC+计分卡 15%、增长栈重建 20%。

**Payback narrative / 回收叙事**: Levers — complaint-driven churn cut (retention +3pp), CAC down 22% via owned funnel, consolidated procurement ~10%, 2 exits removed drag. Directional payback 16–26 months.
**回收叙事**：杠杆——投诉致流失降(留存+3pp)、自有漏斗 CAC 降 22%、集中采购约 10%、2 退出去拖累。方向性回收 16–26 月。

**Three-scenario retrospective per `tools/06` / 三情景复盘（按 tools/06）**:

| Scenario / 情景 | Assumed / 假设 | Landed? / 落点 |
|---|---|---|
| Base / 基准 | 26/30 migrated, payback 22mo / 26/30 迁、回收 22 月 | Landed / 落点 |
| Expected / 预期 | CAC -25%, retention +4pp / CAC-25%、留存+4pp | **CAC missed (-22%), retention near (+3pp)** / CAC 未达(-22%)、留存近(+3pp) |
| Pessimistic / 悲观 | mass revolt, 10 exits / 集体反水、10 退 | **Avoided** — wave model + 2 clean exits only / 规避——波次模型+仅 2 净退 |

**Did expected case land? / 预期是否落地？**: Near. CAC lagged as owned-funnel ramped slower than modeled, but the revolt risk (pessimistic) never materialized thanks to the council + wave design. Net positive, slightly below expected midpoint.
**预期是否落地？**：近。CAC 因自有漏斗慢于模型而滞后，但悲观情景（集体反水）因理事会+波次设计未现。净正，略低于预期中值。

**Savings-lever detail (directional) / 节支杠杆明细（方向性）**:

| Lever / 杠杆 | Expected / 预期 | Landed / 落点 |
|---|---|---|
| Retention (+complaint cut) / 留存 | +4pp | +3pp (near) |
| CAC (owned funnel) / CAC | -25% | -22% (miss) |
| Consolidated procurement / 集中采购 | -10% | ~10% (beat) |
| 2 exits removed drag / 2退出去拖累 | — | realized / 实现 |
| Aggregator take-rate shock / 聚合涨抽 | -4pp margin | capped at 40% / 封顶40% |

**What we would redo / 重做之处**: (1) Start the owned-funnel build in wave-1, not wave-2 — CAC would have hit target; (2) give hostile franchisees the data-export clause answer in week 1, not month 4; (3) write the exit clause into the franchise contract template before the next expansion.
**重做之处**：(1) 自有漏斗波次一即建非二——CAC 可达标；(2) 敌意加盟商首周即得数据导出条答案非第4月；(3) 退出条款写入加盟合同模板再扩。

---

## ⑤ Org & People Evolution / 组织与人才演进

- **M1**: HQ 3-person admin, no data role, no NOC. / 总部 3 人行政，无数据岗无 NOC。
- **M6**: Franchisee council operational; integration PM hired. / 理事会运转；设集成 PM。
- **M12**: NOC + scorecard analyst; growth pod stood up. / 立 NOC+计分卡分析师；增长小队就位。
- **M18**: 28 energized franchisees on unified stack; a "franchise success manager" role created.
**M18**：28 家活力加盟商上统一栈；设「加盟成功经理」岗。

The shift: from **HQ blind / franchisees isolated** to **council-governed shared stack**. The two exits were painful but clarified the network's standard.
**转变**：从**总部盲/加盟商孤岛**到**理事会治下的共享栈**。两退出痛但厘清了网络标准。

**Network health scorecard (M1 vs M18) / 网络健康计分卡（M1 vs M18）**:

| Metric / 指标 | M1 / 月1 | M18 / 月18 |
|---|---|---|
| Unified ID coverage / 统一ID覆盖 | 0% | 93% (28/30) |
| HQ data visibility / 总部可见 | blind / 盲 | daily dashboard / 日看板 |
| Complaints (viral) / 投诉(viral) | high / 高 | -40% / 降40% |
| CAC / 获客成本 | baseline / 基准 | -22% / 降22% |
| Owned-funnel share / 自有漏斗 | 30% | 55% / 55% |
| Franchisee sentiment / 加盟商情绪 | split / 裂 | 28 energized / 28活力 |

The scorecard is what the council reviewed monthly — proof the shared stack paid, not just a promise.
**计分卡即理事会月审物**——证共享栈有回报非空诺。

---

## ⑥ Ten Transferable Lessons / 十条可迁移经验

1. **Diagnose fragmentation before mandating** — 11 stacks mapped first. / 强推前先诊断碎片化——先绘 11 栈。
2. **Council, not decree** — `templates/42` turned internal dynamics into a process. / 理事会非命令——templates/42 把内部博弈变流程。
3. **Wave migration beats big-bang** — proof-first reduces revolt. / 波次胜 big-bang——先证降反水。
4. **Co-invest aligns incentive** — HQ integration, franchisee license. / 共投对齐利益——总部集成、加盟商许可。
5. **Scorecard = coach, not blame** — public leaderboard shamed gently. / 计分卡=辅导非责——公开榜轻点名。
6. **Owned funnel is insurance** — `references/19` saved the CAC shock. / 自有漏斗即保险——references/19 救 CAC 冲击。
7. **Aggregator cap at 40%** — never let one channel own the member. / 聚合封顶 40%——莫让一渠拥有会员。
8. **Tested backup only** — 600 records lost, restored clean. / 唯测过的备份——600 条丢、净恢复。
9. **Clean exit is valid** — 2 refusals de-branded, network stronger. / 干净退出有效——2 拒去牌、网络更强。
10. **HI-7 in SCRM** — private-domain consent respected or complaints return. / SCRM 守 HI-7——私域须 Opt-in 否则投诉回潮。

---

## ⑦ Related Files / 相关文件

- `templates/42-franchise-digital-kit.md` — the council playbook. / 理事会手册。
- `references/19-growth-and-sales-stack.md` — W1–W12 owned funnel. / W1–W12 自有漏斗。
- `data/15-procurement-and-cost-benchmark.md` — 3-quote rule. / 三报价规则。
- `data/21-anti-pattern-library.md` — fragmented-stack, aggregator-lockin. / 碎片化、聚合锁定。
- `references/06` · `references/08` · `references/17` — software, NOC, SCRM. / 软件、NOC、SCRM。
- `tools/06-roi-three-scenario.md` — ROI framing. / ROI 框架。

---

## ⑧ G13 Note / G13 注记

**Architect / 架构师**: Unified ID + reference stack chosen with ≥3 options (Iron Law 8); data-export clause in every franchisee contract; aggregator capped; SCRM consent (HI-7) built into the growth stack. Cross-club data stays within the network's residency basis.
**架构师**：统一 ID+参考栈（铁律8 ≥3 选项）；每加盟合同带数据导出条；聚合封顶；SCRM 守 HI-7。跨店数据留网络驻留依据内。

**Operator / 运营者**: The NOC + scorecard turned 30 blind clubs into a managed network; wave migration meant no club was thrown in cold. Backup discipline (`templates/34`) turned a data-loss scare into a non-event.
**运营者**：NOC+计分卡把 30 盲店变受管网；波次迁移无店被冷抛。备份纪律（templates/34）使数据丢失惊魂成无事件。

**Member / 会员**: "Double-charged" and "lost booking" complaints fell 40% as stacks unified; their data consolidated once, not re-keyed per club; private-domain messages come only with consent (HI-7).
**会员**：栈统一后「重复扣费」「约课丢失」投诉降 40%；数据合一非逐店重录；私域消息仅 Opt-in 达（HI-7）。

> **G13 coverage confirmed / 三视角覆盖确认**: Architect × Operator × Member all承接, no orphan touchpoint. / 三视角均已承接，无孤儿触点。
