# Multi-Market APAC Rollout Plan / APAC 多市场推广计划

> **Cluster / 集群**: G (governance) + H (rollout) + B (software)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Per-market compliance four-pack 🔄 via `tools/05` (`references/10`, `references/11`); payment & messaging stacks 🔄 via `tools/04` (`data/07`).
> **Cross-references / 交叉引用**: `references/10-apac-compliance-east-asia-oceania.md`, `references/11-apac-compliance-south-southeast-asia.md`, `tools/05-regulation-traceability-verification.md`, `data/07-apac-regional-differences.md`, `references/17-omnichannel-messaging.md`, `templates/42` (franchise), `templates/46` (NOC).
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this plan to **coordinate launching the same digital club stack across multiple APAC markets** without re-learning compliance and localization from scratch each time.
本计划用于**跨 APAC 多市场协同上线同一数字化栈**，免得每市场重学合规与本地化。

- **FDMM gate / 等级闸门**: L3+ only — multi-market needs HQ program office.
  L3+ 专属——多市场需 HQ 项目办。
- **Trigger / 触发**: ≥2 markets in the 12-month plan.
  12 个月内 ≥2 市场。

---

## ② Prerequisites checklist / 前置清单

- [ ] Per-market compliance four-pack verified (`tools/05`, `references/10/11`). / 各市场合规四件套核验。
- [ ] Payment stack per market mapped (`data/07`). / 各市场支付栈已绘。
- [ ] Messaging channel per market mapped (`references/17`). / 各市场消息渠道已绘。
- [ ] Localization workbook started. / 本地化手册已启。
- [ ] Pilot-market selected (§3.4). / 试点市场已选（§3.4）。
- [ ] HQ rollout owner & RACI named. / HQ 推广负责人与 RACI 已定。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Market-entry readiness gate (per market) / 市场准入就绪闸门（每市场）

| Gate / 闸 | Market A | Market B |
|---|---|---|
| Compliance four-pack pass 合规四件套过 | [ ] | [ ] |
| Payment stack ready 支付栈就绪 | [ ] | [ ] |
| Messaging channel ready 消息渠道就绪 | [ ] | [ ] |
| Localization done 本地化完成 | [ ] | [ ] |
| Pilot greenlit 试点放行 | [ ] | [ ] |

> **Guidance / 指引**: Run `tools/05` per market; a single missing consent rule blocks the whole launch. Gate is binary — no "mostly ready".
> 指引：逐市场跑 tools/05；漏一条同意规则全盘卡住。闸门是二元的——没有"差不多"。

### 3.2 Localization workbook / 本地化手册

| Dimension / 维度 | Market A | Market B |
|---|---|---|
| Language(s) 语言 | `____` | `____` |
| Currency 货币 | `____` | `____` |
| Tax/VAT handling 税 | `____` | `____` |
| Name order 姓名序 | `____` | `____` |
| Date/number format 日期数字格式 | `____` | `____` |
| Holidays/blackout 假期 | `____` | `____` |
| Address format 地址格式 | `____` | `____` |

> **Red flag / 红线**: Reusing "English name field" in a name-order-different market breaks member records.
> 红线：在姓名序不同市场复用"英文名"字段→会员档案错乱。

### 3.3 Vendor strategy: global vs local / 供应商策略：全球 vs 本地

- Global stack for core (membership/BI) consistency. / 核心（会员/BI）用全球栈保一致。
- Local vendors for payment, ISP, last-mile support. / 支付、ISP、末端支撑用本地商。
- Keep a global integration layer to absorb local differences. / 留全球集成层吸收本地差异。
- :::dynamic-hook topic="apac-local-payment-vendors" staleness="120d" action="tools/04" fallback="treat as unverified"
  As of 2026-07 payment leaders vary by market (e.g. `____` in `____`); confirm current top via `tools/04`.
  截至 2026-07 各市场支付龙头不同（如 `____` 在 `____`）；当前头部经 tools/04 核。
  :::

### 3.4 Pilot-market selection logic / 试点市场选择逻辑

Pick the market that is: compliant-fast + representative + low-cost-to-fail.
选：合规快+有代表性+试错成本低。

- [ ] Representative of region tech maturity. / 代表该区技术成熟度。
- [ ] Shorter compliance lead. / 合规周期更短。
- [ ] One market only first. / 先只一个市场。
- [ ] Has local payment & messaging already mapped. / 本地支付与消息已绘。

> **Micro-example / 微例**: Chose `____` as pilot (fast privacy clearance, similar to 3 later markets); caught a tax-invoice bug before it hit `____`.
> 微例：选 `____` 作试点（隐私清关快、类后续 3 市场）；在波及 `____` 前抓出税票 bug。

### 3.5 Rollout wave plan / 推广波次计划

