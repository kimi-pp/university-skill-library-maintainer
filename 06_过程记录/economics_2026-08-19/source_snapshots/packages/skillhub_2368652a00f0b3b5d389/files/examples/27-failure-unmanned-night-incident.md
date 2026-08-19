# Failure Autopsy — The 02:40 Collapse in the Unmanned Club / 失败解剖——无人店 02:40 的昏倒

> **Cluster / 集群**: T (Physical Security) · J (Resilience) · F (Compliance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Life-safety law is non-negotiable 🔄 — re-verify via `tools/05`; review `playbooks/03` drills quarterly.
> **Cross-references / 交叉引用**: `data/21-anti-pattern-library.md` · `playbooks/03-24h-unmanned-club.md` · `references/16-security-operations-and-emergency.md` · SKILL.md HI-2, HI-4
> **Retrieval note / 检索提示**: Unmanned-club life-safety rules are market-specific — run `tools/05`.

---

## Honesty Preamble / 诚实序言

> Archetypal composite case for teaching, not a claimed real company or incident; numbers are directional. A life-safety failure is the one the library exists to prevent — rehearse the human-backup design.
> 用于教学的原型复合案例，非真实公司或事件；数字方向性。人身安全失败是本库最要防的——请演练人工兜底设计。

---

## ① The Setup / 事发前情

A 24h unmanned studio (FDMM L4/L5) with camera + sensor coverage "so we don't need night staff." The owner believed the AI camera system would catch any emergency. There was no human escalation path — only an app alert that went to a sleeping on-call phone. The pitch to investors was "zero labor after 22:00."

一家 24h 无人工作室（FDMM L4/L5）靠摄像头 + 传感器"覆盖"，所以"晚上不用人"。老板相信 AI 摄像头系统能抓到任何意外。没有人工升级路径——只有一个会推到睡着了的值班手机的 App 告警。对投资人的卖点是"22:00 后零人力"。

What the owner felt: "Sensors are cheaper than a night guard, and the AI never sleeps." He forgot that the AI also never *acts*.

老板的感受：「传感器比夜班人便宜，而且 AI 不睡觉。」他忘了，AI 也从不*行动*。

---

## ② Timeline of Doom / 崩塌时间线

- **Design phase / 设计期**: "Cameras + AI = safe enough, cut night staff." Red flag: no human escalation path (HI-2). / "摄像头+AI 够安全，砍夜班人。"红旗：无人工升级路径（HI-2）。
- **Week 1 / 第1周**: App alert wired to one on-call phone, no fallback if unanswered. / App 告警接一部值班手机，无人接无兜底。
- **02:40 (incident) / 事发**: A member collapses from a cardiac event. Camera "sees" it but the on-call phone is on silent. / 一位会员心脏事件昏倒。摄像头"看到"了，但值班手机静音。
- **02:55**: No human has reacted; a passer-by member finds him 15 min later. / 无人反应；15 分钟后另一名会员路过才发现。
- **03:10**: EMS called; response delayed; injury worsened vs a 2-min response. / 叫急救；响应延迟；相比 2 分钟响应伤情加重。
- **Week 2 / 第2周**: Investigation: no mandated human oversight → license/legal consequence. / 调查：无法定人工监管 → 执照/法律后果。

---

## ③ The Blow-Up / 爆雷后果（方向性区间）

| Dimension / 维度 | Directional range / 方向性区间 |
|---|---|
| Human / 人身 | Injury worsened by delay — incalculable / 因延迟加重——不可计价 |
| Legal / 法律 | License review / penalty; liability (¥-range) / 执照审查/罚款；责任（区间） |
| Money / 资金 | Liability + remediation + possible closure / 责任 + 整改 + 可能关停 |
| Brand / 品牌 | "Unmanned club left member unaided" / "无人店置会员于不顾" |

The human cost is the entire point: a preventable 15-minute gap turned a survivable event into a worsened one. No money figure can sit next to it.

人身代价就是全部重点：一个可避免的 15 分钟缺口，把可生还的事件变成了加重的伤情。没有任何金额能与之并列。

---

## ④ Root-Cause Analysis / 根因分析

**5-Whys / 五问法**

| # | Why / 为何 | Answer / 答 |
|---|---|---|
| 1 | Why worsened? / 为何加重？ | 15-min response delay / 15 分钟响应延迟 |
| 2 | Why delay? / 为何延迟？ | Alert went to silent phone, no human / 告警到静音手机，无人 |
| 3 | Why no human? / 为何无人？ | No escalation path by design / 设计上无升级路径 |
| 4 | Why no path? / 为何无路径？ | Believed sensors replace oversight / 误信传感器能替代监管 |
| 5 | Why believed? / 为何误信？ | HI-2 (human redundancy) violated / 违反 HI-2（人工冗余） |

**Anti-patterns violated / 违反的反模式**: `#ap-012-sensor-over-lifeguard` (spirit: tech over human) · `#ap-040-ekyc-no-fallback` (spirit: no human fallback) · `#ap-054-pool-open-no-lifeguard` (spirit: unattended risk). 
**HI invariant / 硬不变量**: **HI-2** — lone-exerciser / life-safety systems MUST keep human oversight redundancy. Violated. **HI-4** adjacent: exits must stay fail-open.

---

## ⑤ The Counterfactual — Library-Guided Path / 反事实——按本库走的路

| Step / 步 | Library action / 本库动作 | Anchor / 锚点 |
|---|---|---|
| 1 | Design HUMAN-BACKUP: monitored panic button + 24/7 center / 设计人工兜底：受监控呼救钮 + 7×24 中心 | `playbooks/03` |
| 2 | Monthly panic-button escalation drill / 月度呼救钮升级演练 | `playbooks/03` |
| 3 | AI = secondary alarm only; human decides / AI 仅次级告警；人决定 | HI-2 |
| 4 | Fail-safe exits always open; fire monitor-only / 故障安全出口常开；消防只监不控 | HI-4 |
| 5 | `tools/05` life-safety + license scan pre-unmanned / 无人运营前 `tools/05` 查人身安全+执照 | `tools/05` |

---

## ⑥ Early-Warning Checklist (10 signals) / 预警清单

1. "Sensors replace night staff" was the rationale. / 理由是"传感器替代夜班人"。
2. No human escalation path, only an app alert. / 无人工升级路径，只有 App 告警。
3. On-call phone can be silenced/unanswered. / 值班手机可静音/无人接。
4. No panic button with live monitoring. / 无带实时监控的呼救按钮。
5. No monthly escalation drill. / 无月度升级演练。
6. AI treated as the responder, not an alarm. / AI 被当响应者而非告警。
7. Exits not verified fail-open. / 出口未确认故障常开。
8. No `tools/05` life-safety scan. / 未经 `tools/05` 人身安全扫描。
9. Single point of failure on the alert path. / 告警路径单点故障。
10. Lone exerciser unprotected by design. / 独自锻炼者设计上无保护。

> One-line takeaway / 一句话: Unmanned never means unmonitored; a person must always be reachable.
> 无人绝不等于无人管；必须永远能找到人。

---

## ⑦ Related Files / 相关文件

`data/21-anti-pattern-library.md` (#ap-012, #ap-040, #ap-054) · `playbooks/03-24h-unmanned-club.md` · `references/16` §T/§S · SKILL.md HI-2, HI-4.

---

## ⑧ G13 Note / G13 注记

- **Architect / 架构师**: unmanned ≠ unmonitored; human backup is a design requirement (HI-2).
- **Operator / 运营者**: the panic-button drill is the difference between a near-miss and a tragedy.
- **Member / 会员**: a person, not a sensor target — they must always reach a human. No orphan touchpoint.
- **会员**：是人不是传感器目标——必须永远能找到人。无孤儿触点。

> Honesty note / 诚实注记: Archetypal composite; the human cost is directional/incalculable. Life-safety law is market-specific — verify via `tools/05` before unmanned operation.
> 原型复合；人身代价为方向性/不可计价。人身安全法因市场而异——无人运营前经 `tools/05` 核验。
