# Micro-Details Ledger / 微细节总账

> **Cluster / 集群**: O (Micro-details 100+)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify facility/vendor/pricing facts every 180 days via `tools/04`; regulation-linked items must pass `tools/05` before citing.
> **Cross-references / 交叉引用**: SKILL.md (HI-1~HI-8, Clusters D/F/M/R/T), `data/10-hardware-fault-tree-library.md`, `data/11-network-fault-tree-library.md`, `data/12-software-fault-tree-library.md`, `data/21-anti-pattern-library.md`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.

---

## Preamble — Honesty Red Line / 前言·诚实红线

> The "failure story" snippets below are **archetypal patterns**, not claimed real cases. They describe the *shape* of how a detail bites in production, drawn from common industry experience, not from any specific named club or incident. Treat them as cautionary patterns to pre-empt, not as citations of real events.
> 下列"翻车案例"均为**原型模式**，并非声称的真实案例。它们描述的是某类细节在真实运营中"如何咬人"的典型形态，来自行业常见经验，不指向任何具名场馆或事件。请将其视为用于提前防范的警示模式，而非真实事件引用。

> Every entry is bilingual (English first, Chinese below) and carries four parts: Detail / 细节, Why it bites / 痛点, Fix / 规则, Related / 关联.
> 每条均为双语（英文在上、中文在下），含四部分：细节、痛点、规则、关联。

---

## 1. Facility & Infrastructure / 场馆与基础设施

### FACILITY-01 Cable ends must both be labeled on day one {#md-001-cable-label-both-ends}

**Detail / 细节**: Label BOTH ends of every network and power cable on installation day, not just the visible end. 安装当天给每根网线与电源线**两端**都贴标签，不只贴看得见的一端。
Cables that look identical above the ceiling look identical in the rack; unlabeled ends cost hours later. 天花板上长得一样的线，进了机柜也分不清，日后排查要花数小时。

**Why it bites / 痛点**: A contractor leaves, one cable dies six months later, and nobody can trace which end goes where. 施工方走了，半年后某根线坏了，谁也查不出两端接在哪里。
You end up pulling live cables to "find" the dead one — risking an outage you caused yourself. 只能一根根拔活线来"找"坏线，结果自己造成了停网。

**Fix / 规则**: Use a permanent label printer (not handwritten tape) on both ends + keep a floor map of cable runs. 两端都用永久标签机（别用手写胶带），并保留一份走线平面图。
Photo the patch panel and store it in the facility folder. 给配线架拍照，存入场馆资料夹。

**Related / 关联**: SKILL.md Cluster D; HI-4 (fire monitor-only).

### FACILITY-02 Photograph the patch panel before any contractor visit {#md-002-patch-panel-photo}

**Detail / 细节**: Take a dated photo of the full patch panel and rack before any external contractor touches it. 任何外部施工方动手前，给整个配线架与机柜拍一张带日期的照片。
If they "tidy" a cable and break something, you have a before-state to compare. 万一他们"顺手整理"时弄断一根，你有整改前的状态可对照。

**Why it bites / 痛点**: Contractor claims "it was already like that"; you cannot prove otherwise and eat the downtime. 施工方说"本来就那样"，你无法举证，只能自己扛停机损失。
Disputes drag for weeks and the front desk stays offline. 扯皮拖好几周，前台系统一直半瘫。

**Fix / 规则**: Store the photo with a timestamp in the facility asset folder; require sign-off on the before/after state. 照片带时间戳存入场馆资产夹；要求对"整改前/后"状态签字确认。
Make "no photo, no work" a standing rule for vendors. 把"不拍照不动工"作为对供应商的硬性规矩。

**Related / 关联**: SKILL.md Cluster D; `data/11-network-fault-tree-library.md`.

### FACILITY-03 Server closet needs a door lock AND a temperature alarm {#md-003-server-closet-lock-temp}

**Detail / 细节**: The network/servers closet must have a physical door lock and an independent temperature/humidity alarm that pages someone. 网络/服务器机柜间必须同时具备实体门锁与独立的温湿度报警（能主动通知到人）。
A lock stops casual tampering; the alarm catches the AC dying at 2am. 锁防随手乱动；报警能在凌晨空调宕机时第一时间叫人。

**Why it bites / 痛点**: Someone props the door open "for airflow" during summer; gear cooks overnight and the gate controller dies before open. 夏天有人为"通风"把门支着，设备一晚上烤坏，开门前闸机控制器已经挂了。
No alarm = you find out from members queueing at the gate. 没报警=你是靠会员在闸机前排长队才发现的。

**Fix / 规则**: Install a <$30 temp sensor with SMS/WeCom alert; test it monthly. 装一个带短信/企微告警的温感（几十元级），每月测一次。
Keep the closet under 27°C and log the readings. 机柜间保持 27°C 以下并记录。

**Related / 关联**: SKILL.md Cluster D; Cluster T (physical security).

### FACILITY-04 Chalk dust kills electronics — filters quarterly {#md-004-chalk-dust-filters}

**Detail / 细节**: In studios with chalk (climbing, functional training), fine dust conducts and clogs fan filters in adjacent equipment. 在有镁粉/粉笔灰的功能训练、攀岩区，细微粉尘会导电并堵塞相邻设备的风扇滤网。
Quarterly filter cleaning on routers, switches, and access controllers near those zones is mandatory. 靠近这些区域的路由器、交换机、门禁控制器必须每季度清一次滤网。

**Why it bites / 痛点**: A switch slowly overheats, throttles, then drops the whole floor's Wi-Fi during peak class. 交换机慢慢过热、降频，最终在课程高峰时整层 Wi-Fi 掉线。
The cause is invisible until the fan is cemented shut with dust. 原因在风扇被灰"糊死"之前完全看不出来。

**Fix / 规则**: Put a removable filter on intake vents; clean on a calendar reminder, not when it fails. 进气口加可拆滤网；按日历提醒清理，别等坏了再动。
Keep chalk zones physically separated from the rack by at least a wall. 让粉尘区与机柜至少隔一道墙。

**Related / 关联**: SKILL.md Cluster C; `data/10-hardware-fault-tree-library.md`.

### FACILITY-05 The cleaner unplugs things — tape and sign sockets {#md-005-cleaner-unplug}

**Detail / 细节**: Cleaning staff routinely unplug "mystery cords" to use the socket for a vacuum, then never plug them back. 保洁员常为了插吸尘器而拔掉"不认识的线"，事后从不插回。
Tape/overnight-lock the sockets that feed gate controllers, routers, and POS. 给闸机控制器、路由器、POS 所在的插座做封条/夜间上锁。

**Why it bites / 痛点**: Monday 6am: gate won't open because the UPS was unplugged to charge a vacuum Saturday night. 周一早6点：闸机不开，因为周六晚 UPS 被拔去给吸尘器充电了。
Members blame the club, not the vacuum. 会员怪的是场馆，不是吸尘器。

**Fix / 规则**: Use red "DO NOT UNPLUG — 切勿断电" socket plates on critical loads; brief cleaners in onboarding. 关键负载插座用红色"切勿断电"面板；保洁入职时专门交代。
Add a daily open-check that includes "are the three critical sockets live?" 每日开店检查加入"三个关键插座是否通电？"

**Related / 关联**: SKILL.md Cluster L1 (daily ops); Cluster T.

### FACILITY-06 UPS outlets vs surge-only outlets are different sockets {#md-006-ups-vs-surge-outlets}

**Detail / 细节**: A UPS has battery-backed outlets AND surge-only outlets that die the moment mains fails. UPS 既有"电池后备"口，也有"仅防雷"口——后者一停电就跟着断电。
Only the battery-backed outlets protect the gate controller and primary switch. 只有电池后备口能在断电时保住闸机控制器和主交换机。

**Why it bites / 痛点**: You plug the router into the surge-only row "because it was free"; power blinks and the whole club goes dark anyway. 你把路由器插在"仅防雷"那排（因为空着），一停电全馆照样黑。
The UPS was bought but never actually doing its job. UPS 买了却从没真正起作用。

**Fix / 规则**: Label battery-backed outlets in green; test by pulling mains and watching the rack stay up. 把电池后备口标绿；拔掉市电测试机柜是否仍在线。
Critical path: controller → battery outlet → UPS → mains. 关键链路：控制器→电池口→UPS→市电。

**Related / 关联**: SKILL.md Cluster D; HI-4.

### FACILITY-07 Floor drains clog and flood the equipment room {#md-007-floor-drain-clog-flood}

**Detail / 细节**: Shower and pool-area floor drains back up; water seeks the lowest point — often the server/equipment room. 淋浴与泳区地漏会反涌，水往最低处流，常常正好淹了设备间。
A $5 drain strainer prevents a $5,000 flood. 一个几块钱的防堵滤网，能挡住一次几万元的泡水。

**Why it bites / 痛点**: A towel blocks the drain overnight; by morning the rack sits in 2cm of water. 一条毛巾半夜堵了地漏，早上机柜已泡在2厘米水里。
Insurance calls it "gradual seepage" and may deny the claim. 保险公司定性为"缓慢渗水"而拒赔。

**Fix / 规则**: Fit strainers, snake the drains monthly, and raise the rack on a 15cm plinth. 装滤网、每月通一次地漏、机柜抬高于15厘米基座。
Water-leak sensors at floor level page immediately. 地面级漏水传感器即时告警。

**Related / 关联**: SKILL.md Cluster D; Cluster T.

### FACILITY-08 RFID reader height misses wheelchair and stroller {#md-008-rfid-reader-height}

**Detail / 细节**: Wall-mounted RFID readers placed at 140cm miss wheelchair users, children, and strollers at the gate. 装在140厘米高的壁挂读卡器，会漏掉轮椅用户、儿童和推车。
Mount a second low reader or use a floor/pole reader at 90cm. 加装一个90厘米低的读卡器，或用柱式/地感读卡器。

**Why it bites / 痛点**: A member in a wheelchair cannot scan and must be hand-waved in — a compliance and dignity hole. 轮椅会员刷不上，只能被"手动放行"——既不合规范又伤尊严。
You discover it only after a complaint to a disability board. 往往是残联/监管机构接到投诉你才察觉。

**Fix / 规则**: Specify dual-height readers in the access spec; test with a wheelchair during UAT. 在门禁规格里写明双高度读卡器；验收时推轮椅实测。
Accessibility is a硬性 requirement in many APAC markets. 无障碍在多数亚太市场是硬性要求。

**Related / 关联**: SKILL.md HI-1; Cluster F (compliance).

### FACILITY-09 Power sockets behind the reception desk are a tangle trap {#md-009-reception-power-tangle}

**Detail / 细节**: The reception desk powers POS, phone, router, printer, and a display — all from one surge strip that nobody labels. 前台同时给 POS、电话、路由器、打印机、显示屏供电，全接在一个没人贴标签的插排上。
One faulty device trips the strip and the whole front desk goes dark. 任一设备故障跳闸，整个前台全黑。

**Why it bites / 痛点**: Saturday 10am rush: the printer short-circuits, the POS reboots mid-sale, the queue explodes. 周六早10点高峰：打印机短路，POS 中途重启，队伍炸了。
You cannot isolate which device without unplugging everything. 你不把全部拔光就找不到是哪个设备。

**Fix / 规则**: Separate POS/router onto the UPS battery outlets; label each plug; keep a spare strip. POS/路由器单独接 UPS 电池口；每个插头贴标；备一个插排。
Run a 5-minute "front desk power drill" quarterly. 每季度做一次5分钟"前台供电演练"。

**Related / 关联**: SKILL.md Cluster L0 (firefighting); `data/12-software-fault-tree-library.md`.

### FACILITY-10 Ceiling AP placement ignores the squat rack shadow {#md-010-ap-placement-shadow}

**Detail / 细节**: Wi-Fi access points planned on a grid ignore that steel rigs and mirrors create dead zones exactly where members stand with phones. 按网格布的天线忽略了钢架与镜面会在会员举着手机的位置正好形成死角。
Walk-test signal at chest height in the busy zones, not just at the door. 要在繁忙区"胸口高度"实测信号，而不只在门口测。

**Why it bites / 痛点**: Members complain "app won't load my QR" at the exact rack corner every evening. 会员每晚都在同一个器械角抱怨"App 刷不出二维码"。
You blame the app, but it's the RF shadow. 你怪 App，其实是信号阴影。

**Fix / 规则**: Do a heatmap survey post-install; add a small AP or antenna redirect for dead corners. 装完做热力图勘测；死角补小 AP 或调整天线方向。
Re-survey after any rig re-layout. 器械重新布局后重新勘测。

**Related / 关联**: SKILL.md Cluster D; `data/11-network-fault-tree-library.md`.

### FACILITY-11 The "spare" key to the server closet is with the GM's ex {#md-011-spare-key-orphan}

**Detail / 细节**: The only spare key to the network closet was given to a former manager and never recovered at offboarding. 机柜间唯一的备用钥匙给了前任店长，离职时从未收回。
Offboarding checklists that omit physical keys leave silent backdoors. 离职清单若不覆盖实体钥匙，就会留下无声后门。

**Why it bites / 痛点**: A disgruntled ex-staff member walks in at night and reboots the NVR "as a prank". 心怀不满的前员工夜里进来，把录像机"当恶作剧"重启了。
Police call it an inside job you enabled. 警方定性为你自己留下的内鬼通道。

**Fix / 规则**: Rekey on every offboarding; log physical-key issue/return like a credential. 每次离职都换锁芯；实体钥匙的发放/回收像账号一样登记。
Prefer electronic locks with revocable codes. 优先用可撤销密码的电子锁。

**Related / 关联**: SKILL.md Cluster T; HI-5; `data/21-anti-pattern-library.md` #ap-047-offboarding-checklist.

### FACILITY-12 Ventilation noise trips the "smart" sound system {#md-012-hvac-noise-sound}

**Detail / 细节**: Conference-room/Sauna PA systems with auto-gain mistake HVAC rumble for speech and scream feedback. 带自动增益的会议室/桑拿广播系统，会把空调轰鸣误当人声而尖叫啸叫。
Set fixed-gain or noise-gated modes in mechanical rooms. 在设备机房区设为固定增益或噪声门模式。

**Why it bites / 痛点**: Every time the AC kicks in, the studio speaker howls and classes stop. 空调一启动，教室喇叭就鬼叫，课只能停下。
Members think the club is broken. 会员以为场馆设备坏了。

**Fix / 规则**: Disable auto-gain near machinery; schedule a mic-check before each class. 靠机械处关闭自动增益；每节课前做麦克风自检。

**Related / 关联**: SKILL.md Cluster C; Cluster A (zones).

### FACILITY-13 Emergency exit gates must fail OPEN, not closed {#md-013-exit-gate-fail-open}

**Detail / 细节**: Exit/evacuation gates must fail safe-OPEN on power loss, never fail-closed. 疏散/紧急出口闸机断电时必须"故障开"，绝不能"故障关"。
A magnetic lock that drops power and relocks is a life-safety violation. 断电反而上锁的电磁锁是人身安全隐患。

**Why it bites / 痛点**: A blackout during a fire drill traps members at the exit because the lock re-engaged. 消防演练时停电，出口锁因重新通电而锁死，会员被困在出口。
This is a HI-2 / fire-egress red line. 这直接踩了 HI-2 / 消防疏散红线。

**Fix / 规则**: Specify fail-open hardware; test the "pull the plug" behavior at commissioning. 指定故障开硬件；验收时实测"拔电"表现。
Pair with the fire panel as monitor-only (HI-4). 与消防盘联动但仅监测（HI-4）。

**Related / 关联**: SKILL.md HI-2, HI-4; Cluster J.

### FACILITY-14 The rack sits where the mop bucket lives {#md-014-rack-near-mop}

**Detail / 细节**: Installing the network rack in a utility corridor means mops, buckets, and chemical spray live next to live gear. 把网络机柜装在杂务通道，意味着拖把、水桶、消毒喷雾就在带电设备旁。
One overspray corrodes a switch in a season. 一次喷雾飘移，一个季度就能腐蚀一台交换机。

**Why it bites / 痛点**: A cleaner sprays disinfectant; the mist settles on the rack and a port bank dies a slow death. 保洁喷消毒水，雾气落在机柜上，一个端口组慢慢坏死。
Intermittent faults that "no vendor can reproduce". 变成"任何供应商都复现不了"的间歇性故障。

**Fix / 规则**: Co-locate the rack in a dedicated, ventilated, locked closet — never a cleaning corridor. 机柜必须进专用、通风、上锁的房间，绝不在保洁通道。
Use closed-front racks with filtered intake. 用前面板封闭式、进气过滤的机柜。

**Related / 关联**: SKILL.md Cluster D; FACILITY-04.

### FACILITY-15 Outdoor gate reader eats the sun and the rain {#md-015-outdoor-reader-weather}

