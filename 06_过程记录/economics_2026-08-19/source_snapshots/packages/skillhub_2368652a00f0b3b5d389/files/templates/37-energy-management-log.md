# Energy Management Log & Optimization / 能耗管理与优化日志

> **Cluster / 集群**: I (IT governance & money) + T (Physical security)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify electricity tariff and HVAC/IoT pricing every 180 days via `tools/04`; tariff structures are market-specific — verify via `tools/05`.
> **Cross-references / 交叉引用**: `references/08-network-and-infrastructure.md` · `references/16-security-operations-and-emergency.md` · `data/20-micro-details-ledger.md` · `tools/04-dynamic-intelligence-retrieval.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: Track where the club's electricity goes, set a kWh/sqm baseline, and align HVAC with the class calendar so you're not heating an empty studio. For pool clubs, add the heater/pump load. Turn "the bill is huge" into a numbered optimization plan with ROI.
**中文**：追踪场馆电去哪了，定 kWh/㎡ 基线，把空调排程对齐课表——别给空团课室供暖。泳池店加加热器/水泵负荷。把「电费好贵」变成带 ROI 的优化清单。

> 💡 HVAC is usually the biggest club load. Aligning it to the class calendar (not 24/7 blast) is the single fastest payback — often <1 yr (range, market-dependent 🔄).
> 💡 空调通常是场馆最大负荷。对齐课表（而非全天猛吹）是回报最快的一项——常 <1 年（区间，随市场 🔄）。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | Meter reading access / 可读表 | or IoT sub-meter link / 或 IoT 分表 |
| 2 | Floor area / 面积 | sqm of club / 场馆㎡ |
| 3 | Class calendar / 课表 | for HVAC alignment / 空调对齐 |
| 4 | Tariff sheet / 电价单 | per market 🔄 / 随市场 |

---

## ③ THE TEMPLATE / 模板正文

### #meter-sheet Meter Reading Sheet / 读表表

| Date / 日期 | Reading / 读数 (kWh) | Δ use / 用量 | ¥ cost 🔄 | Note / 备注 |
|---|---|---|---|---|
| ____ | ______ | ______ | ¥__ | ______ |

> 🔄 Tariff ranges shift with market and season — re-quote via `tools/04`. Log the same time each period for a clean baseline.
> 🔄 电价区间随市场季节变——经 `tools/04` 重核。每期同时间读，得干净基线。

### #baseline Baseline vs Range / 基线与区间

| Metric / 指标 | Your value / 你的值 | Typical range 🔄 / 典型区间 | Verdict / 判定 |
|---|---|---|---|
| kWh / sqm / month | __ | market-dependent / 随市场 | ok/high / 正常/偏高 |
| HVAC share / 空调占比 | __% | 40–60% typical / 通常 | __ |
| After-hours load / 非营业负荷 | __% | <10% target / 目标<10% | __ |

### #hvac-align HVAC ↔ Class Calendar Alignment / 空调↔课表对齐

| Zone / 区 | Class time / 上课 | HVAC on / 开 | HVAC off / 关 | Waste? / 浪费 |
|---|---|---|---|---|
| Studio A / 团课室A | 18:00–21:00 | 17:30 | 21:15 | __ |
| Floor / 场区 | 07:00–23:00 | 06:45 | 23:15 | __ |
| Unused zone / 空区 | — | off / 关 | — | __ |

> Set HVAC to pre-cool/warm 30 min before class, off 15 min after. Never run full blast in an empty zone (→ `data/21#ap-056` spirit: don't light/heat what you don't use).
> 课前30分预冷/暖、课后15分关。空区绝不全天猛吹（→ `data/21#ap-056` 精神：不用就不供）。

### #pool-addendum Pool-Club Addendum / 泳池店附录

| Load / 负荷 | Reading / 读数 | Schedule / 排程 | Save? / 可省 |
|---|---|---|---|
| Heater / 加热器 | __ kWh | only open hrs / 仅开放时 | __ |
| Pump / 水泵 | __ kWh | variable speed / 变频 | __ |
| Dehumidifier / 除湿 | __ kWh | tie to occupancy / 随人 | __ |

### #quick-win Quick-Win Checklist (10 items) / 速赢清单 10 项

- [ ] HVAC aligned to class calendar / 空调对齐课表
- [ ] Unused zones off / 空区关停
- [ ] LED retrofit done / 换 LED
- [ ] Motion sensors in low-traffic areas / 低流区感应
- [ ] Setpoint 1–2°C relaxed / 设定宽松1–2度
- [ ] Pool pump variable-speed / 水泵变频
- [ ] Off-peak laundry/charging / 错峰洗衣充电
- [ ] Sleep mode on signage/AV / 标牌AV休眠
- [ ] Door air-curtains maintained / 风幕维护
- [ ] Monthly meter review assigned / 月读表到人

### #roi-mini-case ROI Mini-Case for Retrofit / 改造 ROI 小案例

| Investment / 投入 | Cost range 🔄 / 费用区间 | Annual saving / 年省 | Payback / 回收 |
|---|---|---|---|
| HVAC schedule + sensors / 空调排程+感应 | ¥__–__ | ¥__/y | ~__ mo |
| LED retrofit / 换LED | ¥__–__ | ¥__/y | ~__ mo |

> Ranges only (G8). Use `tools/06` three-scenario ROI for any spend >¥100k (Iron Law 6). Honesty: savings are directional until you log 90 days of meters.
> 仅区间（G8）。超10万投入用 `tools/06` 三情景 ROI（铁律6）。诚实：未记90天表前节省仅方向性。

---

## ④ Common Mistakes / 常见错误

- **HVAC 24/7 blast** → biggest avoidable bill. → `data/21#ap-056` spirit.
- **No baseline** → can't prove savings. → log meters first.
- **Ignore pool pump** → silent kWh drain. → pool addendum.
- **Tariff not verified** → wrong ROI math. → `tools/04`.

---

## ⑤ Related Files / 相关文件

- `references/08-network-and-infrastructure.md` — UPS/rack power context. / UPS机柜电上下文。
- `references/16-security-operations-and-emergency.md` — `#t-monthly-physical-checklist`.
- `data/20-micro-details-ledger.md` — energy micro-details. / 能耗微细节。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: Energy is a measurable OPEX layer of FDMM; HVAC↔calendar alignment is a low-cost, high-return control that feeds the ROI discipline (Iron Law 6).
**运营者 / Operator**: A simple meter sheet + 10-item checklist lets a non-technical owner cut cost this month — no energy engineer required.
**会员 / Member**: Efficient clubs can hold or lower membership prices and keep a comfortable, safe environment (pool temp, air quality) without waste — member experience protected, not sacrificed.
