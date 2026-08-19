# Network Build Spec & Acceptance / 场馆网络建设规格与验收

> **Cluster / 集群**: D (Network & server room)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: ISP/vendor price & AP density rules re-verify every 90 days via `tools/04`; Wi-Fi consent + CCTV rules via `tools/05`.
> **Cross-references / 交叉引用**: `references/08` (network), `data/11` (fault trees), `data/20` (micro-details), `data/21` (anti-patterns), `templates/18` (server room).
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this template to write a **network build specification** and run **acceptance** before the contractor leaves site. It turns "the Wi-Fi feels okay" into a signed, measurable checklist.
本模板用于编写**网络建设规格书**并在施工方离场前完成**验收**，把"Wi-Fi 好像还行"变成可签字、可度量的清单。

- **FDMM gate / 等级闸门**: L1 (every club) — cabling at fit-out; L2 — three-SSID VLAN separation; L4 — SD-WAN. Prescribe only the level the club has reached; do not over-build for an L1 paper-club.
  L1（每店）—装修期布线；L2—三 SSID/VLAN 分离；L4—SD-WAN。只给该店已到达的等级，别给 L1 纸表店过度建设。
- **Trigger / 触发**: new build, major renovation, or "we keep having dropouts and nobody wrote the spec."
  新店、大改造，或"老掉线却没人写过规格书"。

---

## ② Prerequisites checklist / 前置清单

- [ ] Floor plan with zone map (`references/02` §2) in hand. / 手头有带分区图的平面图（`references/02` §2）。
- [ ] Dual-ISP decision made (fiber + 5G/second fiber). / 双 ISP 已定（光纤+5G/第二光纤）。
- [ ] Server-room location confirmed (`templates/18`). / 机房位置已定（`templates/18`）。
- [ ] Cabling designed BEFORE renovation starts — wall-closed cabling costs 10× (`references/15#g1-cabling`, `data/21#ap-003-cabling-after-renovation`). / 装修前已出布线设计——封墙后布线贵 10 倍。
- [ ] Local regulation on Wi-Fi consent + CCTV known via `tools/05`. / 已通过 `tools/05` 了解本地 Wi-Fi 同意与监控法规。
- [ ] Budget ranges confirmed (see D8 in `references/08`). / 预算区间已确认（见 `references/08` D8）。

---

## ③ THE TEMPLATE / 模板正文

> **How to fill / 填写说明**: Replace every `____` with your club's value. Bilingual labels are `English / 中文`. Keep one copy per club; file it in the credentials vault (`templates/18`).
> **填写说明**：把每个 `____` 换成你店的值。双语标签为 `English / 中文`。每店存一份，归入凭证库（`templates/18`）。

### 3.1 Coverage requirement worksheet per zone / 分区覆盖需求表

| Zone / 区 | Area m² / 面积 | Concurrent devices / 并发设备 | Required signal / 需达信号 | Notes / 备注 |
|---|---|---|---|---|
| Lobby 大堂 | `____` | `____` (phones+POS) | ≥ -65 dBm | captive portal 门户 |
| Gym floor 操房区 | `____` | `____` | ≥ -67 dBm | mirrors kill signal 镜子杀信号 |
| Studio 教室 | `____` | `____` | ≥ -67 dBm | chalk dust 粉笔灰 |
| Locker 更衣 | `____` | `____` | ≥ -70 dBm | no camera (HI-5) 无摄像头 |
| Cafe 水吧 | `____` | `____` | ≥ -65 dBm | — |
| Outdoor 户外 | `____` | `____` | ≥ -72 dBm | optional 可选 |

> **Micro-example / 微例**: A 800 m² open gym floor with mirrors: plan 3–4 APs, not 1. Survey, don't guess (`references/08` D3).
> 800 ㎡ 带镜子开阔操房：布 3–4 个 AP，不是 1 个。要勘测别瞎猜。

### 3.2 SSID / VLAN plan (member / staff / IoT / CCTV separation) / SSID与VLAN规划（会员/员工/物/监控 四分离）

| Network / 网络 | SSID / 名称 | VLAN ID | Purpose / 用途 | Isolation / 隔离 |
|---|---|---|---|---|
| Member 会员 | `Club-Member` | `____` (e.g. 20) | captive portal, rate-limited 门户限速 | no LAN reach 不可达内网 |
| Staff 员工 | `Club-Staff` | `____` (e.g. 30) | POS/MMS/internal POS/会籍/内部 | no IoT reach 不可达物网 |
| IoT 物 | `Club-IoT` | `____` (e.g. 40) | locks/sensors/signs 锁/传感/标牌 | internet-only 仅外网 |
| CCTV 监控 | (wired / 有线) | `____` (e.g. 50) | NVR backhaul 录像回传 | isolated, no Wi-Fi (`data/21#ap-028-nvr-wifi-backhaul`) |

> **Guidance / 指引**: Three SSIDs can share ONE switch but never see each other's traffic (VLAN = logical wall). Never put CCTV NVR backhaul on Wi-Fi.
> 三个 SSID 可共用一台交换机却互不偷看（VLAN=逻辑墙）。监控 NVR 回传绝不走 Wi-Fi。

### 3.3 Cabling BOM & labeling standard / 布线清单与标签标准

