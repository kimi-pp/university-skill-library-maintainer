# Network Fault Tree Library / 网络故障树库

> **Cluster / 集群**: D (Network & server room / 网络与机房)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify every 90 days; ISP pricing, vendor landscape and SLA norms must pass `tools/04` before citing. Router/modem model menus differ by brand — verify exact menu path per device.
> **Cross-references / 交叉引用**: `references/08-network-and-infrastructure.md` · `data/10-hardware-fault-tree-library.md` (gate sync) · `references/15-lifecycle-scenarios.md` (G2 open/close) · `data/13-inspection-and-maintenance-calendar.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

This file is the **L0 firefighting** backbone for club network issues. Every entry uses the five-segment structure: **Self-check / 自查 → Stop-line / 停手线 → Vendor call script / 报修话术 → Parts & cost hint / 备件与费用参考 → Prevention / 预防措施**. Costs and times are directional ranges only.
本文件是场馆网络问题的 **L0 救火**主干。每条目采用五段式：**自查 → 停手线 → 报修话术 → 备件与费用参考 → 预防措施**。费用与时长仅为方向性区间。

---

## 🖨️ One-Page "Internet Down = Do This" Flow / 断网一页通（打印贴前台）

> Print this section and pin it at the front desk. Follow top to bottom. Do NOT skip steps.
> 打印本节并贴在前台。从上往下执行，不要跳步。

```
START 全场断网？ / Whole club down?
  │
  ├─ 1) 看光猫/路由指示灯 / Check modem & router lights
  │      → 见下方「指示灯速查」/ see "Light Decoder" below
  │
  ├─ 2) 光猫 POWER 灯不亮？ / POWER off?
  │      → 拔插头重插，换插座 / unplug, replug, try another socket
  │      → 仍不亮 = 电源或设备损坏，跳到 #n01
  │
  ├─ 3) 光猫 PON/LOS 红灯闪或常红？ / PON red or LOS blinking red?
  │      → 这是线路/运营商问题，不要动设备 / line/ISP issue, don't touch
  │      → 直接打运营商报修，念 #n01 话术 / call ISP with #n01 script
  │
  ├─ 4) 光猫灯正常但 Wi-Fi 无网？ / Lights OK but no Wi-Fi?
  │      → 重启路由（断电30秒再上电）/ reboot router (30s off)
  │      → 仍无网 = 跳 #n01
  │
  ├─ 5) 只有付款/某系统无网，浏览正常？ / Only payments down, browsing OK?
  │      → 跳 #n02（DNS/端口） / go to #n02 (DNS/port)
  │
  └─ 6) 高峰慢、平时正常？ / Slow only at peak?
         → 跳 #n03 / go to #n03
