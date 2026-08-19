# 13 · Smart Locker System Specification / 智能储物柜系统规格模板

> **Cluster / 集群**: C (Hardware C3) · Template / 模板 · System-Building tier (FDMM L2)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Lock tech & wet-area IP ratings re-verify every 90 days via `tools/04`; biometric rules per `tools/05`.
> **Cross-references / 交叉引用**: `references/07-hardware-landscape-and-vendors.md` (C3 lockers) · `references/02-club-formats-and-zones.md#zone-locker` · `data/21-anti-pattern-library.md#ap-037-spare-key-ex-staff` · `data/21#ap-005-face-entry-no-alt` · `tools/05-regulation-traceability-verification.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用（FDMM 闸门）

**Purpose / 用途**: A specification to zone, count, lock-tech-select and accept smart lockers that replace rental keys.
**用途 / 中文**：用于分区、计数、选锁技术与验收智能储物柜，替代租赁钥匙。

**When to use / 适用场景**:
- You run a locker room and want to drop physical keys — L2. / 有更衣室且想淘汰实体钥匙——L2。
- Planning a new club where lockers share the member credential (band/QR). / 新店规划柜与会员凭证（手环/二维码）共用。
- **HI-5 gate / 闸门**: No imaging device in changing rooms / showers — ever. / 更衣室/淋浴区绝不放任何影像设备。
- **HI-8 gate / 闸门**: Do not collect more than needed; fingerprint lockers need a non-biometric fallback. / 不超需采集；指纹柜需非生物兜底。

---

## ② Prerequisites checklist / 前置清单

- [ ] Zone plan & locker count from `references/02#zone-locker`. / 区域图与柜数取自 `references/02#zone-locker`。
- [ ] Wet-area zones (pool/sauna) identified for IP rating. / 湿区（泳/桑拿）已标以便定 IP。
- [ ] Credential decision aligns with gate spec (`templates/12`). / 凭证决策与闸机规格一致。
- [ ] If fingerprint: legal basis (HI-1) + fallback (HI-8) planned. / 用指纹：合规依据（HI-1）+兜底（HI-8）。
- [ ] Master-key & forgot-code governance owner assigned. / 主密钥与忘码治理负责人已定。

---

## ③ The template / 模板正文

### 3.1 Zoning & count worksheet / 分区与计数表

> **Rule / 规则**: size lockers to peak simultaneous users, not member total. / 按高峰同时在场人数而非会员总数定柜数。
> **What good looks like / 合格标准**: locker:member ratio at peak ≥ 1:1.2 in wet zones, ≥1:3 in dry. / 湿区高峰柜:人 ≥1:1.2，干区 ≥1:3。
> **Red flag / 红旗**: too few wet-zone lockers → members leave bags on floor (slip hazard). / 湿区柜过少 → 会员把包放地上（滑倒隐患）。

| Zone / 区 | Peak users / 高峰人数 | Lockers needed / 需柜数 | IP rating / 防护 | Notes / 注 |
|---|---|---|---|---|
| Dry gym / 干区器械 | ____ | ____ | IP20 | Band/QR / 手环二维码 |
| Wet pool / 湿区泳 | ____ | ____ | IP65+ | Waterproof / 防水 |
| Group class / 团课 | ____ | ____ | IP20 | Shared / 共用 |
| Staff / 员工 | ____ | ____ | IP20 | Separate / 分开 |

### 3.2 Lock tech comparison / 锁技术对比

| Tech / 技术 | How / 方式 | Cost / 成本 | Privacy flag / 隐私 | Fallback / 兜底 |
|---|---|---|---|---|
| RFID band / 手环 | Tap band | Low | Low (HI-8) | QR app / 二维码 |
| PIN code / 密码 | Keypad | Low | None | Receipt PIN / 小票码 |
| **Fingerprint / 指纹** | Biometric | Mid | **HI-1/8 flag** | **Must offer non-bio / 必须非生物替代** |
| App BLE / App 蓝牙 | Phone | Mid | Low | Band / 手环 |

