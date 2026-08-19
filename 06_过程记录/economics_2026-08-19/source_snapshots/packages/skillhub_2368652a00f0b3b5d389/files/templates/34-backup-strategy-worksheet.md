# Backup Strategy Worksheet (3-2-1) / 备份策略工作表（3-2-1）

> **Cluster / 集群**: K (Data & AI) + J (Resilience)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify cloud-storage pricing and retention rules every 180 days via `tools/04`; align with `references/16#j-backup-3-2-1`.
> **Cross-references / 交叉引用**: `references/16-security-operations-and-emergency.md` (#j-backup-3-2-1, #j-crypto-locking malware-response) · `data/21-anti-pattern-library.md` · `data/12-software-fault-tree-library.md` (#s22)
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: Plan and prove your backups using the industry-standard **3-2-1 rule** — before disaster, not after. The #1 club backup mistake is backing up files but forgetting the **MMS/CRM export**, then losing every member record. This worksheet also forces the quarterly restore test that separates real safety from "backup theater."
**中文**：用行业标准 **3-2-1** 提前规划并验证备份，而非灾后。场馆头号备份坑是只备份文件却忘了**会籍/CRM 导出**，结果丢了全部会员档案。本表还强制季度恢复实测——把「真安全」和「备份表演」分开。

> 💡 An untested backup is a hope, not a backup. A backup you never restored can be silently incomplete. Test quarterly — no exceptions (→ `data/21#ap-021-backup-theater`).
> 💡 没实测的备份只是希望，不是备份。从没恢复过的备份可能悄悄不全。季度实测——无例外（→ `data/21#ap-021`）。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | List of systems holding data / 含数据系统清单 | MMS, POS, gate, CCTV, body analyzer / 会籍、收银、闸机、监控、体测 |
| 2 | Cloud account + offline disk / 云账号+离线盘 | two media / 两种介质 |
| 3 | Owner named / 指定负责人 | one person accountable / 一人负责 |
| 4 | FDMM level / FDMM 等级 | L1 = daily cloud + weekly disk / L1 每日云+每周盘 |

---

## ③ THE TEMPLATE / 模板正文

### #backup-3-2-1 The 3-2-1 Rule / 3-2-1 法则

- **3 copies / 三份**: live data + 2 backups. / 在线数据+两份备份。
- **2 media / 两种介质**: e.g. cloud + USB disk. / 如 云端+移动硬盘。
- **1 offsite / 一份异地**: cloud counts; a fire shouldn't burn your only copy. / 云端即算；起火不该烧唯一备份。

### #what-to-backup What-To-Back-Up Inventory / 备份清单（不只文件）

| Source / 来源 | Method / 方式 | ≠ just files! / 不只文件 |
|---|---|---|
| **MMS/CRM export** | scheduled API/CSV dump / 定时 API/CSV 导出 | ⚠️ most-missed / 最常被漏 |
| POS transactions / 收银流水 | gateway + local export / 网关+本地导出 | — |
| Member DB + photos / 会员库+照片 | DB backup / 库备份 | PII — encrypt / 加密 |
| CCTV footage / 监控录像 | NVR archive / NVR 归档 | per market retention / 按市场留存 |
| Body-analyzer data / 体测数据 | export per consent / 按同意导出 | HI-1/HI-8 |
| Config & licenses / 配置与授权 | file + screenshot / 文件+截图 | — |

> 🔄 Cloud pricing ranges shift — re-quote before committing (→ `tools/04`). MMS export format must be open (CSV/JSON) so you are never hostage (→ `data/21#ap-002-no-data-export`).
> 🔄 云价区间易变——承诺前重新询价。MMS 导出须开放格式，免被锁（→ `data/21#ap-002`）。

### #schedule-grid Schedule & Retention Grid / 计划与留存网格

| Source / 来源 | Frequency / 频率 | Media / 介质 | Retention / 留存 🔄 | Owner / 负责 |
|---|---|---|---|---|
| MMS/CRM | daily / 每日 | cloud + disk | 30–90d (market) / 按市场 | IT |
| POS | daily / 每日 | cloud | 365d | FD |
| CCTV | continuous / 持续 | NVR + offsite | per law / 依法 | IT |
| Config | monthly / 每月 | disk | 1y | IT |

### #restore-log Restore-Test Log (QUARTERLY MANDATORY) / 恢复实测日志（季度强制）

| Date / 日期 | Restored what / 恢复项 | Row count match? / 行数吻合 | Spot-check / 抽查 | Result / 结果 | By / 人 |
|---|---|---|---|---|---|
| ____ | MMS __ | Y/N | member X ok | OK/FAIL | ____ |

> Procedure / 步骤: (1) pick a past date; (2) restore to a spare machine; (3) confirm member count + last 7 days txn; (4) log "restore tested YYYY-MM-DD — OK". Fail = fix backup method before anything else.
> 步骤：(1) 选过去日期；(2) 恢复到备用机；(3) 确认会员数+近7天交易；(4) 记「恢复实测 OK」。失败=先修备份。

### #responsibility Responsibility Assignment / 责任分配

| Task / 任务 | Who / 谁 | When / 何时 |
|---|---|---|
| Daily backup verified / 日备核验 | FD / 前台 | open & close / 开店闭店 |
| Quarterly restore / 季恢复 | IT / IT | calendar alert +3d / 提前3天 |
| Cloud account owner / 云账号主 | Owner / 老板 | always / 始终 |

### #cloud-vs-local Cloud vs Local Decision Helper / 云端 vs 本地决策帮手

| If… / 若 | Prefer / 优先 |
|---|---|
| ≤L2, small team / 小团队 | cloud daily + owner disk weekly / 每日云+老板周盘 |
| Video heavy / 录像多 | local NVR + cloud offsite copy / 本地NVR+云异地 |
| Compliance data-sovereignty / 数据驻留 | local-first, no cross-border / 本地优先不出境 (HI-9) |
| Unmanned / 无人 | cloud + auto-test alert / 云+自动测告警 |

---

## ④ Common Mistakes / 常见错误

- **Backup theater** → backed up, never restored, lost data. → `data/21#ap-021-backup-theater`.
- **MMS not exported** → member records gone. → `data/21#ap-002-no-data-export`.
- **Card numbers in backup** → PAN breach. → `data/21#ap-008-card-numbers-spreadsheet`.
- **Single medium** → one failure kills both. → `references/16#j-backup-3-2-1`.

---

## ⑤ Related Files / 相关文件

- `references/16-security-operations-and-emergency.md` — `#j-backup-3-2-1`, `#j-crypto-locking malware-response`.
- `data/12-software-fault-tree-library.md` — `#s22` backup fault anchor.
- `templates/35-sla-contract-review.md` — data-export clause before sign. / 签约前数据导出条款。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: 3-2-1 + quarterly restore is the data-resilience baseline of FDMM; MMS export is explicitly required so member data is never lost to "file-only" thinking (HI-8 minimization vs retention balance).
**运营者 / Operator**: A one-page worksheet + a calendar reminder makes backup discipline a habit, not a project — and the restore log is the operator's proof of "we can reopen."
**会员 / Member**: Tested backups mean the club can recover member records, bookings and balances after an attack — member trust protected by preparation, not luck (HI-2 spirit).
