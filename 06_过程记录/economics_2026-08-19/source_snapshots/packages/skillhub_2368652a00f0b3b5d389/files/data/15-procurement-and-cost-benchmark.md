# Procurement & Cost Benchmark (Club IT) / 采购与成本基准（场馆 IT）

> **Cluster / 集群**: I (IT governance & money) + H (Digital assets) + C/B (Hardware/Software)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: All ranges are directional as of 2026-07 and re-verify every 90 days via `tools/04`; no precise price is stated — only order-of-magnitude ranges with confidence notes.
> **Cross-references / 交叉引用**: `data/03-software-vendor-directory.md`, `data/04-hardware-vendor-directory.md`, `data/21-anti-pattern-library.md`, `references/07-hardware-landscape-and-vendors.md#C13`, `references/15-lifecycle-scenarios.md` (G4), `tools/06-roi-three-scenario.md`.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## How to use this file / 本文件使用说明

This is the **money file** for Cluster I. It gives (a) the cost *structure* of club IT, (b) directional ranges by format, (c) a worked TCO example, (d) a zero-basis procurement process, and (e) negotiation/disposal guidance. All figures are **ranges**, not quotes — they exist so you walk into a vendor meeting with a sanity check, not a number to memorize.
这是集群 I 的**钱文件**。给出（a）场馆 IT 成本结构、（b）按业态的方向性区间、（c）TCO 算例、（d）0 基础采购流程、（e）谈判/残值指引。所有数字都是**区间**非报价——让你带着"谱"进销售会，而非背一个数。

> **Iron Law 6 / 铁律6**: Any single spend >¥100k (or market equivalent) needs a 3-scenario ROI via `tools/06`. These ranges feed that ROI; they are not the ROI themselves.
> 单笔 >10 万元（或等值）须附 `tools/06` 三情景 ROI。本区间喂给 ROI，本身不是 ROI。

---

## 1. Cost structure of club IT / 场馆 IT 成本结构 {#cost-structure}

Club IT spend splits into **one-time (CapEx)** and **recurring (OpEx)**.

| Bucket / 桶 | Type / 类型 | Examples / 示例 | FDMM |
|---|---|---|---|
| One-time / 一次性 | CapEx | hardware fit-out, gate lane, locker bank, network, signage, CCTV install | L1–L2 |
| Recurring /  recurring | OpEx | MMS SaaS, payment %, BI, MarTech, bandwidth, maintenance, replace fund | L2+ |
| Hidden / 隐性 | both | implementation, training, integration, data-export fees, spare parts | all |

> **Rule / 规则**: Budget both buckets. Clubs that only budget CapEx get surprised by Year-2 OpEx. Set a **replace fund** = unit cost ÷ lifespan, parked monthly (see `references/07#C13`).
> 两桶都预算。只算一次性资本支出的馆，第 2 年运营支出会惊到。设"换新基金"= 单价÷寿命，按月存（见 `references/07#C13`）。

---

## 2. Full new-club IT fit-out by format / 新馆 IT 总投入（按业态）{#cost-fitout}

Directional 2026-07 ranges; verify via `tools/04` 🔄. / 方向性 2026-07 区间；经 tools/04 核验 🔄。

| Format / 业态 | Floor / 面积 | One-time IT fit-out / 一次性 IT 总投入 | Recurring /mo / 月 recurring | Notes / 注记 |
|---|---|---|---|---|
| Boutique studio / 精品工作室 | 200–500㎡ | ¥30k–¥150k | ¥1k–¥6k | fewer gates, light network / 少闸轻网 |
| Mid club / 中型馆 | 800–2,000㎡ | ¥120k–¥500k | ¥4k–¥20k | gates+lockers+CCTV+BI / 闸柜监控BI |
| Big-box / 大型综合 | 3,000–8,000㎡ | ¥400k–¥1.5M | ¥15k–¥60k | full stack, SD-WAN later / 全栈后续SD-WAN |
| 24h unmanned / 无人店 | 300–1,000㎡ | ¥150k–¥600k | ¥5k–¥25k | access+CV heavy / 门禁CV重 |

:::dynamic-hook topic="apac-club-it-fitout-range-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
Fit-out ranges widen with city tier and fit-out quality; tier-1 Shanghai fit-out can be 1.5–2× tier-3. Verify per-city via tools/04 before budgeting.
总投入随城市能级与装修档次拉大；一线上海的投入可达三线 1.5–2 倍。预算前按城市经 tools/04 核验。
:::

---

## 3. Directional cost ranges / 方向性成本区间

All ranges directional 2026-07, verify via `tools/04` 🔄. / 均方向性 2026-07，经 tools/04 核验 🔄。

