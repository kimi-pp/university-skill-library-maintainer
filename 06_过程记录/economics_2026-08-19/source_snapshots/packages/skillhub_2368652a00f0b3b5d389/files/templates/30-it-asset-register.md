# IT Asset Register Template / IT 资产台账模板

> **Cluster / 集群**: C (Hardware) + I (IT governance & money)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify hardware/vendor-pricing facts every 180 days via `tools/04`; anchor links into `data/10` and `data/14` must be re-traced if those libraries change.
> **Cross-references / 交叉引用**: `data/10-hardware-fault-tree-library.md` · `data/13-inspection-and-maintenance-calendar.md` · `data/14-repair-scripts-and-sla-library.md` · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: A single printable sheet that lists every piece of IT/AV/security hardware in the club, so nothing is "lost in a drawer." Use it from day one of operations (FDMM L1), and keep it current as the only source of truth for warranty, location, and disposal. It feeds the maintenance calendar (`data/13`) and the repair/SLA library (`data/14`).
**中文**：一份可打印的清单，登记场馆每一件 IT/音视/安防硬件，避免「塞在抽屉里就没人记得」。运营第一天（FDMM L1）就用，并作为保修、位置、报废的唯一真相源。它喂给巡检日历（`data/13`）与报修/SLA 库（`data/14`）。

> 💡 If you only do ONE thing today: print this, walk the floor with a label gun, and fill in the first 10 rows. An asset you can't find is an asset you can't insure or repair.
> 💡 今天只做一件事：打印本表，拿标签枪走场，先填前 10 行。找不到的资产，既保不了险也修不了。

---

## ② Prerequisites / 前置条件

| # | Prerequisite / 前置 | Note / 说明 |
|---|---|---|
| 1 | Club short code + site id / 场馆缩写+门店号 | e.g. `FC-SH-01` (Shanghai site 1) / 如 `FC-SH-01`（上海 1 店） |
| 2 | Zone map / 分区图 | 14 zones from `references/02` — front desk, floor, studio, wet area… / 来自 `references/02` 的 14 区：前台、场区、团课室、湿区… |
| 3 | Label gun or QR stickers / 标签枪或二维码贴 | For the QR-labeling SOP below / 用于下方二维码贴标 SOP |
| 4 | Vendor contact sheet / 供应商联系表 | Name + hotline + account ID per device / 每台设备的名称+热线+账号 |
| 5 | FDMM level known / 已知 FDMM 等级 | L1 runs this manually; L3+ can sync to a CMDB / L1 手填；L3+ 可同步 CMDB |

---

## ③ THE TEMPLATE / 模板正文

### #asset-id-scheme Asset ID Scheme / 资产编号规则

**English**: `FC-<SITE>-<CATEGORY>-<SEQ>` — Category is the C1–C12 code from `data/10`/`references/07`. Example: `FC-SH-01-C2-0007` = Shanghai site 1, access gate, 7th unit.
**中文**：`FC-<门店>-<类别>-<序号>`——类别取 `data/10`/`references/07` 的 C1–C12 码。例：`FC-SH-01-C2-0007` = 上海 1 店、闸机、第 7 台。

### #register-columns Register Columns (fill one row per device) / 台账列（每设备一行）

| Field / 字段 | Bilingual label / 双语标签 | Example / 示例 | Rule / 规则 |
|---|---|---|---|
| Asset ID | 资产编号 | FC-SH-01-C2-0007 | per scheme above / 按上规则 |
| Category | 类别 (C1–C12) | C2 Access gate / 闸机 | link `data/10#C2` |
| Name / Model | 名称/型号 | Turnstile T1 | — |
| Location zone | 所在分区 | Z03 Studio / 团课室 | `references/02` zone |
| Serial No. | 序列号 | SN88…21 | photo it / 拍照留存 |
| Purchase date | 购入日 | 2026-03-12 | — |
| Price range | 价格区间 🔄 | ¥3k–8k | ranges only / 仅区间 |
| Warranty end | 保修到期 | 2028-03-12 | + 🔄 reminder / 加提醒 |
| Vendor & hotline | 厂商与热线 | BrandX 400-… | 24/7? / 是否 24/7 |
| Status | 状态 | Active/Spare/Repair/Retired / 在用/冷备/维修/退役 | — |
| Next maintenance | 下次维护 (link) | `data/13` monthly | anchor / 锚点 |

> 🔄 **Reminder rule / 提醒规则**: Set a calendar alert 60 days before `Warranty end`. At 30 days, email the vendor to confirm EOL/migration path (see `data/14` EOL clause). Warranty windows are volatile — re-verify the vendor's current policy via `tools/04` at each renewal.
> 🔄 **提醒规则**：`保修到期`前 60 天设日历提醒；前 30 天邮件厂商确认 EOL/迁移路径（见 `data/14` EOL 条款）。保修窗口易变——每次续约经 `tools/04` 复核厂商现行政策。

