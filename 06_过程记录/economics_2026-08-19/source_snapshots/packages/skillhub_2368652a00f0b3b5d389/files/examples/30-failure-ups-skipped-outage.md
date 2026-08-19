# Failure Autopsy — The ¥2k UPS That Wasn't Bought / 失败解剖——那台没买的 ¥2k UPS

> **Cluster / 集群**: D (Network & Server Room) · J (Resilience) · C (Hardware)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: UPS/gear specs volatile 🔄 — re-verify via `tools/04`; run `data/13` self-test routine quarterly.
> **Cross-references / 交叉引用**: `data/13-inspection-and-maintenance-calendar.md` · `data/21-anti-pattern-library.md` · `templates/18-server-room-checklist.md` · `references/08-network-and-infrastructure.md` · SKILL.md Iron Law 2
> **Retrieval note / 检索提示**: UPS sizing/pricing marked 🔄 — run `tools/04` before purchase.

---

## Honesty Preamble / 诚实序言

> Archetypal composite case for teaching, not a claimed real company or incident; numbers are directional. A skipped ¥2k line item can cost a full-day closure — rehearse the server-room checklist.
> 用于教学的原型复合案例，非真实公司或事件；数字方向性。砍掉 ¥2k 一项可能赔掉一整天停业——请演练机房清单。

---

## ① The Setup / 事发前情

A single club (FDMM L2) building its server room. The budget review cut the UPS line item: "power is reliable, we'll save ¥2k." The network rack, gate controller, NVR and POS database all ran straight off mains (`data/21#ap-010-skip-ups`).

单店（FDMM L2）在建机房。预算评审砍了 UPS 这项：「电够稳，省 2 千。」网络机柜、闸机控制器、NVR、POS 数据库全直连市电（`data/21#ap-010`）。

---

## ② Timeline of Doom / 崩塌时间线

- **Build / 建设期**: UPS line item cut to save ¥2k. Red flag: no battery backup on critical paths. / 为省 2 千砍 UPS。红旗：关键链路无电池后备。
- **Month 3 / 第3月**: No `data/13#ups-self-test` routine established. / 没建立 `data/13#ups-self-test` 自检。
- **Storm day / 暴风日**: Neighborhood outage during evening settlement. Red flag: NVR + POS mid-write when power died. / 晚间结算时片区停电。红旗：断电时 NVR + POS 正在写。
- **+0h / 当时**: Disk corruption: NVR footage unreadable, POS database inconsistent. / 磁盘损坏：NVR 录像不可读，POS 库不一致。
- **+1h / 1小时后**: Gate controller down (no UPS) — manual buzz-in for all members. / 闸机控制器断电（无 UPS）——全员手动放行。
- **+8h / 8小时后**: Full-day closure; data recovery vendor called. / 全天停业；叫数据恢复供应商。

---

## ③ The Blow-Up / 爆雷后果（方向性区间）

- **Money / 资金**: Data-recovery cost ¥-range (tens of thousands directional) + lost day revenue (¥-range) + UPS cost that was avoided (¥2k) now pointless. / 数据恢复费数万方向性 + 停业一天营收（区间）+ 当初省下的 UPS（2 千）毫无意义。
- **Data / 数据**: NVR footage lost (insurance/evidence gap) + POS DB partial corruption. / NVR 录像丢失（保险/证据缺口）+ POS 库部分损坏。
- **Insurance / 保险**: Claim denied for negligence — no UPS on critical systems (order-of-magnitude: full loss uninsured). Verify policy via `tools/04`. / 因疏忽被拒赔——关键系统无 UPS（量级：全损不赔）。保单经 `tools/04` 核验。
- **Members / 会员**: Day of closure + manual-check-in friction; trust dent. / 停业一天 + 手动签到摩擦；信任受损。

---

## ④ Root-Cause Analysis / 根因分析

**5-Whys / 五问法**

