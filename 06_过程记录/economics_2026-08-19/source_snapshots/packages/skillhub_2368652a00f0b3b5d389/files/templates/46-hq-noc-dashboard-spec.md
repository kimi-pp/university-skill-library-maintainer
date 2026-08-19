# HQ Multi-Club Monitoring (NOC) Dashboard Spec / 总部多店监测（NOC）看板规格

> **Cluster / 集群**: H (infra & monitoring) + G (HQ governance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Tooling vendor examples 🔄 via `tools/04`; fault-tree detail in `data/10/11/12`; quiet-hours policy per market 🔄 via `tools/05`.
> **Cross-references / 交叉引用**: `data/10-hardware-fault-tree-library.md`, `data/11-network-fault-tree-library.md`, `data/12-software-fault-tree-library.md`, `templates/42` (franchise visibility), `tools/05-regulation-traceability-verification.md`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this spec to **build a HQ network-operations view** across all clubs so one screen shows which clubs are healthy and which are silently failing (gate down, backup missed).
本规格用于**搭建总部多店运维视图**，一屏看清各店健康与静默故障（门禁掉、备份漏）。

- **FDMM gate / 等级闸门**: L2+ (5+ clubs); L1 may use a lighter single-sheet.
  L2+（5+ 店）；L1 可用更轻单表。
- **Trigger / 触发**: Club count grows beyond manual WhatsApp checks.
  门店数超出人工微信群排查。

---

## ② Prerequisites checklist / 前置清单

- [ ] Per-club heartbeat sources identified (gate/POS/NVR/UPS). / 各店心跳源已定（门禁/POS/NVR/UPS）。
- [ ] Internet & backup monitoring in place. / 网络与备份监测已就。
- [ ] Franchise vs owned visibility boundaries set (`tools/05`). / 加盟与直营可见边界已定。
- [ ] Alert routing owners named. / 告警路由责任人已定。
- [ ] Fault-tree runbooks linked (`data/10/11/12`). / 故障树 runbook 已链。
- [ ] Dashboard access roles defined. / 看板访问角色已定。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Per-club health signals table / 各店健康信号表

| Signal / 信号 | Source / 源 | Healthy / 健康 | Alert / 告警 |
|---|---|---|---|
| Internet up 网络通 | ping/ISP | ≤ `____` ms | > `____` ms |
| Gate heartbeat 门禁心跳 | access ctrl | < `____` min gap | gap > `____` |
| POS heartbeat 收银心跳 | POS | < `____` min | gap > `____` |
| Backup success 备份成功 | backup job | daily OK | missed `____` |
| NVR disk 录像盘 | NVR | > `____`% free | < `____`% |
| UPS status UPS状态 | UPS | on-line | on-battery > `____` |
| Door count vs avg 门数对比 | access log | ±`____`% | beyond |

> **What good looks like / 合格样**: One dashboard row per club, red row = someone already dispatched.
> 好样：每店一行，红行=已派人。
> **Red flag / 红线**: "We'll know when members complain" → gate was down 3 days.
> 红线："会员投诉才知道"→门禁已掉 3 天。

### 3.2 Alert routing & quiet-hours / 告警路由与静默时段

- Route: L1 club staff → L2 HQ NOC → L3 vendor. / 路由：L1 店员→L2 总部 NOC→L3 厂商。
- Escalation if no ack in `____` min. / `____` 分钟未确认即升级。
- :::dynamic-hook topic="quiet-hours-policy-per-market" staleness="180d" action="tools/05" fallback="treat as unverified"
  As of 2026-07: quiet-hours (no non-critical alerts) vary by market labor law; set per `tools/05`.
  截至 2026-07：静默时段（非紧急不告警）各市场劳动法不同；按 tools/05 设。
  :::
- Critical always-on: gate down, internet down, backup failed. / 紧急常开：门禁掉、网络断、备份失败。

### 3.3 Weekly ops review agenda & scorecard / 周运营复盘议程与记分卡

| Item / 项 | Owner / 责 |
|---|---|
| Red-club review 红店复盘 | NOC lead |
| Repeated-fault trend 重复故障趋势 | Ops |
| Backup-failure drill 备份失败演练 | IT |
| Scorecard update 记分卡更新 | Analyst |

| Scorecard KPI / 指标 | Target / 目标 |
|---|---|
| Clubs green % 绿店率 | ≥ `____`% |
| MTTR (alert→fix) 修复时长 | < `____` h |
| Backup success % 备份成功率 | ≥ `____`% |
| Repeat-fault rate 重复故障率 | < `____`% |

> **Guidance / 指引**: Trend the repeat-fault rate — one club red weekly means a root-cause, not bad luck.
> 指引：盯重复故障率——单店周周红是根因非运气。

### 3.4 Franchise vs owned visibility split / 加盟与直营可见分界

- Owned clubs: full signal detail. / 直营：全信号明细。
- Franchise clubs: aggregate health only; no CCTV/HR detail (`tools/05`, `templates/42` §3.3). / 加盟：仅聚合健康，无监控/人事明细。
- [ ] Boundary documented & agreed. / 边界已记且共识。
- [ ] Franchisee gets own read-only view. / 加盟商得自有只读视图。

> **Privacy boundary / 隐私边界**: HQ sees franchisee club uptime, NOT member faces or staff records.
> 隐私边界：HQ 看加盟店在线率，不看会员脸或员工档。

### 3.5 Tooling tiers by chain size / 按规模分层工具

:::dynamic-hook topic="noc-tooling-vendor-examples" staleness="120d" action="tools/04" fallback="treat as unverified"
As of 2026-07 tiers (examples, verify `tools/04`): 5 clubs `____`; 20 clubs `____`; 50+ `____`.
截至 2026-07 分层（示例，tools/04 核）：5 店 `____`；20 店 `____`；50+ `____`。
:::

| Size / 规模 | Approach / 方式 |
|---|---|
| 5 clubs | spreadsheet + ping scripts |
| 20 clubs | lightweight NMS + dashboard |
| 50+ | full NOC platform + SLA |

> **Rule / 规则**: Don't buy 50+ tier at 5 clubs — overhead eats the benefit.
> 规则：5 店别买 50+ 级——开销吞掉收益。

### 3.6 Runbook links into fault trees / 链入故障树

- Hardware faults → `data/10-hardware-fault-tree-library.md`. / 硬件→data/10。
- Network faults → `data/11-network-fault-tree-library.md`. / 网络→data/11。
- Software faults → `data/12-software-fault-tree-library.md`. / 软件→data/12。
- Each alert must deep-link to its fault tree node. / 每条告警须深链至故障树节点。

---

### 3.7 NOC headcount & capacity / NOC 人力与容量

| Chain size / 规模 | NOC FTE / 人力 | Coverage 覆盖 |
|---|---|---|
| 5 clubs | `____` (shared) | biz hrs |
| 20 clubs | `____` | extended |
| 50+ | `____` + vendor | 24x7 |

> **Rule / 规则**: Headcount scales with alert volume, not club count alone — automate first.
> 规则：人力随告警量而非仅店数扩——先自动化。

### 3.8 Dashboard access roles / 看板访问角色

- HQ NOC: full owned + aggregate franchise. / HQ NOC：全直营+聚合加盟。
- Franchisee: own club read-only. / 加盟商：本店只读。
- Vendor: scoped per contract. / 厂商：按合同限定。
- [ ] Role matrix signed by security. / 角色矩阵经安全签。

### 3.9 Escalation matrix / 升级矩阵

| Severity / 级 | Example 例 | Ack / 确认 | Escalate 升级 |
|---|---|---|---|
| P1 critical P1 | gate down 门禁掉 | `____` min | L3 vendor |
| P2 high P2 | backup failed 备份失败 | `____` min | HQ IT lead |
| P3 medium P3 | NVR disk low 盘低 | `____` h | Club IT |
| P4 low P4 | minor drift 小漂 | next biz 次工 | weekly review |

> **Rule / 规则**: P1/P2 always bypass quiet-hours (§3.2); P3/P4 respect it.
> 规则：P1/P2 恒破静默（§3.2）；P3/P4 守之。

### 3.10 Backup evidence log / 备份证据日志

| Club / 店 | Last good backup 末次好备 | Verified by 核人 |
|---|---|---|
| `____` | `____` | `____` |
| `____` | `____` | `____` |

> **Rule / 规则**: A backup not verified is not a backup — log proof weekly.
> 规则：未核之备非备——周记证据。

## ④ Common mistakes / 常见错误

1. No heartbeat → blind to gate-down. / 无心跳→门禁掉不知。→ §3.1
2. Alerting all night, no quiet-hours. / 全天告警无静默。→ §3.2
3. Full CCTV view of franchisee. / 看加盟商全监控。→ §3.4 (`tools/05`)
4. Wrong tier tool for size. / 规模错配工具。→ §3.5
5. Alerts with no runbook. / 告警无 runbook。→ §3.6
6. No repeat-fault trend → chronic red club. / 无重复故障趋势→慢性红店。→ §3.3

---

## ⑤ Related files / 相关文件

- `data/10-hardware-fault-tree-library.md` — hardware runbooks / 硬件 runbook
- `data/11-network-fault-tree-library.md` — network runbooks / 网络 runbook
- `data/12-software-fault-tree-library.md` — software runbooks / 软件 runbook
- `templates/42-franchise-digital-kit.md` — visibility boundary / 可见边界
- `tools/05-regulation-traceability-verification.md` — franchise privacy verify / 加盟隐私核验

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (signal spec + tooling tiers + runbook wiring), **Operator** (alert routing + weekly review + MTTR discipline), and **Member** (a club that is actually open and working when they arrive, because gate/POS/backup failures are caught before they complain); the franchise visibility split respects privacy while keeping uptime accountability.
本模板覆盖**架构师**（信号规格+工具分层+runbook 接线）、**运营者**（告警路由+周复盘+MTTR 纪律）、**会员**（到店时门店真开着真能用，因门禁/POS/备份故障在投诉前被发现）；加盟可见分界守隐私又保开机问责。
