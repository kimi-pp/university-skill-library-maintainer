# APAC Regional Differences (Non-Regulatory) / 亚太区域差异（非监管类）

> **Cluster / 集群**: F-adjacent (operational variance) · Cross-refs / 交叉引用: `references/10` · `references/11` · `references/17` (messaging) · `data/06` (glossary)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: re-verify every 180 days; platform/payment facts carry 🔄 hooks — run `tools/04` before relying.
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## Why this file / 为何有本文件

Regulation (Cluster F) decides *what you may do*; this file decides *how things actually work on the ground* — payment habits, channels, calendars, power, and onboarding data. Getting these wrong silently breaks a rollout even when you are fully compliant.
监管（集群 F）决定*能做啥*；本文件决定*地面实际如何运转*——支付习惯、渠道、日历、电力、入驻资料。这些搞错会让上线在「完全合规」下仍悄悄失败。

> **Honesty red line / 诚实红线**: payment-method dominance and platform facts are **ranges/trends**, not precise shares; marked 🔄 and verified via `tools/04`. No fabricated market percentages.
> **诚实红线**：支付占比与平台事实为**区间/趋势**而非精确份额；标 🔄 经 `tools/04` 核验。不编造市场百分比。

---

## ① Payment method landscape / 支付手段格局

| Market / 市场 | Dominant methods / 主流方式 | Notes / 备注 |
|---|---|---|
| China mainland / 中国内地 | WeChat Pay + Alipay dominate / 微信支付+支付宝主导 | cash marginal in cities / 城市现金边缘化 🔄 |
| Hong Kong (China) / 中国香港 | Octopus + PayMe + cards / 八达通+PayMe+卡 | QR (AlipayHK/WeChat Pay HK) growing / 二维码增长 🔄 |
| Taiwan (China) / 中国台湾 | Cards + LINE Pay + JKOPAY / 信用卡+LINE Pay+街口 | cash still common / 现金仍常见 🔄 |
| Japan / 日本 | Cash + PayPay + konbini (Konbini payment) / 现金+PayPay+便利店付款 | many still pay at 7-11/Lawson for memberships / 会费常便利店缴 🔄 |
| South Korea / 韩国 | Cards + KakaoPay + NaverPay / 信用卡+KakaoPay+NaverPay | near cashless / 近乎无现金 🔄 |
| Singapore / 新加坡 | PayNow + GrabPay + cards / PayNow+GrabPay+卡 | PayNow QR ubiquitous / PayNow 二维码普及 🔄 |
| Thailand / 泰国 | PromptPay + TrueMoney + GrabPay / PromptPay+TrueMoney+GrabPay | PromptPay QR national / 国家 PromptPay 🔄 |
| Malaysia / 马来西亚 | DuitNow + Touch'n Go + GrabPay / DuitNow+TnG+GrabPay | DuitNow QR growing / DuitNow 增长 🔄 |
| Indonesia / 印尼 | GoPay + OVO + DANA + QRIS / GoPay+OVO+DANA+QRIS | QRIS national interoperable / 国家 QRIS 🔄 |
| Vietnam / 越南 | MoMo + ZaloPay + Viettel Money / MoMo+ZaloPay+ Viettel Money | QR rising / 二维码上升 🔄 |
| India / 印度 | UPI (PhonePe/GPay) + cards / UPI+卡 | UPI dominant for small / UPI 小额主导 🔄 |
| Australia/NZ / 澳新 | Cards + BNPL (Afterpay/Zip) / 卡+先买后付 | EFTPOS + Apple/Google Pay / EFTPOS+钱包 🔄 |

:::dynamic-hook
topic: APAC payment-method share shifts (WeChat/Alipay/PayPay/UPI etc.) / 亚太支付份额迁移
stored-value: wallets gaining vs cash across SEA/India; Japan cash persists; Korea near-cashless — shares move yearly (stored 2026-07)
staleness: HIGH — payment share shifts annually / 高——支付份额逐年变
action: retrieve latest central-bank / processor share stats before POS design
fallback: if retrieval fails, present stored value + "as of 2026-07, verify before use"
:::

**Club takeaway / 场馆要点**: your POS/membership app must plug the **local** rails (e.g. UPI in India, QRIS in Indonesia, PayNow in Singapore, WeChat/Alipay in China). A single global card-only flow will leak conversions.
**要点**：POS/会员 App 须接**本地**通道（印度 UPI、印尼 QRIS、新加坡 PayNow、中国微信/支付宝）。全球仅刷卡会流失转化。

