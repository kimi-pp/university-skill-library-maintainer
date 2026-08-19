# 16 · Digital Signage & Studio AV Plan / 数字标牌与团课 AV 规划模板

> **Cluster / 集群**: C (Hardware C8) + H (Brand) · Template / 模板 · System-Building tier (FDMM L2→L3)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Screen specs, music-licensing & noise rules re-verify every 90 days via `tools/04`; content-rights are volatile.
> **Cross-references / 交叉引用**: `references/07-hardware-landscape-and-vendors.md` (C8 AV) · `references/02-club-formats-and-zones.md` (zone map) · `references/08-network-and-infrastructure.md` (PoE/power) · `data/13-inspection-and-maintenance-calendar.md` · `data/21-anti-pattern-library.md#ap-022-digitize-broken-process`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用（FDMM 闸门）

**Purpose / 用途**: A plan to place, spec, schedule and maintain lobby/studio screens and class AV — branding + info, not noise pollution.
**用途 / 中文**：规划大堂/教室屏幕与团课 AV 的布置、选型、排程与维护——品牌+信息，而非噪音污染。

**When to use / 适用场景**:
- You want class timetables, promos and wayfinding on screens — L2→L3. / 想在屏上放课表、促销、导视——L2→L3。
- You run group classes needing mics/amp/projector. / 跑需麦/功放/投影的团课。
- **FDMM gate / 闸门**: Signage is nice-to-have; never let it outrank life-safety spend. / 标牌是加分项；绝不挤占人身安全预算。
- **Volume gate / 音量闸门**: Studio/music volume must meet local noise/complaint rules (🔄 `tools/04`). / 教室/音乐音量须符合本地噪音/投诉规则。

---

## ② Prerequisites checklist / 前置清单

- [ ] Zone map & screen spots from `references/02-club-formats-and-zones.md`. / 区域图与屏位取自 `references/02`。
- [ ] Power + network drops planned (`references/08` D2). / 电源与网口已规划（`references/08`）。
- [ ] Music rights bundled for market (音集协/JASRAC/OneMusic/COMPASS). / 各市场音乐版权已捆绑。
- [ ] Content owner + update cadence assigned. / 内容负责人与更新节奏已定。
- [ ] Maintenance rota linked to `data/13-inspection-and-maintenance-calendar.md`. / 维护轮值关联 `data/13`。
- [ ] Noise/complaint rule per market confirmed (🔄). / 各市场噪音/投诉规则已确认（🔄）。

---

## ③ The template / 模板正文

### 3.1 Screen placement map worksheet by zone / 分区域屏幕布置表

> **Link / 关联**: zone definitions in `references/02-club-formats-and-zones.md` (`#zone-reception`, `#zone-gate`, `#zone-gymfloor`, `#zone-groupclass`, `#zone-facade` …). / 区域定义见 `references/02`。
> **What good looks like / 合格标准**: each screen has one clear job; no two screens fight for attention in one sightline. / 每屏一个清晰任务；同一视线无两屏抢注意力。
> **Red flag / 红旗**: a screen in a wet zone without IP rating; a screen blocking fire egress. / 湿区屏无防护；屏挡消防疏散。

| Zone / 区 | Screen job / 屏任务 | Size / 尺寸 | Brightness / 亮度 | Network / 网络 | Notes / 注 |
|---|---|---|---|---|---|
| Reception / 前台 | Timetable + promo / 课表+促销 | 43–55" | ≥500 nit | PoE/Wi-Fi | Eye-level / 平视 |
| Gate / 闸机 | Welcome + capacity / 欢迎+满馆 | 32–43" | ≥400 nit | PoE | No block / 不挡 |
| Gym floor / 器械 | Orientation / 导视 | 43" | ≥500 nit | Wi-Fi | Away from sweat / 远汗 |
| Group class / 团课 | Instructor + lyrics / 教练+歌词 | 55–75" | ≥400 nit | HDMI/AP | HDMI-CEC / 自动开关 |
| Façade / 门头 | Brand / 品牌 | Outdoor | High | — | Permit / 报批 |

### 3.2 Content calendar template / 内容日历模板

