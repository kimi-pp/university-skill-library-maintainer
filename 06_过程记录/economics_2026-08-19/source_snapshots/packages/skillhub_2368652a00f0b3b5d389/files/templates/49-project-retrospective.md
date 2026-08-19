# Project Retrospective (Universal Closer) / 项目复盘（通用收尾）

> **Cluster / 集群**: X (Methodology) · lifecycle G6 Retrospective / 全生命周期 G6 复盘阶段
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Benchmark ranges for adoption/ROI are club-specific — re-verify against YOUR `data/01` + `tools/06`, not generic figures; vendor SLA norms via `tools/04`. / 采纳/ROI 基准因馆而异——以你的 `data/01`+`tools/06` 为准，勿用通用数；供应商 SLA 经 `tools/04` 核。
> **Cross-references / 交叉引用**: `templates/07-roi-business-case.md` (planned) · `templates/21-vendor-evaluation-matrix.md` (planned) · `tools/06-roi-three-scenario.md` · `references/18-integration-and-data-plumbing.md` (integration inventory) · `playbooks/08-emergency-runbooks.md` (runbooks) · `data/15-procurement-and-cost-benchmark.md` (asset/VAR register) · `data/21-anti-pattern-library.md` · `tools/01-fdmm-maturity-assessment.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## 1. Purpose & when to use / ① 用途与使用时机

**English / 英文**: The universal closer for ANY digital/AI project — a membership-CRM rollout, a gate upgrade, an AI churn model, a W1–W12 growth program, an unmanned-period pilot. Run it at the lifecycle Retrospective stage (`references/19` G6) to honestly answer: did the promised ROI materialize, what broke, and what do we carry forward? It is the feedback loop that makes the next project smarter.

**中文 / 中文**: 任何数字化/AI 项目的通用收尾——会籍 CRM 上线、闸机升级、AI 流失模型、W1–W12 增长项目、无人时段试点。在生命周期复盘阶段（`references/19` G6）运行，诚实回答：承诺的 ROI 兑现了吗、哪里破了、下一步带什么走？它是让下一个项目更聪明的反馈环。

> **Use this retrospective when / 用本复盘当**:
> - A project has gone live and run ≥30 days (need 30/60/90 adoption data). / 项目已上线且运行 ≥30 天（需 30/60/90 采纳数据）。
> - A business case (`templates/07`, planned) or ROI three-scenario (`tools/06`) was produced at investment decision. / 投资决策时出过商业论证（`templates/07`）或 ROI 三情景（`tools/06`）。
> - A vendor was involved and you will select again (`templates/21`, planned). / 涉及供应商且将再次选型（`templates/21`）。

---

## 2. Prerequisites / ② 前置条件

- [ ] **Business case exists / 商业论证存在**: `templates/07-roi-business-case.md` (planned) or `tools/06` three-scenario output from investment stage. / 投资阶段产出。
- [ ] **Project has gone live / 已上线**: go-live date recorded; ≥30 days of real operation. / 已记录上线日，真实运行 ≥30 天。
- [ ] **Data exported / 数据已导出**: actual spend, adoption, incident, vendor SLA logs available. / 实际花费、采纳、事故、供应商 SLA 日志齐备。
- [ ] **Stakeholders available / 干系人在位**: owner + operator + (if vendor) vendor contact for scoring. / 老板+运营+（若有）供应商对接人。
- [ ] **Honesty agreed / 诚实共识**: report REAL numbers; no rounding failures into wins. / 报真实数；不把失败抹成胜利。

---

## 3. THE TEMPLATE / ③ 模板（填空式）

### 3.1 Outcomes vs business-case / 结果对商业论证 {#outcomes-vs-business-case}
> **Honesty rule / 诚实规则**: Report real numbers. If promised ROI did not materialize, say so and state why — that is the whole point of a retrospective. / 报真实数；承诺 ROI 未兑现就明说并写原因——这正是复盘意义。

| Promised / 承诺 (base·expected·pessimistic) | Actual / 实际 | Verdict / 结论 |
|---|---|---|
| Revenue / 营收: `____` | `____` | met / missed / 达成·未达 |
| Cost saved / 成本省: `____` | `____` | `____` |
| Compliance / 合规: `____` | `____` | `____` |
| Member experience / 会员体验: `____` | `____` | `____` |

> **Link / 链接**: promised figures come from `templates/07-roi-business-case.md` (planned) / `tools/06-roi-three-scenario.md`. If none was written, flag "no baseline → cannot judge ROI" — and write one next time. / 承诺值来自 `templates/07`/`tools/06`；若当初没写，标"无基线→无法判 ROI"，下次必写。

### 3.2 Timeline & budget variance / 时间与预算偏差 {#timeline-budget}
- **Planned go-live / 计划上线**: `____` → **Actual / 实际**: `____` → **Variance / 偏差**: `____ days`
- **Planned budget / 计划预算**: `____` → **Actual / 实际**: `____` → **Variance / 偏差**: `____%`
- **Biggest driver of variance / 最大偏差动因**: `____`

### 3.3 What went well / what hurt / what we'd change / 好·伤·改 {#well-hurt-change}
| What went well / 做得好 | What hurt / 伤处 | What we'd change / 要改 |
|---|---|---|
| `____` | `____` | `____` |

> **Guidance / 指引**: "What hurt" is not blame — it is the risk register for the next project. Be specific (which integration, which week). / "伤处"非追责，是下一项目的风险登记；要具体（哪个集成、哪一周）。

### 3.4 Vendor performance score / 供应商绩效评分 {#vendor-score}
> **Feeds / 反哺**: this score feeds `templates/21-vendor-evaluation-matrix.md` (planned) next time — close the loop. / 本分反哺下次 `templates/21` 选型，闭环。

| Criterion / 维度 | Weight / 权重 | Score 1–5 / 评分 | Note / 备注 |
|---|---|---|---|
| Delivery on time / 准时交付 | `____` | `____` | `____` |
| Support quality / 支持质量 | `____` | `____` | `____` |
| Data-export capability (HI-9) / 数据导出 (HI-9) | `____` | `____` | `____` |
| SLA adherence / SLA 履约 | `____` | `____` | `____` |
| Cost vs quote / 费用对报价 | `____` | `____` | `____` |
| **Weighted total / 加权总分** | — | `____` | re-select? / 是否复选: `____` |

:::dynamic-hook topic="vendor-sla-benchmark-norms-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07: vendor SLA norms (uptime %, response time, on-site fix window) and support-tier pricing differ by market and shift — verify current norms via tools/04 before scoring "SLA adherence" or negotiating the next contract. / 截至 2026-07：供应商 SLA 常态（在线率%、响应时长、上门修复窗）与支持层级定价因市场而异且会变——评"SLA 履约"或谈下份合同前经 tools/04 核当前常态。
:::

### 3.5 Adoption metrics 30 / 60 / 90 days / 30·60·90 天采纳 {#adoption-30-60-90}
| Metric / 指标 | 30d | 60d | 90d | Target / 目标 |
|---|---|---|---|---|
| % staff active / 员工活跃率 | `____` | `____` | `____` | `____` |
| Feature adoption / 功能采纳 | `____` | `____` | `____` | `____` |
| Training completion / 培训完成 | `____` | `____` | `____` | `____` |
| Member-facing usage / 会员端使用 | `____` | `____` | `____` | `____` |

> **Read / 解读**: a tool nobody adopts is a cost, not a win — even if ROI math looked fine. / 没人用的工具是成本非胜利，即便 ROI 算得好看。

### 3.6 Knowledge capture / 知识沉淀 {#knowledge-capture}
> **List which library files to update / 列出要更新的库文件** so the next team inherits the learning:
- **Asset / VAR register / 资产与供应商台账**: `data/15-procurement-and-cost-benchmark.md` — add vendor score (§3.4). / 加供应商评分。
- **Integration inventory / 集成清单**: `references/18-integration-and-data-plumbing.md` — record new webhooks/ID-resolution/consent-ledger links. / 记新 webhook/身份解析/同意台账链接。
- **Runbooks / 运维手册**: `playbooks/08-emergency-runbooks.md` — add ops procedures learned. / 加运维流程。
- **Fault trees / 故障树**: `data/10~12` — if new failure modes found, log them. / 发现新故障模式则记。
- **Micro-details / 微细节**: `data/20-micro-details-ledger.md` — capacity/rate-limit lessons. / 承接/限流教训。
- **Anti-patterns / 反模式**: `data/21-anti-pattern-library.md` — log any new pitfall + remedy. / 记新坑+对策。
- **FDMM level / 成熟度**: update `tools/01-fdmm-maturity-assessment.md` if capability moved. / 能力晋级则更新。

### 3.7 Celebration & credit note / 表彰与署名 {#celebration-credit}
> **Principle / 原则**: People adopt what they're praised for. Name the humans who made it work — front-desk, coach, advisor, IT, vendor contact. / 人被表扬才会采纳。点名让项目成功的人——前台、教练、顾问、IT、供应商对接。

- **Credit / 署名**: `____` (who did what well)
- **Celebrate / 庆祝**: `____` (team note / small ritual)
- **Carry-forward owner / 后续负责人**: `____` (who owns the captured knowledge + next iteration)

### 3.8 Retrospective facilitator script / 复盘主持脚本 {#facilitator-script}
> **Guidance / 指引**: 45–60 min, owner + operator + (vendor if scored). Read the numbers first, feelings last. / 45–60 分钟，老板+运营+（评分则供应商）。先看数，后谈感。

1. **Open / 开场** (5m): state the honesty rule — real numbers, no spin. / 诚实规则：真实数，不粉饰。
2. **Outcomes / 结果** (15m): walk §3.1 row by row; if "missed", state root cause, not excuse. / 逐行走 §3.1；"未达"写根因非借口。
3. **Well / hurt / change / 好伤改** (15m): §3.3; capture specifics. / 走 §3.3，记具体。
4. **Vendor / 供应商** (10m, if any): §3.4 score → re-select decision. / 走 §3.4→复选决策。
5. **Knowledge / 知识** (10m): confirm §3.6 file updates assigned with owners + dates. / 确认 §3.6 文件更新已分人定时。
6. **Close / 收尾** (5m): name credit (§3.7), set carry-forward owner. / 点名表彰（§3.7），定后续负责人。

### 3.9 Decision: continue / retire / 继续或退役 {#decision-continue-retire}
- **Continue / 继续**: ROI met + adoption healthy → standardize & hand to ops. / ROI 达+采纳健康→标准化交运营。
- **Iterate / 迭代**: partial win → log learning (§3.6), plan v2 with changed variable. / 部分赢→记学习，改一变量做 v2。
- **Retire / 退役**: ROI missed + no path → sunset, free the budget, document why in §3.1. / ROI 未达且无路→下线，释放预算，§3.1 写因。
- **Record the decision / 记录决策**: `____` (continue / iterate / retire) + reason + next owner. / 记录：续/迭/退+原因+负责人。

### 3.10 Worked example (illustrative) / 实例（演示） {#worked-example}
> **Outcomes vs business-case / 结果对商业论证** (illustrative only, not benchmarks / 仅演示非基准):
| Promised / 承诺 | Actual / 实际 | Verdict / 结论 |
|---|---|---|
| Revenue +¥180k (expected) | +¥152k | missed (−16%) — root cause: trial→member 18% vs 25% assumed |
| Cost saved ¥40k | ¥38k | met |
| Compliance: HI-3 ok | ok | met |
| Member experience: +0.3 NPS | +0.1 NPS | partial |

> **Read / 解读**: revenue missed because conversion assumption was optimistic — that is the lesson to carry, not a failure to hide. Numbers illustrative. / 营收未达因转化假设过乐观——这是要带走的教训，非要藏的失败。数值演示。

### 3.11 Retrospective output checklist / 复盘产出清单 {#output-checklist}
- [ ] §3.1 outcomes table filled with REAL numbers + verdicts. / §3.1 填真实数+结论。
- [ ] §3.2 timeline & budget variance stated. / §3.2 时空偏差已写。
- [ ] §3.3 well/hurt/change specifics captured. / §3.3 好伤改具体。
- [ ] §3.4 vendor score recorded (if vendor). / §3.4 供应商分已记。
- [ ] §3.5 30/60/90 adoption numbers in. / §3.5 采纳数已入。
- [ ] §3.6 knowledge-capture owners + files assigned. / §3.6 知识沉淀分人定文件。
- [ ] §3.7 credit named; §3.9 decision recorded. / §3.7 点名；§3.9 决策已记。

### 3.12 Cross-market retrospective note / 跨市场复盘注记 {#cross-market}
> **Guidance / 指引**: If the project spanned ≥2 markets, report outcomes PER MARKET — a club chain often wins in one market and loses in another for compliance or adoption reasons (`references/10`/`references/11` vs `references/17`). One blended number hides the lesson. / 若项目跨 ≥2 市场，按市场分别报结果——连锁常在一市场赢、另一市场因合规或采纳输；合并数掩盖教训。

- Per-market adoption (§3.5) may differ sharply by channel maturity. / 各市场采纳因通道成熟度差异大。
- Per-market compliance incidents must surface even if global ROI looked fine. / 即便全球 ROI 好看，各市场合规事故也须浮出。

### 3.13 Owner & cadence / 责任人与节奏 {#owner-cadence}
- **Owner / 责任人**: the project sponsor (owner or chain PM), not the vendor. / 项目发起人（老板或集团 PM），非供应商。
- **Cadence / 节奏**: at go-live +30/60/90 days (§3.5), then at project close, then annual re-read for lessons still valid. / 上线+30/60/90 天（§3.5）、项目收尾、年度重读仍有效者。

### 3.14 Evidence attachments / 证据附件 {#evidence}
> **Guidance / 指引**: Attach, don't assert. A retrospective without evidence is an opinion. / 附证据，勿空言；无证据的复盘是看法。

- Actual spend export from finance / 财务实际花费导出. / 财务实际花费导出。
- Adoption screenshots at 30/60/90 days / 30/60/90 天采纳截图. / 采纳截图。
- Vendor SLA / incident log / 供应商 SLA 与事故日志. / 供应商 SLA 与事故日志。
- Integration inventory diff (before vs after) / 集成清单差异（前vs后）. / 集成清单差异。

---

## 4. Common mistakes / ④ 常见错误

Full remedies in `data/21-anti-pattern-library.md`:
完整对策见 `data/21`：
- **No baseline written / 没写基线**: cannot judge ROI → retrofitted "success". / 无法判 ROI→事后编造"成功"。
- **Rounding failure into win / 把失败抹成胜利**: hides the real lesson, repeats the mistake. / 掩盖真教训，重复犯错。
- **Blame-only "what hurt" / 只追责的"伤处"**: kills psychological safety, loses detail. / 伤安全感，丢细节。
- **Vendor score not fed back / 供应商分不反哺**: re-select the same bad vendor next time. / 下次复选同款烂供应商。
- **Knowledge not captured / 知识不沉淀**: the club re-learns the same lesson at 3× cost. / 同教训 3 倍成本重修。

---

## 5. Related files / ⑤ 相关文件
- `templates/07-roi-business-case.md` (planned) — the promised baseline to compare against. / 对比的承诺基线。
- `templates/21-vendor-evaluation-matrix.md` (planned) — consumes the §3.4 score. / 消费 §3.4 评分。
- `tools/06-roi-three-scenario.md` — original three-scenario ROI. / 原始三情景 ROI。
- `references/18-integration-and-data-plumbing.md` — integration inventory update. / 集成清单更新。
- `playbooks/08-emergency-runbooks.md` — runbook capture. / 运维手册沉淀。
- `data/15-procurement-and-cost-benchmark.md` — VAR/asset register. / 供应商/资产台账。
- `data/21-anti-pattern-library.md` — log new pitfalls. / 记新坑。
- `tools/01-fdmm-maturity-assessment.md` — FDMM level update. / FDMM 等级更新。

---

## 6. G13 tri-perspective note / ⑥ G13 三视角覆盖注记

**Architect / 架构师**: The retrospective closes the stage-gate loop (Diagnose→…→Retrospective) with an evidence-based verdict on ROI, integration inventory and FDMM movement — feeding the next investment decision honestly. / 复盘以证据化结论闭合阶段闸（诊断→…→复盘），沉淀 ROI、集成清单、FDMM 晋级，诚实喂给下次投资决策。
**Operator / 运营者**: 30/60/90 adoption metrics + runbook capture + named credit give the front line a usable handover and a reason to engage the next rollout. / 30/60/90 采纳+运维沉淀+点名表彰，给一线可用交接与下次参与的动因。
**Member / 会员**: Honest "member-experience" row + complaint/guardrail read keep the retrospective accountable to whether the project actually improved the member's club — not just the dashboard. / 诚实的"会员体验"行+投诉/护栏解读，让复盘对"项目是否真改善会员的场馆"负责，而非只对看板。
