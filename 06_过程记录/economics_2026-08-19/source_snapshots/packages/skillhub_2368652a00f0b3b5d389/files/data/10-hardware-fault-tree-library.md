# Hardware Fault Tree Library / 硬件故障树库

> **Cluster / 集群**: C (Hardware ×12 categories) · A (Physical zones)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify every 90 days; vendor prices and model names are volatile — run `tools/04` before relying on any single figure. / 每 90 天复核；供应商价格与型号易变，引用具体数字前先跑 `tools/04`。
> **Cross-references / 交叉引用**: `data/13-inspection-and-maintenance-calendar` (prevention cadence) · `references/09-iot-and-open-protocols` (FTMS/Bluetooth) · `data/12-software-fault-tree-library` (integration faults, payments) · `references/08-network-and-infrastructure` (D1 dual-ISP failover) · `references/12-biometrics-and-cctv` (retention per market) · `references/10-apac-compliance-east-asia-oceania` (HI-1/4/5 legal basis)
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them. / 标注 🔄 的事实易变——引用前先跑 `tools/04`。

---

## How to read this file / 使用说明

Every fault entry uses the **five-segment structure / 五段式**:
1. **Self-check / 自查** — plain words, numbered steps a zero-basis person can do safely. / 说人话，0 基础可安全操作。
2. **Stop-line / 停手线** — when to STOP: electrical, warranty-void, safety risks (**bold**). / 何时绝不能再动。
3. **Vendor call script / 报修话术** — verbatim sentences; have model, serial, error code, photos ready. / 照着念；备好型号、序列号、错误码、照片。
4. **Parts & cost hint / 备件与费用参考** — RANGES only, marked "directional, varies by market". / 仅区间，标「方向性，随市场浮动」。
5. **Prevention / 预防** — maintenance habit + link to `data/13` calendar. / 保养习惯并链到 `data/13` 日历。

Anchors are kebab-case: `#c{NN}-{device}-{E##}-{symptom}`. Every recommendation is L0-friendly unless noted. / 锚点为 kebab 格式；除特别标注外均面向 L0 门店。

---

<a id="universal-triage"></a>
## Universal First 5 Minutes Triage / 通用「前 5 分钟」分流

**English / 英文**
When ANY hardware fault appears, run this order before touching anything:
1. **Is anyone unsafe?** Injury, smoke, spark, water on a powered device, blocked exit → STOP, evacuate/secure, call emergency number. Life first. / 有人不安全？受伤、冒烟、火花、带电设备进水、出口被堵 → 停，撤离/保护现场，打急救电话。生命第一。
2. **Power?** Is the device powered at all? Check the wall socket, power strip, and breaker — not just the device button. / 通电吗？查墙插、插线板、空开，不只是设备开关。
3. **Cable?** Loose, chewed, wet, or wrong cable? Re-seat firmly; replace visibly damaged cables. / 线缆？松脱、咬断、进水、错线？重插紧，明显损坏的更换。
4. **Restart order** (only after 1–3 are safe): peripheral → device → network switch → router → server, waiting 30s between each. / 重启顺序（仅在前三步安全后）：外设→设备→交换机→路由器→服务器，每级间隔 30 秒。
5. **Escalate** if unresolved in 5 min or if it hits a stop-line. Use the ladder below. / 5 分钟未解或触停手线 → 按下方层级上报。

**中文 / 中文**
任何硬件故障出现，先按此顺序，再动手：
1. **有人不安全吗？** 受伤、冒烟、火花、带电设备进水、出口被堵 → 停，撤离/保护现场，打急救电话。生命第一。
2. **通电吗？** 设备到底有没有电？查墙插、插线板、空开——不只是设备按钮。
3. **线缆？** 松、被咬、湿、接错？重插紧；明显损坏的换。
4. **重启顺序**（仅当前三步安全后）：外设→设备→交换机→路由器→服务器，每级等 30 秒。
5. **上报**：5 分钟未解或触停手线，按下方层级升级。

---

<a id="escalation-ladder"></a>
## Escalation Ladder / 上报层级

**English / 英文**
- **L0 Self / 自查**: front-desk or duty staff follows the five-segment card. / 前台或值班按五段式步骤卡处理。
- **L1 Duty manager / 值班店长**: cannot resolve in 10 min, or stop-line touched, or member-impact (gate/POS down). / 10 分钟未解、触停手线，或影响会员（闸机/POS 故障）。
- **L2 Vendor hotline / 供应商热线**: hardware defect, needs parts, under warranty. Have model+serial+error code+photos. / 硬件缺陷、需备件、在保。备好型号+序列号+错误码+照片。
- **L3 HQ IT / 集团 IT**: multi-site, network-wide, data/integration, or compliance (HI-1/4/5) involved. / 多店、全场馆网络、数据/集成，或涉合规（HI-1/4/5）。

**中文 / 中文**
- **L0 自查**：前台或值班按五段式步骤卡。
- **L1 值班店长**：10 分钟未解、触停手线，或影响会员（闸机/POS 故障）。
- **L2 供应商热线**：硬件缺陷、需备件、在保。备好型号+序列号+错误码+照片。
- **L3 集团 IT**：多店、全馆网络、数据/集成，或涉合规（HI-1/4/5）。

---

<a id="safety-iron-rules"></a>
## Safety Iron Rules / 安全铁律

**English / 英文**
1. **Never open powered equipment.** Unplug, wait 60s (capacitors hold charge), then touch. / 绝不打开通电设备。先断电，等 60 秒（电容储电）再碰。
2. **Lockout for wet areas.** Pools, saunas, showers: isolate power before any work; post a warning sign. / 湿区上锁断电。泳池、桑拿、淋浴：作业前隔离电源并挂牌。
3. **People must ALWAYS be able to EXIT.** Door maglocks and gates fail-safe to open; never wire them to trap occupants. / 人永远能逃生。电磁锁与闸机须故障安全于「开」，绝不接成困人。
4. **Fire systems are monitor-only (HI-4).** Business IT must never control fire devices; linkage = alarm signal in, release signal out only. / 消防只联不控（HI-4）。业务系统不得控消防；联动=只收告警、只发释放。
5. **PAT test note.** In markets requiring Portable Appliance Testing (e.g. AU/NZ, UK-origin clubs), keep current tags; untested gear stays unplugged. / PAT 提示。要求便携式电器检测的市场（如澳新），保留有效标签；未检设备保持断电。
6. **Swelling or hot batteries = fire risk.** Isolate immediately, move to non-combustible container, call vendor. / 电池鼓包或发热=火灾风险。立即隔离，置于不燃容器，联系供应商。

**中文 / 中文**
1. **绝不打开通电设备。** 先断电，等 60 秒（电容储电）再碰。
2. **湿区上锁断电。** 泳池、桑拿、淋浴：作业前隔离电源并挂牌。
3. **人永远能逃生。** 电磁锁与闸机须故障安全于「开」，绝不接成困人。
4. **消防只联不控（HI-4）。** 业务系统不得控消防；联动=只收告警、只发释放。
5. **PAT 提示。** 要求便携式电器检测的市场（如澳新），保留有效标签；未检设备保持断电。
6. **电池鼓包或发热=火灾风险。** 立即隔离，置于不燃容器，联系供应商。

---

<a id="c1-printers"></a>
## C1 Printers / Scanners / Label printers / 打印机·扫描仪·标签机（10 项）

<a id="c1-printer-e01-paper-jam"></a>
### C1-E01 Paper jam / 卡纸
**1. Self-check / 自查**
1. Turn off the printer, open every cover, remove all visible paper gently. / 关机，打开所有盖板，轻轻取出可见卡纸。
2. Check the rear or duplex unit for tiny torn pieces. / 检查后部或双面器是否有细小碎纸。
3. Reload a flat, dry stack; do not overfill the tray. / 装入平整干燥的纸，纸盘不要过满。
4. Power on and print a self-test page. / 开机打印自检页。
**2. Stop-line / 停手线**
**Do NOT pull jammed paper against the feed rollers with force, and never reach inside while powered on. / 切勿通电时伸手入内，也不要硬拽卡纸与滚轮对抗。**
**3. Vendor call script / 报修话术**
"Model ___, serial ___. Paper jam in the fuser area, no error code. Already cleared visible paper but jam recurs every print." / 「型号___，序列号___。定影区卡纸，无错误码。已清理可见卡纸但每次打印仍卡。」
**4. Parts & cost hint / 备件与费用参考**
Pickup roller or fuser film, directional USD 10–80, varies by market. / 取纸轮或定影膜，方向性 10–80 美元，随市场浮动。
**5. Prevention / 预防**
Store paper dry; clean pickup rollers quarterly (see `data/13-inspection-and-maintenance-calendar`). / 纸干燥存放；每季度清洁取纸轮（见 `data/13`）。

<a id="c1-printer-e02-ghost-queue"></a>
### C1-E02 Ghost print queue (jobs stuck / 幽灵打印队列)
**1. Self-check / 自查**
1. On the PC, open "Devices and Printers", cancel all pending jobs. / 在电脑打开「设备和打印机」，取消所有挂起任务。
2. Restart the "Print Spooler" service (Windows: services.msc). / 重启「打印后台处理程序」服务（Windows：services.msc）。
3. Reboot the printer; confirm the queue is empty on its screen. / 重启打印机；确认屏上队列为空。
**2. Stop-line / 停手线**
**Do NOT install a second driver for the same printer — it creates duplicate queues. / 不要为同一打印机再装第二个驱动，会生成重复队列。**
**3. Vendor call script / 报修话术**
"Model ___, Windows 11. Jobs stuck in spooler, restarting spooler clears them but they return. Driver version ___. " / 「型号___，Windows 11。任务卡在后台，重启后台处理能清但复发。驱动版本___。」
**4. Parts & cost hint / 备件与费用参考**
Usually software; no parts. Driver reinstall labour directional USD 0–30. / 多为软件，无需备件；重装驱动人工方向性 0–30 美元。
**5. Prevention / 预防**
Set a single default driver; disable "SNMP status" if it causes stalls. / 只设单一默认驱动；如卡顿就关「SNMP 状态」。

<a id="c1-printer-e03-driver-loss"></a>
### C1-E03 Driver lost after system update / 系统更新后驱动丢失
**1. Self-check / 自查**
1. Check if the printer shows "driver unavailable" in Devices. / 查看设备里打印机是否显示「驱动不可用」。
2. Download the exact driver from the vendor site (match OS version). / 从供应商官网下对应系统版本的驱动。
3. Re-add the printer as a local/network port, not "driverless". / 以本地/网络端口重新添加，而非「无驱动」模式。
**2. Stop-line / 停手线**
**Do NOT let Windows auto-pick "Microsoft Print to PDF" or class driver for a receipt/label printer — it breaks sizing. / 勿让系统自动选「PDF」或通用驱动，会破坏小票/标签尺寸。**
**3. Vendor call script / 报修话术**
"Model ___, OS upgraded to ___. Need the signed driver package URL for this exact OS build." / 「型号___，系统升到___。需该 OS 版本签名驱动包链接。」
**4. Parts & cost hint / 备件与费用参考**
No parts; driver free from vendor. / 无备件；驱动官网免费。
**5. Prevention / 预防**
Before OS updates, export the driver; pin a known-good version in `data/13` update checklist. / 更新前导出驱动；在 `data/13` 更新清单锁定可用版本。

<a id="c1-receipt-e04-no-cut"></a>
### C1-E04 Receipt printer not cutting / 小票机不切纸
**1. Self-check / 自查**
1. Confirm paper is loaded with the thermal side facing the correct way. / 确认纸热敏面朝向正确。
2. Clean the cutter slit with a soft brush; remove tiny paper dust. / 用软刷清切刀缝，去除纸屑。
3. Send a "full cut" test from the POS; listen for the cutter motor. / 从 POS 发「全切」测试，听切刀电机声。
**2. Stop-line / 停手线**
**Do NOT poke the cutter with metal; a stuck blade can snap and injure. / 勿用金属捅切刀，卡住的刀片可能崩断伤人。**
**3. Vendor call script / 报修话术**
"Receipt model ___, serial ___. Cutter not actuating, paper feeds but no cut. Error code ___ if shown." / 「小票机型号___，序列号___。切刀不动，走纸但不切。如有错误码___。」
**4. Parts & cost hint / 备件与费用参考**
Cutter module directional USD 8–40. / 切刀模块方向性 8–40 美元。
**5. Prevention / 预防**
Use recommended paper grade; run a cut test weekly in `data/13`. / 用推荐纸品；每周在 `data/13` 跑切纸测试。

<a id="c1-printer-e05-wifi-offline"></a>
### C1-E05 Wi-Fi printer offline / 无线打印机离线
**1. Self-check / 自查**
1. On the printer, print a network config page; check it got an IP. / 打印机打网络配置页，看是否拿到 IP。
2. Ping that IP from the POS; if no reply, the Wi-Fi dropped. / 从 POS ping 该 IP；无回应即 Wi-Fi 断了。
3. Re-enter Wi-Fi (2.4 GHz, not 5 GHz for most club printers) and reconnect. / 重连 Wi-Fi（多为 2.4G，非 5G）再连。
**2. Stop-line / 停手线**
**Do NOT assign a static IP that conflicts with the DHCP pool — it causes intermittent offline. / 勿设与 DHCP 池冲突的静态 IP，会导致时断时续。**
**3. Vendor call script / 报修话术**
"Model ___, Wi-Fi 2.4G SSID ___. Printer shows 'offline', IP ___, ping fails. Need static reservation steps." / 「型号___，2.4G 网络___。显示离线，IP___，ping 不通。需静态保留步骤。」
**4. Parts & cost hint / 备件与费用参考**
Usually config; Wi-Fi dongle if defective directional USD 10–35. / 多为配置；无线模块损坏方向性 10–35 美元。
**5. Prevention / 预防**
Reserve a DHCP static lease for the printer MAC in `references/08-network-and-infrastructure`. / 在 `references/08` 给打印机 MAC 做静态保留。

<a id="c1-printer-e06-toner-streaks"></a>
### C1-E06 Toner streaks / 碳粉条痕
**1. Self-check / 自查**
1. Print a cleaning/density page from the menu. / 从菜单打印清洁/浓度页。
2. Gently rock the toner cartridge side to side to redistribute powder. / 轻轻左右摇碳粉盒使粉末分布均匀。
3. Wipe the corona wire (if accessible) with the built-in green slider. / 用内置绿色滑块擦电晕丝（若可触）。
**2. Stop-line / 停手线**
**Do NOT open the toner drum in bright light — prolonged light damages the drum. / 勿在强光下打开鼓组件，长时间光照会损鼓。**
**3. Vendor call script / 报修话术**
"Laser model ___, serial ___. Vertical black streaks every page, cleaning cycle did not help." / 「激光型号___，序列号___。每页竖黑条，清洁循环无效。」
**4. Parts & cost hint / 备件与费用参考**
Toner USD 20–120; drum if worn USD 40–200, varies by market. / 碳粉 20–120 美元；鼓磨损 40–200 美元，随市场浮动。
**5. Prevention / 预防**
Keep spare toner sealed; schedule drum check in `data/13`. / 备用碳粉密封存放；在 `data/13` 排鼓检查。

<a id="c1-scanner-e07-double-feed"></a>
### C1-E07 Contract scanner feeding double / 合同扫描仪双张进纸
**1. Self-check / 自查**
1. Fan the paper stack to separate sheets before loading. / 装纸前抖开纸张使其分离。
2. Clean the separation pad and rollers with a slightly damp cloth. / 用微湿布擦分离垫与滚轮。
3. Lower the feed count setting if the model allows batch adjust. / 若机型支持，降低批量进纸张数设定。
**2. Stop-line / 停手线**
**Do NOT scan stapled or folded pages — it jams the ADF and tears documents. / 勿扫订书钉或折叠页，会卡 ADF 并撕文件。**
**3. Vendor call script / 报修话术**
"Scanner model ___, double-feed on every 2–3 sheets, separation pad cleaned, still occurs." / 「扫描仪型号___，每 2–3 张双张，已清分离垫仍发生。」
**4. Parts & cost hint / 备件与费用参考**
Separation pad/roller kit directional USD 15–60. / 分离垫/轮套装方向性 15–60 美元。
**5. Prevention / 预防**
Clean rollers monthly; replace pad yearly per `data/13`. / 每月清滚轮；按 `data/13` 每年换垫。

<a id="c1-label-e08-calibration"></a>
### C1-E08 Label printer calibration / 标签机校准
**1. Self-check / 自查**
1. Load the correct label size; close the lid firmly. / 装入正确尺寸标签，盖紧。
2. Run "media calibration" / "gap sensor calibration" from the menu. / 从菜单跑「介质校准」/「间隙传感器校准」。
3. Print a calibration label and confirm no offset. / 打印校准标签，确认无偏移。
**2. Stop-line / 停手线**
**Do NOT peel labels while printing — it can drag the roll and desync the sensor. / 打印时勿撕标签，会拖卷并使传感器失步。**
**3. Vendor call script / 报修话术**
"Label model ___, using ___mm labels. Calibration fails, prints shifted by one label." / 「标签机___，用___mm 标签。校准失败，整张偏移一个标签。」
**4. Parts & cost hint / 备件与费用参考**
Usually free calibration; sensor if defective USD 10–50. / 多免费校准；传感器坏 10–50 美元。
**5. Prevention / 预防**
Recalibrate after every roll change; log in `data/13`. / 每换卷重校准；记 `data/13`。

<a id="c1-printer-e09-wrong-size"></a>
### C1-E09 Printing wrong size / 打印尺寸错
**1. Self-check / 自查**
1. In the print dialog, confirm paper size matches the tray. / 打印对话框确认纸张尺寸与纸盘一致。
2. Check "scale" is 100%, not "fit to page". / 检查缩放为 100%，非「适应页面」。
3. On the printer, set the tray paper type/size correctly. / 打印机上把纸盘尺寸/类型设对。
**2. Stop-line / 停手线**
**Do NOT mix A4 and Letter in one tray expecting auto-detect — it mis-scales. / 勿在同一纸盘混放 A4 与 Letter 指望自动识别，会错比例。**
**3. Vendor call script / 报修话术**
"Model ___, driver set to A4 but prints at Letter. Need the tray-size lock setting." / 「型号___，驱动设 A4 却按 Letter 打。需纸盘尺寸锁定设置。」
**4. Parts & cost hint / 备件与费用参考**
No parts; config only. / 无备件；纯配置。
**5. Prevention / 预防**
Lock tray size in driver; standardize paper in `data/13`. / 驱动锁定纸盘尺寸；`data/13` 统一纸品。

<a id="c1-shared-e10-permission"></a>
### C1-E10 Shared printer permission errors / 共享打印机权限错
**1. Self-check / 自查**
1. On the host PC, re-share the printer and set "Everyone: Print". / 主机上重新共享打印机，设「每个人：打印」。
2. On the client, delete and re-add via the host's IP, not the name. / 客户端删掉，用主机 IP 重加，勿用名称。
3. Ensure both PCs are on the same workgroup/VLAN. / 确认两机同工作组/同 VLAN。
**2. Stop-line / 停手线**
**Do NOT grant "Manage this printer" to all staff — it lets anyone change drivers. / 勿给全员「管理打印机」权限，会让人乱改驱动。**
**3. Vendor call script / 报修话术**
"Two Windows PCs, shared receipt printer on host ___. Client gets 'access denied' after password change." / 「两台 Win 电脑，主机___共享小票机。改密码后客户端报拒绝访问。」
**4. Parts & cost hint / 备件与费用参考**
No parts; IT labour directional USD 0–40. / 无备件；IT 人工 0–40 美元。
**5. Prevention / 预防**
Use a print server or cloud print; document in `references/08`. / 用打印服务器或云打印；记 `references/08`。

