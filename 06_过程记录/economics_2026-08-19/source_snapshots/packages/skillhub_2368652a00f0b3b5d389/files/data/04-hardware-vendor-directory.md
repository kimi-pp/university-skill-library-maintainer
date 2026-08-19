# Hardware Vendor Directory (APAC Landscape) / 硬件供应商名录（亚太格局）

> **Cluster / 集群**: C (Hardware ×12 categories)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Model lines, prices and service-network coverage re-verify every 90 days via `tools/04`; every vendor cell carries 🔄 meaning "example, not endorsement — verify nearest service center before buying".
> **Cross-references / 交叉引用**: `references/07-hardware-landscape-and-vendors.md` (narrative guide), `data/10-hardware-fault-tree-library.md` (fault anchors), `data/15-procurement-and-cost-benchmark.md` (cost & TCO), `data/21-anti-pattern-library.md` (gray-import trap), `data/20-micro-details-ledger.md`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## How to use this directory / 本名录使用说明

A structured, table-heavy map of hardware by category and market. The column that matters most for a club is **service-network** — the nearest service center often decides uptime more than any spec sheet.
按类别与市场的结构化表格地图。对场馆最重要的是**服务网络**列——最近的服务中心往往比任何参数表更决定停机时间。

**Honesty preamble / 诚实前置**: Hardware model lines, warranty terms and — critically — *where the service center actually is* change frequently. A brand famous in one city may have zero coverage 200 km away. Always verify (a) nearest authorized service center, (b) spare-parts lead time, (c) warranty on-site vs carry-in via `tools/04` **and a phone call** before purchase.
硬件型号、保修条款，尤其是"服务中心实际位置"经常变化。某城知名的品牌，200 公里外可能零覆盖。采购前务必核实（a）最近授权服务中心、（b）备件交期、（c）上门还是送修保修——经 tools/04 **加一通电话**。

> **Golden rule / 黄金铁律**: Spec sheet is marketing; service network is reality. A ¥2k-cheaper machine with no local service will cost more in downtime. See `data/21#ap-025-gray-import`.
> 参数表是营销，服务网是现实。便宜 2k 但无本地服务的机器，停机代价更大。见 `data/21#ap-025-gray-import`。

**Column legend / 列说明**: category = 类别 · brand examples 🔄 = 示例非背书 · market presence = 市场覆盖 · service-network note = 服务网注记(真正差异点) · typical warranty patterns = 典型保修模式 · parts availability = 备件可得注记.

---

## 1. Cardio & Strength Brands / 有氧与力量品牌 {#cat-cardio-strength}

| Category / 类 | Brand examples 🔄 | Market presence | Service-network note | Typical warranty pattern | Parts availability |
|---|---|---|---|---|---|
| Cardio (treadmill/bike/elliptical/rower) | Technogym, Life Fitness, Precor, Matrix | Global, premium / 全球高端 | authorized service in major cities; verify / 大城市有授权，需核实 | 2–5y frame, 1–2y parts / 架2–5年件1–2年 | good in metro /  metro 好 |
| Cardio (local) | 舒华 Shua, 英派斯 Impulse, 乔山, 岱宇 | China + APAC | broad China coverage / 中国覆盖广 | 2–3y / 2–3年 | strong local / 本地强 |
| Smart bike (consumer-grade) | Keep-type 智能单车 🔄 | China consumer | limited commercial service / 商用服务有限 | 1y consumer / 1年消费级 | consumer channel / 消费渠道 |
| Strength (selectorized/plate) | 舒华, 英派斯, 泰山, Technogym, Life Fitness | China + global | metro service / metro 服务 | 5–10y frame / 架5–10年 | good / 好 |
| Smart strength | 速境, 万达康, Technogym BIKE/SMART | China + global | sparse for smart boards / 智能板稀疏 | board 1–2y / 板1–2年 | varies / 不一 |

:::dynamic-hook topic="apac-cardio-brand-service-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
Brand service coverage shifts as distributors change. A brand strong in Shanghai may be weak in tier-3 cities. Verify nearest service center per club location via tools/04 + direct call.
品牌服务随经销商变动。上海强的品牌，三线可能弱。按门店位置经 tools/04 + 直拨核实最近服务中心。
:::