| Wave / 波 | Markets / 市场 | Date / 日期 | Owner / 责 |
|---|---|---|---|
| Wave 1 (pilot) 试点 | `____` | `____` | `____` |
| Wave 2 二波 | `____` | `____` | `____` |
| Wave 3 三波 | `____` | `____` | `____` |
| Wave 4 四波 | `____` | `____` | `____` |

> **Rule / 规则**: Each wave starts only after prior wave's go-live checklist is green ≥`____` days.
> 规则：每波须前波上线清单绿 ≥`____` 天才启。

### 3.6 Per-market go-live checklist / 每市场上线清单

- [ ] Compliance sign-off archived. / 合规签字归档。
- [ ] Local payment tested live (small txn). / 本地支付实跑小额测过。
- [ ] Messaging channel verified delivery. / 消息渠道送达已验。
- [ ] Localization QA passed. / 本地化 QA 过。
- [ ] NOC dashboard onboarded (`templates/46`). / NOC 看板已接（templates/46）。
- [ ] Local support number live. / 本地支撑号已通。

### 3.7 HQ rollout-tracking dashboard / HQ 推广跟踪看板

| Metric / 指标 | Target / 目标 |
|---|---|
| Markets live 上线市场 | `____` / `____` |
| Avg time-to-go-live 平均上线时长 | < `____` wks |
| Compliance defects 合规缺陷 | 0 |
| Localization gaps 本地化缺口 | `____` |
| Open vendor issues 未决厂商问题 | `____` |

---

### 3.8 Rollout risk register / 推广风险登记

| Risk / 风险 | Market 市场 | Mitigation 缓解 |
|---|---|---|
| Compliance slip 合规漏 | `____` | §3.1 gate |
| Payment fail 支付失败 | `____` | §3.6 live test |
| Localization bug 本地化bug | `____` | §3.2 QA |
| Vendor delay 厂商延误 | `____` | §3.3 local fallback |

> **Guidance / 指引**: Register reviewed at each wave gate; open high-impact risks block go-live.
> 指引：每波闸复看；高影响未决风险拦上线。

### 3.9 Post-rollout lessons capture / 推广后经验回收

- What localized wrong & why. / 哪本地化错、为何。
- Actual vs planned time-to-go-live. / 实际 vs 计划上线时长。
- Feed templates/next-market. / 回灌下市场模板。

### 3.10 Local vendor scorecard snippet / 本地商评分片段

For each market's local vendors (payment/ISP/support), score quickly:
逐市场本地商（支付/ISP/支撑）快评：

| Vendor / 商 | Market 市场 | Score 分 | Note 注 |
|---|---|---|---|
| `____` | `____` | `____` | `____` |
| `____` | `____` | `____` | `____` |

> **Guidance / 指引**: Reuse `templates/21` weighted scorecard for the full evaluation; this is the per-market extract.
> 指引：完整评用 templates/21 加权卡；此乃逐市场摘录。

### 3.11 Program office RACI / 项目办 RACI

| Role / 角色 | Responsibility / 责 |
|---|---|
| Rollout lead 推广负责 | wave plan, gate decisions |
| Market lead 市场负责 | local compliance, go-live |
| Integration lead 集成负责 | stack deploy, data |
| Comms lead 沟通负责 | member & staff messaging |

> **Rule / 规则**: One accountable owner per market; no shared-blame gates.
> 规则：每市场一责任主；闸门不共责。

## ④ Common mistakes / 常见错误

1. One compliance miss blocks launch. / 一处合规漏全盘卡。→ §3.1 (`tools/05`)
2. Reusing name fields cross-market. / 跨市场复用姓名字段。→ §3.2
3. Global-only vendors, no local payment. / 只用全球商无本地支付。→ §3.3
4. No pilot, big-bang all markets. / 无试点全市场齐发。→ §3.4
5. NOC not onboarded at go-live. / 上线未接 NOC。→ §3.6
6. Wave started before prior green. / 前波未绿就启下波。→ §3.5

---

## ⑤ Related files / 相关文件

- `references/10-apac-compliance-east-asia-oceania.md` — EA/Oceania rules / 东亚大洋洲规则
- `references/11-apac-compliance-south-southeast-asia.md` — S/SE Asia rules / 南亚东南亚规则
- `tools/05-regulation-traceability-verification.md` — four-pack gate / 四件套闸门
- `data/07-apac-regional-differences.md` — payment/messaging maps / 支付消息地图
- `references/17-omnichannel-messaging.md` — channel per market / 各市场渠道

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (vendor strategy + wave plan + tracking dashboard), **Operator** (readiness gate + go-live checklist + pilot logic that de-risks), and **Member** (consistent, localized, compliant experience in every market with working local payment & language); the per-market compliance gate is the non-negotiable protector.
本模板覆盖**架构师**（供应商策略+波次+跟踪看板）、**运营者**（就绪闸门+上线清单+试点降险）、**会员**（每市场一致、本地化、合规、本地支付与语言可用）；逐市场合规闸门是不可谈判的保护。