---

<a id="c2-access-gates"></a>
## C2 Access gates & door control / 闸机与门禁（12 项）

<a id="c2-gate-e01-wont-open"></a>
### C2-E01 Gate won't open (member valid) / 闸机不开（会员有效）
**1. Self-check / 自查**
1. Ask the member to retry the QR/card; watch for a red vs green light. / 让会员重试二维码/卡，看红绿灯。
2. Check the gate controller screen for "communication lost". / 查闸机控制器屏是否「通讯丢失」。
3. Swipe a known-good staff card; if staff works, the member record is stale. / 刷一张已知可用员工卡；员工能过说明会员记录过期。
**2. Stop-line / 停手线**
**Do NOT manually force the barrier arm up by hand repeatedly — it can strip the gear. / 勿反复用手强抬拦阻臂，会打坏齿轮。**
**3. Vendor call script / 报修话术**
"Gate model ___, controller ___. Valid member QR rejected, red light, staff card works. Need manual release + sync steps." / 「闸机___，控制器___。有效会员二维码被拒红灯，员工卡可用。需手动放行+同步步骤。」
**4. Parts & cost hint / 备件与费用参考**
Usually sync; arm motor if stripped USD 60–300. / 多为同步；拦臂电机打坏 60–300 美元。
**5. Prevention / 预防**
Sync member DB hourly; monitor in `data/13`. / 会员库每小时同步；`data/13` 监控。

<a id="c2-gate-e02-stuck-open"></a>
### C2-E02 Gate stuck open / 闸机卡开
**1. Self-check / 自查**
1. Confirm no one is in the lane before acting. / 行动前确认通道无人。
2. Power-cycle the lane controller; the arm should re-home. / 给通道控制器断电重启，拦臂应回位。
3. Check for a stuck "always open" mode set during an event. / 检查是否活动期间误设「常开」模式。
**2. Stop-line / 停手线**
**If the gate controls a paid zone, a stuck-open gate = revenue leak; post a manual checker immediately. / 若闸机管控收费区，卡开=漏费，立即派人手动核验。**
**3. Vendor call script / 报修话术**
"Gate ___, lane ___. Arm stays open after power cycle, likely solenoid or home sensor. Need disable steps." / 「闸机___，通道___。重启后仍常开，疑似电磁阀或归位传感器。需禁用步骤。」
**4. Parts & cost hint / 备件与费用参考**
Solenoid/home sensor directional USD 30–150. / 电磁阀/归位传感器方向性 30–150 美元。
**5. Prevention / 预防**
Audit "open mode" after events; task in `data/13`. / 活动后审计「常开」模式；`data/13` 排任务。

<a id="c2-qr-e03-reader-dead"></a>
### C2-E03 QR reader dead / 二维码读头坏
**1. Self-check / 自查**
1. Clean the reader glass with a lint-free cloth. / 用无绒布擦读头玻璃。
2. Test with a phone torch — is the aiming light on? / 用手机手电照——瞄准灯亮吗？
3. Swap the reader cable to a known-good port. / 把读头线换到已知好端口。
**2. Stop-line / 停手线**
**Do NOT open the reader housing — it is a sealed optical unit, warranty voids on opening. / 勿拆读头外壳，属密封光学件，拆即失保。**
**3. Vendor call script / 报修话术**
"QR reader SN ___. No aiming light, cleaned glass, swapped cable, still dead. Need swap SKU." / 「二维码读头 SN___。无瞄准灯，已清玻璃换线仍死。需换货型号。」
**4. Parts & cost hint / 备件与费用参考**
Reader module directional USD 40–180. / 读头模块方向性 40–180 美元。
**5. Prevention / 预防**
Clean glass daily; spare on shelf per `data/13`. / 每日擦玻璃；`data/13` 备现货。

<a id="c2-rfid-e04-intermittent"></a>
### C2-E04 RFID reader intermittent / 刷卡读头时好时坏
**1. Self-check / 自查**
1. Try several different member cards; if all fail intermittently, it is the reader. / 试多张不同会员卡；若都时好时坏，是读头问题。
2. Check the reader's LED when a card is near — does it flicker? / 卡靠近时看读头灯是否闪。
3. Re-seat the reader's pigtail cable at the controller. / 在控制器端重插读头尾线。
**2. Stop-line / 停手线**
**Do NOT cable-tie the reader lead next to a fluorescent ballast — EMI causes intermittent reads. / 勿把读头线扎在荧光灯镇流器旁，电磁干扰致时断。**
**3. Vendor call script / 报修话术**
"RFID reader ___, intermittent on all cards, LED flickers. Suspect cabling/EMI. Need shielded cable spec." / 「刷卡读头___，所有卡时断，灯闪。疑线缆/干扰。需屏蔽线规格。」
**4. Parts & cost hint / 备件与费用参考**
Reader or shielded cable directional USD 20–120. / 读头或屏蔽线方向性 20–120 美元。
**5. Prevention / 预防**
Route reader cables away from power; log in `data/13`. / 读头线远离电源线；记 `data/13`。

<a id="c2-face-e05-frozen"></a>
### C2-E05 Face terminal frozen (HI-1 compliance) / 人脸终端卡死（HI-1 合规）
**1. Self-check / 自查**
1. Confirm the terminal shows a frozen image, not just slow. / 确认终端是卡死画面，而非单纯慢。
2. Power-cycle the terminal once; wait for full boot. / 断电重启一次，等完整开机。
3. Verify the member can still enter by QR/card as fallback. / 确认会员仍可走二维码/卡作为兜底。
**2. Stop-line / 停手线**
**HI-1: Face biometric must have a recorded legal basis per market. Never "just re-enroll everyone" to fix a freeze — that is a new processing of biometric data; confirm consent records first. / HI-1：人脸生物识别须有当地法定依据。切勿为修卡死「干脆重录所有人」——那是对生物识别数据的新处理，先确认同意记录。**
**3. Vendor call script / 报修话术**
"Face terminal ___, SN ___, frozen on boot logo. Fallback QR works. Need safe-mode reboot, and confirm our consent-log path is intact." / 「人脸终端___，SN___，卡在开机 Logo。二维码兜底可用。需安全模式重启，并确认同意记录路径完好。」
**4. Parts & cost hint / 备件与费用参考**
Usually firmware; mainboard if dead USD 100–400. / 多为固件；主板坏 100–400 美元。
**5. Prevention / 预防**
Keep firmware patched; consent logs audited in `references/12-biometrics-and-cctv`. / 固件常补；同意记录在 `references/12` 审计。

<a id="c2-tailgate-e06-false"></a>
### C2-E06 Anti-tailgate false alarms / 防尾随误报
**1. Self-check / 自查**
1. Check the lane infrared sensors for dust or a sticker. / 查通道红外传感器是否有灰或贴纸。
2. Widen the pass gap setting if members with bags trigger it. / 若背包会员触发，放宽通过间隙设定。
3. Test with a normal walk-through, no second person. / 单人正常走测一次。
**2. Stop-line / 停手线**
**Do NOT disable anti-tailgate entirely for "convenience" — it is a paid-access control; tune, don't disable. / 勿为「方便」彻底关防尾随，那是收费门禁；调参不关功能。**
**3. Vendor call script / 报修话术**
"Gate ___, tailgate alarm on solo passes with bags. Sensors cleaned. Need sensitivity curve." / 「闸机___，单人背包也报尾随。传感器已清。需灵敏度曲线。」
**4. Parts & cost hint / 备件与费用参考**
Sensor array if faulty USD 50–200. / 传感器阵列坏 50–200 美元。
**5. Prevention / 预防**
Quarterly IR alignment in `data/13`. / `data/13` 每季度红外校准。

<a id="c2-fire-e07-linkage"></a>
### C2-E07 Fire-alarm linkage opened all gates (HI-4) / 消防联动全开闸机（HI-4）
**1. Self-check / 自查**
1. Confirm this is a FIRE EVENT, not a false trigger, before anything else. / 首先确认这是真实火警，而非误触发。
2. Gates releasing on fire signal is CORRECT fail-safe behaviour — do not "fix" it by re-locking. / 闸机接消防信号释放是正确故障安全行为——勿为「修」而重新锁上。
3. After the all-clear, reboot controllers to re-arm. / 警报解除后，重启控制器复位。
**2. Stop-line / 停手线**
**HI-4: Fire integration is MONITOR/RELEASE-ONLY. Business IT must NEVER be wired to control, suppress, or delay fire-system release. If a vendor proposes IT-controlled fire logic, refuse and escalate to HQ. / HI-4：消防联动只联不控。业务 IT 绝不可被接去控制、抑制或延迟消防释放。若供应商提议「IT 控消防」，拒绝并上报集团。**
**3. Vendor call script / 报修话术**
"Fire panel ___, gates released on alarm as designed. After all-clear, controllers won't re-arm. Need re-arm procedure — confirm linkage is input-only." / 「消防盘___，闸机按设计释放。解除后控制器不复位。需复位流程——确认联动仅输入。」
**4. Parts & cost hint / 备件与费用参考**
Usually config; interface module USD 30–150. / 多为配置；接口模块 30–150 美元。
**5. Prevention / 预防**
Annual fire-linkage drill logged with fire vendor, not IT alone (`data/13`). / 年度消防联动演练与消防商联记，非仅 IT（`data/13`）。

<a id="c2-controller-e08-offline"></a>
### C2-E08 Controller offline after power cut / 断电后控制器离线
**1. Self-check / 自查**
1. Check the controller has power (LED, not just the gate). / 查控制器本身有电（看 LED，不止闸机）。
2. Confirm the network switch port is up (link light). / 确认交换机端口 up（连线灯）。
3. Reboot controller; many lose their IP after a hard cut. / 重启控制器；很多硬断电后丢 IP。
**2. Stop-line / 停手线**
**Do NOT factory-reset the controller to "fix offline" — you may wipe the access list. / 勿为「修离线」恢复出厂，会清空权限名单。**
**3. Vendor call script / 报修话术**
"Controller ___, SN ___, offline after building power cut. Link light off at switch port ___. Need static IP restore without reset." / 「控制器___，SN___，断电后离线。交换机口___无连线灯。需不改出厂恢复静态 IP。」
**4. Parts & cost hint / 备件与费用参考**
No parts usually; PoE injector if dead USD 15–60. / 通常无件；PoE 注入器坏 15–60 美元。
**5. Prevention / 预防**
Put controllers on UPS; task in `data/13`. / 控制器接 UPS；`data/13` 排任务。

<a id="c2-battery-e09-dead"></a>
### C2-E09 Battery backup dead / 备用电池耗尽
**1. Self-check / 自查**
1. Locate the backup battery (usually a 12V lead-acid near the controller). / 找到备用电池（通常在控制器旁 12V 铅酸）。
2. Measure with a multimeter if you have one; below 11V = dead. / 有万用表量；低于 11V 即废。
3. Confirm the gate still works on mains power. / 确认市电下闸机仍工作。
**2. Stop-line / 停手线**
**Battery acid leaks are corrosive — wear gloves; a swelling battery is a fire risk, isolate it. / 电池漏液具腐蚀性，戴手套；鼓包电池是火灾风险，隔离。**
**3. Vendor call script / 报修话术**
"Backup battery for controller ___ reads ___V, gate drops on any power blink. Need replacement SKU and safe disposal." / 「控制器___ 备电仅___V，一闪断闸机就掉。需换型号与安全处置。」
**4. Parts & cost hint / 备件与费用参考**
12V 7Ah battery directional USD 15–50. / 12V 7Ah 电池方向性 15–50 美元。
**5. Prevention / 预防**
Battery load-test every 6 months in `data/13`. / `data/13` 每 6 个月电池带载测试。

<a id="c2-turnstile-e10-grind"></a>
### C2-E10 Turnstile motor grinding / 三辊闸电机异响
**1. Self-check / 自查**
1. Listen: a grind (not a click) means mechanical, not electronic. / 听声：异响（非咔哒）多为机械非电子。
2. Check for a jammed coin/card in the mechanism. / 查机构里是否卡了硬币/卡。
3. Reduce usage on that lane; divert members. / 该通道减用，引导会员。
**2. Stop-line / 停手线**
**Do NOT oil the mechanism blindly — wrong lubricant jams the encoder. / 勿盲目上油，错润滑油会卡编码盘。**
**3. Vendor call script / 报修话术**
"Turnstile ___, motor grinding on rotation, no error code. Suspect gearbox. Need service visit." / 「三辊闸___，转动电机异响无码。疑齿轮箱。需上门。」
**4. Parts & cost hint / 备件与费用参考**
Gearbox/motor directional USD 80–350. / 齿轮箱/电机方向性 80–350 美元。
**5. Prevention / 预防**
Lubricate per vendor schedule in `data/13`. / 按供应商周期润滑，`data/13`。

<a id="c2-offline-e11-sync-stale"></a>
### C2-E11 Offline-mode member sync stale / 离线模式会员同步过期
**1. Self-check / 自查**
1. Check when the controller last pulled the member DB (sync log). / 查控制器上次拉会员库时间（同步日志）。
2. Force a manual sync from the server. / 从服务器强制手动同步一次。
3. Confirm the offline window setting (how long a card stays valid offline). / 确认离线窗口设定（卡离线有效期）。
**2. Stop-line / 停手线**
**Do NOT extend the offline window to "forever" to avoid sync issues — a revoked member could still enter. / 勿为避同步问题把离线窗口设「永久」，会让已注销会员仍能进。**
**3. Vendor call script / 报修话术**
"Controller ___ offline window set to ___. Sync hasn't run in ___h. Need push-sync trigger." / 「控制器___ 离线窗口___。已___小时未同步。需推送同步触发。」
**4. Parts & cost hint / 备件与费用参考**
No parts; config/connectivity. / 无件；配置/连接。
**5. Prevention / 预防**
Heartbeat sync every 15 min; alert on staleness in `data/13`. / 每 15 分钟心跳同步；`data/13` 过期告警。

<a id="c2-maglock-e12-release-fail"></a>
### C2-E12 Door maglock release failure (safety first) / 电磁锁释放失败（安全第一）
**1. Self-check / 自查**
1. From INSIDE, test the crash-bar / emergency release — people must ALWAYS exit. / 从内侧试紧急释放——人必须永远能出。
2. Check the lock has power (LED on the lock body). / 查锁体有电（LED）。
3. Verify the release signal reaches the lock from the reader/button. / 确认释放信号从读头/按钮到达锁。
**2. Stop-line / 停手线**
**SAFETY: A maglock that fails CLOSED traps people. Any door on an escape route must fail-safe to OPEN. If a lock ever blocks egress, isolate power to that lock immediately and escalate. Never tune a lock to "fail locked". / 安全：电磁锁故障于「关」会困人。任何逃生路线门须故障安全于「开」。若锁阻逃生，立即切断该锁电源并上报。绝不可调成「故障锁死」。**
**3. Vendor call script / 报修话术**
"Maglock on door ___ fails to release on button. Interior crash-bar works. Need fail-safe reconfiguration, NOT a stronger lock." / 「门___ 电磁锁按键不释放。内侧紧急杆可用。需改故障安全，而非换更强锁。」
**4. Parts & cost hint / 备件与费用参考**
Power supply/relay directional USD 25–120. / 电源/继电器方向性 25–120 美元。
**5. Prevention / 预防**
Monthly egress test (no one should be locked in) in `data/13`. / `data/13` 每月逃生测试（不得困人）。

---

<a id="c3-smart-lockers"></a>
## C3 Smart lockers / 智能储物柜（10 项）

<a id="c3-locker-e01-forgot-code"></a>
### C3-E01 Forgot-code opening & authorization log / 忘码开启与授权记录
**1. Self-check / 自查**
1. At the admin panel, search the member by phone/ID, not by locker number. / 在管理端按手机/会员号查，非按柜号。
2. Verify identity (ask for ID) before issuing a remote open. / 发远程开前先核验身份（查证件）。
3. Trigger "remote open" and log the reason. / 触发「远程开」并记录原因。
**2. Stop-line / 停手线**
**Do NOT open a locker for anyone you cannot identity-verify — item-theft risk; every open must be in the authorization log. / 勿给无法核验身份者开柜——有物品被盗风险；每次开启须入授权日志。**
**3. Vendor call script / 报修话术**
"Locker system ___, member ___ verified by ID, forgot code. Need remote-open + confirm it writes to audit log." / 「储物柜系统___，会员___ 持证核验，忘码。需远程开+确认写入审计日志。」
**4. Parts & cost hint / 备件与费用参考**
No parts; software entitlement. / 无件；软件权限。
**5. Prevention / 预防**
Train staff on the verify-then-open SOP in `data/13`. / `data/13` 培训「先核后开」SOP。

<a id="c3-master-e02-governance"></a>
### C3-E02 Master-key governance / 总钥治理
**1. Self-check / 自查**
1. Check who holds the physical master key and whether a log exists. / 查谁持物理总钥，是否有登记。
2. Confirm the digital master key is role-restricted, not shared. / 确认数字总钥按角色限制，非共享。
3. Rotate the master credential quarterly. / 总钥凭证每季度轮换。
**2. Stop-line / 停手线**
**Do NOT leave a master key at the front desk drawer "for convenience" — it is a single point of total compromise. / 勿把总钥放前台抽屉「图方便」，那是全面失守单点。**
**3. Vendor call script / 报修话术**
"Need the master-key access report for audit: who opened which locker, when, by which method." / 「需总钥访问审计报告：谁、何时、以何方式开过哪柜。」
**4. Parts & cost hint / 备件与费用参考**
No parts; governance process. / 无件；治理流程。
**5. Prevention / 预防**
Quarterly key-rotation + access review in `data/13`. / `data/13` 每季度换钥+访问复审。

<a id="c3-battery-e03-dead"></a>
### C3-E03 Lock battery dead / 锁电池耗尽
**1. Self-check / 自查**
1. Try the member's band/card; if the lock beeps weakly or not at all, battery is low. / 试会员手环/卡；锁弱响或不响即低电。
2. Use the emergency power terminal (9V contact) if the model has one. / 若机型有应急供电端，用 9V 触点。
3. Open via admin panel to free the member's items. / 管理端开柜放出物品。
**2. Stop-line / 停手线**
**Do NOT pry the locker door — the latch and frame will bend; use emergency power or admin open. / 勿撬柜门，锁舌与柜体易变形；用应急电或管理开。**
**3. Vendor call script / 报修话术**
"Locker ___ battery dead, member locked out, used 9V terminal to open. Need battery pack SKU." / 「柜___ 电池耗尽，会员被锁，用 9V 端子开了。需电池包型号。」
**4. Parts & cost hint / 备件与费用参考**
Lock battery pack directional USD 5–25. / 锁电池包方向性 5–25 美元。
**5. Prevention / 预防**
Battery low-voltage alert + monthly check in `data/13`. / `data/13` 低电压告警+每月查。