| Daypart / 时段 | Content / 内容 | Owner / 负责人 | Refresh / 更新 |
|---|---|---|---|
| Morning / 早 | Class timetable + tips / 课表+贴士 | Coach | Daily / 日 |
| Midday / 中 | Promo + member story / 促销+会员故事 | Mktg | Weekly / 周 |
| Evening / 晚 | Capacity + social proof / 满馆+口碑 | Mktg | Daily / 日 |
| Event / 活动 | Campaign creative / 活动素材 | Mktg | Per event / 按活动 |

### 3.3 CMS scheduling rules (timezone trap warning) / CMS 排程规则（时区陷阱）

> **Timezone trap / 时区陷阱**: If your CMS is hosted in a different timezone (e.g. regional HQ in another market), schedule times are interpreted in the CMS timezone, NOT the club's local time. A "08:00 promo" may fire at 08:00 HQ time = wrong local time. / 若 CMS 托管在异时区（如区域总部在另一市场），排程按 CMS 时区而非场馆本地时区解释。"08:00 促销"可能按总部 08:00 触发=本地错时。
- [ ] Set CMS timezone = club local timezone per screen. / CMS 时区=各屏本地时区。
- [ ] Proof-of-play log to verify actual play time. / 播放证明日志核验实际播放时间。
- [ ] Offline cache so a network blip doesn't blank the screen. / 离线缓存防断网黑屏。
- [ ] Quiet-hours: no promo audio in late/early windows per market. / 静默时段：按市场深夜/清晨不播促销音。

### 3.4 Hardware spec tiers / 硬件规格分级

| Tier / 级 | Use / 用途 | Spec / 规格 | Cost band 🔄 / 区间 |
|---|---|---|---|
| Basic / 基础 | Info board / 信息板 | 43" FHD, SoC player | ¥1k–4k/screen |
| Standard / 标准 | Timetable + promo | 50" FHD, CMS license | ¥3k–8k/screen |
| Studio / 教室 | Instructor + AV | 65"+ 4K + mic/amp | ¥8k–30k/room |
| Outdoor / 门头 | Façade | High-bright, permit | ¥10k+/screen |

> **Rule / 规则**: brightness must beat gym ambient light; PoE simplifies wiring (`references/08`). / 亮度须压过环境光；PoE 简化布线（`references/08`）。

### 3.5 Volume / noise compliance note (🔄) / 音量合规注记

:::dynamic-hook topic="apac-gym-noise-rule-2026" staleness="180d" action="tools/04" fallback="treat as unverified"
As of 2026-07: APAC cities set venue noise limits (dB(A)) and neighbour-complaint thresholds; group-class music often capped. Exact limit per district must be verified via tools/04 before fixing speaker levels.
截至 2026-07：亚太城市设场所噪音上限（dB(A)）与邻避投诉阈值；团课音乐常受限。各区确切上限经 tools/04 核验后再定音量。
:::

- [ ] Measure ambient + class peak with a dB meter; stay under local limit. / 用分贝计测环境+峰值，守住本地上限。
- [ ] Bass/sub controlled to avoid neighbour complaint. / 低频受控防邻避投诉。
- [ ] Studio doors/closing damped; signage shows "quiet zone" where needed. / 教室门/隔断吸音；必要处标"静音区"。

### 3.6 Maintenance rota (link `data/13`) / 维护轮值

- [ ] Weekly: screen clean, proof-of-play check. / 周：擦屏、查播放证明。
- [ ] Monthly: firmware + content sync test. / 月：固件+内容同步测试。
- [ ] Quarterly: audio level re-measure vs noise rule. / 季：按噪音规则重测音量。
- [ ] Log all in `data/13-inspection-and-maintenance-calendar.md`. / 全部记入 `data/13`。

---

### 3.7 Worked timezone example / 时区实例

- HQ CMS in Singapore (UTC+8); club in Tokyo (UTC+9). / 总部 CMS 新加坡(UTC+8)；场馆东京(UTC+9)。
- Wrong / 错: schedule "18:00 promo" in CMS tz → fires 18:00 SGT = 19:00 JST (1h late). / 按 CMS 时区排"18:00"→新加坡 18:00 = 东京 19:00（晚 1 小时）。
- Right / 对: set screen tz = Asia/Tokyo → fires 18:00 JST exactly. / 屏时区设东京 → 东京 18:00 准点播。
- Proof / 验证: proof-of-play log shows local 18:00; quiet-hours respected (no audio 22:00–08:00). / 播放证明显示本地 18:00；守静默时段（22:00–08:00 无音）。

