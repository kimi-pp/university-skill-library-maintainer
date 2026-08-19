# 11 · POS & Payments Implementation / 收银与支付实施模板

> **Cluster / 集群**: B (Software) + C (Hardware C7) · Template / 模板 · System-Building tier (FDMM L1→L2)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Payment-method matrix, acquirer terms & fapiao rules re-verify every 90 days via `tools/04`; rates are ranges, not quotes.
> **Cross-references / 交叉引用**: `data/07-apac-regional-differences.md#payment-method-landscape` · `references/07-hardware-landscape-and-vendors.md` (C7 POS) · `references/08-network-and-infrastructure.md` (dual-ISP) · `data/21-anti-pattern-library.md#ap-025-bnpl-chargeback-surprise` · `tools/05-regulation-traceability-verification.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用（FDMM 闸门）

**Purpose / 用途**: A fill-in implementation plan for front-desk POS and the payment stack (terminal, acquirer/gateway, settlement, reconciliation, receipts).
**用途 / 中文**：填入式实施计划，覆盖前台收银与支付栈（终端、收单/网关、结算、对账、小票）。

**When to use / 适用场景**:
- Any club taking money (even a tiny one) needs a clean till — L1→L2. / 任何收钱场馆都需干净收银——L1→L2。
- You are opening a new club or replacing a cash-only / manual process. / 新店开业或更换现金/手工收银。
- **FDMM gate / 闸门**: Prepaid/stored-value advice must not breach fund-supervision & consumer-protection rules (HI-3) — verify via `tools/05` before selling stored value. / 储值建议不得违反资金监管与消保法（HI-3）——售储值前经 `tools/05` 核验。
- **Resilience gate / 韧性闸门**: payment must survive an ISP outage — dual-ISP is mandatory (`references/08`). / 支付须扛得住断网——双 ISP 必配（`references/08`）。

---

## ② Prerequisites checklist / 前置清单

- [ ] Legal entity registered in each market; business license for payments. / 各市场法律主体已注册；支付营业资质。
- [ ] Acquirer / payment gateway shortlisted per market (≥2 for redundancy). / 各市场收单/网关已短列（≥2 家冗余）。
- [ ] MMS chosen to post sales to member ledger (`templates/09`). / 已选 MMS 入账会员台账。
- [ ] Accounting setup with deferred-revenue tracking (prepaid clubs). / 财务已设递延收入跟踪（预售馆）。
- [ ] Dual-ISP ordered (fiber + 5G) — `references/08`. / 双 ISP（光纤+5G）已订——`references/08`。
- [ ] Receipt/fapiao field list per market confirmed (🔄 `tools/04`). / 各市场小票/发票字段清单已确认。

---

## ③ The template / 模板正文

### 3.1 Payment-method matrix per market (link `data/07`) / 分市场支付方式矩阵

> **What good looks like / 合格标准**: every local dominant method is accepted; at least one redundant rails per market. / 每个本地主流方式都接；每市场至少一条冗余通道。
> **Red flag / 红旗**: accepting only one method in a market where locals rarely use it → checkout drop-off. / 在本地少用某方式的市场只接这一种 → 结账流失。

| Market / 市场 | Dominant methods / 主流方式 | Backup rails / 备用通道 | Regulatory note (🔄) / 监管注记 |
|---|---|---|---|
| China 大陆 | Alipay, WeChat Pay, UnionPay | E-bank / 网银 | Prepaid fund supervision / 预付资金监管 |
| Hong Kong (China) 中国香港 | Octopus, FPS, AlipayHK | UnionPay | SFC/ customs / 海关消保 |
| Japan 日本 | PayPay, Rakuten Pay, credit | LINE Pay | 預備金 rule / 准备金规则 |
| Korea 韩国 | KakaoPay, NaverPay, card | Samsung Pay | 電子金融法 |
| Singapore 新加坡 | PayNow, GrabPay, card | NETS | MAS e-payments |
| Australia 澳新 | EFTPOS, Apple/Google Pay | Bank transfer | ASIC / AU reg |
| India 印度 | UPI (GPay/PhonePe), cards | Paytm | RBI prepaid |
| SEA 东南亚 | GrabPay, ShopeePay, QRIS | Cards | Per-market / 分市场 |

:::dynamic-hook topic="apac-payment-method-share-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07 QR/wallet share is rising across APAC; exact dominant method per market shifts — verify current share via tools/04 before finalising the matrix.
截至 2026-07 亚太扫码/钱包占比上升；各市场主导方式会变——定矩阵前经 tools/04 核验。
:::

### 3.2 Acquirer / gateway application checklist / 收单/网关申请清单

- [ ] MID (merchant ID) approved per legal entity. / 各主体 MID 已批。
- [ ] Settlement currency & account confirmed. / 结算币种与账户确认。
- [ ] API docs + webhook spec with idempotency key received. / 已收 API 文档+带幂等键 webhook 规范。
- [ ] PCI-DSS / local security attestation scope understood. / 已知 PCI-DSS/本地安全认证范围。
- [ ] Refund & chargeback procedure + fees documented. / 退款与拒付流程+费用已存档。
- [ ] Uptime SLA & support hours in writing. / 在线 SLA 与支持时段书面。

### 3.3 Settlement & reconciliation design (T+n mapping) / 结算与对账设计（T+n 映射）

> **Rule / 规则**: Map every tender to its settlement lag; reconcile daily, not monthly. / 每种支付方式映射到结算延迟；日对账而非月对账。

| Tender / 支付方式 | Settlement lag / 结算延迟 | Reconcile by / 对账方式 | Owner / 负责人 |
|---|---|---|---|
| Alipay / WeChat | T+1 | Auto vs MMS ledger | Finance / 财务 |
| Card (acquirer) | T+2 ~ T+3 | Batch file | Finance |
| Bank transfer | T+0 ~ T+1 | Bank feed | Finance |
| Cash | Same day | Till count | Front desk |
| BNPL (if used) | T+3 ~ T+7 | Portal report | Finance |

> **Red flag / 红旗**: see `data/21#ap-038-deferred-no-reconcile` — selling prepaid but never reconciling deferred revenue hides insolvency. / 售预售却不对账递延收入，会掩盖资不抵债（见锚点）。

