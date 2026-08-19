# 14 · IoT Equipment Onboarding (Cardio / Strength / Sensors) / 物联网器械接入模板

> **Cluster / 集群**: C (Hardware C4/C5/C11) + E (Data) · Template / 模板 · System-Building tier (FDMM L2→L3)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Device protocols & gateway models re-verify every 90 days via `tools/04`; vendor-cloud lock-in terms are volatile.
> **Cross-references / 交叉引用**: `references/09-iot-and-open-protocols.md` (FTMS / ANT+ / gateway) · `references/07-hardware-landscape-and-vendors.md` (C4/C5/C11) · `references/08-network-and-infrastructure.md` (VLAN) · `data/21-anti-pattern-library.md#ap-002-no-data-export` · `data/21#ap-009-shared-admin-login`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用（FDMM 闸门）

**Purpose / 用途**: A repeatable playbook to connect cardio machines, smart strength equipment and floor sensors into the club's data layer (member 360 + BI).
**用途 / 中文**：可复用手册，把有氧器械、智能力量器械与地感传感器接入场馆数据层（会员 360 + BI）。

**When to use / 适用场景**:
- You bought FTMS/ANT+ capable cardio or smart strength — L2→L3. / 买了支持 FTMS/ANT+ 的有氧或智能器械——L2→L3。
- You want usage data to feed churn/Utilisation AI later. / 想让使用数据喂养未来的流失/利用率 AI。
- **FDMM gate / 闸门**: Do not onboard 20+ devices straight to the public internet with no gateway/VLAN — that is an anti-pattern (`references/09` → `data/21#ap-002` family). Use a gateway + VLAN. / 不得把 20+ 设备直连公网无网关/VLAN，那是反模式；用网关+VLAN。
- **HI-8 gate / 闸门**: Capture only what serves the stated purpose (usage, not surveillance video). / 仅采声明目的所需（用量，非监控视频）。

---

## ② Prerequisites checklist / 前置清单

- [ ] Network designed with IoT VLAN (`references/08`). / 已按 IoT VLAN 设计网络。
- [ ] Gateway architecture decided (`references/09` §Gateway). / 网关架构已定（`references/09`）。
- [ ] `references/09-iot-and-open-protocols.md` read for FTMS/ANT+. / 已读 `references/09` 的 FTMS/ANT+。
- [ ] MMS member-ID scheme ready to map device sessions. / MMS 会员 ID 方案就绪以映射器械会话。
- [ ] Default passwords list to be changed on day one. / 待首日修改的默认密码清单。

---

:::dynamic-hook topic="apac-iot-gateway-landscape-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07 FTMS/ANT+ support is widening but vendor-cloud lock-in persists; gateway + VLAN remains the safe default. Verify current device/protocol support via tools/04.
截至 2026-07 FTMS/ANT+ 支持面扩大但厂商云锁定仍在；网关+VLAN 仍是安全默认。当前支持经 tools/04 核验。
:::

## ③ The template / 模板正文

### 3.1 Inventory & capability audit sheet (per unit) / 逐台清点与能力审计表

> **Link / 关联**: Protocol detail in `references/09-iot-and-open-protocols.md` (FTMS §, ANT+ §). / 协议细节见 `references/09`。
> **What good looks like / 合格标准**: every unit has a known protocol; "vendor-cloud only, no export" units are flagged for negotiation or rejection. / 每台协议已知；"仅厂商云、无导出"的台子标红谈判或拒收。
> **Red flag / 红旗**: a console that only speaks its own app = lock-in risk (`data/21#ap-002-no-data-export`). / 只认自家 App 的控制台=锁定风险。

| Asset tag / 编号 | Type / 类型 | Protocol / 协议 | Vendor-cloud? / 厂商云? | Data export? / 可导出? | Gateway / 网关 |
|---|---|---|---|---|---|
| EQ-001 | Treadmill | FTMS / ANT+ | No | Yes (CSV/API) | BLE hub |
| EQ-002 | Bike | FTMS | No | Yes | BLE hub |
| EQ-010 | Smart strength | Vendor API | Yes | API | LAN gateway |
| SN-001 | Occupancy | Modbus/Wi-Fi | No | Yes | IoT gateway |

### 3.2 Gateway architecture choice / 网关架构选择