:::dynamic-hook topic="hardware-price-ranges-apac-2026" staleness="180d" action="tools/04" fallback="treat stored ranges as unverified"
Per-category price ranges (C1 printer ≈ ¥300–1.5k, C10 network ≈ ¥3k–30k/club, C11 IoT ≈ ¥50–2k/node, C12 wearable ≈ ¥5–800) are directional 2026-07 snapshots; re-quote before procurement. / 各类价格区间仅作 2026-07 方向参考，采购前重新询价。
:::

### #category-reference C1–C12 Category Reference / C1–C12 类别速查

| Code | Category / 类别 | Fault anchor / 故障锚点 |
|---|---|---|
| C1 | Printers & scanners / 打印机扫描仪 | `data/10#C1` |
| C2 | Access gates & door control / 闸机门禁 | `data/10#C2` |
| C3 | Smart lockers / 智能储物柜 | `data/10#C3` |
| C4 | Cardio equipment / 有氧器械 | `data/10#C4` |
| C5 | Strength & smart strength / 力量器械 | `data/10#C5` |
| C6 | Body analyzers & posture / 体测体态 | `data/10#C6` |
| C7 | POS & payment HW / 收银支付硬件 | `data/10#C7` |
| C8 | Signage & studio AV / 标牌团课 AV | `data/10#C8` |
| C9 | CCTV & security HW / 监控安防 | `data/10#C9` |
| C10 | Network & server closet / 网络机房 | `data/10#C10` |
| C11 | IoT sensors / IoT 传感器 | `data/10#C11` |
| C12 | Wearables & club devices / 可穿戴发放 | `data/10#C12` |

### #qr-labeling-sop QR-Labeling SOP / 二维码贴标 SOP

1. **Print** a durable QR sticker per asset showing the Asset ID + a short URL to this register row. / 每件资产打印耐用的二维码贴，含资产编号 + 本行短链。
2. **Stick** it where staff can scan without moving the device (back of gate, side of printer). / 贴在员工可扫且不移动设备处（闸机背面、打印机侧面）。
3. **Scan-test** with a phone; if it opens the row, label is good. / 用手机扫码测试，能打开该行即合格。
4. **Re-label** on repair/replace so the ID stays stable even if the box changes. / 维修/换新时重贴，使编号稳定即使设备更换。

### #annual-stocktake Annual Stocktake Procedure / 年度盘点流程

| Step / 步骤 | What / 做什么 | Pass / 通过 |
|---|---|---|
| 1 | Print full register / 打印全表 | one sheet per club / 每店一张 |
| 2 | Walk every zone / 走遍每区 | tick each ID physically / 逐件实物打勾 |
| 3 | Flag mismatches / 标差异 | missing = investigate / 缺失即查 |
| 4 | Update status / 更新状态 | repair/retire logged / 维修退役入档 |
| 5 | Sign & date / 签字日期 | owner + IT contact / 老板+IT 对接 |

### #disposal-record Disposal Record (one row per retired asset) / 报废记录

| Asset ID | Retire date | Reason / 原因 | Method / 方式 | Data wiped? / 数据清除 | Witness / 见证人 |
|---|---|---|---|---|---|
| FC-SH-01-C2-0007 | 2029-04-01 | EOL | recycle / 回收 | Yes/是 | ___ |

> For devices holding data (C6 analyzers, C7 POS, C9 NVR, C12), wipe per `references/16#j-offboarding-checklist` before disposal. A dumped drive is a breach (link `data/21#ap-008-card-numbers-spreadsheet`).
> 含数据的设备（C6 体测、C7 收银、C9 录像机、C12）报废前按 `references/16#j-offboarding-checklist` 清除。丢弃硬盘即泄露（联 `data/21#ap-008`）。

---

## ④ Common Mistakes / 常见错误

- **No register at all** → at audit/renewal you can't prove what you own. → `data/21#ap-024-offboarding-checklist` (lost-track lineage).
- **Gray-import critical gear not tracked** → no local RMA when it dies Saturday. → `data/21#ap-016-gray-import-critical`.
- **Skip the UPS line item** → Saturday outage, manual buzz for 400 members. → `data/21#ap-010-skip-ups`.
- **Serial not photographed** → vendor disputes warranty. → `data/14` pre-call evidence rule.

---

## ⑤ Related Files / 相关文件

- `data/10-hardware-fault-tree-library.md` — fault anchors per category. / 各类故障锚点。
- `data/13-inspection-and-maintenance-calendar.md` — next-maintenance cadence. / 下次维护节奏。
- `data/14-repair-scripts-and-sla-library.md` — warranty vs paid-repair math. / 保内 vs 付费维修算术。
- `references/07-hardware-landscape-and-vendors.md` — C1–C12 buy guides. / C1–C12 选购指南。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: The register is the physical inventory layer of FDMM; every ID links to a `data/10` fault anchor and a `data/13` maintenance cadence, so prevention and firefighting share one map.
**运营者 / Operator**: A printable sheet a rookie can fill in during a 1-hour walk — no IT degree needed; it is also the operator's evidence for warranty claims and insurance.
**会员 / Member**: Accurate asset tracking means faster repair of gates/POS/cameras and safer life-safety gear — member experience and safety protected by boring bookkeeping, not luck.
