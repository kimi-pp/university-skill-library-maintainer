# 12 · Access Control & Gate Specification / 门禁与闸机规格模板

> **Cluster / 集群**: C (Hardware C2) + B (Access software) · Template / 模板 · System-Building tier (FDMM L2)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Fire-code & biometric rules re-verify every 90 days via `tools/05`; gate fail-mode regulations are market-specific.
> **Cross-references / 交叉引用**: `references/07-hardware-landscape-and-vendors.md` (C2 gates) · `references/02-club-formats-and-zones.md#zone-gate` · `data/21-anti-pattern-library.md#ap-005-face-entry-no-alt` · `data/21#ap-007-fire-system-it-control` · `tools/05-regulation-traceability-verification.md` · `templates/09-mms-selection-scorecard.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/05` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/05` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用（FDMM 闸门）

**Purpose / 用途**: A specification to size, select and accept access gates and the access-control logic that decides who may enter.
**用途 / 中文**：用于闸机选型、 sizing 与验收，以及决定「谁能进」的门禁逻辑规格。

**When to use / 适用场景**:
- You need QR / band / face entry or plan 24h unmanned — L2. / 需二维码/手环/人脸入场或上 24h 无人——L2。
- Renovation is being planned (cabling must precede build). / 正在规划装修（布线须先于施工）。
- **HI-4 gate / 闸门**: Fire-safety integration is monitor-only; never let business systems control fire-safety devices. / 消防联动只联不控，业务系统不得控制消防设备。
- **HI-1 gate / 闸门**: Face / biometric entry MUST cite the target market's legal basis and offer a non-biometric alternative. / 人脸/生物识别入场必须带目标市场合规依据并提供非生物识别替代。

---

## ② Prerequisites checklist / 前置清单

- [ ] MMS chosen with real-time status sync (`templates/09`). / 已选支持实时同步的 MMS。
- [ ] Zone plan & gate location from `references/02#zone-gate`. / 区域图与闸位取自 `references/02#zone-gate`。
- [ ] Fire code for gate fail-mode confirmed via `tools/05` (fail-open usual). / 闸机断电策略消防条款经 `tools/05` 确认（多断电开）。
- [ ] Network VLAN for access-IoT planned (`references/08`). / 门禁 IoT 的 VLAN 已规划。
- [ ] If face: legal basis + DPIA drafted (HI-1) and non-biometric alternative designed. / 用人脸：合规依据+DPIA 已拟（HI-1），非生物替代已设计。
- [ ] Tailgating control approach (IR + CCTV review) decided. / 防尾随方案（红外+监控复核）已定。

---

## ③ The template / 模板正文

### 3.1 Lane sizing worksheet (peak throughput math) / 闸道数测算表（高峰吞吐）

> **Formula / 公式**: lanes needed = ceil( peak_arrivals_per_min × avg_pass_seconds ÷ 60 ÷ target_utilisation ). / 所需闸数 = 上限取整（每分钟高峰到场数 × 平均通行秒 ÷ 60 ÷ 目标利用率）。
> **What good looks like / 合格标准**: peak queue wait < 30s at 70% lane utilisation. / 高峰排队 <30 秒且闸道利用率 70%。
> **Red flag / 红旗**: sizing on average traffic → morning peak becomes a 10-minute jam. / 按平均流量测算 → 早高峰堵 10 分钟。

| Input / 输入 | Value / 值 | Unit / 单位 |
|---|---|---|
| Peak arrival rate / 高峰到场率 | ____ | members/min |
| Avg pass time / 平均通行时间 | ____ | seconds (QR ~2s, band ~1.5s, face ~3s) |
| Target utilisation / 目标利用率 | 0.70 | ratio |
| Computed lanes / 测算闸数 | =ceil(...) | lanes |
| Add 1 spare lane / 加 1 备用闸 | +1 | lane |

### 3.2 Credential matrix (QR / RFID / face) / 凭证矩阵

> **Face rule (HI-1) / 人脸规则**: If face is used, a NON-biometric alternative (QR or RFID band) MUST be offered and documented as the fallback for any member who opts out. / 用人脸则必须提供非生物替代（二维码或 RFID 手环）并记录为退出者的兜底。

