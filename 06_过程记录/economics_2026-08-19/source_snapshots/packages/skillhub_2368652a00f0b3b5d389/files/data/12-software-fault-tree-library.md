# Software & SaaS Fault Tree Library / 软件与 SaaS 故障树库

> **Cluster / 集群**: B (Software systems) + N (Integration) + M (Messaging)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify every 90 days; vendor status-page URLs, API/template policies and pricing pass `tools/04` before citing. SaaS menus change frequently — verify exact path per vendor.
> **Cross-references / 交叉引用**: `references/06-software-landscape-apac-vendors.md` · `references/17-omnichannel-messaging.md` · `references/18-integration-and-data-plumbing.md` · `data/10-hardware-fault-tree-library.md` (#C2 gate sync) · `data/11-network-fault-tree-library.md` · `data/13-inspection-and-maintenance-calendar.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

This is the **L0/L1 software firefighting** library. Every entry uses the five-segment structure: **Self-check / 自查 → Stop-line / 停手线 → Vendor support script / 报修话术（含需准备的日志/截图）→ Cost-impact hint / 费用影响参考 → Prevention / 预防措施**. For AI-bot issues see #s34 (HI-6 / HI-2 fallbacks).
本文件是 **L0/L1 软件救火**库。每条目五段式：**自查 → 停手线 → 报修话术（含需准备的日志/截图）→ 费用影响参考 → 预防措施**。AI 机器人问题见 #s34（HI-6/HI-2 兜底）。

---

## #s01-mms-login-fail /  会籍系统登录失败

**Self-check / 自查（说人话）**
- Three different causes: (a) wrong password, (b) account locked after too many tries, (c) vendor server down. First: can ANY staff log in? If yes → it's your account; if no → vendor outage.
  三类原因：(a) 密码错，(b) 多次尝试被锁，(c) 厂商服务器挂。先问：有员工能登吗？能=你账号问题；都不能=厂商故障。
- Check the vendor status page (saved in `data/13` or bookmarks) before calling.
  打电话前先查厂商状态页（存 `data/13` 或书签）。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT keep guessing passwords — you'll lock the account for everyone. After 3 fails, stop and use "forgot password" or call the vendor admin.
  不要一直猜密码——会锁全员。错 3 次就停，用「忘记密码」或叫厂商管理员。

**Vendor support script / 报修话术（准备：报错截图 + 账号 + 时间）**
- "账号 <账号> 于 <时间> 登录报 <错误原文/截图>。请确认：是密码错、账号锁定，还是服务端故障？我要工单号。"
- EN: "Account <id> failed login at <time> with <exact error/screenshot>. Confirm: wrong password, lockout, or server-side fault? Ticket number please."

**Cost-impact hint / 费用影响参考**
- Usually **¥0** (password/lock). Outage: covered by SLA if business plan (see `data/14`); free tier often no SLA (range 🔄).
  通常 **¥0**（密码/锁定）。故障：商用套餐走 SLA（`data/14`）；免费版常无 SLA（区间 🔄）。

**Prevention / 预防措施**
- Use SSO/MFA where offered; keep one **super-admin emergency account** with a documented recovery path; train "3 strikes = stop."
  用 SSO/MFA；留一个**超级管理员应急账号**并有书面恢复路径；培训「错 3 次就停」。

---

## #s02-membership-renewal-double-charge /  续费被扣两次

**Self-check / 自查（说人话）**
- A member was charged twice for one renewal. Check the MMS payment log: two transactions same amount, same member, seconds apart.
  会员被扣两次续费。查会籍支付日志：两笔同额、同会员、相隔几秒。
- Confirm it's not two separate products (e.g. membership + personal-training) — read both line items.
  先确认不是两笔不同产品（如会籍+私教）——读两行明细。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT promise the refund timeline you can't control. Tell the member "we've flagged it, the bank/provider needs 3–10 business days" (range).
  不要承诺你控制不了的退款时间。告诉会员「已标记，银行/支付方需 3–10 工作日」（区间）。

**Vendor support script / 报修话术（准备：两笔交易号 + 会员ID + 时间）**
- "会员 <ID> 于 <时间> 被扣两笔 <金额>，交易号 <A>/<B>。请确认重复扣款并启动原路退回，给我们处理工单号。"

**Cost-impact hint / 费用影响参考**
- Refund **¥0** to member (you absorb then reclaim from gateway). Gateway may keep a small fee on refund (range 🔄).
  会员侧退回 **¥0**（你先垫再向网关追）。网关退款可能留小额手续费（区间 🔄）。

**Prevention / 预防措施**
- Enable **idempotency / duplicate-transaction guard** at the gateway; reconcile daily (see `data/13` closing checklist). Flag double-charge pattern in `data/16`.
  开启**幂等/重复交易拦截**；每日对账（见 `data/13` 闭店清单）。`data/16` 标记双扣模式。

---

## #s03-member-cant-book-class /  会员约不了课

**Self-check / 自查（说人话）**
- Three causes: (a) class full / quota reached, (b) membership type not eligible (e.g. blocked plan), (c) app cache stale showing wrong availability.
  三类：(a) 课满/名额到，(b) 会籍类型不符（如冻结套餐），(c) App 缓存旧显示错余位。
- Refresh the app / re-login; check the class capacity in MMS backend; check the member's status (frozen/hold).
  刷新 App/重登；后台查课程容量；查会员状态（冻结/暂停）。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT manually overwrite a full class "to please a VIP" without a waitlist rule — you'll breach capacity and safety (HI-2 for packed studios).
  不要为「哄 VIP」手动塞满班不设候补——超员违安全（HI-2 满房）。

**Vendor support script / 报修话术（准备：会员ID + 课程ID + 报错截图）**
- "会员 <ID> 约课 <课程ID> 报 <错误>，后台显示容量 <X>/名额 <Y>/会员状态 <Z>。请确认是配额、资格还是缓存问题。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config/cache). Capacity redesign if chronic: consult `references/06`.
  配置/缓存 **¥0**。若长期满员需重设计：见 `references/06`。

**Prevention / 预防措施**
- Set **waitlist + auto-promote**; cache TTL short (≤60s); communicate quota rules to members at sale (HI-3 prepaid clarity).
  设**候补+自动递补**；缓存 TTL 短（≤60s）；售卡时讲清名额规则（HI-3 预付透明）。

---

## #s04-class-schedule-vanished /  课表消失

**Self-check / 自查（说人话）**
- The weekly schedule disappeared or shows wrong days. Often a **timezone / DST** bug or a publish that wasn't confirmed.
  周课表消失或日期错。常是**时区/夏令时**bug，或发布未确认。
- Check: is the club's timezone set right in MMS? Did the scheduler "save" but not "publish"? Compare to last week's backup.
  查：会籍系统时区对吗？排课是「保存」还是「发布」？对比上周备份。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT bulk-edit the live schedule during peak booking — you may double-post or wipe more. Restore from backup first (see #s22).
  高峰别在线上批量改课表——可能重复或删更多。先备份恢复（见 #s22）。

**Vendor support script / 报修话术（准备：时区设置截图 + 发布记录）**
- "课表消失/日期错位，时区设为 <值>。请确认是否时区/DST 导致，并协助从 <日期> 备份恢复。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config/restore).
  配置/恢复 **¥0**。

**Prevention / 预防措施**
- Lock **timezone to club locale**; "save then publish" workflow with a second approver; weekly backup review (`data/13`).
  **时区锁定本地球**；「保存→发布」双人核；周备份复核（`data/13`）。

---

## #s05-app-push-not-delivered /  App 推送收不到

**Self-check / 自查（说人话）**
- You sent a push (class reminder) but members say they didn't get it. Check: did the member enable notifications? Did the push vendor report "sent" or "failed"?
  发了推送（上课提醒）会员说没收到。查：会员开了通知吗？推送商回报「已发」还是「失败」？
- iOS/Android need valid push certificates; expired cert = silent fail.
  iOS/Android 需有效推送证书；证书过期=静默失败。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT spam re-send 10× "to be sure" — that trains members to ignore and hurts deliverability. Send once, follow via SMS/WhatsApp.
  不要为「确保」重发 10 次——教会会员无视且伤送达。发一次，转短信/WhatsApp 兜底。

**Vendor support script / 报修话术（准备：推送任务ID + 失败报告）**
- "推送任务 <ID> 报告 <已发/失败数>。请确认是证书过期、令牌失效还是配额耗尽。"

**Cost-impact hint / 费用影响参考**
- Usually **¥0** (cert/token). Push volume over plan: **¥100–¥1,000/mo** (range 🔄).
  常 **¥0**（证书/令牌）。超量推送：**¥100–¥1000/月**（区间 🔄）。

**Prevention / 预防措施**
- Renew **push certs** before expiry (calendar in `data/13` annual); monitor delivery rate; use multi-channel fallback (see `references/17`).
  到期前续**推送证书**（`data/13` 年历）；监控送达率；多通道兜底（见 `references/17`）。

---

## #s06-miniprogram-white-screen /  小程序白屏

**Self-check / 自查（说人话）**
- The WeChat/Alipay mini-program shows a white/blank screen. Usually a JS error, an expired domain whitelist, or the backend API down.
  微信/支付宝小程序白屏。常是 JS 错误、域名白名单过期，或后端 API 挂。
- Try opening on another phone; check the mini-program's "request domain" whitelist in the platform console; check backend status.
  换手机试；查平台后台小程序「请求域名」白名单；查后端状态。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT edit production mini-program code live during open hours — publish to a test version first.
  营业时间不要直接改生产小程序代码——先发测试版。

**Vendor support script / 报修话术（准备：白屏截图 + 控制台报错 + 域名配置）**
- "小程序白屏，控制台报 <错误>，请求域名白名单含 <列表>。请协助定位是前端报错还是后端 API 不可达。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config/whitelist). Custom dev fix: **¥500–¥5,000** (range 🔄).
  配置/白名单 **¥0**。定制修复：**¥500–¥5000**（区间 🔄）。

**Prevention / 预防措施**
- Keep **domain whitelist** current; staging→prod publish flow; monitor backend health (`data/13`).
  **域名白名单**常新；测试→生产发布流；监控后端（`data/13`）。

---

## #s07-pos-not-syncing-mms /  POS 不与会籍同步

**Self-check / 自查（说人话）**
- A sale at the POS doesn't appear in the MMS, or membership bought at front desk doesn't unlock in the app.
  POS 的成交不在会籍显示，或前台买的会籍 App 不解锁。
- Check the integration token / webhook status (see #s24); check "last sync time" in both systems; a network blip (see `data/11`) can stall the queue.
  查集成令牌/webhook 状态（见 #s24）；查两系统「最后同步时间」；网络闪断（`data/11`）会卡队列。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT manually edit the member's record in BOTH systems to "fix" — you'll create a divergence that breaks future sync. Fix at the source, then re-sync.
  不要两系统都手改「修」——会造成分歧破坏后续同步。源头改，再重同步。

**Vendor support script / 报修话术（准备：两系统最后同步时间 + 订单号）**
- "订单 <号> 在 POS 成功但 MMS 缺失，POS 最后同步 <时间>。请查集成/webhook 是否积压或失败。"

**Cost-impact hint / 费用影响参考**
- **¥0** (token/re-sync). Integration rebuild: **¥2,000–¥20,000** (range 🔄).
  **¥0**（令牌/重同步）。重做集成：**¥2000–¥20000**（区间 🔄）。

**Prevention / 预防措施**
- Monitor **webhook queue depth**; alert on sync lag >5 min; quarterly token sweep (#s24, `data/13`).
  监控**webhook 队列深度**；同步延迟 >5 分报警；季度令牌巡检（#s24、`data/13`）。

---

## #s08-gate-expired-valid-member /  闸机对有效会员报「过期」

**Self-check / 自查（说人话）**
- A paying member is blocked at the gate with "expired", but their MMS shows active. This is a **sync lag** between MMS and the gate controller.
  付费会员被闸机拦「过期」，但会籍显示有效。这是**会籍与闸机控制器同步延迟**。
- Check the gate's "last sync" timestamp; check whether the member's status changed recently (renewal just now). See `data/10` #C2 gate sync.
  查闸机「最后同步」时间；查会员状态是否刚变更（刚续费）。见 `data/10` #C2 闸机同步。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT disable the gate's validation "so everyone gets in" during a sync lag — that's a security/access-control breach (HI-5/physical security). Manually admit + force a sync.
  同步延迟时别为「都放进」关掉闸机校验——那是门禁/安全事件（HI-5/物理安全）。人工放行 + 强制同步。

**Vendor support script / 报修话术（准备：会员ID + 闸机最后同步时间 + MMS状态截图）**
- "会员 <ID> MMS 有效，但闸机 <编号> 报过期，闸机最后同步 <时间>。请强制同步并查 MMS→闸机链路延迟。"

**Cost-impact hint / 费用影响参考**
- **¥0** (sync). Recurring lag may need a controller/network fix: **¥0–¥3,000** (range 🔄).
  **¥0**（同步）。反复延迟或需控器/网络修：**¥0–¥3000**（区间 🔄）。

**Prevention / 预防措施**
- Gate polls MMS on a **short interval (≤60s)** + on-demand sync on renewal; off-line fail-open policy documented (HI-2 safety for egress). Link `data/10` #C2.
  闸机**短轮询（≤60s）** + 续费即时同步；离线 fail-open 策略书面化（HI-2 疏散安全）。联 `data/10` #C2。

---

## #s09-body-scan-missing-profile /  体测数据不在会员档案

**Self-check / 自查（说人话）**
- A body-composition scan finished but the numbers don't show in the member's profile.
  体测做完了，但会员档案没数据。
- Check: did the scanner upload to the right member ID? Was the device online? Did the MMS "pull" the result? (see `data/11` IoT drop, #s31).
  查：体测仪传到对的会员 ID 了吗？设备在线吗？会籍「拉取」结果了吗？（见 `data/11` IoT 掉线、#s31）

**Stop-line / 停手线（何时绝也不能动）**
- Do NOT re-enter fake numbers "to show the member something" — that's data fabrication (HI-8, HI-6 health boundary). Re-scan or retrieve the original file.
  不要编假数「给会员看」——那是造假（HI-8、HI-6 健康边界）。重测或取原文件。

**Vendor support script / 报修话术（准备：设备序列号 + 会员ID + 扫描时间）**
- "体测仪 <SN> 于 <时间> 完成，会员 <ID> 档案无数据。请确认设备上传与会籍拉取链路。"

**Cost-impact hint / 费用影响参考**
- **¥0** (re-sync). Device offline chronic: see `data/11` #n31.
  **¥0**（重同步）。设备常离线：见 `data/11` #n31。

**Prevention / 预防措施**
- Confirm scan→profile mapping; device on **IoT VLAN with stable 2.4G** (`data/11` #n31); verify after each session at busy hours.
  确认扫描→档案映射；设备放**稳定 2.4G 的 IoT VLAN**（`data/11` #n31）；高峰每场后核。

---

## #s10-report-numbers-dont-match /  两系统数字对不上（假 bug #1）

**Self-check / 自查（说人话）**
- The MMS says 120 visits, the POS says 118 sales, the app says 115 — "which is right?" Usually a **definition mismatch**, not a bug.
  会籍说 120 入场，POS 说 118 成交，App 说 115——「哪个对？」常是**定义不同**，不是 bug。
- Ask: are we counting "check-ins" vs "unique members" vs "paid visits"? Different systems count differently. Align the definition first.
  问：数的是「入场次数」还是「去重会员」还是「付费入场」？不同系统口径不同。先对齐口径。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT "adjust" one system's number to match another — that hides the real definition gap and corrupts audit trails.
  不要为「对上」去改某系统数字——掩盖真实口径差且毁审计。

**Vendor support script / 报修话术（照着念）**
- "请帮我确认各系统指标定义：<指标> 在 MMS/POS/App 分别如何计数？我们需统一口径再比对。"

**Cost-impact hint / 费用影响参考**
- **¥0** (definition alignment). BI unification if needed: see `references/18`.
  **¥0**（口径对齐）。若需 BI 统一：见 `references/18`。

**Prevention / 预防措施**
- Publish a **one-page metric dictionary** (what each number means, where sourced) in `data/20`; reconcile weekly (`data/13`).
  发**一页指标词典**（每数含义、来源）存 `data/20`；每周对账（`data/13`）。

---

## #s11-campaign-not-sending /  营销群发发不出去

**Self-check / 自查（说人话）**
- The SMS/email/WhatsApp/LINE campaign didn't send. Common: quota exhausted, consent missing, or template rejected by the platform.
  短信/邮件/WhatsApp/LINE 群发没发。常见：额度耗尽、缺同意、或平台拒模板。
- Check the channel console: "sent / failed / blocked" counts; check consent list; check template approval status (per market anti-spam, HI-7). Link `references/17`.
  查通道后台「已发/失败/拦截」；查同意名单；查模板审核状态（按市场反垃圾，HI-7）。联 `references/17`。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT buy a "no-consent bulk sender" to bypass — that violates HI-7 and anti-spam law, risks fines and channel ban.
  不要买「无同意群发器」绕过——违 HI-7 与反垃圾法，有罚款与封通道风险。

**Vendor support script / 报修话术（准备：活动ID + 失败原因 + 模板ID）**
- "活动 <ID> 未发，后台 <原因>。请确认是额度、同意缺失还是模板驳回（市场 <X> 规则）。"

**Cost-impact hint / 费用影响参考**
- Quota top-up: **¥50–¥500/mo** (range 🔄). Template rejection: **¥0** rework.
  额度补足：**¥50–¥500/月**（区间 🔄）。模板驳回：改写 **¥0**。

**Prevention / 预防措施**
- Maintain **opt-in consent ledger** (HI-7); pre-approve templates; monitor quota; multi-channel fallback (`references/17`, `data/13`).
  维护**Opt-in 同意台账**（HI-7）；模板预审；监控额度；多通道兜底（`references/17`、`data/13`）。

---

## #s12-payment-gateway-settlement-mismatch /  支付对账不平

**Self-check / 自查（说人话）**
- Gateway says settled ¥X, your MMS says ¥Y, difference ¥D. Check: pending settlements, refunds, fees, and time-zone cut-off of the settlement day.
  网关结算 ¥X，会籍 ¥Y，差 ¥D。查：待结算、退款、手续费、结算日时区切分。
- Most mismatches are timing (T+1/T+2 settlement) or gateway fee, not missing money.
  多数不平是时点（T+1/T+2 结算）或网关费，不是丢钱。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT book the difference as "loss" immediately — wait one settlement cycle; abrupt journal edits hurts audit.
  不要马上把差额记「亏损」——等一个结算周期；贸然改账伤审计。

**Vendor support script / 报修话术（准备：对账表 + 结算周期 + 差异明细）**
- "结算周期 <起止>，网关 <X> 会籍 <Y> 差 <D>。请逐笔对：待结/退款/手续费/时区切分。"

**Cost-impact hint / 费用影响参考**
- Gateway fee typically **0.3%–3.5%** per txn (range, market-dependent 🔄). Reconcile daily (`data/13`).
  网关费率通常**每笔 0.3%–3.5%**（区间，随市场 🔄）。每日对账（`data/13`）。

**Prevention / 预防措施**
- Daily **auto-reconcile** report; flag mismatch >0.5% for review; keep settlement calendar in `data/20`.
  每日**自动对账**报告；差异 >0.5% 即查；`data/20` 留结算日历。

---

## #s13-refund-stuck /  退款卡住

**Self-check / 自查（说人话）**
- A refund initiated days ago hasn't returned to the member's card/wallet. Check status: "pending at gateway" vs "rejected" vs "bank processing".
  退款发起多日未到账。查状态：「网关处理中」vs「被拒」vs「银行处理中」。
- Banks take 3–10 business days (range); gateways sometimes need manual approval for large amounts.
  银行需 3–10 工作日（区间）；网关大额有时需人工批。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT issue a second refund "to speed up" — you'll double-refund (see #s02). Track the original ticket.
  不要为「快点」再退一笔——会双退（见 #s02）。跟原工单。

**Vendor support script / 报修话术（准备：原交易号 + 退款单号 + 状态）**
- "退款 <单号> 于 <时间> 发起，状态 <X>。请推进并给预计到账时间。"

**Cost-impact hint / 费用影响参考**
- Refund **¥0** to member; gateway may keep original fee (range 🔄).
  会员侧 **¥0**；网关或留原手续费（区间 🔄）。

**Prevention / 预防措施**
- Set a **refund SLA** with the gateway in writing (see `data/14`); track all refunds in one sheet (`data/16`).
  与网关**书面约定退款 SLA**（见 `data/14`）；所有退款记一表（`data/16`）。

---

## #s14-invoice-numbering-gaps /  发票号码断号（合规红旗）

**Self-check / 自查（说人话）**
- Invoice numbers jump (e.g. 104, 106 — 105 missing). Tax authorities may see gaps as deleted/voided records.
  发票号跳号（如 104、106——缺 105）。税务可能视断号为删/废记录。
- Check: was 105 a voided invoice (should be kept as "void", not deleted)? Or did a duplicate get merged?
  查：105 是作废发票（应保留为「作废」非删除）？还是重复合并？

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT delete invoices to "fix" gaps — that's a compliance violation (tax). Void, don't delete; keep the audit trail.
  不要删发票「修」断号——那是违规（税务）。作废不删除，留审计。

**Vendor support script / 报修话术（照着念）**
- "发票号 <前后> 之间缺 <号>。请确认是作废保留还是数据问题，确保不物理删除。"

**Cost-impact hint / 费用影响参考**
- **¥0** (process). Wrong deletion could trigger tax penalty (market-specific, verify via `tools/05`).
  **¥0**（流程）。误删或触税务罚款（随市场，经 `tools/05` 核验）。

**Prevention / 预防措施**
- Configure **void-not-delete**; monthly invoice-sequence audit (`data/13`); tax-rule check via `tools/05`.
  设**作废不删除**；月发票连号审计（`data/13`）；税务规则经 `tools/05` 核验。

---

## #s15-staff-permission-error-role-change /  调岗后权限错

**Self-check / 自查（说人话）**
- After a staff role change (e.g. coach→manager), they can't do new tasks or still see old ones. Permission mapping didn't update.
  员工调岗（如教练→店长）后做不了新事或还能看旧的。权限映射没更新。
- Check the role matrix: which permissions belong to "manager" vs "coach". Was the change applied?
  查角色矩阵：「店长」vs「教练」各有哪些权限。改动生效了吗？

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT grant "admin to everyone" as a shortcut — over-permission is a data-leak path (HI-8, `references/16`). Apply least-privilege.
  不要图省事给「全员管理员」——过度授权是泄露通道（HI-8、`references/16`）。最小权限。

**Vendor support script / 报修话术（准备：员工ID + 原/新角色 + 缺/多权限）**
- "员工 <ID> 由 <旧岗> 调 <新岗>，权限未同步（缺 <X>/多 <Y>）。请按角色矩阵修正。"

**Cost-impact hint / 费用影响参考**
- **¥0** (RBAC config).
  RBAC 配置 **¥0**。

**Prevention / 预防措施**
- Maintain a **role-permission matrix** in `data/20`; review on every role change + quarterly audit (`data/13`).
  在 `data/20` 维护**角色权限矩阵**；每次调岗 + 季度审计（`data/13`）。

---

## #s16-data-export-incomplete /  切换厂商前导出不全 ⛔

**Self-check / 自查（说人话）**
- You're switching MMS vendors. The export from the old system missed members, payments, or body-scan history.
  你要换会籍系统。旧系统导出漏了会员、交易或体测历史。
- Before anything else: verify the export covers ALL entities (members, contracts, transactions, points, scan files) by row-count vs the live count.
  首要：核对导出覆盖所有实体（会员、合同、交易、积分、体测文件），按行数对比在库数。

**Stop-line / 停手线（何时绝不能再动）**
- 🛑 **NEVER terminate the old contract or cut its access before the export is verified complete and re-imported into the new system successfully.** This is the #1 cause of permanent member-data loss. Keep parallel run ≥30 days.
  🛑 **在导出核验完整、并成功导入新系统之前，绝不要终止旧合同或断其访问。** 这是会员数据永久丢失的头号原因。并行运行 ≥30 天。

**Vendor support script / 报修话术（准备：导出清单 + 行数对比 + 缺失项）**
- "导出缺 <项>，行数 <导出> vs 在库 <实际>。请补全全量导出（含 <字段>）后再终止服务。"

**Cost-impact hint / 费用影响参考**
- Export usually **¥0** (your data, HI-8). Data-recovery after termination: often **impossible / ¥5,000–¥50,000** if at all (range 🔄).
  导出常 **¥0**（你的数据，HI-8）。终止后恢复：常**不可能 / 若有则 ¥5000–¥50000**（区间 🔄）。

**Prevention / 预防措施**
- Contract a **data-export + parallel-run clause** BEFORE signing the new vendor (see `data/14` exit clause, `references/05`). Verify export at every renewal.
  签新厂商前合同写**数据导出 + 并行运行条款**（见 `data/14` 退出条款、`references/05`）。每次续约核验导出。

---

## #s17-saas-vendor-outage /  会籍 SaaS 厂商故障

**Self-check / 自查（说人话）**
- The whole MMS/app is unreachable for everyone, not just your club. Check the vendor status page (bookmarked) and social media.
  整个会籍/App 全员不可达，不只你店。查厂商状态页（书签）与社媒。
- Confirm it's not your network (see `data/11` #n01) by testing another site on the same device.
  同设备测别的站，确认不是你网（见 `data/11` #n01）。

**Stop-line / 停手线（何时绝也不能动）**
- Do NOT "fix it yourself" by changing config during a vendor outage — you'll conflict with their recovery. Wait for their all-clear.
  厂商故障时别「自己改配置修」——会和他们的恢复冲突。等他们恢复通告。

**Vendor support script / 报修话术（准备：状态页截图 + 影响范围 + 会员投诉量）**
- "状态页显示 <服务> 异常，我方 <N> 名会员受影响，营业中断。请给 ETR 与事后补偿（SLA）。"

**Cost-impact hint / 费用影响参考**
- Outage credit per SLA: **1–7 days fee** (range 🔄). No SLA = usually none.
  按 SLA 故障抵扣：**1–7 天费用**（区间 🔄）。无 SLA 常无。

**Prevention / 预防措施**
- Choose vendors **with published status page + SLA**; keep an offline check-in fallback (paper roster + manual gate release, HI-2); log outages (`data/16`).
  选**有状态页 + SLA** 的厂商；保留离线入场兜底（纸质名册 + 人工放行，HI-2）；记故障（`data/16`）。

---

## #s18-version-update-broke-workflow /  版本更新搞坏了流程

**Self-check / 自查（说人话）**
- After a vendor pushed an update, a workflow you used daily broke (button moved, field renamed, report changed).
  厂商推送更新后，你常用的流程坏了（按钮挪了、字段改名、报表变）。
- Check the vendor's release notes; often it's a UI/label change, not data loss.
  查厂商发版说明；常是界面/标签变，非丢数据。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT roll back production yourself by editing the database — wait for vendor support or a guided rollback.
  不要自己改数据库回滚生产——等厂商支持或引导回滚。

**Vendor support script / 报修话术（准备：更新版本号 + 前后截图 + 影响步骤）**
- "版本 <号> 后 <步骤> 失效，见前后截图。请给临时方案或紧急修复排期。"

**Cost-impact hint / 费用影响参考**
- **¥0** (vendor fix). Custom workaround dev: **¥500–¥5,000** (range 🔄).
  **¥0**（厂商修）。定制绕行开发：**¥500–¥5000**（区间 🔄）。

**Prevention / 预防措施**
- Opt for **staging updates** where possible; keep a one-page "current workflow" SOP in `data/20`; train staff on change.
  尽量选**灰度/测试更新**；`data/20` 留「当前流程」SOP；培训应对变更。

---

## #s19-browser-webview-compatibility /  浏览器/内核兼容

**Self-check / 自查（说人话）**
- The admin page works in Chrome but breaks in the old in-app browser or Safari. Often a webview engine too old for new JS.
  后台 Chrome 正常，旧 App 内浏览器或 Safari 坏。常是内核太旧跑不了新 JS。
- Test in the latest Chrome + the device's actual webview; check console errors.
  用最新 Chrome + 设备真实内核测；查控制台报错。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT force members to "use a computer" permanently — that's a UX failure. Push a webview/lite-page fix.
  不要永久让会员「用电脑」——那是体验失败。推内核/轻页修复。

**Vendor support script / 报修话术（准备：浏览器/版本 + 报错 + 设备型号）**
- "页面在 <浏览器/版本> 报 <错>，最新 Chrome 正常。请兼容或提供轻量页。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config). Custom lite page: **¥500–¥5,000** (range 🔄).
  配置 **¥0**。定制轻页：**¥500–¥5000**（区间 🔄）。

**Prevention / 预防措施**
- Pin a **supported-browser list**; prompt updates; test on the lowest common device quarterly.
  固化**支持的浏览器清单**；提示更新；季度在最低端设备测。

---

## #s20-printer-driver-vs-software /  打印机驱动 vs 软件扯皮

**Self-check / 自查（说人话）**
- The MMS says "printed" but nothing comes out, or it prints garbage. Decide: is it the printer (test page works?) or the software's print template?
  会籍说「已打印」却不出，或打出来乱码。判断：打印机本身（测试页行吗）还是软件打印模板？
- Print a Windows test page. If that works, the issue is the app/template, not the driver.
  打一张系统测试页。若行，是 App/模板问题，非驱动。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT reinstall the whole MMS to "fix printing" — that risks config loss. Isolate printer vs app first.
  不要为「修打印」重装整个会籍——有配置丢失风险。先隔离打印 vs App。

**Vendor support script / 报修话术（准备：测试页结果 + 报错 + 模板截图）**
- "系统测试页正常但 MMS 打印 <现象>。请查打印模板/驱动调用。"

**Cost-impact hint / 费用影响参考**
- Usually **¥0** (driver/template). New printer: **¥300–¥3,000** (range 🔄).
  常 **¥0**（驱动/模板）。新打印机：**¥300–¥3000**（区间 🔄）。

**Prevention / 预防措施**
- Keep **driver + template version** noted; assign printer a DHCP reservation (`data/11` #n15); test print at open (`data/13`).
  记**驱动+模板版本**；打印机 DHCP 保留（`data/11` #n15）；开店测打（`data/13`）。

---

## #s21-econtract-signature-invalid /  电子合同签名无效

**Self-check / 自查（说人话）**
- A member claims the e-contract signature is "invalid" / not showing. Check: did the signing session expire? Was the document completed or abandoned?
  会员说电子合同签名「无效」/不显示。查：签署会话是否过期？文档是完成还是弃签？
- Most "invalid" = session timeout or the member closed before final submit.
  多数「无效」=会话超时或会员未最终提交就关了。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT re-use a member's previously captured signature image on a new contract — that's forgery risk and may void enforceability (HI-3 prepaid/contract).
  不要在新合同复用会员旧签名图——有伪造风险且或致合同无效（HI-3 预付/合同）。

**Vendor support script / 报修话术（准备：合同ID + 签署状态 + 时间）**
- "合同 <ID> 签署状态 <X>，会员称无效。请确认是否会话超时/未最终提交，并补签流程。"

**Cost-impact hint / 费用影响参考**
- **¥0** (re-sign). E-signature platform fee: **¥0–¥3,000/yr** (range 🔄).
  **¥0**（重签）。电子签平台费：**¥0–¥3000/年**（区间 🔄）。

**Prevention / 预防措施**
- Use a **compliant e-sign vendor** with audit trail; session timeout visible to member; keep signed PDF in member file (HI-3).
  用**带审计轨迹的合规电子签**；会员可见会话超时；签后 PDF 存会员档（HI-3）。

---

## #s22-backup-restore-test-failed /  备份恢复演练失败

**Self-check / 自查（说人话）**
- You tried restoring the MMS backup to a test environment and it failed or data looked wrong. The backup is not trustworthy.
  你把会籍备份恢复到测试环境失败或数据不对。备份不可信。
- Check: backup completed fully? Wrong version? Corrupt file? Restore to the matching version.
  查：备份完整吗？版本错？文件坏？恢复到匹配版本。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT discover backup is broken ONLY during a real disaster. Test quarterly (see `data/13`). If test failed, escalate now.
  不要等真灾难才发现备份坏。季度测（`data/13`）。测失败现在就升级处理。

**Vendor support script / 报修话术（准备：备份文件信息 + 恢复报错）**
- "备份 <文件/时间> 恢复失败，报错 <X>。请协助修复备份链路并验证可恢复。"

**Cost-impact hint / 费用影响参考**
- Backup storage **¥0–¥500/mo** (range 🔄). DR rebuild if lost: **¥5,000–¥50,000+** (range 🔄).
  备份存储 **¥0–¥500/月**（区间 🔄）。若丢数据重建：**¥5000–¥50000+**（区间 🔄）。

**Prevention / 预防措施**
- **Quarterly restore drill** (`data/13`); 3-2-1 backup (3 copies, 2 media, 1 off-site); verify backup size vs live.
  **季度恢复演练**（`data/13`）；3-2-1 备份（3 份、2 介质、1 异地）；备份体积对在库。

---

## #s23-account-sharing-false-positive /  账号共享误判

**Self-check / 自查（说人话）**
- The system flagged "account sharing" (one login used by two people) but it's a false positive: member logged in on phone + front-desk kiosk, or weak session handling.
  系统标「账号共享」（一账号两人用）但是误判：会员手机 + 前台自助机同时登，或会话处理弱。
- Check login IPs/device types; if both are the member's own devices, it's normal.
  查登录 IP/设备类型；若都是会员自己设备，正常。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT auto-ban a member on a false positive — that's a churn + complaint risk. Verify before action (HI-7 respect, member trust).
  不要误判就自动封会员——流失 + 投诉风险。动作前先核实（HI-7、会员信任）。

**Vendor support script / 报修话术（准备：账号 + 登录设备/IP + 时间）**
- "账号 <ID> 被标共享，但两设备均属本人（手机+前台）。请调整判定阈值或加家庭共享白名单。"

**Cost-impact hint / 费用影响参考**
- **¥0** (threshold). Family-share feature if needed: see `references/06`.
  阈值 **¥0**。若需家庭共享功能：见 `references/06`。

**Prevention / 预防措施**
- Set **reasonable concurrent-device policy** (e.g. 2 devices); allow declared family sharing; tune detection to reduce false positives.
  设**合理同设备数**（如 2 台）；允许申报家庭共享；调检测降误判。

---

## #s24-integration-token-expired /  集成令牌过期（静默杀手）

**Self-check / 自查（说人话）**
- Syncs between systems silently stop (POS↔MMS, MMS↔gate, app↔MMS). No error shown — just stale data. The OAuth/API token expired.
  系统间同步静默停（POS↔会籍、会籍↔闸机、App↔会籍）。无报错——只是数据旧。OAuth/API 令牌过期了。
- Check "last successful sync" — if it stopped on a specific date and never resumed, it's the token (see #s07).
  查「最后成功同步」——若某日停了不再续，是令牌（见 #s07）。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT hard-code a token with no expiry monitoring — it will expire at 2am on a holiday. Monitor + auto-renew.
  不要把令牌写死又不监控过期——它会在假期凌晨 2 点过期。监控 + 自动续。

**Vendor support script / 报修话术（准备：集成名 + 最后成功同步时间 + 报错）**
- "集成 <名> 自 <时间> 起无成功同步，疑令牌过期。请指导重授权/轮换并开启到期提醒。"

**Cost-impact hint / 费用影响参考**
- **¥0** (re-auth). Chronic: use a token-vault/auto-renew: **¥0–¥2,000** (range 🔄).
  **¥0**（重授权）。反复：令牌库/自动续：**¥0–¥2000**（区间 🔄）。

**Prevention / 预防措施**
- **Quarterly token-expiry sweep** + calendar reminders 7 days before expiry (`data/13`); prefer auto-renewing credentials.
  **季度令牌过期巡检** + 到期前 7 天日历提醒（`data/13`）；优先自动续凭据。

---

## #s25-duplicate-member-records-merge /  重复会员记录合并

**Self-check / 自查（说人话）**
- The same person has two member profiles (e.g. signed up via app and again at front desk). You need to merge, keeping the active contract and history.
  同一人有两份会员档案（如 App 注册 + 前台又注册）。需合并，保留有效合同与历史。
- Identify the master record (the one with the active contract); merge the other's visits/points into it; never delete the contract.
  定主记录（有有效合同的）；把另一份的入场/积分并过去；绝不删合同。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT delete one record outright — you'll lose the contract or payment history (audit/tax). Merge, don't drop.
  不要直接删一条——会丢合同或交易史（审计/税务）。合并不删。

**Vendor support script / 报修话术（准备：两记录ID + 主记录判定 + 需合并字段）**
- "会员 <姓名> 有 <ID-A>/<ID-B> 两档，主为 <A>（有效合同）。请合并 B 的 <字段> 至 A，保留合同。"

**Cost-impact hint / 费用影响参考**
- **¥0** (merge tool). Messy DB cleanup if chronic: **¥2,000–¥20,000** (range 🔄).
  合并 **¥0**。若库常年乱：清理 **¥2000–¥20000**（区间 🔄）。

**Prevention / 预防措施**
- Enforce **unique identity at signup** (phone/member no. dedup); train front desk to search before creating (`data/13`).
  注册即**唯一身份去重**（手机/会员号）；前台建档前先查（`data/13`）。

---

## #s26-gdpr-pipi-deletion-request /  删数据请求（GDPR/PIPL 类）

**Self-check / 自查（说人话）**
- A member asks to delete their personal data ("right to erasure"). You must honor it per market law (e.g. PIPL China, GDPR EU) but keep what law requires (tax records).
  会员要求删除个人数据（「被遗忘权」）。按市场法（如中国 PIPL、欧盟 GDPR）须履行，但法定需留的（税务记录）要留。
- Separate "delete profile" from "retain legal records" — you can anonymize, not fully destroy, where law demands.
  区分「删档案」与「留法定记录」——法定处可匿名化而非全销毁。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT delete everything including tax/contract records — that breaches retention law. Do NOT refuse lawful deletion either. Anonymize the right parts.
  不要连税务/合同记录一起删——违留存法。也不要非法拒绝删除。对的部分匿名化。

**Vendor support script / 报修话术（准备：会员ID + 请求日期 + 适用法域）**
- "会员 <ID> 依 <法域> 要求删除个人数据。请协助：匿名化档案，保留法定留存部分，并出处理证明。"

**Cost-impact hint / 费用影响参考**
- **¥0** (process). Wrongful deletion/retention fine: market-specific, large (verify `tools/05`).
  **¥0**（流程）。错删/错留罚款：随市场，数额巨大（经 `tools/05` 核验）。

**Prevention / 预防措施**
- Build **data-retention + erasure workflow** per market (HI-1 for biometrics); document in `references/10/11`; quarterly review (`data/13`).
  按市场建**留存 + 删除工作流**（HI-1 生物识别）；记 `references/10/11`；季度复核（`data/13`）。

---

## #s27-test-vs-production-confusion /  测试环境与生产搞混

**Self-check / 自查（说人话）**
- Someone "tested" in production (e.g. sent a real campaign, edited a live price) thinking it was the test environment.
  有人在生产「测试」（如发了真活动、改了真价格），以为在测试环境。
- Check environment banners/URLs: is the URL "test." or "sandbox"? Was the action on live data?
  查环境标识/URL：是「test.」或「sandbox」吗？动作落在真数据上了吗？

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT "test in production during quiet hours" as a habit — one wrong click hits real members. Always use the sandbox.
  不要养成「 quiet 时在生产测」——错一点就伤真会员。永远用沙箱。

**Vendor support script / 报修话术（准备：环境 + 动作 + 影响范围）**
- "误在生产 <环境> 执行 <动作>，影响 <范围>。请协助回滚/纠正。"

**Cost-impact hint / 费用影响参考**
- **¥0**–rollback cost varies (range 🔄).
  **¥0**–回滚成本不定（区间 🔄）。

**Prevention / 预防措施**
- **Distinct colors/URLs** for test vs prod; separate logins; "danger: production" banner; train staff (`data/13`).
  测试/生产**配色/URL 区分**；分登录；生产标「危险」横幅；培训（`data/13`）。

---

## #s28-intern-deleted-class-template /  实习生存课模板

**Self-check / 自查（说人话）**
- A class template (used for weekly scheduling) was deleted by mistake. Check if it's soft-deleted (recoverable) or hard-deleted.
  课模板（用于周排课）被误删。查是软删（可恢复）还是硬删。
- Most MMS have a trash/recycle; restore from there before panicking.
  多数会籍有回收站；先那恢复别慌。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT rebuild the whole week manually before checking the trash — you may create duplicates. Restore the template first.
  查回收站前别手动重排整周——会造重复。先恢复模板。

**Vendor support script / 报修话术（准备：模板名 + 删除时间 + 是否软删）**
- "课模板 <名> 于 <时间> 被删，请确认软删并协助从回收站恢复。"

**Cost-impact hint / 费用影响参考**
- **¥0** (restore). Hard-delete recovery: **¥0–¥5,000** (range 🔄).
  **¥0**（恢复）。硬删恢复：**¥0–¥5000**（区间 🔄）。

**Prevention / 预防措施**
- **Role-based delete limits** (intern = view/limited); weekly template backup; trash-retention policy (`data/13`, #s15).
  **按角色限删**（实习生=查看/受限）；周模板备份；回收站留存策略（`data/13`、#s15）。

---

## #s29-api-rate-limit-promo /  促销时 API 限流

**Self-check / 自查（说人话）**
- During a big promo, check-ins/bookings started failing with "429 Too Many Requests". The API hit its rate limit.
  大促时入场/约课开始失败报「429 太多请求」。API 触限流。
- Check the vendor's rate-limit tier; promo traffic exceeded it.
  查厂商限流档位；促销流量超了。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT retry in a tight loop on 429 — that deepens the limit. Back off (wait, then retry) and throttle.
  429 不要紧循环重试——会更深触限。退避（等再试）并限流。

**Vendor support script / 报修话术（准备：时间点 + 429 量 + 促销规模）**
- "促销 <时间> 出现大量 429，峰值 <QPS>。请临时提额或确认排队策略。"

**Cost-impact hint / 费用影响参考**
- Limit raise: **¥0–¥2,000/mo** (range 🔄). Lost promo sales if unhandled: variable.
  提额：**¥0–¥2000/月**（区间 🔄）。不处理丢促销：不定。

**Prevention / 预防措施**
- Pre-book **rate-limit headroom** before promos; client-side throttle + backoff; load-test (`references/18`).
  大促前预购**限流余量**；客户端限流+退避；压测（`references/18`）。

---

## #s30-webhook-queue-backlog /  故障后 webhook 队列积压

**Self-check / 自查（说人话）**
- After an outage, data between systems is stale even though both are "up" — the webhook queue is backed up.
  故障后两系统数据旧，尽管都「在」。webhook 队列积压。
- Check queue depth/age; old events may need replay, not just new ones.
  查队列深度/年龄；旧事件或需重放，非只新事件。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT "clear the queue" to make the number look good — you'll drop real events. Replay or drain properly.
  不要「清队列」让数字好看——会丢真事件。重放或正确排空。

**Vendor support script / 报修话术（准备：队列深度 + 最旧事件时间 + 系统对）**
- "系统 <A>→<B> webhook 积压 <N> 条，最旧 <时间>。请协助重放/排空且不丢事件。"

**Cost-impact hint / 费用影响参考**
- **¥0** (replay). Architecture fix if chronic: see `references/18`.
  **¥0**（重放）。若常发需架构修：见 `references/18`。

**Prevention / 预防措施**
- Monitor **queue depth + age**; alert on backlog; idempotent consumers so replay is safe (#s07, #s24).
  监控**队列深度+年龄**；积压报警；消费幂等以便安全重放（#s07、#s24）。

---

## #s31-offline-mode-conflict-reconnect /  离线模式重连冲突

**Self-check / 自查（说人话）**
- The club ran in offline mode (gate/MMS local cache), then reconnected and some records conflict (two check-ins, a sale duplicated).
  场馆离线运行（闸机/会籍本地缓存），重连后记录冲突（双入场、重复成交）。
- Check conflict-resolution: does the system keep both or merge? Usually last-write-wins drops one.
  查冲突解决：系统是都留还是合并？常「后写覆盖」丢一条。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT manually delete "the duplicate" without logging — you may erase the real one. Let the merge rule run, then verify.
  不要不记录就手删「重复」——可能删真的。让合并规则跑，再核。

**Vendor support script / 报修话术（准备：冲突记录 + 离线时段 + 合并结果）**
- "离线 <时段> 后重连，<记录> 冲突。请确认合并规则并补正差异。"

**Cost-impact hint / 费用影响参考**
- **¥0** (merge). Recurring: offline-mode design review (see `data/10` gate, `references/08`).
  **¥0**（合并）。反复：离线模式设计复核（见 `data/10` 闸机、`references/08`）。

**Prevention / 预防措施**
- Design **offline-first with idempotent sync** + conflict log; test reconnect drill (`data/13`); keep offline window short.
  设计**离线优先 + 幂等同步** + 冲突日志；测重连演练（`data/13`）；离线窗口要短。

---

## #s32-franchise-sees-hq-data /  加盟店看到总部数据（隔离失守）

**Self-check / 自查（说人话）**
- A franchise/branch store can see another store's or HQ's member data. Permission isolation failed — a **security incident**, not a bug.
  加盟/分店能看到别店或总部的会员数据。权限隔离失败——是**安全事件**非 bug。
- Confirm scope: which stores' data is visible? Is it read-only or editable? Log it immediately.
  确认范围：能看到哪些店数据？只读还是可改？立刻记录。

**Stop-line / 停手线（何时绝不能再动）**
- 🛑 Treat as a **security incident**: isolate the account, preserve logs, notify the data-protection owner. Do NOT let the franchisee keep browsing while you "look into it" (HI-8, `references/16`).
  🛑 视为**安全事件**：隔离账号、留日志、报数据保护负责人。调查期间不要让加盟商继续浏览（HI-8、`references/16`）。

**Vendor support script / 报修话术（准备：账号 + 可见范围 + 时间 + 日志）**
- "加盟店 <ID> 越权见 <范围> 数据，疑似隔离失效。请紧急收口权限并排查根因，我们按安全事件处理。"

**Cost-impact hint / 费用影响参考**
- **¥0** (fix) but breach may trigger regulatory penalty (market-specific, verify `tools/05`).
  **¥0**（修复）但泄露或触监管罚款（随市场，经 `tools/05` 核验）。

**Prevention / 预防措施**
- Enforce **per-tenant data isolation** + least-privilege; quarterly permission audit (`data/13`); incident runbook (`references/16`).
  强制**租户间数据隔离** + 最小权限；季度权限审计（`data/13`）；事件手册（`references/16`）。

---

## #s33-wrong-market-currency-tax /  币种/税率设错市场

**Self-check / 自查（说人话）**
- A club in Market A shows prices/tax of Market B (e.g. a regional chain template copied wrong). Members see wrong currency or tax.
  A 市场店显示 B 市场价/税（如区域连锁模板拷错）。会员见错币种或税。
- Check the club's locale/currency/tax-profile setting; compare to the correct market baseline.
  查该店 locale/币种/税档；对比正确市场基线。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT change currency/tax live during open hours on a running system — it corrupts historical transactions. Correct via a config change + restate.
  营业时间不要在生产直接改币种/税——毁历史交易。用配置改 + 重述。

**Vendor support script / 报修话术（准备：店ID + 当前/应有币种税档）**
- "店 <ID> 币种/税档误设为 <X>，应为 <Y>。请协助切换并核对历史交易口径。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config). Wrong tax filing risk: market-specific (verify `tools/05`).
  配置 **¥0**。错税申报风险：随市场（经 `tools/05` 核验）。

**Prevention / 预防措施**
- Per-club **locale/currency/tax profile** locked at setup; template copy guarded; monthly check (`data/13`).
  每店**locale/币种/税档**设立即锁；模板复制加校验；月核（`data/13`）。

---

## #s34-ai-bot-answering-wrong /  AI 机器人答错（熔断）

**Self-check / 自查（说人话）**
- Your AI chatbot gives wrong answers (wrong price, wrong policy, hallucinated class). Members are misled. This is an HI-6/HI-2 risk — the bot must not mislead on health/money.
  AI 客服答错（错价、错政策、编造课程）。会员被误导。这是 HI-6/HI-2 风险——机器人不得在健康/金钱上误导。
- Confirm the error type: factual (wrong data) vs harmful (health/medical claim). Harmful = immediate kill-switch.
  确认错误类型：事实错（数据错）还是有害（健康/医疗断言）。有害=立即熔断。

**Stop-line / 停手线（何时绝不能再动）**
- 🛑 If the bot gives **health/medical or safety advice**, or clearly wrong financial info, **activate the kill-switch immediately** and route to a human. Never let a wrong AI answer stand (HI-6 refer-to-human, HI-2 safety).
  🛑 若机器人给**健康/医疗或安全建议**，或明显错误的财务信息，**立即熔断**转人工。绝不让错的 AI 答案留着（HI-6 转人、HI-2 安全）。

**Vendor support script / 报修话术（准备：错误对话截图 + 类型 + 影响会员数）**
- "AI 客服于 <时间> 对会员 <ID> 给出 <错误类型> 回答（截图）。请立即熔断并转人工，排查知识库/检索源。"

**Cost-impact hint / 费用影响参考**
- **¥0** (kill-switch). Wrong-answer liability: varies; keep human fallback (HI-2). Bot platform fee **¥0–¥5,000/mo** (range 🔄).
  **¥0**（熔断）。答错责任：不定；保留人工兜底（HI-2）。机器人平台费 **¥0–¥5000/月**（区间 🔄）。

**Prevention / 预防措施**
- Build a **kill-switch + human fallback** by default (HI-6/HI-2); ground the bot on verified knowledge; log + review wrong answers weekly; never let it diagnose health (HI-6).
  默认建**熔断 + 人工兜底**（HI-6/HI-2）；机器人基于已核实知识；周审错误答案；绝不诊断健康（HI-6）。

---

## #s35-mms-slow-dashboard /  会籍后台慢

**Self-check / 自查（说人话）**
- The MMS dashboard loads slowly but other sites are fine. Could be vendor server load, your browser, or a huge unfiltered report query.
  会籍后台慢但别的站正常。可能厂商服务器负载、你浏览器、或巨大未筛选报表查询。
- Try another browser/incognito; check if it's only at month-end (big report). Compare with a colleague.
  换浏览器/无痕；查是否仅月末（大报表）慢；与同事比对。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT run a giant unscheduled export during peak hours — it hammers the shared server for all clubs on that vendor.
  高峰不要跑巨大非计划导出——会拖垮该厂商所有店共用的服务器。

**Vendor support script / 报修话术（准备：时段 + 操作 + 同事对比）**
- "后台 <操作> 于 <时段> 慢，其他站正常。请查服务端负载或我们账号资源。"

**Cost-impact hint / 费用影响参考**
- **¥0** (vendor). Upgrade tier if chronic: **¥200–¥2,000/mo** (range 🔄).
  **¥0**（厂商）。若常发升档：**¥200–¥2000/月**（区间 🔄）。

**Prevention / 预防措施**
- Schedule heavy reports off-peak; clear cache; monitor; choose vendor with headroom (`references/06`).
  重报表排错峰；清缓存；监控；选有余量厂商（`references/06`）。

---

## #s36-member-checkin-duplicate /  会员重复入场

**Self-check / 自查（说人话）**
- A member appears checked in twice for one visit (double count). Usually a tap-twice or a sync replay (see #s31).
  会员一次入场计了两次（重复计数）。常是连刷两次或同步重放（见 #s31）。
- Check the check-in log timestamps; two entries seconds apart = accidental double tap.
  查入场日志时间；相隔几秒两笔=误连刷。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT silently delete one without a note — that hides a possible gate/sync bug. Log and root-cause.
  不要无记录静删一条——掩盖可能的闸机/同步 bug。记录并查根因。

**Vendor support script / 报修话术（准备：会员ID + 两笔时间 + 闸机编号）**
- "会员 <ID> <时间> 在闸机 <号> 重复入场，疑似连刷/重放。请去重并查根因。"

**Cost-impact hint / 费用影响参考**
- **¥0** (dedup). Recurring: gate/sync fix (#s08, #s31).
  **¥0**（去重）。反复：闸机/同步修（#s08、#s31）。

**Prevention / 预防措施**
- Add a **short debounce** (ignore 2nd tap within 30s) at the gate; reconcile visits daily (`data/13`).
  闸机加**短防抖**（30 秒内忽略二次）；每日核入场（`data/13`）。

---

## #s37-coupon-code-invalid /  优惠券码无效

**Self-check / 自查（说人话）**
- A member's promo code says "invalid" at checkout though it should work. Check: expired? min-spend not met? already used? wrong club?
  会员优惠码结账报「无效」但应可用。查：过期？未达门槛？已用？错店？
- Read the coupon's rules in the MMS; compare to the member's basket.
  读会籍里券规则；对比会员购物车。

**Stop-line / 停手线（何时绝也不再动）**
- Do NOT manually discount "to make the member happy" without logging a reason — that hurts margin tracking. Log the override.
  不要为「哄会员」手动打折不记因——伤毛利追踪。记 override 原因。

**Vendor support script / 报修话术（准备：券码 + 规则 + 购物车）**
- "券 <码> 报无效，规则 <X>，购物车 <Y>。请确认是过期/门槛/已用/错店。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config). Promo abuse if loose: see `references/19`.
  配置 **¥0**。若宽松致薅羊毛：见 `references/19`。

**Prevention / 预防措施**
- Clear **coupon rules + validity**; train front desk on override logging; monitor redemption (`data/13`, `references/19`).
  清晰**券规则+有效期**；培训前台 override 记录；监控核销（`data/13`、`references/19`）。

---

## #s38-loyalty-points-missing /  积分丢失

**Self-check / 自查（说人话）**
- A member's loyalty points didn't credit after a purchase or class. Check: did the earning rule fire? Was the member in an excluded plan?
  会员消费/上课后积分没到。查：积分规则触发了吗？会员是否在不计分区？
- Check the points log for that member; compare to the transaction that should have earned.
  查该会员积分日志；对比应得的那笔交易。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT hand-add points arbitrarily — that breaks the earning model and invites abuse. Credit only with a traced reason.
  不要随意手加积分——破坏积分模型且招滥用。只凭可溯原因补。

**Vendor support script / 报修话术（准备：会员ID + 交易号 + 应得规则）**
- "会员 <ID> 交易 <号> 未得积分，规则应 <X>。请查规则触发并补正。"

**Cost-impact hint / 费用影响参考**
- **¥0** (re-credit). Points-fraud if loose: see `references/19`.
  **¥0**（补记）。若宽松致积分欺诈：见 `references/19`。

**Prevention / 预防措施**
- Test **earning rules** after any change; reconcile points monthly; log manual credits (`data/13`).
  任何改动后测**积分规则**；月核积分；手补记录（`data/13`）。

---

## #s39-qr-code-not-scanned-gate /  二维码闸机扫不开

**Self-check / 自查（说人话）**
- A member's QR (in app) won't scan at the gate — screen too dim, QR expired, or camera dirty.
  会员 App 二维码闸机扫不开——屏太暗、二维码过期、或摄像头脏。
- Try brighter screen / rescan / another member's QR to isolate (member phone vs gate camera).
  试调亮屏/重扫/换会员二维码隔离（会员手机 vs 闸机摄像头）。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT disable QR validation "so it always opens" — that lets anyone in (HI-5/access). Keep validation; clean camera; extend QR TTL.
  不要为「永远开」关掉二维码校验——谁都能进（HI-5/门禁）。保留校验；擦摄像头；延长 QR 有效期。

**Vendor support script / 报修话术（准备：闸机编号 + 现象 + 隔离结果）**
- "闸机 <号> 扫不开 QR，疑似 <屏暗/过期/摄像头脏>。请延长 TTL 并排查摄像头。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config/clean). Camera swap: **¥200–¥1,500** (range 🔄).
  配置/清洁 **¥0**。换摄像头：**¥200–¥1500**（区间 🔄）。

**Prevention / 预防措施**
- Set **QR TTL ≥ 30s**; weekly camera clean; offline fallback (manual admit, HI-2) (`data/13`, #s08).
  设**QR 有效期 ≥30 秒**；周擦摄像头；离线兜底（人工放行，HI-2）（`data/13`、#s08）。

---

## #s40-crm-duplicate-campaign-sent /  CRM 重复群发

**Self-check / 自查（说人话）**
- The same campaign hit members twice. Check: was it scheduled twice, or did a retry resend?
  同一活动发给会员两次。查：排了两次，还是重试重发？
- Check the campaign send log: two send jobs or one job double-delivered?
  查群发日志：两个发送任务，还是一个任务双投？

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT "send a third apology blast" without checking — you'll annoy more. Diagnose first, then a single measured message (HI-7 respect).
  不要不查就「再发第三封道歉」——更烦。先诊断，再发一封克制说明（HI-7 尊重）。

**Vendor support script / 报修话术（准备：活动ID + 两次发送记录）**
- "活动 <ID> 重复发送，日志见 <两次记录>。请查是重复排程还是重试重投，并防再发。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config). Channel fatigue hurts deliverability (see `references/17`).
  配置 **¥0**。通道疲劳伤送达（见 `references/17`）。

**Prevention / 预防措施**
- **Dedupe before send** + send-idempotency; pre-send preview to a test list (`data/13`, `references/17`).
  发送前**去重** + 发送幂等；发前先发测试名单（`data/13`、`references/17`）。

---

## #s41-mobile-app-crash-on-launch /  App 一开就崩

**Self-check / 自查（说人话）**
- The member app crashes immediately on open. Usually an OS-update incompatibility or a bad app release.
  App 一开就崩。常是系统更新不兼容或 App 发版坏。
- Check app store for an update; try another phone; check the vendor's status for a known bad release.
  查应用商店更新；换手机试；查厂商状态是否已知坏版。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT push a rushed hotfix to production during peak without testing — you may make it worse. Staged rollout + test first.
  高峰不要未测就推热修生产——可能更糟。灰度 + 先测。

**Vendor support script / 报修话术（准备：App 版本 + 手机型号/系统 + 崩溃日志）**
- "App <版本> 在 <机型/系统> 启动即崩，日志 <X>。请确认是否已知坏版并给修复排期。"

**Cost-impact hint / 费用影响参考**
- **¥0** (vendor fix). Custom app maint: **¥1,000–¥10,000/mo** (range 🔄).
  **¥0**（厂商修）。定制 App 维护：**¥1000–¥10000/月**（区间 🔄）。

**Prevention / 预防措施**
- **Staged release** + crash-monitoring; keep a lite web app as fallback (`references/06`).
  **灰度发布** + 崩溃监控；留轻量网页版兜底（`references/06`）。

---

## #s42-wearable-data-not-syncing /  手环数据不同步

**Self-check / 自查（说人话）**
- A member's wearable (watch/band) steps/HR don't appear in the club app. Check Bluetooth/onboarding + the wearable vendor's API link.
  会员手环步数/心率不在 club App 显示。查蓝牙/绑定 + 手环厂商 API 链路。
- Confirm the wearable is paired in the club app and the wearable vendor account is linked.
  确认手环在 club App 已配对、且手环厂商账号已关联。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT store raw health data beyond need — minimize (HI-8, HI-1 for health). Sync only consented metrics.
  不要超需存原始健康数据——最小化（HI-8、HI-1 健康）。只同步已同意指标。

**Vendor support script / 报修话术（准备：手环型号 + 关联状态 + 错误）**
- "手环 <型号> 与俱乐部 App 关联 <状态>，数据不同步，报 <错>。请查 API 链路。"

**Cost-impact hint / 费用影响参考**
- **¥0** (re-link). Wearable integration build: **¥2,000–¥20,000** (range 🔄).
  **¥0**（重关联）。手环集成开发：**¥2000–¥20000**（区间 🔄）。

**Prevention / 预防措施**
- Document **supported wearables**; consent-gated sync; minimal health fields (HI-8); test on onboarding (`data/13`).
  记**支持手环**；同意门控同步；最小健康字段（HI-8）；绑定即测（`data/13`）。

---

## #s43-survey-feedback-not-saved /  满意度调查没保存

**Self-check / 自查（说人话）**
- A member submitted feedback but it's not in the system. Check: did the form actually submit (network drop mid-submit, see `data/11`) or save to a different module?
  会员提交了反馈但系统没有。查：表单真提交了（提交中网络断，见 `data/11`）还是存到别的模块？
- Check the submissions log / spam filter; a keyword may have been filtered.
  查提交日志/垃圾过滤；某关键词或被滤。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT discard member feedback as "lost" without a search — it's voice-of-customer gold. Search broadly first.
  不要不搜就当「丢了」扔掉会员反馈——那是客户之声金矿。先广搜。

**Vendor support script / 报修话术（准备：会员ID + 提交时间 + 网络状态）**
- "会员 <ID> <时间> 提交反馈未入库，当时网络 <状态>。请查提交链路/过滤。"

**Cost-impact hint / 费用影响参考**
- **¥0** (retrieve). Feedback system build: see `references/19`.
  **¥0**（找回）。反馈系统建设：见 `references/19`。

**Prevention / 预防措施**
- Confirm **submit success** UI + server-side save + retry on network drop (`data/11`); weekly feedback review (`data/13`).
  确认**提交成功**界面 + 服务端保存 + 断网重试（`data/11`）；周审反馈（`data/13`）。

---

## #s44-multi-language-mismatch /  多语言显示错乱

**Self-check / 自查（说人话）**
- The app/portal shows mixed languages (e.g. Chinese labels in an English-market club) or wrong locale. Default language setting is off.
  App/门户语言混排（如英文市场店现中文标签）或 locale 错。默认语言设置错。
- Check the club's default-language setting and the member's app locale; compare.
  查该店默认语言设置与会员 App locale；对比。

**Stop-line / 停手线（何时绝不能再动）**
- Do NOT hard-set one language globally for a multi-market chain — each club needs its own locale (market fit, Iron Law 1).
  不要为多市场连锁全局硬设一种语言——每店需各自 locale（市场适配，铁律1）。

**Vendor support script / 报修话术（准备：店ID + 当前/应设语言）**
- "店 <ID> 默认语言误为 <X>，应为 <Y>。请按店设 locale，勿全局覆盖。"

**Cost-impact hint / 费用影响参考**
- **¥0** (config). Localization build: **¥2,000–¥20,000** (range 🔄).
  配置 **¥0**。本地化建设：**¥2000–¥20000**（区间 🔄）。

**Prevention / 预防措施**
- **Per-club locale** locked at setup; member-app respects device locale; monthly check (`data/13`, Iron Law 1).
  **每店 locale** 设立即锁；会员 App 跟随设备 locale；月核（`data/13`、铁律1）。

---

## G13 Tri-Perspective Note / G13 三视角覆盖说明

**Architect (架构师视角)**: Software faults span Clusters B/N/M. Each five-segment entry is traceable to a vendor, an integration layer (`references/18`) or a messaging rule (`references/17`). Stop-lines enforce HI-2 (safety), HI-6 (no diagnosis), HI-7 (consent), HI-8 (minimization/isolation) and the Iron-Law-1 market fit. #s16 (data export) and #s32 (isolation breach) are hard safety/compliance gates.
**架构师视角**：软件故障跨 B/N/M 集群。每条五段式可溯源到厂商、集成层（`references/18`）或消息规则（`references/17`）。停手线落实 HI-2（安全）、HI-6（不诊断）、HI-7（同意）、HI-8（最小化/隔离）与铁律1 市场适配。#s16（数据导出）与 #s32（隔离失守）是安全/合规硬闸。

**Operator (运营者视角)**: The five segments give the front desk a verbatim script and a "what to prepare" list (logs/screenshots) so a non-IT person can open a useful ticket in minutes. Cost-impact is directional so the owner can prioritize. #s16's STOP-LINE protects against the costliest mistake: losing all member data at vendor switch.
**运营者视角**：五段式给前台「照着念」的话术与「准备什么」（日志/截图），让非 IT 也能几分钟开有效工单。费用影响为方向性，便于老板排优先级。#s16 的停手线防最贵错误：换厂商时丢光会员数据。

**Member (会员视角)**: Wrong charges (#s02), denied entry (#s08), bad AI answers (#s34), and privacy leaks (#s32, #s26) are member-trust events. The library keeps the member informed with honest timelines and protects their data and consent (HI-7/HI-8), with human fallback always available (HI-2/HI-6).
**会员视角**：错扣（#s02）、被拦（#s08）、AI 答错（#s34）、隐私泄露（#s32、#s26）都是会员信任事件。本库让会员得到诚实时限告知，并保护其数据与同意（HI-7/HI-8），且始终有人工兜底（HI-2/HI-6）。

---

*Legal Notice / 法律声明 · Disclaimer / 免责声明 · Friendly Reminder / 温馨提示 · Author / 作者信息 — see SKILL.md output block. / 见 SKILL.md 输出规范块。*
