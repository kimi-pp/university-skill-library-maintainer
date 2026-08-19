# Vendor Evaluation Scorecard & Decision Record / 供应商评分卡与决策记录

> **Cluster / 集群**: I (IT governance & money) + B (software)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Vendor financials & service network 🔄 via `tools/04`; verify nearest service center by phone before scoring (`data/04`).
> **Cross-references / 交叉引用**: `data/04-hardware-vendor-directory.md`, `data/21#ap-002-no-data-export`, `data/21#ap-016-gray-import-critical`, `templates/20` (RFP), `templates/22` (migration).
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this scorecard to **objectively compare vendors** after the RFP and record the decision (with dissent). It turns "I liked their sales guy" into a weighted, auditable choice.
本评分卡用于 RFP 后**客观比选供应商**并记录决策（含异议）。把"我喜欢销售"变成加权、可审计的选择。

- **FDMM gate / 等级闸门**: L1+ for any core-system purchase. Keep weights simple for L1; add financial-stability depth at L3+.
  L1+ 凡核心系统采购。L1 权重从简；L3+ 加重财务稳健。
- **Trigger / 触发**: ≥3 vendor responses, or a single "only one option" claim to challenge.
  ≥3 家回标，或有人称"只有一家"需反驳。

---

## ② Prerequisites checklist / 前置清单

- [ ] RFP issued with comparable pricing (`templates/20` §3.6). / 已发 RFP 且报价可比。
- [ ] ≥3 vendors, ≥1 local + ≥1 low-cost (`SKILL.md` Iron Law 8). / ≥3 家，含本地+低成本。
- [ ] Service-network verified per club location (`data/04`). / 已按门店位置核验服务网络。
- [ ] Data-export clause present in every bid (`data/21#ap-002-no-data-export`). / 每标均含导出条款。
- [ ] Reference-check script ready (§3.3). / 参考核查话术就绪（§3.3）。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Weighted scorecard / 加权评分卡

Score each vendor 1–5 per criterion; weighted total = Σ(score × weight).
每项按 1–5 打分；加权总分 = Σ(分×权重)。

| Criterion / 标准 | Weight / 权重 | Vendor A | Vendor B | Vendor C |
|---|---|---|---|---|
| Functionality 功能 | 30% | `____` | `____` | `____` |
| Service-network 服务网络 | 20% | `____` | `____` | `____` |
| Financial stability 财务稳健 | 15% | `____` | `____` | `____` |
| Integration & API 集成 | 15% | `____` | `____` | `____` |
| Compliance 合规 | 10% | `____` | `____` | `____` |
| Price (lower=better, invert) 价格 | 10% | `____` | `____` | `____` |
| **Weighted total 加权总分** | **100%** | `____` | `____` | `____` |

> **Guidance / 指引**: Service-network often decides uptime more than spec (`data/04`). A ¥2k-cheaper machine with no local service costs more in downtime (`data/21#ap-016-gray-import-critical`).
> 服务网络常比参数更决定可用性。便宜 2k 无本地服务=停机更贵。

### 3.2 Service-network verification steps (nearest engineer test) / 服务网络核验（最近工程师测试）

Per `data/04`, verify BEFORE scoring — a phone call beats a brochure.
按 `data/04`，打分前核验——电话胜过彩页。

- [ ] Asked: "Nearest authorized service center to [my address]?" / 已问："离我地址最近的授权服务中心？"
- [ ] Confirmed spare-parts lead time (days). / 已确认备件交期（天）。
- [ ] Confirmed on-site vs carry-in warranty. / 已确认上门还是送修保修。
- [ ] Ran a test: called the local number, timed the response. / 实测：打电话计响应。
- [ ] Logged result in scorecard service-network cell. / 结果记入服务网络格。

### 3.3 Reference-check script / 参考核查话术

Ask each provided reference (verbatim / 照念):
向每家提供的参考客户提问（照念）：

1. "How long have you run this vendor in a club like mine?" / "您在多像我店的场馆用这家多久了？"
2. "What broke, and how fast did they fix it?" / "出过什么故障，修多快？"
3. "Did data export work when you tested it?" / "您测导出时好用吗？"
4. "Would you re-buy? Why/why not?" / "还会再买吗？为什么？"
5. "Any surprise fees after go-live?" / "上线后有隐藏费用吗？"

> **Stop-line / 停手线**: If a vendor refuses references or all refs are "a friend", flag gray-import risk (`data/21#ap-016-gray-import-critical`).
> 供应商拒给参考或全是"朋友"，标灰货风险。

### 3.4 Pilot clause language / 试点条款话术

Include in contract — never skip for L2+ AI or core systems.
写入合同——L2+ 的 AI 或核心系统绝不省。

> "Vendor provides a `____`-day pilot at `____` site with defined success metrics (`____`). Either party may exit without penalty if metrics unmet. Pilot data export tested before full rollout."
> "供应商在 `____` 店提供 `____` 天试点，成功指标明确（`____`）。未达标任一方无责退出。全面推广前先测数据导出。"

### 3.5 Decision record with dissent log / 决策记录与异议日志

| Field / 项 | Content / 内容 |
|---|---|
| Decision 决策 | select `____` (score `____`) |
| Rationale 理由 | `____` |
| Dissent 异议 | who `____`: `____` |
| Conditions 条件 | pilot pass + export verified |
| Sign-off 签字 | `____` date `____` |

> **Rule / 规则**: Record dissent even if overruled — it is the audit trail and protects the club later.
> 即便被否决也要记异议——这是审计线索，日后护店。

---

## ④ Common mistakes / 常见错误

1. No data-export clause in bid → lock-in. / 标中无导出条款→锁定。→ `data/21#ap-002-no-data-export`
2. Gray import with no local service. / 灰货无本地服务。→ `data/21#ap-016-gray-import-critical`
3. Judging by sales charm, not scorecard. / 凭销售魅力而非评分卡。
4. Skipping reference calls. / 跳过参考电话。→ §3.3
5. No pilot for AI/core system. / 核心/AI 无试点。→ §3.4

---

## ⑤ Related files / 相关文件

- `templates/20-rfp-technical-spec.md` — RFP skeleton / 招标骨架
- `data/04-hardware-vendor-directory.md` — service-network golden rule / 服务网络黄金律
- `data/21-anti-pattern-library.md#ap-016-gray-import-critical` — gray import / 灰货
- `templates/22-data-migration-plan.md` — exit readiness / 退出就绪
- `tools/04-dynamic-intelligence-retrieval.md` — vendor 🔄 verify / 供应商核验

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (weighted scoring + integration depth), **Operator** (service-network test + reference script + pilot safety), and **Member** (data portability via export clause, reliable uptime via local service, no surprise fees); the dissent log is the club's protection against groupthink.
本模板覆盖**架构师**（加权评分+集成深度）、**运营者**（服务网络实测+参考话术+试点保护）、**会员**（导出条款保可携、本地服务保可用、无隐藏费）；异议日志防集体盲思，护店。