<a id="c3-rfid-e04-no-pair"></a>
### C3-E04 RFID band not pairing / 手环不配对
**1. Self-check / 自查**
1. Confirm the band is the club's frequency (125kHz vs 13.56MHz). / 确认手环是场馆频段（125k vs 13.56M）。
2. Re-seat the band battery or replace it. / 重装或更换手环电池。
3. Re-enroll the band at the admin panel. / 管理端重新登记手环。
**2. Stop-line / 停手线**
**Do NOT issue a member two active bands "just in case" — it breaks audit and item security. / 勿为「以防万一」发两张活跃手环，会破坏审计与物品安全。**
**3. Vendor call script / 报修话术**
"Band ___ won't pair, correct frequency, fresh battery. Need re-enroll + confirm band whitelist." / 「手环___ 不配对，频段对、电池新。需重登记+确认白名单。」
**4. Parts & cost hint / 备件与费用参考**
Band directional USD 3–15. / 手环方向性 3–15 美元。
**5. Prevention / 预防**
Band inventory audit in `data/13`. / `data/13` 手环库存审计。

<a id="c3-board-e05-offline"></a>
### C3-E05 Locker controller board offline / 储物柜控制板离线
**1. Self-check / 自查**
1. Check the board's power LED and network LED. / 查控制板电源灯与网络灯。
2. Reboot the board; many recover from a comms stall. / 重启控制板；多数能从通讯卡死恢复。
3. Confirm the upstream switch port is up. / 确认上游交换机端口 up。
**2. Stop-line / 停手线**
**Do NOT reset the board to factory — it can forget locker-to-member mappings. / 勿恢复控制板出厂，会丢柜-会员映射。**
**3. Vendor call script / 报修话术**
"Locker controller board ___, SN ___, offline, link light off at switch ___. Need remote config restore." / 「储物柜控制板___，SN___，离线，交换机___口无灯。需远程配置恢复。」
**4. Parts & cost hint / 备件与费用参考**
Controller board directional USD 40–200. / 控制板方向性 40–200 美元。
**5. Prevention / 预防**
Board on UPS; port monitoring in `data/13`. / 控制板接 UPS；`data/13` 端口监控。

<a id="c3-latch-e06-jam"></a>
### C3-E06 Jammed latch / 锁舌卡死
**1. Self-check / 自查**
1. Gently wiggle the door while a staff triggers open from admin. / 员工从管理端触发开时，轻晃门。
2. Check for a foreign object in the strike plate. / 查锁扣板是否有异物。
3. Spray a dry PTFE lube, not oil, into the latch. / 向锁舌喷干性 PTFE 润滑剂，非油。
**2. Stop-line / 停手线**
**Do NOT drill the latch to force open — it destroys the lock and the audit trail. / 勿钻孔强开，会毁锁与审计轨迹。**
**3. Vendor call script / 报修话术**
"Locker ___ latch jammed, object in strike, dry lube didn't free it. Need locksmith-safe open." / 「柜___ 锁舌卡，锁扣有异物，干润无效。需无损开锁。」
**4. Parts & cost hint / 备件与费用参考**
Latch/strike kit directional USD 10–50. / 锁舌/锁扣套方向性 10–50 美元。
**5. Prevention / 预防**
Quarterly latch exercise in `data/13`. / `data/13` 每季度锁舌活动。

<a id="c3-water-e07-damage"></a>
### C3-E07 Water damage in wet area / 湿区进水损坏
**1. Self-check / 自查**
1. If water reached the lock, ISOLATE POWER to that bank immediately. / 若水到锁，立即切断该组电源。
2. Do not attempt to open electronically until dry. / 未干前勿尝试电子开启。
3. Dry with a fan; test only after 24h dry. / 用风扇吹干；干透 24 小时后再测。
**2. Stop-line / 停手线**
**Wet-area lockers near pools/saunas: powered locks + water = shock risk. Power off first, dry second, test third. / 泳池/桑拿旁湿区：带电锁+水=触电风险。先断电、再风干、后测试。**
**3. Vendor call script / 报修话术**
"Locker bank ___ near pool got splashed, powered off. Need IP-rated replacement guidance." / 「泳池旁柜组___ 溅水，已断电。需 IP 等级替换建议。」
**4. Parts & cost hint / 备件与费用参考**
IP65 lock directional USD 30–120. / IP65 锁方向性 30–120 美元。
**5. Prevention / 预防**
Spec IP-rated locks for wet zones; review in `data/13`. / 湿区指定 IP 等级锁；`data/13` 复审。

<a id="c3-overnight-e08-sop"></a>
### C3-E08 Member items locked overnight SOP / 会员物品过夜被锁 SOP
**1. Self-check / 自查**
1. Confirm the club is closed and the member is gone. / 确认已闭店、会员离场。
2. From admin, note the locker number and member ID — do NOT open yet. / 管理端记下柜号与会员号——先不开。
3. Call the member; if unreachable, follow the overnight SOP. / 联系会员；联系不上按过夜 SOP。
**2. Stop-line / 停手线**
**Do NOT open a member's locker without authorization just because it is "overnight" — that is a privacy breach. Open only per the approved SOP with a witness and a log. / 勿仅因「过夜」就擅自开会员柜，属隐私侵犯。仅按已批 SOP、有见证、有日志方可开。**
**3. Vendor call script / 报修话术**
"Member ___ items in locker ___ overnight, unreachable. Need the compliant overnight-open SOP checklist." / 「会员___ 物品留柜___ 过夜，联系不上。需合规过夜开启 SOP 清单。」
**4. Parts & cost hint / 备件与费用参考**
No parts; process + witness. / 无件；流程+见证。
**5. Prevention / 预防**
Pre-print the SOP at the desk; drill in `data/13`. / 前台预印 SOP；`data/13` 演练。

<a id="c3-mass-e09-release"></a>
### C3-E09 Mass-release after system crash / 系统崩溃后批量释放
**1. Self-check / 自查**
1. After a server crash, confirm the locker DB is intact before any release. / 服务器崩后，先确认储物柜库完好再释放。
2. Use the "mass open by zone" admin function, not one-by-one. / 用「分区批量开」管理功能，非逐个。
3. Log the event with timestamp and reason. / 带时间戳与原因记录事件。
**2. Stop-line / 停手线**
**Do NOT mass-open during open hours "to be safe" — it empties every locker and invites theft. Only mass-release post-crash with staff present. / 营业中勿为「保险」批量开，会清空所有柜招贼。仅崩溃后、有员工在场才批量释放。**
**3. Vendor call script / 报修话术**
"Locker server crashed, DB restored, need safe mass-release per zone with audit. Confirm no data loss." / 「储物柜服务器崩，库已恢复，需分区安全批量释放带审计。确认无数据丢失。」
**4. Parts & cost hint / 备件与费用参考**
No parts; software function. / 无件；软件功能。
**5. Prevention / 预防**
DB backup 3x/day; verify in `data/13`. / 库每日备 3 次；`data/13` 校验。

<a id="c3-retrofit-e10-decision"></a>
### C3-E10 Retrofit vs replace decision / 改造还是更换
**1. Self-check / 自查**
1. Count how many locks fail per month versus total locks. / 统计每月坏锁数占总锁比。
2. Check spare-part availability and price for the old model. / 查旧型号备件可得性与价格。
3. Compare retrofit kit cost vs full replace cost. / 比改造套件与整体更换成本。
**2. Stop-line / 停手线**
**Do NOT retrofit a wet-area bank with non-IP parts "because they're cheaper" — it will fail again in months. / 勿为「便宜」用非 IP 件改造湿区柜组，数月必再坏。**
**3. Vendor call script / 报修话术**
"___ locks of ___ total failing monthly. Retrofit kit quote vs full replace quote requested, with 3-year TCO." / 「共___柜，月坏___。请报改造套件与整体更换价，含 3 年总拥有成本。」
**4. Parts & cost hint / 备件与费用参考**
Retrofit USD 20–80/lock; replace USD 80–300/lock, directional. / 改造 20–80/柜；更换 80–300/柜，方向性。
**5. Prevention / 预防**
Track failure rate in `data/13`; trigger replace at threshold. / `data/13` 跟踪故障率；过阈即换。

---

<a id="c4-cardio-equipment"></a>
## C4 Cardio equipment / 有氧器械（16 项）

<a id="c4-treadmill-e01-belt-slip"></a>
### C4-E01 Treadmill belt slip / 跑步机跑带打滑
**1. Self-check / 自查**
1. Power off; stand on the side rails, not the belt. / 断电；站侧轨，勿站带。
2. Tighten the rear roller bolts a quarter-turn each, evenly both sides. / 两侧后滚筒螺栓各紧 1/4 圈，均匀。
3. If belt is dry, apply silicone lube under the belt (not on top). / 带干则在带下涂硅油（非表面）。
4. Power on, walk at low speed to test. / 开机低速走测。
**2. Stop-line / 停手线**
**Do NOT over-tighten the belt — it overloads the motor and the deck. And never adjust while the belt is moving. / 勿过紧跑带，会超载电机与跑板；且绝不在带动时调整。**
**3. Vendor call script / 报修话术**
"Treadmill ___, belt slips under load, tightened evenly, lubed, still slips at speed 6. Need roller/deck check." / 「跑步机___，负载下打滑，已匀紧上油，6 速仍滑。需滚筒/跑板查。」
**4. Parts & cost hint / 备件与费用参考**
Belt USD 40–200; deck if worn USD 100–400, directional. / 跑带 40–200 美元；跑板磨损 100–400 美元，方向性。
**5. Prevention / 预防**
Lube every 150 km / 3 months per `data/13`. / 每 150 公里/3 月润滑，`data/13`。

<a id="c4-treadmill-e02-estop-lost"></a>
### C4-E02 Emergency-stop key lost / 急停钥匙丢失
**1. Self-check / 自查**
1. Look in the usual tray; the key is magnetic, often falls near the console. / 找常用托盘；钥匙带磁，常掉控制台旁。
2. Use the spare key from the manager's kit. / 用店长工具包里的备用钥匙。
3. Until replaced, tape the stop clearly OUT and warn coaches. / 补前用醒目胶带标「停」并知会教练。
**2. Stop-line / 停手线**
**Never run a treadmill with the e-stop bypassed by a paperclip or tape — that removes the life-safety cutoff. / 绝不可用回形针/胶带短接急停运行跑步机，那移除生命安全切断。**
**3. Vendor call script / 报修话术**
"Treadmill ___ e-stop key lost, using spare. Need replacement magnet key SKU, qty 5." / 「跑步机___ 急停钥匙丢，用备用。需磁吸急停钥匙型号，5 个。」
**4. Parts & cost hint / 备件与费用参考**
E-stop key directional USD 2–10. / 急停钥匙方向性 2–10 美元。
**5. Prevention / 预防**
Spare keys logged at desk; count monthly in `data/13`. / 备用钥匙前台登记；`data/13` 每月清点。

<a id="c4-console-e03-black"></a>
### C4-E03 Console black screen / 控制台黑屏
**1. Self-check / 自查**
1. Check the console has power (fan sound, LED). / 查控制台有电（风扇声、LED）。
2. Unplug the console cable at the base, reseat, wait 30s, replug. / 拔底座控制台线重插，等 30 秒再接。
3. Try a different outlet on the same circuit. / 同回路换插座试。
**2. Stop-line / 停手线**
**Do NOT open the console hood — capacitors in the motor drive hold charge and can shock. / 勿开控制台盖，电机驱动电容储电可致触电。**
**3. Vendor call script / 报修话术**
"Treadmill ___ console black, base has power, reseated console cable, no change. Serial ___." / 「跑步机___ 控制台黑，底座有电，重插线无变化。序列号___。」
**4. Parts & cost hint / 备件与费用参考**
Console board directional USD 80–350. / 控制台板方向性 80–350 美元。
**5. Prevention / 预防**
Surge protection on every machine; `data/13` check. / 每台接浪涌保护；`data/13` 查。

<a id="c4-console-e04-frozen"></a>
### C4-E04 Console frozen mid-class / 课程中控制台卡死
**1. Self-check / 自查**
1. Press and hold the power/stop for 10s to soft-reset. / 长按电源/停止 10 秒软复位。
2. If unresponsive, pull the safety key to cut drive, then power cycle. / 无响应则拔安全钥匙切断驱动，再断电重启。
3. Move the class member to another machine. / 把上课会员移到其他器械。
**2. Stop-line / 停手线**
**Do NOT yank the power cord while a member is on the belt at speed — stop the belt first via key or e-stop. / 会员在带上有速度时勿猛拔电源线，先经钥匙或急停停带。**
**3. Vendor call script / 报修话术**
"Model ___ froze during class, soft-reset failed, needed key pull. Frequent freeze. Need firmware/log pull." / 「型号___ 课上卡死，软复位无效需拔钥匙。频发。需固件/日志提取。」
**4. Parts & cost hint / 备件与费用参考**
Usually firmware; console if dead USD 80–350. / 多为固件；控制台坏 80–350 美元。
**5. Prevention / 预防**
Firmware updates off-peak; schedule in `data/13`. / 固件非高峰更新；`data/13` 排期。

<a id="c4-incline-e05-stuck"></a>
### C4-E05 Incline stuck / 坡度卡住
**1. Self-check / 自查**
1. Try lowering then raising incline via buttons. / 用按钮先降后升坡度。
2. Listen for the incline motor — silence means no drive. / 听坡度电机声——无声即无驱动。
3. Power cycle; some re-home the incline on boot. / 断电重启；部分开机自归位坡度。
**2. Stop-line / 停手线**
**Do NOT push the deck up/down by hand to "help" — the incline screw can pinch. / 勿用手抬/压跑板「帮忙」，坡度丝杠会夹手。**
**3. Vendor call script / 报修话术**
"Incline stuck at ___%, motor silent, reboot no re-home. Model ___. Need incline motor/screw." / 「坡度卡___%，电机无声，重启不归位。型号___。需坡度电机/丝杠。」
**4. Parts & cost hint / 备件与费用参考**
Incline motor directional USD 60–250. / 坡度电机方向性 60–250 美元。
**5. Prevention / 预防**
Cycle incline weekly; task in `data/13`. / `data/13` 每周坡度循环。

<a id="c4-error-e06-exx"></a>
### C4-E06 Error-code families (generic "Exx" drive errors) / 通用 Exx 驱动错误码
**1. Self-check / 自查**
1. Read the exact code (E01, E07, E03…) and write it down. / 读确切码（E01/E07/E03…）记下。
2. Power off, unplug, wait 60s, reboot once. / 断电拔插，等 60 秒，重启一次。
3. If the same code returns, stop using the machine and tag it. / 同码再现，停用并贴标。
**2. Stop-line / 停手线**
**Do NOT open the hood on any "Exx" drive error — motor capacitors hold charge for minutes and can kill. Tag "OUT OF SERVICE" and call the vendor. / 任何 Exx 驱动错误勿开盖，电机电容储电数分钟可致命。贴「停用」并叫供应商。**
**3. Vendor call script / 报修话术**
"Treadmill/bike ___ shows error E___, reboot once, same code. Serial ___. Need drive-board service, do NOT open hood." / 「跑步机/单车___ 报 E___，重启一次同码。序列号___。需驱动板维修，勿开盖。」
**4. Parts & cost hint / 备件与费用参考**
Drive board/motor directional USD 100–500. / 驱动板/电机方向性 100–500 美元。
**5. Prevention / 预防**
Log error codes centrally; trend in `data/13`. / 错误码集中记录；`data/13` 看趋势。

<a id="c4-bike-e07-resistance"></a>
### C4-E07 Bike resistance dead / 单车阻力失效
**1. Self-check / 自查**
1. Confirm the bike powers on and pairs. / 确认单车开机并配对。
2. Try the resistance buttons; no change = brake assembly fault. / 试阻力键；无变化=刹车组件故障。
3. Reboot the console once. / 控制台重启一次。
**2. Stop-line / 停手线**
**Do NOT ride a bike with zero resistance control if the brake is electromagnetic — it can suddenly lock; tag it out. / 电磁刹车单车若阻力失控勿骑，可能突锁；贴标停用。**
**3. Vendor call script / 报修话术**
"Bike ___ resistance buttons do nothing, console rebooted. Need brake/eddy board." / 「单车___ 阻力键无反应，控制台已重启。需刹车/涡流板。」
**4. Parts & cost hint / 备件与费用参考**
Brake assembly directional USD 50–220. / 刹车组件方向性 50–220 美元。
**5. Prevention / 预防**
Resistance self-test monthly in `data/13`. / `data/13` 每月阻力自检。

<a id="c4-rower-e08-chain"></a>
### C4-E08 Rower chain noise / 划船机链条异响
**1. Self-check / 自查**
1. Wipe the chain with a dry cloth to remove grit. / 干布擦链条去砂。
2. Apply a light chain oil (not WD-40 alone) to the chain. / 链条上少量链油（非仅 WD-40）。
3. Check the chain for stiff links or rust. / 查链条有无死链或锈。
**2. Stop-line / 停手线**
**Do NOT over-oil — excess oil flings onto the rail and clothes, and attracts dirt. / 勿过量上油，油会甩到轨道衣物并吸灰。**
**3. Vendor call script / 报修话术**
"Rower ___ chain noisy, cleaned and lightly oiled, still clicks. Check sprocket." / 「划船机___ 链条响，已清轻油仍响。查链轮。」
**4. Parts & cost hint / 备件与费用参考**
Chain/sprocket directional USD 20–90. / 链条/链轮方向性 20–90 美元。
**5. Prevention / 预防**
Oil every 2 weeks; `data/13` log. / `data/13` 每两周上油。

<a id="c4-elliptical-e09-wobble"></a>
### C4-E09 Elliptical wobble / 椭圆机晃动
**1. Self-check / 自查**
1. Check the floor is level under the machine. / 查器械下地面是否水平。
2. Tighten the levelling feet until all four touch. / 调平脚拧紧至四脚着地。
3. Tighten the main frame bolts. / 紧主框架螺栓。
**2. Stop-line / 停手线**
**Do NOT use shims that raise the machine off its stabilisers — it stresses the welds. / 勿用垫片把器械垫离稳定脚，会应力焊点。**
**3. Vendor call script / 报修话术**
"Elliptical ___ wobbles even after levelling feet. Suspect loose frame bolt or cracked weld." / 「椭圆机___ 调平后仍晃。疑框架螺栓松或焊缝裂。」
**4. Parts & cost hint / 备件与费用参考**
Stabiliser/bolt kit directional USD 10–60. / 稳定脚/螺栓套方向性 10–60 美元。
**5. Prevention / 预防**
Monthly bolt torque check in `data/13`. / `data/13` 每月螺栓扭矩查。

<a id="c4-usb-e10-dead"></a>
### C4-E10 USB/charging ports dead / USB/充电口坏
**1. Self-check / 自查**
1. Try a different cable and device in the port. / 换线换设备试该口。
2. Reboot the console once. / 控制台重启一次。
3. Check the port for lint/debris with a wooden pick. / 木签挑出口内绒屑。
**2. Stop-line / 停手线**
**Do NOT probe the port with metal — a short can damage the console board. / 勿用金属探口，短路会损控制台板。**
**3. Vendor call script / 报修话术**
"Model ___ USB port dead on all cables, cleaned, rebooted. Need port/board." / 「型号___ USB 口所有线均坏，已清已重启。需口/板。」
**4. Parts & cost hint / 备件与费用参考**
Port/console board directional USD 30–200. / 端口/控制台板方向性 30–200 美元。
**5. Prevention / 预防**
Clean ports monthly; `data/13`. / `data/13` 每月清口。

