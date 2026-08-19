# Ticket & Repair Form / 工单与维修表单

> **Cluster / 集群**: I (IT governance & money) + D (Network) + C (Hardware)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify SLA norms and labor rates every 90 days via `tools/04`/`tools/05`; market politeness norms shift — verify via `tools/04`.
> **Cross-references / 交叉引用**: `data/14-repair-scripts-and-sla-library.md` · `data/13-inspection-and-maintenance-calendar.md` · `data/21-anti-pattern-library.md` · `references/16-security-operations-and-emergency.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: The single form every repair call and every internal ticket lives on. Pair it with `data/14` call scripts so you always get a **ticket number + a started SLA clock**. Use it the moment any device fails — gate, POS, network, camera, treadmill.
**中文**：每次报修电话与每次内部工单都用这一张表。配合 `data/14` 话术，确保你永远拿到**工单号 + 已启动的 SLA 计时**。任何设备坏了——闸机、POS、网络、摄像头、跑步机——立即用。

> 💡 One rule beats a long training: **describe the symptom, never the diagnosis.** "The gate won't open for valid members" — not "your controller is broken." Vendors fix faster when you hand them evidence, not blame.
> 💡 一条规矩胜过长篇培训：**说症状，不说诊断。**「有效会员闸机不开」——别说「你控制器坏了」。你给证据而非甩锅，厂商修得更快。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Why / 为何 |
|---|---|---|
| 1 | Asset register row / 资产台账行 | grab the Asset ID + vendor hotline / 取资产编号+厂商热线 |
| 2 | Evidence ready / 证据备齐 | photo / error code / serial (see below) / 照片/错误码/序列号 |
| 3 | Severity decided / 定好等级 | use the matrix below / 用下方矩阵 |
| 4 | `data/14` open on screen / 打开 `data/14` | for the verbatim call script / 照念话术 |

---

## ③ THE TEMPLATE / 模板正文

### #severity-matrix Severity Matrix / 严重度矩阵

| Level / 等级 | Example / 示例 | Response target / 响应目标 🔄 | Resolution target / 解决目标 🔄 |
|---|---|---|---|
| **P1** revenue-stopping / 营收断流 | whole club offline at peak, POS dead, gate stuck with members inside / 高峰全店断、POS 死、闸机困人 | < 2h / <2小时 | < 4h / <4小时 |
| **P2** degraded / 降级 | one camera down, one SSID missing, one treadmill dead / 一摄黑、一名缺失、一台器械坏 | < 4h business / <4小时工作 | < 1 day / <1天 |
| **P3** minor / 轻微 | printer quality, slow report / 打印质量、报表慢 | < 1 day / <1天 | < 3 days / <3天 |
| **P4** cosmetic / 外观 | label typo, UI nit / 标签错、小UI | batch monthly / 并入月单 | best-effort / 尽力 |

> 🔄 Targets are directional templates — your signed SLA may differ; always write BOTH response AND resolution per level (trap: "response 4h" with no resolution promise, see `data/14`).
> 🔄 目标仅为方向模板——你签的 SLA 可能不同；每级都要写「响应+解决」二者（坑：「响应4h」却不承诺解决，见 `data/14`）。

### #symptom-prompts Symptom Description Prompts / 症状描述提示

Answer these, don't free-write a diagnosis:
逐条回答，别自由发挥下诊断：

- **What exactly happened? / 确切发生了什么？** e.g. "valid member tapped QR, gate showed red, no open." / 如「有效会员刷码，闸机红灯，不开」。
- **When did it start? / 何时开始？** exact time / 确切时间。
- **Who/what is affected? / 影响谁/什么？** N members / N devices / N 名会员/N 台。
- **What did you already try? / 你已试过？** reboot? screenshot? / 重启？截图？

### #evidence-checklist Evidence Checklist / 证据清单

| Category / 类别 | Evidence / 证据 |
|---|---|
| Network / 网络 | modem-light photo, speed test, exact start time / 光猫灯照片、测速、起始时间 |
| MMS SaaS | error screenshot, last-sync time, member ID, impact count / 报错截图、末同步、会员ID、影响数 |
| Equipment / 设备 | model + SN, symptom text, reboot proof, photo/video / 型号+序列号、症状原文、重启证明、照片 |
| Payment / 支付 | two txn IDs, amount, gateway status, time / 两笔交易号、金额、网关状态、时间 |
| CCTV / 监控 | channel id, black-screen time, NVR status / 通道号、黑屏时间、NVR状态 |

> Rule: **screenshot + timestamp + your account ID.** Without these three, the agent asks and the SLA clock waits.
> 规矩：**截图 + 时间戳 + 账号ID**。缺这三项，客服反问、计时就等。

### #ticket-form The Ticket Form (one copy per fault) / 工单表单（每故障一份）

```
Vendor / 厂商: ____________   Ticket # / 工单号: ____________
Opened / 开: <date time>   Asset ID / 资产号: ____________
Severity / 等级: P1□ P2□ P3□ P4□
Symptom (not diagnosis) / 症状(非诊断): ________________________
Evidence attached / 证据: photo□ log□ SN□  error-code: ______
SLA response / 响应时限: ____   SLA resolution / 解决时限: ____   Clock start / 起算: ____
Updates / 跟进: <time> <who> <what> | <time> <who> <what>
Breach? / 超SLA?: Yes□ No□   Credit claimed / 主张抵扣: ____   Resolved / 解决: <time>
Vendor ticket-number confirmed in writing? / 工单号书面确认?: Yes□ No□
```

### #resolution-log Resolution & Root-Cause Log / 解决与根因记录

| Field / 字段 | Fill / 填写 |
|---|---|
| Root cause / 根因 | what actually broke / 到底哪坏 |
| Fix applied / 处置 | reboot / replace / config / 重启/换/配置 |
| Recurring? / 反复? | yes → demand EOL/replace (see `data/14`) / 是→要求换或 EOL |
| Prevent again? / 预防 | patch / spare / training / 补丁/冷备/培训 |

### #monthly-trend Monthly Ticket-Trend Review Sheet / 月度工单趋势表

| Month / 月 | P1 | P2 | P3 | P4 | Breaches / 超SLA | Top vendor / 头号厂商 | Repeat fault / 反复坏 |
|---|---|---|---|---|---|---|---|
| ____ | __ | __ | __ | __ | __ | ________ | ________ |

> At renewal, this sheet is your negotiation leverage (see `templates/36-renewal-negotiation-prep.md` and `data/14` renewal section). A repeat fault on one device = replace, not repair.
> 续约时这表是你的谈判筹码（见 `templates/36`、`data/14` 续约节）。同设备反复坏 = 换而非修。

---

## ④ Common Mistakes / 常见错误

- **Diagnosis instead of symptom** → vendor blames "your environment", clock stalls. → `data/14` universal 5-step.
- **No ticket number captured** → no SLA, no credit, no track. → `data/21#ap-024` lineage.
- **Backup theater on repair** → "replaced, didn't check data". → `data/21#ap-021-backup-theater`.
- **Paying for repeat repairs** → repair ≥40% of replace & >3–5yr old ⇒ replace. → `data/14` warranty math.

---

## ⑤ Related Files / 相关文件

- `data/14-repair-scripts-and-sla-library.md` — verbatim scripts + SLA clause library. / 照念话术 + SLA 条款库。
- `data/13-inspection-and-maintenance-calendar.md` — when to run checks. / 何时跑检查。
- `references/16-security-operations-and-emergency.md` — incident & breach handling. / 事件与泄露处置。
- `templates/38-emergency-contact-card.md` — who-to-call ladder. / 呼叫阶梯。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: The form enforces the response-vs-resolution SLA discipline and feeds the contract exit/penalty clauses (HI-8) — every ticket is a data point for vendor governance.
**运营者 / Operator**: A fill-in-blank form + the `data/14` script means a front-desk rookie can open a disciplined ticket and protect the SLA clock without IT help.
**会员 / Member**: Faster, evidence-based repairs mean less downtime at the gate/POS/cameras; the written recap also protects member-data breach evidence (HI-1) when a vendor handles PII.
