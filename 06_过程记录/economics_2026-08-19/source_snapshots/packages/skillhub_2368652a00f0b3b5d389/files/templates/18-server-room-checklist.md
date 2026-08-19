# Server / Network Closet Standard & Checklist / 服务器/网络机房标准与清单

> **Cluster / 集群**: D (Network & server room)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: UPS sizing & vendor price re-verify every 90 days via `tools/04`; rack/cooling spec stable but market prices 🔄.
> **Cross-references / 交叉引用**: `references/08` (D4), `data/11#n23-poe-camera-all-down`, `data/20` (micro-details), `data/21#ap-010-skip-ups`, `templates/17` (network build).
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this checklist to specify and maintain the **server/network closet** — the box that holds the brain (switch, NVR, server, UPS). Even a tiny club needs one; "we'll put the switch on a shelf" is a future outage.
本清单用于规定与维护**机房**——装"大脑"（交换机、NVR、服务器、UPS）的箱子。再小的店也要机房；"交换机放架子上就行"是未来的故障。

- **FDMM gate / 等级闸门**: L1 (every club, even a wall-mount rack). Do not prescribe L4 hot-aisle containment to an L1 studio.
  L1（每店，哪怕挂墙机柜）。别给 L1 工作室上 L4 热通道封闭。
- **Trigger / 触发**: new build, closet overheating, UPS beeping, "which password was the Wi-Fi?".
  新店、机房过热、UPS 鸣叫、"Wi-Fi 密码是哪个来着"。

---

## ② Prerequisites checklist / 前置清单

- [ ] Dedicated IT circuit planned, separate from general load (`references/15#g1-site-survey`). / 已规划 IT 独立回路，独立于总负载。
- [ ] Location away from showers, pool, direct sun. / 位置远离淋浴、泳池、直晒。
- [ ] Chalk-generating zones (yoga/pilates) nearby → dust plan. / 附近有产粉笔灰区（瑜伽/普拉提）→ 防尘计划。
- [ ] UPS sizing worksheet filled (§3.3). / UPS 选型表已填（§3.3）。
- [ ] Physical lock + spare key controlled. / 物理锁+备用钥匙受控。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Location & sizing / 位置与尺寸

| Item / 项 | Spec / 规格 | Fill / 填写 |
|---|---|---|
| Location 位置 | dry, ventilated, locked, no pipe above 上方无水管 | `____` |
| Min size 最小尺寸 | wall rack ≥ 12U; floor rack ≥ 18U | `____` U |
| Clearance 余隙 | 60 cm front, 30 cm rear for airflow 前 60 后 30 | `____` |
| Dedicated circuit 独立回路 | own breaker, surge-protected 独立空开+防雷 | `____` A |

> **Guidance / 指引**: Never above a shower or under a water pipe. A leak over the switch = total club down (`data/11#n23-poe-camera-all-down` on the CCTV side).
> 绝不在淋浴上方或水管下。漏水浇交换机=全场瘫。

### 3.2 Power / 供电（含 UPS 选型工作表）

**Dedicated circuit / 独立回路**: One breaker feeds ONLY the closet. No treadmills on it.
独立空开仅供机房，跑步机不得共用。

**UPS sizing worksheet (worked math, see `references/08` D4) / UPS 选型工作表（算例见 `references/08` D4）**

| Load component / 负载项 | Watts / 瓦 |
|---|---|
| Switch 交换机 | `____` (e.g. 50) |
| APs (PoE) AP数 | `____` (e.g. 6×15=90) |
| NVR + cameras NVR+摄像头 | `____` (e.g. 60) |
| Router 路由 | `____` (e.g. 15) |
| Server 服务器 | `____` (e.g. 150) |
| **Subtotal 小计** | `____` W |
| +30% headroom 余量 | `____` W |
| **Target runtime 目标续航** | `____` min → battery Wh = target W × (min/60) |
| **Choose UPS ≥** | `____` Wh |

> **Micro-example / 微例**: 365 W + 30% = 475 W; 30 min → 237.5 Wh → choose ≥300 Wh unit. Swap battery every 2–3 yrs (`data/20#md-006-ups-vs-surge-outlets`).
> 365W+30%=475W；30 分钟→237.5Wh→选 ≥300Wh。电池 2–3 年一换。

**UPS beep table / 蜂鸣表**: long steady = on battery; fast = low; chirp 30s = battery fault (replace).
长鸣=用电池；急鸣=电量低；半分钟啾=电池坏（换）。

