# System Migration & Data Plan / 系统迁移与数据方案

> **Cluster / 集群**: N (Integration) + G (lifecycle G4)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Export tooling & volume 🔄 via `tools/04`; retention law via `tools/05`; align to `references/15#g4-renovation`.
> **Cross-references / 交叉引用**: `data/12#s16-data-export-incomplete`, `data/12#s10-report-numbers-dont-match`, `templates/20` (exit clause), `templates/21`, `references/15#g4-renovation`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this plan to **migrate member/system data between platforms** without losing a single record or double-charging anyone. It is the safeguard for `references/15#g4-renovation`.
本方案用于**跨平台迁移会员/系统数据**，不丢一条、不重复扣费。是 `references/15#g4-renovation` 的安全网。

- **FDMM gate / 等级闸门**: L1→L2 (first SaaS migration) and every later switch. Always run dry-run + reconciliation.
  L1→L2（首套 SaaS 迁移）及之后每次切换。必跑空跑+对账。
- **Trigger / 触发**: replacing membership/POS system, M&A member merge, or "old contract ends next month".
  替换会籍/POS、并购合会员、或"旧合同下月到期"。

---

## ② Prerequisites checklist / 前置清单

- [ ] Data-export clause confirmed in OLD contract (`templates/20` §3.4). / 旧合同导出条款已确认。
- [ ] New system fields mapped (§3.1). / 新系统字段已映射（§3.1）。
- [ ] Dry-run environment ready (§3.3). / 空跑环境就绪（§3.3）。
- [ ] Cutover window agreed (low-traffic, §3.4). / 切换窗口已定（低峰，§3.4）。
- [ ] Member comms drafted (§3.6). / 会员通知已拟（§3.6）。
- [ ] Rollback criteria set (§3.5). / 回滚标准已定（§3.5）。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Source inventory & field-mapping workbook / 源清单与字段映射表

| Source field / 源字段 | Old system / 旧系统 | Target field / 新系统 | Transform / 转换 | Owner / 负责人 |
|---|---|---|---|---|
| Member ID 会员号 | `____` | `____` | direct/映射 | `____` |
| Name+phone 姓名手机 | `____` | `____` | hash? 是否脱敏 | `____` |
| Balance 储值余额 | `____` | `____` | currency 币种 | `____` |
| Bookings 预约 | `____` | `____` | date tz 时区 | `____` |
| Orders 订单 | `____` | `____` | idempotency 幂等 | `____` |
| Consents 同意 | `____` | `____` | retain 保留 | `____` |

> **Guidance / 指引**: Map EVERY field; unmapped = silently dropped (`data/12#s16-data-export-incomplete`). Biometric templates: export only if market allows, local-first (HI-9).
> 每个字段都要映射；漏映=静默丢失。生物模板：仅当地允许且本地优先才导出（HI-9）。

### 3.2 Cleansing rules log / 清洗规则日志

| Rule / 规则 | Action / 动作 | Count / 数量 |
|---|---|---|
| Duplicate member 重复会员 | merge by phone 按手机合并 | `____` |
| Invalid phone 无效手机 | flag, don't block 标疑不阻 | `____` |
| Negative balance 负余额 | review 复核 | `____` |
| Orphan booking 孤儿预约 | cancel+notify 取消通知 | `____` |

### 3.3 Dry-run plan & reconciliation counts (MUST balance) / 空跑与对账（必须平）

Run migration to a TEST instance; reconcile totals BEFORE touching prod.
先迁到测试实例；动生产前对账。

| Entity / 对象 | Old count / 旧数 | New count / 新数 | Diff / 差 | Verdict / 判 |
|---|---|---|---|---|
| Members 会员 | `____` | `____` | `____` | pass/fail |
| Balances sum 余额和 | `____` | `____` | `____` | pass/fail |
| Bookings 预约 | `____` | `____` | `____` | pass/fail |
| Orders 订单 | `____` | `____` | `____` | pass/fail |