<a id="c4-ftms-e11-no-bt"></a>
### C4-E11 FTMS/Bluetooth not broadcasting / FTMS/蓝牙不广播
**1. Self-check / 自查**
1. On the machine, enter "pairing mode" from the menu (not just power on). / 器械上从菜单进「配对模式」，非仅开机。
2. Forget the old device in the phone/app, then re-scan. / 手机/App 忘掉旧设备再扫。
3. Move phones within 1 m; Bluetooth is short-range. / 手机移到 1 米内；蓝牙近距离。
**2. Stop-line / 停手线**
**Do NOT install a 3rd-party Bluetooth dongle into club cardio without vendor approval — it can break FTMS certification. / 未经供应商同意勿给场馆有氧装第三方蓝牙棒，会破 FTMS 认证。**
**3. Vendor call script / 报修话术**
"Model ___ FTMS not discoverable, pairing mode on, phone can't see it. Need BT module/firmware per `references/09-iot-and-open-protocols`." / 「型号___ FTMS 不可见，已配对模式，手机搜不到。需蓝牙模块/固件，见 `references/09`。」
**4. Parts & cost hint / 备件与费用参考**
BT module directional USD 15–80. / 蓝牙模块方向性 15–80 美元。
**5. Prevention / 预防**
Keep FTMS firmware current; see `references/09`. / FTMS 固件保持新；见 `references/09`。

<a id="c4-display-e12-dim"></a>
### C4-E12 Display dim / 屏幕变暗
**1. Self-check / 自查**
1. Check the brightness setting in the menu. / 查菜单亮度设定。
2. Clean the screen; sweat film cuts visibility. / 擦屏；汗膜降可视。
3. Reboot the console. / 重启控制台。
**2. Stop-line / 停手线**
**Do NOT max brightness permanently to "fix" dimness — it hides a failing backlight and burns the panel. / 勿长期拉满亮度「修」暗，那掩盖背光衰竭并烧屏。**
**3. Vendor call script / 报修话术**
"Model ___ display dim even at max brightness, cleaned. Backlight suspect." / 「型号___ 满亮仍暗，已擦。疑背光。」
**4. Parts & cost hint / 备件与费用参考**
LCD/backlight directional USD 40–200. / 液晶/背光方向性 40–200 美元。
**5. Prevention / 预防**
Wipe after each use; `data/13` check. / 每次用完擦；`data/13` 查。

<a id="c4-belt-e13-lube"></a>
### C4-E13 Belt lubrication schedule / 跑带润滑周期
**1. Self-check / 自查**
1. Lift the belt edge; if the deck looks dry/matte, it needs lube. / 掀带边；跑板发干/哑光即需润。
2. Apply silicone only under the belt, spread by walking. / 硅油只涂带下，走步摊开。
3. Record the date on the machine card. / 在器械卡记日期。
**2. Stop-line / 停手线**
**Do NOT use furniture polish or oil-based lube — it degrades the deck and is a fire-smoke risk. / 勿用家具蜡或油基润滑剂，会损跑板且有烟燃风险。**
**3. Vendor call script / 报修话术**
"Need the OEM silicone spec and lube interval for model ___ (hours-based)." / 「需型号___ 原厂硅油规格与按小时润滑周期。」
**4. Parts & cost hint / 备件与费用参考**
Silicone lube USD 5–25/bottle. / 硅油 5–25 美元/瓶。
**5. Prevention / 预防**
Log hours + lube in `data/13` calendar. / `data/13` 记小时数+润滑。

<a id="c4-static-e14-shock"></a>
### C4-E14 Static shocks / 静电打手
**1. Self-check / 自查**
1. Increase humidity in the room if very dry (winter). / 若极干（冬季）提高室内湿度。
2. Use a grounded anti-static mat at the front of the treadmill. / 跑步机前铺接地防静电垫。
3. Lube the belt (dry belt generates static). / 润带（干带生静电）。
**2. Stop-line / 停手线**
**Do NOT run a humidifier next to powered cardio — water + electronics = shock/fire. / 勿在带电有氧旁开加湿器，水+电=触电/火。**
**3. Vendor call script / 报修话术**
"Members get static shocks on treadmill ___. Room RH is ___%. Need grounding check." / 「会员在跑步机___ 被静电打。室内湿度___%。需接地查。」
**4. Parts & cost hint / 备件与费用参考**
Ground strap/mat directional USD 10–40. / 接地带/垫方向性 10–40 美元。
**5. Prevention / 预防**
Monitor RH in `data/13`; keep 40–60%. / `data/13` 监湿度，维持 40–60%。

<a id="c4-breaker-e15-trip"></a>
### C4-E15 Machine trips breaker / 器械跳闸（见 C10）
**1. Self-check / 自查**
1. Note which breaker tripped and what else is on that circuit. / 记跳闸的空开及该回路其他负载。
2. Unplug the machine; reset the breaker; plug back alone. / 拔器械；复位空开；单独插回。
3. If it trips alone, the machine has a short — tag out. / 单独仍跳即短路，贴标停用。
**2. Stop-line / 停手线**
**Do NOT keep resetting a breaker that immediately trips — that wires heat and is a fire risk. Call the vendor/electrician. / 勿反复复位一合就跳的空开，线会发热起火。叫供应商/电工。**
**3. Vendor call script / 报修话术**
"Treadmill ___ trips breaker ___ on its own circuit. Suspect drive short. See `data/10#c10-internet-down` power flow." / 「跑步机___ 在专有回路仍跳空开___。疑驱动短路。见 `data/10#c10-internet-down` 电力流。」
**4. Parts & cost hint / 备件与费用参考**
Drive board/motor directional USD 100–500. / 驱动板/电机方向性 100–500 美元。
**5. Prevention / 预防**
Dedicated circuits per machine; audit in `data/13`. / 每台专用回路；`data/13` 审计。

<a id="c4-ent-e16-screen-old"></a>
### C4-E16 Entertainment screen apps outdated / 娱乐屏应用过期
**1. Self-check / 自查**
1. Check the app store / vendor portal for updates. / 查应用商店/供应商门户更新。
2. Connect the screen to club Wi-Fi (not member guest SSID). / 屏连场馆 Wi-Fi（非会员访客 SSID）。
3. Run the vendor's update, not a public app store sideload. / 跑供应商更新，非公域商店侧载。
**2. Stop-line / 停手线**
**Do NOT sideload random Android apps onto cardio screens — it breaks the kiosk mode and may void the service contract. / 勿给有氧屏侧载随意安卓应用，会破 kiosk 模式并可能失保。**
**3. Vendor call script / 报修话术**
"Entertainment screen on ___ apps outdated, on club SSID, need vendor OTA update package." / 「___ 娱乐屏应用过期，已连场馆 SSID，需供应商 OTA 包。」
**4. Parts & cost hint / 备件与费用参考**
Usually free OTA; module if dead USD 60–250. / 多免费 OTA；模块坏 60–250 美元。
**5. Prevention / 预防**
OTA window monthly in `data/13`. / `data/13` 每月 OTA 窗口。

---

<a id="c5-strength"></a>
## C5 Strength & smart strength / 力量与智能力量（8 项）

<a id="c5-cable-e01-fray"></a>
### C5-E01 Cable fray (STOP-LINE: remove from service) / 钢索磨损（停手线：立即停用）
**1. Self-check / 自查**
1. Visually inspect the cable along its full length for broken strands. / 全程目视查钢索有无断丝。
2. Check near the pulleys where wear concentrates. / 查滑轮附近磨损集中处。
3. If ANY strand is broken, the machine is OUT. / 任一处断丝即停用。
**2. Stop-line / 停手线**
**MEMBER SAFETY: A frayed cable can SNAP under load and injure. Remove the machine from service IMMEDIATELY, tag it, and do not let anyone use it until the cable is replaced. / 会员安全：磨损钢索负载下可崩断伤人。立即停用、贴标，换索前任何人不得用。**
**3. Vendor call script / 报修话术**
"Strength machine ___ cable has broken strands at pulley ___. Out of service now. Need OEM cable + tension spec." / 「力量器械___ 滑轮___ 处钢索断丝。已停用。需原厂钢索+张力规格。」
**4. Parts & cost hint / 备件与费用参考**
Cable directional USD 20–120. / 钢索方向性 20–120 美元。
**5. Prevention / 预防**
Weekly cable inspection; `data/13` checklist. / `data/13` 每周钢索检查。

<a id="c5-pin-e02-missing"></a>
### C5-E02 Selector pin missing / 插销缺失
**1. Self-check / 自查**
1. Check the pin rack and nearby machines. / 查插销架与邻近器械。
2. Issue a spare from the manager kit. / 店长工具包发备用。
3. Tag the weight stack "do not use" until the pin returns. / 配重片贴「勿用」待销归。
**2. Stop-line / 停手线**
**Do NOT let a member use a machine with a makeshift pin (screwdriver, bolt) — it can slip and drop the stack. / 勿让会员用代用插销（螺丝刀、螺栓），会滑脱砸下配重。**
**3. Vendor call script / 报修话术**
"Need OEM selector pins for ___ stacks, qty ___, with safety lanyard." / 「需___ 配重原厂插销___ 个，带安全绳。」
**4. Parts & cost hint / 备件与费用参考**
Pin directional USD 3–15. / 插销方向性 3–15 美元。
**5. Prevention / 预防**
Pin count at close; `data/13` task. / 闭店点数；`data/13` 任务。

<a id="c5-screen-e03-unresponsive"></a>
### C5-E03 Smart-strength screen unresponsive / 智能力量屏无响应
**1. Self-check / 自查**
1. Wake the screen (tap, not just look). / 点屏唤醒，非仅看。
2. Reboot the attached tablet/console. / 重启附带平板/控制台。
3. Confirm the machine still moves manually (screen is secondary). / 确认器械仍可手动动（屏为辅）。
**2. Stop-line / 停手线**
**Do NOT force a software reset that wipes the rep logger without backing up member sessions. / 勿在未按备份会员记录前强复位清掉次数记录。**
**3. Vendor call script / 报修话术**
"Smart strength ___ screen frozen, reboot no help. Need console replacement/SKU." / 「智能力量___ 屏卡，重启无效。需控制台换/型号。」
**4. Parts & cost hint / 备件与费用参考**
Tablet/console directional USD 80–400. / 平板/控制台方向性 80–400 美元。
**5. Prevention / 预防**
Sync logs to MMS hourly; `data/12-software-fault-tree-library`. / 记录每小时同步 MMS；见 `data/12`。

<a id="c5-loadcell-e04-drift"></a>
### C5-E04 Load cell drift / 称重传感器漂移
**1. Self-check / 自查**
1. Place a known weight (e.g. a 20 kg plate) and compare to the reading. / 放已知重（如 20kg 片）比对读数。
2. Re-zero the cell via the menu with no load. / 空载经菜单重新归零。
3. If it still drifts, the cell is failing. / 仍漂即传感器衰竭。
**2. Stop-line / 停手线**
**Do NOT ignore drift on a smart strength unit — wrong load data misleads training and member trust. / 智能力量单位移勿忽视，错误负荷误导训练与会员信任。**
**3. Vendor call script / 报修话术**
"Smart strength ___ load cell reads ___kg for 20kg, re-zeroed. Need calibration/replacement." / 「智能力量___ 传感器 20kg 读___，已归零。需校准/换。」
**4. Parts & cost hint / 备件与费用参考**
Load cell directional USD 40–200. / 称重传感器方向性 40–200 美元。
**5. Prevention / 预防**
Monthly calibration check in `data/13`. / `data/13` 每月校准查。

<a id="c5-pulley-e05-squeak"></a>
### C5-E05 Pulley squeak / 滑轮异响
**1. Self-check / 自查**
1. Identify which pulley squeaks (follow the sound). / 定位异响滑轮（循声）。
2. Apply a dry PTFE lube to the bearing, not oil. / 轴承上干性 PTFE 润滑，非油。
3. Spin by hand to confirm quiet. / 手转确认静。
**2. Stop-line / 停手线**
**Do NOT grease a worn bearing expecting silence — it hides impending seizure. / 勿为静而润磨损轴承，那掩盖即将卡死。**
**3. Vendor call script / 报修话术**
"Machine ___ pulley ___ squeaks, dry-lubed, returns. Bearing worn." / 「器械___ 滑轮___ 响，干润仍响。轴承磨损。」
**4. Parts & cost hint / 备件与费用参考**
Pulley/bearing directional USD 8–50. / 滑轮/轴承方向性 8–50 美元。
**5. Prevention / 预防**
Quarterly lube in `data/13`. / `data/13` 每季度润滑。

<a id="c5-upholstery-e06-tear"></a>
### C5-E06 Upholstery tear (hygiene + brand) / 坐垫破损（卫生+品牌）
**1. Self-check / 自查**
1. Check if the foam is exposed (hygiene + injury risk). / 查是否露海绵（卫生+受伤风险）。
2. Cover with tape temporarily if minor. / 轻微可临时胶布覆盖。
3. Flag for re-upholster before member contact. / 会员接触前标换垫。
**2. Stop-line / 停手线**
**Do NOT leave exposed foam pads in use — sweat soaks in, becomes a hygiene and slip hazard. / 勿让露海绵坐垫继续使用，汗渗入成卫生与打滑隐患。**
**3. Vendor call script / 报修话术**
"Pad on ___ torn, foam exposed. Need OEM vinyl cover + stapler spec." / 「___ 坐垫破，露海绵。需原厂革面+钉枪规格。」
**4. Parts & cost hint / 备件与费用参考**
Vinyl cover directional USD 15–80. / 革面方向性 15–80 美元。
**5. Prevention / 预防**
Wipe + inspect pads weekly; `data/13`. / `data/13` 每周擦检坐垫。

<a id="c5-counter-e07-no-reps"></a>
### C5-E07 Counter not logging reps / 次数不记录
**1. Self-check / 自查**
1. Confirm the machine is paired to the member's session. / 确认器械已配对会员本次。
2. Check the rep sensor lens for sweat/tape cover. / 查次数传感器镜面有无汗/胶覆盖。
3. Re-pair and do one test rep. / 重新配对做 1 次测试。
**2. Stop-line / 停手线**
**Do NOT disable the counter "because it's wrong" — it breaks the smart-strength value prop; fix the sensor. / 勿因「不准」关计数，那废掉智能力量卖点；修传感器。**
**3. Vendor call script / 报修话术**
"Smart strength ___ not logging reps, lens clean, re-paired, still 0. Need sensor/board." / 「智能力量___ 不记次，镜面净已重配仍 0。需传感器/板。」
**4. Parts & cost hint / 备件与费用参考**
Rep sensor directional USD 20–100. / 次数传感器方向性 20–100 美元。
**5. Prevention / 预防**
Sensor clean weekly; `data/13`. / `data/13` 每周清传感器。

<a id="c5-firmware-e08-brick"></a>
### C5-E08 Firmware update bricked console / 固件升级变砖
**1. Self-check / 自查**
1. Confirm the console is truly dead (no LED, no charge light). / 确认控制台真死（无 LED、无充灯）。
2. Try the vendor's recovery mode (usually hold a combo button on power). / 试供应商恢复模式（通常开机长按组合键）。
3. Do NOT retry the same file. / 勿重试同一文件。
**2. Stop-line / 停手线**
**Do NOT power-cycle during a firmware flash — that is what bricks it; if mid-flash, wait the full stated time. / 固件刷写中勿断电，那正是变砖原因；刷写中须等足标称时间。**
**3. Vendor call script / 报修话术**
"Smart strength ___ console bricked after OTA ___%. Need recovery image + RMA steps." / 「智能力量___ 控制台 OTA ___% 变砖。需恢复镜像+RMA 步骤。」
**4. Parts & cost hint / 备件与费用参考**
Console board directional USD 80–400; RMA labour varies. / 控制台板方向性 80–400 美元；RMA 人工浮动。
**5. Prevention / 预防**
Stage firmware on one unit first; `data/13` gate. / 先在一台灰度；`data/13` 闸门。

---

<a id="c6-body-scanners"></a>
## C6 Body-composition & posture scanners / 体测与体态扫描（8 项）

<a id="c6-inbody-e01-no-power"></a>
### C6-E01 InBody-type won't power / 体测仪不通电
**1. Self-check / 自查**
1. Check the wall outlet and the brick adapter LED. / 查墙插与电源适配器 LED。
2. Try the club's known-good IEC cable. / 试场馆已知好 IEC 线。
3. Confirm the breaker for that circuit. / 确认该回路空开。
**2. Stop-line / 停手线**
**Do NOT open the base unit — it has measurement circuitry and a charged PSU; refer to vendor. / 勿开主机底座，内含测量电路与带电电源，交供应商。**
**3. Vendor call script / 报修话术**
"Body scanner ___ no power, adapter LED off, swapped cable, still dead. Serial ___." / 「体测仪___ 不通电，适配器灯灭，换线仍死。序列号___。」
**4. Parts & cost hint / 备件与费用参考**
PSU/adapter directional USD 20–100. / 电源适配器方向性 20–100 美元。
**5. Prevention / 预防**
Surge strip + UPS; `data/13`. / 接浪涌+UPS；`data/13`。

<a id="c6-inbody-e02-inconsistent"></a>
### C6-E02 Results wildly inconsistent / 结果漂移大
**1. Self-check / 自查**
1. Wipe the electrodes; sweat film changes impedance. / 擦电极；汗膜改变阻抗。
2. Ask the member to stand barefoot, still, feet fully on pads. / 让会员赤脚静立，双脚满踩电极。
3. Re-measure the same person twice, 5 min apart. / 同一人隔 5 分钟测两次。
**2. Stop-line / 停手线**
**HI-6 boundary: If results suggest a medical issue, refer the member to a qualified professional — the scanner never diagnoses. / HI-6 边界：若结果提示医学问题，转介专业人士；本仪不做诊断。**
**3. Vendor call script / 报修话术**
"Scanner ___ same person varies ___kg body fat between tests. Electrodes cleaned. Need calibration." / 「扫描仪___ 同一人两次体脂差___kg。电极已擦。需校准。」
**4. Parts & cost hint / 备件与费用参考**
Electrode pad/calibration directional USD 30–200. / 电极垫/校准方向性 30–200 美元。
**5. Prevention / 预防**
Daily electrode wipe + monthly calibration; `data/13`. / `data/13` 每日擦电极+每月校准。

<a id="c6-printer-e03-jam"></a>
### C6-E03 Printer module jam / 打印模块卡纸
**1. Self-check / 自查**
1. Open the result-print slot, remove jammed paper. / 开结果打印槽，取卡纸。
2. Confirm paper roll is the correct width. / 确认纸卷宽度对。
3. Clean the cutter. / 清切刀。
**2. Stop-line / 停手线**
**Do NOT pull thermal paper against the cutter motor. / 勿逆切刀电机扯热敏纸。**
**3. Vendor call script / 报修话术**
"Body scanner ___ result printer jams every print, correct paper, cutter cleaned." / 「体测仪___ 结果打印每次卡，纸对、刀清。」
**4. Parts & cost hint / 备件与费用参考**
Print module directional USD 30–150. / 打印模块方向性 30–150 美元。
**5. Prevention / 预防**
Use specified roll; `data/13` stock check. / 用指定纸卷；`data/13` 库存查。

