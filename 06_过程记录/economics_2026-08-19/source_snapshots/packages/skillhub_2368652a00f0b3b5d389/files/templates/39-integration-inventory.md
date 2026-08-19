# Integration Inventory / 集成清单

> **Cluster / 集群**: N (Integration layer)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify iPaaS/vendor API status every 180 days via `tools/04`; align exactly with `references/18-integration-and-data-plumbing.md`.
> **Cross-references / 交叉引用**: `references/18-integration-and-data-plumbing.md` · `data/12-software-fault-tree-library.md` · `data/21-anti-pattern-library.md` · `data/14-repair-scripts-and-sla-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: The master map of every connection between your systems — what talks to what, how, who owns it, and when the token expires. Before you switch ANY system, you check this table. It prevents the "silent killer": an expired API key that quietly stops syncing at 2am on a holiday.
**中文**：各系统间每一次连接的总图——谁连谁、怎么连、谁负责、令牌何时过期。切换**任何**系统前先查此表。它防「静默杀手」：过期 API 密钥在假期凌晨 2 点悄悄停同步。

> 💡 Golden rule: Native connector > iPaaS > CSV/manual > custom API. Default to the first two. A connection you can't see is a connection that will break unseen (→ `data/21#ap-029` custom-API-first, `references/18#n1`).
> 💡 黄金铁律：原生 > iPaaS > 导表 > 定制 API。默认走前两档。看不见的连接会在看不见时断（→ `data/21#ap-029`, `references/18#n1`）。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | List of systems / 系统清单 | MMS, POS, gate, app, ads, SCRM… / 会籍收银闸机App广告私域 |
| 2 | Access to integration console / 集成后台 | native or iPaaS / 原生或 iPaaS |
| 3 | `references/18` open / 打开 | for pattern ladder / 方式阶梯 |
| 4 | FDMM level / FDMM 等级 | L2+ has real integrations / L2+ 有真集成 |

---

## ③ THE TEMPLATE / 模板正文

### #connection-register Connection Register / 连接登记

| System A / 系统A | System B / 系统B | Method / 方式 | Data flowing / 数据 | Owner / 负责 | Token expiry / 令牌到期 🔄 | Health / 健康 |
|---|---|---|---|---|---|---|
| MMS | Payments | native | billing / 扣费 | IT | n/a | green |
| MMS | Access | native | valid flag / 有效标 | IT | n/a | green |
| CRM | Messaging | iPaaS | opt-in list / 同意名单 | Mkt | 2026-12-01 | amber |
| Ads | CRM (CAPI) | API | conversion / 转化 | Mkt | 2026-10-15 | green |

> 🔄 **Reminder rule**: Calendar alert 30 days before every `Token expiry`. A dead token = silent sync death (→ `data/12#s24`, `data/13` quarterly token sweep). "Silent killer" — link `data/12` integration anchors.
> 🔄 **提醒规则**：每个`令牌到期`前 30 天日历提醒。死令牌=静默停同步（→ `data/12#s24`, `data/13` 季令牌巡检）。「静默杀手」——联 `data/12` 集成锚点。

### #health-check Health-Check Schedule / 健康检查节奏

| Cadence / 频次 | Check / 查 | Tool / 工具 |
|---|---|---|
| Daily / 每日 | sync lag <5 min / 同步<5分 | MMS vs POS / 两系统 |
| Weekly / 周 | restore sample / 恢复抽样 | backup / 备份 |
| Quarterly / 季 | token sweep / 令牌巡检 | register above / 上表 |

> amber >30 days untested → retest before relying (→ `references/18#n9`).
> 超30天未测标黄→依赖前重测（→ `references/18#n9`）。

### #change-impact Change-Impact Checklist (BEFORE you switch any system) / 切换前影响核查

Before changing System X, tick each:
切换系统 X 前逐项勾：

- [ ] Listed all connections touching X in this register. / 本表中涉 X 的连接已列全。
- [ ] Notified each owner (IT/Mkt/Finance). / 已通知各负责人。
- [ ] Identified fallback (CSV/manual) if it breaks. / 已定崩了的人工兜底。
- [ ] Scheduled cutover in low-traffic window. / 切换排低谷窗口。
- [ ] Kept old export running 7 days post-cutover. / 旧导出切换后留7天。
- [ ] Dry-run passed with test member (5 scenarios). / 测试会员五场景试跑过。

> Skipping this = the "blame triangle" and double-charges (→ `data/21#ap-013-migrate-peak`, `references/18#n5b`).
> 跳过=甩锅三角与重复扣费（→ `data/21#ap-013`, `references/18#n5b`）。

---

## ④ Common Mistakes / 常见错误

- **Custom API before native** → fragile, breaks silently. → `data/21#ap-029` (also `references/18#ap-029`).
- **Expired token unnoticed** → sync dies at 2am holiday. → `data/12#s24`, `data/13` token sweep.
- **No idempotency** → double charges. → `references/18#n3`, `data/21#ap-033`.
- **Over-integration** → breaks >weekly, costs > value. → `data/21#ap-030-over-integration`, `references/18#n7`.

---

## ⑤ Related Files / 相关文件

- `references/18-integration-and-data-plumbing.md` — pattern ladder, 8 integrations, API contract. / 方式阶梯、8打通、API合同。
- `data/12-software-fault-tree-library.md` — `#s24` token, `#s07` sync, `#s03` booking anchors. / 令牌/同步/约课锚点。
- `templates/33-account-permission-matrix.md` — who owns each connection. / 每连接谁负责。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: The register is the integration layer of FDMM; token-expiry reminders and the change-impact checklist enforce the "monitor, don't surprise" discipline and prevent silent data divergence (HI-8 data minimization in transit).
**运营者 / Operator**: One sheet the IT contact updates quarterly — no integration engineer needed; it is the operator's shield against "why did bookings stop syncing?"
**会员 / Member**: Healthy integrations mean one profile, no duplicate charges, consistent journey — member trust protected by visible plumbing, not mystery outages.