| Credential / 凭证 | Speed / 速度 | Cost / 成本 | Privacy / 隐私 | Fallback? / 兜底 |
|---|---|---|---|---|
| QR (app) / 二维码 | ~2s | Low | Low | Primary / 主用 |
| RFID band / 手环 | ~1.5s | Mid | Mid (HI-8 min) | Primary / 主用 |
| Face / 人脸 | ~3s | High | High (HI-1) | Opt-in only + alt / 仅 Opt-in+替代 |

> **Compliance section (HI-1, MANDATORY if face) / 合规段（HI-1，用人脸必填）**:
- [ ] Legal basis cited: `[law + version + article]` per market, retrieved date ____. / 合规依据：各市场 `[法规+版本+条款]`，检索日____。
- [ ] Template stored local-first where market demands (HI-9). / 生物模板按市场要求本地优先（HI-9）。
- [ ] Non-biometric alternative offered to every member by default. / 默认向每位会员提供非生物替代。
- [ ] No face capture in changing rooms / showers (HI-5). / 更衣室/淋浴区无人脸采集（HI-5）。
- [ ] Retention & deletion schedule linked to `tools/05`. / 留存与删除计划关联 `tools/05`。

:::dynamic-hook topic="apac-gate-fail-mode-regulation-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07 most APAC fire codes require gates fail-open on power loss for egress; biometric entry (face) needs a market legal basis + non-biometric alternative. Verify exact clause per market via tools/05.
截至 2026-07 多数亚太消防法规要求断电开闸疏散；人脸入场需市场合规依据+非生物替代。具体条款经 tools/05 核验。
:::

### 3.3 Offline-mode requirements / 离线模式要求

- [ ] Gate caches valid credentials for ≥24h without MMS. / 闸机缓存有效凭证 ≥24h 不依赖 MMS。
- [ ] On reconnect, event log syncs with idempotency key. / 重连后事件日志带幂等键同步。
- [ ] Fail policy explicit: fail-open (egress) vs fail-closed (paid zone) per fire code. / 断电策略明确：依消防定开/关。
- [ ] Local audit log on controller, not only cloud. / 控制器本地审计日志，非仅云。

### 3.4 Fire-linkage clause (monitor-only, HI-4) / 消防联动条款（只联不控，HI-4）

> **Hard rule / 铁律**: The access system may RECEIVE a fire alarm signal to unlock gates for egress, but MUST NOT send any command that controls fire-safety devices (suppression, dampers, alarms). / 门禁可「接收」消防信号以开闸疏散，但绝不可「下发」控制消防设备（灭火、风阀、报警）的指令。

- [ ] Integration type: **monitor-only / 只监不控**. / 集成类型：只监不控。
- [ ] Gate unlocks on fire signal; suppression system independent. / 消防信号触发开闸；灭火系统独立。
- [ ] No shared controller with fire panel; signal is one-way read. / 不与消防盘共用控制器；信号单向读取。
- [ ] Documented in commissioning pack; signed by fire-safety officer. / 写入验收包并由消防安全员签字。

> **Red flag / 红旗**: `data/21#ap-007-fire-system-it-control` — IT integrations controlling the fire system is a life-safety violation. / IT 联动控消防是人身安全违规（见锚点）。

### 3.5 Installation acceptance checklist / 安装验收清单

- [ ] Gate aligned, no forced gap > tailgate threshold. / 闸机对齐，强制间隙小于防尾随阈值。
- [ ] Pass-time measured at peak (QR/band/face). / 高峰实测通行时间。
- [ ] Fail-mode tested (cut power → correct open/closed). / 断电策略实测。
- [ ] Offline cache tested (MMS down 1h → still opens). / 离线缓存实测。
- [ ] Event log export tested to MMS. / 事件日志导出至 MMS 实测。
- [ ] Fire-signal unlock tested, suppression untouched. / 消防信号开闸实测，灭火未动。

### 3.6 Integration test cases with MMS / 与 MMS 集成测试用例

| # | Test / 测试 | Expected / 预期 |
|---|---|---|
| 1 | New member → gate accepts within 1 min | Sync < 60s / 同步 <60秒 |
| 2 | Frozen member → gate rejects | Immediate / 即时 |
| 3 | Expired member → gate rejects | Immediate / 即时 |
| 4 | Band lost → reissue → old band dead | Old credential revoked / 旧凭证失效 |
| 5 | MMS down → cached entry works | Offline pass OK / 离线可过 |
| 6 | Fire signal → gates open, no control sent | Monitor-only / 只监不控 |