---

## ② Messaging channel norms / 消息通道惯例

Pointer to the dedicated chapter: **`references/17-omnichannel-messaging.md`**. Summary / 摘要:
- China mainland: WeChat Work / 企业微信 + SMS + Mini-program. / 中国：企业微信 + 短信 + 小程序。
- Hong Kong (China) / Taiwan (China): WhatsApp + LINE. / 港台：WhatsApp + LINE。
- Japan: LINE is king (OTannouncements, coupons). / 日本：LINE 为王。
- South Korea: KakaoTalk / KakaoTalk 为主.
- SEA: WhatsApp (SG/MY/TH), Zalo (VN), LINE (TH), Gojek/Grab in-app. / 东南亚：WhatsApp、Zalo（越）、LINE（泰）。
- India: WhatsApp + SMS (DND-aware). / 印度：WhatsApp + 短信（注意 DND）。
- ANZ: Email + SMS + app push. / 澳新：邮件 + 短信 + App 推送。

**Club takeaway / 要点**: marketing opt-in (HI-7) must be captured **in the channel you'll use** — consent given on WeChat does not cover WhatsApp.
**要点**：营销 Opt-in（HI-7）须在你*将用的渠道*取得——微信给的同意不覆盖 WhatsApp。

---

## ③ Language / locale & name-order / 语言·区域与姓名顺序

| Market / 市场 | Default locale / 默认区域 | Name order / 姓名顺序 | Address format / 地址格式 |
|---|---|---|---|
| China mainland / 中国内地 | zh-CN, simplified / 简体 | Family+Given (张三) | smallest→largest (room→bldg→st) |
| Hong Kong (China) / 中国香港 | zh-HK + en | Given-Family (English) / 姓在前(中) | mixed / 混合 |
| Taiwan (China) / 中国台湾 | zh-TW, traditional / 繁体 | Family+Given | smallest→largest |
| Japan / 日本 | ja-JP | Family-Given (Yamada Taro) | postal code first / 邮编前置 |
| South Korea / 韩国 | ko-KR | Family-Given (Kim Min-jun) | postal code first / 邮编前置 |
| Singapore / 新加坡 | en-SG + zh | Given-Family (English) | largest→smallest |
| Thailand / 泰国 | th-TH | Given-Family (English order) | postal code last / 邮编在后 |
| Malaysia / 马来西亚 | en-MY + ms | Given-Family | largest→smallest |
| Indonesia / 印尼 | id-ID | Given-Family | postal code last / 邮编在后 |
| Vietnam / 越南 | vi-VN | Family+Given (Nguyen Van A) | smallest→largest |
| India / 印度 | en-IN + local | Given-Family | postal code last / 邮编在后 |
| Australia/NZ / 澳新 | en-AU / en-NZ | Given-Family | largest→smallest |

**Club takeaway / 要点**: never force "First / Last" Western order on member forms; support family-name-first and postal-code-first layouts or you'll corrupt member records.
**要点**：会员表单勿强推西方「名/姓」顺序；须支持姓在前、邮编前置，否则污染会员档案。

---

## ④ Public holidays & peak-season calendar / 公共假期与旺季日历

| Event / 事件 | Markets / 市场 | IT-load impact / IT 负载影响 |
|---|---|---|
| Chinese New Year (CNY) / 春节 | China mainland, HK, TW, SEA Chinese communities | mass travel; booking spikes pre/post; plan capacity / 出行潮，节前节后预约峰值 |
| Golden Week / 黄金周 | China mainland (Oct), Japan (Golden Week May) | heavy day-pass & class load / 日票与课程负载重 |
| Ramadan / 斋月 | Indonesia, Malaysia, (observers in SG/TH) | shifted operating hours; night-traffic changes / 营业时间调整，夜间流量变 |
| Diwali / 排灯节 | India | gifting/membership-promo spike; regional holidays / 赠礼会籍促销峰值，地方假 |
| Songkran / 宋干节 | Thailand | April closure/travel; water-event marketing / 4 月闭店出行，泼水营销 |
| Obon / 盂兰盆 | Japan | August travel dip / 8 月出行低谷 |
| Year-end / 年末 | all | promotion + renewal peak / 促销与续费峰值 |

**Club takeaway / 要点**: size your booking/POS/CRM autoscaling and on-call rota around these; a "24h unmanned" club still needs remote-monitoring cover during local peaks.
**要点**：按此给约课/POS/CRM 做弹性扩容与值班排班；「24h 无人」馆在本地峰值仍需远程监控值守。

