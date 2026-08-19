# Inspection Checklist Pack (Printable) / 巡检清单包（可打印）

> **Cluster / 集群**: G (Lifecycle) + D (Network) + C (Hardware)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify vendor patch cadence and UPS/PAT rules every 90 days via `tools/04`/`tools/05`; align exactly with `data/13-inspection-and-maintenance-calendar.md`.
> **Cross-references / 交叉引用**: `data/13-inspection-and-maintenance-calendar.md` · `data/10-hardware-fault-tree-library.md` · `data/11-network-fault-tree-library.md` · `data/12-software-fault-tree-library.md` · `references/16-security-operations-and-emergency.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: Laminated, pocket-sized cards for the daily open/close, weekly walk-test, monthly patch-day, plus pool/sauna and 24h-unmanned add-ons. Designed so a rookie with no IT background can run them. Every item has plain-words "how to check", a pass/fail box, and a fault-tree anchor — so a FAIL becomes a ticket, not a guess.
**中文**：塑封、巴掌大的卡片，覆盖日开店/闭店、周走动测试、月维护日，外加泳池/桑拿与 24h 无人附加卡。专为无 IT 背景的新手设计。每项都有说人话的「怎么查」、合格/失败框、故障树锚点——失败即开单，而非瞎猜。

> ⚠️ **Life-safety items (pool/sauna/unmanned) = close-and-escalate, never queue** (HI-2). Digital alerts only help; human oversight is mandatory.
> ⚠️ **人身安全项（泳池/桑拿/无人）= 闭店升级，绝不排队**（HI-2）。数字告警只辅助；人工监管强制。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | Print + laminate / 打印塑封 | desk + comms cabinet / 前台+弱电柜 |
| 2 | Test member or staff QR / 测试会员或员工码 | for gate check / 闸机检查用 |
| 3 | Wired laptop + phone / 有线本+手机 | net & Wi-Fi check / 网络与 Wi-Fi 检 |
| 4 | FDMM level known / 已知 FDMM | L1 = daily+weekly only / L1 仅日+周 |

---

## ③ THE TEMPLATE / 模板正文

### #card-daily-open Daily Opening — 10 Items / 每日开店 10 项

Date / 日期: ____  Shift / 班: ____  By / 记录人: ____   (✓ pass / ✗ fail)

| # | Item / 项目 | How to check (plain) / 怎么查（说人话） | ✔/✗ | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Gate opens valid QR/face / 闸机有效码可开 | Tap a test member at open / 开店刷测试会员 | □ | `data/12#s08`, `data/10#C2` |
| 2 | Receipt printer test / 小票测试 | Print one test slip / 打一张测试 | □ | `data/12#s20`, `data/11#n15` |
| 3 | Internet up (wired) / 有线网通 | Open a site on wired laptop / 有线本开网页 | □ | `data/11#n01` |
| 4 | MMS login works / 会籍能登 | Log in ≥1 staff / 至少1员工登 | □ | `data/12#s01` |
| 5 | Member Wi-Fi visible / 会员Wi-Fi可见 | Scan with phone / 手机扫 | □ | `data/11#n04` |
| 6 | Cameras recording / 摄像头在录 | Check live view on NVR / 看 NVR 实时 | □ | `data/11#n23`, `#n13` |
| 7 | POS ¥1 test sale / POS测¥1 | Tiny sale then refund / 小额测再退 | □ | `data/11#n02`, `data/12#s12` |
| 8 | App shows classes / App显课表 | Open app confirm schedule / 开 App 确认 | □ | `data/12#s04`, `#s03` |
| 9 | Backup ran / 昨夜备份 | Confirm timestamp / 确认时间 | □ | `data/12#s22` |
| 10 | UPS green / UPS绿 | Look at display / 看显示 | □ | `data/11` (weekly test) |

> FAIL on #1 or #3 before peak = go/no-go call (HI-2 egress). Don't open silently — ticket + manual check-in note.
> #1 或 #3 高峰前失败 = 开/不开决策（HI-2 疏散）。别悄悄开门——开单+人工入场告示。

### #card-daily-close Daily Closing — 8 Items / 每日闭店 8 项

Date / 日期: ____  By / 记录人: ____   (✓ / ✗)

| # | Item / 项目 | How to check / 怎么查 | ✔/✗ | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Sales reconciled / 营收对账 | MMS vs POS vs gateway / 三系统对账 | □ | `data/12#s12`, `#s10` |
| 2 | Sync cleared / 同步无积压 | Last sync both sides / 查两系统末同步 | □ | `data/12#s07`, `#s30` |
| 3 | Prod env confirmed / 在生产 | Confirm prod URL / 确认生产 URL | □ | `data/12#s27` |
| 4 | Staff logged out / 员工退出 | Sign out shared stations / 共用机退出 | □ | `data/12#s15` |
| 5 | Cams still recording / 仍在录 | Confirm continuous / 确认持续录 | □ | `data/11#n23` |
| 6 | Gate close mode / 闸机闭店 | Confirm after-hours lock / 闭店锁定 | □ | `data/10#C2` |
| 7 | Backup verified / 备份已核 | Compare size vs live / 比体积 | □ | `data/12#s22` |
| 8 | Cabinet locked+UPS / 柜锁+UPS | Lock + UPS feed / 查锁+UPS | □ | `references/16`, `data/11#n06` |