> **Biometric flag / 生物识别红旗**: Fingerprint lockers are a biometric system — apply HI-1 (legal basis) and HI-8 (minimisation) and ALWAYS offer a non-biometric unlock for opt-outs. Avoid fingerprint in changing rooms where HI-5 sensitivity is high. / 指纹柜即生物识别系统——适用 HI-1（依据）与 HI-8（最小化），且必须为退出者提供非生物解锁；更衣室 HI-5 敏感区慎用。

:::dynamic-hook topic="apac-fingerprint-locker-regulation-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07 APAC markets treat fingerprint lockers as biometric systems; many require consent + local template storage + a non-biometric fallback. Verify via tools/05 before deploying fingerprint locks.
截至 2026-07 亚太将指纹柜视为生物识别系统；多市场要求同意+本地模板+非生物兜底。部署前经 tools/05 核验。
:::

### 3.3 Master-key & forgot-code governance SOP fields / 主密钥与忘码治理 SOP 字段

> **What good looks like / 合格标准**: every override is logged with who/why/timestamp; ex-staff keys revoked. / 每次超控记录谁/为何/时间；离职员工密钥已注销。
> **Red flag / 红旗**: `data/21#ap-037-spare-key-ex-staff` — spare keys in hands of ex-staff. / 离职员工手持备用钥匙（见锚点）。

| Field / 字段 | Required value / 必填值 |
|---|---|
| Master-key custodian / 主密钥保管人 | Named person + backup / 具名+替补 |
| Override log / 超控日志 | who / why / timestamp / who为何时间 |
| Forgot-code reset / 忘码重置 | Identity verify → reissue, old dead / 核验身份→重发旧失效 |
| Revocation on exit / 离职注销 | Same-day key/band kill / 当日杀密钥手环 |
| Audit cadence / 审计频率 | Monthly review / 月度复核 |

### 3.4 Wet-area IP rating requirements / 湿区防护等级要求

- [ ] Pool/sauna lockers rated **IP65 or higher** (water jet proof). / 泳/桑拿柜 **IP65 及以上**（防喷水）。
- [ ] Electronic controller elevated above splash line. / 电子控制器高于溅水线。
- [ ] Drainage & ventilation around bank to avoid mould. / 柜群周边排水通风防霉。
- [ ] No camera, no biometric imaging in the room (HI-5). / 室内无摄像头无生物影像（HI-5）。

### 3.5 Acceptance tests / 验收测试

| # | Test / 测试 | Expected / 预期 |
|---|---|---|
| 1 | Band taps → opens correct cell | No cross-open / 不错开 |
| 2 | Forgot-code → reset → old code dead | Old revoked / 旧码失效 |
| 3 | Controller down → manual override logged | Override logged / 超控留痕 |
| 4 | Wet zone hosed (sim) → no fault | IP65 holds / 防护达标 |
| 5 | Power loss → stored state retained | State kept / 状态保留 |
| 6 | Ex-staff band → rejected | Revoked / 已注销 |

---

### 3.6 Worked count example / 计数实例

- Wet zone peak / 湿区高峰: 40 users → lockers = ceil(40 × 1.2) = 48 cells (IP65+). / 40 人 → 48 格（IP65+）。
- Dry zone peak / 干区高峰: 120 users → lockers = ceil(120 ÷ 3) = 40 cells (IP20). / 120 人 → 40 格（IP20）。
- Staff / 员工: 10 → 12 cells separate. / 员工 10 人 → 12 格分开。
- Total / 合计: 100 cells across zones; size the controller for 20% growth headroom. / 合计 100 格；控制器预留 20% 增长余量。

### 3.7 Forgot-code runbook (micro-example) / 忘码处置手册（微例）