---

## ⑤ Power plugs / voltage & equipment import / 插头·电压与设备进口

| Market / 市场 | Plug / 插头 | Voltage / 电压 | Import note / 进口注意 |
|---|---|---|---|
| China mainland / 中国内地 | A/C/I (GB2099) | 220V 50Hz | CCC mark for equipment / 设备需 CCC |
| Hong Kong (China) / 中国香港 | G (BS1363) | 220V 50Hz | BS safety / BS 安全 |
| Taiwan (China) / 中国台湾 | A/B (NEMA) | 110V 60Hz | step-down for 220V gear / 220V 设备需降压 |
| Japan / 日本 | A (JIS) | 100V 50/60Hz | PSE mark; 100V needs careful spec / PSE 标志，100V 须慎配 |
| South Korea / 韩国 | C/F | 220V 60Hz | KC mark / KC 标志 |
| Singapore / 新加坡 | G | 230V 50Hz | PSB/Safety mark / 安全标志 |
| Thailand / 泰国 | A/B/C/O | 220V 50Hz | TISI mark / TISI 标志 |
| Malaysia / 马来西亚 | G | 240V 50Hz | SIRIM / SIRIM 认证 |
| Indonesia / 印尼 | C/F/G | 230V 50Hz | SNI mark / SNI 标志 |
| Vietnam / 越南 | A/C | 220V 50Hz | CR mark / CR 认证 |
| India / 印度 | C/D/M | 230V 50Hz | BIS mark / BIS 标志 |
| Australia/NZ / 澳新 | I (AS/NZS 3112) | 230/240V 50Hz | RCM mark / RCM 标志 |

**Club takeaway / 要点**: a "global" treadmill bought in one market may need a transformer or fail certification elsewhere — factor certification + voltage into the FDMM hardware plan (`references/07`).
**要点**：某市场买的「全球」跑步机在别处可能需变压器或不达认证——认证 + 电压须计入硬件规划（`references/07`）。

---

## ⑥ Typhoon / monsoon / earthquake resilience / 台风·季风·地震韧性

- **Typhoon belt / 台风带**: Taiwan (China), Hong Kong (China), Philippines-adjacent, Japan (Sep–Oct), Vietnam (Jul–Nov), South China coast. → UPS + generator for gates/CCTV; offline-mode POS (no cloud dependency). / 台港日越华南——闸机监控配 UPS+发电；POS 离线模式（不依赖云）。
- **Monsoon / 季风**: India (Jun–Sep), Thailand/Malaysia/Indonesia (Nov–Mar). → waterproof cabling, raised server/network gear, flood-rated IDF rooms. / 印泰马印尼——防水线缆、设备上架抬高、弱电间防洪。
- **Earthquake / 地震**: Japan, Taiwan (China), NZ, Indonesia. → seismic-rated racking, automatic safe-shutdown for lifts/gates, data replication off-region (check residency first). / 日台新印尼——机柜抗震、闸机电梯自动安全停机、数据异地副本（先查驻留）。
- **All / 通用**: SD-WAN multi-link (`references/08`) so a single carrier outage does not close the club. / SD-WAN 多链路，单运营商断网不闭馆。

---

## ⑦ Labor norms affecting rostering / 影响排班的劳工规范

| Market / 市场 | Rostering note / 排班要点 |
|---|---|
| China mainland / 中国内地 |  overtime caps; social-insurance filing / 加班上限，社保申报 |
| Japan / 日本 | 36-agreement caps; late-night premiums / 36 协定上限，深夜加成 |
| South Korea / 韩国 | 52-hour workweek cap / 52 小时周上限 |
| Australia/NZ / 澳新 | award/penalty rates; casual loadings / 裁定费率，临时工加成 |
| Singapore / 新加坡 | EA/TA norms; rest-day rules / 雇佣法，休息日 |
| SEA / 东南亚 | varied; mandatory rest + overtime pay / 各异，强制休息+加班费 |

**Club takeaway / 要点**: rostering SaaS must encode local overtime/penalty rules or you'll generate illegal schedules and payroll disputes.
**要点**：排班 SaaS 须内嵌本地加班/加成规则，否则生成违法排班与薪资纠纷。

---

## ⑧ Tipping & pricing-display norms / 小费与标价惯例

