# New Club Pre-Opening IT Gantt / 新店筹建 IT 甘特图

> **Cluster / 集群**: G (Lifecycle G1)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: ISP/3-phase/power lead times re-verify every 90 days via `tools/04`; alignment to `references/15#g1-preopening`.
> **Cross-references / 交叉引用**: `references/15` (G1), `references/08` (network), `data/15` (cost), `data/21` (anti-patterns), `templates/17`, `templates/18`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this Gantt to sequence the **entire pre-opening IT program** so nothing is discovered the week of soft launch. It is the spine of `references/15#g1-preopening`.
本甘特图用于编排**筹建期全部 IT 工作**，避免软开业前一周才发现漏项。它是 `references/15#g1-preopening` 的主干。

- **FDMM gate / 等级闸门**: L1 (every new club). The long-lead logic applies regardless of level — ISP and gates are always long-lead.
  L1（每新店）。长交期逻辑与等级无关——ISP 与闸机永远长交期。
- **Trigger / 触发**: signed lease, or "we open in 12 weeks, is IT ready?".
  已签租约，或"12 周后开业，IT 就绪没"。

---

## ② Prerequisites checklist / 前置清单

- [ ] Lease signed; power capacity & three-phase confirmed (`references/15#g1-site-survey`). / 已签租约；电力与三相已确认。
- [ ] Floor plan + zone map locked. / 平面图与分区图已定。
- [ ] Budget ranges from `data/15` confirmed. / 预算区间（`data/15`）已确认。
- [ ] Long-lead items identified (§3.3). / 长交期项已识别（§3.3）。
- [ ] Opening date fixed (anchor T-0). / 开业日已定（锚定 T-0）。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Gantt table / 甘特表

Columns = weeks relative to opening: T-12w → T-10 → T-8 → T-6 → T-4 → T-2 → T-0 (soft launch) → T+2w.
列=相对开业周：T-12w → T-10 → T-8 → T-6 → T-4 → T-2 → T-0(软开业) → T+2w。

| Workstream / 工作流 | T-12 | T-10 | T-8 | T-6 | T-4 | T-2 | T-0 | T+2 |
|---|---|---|---|---|---|---|---|---|
| **ISP order (LONG LEAD)** 运营商下单（长交期） | ████ | ██ | | | | | | |
| Power & 3-phase upgrade 电力/三相增容 | ████ | ██ | | | | | | |
| **Cabling before renovation** 装修前布线 | | ████ | ██ | | | | | |
| Low-voltage design sign-off 弱电设计签核 | | ██ | | | | | | |
| Hardware delivery (gates, APs, server) 硬件到货 | | | ████ | ██ | | | | |
| Rack & server room build 机柜机房建设 | | | | ████ | ██ | | | |
| Network provisioning 网络开通 | | | | ██ | ████ | | | |
| Systems provisioning (CRM/POS/gate) 系统开通 | | | | | ████ | ██ | | |
| CCTV + signage 监控与标牌 | | | | | ██ | ████ | | |
| Staff training 员工培训 | | | | | | ████ | ██ | |
| **Soft-launch load test** 软开业压测 | | | | | | | ████ | ██ |
| Outage drill 断网演练 | | | | | | | ██ | |
| Go-live + stabilize 上线与稳定 | | | | | | | | ████ |

> **Fill rule / 填写规则**: Copy the bar lengths to your real calendar. ISP + power MUST start at T-12 (longest lead). Cabling MUST finish before renovation partitions (`data/21#ap-003-cabling-after-renovation`).
> 把条形长度套到真实日历。ISP+电力必须从 T-12 起（交期最长）。布线必须在隔墙前完。

### 3.2 Dependency map / 依赖关系

- ISP & power (T-12) → network provisioning (T-6). / 运营商与电力 → 网络开通。
- Cabling (T-8) → rack build (T-6) → network (T-6). / 布线 → 机房建设 → 网络。
- Hardware delivery (T-8) → systems provisioning (T-4). / 硬件到货 → 系统开通。
- Systems provisioning → staff training → soft-launch test. / 系统开通 → 培训 → 软开业压测。
- Soft-launch load test gates go-live (T-0). / 软开业压测是上线闸门。

