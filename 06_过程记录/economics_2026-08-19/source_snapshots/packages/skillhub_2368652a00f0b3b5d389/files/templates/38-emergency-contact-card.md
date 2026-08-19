# Emergency Contact Card (Wall-Mounted) / 应急联系卡（贴墙）

> **Cluster / 集群**: J (Resilience) + T (Physical security)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify all hotlines every 90 days; vendor 24/7 numbers shift — verify via `tools/04`. Align with `references/16-security-operations-and-emergency.md`.
> **Cross-references / 交叉引用**: `references/16-security-operations-and-emergency.md` · `data/10` / `data/11` / `data/12` fault trees · `templates/31-ticket-and-repair-form.md` · `data/14-repair-scripts-and-sla-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: ONE laminated A4 sheet pinned at the front desk and in the comms cabinet. When something dies mid-shift, nobody should be searching email for a number. It gives the who-to-call ladder, the first-3-steps per system, and shutoff locations — readable in a panic.
**中文**：一张塑封 A4，贴前台与弱电柜。当班中某系统瘫了，没人该去邮件里翻电话。它给「呼叫阶梯」、各系统「前3步」、以及断点位置——慌乱中也能读。

> 💡 **Keep this printed. It is useless inside a dead computer.** A phone with no charge, a contact list only in the CRM, a shutoff location nobody wrote down — that's how a 10-minute outage becomes a 3-hour one.
> 💡 **把它打印出来。死电脑里它一文不值。** 手机没电、通讯录只在 CRM、断点位置没人写——这就是 10 分钟故障变 3 小时的原因。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | All vendor hotlines / 全部厂商热线 | 24/7 labelled / 标「应急」 |
| 2 | Duty-manager + HQ numbers / 值班+总部号 | on speed-dial / 速拨 |
| 3 | Shutoff locations known / 断点已知 | power + water / 电+水 |
| 4 | Printed ×2 / 打印两份 | desk + cabinet / 前台+柜 |

---

## ③ THE TEMPLATE / 模板正文

### #call-ladder Who-To-Call Ladder / 呼叫阶梯

1. **Duty manager / 值班店长** — first responder on site. / 现场第一响应。
2. **Vendor hotlines / 厂商热线** (table below). / 下表。
3. **ISP / 运营商** — if internet is the fault. / 若网络问题。
4. **Electrician / 电工** — power, UPS, breaker (HI-2). / 电、UPS、空开。
5. **HQ / 总部** — escalate + comms. / 升级+对外。

| Vendor / 厂商 | 24/7 hotline / 应急热线 🔄 | Account ID / 账号 | For / 管 |
|---|---|---|---|
| Gate / 闸机 | ________ | ____ | `data/10#C2` |
| MMS / 会籍 | ________ | ____ | `data/12#s01` |
| POS / 收银 | ________ | ____ | `data/12#s12` |
| ISP / 运营商 | ________ | ____ | `data/11#n01` |
| CCTV / 监控 | ________ | ____ | `data/11#n23` |
| Electrician / 电工 | ________ | ____ | HI-2 |

### #first-3-steps Per-System First-3-Steps / 各系统前3步

| System / 系统 | First 3 steps / 前3步 | Anchor / 锚点 |
|---|---|---|
| **Gate stuck / 闸机卡** | 1) staff QR test 员工码测 2) reboot controller 重启控器 3) manual release + log 人工放行+记 | `data/10#C2-E01` |
| **POS dead / 收银死** | 1) check power/UPS 查电 2) test ¥1 sale 测小额 3) fallback manual receipt 手工票 | `data/12#s12`, `data/11#n02` |
| **Internet down / 断网** | 1) modem light 看灯 2) power-cycle 重启 3) 4G/5G failover 切备份 | `data/11#n01`, `#n11` |
| **MMS down / 会籍瘫** | 1) other staff login 换人登 2) last-sync check 查末同步 3) vendor ticket 开工单 | `data/12#s01`, `#s07` |

### #shutoff-locations Power & Water Shutoff / 断电断水位置

| Item / 项 | Location / 位置 | Labeled? / 已标 | Photo? / 照片 |
|---|---|---|---|
| Main breaker / 总空开 | ________ | □ | □ |
| UPS feed / UPS供电 | ________ | □ | □ |
| Water main / 总水阀 | ________ | □ | □ |
| Pool pump isolator / 水泵隔离 | ________ | □ | □ |

### #incident-stub Incident Log Stub / 事件日志存根

| Time / 时间 | What / 何事 | First action / 首措 | Vendor ticket / 工单 | Resolved / 解决 |
|---|---|---|---|---|
| ____ | ________ | ________ | ____ | ____ |

> A check you didn't log didn't happen (→ `data/13` logging rule). Life-safety event = close-and-escalate, never queue (HI-2).
> 没记的检=没做（→ `data/13`）。人身安全事件=闭店升级，绝不排队（HI-2）。

---

## ④ Common Mistakes / 常见错误

- **Contacts only in CRM** → unreachable when CRM is down. → `data/21#ap-049` spirit (single point).
- **No printed card** → panic search wastes SLA clock. → `templates/31`.
- **Forget power shutoff** → unsafe fix. → HI-2.
- **Life-safety queued** → tragedy. → `data/21#ap-012`, `#ap-054`.

---

## ⑤ Related Files / 相关文件

- `references/16-security-operations-and-emergency.md` — breach & physical security. / 泄露与物理安全。
- `templates/31-ticket-and-repair-form.md` — open the ticket after first-3-steps. / 前3步后开单。
- `data/13-inspection-and-maintenance-calendar.md` — escalation path. / 升级路径。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: The card is the operational face of Cluster J/T — it binds the fault-tree anchors to a human call ladder and enforces HI-2 life-safety escalation as a printed, unavoidable step.
**运营者 / Operator**: A wall sheet any rookie can read under stress — no system login needed; it protects the SLA clock and the club's insurance evidence.
**会员 / Member**: Fast, correct first response means shorter downtime at the gate/POS and, above all, member bodies protected by immediate life-safety escalation (HI-2).