### 3.8 Launch checklist / 上线清单

- [ ] Screen job per zone clear; no two fight in one sightline (§3.1). / 每屏任务清晰；同视线无两屏抢注意力（§3.1）。
- [ ] CMS timezone = local per screen; proof-of-play verifies (§3.3). / CMS 时区=各屏本地；播放证明核验（§3.3）。
- [ ] Brightness beats gym ambient; PoE wired (`references/08`). / 亮度压过环境光；PoE 布线（references/08）。
- [ ] Music rights bundled for market; no unlicensed tracks. / 各市场音乐版权已捆绑；无未授权曲。
- [ ] Volume measured under local limit; quiet-hours set (🔄). / 音量低于本地上限；静默时段已设（🔄）。
- [ ] Maintenance rota live in `data/13`. / 维护轮值已在 `data/13` 生效。

### 3.9 Content governance note / 内容治理注记

- [ ] Approver: every promo creative signed off before push (no orphan auto-post). / 审批：每条促销素材推送前签字（无孤儿自动发）。
- [ ] Cadence: timetable daily, promo weekly, campaign per event. / 节奏：课表日更、促销周更、活动按场次。
- [ ] Takedown: wrong/ expired creative pulled within 4h. / 下架：错/过期素材 4h 内撤。
- [ ] Localisation: copy in club's language(s); no untranslated placeholder. / 本地化：按场馆语言；无未译占位。
- [ ] Accessibility: text large enough at viewing distance. / 可达性：文字在观看距离足够大。

### 3.10 Quiet-hours example / 静默时段示例

- China / 中国: no promotional audio 22:00–08:00 local. / 本地 22:00–08:00 无促销音。
- Japan / 日本: residential neighbour sensitivity high; cap class music dB. / 住宅邻避敏感高；团课音乐限 dB。
- ANZ / 澳新: council noise order may start 21:00 on weekdays. / 市议会噪音令工作日或自 21:00。
- Rule / 规则: verify exact window per district via `tools/04` (🔄). / 各行政区确切时段经 tools/04 核验（🔄）。

## ④ Common mistakes (anti-patterns) / 常见错误（反模式）

- `data/21#ap-022-digitize-broken-process` — auto-pushing promos to screens with no content owner. / 无内容负责人却自动推促销上屏。
- `data/21#ap-023-untrained-system-promo` — staff can't update a blank/error screen. / 员工不会修黑屏/报错屏。
- Wrong timezone CMS firing promos at 03:00 local (see §3.3). / CMS 时区错致凌晨 3 点播促销（见 §3.3）。
- Music played without bundled rights → takedown/fine. / 未捆绑版权播音乐→下架/罚款。

---

## ⑤ Related files / 相关文件

- `references/07-hardware-landscape-and-vendors.md` (C8 AV). / AV 硬件。
- `references/02-club-formats-and-zones.md` — zone touchpoints. / 区域触点。
- `references/08-network-and-infrastructure.md` — PoE & power. / PoE 与电源。
- `data/13-inspection-and-maintenance-calendar.md` — maintenance log. / 维护台账。
- `references/06-software-landscape-apac-vendors.md` (§17 signage CMS). / 标牌 CMS。

---

## ⑥ G13 tri-perspective note / G13 三视角覆盖说明

This template serves **Architect** (placement map + spec tiers + CMS timezone rule), **Operator** (content calendar + maintenance rota + volume control), and **Member** (clear wayfinding, useful timetable, calm environment, no noise intrusion); the timezone trap and noise-compliance clauses protect the member's experience and the operator's neighbour relations — no orphaned touchpoint.
本模板覆盖**架构师**（布置图+规格分级+CMS 时区规则）、**运营者**（内容日历+维护轮值+音量控制）、**会员**（清晰导视、实用课表、安静环境、无噪音侵扰）；时区陷阱与音量合规守护会员体验与运营者邻里关系——无孤儿触点。