### 3.3 Long-lead-item warning list / 长交期预警清单

> **Rule / 规则**: Order these FIRST or your opening slips. Lead times 🔄 — confirm per market via `tools/04`.
> 这些**最先订**，否则开业延期。交期 🔄——按市场经 `tools/04` 确认。

| Item / 项 | Typical lead / 典型交期 | Risk if late / 延误风险 |
|---|---|---|
| ISP fiber install 光纤安装 | 4–12 wks 🔄 | no internet at open 开业无网 |
| 3-phase upgrade 三相增容 | 2–16 wks 🔄 | HVAC/IT underpowered 电力不足 |
| Gates & turnstiles 闸机 | 4–10 wks 🔄 | no entry control 无入场管控 |
| Servers / NVR 服务器/NVR | 2–6 wks 🔄 | no system at open 开业无系统 |
| Specialty sensors 专用传感 | 3–8 wks 🔄 | missing safety link 缺安全联动 |

### 3.4 Go-live readiness gate checklist / 上线就绪闸门清单

Linked to `references/15#g1-preopening`. All must be ✓ before T-0.
对接 `references/15#g1-preopening`。T-0 前须全 ✓。

- [ ] Dual ISP up + failover tested (<60 s). / 双 ISP 起+切换测过（<60s）。
- [ ] Network built & accepted (`templates/17` §3.5). / 网络建成验收过。
- [ ] Server room built & cooled (`templates/18`). / 机房建成散热好。
- [ ] CRM/POS/gate synced end-to-end; test card opens. / 会籍/POS/闸机端到端通；测试卡可开。
- [ ] CCTV recording + signage + retention set (HI-5). / 监控录制+标识+留存设好（HI-5）。
- [ ] Backups 3-2-1 verified. / 备份 3-2-1 已验。
- [ ] Staff trained; outage drill passed. / 员工已训；断网演练过。
- [ ] Soft-launch load test passed (gate throughput, Wi-Fi, POS concurrency). / 软开业压测过（闸机吞吐、Wi-Fi、POS 并发）。

> **Stop-line / 停手线**: If the readiness gate is not fully ✓, do NOT open. A promo with untrained staff on a half-built system is a disaster (`data/21#ap-023-untrained-system-promo`).
> 就绪闸门未全 ✓，绝不开业。半成品系统+未训员工+大促=灾难。

---

## ④ Common mistakes / 常见错误

1. Cabling after renovation → 10× cost & slip. / 装修后布线→10 倍成本且延期。→ `data/21#ap-003-cabling-after-renovation`
2. ISP ordered at T-4 → no internet at open. / T-4 才订运营商→开业无网。
3. Migrating data during peak opening. / 开业高峰做数据迁移。→ `data/21#ap-013-migrate-peak`
4. Promo before staff trained. / 员工未训就大促。→ `data/21#ap-023-untrained-system-promo`
5. Skipping soft-launch load test. / 跳过软开业压测。

---

## ⑤ Related files / 相关文件

- `references/15-lifecycle-scenarios.md#g1-preopening` — full G1 narrative / G1 全流程
- `templates/17-network-build-and-acceptance.md` — network spec / 网络规格
- `templates/18-server-room-checklist.md` — closet / 机房
- `data/15-procurement-and-cost-benchmark.md` — cost ranges / 成本区间
- `references/08-network-and-infrastructure.md` — D1–D8 basis / 设计依据

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (dependency map + long-lead logic), **Operator** (Gantt bars + readiness gate + training window), and **Member** (smooth soft-launch, no "system down on day one", always-open gates via tested failover); each mistake links to `data/21` anchors for prevention.
本模板覆盖**架构师**（依赖图+长交期逻辑）、**运营者**（甘特条+就绪闸门+培训窗口）、**会员**（软开业顺畅、不开业即瘫、双线保闸机常开）；每条错误链 `data/21` 锚点可预防。