**Detail / 细节**: Outdoor gate readers need an IP65+ rating and sunshade; a cheap indoor reader dies in one monsoon season. 室外读卡器需 IP65 以上并配遮阳罩；廉价室内款一个雨季就报废。
Direct sun also washes out the LED and confuses the QR camera. 直射阳光还会让 LED 过曝、干扰二维码摄像头。

**Why it bites / 痛点**: The entry reader fogs every morning and members tap 5 times to get in. 入口读卡器每天早上有雾，会员要刷5次才进得去。
Warranty voids because it was "installed outdoors against spec". 保修因"违规装室外"作废。

**Fix / 规则**: Buy the rated-enclosure SKU; add a hood and a drip loop on the cable. 买带防护外壳的型号；加遮阳罩、线缆做滴水弯。
Seal conduit ends against insects. 导管口封堵防虫。

**Related / 关联**: SKILL.md Cluster C; `data/10-hardware-fault-tree-library.md`.

### FACILITY-16 The single 16A circuit feeds the whole club {#md-016-shared-circuit-overload}

**Detail / 细节**: Many fit-outs run the entire front desk + lighting + AC controller off one 16A circuit. 很多装修把整个前台+照明+空调控制器都挂在同一路16A上。
A space heater plugged at the desk trips the breaker and the gate dies. 前台插个电暖器就跳闸，闸机跟着死。

**Why it bites / 痛点**: Winter morning: someone plugs a heater, the breaker drops, members queue in the cold. 冬天早晨：有人插电暖器，跳闸，会员在冷风里排队。
Electrician says "it was always like that". 电工说"一直都这样"。

**Fix / 规则**: Run a dedicated circuit for IT/security loads; label the breaker. IT/安防负载单独走一路，并在电箱贴标。
Load-calculate before adding any heated device. 加任何电热设备前先算负载。

**Related / 关联**: SKILL.md Cluster D; FACILITY-06.

### FACILITY-17 Wall ports get painted over and forgotten {#md-017-wall-port-painted}

**Detail / 细节**: During a repaint, wall data ports get covered in emulsion and the labels vanish. 重新刷墙时，墙面数据口被乳胶漆盖住，标签也消失了。
Six months later nobody knows which port maps to which office. 半年后没人知道哪个口对应哪间办公室。

**Why it bites / 痛点**: You need to relocate the manager's desk and there is literally no live port to find. 你要给店长挪工位，却根本找不到一个活口。
A contractor charges a half-day just to tone out the wall. 只能请施工方花半天用寻线仪测墙。

**Fix / 规则**: Mask ports before paint; re-label immediately after; keep a port map. 刷墙前贴住端口；完工立刻重贴标；保留端口映射图。
Use color-coded faceplates per zone. 按区域用不同颜色面板。

**Related / 关联**: SKILL.md Cluster D; FACILITY-01.

### FACILITY-18 The NVR clock drifts and breaks the "alibi" {#md-018-nvr-clock-drift}

**Detail / 细节**: CCTV NVR clocks drift if not NTP-synced; footage timestamps then mismatch access logs. 录像机若不同步 NTP，时钟会漂移，录像时间戳就与门禁日志对不上。
Incident investigations need the two to agree to the minute. 事故调查要求两者时间误差在分钟级内吻合。

**Why it bites / 痛点**: A theft claim: gate log says 21:02 entry, video says 21:19 — insurer questions everything. 盗窃报案：门禁记录21:02进，录像显示21:19——保险公司全盘质疑。
Your evidence looks fabricated even though it isn't. 你的证据看起来像造假，其实只是时钟漂移。

**Fix / 规则**: Force NTP on all NVR, gate controller, and server; alert on >30s drift. 所有录像机、门禁、服务器强制 NTP；漂移超30秒即告警。
Quarterly time-consistency audit. 每季度做时间一致性核对。

**Related / 关联**: SKILL.md Cluster F; `data/16-freshness-ledger.md`.

---

## 2. Gates & Front Desk / 闸机与前台

### GATES-01 Always keep 10 blank RFID cards in stock {#md-019-blank-rfid-cards-stock}

**Detail / 细节**: Keep at least 10 blank, pre-formatted RFID cards at the desk at all times for walk-ins and replacements. 前台常备至少10张已预格式化的空白卡，供临到会员与补卡用。
A "we're out of cards" moment at 6pm Saturday is a lost sale. 周六晚6点"卡用完了"= 一笔流失的生意。

**Why it bites / 痛点**: A prospect wants to join on the spot; you can't issue a card and they "think about it" — and never return. 意向客想当场办卡，你发不出卡，他说"再想想"——再没回来。
High-intent moments are one-time windows. 高意向时刻是一次性窗口。

**Fix / 规则**: Par-level 10 cards; auto-reorder at 5; log every blank issued. 设10张安全库存，剩5张自动补；每张发出都登记。
Test a blank card on the reader monthly (cards silently demagnetize). 每月在读写器上测一张空白卡（卡会无声消磁）。

**Related / 关联**: SKILL.md Cluster L1; `data/12-software-fault-tree-library.md`.

### GATES-02 Gate offline-cache must exceed the longest ISP outage {#md-020-gate-offline-cache}

**Detail / 细节**: The gate's local offline cache (valid entry tokens) must outlast your worst realistic ISP outage, not just 15 minutes. 闸机本地离线缓存（有效入场令牌）必须撑过你最 realistic 的断网时长，而不只是15分钟。
Size it to ≥72h of member tokens if your ISP is flaky. 若运营商不稳定，按≥72小时会员令牌来配。

**Why it bites / 痛点**: A 6-hour fiber cut means the gate rejects everyone after the 15-min cache expires. 光纤断了6小时，15分钟缓存一过，闸机开始拒所有人于门外。
You manually buzz in 400 members — chaos and a staffing nightmare. 你只能手动放行400名会员——混乱且极度耗人。

**Fix / 规则**: Provision offline token validity ≥ expected max outage; test by killing WAN. 离线令牌有效期≥预期最长断网；拔 WAN 实测。
Keep a paper backup entry list for total failure. 全故障时备一份纸质入场名单。

**Related / 关联**: SKILL.md Cluster D; HI-2.

### GATES-03 Fire-drill day = gates auto-open; plan member comms {#md-021-fire-drill-gate-open}

**Detail / 细节**: On scheduled fire drills, gates must auto-release; members need a pre-written comms blurb so they don't panic. 消防演练日闸机必须自动释放；需提前准备好给会员的沟通文案，免得他们慌。
Drill days are also prime "why is the gate open?" confusion moments. 演练日也是"闸机怎么开着？"最易引发困惑的时刻。

**Why it bites / 痛点**: A drill triggers open gates; a member assumes "it's broken, free entry!" and posts it online. 演练导致闸机敞开；某会员以为"坏了，随便进"，还发上网。
Reputation dent over a miscommunication. 一次沟通失误，口碑受损。

**Fix / 规则**: Wire drill signal to fail-open; post signage + app push "scheduled drill". 将演练信号接故障开；贴标识+App推送"例行演练"。
Brief staff on the drill script. 给员工做演练话术培训。

**Related / 关联**: SKILL.md HI-2, HI-4; Cluster M.

### GATES-04 The gate reads the phone case, not the member {#md-022-gate-phone-case}

**Detail / 细节**: NFC-on-phone entry fails when the member uses a thick/metal phone case or a magnetic mount. 手机 NFC 入场在会员用厚壳/金属壳/磁吸支架时会失败。
Always issue a physical card or a wallet-tag fallback. 务必同时发实体卡或挂坠标签作为兜底。

**Why it bites / 痛点**: "Tap to enter" works at home, fails at the club; member thinks the system is down. "碰一碰"在家好使，在馆里失灵，会员以为系统挂了。
Support tickets spike every Monday. 每周一工单暴涨。

**Fix / 规则**: Default to a physical credential; treat phone-NFC as convenience only. 默认发实体凭证；手机 NFC 仅作便利项。
Document "remove case / use card" in the app FAQ. 在 App 常见问题写清"摘壳/用卡"。

**Related / 关联**: SKILL.md Cluster L0; `data/12-software-fault-tree-library.md`.

### GATES-05 Turnstile counts two for one wide shoulders {#md-023-turnstile-double-count}

**Detail / 细节**: Mechanical turnstiles can mis-count a member + gym bag as two entries, corrupting occupancy data. 机械三辊闸可能把"会员+健身包"误计为两次入场，污染在馆人数。
Occupancy drives HVAC, staffing, and fire-limit alerts. 在馆人数关系到空调、排班与消防限流告警。

**Why it bites / 痛点**: Dashboard shows 120 in-house but only 90 bodies; fire marshal queries the limit. 看板显示120人，实际只有90，消防来查限流。
Your occupancy metric is quietly wrong all year. 你的在馆指标一整年都悄悄失真。

**Fix / 规则**: Use optical/AI people-counting at the lane, not just the turnstile pulse. 用光幕/AI 人数统计，而不只靠三辊闸脉冲。
Reconcile turnstile vs camera weekly. 每周把三辊闸与摄像头数字对账。

**Related / 关联**: SKILL.md Cluster U; `data/01-kpi-benchmark-library.md`.

### GATES-06 Desk phone line is also the alarm line {#md-024-desk-phone-alarm-line}

**Detail / 细节**: The alarm panel often shares the desk's analog phone line; unplugging the phone for a VoIP swap kills the alarm path. 报警主机常与前台模拟电话线共用；为换 VoIP 而拔掉电话，会切断报警通道。
Verify the alarm has its own path before any telephony change. 任何电话系统改造前，先确认报警有独立通道。

**Why it bites / 痛点**: You "upgrade" to VoIP; a week later a break-in goes unreported to the monitoring center. 你"升级"成 VoIP；一周后被盗，监控中心没收到报警。
Insurer reduces payout for disabled alarm. 保险公司因报警失效而少赔。

**Fix / 规则**: Give the alarm a dedicated SIM/IPO connection independent of desk phones. 给报警独立的 SIM/网络通道，不依赖前台电话。
Test the alarm signal after every telecom change. 每次通信改造后测一次报警信号。

**Related / 关联**: SKILL.md Cluster T; Cluster D.

### GATES-07 The QR on the app expires mid-scan {#md-025-qr-expiry-midscan}

**Detail / 细节**: App entry QR that expires in 30s frustrates members with poor signal who can't refresh it at the gate. 入场二维码30秒就过期，信号差的会员在闸机前刷不出新的。
Set a grace period and allow a manual "show ID" fallback at the desk. 设宽限期，并允许前台"出示证件"兜底。

**Why it bites / 痛点**: Basement club, no signal, QR won't refresh, member blocked at the turnstile in front of others. 地下场馆没信号，二维码刷不出，会员在闸机前当众被拦。
Shame + churn risk. 社死+流失风险。

**Fix / 规则**: Cache a valid QR offline for the session; train desk on ID fallback. 让会话内二维码可离线缓存；前台训练证件兜底流程。
Measure "gate-block rate" as a KPI. 把"闸机拦截率"设为 KPI。

**Related / 关联**: SKILL.md Cluster U; `data/01-kpi-benchmark-library.md`.

### GATES-08 Member photo in CRM is 5 years old {#md-026-crm-photo-stale}

**Detail / 细节**: Face-gate and desk verification rely on a member photo that was uploaded at signup and never refreshed. 人脸闸机与前台核验依赖入会时上传、此后从未更新的照片。
Weight-loss/growth members become unrecognizable; false rejects rise. 会员变瘦/变壮后认不出，误拒率上升。

**Why it bites / 痛点**: A loyal member is falsely rejected at the gate and argues with staff publicly. 老会员被误拒，在闸机前和员工公开争执。
Trust damage over a stale image. 一张过期照片伤了信任。

**Fix / 规则**: Prompt a selfie re-upload every 12 months; allow desk override with logging. 每12个月提示重传自拍；前台可人工放行并留痕。
Never make face-match the only path (HI-1). 绝不让人脸匹配成为唯一路径（HI-1）。

**Related / 关联**: SKILL.md HI-1; Cluster F.

### GATES-09 The intercom to the back office is "always on" {#md-027-intercom-always-on}

**Detail / 细节**: A desk-to-backoffice intercom left in permanent open-mic mode leaks member conversations to the office. 前台到办公室的对讲长期"常开麦"，把会员对话漏给办公室。
PII spoken at the desk gets broadcast unintentionally. 前台说的会员隐私被无意间广播。

**Why it bites / 痛点**: A staff member in the office hears a member's medical note over the open mic. 办公室员工通过常开麦听到某会员的健康备注。
Privacy complaint under PDPA/PIPL-style law. 触发类 PIPL/PDPA 的隐私投诉。

**Fix / 规则**: Use push-to-talk; disable open-mic; mute by default. 用按讲即说；关闭常开麦；默认静音。
Train on "no PII over shared audio". 培训"共享音频不外泄 PII"。

**Related / 关联**: SKILL.md HI-5, HI-8; Cluster F.

### GATES-10 Receipt printer shares the only USB with the POS {#md-028-printer-pos-usb}

**Detail / 细节**: The receipt printer and a secondary scanner fight over the single POS USB hub; one reboot kills the other. 小票打印机与备用扫码枪抢同一个 POS USB 集线器，一个重启另一个就掉。
Use a powered hub with per-port overload protection. 用带每口过载保护的供电集线器。

**Why it bites / 痛点**: Printer jams, you reboot it, and the barcode scanner drops mid-checkout. 打印机卡纸你重启它，结果结账中扫码枪掉了。
Line builds; member abandons the purchase. 队伍变长；会员放弃购买。

**Fix / 规则**: Powered hub + label ports; keep a spare printer ribbon/paper box at desk. 供电集线器+端口贴标；前台备打印机色带/纸一盒。
See `data/12-software-fault-tree-library.md` printer entries. 见 `data/12` 打印机条目。

**Related / 关联**: SKILL.md Cluster L0; `data/12-software-fault-tree-library.md`.

### GATES-11 The "guest pass" QR is screenshot-shareable {#md-029-guest-pass-screenshot}

**Detail / 细节**: A guest-pass QR that is just an image can be screenshotted and shared, letting non-guests in repeatedly. 只是一张图的访客码会被截图转发，让非访客反复入场。
Bind the pass to a single device + one-time or short-window validity. 把访客码绑定单设备，并设为一次性或极短时效。

**Why it bites / 痛点**: A member screenshots a friend's pass; 10 people enter on one code in a week. 会员截图朋友的码；一周内10人用同一码进场。
You lose track of real headcount and liability. 真实人数与责任边界全乱。

**Fix / 规则**: Issue signed, expiring, device-bound passes; log each scan. 发带签名、限时、绑设备的码；每次扫码留痕。
Revoke remotely on suspicion. 有嫌疑可远程作废。

**Related / 关联**: SKILL.md Cluster T; HI-8.

### GATES-12 Front-desk tablet doubles as the staff WhatsApp phone {#md-030-desk-tablet-mixed}

**Detail / 细节**: Using the member-facing check-in tablet also for staff WhatsApp blurs contexts and drains battery at peak. 把会员自助签到平板同时当员工微信用，场景混淆且高峰掉电。
Separate the staff-comms device from the member kiosk. 员工沟通设备与会员终端必须分开。

**Why it bites / 痛点**: A member sees a staff WhatsApp pop up on the "check-in" screen — unprofessional and a data-leak surface. 会员在"签到"屏上看到员工微信弹出——既不专业又是泄露面。
The tablet dies at 7pm just as class check-in peaks. 平板晚7点没电，正好撞上课签到高峰。

**Fix / 规则**: Dedicate the kiosk to check-in only; issue staff a separate handset. 自助机只做签到；员工另发独立手机。
Enforce kiosk-lockdown mode. 自助机启用锁定模式。

**Related / 关联**: SKILL.md HI-8; Cluster M.

---

## 3. Payments & POS / 收银与支付

### PAY-01 QR paid-but-no-record at settlement cutoff {#md-031-qr-paid-no-record}

**Detail / 细节**: A member pays by QR at 23:58; the acquirer settles at 00:00 and the record lands in the next day, showing "paid but no order". 会员23:58扫码付，收单机构在00:00结算，记录落入次日，显示"已付但无订单"。
Daily reconciliation must run at a fixed hour AFTER the cutoff, not before. 日对账必须在结算截点**之后**的固定时刻跑，而不是之前。

**Why it bites / 痛点**: You reconcile at 23:30, see a "missing" payment, refund the member — then the real record arrives and you've double-paid. 你23:30对账发现"少了"一笔，给会员退款——随后真实记录到了，等于付了两次。
Cash leakage you caused yourself. 自己造成的资金漏损。

**Fix / 规则**: Know each acquirer's cutoff; schedule reconciliation 1h after; flag "pending-settle" separately. 摸清每家收单截点；对账排在其后1小时；把"待结算"单独标出。
Keep a 3-day "in-flight" ledger. 保留3天"在途"台账。

**Related / 关联**: SKILL.md Cluster R; `data/21-anti-pattern-library.md` #ap-044-payment-reconcile-hour.