| # | Why / 为何 | Answer / 答 |
|---|---|---|
| 1 | Why data lost? / 为何丢数据？ | Power died mid-write, no battery / 写入中断电，无电池 |
| 2 | Why no battery? / 为何无电池？ | UPS line item cut / UPS 项被砍 |
| 3 | Why cut? / 为何砍？ | "Save ¥2k" in budget / 预算里"省 2 千" |
| 4 | Why no test? / 为何无测试？ | `data/13` self-test routine absent / 缺 `data/13` 自检流程 |
| 5 | Why no gate? / 为何无闸？ | `templates/18` + `data/21#ap-010` ignored / 忽略 `templates/18` + `data/21#ap-010` |

**Anti-patterns violated / 违反的反模式**: `#ap-010-skip-ups` (the named one) · `#ap-028-nvr-wifi-backhaul` (spirit: fragile single path for critical footage) · `#ap-021-backup-theater` (spirit: untested recovery).
**HI invariant / 硬不变量**: Iron Law 2 (fail-safe / resilience) strained; HI-4 adjacent (exits must fail-open regardless).

---

## ⑤ The Counterfactual — Library-Guided Path / 反事实——按本库走的路

1. `templates/18-server-room-checklist.md`: UPS sized for ≥ the longest realistic outage, on battery-backed outlets ONLY (network, gate controller, NVR, POS DB). / `templates/18`：UPS 按"最长合理断网"配，只接电池后备口（网络、闸机控制器、NVR、POS 库）。
2. `data/13-inspection-and-maintenance-calendar.md#ups-self-test`: quarterly self-test; replace battery on amber. / `data/13#ups-self-test`：季度自检；琥珀即换电池。
3. PoE wired backbone for cameras, not Wi-Fi-only (`data/21#md-124`, `AP-028` fix). / 摄像头用 PoE 有线主干，不只 Wi-Fi（`data/21#md-124`、`AP-028` 修正）。
4. Quarterly restore drill to sandbox (`data/21#md-021` spirit) — verify recovery before you need it. / 季度沙箱恢复演练（`data/21#md-021` 精神）——用前先验证能恢复。
5. `references/08-network-and-infrastructure.md`: fail-safe design; exits/gates fail-open on power loss. / `references/08`：故障安全设计；断电时出口/闸机故障常开。

---

## ⑥ Early-Warning Checklist (10 signals) / 预警清单

1. UPS line item cut to save cost. / 为省钱砍 UPS 项。
2. Critical systems on raw mains. / 关键系统直连市电。
3. No UPS self-test routine. / 无 UPS 自检流程。
4. Camera backhaul Wi-Fi-only. / 摄像头只走 Wi-Fi 回传。
5. Backups never restore-tested. / 备份从不恢复演练。
6. No generator for long outages. / 长停电无发电机。
7. Server closet unlocked / uncooled (`data/21#md-003`). / 机房未锁/未控温（`data/21#md-003`）。
8. Settlement runs during storm season unguarded. / 暴风季结算无人值守。
9. Insurance never asked about UPS requirement. / 从没问保险对 UPS 的要求。
10. No `templates/18` checklist in use. / 没在用 `templates/18` 清单。

---

## ⑦ Related Files / 相关文件

`data/13-inspection-and-maintenance-calendar.md` (#ups-self-test, #closing-checklist) · `data/21-anti-pattern-library.md` (#ap-010, #ap-028, #ap-021) · `templates/18-server-room-checklist.md` · `references/08-network-and-infrastructure.md` · SKILL.md Iron Law 2, HI-4.

---

## ⑧ G13 Note / G13 注记

- **Architect / 架构师**: UPS + fail-open + wired backbone are resilience design requirements (Iron Law 2).
- **Operator / 运营者**: the quarterly self-test is what prevents a ¥2k skip from becoming a full-day loss.
- **Member / 会员**: a club that stays open and keeps their data is the baseline promise. No orphan touchpoint.
- **会员**：能开门、数据不丢是底线承诺。无孤儿触点。

> Honesty note / 诚实注记: Archetypal composite; cost figures directional. UPS specs/pricing and insurance terms are volatile — verify via `tools/04` before purchase and `tools/05` for any compliance angle.
> 原型复合；成本为方向性。UPS 规格/价格与保险条款易变——购买前经 `tools/04` 核验、合规面经 `tools/05` 核验。
