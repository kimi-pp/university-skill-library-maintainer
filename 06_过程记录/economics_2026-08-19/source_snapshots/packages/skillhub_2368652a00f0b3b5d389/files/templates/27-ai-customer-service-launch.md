# Member-Facing AI Bot Launch / 面向会员 AI 客服机器人上线

> **Cluster / 集群**: E (Data & AI) + M (messaging) + K (LLM governance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Platform policy (WhatsApp/LINE/Kakao/WeChat) re-verify via `tools/04`; medical/refund routing rules per market via `tools/05`.
> **Cross-references / 交叉引用**: `references/04-ai-application-landscape.md#ai-01-customer-service-bot` · `references/13-data-and-llm-engine.md#k-41-rag-bot` · `references/17-omnichannel-messaging.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.

---

## ① Purpose & when to use / 用途与适用时机

**Use this launch charter to scope, build, guardrail, and monitor a member-facing AI assistant** (web/app/IM) that answers FAQs 24/7 — the highest-ROI, lowest-risk first AI for most clubs.
**用本上线章程界定、构建、护栏并监控「面向会员的 AI 助手」**（网页/App/IM）全天候答 FAQ——多数场馆 ROI 最高、风险最低的首选 AI。

> **FDMM gate / FDMM 门槛**: Requires **FDMM ≥ L2** with a clean FAQ knowledge base + IM channel integration (`references/04#ai-01-customer-service-bot`). L1 clubs can start with a scripted rule-bot, not an LLM.
> **FDMM 门槛**：需 **FDMM ≥ L2** 且干净 FAQ 知识库+IM 通道集成（`references/04#ai-01-customer-service-bot`）。L1 馆可用规则机器人起步，非大模型。

> **If below the gate / 若未达门槛**: use a menu/rule chatbot on your existing IM (no LLM). An LLM bot without a clean KB hallucinates policy. Get the knowledge base right first (§3.2).
> **若未达门槛**：用现有 IM 上的菜单/规则机器人（非 LLM）。无干净知识库的大模型会编政策。先把知识库做对（§3.2）。

---

## ② Prerequisites checklist / 前置条件清单

- [ ] **FAQ knowledge base** exists and is reviewed by a human. / FAQ 知识库存在且经人工审阅。
- [ ] **IM channel(s)** connected (WeChat/LINE/WhatsApp per market). / IM 通道已连（按市场用微信/LINE/WhatsApp）。
- [ ] **Source-doc inventory** with a freshness owner (§3.2). / 源文档清单+保鲜负责人（§3.2）。
- [ ] **Guardrails configured** (forbidden topics → human, §3.3). / 护栏已配（禁题→人工，§3.3）。
- [ ] **Kill-switch + fallback** tested (§3.4). / 熔断+兜底已测（§3.4）。
- [ ] **PII redaction** before any model call (§k-42 refs/13). / 调模型前 PII 脱敏（§k-42 refs/13）。
- [ ] **Multilingual plan** per market (§3.6). / 多语种计划按市场（§3.6）。

---

## ③ THE TEMPLATE / 模板

### 3.1 Scope & intent list (top-30 FAQ mining) / 范围与意图清单（Top-30 FAQ 挖掘） {#b1-intents}

> Mine your real questions first — do not invent intents. The bot should cover the top 30 only at launch.
> 先挖真实问题——别编造意图。上线只覆盖 Top-30。

| # | Member question (EN / 中文) | Volume / 量 | Source / 来源 | Bot-able? / 可机器人? |
|---|---|---|---|---|
| 1 | "Opening hours? / 营业时间？" | ___ | chat log / 聊天日志 | ✅ |
| 2 | "Freeze my membership? / 能冻结会籍？" | ___ | tickets / 工单 | ⚠️ → human (refund-adjacent) |
| 3 | "I have knee pain, what exercise? / 膝盖痛练什么？" | ___ | chat / 聊天 | ❌ → human (HI-6) |
| … | | | | |

> Micro-example / 微例: "where is my locker" and "how do I book" are bot-able; "cancel and refund" and "injury advice" route to humans.
> 「储物柜在哪」「怎么约课」可机器人；「退费」「伤病建议」转人工。

### 3.2 RAG knowledge-base build checklist / RAG 知识库构建清单 {#b2-rag-kb}

> Use RAG, not fine-tuning: cheaper, updatable, source-citable, less hallucination (`references/13#k-41-rag-bot`).
> 用 RAG 非微调：更便宜、可更新、可溯源、少幻觉（`references/13#k-41-rag-bot`）。

| Source doc / 源文档 | Owner / 负责人 | Freshness / 保鲜 | In KB? / 入库? |
|---|---|---|---|
| Membership T&Cs / 会籍条款 | legal / 法务 | reviewed ___ | ☐ |
| Class catalog / 课程目录 | ops | weekly / 周 | ☐ |
| Freeze/transfer policy / 冻结转让政策 | CS lead | quarterly / 季 | ☐ |
| Pricing sheet / 价目 | sales | on change / 变更时 | ☐ |

- Every answer cites its source snippet ("per our cancellation policy §X"). / 每答引用来源片段（"依退会政策§X"）。
- A **freshness owner** re-checks each doc on its cadence. / **保鲜负责人**按节奏复核每文档。

### 3.3 Guardrails spec / 护栏规格 {#b3-guardrails}

> System prompt locks the role; forbidden topics always escalate to a human.
> 系统提示锁定角色；禁题始终转人工。

| Forbidden topic / 禁题 | Route to / 转至 | Basis / 依据 |
|---|---|---|
| Medical / injury advice / 医疗/伤病建议 | human coach/pro | **HI-6** |
| Refunds / contract change / 退款/改合同 | human advisor | HI-3 |
| Another member's data / 他人数据 | refuse + log | HI-1/HI-8 |
| Legal dispute / 法律争议 | human + legal | — |

- Bot may **read** status, never auto-refund or alter contracts. / 机器人可*查*状态，绝不自动退款或改合同。
- Confidence below threshold → "let me connect you to the front desk." / 置信低于阈值→「为您转前台」。

### 3.4 Kill-switch & fallback design / 熔断与兜底设计 {#b4-kill-switch}

> **2-failed-answers handoff rule**: if the bot gives 2 unsatisfactory answers in a thread (or 1 clearly-wrong policy answer), auto-handoff to a human with full transcript.
> **2 次失败回答转人工规则**：机器人在同一会话给出 2 次不满意回答（或 1 次明显错政策回答），自动转人工并附完整记录。

- [ ] Global kill-switch tested (vendor SLA + your own toggle). / 全局熔断已测（供应商 SLA+自有开关）。
- [ ] Handoff preserves context (no "please repeat"). / 转人工保留上下文（勿「请重说」）。
- [ ] Off-hours fallback message clearly states human hours. / 非工作时段兜底明确写人工时段。

### 3.5 Quality monitoring rubric (weekly transcript sampling) / 质量监控表（每周抽样） {#b5-quality}

| Sample / 样本 | Correct? / 正确? | On-brand? / 贴牌? | Escalated right? / 转对? | Note / 备注 |
|---|---|---|---|---|
| chat #___ | ☐Y ☐N | ☐Y ☐N | ☐Y ☐N | |
| chat #___ | ☐Y ☐N | ☐Y ☐N | ☐Y ☐N | |

- Sample ≥ 20 transcripts/week; track wrong-answer rate (target <5%). / 每周抽样≥20 会话；错答率目标<5%。
- Log prompt-injection attempts (§k-43 refs/13). / 记录提示注入尝试。

### 3.6 Multilingual coverage plan per market / 按市场多语种计划 {#b6-multilingual}

| Market / 市场 | Languages / 语言 | Channel / 通道 | Coverage / 覆盖 |
|---|---|---|---|
| CN / 中国 | zh-CN | WeChat | full / 全 |
| JP / 日本 | ja + en | LINE | full / 全 |
| SG / 新加坡 | en + zh + ms | WhatsApp | full / 全 |
| AU / 澳洲 | en | web/app | full / 全 |

> Do NOT promise perfect translation; verify claims don't drift across languages (HI-6 medical phrasing). / 勿承诺完美翻译；校验跨语言语义不漂移（HI-6 医疗措辞）。

### 3.7 Pre-launch dry-run checklist / 上线前演练清单 {#b7-dry-run}

> Run this before any member sees the bot — a bad first impression is hard to undo.
> 会员见机器人前先跑——第一印象差难挽回。

- [ ] 20 scripted Q&A pass (incl. 3 medical/refund → human). / 20 个脚本问答通过（含 3 个医疗/退款→人工）。
- [ ] 1 prompt-injection attempt rejected + logged. / 1 次提示注入被拒+记录。
- [ ] Kill-switch toggled off→on successfully. / 熔断开关成功关→开。
- [ ] Handoff preserves transcript context. / 转人工保留记录上下文。
- [ ] PII redaction verified on a test query. / PII 脱敏经测试查询验证。

---

## ④ Common mistakes / 常见误区

- **LLM without clean KB** → hallucinated policy, member harm. / 无干净知识库的大模型→编政策、伤会员。
- **Medical advice given** → HI-6 breach, liability. / 给医疗建议→HI-6 违规、担责。
- **No kill-switch** → bad answer loops unchecked. / 无熔断→错答循环无人管。
- **Raw PII into model** → leak. / 原始 PII 进模型→泄露。
- **Over-claiming language** → mistranslated promises. / 过度承诺语种→误译承诺。

> Full remedy catalogue: `data/21-anti-pattern-library.md`.
> 完整对策：见 `data/21-anti-pattern-library.md`。

---

## ⑤ Related files / 相关文件

- `references/04-ai-application-landscape.md#ai-01-customer-service-bot` — use-case scope. / 用例范围。
- `references/13-data-and-llm-engine.md#k-41-rag-bot` — RAG design. / RAG 设计。
- `references/13-data-and-llm-engine.md#k-42-guardrails` — guardrail spec. / 护栏规格。
- `references/17-omnichannel-messaging.md` — channel setup. / 通道配置。
- `tools/06-roi-three-scenario.md` — bot ROI. / 机器人 ROI。

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: FDMM L2 gate + RAG (not fine-tune) + PII redaction + kill-switch + model registry; L1 gets rule-bot only.
- **Operator / 运营者**: intent mining, KB freshness owner, weekly quality sampling, 2-fail handoff, multilingual plan — measurable, controllable rollout.
- **Member / 会员**: 24/7 answers, medical/refund always to a human (HI-6/HI-3), data not leaked (HI-1/HI-8), language they understand, easy escape to a person.
本文件覆盖架构师（FDMM L2 门槛+RAG 非微调+PII 脱敏+熔断+注册表；L1 仅规则机器人）、运营者（意图挖掘、知识库保鲜负责人、每周质量抽样、2 败转人工、多语种计划——可度量可控上线）、会员（24/7 应答、医疗/退款始终转人工 HI-6/HI-3、数据不泄露 HI-1/HI-8、懂的语言、易转真人）。