---

## 2. Gates & Access Control / 闸机与门禁 {#cat-gates-access}

| Category / 类 | Brand examples 🔄 | Market presence | Service-network note | Warranty pattern | Parts availability |
|---|---|---|---|---|---|
| Turnstile/swing gate | 海康, 大华, 捷顺, 同旺, ASSA ABLOY, dormakaba, 令令开门 | China + global | metro strong; ASSA/dormakaba global / metro 强 | 1–3y / 1–3年 | good / 好 |
| Reader (NFC/QR/face) | 复旦微电子 RFID, NXP, 海康 | all | module-level service / 模块级 | 1–2y / 1–2年 | good / 好 |

> **Fail-mode decision / 断电策略**: Fire code usually requires fail-OPEN for egress (HI-4). Confirm exact clause via `tools/05`. A "facial gate" not synced to MMS is an orphan (see `data/21`).
> 消防多要求断电开闸疏散（HI-4）。具体条款经 tools/05。不接 MMS 的"人脸闸机"是孤儿（见 `data/21`）。

---

## 3. Smart Lockers / 智能储物柜 {#cat-lockers}

| Category / 类 | Brand examples 🔄 | Market presence | Service-network note | Warranty pattern | Parts availability |
|---|---|---|---|---|---|
| RFID/barcode/app lock | 好易通, 易丰, 悍高, 智莱, 基信 | China + APAC | controller is single point / 控制器为单点 | 1–3y / 1–3年 | cell locks stock / 格锁有备 |
| Pool-grade waterproof | same + 西昊 | China | verify IP rating service / 核 IP 防护服务 | 1–2y / 1–2年 | varies / 不一 |

---

## 4. Body-Composition Analyzers / 体测仪 {#cat-body-comp}

| Category / 类 | Brand examples 🔄 | Market presence | Service-network note | Warranty pattern | Parts availability |
|---|---|---|---|---|---|
| BIA 8-point | InBody, 体脂康, 好尚 | Global, China | InBody global service / 全球服务 | 2–3y / 2–3年 | electrodes stock / 电极有备 |
| Local BIA | 清华同方-type, 姿动 posture | China | local / 本地 | 1–2y / 1–2年 | varies / 不一 |
| Posture/gait scanner | 姿动, 国际 CV SaaS | China/global | software-led / 软件主导 | 1y / 1年 | n/a |

> **Certification / 认证**: Local medical-device class varies by market (S1 in `references/07`). "Hospital-grade" without local cert is a red flag. Verify via `tools/05`.
> 本地医疗器械分级因市场而异（见 `references/07` S1）。无本地认证的"医院级"是红旗。经 tools/05 核验。

---

## 5. POS Terminals per market / 收银终端（分市场）{#cat-pos-terminal}

| Market / 市场 | Terminal brand examples 🔄 | Acquirer-tied nuance / 收单绑定细则 |
|---|---|---|
| China 大陆 | 商米, 美团收银, 拉卡拉, 新大陆 | Alipay/WeChat SDK built-in / 内置支付宝微信 SDK |
| Japan 日本 | Recruit-type, Square, Hitachi-Omron | GMO/本地收单必备 / 需本地收单 |
| Korea 韩国 | Kakao/本土终端 | KakaoPay 集成 / KakaoPay 集成 |
| ANZ 澳新 | Square, Verifone, EFTPOS | EFTPOS 本地 / EFTPOS 本地 |
| SEA 东南亚 | 本土 + Adyen/Xendit/2C2P | 收单绑定强 / 收单绑定强 |
| India 印度 | 本土 + Razorpay | UPI 必备 / UPI 必备 |

> **Nuance / 细则**: Terminal often locks to an acquirer; switching processor later may mean new hardware. Ask "can I use my own acquirer?" before buying (see `data/15` procurement).
> 终端常绑定收单；日后换通道可能要换硬件。采购前问"能否用自己的收单？"（见 `data/15`）。