### PAY-02 Never refund cash for a digital payment {#md-032-no-cash-refund-digital}

**Detail / 细节**: If a member paid by WeChat/Alipay/card, refund back to the SAME method — never hand cash. 会员用微信/支付宝/银行卡付的，必须原路退回，绝不发现金。
Cash refund of a digital payment is a classic fraud / illicit-funds vector. 数字支付发现金退款是经典的欺诈/非法资金流转路径。

**Why it bites / 痛点**: A "member" disputes a card payment with the bank AND already took your cash refund — you lose twice. 某人就银行卡支付发起争议，又已拿了你的现金退款——你赔两次。
Acquirer charges back and fines you. 收单机构追偿并罚款。

**Fix / 规则**: Policy: refunds only to original method; system-enforce, don't allow cash button. 制度：仅原路退；系统强制，禁用现金退款按钮。
Log every refund with original txn ID. 每笔退款记原交易号。

**Related / 关联**: SKILL.md HI-3; Cluster R; #ap-044.

### PAY-03 Terminal paper rolls need a spare box on-site {#md-033-terminal-paper-spare}

**Detail / 细节**: Keep at least one full box of the exact thermal roll the POS/QR terminal uses, on-site, not at a supplier. 至少备一整盒 POS/扫码终端**专用**热敏纸，放在馆内，而非在供应商处。
Wrong-width rolls jam and tear mid-receipt. 宽度不对的纸会卡纸、中途撕裂。

**Why it bites / 痛点**: Saturday noon: roll runs out, the spare is the wrong width, the line freezes. 周六中午：纸用完，备用宽度不对，队伍卡死。
Members walk without paying for add-ons. 会员没买成附加项就走了。

**Fix / 规则**: Stock the exact SKU; auto-reorder at 2 rolls; label the box. 备正确型号；剩2卷自动补；盒子贴标。
Train any staff to swap a roll in 30s. 训练任意员工30秒换纸。

**Related / 关联**: SKILL.md Cluster L0; GATES-10.

### PAY-04 The "test" payment button is live in production {#md-034-test-pay-live}

**Detail / 细节**: A sandbox/test payment toggle left on in production marks real sales as "test" and they never settle. 生产环境里若残留"测试支付"开关，真实交易会被标为"测试"而永不结算。
Gate every deploy with a check that test mode is OFF in prod. 每次发布用检查项确认生产环境测试模式已关闭。

**Why it bites / 痛点**: A month of sales shows as test transactions; the bank never credited you. 一个月的营业额都显示为测试交易，银行从没给你入账。
You discover the gap at month-end reconciliation. 月底对账才发现窟窿。

**Fix / 规则**: Separate test/prod env keys; alert if a prod txn is tagged test. 测试/生产密钥分离；生产交易被标测试即告警。
Daily "settled vs recorded" mismatch alert. 每日"已结算 vs 已记录"不符即告警。

**Related / 关联**: SKILL.md Cluster R; `data/12-software-fault-tree-library.md`.

### PAY-05 Stored-value top-up via personal QR = fund risk {#md-035-personal-qr-topup}

**Detail / 细节**: Letting a coach collect stored-value top-ups via their personal WeChat/Alipay QR mixes club funds with personal accounts. 让教练用个人微信/支付宝码收储值充值，等于把店面资金混进私人账户。
This is a fund-compliance and embezzlement red line (HI-3). 这是资金合规与挪用红线（HI-3）。

**Why it bites / 痛点**: The coach leaves owing ¥30k of "top-ups" that were never in the club ledger. 教练离职时欠着3万元"充值"从未进馆账。
Members sue the club; the club can't trace the money. 会员告场馆；场馆追不回钱。

**Fix / 规则**: All top-ups go to the club's verified merchant account only. 所有充值只进场馆认证商户号。
See `data/21` #ap-001-coach-personal-qr (💀). 见 `data/21` #ap-001（💀）。

**Related / 关联**: SKILL.md HI-3; `data/21-anti-pattern-library.md` #ap-001-coach-personal-qr.

### PAY-06 Multi-currency display rounds the wrong way {#md-036-multicurrency-rounding}

**Detail / 细节**: In cross-border/multi-currency clubs, displaying prices in a converted currency must round for DISPLAY only, never alter the settlement amount. 跨境/多币种场馆里，换算后价格只用于展示取整，绝不能改动结算金额。
Rounding the settled value creates reconciliation gaps. 对结算值取整会造成对账缺口。

**Why it bites / 痛点**: ¥99 shown as S$18.99 but settled S$19.00 — pennies leak and audit flags it. 显示¥99=新元18.99，却按19.00结算——零钱流失被审计标记。
Annual pennies become a real audit finding. 一年零钱变成实打实的审计问题。

**Fix / 规则**: Settle in the contractual currency; show converted value as "approx / 约". 按合同币种结算；换算值标"约"。
Reconcile in base currency only. 只对基准币种对账。

**Related / 关联**: SKILL.md Cluster R; `data/02-regulation-traceability-index.md`.

### PAY-07 POS offline mode silently drops the tip line {#md-037-pos-offline-tip-drop}

**Detail / 细节**: Some POS apps in offline mode record the sale but drop the optional tip/Add-on, losing coach commission data. 某些 POS 在离线模式下记了主单却丢了可选小费/附加项，教练提成数据缺失。
Staff commissions then look "short" and trust erodes. 员工提成显得"少了"，信任受损。

**Why it bites / 痛点**: A coach sees ¥0 tip on a session they know was tipped; they suspect the club is skimming. 教练看到某节课小费为0，而明知被给过；怀疑场馆克扣。
Morale and false accusations. 士气掉，还引发冤枉。

**Fix / 规则**: Queue offline tips and sync on reconnect; reconcile tips weekly. 离线小费入队，重连后同步；每周对小费对账。
Alert if offline session count ≠ synced count. 离线场次≠同步场次即告警。

**Related / 关联**: SKILL.md Cluster R; Cluster P.

### PAY-08 Refund approval is one tap on the intern's login {#md-038-refund-intern-login}

**Detail / 细节**: If refund approval is reachable from any staff login, an intern can push a ¥5k refund with no second eye. 若任意员工账号都能批退款，实习生点一下就能放5千元退款，无人复核。
Refunds need a two-person or manager-threshold rule. 退款需双人复核或店长额度规则。

**Why it bites / 痛点**: An intern "practices" a refund to a friend's account; ¥5k vanishes. 实习生拿朋友账号"练手"退款；5千元蒸发。
CCTV shows it but the policy allowed it. 监控拍到了，但制度本就允许。

**Fix / 规则**: Role-based refund caps; ≥threshold requires manager OTP. 基于角色的退款上限；超阈值需店长 OTP。
Weekly refund report to owner. 每周给老板出退款报告。

**Related / 关联**: SKILL.md Cluster I; HI-3.

### PAY-09 The card terminal firmware update breaks EMV {#md-039-terminal-firmware-emv}

**Detail / 细节**: An automatic terminal firmware update can break EMV chip reading; suddenly all card taps fail. 终端自动固件升级可能破坏 EMV 芯片读取，突然所有插卡都失败。
Stagger updates; never auto-update on a payday weekend. 分批升级；发薪周末绝不自动更。

**Why it bites / 痛点**: Payday Saturday: chips stop working, only NFC works, queue triples. 发薪周六：芯片失灵，只剩 NFC，队伍三倍长。
Members blame the club, not the vendor. 会员怪场馆，不怪供应商。

**Fix / 规则**: Pin firmware version; update off-peak with a rollback image. 锁定固件版本；非高峰更新并备回滚镜像。
Keep a manual imprint fallback for total failure. 全故障备手压凭条兜底。

**Related / 关联**: SKILL.md Cluster L0; `data/12-software-fault-tree-library.md`.

### PAY-10 "Buy 10 get 1 free" math explodes at refund {#md-040-multiplier-refund-math}

**Detail / 细节**: Package deals (buy 10, get 1 free) need a clear remaining-unit ledger; refunds mid-package require pro-rata, not full, math. 套餐（买10送1）需有清晰余次台账；套餐中途退款须按剩余比例，而非全额。
Naive "refund the whole thing" overpays. 简单"全退"会退超。

**Why it bites / 痛点**: Member used 9 of 11 sessions, cancels, and you refund the full ¥1,100 — net loss. 会员用了11次中的9次后取消，你退了全额1100元——净亏。
Promo math done on the back of a napkin. 促销算法靠拍脑袋。

**Fix / 规则**: System must compute pro-rata automatically; show the member the breakdown. 系统自动按剩余比例算；向会员展示明细。
Pre-define refund formula in the contract. 合同里先写明退款公式。

**Related / 关联**: SKILL.md HI-3; Cluster R.

### PAY-11 The payment link is sent in a group chat {#md-041-payment-link-groupchat}

**Detail / 细节**: Sending a personal payment link in a member WeChat group exposes one member's pending amount to others. 在会员微信群里发个人支付链接，会让他人看到某会员的待付金额。
Privacy + social-pressure harm. 隐私+社交压力伤害。

**Why it bites / 痛点**: A member's ¥8,000 renewal link is visible to the whole group; they feel exposed. 某会员8千元续费链接被全群看见；他觉得被曝光。
Complaint to the group and churn. 在群里投诉并流失。

**Fix / 规则**: Send payment links 1:1 only via the official channel; never in groups. 支付链接只走官方渠道一对一发；绝不进群。
Use the SCRM private-message path. 用 SCRM 私信路径。

**Related / 关联**: SKILL.md HI-8; Cluster M.

### PAY-12 Settlement bank changes without a DR test {#md-042-bank-change-no-dr}

**Detail / 细节**: Switching the settlement/acquiring bank mid-contract needs a parallel-run and a disaster-recovery check, not a hard cutover. 中途换结算/收单银行需并行运行+灾备验证，不能硬切换。
A hard cutover can misroute a day of funds. 硬切换可能让一天的资金错路。

**Why it bites / 痛点**: You flip the bank Friday; Monday shows ¥40k "in transit" with no endpoint. 周五切银行；周一显示4万元"在途"无着落。
Three days of "where is my money" panic. 三天"钱去哪了"的恐慌。

**Fix / 规则**: Parallel-run 1 week; reconcile both sides before decommission. 并行跑一周；双侧对完再下线旧通道。
Keep old endpoint warm 30 days. 旧通道保温30天。

**Related / 关联**: SKILL.md Cluster R; `data/21-anti-pattern-library.md` #ap-036-migrate-peak.

---

## 4. Membership Data / 会员数据

### MEM-01 Phone number is NOT a unique ID {#md-043-phone-not-unique}

**Detail / 细节**: Families and couples often share or reuse a mobile number across member profiles; phone is not a safe primary key. 家庭/情侣常共用或复用手机号；电话不能作为安全主键。
Use a system-assigned member ID as the key; store phone as an attribute. 用系统分配会员号作主键；手机号只是属性。

**Why it bites / 痛点**: Two sisters share a number; one's check-in merges into the other's attendance and churn score. 两姐妹共用号；一人打卡并入了另一人的出勤与流失分。
Analytics and billing both corrupt. 分析与账单双双失真。

**Fix / 规则**: Enforce unique member_id; allow multiple members per phone with role tags. 强制会员号唯一；同号多会员加关系标签。
De-dupe report monthly. 每月出重复报告。

**Related / 关联**: SKILL.md Cluster E; `data/09-algorithm-kernel-library.md`.

### MEM-02 Name order differs by market — store given/family separately {#md-044-name-order-market}

**Detail / 细节**: Given-name/family-name order flips across markets (West: given first; East Asia: family first; some double surnames). 名/姓顺序跨市场相反（西方名在前；东亚姓在前；还有复姓）。
Store given and family in separate fields; render per market. 用独立字段存名与姓；按市场渲染。

**Why it bites / 痛点**: A Japanese member's family name is printed as their first name on the cert — offensive and wrong. 日本会员的姓被印成名字，证书既错又失礼。
VIP complaint, brand damage. 大客户投诉，品牌受损。

**Fix / 规则**: Two fields + a display-format setting per market. 两字段+按市场设显示格式。
Never concatenate then split. 绝不先拼接再拆分。

**Related / 关联**: SKILL.md Cluster F; `data/06-bilingual-glossary.md`.

### MEM-03 Test members pollute analytics — prefix TEST- and filter {#md-045-test-member-pollution}

**Detail / 细节**: Staff create test members for training; if not prefixed TEST- and filtered, they skew churn, attendance, and revenue dashboards. 员工为培训建测试会员；若不标 TEST- 并过滤，会污染流失、出勤、营收看板。
A standing filter must exclude TEST- from all KPIs. 所有 KPI 须有常驻过滤器排除 TEST-。

**Why it bites / 痛点**: 40 test accounts with "attended 0 classes" drag your avg-engagement down 8% for a quarter. 40个"0节课"的测试号把季度平均活跃拉低8%。
You "fix" a problem that was Never real. 你去"修"一个根本不存在的问题。

**Fix / 规则**: Mandatory TEST- prefix + a global analytics exclude list. 强制 TEST- 前缀+全局分析排除名单。
Delete test data monthly. 每月清测试数据。

**Related / 关联**: SKILL.md Cluster E; `data/01-kpi-benchmark-library.md`.

### MEM-04 Member merge is irreversible — export first {#md-046-member-merge-irreversible}

**Detail / 细节**: Merging two member records is usually irreversible and reassigns all history; always export both BEFORE merging. 合并两个会员档案通常不可逆，会重派全部历史；合并前务必先导出两者。
One wrong merge can orphan a membership and its payments. 一次错并可能让会籍与付款变成孤儿。

**Why it bites / 痛点**: You merge a typo-duplicate but it was actually a real second account with a paid package. 你合并了"重复笔误"，但它其实是带已购套餐的真实二号账户。
The paid package vanishes from reporting. 已购套餐从报表里消失。

**Fix / 规则**: Export both CSVs, snapshot the DB, require manager approval to merge. 先导出两份CSV、给库做快照、合并需店长批准。
Log the merge with before/after IDs. 合并记前后ID日志。

**Related / 关联**: SKILL.md Cluster E; `data/21-anti-pattern-library.md` #ap-048-no-data-export.

### MEM-05 Birthday field has no year = age-gate fails {#md-047-birthday-no-year}