> Item 1 mismatch >0.5% = STOP and re-check before you leave. Item 7 proves the backup is real, not just "ran".
> 第1项差异>0.5% 即停手重查再走。第7项证明备份真成了，不只「跑了」。

### #card-weekly Weekly Walk-Test — 4 Items / 每周走动 4 项

Date / 日期: ____  By / 记录人: ____

| # | Item / 项目 | How / 怎么 | ✔/✗ | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Backup restore test / 恢复验证 | Restore a small sample / 抽小样恢复 | □ | `data/12#s22` |
| 2 | UPS self-test / UPS自检 | Press test button / 按自检键 | □ | — |
| 3 | Camera all-zone / 全区域看 | Scroll all channels / 过全部通道 | □ | `data/11#n13`, `#n23` |
| 4 | Wi-Fi walk test / Wi-Fi走测 | Walk floor with speed app / 拿测速走场 | □ | `data/11#n03`, `#n26` |

### #card-monthly Monthly Patch-Day — 4 Items / 每月维护日 4 项

Date / 日期: ____  By / 记录人: ____   ⚠️ At close, never peak / 闭店做，绝不高峰

| # | Item / 项目 | How / 怎么 | ✔/✗ | Anchor / 锚点 |
|---|---|---|---|---|
| 1 | Patch off-peak / 错峰更新 | Apply + test at close / 闭店更新并测 | □ | `data/12#s18` |
| 2 | Permission audit (lite) / 权限轻审 | Role matrix vs staff / 比矩阵与员工 | □ | `data/12#s15` |
| 3 | Vendor SLA review / SLA复核 | Outage log vs SLA / 对日志与SLA | □ | `data/11#n10`, `data/14` |
| 4 | Failover drill / failover演练 | Unplug main 1 min / 拔主线1分 | □ | `data/11#n11` |

### #card-pool Pool / Sauna Add-on — 4 Items / 泳池·桑拿附加 4 项

> HI-2 life-safety — FAIL = close-and-escalate. / HI-2 人身安全——失败即闭店升级。

| Freq / 频次 | Item / 项目 | How / 怎么 | ✔/✗ | Anchor / 锚点 |
|---|---|---|---|---|
| Daily | Anti-drown alert online / 防溺告警在线 | Alert system green / 告警绿 | □ | `data/11#n23`, `references/16` |
| Daily | Sauna over-temp reports / 桑拿超温上报 | Check temp feed / 查温度流 | □ | `references/16` (HI-2) |
| Weekly | Pool chemical/IoT sync / 水质同步 | Sensor vs manual / 传感器对手测 | □ | `data/11#n31` |
| Quarterly | AED connectivity / AED联网 | Status ping / 状态ping | □ | `references/16` |

### #card-unmanned 24h Unmanned Add-on — 4 Items / 24h 无人附加 4 项

> Redundant fail-safe required (HI-2). Cold-spare on site. / 需冗余故障安全（HI-2）。现场留冷备。

| Freq / 频次 | Item / 项目 | How / 怎么 | ✔/✗ | Anchor / 锚点 |
|---|---|---|---|---|
| Daily | Offline-mode fallback / 离线兜底 | Simulate net loss, gate admits / 模拟断网可放 | □ | `data/12#s31`, `#s08` |
| Daily | Cold-spare PoE present / 冷备在位 | Physically confirm / 实物确认 | □ | `data/11#n23` |
| Weekly | Remote all-zone cam / 远程全区域 | Review channels remote / 远程过通道 | □ | `data/11#n13` |
| Monthly | Intrusion/alert test / 入侵告警测 | Trigger test alert / 触发测试 | □ | `references/16` |

---

## ④ Common Mistakes / 常见错误

- **Skip restore test** → backup fails when needed. → `data/21#ap-021-backup-theater`.
- **Patch during peak** → class-hour disaster. → `data/13` monthly note.
- **Pool check "queued"** → tragedy. → `data/21#ap-012-sensor-over-lifeguard`, `data/21#ap-054-pool-open-no-lifeguard` (HI-2).
- **Gate FAIL opened wide** → use staff QR, never wide. → `data/13` "can't do a check".

---

## ⑤ Related Files / 相关文件

- `data/13-inspection-and-maintenance-calendar.md` — master cadence this pack operationalizes. / 本包落地的主日历。
- `data/10` / `data/11` / `data/12` — fault-tree anchors referenced per item. / 每项引用的故障树。
- `templates/38-emergency-contact-card.md` — if a check FAILS, who to call. / 检查失败时的呼叫卡。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: Each card item links to a `data/10~12` fault anchor so prevention and firefighting share one map; pool/unmanned cards enforce HI-2 fail-safe redundancy.
**运营者 / Operator**: Laminate and pin — a rookie runs open/close without IT; the pass/fail box + anchor turns vague worry into a ticket with evidence.
**会员 / Member**: Consistent maintenance = fewer outages, safer pools/saunas, reliable check-in even unmanned — trust protected by boring routine, not luck (HI-2, HI-8).