### 3.4 Receipt / fapiao compliance fields (🔄) / 小票/发票合规字段

:::dynamic-hook topic="apac-receipt-fapiao-fields-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07: China requires fapiao-capable fields (tax ID, itemised goods); Japan needs consumption-tax breakdown; AU needs GST; KR needs cash-receipt. Verify exact field set per market via tools/04.
截至 2026-07：中国需发票字段（税号、明细）；日本需消费税拆分；澳需 GST；韩需现金收据。各市场字段经 tools/04 核验。
:::

- [ ] Club legal name + tax ID. / 场馆法定名称+税号。
- [ ] Transaction no., date/time, tender type. / 交易号、日期时间、支付方式。
- [ ] Itemised line items + amount + tax. / 明细行+金额+税。
- [ ] Refund / void clearly marked. / 退款/作废清晰标注。

### 3.5 Failover plan (dual-ISP) / 故障转移计划（双 ISP）

> **Rule / 规则**: Payment terminal must fail over to backup ISP with no manual rebuild. / 支付终端须自动切备用 ISP，无需手动重建。

- [ ] Dual ISP: fiber primary + 5G/4G backup (`references/08-network-and-infrastructure.md`). / 双 ISP：光纤主+5G/4G 备。
- [ ] Terminal has offline mode: queue sales, sync on reconnect. / 终端离线模式：排队销售，重连同步。
- [ ] One firewall, three VLANs (staff / guest / payment-IoT). / 一台防火墙、三 VLAN（员工/访客/支付IoT）。
- [ ] Daily automated backup of transaction log (3-2-1). / 交易流水日自动备份（3-2-1）。

### 3.6 UAT script (refund / partial / chargeback) / UAT 脚本（退款/部分/拒付）