<a id="c6-sync-e04-mms"></a>
### C6-E04 Data not syncing to MMS / 数据不同步 MMS
**1. Self-check / 自查**
1. Confirm the scanner has network (Wi-Fi/Ethernet LED). / 确认扫描仪有网（Wi-Fi/以太网灯）。
2. Re-enter the MMS API key/token at the scanner. / 扫描仪重填 MMS API 密钥/令牌。
3. Trigger a manual upload of the last result. / 手动上传最近一条结果。
**2. Stop-line / 停手线**
**Do NOT store member health data locally on an unencrypted scanner SD — it violates minimization (HI-8). / 勿把会员健康数据明文存扫描仪 SD，违反最小化（HI-8）。**
**3. Vendor call script / 报修话术**
"Scanner ___ not pushing to MMS, network OK, token re-entered. Need API endpoint + field map. See `data/12-software-fault-tree-library`." / 「扫描仪___ 推不到 MMS，网通、令牌重填。需 API 端点+字段映射。见 `data/12`。」
**4. Parts & cost hint / 备件与费用参考**
No parts; integration config. / 无件；集成配置。
**5. Prevention / 预防**
Sync health-check in `data/13`; link `data/12`. / `data/13` 同步健康检查；链 `data/12`。

<a id="c6-calib-e05-drift"></a>
### C6-E05 Calibration drift / 校准漂移
**1. Self-check / 自查**
1. Run the built-in self-check/calibration routine. / 跑内置自检/校准。
2. Use the vendor's reference load if provided. / 用供应商参考负载（若有）。
3. Record the before/after offset. / 记录前后偏差。
**2. Stop-line / 停手线**
**Do NOT "zero-trick" by editing stored offsets manually — it hides drift and corrupts trends. / 勿手动改存偏移「凑零」，掩盖漂移并毁趋势。**
**3. Vendor call script / 报修话术**
"Scanner ___ calibration drifts ___% weekly. Need tech calibration visit." / 「扫描仪___ 校准每周漂___%。需技术校准上门。」
**4. Parts & cost hint / 备件与费用参考**
Calibration service directional USD 50–250. / 校准服务方向性 50–250 美元。
**5. Prevention / 预防**
Scheduled calibration in `data/13`. / `data/13` 排期校准。

<a id="c6-consent-e06-broken"></a>
### C6-E06 Consent flow broken (HI-1: no scan without recorded consent) / 同意流断裂（HI-1：无记录同意不扫描）
**1. Self-check / 自查**
1. Check the consent flag in the member record before scanning. / 扫描前查会员记录同意标志。
2. If the consent UI is broken, do NOT scan "and fix later". / 若同意 UI 坏，勿「先扫后补」。
3. Fall back to a signed paper consent, logged. / 回退纸质签字同意并登记。
**2. Stop-line / 停手线**
**HI-1: Never run a body scan on a member without a recorded legal basis of consent for that market. A broken consent flow = STOP scanning until fixed. / HI-1：无当地法定同意记录绝不体测。同意流坏=停扫直至修复。**
**3. Vendor call script / 报修话术**
"Consent module ___ broken, cannot record opt-in. Need fix before any scan; confirm our lawful basis per `references/12-biometrics-and-cctv`." / 「同意模块___ 坏，无法记录 Opt-in。修复前停扫；确认法定依据见 `references/12`。」
**4. Parts & cost hint / 备件与费用参考**
No parts; software/legal. / 无件；软件/法务。
**5. Prevention / 预防**
Consent audit monthly; `references/12`. / `references/12` 每月同意审计。

<a id="c6-posture-e07-shutter"></a>
### C6-E07 Posture-camera privacy shutter policy / 体态相机隐私遮挡策略
**1. Self-check / 自查**
1. Confirm the physical shutter is CLOSED when not in a session. / 确认非拍摄时物理遮挡盖关闭。
2. Verify the LED indicator shows "off" when shuttered. / 确认遮挡时指示灯「关」。
3. Train coaches to open only during the member's booked slot. / 训练教练仅会员预约时段开。
**2. Stop-line / 停手线**
**HI-5: Cameras are NEVER permitted in changing rooms/showers. If a posture camera's view can see a changing area, reposition or disable it immediately. / HI-5：更衣室/淋浴绝对禁相机。若体态相机视野可见更衣区，立即移位或禁用。**
**3. Vendor call script / 报修话术**
"Posture camera ___ shutter stuck open, LED mismatch. Need shutter servo + privacy config." / 「体态相机___ 遮挡盖卡开，灯不符。需遮挡伺服+隐私配置。」
**4. Parts & cost hint / 备件与费用参考**
Shutter module directional USD 20–100. / 遮挡模块方向性 20–100 美元。
**5. Prevention / 预防**
Privacy check in `data/13`; link `references/12`. / `data/13` 隐私检查；链 `references/12`。

<a id="c6-export-e08-format"></a>
### C6-E08 Export format mismatch / 导出格式不符
**1. Self-check / 自查**
1. Check the export menu for CSV/PDF/API options. / 查导出菜单 CSV/PDF/API 选项。
2. Match the MMS expected field names. / 对齐 MMS 期望字段名。
3. Test-export one record and open it. / 测导一条并打开。
**2. Stop-line / 停手线**
**Do NOT hand-edit exported health files in bulk "to make them fit" — it risks data errors and privacy leaks. / 勿为「匹配」批量手改导出的健康文件，易出错且泄隐私。**
**3. Vendor call script / 报修话术**
"Scanner ___ exports ___ format, MMS expects ___. Need mapping or firmware with correct template." / 「扫描仪___ 导___ 格式，MMS 要___。需映射或带正确模板的固件。」
**4. Parts & cost hint / 备件与费用参考**
No parts; template/config. / 无件；模板/配置。
**5. Prevention / 预防**
Pin export template version; `data/13`. / 锁定导出模板版本；`data/13`。

---

<a id="c7-pos-payment"></a>
## C7 POS & payment hardware / 收银与支付硬件（12 项）

<a id="c7-terminal-e01-offline"></a>
### C7-E01 Card terminal offline (dual-ISP failover check) / 银行卡终端离线（双 ISP 倒换查）
**1. Self-check / 自查**
1. Check the terminal's signal/Wi-Fi and the club's primary ISP. / 查终端信号/Wi-Fi 与场馆主 ISP。
2. If primary ISP is down, confirm the failover line is active (see `references/08` D1). / 主 ISP 断，确认备用线生效（见 `references/08` D1）。
3. Reboot the terminal once on the working line. / 在可用线上重启终端一次。
**2. Stop-line / 停手线**
**Do NOT process card payments over a member's personal hotspot without the vendor's compliant connection — it breaks PCI scope. / 勿经会员个人热点刷卡，未经供应商合规连接会破 PCI 范围。**
**3. Vendor call script / 报修话术**
"Terminal ___ offline, primary ISP down, failover active per `references/08` D1, reboot no link. Need SIM/line check." / 「终端___ 离线，主 ISP 断，备用已活（见 `references/08` D1），重启无链。需 SIM/线路查。」
**4. Parts & cost hint / 备件与费用参考**
SIM/line directional USD 0–30/mo; terminal if dead USD 80–300. / SIM/线路方向性 0–30 美元/月；终端坏 80–300 美元。
**5. Prevention / 预防**
Dual-ISP failover drill; `references/08` D1 + `data/13`. / 双 ISP 倒换演练；`references/08` D1 + `data/13`。

<a id="c7-qr-e02-no-confirm"></a>
### C7-E02 QR-code payment not confirming / 二维码支付不确认
**1. Self-check / 自查**
1. Member paid but system shows no record — first check the payment gateway dashboard. / 会员已付系统无记录——先查支付网关后台。
2. Match the transaction time and amount. / 对交易时间与金额。
3. Use the "reconcile by reference No." function. / 用「凭参考号对账」功能。
**2. Stop-line / 停手线**
**Do NOT tell the member "you weren't charged" if the gateway shows paid — they were; it is a sync lag. Verify before refunding. / 网关显示已付勿告会员「没扣」，那只是同步延迟。退款前先核实。**
**3. Vendor call script / 报修话术**
"Member paid via QR ___ at ___, gateway shows settled, POS no record. Need webhook retry + idempotency check. See `data/12`." / 「会员___ 时二维码付，网关已结，POS 无记录。需 webhook 重试+幂等查。见 `data/12`。」
**4. Parts & cost hint / 备件与费用参考**
No parts; integration. / 无件；集成。
**5. Prevention / 预防**
Hourly reconciliation alert; `data/12` + `data/13`. / 每小时对账告警；`data/12`+`data/13`。

<a id="c7-receipt-e03-mismatch"></a>
### C7-E03 Receipt mismatch / 小票金额不符
**1. Self-check / 自查**
1. Compare the POS cart total to the printed receipt line by line. / 逐行比对 POS 车总额与小票。
2. Check for a mis-applied discount or tax setting. / 查是否误用折扣或税率。
3. Reprint from the transaction, not a new sale. / 从原交易重打，非新单。
**2. Stop-line / 停手线**
**Do NOT void and re-ring "to fix the receipt" without a manager code — that hides a till discrepancy. / 勿无店长码就作废重录「修小票」，会掩盖钱箱差异。**
**3. Vendor call script / 报修话术**
"POS ___ receipt total differs from cart by ___. Tax/discount suspect. Need till report pull." / 「POS___ 小票总额与车差___。疑税/折扣。需钱箱报表提取。」
**4. Parts & cost hint / 备件与费用参考**
No parts; software/config. / 无件；软件/配置。
**5. Prevention / 预防**
End-of-day till reconcile; `data/13`. / `data/13` 日结钱箱对账。

<a id="c7-terminal-e04-swell"></a>
### C7-E04 Terminal battery swelling (STOP-LINE fire risk) / 终端电池鼓包（停手线：火灾风险）
**1. Self-check / 自查**
1. Look for a bulge in the terminal case or a non-closing battery cover. / 查终端外壳鼓起或电池盖关不上。
2. Smell for a chemical/rotten odour. / 闻有无化学/酸臭。
3. Stop using it; isolate from flammables. / 停用；远离可燃物。
**2. Stop-line / 停手线**
**FIRE RISK: A swelling battery can ignite. Power off, do NOT charge, place in a non-combustible container (metal tray), and call the vendor for safe handling. Never puncture it. / 火灾风险：鼓包电池可自燃。断电、勿充、置不燃容器（金属盘），联系供应商安全处理。绝勿刺穿。**
**3. Vendor call script / 报修话术**
"Payment terminal ___ battery swelling, powered off, isolated. Need safe pickup + replacement, NOT a charge." / 「支付终端___ 电池鼓包，已断电隔离。需安全取走+更换，勿充。」
**4. Parts & cost hint / 备件与费用参考**
Terminal directional USD 80–300; safe-disposal may cost extra. / 终端方向性 80–300 美元；安全处置或另费。
**5. Prevention / 预防**
Monthly device inspection for swell; `data/13`. / `data/13` 每月查鼓包。

<a id="c7-drawer-e05-stuck"></a>
### C7-E05 Cash drawer stuck / 钱箱卡住
**1. Self-check / 自查**
1. Confirm the drawer is not physically locked by the key. / 确认钱箱未被钥匙物理锁。
2. From the POS, send an "open drawer" command. / POS 发「开钱箱」指令。
3. Gently lift the front lip while triggering open. / 触发开时轻抬前缘。
**2. Stop-line / 停手线**
**Do NOT force the drawer with a crowbar — it bends the slide and jams the till. / 勿用撬棍强开钱箱，会弯滑轨卡死钱箱。**
**3. Vendor call script / 报修话术**
"Drawer ___ stuck, key not locked, POS open command no move. Need slide/relay." / 「钱箱___ 卡，钥匙未锁，POS 开指令不动。需滑轨/继电器。」
**4. Parts & cost hint / 备件与费用参考**
Drawer slide/relay directional USD 15–80. / 钱箱滑轨/继电器方向性 15–80 美元。
**5. Prevention / 预防**
Weekly slide clean; `data/13`. / `data/13` 每周清滑轨。

<a id="c7-scanner-e06-double"></a>
### C7-E06 Barcode scanner double-scan / 条码枪重复扫
**1. Self-check / 自查**
1. Check the scan trigger isn't stuck down. / 查扫描扳机是否卡住。
2. Reduce the "repeat scan" timeout in the scanner config. / 扫描配置里缩短「重复扫」超时。
3. Test on one barcode slowly. / 单个码慢测。
**2. Stop-line / 停手线**
**Do NOT disable the scanner "to stop double scans" — items won't ring up at all. / 勿为停重复扫而禁用扫描枪，那样商品完全不入单。**
**3. Vendor call script / 报修话术**
"Scanner ___ double-scans one item, trigger not stuck. Need debounce config." / 「扫描枪___ 单品重复扫，扳机未卡。需去抖配置。」
**4. Parts & cost hint / 备件与费用参考**
Scanner directional USD 20–120. / 扫描枪方向性 20–120 美元。
**5. Prevention / 预防**
Config locked per `data/13`. / 配置锁定；`data/13`。

<a id="c7-double-e07-settle"></a>
### C7-E07 Payment settled twice / 重复结算
**1. Self-check / 自查**
1. Search the gateway for two settlements same reference. / 网关查同参考号两笔结算。
2. Check if the member tapped twice at the terminal. / 查会员是否在终端连点两次。
3. Flag one for refund via manager approval. / 经店长批注一笔退款。
**2. Stop-line / 停手线**
**Do NOT refund from the terminal without gateway confirmation — you may double-refund. Verify in the gateway first. / 未经网关确认勿从终端退款，会退两次。先在网关核实。**
**3. Vendor call script / 报修话术**
"Duplicate settlement ref ___ on terminal ___. Gateway shows 2. Need refund path + idempotency fix. See `data/12`." / 「参考___ 在终端___ 重复结算，网关显示 2 笔。需退款路径+幂等修复。见 `data/12`。」
**4. Parts & cost hint / 备件与费用参考**
No parts; process. / 无件；流程。
**5. Prevention / 预防**
Idempotency key enforced; `data/12` + `data/13`. / 强制幂等键；`data/12`+`data/13`。

<a id="c7-offline-e08-voucher"></a>
### C7-E08 Offline vouchers when all payments down (business continuity) / 全支付中断的离线凭证（业务连续性）
**1. Self-check / 自查**
1. Declare "cash/ voucher only" at the desk. / 前台宣布「仅现金/凭证」。
2. Write a paper voucher with member ID, amount, time, staff sign. / 开纸质凭证：会员号、金额、时间、员工签字。
3. Reconcile all vouchers the moment any payment line returns. / 任一支付恢复即全量对账。
**2. Stop-line / 停手线**
**Do NOT let members "just go, pay later" without a signed voucher and ID — that is uncollected revenue. / 勿让会员「先走后付」而无签字凭证与 ID，那是未收营收。**
**3. Vendor call script / 报修话术**
"All payment lines down, running paper vouchers per BCP. Need bulk reconciliation import when up. See `data/12`." / 「全支付中断，按 BCP 走纸质凭证。恢复后需批量对账导入。见 `data/12`。」
**4. Parts & cost hint / 备件与费用参考**
No parts; paper + process. / 无件；纸+流程。
**5. Prevention / 预防**
BCP drill quarterly; `data/13` + `playbooks/08`. / 每季度 BCP 演练；`data/13`+`playbooks/08`。

<a id="c7-pci-e09-flag"></a>
### C7-E09 PCI red flags / PCI 红旗
**1. Self-check / 自查**
1. Ask staff: are we ever writing card numbers on paper? / 问员工：是否曾在纸上写卡号？
2. Check the terminal screen is not visible to queue members. / 查终端屏不对排队会员可见。
3. Confirm receipts truncate the PAN (only last 4 digits). / 确认小票隐去卡号（仅后 4 位）。
**2. Stop-line / 停手线**
**PCI: NEVER write full card numbers, CVV, or PIN on any paper, note, or screenshot. If found, destroy it and report to the QSA/manager immediately. / PCI：绝不在任何纸、便签、截图标全卡号、CVV 或密码。发现即销毁并立即报 QSA/店长。**
**3. Vendor call script / 报修话术**
"Need our PCI scope review: terminals ___, receipt truncation confirmed, no card data stored. See `references/08`." / 「需 PCI 范围复核：终端___，小票已隐去，无卡数据存储。见 `references/08`。」
**4. Parts & cost hint / 备件与费用参考**
No parts; compliance. / 无件；合规。
**5. Prevention / 预防**
PCI awareness training; `data/13`. / `data/13` PCI 意识培训。

<a id="c7-cert-e10-expiry"></a>
### C7-E10 Terminal certificate expiry / 终端证书过期
**1. Self-check / 自查**
1. Check the terminal error: "certificate expired/invalid". / 查终端错：「证书过期/无效」。
2. Confirm the terminal clock/date is correct (see C9 time drift). / 确认终端时钟正确（见 C9 时间漂移）。
3. Trigger a cert refresh from the vendor portal. / 供应商门户触发证书刷新。
**2. Stop-line / 停手线**
**Do NOT set the terminal date far in the past "to make the cert valid" — it breaks every secure handshake. / 勿把终端日期调回过去「让证书有效」，会破坏所有安全握手。**
**3. Vendor call script / 报修话术**
"Terminal ___ cert expired error, clock correct, refresh failed. Need cert push." / 「终端___ 证书过期错，时钟对，刷新失败。需证书推送。」
**4. Parts & cost hint / 备件与费用参考**
No parts; cert lifecycle. / 无件；证书生命周期。
**5. Prevention / 预防**
Cert expiry calendar alert; `data/13`. / `data/13` 证书过期日历告警。

<a id="c7-dynamic-e11-qr-dead"></a>
### C7-E11 Dynamic QR display dead / 动态二维码屏坏
**1. Self-check / 自查**
1. Confirm the display has power (LED). / 确认显示屏有电（LED）。
2. Reboot the display; many recover from a hung page. / 重启显示屏；多数能从卡页恢复。
3. Switch to a printed static QR as fallback. / 切到打印静态二维码兜底。
**2. Stop-line / 停手线**
**Do NOT let members scan a staff personal QR "just this once" for club payment — that mixes personal and club funds (compliance + tax risk). / 勿让会员扫员工个人二维码收场馆款，那混同个人与场馆资金（合规+税务风险）。**
**3. Vendor call script / 报修话术**
"Dynamic QR display ___ dead, reboot no help, using paper fallback. Need display/SKU." / 「动态二维码屏___ 坏，重启无效，用纸质兜底。需屏/型号。」
**4. Parts & cost hint / 备件与费用参考**
Display directional USD 30–200. / 显示屏方向性 30–200 美元。
**5. Prevention / 预防**
Spare paper QR at desk; `data/13`. / 前台备纸质 QR；`data/13`。