**Bill of materials / 物料清单**
- Cat6 cable: `____` m (leave 30% spare / 留 30% 余量). / Cat6 线：`____` 米。
- Patch panel ports: `____` (30% spare / 余量). / 配线架端口：`____`。
- AP (PoE): `____` units @ `____` each 🔄. / AP：`____` 台，单价 🔄。
- Core switch + UPS: `____` (see `templates/18`). / 核心交换+UPS：`____`。
- Conduit: `____` (label every drop / 每个网口贴标). / 管线：`____`。

**Labeling rule / 标签规则**: `FLOOR-ZONE-NUMBER` e.g. `L1-LOBBY-03`. Both ends match. A cable with no label is a future outage (`data/20#md-001-cable-label-both-ends`, `data/21#ap-003-cabling-after-renovation`).
标签规则：`楼层-区-号`，如 `L1-LOBBY-03`，两端一致。没标签的线=未来故障。

### 3.4 AP placement notes for metal-heavy floors / 金属重地面 AP 布点注意

- Metal weights + mirrors attenuate 8–15 dB — place APs in OPEN ceiling, not behind racks. / 金属器械+镜子衰减 8–15 dB——AP 装开阔天花板，别藏器械后。
- One AP per ~200–300 m² open floor; density up near mirror walls. / 开阔区每约 200–300 ㎡ 一个 AP；镜墙附近加密。
- Mount height 2.4–3 m; avoid inside metal lockers or under steel beams. / 安装高度 2.4–3 m；避开金属柜与钢梁下。

### 3.5 Acceptance tests / 验收测试

| Test / 测试 | Method / 方法 | Pass criterion / 通过判据 |
|---|---|---|
| Walk test grid 走动网格 | walk every zone, record signal at `____` grid points | ≥ -70 dBm in 95% points |
| Throughput 吞吐 | iperf/speedtest at peak, staff+member+IOT | ≥ `____` Mbps per SSID |
| Dual-ISP failover 双线切换 | kill primary WAN | backup live < `____` s, POS continues |
| Gate fail-open 闸机故障开 | cut power to reader | gate opens (HI-4 safe) 故障开 |
| Outage drill 断网演练 | full WAN down | offline check-in + offline POS ok |

> **Stop-line / 停手线**: Do NOT sign acceptance if walk-test < 90% or failover > 60 s. A "demo that worked" is NOT acceptance (`data/21#ap-020-demo-not-acceptance`).
> 走动测试 <90% 或切换 >60 秒，绝不签字。demo 成功 ≠ 验收。

### 3.6 Handover documentation checklist / 移交文档清单

- [ ] As-built diagram (real, not sales drawing) / 竣工图（真实非效果图）
- [ ] Label map + photo of every patch panel / 标签图 + 每块配线架照片
- [ ] SSID/VLAN/IP table / SSID/VLAN/IP 表
- [ ] Credentials vault (see `templates/18`) / 凭证库
- [ ] ISP contracts + SLA / 运营商合同与 SLA
- [ ] Signed acceptance sheet / 已签验收单

---

## ④ Common mistakes / 常见错误

1. Cabling after paint → 10× cost. / 刷漆后布线→10 倍成本。→ `data/21#ap-003-cabling-after-renovation`
2. One SSID for all → lobby chokes gates. / 单 SSID→大堂憋死闸机。→ `data/11#n04-one-ssid-missing`, `data/11#n06-vlan-misconfig`
3. CCTV on Wi-Fi backhaul → blind spots on outage. / 监控走 Wi-Fi 回传→断网盲区。→ `data/21#ap-028-nvr-wifi-backhaul`
4. No labels → any fix is guesswork. / 无标签→修全靠猜。→ `data/20#md-001-cable-label-both-ends`
5. Logging member MAC without notice → privacy breach. / 无告知记 MAC→隐私违规。→ `data/21#ap-055-wifi-mac-no-notice`
6. Signing on demo only. / 仅按 demo 签字。→ `data/21#ap-020-demo-not-acceptance`

---

## ⑤ Related files / 相关文件

- `references/08-network-and-infrastructure.md` — D1–D8 design basis / 设计依据
- `templates/18-server-room-checklist.md` — closet standard + UPS math / 机房标准与 UPS 算法
- `references/15-lifecycle-scenarios.md#g1-preopening` — pre-opening sequence / 筹建编排
- `data/11-network-fault-tree-library.md` — outage diagnostics / 故障诊断
- `tools/05-regulation-traceability-verification.md` — Wi-Fi/CCTV consent / 同意合规

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (zone coverage worksheet + VLAN plan + BOM), **Operator** (acceptance walk-test grid + failover drill + as-built doc), and **Member** (reliable Wi-Fi, always-open gates via dual-ISP failover, no camera in changing rooms per HI-5); every mistake links to a `data/11`/`data/21` anchor so non-IT staff can act.
本模板覆盖**架构师**（分区覆盖表+VLAN 规划+清单）、**运营者**（验收走动网格+切换演练+竣工文档）、**会员**（稳定 Wi-Fi、双线保闸机常开、更衣室无监控 HI-5）；每条错误链 `data/11`/`data/21` 锚点，非 IT 也能执行。