### 3.3 Cooling & dust control (chalk!) / 散热与防尘（粉笔灰！）

- Target 22–26 °C, airflow front-to-back, no sealed shoebox. / 目标 22–26°C，前进后出，别封鞋盒。
- **Chalk dust / 粉笔灰**: Yoga/pilates chalk clogs fans → fit intake filter, clean quarterly. / 瑜伽/普拉提粉笔灰堵风扇→装进风滤网，季度清。
- If >35 °C: shut non-critical gear to save UPS (`references/08` overheat). / >35°C 关非关键保 UPS。

### 3.4 Physical security / 物理安全

- [ ] Locked door; key with 2 named staff only. / 门锁；仅 2 名指定员工持钥匙。
- [ ] No food/drink inside. / 机房内禁饮食。
- [ ] Offboarding removes key + access (`data/21#ap-024-offboarding-checklist`). / 离职收回钥匙与权限。
- [ ] Logbook of who entered. / 进出入登记。

### 3.5 Labeling & photo documentation SOP / 标签与拍照留档 SOP

1. Label every cable both ends: `FLOOR-ZONE-NUMBER`. / 每线两端贴标：`楼层-区-号`。
2. Photograph rack before closing walls AND after final patch. / 封墙前与最终配线后各拍机柜。
3. Keep as-built photo set in credentials vault (§3.6). / 竣工照存入凭证库。
4. One change = one photo update (do not let photos rot). / 一动就更新照，别让照片过期。

### 3.6 Credentials vault (handover doc set) / 凭证库（移交文档集）

Store encrypted, access-controlled: ISP contracts, VLAN/IP table, device admin passwords, UPS model+serial, as-built diagram, photo set. See `templates/17` §3.6.
加密、受控存放：运营商合同、VLAN/IP 表、设备管理员密码、UPS 型号序列、竣工图、照片集。见 `templates/17` §3.6。

### 3.7 Quarterly inspection checklist / 季度巡检清单

- [ ] Temp 22–26 °C verified with thermometer. / 温度实测 22–26°C。
- [ ] Fan/filter cleaned (chalk check). / 风扇滤网已清（查粉笔灰）。
- [ ] UPS self-test passed; battery date logged. / UPS 自检过；电池日期登记。
- [ ] Labels legible; photos match reality. / 标签清晰；照片与实况一致。
- [ ] Spare key accounted for. / 备用钥匙在册。
- [ ] No unauthorized device plugged in. / 无未授权设备接入。

---

## ④ Common mistakes / 常见错误

1. Skip the UPS to save money → one blink kills recordings. / 省钱不买 UPS→一闪没录像。→ `data/21#ap-010-skip-ups`
2. Closet above a shower → leak kills switch. / 机房在淋浴上→漏水废交换机。→ `data/11#n23-poe-camera-all-down`
3. No intake filter near chalk zone → fans clog. / 粉笔灰区无滤网→风扇堵。
4. Photos never updated → as-built lies. / 照片从不更新→竣工图说谎。
5. Shared admin login → offboarding gap. / 共用管理员账号→离职漏洞。→ `data/21#ap-024-offboarding-checklist`

---

## ⑤ Related files / 相关文件

- `references/08-network-and-infrastructure.md#d4-closet` — D4 design basis / 设计依据
- `templates/17-network-build-and-acceptance.md` — network spec + as-built / 网络规格与竣工
- `data/11-network-fault-tree-library.md#n23-poe-camera-all-down` — closet fault / 机房故障
- `data/20-micro-details-ledger.md#md-006-ups-vs-surge-outlets` — UPS detail / UPS 细节
- `references/15-lifecycle-scenarios.md#g1-preopening` — power-first survey / 先查电

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (sizing + UPS math + location rules), **Operator** (quarterly SOP, photo doc, beep table for non-IT), and **Member** (always-on gates/recording via UPS redundancy, no data loss); each mistake links to `data/11`/`data/21`/`data/20` anchors for actionable fixes.
本模板覆盖**架构师**（尺寸+UPS 算法+位置规则）、**运营者**（季度 SOP、拍照留档、蜂鸣表非 IT 可用）、**会员**（UPS 冗余保闸机/录像常开、不丢数据）；每条错误链 `data/11`/`data/21`/`data/20` 锚点可立即整改。
