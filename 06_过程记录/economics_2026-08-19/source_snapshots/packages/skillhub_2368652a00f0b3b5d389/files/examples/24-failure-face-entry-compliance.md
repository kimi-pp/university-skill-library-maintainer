# Failure Autopsy — Face-Entry Rollout Without a Legal Basis / 失败解剖——无法律依据的人脸入场上线

> **Cluster / 集群**: F (Compliance) · C (Hardware) · V (Meta)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Biometric law is volatile 🔄 — re-verify the target market's basis via `tools/05` before any rollout.
> **Cross-references / 交叉引用**: `data/21-anti-pattern-library.md` · `references/12-biometrics-and-cctv.md` · `tools/05-regulation-traceability-verification.md` · SKILL.md HI-1
> **Retrieval note / 检索提示**: Biometric rules are market-specific; no universal "yes". Run `tools/05` first.

---

## Honesty Preamble / 诚实序言

> Archetypal composite case for teaching, not a claimed real company or incident; numbers are directional. Biometric missteps are club-ending in strict markets — rehearse the compliance gate.
> 用于教学的原型复合案例，非真实公司或事件；数字方向性。生物识别失误在严监管市场是关店级——请演练合规闸。

---

## ① The Setup / 事发前情

A boutique studio in a strict biometric market (FDMM L2→L3) wanted the "frictionless" wow factor. The owner said: "Just put face-gates at the door, members will love it." No legal-basis check, no alternative offered, consent bundled into the general T&Cs. The vendor demo looked magical, and the owner signed the PO the same afternoon.

一家位于严监管生物识别市场的精品工作室（FDMM L2→L3）想要"无感通行"的噱头。老板说：「门口直接上人脸闸机，会员肯定爱用。」没做法律依据核查、没给替代方案、同意埋进总条款。供应商 demo 看着像魔法，老板当天下午就签了采购单。

What the owner felt: "This is innovation; the old QR cards feel cheap." He confused a compliance question for an aesthetic one.

老板的感受：「这是创新；老扫码卡显得廉价。」他把合规问题错当成了审美问题。

---

## ② Timeline of Doom / 崩塌时间线

- **Week 0 / 第0周**: Decide face-only entry "because it looks high-tech." Red flag: no non-biometric fallback designed. / 决定"只用人脸"因为显科技感。红旗：没设计非生物识别兜底。
- **Week 1 / 第1周**: Bundle biometric consent inside general signup T&Cs (`AP-047`). Red flag: no standalone opt-in. / 把生物识别同意埋进注册总条款（`AP-047`）。红旗：无独立 opt-in。
- **Week 2 / 第2周**: Go live. A member with a medical mask is hard-blocked at the queue; public argument. / 上线。戴口罩会员在队前被硬拦；当众争执。
- **Week 3 / 第3周**: A child member fails face-match (growth) and is locked out in front of parents. / 一名儿童会员人脸识别失败（长开了）在父母面前被拦。
- **Week 4 / 第4周**: A privacy-minded member files a regulator complaint: no legal basis, no alternative, invalid consent. / 一位注重隐私的会员向监管投诉：无依据、无替代、同意无效。
- **Week 6 / 第6周**: Regulator orders removal of face-processing + a penalties exposure; local press picks it up. / 监管责令拆除人脸处理 + 面临罚款；本地媒体跟进。

---

## ③ The Blow-Up / 爆雷后果（方向性区间）

| Dimension / 维度 | Directional range / 方向性区间 |
|---|---|
| Removal + re-fit / 拆除改回 | Tens of thousands (¥) to re-fit QR/RFID / 数万（¥）改回扫码/RFID |
| Penalty exposure / 罚款暴露 | Regulatory fine (¥-range), market-specific / 监管罚款（区间），因市场而异 |
| Members / 会员 | Privacy-sensitive slice churns; trust damaged / 重视隐私者部分流失；信任受损 |
| PR / 舆情 | "Club surveils members" narrative / "场馆监控会员"叙事 |

The owner's worst moment: explaining to the board why a "free" tech upgrade cost a five-figure removal and an open investigation.