- [ ] **Full refund**: pay → full refund-to-source → ledger returns to zero. / 全额退：支付→原路全额退→台账归零。
- [ ] **Partial refund**: pay ¥100, refund ¥30 → balance ¥70 correct. / 部分退：付100退30→余额70正确。
- [ ] **Offline sale**: kill ISP → sell offline → reconnect → sync reconciles. / 离线售：断 ISP→离线卖→重连→对账平。
- [ ] **Chargeback**: simulate dispute → acquirer case logged → evidence (MMS + CCTV) attached. / 拒付：模拟争议→收单案件登记→附证据（MMS+监控）。
- [ ] **Mixed tender**: part wallet + part card in one basket. / 混合支付：钱包+卡同单。

---

### 3.7 Worked reconciliation example / 对账实例

- Day sales / 日售: Alipay ¥12,000 (T+1), WeChat ¥8,000 (T+1), Card ¥5,000 (T+2), Cash ¥2,000 (same day). / 支付宝/微信 T+1，卡 T+2，现金当日。
- MMS ledger total / MMS 台账: ¥27,000 matches the till. / 台账 ¥27,000 与钱箱一致。
- Next-day bank / 次日到账: ¥20,000 (Alipay + WeChat + Cash); card ¥5,000 appears T+2. / 次日到 2 万（支付宝+微信+现金）；卡 T+2 到 5 千。
- Variance / 差异: ¥0 once card settles → reconciled, no deferred gap (`data/21#ap-038`). / 卡结清后差异 0 → 平账，无递延缺口。
- Audit trail / 审计链: each row carries tender type + MMS txn id + bank batch id. / 每行带支付方式+MMS 交易号+银行批次号。

### 3.8 Go-live cutover checklist / 上线切换清单

- [ ] At least 2 acquirers live (no single point of failure). / 至少 2 家收单在线（无单点）。
- [ ] Dual-ISP verified: kill primary → terminal fails over, sale still posts. / 双 ISP 已验：断主→终端切换，交易仍入账。
- [ ] Refund-to-source tested on each tender. / 各支付方式原路退款已测。
- [ ] Daily reconciliation job scheduled & alert on variance >0. / 日对账任务已排程，差异>0 告警。
- [ ] Receipt fields match market template (🔄 `tools/04`). / 小票字段符合市场模板。
- [ ] Refund policy posted at front desk & in app. / 退款政策已贴前台与 App。
- [ ] Chargeback evidence pack (MMS + CCTV) ready. / 拒付证据包（MMS+监控）就绪。

## ④ Common mistakes (anti-patterns) / 常见错误（反模式）

- `data/21#ap-025-bnpl-chargeback-surprise` — BNPL without modelling chargeback cost. / 上 BNPL 却未算拒付成本。
- `data/21#ap-038-deferred-no-reconcile` — prepaid sold, deferred revenue never reconciled. / 售预售却不核递延收入。
- `data/21#ap-031-payment-link-groupchat` — taking payment via group-chat link (no ledger). / 群聊链接收款（无台账）。
- `data/21#ap-032-cash-refund-digital` — refunding a digital payment in cash (audit gap). / 数字支付却现金退（审计缺口）。
- `data/21#ap-039-refund-policy-late` — no written refund policy before go-live. / 上线前无书面退款政策。

---

## ⑤ Related files / 相关文件

- `references/07-hardware-landscape-and-vendors.md` (C7 POS terminals). / POS 终端硬件。
- `references/08-network-and-infrastructure.md` — dual-ISP & VLAN. / 双 ISP 与 VLAN。
- `data/07-apac-regional-differences.md` (§① payment landscape). / 支付手段格局。
- `templates/09-mms-selection-scorecard.md` — MMS posts the sale. / MMS 入账。

---

## ⑥ G13 tri-perspective note / G13 三视角覆盖说明

This template serves **Architect** (rails + reconciliation design + dual-ISP), **Operator** (UAT script + failover runbook + receipt fields), and **Member** (reliable checkout, clear receipt, fast refund, data-safe payment); the dual-ISP and reconciliation rules protect the member's money-path and the operator's solvency — no orphaned touchpoint.
本模板覆盖**架构师**（通道+对账设计+双 ISP）、**运营者**（UAT 脚本+故障转移手册+小票字段）、**会员**（可靠结账、清晰小票、快速退款、支付数据安全）；双 ISP 与对账规则护住会员资金路径与运营者偿付能力——无孤儿触点。