> **Stop-line / 停手线**: If any row fails, DO NOT proceed. A mismatch here = double-charge or lost member later (`data/12#s10-report-numbers-dont-match`).
> 任一行不平，绝不动生产。此处不平=日后重复扣费或丢会员。

### 3.4 Cutover runbook (hour-by-hour) / 切换手册（逐小时）

| Time / 时间 | Action / 动作 | Owner / 人 | Check / 核查 |
|---|---|---|---|
| T-2h | freeze new writes on old 旧系统冻结写入 | `____` | snapshot 快照 |
| T-1h | full export + checksum 全导出+校验 | `____` | hash ok |
| T+0h | import to prod 导入生产 | `____` | counts match 数对 |
| T+1h | smoke test: login, check-in, pay 冒烟测 | `____` | 3 passes 三项过 |
| T+2h | open to members 对会员开放 | `____` | monitor 监控 |

### 3.5 Rollback criteria / 回滚标准

Roll back to OLD system if ANY:
任一中即回滚旧系统：
- [ ] Member count mismatch > `____` %. / 会员数差 > `____`%。
- [ ] Balance sum mismatch > `____` ¥. / 余额和差 > `____` 元。
- [ ] Check-in fails for test cards. / 测试卡入场失败。
- [ ] Payment not reconciling. / 支付不对账。

> Old system stays LIVE (read-only) for `____` days post-cutover. / 切换后旧系统保留只读 `____` 天。

### 3.6 Member communication templates / 会员通知模板

**Pre-notice (T-7d) / 预告（T-7天）**:
> "We're upgrading our system on `____`. Your membership, balance and bookings are safe and will move automatically. You may need to re-set your password/app login." / "我们将于`____`升级系统。您的会籍、余额、预约安全且自动迁移。您可能需重设密码/App 登录。"

**Go-live (T+0) / 上线**:
> "Upgrade complete — welcome back! If anything looks wrong, tell front desk; your old data is retained." / "升级完成，欢迎回来！若有异常请告知前台；旧数据已留底。"

### 3.7 STOP-LINE (critical) / 绝对停手线（关键）

> **NEVER terminate the old contract or shut down the old system before a VERIFIED export + reconciliation passes.**
> **在经核实的导出且对账通过之前，绝不可终止旧合同或关停旧系统。**

See `data/12#s16-data-export-incomplete` — switching vendor before export = trapped + lost records. Keep old system read-only live for the quarantine window.
见 `data/12#s16-data-export-incomplete`——导出前换供应商=被困+丢数据。旧系统保留只读活过隔离期。

---

## ④ Common mistakes / 常见错误

1. Kill old contract before verified export → trapped. / 验证导出前砍旧合同→被困。→ `data/12#s16-data-export-incomplete`
2. Migrating during peak opening. / 开业高峰迁移。→ `data/21#ap-013-migrate-peak`
3. Unmapped fields silently dropped. / 字段漏映静默丢。→ `data/12#s16-data-export-incomplete`
4. Numbers don't match, go live anyway. / 数对不上仍上线。→ `data/12#s10-report-numbers-dont-match`
5. No rollback window → no way back. / 无回滚窗口→无退路。

---

## ⑤ Related files / 相关文件

- `references/15-lifecycle-scenarios.md#g4-renovation` — G4 narrative / G4 全流程
- `templates/20-rfp-technical-spec.md` — exit clause / 退出条款
- `templates/21-vendor-evaluation-matrix.md` — pick new vendor / 选新供应商
- `data/12-software-fault-tree-library.md#s16-data-export-incomplete` — export red line / 导出红线
- `tools/05-regulation-traceability-verification.md` — retention / 留存合规

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (field mapping + reconciliation logic), **Operator** (cutover runbook + rollback + comms), and **Member** (balance/booking safety, transparent notice, no double-charge); the STOP-LINE protects members from data loss and the club from lock-in.
本模板覆盖**架构师**（字段映射+对账逻辑）、**运营者**（切换手册+回滚+通知）、**会员**（余额/预约安全、透明通知、不重复扣费）；绝对停手线护会员数据、防店铺被锁。