### 3.1 Membership SaaS per month / 会籍 SaaS 月费 {#cost-mms}

| Market / 市场 | Per-club/mo pattern / 按店月订模式 | Confidence / 置信 |
|---|---|---|
| China 大陆 | ¥500–¥8,000/mo by member count / 按会员量 | medium / 中 |
| Global APAC | US$100–US$1,500/mo / 国际 | medium / 中 |

### 3.2 Gate lane / 闸机通道 {#cost-gate-lane}

- Unit: ¥3k–¥20k per gate lane 🔄 (swing/turnstile; face reader adds). / 每闸 ¥3k–¥20k 🔄。
- Install often excluded — request all-in price. / 安装常不含——要全包价。

### 3.3 Locker bank / 储物柜组 {#cost-locker-bank}

- ¥500–¥2,500 per cell 🔄; a 50-cell bank = ¥25k–¥125k. / 每格 ¥500–¥2,500 🔄；50 格=¥25k–¥125k。
- Central controller = single point of failure (see `data/04#cat-lockers`). / 集中控制器=单点（见 `data/04#cat-lockers`）。

### 3.4 Network per sqm / 网络每平米 {#cost-network-sqm}

- ¥30–¥150/㎡ for prosumer/enterprise gear + cabling 🔄. / 准企业/企业设备+布线 ¥30–¥150/㎡ 🔄。
- VLAN-capable minimum for any club with POS+gates. / 有收银+闸机的馆至少支持 VLAN。

### 3.5 CCTV per camera installed / 监控每路（含安装）{#cost-cctv-camera}

- ¥300–¥3k per camera + NVR + install 🔄; retention storage per law. / 每路 ¥300–¥3k + NVR + 安装 🔄；留存存储依法。
- No cameras in changing rooms (HI-5). / 更衣室禁摄（HI-5）。

### 3.6 Signage screen installed / 数字标牌屏（含安装）{#cost-signage-screen}

- ¥1k–¥8k per screen installed (consumer–commercial) 🔄 + CMS ¥0–¥300/screen/mo. / 每屏含安装 ¥1k–¥8k 🔄 + CMS ¥0–¥300/屏/月。

### 3.7 UPS / 不间断电源 {#cost-ups}

- Front-desk ¥500–¥3k; rack ¥2k–¥15k 🔄 by load. / 前台 ¥500–¥3k；机架 ¥2k–¥15k 🔄（按负载）。

### 3.8 Cardio unit by tier / 有氧器械（分档）{#cost-cardio-unit}

| Tier / 档 | Unit range / 单价 🔄 |
|---|---|
| Consumer smart bike / 消费级智能单车 | ¥800–¥4k |
| Commercial entry / 商用入门 | ¥3k–¥15k |
| Commercial premium / 商用高端 | ¥20k–¥60k |

### 3.9 Body scanner / 体测仪 {#cost-body-scanner}

- BIA ¥8k–¥80k 🔄 by electrode count + cert; posture scanner separate. / 生物电阻抗 ¥8k–¥80k 🔄（按电极数+认证）；体态扫描另计。

---

## 4. TCO worked example — 3-year MMS / TCO 算例：3 年会籍系统 {#tco-mms}

Directional, China mid-club, 800 members. / 方向性，中国中型馆，800 会员。

| Line / 项 | Year 1 / 年1 | Year 2 / 年2 | Year 3 / 年3 | 3-yr total / 三年合计 |
|---|---|---|---|---|
| License (¥2k/mo) | ¥24k | ¥24k | ¥24k | ¥72k |
| Implementation / 实施 | ¥8k | — | — | ¥8k |
| Training / 培训 | ¥3k | ¥1k | ¥1k | ¥5k |
| Integration (gate+payment) / 集成 | ¥5k | — | — | ¥5k |
| Data-export / API fee / 导出费 | ¥1k | ¥1k | ¥1k | ¥3k |
| Replace fund (negligible) | — | — | — | — |
| **Total / 合计** | **¥41k** | **¥26k** | **¥26k** | **¥93k** |

> **Hidden-cost lesson / 隐性成本启示**: The license is ~77% of 3-yr cost; the other 23% (implementation/training/integration/export) is what beginners forget. Always ask "what's NOT in the ¥2k/mo?" 
> 授权约占三年 77%；其余 23%（实施/培训/集成/导出）是新手会忘的。永远问"这每月价里不含什么？"

---

## 5. Procurement process for zero-basis / 0 基础采购流程 {#procurement-process}

A repeatable sequence. Skip a stage = risk (Iron Law 5). / 可复用流程。跳阶段=风险（铁律5）。

