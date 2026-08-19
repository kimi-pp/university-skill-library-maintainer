# Inspection & Maintenance Calendar / 巡检与维护日历

> **Cluster / 集群**: G (Lifecycle) + D (Network) + C (Hardware)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify every 90 days; vendor patch cadence and UPS/PAT test rules pass `tools/04`/`tools/05` before citing. Aligns with `references/15` G2 open/close.
> **Cross-references / 交叉引用**: `references/15-lifecycle-scenarios.md` · `data/11-network-fault-tree-library.md` · `data/12-software-fault-tree-library.md` · `data/10-hardware-fault-tree-library.md` · `references/16-security-operations-and-emergency.md` · `references/05-methodology-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

The preventive backbone. Every checklist item shows **How to check (plain words) / 怎么查（说人话）**, **What failure looks like / 失败长啥样**, and a **Fault-tree anchor / 故障树锚点** for when it breaks. Print the daily sheets and pin them.
预防主干。每条巡检项给出**怎么查（说人话）**、**失败长啥样**、以及出问题时对应的**故障树锚点**。打印日检表贴墙。

---

## How to Run This Calendar / 怎么用这本日历

**Owner / 负责人**: Daily checks = front desk or duty manager (FDMM L1). Monthly+ = the club's IT contact or MSP. Annual = owner + MSP.
**负责人**：日检 = 前台或值班店长（FDMM L1）。月检以上 = 本店 IT 对接人或 MSP。年检 = 老板 + MSP。

**Print & pin / 打印贴墙**: Print the Daily Opening (10) and Closing (8) tables, laminate, and pin at the desk and the comms cabinet. The weekly/monthly tables go in the club's operations binder.
**打印贴墙**：日开店（10）与闭店（8）表打印塑封，贴前台与弱电柜。周/月表入运营活页夹。

**Log everything / 事事留痕**: Every check gets a tick + initials + time. Failures get a one-line note + the fault-tree anchor + the ticket number once raised. This log is your evidence for SLA credits and insurance (see `data/14`, `data/16`).
**事事留痕**：每项打勾 + 签名缩写 + 时间。失败写一行备注 + 故障树锚点 + 工单号。此日志是 SLA 抵扣与保险的证据（见 `data/14`、`data/16`）。

**FDMM fit / 层级适配**: A paper-club (L1) runs daily + weekly only. An integrated club (L2+) adds monthly + quarterly. A chain (L4+) runs the full annual map across all sites. Never prescribe L4 discipline to an L1 club (Iron Law 7).
**层级适配**：纸表店（L1）只跑日+周。集成店（L2+）加月+季。连锁（L4+）全店跑年检地图。别给 L1 店上 L4 纪律（铁律7）。

---

## Daily — Opening (10 items) / 每日开店（10 项）

| # | Item / 项目 | How to check / 怎么查 | Failure look / 失败长啥样 | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Gate opens with valid QR/face / 闸机有效二维码/人脸可开 | Tap a test member or staff at open / 开店用测试会员或员工刷一下 | Gate stuck, "expired" on valid / 闸机卡、有效也报过期 | `data/12` #s08, `data/10` #C2 |
| 2 | Receipt printer test page / 小票机测试页 | Print one test slip from POS / POS 打一张测试小票 | No paper jam or blank / 卡纸或空白 | `data/12` #s20, `data/11` #n15 |
| 3 | Internet up (wired test) / 有线网络通 | Open a site on a wired laptop / 插线笔记本开个网页 | Red modem light or no page / 光猫红灯或打不开 | `data/11` #n01 |
| 4 | MMS login works for ≥1 staff / 会籍至少1员工能登 | Log in at open / 开店登一次 | Login fail / 登不上 | `data/12` #s01 |
| 5 | Member Wi-Fi broadcast visible / 会员 Wi-Fi 名可见 | Scan with a phone / 手机扫一下 | SSID missing / 少了一个名 | `data/11` #n04 |
| 6 | Cameras recording (spot 1–2) / 摄像头在录（抽1–2） | Check live view on NVR / 看 NVR 实时画面 | Black screen / 黑屏 | `data/11` #n23, #n13 |
| 7 | POS can take a ¥1 test sale / POS 能刷 ¥1 测试 | Do a tiny test sale, then refund / 刷小额测试再退 | Payment fail / 支付失败 | `data/11` #n02, `data/12` #s12 |
| 8 | Booking app shows today's classes / 约课 App 显示今日课 | Open app, confirm schedule / 开 App 确认课表 | Schedule missing / 课表没了 | `data/12` #s04, #s03 |
| 9 | Backup ran last night / 昨夜备份已跑 | Confirm backup timestamp / 确认备份时间 | No backup / 无备份 | `data/12` #s22 |
| 10 | UPS shows green / UPS 绿灯 | Look at UPS display / 看 UPS 显示 | Red/beeping / 红或叫 | `data/11` (weekly test) |

**Execution note / 执行要点**: Run items 1–10 in order before doors open. If any FAILS, do not open silently — raise the ticket, post a manual-check-in note, and tell the duty manager. A failed gate (#1) or internet (#3) before peak is a go/no-go call (HI-2 egress safety).
**执行要点**：开店前按顺序跑 1–10。任一失败不要悄悄开门——开工单、贴人工入场告示、报值班店长。闸机（#1）或网络（#3）在高峰前失败是「开/不开」的决策点（HI-2 疏散安全）。

---

## Daily — Closing (8 items) / 每日闭店（8 项）

| # | Item / 项目 | How to check / 怎么查 | Failure look / 失败长啥样 | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Daily sales reconciled / 当日营收已对账 | Run MMS vs POS vs gateway report / 跑会籍vsPOSvs网关对账 | Mismatch >0.5% / 差>0.5% | `data/12` #s12, #s10 |
| 2 | Sync lag cleared (no backlog) / 同步无积压 | Check last sync time both systems / 查两系统最后同步 | Stale >5 min / 旧>5分 | `data/12` #s07, #s30 |
| 3 | Test vs prod env confirmed / 确认在生产环境 | Confirm you're on prod URL / 确认是生产 URL | Wrong env banner / 环境错 | `data/12` #s27 |
| 4 | All staff logged out of MMS / 员工退出会籍 | Sign out shared stations / 共用机退出 | Session left open / 没退 | `data/12` #s15 |
| 5 | Cameras still recording / 摄像头仍在录 | Confirm continuous record / 确认持续录 | Rec stopped / 录停 | `data/11` #n23 |
| 6 | Gate set to close mode / 闸机切闭店模式 | Confirm after-hours lock / 确认闭店锁定 | Gate open / 闸机开 | `data/10` #C2 |
| 7 | Backup verified (size vs live) / 备份已核（体积对在库） | Compare backup size / 对比体积 | Size mismatch / 体积不符 | `data/12` #s22 |
| 8 | Network gear powered via UPS, cabinet locked / 网络设备走UPS、柜已锁 | Check lock + UPS feed / 查锁+UPS供电 | Cabinet open / 柜开 | `references/16`, `data/11` #n06 |

**Execution note / 执行要点**: Close items are the "did we leave anything broken" pass. Item 1 (reconcile) is the money gate — a mismatch >0.5% is a STOP and re-check before you leave. Item 7 proves the nightly backup is real, not just "ran".
**执行要点**：闭店项是「有没有留烂摊子」过关。第1项（对账）是钱闸——差异>0.5% 即停手重查再走。第7项证明夜间备份真成了，不只「跑了」。

---

## Weekly (4 checks) / 每周（4 项）

| # | Item / 项目 | How to check / 怎么查 | Failure look / 失败长啥样 | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Backup restoration verification / 备份可恢复验证 | Restore a small sample to test / 抽小样恢复到测试 | Restore fails / 恢复失败 | `data/12` #s22 |
| 2 | UPS self-test / UPS 自检 | Press UPS test button / 按 UPS 自检键 | Fault indicated / 报故障 | — |
| 3 | Camera spot-check (all zones) / 摄像头全区域抽看 | Scroll through all channels / 逐个通道过 | Blind spot / 盲区 | `data/11` #n13, #n23 |
| 4 | Wi-Fi walk test / Wi-Fi 走动测试 | Walk the floor with a speed app / 拿测速 App 走场 | Dead zone / 死角 | `data/11` #n03, #n26 |

**Execution note / 执行要点**: Do these at close on a quiet day. The restore verification (#1) is the single most skipped and most valuable check — a backup you never tested is a hope, not a safeguard. Log the restore timestamp.
**执行要点**：挑安静日闭店做。恢复验证（#1）最常被跳、也最值钱——没测过的备份只是希望，不是保障。记恢复时间。

---

## Monthly (4 checks) / 每月（4 项）

| # | Item / 项目 | How to check / 怎么查 | Failure look / 失败长啥样 | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Patch day (off-peak) / 维护日（错峰） | Apply updates at close, test / 闭店更新并测 | Broken workflow / 流程坏 | `data/12` #s18 |
| 2 | Permission audit (lite) / 权限轻审计 | Review role matrix vs staff / 比对角色矩阵与员工 | Over/under-permission / 权限错 | `data/12` #s15 |
| 3 | Vendor SLA review / 供应商 SLA 复核 | Check outage log vs SLA / 对故障日志与SLA | Uncredited outage / 未赔 | `data/11` #n10, `data/14` |
| 4 | Failover drill (unplug main line 1 min) / failover 演练（拔主线1分） | Confirm Wi-Fi survives on 4G/5G / 确认切备份还在 | Backup didn't kick / 备份没切 | `data/11` #n11 |

**Execution note / 执行要点**: Patch day must be at close, never peak — a bad update during class hours is a member-experience disaster. The SLA review (#3) turns your `data/16` outage log into real money (service credits). Failover drill (#4) proves the 4G/5G backup actually works before you need it.
**执行要点**：维护日必须闭店、绝不高峰——上课时更新翻车是体验灾难。SLA 复核（#3）把 `data/16` 故障日志变真金（服务抵扣）。failover 演练（#4）在需用前证明 4G/5G 备份真能用。

---

## Quarterly (4 checks) / 每季度（4 项）

| # | Item / 项目 | How to check / 怎么查 | Failure look / 失败长啥样 | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Integration token-expiry sweep / 集成令牌过期巡检 | List all tokens + expiry / 列全部令牌与到期 | Expiring soon / 将过期 | `data/12` #s24, #s07 |
| 2 | DR tabletop (restore drill) / 灾备桌面演练（恢复演练） | Full restore to staging / 全量恢复到预发 | Restore incomplete / 恢复不全 | `data/12` #s22 |
| 3 | Data-quality sampling / 数据质量抽样 | Sample 20 member records / 抽20会员档案 | Mismatch / 不一致 | `data/12` #s10, #s25 |
| 4 | Security self-audit (lite) / 安全自审（轻） | Run `references/16` checklist / 跑 `references/16` 清单 | Isolation gap / 隔离漏 | `references/16`, `data/12` #s32 |

**Execution note / 执行要点**: The token sweep (#1) catches the silent killer before it strikes at 2am on a holiday. The DR tabletop (#2) is a full restore, not a sample — prove the whole club can come back. Security lite (#4) is the early-warning version of the annual full audit.
**执行要点**：令牌巡检（#1）在假期凌晨 2 点爆发前抓出静默杀手。灾备桌面（#2）是全量恢复非抽样——证明整店能回来。安全轻审（#4）是年检全审的预警版。

---

## Annual (5 checks) / 每年（5 项）

| # | Item / 项目 | How to check / 怎么查 | Failure look / 失败长啥样 | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Contract renewals map / 合同续约地图 | List all vendor renewals + dates / 列全部厂商续约与日期 | Forgotten auto-renew / 忘续约 | `data/14`, `references/05` |
| 2 | Password rotation / 密码轮换 | Rotate admin/service creds / 轮换管理员与服务凭据 | Stale creds / 凭据旧 | `data/12` #s15 |
| 3 | PAT electrical testing note / 电气检测（PAT）备注 | Arrange certified electrician / 约持证电工 | Overdue tag / 超期 | `data/11` (electrician), `data/14` |
| 4 | Insurance review / 保险复核 | Confirm cyber/equipment cover / 确认网络/设备险 | Gap / 缺口 | `references/16`, `references/05` |
| 5 | Security self-audit (full) / 安全自审（全） | Full `references/16` pass / 全过 `references/16` | Findings / 发现项 | `references/16` |

**Execution note / 执行要点**: The renewals map (#1) is where you find auto-renew traps and missing exit/data-return clauses before they bite (link `data/14` exit clause, HI-8). PAT (#3) is a legal/insurance requirement in many markets — verify the exact cadence via `tools/05`.
**执行要点**：续约地图（#1）让你在自动续约陷阱与缺失退出/数据返还条款咬人前发现（联 `data/14` 退出条款、HI-8）。PAT（#3）多市场为法定/保险要求——确切周期经 `tools/05` 核验。

---

## Pool / Sauna Club Add-ons / 泳池·桑拿店附加项

> Life-safety items (HI-2). These are operational checks; the digital layer must alert, not replace human supervision.
> 人身安全项（HI-2）。以下为运营检查；数字化层只告警，不替代人工监管。

| Freq / 频次 | Item / 项目 | How to check / 怎么查 | Anchor / 锚点 |
|---|---|---|---|
| Daily | Anti-drowning camera/alert online / 防溺水摄像头告警在线 | Confirm alert system green / 确认告警系统绿 | `data/11` #n23, `references/16` |
| Daily | Sauna over-temp sensor reports / 桑拿超温传感器上报 | Check temp alert feed / 查温度告警流 | `references/16` (HI-2) |
| Weekly | Pool chemical/IoT sensor sync / 水质IoT传感器同步 | Compare sensor vs manual test / 传感器对手测 | `data/11` #n31 |
| Quarterly | AED connectivity check / AED 联网检查 | Confirm AED status ping / 确认 AED 状态 ping | `references/16` |

**Note / 备注**: Any failure of a life-safety check is a **close-and-escalate** event, not a ticket-in-queue. Human supervision redundancy is mandatory (HI-2). The digital alert is a helper, never the sole safeguard.
**备注**：人身安全项失败是**闭店升级**事件，非排队工单。人工监管冗余强制（HI-2）。数字告警只是辅助，绝非零保障。

---

## 24h Unmanned Club Add-ons / 24h 无人店附加项

> Unmanned periods need redundant fail-safe (HI-2). Keep cold-spares on site.
> 无人时段需冗余故障安全（HI-2）。现场留冷备。

| Freq / 频次 | Item / 项目 | How to check / 怎么查 | Anchor / 锚点 |
|---|---|---|---|
| Daily | Offline-mode fallback verified / 离线兜底已验 | Simulate net loss, gate still admits / 模拟断网闸机仍可放 | `data/12` #s31, #s08 |
| Daily | Cold-spare PoE switch present / 冷备 PoE 交换在位 | Physically confirm spare / 实物确认备机 | `data/11` #n23 |
| Weekly | Remote camera all-zone check / 远程全区域看摄像头 | Review all channels remote / 远程过全部通道 | `data/11` #n13 |
| Monthly | Intrusion/alert test / 入侵告警测试 | Trigger test alert / 触发测试告警 | `references/16` |

**Note / 备注**: In unmanned hours there is no human to "notice" a failure, so the redundancy must be self-evident: a spare device physically present, an offline mode proven, and a remote alert that reaches a human phone. Test the alert reaches a real person, not just "the system logged it" (HI-2).
**备注**：无人时段没人「发现」故障，故冗余必须自明：实物冷备、已验证离线模式、能到人手机的远程告警。测告警要真到人，不只「系统记了」（HI-2）。

---

## Logging & Evidence / 记录与证据

Keep one log per club with: date, item, result (OK/FAIL), initials, and for FAILs the anchor + ticket number. This log feeds:
每店留一本日志：日期、项目、结果（OK/失败）、签名、失败项记锚点+工单号。此日志喂给：
- `data/16-freshness-ledger.md` — outage/SLA evidence for vendor negotiation.
- `data/14-repair-scripts-and-sla-library.md` — proof for service-credit claims.
- Insurance and compliance audits (link `references/16`, `references/05`).

A check you didn't log didn't happen. A failure you didn't ticket didn't get fixed.
没记的检 = 没做。没开单的故障 = 没修。

---

## Escalation Path When a Check Fails / 检查发现问题的升级路径

1. **Daily FAIL** → raise ticket immediately, notify duty manager, apply manual fallback (e.g. paper roster, manual gate release per HI-2). / 日检失败 → 立即开单、报值班店长、上人工兜底（纸质名册、人工放行，依 HI-2）。
2. **Weekly FAIL (restore/UPS/camera/Wi-Fi)** → escalate to IT contact/MSP within 24h; log in `data/16`. / 周检失败 → 24h 内报 IT 对接人/MSP；记 `data/16`。
3. **Monthly/Quarterly FAIL (SLA/token/DR/security)** → owner + MSP review; if security gap, treat per `references/16` incident runbook (HI-8). / 月/季检失败 → 老板+MSP 复核；安全漏按 `references/16` 事件手册（HI-8）。
4. **Life-safety FAIL (pool/sauna/unmanned)** → close-and-escalate, human supervision mandatory (HI-2). / 人身安全失败 → 闭店升级，人工监管强制（HI-2）。

---

## Market Localization Note / 市场本地化备注

- **JP / KR**: Vendors expect polite, written escalation (see `data/14` market notes). Log in local language + keep an English copy for HQ. / 厂商期待礼貌书面升级（见 `data/14` 市场备注）。本地语记 + 留英文副本给总部。
- **CN**: WeChat/enterprise groups common for vendor comms; keep the outage log exportable for tax/consumer-protection queries. / 微信/企业群常用于厂商沟通；故障日志可导出以备税务/消保查询。
- **SEA / Oceania**: WhatsApp/LINE/Zalo per market; confirm PAT/electrical test cadence with local regulations via `tools/05`. / 按市场用 WhatsApp/LINE/Zalo；PAT/电气检测周期经 `tools/05` 与当地法规核对。

---

## FDMM → Checklist Coverage Map / 层级→清单覆盖映射

Which checks a club runs depends on its FDMM level (Iron Law 7 — never over-prescribe). Use this map:
不同层级跑不同检查（铁律7——绝不超配）。对照下表：

| FDMM / 层级 | Runs / 执行 | Skip for now / 暂不做 | Why / 原因 |
|---|---|---|---|
| L1 Paper & spreadsheet / 纸表 | Daily open+close only / 仅日开店闭店 | Weekly restore, quarterly DR / 周恢复、季灾备 | No real backup yet, focus on basics / 还没真备份，抓基础 |
| L2 Single-system online / 单系统在线 | + Weekly + Monthly / 加周月 | Quarterly DR full / 季全灾备 | One system, restore sample enough / 单系统，抽样恢复够 |
| L3 Integrated / 集成 | + Quarterly token & data-quality / 加季令牌与数据质量 | — | Integrations need token sweeps / 集成需令牌巡检 |
| L4 Chain / 连锁 | + Annual renewals map across sites / 加年检全店续约地图 | — | Multi-site = contract risk / 多店=合同风险 |
| L5 Autonomous / 自主 | Full + automated logging / 全+自动日志 | — | Unmanned needs full redundancy / 无人需全冗余 |

---

## Why Clubs Skip These (and the cost) / 为什么店会漏做（及代价）

| Skipped / 漏做 | Excuse / 借口 | Real cost when it bites / 真出事代价 | Anchor / 锚点 |
|---|---|---|---|
| Nightly backup verify / 夜备核验 | "It ran, so it's fine" / 跑了就行 | Restore fails at real disaster → data gone / 真灾备恢复失败→数据没 | `data/12` #s22 |
| Failover drill / failover 演练 | "We have 4G backup" / 有备份 | Backup never kicks during outage / 断网时备份没切 | `data/11` #n11 |
| Token sweep / 令牌巡检 | "It just works" / 一直好用 | Sync silently dies at 2am holiday / 假期凌晨同步静默死 | `data/12` #s24 |
| Permission audit / 权限审计 | "Everyone's trusted" / 都信得过 | Over-permission leak or lockout / 过度授权泄露或锁 | `data/12` #s15, #s32 |
| UPS self-test / UPS 自检 | "Light is green" / 灯绿 | Battery dead when power cuts / 断电电池已坏 | `data/11` (weekly) |
| PAT / electrical / 电气检测 | "Never failed" / 从没坏 | Insurance voids claim / 保险拒赔 | `data/11` (electrician) |

The pattern: the skipped check is always the one that fails when it matters most. The log is cheap insurance.
规律：漏做的那项总在最需要时坏。日志是便宜的保险。

---

## Make It Effortless / 让执行不费力

- **Laminate the daily sheets / 日表塑封**: At the desk and the cabinet so they're always visible, no "I forgot the file". / 贴前台与柜，永远可见，不「忘文件」。
- **One shared checklist app / 共用清单 App**: For L2+, use a simple task app with the daily list; ticks auto-log with timestamp + user. / L2+ 用简单任务 App，打勾自动记时间+人。
- **Pair checks with routine / 检查嵌入日常**: Opening checks ride the unlock ritual; closing checks ride the cash-up. No extra "maintenance meeting" needed. / 开店检随开门、闭店检随对账，不另开「维护会」。
- **Calendar reminders / 日历提醒**: Monthly/quarterly/annual items get calendar alerts 3 days early, assigned to a named owner. / 月/季/年项提前 3 天日历提醒，指定到人。
- **Rotate the owner / 轮换负责人**: So one person's blind spot doesn't become the club's blind spot. / 轮换负责人，避免一人盲区变全店盲区。

---

## Shift Handover / 交接班

At handover, the outgoing shift confirms: (1) all daily-open items passed or tickets raised, (2) any FAIL carried on the log with anchor + ticket, (3) the nightly backup will run. The incoming shift reads the log before taking the floor — a FAIL from yesterday is today's first job.
交接班时交班确认：(1) 日开店项全过或已开单，(2) 失败项带锚点+工单留在日志，(3) 夜备会跑。接班先读日志再上岗——昨天的失败是今天第一件事。

---

## Sample Daily Log Template / 日检日志模板（可直接抄）

```
Date / 日期: ____  Shift / 班: 开☑ 闭☑  Logged by / 记录人: ____
开业 Opening:  [1]Gate [2]Printer [3]Net [4]MMS [5]Wi-Fi [6]Cam [7]POS [8]App [9]Backup [10]UPS  (✓/✗ per item)
闭店 Closing: [1]Recon [2]Sync [3]Env [4]Logout [5]Cam [6]Gate [7]Backup [8]Cabinet (✓/✗)
FAILs / 失败: item __ → anchor __ → ticket __ → owner __ → ETA __
备注 Notes: ________________________________________________________
```

Print one per day per club. At month-end, the stack of sheets is your audit trail and SLA-evidence (link `data/16`, `data/14`).
每店每日打印一份。月末这叠纸就是你的审计轨迹与 SLA 证据（联 `data/16`、`data/14`）。

---

## When You Can't Do a Check / 做不了某项检查时

- **No test member for the gate (#1)** → use a staff QR; never open the gate wide. If no staff QR works, it's a #s08 failure, ticket now. / 无测试会员 → 用员工二维码；绝不敞闸。员工码也不行即 #s08 失败，立即开单。
- **No wired laptop for net (#3)** → use a phone on the club's Wi-Fi as a weak proxy, but note "Wi-Fi-only check" — a Wi-Fi pass doesn't prove wired health. / 无有线本 → 用连店 Wi-Fi 的手机弱代，但注明「仅 Wi-Fi 检」——Wi-Fi 通不代表有线健康。
- **Backup timestamp missing (#9/#7)** → treat as FAIL, run a manual backup immediately, verify, then ticket if it fails. / 无备份时间 → 当失败，立即手跑备份并验证，失败则开单。
- **UPS no display (#10)** → check the wall power + breaker; if the UPS is beeping, it's on battery and may die — escalate. / UPS 无显示 → 查墙电+空开；若 UPS 叫，已在电池上或很快没电——升级。

The rule: a check you substitute must be logged as "substitute" with the reason, never silently skipped.
规矩：替代检查须记「替代」+原因，绝不静默跳过。

---

## Seasonal & Event Peaks / 旺季与活动峰值

- **New-Year / membership rush (Jan in many markets)** → add a 2nd daily reconciliation and a booking-capacity watch; API rate-limit risk spikes (see `data/12` #s29). / 新年办卡潮（多市场 1 月）→ 加第二次日对账 + 课容监控；API 限流风险升（见 `data/12` #s29）。
- **Promo days / 大促日** → pre-book rate-limit headroom 3 days before; staff on standby for payment failover (see `data/11` #n02). / 大促日 → 提前 3 天预购限流余量；员工待命支付 failover（见 `data/11` #n02）。
- **Summer pool season / 泳季** → double the life-safety checks frequency; heat stresses sauna sensors (HI-2). / 夏季泳季 → 人身安全项频次加倍；高温压桑拿传感器（HI-2）。
- **Year-end / 年末** → run the annual map early (Dec), not in a holiday lull when vendors are slow. / 年末 → 年检地图提前（12 月）跑，别等假期厂商慢。

---

## Versioning This Calendar / 日历版本管理

- Keep the `last-verified` header current; if a check changes (new vendor, new device), bump the date and note what changed in the club's ops binder. / 保持 `last-verified` 头最新；某项变了（新厂商、新设备）就更新日期并在活页夹记变更。
- If `tools/04`/`tools/05` surface a regulation change (e.g. PAT cadence, biometric alert rule), update the affected add-on and re-verify. / 若 `tools/04`/`tools/05` 露出法规变更（如 PAT 周期、生物识别告警规则），更新对应附加项并重核。
- Old printed sheets: stamp "SUPERSEDED / 已废止" before binning so no one runs a stale checklist. / 旧打印表：丢前盖「已废止」，免有人跑过期清单。

**Red-line summary / 红线摘要**: Life-safety checks (pool/sauna/unmanned) = close-and-escalate, never queue. Backup/restore + failover + token sweeps = the three checks clubs most regret skipping. Log everything; a check not logged didn't happen.
**红线摘要**：人身安全项（泳池/桑拿/无人）= 闭店升级，绝不排队。备份恢复 + failover + 令牌巡检 = 店最悔漏的三项。事事留痕；没记的检 = 没做。

**Coverage count / 覆盖计数**: 10 opening + 8 closing + 4 weekly + 4 monthly + 4 quarterly + 5 annual = 35 base items, plus 4 pool/sauna + 4 unmanned add-ons = 43 tracked checks per club. / 10 开店 + 8 闭店 + 4 周 + 4 月 + 4 季 + 5 年 = 35 基础项，加 4 泳池/桑拿 + 4 无人 = 每店 43 个跟踪项。

---

## G13 Tri-Perspective Note / G13 三视角覆盖说明

**Architect (架构师视角)**: The calendar operationalizes FDMM L1 daily discipline and feeds the DR/security loops (Cluster G/J). Each item links to a fault-tree anchor so prevention and firefighting share one map. Pool/sauna and 24h add-ons enforce HI-2 fail-safe redundancy. The escalation path binds operations to the SLA/security libraries.
**架构师视角**：本日历落地 FDMM L1 日常纪律，并喂给灾备/安全闭环（G/J 集群）。每项联故障树锚点，使预防与救火共用一张图。泳池/桑拿与 24h 附加项落实 HI-2 故障安全冗余。升级路径把运营绑到 SLA/安全库。

**Operator (运营者视角)**: Printable, plain-words checklists mean a rookie can run open/close without IT. "What failure looks like" turns vague worry into a clear action + anchor. The log is the operator's shield in vendor and insurance disputes. Monthly/quarterly/annual cadence protects budget (SLA credits, renewals).
**运营者视角**：可打印、说人话的清单让新手无 IT 也能开店闭店。「失败长啥样」把模糊担心变清晰动作+锚点。日志是运营者在厂商/保险纠纷中的盾。月/季/年节奏护预算（SLA 抵扣、续约）。

**Member (会员视角)**: A well-run calendar means fewer outages, safer pools/saunas, and reliable check-in even unmanned — member trust protected by boring, consistent maintenance (HI-2, HI-8). Life-safety checks put member bodies before convenience.
**会员视角**：良好日历 = 更少故障、更安全泳池/桑拿、无人也可靠入场——会员信任靠枯燥而稳定的维护守护（HI-2、HI-8）。人身安全检查把会员身体置于便利之前。

---

*Legal Notice / 法律声明 · Disclaimer / 免责声明 · Friendly Reminder / 温馨提示 · Author / 作者信息 — see SKILL.md output block. / 见 SKILL.md 输出规范块。*
