# Site Selection Digital Scorecard / 选址数字化评分卡

> **Cluster / 集群**: B (software) + H (site & infra)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: ISP availability & power capacity 🔄 via `tools/04`; trade-area data sources 🔄 via `tools/04`; site-selection kernel in `data/09-algorithm-kernel-library.md`.
> **Cross-references / 交叉引用**: `data/09-algorithm-kernel-library.md` (site-selection kernel), `data/21-anti-pattern-library.md`, `templates/42` (franchise kit), `templates/46` (NOC).
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this scorecard to **digitally evaluate a candidate site** before signing a lease — catching IT-readiness and trade-area red flags that a broker's photos hide.
本评分卡用于签约前**数字化评估候选址**，揪出经纪照片藏住的 IT 就绪与商圈红旗。

- **FDMM gate / 等级闸门**: L1+ for any new club; L3+ adds weighted model + footfall sensors.
  L1+ 新店；L3+ 加加权模型与客流传感。
- **Trigger / 触发**: Lease negotiation starts; run before deposit paid.
  起租谈判；付定金前跑完。

---

## ② Prerequisites checklist / 前置清单

- [ ] Trade-area data sources identified (`data/09` kernel). / 商圈数据源已定。
- [ ] ISP & power pre-check booked with landlord. / 已与房东约 ISP&电力预检。
- [ ] Rent & revenue assumptions drafted. / 租金与营收假设已拟。
- [ ] Accessibility & competition mapped. / 可达性与竞争已绘。
- [ ] Building IT-readiness audit slot booked. / 楼宇 IT 就绪审计时档已约。
- [ ] Local comp set (similar clubs) listed. / 本地竞品组（同类店）已列。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Trade-area analysis worksheet / 商圈分析表

| Factor / 因子 | Source / 源 🔄 | Value / 值 |
|---|---|---|
| Population in 3km 3公里人口 | `____` (census/3rd-party) | `____` |
| Avg household income 户均收入 | `____` | `____` |
| Competitors within 2km 2公里竞品 | `____` map | `____` clubs |
| Complementary POI 互补POI | `____` (mall/office) | `____` |
| White-collar density 白领密度 | `____` | `____` |
| Daytime vs night pop 昼夜人口差 | `____` | `____` |

> **Guidance / 指引**: Pull POI & population from verified sources (`data/09` kernel); a broker's "busy area" is not data. Cross-check at least two independent sources.
> 指引：人口与 POI 取核验源；经纪说"地段旺"不是数据。至少两独立源交叉验。

### 3.2 Footfall & accessibility scoring / 客流与可达性评分

Score 1–5; weight as needed.
按 1–5 打分，按需加权。

| Item / 项 | Score / 分 | Note / 注 |
|---|---|---|
| Street-level footfall 临街客流 | `____` | `____` |
| Transit proximity 近公交 | `____` | `____` |
| Parking spaces 车位 | `____` | `____` |
| Visibility 可见度 | `____` | `____` |
| Walking convenience 步行便利 | `____` | `____` |

> **Micro-example / 微例**: Site B had high broker footfall but transit score 2/5 and only 4 parking; Site A scored 4/5 transit and 30 parks — chose A despite lower street count.
> 微例：B 经纪客流高但交通 2/5、车位 4；A 交通 4/5、车位 30——选 A 虽临街少。

### 3.3 Building IT-readiness audit / 楼宇 IT 就绪审计

:::dynamic-hook topic="isp-availability-long-lead" staleness="120d" action="tools/04" fallback="treat as unverified"
As of 2026-07: ISP fiber lead time in secondary APAC cities can be `____`–`____` weeks; ALWAYS confirm before lease — it is the #1 long-lead blocker.
截至 2026-07：APAC 二线城市 ISP 光纤交期可达 `____`–`____` 周；租前必核——头号长周期阻塞。
:::

| Check / 检查 | Spec / 规格 | Pass? / 过? |
|---|---|---|
| Power capacity 供电容量 | ≥ `____` kVA | [ ] |
| 3-phase available 三相电 | yes/no | [ ] |
| ISP availability ISP可用 | `____` providers | [ ] |
| ISP lead time ISP交期 | ≤ `____` wks | [ ] |
| Floor load 楼板承重 | ≥ `____` kg/m² | [ ] |
| HVAC headroom 空调余量 | `____` | [ ] |
| Riser/cabling rights 布线权 | yes/no | [ ] |

> **Red flag / 红线**: No 3-phase or ISP >8 weeks lead → delay opening or pay 4G backup forever.
> 红线：无三相或 ISP>8 周→延期开业或永久烧 4G 备线。

### 3.4 Rent-vs-revenue model hooks / 租收模型钩子

- Est. monthly revenue `____` (range, verify `data/15`). / 预估月营收（区间，data/15 核）。
- Est. monthly opex (ex-rent) `____`. / 预估月运营支出（除租）。
- Rent as % of revenue target < `____`%. / 租金占营收比目标 < `____`%。
- Breakeven month `____`. / 盈亏平衡月 `____`。
- Sensitivity: revenue -15% → still viable? / 敏感：营收-15%仍可行？