| Scope / 范围 | Option / 方案 | When / 适用 |
|---|---|---|
| Small club / 小馆 | BLE hub + club Wi-Fi (VLAN) | <15 BT devices / <15 蓝牙设备 |
| Mid / 中馆 | Local IoT gateway (MQTT) | Mixed protocols / 多协议 |
| Multi-club / 多店 | Edge gateway + cloud broker | Central BI / 集中 BI |

> **Rule / 规则**: gateway sits on IoT VLAN, not guest VLAN; outbound via broker with auth. / 网关在 IoT VLAN 而非访客 VLAN；经带鉴权的 broker 上行。

### 3.3 Data mapping to member 360 / 映射到会员 360

- [ ] Device session → member ID (scan/band at machine or app start). / 器械会话→会员 ID（机器扫码/App 启动）。
- [ ] Fields: duration, distance, calories, HR (if ANT+), reps (smart). / 字段：时长、距离、卡路里、心率（ANT+）、次数（智能）。
- [ ] Land in MMS member profile + BI fact table. / 落入 MMS 会员档案+BI 事实表。
- [ ] No raw video / audio captured (HI-8). / 不采原始视频/音频。
- [ ] Retention per `tools/05` schedule. / 留存依 `tools/05` 计划。

### 3.4 Pairing UX plan / 配对体验方案

- [ ] Member scans QR/band at machine → session auto-tags. / 会员机器扫码/手环→会话自动归属。
- [ ] Coach can pair HR strap via ANT+ in 2 taps. / 教练 2 步配对手环（ANT+）。
- [ ] Failure message plain: "Tap again / 再扫一次", not an error code. / 失败提示说人话。
- [ ] Offline: machine stores session, syncs on reconnect. / 离线：机器存会话，重连同步。

### 3.5 Security hardening checklist / 安全加固清单

- [ ] Change ALL default passwords (device + gateway) day one. / 首日改全部默认密码（设备+网关）。
- [ ] Place devices on isolated IoT VLAN (`references/08`). / 设备置于隔离 IoT VLAN。
- [ ] Disable unused services (telnet, UPnP). / 关无用服务（telnet、UPnP）。
- [ ] Unique admin per vendor, no shared login (`data/21#ap-009`). / 各厂商独立管理员，不共用（见锚点）。
- [ ] Firmware update policy + offline image backup. / 固件更新策略+离线镜像备份。
- [ ] Broker auth (cert/key), no anonymous publish. / broker 鉴权（证书/密钥），禁匿名发布。

---

### 3.6 Worked gateway example / 网关实例

- Club / 场馆: 12 treadmills (FTMS), 8 bikes (FTMS), 6 smart strength (vendor API), 4 occupancy (Modbus). / 12 跑台+8 单车(FTMS)、6 智能力量(厂商API)、4 占用(Modbus)。
- Choice / 选择: local IoT gateway (MQTT) on IoT VLAN; BLE hub for cardio, LAN gateway for strength, Modbus→MQTT bridge for sensors. / 本地 IoT 网关(MQTT)在 IoT VLAN；有氧用 BLE 汇、力量用 LAN 网关、占用用 Modbus→MQTT 桥。
- Data path / 路径: device → gateway → broker(auth) → MMS + BI. No device on guest VLAN, none on public internet. / 设备→网关→broker(鉴权)→MMS+BI。无设备处访客 VLAN，无直连公网。
- Failure / 故障: gateway down → devices cache sessions, sync on recovery (idempotent). / 网关宕→设备缓存会话，恢复后幂等同步。

### 3.7 Onboarding rollout plan / 接入推广计划

- Phase 1 / 阶段一: audit & label every unit (§3.1 sheet). / 审计并贴标每台（§3.1 表）。
- Phase 2 / 阶段二: stand up gateway + IoT VLAN; onboard cardio (FTMS/BLE) first. / 立网关+IoT VLAN；先接有氧（FTMS/BLE）。
- Phase 3 / 阶段三: add smart strength (vendor API) + sensors (Modbus bridge). / 加智能力量（厂商API）+传感器（Modbus 桥）。
- Phase 4 / 阶段四: map sessions to member 360; validate in BI. / 会话映射会员 360；BI 校验。
- Phase 5 / 阶段五: security hardening pass (§3.5) + firmware baseline. / 安全加固（§3.5）+固件基线。