1. **3-quote rule / 三家比价**: Get ≥3 written quotes, each separating one-time vs recurring. / 拿 ≥3 份书面报价，一次性与 recurring 分开。
2. **Spec sheet vs demo script / 参数表 vs 演示脚本**: Write a demo script (your real flows: check-in at peak, refund, freeze) and make each vendor run it. / 写演示脚本（你的真实流程：高峰入场、退款、冻结），让每家跑一遍。
3. **Reference calls / 同行电话**: Call 2–3 other club owners using the vendor. Ask: / 给 2–3 家用该厂商的老板打电话。问：
   - "What broke in month 6?" / "第 6 个月什么坏了？"
   - "Did they answer at 7am when the gate died?" / "闸机早上 7 点死时他们接了吗？"
   - "Any fee not in the contract?" / "合同外有费用吗？"
4. **Pilot clause / 试点条款**: Sign with a 30–60 day pilot + acceptance criteria before full rollout. / 签 30–60 天试点+验收标准，再全面铺开。
5. **Payment milestones / 付款节点**: Tie payment to acceptance: 30% deposit, 40% on install, 30% on signed acceptance. Never 100% upfront. / 付款绑验收：3 成定金、4 成安装、3 成验收签字。绝不全款预付。

---

## 6. Negotiation levers / 谈判杠杆 {#negotiation-levers}

| Lever / 杠杆 | How / 怎么用 | Trap / 坑 |
|---|---|---|
| Multi-year vs flexibility / 多年 vs 灵活 | 2-yr commit may cut 10–20% but locks you / 2年约或降10–20%但锁定 | exit/export clause first / 先要退出导出条款 |
| End-of-quarter timing / 季末时点 | Vendors discount to hit quota (Mar/Jun/Sep/Dec) / 季末冲量打折 | don't rush due diligence / 别省尽调 |
| Bundling traps / 捆绑坑 | "free gate with MMS" may hide weak gate / "送闸机"可能闸弱 | test the free item hard / 白送的更要狠测 |

> **Red line / 红线**: Never trade away the data-export clause for a discount (see `data/21#ap-021-no-export-clause`).
> 绝不为折扣放弃数据导出条款（见 `data/21#ap-021-no-export-clause`）。

---

## 7. Leasing vs buying (equipment finance) / 租赁 vs 买（设备金融）{#leasing-vs-buying}

| Option / 方式 | Pros / 优 | Cons / 劣 | When / 何时 |
|---|---|---|---|
| Buy / 买 | asset on books, no interest / 资产入账无息 | upfront cash, obsolescence risk / 现金占用过时风险 | stable format, long horizon / 业态稳周期长 |
| Lease / 租 | preserves cash, upgrade path / 保现金可升级 | total cost higher, return conditions / 总成本更高归还条件 | fast-changing tech (CV/smart) / 快变技术(CV/智能) |
| Finance/分期 | spreads cost / 摊薄成本 | interest, lien on asset / 利息资产抵押 | mid cashflow club / 现金流中等 |

> **Rule / 规则**: Lease only tech that depreciates fast (smart screens, CV). Buy durable steel (strength frames). 
> 只租贬值快的技术（智能屏、CV）；买耐用的钢（力量架）。

---

## 8. Gray-market warning / 水货警告 {#gray-market-warning}

:::dynamic-hook topic="apac-gray-import-warranty-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
Gray-import hardware voids local warranty and leaves no parts pipeline; for safety/access gear this is a life-safety and ops risk. Verify authorized seller via brand site (tools/04).
水货硬件使本地保修失效且无备件；对安全/门禁设备是人身安全与运营风险。经品牌官网（tools/04）核实授权卖家。
:::

> **Anti-pattern / 反模式**: Gray-import trap → `data/21#ap-025-gray-import`. The "cheap" gate that dies in 6 months costs more than buying direct.
> 水货陷阱 → `data/21#ap-025-gray-import`。"便宜"闸机半年坏，比直采更贵。

---

## 9. Disposal & residual value / 处置与残值 {#disposal-residual}

| Class / 类 | Residual / 残值 | Channel / 渠道 |
|---|---|---|
| Cardio/strength steel | 10–30% refurb | refurb resellers, scrap / 翻新商、回炉 |
| Gates/lockers | 10–20% | refurb resellers / 翻新商 |
| Network gear | mid | enterprise resale / 企业二手 |
| CCTV | low | secure-wipe disks first / 先擦盘 |
| Wearables/bands | low | recycle / 回收 |

> **Privacy / 隐私**: Wipe all storage (CCTV, POS, gate controllers) before disposal — member data must not leave with the hardware (HI-9).
> 处置前擦净所有存储（监控/收银/闸控）；会员数据不得随硬件走（HI-9）。