---

## 6. Digital Signage / 数字标牌 {#cat-signage}

| Category / 类 | Brand examples 🔄 | Market presence | Service-network note | Warranty pattern | Parts availability |
|---|---|---|---|---|---|
| Lobby/studio screens | 视达, 小鸟看看, 星际, Yodeck, NoviSign | China + global | screen swap service / 换屏服务 | 1–3y / 1–3年 | panels stock / 屏有备 |
| Smart mirror | 小米, 华为, 国际 mirror | China/global | consumer-grade / 消费级 | 1y / 1年 | varies / 不一 |

---

## 7. CCTV & Security (compliance note) / 监控与安防（合规注记）{#cat-cctv}

| Category / 类 | Brand examples 🔄 | Market presence | Service-network note | Warranty pattern | Parts availability |
|---|---|---|---|---|---|
| Cameras/NVR | 海康, 大华, 宇视, Axis, Hanwha, Reolink | China + global | metro strong / metro 强 | 2–3y / 2–3年 | good / 好 |

:::dynamic-hook topic="apac-cctv-brand-procurement-restriction-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
Some brands face public-sector procurement restrictions in certain APAC markets (e.g. government/state-adjacent venues). For a private gym this is usually fine, but verify procurement rules for your exact entity type and market via tools/05 before bulk buy.
某些品牌在部分亚太市场涉公共采购限制（如政府/国有相关场所）。民营健身房通常无碍，但批量采购前按"你的实体类型+市场"经 tools/05 核验采购规则。
:::

> **No-go zones / 禁区**: Changing rooms & showers = absolute no imaging (HI-5). Retention period per market law (see `references/12`).
> 更衣室与淋浴区=绝对禁摄（HI-5）。留存期依法（见 `references/12`）。

---

## 8. Network Gear Tiers / 网络设备分层 {#cat-network-gear}

| Tier / 档 | Examples 🔄 | When it is FINE for a club / 何时够用 | When to AVOID / 何时避开 |
|---|---|---|---|
| Consumer / 消费级 | TP-Link 家用, 小米家宽 | single-room pop-up, <50㎡, no POS dependency / 单间快闪<50㎡无收银依赖 | any club with POS, gates, >1 AP / 任何有收银闸机多 AP 的馆 |
| Prosumer / 准企业 | Ubiquiti UniFi, TP-Link Omada | boutique studio ≤300㎡, 1–3 APs, VLAN capable / 精品≤300㎡ 1–3 AP 支持VLAN | multi-site chain needing central mgmt / 需集中管理的多店 |
| Enterprise / 企业 | 锐捷, 信锐, H3C, Cisco, Aruba, Meraki | multi-club, SD-WAN, VLAN, SLA / 多店 SD-WAN VLAN SLA | single tiny studio (overkill cost) / 单小店（过度成本） |

> **Rule / 规则**: A club with gates + POS + CCTV needs VLAN-capable gear minimum (prosumer+). Consumer Wi-Fi is the #1 silent cause of "internet is fine but gate won't open" (see `data/08#router-multi-hop`).
> 有闸机+收银+监控的馆至少需支持 VLAN（准企业起）。消费级 Wi-Fi 是"网好但闸不开"的头号隐性原因（见 `data/08#router-multi-hop`）。

---

## 9. UPS / 不间断电源 {#cat-ups}

| Tier / 档 | Brand examples 🔄 | Use / 用途 | Warranty pattern | Notes / 注记 |
|---|---|---|---|---|
| Entry / 入门 | 山特, APC Back-UPS, 华为 | front-desk POS + gate controller / 前台收银+闸控 | 2y battery / 电池2年 | battery swap 2–3y / 电池2–3年换 |
| Rack / 机架 | APC Smart-UPS, 华为, 伊顿 | server closet NVR+network / 机房 NVR+网络 | 2–3y / 2–3年 | size by load / 按负载选型 |

> **Sizing / 选型**: See `references/08` D4 UPS sizing. Under-sized UPS = beeping every brownout (see `references/07#ups-beep-table`).
> 选型见 `references/08` D4。小 UPS = 每次电压波动都叫（见 `references/07#ups-beep-table`）。