**Detail / 细节**: Storing birthday as month-day only (for campaigns) breaks any age verification (minors' rules, HI-6/HI-1). 只为营销存"月-日"会破坏任何年龄核验（未成年人规则、HI-6/HI-1）。
Keep full DOB where legally required, minimize elsewhere. 法定需完整生日处保留，其他处最小化。

**Why it bites / 痛点**: A "under-16 free day" campaign admits a 12-year-old to an adult-only zone because age was unknown. "16岁以下免费日"因不知年龄，让12岁孩子进了成人区。
Safeguarding incident. 监护保护事故。

**Fix / 规则**: Store DOB for age-gated products; restrict visibility by role. 年龄受限产品存完整生日；按角色限制可见性。
See HI-1/minors rules in `data/02`. 见 `data/02` 的 HI-1/未成年人规则。

**Related / 关联**: SKILL.md HI-1, HI-6; Cluster F.

### MEM-06 Email is the recovery key but 30% are typos {#md-048-email-typo-recovery}

**Detail / 细节**: Password/account recovery relies on email, but ~30% of captured emails have typos and bounce. 账号找回依赖邮箱，但约30%录入邮箱有错字会退信。
Verify email on capture with a confirmation click. 采集时用确认点击校验邮箱。

**Why it bites / 痛点**: A member locks out, the reset goes to a typo address, and they can't get back in. 会员被锁，重置信发到错字地址，再也登不回。
Support spends 20 min per case "proving" identity. 客服每例花20分钟"证明"身份。

**Fix / 规则**: Send a verification email at signup; mark unverified accounts. 注册时发验证信；标"未验证"账户。
Offer phone/SMS as alternate recovery. 提供手机/短信作为备用找回。

**Related / 关联**: SKILL.md Cluster L1; Cluster M.

### MEM-07 Member photo used for ads without consent {#md-049-photo-used-ads}

**Detail / 细节**: Pulling member check-in selfies into marketing creatives without explicit consent breaches HI-8/minimization. 未经明确同意把会员打卡自拍用于广告素材，违反 HI-8/最小化。
Consent must be specific to "marketing use of my image". 同意必须具体到"我的肖像用于营销"。

**Why it bites / 痛点**: A member spots themselves in a poster and demands removal + threatens a complaint. 会员发现自己在海报上，要求下架并扬言投诉。
Regulator sees inferred consent as no consent. 监管视"推定同意"为无同意。

**Fix / 规则**: Capture a separate marketing-consent flag; default off. 单独采集"营销同意"开关；默认关。
Audit creative assets against the consent list. 用同意名单审计素材。

**Related / 关联**: SKILL.md HI-8; Cluster F; `data/21` #ap-049-consent-screenhots.

### MEM-08 "Inactive" auto-delete destroys legal records {#md-050-inactive-autodelete}

**Detail / 细节**: A script that auto-deletes "inactive >2yr" members can erase records needed for tax/consumer disputes. 自动删"沉默超2年"会员的脚本，可能销毁税务/消费争议所需的记录。
Retention law often trumps your cleanup urge. 留存法常压过你的清理冲动。

**Why it bites / 痛点**: A 3-year consumer complaint arrives; the member was auto-purged and you can't defend. 三年后消费投诉来了；会员已被自动清掉，你无法自证。
Regulatory penalty for unlawful deletion. 因违法删除被罚。

**Fix / 规则**: Anonymize, don't delete; keep a frozen archive per retention schedule. 做匿名化而非删除；按留存期留冻结归档。
Legal hold overrides auto-purge. 法律保留优先于自动清。

**Related / 关联**: SKILL.md HI-8; Cluster F; `data/02`.

### MEM-09 Duplicated QR token after card reissue {#md-051-qr-token-dup}

**Detail / 细节**: Reissuing a lost card must invalidate the old token; otherwise the lost card's QR still opens the gate. 补发丢失卡必须作废旧令牌；否则丢卡的二维码仍能开门。
Token revocation must be atomic with reissue. 令牌撤销必须与补卡原子化同步。

**Why it bites / 痛点**: A member "loses" a card, gets a new one, and the old one (found by someone) still works for a month. 会员"丢"卡后补办，旧卡（被他人捡到）还能用一个月。
Unauthorized entries you never noticed. 你从没注意到的非法入场。

**Fix / 规则**: On reissue, revoke all prior tokens; confirm old QR rejected at gate. 补卡即作废全部旧令牌；在闸机验证旧码已拒。
Weekly revoked-token scan. 每周扫一次已撤令牌。

**Related / 关联**: SKILL.md HI-1; Cluster T.

### MEM-10 CRM "member since" resets on each renewal {#md-052-member-since-reset}

**Detail / 细节**: If renewal recreates the record, "member since" resets and loyalty tiers miscalculate. 若续费重建档案，"入会日期"会重置，导致等级权益算错。
Keep an immutable original-signup timestamp. 保留不可变的首次注册时间戳。

**Why it bites / 痛点**: A 5-year member renews and suddenly loses "gold" perks they earned. 五年会员续费后突然丢了辛苦攒的"金卡"权益。
Loyalty backlash. 忠诚反噬。

**Fix / 规则**: Separate signup_date (immutable) from last_renewal_date. 把 signup_date（不可变）与 last_renewal_date 分开。
Test renewal doesn't touch signup_date. 测续费不碰 signup_date。

**Related / 关联**: SKILL.md Cluster U; `data/01-kpi-benchmark-library.md`.

### MEM-11 Spouse on same plan, separate consent needed {#md-053-spouse-consent-separate}

**Detail / 细节**: A family plan covers two adults; marketing/health messages need EACH adult's own consent, not one spouse's. 家庭计划含两位成人；营销/健康消息需各自同意，而非一方代签。
One consent does not cover the other under HI-7. 依 HI-7，一方同意不覆盖另一方。

**Why it bites / 痛点**: You text the husband's wellness promo to the wife; she never opted in and complains. 你给妻子发本属丈夫的健康促销；她从未勾选而投诉。
Spam-law exposure. 触发反垃圾法风险。

**Fix / 规则**: Per-person consent flags even on shared plans. 即便共享计划也逐人存同意标志。
Opt-in captured at activation of each member. 每位会员激活时各自采集 opt-in。

**Related / 关联**: SKILL.md HI-7; Cluster M.

### MEM-12 Freeze/reactivate changes the billing anniversary {#md-054-freeze-anniversary-drift}

**Detail / 细节**: A membership freeze followed by reactivation can shift the billing anniversary if the system "restarts" the term. 会籍冻结后复开，若系统"重启"周期，会导致扣费周年日漂移。
Define freeze as pause, not restart. 把冻结定义为"暂停"而非"重启"。

**Why it bites / 痛点**: After a 2-month freeze the annual fee suddenly charges a month early, member disputes it. 冻结2个月后年费突然早收一个月，会员争议。
Chargeback + complaint. 拒付+投诉。

**Fix / 规则**: Model freeze as a timeline offset; never recreate the term. 冻结建模为时间轴偏移；绝不重建周期。
Show the member the next-charge date after freeze. 冻结后向会员展示下次扣费日。

**Related / 关联**: SKILL.md HI-3; Cluster R.

---

## 5. Messaging & CRM Outreach / 消息与会员触达

### MSG-01 WhatsApp template rejections are usually formatting {#md-055-whatsapp-template-format}

**Detail / 细节**: WhatsApp (Meta) template messages get rejected mostly for forbidden formatting: stray emoji in variables, unescaped braces, or promotional wording in a transactional template. WhatsApp 模板被拒多半因格式：变量里混了表情、花括号未转义、或在交易类模板写促销语。
Read Meta's template policy before submitting. 提交前先读 Meta 模板政策。

**Why it bites / 痛点**: You submit a "reminder" template with "🎉 50% OFF" inside — rejected, campaign delayed a week. 你在"提醒"模板里塞了"🎉 5折"——被拒，活动推迟一周。
Approval SLA burns your launch window. 审核 SLA 吃掉你的上线窗口。

**Fix / 规则**: Keep transactional templates plain; put promo in a separate approved template. 交易模板保持纯文本；促销放另一已审模板。
Pre-validate with Meta's sample rules. 用 Meta 样例规则预审。

**Related / 关联**: SKILL.md Cluster M; `references/17-omnichannel-messaging.md`.

### MSG-02 Quiet hours differ per market {#md-056-quiet-hours-market}

**Detail / 细节**: Acceptable send windows vary: SG strict on nighttime SMS; JP tolerant but brand-sensitive; some markets ban pre-8am/post-9pm commercial pushes. 可发送时段各异：新加坡严管夜间短信；日本较宽松但重品牌；部分市场禁早8前/晚9后商业推送。
Encode per-market quiet hours in the scheduler. 在调度器里按市场编码静默时段。

**Why it bites / 痛点**: You blast a 6am class promo in SG; telco blocks your sender ID for a month. 你在新加坡早6点群发课程促销；运营商封你发送号一个月。
All SMS dead during peak season. 旺季所有短信全死。

**Fix / 规则**: Per-market send windows + telco allow-list; default to conservative. 按市场设发送窗+运营商白名单；默认保守。
See `data/07-apac-regional-differences.md`. 见 `data/07`。

**Related / 关联**: SKILL.md HI-7; Cluster F.

### MSG-03 Birthday campaigns crash on Feb-29 members {#md-057-birthday-feb29}

**Detail / 细节**: Leap-year (Feb 29) birthdays break naive "add 1 year" date logic and can crash or skip the campaign. 闰年（2/29）生日会搞崩"加一年"的幼稚日期逻辑，导致活动崩溃或漏发。
Handle missing-day years explicitly. 显式处理"无该日"的年份。

**Why it bites / 痛点**: The birthday job throws on Feb 29 and the whole nightly batch fails silently. 生日任务在2/29抛错，整夜批处理静默失败。
Nobody gets a birthday message that month. 那个月没人收到生日消息。

**Fix / 规则**: Use date libraries that handle leap years; test with 02-29 fixtures. 用能处理闰年的日期库；用02-29样例测。
Log batch completion, alert on zero-send. 记批处理完成，零发送即告警。

**Related / 关联**: SKILL.md Cluster M; `data/12-software-fault-tree-library.md`.

### MSG-04 Unsubscribe link must work BEFORE the campaign sends {#md-058-unsubscribe-pre-send}

**Detail / 细节**: The unsubscribe link must be live and tested BEFORE any campaign launches — a dead link is an automatic compliance violation. 退订链接必须在活动发出前就可用且测过——死链=自动违规。
Test the full unsub flow on a seed list first. 先用种子名单测完整退订流程。

**Why it bites / 痛点**: You send 20k messages; the unsub link 404s; members report spam en masse. 你发了2万条；退订链接404；会员集体举报垃圾邮件。
Sender reputation destroyed overnight. 发送信誉一夜归零。

**Fix / 规则**: Pre-send checklist includes "unsub link clicked on 3 devices". 发前清单含"在3种设备上点过退订"。
Monitor unsub latency <5 min. 监控退订生效<5分钟。

**Related / 关联**: SKILL.md HI-7; `data/21` #ap-050-whatsapp-quality.

### MSG-05 LINE/WeChat rich menus break on OS updates {#md-059-line-menu-os-update}

**Detail / 细节**: Platform-rich menus (LINE Flex, WeChat menu) can break after a client OS update; the fallback should be plain text. LINE/微信富菜单（Flex/自定义菜单）可能在客户端系统更新后失效；兜底应是纯文本。
Always design a text-only fallback path. 永远设计纯文本兜底路径。

**Why it bites / 痛点**: An OS update hides your menu; members tap and get a blank bubble, then churn-question the club. 系统更新藏起菜单；会员点出空白气泡，开始质疑场馆。
Support can't reproduce on their own phones. 客服在自己手机上复现不了。

**Fix / 规则**: Test menus after each major platform release; keep a text command set. 每次大版本平台发布后测菜单；保留文字指令集。
Keyword auto-reply as backstop. 关键词自动回复作后盾。

**Related / 关联**: SKILL.md Cluster M; `references/17-omnichannel-messaging.md`.

### MSG-06 Sending the same message from 3 systems double-delivers {#md-060-multi-system-double-send}

**Detail / 细节**: If CRM, SCRM, and the app push all send "renewal reminder", a member gets it 3× from different numbers. 若 CRM、SCRM、App 推送都发"续费提醒"，会员会从三个号收到3遍。
Centralize the send-orchestration with a dedup window. 用统一发送编排+去重窗口集中发放。

**Why it bites / 痛点**: A member gets 3 renewal nudges in one hour and feels harassed. 会员一小时内收到3次续费催促，感觉被骚扰。
Unsubscribe + bad review. 退订+差评。

**Fix / 规则**: One campaign bus; per-member cooldown across channels. 单一活动总线；跨渠道按会员冷却。
Log all sends per member_id. 按 member_id 记所有发送。

**Related / 关联**: SKILL.md HI-7; Cluster M.

### MSG-07 Short links expire and rot the audit trail {#md-061-shortlink-expiry}

**Detail / 细节**: Using a short-link service with a 90-day TTL means old campaign links in member histories rot and break attribution. 用90天有效期的短链服务，会导致会员历史里的旧活动链接失效、归因断裂。
Prefer permanent redirects or your own domain. 优先用永久重定向或自有域名。

**Why it bites / 痛点**: A member clicks a 4-month-old link in their chat; it 404s; you lose the upsell. 会员点4个月前的聊天链接；404；你丢了追加销售。
Attribution reports lie. 归因报告失真。

**Fix / 规则**: Own the redirect domain; set TTL = never or very long. 自有重定向域名；TTL 设永久或极长。
Monitor link health weekly. 每周监测链接健康。

**Related / 关联**: SKILL.md Cluster W; `data/01-kpi-benchmark-library.md`.

### MSG-08 "Hi {first_name}" shows the literal brace {#md-062-merge-tag-brace}

**Detail / 细节**: A missing merge-field fallback renders "Hi {first_name}" literally when the field is empty. 合并字段缺兜底时，字段为空会原样显示"Hi {first_name}"。
Always set a fallback like "Hi there". 始终设"Hi there"类兜底。

**Why it bites / 痛点**: 5% of members have no first name; they get a broken-looking message and think the system is buggy. 5%会员无名字；收到破损信息，以为系统有 bug。
Brand looks amateur. 品牌显得业余。

**Fix / 规则**: Default merge fallback per field; QA on empty-data seeds. 每字段设兜底；用空数据种子做 QA。
Pre-send render test on 5 empty profiles. 发前用5个空档案渲染测试。

**Related / 关联**: SKILL.md Cluster W; `references/17-omnichannel-messaging.md`.

### MSG-09 WhatsApp quality rating tanks from quick replies {#md-063-whatsapp-quality-quickreply}

**Detail / 细节**: Using quick-reply buttons excessively or sending templated promos in a service conversation drops Meta's quality rating. 过度用快捷按钮或在服务会话里发模板促销，会拉低 Meta 质量评分。
Quality rating gates your future reach. 质量评分卡着你未来的触达量。

**Why it bites / 痛点**: Rating falls to "low"; Meta throttles all your templates for 7 days mid-promo. 评分跌到"低"；Meta 在促销中途限流你所有模板7天。
Launch implodes. 活动崩盘。

**Fix / 规则**: Respect conversation types; don't promo inside service chats. 区分会话类型；服务会话内不发促销。
Watch the quality dashboard daily in campaign weeks. 活动周每日盯质量看板。

**Related / 关联**: SKILL.md HI-7; `data/21` #ap-050-whatsapp-quality.

### MSG-10 Zalo/Kakao need local sender registration {#md-064-zalo-kakao-sender}

**Detail / 细节**: Zalo (VN) and KakaoTalk (KR) require local business sender registration; sending before approval gets blocked at the gateway. Zalo（越南）与 KakaoTalk（韩国）需本地企业发送方注册；未批先发会在网关被拦。
Start sender verification early — it takes weeks. 发送方认证要趁早——耗时数周。

**Why it bites / 痛点**: You plan a VN launch; Zalo sender still "pending" on day 1; zero messages go out. 你规划越南上线；Zalo 发送方第一天仍"待审"；一条都没发出去。
Grand opening has no comms. 开业大促毫无触达。

**Fix / 规则**: Register sender 4+ weeks ahead; have SMS fallback. 提前4周以上注册发送方；备 SMS 兜底。
Track approval status in the project plan. 在项目计划里跟踪审批状态。

**Related / 关联**: SKILL.md Cluster F; `references/17-omnichannel-messaging.md`.

### MSG-11 Push notification token dies on app update {#md-065-push-token-app-update}

**Detail / 细节**: After an app update, device push tokens can invalidate; members stop receiving class reminders until they reopen the app. App 更新后设备推送令牌可能失效；会员重开 App 前收不到上课提醒。
Re-register the token on every app foreground. 每次 App 回到前台都重注册令牌。

**Why it bites / 痛点**: Post-update week: 40% of members miss class reminders and no-show, hurting utilization. 更新后一周：40%会员漏接提醒而爽约，拉低坪效。
Attendance dips with no obvious cause. 出勤莫名下滑。

**Fix / 规则**: Refresh token on launch; fall back to SMS/WhatsApp if push fails twice. 启动即刷令牌；推送连败两次改 SMS/WhatsApp。
Track push-delivery rate as a KPI. 把推送到达率设为 KPI。

**Related / 关联**: SKILL.md Cluster U; `data/01-kpi-benchmark-library.md`.

### MSG-12 "Reply STOP" must actually stop all threads {#md-066-stop-all-threads}

**Detail / 细节**: A member who replies STOP must be suppressed across EVERY channel and system, not just the one they replied on. 会员回复 STOP 后必须在所有渠道与系统全 suppression，而非仅限其回复的那一个。
Central opt-out list consumed by all senders. 所有发送方共用一个中央退订名单。

**Why it bites / 痛点**: They STOP on SMS but keep getting app pushes; they screenshot and file a spam complaint. 他在短信退订，却仍收 App 推送；截图举报垃圾信息。
Regulator fine + sender block. 监管罚款+发送封禁。

**Fix / 规则**: One global suppression list; every sender checks it pre-send. 单一全局退订名单；每个发送方发前查。
Confirm opt-out within minutes. 退订数分钟内生效。

**Related / 关联**: SKILL.md HI-7; Cluster M.

---

## 6. Classes, Booking & Scheduling / 课程、预约与排期

### CLS-01 DST changes double-book classes in AU/NZ {#md-067-dst-double-book}

**Detail / 细节**: Australia/NZ daylight-saving transitions shift local times; a naive scheduler can create two "7am" slots or skip one. 澳/新夏令时切换会平移本地时间；幼稚排期器可能造出两个"早7"或漏掉一个。
Use timezone-aware scheduling with explicit DST handling. 用带显式 DST 处理的时区感知排期。

**Why it bites / 痛点**: On DST day, the 7am yoga appears twice; 20 members double-booked, 10 turned away. 夏令日早7瑜伽出现两次；20人重复预约，10人被拒。
Angry members, refund requests. 会员暴怒，要求退款。

**Fix / 规则**: Store class times in UTC + market tz; test the DST boundary yearly. 课程时间存 UTC+市场时区；每年测 DST 边界。
Freeze edits on DST transition days. DST 切换日冻结改期。

**Related / 关联**: SKILL.md Cluster F; `data/07-apac-regional-differences.md`.

### CLS-02 Waitlist auto-promote needs a notification {#md-068-waitlist-auto-promote}

**Detail / 细节**: When a waitlisted member is auto-promoted to a spot, they MUST get a push/SMS, or they won't show and the spot wastes. 候补会员被自动递补时，必须收到推送/SMS，否则他们不会来，位置白费。
Silent promotion = silent no-show. 静默递补=静默爽约。

**Why it bites / 痛点**: The system promotes Member B at 8pm for a 9pm class; B never sees it and doesn't come. 系统晚8点把B递补进晚9的课；B 没看见也没来。
You turned away a walk-in who'd have filled it. 你却拒了一位本可填满的临到客。

**Fix / 规则**: Auto-promote + immediate notification + 30-min confirm window. 自动递补+即时通知+30分钟确认窗。
If no confirm, cascade to next. 不确认则顺延下一位。

**Related / 关联**: SKILL.md Cluster U; `data/01-kpi-benchmark-library.md`.

### CLS-03 Instructor substitution must propagate to app {#md-069-instructor-substitution}

**Detail / 细节**: When a coach is swapped, the change must push to the app/class listing, or members show up for the wrong trainer and review-bomb. 教练被换时，变更必须推送到 App/课表，否则会员为错的人而来并狂打差评。
Update the displayed instructor atomically with the roster change. 课表展示教练与排班变更须原子化同步。

**Why it bites / 痛点**: A star trainer is replaced by a sub; the app still shows the star; 15 members complain and rate 1★. 明星教练被替补，App 仍显示明星；15人投诉并打1星。
Reputation hit you didn't cause but own. 口碑重创，虽非你本意却由你承担。

**Fix / 规则**: On substitution, push notification + app refresh + desk cue. 换人即推送+App刷新+前台提示。
QA the listing after every roster edit. 每次排班改动后 QA 课表。

**Related / 关联**: SKILL.md Cluster P; Cluster U.

### CLS-04 "Unlimited" class pass hits a hidden weekly cap {#md-070-unlimited-hidden-cap}

**Detail / 细节**: Some "unlimited" class passes actually carry a fine-print weekly cap; the app must enforce and SHOW it, or members feel cheated. 某些"无限"课包其实有细则周上限；App 须执行并明示，否则会员觉得被骗。
Display the real remaining quota transparently. 透明展示真实剩余额度。

**Why it bites / 痛点**: Member tries to book a 6th class, blocked by a hidden cap, and posts "SCAM" online. 会员约第6节课被隐藏上限拦下，上网发"诈骗"。
Trust crisis from fine print. 细则引发的信任危机。

**Fix / 规则**: Surface the cap in the product description and the booking UI. 在产品说明与预约界面都亮出上限。
Never market "unlimited" if a cap exists. 有上限就别打"无限"招牌。

**Related / 关联**: SKILL.md HI-3; Cluster W.

### CLS-05 Booking closes but door-list still admits {#md-071-booking-close-doorlist}

**Detail / 细节**: If online booking closes at T-30min but the door-list still admits walk-ins, capacity control breaks and classes overfill. 若线上预约 T-30 关闭，但门禁名单仍放临到，容量管控失效、课程超载。
The gate admit-list must respect the booking cutoff. 闸机准入名单须遵守预约截止。

**Why it bites / 痛点**: A 20-cap class ends with 28 bodies because door-list ignored the cap. 20人课最终挤进28人，因为门禁无视上限。
Safety + experience failure. 安全+体验双重失败。

**Fix / 规则**: Sync booking cap to the gate admit-list in real time. 预约上限与闸机准入名单实时同步。
Hard-stop at capacity with a waitlist. 满员硬停并转候补。

**Related / 关联**: SKILL.md HI-2; Cluster A.

### CLS-06 Recurring class skips public holidays silently {#md-072-recurring-skip-holiday}

**Detail / 细节**: A recurring weekly class that collides with a public holiday may be auto-skipped by the scheduler without notice. 与公共假日撞期的周常课，可能被排期器无声跳过。
Holiday calendars differ sharply across APAC markets. 亚太各市场假日日历差异极大。

**Why it bites / 痛点**: Members show up on a public-holiday Monday; no class, door locked, 1★ reviews. 会员在公共假日周一赶来；没课、门锁，打1星。
You didn't know the scheduler dropped it. 你根本不知道排期器把它删了。

**Fix / 规则**: Load market holiday calendars; notify on any auto-skip. 载入市场假日历；任何自动跳过都通知。
Manual confirm for holiday-week schedules. 假日周排期人工确认。

**Related / 关联**: SKILL.md Cluster F; `data/13-inspection-and-maintenance-calendar.md`.

### CLS-07 Coach no-show with no auto-notice to members {#md-073-coach-noshow-notice}

**Detail / 细节**: If a coach calls in sick, members booked must be notified before they travel, not on arrival. 教练请病假时，须在被约会员出发前通知，而非等他们到了再说。
Wire absence to an auto-cancel + refund/credit flow. 把缺席接自动取消+退款/补偿流程。

**Why it bites / 痛点**: 12 members travel across town for a class that was cancelled an hour ago. 12名会员跨城赶来，课一小时前已取消。
Fury + wasted time + churn. 暴怒+白跑+流失。

**Fix / 规则**: Coach check-in deadline 2h before; auto-notify on miss. 教练课前2小时签到截止；漏签自动通知。
Credit + apology template ready. 备好补偿+致歉模板。

**Related / 关联**: SKILL.md Cluster P; Cluster M.

### CLS-08 Two members same name, wrong check-in credited {#md-074-same-name-checkin}

**Detail / 细节**: Two "John Smith" in the club: the desk checks in the wrong one, corrupting attendance and coach pay. 馆里两个"John Smith"：前台给错人签到，污染出勤与教练工资。
Disambiguate by member_id, never by name alone. 用会员号区分，绝不只靠名字。

**Why it bites / 痛点**: Coach gets paid for a class the other John attended; reconciliation fight. 教练因另一位 John 的出勤被发薪；对账扯皮。
Payroll dispute. 工资争议。

**Fix / 规则**: Desk UI shows member_id + photo; confirm before tap. 前台界面显示会员号+照片；点前确认。
See MEM-02 name handling. 见 MEM-02 姓名处理。

**Related / 关联**: SKILL.md Cluster P; MEM-02.

### CLS-09 Class recording posted without consent of minors {#md-075-class-recording-minors}

**Detail / 细节**: Posting class livestreams/recordings that include minors without parental consent breaches HI-1/HI-5. 发布含未成年人的课程直播/录像，未经家长同意即违反 HI-1/HI-5。
Blur or exclude minors; get written consent. 对未成年人打码或排除；取书面同意。

**Why it bites / 痛点**: A parent sees their child in a public class video; regulatory complaint. 家长看到孩子出现在公开课程视频；监管投诉。
Potential platform takedown + fine. 可能被下架+罚款。

**Fix / 规则**: Minor-exclusion policy in filming SOP; consent captured per guardian. 拍摄 SOP 含未成年人排除政策；每位监护人单独同意。
See `data/02` minors rules. 见 `data/02` 未成年人规则。

**Related / 关联**: SKILL.md HI-1, HI-5; Cluster F.

### CLS-10 Peak-class reminder sent during the class {#md-076-reminder-during-class}

**Detail / 细节**: A mistimed cron sends the "your class starts in 1h" reminder while the class is already happening. 错时 cron 在课正在进行时发出"距开课还有1小时"提醒。
Offset the reminder from the actual start correctly. 提醒偏移须相对真实开课时间正确计算。

**Why it bites / 痛点**: Members in the middle of a session get a "starts in 1h" ping — confusing and unprofessional. 正在上课的会员收到"1小时后开课"提示——混乱且不专业。
Erodes trust in notifications. 削弱对通知的信任。

**Fix / 规则**: Compute reminder from the class's real start; test across timezones. 提醒相对课程真实开课算；跨时区测试。
Never schedule reminders off "now + fixed". 绝不用"现在+固定值"排提醒。

**Related / 关联**: SKILL.md Cluster M; CLS-01.

---

## 7. AI & Data Engine / AI 与数据引擎

### AI-01 Churn model retrained on a promo month = garbage {#md-077-churn-promo-retrain}

**Detail / 细节**: Retraining the churn model on a month with a huge acquisition promo bakes in abnormal behavior as "normal". 在含大额获客促销的月份重训流失模型，会把异常行为当"正常"学进去。
Exclude promo/anomaly windows from training data. 训练数据须排除促销/异常窗口。

**Why it bites / 痛点**: Post-promo, the model flags 40% of new members as "high churn" and you discount them all — margin evaporates. 促销后模型把40%新会员标"高流失"，你全给打折——利润蒸发。
You optimized against your own distortion. 你对着自己造的失真做了优化。

**Fix / 规则**: Tag promo cohorts; train on steady-state windows only. 给促销群体打标；只在稳态窗口训练。
Backtest on a clean holdout. 在干净留存集上回测。

**Related / 关联**: SKILL.md Cluster E; `data/09-algorithm-kernel-library.md`.

### AI-02 Bot must hand off after 2 failed answers {#md-078-bot-handoff-2fails}

**Detail / 细节**: A member-facing chatbot should escalate to a human after 2 failed/low-confidence answers, not loop forever. 面向会员的聊天机器人应在2次失败/低置信回答后转人工，而非死循环。
Set a confidence threshold + attempt cap. 设置信阈值+尝试上限。

**Why it bites / 痛点**: A member asks about a refund 5 times; the bot repeats "please elaborate" and they rage-quit. 会员问退款问了5次；机器人反复"请详述"，他气到退出。
Complaint + lost renewal. 投诉+续费流失。

**Fix / 规则**: On 2 fails or <0.6 confidence, route to human with context. 2次失败或置信<0.6，带上下文转人工。
Log handoffs for QA. 记转人工日志供 QA。

**Related / 关联**: SKILL.md Cluster E; HI-6.

### AI-03 Never let AI answer medical/injury questions (HI-6) {#md-079-ai-no-medical}

**Detail / 细节**: The AI must never diagnose injuries or give medical advice; it must refer to a qualified professional (HI-6). AI 绝不可诊断伤情或给医疗建议；须转介专业人士（HI-6）。
Hard-guardrail the health/medical intent class. 对"健康/医疗"意图类加硬护栏。

**Why it bites / 痛点**: A member asks "my knee hurts, should I squat?" the bot says "light reps are fine"; they injure further and blame the club. 会员问"膝盖疼能深蹲吗"，机器人说"轻量可"，结果伤加重，怪场馆。
Liability + HI-6 violation. 责任+违反 HI-6。

**Fix / 规则**: Detect medical intent → respond with "consult a pro" + disclaimer, never advice. 识别医疗意图→回"请咨询专业人士"+免责，绝不给建议。
Log all medical-intent hits. 记录所有医疗意图命中。

**Related / 关联**: SKILL.md HI-6; Cluster S; `data/21` #ap-051-ai-medical.

### AI-04 Churn score shown to coach creates bias {#md-080-churn-score-coach-bias}

**Detail / 细节**: If coaches see each member's "churn risk" score, they treat high-risk members differently, creating self-fulfilling loops. 若教练能看到每位会员的"流失风险分"，会区别对待高风险者，形成自证预言。
Show actionable nudge, not the raw score, to front-line. 给一线看"可执行提示"而非原始分。

**Why it bites / 痛点**: Coach ignores "low-risk" members who then quietly lapse; or pushes "high-risk" too hard and they churn faster. 教练忽视"低风险"致其悄悄流失；或猛推"高风险"反而加速流失。
Model validity degrades. 模型效度退化。

**Fix / 规则**: Surface "suggested action" only; keep scores with the analyst. 只呈现"建议动作"；分数留在分析层。
Audit for disparate treatment. 审计差别对待。

**Related / 关联**: SKILL.md Cluster E; `data/09-algorithm-kernel-library.md`.

### AI-05 Training data leaks PII into the prompt store {#md-081-ai-pii-prompt-store}

**Detail / 细节**: Feeding member names/health notes into a third-party LLM prompt store can leak PII to the vendor (HI-8). 把会员姓名/健康备注喂进第三方 LLM 提示库，可能把 PII 泄露给供应商（HI-8）。
Redact/pseudonymize before any external call. 任何外部调用前先脱敏/假名化。

**Why it bites / 痛点**: A support bot logs "Member Zhang, knee surgery, wants refund" to the LLM vendor's store. 客服机器人把"会员张，膝盖手术，要退款"记进 LLM 供应商库。
Cross-border PII breach finding. 跨境 PII 泄露认定。

**Fix / 规则**: Pseudonymize IDs; strip free-text health before send; self-host where possible. 假名化 ID；发送前剥离健康自由文本；可行则自托管。
Contractual DPA + data-residency check. 签 DPA+数据驻留核查。

**Related / 关联**: SKILL.md HI-8; Cluster K; `references/13-data-and-llm-engine.md`.

### AI-06 "AI trainer" recommends load beyond safe form {#md-082-ai-trainer-load}

**Detail / 细节**: A CV/posture AI that only cues form but also "recommends" weight increases can push unsafe loads (HI-2/HI-6). 只做姿态提示、却又"建议"加重的 CV/体态 AI，可能推不安全负荷（HI-2/HI-6）。
Keep AI to form feedback; never auto-prescribe load progressions. 让 AI 只做姿态反馈；绝不自动开负荷进阶。

**Why it bites / 痛点**: The AI says "add 5kg" to a member with poor form; they injure a shoulder. AI 对姿态差的会员说"加5公斤"；肩伤。
Injury + liability. 受伤+责任。

**Fix / 规则**: Constrain AI output to form cues; flag "consult coach" for progression. 限制 AI 输出为姿态提示；进阶标"请咨询教练"。
Human-in-loop for any load change. 任何负荷变更走人在回路。

**Related / 关联**: SKILL.md HI-2, HI-6; Cluster K.

### AI-07 Model drift silently degrades recommendations {#md-083-model-drift-silent}

**Detail / 细节**: Without monitoring, a recommendation model's accuracy decays as member behavior shifts; nobody notices for months. 缺监控时，推荐模型精度随会员行为漂移而衰减，数月无人察觉。
Track live performance vs a baseline continuously. 持续跟踪线上表现相对基线。

**Why it bites / 痛点**: The "class recommender" quietly pushes irrelevant classes; open-rate halves; you blame content. 课程推荐悄悄推无关课；打开率减半，你怪内容。
Wrong root cause, wasted effort. 根因错了，白费劲。

**Fix / 规则**: Weekly drift report; auto-retrain trigger on threshold breach. 每周漂移报告；超阈自动重训。
Keep a champion/challenger setup. 保留冠军/挑战者并行。

**Related / 关联**: SKILL.md Cluster E; `data/09-algorithm-kernel-library.md`.

### AI-08 Chatbot trained on outdated pricing answers wrong {#md-084-bot-outdated-pricing}

**Detail / 细节**: The bot's knowledge of prices/packages goes stale; it quotes last year's promo as current. 机器人对价格/套餐的知识过时；把去年促销当现行报。
Ground the bot in a live product API, not static text. 让机器人接实时产品 API，而非静态文本。

**Why it bites / 痛点**: Bot quotes ¥199 but the real price is ¥299; member demands the lower at the desk. 机器人报199，实际299；会员在前台要求按低价。
Margin leak + trust hit. 利润漏+信任损。

**Fix / 规则**: Pull prices from the live catalog; expire cached answers hourly. 价格取自实时目录；缓存答案每小时过期。
Human-confirm on any price quote. 任何报价人工可核。

**Related / 关联**: SKILL.md Cluster E; `data/12-software-fault-tree-library.md`.

### AI-09 Voice-bot without DNC check calls a do-not-contact member {#md-085-voicebot-no-dnc}

**Detail / 细节**: An AI outbound voice bot must check the Do-Not-Contact list and consent before dialing, or it breaks HI-7. AI 外呼语音机器人拨号前必须查"免联系名单"与同意，否则违反 HI-7。
Gate every dial on the suppression list. 每次拨号都过退订名单闸门。

**Why it bites / 痛点**: The bot calls a member who opted out; they record it and file a spam complaint with the regulator. 机器人打给已退订会员；对方录音并向监管举报。
Fine + campaign kill. 罚款+活动腰斩。

**Fix / 规则**: Pre-dial DNC + consent check; log each call. 拨前查 DNC+同意；记每通电话。
See `data/21` #ap-011-ai-outbound-no-consent (💀). 见 `data/21` #ap-011（💀）。

**Related / 关联**: SKILL.md HI-7; `data/21-anti-pattern-library.md` #ap-011-ai-outbound-no-consent.

### AI-10 Sentiment model mislabels translated reviews {#md-086-sentiment-translation}

**Detail / 细节**: Running sentiment on machine-translated reviews from KR/JP/VN can flip polarity (e.g., sarcasm lost), corrupting the CX score. 对韩/日/越等机器翻译后的评论跑情感分析，会因反讽等丢失而翻转极性，污染 CX 分。
Use native-language models or human-coded samples for calibration. 用母语模型或以人工标注样本校准。

**Why it bites / 痛点**: Japanese sarcastic praise is scored negative; you "fix" a problem members actually liked. 日式反讽好评被判为负；你去"修"会员其实满意的点。
Wrong priorities. 优先级错乱。

**Fix / 规则**: Per-language sentiment models; sample human audit monthly. 按语言建情感模型；每月人工抽检。
Don't translate-then-score for CX KPIs. CX KPI 不翻译后评分。

**Related / 关联**: SKILL.md Cluster U; `data/01-kpi-benchmark-library.md`.

### AI-11 Face-match threshold too low = false entry {#md-087-face-threshold-low}

**Detail / 细节**: Setting the face-gate match threshold too low lets similar-looking members through on each other's accounts. 人脸闸机匹配阈值过低，会让长相相近的会员互相冒用通行。
Tune threshold with a false-accept vs false-reject tradeoff per market. 按市场在误识率与误拒率间调阈值。

**Why it bites / 痛点**: Two look-alike members; one's account is used by the other for weeks; billing and access both wrong. 两个撞脸会员；一人账号被另一人用了几周；账单与门禁都错。
Fraud + privacy mix-up. 欺诈+隐私混淆。

**Fix / 规则**: Set conservative threshold; require a second factor for disputes. 阈值从严；争议时启二次因子。
Never face-only (HI-1). 绝人脸唯一（HI-1）。

**Related / 关联**: SKILL.md HI-1; Cluster F.

### AI-12 "Smart" pricing bot undercuts on a holiday {#md-088-smart-pricing-holiday}

**Detail / 细节**: An autonomous promo/pricing bot can fire a deep discount into a high-demand holiday window, torching margin. 自动促销/定价机器人可能在高需求假日窗口打出深折，烧光利润。
Cap bot authority; require human approval above a discount floor. 限制机器人权限；超折扣下限须人工批。
Keep a kill switch (see `data/21` #ap-053-no-kill-switch). 保留熔断开关（见 `data/21` #ap-053）。

**Why it bites / 痛点**: Bot drops New Year premium slots to 50% "to fill capacity" that was already 95% full. 机器人为"填满"本已95%满的元旦 premium 时段打到5折。
¥200k margin lost in a weekend. 一个周末亏掉20万毛利。

**Fix / 规则**: Discount floor + holiday blackout list + kill switch. 折扣下限+假日禁促清单+熔断开关。
Daily margin alert during bot-active periods. 机器人活跃期每日毛利告警。

**Related / 关联**: SKILL.md Cluster W; `data/21-anti-pattern-library.md` #ap-053-ai-no-kill-switch.

---

## 8. Compliance & Privacy / 合规与隐私

### CMP-01 Consent screenshots need timestamps {#md-089-consent-screenshot-timestamp}

**Detail / 细节**: A bare consent screenshot is weak evidence; it must show the member, the consent version, and a server timestamp. 一张无上下文的同意截图证据力弱；须含会员、同意版本号与服务器时间戳。
Store consent as structured records, not images. 把同意存为结构化记录，而非图片。

**Why it bites / 痛点**: A dispute arises; your screenshot has no date; the regulator calls it unverifiable. 起争议；你的截图无日期；监管认定不可核实。
Consent deemed not obtained. 视为未获同意。

**Fix / 规则**: Log consent with version + timestamp + member_id in the DB. 在库里按版本+时间戳+member_id 记同意。
Exportable for audit. 可导出供审。

**Related / 关联**: SKILL.md HI-7, HI-8; `data/02-regulation-traceability-index.md`.

### CMP-02 CCTV retention auto-delete must be verified monthly {#md-090-cctv-retention-verify}

**Detail / 细节**: Both over-retention AND under-retention of CCTV are violations; the auto-delete schedule must be verified monthly. 监控录像保留过长与过短都违规；自动删除计划须每月核验。
Set per-market legal retention; alert on deviation. 按市场法定保留期设置；偏差即告警。

**Why it bites / 痛点**: The NVR was set to "keep 90 days" but the law says 30; a breach exposes 3× footage. 录像机设"存90天"，法定30天；出事曝光3倍时长录像。
Regulatory penalty for over-retention. 因超期留存被罚。

**Fix / 规则**: Per-market retention config; monthly delete-log review. 按市场配置保留期；每月查删除日志。
See `data/02` CCTV rules. 见 `data/02` 监控规则。

**Related / 关联**: SKILL.md HI-5; Cluster F; `data/02-regulation-traceability-index.md`.

### CMP-03 Staff group chats leak member PII {#md-091-staff-chat-pii-leak}

**Detail / 细节**: Staff WeChat/LINE groups routinely paste member phone numbers, health notes, and photos — a PII leak surface. 员工微信/LINE 群常粘贴会员电话、健康备注、照片——这是 PII 泄露面。
Set rules + use the CRM internal note field instead. 立规矩+改用 CRM 内部备注字段。

**Why it bites / 痛点**: A group screenshot with 20 member phones leaks; one member complains; investigation spreads. 含20个会员电话的群截图外泄；一人投诉，调查扩大。
PDPA/PIPL exposure. 触类 PIPL/PDPA。

**Fix / 规则**: Ban PII in external chats; use masked CRM notes; train on HI-8. 禁外部聊天含 PII；用脱敏 CRM 备注；按 HI-8 培训。
Periodic chat audit. 定期聊天审计。

**Related / 关联**: SKILL.md HI-8; Cluster F.

### CMP-04 Biometric consent separate from T&Cs {#md-092-biometric-consent-separate}

**Detail / 细节**: Face/vein/fingerprint consent must be a SEPARATE, explicit opt-in, not buried in general terms (HI-1). 人脸/静脉/指纹同意必须是独立的、明确的 opt-in，不能埋进总条款（HI-1）。
Offer a non-biometric alternative always. 永远提供非生物识别替代。

**Why it bites / 痛点**: You bundle face-enrollment in the signup T&Cs; a member objects; regulator says invalid consent. 你把人脸录入绑进注册条款；会员反对；监管认定同意无效。
Forced re-consent + possible fine. 被迫重新征同意+可能罚款。

**Fix / 规则**: Standalone biometric consent + card fallback; see `data/21` #ap-005-face-no-alt (💀). 独立生物识别同意+刷卡兜底；见 `data/21` #ap-005（💀）。
See `data/02` biometric rules. 见 `data/02` 生物识别规则。

**Related / 关联**: SKILL.md HI-1; `data/21-anti-pattern-library.md` #ap-005-face-entry-no-alt.

### CMP-05 Cameras in changing rooms "for safety" = criminal {#md-093-camera-changing-room}

**Detail / 细节**: Any imaging device in changing rooms/showers is an absolute no-go (HI-5) and can be criminal exposure. 更衣室/淋浴区任何影像设备都是绝对禁区（HI-5），可能构成刑事暴露。
Remove; if "safety" needed, use motion sensors without optics. 移除；若需"安全"，用无光学的人体存在传感器。

**Why it bites / 痛点**: A hidden cam in a locker room is discovered; criminal investigation + club shuttered. 更衣室暗藏摄像头被发现；刑事调查+场馆关停。
Existential. 灭顶之灾。

**Fix / 规则**: Hard ban; physical audit of every lens location; sign-off. 硬性禁止；对每个镜头位置做物理审计+签字。
See `data/21` #ap-006-camera-changing-room (💀). 见 `data/21` #ap-006（💀）。

**Related / 关联**: SKILL.md HI-5; `data/21-anti-pattern-library.md` #ap-006-camera-changing-room.

### CMP-06 Cross-border data with no residency plan {#md-094-crossborder-no-residency}

**Detail / 细节**: Storing APAC member data on a foreign cloud without a residency plan breaches localization rules in several markets. 把亚太会员数据存境外云而无驻留方案，违反多个市场的本地化规则。
Map data flows per market; localize where required. 按市场绘数据流；需驻留处本地化。

**Why it bites / 痛点**: A VN/SG member's data sits on a US region; regulator demands localization; you scramble to migrate. 越南/新加坡会员数据在美国节点；监管要求本地化，你手忙脚乱迁移。
Order to suspend processing. 被令暂停处理。

**Fix / 规则**: Per-market data-residency config; DPA + transfer mechanism. 按市场设数据驻留；DPA+传输机制。
See `data/02` residency rules. 见 `data/02` 驻留规则。

**Related / 关联**: SKILL.md HI-9 (data sovereignty); Cluster F; `references/13-data-and-llm-engine.md`.

### CMP-07 "Legitimate interest" misused for marketing {#md-095-legitimate-interest-marketing}

**Detail / 细节**: Using "legitimate interest" as the lawful basis for marketing emails is invalid in most APAC regimes — you need consent (HI-7). 用"合法利益"作营销邮件的法律依据，在多数亚太法域无效——需要同意（HI-7）。
Market only on opt-in. 仅基于 opt-in 营销。

**Why it bites / 痛点**: You email a bought list citing "legitimate interest"; regulator disagrees; fine. 你以"合法利益"给买来的名单发邮；监管不认；罚款。
Sender reputation dead. 发送信誉归零。

**Fix / 规则**: Consent-based marketing only; document the basis per send. 仅同意制营销；每次发送记录依据。
See `data/02` lawful-basis map. 见 `data/02` 法律依据映射。

**Related / 关联**: SKILL.md HI-7; Cluster F.

### CMP-08 Minor's data kept like an adult's {#md-096-minor-data-adult}

**Detail / 细节**: Minors' data needs parental consent and often tighter retention; treating it like adult data breaches HI-1. 未成年人数据需家长同意且常需更严留存；当成人数据处理即违反 HI-1。
Tag minor accounts; gate processing on guardian consent. 标记未成年账户；处理以监护人同意为闸。

**Why it bites / 痛点**: A 15-year-old's profile is marketed to; parent complains; enhanced scrutiny triggered. 15岁档案被营销；家长投诉；触发强化审查。
Higher-penalty category. 进入高罚区间。

**Fix / 规则**: Minor flag + guardian consent + shorter retention. 未成年标志+监护人同意+更短留存。
See `data/02` minors rules. 见 `data/02` 未成年人规则。

**Related / 关联**: SKILL.md HI-1; Cluster F.

### CMP-09 Privacy policy never shown in the member's language {#md-097-privacy-policy-language}

**Detail / 细节**: In multilingual markets, showing the privacy policy only in English when members read Japanese/Thai/Korean is non-compliant. 多语市场里只给英文隐私政策、而会员读日/泰/韩文，即不合规。
Provide the policy in the member's market language. 隐私政策须提供会员所在市场语言版本。

**Why it bites / 痛点**: A TH member signs a policy they can't read; regulator flags invalid consent. 泰国会员签了看不懂的政策；监管认定同意无效。
Consent voided. 同意作废。

**Fix / 规则**: Localized policy per market; record which version was accepted. 按市场本地化政策；记录接受了哪个版本。
Version-link in the CRM. CRM 内链政策版本。

**Related / 关联**: SKILL.md Cluster F; `data/06-bilingual-glossary.md`.

### CMP-10 Deleted account still receives campaigns {#md-098-deleted-account-campaign}

**Detail / 细节**: "Delete my account" must purge the member from ALL send lists; a lingering record keeps emailing them. "删除账户"必须从所有发送名单清除；残留记录会持续发邮件。
Honor erasure across every system (HI-8). 跨所有系统履行删除权（HI-8）。

**Why it bites / 痛点**: A deleted member gets a promo; they reply "I left, stop" and escalate to a regulator. 已删会员收到促销；回"我已退，别发"并升级到监管。
Erasure-right violation. 违反删除权。

**Fix / 规则**: Erasure workflow hits CRM, SCRM, app, and archives; confirm zero-send. 删除流程覆盖 CRM/SCRM/App/归档；确认零发送。
Quarterly erasure audit. 每季度删除权审计。

**Related / 关联**: SKILL.md HI-8; Cluster F.

### CMP-11 Security camera points at the street/passers-by {#md-099-camera-public-street}

**Detail / 细节**: An externally-facing camera that captures passers-by on a public street may need signage and a narrower FOV per local law. 朝外的摄像头若拍到公共街道路人，按当地法可能需标识并收窄视角。
Aim cameras at your entrance only; post notice. 镜头只对准自家入口；张贴告示。

**Why it bites / 痛点**: A camera sweeps the sidewalk; a neighbor complains of mass surveillance; order to re-aim. 摄像头扫到人行道；邻居投诉大规模监控；被令调角度。
Community friction. 社区摩擦。

**Fix / 规则**: Narrow FOV; public CCTV signage; document the rationale. 收窄视角；公共监控标识；记录理由。
See `data/02` CCTV rules. 见 `data/02` 监控规则。

**Related / 关联**: SKILL.md HI-5; Cluster F.

### CMP-12 "Free WiFi" logs member MAC without notice {#md-100-wifi-mac-logging}

**Detail / 细节**: Captive-portal WiFi that logs member device MAC addresses without notice is covert tracking (HI-8). 捕获门户 WiFi 在会员无告知下记录设备 MAC 属隐性追踪（HI-8）。
Show a notice + consent; minimize what's logged. 显示告知+同意；最小化记录内容。

**Why it bites / 痛点**: The portal silently fingerprints every device; a privacy researcher flags it; bad press. 门户静默给每台设备建档；隐私研究者曝光；负面舆情。
Trust hit. 信任受损。

**Fix / 规则**: Consent screen on connect; log session only, not perpetual MAC. 连接时 consent 屏；只记会话不永久存 MAC。
Retain minimal, delete on disconnect. 最小化留存，断开即删。

**Related / 关联**: SKILL.md HI-8; Cluster F.

---

## 9. Vendors & Procurement / 供应商与采购

### VEN-01 The demo account is always faster than production {#md-101-demo-faster-than-prod}

**Detail / 细节**: Vendor demos run on a tiny clean dataset and a fat server; production on your real load is slower — never accept "demo = reality". 供应商 demo 跑在干净小数据+高配服务器上；生产在你真实负载下更慢——绝不可"demo=现实"。
Demand a pilot on your own data volume. 要求用你自己的数据量做试点。

**Why it bites / 痛点**: Post-launch the "instant" search takes 9 seconds with 8k members; members feel it's broken. 上线后"秒开"搜索在8千会员时变9秒；会员觉得坏了。
Adoption fails, blame the club. 采纳失败，怪场馆。

**Fix / 规则**: Pilot with production-scale data; measure latency SLA. 用生产级数据试点；测延迟 SLA。
See `data/21` #ap-034-demo-not-acceptance. 见 `data/21` #ap-034。

**Related / 关联**: SKILL.md Cluster B; `data/21-anti-pattern-library.md` #ap-034-demo-not-acceptance.

### VEN-02 "Unlimited" plans have fair-use clauses {#md-102-unlimited-fairuse}

**Detail / 细节**: "Unlimited" SMS/API/push plans almost always carry a fair-use clause that throttles you at peak. "无限"短信/API/推送套餐几乎都带公平使用条款，高峰即限流。
Read the fair-use small print before committing. 承诺前读公平使用细则。

**Why it bites / 痛点**: Your promo sends 200k messages; the "unlimited" plan throttles to 1k/hr; campaign dies. 促销发20万条；"无限"套餐限到1千/时；活动死。
Peak-season blackout. 旺季黑屏。

**Fix / 规则**: Negotiate a committed throughput; get it in writing. 谈承诺吞吐；写进合同。
See `data/21` #ap-052-promo-no-headroom. 见 `data/21` #ap-052。

**Related / 关联**: SKILL.md Cluster W; `data/21-anti-pattern-library.md` #ap-052-promo-no-headroom.

### VEN-03 Sandbox API keys in production = silent failures {#md-103-sandbox-keys-prod}

**Detail / 细节**: Deploying with sandbox/test API keys in production yields silent failures (no error, no action) because the endpoint is a stub. 生产环境用了沙箱/测试 API 密钥，会因端点是桩而静默失败（无报错无动作）。
Keyed environments must be separated and verified at deploy. 环境密钥须分离，发布时核验。

**Why it bites / 痛点**: Messages "send" but nobody receives for a week; you notice only when a member asks. 消息"已发"却无人收到，持续一周；会员来问才发现。
Comms blackout, unnoticed. 触达中断，无人察觉。

**Fix / 规则**: Separate keys per env; deploy check fails if prod uses sandbox key. 按环境分密钥；生产用沙箱密钥则发布检查失败。
Smoke-test prod sends post-deploy. 发布后冒烟测生产发送。

**Related / 关联**: SKILL.md Cluster N; `data/12-software-fault-tree-library.md`.

### VEN-04 Prepay 3+ years of SaaS for a discount, pre-pilot {#md-104-prepaid-3yr-pre-pilot}

**Detail / 细节**: Paying 3+ years upfront for a "discount" before a pilot proves fit is a lock-in and cash trap. 试点未证适配就为折扣预付3年以上 SaaS，是锁定+资金陷阱。
Pilot first; pay annual max until proven. 先试点；证实前最多年付。

**Why it bites / 痛点**: The tool doesn't fit after 4 months; you're stuck with 32 months prepaid, non-refundable. 工具4个月后证明不适配；还被32个月预付绑死，不退。
Sunk cost you can't escape. 沉没成本无法脱身。

**Fix / 规则**: Cap prepay at 12 months pre-proven; review clause. 证实前预付封顶12个月；留复核条款。
See `data/21` #ap-033-prepaid-3yr. 见 `data/21` #ap-033。

**Related / 关联**: SKILL.md Iron Law 8 (vendor neutrality); `data/21-anti-pattern-library.md` #ap-033-prepaid-3yr.

### VEN-05 Gray-import equipment for mission-critical lanes {#md-105-gray-import-critical}

**Detail / 细节**: Gray-import gate/network gear lacks local warranty and firmware; a failure mid-operation has no support. 水货闸机/网络设备无本地保修与固件；运营中故障无支持。
Buy locally-supported SKUs for critical paths. 关键链路买本地支持型号。

**Why it bites / 痛点**: The gray-import gate dies on a Saturday; no local RMA; club runs manual for a week. 水货闸机周六坏了；无本地返修；手动放行一周。
Revenue + experience loss. 营收+体验双损。

**Fix / 规则**: Local warranty + SLA for critical gear; validate serial region. 关键设备本地保修+SLA；核序列号区域。
See `data/21` #ap-037-gray-import-critical. 见 `data/21` #ap-037。

**Related / 关联**: SKILL.md Cluster C; `data/21-anti-pattern-library.md` #ap-037-gray-import-critical.

### VEN-06 "Free" integration hides per-transaction fees {#md-106-free-integration-fees}

**Detail / 细节**: A "free" integration often hides per-transaction or per-API-call fees that dominate cost at scale. "免费"集成常藏按交易/按调用的费用，规模化后成为主成本。
Model total cost at your volume, not the sticker. 按你的量建模总成本，而非看标价。

**Why it bites / 痛点**: "Free" connector costs ¥0.02/call; at 2M calls/yr that's ¥40k you didn't budget. "免费"连接器每调0.02元；年2千万调=4万元没进预算。
Budget blowout. 预算爆雷。

**Fix / 规则**: Get the full fee schedule; model at 3× current volume. 拿完整费率表；按当前3倍量建模。
See `data/15-procurement-and-cost-benchmark.md`. 见 `data/15` 采购成本基准。

**Related / 关联**: SKILL.md Cluster I; `data/15-procurement-and-cost-benchmark.md`.

### VEN-07 Reference customer is in a different format/market {#md-107-reference-different-format}

**Detail / 细节**: A vendor's reference client in a different format/market doesn't predict fit for yours. 供应商的标杆客户若业态/市场不同，不能预测对你的适配。
Demand a same-format, same-market reference. 要求同业态同市场的参考案例。

**Why it bites / 痛点**: Their star case is a Tokyo boutique; you're a SG mega club; the workflow collapses. 他们的明星案例是东京精品馆；你是新加坡大型馆；工作流崩了。
Misfit discovered post-contract. 合同后才发现不适配。

**Fix / 规则**: Insist on a comparable reference + a site visit or call. 坚持可比参考+实地/电话走访。
See `data/03-software-vendor-directory.md`. 见 `data/03` 软件供应商名录。

**Related / 关联**: SKILL.md Iron Law 1 (format-fit); `data/03-software-vendor-directory.md`.

### VEN-08 No data-export clause before signing {#md-108-no-export-clause}

**Detail / 细节**: Signing without a data-export clause (format, timeline, cost) traps you if you leave (vendor lock). 签约时无数据导出条款（格式/时限/费用），退坑即被绑（供应商锁定）。
Export terms must be in the contract, not the ToS. 导出条款须在合同里，而非服务条款。

**Why it bites / 痛点**: You switch vendors; the old one says export is "¥80k + 60 days"; you're stuck or pay up. 你换供应商；旧的说导出"8万+60天"；要么被困要么掏钱。
Lock-in realized. 锁定成真。

**Fix / 规则**: Contractual export: CSV/API, ≤30 days, fixed/zero fee. 合同导出：CSV/API、≤30天、固定/零费用。
Never sign without it (see `data/21` #ap-002). 无此不签约（见 `data/21` #ap-002）。

**Related / 关联**: SKILL.md Iron Law 8; `data/21-anti-pattern-library.md` #ap-002-no-data-export.

### VEN-09 Support SLA measured on vendor's clock, not yours {#md-109-sla-vendor-clock}

**Detail / 细节**: Vendor SLAs often start the timer at "ticket acknowledged", not "you reported" — gaps don't count. 供应商 SLA 常从"工单已确认"起算而非"你报修"，空档不计入。
Define SLA start = your report timestamp. 定义 SLA 起点=你报修时间戳。

**Why it bites / 痛点**: You report at 9pm; they acknowledge 9am; the 4h SLA "starts" at 9am and they "met" it at 1pm — you were down 16h. 你晚9点报修；他们早9点确认；4小时 SLA"从早9点算"，下午1点"达标"——你其实宕了16小时。
Real downtime invisible in the SLA. 真实停机在 SLA 里看不见。

**Fix / 规则**: SLA clock = your report time; penalize unacknowledged gaps. SLA 时钟=你报修时；未确认空档计入惩罚。
Track independently. 独立跟踪。

**Related / 关联**: SKILL.md Cluster I; `data/14-repair-scripts-and-sla-library.md`.

### VEN-10 "Lifetime license" dies at version 2 {#md-110-lifetime-license-v2}

**Detail / 细节**: A "lifetime license" may mean "lifetime of v1" — v2 becomes a paid upgrade. "终身授权"可能指"v1 的终身"——v2 变成付费升级。
Clarify: lifetime = all future versions, or named version only. 澄清：终身=含未来所有版本，还是仅指定版本。

**Why it bites / 痛点**: v2 launches with must-have security fixes; "lifetime" doesn't cover it; pay again or stay insecure. v2 带着必需安全补丁上线；"终身"不涵盖；要么再掏钱要么无防护。
Security debt. 安全债。

**Fix / 规则**: Define version coverage in writing; include security updates. 书面定义版本覆盖；含安全更新。
Budget for upgrade cycles. 为升级周期备预算。

**Related / 关联**: SKILL.md Cluster I; `data/15-procurement-and-cost-benchmark.md`.

---

## 10. Finance, Tax & Anti-Fraud / 财税与反欺诈

### FIN-01 Deferred revenue must reconcile with MMS monthly {#md-111-deferred-revenue-reconcile}

**Detail / 细节**: Prepaid memberships are deferred revenue; the spreadsheet must reconcile with the membership system monthly or audit pain follows. 预付会籍是递延收入；表格须与会员系统每月对账，否则审计痛苦。
Automate the deferred schedule from the system of record. 递延排程从源系统自动出。

**Why it bites / 痛点**: At year-end the deferred balance is ¥300k off vs the MMS; auditor flags material misstatement. 年末递延余额与会员系统差30万；审计标定重大错报。
Restated financials + penalty. 重述财报+罚款。

**Fix / 规则**: Monthly auto-reconcile; variance alert >0.5%. 每月自动对账；差异>0.5%即告警。
See `data/21` #ap-054-deferred-no-reconcile. 见 `data/21` #ap-054。

**Related / 关联**: SKILL.md Cluster R; `data/21-anti-pattern-library.md` #ap-054-deferred-no-reconcile.

### FIN-02 Refund policy must be in the system BEFORE first refund {#md-112-refund-policy-preloaded}

**Detail / 细节**: The refund rules must be configured in the system BEFORE the first refund request, or staff improvise inconsistently. 退款规则须在首个退款请求前就配进系统，否则员工各自发挥、前后不一。
Pre-load the policy; train on it. 预先载入政策；培训到位。

**Why it bites / 痛点**: First big refund: two staff give two answers; the member records both and complains of unfairness. 首笔大额退款：两员工给两种说法；会员录下并投诉不公。
Consistency complaint + precedent mess. 一致性投诉+先例混乱。

**Fix / 规则**: System-enforced refund logic; manager override logged. 系统强制退款逻辑；店长覆盖留痕。
See `data/21` #ap-055-refund-policy-late. 见 `data/21` #ap-055。

**Related / 关联**: SKILL.md HI-3; `data/21-anti-pattern-library.md` #ap-055-refund-policy-late.

### FIN-03 BNPL chargebacks surprise finance {#md-113-bnpl-chargeback-surprise}

**Detail / 细节**: Buy-now-pay-later plans shift default risk; chargebacks land months later and shock the P&L if unmodeled. 先买后付把违约风险后移；拒付数月后到来，未建模则冲击利润表。
Model BNPL default as a contra-revenue reserve. 把 BNPL 违约建模为收入备抵。

**Why it bites / 痛点**: Q4 looks great on BNPL sales; Q2 next year ¥150k chargebacks hit with no reserve. Q4 因 BNPL 销售好看；次年 Q2 15万拒付来袭，毫无准备。
Profit whiplash. 利润过山车。

**Fix / 规则**: Reserve for BNPL defaults; report deferred+risk together. 为 BNPL 违约计提；递延与风险合并报。
See `data/02` prepaid rules. 见 `data/02` 预付规则。

**Related / 关联**: SKILL.md HI-3; Cluster R.

### FIN-04 Cash drawer never reconciled = silent theft {#md-114-cash-drawer-no-reconcile}

**Detail / 细节**: If the cash drawer isn't reconciled every close, small skims go unnoticed for months. 现金抽屉若不清机对账，小额揩油数月无人察觉。
Mandatory per-shift cash count + variance log. 强制每班点钞+差异日志。

**Why it bites / 痛点**: A part-time cashier skims ¥20/day; a year later it's ¥7k gone, undetectable. 兼职收银每天揩20元；一年后7千没了，查不出。
Trust + loss. 信任+损失。

**Fix / 规则**: Count drawer at open & close; alert on >¥50 variance. 开班下班均点钞；差异>50元即告警。
Rotate cashier duties. 收银职责轮岗。

**Related / 关联**: SKILL.md Cluster R; Cluster I.

### FIN-05 "Comp" members distort unit economics {#md-115-comp-member-distortion}

**Detail / 细节**: Complimentary/staff/family members must be excluded from per-member revenue KPIs or they distort unit economics. 赠卡/员工/家属会员须从"每会员营收"KPI 排除，否则扭曲单位经济。
Tag comp members; filter from financial KPIs. 标记赠卡会员；从财务 KPI 过滤。

**Why it bites / 痛点**: 60 comp accounts drag ARPU down 12%; you "raise prices" to fix a phantom problem. 60个赠卡拉低 ARPU 12%；你为"虚问题"去涨价。
Wrong pricing move. 错误定价动作。

**Fix / 规则**: Comp flag + finance-only view; reconcile with MEM-03 test filter. 赠卡标志+财务专用视图；与 MEM-03 测试过滤联动。
See `data/01-kpi-benchmark-library.md`. 见 `data/01` KPI 库。

**Related / 关联**: SKILL.md Cluster U; `data/01-kpi-benchmark-library.md`.

### FIN-06 Tax invoice details mismatch the contract {#md-116-tax-invoice-mismatch}

**Detail / 细节**: The tax invoice line items must match the signed contract; mismatches block reimbursement and audit. 税务发票明细须与签约合同一致；不符会卡报销与审计。
Generate invoices from the contracted catalog. 发票从合同目录生成。

**Why it bites / 痛点**: Invoice says "consulting" but contract says "software"; corporate client rejects it; payment delayed 2 months. 发票写"咨询"而合同写"软件"；企业客户拒收；回款迟2月。
Cash-flow gap. 现金流缺口。

**Fix / 规则**: Invoice template bound to contract line items; pre-audit. 发票模板绑定合同条目；预先审计。
See `data/02` tax rules. 见 `data/02` 税务规则。

**Related / 关联**: SKILL.md Cluster R; `data/02-regulation-traceability-index.md`.

### FIN-07 Currency of reporting flips with FX silently {#md-117-reporting-currency-fx}

**Detail / 细节**: A multi-currency club must fix ONE reporting currency; letting it follow spot FX silently makes YoY comparisons meaningless. 多币种场馆须固定单一报告币种；任其随即期汇率浮动会让同比失去意义。
Lock reporting currency + translate at a fixed rate for comparison. 锁定报告币种+对比用固定汇率折算。

**Why it bites / 痛点**: Revenue "drops 8%" YoY but it's just FX; you make a wrong cut decision. 营收"同比降8%"其实只是汇率；你做了错误收缩决策。
Bad strategy from FX noise. 被汇率噪声带歪战略。

**Fix / 规则**: Fixed reporting FX for trends; show actuals separately. 趋势用固定汇率；实际值单独列。
See `data/07-apac-regional-differences.md`. 见 `data/07`。

**Related / 关联**: SKILL.md Cluster R; `data/07-apac-regional-differences.md`.

### FIN-08 Prepaid funds mixed with operating account {#md-118-prepaid-mixed-account}

**Detail / 细节**: Prepaid member funds must be segregated (supervision) from the operating account per HI-3; mixing is a compliance red line. 预付会员资金须按 HI-3 与运营账户隔离（监管）；混用是合规红线。
Use a dedicated supervised account; reconcile regularly. 用专用监管账户；定期对账。

**Why it bites / 痛点**: You spend prepaid funds on payroll; a dip in new sales leaves you unable to refund — scandal. 你把预付金挪用发工资；新售下滑后无力退款——丑闻。
Fund-supervision violation + insolvency risk. 违反资金监管+破产风险。

**Fix / 规则**: Segregated account + periodic reconciliation to deferred schedule. 隔离账户+定期与递延排程对账。
See `data/02` fund-supervision rules. 见 `data/02` 资金监管规则。

**Related / 关联**: SKILL.md HI-3; Cluster R; `data/02-regulation-traceability-index.md`.

---

## 11. 24h Unmanned & Physical Security / 24小时无人与物理安全

### UNM-01 e-KYC fails for foreign visitors — manual fallback {#md-119-ekyc-foreign-fallback}

**Detail / 细节**: Electronic KYC often fails for foreign passports/visas; an unmanned club must have a manual fallback path. 电子 KYC 常对外籍护照/签证失败；无人场馆须有手动兜底路径。
Pre-register foreigners with staff verification. 外籍人士经员工核验预登记。

**Why it bites / 痛点**: A tourist can't pass e-KYC at 11pm; the unmanned club denies entry with no human to help. 游客晚11点过不了 e-KYC；无人场馆拒入且无人可求助。
Bad review + lost sale + accessibility issue. 差评+丢单+无障碍问题。

**Fix / 规则**: Manual fallback (staff video-verify or pre-clear); log the exception. 手动兜底（员工视频核或预先放行）；记异常。
See `data/21` #ap-056-no-fallback-ekyc. 见 `data/21` #ap-056。

**Related / 关联**: SKILL.md Cluster T; HI-1; `data/21-anti-pattern-library.md` #ap-056-ekyc-no-fallback.

### UNM-02 Panic button test weekly with log {#md-120-panic-button-weekly}

**Detail / 细节**: The lone-worker panic button must be tested weekly with a logged result; a dead button is a life-safety gap. 独处员工 panic 按钮须每周测并记日志；失效按钮是人身安全缺口。
Unattended periods multiply the risk (HI-2). 无人时段放大风险（HI-2）。

**Why it bites / 痛点**: The button battery died; a late-night incident had no alert; regulator finds no test log. 按钮电池没了；深夜事故无告警；监管查无测试日志。
HI-2 / duty-of-care failure. 违反 HI-2 / 照护义务。

**Fix / 规则**: Weekly test + log; low-battery alert; spare unit on-site. 每周测+记；低电量告警；现场备机。
See `data/13-inspection-and-maintenance-calendar.md`. 见 `data/13` 检修日历。

**Related / 关联**: SKILL.md HI-2; Cluster T.

### UNM-03 Unmanned hours still need a human on-call {#md-121-unmanned-human-oncall}

**Detail / 细节**: "Unmanned" means no front desk, not no human — an on-call person must be reachable for incidents (HI-2). "无人"指无前台，非无人类——须有可联系的待命人处理突发（HI-2）。
Define on-call SLA + escalation. 定义待命 SLA+升级路径。

**Why it bites / 痛点**: A member injures at 2am; no one is reachable; response delayed; severity worsens. 会员凌晨2点受伤；联系不上人；响应延迟；伤情加重。
Liability from absent oversight. 因缺监管而担责。

**Fix / 规则**: Named on-call + 10-min ack SLA + panic integration. 指定待命+10分钟确认 SLA+联动 panic。
See `references/16-security-operations-and-emergency.md`. 见 `references/16` 安全应急。

**Related / 关联**: SKILL.md HI-2; Cluster J.

### UNM-04 Smart locker jams and traps belongings {#md-122-smart-locker-jam}

**Detail / 细节**: Smart lockers can jam; an unmanned club needs a remote-release or physical override so members aren't trapped without their bag. 智能储物柜可能卡死；无人场馆须有远程开或物理应急，免得会员拿不回包。
Provide a 24/7 override path. 提供7×24应急开路径。

**Why it bites / 痛点**: A locker jams at midnight; member's laptop is locked in; no staff; police called. 储物柜半夜卡死；会员电脑锁里；无员工；报警。
Reputation + possible claim. 口碑+可能索赔。

**Fix / 规则**: Remote-release API + physical master key in a sealed box. 远程开 API+封存物理总钥匙。
Daily locker health self-test. 每日储物柜自检。

**Related / 关联**: SKILL.md Cluster T; `data/10-hardware-fault-tree-library.md`.

### UNM-05 Glass-door sensor false-trips the alarm nightly {#md-123-glass-sensor-falsetrip}

**Detail / 细节**: A mis-aimed glass-break sensor false-trips the alarm every windy night, training staff to ignore it. 玻璃破碎传感器瞄错，每有大风夜误报，让员工学会无视。
Alarm fatigue defeats the system. 告警疲劳让系统形同虚设。

**Why it bites / 痛点**: After 20 false alarms, a real break-in alarm is dismissed as "another false". 20次误报后，真正的破门告警被当"又误报"忽略。
Theft during the ignored alert. 被忽略的告警期间遭窃。

**Fix / 规则**: Re-aim sensors; require two-factor (glass + motion) before alert. 重瞄传感器；玻璃+移动双因子才告警。
Log and tune false-trip rate. 记误报率并调参。

**Related / 关联**: SKILL.md Cluster T; `data/11-network-fault-tree-library.md`.

### UNM-06 Unmanned club's Wi-Fi is the only camera backhaul {#md-124-wifi-only-camera-backhaul}

**Detail / 细节**: If cameras backhaul only over Wi-Fi and the AP reboots, you lose footage exactly when incidents happen. 若摄像头只走 Wi-Fi 回传，AP 一重启，恰好在出事时丢录像。
Use wired backhaul for security cameras. 安防摄像头用有线回传。

**Why it bites / 痛点**: A break-in occurs during an AP reboot; zero footage; insurance denies the claim. 破门发生在 AP 重启时；零录像；保险拒赔。
Unrecoverable loss. 不可挽回损失。

**Fix / 规则**: PoE wired backbone for cameras; Wi-Fi only as redundant. 摄像头用 PoE 有线主干；Wi-Fi 仅冗余。
See `data/11-network-fault-tree-library.md`. 见 `data/11` 网络故障树。

**Related / 关联**: SKILL.md Cluster D; Cluster T.

### UNM-07 Temperature log for sauna/steam is manual and forgotten {#md-125-sauna-temp-manual}

**Detail / 细节**: Unattended sauna/steam rooms need automated over-temp cutoffs + logs; a manual log gets skipped at night. 无人桑拿/蒸汽房需自动超温切断+记录；手工记录夜班会被漏。
Automate the safety cutoff; keep the log. 自动化安全切断；保留日志。

**Why it bites / 痛点**: Overnight the heater faults hot; no cutoff; a member is burned next morning's first user. 整夜加热器故障升温；无切断；次日首位会员烫伤。
HI-2 / life-safety incident. 违反 HI-2 / 人身安全事件。

**Fix / 规则**: Hardwired over-temp limit switch + alert; never software-only. 硬接线超温限位开关+告警；绝不只靠软件。
See `references/16-security-operations-and-emergency.md`. 见 `references/16`。

**Related / 关联**: SKILL.md HI-2; Cluster J.

### UNM-08 The "unmanned" app check-in still needs ID proof {#md-126-unmanned-id-proof}

**Detail / 细节**: Even unmanned, first-time or flagged entries need an ID-proof step to stop shared-account abuse. 即便无人，首次或标记入场也需身份验证步骤，防共享账户滥用。
Keep a lightweight verify for risk flags. 对风险标记保留轻量核验。

**Why it bites / 痛点**: A shared account is used by 5 people in an unmanned club; capacity and billing both wrong. 无人馆里一个共享账号被5人用；容量与账单都错。
Fraud + safety overflow. 欺诈+安全超载。

**Fix / 规则**: Risk-based step-up verification; flag shared-device logins. 基于风险的递进核验；标记共享设备登录。
See MEM-01/MEM-09. 见 MEM-01/MEM-09。

**Related / 关联**: SKILL.md Cluster T; HI-1.

### UNM-09 Emergency lighting fails because bulbs are dimmed {#md-127-emergency-light-dimming}

**Detail / 细节**: Smart lighting that "dims for ambiance" can dim emergency exit lights below code; separation is required. 为氛围"调暗"的智能照明可能把应急出口灯调到不合规亮度；须分离。
Emergency lights on a separate, non-dimmable circuit. 应急灯走独立、不可调光回路。

**Why it bites / 痛点**: A power dip triggers dimmed "emergency" lights too faint to see; evacuation slows. 断电时调暗的"应急"灯太暗看不见；疏散变慢。
Life-safety code breach. 违反人身安全规范。

**Fix / 规则**: Separate emergency circuit; monthly 90-min battery test. 独立应急回路；每月90分钟电池测。
See FACILITY-13. 见 FACILITY-13。

**Related / 关联**: SKILL.md HI-2; Cluster D.

### UNM-10 Offboarding still leaves gate app access {#md-128-offboarding-gate-access}

**Detail / 细节**: When an employee leaves, their gate-app/credential access must be revoked same-day, not "next week". 员工离职时其闸机 App/凭证访问须当日撤销，而非"下周"。
See also FACILITY-11 physical keys. 亦见 FACILITY-11 实体钥匙。

**Why it bites / 痛点**: A fired employee's app still opens the back gate; they enter at night "to collect things". 被解雇员工 App 仍能开后门；夜里进来"拿东西"。
Theft + liability. 盗窃+责任。

**Fix / 规则**: Same-day revoke of all digital + physical access; checklist sign-off. 当日撤销全部数字+实体访问；清单签字。
See `data/21` #ap-047-offboarding-checklist. 见 `data/21` #ap-047。

**Related / 关联**: SKILL.md Cluster T; `data/21-anti-pattern-library.md` #ap-047-offboarding-checklist.

---

## 12. Pool, Sauna & Wet Areas / 泳池、桑拿与涉水区

### POOL-01 Humidity kills tablets — IP-rated cases {#md-129-pool-tablet-ip-case}

**Detail / 细节**: Pool-deck tablets/kiosks corrode fast; only IP65+ enclosed devices survive, with regular silicone-gasket checks. 池边平板/自助机腐蚀极快；只有 IP65+ 封装设备能扛，并定期查硅胶密封。
Consumer tablets die in weeks poolside. 消费级平板在池边几周就废。

**Why it bites / 痛点**: A standard iPad at the pool desk blacks out in 3 weeks; check-in reverts to paper. 池边前台标准 iPad 三周黑屏；签到退回纸质。
Member friction + data gap. 会员摩擦+数据缺口。

**Fix / 规则**: IP65 enclosure + desiccant; quarterly gasket inspection. IP65 封装+干燥剂；每季度查密封。
See `data/10-hardware-fault-tree-library.md`. 见 `data/10` 硬件故障树。

**Related / 关联**: SKILL.md Cluster C; `data/10-hardware-fault-tree-library.md`.

### POOL-02 Sensor probes need calibration-fluid stock {#md-130-pool-probe-calibration}

**Detail / 细节**: pH/ORP/chlorine probes drift; without calibration fluid in stock, readings go unverified and the water quality blinds. pH/ORP/余氯探头会漂移；不备校准液，读数无法校验，水质变盲。
Keep calibration standards + a schedule. 备校准标液+排期。

**Why it bites / 痛点**: A probe drifts high; the system under-doses chlorine; a skin-irritation cluster follows. 探头漂高；系统少加氯；随后出现皮肤刺激聚集。
Health incident + closure. 健康事件+停业。

**Fix / 规则**: Monthly calibration with fresh fluid; log the offset. 每月用新液校准；记偏移。
Manual test strip cross-check daily. 每日试纸人工复核。

**Related / 关联**: SKILL.md HI-2; Cluster J; `data/13-inspection-and-maintenance-calendar.md`.

### POOL-03 Anti-drowning camera trusts AI over lifeguard {#md-131-pool-ai-over-lifeguard}

**Detail / 细节**: Computer-vision drowning detection must ASSIST the lifeguard, never replace them (HI-2). AI 防溺水视觉须**辅助**救生员，绝不可替代（HI-2）。
Keep a human watch at all times; AI is an extra alarm. 始终保留人工盯防；AI 只是额外报警。

**Why it bites / 痛点**: The club relies on AI alone; the model misses a rare pose; a drowning is undetected. 场馆只靠 AI；模型漏掉罕见姿态；溺水未被发现。
HI-2 violation + tragedy. 违反 HI-2 + 悲剧。

**Fix / 规则**: AI = secondary alert only; lifeguard on duty mandatory; fail-safe. AI 仅作次级告警；救生员在岗强制；故障安全。
See `data/21` #ap-012-sensor-over-lifeguard (💀). 见 `data/21` #ap-012（💀）。

**Related / 关联**: SKILL.md HI-2; `data/21-anti-pattern-library.md` #ap-012-sensor-over-lifeguard.

### POOL-04 Pool-gate QR reader fogs every morning {#md-132-pool-gate-fog}

**Detail / 细节**: The humid pool-entry reader fogs at the temperature swing each morning; a hydrophobic film + heater solves it. 潮湿的泳区入口读卡器每天温差时起雾；疏水膜+加热可解。
Same root cause as FACILITY-15 but pool-specific humidity. 与 FACILITY-15 同因，但泳区湿度特有问题。

**Why it bites / 痛点**: Morning swimmers tap 4× to enter; queue at the lane. 晨泳者刷4次才进；泳道排队的队。
Churn among your most loyal segment. 最忠诚客群反而流失。

**Fix / 规则**: Heated/anti-fog reader + IP65; wipe schedule. 加热/防雾读卡器+IP65；定时擦拭。
See FACILITY-15. 见 FACILITY-15。

**Related / 关联**: SKILL.md Cluster C; FACILITY-15.

### POOL-05 Wet-area outlets must be GFCI/RCD protected {#md-133-pool-gfci-outlet}

**Detail / 细节**: Any outlet near water needs GFCI/RCD protection; a standard socket is a shock hazard. 近水插座须有漏电保护（GFCI/RCD）；普通插座是触电隐患。
Mandatory for pooldeck power. 池边供电强制。

**Why it bites / 痛点**: A standard socket by the pool gets splashed; a member plugging in a phone charger is shocked. 池边普通插座被溅水；会员插手机充电器时触电。
Injury + liability. 伤害+责任。

**Fix / 规则**: GFCI/RCD on all wet-area circuits; test monthly. 所有涉水回路装漏电保护；每月测。
See `references/16-security-operations-and-emergency.md`. 见 `references/16`。

**Related / 关联**: SKILL.md HI-2; Cluster D.

### POOL-06 Chemical store temp alarm missing {#md-134-pool-chem-temp-alarm}

**Detail / 细节**: Pool chemicals (chlorine, acid) need a temperature/alarm-controlled store; overheating or leaking goes unnoticed unmanned. 泳池药剂（氯、酸）须温控+报警的库房；无人时过热或泄漏无人知。
Environmental monitoring on the chem room. 药剂间装环境监控。

**Why it bites / 痛点**: A summer afternoon the chem store hits 45°C; a container leaks; toxic fumes. 夏日午后药剂间达45°C；容器泄漏；有毒气体。
Evacuation + hazard. 疏散+危害。

**Fix / 规则**: Temp + gas-leak sensors with alert; ventilated store. 温度+气体泄漏传感告警；通风库房。
See Cluster J. 见集群 J。

**Related / 关联**: SKILL.md HI-2; Cluster J.

### POOL-07 Lane-booking double-counts during a meet {#md-135-pool-lane-doublecount}

**Detail / 细节**: During a club swim meet, manual lane reservations + the app double-book the same lane. 俱乐部泳赛时，人工泳道预约与 App 重复占了同一泳道。
Single source of truth for lane state. 泳道状态须单一真相源。

**Why it bites / 痛点**: Two groups assigned one lane; on-site argument; event delayed. 两组被分到同一条道；现场争执；活动延误。
Reputation with your community. 社区口碑受损。

**Fix / 规则**: App is the sole lane ledger; manual overrides logged. App 为唯一泳道账；人工改动作记录。
See CLS-05 capacity sync. 见 CLS-05 容量同步。

**Related / 关联**: SKILL.md Cluster A; CLS-05.

### POOL-08 Underwater speaker audio leaks to neighbors {#md-136-pool-speaker-leak}

**Detail / 细节**: Underwater/pooldeck speakers can transmit through the structure to adjacent units; volume + scheduling limits needed. 水下/池边音箱会经结构传声到邻户；需限音量+限时段。
Acoustic isolation + quiet hours. 声学隔离+静默时段。

**Why it bites / 痛点**: Evening aqua-class music vibrates the upstairs residences; noise complaint to the building. 傍晚水中课音乐震到楼上住宅；遭楼宇噪声投诉。
Lease/municipal friction. 租赁/市政摩擦。

**Fix / 规则**: Limit dB + end by local quiet hour; survey neighbors. 限分贝+当地静默前结束；走访邻居。
See MSG-02 quiet hours. 见 MSG-02 静默时段。

**Related / 关联**: SKILL.md Cluster A; MSG-02.

### POOL-09 Shower water temp scald without mixer limit {#md-137-pool-shower-scald}

**Detail / 细节**: Public showers need anti-scald thermostatic mixers; an unmanaged supply can flash hot and burn. 公共淋浴需防烫恒温混水阀；无管控供水会骤热烫伤。
Set a hard max outlet temperature. 设硬性出水最高温。

**Why it bites / 痛点**: A cold-water pressure drop spikes the shower to 60°C; a member is scalded. 冷水压力掉，淋浴骤升60°C；会员烫伤。
Injury + claim. 伤害+索赔。

**Fix / 规则**: Thermostatic mixers with max-temp stop; quarterly test. 带最高温限的恒温混水阀；每季度测。
See `data/13-inspection-and-maintenance-calendar.md`. 见 `data/13` 检修日历。

**Related / 关联**: SKILL.md HI-2; Cluster J.

### POOL-10 Pool app shows "open" but the lifeguard called in sick {#md-138-pool-open-no-lifeguard}

**Detail / 细节**: The app/pool status must reflect lifeguard availability; showing "pool open" with no guard on duty is a safety lie. App/泳池状态须反映救生员在岗；显示"泳池开放"却无救生员是在安全上撒谎。
Gate pool access on lifeguard-on-duty status. 泳池准入以救生员在岗为闸。

**Why it bites / 痛点**: The app says open; a member swims solo; a cramp becomes an emergency with no one watching. App 说开放；会员独自游；抽筋成急救却无人盯。
HI-2 / life-safety failure. 违反 HI-2 / 人身安全失败。

**Fix / 规则**: Pool status = lifeguard status; auto-close on guard absence. 泳池状态=救生员状态；缺岗自动关闭。
Desk/APP sync on guard check-in. 救生员签到即同步前台/App。

**Related / 关联**: SKILL.md HI-2; CLS-07.

---

## G13 Tri-Perspective Coverage / G13 三视角覆盖矩阵

> This ledger was authored to cover the Architect × Operator × Member touchpoints so no micro-detail is an orphan.
> 本总账覆盖「架构师 × 运营者 × 会员」三类触点，确保每条微细节都不是孤儿。

- **Architect / 架构师**: Facility wiring, network/UPS design, data-model keys, AI guardrails, compliance mappings, vendor lock-in clauses, pool safety architecture — the "build it right" layer (FACILITY-01~18, PAY-04/06, MEM-01/02/04, AI-01~12, CMP-01~12, VEN-01~10, UNM-06/09, POOL-03/05/09).
- **Operator / 运营者**: Front-desk stocks, gate caching, reconciliation hour, refund rules, scheduling DST, coach substitution, offboarding, panic-button tests, chemical calibration — the "run it daily" layer (GATES-01~12, PAY-01/02/03/08/10/11, MEM-03/05/08/10/12, MSG-01~12, CLS-01~10, FIN-01~08, UNM-01~10, POOL-01/02/04/06/07/08/10).
- **Member / 会员**: Recognition fairness, privacy of photo/PII, no surprise charges, reachable support, safe environment, honest "open" status, dignified access — the "experience & trust" layer (MEM-02/05/07/09/11, MSG-03/04/08/11/12, CLS-02/03/04/09, AI-02/03/08, CMP-03/05/09/10/12, POOL-03/09/10).

> **Honesty note / 诚实注记**: Every "failure story" above is an archetypal pattern, not a claimed real incident. Verify market-specific regulations via `tools/05` and volatile vendor/pricing facts via `tools/04` before acting.
> 上述每个"翻车案例"均为原型模式，非声称的真实事件。行动前请经 `tools/05` 核验市场法规、经 `tools/04` 核验易变供应商/价格事实。