### 3.5 Weighted decision matrix / 加权决策矩阵

| Criterion / 标准 | Weight / 权 | Site A | Site B |
|---|---|---|---|
| Trade-area 商圈 | 30% | `____` | `____` |
| IT-readiness IT就绪 | 25% | `____` | `____` |
| Accessibility 可达 | 20% | `____` | `____` |
| Rent-efficiency 租效 | 15% | `____` | `____` |
| Competition 竞争 | 10% | `____` | `____` |
| **Total 总分** | **100%** | `____` | `____` |

> **What good looks like / 合格样**: Decision traces to the matrix, not "I liked the area". Dissent noted if override.
> 好样：决策可溯至矩阵，非"我喜欢这区"。推翻须记异议。

### 3.6 Red-flags list / 红旗清单

- [ ] ISP unavailable or >8wk lead. / ISP 不可用或 >8 周。
- [ ] Single-phase only, heavy equip needed. / 仅单相却需重设备。
- [ ] Floor load < equip need. / 承重不足。
- [ ] No redundant ISP path. / 无冗余 ISP。
- [ ] Landlord refuses cabling. / 房东拒布线。
- [ ] Rent >25% of modeled revenue. / 租金>建模营收25%。

> **Stop-line / 停手线**: Any red flag unmitigated = do not pay deposit.
> 停手线：红旗未化解≠别付定金。

### 3.7 Post-decision audit (lessons log) / 决策后复盘（经验档）

- What scored wrong & why. / 哪分错、为何。
- Actual vs modeled revenue at month 6. / 第 6 月实际 vs 建模营收。
- Feed back into `data/09` kernel weights. / 回灌 data/09 内核权重。

---

### 3.8 Sensitivity & scenario example / 敏感与情景示例

Model three cases; pick site robust to downside.
建三情景；选抗下行址。

| Scenario / 情景 | Revenue 营收 | Verdict 判 |
|---|---|---|
| Base 基准 | `____` | `____` |
| Optimistic 乐观 | `____` | `____` |
| Pessimistic 悲观 | `____` | `____` |

> **Micro-example / 微例**: Site B won on base case but lost money in pessimistic (ISP backup cost); Site A stayed green in all three → safer pick.
> 微例：B 基准胜但悲观亏（ISP 备线费）；A 三情景皆绿→更稳。

### 3.9 Decision sign-off / 决策签字

| Field / 项 | Content / 内容 |
|---|---|
| Selected site 选中址 | `____` (score `____`) |
| Rejected alt 落选 | `____` (reason `____`) |
| Conditions 条件 | ISP ≤`____`wk, rent ≤`____`% |
| Sign-off 签字 | `____` date `____` |

### 3.10 Site file archive / 址档归档

Keep one folder per candidate with: trade-area export, IT-readiness photos, ISP quote, signed checklist, decision sign-off (§3.9).
每候选址一档：商圈导出、IT 就绪照、ISP 报价、签核清单、决策签字（§3.9）。

> **Rule / 规则**: Archive even rejected sites — next expansion reuses the data.
> 规则：落选址也归档——下次扩店复用数据。

## ④ Common mistakes / 常见错误

1. Signing before ISP check → months of 4G. / 查 ISP 前签约→数月 4G。→ §3.3
2. Trusting broker footfall, not data. / 信经纪客流不信数据。→ §3.1 (`data/09`)
3. Ignoring 3-phase for sauna/equipment. / 忽略重设备三相。→ §3.3
4. No weighted matrix → emotional pick. / 无加权矩阵→凭感觉选。
5. Floor-load surprise at fit-out. / 装修才发现承重不够。→ §3.3
6. Rent > viable % ignored. / 忽略租金占比过高。→ §3.4
7. No post-audit → repeat error. / 无复盘→重复错。→ §3.7

---

## ⑤ Related files / 相关文件

- `data/09-algorithm-kernel-library.md` — site-selection kernel / 选址内核
- `templates/42-franchise-digital-kit.md` — franchise site onboarding / 加盟店上线
- `templates/46-hq-noc-dashboard-spec.md` — post-open monitoring / 开业后监测
- `data/21-anti-pattern-library.md` — fit-out surprises / 装修翻车
- `tools/04-dynamic-intelligence-retrieval.md` — 🔄 ISP/power verify / 核验

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (IT-readiness audit + weighted matrix), **Operator** (footfall/accessibility scoring + red-flag stop-line that prevents costly delays), and **Member** (a site that actually opens on time with reliable connectivity and easy access); the ISP long-lead hook is the single most opening-delay-saving check.
本模板覆盖**架构师**（IT 就绪审计+加权矩阵）、**运营者**（客流/可达评分+防延误红旗停手线）、**会员**（按时开业、联网稳、好到达）；ISP 长周期钩子是省最多开业延误的一检。
