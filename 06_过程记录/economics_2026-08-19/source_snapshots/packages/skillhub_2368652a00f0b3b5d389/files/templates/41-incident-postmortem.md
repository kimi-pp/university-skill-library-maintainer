# Incident Postmortem (Blameless) / 事件复盘（无指责）

> **Cluster / 集群**: J (Resilience) + V (Skill meta-capabilities)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify breach-notification windows every 90 days via `tools/05`; align with `references/16-security-operations-and-emergency.md`.
> **Cross-references / 交叉引用**: `data/10-hardware-fault-tree-library.md` · `data/11-network-fault-tree-library.md` · `data/12-software-fault-tree-library.md` · `data/20-micro-details-ledger.md` · `data/13-inspection-and-maintenance-calendar.md` · `references/16-security-operations-and-emergency.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: After any significant incident (outage, breach, double-charge, safety near-miss), write this — **blameless**. Its real job is not to find who to punish, but to feed the library: did our checklists and fault-trees cover this? If not, the gap goes into `data/10~12` + `data/20` so YOUR club's next incident is someone else's prevented one.
**中文**：任何重大事件（宕机、泄露、重复扣费、安全险情）后写这份——**无指责**。它真正的目的不是找人罚，而是喂给库：我们的清单和故障树覆盖到这事了吗？没覆盖，缺口就进 `data/10~12` + `data/20`，让你场馆的下次事件成为别人被拦下的一次。

> 💡 Blameless = people acted on the info they had. Find the system gap, not the scapegoat. A postmortem that blames is a postmortem nobody files (→ `references/16#j-offboarding-checklist` spirit: process over person).
> 💡 无指责=人按当时所知行动。找系统缺口，不找替罪羊。甩锅的复盘没人愿意写（→ `references/16#j-offboarding-checklist` 精神：流程重于人）。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | Incident already contained / 事件已控 | before writing / 写前 |
| 2 | Logs & tickets / 日志工单 | from `data/14`, `data/16` |
| 3 | Timeline facts / 时间线事实 | not assumptions / 非臆测 |
| 4 | Owner + date set / 定人定日 | for actions / 行动 |

---

## ③ THE TEMPLATE / 模板正文

### #timeline Timeline Reconstruction / 时间线重建

| Time / 时间 | Event / 事件 | Detected by / 发现方 | Action / 处置 |
|---|---|---|---|
| __:__ | fault began / 故障起 | __ | __ |
| __:__ | detected / 发现 | __ | __ |
| __:__ | ticket raised / 开单 | __ | __ |
| __:__ | resolved / 解决 | __ | __ |

### #impact Impact Quantification / 影响量化

| Metric / 指标 | Value / 数值 | Note / 备注 |
|---|---|---|
| Members affected / 影响会员 | __ | count / 数 |
| Revenue lost / 损失营收 | ¥__ | range / 区间 |
| Hours down / 停机时 | __ h | — |
| Safety impact? / 安全影响? | Yes/No | HI-2 if yes / 是则 HI-2 |

### #five-whys 5-Whys Worksheet / 五问法

| # | Why / 为何 | Answer / 答 |
|---|---|---|
| 1 | Why did it fail? / 为何坏 | ________ |
| 2 | Why that? / 为何如此 | ________ |
| 3 | Why that? / 为何如此 | ________ |
| 4 | Why that? / 为何如此 | ________ |
| 5 | Root cause / 根因 | ________ |

### #factors-vs-root Contributing Factors vs Root Cause / 促成因素 vs 根因

| Type / 类 | Description / 描述 |
|---|---|
| Contributing / 促成 | ________ (made it worse) |
| Root cause / 根因 | ________ (the fixable source) |

> Separate them: you can't fix "contributing" without killing the root. A symptom fix = next month's repeat (→ `data/21#ap-021` spirit).
> 分开：不除根因，治「促成」没用。治标=下月再犯（→ `data/21#ap-021` 精神）。

### #action-items Action Items / 行动项

| # | Action / 行动 | Owner / 负责 | Due / 期限 | Status / 状态 |
|---|---|---|---|---|
| 1 | ________ | ____ | ____ | □ |
| 2 | ________ | ____ | ____ | □ |

### #library-feedback Library Feedback Loop / 入库反馈（关键）

> Did our checklists / fault-trees cover this? / 我们的清单/故障树覆盖到吗？

- [ ] Covered — anchor exists: `data/__#__` / 已覆盖—锚点：____
- [ ] **Gap** — new fault-tree entry needed in `data/10` / `data/11` / `data/12`: ____ / **缺口**—需在库新增：____
- [ ] **Micro-detail** to add to `data/20-micro-details-ledger.md`: ____ / 需加微细节至 `data/20`：____
- [ ] Checklist update needed in `data/13`: ____ / 需更 `data/13` 清单：____

> This is how the library learns from YOUR club. File the gap within 1 week of the incident.
> 库就是这样从你场馆学到的。事件后 1 周内把缺口入库。

---

## ④ Common Mistakes / 常见错误

- **Blame the person** → no real fix, repeat incident. → `references/16` process-over-person.
- **Symptom fix only** → root cause lives. → `data/21#ap-021` (theater).
- **No library feedback** → next club repeats it. → `data/20` ledger purpose.
- **Skip impact numbers** → can't prioritize. → quantify always (G8 ranges).

---

## ⑤ Related Files / 相关文件

- `data/10` / `data/11` / `data/12` — add new fault-tree entries here. / 在此加故障树。
- `data/20-micro-details-ledger.md` — capture the micro-detail. / 记微细节。
- `data/13-inspection-and-maintenance-calendar.md` — update checklists. / 更新清单。
- `references/16-security-operations-and-emergency.md` — breach 72h if applicable. / 若涉泄露。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: The postmortem closes the FDMM learning loop — every incident becomes a `data/10~12` fault anchor or a `data/20` micro-detail, so the library compounds instead of repeating (Cluster V).
**运营者 / Operator**: A blameless, fill-in form means a shift lead can run a useful review the next morning — no incident-manager certification needed; it protects the SLA-credit and insurance record too.
**会员 / Member**: Incidents that get root-caused (not patched) mean fewer recurrences, safer environments, and better-protected data — member trust rebuilt by demonstrated learning, not apologies (HI-2, HI-8).