<a id="c7-tips-e12-config"></a>
### C7-E12 Tips/rounding config errors / 小费/舍入配置错
**1. Self-check / 自查**
1. Check the rounding rule (0.5 / whole / no rounding) per market. / 查舍入规则（0.5/整数/不舍）按市场。
2. Check the tip preset percentages. / 查小费预设比例。
3. Run a test sale of a tricky amount (e.g. 9.99). / 测一笔刁钻金额（如 9.99）。
**2. Stop-line / 停手线**
**Do NOT change rounding to "always round up" — in some markets that is a consumer-protection violation (HI-3 adjacent). Confirm local rule. / 勿改「总是进位」，部分市场属消保违规（近 HI-3）。先确认当地规则。**
**3. Vendor call script / 报修话术**
"POS ___ rounding/tip wrong for market ___. Need config per local rule. See `references/10`." / 「POS___ 舍入/小费不符市场___。需按当地规则配置。见 `references/10`。`
**4. Parts & cost hint / 备件与费用参考**
No parts; config. / 无件；配置。
**5. Prevention / 预防**
Config review at go-live + annually; `data/13`. / 上线+每年配置复审；`data/13`。

---

<a id="c8-signage-av"></a>
## C8 Digital signage & studio AV / 数字标牌与教室 AV（12 项）

<a id="c8-signage-e01-black"></a>
### C8-E01 Screen black but power on / 屏黑但通电
**1. Self-check / 自查**
1. Confirm the source (media player) is on and sending signal. / 确认信号源（播放器）开机并在发信号。
2. Check the HDMI/display cable is seated at both ends. / 查 HDMI/显示线两端插紧。
3. Try the menu/remote "input" switch. / 遥控器试「输入源」切换。
**2. Stop-line / 停手线**
**Do NOT open the panel — backlights carry high voltage; refer to AV vendor. / 勿开屏，背光高压；交 AV 供应商。**
**3. Vendor call script / 报修话术**
"Signage ___ black, player powered, HDMI reseated, no image. Need panel/board." / 「标牌___ 黑，播放器通电，HDMI 重插无图。需屏/板。」
**4. Parts & cost hint / 备件与费用参考**
Panel/mainboard directional USD 80–500. / 屏/主板方向性 80–500 美元。
**5. Prevention / 预防**
Cable check monthly; `data/13`. / `data/13` 每月查线。

<a id="c8-signage-e02-bootloop"></a>
### C8-E02 Signage player boot loop / 播放器反复重启
**1. Self-check / 自查**
1. Pull power, wait 30s, reboot once. / 拔电等 30 秒，重启一次。
2. Check the SD/USB for corruption; reflash the image. / 查 SD/USB 损坏；重刷镜像。
3. Confirm the network isn't pushing a bad update. / 确认网络未推坏更新。
**2. Stop-line / 停手线**
**Do NOT keep power-cycling a player that boots to a crash — it can corrupt the storage further. / 勿对崩溃重启的播放器反复断电，会进一步损存储。**
**3. Vendor call script / 报修话术**
"Player ___ boot-loops, reflashed image, still loops. Need RMA/replace." / 「播放器___ 反复重启，重刷仍环。需 RMA/换。」
**4. Parts & cost hint / 备件与费用参考**
Player directional USD 40–250. / 播放器方向性 40–250 美元。
**5. Prevention / 预防**
Stable image + offline fallback; `data/13`. / 稳定镜像+离线兜底；`data/13`。

<a id="c8-content-e03-wrong"></a>
### C8-E03 Wrong content playing (CMS timezone trap) / 播错内容（CMS 时区陷阱）
**1. Self-check / 自查**
1. Check the CMS schedule timezone vs the screen's local timezone. / 查 CMS 排期时区与屏本地时区。
2. Confirm the player clock is correct (see C9 time drift). / 确认播放器时钟对（见 C9 时间漂移）。
3. Push the correct playlist manually. / 手动推正确播放列表。
**2. Stop-line / 停手线**
**Do NOT "fix" by setting the player to a wrong timezone to match the CMS — it breaks all timed content. Fix the CMS source of truth. / 勿为匹配 CMS 把播放器设错时区，会毁所有定时内容。修 CMS 真相源。**
**3. Vendor call script / 报修话术**
"Screen ___ plays wrong playlist, CMS tz UTC, screen tz local. Need CMS tz correction." / 「屏___ 播错列表，CMS 时区 UTC，屏本地。需 CMS 时区修正。」
**4. Parts & cost hint / 备件与费用参考**
No parts; CMS config. / 无件；CMS 配置。
**5. Prevention / 预防**
Timezone audit in `data/13`. / `data/13` 时区审计。

<a id="c8-hdmi-e04-handshake"></a>
### C8-E04 HDMI handshake failures / HDMI 握手失败
**1. Self-check / 自查**
1. Unplug HDMI at both ends, wait, reseat firmly. / 两端拔 HDMI，等，重插紧。
2. Try a different HDMI port on the source. / 信号源换 HDMI 口。
3. Lower resolution to 1080p as a test. / 降分辨率到 1080p 测。
**2. Stop-line / 停手线**
**Do NOT force a 4K/120Hz signal the cable can't carry — it handshakes then drops; use a rated cable. / 勿强发线带不动的 4K/120Hz，会握手后掉；用达标线。**
**3. Vendor call script / 报修话术**
"Source ___ to screen ___ HDMI no signal intermittently, reseated, same. Need rated cable/extender." / 「源___ 到屏___ HDMI 间歇无信号，重插同。需达标线/延长器。」
**4. Parts & cost hint / 备件与费用参考**
HDMI cable/extender directional USD 10–80. / HDMI 线/延长器方向性 10–80 美元。
**5. Prevention / 预防**
Use certified cables; `data/13` inventory. / 用认证线；`data/13` 库存。

<a id="c8-projector-e05-overheat"></a>
### C8-E05 Projector overheating shutdown mid-class / 投影课中过热关机
**1. Self-check / 自查**
1. Check the air filter for dust clog. / 查空气滤网是否积灰堵。
2. Confirm nothing blocks the exhaust. / 确认排风无遮挡。
3. Let it cool fully before restarting. / 彻底冷却再重启。
**2. Stop-line / 停手线**
**Do NOT restart a hot projector immediately — thermal cycling cracks the lamp; wait 30+ min. / 勿立即重启发烫投影，热循环会裂灯；等 30+ 分钟。**
**3. Vendor call script / 报修话术**
"Projector ___ overheats mid-class, filter cleaned, still trips. Need fan/lamp check." / 「投影___ 课中过热，滤网已清仍跳。需风扇/灯查。」
**4. Parts & cost hint / 备件与费用参考**
Lamp/fan directional USD 50–400. / 灯/风扇方向性 50–400 美元。
**5. Prevention / 预防**
Filter clean monthly; `data/13`. / `data/13` 每月清滤网。

<a id="c8-mic-e06-dropout"></a>
### C8-E06 Mic dropouts / 麦克风断音
**1. Self-check / 自查**
1. Swap the mic battery. / 换麦电池。
2. Check for another device on the same frequency (clash). / 查同频其他设备（冲突）。
3. Move the receiver antenna clear of metal. / 接收天线远离金属。
**2. Stop-line / 停手线**
**Do NOT crank transmit power to "fix" dropouts — it causes co-channel interference with neighbouring clubs. / 勿为修断音拉发射功率，会干扰邻馆同频。**
**3. Vendor call script / 报修话术**
"Mic ___ drops out, fresh battery, freq clash suspected. Need clean frequency plan." / 「麦___ 断音，新电池，疑同频冲突。需干净频点规划。」
**4. Parts & cost hint / 备件与费用参考**
Mic/battery directional USD 20–200. / 麦/电池方向性 20–200 美元。
**5. Prevention / 预防**
Frequency plan + battery rotation; `data/13`. / 频点规划+电池轮换；`data/13`。

<a id="c8-amp-e07-hum"></a>
### C8-E07 Amp hum / 功放交流声
**1. Self-check / 自查**
1. Check all audio grounds are bonded (no ground loop). / 查音频地是否共接（无地环）。
2. Unplug sources one by one to find the hum source. / 逐个拔信号源定位哼声源。
3. Use a DI box on the offending source. / 对该源加 DI 盒。
**2. Stop-line / 停手线**
**Do NOT lift the safety ground on the amp to kill hum — that removes earth protection. Use a proper ground isolator. / 勿为消哼声断开功放保护地，那移除接地保护。用正规隔离器。**
**3. Vendor call script / 报修话术**
"AV rack ___ amp hums, ground loop suspected. Need isolator/ground plan." / 「AV 机柜___ 功放哼声，疑地环。需隔离器/接地规划。」
**4. Parts & cost hint / 备件与费用参考**
DI/isolator directional USD 10–60. / DI/隔离器方向性 10–60 美元。
**5. Prevention / 预防**
Rack grounding audit; `data/13`. / `data/13` 机柜接地审计。

<a id="c8-speaker-e08-crackle"></a>
### C8-E08 Speaker crackle / 音箱破音
**1. Self-check / 自查**
1. Wiggle the speaker cable at both ends — crackle on move = loose. / 两端晃音箱线——动则响即松。
2. Lower the amp level; clipping causes crackle. / 降功放电平；削波致破音。
3. Swap the speaker to isolate. / 换音箱定位。
**2. Stop-line / 停手线**
**Do NOT run the amp into clipping for a whole class — it can blow the tweeter. / 勿整节课让功放削波，会烧高音。**
**3. Vendor call script / 报修话术**
"Speaker ___ crackles on cable move, amp not clipping. Need connector/voice-coil." / 「音箱___ 动线破音，功放未削波。需接头/音圈。」
**4. Parts & cost hint / 备件与费用参考**
Speaker/driver directional USD 30–300. / 音箱/单元方向性 30–300 美元。
**5. Prevention / 预防**
Connector check quarterly; `data/13`. / `data/13` 每季度查接头。

<a id="c8-bt-e09-pairing"></a>
### C8-E09 Bluetooth pairing chaos in cycling studio / 动感单车室蓝牙配对乱
**1. Self-check / 自查**
1. Clear old pairings on the studio receiver. / 清单车室接收器旧配对。
2. Pair one coach device only as the source. / 仅配对一台教练设备作音源。
3. Keep member phones in bag mode (BT off) during class. / 课中会员手机蓝牙关（放包）。
**2. Stop-line / 停手线**
**Do NOT pair every member phone to the studio speakers — it creates a pairing war and drops audio. / 勿把每部会员手机都配到教室音响，会引发配对战并断音。**
**3. Vendor call script / 报修话术**
"Cycling studio ___ BT chaos, many paired. Need coach-only pairing policy + firmware." / 「单车室___ 蓝牙乱，配很多。需仅教练配对策略+固件。」
**4. Parts & cost hint / 备件与费用参考**
Receiver directional USD 40–200. / 接收器方向性 40–200 美元。
**5. Prevention / 预防**
Policy + firmware lock; `data/13`. / 策略+固件锁；`data/13`。

<a id="c8-screen-e10-burnin"></a>
### C8-E10 Screen burn-in / 屏烧印
**1. Self-check / 自查**
1. Confirm burn-in (ghost logo) vs temporary image retention. / 确认烧印（残影 Logo）vs 临时残像。
2. Run a screen-wash/color-cycle for an hour. / 跑一小时洗屏/彩条。
3. If permanent, plan replacement. / 若永久，排更换。
**2. Stop-line / 停手线**
**Do NOT leave a static logo on 24/7 — that is what burns the panel; use a screensaver/rotation. / 勿 24/7 留静态 Logo，那正是烧屏原因；用屏保/轮播。**
**3. Vendor call script / 报修话术**
"Signage ___ shows permanent logo burn-in. Need panel replace + rotation policy." / 「标牌___ 永久 Logo 烧印。需换屏+轮播策略。」
**4. Parts & cost hint / 备件与费用参考**
Panel directional USD 80–500. / 屏方向性 80–500 美元。
**5. Prevention / 预防**
Screensaver/rotation; `data/13`. / 屏保/轮播；`data/13`。

<a id="c8-mirror-e11-fog"></a>
### C8-E11 Mirror-display fog damage / 镜面屏雾气损坏
**1. Self-check / 自查**
1. If fog forms behind the glass, power off and dry the room. / 若玻璃后起雾，断电并干燥房间。
2. Do NOT wipe inside the sealed mirror. / 勿擦密封镜内部。
3. Check the studio HVAC humidity. / 查教室空调湿度。
**2. Stop-line / 停手线**
**Do NOT mount a display mirror in a high-humidity studio without an IP rating — condensation kills it. / 勿在无 IP 等级的高湿教室装镜显，冷凝会毁屏。**
**3. Vendor call script / 报修话术**
"Mirror display ___ fogged inside, sealed. Need IP-rated replace + humidity control." / 「镜显___ 内部起雾，密封。需 IP 等级换+湿度控制。」
**4. Parts & cost hint / 备件与费用参考**
IP-rated display directional USD 100–600. / IP 等级屏方向性 100–600 美元。
**5. Prevention / 预防**
Humidity control + IP spec; `data/13`. / 湿度控制+IP 规格；`data/13`。

<a id="c8-volume-e12-limit"></a>
### C8-E12 Volume-limit compliance (noise regulations near residential) / 音量合规（近住宅噪声法规）
**1. Self-check / 自查**
1. Measure the studio SPL at the wall nearest residences. / 测最靠住宅的墙侧声压级。
2. Compare to the local limit (🔄 varies by market — verify via `tools/04`). / 对比当地限值（🔄 随市场变，经 `tools/04` 核实）。
3. Cap the amp at the compliant level. / 功放限定合规电平。
**2. Stop-line / 停手线**
**🔄 Compliance: Exceeding local noise limits can mean fines or licence loss. Never raise volume "because the coach wants it" beyond the legal cap. Verify the market rule before any change. / 🔄 合规：超当地噪声限可罚款或吊照。绝勿为「教练想」超法定上限。改动前先核实市场规则。**
**3. Vendor call script / 报修话术**
"Studio ___ near residences, SPL ___ dB at wall, limit ___ per `tools/04`. Need hard limiter set." / 「教室___ 近住宅，墙侧___分贝，限值___（经 `tools/04`）。需硬限幅设定。」
**4. Parts & cost hint / 备件与费用参考**
Limiter directional USD 20–120. / 限幅器方向性 20–120 美元。
**5. Prevention / 预防**
SPL log + legal check; `references/10` + `data/13`. / 声压记录+法务查；`references/10`+`data/13`。

---

<a id="c9-cctv"></a>
<a id="c8-security"></a>
## C9 CCTV & security / 监控与安防（10 项）

> Router alias: the intake router (`tools/00`) links CCTV symptoms to `#C8-security`; this anchor resolves here (CCTV lives in C9 per the category map). / 路由别名：路由器将 CCTV 症状链到 `#C8-security`，此锚点在此解析（按类别图 CCTV 属 C9）。

<a id="c9-camera-e01-offline"></a>
### C9-E01 Camera offline / 摄像头离线
**1. Self-check / 自查**
1. Check the camera's PoE switch port link light. / 查相机 PoE 交换机口连线灯。
2. Reboot the camera from the NVR or PoE port. / 从 NVR 或 PoE 口重启相机。
3. Confirm the cable isn't cut (see C10 cable damage). / 确认线未断（见 C10 线缆损）。
**2. Stop-line / 停手线**
**Do NOT ignore a camera offline in a high-risk zone (entry, gym floor) — it is a security blind spot; restore fast. / 勿忽视高风险区（入口、器械区）相机离线，那是安防盲区；速恢复。**
**3. Vendor call script / 报修话术**
"Camera ___ offline, PoE port ___ no link, reboot no help. Need port/cable/cam check." / 「相机___ 离线，PoE 口___ 无链，重启无效。需口/线/机查。」
**4. Parts & cost hint / 备件与费用参考**
Camera/PoE directional USD 30–250. / 相机/PoE 方向性 30–250 美元。
**5. Prevention / 预防**
Port + cable monitor; `data/13`. / 端口+线缆监控；`data/13`。

<a id="c9-nvr-e02-full"></a>
### C9-E02 NVR disk full / overwrite policy vs retention / NVR 盘满（覆盖策略 vs 留存）
**1. Self-check / 自查**
1. Check the NVR storage % and overwrite setting. / 查 NVR 存储%与覆盖设置。
2. Confirm overwrite is ON so recording continues. / 确认覆盖开，录影续。
3. Compare retained days to the legal minimum (see `references/12`). / 留存天数对比法定最低（见 `references/12`）。
**2. Stop-line / 停手线**
**Do NOT set "no overwrite" to "keep everything" — the NVR stops recording when full, losing live evidence. Balance retention vs legal minimum. / 勿设「不覆盖全保留」，NVR 满即停录，丢实时证据。留存须平衡法定最低。**
**3. Vendor call script / 报修话术**
"NVR ___ disk full, overwrite ON, retains ___d, legal min ___d per `references/12`. Need storage add." / 「NVR___ 盘满，覆盖开，留___天，法定最低___天（见 `references/12`）。需扩容。」
**4. Parts & cost hint / 备件与费用参考**
HDD directional USD 40–200. / 硬盘方向性 40–200 美元。
**5. Prevention / 预防**
Retention vs legal review; `references/12` + `data/13`. / 留存vs法定复审；`references/12`+`data/13`。

<a id="c9-night-e03-noise"></a>
### C9-E03 Night image noise / 夜景噪点
**1. Self-check / 自查**
1. Check the IR LEDs are on at night. / 查夜间红外灯亮。
2. Clean the dome/glass of dust and spider web. / 清球罩/玻璃灰与蛛网。
3. Lower the gain or enable WDR if available. / 降增益或开宽动态（若有）。
**2. Stop-line / 停手线**
**Do NOT add external floodlights pointing at the lens — it washes the image and blinds IR. / 勿加对着镜头的补光，会冲白画面并废红外。**
**3. Vendor call script / 报修话术**
"Camera ___ noisy at night, IR on, glass clean. Need low-light firmware/sensor." / 「相机___ 夜噪，红外开、玻璃净。需低照度固件/传感器。」
**4. Parts & cost hint / 备件与费用参考**
Camera directional USD 40–300. / 相机方向性 40–300 美元。
**5. Prevention / 预防**
Lens clean monthly; `data/13`. / `data/13` 每月净镜。

<a id="c9-camera-e04-fog"></a>
### C9-E04 Camera fogged in humid zones / 湿区相机起雾
**1. Self-check / 自查**
1. Check the housing has a working breather/desiccant. / 查护罩透气阀/干燥剂是否有效。
2. Confirm the heater (if fitted) is on. / 确认加热（若有）开。
3. Wipe external condensation only. / 仅擦外部冷凝。
**2. Stop-line / 停手线**
**Do NOT open the dome in humid areas to "wipe inside" — moisture enters and fogs permanently. / 勿在湿区开球罩「擦内」，湿气进会永久雾。**
**3. Vendor call script / 报修话术**
"Camera ___ fogged in pool area, breather old. Need IP66 + desiccant kit." / 「相机___ 泳区起雾，透气阀旧。需 IP66+干燥套。」
**4. Parts & cost hint / 备件与费用参考**
Housing/IP66 directional USD 30–200. / 护罩/IP66 方向性 30–200 美元。
**5. Prevention / 预防**
Desiccant replace quarterly; `data/13`. / `data/13` 每季度换干燥剂。