- **Tipping / 小费**: generally **not** expected in China, Japan, Korea, Taiwan (China); customary in some ANZ hospitality but **not** in gym membership. → do not build "tip the coach" flows in East Asia. / 中日韩台通常**不**收小费；澳新 hospitality 偶有但会籍不收——东亚勿做「 coach 打赏」流程。
- **Pricing display / 标价**: include all-in price + tax where the market expects (e.g. AU " GST inclusive" norms; Japan tax-in/税込 vs tax-ex). Hide no mandatory fees — prepaid/contract fairness (HI-3) demands transparent total price. / 含税前价按市场习惯（澳「含 GST」、日本税込/税别）。不得隐藏强制费——预付/合同公平（HI-3）要求总价透明。

---

## ⑨ Business-registration data needed by SaaS onboarding / SaaS 入驻所需工商资料

| Market / 市场 | Typical data / 典型资料 |
|---|---|
| China mainland / 中国内地 | 统一社会信用代码 + 营业执照 + 法人 ID / USCC + business license + legal-rep ID |
| Hong Kong (China) / 中国香港 | BR + CR (company registry) no. / 商业登记 + 公司注册号 |
| Taiwan (China) / 中国台湾 | 統一編號 + 公司/行號登記 / uniform no. + registration |
| Japan / 日本 | 法人番号 (Corporate Number) + 屋号 / Corporate No. + trade name |
| South Korea / 韩国 | 사업자등록번호 (Biz Reg No.) / business registration no. |
| Singapore / 新加坡 | UEN (Unique Entity Number) / 唯一实体号 |
| Thailand / 泰国 | ทะเบียนพาณิชย์ (Thai reg no.) / registered partnership no. |
| Malaysia / 马来西亚 | SSM registration no. / SSM 注册号 |
| Indonesia / 印尼 | NIB (Business Identification No.) / 企业识别号 |
| Vietnam / 越南 | MST (Mã số thuế / tax code) / 税码 |
| India / 印度 | GSTIN + CIN / GST 号 + 公司号 |
| Australia/NZ / 澳新 | ABN / ACN (AU) · NZBN (NZ) / 商业号 |

**Club takeaway / 要点**: your onboarding form should collect the **correct local identifier** up front — mismatched IDs break tax receipts, payment settlement, and compliance reporting.
**要点**：入驻表单应 upfront 采集**正确本地标识**——ID 错配会毁掉税务发票、支付结算与合规上报。

---

## ⑩ Connectivity & ISP landscape / 网络连接与运营商

| Market / 市场 | Typical fixed / 固定宽带 | Mobile / 移动 | Resilience note / 韧性要点 |
|---|---|---|---|
| China mainland / 中国内地 | 电信/联通/移动 | 三大 + 广电 | ICP/备案 for public servers / 公网服务器需备案 |
| Japan / 日本 | NTT/au/KDDI | docomo/au/SoftBank | redundant fiber common / 光纤冗余普遍 |
| South Korea / 韩国 | KT/SK/LG | three carriers | among fastest; cheap redundancy / 极快，冗余便宜 |
| Singapore / 新加坡 | Singtel/StarHub/M1 | three | dense, cheap dual-link / 密集，双链便宜 |
| SEA / 东南亚 | varies / 各异 | varies | monsoon/typhoon → multi-link + 4G backup / 季风台风→多链路+4G 备 |
| India / 印度 | Jio/Airtel/BSNL | Jio/Airtel/Vi | power cuts → UPS essential / 断电多→UPS 必备 |
| Australia/NZ / 澳新 | NBN (AU) / fibre (NZ) | Telstra/Optus/Spark | remote sites → satellite/LTE backup / 偏远点→卫星/LTE 备 |

**Club takeaway / 要点**: design SD-WAN with at least two independent carriers (`references/08`); a single ISP outage must not close the club or stop POS.
**要点**：SD-WAN 至少双运营商独立链路（`references/08`）；单 ISP 断网不得闭馆或停 POS。

## ⑪ Member-acquisition channel norms / 获客渠道惯例

- China mainland: 抖音/小红书 + 私域企微 + 大众点评. / 抖音/小红书+私域企微+点评。
- Japan: 集客 via LINE + 駅広告 + 口コミ. / LINE+车站广告+口碑。
- South Korea: 인스타/네이버 + Kakao channel. / Instagram/Naver+Kakao。
- SEA: TikTok/Shopee/Lazada live + Grab/Gojek. / TikTok/电商直播+出行 App。
- India: Instagram + WhatsApp + 团购平台. / Instagram+WhatsApp+团购。
- ANZ: Google/Meta + 口碑 + 本地社群. / Google/Meta+口碑+本地社群。

