# Repair Scripts & SLA Library / 报修话术与 SLA 条款库

> **Cluster / 集群**: I (IT governance & money) + D (Network) + C (Hardware)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify every 90 days; SLA norms, labor rates and warranty terms pass `tools/04`/`tools/05` before citing. Market politeness norms shift — verify via `tools/04`.
> **Cross-references / 交叉引用**: `references/05-methodology-library.md` (money questions) · `references/07-hardware-landscape-and-vendors.md` · `references/08-network-and-infrastructure.md` · `data/11-network-fault-tree-library.md` · `data/12-software-fault-tree-library.md` · `data/13-inspection-and-maintenance-calendar.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

Vendor-interaction leverage kit for zero-basis operators. The goal: get a **ticket number and a started SLA clock** in one call, with evidence ready, without admitting fault you don't have.
0 基础经营者的「对付厂商」筹码。目标：一通电话拿到**工单号 + 已启动的 SLA 计时**，证据备齐，且不替自己没犯的错背锅。

---

## Universal Repair Call Structure / 通用报修通话结构

Use this 5-step order on EVERY vendor call. Say symptom, not diagnosis.
每次厂商电话都用这 5 步。说「症状」，别说「诊断」。

1. **Identify / 亮身份**: Club name, account ID, your name, the device/location. / 店名、账号、你姓名、设备/位置。
2. **Describe symptom, not diagnosis / 说症状不说诊断**: "The gate won't open for valid members" — NOT "your controller is broken". / 「有效会员闸机不开」——别说「你控制器坏了」。
3. **Evidence ready / 证据备齐**: ticket-ready screenshot/log/photo/error text in hand before dialing. / 打电话前手里备好截图/日志/照片/报错原文。
4. **Get the ticket number / 要工单号**: "Please give me the ticket number." Write it down immediately. / 「请给我工单号。」立刻记下。
5. **Confirm SLA clock started / 确认 SLA 计时已起**: "What is the response time and resolution target per our SLA? When does the clock start?" / 「按 SLA 响应与解决时限是多少？计时从何时起？」

> 💡 If the agent won't give a ticket number, say: "Without a ticket number I can't track this or claim SLA — please raise one now." Hold the line.
> 💡 若客服不给工单号，说：「没工单号我无法跟踪也无法主张 SLA——请现在开一个。」别挂。

---

## Per-Category Call Scripts / 分类报修话术（照着念）

### Equipment vendor (treadmill/locker/scanner) / 设备厂商（跑步机/储物柜/体测仪）
- ZH: "你好，我是 <店名>，设备 <型号/序列号> 于 <时间> 出现 <症状原文>。已按手册重启无效。请开维修工单，给工单号，并说明保内/保外与上门时限。"
- EN: "This is <club>, unit <model/SN> showed <exact symptom> at <time>. Reboot per manual failed. Please raise a ticket, give the number, and state in/out of warranty and on-site ETA."

### MMS SaaS support / 会籍 SaaS 客服
- ZH: "账号 <ID>，于 <时间> <现象>，后台最后同步 <时间>。请确认是服务端还是配置问题，给工单号与 ETR。影响 <N> 名会员。"
- EN: "Account <id>, at <time> <symptom>, last sync <time>. Confirm server-side or config; give ticket number and ETR. <N> members impacted."

### ISP line fault / 运营商线路故障
- ZH: "地址 <地址>，光猫 PON/LOS 红灯，已重启光猫路由仍无外网。请派单给工单号，全场 <N> 人断网，给 ETR 与是否赔服务抵扣。"
- EN: "At <address> modem PON/LOS red, power-cycled, still down. Raise a ticket, give number; ~<N> people offline. ETR and any service credit?"

### Electrician / 电工
- ZH: "店内有 <现象，如UPS叫/插座无电>。疑似电气问题，请带证上门排查，先做安全断电再修。事关人员安全（HI-2）。"
- EN: "We see <symptom, UPS beeping/no power>. Suspect electrical; please attend certified, isolate safely first. Life-safety relevant (HI-2)."

### Cabling contractor / 布线师傅
- ZH: "请带 Fluke 级测试仪来，验收 <N> 个信息点，要求全 8 芯通且达标 Cat6，交测试报告。"
- EN: "Bring a certifier, verify <N> drops, all 8 wires through, Cat6 compliant, hand over a test report."

### CCTV installer / 监控安装商
- ZH: "摄像头 <编号> 于 <时间> 黑屏，NVR 正常。请远程或上门排查，确认是否 PoE 供电或链路问题，给工单号。涉及安全（HI-5 禁区外）。"
- EN: "Camera <id> black at <time>, NVR fine. Remote or on-site check PoE/link; ticket number please. Security-related (HI-5 outside no-go zones)."

---

## Escalation Phrases: Work vs Backfire / 升级话术：管用 vs 反效果

| Situation / 场景 | Works / 管用 | Backfires / 反效果 |
|---|---|---|
| No ticket number / 没工单号 | "没工单我无法跟踪也无法主张 SLA，请现在开。" | "你这什么破系统！" (情绪化) |
| Too slow / 太慢 | "按 SLA 响应时限已超 <X>，请升级资深工程师并给新 ETR。" | "再不修我投诉你！" (空威胁) |
| They blame you / 甩锅给你 | "我方已按手册重启并备好日志，请基于证据排查而非假设我方责任。" | "不可能使我们的错！" (对抗) |
| Recurring fault / 反复坏 | "这季度第 <N> 次，请根治而非临时修，并启动换机/退款评估。" | "你们就是骗子。" (人身) |
| Money dispute / 费用争议 | "按合同 <条款> 此项应在保内/应赔，请引用条款。" | "不付钱了！" (违约风险) |

> Rule: stay factual, cite the SLA/contract clause, never insult. Calm + clause = leverage.
> 规矩：只讲事实、引 SLA/合同条款、不人身攻击。冷静 + 条款 = 筹码。

---

## SLA Clause Library / SLA 条款库

Copy these clause intents into every vendor contract. Define in plain words before signing (link `references/05` money questions).
把这些条款意图写进每个厂商合同。签约前用说人话定义（联 `references/05` 钱的问题）。

### Response vs Resolution time / 响应时限 vs 解决时限
- **Response / 响应**: time to first human reply ("we got your ticket"). / 首次人工回复的时间（「收到工单」）。
- **Resolution / 解决**: time to actually fix or workaround. / 真正修好或绕过的时限。
- Trap: a vendor quoting only "response 4h" may never promise resolution. Always write BOTH, per severity (P1/P2/P3).
- 坑：只报「响应 4h」的厂商可能从不承诺解决。P1/P2/P3 各级都写「响应+解决」二者。

### Business-hours traps / 营业时间陷阱
- "Business hours 9–6 Mon–Fri" means a Saturday morning outage waits until Monday. For a gym (evenings/weekends peak), demand **24/7 or at least extended/peak coverage**.
- 「营业时间 9–6 工作日」= 周六早上的故障等到周一。健身房高峰在晚/周末，要**24/7 或至少延长/高峰覆盖**。

### Penalty / service-credit clause / 罚则或服务抵扣条款
- "If resolution misses SLA by >X, client receives Y days of fee as credit." This is your money back without a fight (see `data/11` #n10).
- 「解决超 SLA 超 X，客户获 Y 天费用抵扣。」这是不打架拿回的钱（见 `data/11` #n10）。

### Spare-part availability clause / 备件可用条款
- "Critical spares (gate controller, PoE switch, UPS) stocked or 24h deliverable." For 24h clubs this is HI-2 safety, not convenience.
- 「关键备件（闸机控器、PoE 交换、UPS）有库存或 24h 可达。」24h 店这是 HI-2 安全，非便利。

### End-of-life (EOL) notice clause / 停产(EOL)通知条款
- "Vendor gives ≥90 days written EOL notice + migration path." Prevents sudden "no longer supported" stranding you.
- 「厂商提前 ≥90 天书面 EOL 通知 + 迁移路径。」防突然「不再支持」把你晾着。

### Exit / data-return clause / 退出与数据返还条款
- "On termination, full data export in standard format within X days, no extra fee, parallel-run supported." This is HI-8 + the #s16 STOP-LINE protector.
- 「终止时 X 天内标准格式全量导出、不另收费、支持并行运行。」这是 HI-8 + #s16 停手线的护盾。

---

## Market Localization Notes / 市场本地化备注

🔄 Verify current norms via `tools/04` before a cross-market rollout.
🔄 跨市场扩张前经 `tools/04` 核验当前规范。

- **Japan / 韩国 (JP/KR)**: Politeness + written escalation win. Open with apology-for-trouble ("ご迷惑をおかけして…"), state facts calmly, escalate in writing (email/fax). Direct/blunt styles backfire and slow you down. / 礼貌 + 书面升级制胜。以「给您添麻烦」开场，冷静陈述，书面升级。直接生硬反效果且拖慢。
- **CN**: WeChat / enterprise WeChat groups are the fast channel; keep the outage log exportable for tax/consumer-protection queries. / 微信/企业微信是快通道；故障日志可导出备税务/消保查询。
- **KR**: KakaoTalk for vendor comms; keep a Korean + English copy of the ticket. / KakaoTalk 沟通；工单留韩英双份。
- **SEA / Oceania**: LINE (TH/TW) / WhatsApp (SG/MY/PH/AU/NZ) / Zalo (VN) per market; confirm SLA in writing as chat logs alone may not bind. / 按市场用 LINE/WhatsApp/Zalo；SLA 要书面确认，聊天记录未必具约束力。
- **Direct-style markets**: Lead with the symptom + ticket demand; less ceremony is fine, but still cite the clause. / 直接风格市场：直说症状+要工单；少客套无妨，仍引条款。

> Universal: whatever the market, **get the ticket number and the SLA clock in writing**. Politeness opens doors; the clause closes the deal.
> 通用：不论市场，**工单号与 SLA 计时要落到书面**。礼貌开门，条款成交。

---

## Complaint-Letter Template Pointers / 投诉信模板要点

When phone fails, send a written complaint. Structure (bilingual):
电话不行就发书面投诉。结构（双语）：
1. **Header / 抬头**: date, your club, account ID, all prior ticket numbers. / 日期、店名、账号、所有历史工单号。
2. **Fact timeline / 事实时间线**: when it broke, what you did, what they said, SLA breached by how much. / 何时坏、你做了啥、他们说啥、SLA 超多少。
3. **Clause cited / 引用条款**: paste the exact SLA/contract line. / 贴确切 SLA/合同原文。
4. **Ask / 诉求**: specific remedy (credit / on-site / replacement) + deadline. / 具体补救（抵扣/上门/换机）+ 期限。
5. **Copy / 抄送**: your legal/owner; note you'll escalate to consumer body if unresolved (market-specific, verify `tools/05`). / 抄送法务/老板；注明未决将上报消保（随市场，经 `tools/05`）。

Keep it factual, dated, and saved — this letter is your evidence for refunds, credits, or disputes.
保持事实、带日期、留存——这封信是你退款/抵扣/争议的凭证。

---

## Multi-Vendor Triangulation (the blame triangle) / 多厂商甩锅三角

The classic: **printer won't print → network vendor says "not us", POS vendor says "network", MSP says "printer driver".** Nobody fixes it. Use this script to force ownership.
经典：打印机打不出→网络商说「不是我」、POS 商说「网络」、MSP 说「驱动」。没人修。用此话术逼出责任方。

- Step 1 — isolate with evidence: "We printed a Windows test page (passes) → printer+driver OK. We pinged the POS from the printer (pass/fail). We checked the POS can reach the gateway (pass/fail)." Present the matrix.
- 第1步—证据隔离：「我们打了系统测试页（过）→ 打印机+驱动 OK。从打印机 ping POS（过/不过）。查 POS 能否到网关（过/不过）。」抛矩阵。
- Step 2 — name the gap: "The failure sits between <A> and <B>. <A> vendor, please confirm your side; <B> vendor, yours." Don't let "not me" end the call.
- 第2步—点出缺口：「故障在 <A> 与 <B> 之间。<A> 商请确认你侧；<B> 商你侧。」别让「不是我」结束通话。
- Step 3 — joint call: "Please book a 3-way call at <time> with <A> and <B>." A joint call kills the triangle fast.
- 第3步—三方会：「请约 <时间> 与 <A><B> 三方通话。」三方会秒杀甩锅三角。
- Log the matrix + the call in `data/16`. If still unresolved, escalate per `data/13` escalation path.
- 矩阵+通话记 `data/16`。仍不决按 `data/13` 升级路径上报。

---

## Warranty vs Paid-Repair Decision Math / 保内 vs 付费维修决策算术

Before saying yes to a paid repair, run this:
答应付费维修前，算这笔：

| Factor / 因子 | Warranty (free) / 保内免费 | Paid repair / 付费修 | Replace / 换新 |
|---|---|---|---|
| Age vs warranty / 年龄vs保 | In warranty / 在保 | Out, <3yr / 过保<3年 | >3–5yr / >3–5年 |
| Repair cost / 维修费 | ¥0 | <40% of replace / <换新40% | ≥40% of replace / ≥换新40% |
| Downtime cost / 停机成本 | Low / 低 | Medium / 中 | High if wait / 等则高 |
| Decision / 决策 | Use warranty / 走保 | Repair / 修 | Replace / 换 |

- Rule of thumb: if repair cost ≥ 40% of replacement AND the unit is >3–5 yr old, replace (range, market-dependent 🔄). For life-safety items (gate, AED, sauna sensor), prefer replace over repeated repair (HI-2).
- 经验：维修费 ≥ 换新 40% 且机龄 >3–5 年 → 换新（区间，随市场 🔄）。人身安全项（闸机、AED、桑拿传感器）优先换新而非反复修（HI-2）。
- Always get the **≥3 quotes** rule (HI-8): warranty claim, paid quote, replacement quote — compare before paying a cent.
- 永远**≥3 家比价**（HI-8）：保内索赔、付费报价、换新报价——付一分前先比。

---

## Pre-Call Evidence Checklist / 打电话前证据清单

Have these ready before dialing — a call without evidence wastes the first 10 minutes and loses the SLA clock.
打电话前备齐——没证据的电话浪费前 10 分钟且丢失 SLA 计时。

| Category / 类别 | Evidence to have / 需备证据 |
|---|---|
| Network (ISP/MSP) / 网络 | Modem light photo, speed test result, neighbor-check note, exact start time / 光猫灯照片、测速结果、邻居核查、确切开始时间 |
| MMS SaaS | Error screenshot, last-sync time, member ID, impact count / 报错截图、最后同步、会员ID、影响数 |
| Equipment / 设备 | Model + SN, symptom text, reboot proof, photo/video / 型号+序列号、症状原文、重启证明、照片视频 |
| Payment / 支付 | Two txn IDs, amount, gateway status, time / 两笔交易号、金额、网关状态、时间 |
| CCTV / 监控 | Channel id, black-screen time, NVR status / 通道号、黑屏时间、NVR 状态 |
| Electric / 电气 | Symptom, UPS display, breaker state / 症状、UPS 显示、空开状态 |

> Rule: screenshot + timestamp + your account ID. Without these three, the agent will ask and the clock waits.
> 规矩：截图 + 时间戳 + 账号ID。缺这三项，客服会反问、计时就等。

---

## Ticket Tracking Template / 工单跟踪模板（抄用）

```
Vendor / 厂商: ____  Ticket # / 工单号: ____  Opened / 开: <date time>
Symptom / 症状: ________________________________________
SLA response / 响应时限: ____  SLA resolution / 解决时限: ____  Clock start / 起算: ____
Updates / 跟进: <time> <who> <what>  |  <time> <who> <what>
Breach? / 超SLA?: Yes/No  Credit claimed / 主张抵扣: ____  Resolved / 解决: <time>
Escalated to / 升级至: ____  Note / 备注: ________________________
```

One row per ticket, kept in `data/16-freshness-ledger.md`. At renewal, this sheet is your negotiation leverage (see below).
每单一行，存 `data/16`。续约时这表是你的谈判筹码（见下）。

---

## Red Flags in a Vendor's First Reply / 厂商首次回复的红旗

- "Please try restarting" as the ONLY answer, ignoring your reboot proof → they didn't read; push for tier-2. / 只回「重启」无视你重启证明 → 没看；要求二线。
- "No SLA on this plan" → you're on a free/cheap tier; budget for paid support or switch (HI-8). / 「此套餐无 SLA」→ 你在免费/低价档；备付费支持或换（HI-8）。
- "That's a different team" with no handoff → blame triangle starting; demand a joint call (see triangulation). / 「那是另一队」不交接 → 甩锅三角起；要求三方会（见三角）。
- "We don't provide the ticket number" → refuse; no ticket = no SLA, no track. Hold firm. / 「不给工单号」→ 拒；无单=无SLA无跟踪。坚持。
- "It's a known issue, no ETA" → ask for the public status-page link and a credit policy. / 「已知问题无 ETA」→ 要公开状态页链接与抵扣政策。

---

## Renewal Negotiation Using Your SLA Log / 用 SLA 日志谈续约

Before any renewal, open `data/16` and compute:
续约前开 `data/16` 算：
1. **Outage hours past year / 全年故障小时** → if high, demand better SLA or leave. / 高则要求更好 SLA 或走。
2. **SLA breaches (credits owed but not given) / 超 SLA（应抵未抵）** → demand back-credit or discount. / 要求补抵扣或折扣。
3. **Repeat faults same device / 同设备反复坏** → demand free replacement or EOL migration path. / 要求免费换或 EOL 迁移。
4. **Response/resolution actually met? / 响应解决真达标？** → if not, renegotiate the numbers down (stricter) or switch. / 没达标则重谈更严数字或换。

Lead the renewal call with the log, not with loyalty. Vendors discount proven pain more than friendly reminders (link `references/05` money questions, `data/13` annual map).
续约电话带日志开场，而非带忠诚。厂商对「有据的痛」比「友好的提醒」更肯降价（联 `references/05` 钱的问题、`data/13` 年检地图）。

---

## After-Hours Emergency Escalation / 非工作时间紧急升级

For a gym, "after hours" is often peak. Define urgency BEFORE you need it:
对健身房，「非高峰」常是高峰。紧急度要提前定义：

- **P1 (life-safety / 人身安全)**: gate stuck closed with members inside, AED/comms dead, sauna over-temp. → call NOW, cite HI-2, demand immediate. / 闸机误关困人、AED/通讯死、桑拿超温 → 立刻打，引 HI-2，要求即刻。
- **P1 (revenue-down / 营收断)**: whole club offline at peak, POS dead. → call NOW, cite SLA, demand <2h response. / 高峰全店断、POS 死 → 立刻打，引 SLA，要求 <2h 响应。
- **P2 (degraded / 降级)**: one camera down, one SSID missing. → next-business-hour ticket. / 一摄黑、一名缺失 → 次工作日单。
- **P3 (cosmetic / 外观)**: label typo, minor UI. → batch into monthly. / 标签错、小UI → 并入月单。

Keep the vendor's 24/7 emergency number in the front-desk phone labeled "EMERGENCY <vendor>" — not buried in an email.
厂商 24/7 应急号存前台手机为「应急<厂商>」——别埋在邮件里。

---

## Contract Traps Beyond SLA / SLA 之外的合同坑

Beyond the SLA clause library, watch these in the fine print (link `references/05` money questions, HI-8):
除 SLA 条款库，细看这些小字（联 `references/05` 钱的问题、HI-8）：

- **Auto-renew with short notice window / 自动续约+短通知窗**: "auto-renews unless cancelled 90 days prior" — mark the calendar at signing. / 「提前 90 天不取消即自动续」——签约即标日历。
- **Price-escalation clause / 涨价条款**: "vendor may raise fees ≤X%/yr" — cap it or negotiate a floor. / 「厂商可年涨 ≤X%」——封顶或谈下限。
- **Data egress fee / 数据出口费**: "export costs ¥X per GB" — kills the exit clause; demand free export. / 「导出每 GB 收 ¥X」——废了退出条款；要求免费导出。
- **Liability cap below your loss / 责任上限低于损失**: "vendor liability capped at 1 month fee" — negotiate up for data-loss scenarios. / 「厂商责任上限 1 月费」——数据丢失场景谈高。
- **Sole-source lock-in / 独家锁定**: "must use vendor's only certified tech" — verify ≥3 options exist (HI-8). / 「须用厂商唯一认证技术」——确认有 ≥3 选项（HI-8）。
- **Jurisdiction & language / 管辖与语言**: dispute resolved in vendor's country/language — negotiate local venue for cross-border. / 争议在厂商国/语解决——跨境谈本地管辖。

Every trap above has a one-line fix: **read before sign, get ≥3 quotes, keep the exit clause free** (HI-8).
以上每坑一句话解：**签前读、≥3 家比、退出条款免费**（HI-8）。

---

## Closing the Call / 收尾纪律

Before you hang up, confirm three things aloud. If you can't, the call isn't done.
挂断前口头确认三件事。确认不了，电话就没完。

1. **Ticket number stated & noted / 工单号已报且记下**: "So the ticket is <number>, correct?" / 「工单是 <号>，对吗？」
2. **SLA clock stated / SLA 计时已说**: "Response by <time>, resolution by <time>, clock starts now?" / 「响应 <时间>、解决 <时间>、计时现在起？」
3. **Next step owned / 下一步有人认领**: "Who does what by when? I'll get <evidence> to you by <time>." / 「谁何时做啥？我 <时间> 前给你 <证据>。」

Then send a **written recap** (email/chat) within the hour: ticket number + symptom + SLA times + your next action. A verbal promise with no written recap is the #1 reason tickets vanish.
然后一小时内发**书面复述**（邮件/聊天）：工单号 + 症状 + SLA 时间 + 你方下一步。口头承诺无书面复述，是工单消失的头号原因。

> 💡 The written recap is also your proof if they later claim "you never reported this." Keep a copy in `data/16`.
> 💡 书面复述也是他们日后称「你从没报过」时的证据。副本存 `data/16`。

---

## At-a-Glance Index / 一页索引

- Call flow / 通话流程: Universal 5-step (identify → symptom → evidence → ticket → SLA clock). / 通用 5 步（亮身份→症状→证据→工单→SLA 计时）。
- Scripts / 话术: 6 categories verbatim (equipment, MMS, ISP, electrician, cabling, CCTV). / 6 类照念（设备、会籍、运营商、电工、布线、监控）。
- SLA clauses / SLA 条款: response vs resolution, business-hours, penalty/credit, spare-part, EOL, exit/data-return. / 响应vs解决、营业时间、罚则抵扣、备件、EOL、退出数据返还。
- Escalation / 升级: works-vs-backfires table; written complaint structure; triangulation script. / 管用vs反效果表；书面投诉结构；甩锅三角话术。
- Decisions / 决策: warranty vs paid-repair math; contract traps; renewal via SLA log. / 保内vs付费算术；合同坑；用 SLA 日志谈续约。

> Keep this file open during any vendor call — it is the operator's script, not a manual to read later.
> 任何厂商电话时把这文件打开——它是运营者的台词本，不是事后才看的说明书。

---

## G13 Tri-Perspective Note / G13 三视角覆盖说明

**Architect (架构师视角)**: This library is the contractual front-line of Cluster I. The universal call structure + SLA clause library turn vague "it's broken" into ticketing discipline, and the exit/data-return clause is the legal shield behind HI-8 and the #s16 STOP-LINE. Market notes keep escalation effective across the 12 APAC markets.
**架构师视角**：本库是 I 集群的合同前线。通用话术 + SLA 条款库把模糊「坏了」变工单纪律；退出/数据返还条款是 HI-8 与 #s16 停手线的法律盾。市场备注让 12 亚太市场升级有效。

**Operator (运营者视角)**: Zero-basis operators get verbatim sentences to read aloud, a blame-triangle script for the "not my problem" wall, and a repair-vs-replace math table — no jargon needed to hold a vendor accountable. The ticket number is the operator's single most powerful word.
**运营者视角**：0 基础经营者拿到照念的句子、对付「不归我管」墙的甩锅三角话术、修 vs 换算术表——无需行话即可让厂商负责。工单号是运营者最有力的一个词。

**Member (会员视角)**: Faster, evidence-based repairs mean less downtime at the gate, the POS and the cameras — member experience and safety (HI-2) protected not by luck but by contract. The exit clause also protects member data portability (HI-8) when switching vendors.
**会员视角**：更快、有据的维修 = 闸机/POS/摄像头更少停机——会员体验与安全（HI-2）靠合同而非运气守护。退出条款还保护换厂商时会员数据可携（HI-8）。

---

*Legal Notice / 法律声明 · Disclaimer / 免责声明 · Friendly Reminder / 温馨提示 · Author / 作者信息 — see SKILL.md output block. / 见 SKILL.md 输出规范块。*