<a id="c9-export-e05-police"></a>
### C9-E05 Playback export for police request / 警方调取回放导出
**1. Self-check / 自查**
1. Verify the request is lawful (warrant/subpoena or local equivalent). / 核实请求合法（搜查令/传票或当地等价）。
2. Log the request: who, when, what cameras, what period. / 记录请求：谁、何时、哪些相机、时段。
3. Export to a sealed medium, hand to the officer. / 导到密封介质交警官。
**2. Stop-line / 停手线**
**Privacy: Only lawful requests with proper authority get footage. Never email CCTV to a member "to check their own clip" — that leaks third parties. Log every export. / 隐私：仅合法有权机关可取素材。绝勿把监控邮件给会员「看自己那段」，会泄第三方。每次导出须记录。**
**3. Vendor call script / 报修话术**
"Police request for camera ___ period ___. Lawful basis verified, exporting to sealed USB, logging access." / 「警方调相机___ 时段___。已核合法依据，导密封 U 盘并记录访问。」
**4. Parts & cost hint / 备件与费用参考**
No parts; process + log. / 无件；流程+日志。
**5. Prevention / 预防**
Access-log review; `references/12` + `data/13`. / 访问日志复审；`references/12`+`data/13`。

<a id="c9-time-e06-drift"></a>
### C9-E06 Time drift breaks evidence value (NTP) / 时间漂移毁证据价值（NTP）
**1. Self-check / 自查**
1. Check the NVR system time vs a trusted clock. / 查 NVR 系统时间对比可信钟。
2. Enable NTP to a local/time server. / 启 NTP 对本地/时间服务器。
3. Re-sync all cameras from the NVR. / 从 NVR 重新同步所有相机。
**2. Stop-line / 停手线**
**Do NOT manually set camera clocks to "about right" — evidence with wrong timestamps is challenged in court. Use NTP. / 勿把相机时间设「差不多」，错时间戳证据在庭上受质疑。用 NTP。**
**3. Vendor call script / 报修话术**
"NVR ___ time drifts ___ min/week, NTP was off. Need NTP lock + all-cam resync." / 「NVR___ 每周漂___分，NTP 关。需 NTP 锁定+全相机同步。」
**4. Parts & cost hint / 备件与费用参考**
No parts; config. / 无件；配置。
**5. Prevention / 预防**
NTP monitor; `data/13`. / `data/13` NTP 监控。

<a id="c9-motion-e07-flood"></a>
### C9-E07 Motion alerts flood / 移动告警轰炸
**1. Self-check / 自查**
1. Check the motion mask/zone — is a tree or fan inside it? / 查移动遮挡/区域——内有树或风扇？
2. Raise the sensitivity threshold. / 升灵敏度阈值。
3. Set a schedule (ignore business hours). / 设排程（营业时段忽略）。
**2. Stop-line / 停手线**
**Do NOT disable motion alerts entirely — they are the intrusion early-warning; tune the zone, not the feature. / 勿彻底关移动告警，那是入侵预警；调区域非关功能。**
**3. Vendor call script / 报修话术**
"NVR ___ motion flood, zone includes AC unit. Need zone retune + schedule." / 「NVR___ 移动轰炸，区域含空调。需区域重调+排程。」
**4. Parts & cost hint / 备件与费用参考**
No parts; config. / 无件；配置。
**5. Prevention / 预防**
Zone review quarterly; `data/13`. / `data/13` 每季度区域复审。

<a id="c9-cable-e08-ingress"></a>
### C9-E08 Cable water ingress / 线缆进水
**1. Self-check / 自查**
1. Find the low point where water entered the conduit. / 找水进管道的低位点。
2. Dry the joint; apply self-amalgamating tape. / 烘干接头；缠自融胶带。
3. Route the replacement high and drip-looped. / 换线走高并滴水弯。
**2. Stop-line / 停手线**
**Do NOT leave a wet RJ45 powering a PoE camera — it can short the port and the switch. Isolate first. / 勿留湿 RJ45 给 PoE 相机供电，会短端口与交换机。先隔离。**
**3. Vendor call script / 报修话术**
"Camera ___ cable water ingress at low point, port disabled. Need re-route + gel joint." / 「相机___ 线缆低位进水，端口禁。需重布+胶接。」
**4. Parts & cost hint / 备件与费用参考**
Cable/gel kit directional USD 10–80. / 线/胶套方向性 10–80 美元。
**5. Prevention / 预防**
Drip-loop + annual conduit check; `data/13`. / 滴水弯+每年管道查；`data/13`。

<a id="c9-illegal-e09-placement"></a>
### C9-E09 Illegal-placement discovery (HI-5: changing rooms absolute ban) / 发现违规布点（HI-5：更衣室绝对禁）
**1. Self-check / 自查**
1. If ANY camera is found in a changing room/shower, note its ID and location. / 若更衣室/淋浴发现任何相机，记其 ID 与位置。
2. Cover the lens immediately (tape/flag) but do NOT delete footage yet. / 立即遮镜头（胶布/标）但暂勿删录像。
3. Escalate to HQ + privacy officer at once. / 立即上报集团+隐私官。
**2. Stop-line / 停手线**
**HI-5: Changing rooms & showers are an ABSOLUTE no-go for any imaging device. Discovery = immediate physical removal (lens covered first), incident procedure, and legal review. Never tolerate "it was just for security". / HI-5：更衣室与淋浴是任何影像设备的绝对禁区。发现=立即物理移除（先遮镜头）、走事件流程、法务复审。绝不容忍「只是为安全」。**
**3. Vendor call script / 报修话术**
"Camera ___ discovered in changing room ___. Lens covered, escalating to HQ + privacy officer per HI-5. Need removal + incident record." / 「相机___ 发现于更衣室___。已遮镜头，按 HI-5 上报集团+隐私官。需移除+事件记录。」
**4. Parts & cost hint / 备件与费用参考**
No parts; removal + legal. / 无件；移除+法务。
**5. Prevention / 预防**
Site survey + zone ban list; `references/12` + `data/13`. / 勘点+禁区清单；`references/12`+`data/13`。

<a id="c9-nvr-e10-default"></a>
### C9-E10 NVR password default (change day one) / NVR 默认密码（首日必改）
**1. Self-check / 自查**
1. Try logging in with the vendor default (do NOT leave it). / 试默认登录（绝不留用）。
2. If default works, change it NOW to a strong unique password. / 若默认可用，立即改强唯一密码。
3. Record it in the secrets vault, not on a sticky note. / 存密库，非便利贴。
**2. Stop-line / 停手线**
**Do NOT keep a default NVR password — it is the #1 path to footage theft and privacy breach. Change before go-live. / 勿留 NVR 默认密码，那是素材被盗与隐私泄露头号路径。上线前必改。**
**3. Vendor call script / 报修话术**
"NVR ___ still on default creds. Need forced password change + 2FA where supported." / 「NVR___ 仍默认凭证。需强制改密+支持处开 2FA。」
**4. Parts & cost hint / 备件与费用参考**
No parts; security config. / 无件；安全配置。
**5. Prevention / 预防**
Default-cred scan at install; `data/13`. / `data/13` 安装时默认凭证扫描。

---

<a id="c10-network"></a>
## C10 Network hardware & server closet / 网络硬件与机房（12 项）

<a id="c10-internet-e01-down"></a>
### C10-E01 Whole-club internet down flowchart / 全馆断网流程图
**1. Self-check / 自查**
1. Check the router/ONT link light at the club. / 查场馆路由器/光猫连线灯。
2. Reboot the router + ONT, 30s apart. / 重启路由+光猫，间隔 30 秒。
3. Call the ISP with the account No. if still down. / 仍断则凭账号号叫 ISP。
**2. Stop-line / 停手线**
**Do NOT reboot the ISP fibre ONT repeatedly — it can lock the line for 15+ min. One reboot, then wait. / 勿反复重启 ISP 光猫，会锁线 15+ 分钟。重启一次然后等。**
**3. Vendor call script / 报修话术**
"Account ___ whole club down, ONT link off, one reboot done, still off. Need line test." / 「账号___ 全馆断，光猫无链，已重启一次仍断。需线路检测。」
**4. Parts & cost hint / 备件与费用参考**
Usually ISP; ONT if dead USD 0–80. / 多属 ISP；光猫坏 0–80 美元。
**5. Prevention / 预防**
Dual-ISP failover (see `references/08` D1) + `data/13`. / 双 ISP 倒换（见 `references/08` D1）+ `data/13`。

<a id="c10-wifi-e02-dead"></a>
### C10-E02 Single-zone Wi-Fi dead / 单区 Wi-Fi 死
**1. Self-check / 自查**
1. Check that zone's AP link light at the switch. / 查该区 AP 在交换机的连线灯。
2. Reboot the AP (PoE off/on at the port). / 重启 AP（端口 PoE 关/开）。
3. Walk the zone with a phone to map the dead spot. / 手机走查该区定位死点。
**2. Stop-line / 停手线**
**Do NOT add a cheap consumer repeater as "the fix" — it creates a second SSID and roaming chaos. Use a proper AP. / 勿加廉价消费中继「修」，会生第二 SSID 与漫游乱。用正规 AP。**
**3. Vendor call script / 报修话术**
"Zone ___ Wi-Fi dead, AP ___ port no link, rebooted, still dead. Need AP swap." / 「区___ Wi-Fi 死，AP___ 端口无链，已重启仍死。需换 AP。」
**4. Parts & cost hint / 备件与费用参考**
AP directional USD 40–250. / AP 方向性 40–250 美元。
**5. Prevention / 预防**
AP health monitor; `references/08` + `data/13`. / AP 健康监控；`references/08`+`data/13`。

<a id="c10-ap-e03-heat"></a>
### C10-E03 AP rebooting under heat / AP 高温反复重启
**1. Self-check / 自查**
1. Feel the AP — is it hot to touch? / 摸 AP——烫手？
2. Check the ceiling/vent near it is blocked. / 查附近天花/出风口是否被堵。
3. Relocate or add passive ventilation. / 移位或加被动通风。
**2. Stop-line / 停手线**
**Do NOT mount APs in direct sun or above heat sources (sauna duct, kitchen) — they thermal-reboot. / 勿把 AP 装直射阳光或热源（桑拿管、厨房）上方，会热重启。**
**3. Vendor call script / 报修话术**
"AP ___ reboots when hot, near ___ heat source. Need cooler site/industrial AP." / 「AP___ 受热重启，近___ 热源。需更冷点位/工业 AP。」
**4. Parts & cost hint / 备件与费用参考**
AP directional USD 40–250. / AP 方向性 40–250 美元。
**5. Prevention / 预防**
Thermal map of sites; `references/08` + `data/13`. / 点位热图；`references/08`+`data/13`。

<a id="c10-switch-e04-port"></a>
### C10-E04 Switch port dead / 交换机端口死
**1. Self-check / 自查**
1. Move the device to a known-good port to confirm. / 把设备换到已知好端口确认。
2. Re-seat the cable; try another cable. / 重插线；换线试。
3. Reboot the switch if multiple ports die. / 多口死则重启交换机。
**2. Stop-line / 停手线**
**Do NOT keep plugging into a port that sparks or smells — it can take the switch down. Isolate that port. / 勿继续插有火花或异味端口，会拖垮交换机。隔离该口。**
**3. Vendor call script / 报修话术**
"Switch ___ port ___ dead, device works on port ___, cable swapped. Need port/unit." / 「交换机___ 口___ 死，设备换口___ 可用、线已换。需口/机。」
**4. Parts & cost hint / 备件与费用参考**
Switch directional USD 60–600. / 交换机方向性 60–600 美元。
**5. Prevention / 预防**
Port log + spare switch; `data/13`. / 端口日志+备用交换机；`data/13`。

<a id="c10-poe-e05-budget"></a>
### C10-E05 PoE budget exceeded (new cameras killed the APs) / PoE 预算超（新相机拖垮 AP）
**1. Self-check / 自查**
1. Sum the PoE draw of all devices vs the switch budget. / 合计所有设备 PoE 功耗对比交换机预算。
2. Find what was added last (new cameras). / 找最后加的（新相机）。
3. Move some devices to a second PoE switch. / 部分设备移到第二台 PoE 交换机。
**2. Stop-line / 停手线**
**Do NOT keep adding PoE devices to one switch until APs drop — plan the budget before install. / 勿不断往一台交换加 PoE 直到 AP 掉，安装前先算预算。**
**3. Vendor call script / 报修话术**
"Switch ___ PoE budget ___W, devices draw ___W after adding cameras, APs dropping. Need second switch." / 「交换机___ PoE 预算___W，加相机后耗___W，AP 掉。需第二台。」
**4. Parts & cost hint / 备件与费用参考**
PoE switch directional USD 80–600. / PoE 交换机方向性 80–600 美元。
**5. Prevention / 预防**
PoE budget plan; `references/08` + `data/13`. / PoE 预算规划；`references/08`+`data/13`。

<a id="c10-ups-e06-beep"></a>
### C10-E06 UPS beeping table (what each beep means) / UPS 蜂鸣含义表
**1. Self-check / 自查**
1. Count the beep pattern: 1/sec = on battery; 2/sec = low battery; solid tone = overload. / 数蜂鸣：每秒1=用电池；每秒2=低电；长鸣=过载。
2. Save work; the UPS is buying you minutes. / 存盘；UPS 只给你几分钟。
3. Check load vs UPS rating. / 查负载对比 UPS 额定。
**2. Stop-line / 停手线**
**Do NOT ignore a continuous overload beep — it means the UPS is carrying too much and may drop everything. Reduce load now. / 勿忽视持续过载蜂鸣，意即 UPS 超载将全断。立即减载。**
**3. Vendor call script / 报修话术**
"UPS ___ beeps ___ pattern, load ___W of ___VA. Need battery/uprated unit." / 「UPS___ 蜂鸣___ 模式，负载___W/___VA。需电池/升容。」
**4. Parts & cost hint / 备件与费用参考**
Battery/UPS directional USD 60–600. / 电池/UPS 方向性 60–600 美元。
**5. Prevention / 预防**
Load audit + battery test; `data/13`. / 负载审计+电池测；`data/13`。

<a id="c10-ups-e07-swell"></a>
### C10-E07 UPS battery swollen (STOP-LINE) / UPS 电池鼓包（停手线）
**1. Self-check / 自查**
1. Look for a bulged UPS case or a hot exterior. / 查 UPS 外壳鼓起或外表发热。
2. Stop loading it; move gear to mains or another UPS. / 停载；设备移市电或另台 UPS。
3. Power the UPS off carefully. / 小心关 UPS。
**2. Stop-line / 停手线**
**FIRE RISK: A swollen UPS battery can vent/ignite. Power off, isolate, place in a non-combustible container, and call the vendor. Never puncture. / 火灾风险：UPS 鼓包电池可喷燃。断电隔离置不燃容器联系供应商。绝勿刺穿。**
**3. Vendor call script / 报修话术**
"UPS ___ battery swollen, powered off, isolated. Need safe removal + replacement, NOT a charge." / 「UPS___ 电池鼓包，已断电隔离。需安全拆除+更换，勿充。」
**4. Parts & cost hint / 备件与费用参考**
UPS battery directional USD 40–300. / UPS 电池方向性 40–300 美元。
**5. Prevention / 预防**
Battery inspect every 6 months; `data/13`. / `data/13` 每 6 个月查电池。

<a id="c10-router-e08-lost"></a>
### C10-E08 Router config lost after power surge / 浪涌后路由器配置丢失
**1. Self-check / 自查**
1. Check if the router boots to default (no VLANs, no Wi-Fi name). / 查路由是否启到默认（无 VLAN、无 Wi-Fi 名）。
2. Restore the last config backup. / 恢复最近配置备份。
3. If no backup, re-enter from the documented baseline. / 无备则从文档基线重录。
**2. Stop-line / 停手线**
**Do NOT "just make it work" with a consumer router — you lose VLAN/guest isolation and PCI scope. Restore the managed config. / 勿用消费路由「先通」，会丢 VLAN/访客隔离与 PCI 范围。恢复管理型配置。**
**3. Vendor call script / 报修话术**
"Router ___ config lost after surge, no backup. Need baseline restore per `references/08`." / 「路由___ 浪涌后配置丢，无备。需按 `references/08` 基线恢复。」
**4. Parts & cost hint / 备件与费用参考**
Surge protector USD 15–80; router if dead USD 60–400. / 浪涌保护器 15–80 美元；路由坏 60–400 美元。
**5. Prevention / 预防**
Config backup + surge strip; `data/13`. / 配置备份+浪涌条；`data/13`。

<a id="c10-cable-e09-damage"></a>
### C10-E09 Cable rat-bite / water damage / 线缆鼠咬/水损
**1. Self-check / 自查**
1. Trace the failed run; look for chew marks or a wet spot. / 查故障线；找咬痕或湿点。
2. For data, re-terminate or replace the segment. / 数据线重做端或换段。
3. Route replacement through conduit, off the floor. / 换线走管，离地。
**2. Stop-line / 停手线**
**Do NOT splice a mains cable with tape — that is a fire/shock hazard; use a proper junction box or replace. / 勿用胶布接主电线，是火/触电隐患；用正规接线盒或换。**
**3. Vendor call script / 报修话术**
"Cable ___ rat-bitten/water-damaged at ___, service lost. Need re-run in conduit." / 「线缆___ 鼠咬/水损于___，业务断。需穿管重布。」
**4. Parts & cost hint / 备件与费用参考**
Cable/conduit directional USD 10–100/m. / 线/管方向性 10–100 美元/米。
**5. Prevention / 预防**
Pest control + conduit; `data/13`. / 灭鼠+穿管；`data/13`。

<a id="c10-closet-e10-overheat"></a>
### C10-E10 NVR/server closet overheating (chalk dust filters) / 机房过热（粉尘滤网）
**1. Self-check / 自查**
1. Check the closet temp; >27°C is risky for gear. / 查机房温；>27°C 对设备有险。
2. Clean the intake filters (chalk/gym dust clogs them). / 清进风滤网（粉笔/场馆灰堵）。
3. Confirm exhaust fan runs. / 确认排风扇转。
**2. Stop-line / 停手线**
**Do NOT block the closet door open "for airflow" during class hours — it exposes gear to dust and tampering; add active cooling instead. / 勿为通风上课时敞机房门，会进灰且易被碰；改加主动制冷。**
**3. Vendor call script / 报修话术**
"Closet ___ at ___°C, filters clogged with chalk dust, fans on. Need filter change + AC." / 「机房___ 达___°C，滤网堵粉笔灰，风扇转。需换滤+空调。」
**4. Parts & cost hint / 备件与费用参考**
Filter/AC directional USD 20–400. / 滤网/空调方向性 20–400 美元。
**5. Prevention / 预防**
Filter clean monthly; `data/13`. / `data/13` 每月清滤网。