老板最难的时刻：向董事会解释，一个"免费"的技术升级为何要花五位数拆除、还留下一桩在查案件。

---

## ④ Root-Cause Analysis / 根因分析

**5-Whys / 五问法**

| # | Why / 为何 | Answer / 答 |
|---|---|---|
| 1 | Why regulator action? / 为何被查？ | Face processing without legal basis / 无依据做人脸处理 |
| 2 | Why no basis? / 为何无依据？ | No `tools/05` check before rollout / 上线前没 `tools/05` 核查 |
| 3 | Why skipped? / 为何跳过？ | "Looks high-tech" impulse over compliance / "显科技感"冲动压过合规 |
| 4 | Why no alternative? / 为何无替代？ | Face designed as ONLY path / 人脸被设计成唯一通路 |
| 5 | Why only path? / 为何唯一？ | HI-1 + AP-005/030/047 all ignored / HI-1 与 AP-005/030/047 全被忽略 |

**Anti-patterns violated / 违反的反模式**: `#ap-005-face-entry-no-alt` · `#ap-030-face-only-gate` · `#ap-047-biometric-consent-bundled`.
**HI invariant / 硬不变量**: **HI-1** — biometric recommendations MUST cite the target market's legal basis. Violated.

---

## ⑤ The Counterfactual — Library-Guided Path / 反事实——按本库走的路

| Step / 步 | Library action / 本库动作 | Anchor / 锚点 |
|---|---|---|
| 1 | Legal-basis check (~10 min) before purchase / 采购前法律依据核查（约10分钟） | `tools/05` |
| 2 | Confirm explicit opt-in + alt path required / 确认需独立 opt-in + 替代通路 | `references/12` |
| 3 | Deploy QR + RFID as guaranteed path; face convenience-only / 扫码+RFID 保底；人脸仅便民 | `data/21#md-092` |
| 4 | Standalone revocable biometric consent / 独立可撤销生物识别同意 | `data/21#ap-047` fix |
| 5 | Local-first template storage (minimization) / 模板本地优先（最小化） | HI-1 / HI-8 |

---

## ⑥ Early-Warning Checklist (10 signals) / 预警清单

1. Face is the ONLY entry method. / 人脸是唯一入场方式。
2. Biometric consent buried in general T&Cs. / 生物识别同意埋进总条款。
3. No `tools/05` legal-basis check before purchase. / 采购前未经 `tools/05` 法律依据核查。
4. No QR/RFID fallback device bought. / 没买扫码/RFID 兜底设备。
5. "Looks high-tech" was the main reason. / "显科技感"是主因。
6. Templates stored off-market / cross-border. / 模板出境存储。
7. No revocation path for members. / 会员无撤销路径。
8. Minors could be enrolled without guardian consent. / 未成年人可无监护人同意录入。
9. Camera FOV could sweep the street without signage. / 摄像头视角无标识扫到街道（`AP-046`）。
10. No DPIA / privacy assessment on file. / 无隐私影响评估存档。

> One-line takeaway / 一句话: Face is a convenience layer, never the only door.
> 人脸是便民层，绝不是唯一的门。

---

## ⑦ Related Files / 相关文件

`data/21-anti-pattern-library.md` (#ap-005, #ap-030, #ap-047) · `references/12-biometrics-and-cctv.md` · `tools/05` · SKILL.md HI-1, HI-8.

---

## ⑧ G13 Note / G13 注记

- **Architect / 架构师**: face = convenience layer over a guaranteed non-biometric path (HI-1).
- **Operator / 运营者**: consent capture + revocation is a daily workflow, not a one-time checkbox.
- **Member / 会员**: dignified, choice-based entry; no one is locked out for refusing biometrics. No orphan touchpoint.
- **会员**：有尊严、可选择的入场；拒用人脸者不被拦。无孤儿触点。

> Honesty note / 诚实注记: Archetypal composite; cost/penalty figures are directional. Biometric law is market-specific — verify the exact basis via `tools/05` before any rollout.
> 原型复合；成本/罚款为方向性。生物识别法因市场而异——任何上线前经 `tools/05` 核验确切依据。