---

### 3.10 Bandwidth / line / 带宽线路 {#cost-bandwidth}

- Club fiber ¥200–¥2,000/mo by market & speed 🔄; backup 4G/5G failover recommended for 24h/big-box. / 场馆光纤 ¥200–¥2,000/月（因市场速率）；无人店/大馆建议 4G/5G 备用故障切换。

### 3.11 Server closet / 机房 {#cost-server-closet}

- ¥3k–¥30k/club for switch+AP+UPS+NVR rack (see `data/04#cat-network-gear`). / 每店 ¥3k–¥30k（交换机+AP+UPS+NVR 机柜，见 `data/04#cat-network-gear`）。

---

## 4.1 Hardware TCO worked example — gate bank + network / TCO 算例：闸机组+网络

Directional, China mid-club, 2 gate lanes + network. / 方向性，中国中型馆，2 闸+网络。

| Line / 项 | One-time / 一次性 | 3-yr recurring / 三年recurring | 3-yr total / 三年合计 |
|---|---|---|---|
| 2 gate lanes (¥8k each) | ¥16k | maintenance ¥600/y | ¥17.8k |
| Network (prosumer) | ¥12k | bandwidth ¥3.6k/y + maint ¥0.6k/y | ¥25.8k |
| UPS | ¥3k | battery swap ¥1k/y | ¥6k |
| **Total / 合计** | **¥31k** | — | **¥49.6k** |

> Lesson / 启示: recurring (bandwidth + maintenance + battery) is ~38% of 3-yr cost — the part beginners forget. / recurring（带宽+维护+电池）约占三年 38%——新手易忘的部分。

---

## 5.1 Spec-sheet template / 参数表模板

When requesting quotes, send vendors this minimum: / 索报价时发给厂商的最低清单：
- Club format & floor area / 业态与面积
- Member count & peak concurrency / 会员数与高峰并发
- Required integrations (MMS, payment, gate) / 需集成（MMS、支付、闸）
- Compliance market(s) / 合规市场
- Acceptance criteria (pilot 30–60d) / 验收标准（试点30–60天）

---

## 6.1 Timing calendar / 谈判时点日历

| Window / 时点 | Lever / 杠杆 |
|---|---|
| Mar/Jun/Sep/Dec end / 季末 | quota discount / 冲量折扣 |
| Renewal 60d before / 续约前60天 | multi-year vs flexibility / 多年vs灵活 |
| Post-demo / 演示后 | bundle break-out / 拆捆绑 |

> **Red line / 红线**: never trade data-export clause for discount (see `data/21#ap-021-no-export-clause`).
> 绝不为折扣弃数据导出条款（见 `data/21#ap-021-no-export-clause`）。

---

## 10. Downtime cost note / 停机成本注记

A gate down at 7am Monday can block dozens of check-ins → lost day passes + churn signal. Budget for redundancy (spare reader, fail-open) not just the cheapest lane. Quantify in ROI via `tools/06`.
周一 7 点闸机坏，挡几十人入场→丢次卡+流失信号。要为冗余（备用读头、断电开）预算，而非只买最便宜的闸。用 `tools/06` 量化进 ROI。

---

## 11. One-page budget template / 一页预算模板

| Bucket / 桶 | CapEx / 一次性 | OpEx/mo / 月 | Replace fund/mo / 换新基金 |
|---|---|---|---|
| MMS | — | ¥2k | — |
| Gates | ¥16k | ¥50 | ¥450 |
| Network | ¥12k | ¥350 | ¥170 |
| CCTV | ¥10k | ¥50 | ¥300 |
| Signage | ¥8k | ¥200 | ¥230 |
| Body | ¥20k | — | ¥500 |
| Replace fund total / 换新合计 | — | — | ~¥1.65k/mo |

> Rule / 规则: park the replace fund monthly so year-6 cliff never hits (see `references/07#C13`).
> 每月存换新基金，避免第 6 年全坏悬崖（见 `references/07#C13`）。

---

## G13 Tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: cost structure + TCO model + leasing math for capex planning.
- **Operator / 运营者**: 3-quote rule, demo script, reference calls, payment milestones, negotiation levers.
- **Member / 会员**: privacy-safe disposal, no lock-in (export clause), reliable service funded by replace fund. No money touchpoint is orphaned.
本文件覆盖架构师（成本结构+TCO+租赁算账）、运营者（三家比价/演示脚本/同行电话/付款节点/谈判杠杆）、会员（隐私安全处置/无锁定/换新基金保障服务）三视角；无孤儿财务触点。