---

## 10. IoT / Sensors / IoT 传感器 {#cat-iot-sensors}

| Category / 类 | Brand examples 🔄 | Market presence | Service note | Warranty | Parts |
|---|---|---|---|---|---|
| Occupancy/temp/energy | 涂鸦, 安科瑞, 小米 IoT, Schneider, Siemens, 海康传感 | China + global | module service / 模块级 | 1–2y / 1–2年 | varies / 不一 |
| Pool water quality | 本地水质传感器 | China | local / 本地 | 1y / 1年 | varies / 不一 |

> **API red line / API 红线**: No sensor without API/Modbus export — a "smart" sensor you can't pull data from is decoration (see `data/20#md-071-spec-marketing`).
> 无 API/Modbus 导出的传感器=摆设（见 `data/20#md-071-spec-marketing`）。

---

## 11. Group HR Systems / 团体心率系统 {#cat-group-hr}

| Category / 类 | Brand examples 🔄 | Market presence | Service note | Warranty | Parts |
|---|---|---|---|---|---|
| Club group HR | Myzone-type, 国际 HR SaaS, 本土心率带 | global + China | strap-level / 心率带级 | 1y / 1年 | straps stock / 带备 |
| HR straps/bands | Garmin, Polar, Wahoo, 小米手环 | global | consumer service / 消费级 | 1y / 1年 | good / 好 |

> **Note / 注**: Group HR needs ANT+/Bluetooth chest straps + a display gateway; verify chest-strap durability (members sweat) before bulk buy.
> 团体心率需 ANT+/蓝牙胸带 + 显示网关；批量前核胸带耐用（会员出汗）。

---

## 12. Buying-channel guidance / 采购渠道指引 {#buying-channel}

| Channel / 渠道 | Pros / 优 | Cons / 劣 | When / 何时 |
|---|---|---|---|
| Direct from brand / 品牌直采 | best warranty, SLA / 保修最佳 | higher price, slower for SMB / 价高 SMB慢 | multi-club chain / 多店连锁 |
| Distributor / 经销商 | local service, bundle / 本地服务可捆绑 | markup, may lock brand / 加价可能锁品牌 | most clubs / 多数场馆 |
| Gray import / 水货 | cheap / 便宜 | NO local warranty, no parts, compliance risk / 无本地保修无备件合规风险 | NEVER for safety/access gear / 安全门禁设备绝不 |

:::dynamic-hook topic="apac-hardware-gray-import-risk-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
Gray-import fitness hardware is common in APAC grey markets; it voids local warranty and leaves you with no parts. Verify the seller is authorized via brand's site (tools/04) before paying.
亚太水货健身硬件常见；它使本地保修失效且无备件。付款前经品牌官网（tools/04）核实卖家授权。
:::

> **Anti-pattern link / 反模式链接**: Gray-import trap → `data/21#ap-025-gray-import`. The "cheap" gate that dies in 6 months costs more than buying direct.
> 水货陷阱 → `data/21#ap-025-gray-import`。"便宜"闸机半年坏，比直采更贵。

---

## 13. Per-region brand map / 分区域品牌图

| Region / 区域 | Cardio/strength 🔄 | Access/IoT 🔄 | POS 🔄 |
|---|---|---|---|
| China 大陆 | 舒华/乔山/英派斯 | 海康/大华/捷顺 | 商米/美团/拉卡拉 |
| Japan 日本 | Technogym/Life Fitness | 国产品 | Recruit/Square |
| Korea 韩国 | 国产品 | 韩系 | Kakao/本土 |
| ANZ 澳新 | Technogym/Life Fitness | ASSA/dormakaba | Square/EFTPOS |
| SEA 东南亚 | 舒华/Technogym | 海康/本土 | 本土/Adyen |

All 🔄 examples not endorsements; verify via `tools/04`. / 均 🔄 示例非背书；经 tools/04 核验。

---

## 13. Per-category go/no-go checklist / 各类采购可行清单