**Club takeaway / 要点**: lead capture must respect the same opt-in (HI-7) as retention marketing; consent collected on one platform does not cover another.
**要点**：获客留资须遵守与留存营销同样的 Opt-in（HI-7）；一平台同意不覆盖另一平台。

## ⑫ Climate & humidity impact on equipment / 气候湿度对设备影响

- High-humidity markets (SEA, southern China, coastal JP): corrode treadmill electronics & RFID readers → IP-rated enclosures, silica control, quarterly dehumidifier service. / 高湿（东南亚、华南、沿海日）：腐蚀跑步机电子与读卡器→IP 防护、控湿、季度除湿维护。
- Heat (India/SEA summer): HVAC redundancy for server/IDF rooms; thermal shutdown protection. / 高温（印度/东南亚夏季）：机房空调冗余，过温保护停机。
- Cold-dry (northern China winter): static control for network gear. / 干冷（华北冬季）：网络设备防静电。
- Salt-air (coastal TW/JP/AU): outdoor AP/cameras need marine-grade coating. / 海风盐蚀（沿海台日澳）：户外 AP/摄像头需船用级涂层。

## ⑬ Currency & invoicing / 货币与开票

| Market / 市场 | Currency / 货币 | Invoice note / 开票要点 |
|---|---|---|
| China mainland / 中国内地 | CNY ¥ | 增值税发票 VAT special / 增值税专票 |
| Hong Kong (China) / 中国香港 | HKD HK$ | receipt vs invoice / 收据与发票 |
| Taiwan (China) / 中国台湾 | TWD NT$ | 統一發票 / 统一发票 |
| Japan / 日本 | JPY ¥ | インボイス (invoice) system / 发票制度 |
| South Korea / 韩国 | KRW ₩ | 세금계산서 / 税务计算书 |
| Singapore / 新加坡 | SGD S$ | GST-registered invoicing / 含 GST 开票 |
| Thailand / 泰国 | THB ฿ | ใบกำกับภาษี / 税务发票 |
| Malaysia / 马来西亚 | MYR RM | SST invoice / SST 发票 |
| Indonesia / 印尼 | IDR Rp | 税率 faktur pajak / 税务发票 |
| Vietnam / 越南 | VND ₫ | hóa đơn điện tử / 电子发票 |
| India / 印度 | INR ₹ | GST e-invoice / GST 电子发票 |
| Australia/NZ / 澳新 | AUD/NZD | GST-inclusive display / 含 GST 显示 |

**Club takeaway / 要点**: the billing/CRM module must emit the **local invoice type** and display tax per local norm — mismatches block reconciliation and tax filing.
**要点**：计费/CRM 须出具**本地发票类型**并按本地习惯显示税额——错配会卡住对账与报税。

## Rollout checklist for a new market / 新市场落地清单

1. Local business ID + bank account (`§⑨`). / 本地工商号+银行账户。
2. Local payment rails in POS (`§①`). / POS 接本地支付通道。
3. Locale/name/address form fields (`§③`). / 表单区域/姓名/地址字段。
4. Language + messaging channel + opt-in capture (`§②`, `§⑪`). / 语言+消息渠道+Opt-in 采集。
5. Power/voltage/certification for hardware (`§⑤`, `§⑫`). / 硬件电力/电压/认证。
6. Holiday/peak capacity plan (`§④`). / 假期/峰值容量规划。
7. Disaster resilience (UPS/SD-WAN/offline POS) (`§⑥`, `§⑩`). / 灾害韧性（UPS/SD-WAN/离线 POS）。
8. Labour/rostering rules in scheduling SaaS (`§⑦`). / 排班 SaaS 内嵌劳工规则。
9. Run `references/10`–`12` four-pack + `tools/05` before go-live. / 上线前跑四件套与 `tools/05`。

## Cross-links / 交叉引用

- Compliance four-pack & red lines: `references/10` · `references/11` · `references/12` · `data/02`. / 合规四件套与红线：`references/10`/`11`/`12`、`data/02`。
- Messaging channels deep-dive: `references/17-omnichannel-messaging.md`. / 消息通道详述：`references/17`。
- Hardware/voltage planning: `references/07-hardware-landscape-and-vendors.md`. / 硬件电压规划：`references/07`。
- Network resilience (SD-WAN): `references/08-network-and-infrastructure.md`. / 网络韧性：`references/08`。

## ⑭ Member app store & OS norms / 会员 App 商店与系统惯例