1. Member reports forgotten code at front desk. / 会员前台报忘码。
2. Desk verifies identity (photo + emergency contact on file). / 前台核验身份（照片+紧急联系人）。
3. Issue one-time override PIN; old code dead immediately. / 发一次性超控码；旧码即时失效。
4. Member sets new code; override logged with timestamp. / 会员设新码；超控带时间戳留痕。
5. If override misused → revoke custodian key, audit (HI-8). / 若超控被滥用 → 注销保管人密钥并审计。

### 3.8 Handover checklist / 移交清单

- [ ] Count matches §3.6 (wet IP65+, dry IP20, staff separate). / 数量符合 §3.6（湿区 IP65+、干区 IP20、员工分开）。
- [ ] Lock tech decided; fingerprint (if any) has PIN/band fallback (HI-8). / 锁技术已定；指纹（若有）有密码/手环兜底。
- [ ] Master-key custodian named + backup; override log format set. / 主密钥保管人具名+替补；超控日志格式定。
- [ ] Forgot-code runbook (§3.7) trained to front desk. / 忘码手册（§3.7）已训前台。
- [ ] Wet-area IP rating verified by hose test (§3.5 #4). / 湿区防护经喷水测试（§3.5 #4）。
- [ ] Assignment log exports to MMS (`data/21#ap-002`). / 分配日志可导出 MMS。
- [ ] No camera/biometric imaging in room (HI-5). / 室内无摄像头/生物影像（HI-5）。

### 3.9 SLA & spare-parts note / SLA 与备件注记

- [ ] Warranty length stated; on-site vs carry-in in writing. / 保修时长书面；上门或送修写明。
- [ ] Spare cell & controller stocked on site (one fault ≠ whole bank down). / 现场备格与控制器（一坏≠整组瘫）。
- [ ] Mean-time-to-repair target ≤ 24h for a jammed cell. / 卡格修复目标 ≤24h。
- [ ] Refurb resale value ~15%; steel body reusable. / 二手约 15%；钢体可复用。
- [ ] End-of-life: secure-wipe any controller that stored codes. / 退役：存码控制器先安全擦除。

### 3.10 Acceptance one-liner / 验收一句话

> **Pass criterion / 通过判据**: "Every cell opens for its owner, rejects others, survives a power cut, and every override is logged — with no camera in the room." / 「每格只开主人、拒他人、抗断电、超控留痕，且室内无摄像头」即为通过。

## ④ Common mistakes (anti-patterns) / 常见错误（反模式）

- `data/21#ap-037-spare-key-ex-staff` — spare keys held by former staff. / 离职员工持备用钥匙。
- `data/21#ap-005-face-entry-no-alt` — fingerprint lockers with no PIN/band fallback. / 指纹柜无密码/手环兜底。
- `data/21#ap-002-no-data-export` — locker assignment log cannot be exported to MMS. / 柜分配日志不可导出 MMS。

---

## ⑤ Related files / 相关文件

- `references/07-hardware-landscape-and-vendors.md` (C3). / 储物柜硬件。
- `references/02-club-formats-and-zones.md#zone-locker`. / 更衣室区触点。
- `templates/12-access-control-gate-spec.md` — shared credential. / 共用凭证。
- `tools/05-regulation-traceability-verification.md` — biometric basis if fingerprint. / 用指纹时的合规依据。

---

## ⑥ G13 tri-perspective note / G13 三视角覆盖说明

This template serves **Architect** (zoning math + lock-tech comparison + IP spec), **Operator** (governance SOP + acceptance tests), and **Member** (fast secure storage, privacy choice, no surveillance in changing rooms); the HI-5 no-imaging and HI-8 minimisation clauses protect the member's dignity and data — no orphaned touchpoint.
本模板覆盖**架构师**（分区测算+锁技术对比+防护规格）、**运营者**（治理 SOP+验收测试）、**会员**（快速安全储物、隐私选择、更衣室无监控）；HI-5 禁摄与 HI-8 最小化守护会员尊严与数据——无孤儿触点。