A compact pre-buy gate per category so a beginner doesn't miss the one thing that matters.
每类采购前的精简门槛，避免新手漏掉那件要命的事。

| Category / 类 | Go if… / 可行条件 | No-go if… / 否决条件 |
|---|---|---|
| Cardio / 有氧 | continuous HP rated, deck warranty, FTMS | "peak HP" only, no warranty / 只标峰值马力无保修 |
| Gate / 闸机 | fail-mode decided + fire-code ok (HI-4) | face gate not synced to MMS / 不接 MMS 人脸闸 |
| Locker / 柜 | centralized controller redundant, pool IP rated | biometric-only in changing room (HI-5) / 更衣室纯生物 |
| Body / 体测 | local medical-device cert (S1) | "hospital-grade" no cert / 无认证"医院级" |
| POS / 收银 | local pay SDK + offline mode | weak all-in-one printer / 弱一体机打印 |
| CCTV / 监控 | retention per law, no HI-5 zones | "AI" with no export path / 无导出"全AI" |
| Network / 网络 | VLAN capable, PoE budget sized | "gaming router" for club / 场馆用电竞路由 |
| IoT / 传感器 | API/Modbus export + IP rating | no API "smart" sensor / 无API"智能" |
| Wearable / 穿戴 | durable, waterproof, swap battery | "free" fragile band / 易坏"免费"环 |

---

## 14. Warranty red lines / 保修红线

- Never accept "consumables not covered" without a listed price (belt, cutter, electrode). / 不接受"耗材不保"却不列价（跑带、切刀、电极）。
- Spare-parts availability must be stated for ≥ life of product, with lead time. / 备件可得须声明≥产品寿命，含交期。
- On-site response time in writing (SLA), e.g. 48h metro / 72h remote. / 上门响应时间书面（SLA），如 metro 48h / remote 72h。
- Verify the seller is an authorized service partner via brand site (tools/04) before paying. / 付款前经品牌官网（tools/04）核实卖家为授权服务伙伴。

---

## 15. Service-center verification script / 服务中心核实话术

Plain words / 说人话 — ask before you buy: / 采购前问：
1. "Nearest authorized service center to [my address]?" / "离我地址最近的授权服务中心？"
2. "Spare-part lead time for [model]?" / "[型号] 备件交期？"
3. "On-site SLA in writing?" / "上门 SLA 书面？"
4. "Warranty on-site or carry-in?" / "保修上门还是送修？"

> **Rule / 规则**: No answer to Q1–Q3 = walk away. A cheap machine with no service is the most expensive one (see `data/21#ap-025-gray-import`).
> Q1–Q3 答不出=走人。无服务的便宜机器最贵（见 `data/21#ap-025-gray-import`）。

---

## 16. Network tier decision table / 网络分层决策表

| Club profile / 场馆画像 | Tier / 档 | Why / 原因 |
|---|---|---|
| ≤300㎡, no POS dependency | Consumer OK / 消费级可 | low impact radius / 影响面小 |
| ≤500㎡ boutique, 1–3 AP, VLAN needed | Prosumer / 准企业 | VLAN + cost balance / VLAN+成本平衡 |
| ≥800㎡ or multi-AP or POS+gates | Enterprise entry / 企业入门 | SLA, central mgmt / SLA集中管理 |
| Multi-site chain | Enterprise + SD-WAN | group control / 集团管控 |

---

## G13 Tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: tier selection (consumer/prosumer/enterprise) + fault-tree links to `data/10`.
- **Operator / 运营者**: service-network reality + warranty/SLA + buying-channel trade-offs.
- **Member / 会员**: reliable entry (gates), lockers, body tests, wearables — all depend on the service network behind the brand. No hardware class is an orphan (every category → `data/10` fault anchor).
本文件覆盖架构师（分层选型+故障树锚点）、运营者（服务网现实+保修/SLA+渠道权衡）、会员（可靠入场/柜/体测/穿戴，全靠品牌背后的服务网）。无孤儿硬件类（每类→ `data/10` 故障锚点）。