| Market / 市场 | App stores / 商店 | OS share / 系统占比 | Note / 备注 |
|---|---|---|---|
| China mainland / 中国内地 | 应用宝/华为/小米 (no Google Play) | Android domestic + iOS | push via 厂商通道 / 厂商推送 |
| Hong Kong (China) / 中国香港 | App Store + Google Play | iOS + Android | standard / 标准 |
| Taiwan (China) / 中国台湾 | App Store + Google Play | iOS + Android | standard / 标准 |
| Japan / 日本 | App Store + Google Play | iOS-heavy | LINE login popular / LINE 登录盛行 |
| South Korea / 韩国 | One Store + Play + App Store | Android + iOS | Kakao login / Kakao 登录 |
| SEA / 东南亚 | Play + App Store | Android-heavy | OVOP / Gojek super-apps / 超级 App |
| India / 印度 | Play + App Store | Android-heavy | UPI deep-links / UPI 深链 |
| Australia/NZ / 澳新 | App Store + Google Play | iOS + Android | standard / 标准 |

**Club takeaway / 要点**: in China mainland you cannot rely on Google Play/FCM push — integrate domestic OEM push channels; in KR/JP prefer native social login (Kakao/LINE).
**要点**：中国内地不能依赖 Google Play/FCM 推送——须接国产厂商推送；韩/日优先本地社交登录（Kakao/LINE）。

## ⑮ Cultural note — face/photo sensitivity / 文化注记——人脸与照片敏感度

- **High sensitivity / 高敏感**: Japan, South Korea, Taiwan (China) — members dislike being photographed/identified without clear reason; default to non-face entry and ask before any group photo. / 日韩台——无明确理由不愿被拍/识别；默认非人脸入场，群拍前须问。
- **Moderate / 中**: China mainland, SEA, India — QR/face accepted if consent + benefit clear. / 中国内地、东南亚、印度——同意+收益明确则接受二维码/人脸。
- **Pool/change-room / 泳池更衣**: universally sensitive everywhere — reinforce HI-5 with cultural tact, not just law. / 泳池更衣全球敏感——以文化体贴而非仅法律强化 HI-5。

## One-page rollout summary table / 一页落地总表

| Dimension / 维度 | East Asia (cn/hk/tw/jp/kr) | SEA (sg/th/my/id/vn) | India / 印度 | ANZ / 澳新 |
|---|---|---|---|---|
| Payment / 支付 | wallets+cards / 钱包+卡 | QR wallets / 二维码钱包 | UPI | cards+BNPL |
| Message / 消息 | WeChat/LINE/Kakao | WhatsApp/LINE/Zalo | WhatsApp+SMS(DND) | email+SMS |
| Voltage / 电压 | 100–220V mixed | 220–240V | 230V | 230/240V |
| Holiday peak / 旺季 | CNY/Golden Week | Ramadan/Songkran | Diwali | year-end |
| Resilience / 韧性 | typhoon/quake | monsoon/typhoon | power-cut | remote/quake |
| Prep. strength / 预付强度 | medium–strong | low–medium | low–medium | low–medium |

> Use this table as the cover sheet for a new-market kickoff; drill into the section numbers above for detail.
> 本表作新市场启动封面；细节下钻至上述各节编号。

## What this file deliberately omits / 本文件刻意省略

- Regulatory four-pack detail — see `references/10`/`11`/`12` & `data/02`. / 监管四件套细节——见 `references/10`/`11`/`12` 与 `data/02`。
- Exact market-share percentages — only trends/ranges, verified via `tools/04`. / 精确市占率——仅趋势/区间，经 `tools/04` 核验。
- Deep tax-code & labour-law text — pointers only. / 深层税法与劳工法条——仅指引。
- Regulatory four-pack obligations — governed by `references/10`/`11`/`12` & `data/02`. / 监管四件套义务——由 `references/10`/`11`/`12` 与 `data/02` 管辖。
- Vendor/pricing specifics — see `data/03`–`data/04` & `data/15`. / 供应商/价格细节——见 `data/03`–`data/04` 与 `data/15`。

> **G13 tri-perspective note / 三视角注记**: Architect — design POS/locale/power/resilience to the per-market table, not a single global default. Operator — build onboarding + rostering around local IDs and labour rules. Member — experiences familiar payment, language, and channel norms with no confusing foreign defaults.
> **G13 三视角**：架构师——按各市场表格而非单一全球默认设计 POS/区域/电力/韧性；运营者——围绕本地 ID 与劳工规则做入驻与排班；会员——享有熟悉的支付、语言与渠道，无困惑的异域默认。