<a id="c10-isp-e11-blame"></a>
### C10-E11 ISP blames "your equipment" script / ISP 推「你设备问题」话术
**1. Self-check / 自查**
1. Confirm the ONT link light is OFF (line side, not your router). / 确认光猫连线灯 OFF（线路侧，非你路由）。
2. Reboot ONT once, wait 10 min. / 光猫重启一次等 10 分。
3. Note the exact time of failure for the ticket. / 记故障确切时间备单。
**2. Stop-line / 停手线**
**Do NOT accept "it's your router" when the ONT shows no line sync — that is the ISP's side. Insist on a line test. / 光猫无线路同步时勿认「是你路由」，那是 ISP 侧。坚持线路检测。**
**3. Vendor call script / 报修话术**
"ONT link OFF after reboot, line sync lost, not my router. Account ___. Need remote line test + ticket ___." / 「光猫重启后仍无链、失同步，非我路由。账号___。需远程线测+工单___。」
**4. Parts & cost hint / 备件与费用参考**
Usually ISP; no club cost. / 多属 ISP；场馆无费。
**5. Prevention / 预防**
Keep a 2nd ISP; `references/08` D1. / 留第二 ISP；`references/08` D1。

<a id="c10-hard-e12-reboot"></a>
### C10-E12 When to hard-reboot vs never / 何时硬重启 vs 绝不
**1. Self-check / 自查**
1. Soft-reboot first (admin reload) for routers/switches. / 路由/交换先软重启（管理重载）。
2. Hard power-cycle only if soft fails and after saving config. / 仅软重启无效且存配置后才硬断电。
3. Never hard-reboot during a firmware update or database write. / 固件更新或库写入中绝硬重启。
**2. Stop-line / 停手线**
**Do NOT hard-power a storage/DB server mid-write — it corrupts data. Soft-shutdown only. / 库/存储写入中勿硬断电，会损数据。仅软关。**
**3. Vendor call script / 报修话术**
"Need the safe reboot order for stack ___: soft-reload switches, hard only post-config-backup. Confirm." / 「需设备栈___ 安全重启顺序：先软重载交换，仅备份后硬重。确认。」
**4. Parts & cost hint / 备件与费用参考**
No parts; procedure. / 无件；流程。
**5. Prevention / 预防**
Reboot runbook in `data/13` + `playbooks/08`. / `data/13`+`playbooks/08` 重启手册。

---

<a id="c11-iot-sensors"></a>
## C11 IoT sensors / 物联网传感器（6 项）

<a id="c11-occupancy-e01-drift"></a>
### C11-E01 Occupancy counter drift / 人流计数漂移
**1. Self-check / 自查**
1. Compare the sensor count to a manual 10-min count. / 传感器计数对比人工 10 分钟数。
2. Clean the sensor lens (dust changes detection). / 净传感器镜（灰变检测）。
3. Re-calibrate the counting line in the app. / App 重新校准计数线。
**2. Stop-line / 停手线**
**Do NOT use occupancy count for fire-load or capacity limits — it is a marketing metric, not a safety count. / 勿把人流计数用于消防荷载或容量上限，那是营销指标非安全计数。**
**3. Vendor call script / 报修话术**
"Sensor ___ over/under counts by ___%, lens clean, recalibrated. Need firmware/AI model." / 「传感器___ 偏计___%，镜净已校准。需固件/算法。」
**4. Parts & cost hint / 备件与费用参考**
Sensor directional USD 40–250. / 传感器方向性 40–250 美元。
**5. Prevention / 预防**
Monthly calibration; `data/13`. / `data/13` 每月校准。

<a id="c11-pool-e02-false"></a>
### C11-E02 Pool water-quality sensor false alarms (HI-2) / 泳池水质传感器误报（HI-2）
**1. Self-check / 自查**
1. Cross-check the sensor reading with a manual test strip. / 传感器读数与人工试纸交叉核。
2. Calibrate the probe with the standard solution. / 用标准液校准探头。
3. Confirm the probe is not fouled by sunscreen/oil. / 确认探头未被防晒/油污。
**2. Stop-line / 停手线**
**HI-2: Sensor alerts NEVER replace lifeguard or manual water testing. A green sensor is not a substitute for the mandated human check — keep the manual test as the legal record. / HI-2：传感器告警绝不替代救生员或人工水质检测。传感器绿不等于免人工检，人工检测才是法定记录。**
**3. Vendor call script / 报修话术**
"Pool sensor ___ false high/low, manual strip normal, probe cleaned. Need recalibration, but manual test stays primary per HI-2." / 「泳池传感器___ 误报，人工试纸正常，探头已清。需校准，但人工检测依 HI-2 仍为主。」
**4. Parts & cost hint / 备件与费用参考**
Probe/cal fluid directional USD 20–150. / 探头/校准液方向性 20–150 美元。
**5. Prevention / 预防**
Manual test log + sensor calibration; `data/13`. / `data/13` 人工检测记录+传感器校准。

<a id="c11-temp-e03-offline"></a>
### C11-E03 Temp/humidity sensor offline / 温湿度传感器离线
**1. Self-check / 自查**
1. Check the sensor's battery or PoE/USB power. / 查传感器电池或 PoE/USB 电。
2. Confirm the gateway sees it (re-join). / 确认网关可见（重新入网）。
3. Move it closer to the gateway if weak. / 信号弱则移近网关。
**2. Stop-line / 停手线**
**Do NOT place temp/humidity sensors in direct airflow (AC vent, sauna exhaust) — readings become useless. / 勿把温湿度传感器放直吹气流（空调口、桑拿排），读数失效。**
**3. Vendor call script / 报修话术**
"Sensor ___ offline, battery ___%, gateway ___ can't see it. Need re-join/replace." / 「传感器___ 离线，电池___%，网关___ 不可见。需重入网/换。」
**4. Parts & cost hint / 备件与费用参考**
Sensor directional USD 15–100. / 传感器方向性 15–100 美元。
**5. Prevention / 预防**
Battery + placement audit; `data/13`. / `data/13` 电池+布点审计。

<a id="c11-energy-e04-gateway"></a>
### C11-E04 Energy meter gateway dead / 电表网关死
**1. Self-check / 自查**
1. Check the gateway power and link light. / 查网关电源与连线灯。
2. Reboot the gateway once. / 网关重启一次。
3. Confirm the meters still pulse (local display). / 确认电表仍走字（本地显）。
**2. Stop-line / 停手线**
**Do NOT open the utility meter enclosure — it is live mains; only licensed electricians touch it. / 勿开电表箱，那是带电主电，仅持证电工可触。**
**3. Vendor call script / 报修话术**
"Energy gateway ___ dead, meters still pulse, reboot no help. Need gateway replace." / 「电表网关___ 死，电表仍走字，重启无效。需换网关。」
**4. Parts & cost hint / 备件与费用参考**
Gateway directional USD 40–250. / 网关方向性 40–250 美元。
**5. Prevention / 预防**
Gateway monitor; `data/13`. / `data/13` 网关监控。

<a id="c11-battery-e05-lifecycle"></a>
### C11-E05 Sensor battery lifecycle / 传感器电池寿命
**1. Self-check / 自查**
1. Read the battery % in the sensor app. / 传感器 App 读电池%。
2. Replace at the low threshold (e.g. <20%) in a batch. / 到低位（如<20%）批量换。
3. Log the replace date per sensor. / 逐传感器记换日期。
**2. Stop-line / 停手线**
**Do NOT mix old and new batteries in a multi-cell sensor — it leaks and imbalances. / 勿在多芯传感器混新旧电池，会漏液失衡。**
**3. Vendor call script / 报修话术**
"Need bulk battery SKU for ___ sensors, qty ___, with the right chemistry." / 「需___ 传感器批量电池型号___ 个，正确化学体系。」
**4. Parts & cost hint / 备件与费用参考**
Battery directional USD 2–15 each. / 电池方向性 2–15 美元/节。
**5. Prevention / 预防**
Batch replace + log; `data/13`. / `data/13` 批量换+记录。

<a id="c11-lora-e06-interference"></a>
### C11-E06 LoRa/Wi-Fi interference / LoRa/Wi-Fi 干扰
**1. Self-check / 自查**
1. Check if a new Wi-Fi AP or microwave sits on the sensor band. / 查新 Wi-Fi AP 或微波是否占传感器频段。
2. Move the sensor gateway off the conflicting channel. / 传感器网关避开冲突信道。
3. Lower the sensor report rate to reduce collisions. / 降传感器上报率减冲突。
**2. Stop-line / 停手线**
**Do NOT crank sensor transmit power to "fix" drops — it floods the band and hurts neighbours. / 勿为修掉线拉传感器发射功率，会占满频段害邻。**
**3. Vendor call script / 报修话术**
"LoRa sensors ___ drop near new AP ___. Need channel plan + gateway move." / 「LoRa 传感器___ 在新 AP___ 旁掉。需信道规划+网关移。」
**4. Parts & cost hint / 备件与费用参考**
Gateway/antenna directional USD 20–150. / 网关/天线方向性 20–150 美元。
**5. Prevention / 预防**
Spectrum plan; `references/08` + `data/13`. / 频谱规划；`references/08`+`data/13`。

---

<a id="c12-wearables"></a>
## C12 Wearables & club devices / 穿戴与场馆设备（6 项）

<a id="c12-hr-e01-no-pair"></a>
### C12-E01 HR strap not pairing to group screen / 心率带不配对大屏
**1. Self-check / 自查**
1. Wet the strap electrodes (skin contact needs moisture). / 湿心率带电极（接触需湿）。
2. Put the strap on; many need a heartbeat to broadcast. / 戴上带；很多需心跳才广播。
3. Re-scan from the group screen, one member at a time. / 大屏逐一重扫。
**2. Stop-line / 停手线**
**Do NOT pair a member's HR strap to another member's profile — it corrupts their training record. One strap, one profile. / 勿把会员心率带配到他人档案，会污其训练记录。一带一档。**
**3. Vendor call script / 报修话术**
"HR strap ___ won't pair to screen ___, wet, worn, re-scanned. Need BLE fix." / 「心率带___ 不配屏___，已湿已戴已重扫。需 BLE 修复。」
**4. Parts & cost hint / 备件与费用参考**
Strap directional USD 15–80. / 心率带方向性 15–80 美元。
**5. Prevention / 预防**
Pre-class pair test; `data/13`. / `data/13` 课前配对测。

<a id="c12-band-e02-battery"></a>
### C12-E02 Band battery mass-failure batch / 手环电池批量失效
**1. Self-check / 自查**
1. Count how many bands died in the same week. / 统计同周坏几只手环。
2. Check the batch/lot number — likely one bad lot. / 查批次号——疑同批坏。
3. Quarantine the lot; issue from another lot. / 隔离该批；发另一批。
**2. Stop-line / 停手线**
**Do NOT distribute a known bad-lot batch "to use them up" — members get a dead band mid-class. / 勿把已知坏批「用完」，会员课上拿到死带。**
**3. Vendor call script / 报修话术**
"Band lot ___ mass battery failure, ___ of ___ dead this week. Need RMA for the lot." / 「手环批___ 电池批量失效，本周___/___ 坏。需整批 RMA。」
**4. Parts & cost hint / 备件与费用参考**
Band directional USD 3–15 each; RMA may be free. / 手环方向性 3–15 美元/只；RMA 或免费。
**5. Prevention / 预防**
Lot tracking + burn-in; `data/13`. / `data/13` 批次追踪+老化。

<a id="c12-strap-e03-sanitize"></a>
### C12-E03 Sanitation of shared straps / 共享带消毒
**1. Self-check / 自查**
1. Wipe the strap with club-approved disinfectant after each use. / 每次用后俱乐部核准消毒剂擦带。
2. Never submerge the electronics pod. / 电子模块勿浸水。
3. Air-dry on a rack, not in a closed bin. / 置架风干，非密闭桶。
**2. Stop-line / 停手线**
**Do NOT spray disinfectant directly onto the pod — it seeps in and kills the sensor. Spray on cloth first. / 勿把消毒剂直喷模块，会渗入毁传感器。先喷布再擦。**
**3. Vendor call script / 报修话术**
"Need the approved sanitizer list + pod-safe cleaning SOP for straps ___." / 「需核准消毒剂清单+模块安全清洁 SOP，手环___。」
**4. Parts & cost hint / 备件与费用参考**
Disinfectant + strap directional USD 5–30. / 消毒剂+带方向性 5–30 美元。
**5. Prevention / 预防**
Sanitize log per session; `data/13`. / `data/13` 每时段消毒记录。

<a id="c12-phone-e04-pairing"></a>
### C12-E04 Member phone-pairing support script / 会员手机配对支持话术
**1. Self-check / 自查**
1. Ask the member to enable Bluetooth + location (Android needs both). / 让会员开蓝牙+定位（安卓需两者）。
2. Tell them to select the club's device, not a neighbour's. / 让其选手场馆设备，非邻座。
3. Confirm the app has the right permission (nearby devices). / 确认 App 有正确权限（附近设备）。
**2. Stop-line / 停手线**
**Do NOT ask members to disable phone security or install unknown profiles to pair — that is a phishing vector. / 勿让会员为配对关手机安全或装未知描述文件，那是钓鱼入口。**
**3. Vendor call script / 报修话术**
"Support script: enable BT+location, pick club device ___, grant nearby-device permission. No security off." / 「支持话术：开蓝牙+定位，选手场馆设备___，给附近设备权限。勿关安全。」
**4. Parts & cost hint / 备件与费用参考**
No parts; support script. / 无件；支持话术。
**5. Prevention / 预防**
Desk cue card; `data/13`. / `data/13` 前台提示卡。

<a id="c12-firmware-e05-fleet"></a>
### C12-E05 Firmware fleet updates / 固件批量升级
**1. Self-check / 自查**
1. Stage the update on 5% of devices first. / 先对 5% 设备灰度。
2. Watch for brick/freeze reports for 24h. / 观察 24 小时有无变砖/卡。
3. Roll out the rest in waves. / 分批推其余。
**2. Stop-line / 停手线**
**Do NOT bulk-update all wearables at once during peak class — a bad image bricks the whole fleet mid-session. / 勿在高峰课中一次性批量更所有穿戴，坏镜像会课上整批变砖。**
**3. Vendor call script / 报修话术**
"Need staged fleet update plan for ___ devices, 5% canary, wave rollout, rollback image ready." / 「需___ 设备灰度批量升级计划，5% 金丝雀，分批推，回滚镜像就绪。」
**4. Parts & cost hint / 备件与费用参考**
No parts; OTA process. / 无件；OTA 流程。
**5. Prevention / 预防**
Canary + rollback in `data/13`. / `data/13` 金丝雀+回滚。

<a id="c12-lost-e06-wipe"></a>
### C12-E06 Lost-device data wipe / 丢失设备数据擦除
**1. Self-check / 自查**
1. From the admin console, mark the device lost. / 管理台标设备丢失。
2. Trigger remote wipe of any member data on it. / 触发远程擦除其上会员数据。
3. Log the wipe with time + reason. / 带时间+原因记擦除。
**2. Stop-line / 停手线**
**HI-8: A lost club device may hold member health data — wipe it remotely the moment it is reported lost; do not wait. / HI-8：丢失场馆设备或含会员健康数据，报丢即远程擦，勿等。**
**3. Vendor call script / 报修话术**
"Device ___ reported lost, remote wipe triggered, member data cleared, logged. Confirm wipe receipt." / 「设备___ 报丢，已远程擦，会员数据清，已记。确认擦除回执。」
**4. Parts & cost hint / 备件与费用参考**
No parts; remote action. / 无件；远程操作。
**5. Prevention / 预防**
Lost-device runbook; `references/12` + `data/13`. / `references/12`+`data/13` 丢设备手册。

---

## G13 Tri-Perspective Note / G13 三视角注记

**English / 英文**
This fault-tree library was authored under the G13 coverage matrix (Architect × Operator × Member) so no touchpoint is orphaned:
- **Architect (总师视角)**: Every entry cites the FDMM-agnostic L0 fix but flags escalations to L2/L3, network/integration cross-refs (`references/08`, `data/12`), and CAPEX ranges for retrofit/replace decisions (C3-E10, C10-E05). Compliance hard-lines (HI-1/4/5/6/8) are wired into the relevant entries, never optional.
- **Operator (商家/店长视角)**: Five-segment cards are printable and role-fit (front desk does self-check + vendor script; duty manager owns stop-lines and escalation). Business-continuity paths (C7-E08 offline vouchers, C10-E01 dual-ISP) protect revenue during outages.
- **Member (会员视角)**: Safety stop-lines (C5-E01 cable fray, C2-E12 egress, C4-E06 capacitor, C7-E04/C10-E07 battery swell) protect the person first. Privacy and consent (C6-E06 HI-1, C9-E05/C9-E09 HI-5, C12-E06 HI-8) protect the member's data and dignity. HI-2 keeps human oversight on pool/sensor safety.

The library is directional, not authoritative on prices: every cost is a range marked "varies by market", and volatile facts (🔄 noise limits, vendor pricing) require `tools/04` before action. No entry prescribes an L4/L5 solution to an L1 club.

**中文 / 中文**
本故障树库按 G13 覆盖矩阵（架构×商家×会员）撰写，无孤儿触点：
- **总师视角**：每条给 L0 通用修法，但标向 L2/L3 升级、网络/集成交叉引用（`references/08`、`data/12`），并对改造/更换决策给 CAPEX 区间（C3-E10、C10-E05）。合规硬线（HI-1/4/5/6/8）嵌入相关条目，非可选项。
- **商家/店长视角**：五段式可打印、按角色——前台做自查+报修话术，店长守停手线与升级。业务连续性路径（C7-E08 离线凭证、C10-E01 双 ISP）保断网时营收。
- **会员视角**：安全停手线（C5-E01 钢索、C2-E12 逃生、C4-E06 电容、C7-E04/C10-E07 电池鼓包）先保人。隐私与同意（C6-E06 HI-1、C9-E05/C9-E09 HI-5、C12-E06 HI-8）保会员数据与尊严。HI-2 保泳池/传感器人工冗余。

本库为方向性、非价格权威：每笔费用均为区间并标「随市场浮动」，易变事实（🔄 噪声限值、供应商价）行动前需 `tools/04`。无任何条目向 L1 场馆推荐 L4/L5 方案。

---

> **Legal Notice / 法律声明**: This Skill is an original personal work, for personal learning only. Any commercial use (including but not limited to resale, bundling, commercial training, SaaS delivery) without the author's written consent is prohibited. / 本 Skill 为个人原创作品，仅供个人学习使用。未经作者书面授权，禁止任何商业用途（包括但不限于转售、捆绑销售、商业培训、SaaS 化服务）。
> **Disclaimer / 免责声明**: Content is for learning and reference only and does not constitute professional advice. Users must verify key information and consult qualified professionals before business or technical decisions. Fitness-club systems touch personal safety, biometric privacy, minors' data, prepaid funds and health data; any solution MUST pass pilot validation, safety review and compliance review before rollout. / 本 Skill 提供的内容仅供学习和参考，不构成任何形式的专业意见。使用者应自行核实关键信息，并在做出商业或技术决策前咨询具备相应资质的专业人士。健身场馆方案攸关人身安全、生物识别隐私、未成年人数据、预付资金与健康数据，任何方案实施前必须经过试点验证、安全评审与合规审查。
> **Friendly Reminder / 温馨提示**: 💡 Every delivery is a continuation of trust. Verify the data, keep the logic self-consistent, keep the architecture rigorous, keep safety redundant, keep sources traceable. / 每一次方案的交付，都是信任的延续。数据要核实，逻辑要自洽，架构要严谨，安全要冗余，来源要溯源。
> **Author / 作者信息**: yinjianheng（殷健恒）| yinjianheng@foxmail.com | WeChat 微信：YJH-yinjianheng