> **What good looks like / 合格标准**: after Phase 4, ≥95% of sessions attribute to a member ID with zero devices on public internet. / Phase 4 后 ≥95% 会话归属会员 ID，零设备直连公网。
> **Red flag / 红旗**: skipping Phase 2 (gateway) and putting devices on guest Wi-Fi → breach + lock-in. / 跳 Phase 2（网关）把设备放访客 Wi-Fi → 违约+锁定。

### 3.8 Device security baseline / 设备安全基线

- [ ] Inventory CMDB entry per device (asset tag, firmware ver, owner). / 每台设备入 CMDB（编号、固件版、负责人）。
- [ ] Outbound allow-list: only broker endpoint + NTP; block rest. / 出向白名单：仅 broker 端点+NTP；其余阻断。
- [ ] TLS pinned for broker; reject self-signed in prod. / broker 钉 TLS；生产拒自发证书。
- [ ] Logs shipped to central SIEM; no local default creds. / 日志送中央 SIEM；无本地默认凭证。
- [ ] Quarterly firmware review; offline image stored. / 季度固件复核；存离线镜像。
- [ ] Decommission wipes config + revokes cert/key. / 退役擦配置并注销证书/密钥。

### 3.9 Troubleshooting quick card / 排障速卡

| Symptom / 症状 | Self-check / 自查 | Stop-line / 停手线 |
|---|---|---|
| Device offline / 离线 | Gateway up? VLAN ok? / 网关在？VLAN 通？ | Don't expose to public net / 勿直连公网 |
| Session not attributed / 会话无归属 | Member scanned? ID mapped? / 会员扫码？ID 映射？ | Don't edit DB by hand / 勿手改库 |
| HR strap dead / 心率带没电 | Battery? ANT+ paired? / 电池？ANT+ 配对？ | Don't buy proprietary lock-in / 勿买专有锁定 |
| Data gap / 数据缺口 | Broker auth? retry queue? / broker 鉴权？重试队列？ | Don't disable TLS / 勿关 TLS |

> **Rule / 规则**: every fault has a logged path; no silent data loss. / 每个故障有日志路径；杜绝静默丢数据。

### 3.10 Vendor question snippet / 供应商提问片段

Ask before signing / 签约前必问:
- "Does the console export session data via FTMS or open API, or only your app?" / 「控制台经 FTMS 或开放 API 导出，还是只认你家 App？」
- "If your cloud stops, can devices still cache & export locally?" / 「你家云停了，设备还能本地缓存导出吗？」
- "What are the default credentials, and can we enforce cert auth to the broker?" / 「默认凭证是什么，能否强制 broker 证书鉴权？」

> **Red flag / 红旗**: "only our app" + "no local export" = lock-in (`data/21#ap-002`). / 「只认我家 App」+「无本地导出」=锁定（见锚点）。

## ④ Common mistakes (anti-patterns) / 常见错误（反模式）

- `data/21#ap-002-no-data-export` — buying kit whose data you can never export. / 买数据永不可导出的设备。
- `data/21#ap-009-shared-admin-login` — one shared admin across all IoT vendors. / 各 IoT 厂商共用一管理员。
- `references/09` no-gateway pattern — 20 devices straight to internet, no gateway/VLAN. / 20 设备直连公网无网关 VLAN。
- `data/21#ap-016-gray-import-critical` — grey-import smart kit with no local firmware/support. / 灰货智能设备无本地固件/支持。

---

## ⑤ Related files / 相关文件

- `references/09-iot-and-open-protocols.md` — protocol bible. / 协议全书。
- `references/08-network-and-infrastructure.md` — VLAN & gateway placement. / VLAN 与网关位置。
- `templates/09-mms-selection-scorecard.md` — MMS is the data sink. / MMS 是数据汇。
- `references/04-ai-application-landscape.md` — downstream churn/utilisation AI. / 下游流失/利用率 AI。

---

## ⑥ G13 tri-perspective note / G13 三视角覆盖说明

This template serves **Architect** (gateway choice + VLAN + data mapping), **Operator** (security hardening + inventory audit), and **Member** (smooth pairing, private usage data, no surveillance); the HI-8 minimisation and no-gateway-flat-internet rules keep the member's data purposeful and contained — no orphaned touchpoint.
本模板覆盖**架构师**（网关选择+VLAN+数据映射）、**运营者**（安全加固+逐台审计）、**会员**（顺畅配对、私用数据、无监控）；HI-8 最小化与"不直连公网"规则让会员数据目的明确且受控——无孤儿触点。