```

**Light Decoder (plain words) / 指示灯速查（说人话）**

| Light / 灯 | Normal / 正常 | Problem / 异常 | Meaning / 意思 |
|---|---|---|---|
| POWER | 常亮绿 / solid green | 不亮 / off | 没通电或电源坏 / no power |
| PON / LINK | 常亮绿 / solid green | 闪红/常红 / red | 运营商线路断了 / ISP line down |
| LOS | 灭 / off | 红 / red | 光纤收不到光 / no light from fiber |
| LAN | 亮（插线时）/ on when cabled | 灭（已插线）/ off cabled | 网线松或坏 / loose/bad cable |
| Wi-Fi / WLAN | 常亮 / solid | 灭 / off | Wi-Fi 关了或路由挂 / Wi-Fi off or dead |
| INTERNET / 地球 | 常亮 / solid | 灭 / off | 已连光猫但无外网 / up to modem, no net |

> 💡 Rule of thumb: **red light on the modem = ISP's problem, not yours.** Don't reboot endlessly; call the ISP.
> 💡 铁律：**光猫红灯 = 运营商的问题，不是你的。** 别无限重启，直接打运营商。

---

## #n01-whole-club-down / 全场断网（主流程图）

**Self-check / 自查（说人话）**
- Step 1: Look at the modem lights using the decoder above. If PON/LOS is red, the line from the street is down — it is the ISP's fault, not your router.
  先看光猫指示灯。若 PON/LOS 红灯，是外面光纤断了——运营商的锅，不是路由器的。
- Step 2: Ask a neighbor or nearby shop on the same ISP if they are also down (use your phone's 4G). If yes, it is a district outage.
  用手机 4G 问问同运营商的邻居/隔壁店是否也断。是，则是片区故障。
- Step 3: If only your club is down and POWER is on, unplug the modem AND router, wait 30 seconds, plug modem first, wait 2 minutes for lights to settle, then router.
  若仅你店断且通电正常，拔掉光猫和路由，等 30 秒，先插光猫，等 2 分钟灯稳定，再插路由。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT open the modem/router casing, do NOT cut or splice any cable, do NOT reset the modem to factory (you may lose the ISP config and need a technician visit).
  不要拆光猫/路由外壳，不要剪或接任何线，不要恢复出厂（会丢运营商配置，需师傅上门）。
- If you smell burning or see smoke from the device, cut power at the wall and call an electrician (see `data/14` electrician script) — this is a fire-safety issue, not IT.
  如闻到焦味或看到烟，墙上断电并叫电工——这是消防问题，非 IT。

**Vendor call script / 报修话术（照着念）**
- To ISP: "你好，我是 XX 健身房，地址是 <地址>。我们的光猫 PON 灯红色闪烁，LOS 红灯，已重启光猫和路由仍无外网。请派单，我要一个工单号（ticket number）。全场约 <N> 名会员和收银都断网，营业受影响，请给预计恢复时间。"
- To ISP (EN): "This is <club> at <address>. Our modem PON light is red and LOS is red; we power-cycled modem and router, still no internet. Please raise a ticket and give me the ticket number. The whole club — ~<N> members and POS — is offline. What is the ETR?"

**Parts & cost hint / 备件与费用参考**
- ISP line fault: usually **free** repair under the monthly plan (range ¥0; confirm no visit fee 🔄).
  运营商线路故障：通常月费内含免费维修（区间约 ¥0；确认无上门费 🔄）。
- If the modem is YOUR property and died: replacement **¥200–¥800** depending on GPON model (range, verify 🔄).
  若光猫是你自购且损坏：更换 **¥200–¥800**（区间，需核验 🔄）。
- Business-grade 4G/5G backup router (for failover): **¥800–¥3,000** one-time + **¥50–¥300/mo** data plan (range, market-dependent 🔄).
  商用 4G/5G 备份路由：一次性 **¥800–¥3000** + 月租 **¥50–¥300**（区间，随市场 🔄）。

**Prevention / 预防措施**
- Subscribe to a business plan with an **SLA + a backup 4G/5G link** (see `data/14` SLA clauses). Keep the modem on a UPS (see `data/13` weekly UPS self-test).
  签约带 SLA 的商用套餐 + 4G/5G 备份链路（见 `data/14` SLA 条款）。光猫接 UPS（见 `data/13` 周检 UPS）。
- Save the ISP 24h line-fault number in the front-desk phone as "网络报修" before you need it.
  把运营商 24h 报修号存前台手机为「网络报修」，平时就存好。

---

## #n02-payments-down-browsing-works / 付款断但能上网

**Self-check / 自查（说人话）**
- Symptom: staff can browse the web and use WeChat, but the POS / payment gateway / MMS cloud sync fails. This is usually a **DNS or specific-port** block, not a full outage.
  现象：能刷网页、用微信，但 POS/支付网关/会籍云同步失败。通常是 **DNS 或某个端口**被挡，不是全断。
- Open a normal site (e.g. a news site) on the POS tablet. If it loads but payment fails, the payment server's address or port is the problem.
  在 POS 平板上打开普通网站。若能开但支付失败，是支付服务器地址或端口的问题。
- Try switching the POS to phone hotspot for 2 minutes as a test (see failover below).
  把 POS 临时切到手机热点测 2 分钟（见下方 failover）。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT disable the firewall entirely to "make it work" — that exposes the whole club. Do NOT change DNS to an unknown public server on the main router without noting the original.
  不要为「能付就行」把防火墙全关——整店暴露。不要在主路由乱改 DNS 而不记录原值。

**Vendor call script / 报修话术（照着念）**
- To payment vendor: "我们的收银能上网，但支付网关报错 <错误码/截图>。请确认贵司支付接口域名和端口是否变更，是否你们服务端故障。我们需要一个工单号。"
- To ISP (if DNS suspected): "DNS 解析 <支付域名> 失败，其他网站正常，请检查是否局部 DNS 污染或限速。"

**Parts & cost hint / 备件与费用参考**
- Most causes are config, **¥0** to fix. A 4G failover SIM for the POS lane: **¥30–¥150/mo** (range 🔄).
  多为配置问题，修复 **¥0**。POS 专线的 4G 备线 SIM：**¥30–¥150/月**（区间 🔄）。

**Prevention / 预防措施**
- Put POS/payment on its own VLAN with a **fixed DNS (e.g. 8.8.8.8 / 1.1.1.1 as secondary)** and a 4G auto-failover (see `references/08` VLAN design).
  把 POS/支付放独立 VLAN，配固定 DNS（备用 8.8.8.8/1.1.1.1）+ 4G 自动 failover（见 `references/08` VLAN 设计）。
- Save the payment vendor's status-page URL; check it before calling (see `data/12` #s17 vendor-outage).
  存支付供应商状态页 URL，先查再打电话（见 `data/12` #s17 厂商故障）。

---

## #n03-wifi-slow-peak / 高峰 Wi-Fi 慢

**Self-check / 自查（说人话）**
- Slow only when the club is busy (evenings/weekends), fine at 10am. This is **capacity/concurrency**, not a fault.
  仅高峰（晚/周末）慢，上午 10 点正常。这是**容量/并发**问题，不是故障。
- Count how many devices are on: member phones + staff + cameras + IoT. A cheap router may choke above ~30–50 devices.
  数在线设备：会员手机+员工+摄像头+IoT。廉价路由 30–50 台以上就卡。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT just "buy a bigger antenna" — that rarely fixes concurrency. Do NOT add a second random router (causes double-NAT, see #n08).
  不要只买「更大天线」——基本不治并发。不要再加一个随机路由（会造成双 NAT，见 #n08）。

**Vendor call script / 报修话术（照着念）**
- To MSP/network vendor: "晚高峰约 <N> 台设备同时在线，Wi-Fi 延迟高、视频卡。请评估是否需要企业级 AP + 控制器，或增加 AP 点位。请给方案和报价区间。"

**Parts & cost hint / 备件与费用参考**
- Add 1–2 business APs: **¥600–¥2,500** each (range 🔄). Controller-based mesh for a full club: **¥3,000–¥15,000** (range, size-dependent 🔄).
  增 1–2 个商用 AP：每个 **¥600–¥2500**（区间 🔄）。全店控制器组 Mesh：**¥3000–¥15000**（区间，看面积 🔄）。

**Prevention / 预防措施**
- Deploy **enterprise APs with a controller** from day one for any club >150㎡ or >50 daily check-ins (FDMM L2+). Separate member-guest and staff-IoT SSIDs (see #n04).
  任何 >150㎡ 或日入场 >50 的店，开业即上**企业级 AP + 控制器**。会员访客与员工 IoT 分 SSID（见 #n04）。

---

## #n04-one-ssid-missing / 少了一个 Wi-Fi 名称

**Self-check / 自查（说人话）**
- You have two Wi-Fi names (e.g. "Club-Guest" and "Club-Staff") but one disappeared from the list. The other still works.
  你有两个 Wi-Fi 名（如 Club-Guest、Club-Staff），但少了一个，另一个正常。
- Log into the router/controller admin and check the SSID broadcast setting for that network — it may have been turned off or renamed.
  登路由/控制器后台，查该网络的 SSID 广播开关——可能被关或改名。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT create a new SSID with the old name and a new password — members' saved devices will conflict and you'll get a flood of "Wi-Fi broken" complaints.
  不要新建同名新密码的 SSID——会员已存设备会冲突，投诉爆棚。

**Vendor call script / 报修话术（照着念）**
- "控制器里 <SSID名> 广播关闭了，请远程帮我们重新开启，并确认不是固件 bug。"

**Parts & cost hint / 备件与费用参考**
- Usually **¥0** (config). If the AP broadcasting that SSID died: **¥600–¥2,500** (range 🔄).
  通常 **¥0**（配置）。若该 SSID 所在 AP 坏：换 **¥600–¥2500**（区间 🔄）。

**Prevention / 预防措施**
- Document all SSID names/passwords/VLAN tags in `data/20-micro-details-ledger.md`. Change only via the controller, never per-AP.
  把所有 SSID 名称/密码/VLAN 标签记到 `data/20` 微细节账。只在控制器改，绝不在单 AP 上改。

---

## #n05-captive-portal-loop /  captive portal 死循环

**Self-check / 自查（说人话）**
- Guest connects to Wi-Fi, gets the login page, enters phone/accepts, but the page reloads and asks again forever.
  访客连 Wi-Fi，跳登录页，输手机/点同意，页面刷新又来一遍。
- This is usually the portal server unreachable, or the device's "private MAC" / random MAC blocking its own session cookie.
  通常是 portal 服务器不可达，或设备的「私有 MAC/随机 MAC」挡掉了自己的会话 cookie。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT tell members to "turn off MAC randomization" as a fix for everyone — on some markets that breaks their privacy expectation. Offer a one-time bypass code instead.
  不要对所有人说「关掉随机 MAC」——部分市场这违背隐私预期。改为发一次性放行码。

**Vendor call script / 报修话术（照着念）**
- " captive portal 认证后跳转回登录页，疑似会话未保持。请检查 portal 与 RADIUS/认证服务连通，并给我们一个临时免认证码先让会员上网。"

**Parts & cost hint / 备件与费用参考**
- Usually **¥0** (vendor-side). If you self-host the portal on a tiny box that died: **¥500–¥2,000** (range 🔄).
  通常 **¥0**（厂商侧）。若自建 portal 小盒子坏：换 **¥500–¥2000**（区间 🔄）。

**Prevention / 预防措施**
- Use the **vendor-hosted captive portal** (not self-hosted) for L1–L2 clubs. Set session idle-timeout to a sane value (e.g. 4h) to avoid mid-workout drops.
  L1–L2 店用**厂商托管 portal**（别自建）。会话空闲超时设合理值（如 4 小时），避免锻炼中掉线。

---

## #n06-vlan-misconfig /  VLAN 配错（有人插错口）

**Self-check / 自查（说人话）**
- After "someone plugged a cable into the wrong port," strange things happen: cameras show on guest Wi-Fi, or staff PCs can't reach the MMS, or the gate VLAN is isolated.
  在「有人把线插错口」之后，怪事发生：摄像头出现在访客 Wi-Fi，或员工电脑连不上会籍系统，或闸机 VLAN 被隔离。
- Find the switch port map. A port meant for "cameras (VLAN 30)" may now carry "guest (VLAN 10)" traffic because the cable was moved.
  找交换机端口图。本应接「摄像头(VLAN30)」的口，因挪线现在跑「访客(VLAN10)」。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT renumber VLANs on a live switch during open hours — one typo isolates the gate or payment. Do this only at close (see `data/13` closing checklist).
  营业时间不要在运行中的交换机上改 VLAN——一个错字就隔离闸机或支付。只闭店后做（见 `data/13` 闭店清单）。

**Vendor call script / 报修话术（照着念）**
- "交换机端口 VLAN 归属被改动，导致 <现象>。请提供标准端口-VLAN 对照表，并远程帮我们按表复位。"

**Parts & cost hint / 备件与费用参考**
- Config fix **¥0–¥500** MSP visit (range 🔄). Managed switch if none: **¥1,000–¥6,000** (range 🔄).
  配置修复 **¥0–¥500** MSP 上门（区间 🔄）。若无网管交换：换 **¥1000–¥6000**（区间 🔄）。

**Prevention / 预防措施**
- **Label every port** with its VLAN in plain text at the patch panel. Lock the comms cabinet (see `references/16` physical security). Train staff: "only IT touches the cabinet."
  在配线架给每个口贴明文 VLAN 标签。锁好弱电柜（见 `references/16` 物理安全）。培训员工：「只有 IT 碰柜子」。

---

## #n07-dhcp-exhaustion /  DHCP 耗尽（会员手机吃光 IP）

**Self-check / 自查（说人话）**
- New devices can't get online, but devices that were already connected are fine. The DHCP pool (e.g. 192.168.1.2–100) ran out because every member phone grabbed an IP and never released it.
  新设备连不上，但已连的没事。DHCP 地址池（如 192.168.1.2–100）被吃光——会员手机每台占一个 IP 不释放。
- On the router, check "DHCP lease table" — if it shows ~100/100 used, that's the proof.
  路由后台看「DHCP 租约表」——若显示约 100/100 已用，即证据。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT just reboot the router to "clear it" during peak — you'll drop every connected member for 2 minutes and anger everyone. Shorten lease time instead.
  高峰不要为「清地址」重启路由——会让全体会员掉线 2 分钟。改为缩短租约时间。

**Vendor call script / 报修话术（照着念）**
- "DHCP 地址池 <范围> 已满，新设备获取不到 IP。请把租约时间改为 1–2 小时，并把池扩大到 /22 或加 VLAN 分段。"

**Parts & cost hint / 备件与费用参考**
- Config **¥0**. If you need a bigger router because the current one can't handle >100 leases: **¥800–¥4,000** (range 🔄).
  配置 **¥0**。若当前路由不支持 >100 租约需换：换 **¥800–¥4000**（区间 🔄）。

**Prevention / 预防措施**
- Set guest DHCP lease to **1–2 hours** and size the pool for 2× peak devices. Put guests on their own /22 subnet (see `references/08`).
  访客 DHCP 租约设 **1–2 小时**，地址池按峰值 2 倍预留。访客独立 /22 子网（见 `references/08`）。

---

## #n08-double-nat /  双 NAT（乱加路由）

**Self-check / 自查（说人话）**
- Someone added a random home router behind the club router "to get better Wi-Fi." Now port-forwarding, cameras and the gate IPsec tunnel stop working — two routers fight over the network.
  有人为「信号更好」在俱乐部路由后加了个家用路由。现在端口转发、摄像头、闸机 IPsec tunnel 全挂——两个路由抢网络。
- Symptom: you're behind two private networks (e.g. 192.168.1.x inside 10.0.0.x). Online "what is my IP" shows a private IP, or port checks fail.
  现象：你在两个私网里（如 192.168.1.x 套 10.0.0.x）。查「我的 IP」显示私网，或端口检测失败。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT enable "AP mode" blindly on the wrong box — you may kill the only DHCP and drop the whole club. Identify which device is the real gateway first.
  不要盲目把某台设成「AP 模式」——可能干掉唯一 DHCP 让全店断网。先确认哪台是真网关。

**Vendor call script / 报修话术（照着念）**
- "我们有两个路由串接导致双 NAT，端口转发和 IPsec tunnel 失效。请把后加的路由改成 AP/桥接模式，由主路由统一分配。"

**Parts & cost hint / 备件与费用参考**
- Config **¥0**. If you'd rather replace the weak router with a proper AP: **¥600–¥2,500** (range 🔄).
  配置 **¥0**。若干脆换掉弱路由为正经 AP：换 **¥600–¥2500**（区间 🔄）。

**Prevention / 预防措施**
- Rule: **only ONE router/gateway** per club. Extra coverage = APs in bridge mode, not new routers. Paint this rule on the cabinet door.
  规矩：**每店只有一个路由/网关**。要扩覆盖 = 桥接模式 AP，不是新路由。把这条写柜门上。

---

## #n09-ip-conflict /  IP 冲突

**Self-check / 自查（说人话）**
- One device keeps dropping off, and the router logs "duplicate IP" or two devices fight for the same address (e.g. someone set a static IP that the DHCP also handed out).
  某设备反复掉，路由日志「IP 冲突」，两台抢同一地址（如有人设了静态 IP，DHCP 又发出同一个）。
- Check the lease table for two MACs on one IP.
  查租约表是否两个 MAC 占同一 IP。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT assign static IPs to printers/gates by guessing — always use DHCP reservation (see #n15) so the router owns the table.
  不要靠猜给打印机/闸机设静态 IP——用 DHCP 保留（见 #n15），让路由掌握表。

**Vendor call script / 报修话术（照着念）**
- "IP <地址> 冲突，两台设备抢。请把 <设备> 改为 DHCP 保留地址，避免再冲突。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config.
  配置 **¥0**。

**Prevention / 预防措施**
- Centralize ALL fixed addresses as **DHCP reservations** with a note field ("Gate", "Receipt printer"). Never hand-set static IPs.
  所有固定地址统一用 **DHCP 保留**并加备注（「闸机」「小票机」）。绝不手设静态 IP。

---

## #n10-isp-outage-verify /  运营商故障核实与索赔

**Self-check / 自查（说人话）**
- Before claiming compensation, PROVE it's the ISP: modem PON/LOS red (see decoder), neighbor on same ISP also down, and your own gear rebooted clean.
  索赔前先自证是运营商：光猫 PON/LOS 红（见速查）、同运营商邻居也断、自家设备已干净重启。
- Note the **exact start time** and ask the ISP for the ticket number + confirmed fault.
  记下**确切开始时间**，向运营商要工单号 + 故障确认。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT accept "we fixed it" by phone without checking your own connection. Do NOT sign any "case closed" without the ETR honoured.
  别听电话说「修好了」就信，自己测。别在 ETR 未兑现时签「已解决」。

**Vendor call script / 报修话术（照着念）**
- "工单 <号>，故障始于 <时间>，持续 <时长>。按合同 SLA 我方有权申请服务补偿（service credit），请提供补偿流程。"
- EN: "Ticket <n>, outage started <time>, duration <x>. Per SLA we request a service-credit; please advise the process."

**Parts & cost hint / 备件与费用参考**
- Compensation is typically **1–7 days of fee credits** for business plans with SLA (range, contract-dependent 🔄). No SLA = usually nothing.
  带 SLA 的商用套餐通常赔 **1–7 天费用抵扣**（区间，看合同 🔄）。无 SLA 通常无赔偿。

**Prevention / 预防措施**
- Choose ISP plans **with a written SLA and service-credit clause** (see `data/14` SLA library). Log every outage in `data/16-freshness-ledger.md` for renewal negotiation.
  选**含书面 SLA 与服务抵扣条款**的套餐（见 `data/14` SLA 库）。每次故障记 `data/16` 保鲜账，用于续约谈判。

---

## #n11-4g5g-backup-wont-kick /  4G/5G 备份不自动切换

**Self-check / 自查（说人话）**
- You paid for a 4G/5G backup but when the main line died, nobody got internet. The failover didn't trigger.
  你买了 4G/5G 备份，但主线断时没人能上网，failover 没触发。
- Check: is the backup SIM active and topped up? Is "failover" enabled, or is it manual-only? Does the router see the cellular signal?
  查：备份 SIM 是否激活且有余额？failover 是「自动」还是「仅手动」？路由能否看到蜂窝信号？

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT leave the backup as the only link during a long outage without checking data caps — you may burn through the plan and get cut off mid-day.
  长断网时不要把备份当唯一链路而不看流量上限——可能一天烧光被掐。

**Vendor call script / 报修话术（照着念）**
- "主线路断了，4G 备份未自动切换。请确认 failover 策略为自动、检测阈值、以及 SIM 状态。我们需要它现在手动切到备份。"

**Parts & cost hint / 备件与费用参考**
- Failover router **¥800–¥3,000** + data **¥50–¥300/mo** (range 🔄). Misconfig fix usually **¥0**.
  切换路由 **¥800–¥3000** + 流量 **¥50–¥300/月**（区间 🔄）。配置错修复多 **¥0**。

**Prevention / 预防措施**
- Test failover **monthly** (unplug the main line for 1 minute at close, confirm Wi-Fi survives) — see `data/13` monthly drill. Set data cap alerts.
  每月测 failover（闭店拔主线 1 分钟，确认 Wi-Fi 还在）——见 `data/13` 月测。设流量预警。

---

## #n12-tunnel-hq-down /  连总部 IPsec tunnel 断

**Self-check / 自查（说人话）**
- Branch club can't reach HQ systems (central MMS, shared drive). Local internet is fine; only the tunnel to HQ is down.
  分店连不上总部系统（中央会籍、共享盘）。本地网正常，只连总部的隧道断。
- Check the IPsec tunnel status light on the branch router; try pinging HQ IP from the router. If local browse works but HQ IP fails, it's the tunnel or HQ side.
  查分店路由 IPsec tunnel 状态灯；从路由 ping 总部 IP。本地能刷但总部 IP 不通 = 隧道或总部侧问题。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT open a wide port-forward to HQ "to bypass IPsec tunnel" — that's a security incident path. Keep the tunnel.
  不要为「绕过 IPsec tunnel」开大端口转发到总部——那是安全事件通道。保留隧道。

**Vendor call script / 报修话术（照着念）**
- To HQ IT / MSP: "分店 <名> 本地网正常，但到总部 <IP/域名> 的 IPsec tunnel 隧道 down，隧道状态灯红。请查总部端或重派隧道配置。"

**Parts & cost hint / 备件与费用参考**
- Usually **¥0** (config/tunnel reset). SD-WAN appliance if scaling: **¥3,000–¥20,000** per site (range, L4 🔄).
  通常 **¥0**（配置/隧道重派）。若上 SD-WAN：**每站点 ¥3000–¥20000**（区间，L4 🔄）。

**Prevention / 预防措施**
- Monitor the tunnel with a **heartbeat alert** to HQ (ping every 1 min, alert on loss >3). Keep a documented fallback path (see `references/16` resilience).
  用**心跳告警**监控隧道（每分钟 ping，丢 3 次即报警）。保留书面 fallback 路径（见 `references/16` 韧性）。

---

## #n13-port-forward-broke-camera /  端口转发坏了，摄像头看不了

**Self-check / 自查（说人话）**
- After a router change/reboot, remote camera view (on your phone off-site) stopped working, but cameras record locally fine.
  路由更换/重启后，手机远程看摄像头没了，但本地录像正常。
- The port-forward rule (e.g. WAN:8000 → NVR:80) was lost because the new router has a different UI, or the NVR IP changed (see #n15).
  端口转发规则（如 WAN:8000→NVR:80）丢了——新路由界面不同，或 NVR IP 变了（见 #n15）。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT expose camera ports to the open internet without authentication — that's how camera feeds get compromised (see `references/12` CCTV compliance + HI-5).
  不要无认证把摄像头端口暴露公网——摄像头被入侵就这么来的（见 `references/12` 合规 + HI-5）。

**Vendor call script / 报修话术（照着念）**
- "路由重启后摄像机远程端口转发丢失，请帮我们重配 WAN:<端口> → NVR <内网IP>:<端口>，并启用强密码/HTTPS。"

**Parts & cost hint / 备件与费用参考**
- Config **¥0**. A cloud-NVR that needs no port-forward: **¥1,500–¥8,000** (range 🔄).
  配置 **¥0**。免端口转发的云 NVR：**¥1500–¥8000**（区间 🔄）。

**Prevention / 预防措施**
- Use a **cloud/NVR with encrypted tunnel** (no manual port-forward). If port-forward is required, pair with DHCP reservation (#n15) + strong creds + allow-list.
  用**带加密隧道的云 NVR**（免手动转发）。若必须转发，配合 DHCP 保留（#n15）+ 强密码 + 白名单。

---

## #n14-new-device-cant-join-staff-wifi /  新设备连不上员工 Wi-Fi

**Self-check / 自查（说人话）**
- A new staff phone/laptop can't join the staff SSID while others can.
  新员工手机/笔记本连不上员工 SSID，别人能。
- Check: is MAC-filtering on? Is the device's "private address" feature randomizing its MAC and getting blocked? Is the staff SSID hidden?
  查：是否开了 MAC 过滤？设备的「私有地址」是否在随机 MAC 被挡？员工 SSID 是否隐藏？

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT disable MAC filtering globally to "fix one device" — that weakens control. Add the device's real MAC to the allow-list instead.
  不要为「修一台」全局关 MAC 过滤——削弱管控。把该设备真实 MAC 加入白名单。

**Vendor call script / 报修话术（照着念）**
- "请帮我们把 <设备> 的 MAC 加入员工 SSID 白名单，并确认隐藏 SSID 是否需要手动输入。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config.
  配置 **¥0**。

**Prevention / 预防措施**
- Keep a **staff device register** (MAC + name) in `data/20`. Onboard new devices at close, not during rush.
  在 `data/20` 维护**员工设备登记表**（MAC+姓名）。新员工设备闭店时登记，别在高峰。

---

## #n15-printer-offline-after-reboot /  路由重启后打印机离线

**Self-check / 自查（说人话）**
- After a router reboot, the receipt printer shows "offline" at the POS even though it's plugged in and powered.
  路由重启后，小票机在 POS 上显示「离线」，但插着电。
- The printer had a static IP that now collides or fell outside the new DHCP range; or the POS points to the old IP.
  打印机原是静态 IP，现在冲突或落在新 DHCP 范围外；或 POS 指向旧 IP。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT keep using static IPs on printers — this is exactly why. Convert to DHCP reservation now.
  不要继续给打印机用静态 IP——这正是病根。现在改成 DHCP 保留。

**Vendor call script / 报修话术（照着念）**
- "打印机原静态 IP 冲突，请改为 DHCP 保留（MAC <xx:xx> → 固定 <IP>），并同步 POS 打印设置。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config.
  配置 **¥0**。

**Prevention / 预防措施**
- **All fixed devices = DHCP reservation** (see #n09). Document the reservation table in `data/20`. Never hand-set static IPs.
  **所有固定设备 = DHCP 保留**（见 #n09）。保留表记 `data/20`。绝不手设静态 IP。

---

## #n16-speedtest-interpret /  speedtest 怎么看懂（非 IT 版）

**Self-check / 自查（说人话）**
- Run a speed test (e.g. speedtest.net or your ISP's) on a wired laptop during the problem. Three numbers matter: **Download / Upload / Ping**.
  故障时段用插网线的笔记本跑测速（speedtest.net 或运营商测速）。三个数关键：**下载 / 上传 / 延迟(Ping)**。
- Download = how fast pages/videos load. Upload = how fast you send (cloud sync, live stream). Ping = reaction time; high ping = laggy even if download is big.
  下载=网页/视频加载快慢。上传=你发出去多快（云同步、直播）。Ping=反应时间；Ping 高=即便下载大也卡。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT compare Wi-Fi speed to the plan's wired speed — Wi-Fi is always lower. Test wired for a fair read.
  不要拿 Wi-Fi 速度和套餐有线速度比——Wi-Fi 本来就低。要公平就测有线。

**Vendor call script / 报修话术（照着念）**
- "有线测速：下载 <X> / 上传 <Y> / Ping <Z> Mbps，套餐应为 <套餐值>。请解释差距并排查。"

**Parts & cost hint / 备件与费用参考**
- If you're at <50% of plan consistently: may be ISP throttling or bad cable — **¥0–¥500** (range 🔄).
  若长期 <套餐 50%：可能限速或线坏——**¥0–¥500**（区间 🔄）。

**Prevention / 预防措施**
- Keep a **baseline speed log** (test wired once a month) in `data/16` so you can prove degradation to the ISP.
  在 `data/16` 留**测速基线**（每月有线测一次），以便向运营商证明劣化。

---

## #n17-bufferbloat-livestream /  直播课缓冲膨胀

**Self-check / 自查（说人话）**
- During a live-streamed class, the stream stutters for members even though download speed is fine.
  直播课时会员端卡顿，但下载速度正常。
- This is **bufferbloat**: when someone uploads a big file or the backup runs, latency spikes. The live stream (which needs low, steady ping) suffers.
  这是**缓冲膨胀**：有人传大文件或备份运行时延迟飙升。直播（要低且稳的 ping）就遭殃。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT throttle the live stream's own bandwidth to "fix" it — throttle the bulk uploaders instead (QoS).
  不要为「修」去限制直播自身带宽——去限大上传源（QoS）。

**Vendor call script / 报修话术（照着念）**
- "请开启 QoS / Smart Queue，把直播和收银标记为最高优先级，备份和同步降级到空闲时段。"

**Parts & cost hint / 备件与费用参考**
- Usually **¥0** (QoS config). If the router is too weak for SQM: upgrade **¥800–¥4,000** (range 🔄).
  通常 **¥0**（QoS 配置）。若路由太弱不支持 SQM：换 **¥800–¥4000**（区间 🔄）。

**Prevention / 预防措施**
- Enable **QoS / fq_codel SQM** at provisioning. Schedule backups at 3am, not class time (see `data/13` monthly patch day off-peak).
  部署即开 **QoS/fq_codel SQM**。备份排凌晨 3 点，别排上课时段（见 `data/13` 月维护错峰）。

---

## #n18-cable-tester-basics /  测线仪入门

**Self-check / 自查（说人话）**
- If a wall port or device "has no link" but the cable looks fine, a **cable tester** (¥30–¥200) shows which of the 8 wires inside are broken or crossed.
  若墙面口或设备「无连接」但线看着没事，用**测线仪**（¥30–¥200）看 8 根芯哪根断或错序。
- Two lights run 1–8 in order at both ends = good. A missing number = that wire is broken.
  两端灯按 1–8 顺序亮=好。缺号=那根断。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT pull cables hard through walls yourself — you'll shred them. Call a cabling contractor for in-wall runs (see #n19).
  不要自己硬拉墙内线——会拉断。墙内布线叫布线师傅（见 #n19）。

**Vendor call script / 报修话术（照着念）**
- To cabling contractor: "请带 Fluke 级测试仪来，验收 <N> 个信息点，要求全 8 芯通且达标 Cat6。"

**Parts & cost hint / 备件与费用参考**
- Hand tester **¥30–¥200**; pro certifier rental **¥200–¥800/day** (range 🔄). Re-termination per drop **¥50–¥200** (range 🔄).
  手持测线仪 **¥30–¥200**；专业认证仪日租 **¥200–¥800**（区间 🔄）。单点重新打线 **¥50–¥200**（区间 🔄）。

**Prevention / 预防措施**
- At fit-out, require the contractor to **certify every drop** and hand over a test report. Keep it in `data/20`.
  装修时要求师傅**逐点认证**并交测试报告，存 `data/20`。

---

## #n19-call-cabling-vs-isp-vs-msp /  该叫布线 / 运营商 / MSP

**Self-check / 自查（说人话）**
- **Cabling contractor / 布线师傅**: physical cable broken, wall port dead, new points needed, patch panel mess.
  **布线师傅**：线断了、墙口死、要加信息点、配线架乱。
- **ISP / 运营商**: red light on modem, no signal from street, speed below plan at the demarcation point.
  **运营商**：光猫红灯、外面无信号、分界点速度不达标。
- **MSP / 网络服务商**: config, VLAN, Wi-Fi design, firewall, IPsec tunnel, recurring management.
  **MSP**：配置、VLAN、Wi-Fi 设计、防火墙、IPsec tunnel、长期托管。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT let the cabling contractor "also configure your firewall" unless they are a real MSP — misconfigured security is worse than no config.
  别让布线师傅「顺便配防火墙」除非他是真 MSP——错误的安全配置比没有更糟。

**Vendor call script / 报修话术（照着念）**
- "先判断：是物理线（找布线）还是配置（找 MSP）还是信号（找运营商）。按 #n01 解码器先定位再叫人。"

**Parts & cost hint / 备件与费用参考**
- Cabling: **¥50–¥200/point**; ISP business visit often free under SLA; MSP retainer **¥500–¥5,000/mo** (range 🔄).
  布线：每点 **¥50–¥200**；运营商商访常免费（SLA 内）；MSP 托管 **¥500–¥5000/月**（区间 🔄）。

**Prevention / 预防措施**
- Keep three saved numbers (cabling / ISP / MSP) in the front-desk phone. Know which is which before panic.
  前台手机存三个号（布线/运营商/MSP）。慌之前先分清该打哪个。

---

## #n20-quotation-red-flags /  网络供应商报价红旗

**Self-check / 自查（说人话）**
- Red flags in a network quote: no itemized parts (just "network solution ¥X"), no model numbers, no SLA, no warranty period, "free install" but 3-year lock-in, only ONE vendor offered.
  报价红旗：不分项（只写「网络方案 ¥X」）、无型号、无 SLA、无保修期、「免费安装」却绑 3 年、只给一家。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT sign a network contract with no data-export / exit clause — you'll be locked (see `data/14` exit clause + HI-8).
  不要签无数据导出/退出条款的网络合同——会被锁死（见 `data/14` 退出条款 + HI-8）。

**Vendor call script / 报修话术（照着念）**
- "请拆项报价（设备型号+数量+单价+人工），并写明 SLA、保修、退出与数据返还条款。我们至少比 3 家。"

**Parts & cost hint / 备件与费用参考**
- Always get **≥3 quotes** incl. one local + one low-cost option (HI-8). Typical club LAN: **¥3,000–¥20,000** (range 🔄).
  永远**≥3 家比价**，含本地 + 低成本选项（HI-8）。典型场馆局域网：**¥3000–¥20000**（区间 🔄）。

**Prevention / 预防措施**
- Use the `data/14` SLA clause library + `references/05` money questions before signing. Never pay 100% upfront.
  签约前用 `data/14` SLA 条款库 + `references/05` 钱的问题。绝不 100% 预付。

---

## #n21-dns-poisoning-intermittent /  间歇性 DNS 污染

**Self-check / 自查（说人话）**
- Some sites load, some show "can't be reached" or a weird ad page intermittently. This smells like DNS hijack/poisoning.
  有的站能开，有的间歇「无法访问」或跳奇怪广告页。像 DNS 劫持/污染。
- On the POS, try a different DNS (set temporarily to 8.8.8.8) — if payment then works, DNS was the culprit.
  POS 上临时改 DNS 为 8.8.8.8 测——若支付好了，DNS 是元凶。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT keep a hijacked DNS "because it's faster" — it can silently redirect payments to a fake page (fraud). Switch and report.
  不要因「更快」留着被劫持 DNS——它可能静默把支付导到假页（诈骗）。换掉并上报。

**Vendor call script / 报修话术（照着念）**
- "我们怀疑 DNS 被劫持，请改为可信 DNS 并开启 DNSSEC/DoH，排查局域网是否有恶意设备。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config; if a device is the source, removal **¥0–¥500** (range 🔄).
  配置 **¥0**；若某设备是源头，清除 **¥0–¥500**（区间 🔄）。

**Prevention / 预防措施**
- Use **DNS over HTTPS / DNSSEC** at the router, and monitor for unknown DNS servers pushed to clients.
  路由开 **DoH/DNSSEC**，监控是否有未知 DNS 被下发。

---

## #n22-switch-loop-broadcast-storm /  交换机环路广播风暴

**Self-check / 自查（说人话）**
- Suddenly everything slows to a crawl or the whole network collapses, and you find two cables both plugged between the same two switches (a loop).
  突然全网卡死或全崩，发现两根线把同一对交换机都插上了（成环）。
- Unplug one of the loop cables → network recovers in seconds. That's the proof.
  拔掉一根环线 → 几秒恢复。即证据。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT leave spare cables dangling in the cabinet — someone will "helpfully" plug both ends. Enable loop protection (STP) on managed switches.
  别在柜里留悬空多余线——会有人「好心」两头都插。网管交换开环路保护（STP）。

**Vendor call script / 报修话术（照着念）**
- "请在所有接入交换开启 STP / loop guard，避免误插成环导致广播风暴。"

**Parts & cost hint / 备件与费用参考**
- **¥0** (enable STP). Managed switch if none: **¥1,000–¥6,000** (range 🔄).
  配置 **¥0**（开 STP）。若无网管交换：换 **¥1000–¥6000**（区间 🔄）。

**Prevention / 预防措施**
- Enable **STP/loop guard** + cabinet locked + ports labeled. One cable per intended link only.
  开 **STP/环路保护** + 锁柜 + 端口标签。每链路只一根线。

---

## #n23-poe-camera-all-down /  PoE 交换坏，摄像头全掉

**Self-check / 自查（说人话）**
- All cameras on one switch went dark at once, but the NVR is fine. They're powered by the switch (PoE) — that switch lost power or died.
  同一交换下的摄像头同时黑，NVR 正常。它们由交换供电（PoE）——那台交换断电或坏。
- Check the PoE switch's power light and its own uplink. If its fan is dead/no light, it's the switch.
  查 PoE 交换电源灯与上联。若风扇停/无灯，是交换。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT daisy-chain too many PoE devices on one small switch — overload kills them. Size PoE budget = sum of device watts ×1.3.
  不要在一台小交换上串太多 PoE 设备——过载烧。PoE 预算 = 设备总瓦 ×1.3。

**Vendor call script / 报修话术（照着念）**
- "PoE 交换 <型号/位置> 断电，<N> 路摄像全掉。请带同规格备机现场更换，并核算 PoE 功率余量。"

**Parts & cost hint / 备件与费用参考**
- PoE switch **¥800–¥5,000** (range 🔄). Spare on-site for 24h clubs strongly advised: **¥800–¥5,000** (range 🔄).
  PoE 交换 **¥800–¥5000**（区间 🔄）。24h 店强烈建议现场备机：**¥800–¥5000**（区间 🔄）。

**Prevention / 预防措施**
- Keep a **cold-spare PoE switch** for 24h/unmanned clubs (HI-2 safety). UPS on the switch. Size PoE budget with headroom.
  24h/无人店留**冷备 PoE 交换**（HI-2 安全）。交换接 UPS。PoE 预算留余量。

---

## #n24-firmware-update-bricked-router /  固件升级变砖

**Self-check / 自查（说人话）**
- During a router firmware update it lost power / hung, and now it won't boot (all lights frozen or off).
  路由固件升级时断电/卡死，现在不开机（灯全冻或全灭）。
- Unplug, wait 60s, plug, hold the reset only if the vendor doc says a recovery mode exists. Otherwise it's bricked.
  拔电等 60 秒再插，仅当厂商文档说有恢复模式才按复位。否则已变砖。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT update router firmware during open hours. Do NOT interrupt power mid-update. Schedule at close (see `data/13` patch day).
  营业时间不要升固件。升级中途不要断电。排闭店后（见 `data/13` 维护日）。

**Vendor call script / 报修话术（照着念）**
- "固件升级中断导致路由无法启动，请指导 TFTP 恢复或带备机现场救。我们需尽快恢复营业网络。"

**Parts & cost hint / 备件与费用参考**
- Recovery usually **¥0** if you have a backup config file. New router **¥800–¥4,000** (range 🔄).
  有配置备份多 **¥0**。新路由 **¥800–¥4000**（区间 🔄）。

**Prevention / 预防措施**
- **Back up router config** before every update; update at close only; keep a spare or config file in `data/20`.
  每次升级前**备份路由配置**；只闭店升级；`data/20` 留备机或配置文件。

---

## #n25-mtu-mismatch-tunnel /  MTU 不匹配导致 IPsec tunnel 卡

**Self-check / 自查（说人话）**
- IPsec tunnel connects but some things hang (big files, certain pages) while small traffic works. Classic MTU mismatch (packets too big, get silently dropped).
  IPsec tunnel 连上了但大文件/某些页卡，小流量正常。典型 MTU 不匹配（包太大被静默丢）。
- From the router, ping with "do not fragment" + size 1400/1472 to find the max that works, then set MTU accordingly.
  从路由 ping 加「不分片」+ 大小 1400/1472，找能通的最大值，据此设 MTU。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT set MTU to 1492 blindly on all links — cellular vs fibre differ. Measure per link.
  不要所有链路盲目设 1492——蜂窝和光纤不同。逐链路测。

**Vendor call script / 报修话术（照着念）**
- "IPsec tunnel 大包不通，疑似 MTU 不匹配，请协助按链路测算并设值。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config.
  配置 **¥0**。

**Prevention / 预防措施**
- Document per-link MTU in `data/20`. Standardize on the measured value at provisioning.
  在 `data/20` 记逐链路 MTU。部署即按测量值固化。

---

## #n26-wifi-channel-congestion /  Wi-Fi 信道拥堵

**Self-check / 自查（说人话）**
- In a mall or dense building, Wi-Fi is slow for everyone, even off-peak. Neighbor APs crowd the same channel (like 20 radios on channel 6).
  商场/密集楼里全员慢，即便非高峰。邻居 AP 挤同一信道（像 20 个电台都在 6 信道）。
- Use a Wi-Fi analyzer app (free) to see channel overlap; switch to a less crowded channel or let the controller auto-pick.
  用免费 Wi-Fi 分析 App 看信道重叠；切到不挤的信道，或让控制器自动选。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT max out transmit power to "overpower" neighbors — that increases interference for everyone including you. Use moderate power + more APs.
  不要为「压过」邻居把功率拉满——加剧互相干扰。用适中功率 + 更多 AP。

**Vendor call script / 报修话术（照着念）**
- "周边 AP 信道拥堵，请开启自动信道选择（ACS）并评估增加 AP 点位。"

**Parts & cost hint / 备件与费用参考**
- Config **¥0**; extra AP **¥600–¥2,500** (range 🔄).
  配置 **¥0**；增 AP **¥600–¥2500**（区间 🔄）。

**Prevention / 预防措施**
- Use **controller-based auto-channel (ACS)** + 5GHz preference for dense sites. Survey at fit-out.
  用**控制器自动信道（ACS）** + 密集场所优先 5GHz。装修时做勘测。

---

## #n27-guest-network-leaks-internal /  访客网漏到内网

**Self-check / 自查（说人话）**
- A guest on the "Club-Guest" Wi-Fi can reach the staff PC or the MMS IP. The guest VLAN is not isolated from the internal one.
  访客在「Club-Guest」竟能访问员工电脑或会籍系统 IP。访客 VLAN 没和内网隔离。
- From a guest device, try to ping the MMS/internal gateway IP. If it replies, isolation failed.
  用访客设备 ping 会籍/内网网关 IP，若通，隔离失败。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT run guests and staff on the same network "for simplicity" — that's a data-breach path (HI-8, `references/16`).
  不要为「省事」让访客员工同网——那是数据泄露通道（HI-8、`references/16`）。

**Vendor call script / 报修话术（照着念）**
- "访客 VLAN 未隔离，可访问内网 <IP>。请启用 client isolation / 访客隔离，并确认 guest 仅能出公网。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config (on managed gear). If gear can't isolate: upgrade **¥1,000–¥6,000** (range 🔄).
  配置 **¥0**（网管设备）。若设备不能隔离：升级 **¥1000–¥6000**（区间 🔄）。

**Prevention / 预防措施**
- Enforce **client isolation + guest VLAN with no route to internal** at design time (see `references/08`). Audit quarterly (`data/13`).
  设计即强制**客户端隔离 + 访客 VLAN 不通内网**（见 `references/08`）。季度审计（`data/13`）。

---

## #n28-certificate-expired-captive /  证书过期，captive 弹警告

**Self-check / 自查（说人话）**
- Guest portal shows "Your connection is not private" / red lock because the portal's TLS certificate expired.
  访客 portal 显示「连接非私密」/ 红锁，因为 portal 的 TLS 证书过期。
- Check the certificate expiry date in the controller; renew it.
  查控制器里证书到期日，续。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT tell members to "ignore the warning and proceed" as standard practice — that trains them to click through real phishing.
  不要常规让会员「忽略警告继续」——那会教会他们点真钓鱼。

**Vendor call script / 报修话术（照着念）**
- " captive portal 证书于 <日期> 过期，请协助续签并开启自动续期。"

**Parts & cost hint / 备件与费用参考**
- Cert often **¥0** (Let's Encrypt auto). Paid cert **¥200–¥2,000/yr** (range 🔄).
  证书常 **¥0**（Let's Encrypt 自动）。付费证书 **¥200–¥2000/年**（区间 🔄）。

**Prevention / 预防措施**
- Use **auto-renewing certs (ACME)**; calendar a check 30 days before expiry in `data/13` annual review.
  用**自动续期证书（ACME）**；`data/13` 年检里到期前 30 天设提醒。

---

## #n29-rogue-ap-neighbor /  邻居私接 AP 干扰

**Self-check / 自查（说人话）**
- A new "FREE Wi-Fi" or a neighbor's router appears and your members keep dropping. Someone plugged an AP somewhere nearby on your channel.
  出现新「FREE Wi-Fi」或邻居路由，会员老掉。附近有人在你信道上私接 AP。
- Wi-Fi analyzer shows a strong unknown SSID on your channel.
  分析 App 显示你信道上有强未知 SSID。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT try to "jam" or overpower the neighbor's AP — illegal in most markets. Use 5GHz / different channel / report to building mgmt.
  不要去「干扰」或压邻居 AP——多数市场违法。用 5GHz/换信道/报物业。

**Vendor call script / 报修话术（照着念）**
- To building mgmt: "请协调 <楼层/铺位> 的 AP 信道，避免与我店 2.4G 冲突；必要时请其改为 5G。"

**Parts & cost hint / 备件与费用参考**
- Usually **¥0** (channel change). Shielding/5G gear **¥600–¥2,500** (range 🔄).
  常 **¥0**（换信道）。屏蔽/5G 设备 **¥600–¥2500**（区间 🔄）。

**Prevention / 预防措施**
- Prefer **5GHz** for staff; coordinate channels with building at fit-out; keep a channel plan in `data/20`.
  员工优先 **5GHz**；装修与物业协调信道；`data/20` 留信道规划。

---

## #n30-sip-voip-calls-drop /  SIP 电话断线

**Self-check / 自查（说人话）**
- VOIP desk phone or softphone drops calls after ~30s, or can't hear one side. Classic SIP ALG / NAT issue.
  桌面 VOIP 或软电话约 30 秒掉线，或单方无声。典型 SIP ALG/NAT 问题。
- Toggle SIP ALG off in the router; ensure UDP ports for RTP are open.
  路由关掉 SIP ALG；确保 RTP 的 UDP 端口开放。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT open all UDP ports "to fix audio" — scope only the RTP range the vendor gives.
  不要为「修声音」全开 UDP——只开供应商给的 RTP 范围。

**Vendor call script / 报修话术（照着念）**
- "VOIP 30 秒断线，疑似 SIP ALG/NAT，请关 ALG 并开放 RTP <端口范围>。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config.
  配置 **¥0**。

**Prevention / 预防措施**
- At provisioning, set SIP ALG **off** and whitelist the VOIP provider's RTP range. Document in `data/20`.
  部署即关 SIP ALG 并放行 VOIP 商 RTP 范围。记 `data/20`。

---

## #n31-iot-devices-drop-wifi /  IoT 设备老掉 Wi-Fi

**Self-check / 自查（说人话）**
- Smart locks, body scanners, treadmills' IoT module drop off Wi-Fi randomly. They often only support 2.4GHz and old security (WPA/WEP).
  智能锁、体测仪、跑步机 IoT 模块随机掉。它们常只支持 2.4G 和老安全（WPA/WEP）。
- Confirm the SSID they join is 2.4GHz, not 5GHz, and uses a compatible security mode.
  确认它们连的 SSID 是 2.4G 而非 5G，且安全模式兼容。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT lower the whole club's Wi-Fi security to WEP "so the lock works" — that breaks member-data protection. Put IoT on a separate low-security VLAN instead.
  不要为「锁能用」把全店 Wi-Fi 降到 WEP——破坏会员数据保护。把 IoT 放独立低安全 VLAN。

**Vendor call script / 报修话术（照着念）**
- "请为 IoT 设备开一个独立 2.4G SSID（VLAN），仅放行其所需端口，不与会员网同安全域。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config (VLAN). IoT gateway if needed **¥300–¥1,500** (range 🔄).
  配置 **¥0**（VLAN）。若需 IoT 网关 **¥300–¥1500**（区间 🔄）。

**Prevention / 预防措施**
- Design an **IoT-only VLAN/SSID (2.4G)** at fit-out; isolate from member & staff data (HI-8, `references/08`).
  装修即设计**IoT 专用 VLAN/SSID(2.4G)**；与会员/员工数据隔离（HI-8、`references/08`）。

---

## #n32-subnet-full-cant-add-device /  子网满，加不了新设备

**Self-check / 自查（说人话）**
- You bought a new device but "can't add it" — the subnet (e.g. 192.168.1.0/24 = max 254 devices) is full.
  买了新设备却「加不进」——子网满了（如 192.168.1.0/24 最多 254 台）。
- Count leases; if near 254, you've hit the ceiling.
  数租约；若近 254，到顶了。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT just change the mask to /16 on a live network during hours — you'll create ARP storms. Plan a maintenance window.
  营业时间不要直接改掩码成 /16——会引发 ARP 风暴。排维护窗口。

**Vendor call script / 报修话术（照着念）**
- "子网 /24 已满，请把 guest 或 IoT 移到独立 /22，或在闭店后扩网段。"

**Parts & cost hint / 备件与费用参考**
- **¥0** config (at close).
  配置 **¥0**（闭店后）。

**Prevention / 预防措施**
- Size subnets for **3× expected devices** at design; split guest/IoT/staff early (`references/08`).
  设计即按**预期 3 倍设备**留子网；早分访客/IoT/员工（`references/08`）。

---

## G13 Tri-Perspective Note / G13 三视角覆盖说明

**Architect (架构师视角)**: Network faults map to Cluster D. The five-segment entries give zero-basis operators a reproducible decision path; every entry ties to FDMM level and, where relevant, to VLAN/security design in `references/08` and `references/16`. Red-light/stop-line items enforce HI-2 (safety) and HI-8 (minimization/isolation).
**架构师视角**：网络故障归属集群 D。五段式给 0 基础经营者可复用的决策路径；每条锚定 FDMM 层级，并在相关处联 `references/08`/`references/16` 的 VLAN/安全设计。停手线落实 HI-2（安全）与 HI-8（最小化/隔离）。

**Operator (运营者视角)**: The one-page internet-down flow is printable and pinned at the desk — the shortest path from "we're down" to "ticket number in hand." Costs are directional ranges so the owner can budget without false precision.
**运营者视角**：断网一页通可打印贴前台——从「断了」到「拿到工单号」的最短路径。费用为方向性区间，老板可估预算而不被虚假精确误导。

**Member (会员视角)**: Most network faults are invisible if handled fast; the captive-portal, guest-isolation and certificate entries protect member privacy and data (HI-8, `references/12`). A 4G/5G backup and monthly failover test keep classes and check-in working even when the line is down.
**会员视角**：多数网络故障若处理快则无感；captive portal、访客隔离、证书条目保护会员隐私与数据（HI-8、`references/12`）。4G/5G 备份 + 月测 failover 让断线时上课与入场仍正常。

---

*Legal Notice / 法律声明 · Disclaimer / 免责声明 · Friendly Reminder / 温馨提示 · Author / 作者信息 — see SKILL.md output block. / 见 SKILL.md 输出规范块。*