---

### 3.7 Worked lane-sizing example / 闸数测算实例

- Peak arrival / 高峰到场: 60 members in 15 min → 4/min. / 15 分钟到 60 人 → 4/分。
- Pass time (band) / 通行(手环): 1.5s. / 1.5 秒。
- Lanes / 闸数 = ceil(4 × 1.5 ÷ 60 ÷ 0.70) = ceil(0.143) = 1 → +1 spare = 2 lanes. / = 上限取整(…) = 1 → +1 备用 = 2 闸。
- Check / 复核: 2 lanes @1.5s handle 80/min; at 4/min peak queue wait < 30s. / 2 闸可处理 80/分；4/分高峰排队 <30 秒。
- If face only / 若仅人脸: pass 3s → still 2 lanes, but add non-bio alternative (HI-1). / 若仅人脸 3 秒→仍 2 闸，但须加非生物替代。

### 3.8 Commissioning sign-off / 验收签字清单

- [ ] Lane count matches §3.7 worksheet (peak queue < 30s observed). / 闸数符合 §3.7 测算（实测高峰排队<30 秒）。
- [ ] Credential matrix agreed; if face, HI-1 section fully filled + alternative offered. / 凭证矩阵已定；用人脸则 HI-1 段填全且提供替代。
- [ ] Offline cache survived 1h MMS outage in test. / 离线缓存经 1 小时 MMS 断网测试。
- [ ] Fire-signal unlock tested; suppression confirmed untouchable (HI-4). / 消防信号开闸已测；灭火确认未触动（HI-4）。
- [ ] Integration test cases §3.6 all PASS, signed by installer + club IT. / §3.6 集成用例全 PASS，安装方与场馆 IT 签字。
- [ ] Event-log export to MMS verified by Finance/Ops. / 事件日志导出至 MMS 经运营/财务核验。

### 3.9 Credential quick-pick / 凭证速选

| If club is… / 若场馆为… | Best primary / 最佳主用 | Why / 原因 |
|---|---|---|
| L1 small, low budget | QR (app) | Zero hardware, MMS-backed / 零硬件，MMS 支撑 |
| L2 mid, 24h unmanned | RFID band | Fast, durable, offline cache / 快、耐、离线缓存 |
| L2+ with HI-1 basis | Band + optional face | Face only opt-in + alt / 人脸仅 Opt-in+替代 |

> **Rule / 规则**: never make face the ONLY path — `data/21#ap-030-face-only-gate`. / 绝不让人脸成唯一路径（见锚点）。

## ④ Common mistakes (anti-patterns) / 常见错误（反模式）

- `data/21#ap-005-face-entry-no-alt` — face entry with no non-biometric alternative. / 人脸入场无替代。
- `data/21#ap-030-face-only-gate` — gate that ONLY accepts face. / 只认人脸的闸机。
- `data/21#ap-007-fire-system-it-control` — IT controlling fire devices. / IT 控消防设备。
- `data/21#ap-002-no-data-export` — access-event log cannot be exported. / 门禁日志不可导出。

---

## ⑤ Related files / 相关文件

- `references/07-hardware-landscape-and-vendors.md` (C2). / 闸机硬件。
- `references/02-club-formats-and-zones.md#zone-gate`. / 闸机区触点。
- `references/12-biometrics-and-cctv.md` — biometric legal basis. / 生物识别合规依据。
- `templates/13-smart-locker-spec.md` — lockers often share the credential. / 柜常共用凭证。

---

## ⑥ G13 tri-perspective note / G13 三视角覆盖说明

This template serves **Architect** (sizing math + integration tests + HI-4 clause), **Operator** (acceptance checklist + offline runbook), and **Member** (fast fair entry, privacy choice via non-biometric alternative, safe egress on fire); the HI-1 alternative and HI-4 monitor-only clauses keep the member's privacy and life-safety non-negotiable — no orphaned touchpoint.
本模板覆盖**架构师**（测算+集成测试+HI-4 条款）、**运营者**（验收清单+离线手册）、**会员**（快速公平入场、隐私选择权、消防安全带撤离）；HI-1 替代与 HI-4 只监不控是不可妥协的隐私与人身安全底线——无孤儿触点。
