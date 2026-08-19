# Case 06 · Swim Club with Pool IoT — Water Quality & Manual Redundancy / 案例06 · 泳馆（池 IoT）：水质与人工冗余

> **Cluster / 集群**: A (formats) · C (hardware) · J (resilience) · F (compliance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: minors' data rule passes `tools/05`; humidity-rated hardware passes `tools/04`.
> **Cross-references / 交叉引用**: `references/02-club-formats-and-zones.md#format-swim` · `references/12-biometrics-and-cctv.md` (HI-5) · `playbooks/03-24h-unmanned-club.md` (HI-2 pattern) · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: 🔄 humidity-proof device ratings vary by brand — verify via `tools/04` before poolside purchase. / 标注 🔄 的防湿设备等级因品牌而异——池边采购前经 `tools/04` 核验。

> **Honesty preamble / 诚实声明**: This is an archetypal composite case built from common industry patterns for teaching purposes — not a claimed real company. Numbers are directional. / 本案例为教学用途的原型合成案例，非真实公司；数字为方向性参考。

---

## ① Context card / 背景卡 {#case-06-context}

- **Format / 业态**: Swim club with pool, 1,200 sqm, ~850 members (40% minors), lane + lessons. / 带泳池泳馆，1200 平米，约 850 会员（40% 未成年），泳道 + 课程。
- **Market / 市场**: Malaysia (KL). / 马来西亚（吉隆坡）。
- **FDMM start / 起点等级**: L2→L3 (water sensors + anti-drowning assist). / L2→L3（水质传感 + 防溺水辅助）。
- **Team / 团队**: owner + lifeguard team (4) + 2 swim coaches + 1 maintenance. / 老板 + 救生员队（4）+ 2 教练 + 1 维保。
- **Annual IT envelope / 年 IT 预算带**: directional RM120k–RM260k opex + RM200k–RM400k capex (sensors + IP65 kiosks + CCTV). / 方向性经营支出 12–26 万林吉特 + 资本开支 20–40 万（传感+IP65一体机+CCTV）。
- **Why this case / 为何选它**: Life-safety (HI-2) water monitoring + minors' data (HI-1) + humidity kills electronics — the redundancy textbook. / 人身安全（HI-2）水质监控 + 未成年人数据（HI-1）+ 湿气毁电子——冗余教科书。

---

## ② The starting mess / 起初的一团乱 {#case-06-mess}

- Water quality was tested by hand twice a day; a long weekend gap let chlorine drift and members complained of eye irritation. / 水质靠每天手测两次；一个长周末的空档让余氯漂移，会员投诉眼睛刺痛。
- Two consumer tablets used for lane booking died within 4 months — poolside humidity (95%+) killed them. / 两台消费级平板用于泳道预约，4 个月内全坏——池边湿度（95%+）弄死了它们。
- Kids' class roster with birthdates sat in a plain Excel on a shared laptop — minors' data exposed to any staff. / 儿童课名册（含出生日期）躺在共享笔记本的明文 Excel 里——未成年人数据对任一员工完全敞开。
- Underlying cause / 根因: the club trusted single points (one sensor idea, consumer gear, plain Excel) with no redundancy — direct HI-2/HI-1 violation. / 根因：场馆信任单点（单一传感设想、消费级设备、明文 Excel）无冗余——直接违 HI-2/HI-1。

---

## ③ The journey (phase-by-phase) / 转型之路（分阶段） {#case-06-journey}

### Phase 1 — Water sensors WITH manual redundancy (Month 0–3) / 水质传感 + 人工冗余 {#case-06-journey-p1}
- Installed free-chlorine/pH/turbidity sensors on IoT VLAN per `references/02-club-formats-and-zones.md#zone-pool`; KEPT manual test 2×/day as legal + safety redundancy (HI-2). / 按 `references/02#zone-pool` 在 IoT VLAN 装余氯/pH/浊度传感；保留每天 2 次手测作法律 + 安全冗余（HI-2）。
- Reasoning / 理由: HI-2 — sensor is assist, manual test is the mandated backup; sensor drift must be caught by a human. / HI-2——传感仅辅助，手测是法定备份；传感漂移须由人抓出。
- Library used / 用到的库: `references/02#zone-pool` · `references/16` (safety) · `data/13-inspection-and-maintenance-calendar.md`. / 用到的库：`references/02#zone-pool` · `references/16`（安全）· `data/13`（巡检日历）。

### Phase 2 — Humidity-proofing electronics (Month 2–5) / 电子防湿 {#case-06-journey-p2}
- Replaced consumer tablets with IP65-rated booking kiosks + conformal-coated boards; dehumidifier + airflow redesign around the desk. / 消费平板换成 IP65 级预约一体机 + 涂覆板；加湿器 + 桌面气流重设计。
- Anti-drowning AI camera assist-only, separate CCTV network, lifeguard mandatory (HI-2). / 防溺水 AI 摄像仅辅助、走独立 CCTV 网、救生员强制（HI-2）。
- Library used / 用到的库: `references/07-hardware-landscape-and-vendors.md` (IP65) · `references/12` (CCTV) · `tools/04` (pricing). / 用到的库：`references/07`（IP65）· `references/12`（CCTV）· `tools/04`（价格）。

### Phase 3 — Minors' data compliance (Month 3–6) / 未成年人数据合规 {#case-06-journey-p3}
- Moved kids' roster to access-controlled store, parental consent captured, birthdate minimized to age-band (HI-1, HI-8). / 儿童名册迁入受控存储、采监护人同意、出生日期最小化为年龄段（HI-1、HI-8）。
- Lifeguard scheduling automated from attendance + cert expiry. / 救生员排班按出勤 + 证照到期自动排。
- Library used / 用到的库: `tools/05` (minors' law) · `references/10-apac-compliance-east-asia-oceania.md` · `data/02-regulation-traceability-index.md`. / 用到的库：`tools/05`（未成年法）· `references/10`（东亚大洋洲合规）· `data/02`（法规溯源）。

### Phase 4 — Lifeguard scheduling & alerting (Month 6–10) / 救生员排班与告警 {#case-06-journey-p4}
- Sensor out-of-range → dashboard + SMS to maintenance + manual-test prompt; cert-expiry alert 30 days ahead. / 传感越界 → 看板 + 短信维保 + 手测提示；证照到期提前 30 天告警。
- Library used / 用到的库: `references/16` (emergency) · `data/20-micro-details-ledger.md`. / 用到的库：`references/16`（应急）· `data/20`（微细节）。

:::dynamic-hook topic="my-minors-data-rule-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
Malaysia's personal-data treatment of minors (PDPA application to children) is interpreted per current guideline; verify storage & consent rule via `tools/05` before collecting any minor's birthdate. / 马来西亚对未成年人个人数据（PDPA 对儿童的适用）按现行指南解释；采集任何未成年人出生日期前经 `tools/05` 核验存储与同意规则。
:::

---

## ④ What went wrong / 踩过的坑 {#case-06-setbacks}

### Setback 1 — Humidity killed two tablets / 湿气毁了两台平板
- Consumer tablets by the pool died in 4 months; lane booking went offline during peak lessons, frustrating parents. / 池边消费平板 4 个月报废；高峰课程时泳道预约离线，家长抓狂。
- Fix / 修复: IP65 kiosks + conformal coating + dehumidification; zero device loss in next 12 months (directional). / 换 IP65 一体机 + 涂覆 + 除湿；其后 12 个月零设备损失（方向性）。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-humidity-device-loss` (consumer gear poolside). / 对应反模式：池边用消费级设备。

### Setback 2 — Sensor false-normal caught by manual test / 传感假正常被手测抓出
- A fouled chlorine probe reported "normal" for a day; the manual 2×/day test caught the real low-chlorine state before members swam. / 一只脏污的余氯探头报了「正常」一整天；每天 2 次手测在会员下水前抓出了真实的低余氯。
- Fix / 修复: added probe auto-clean cycle + monthly calibration + manual test kept as mandated backup; alert on sensor/manual gap. / 加探头自清洁 + 月校准 + 保留手测为法定备份；传感/手测差异即告警。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-sensor-false-normal` (trust-sensor-only). / 对应反模式：唯信传感。

---

## ⑤ Outcomes (6–18 months later, directional) / 结果（方向性） {#case-06-outcomes}

- Water incidents (irritation complaints): down directional 60–85% with sensor + manual double net. / 水质事件（刺痛投诉）：传感 + 手测双网方向性降 60–85%。
- Device loss: 2 tablets/4mo → ~0/12mo after IP65 + dehumidify. / 设备损失：2 台/4 月 → IP65 + 除湿后约 0/12 月。
- Minors' data exposure: from plain Excel to access-controlled, consent-logged, age-band only. / 未成年人数据暴露：明文 Excel → 受控 + 同意留痕 + 仅年龄段。
- Lifeguard coverage: cert-expiry alerts prevented 2 lapsed-cert gaps. / 救生员覆盖：证照到期告警避免 2 次证照空窗。
- Honest caveat / 诚实提示: manual test is a legal floor in many markets — sensors ADD safety, never replace it (HI-2). / 手测在许多市场是法律底线——传感是「加」安全，绝不「替」安全（HI-2）。

---

## ⑥ Transferable lessons / 可迁移经验 {#case-06-lessons}

- Pool sensors are assist; keep mandated manual testing as redundancy (HI-2). / 池传感仅辅助；保留法定手测作冗余（HI-2）。
- Never trust a single sensor — manual cross-check catches false-normal. / 绝不唯信单一传感——人工交叉抓假正常。
- Poolside electronics must be IP65+ and dehumidified; consumer gear dies. / 池边电子须 IP65+ 且除湿；消费级必死。
- Minors' data: access-control + parental consent + minimize to age-band (HI-1/HI-8). / 未成年人数据：受控 + 监护人同意 + 最小化为年龄段（HI-1/HI-8）。
- Anti-drowning AI is assist-only; lifeguard is mandatory. / 防溺水 AI 仅辅助；救生员强制。
- CCTV near pool must avoid changing areas (HI-5). / 泳区 CCTV 须避更衣区（HI-5）。
- Sensor/manual gap alert turns redundancy into an active control. / 传感/手测差异告警把冗余变成主动控制。
- Cert-expiry alerting is a silent life-safety win. / 证照到期告警是隐性的生命安全收益。

---

## ⑦ Related files / 相关文件 {#case-06-related}

- `references/02-club-formats-and-zones.md#format-swim` · `#zone-pool` · `#zone-kids` · `#zone-locker`
- `references/12-biometrics-and-cctv.md` (HI-5) · `references/07-hardware-landscape-and-vendors.md` · `references/16-security-operations-and-emergency.md`
- `playbooks/03-24h-unmanned-club.md` (HI-2 pattern) · `tools/05-regulation-traceability-verification.md` · `tools/04-dynamic-intelligence-retrieval.md`
- `data/21-anti-pattern-library.md#ap-humidity-device-loss` · `#ap-sensor-false-normal` · `data/13-inspection-and-maintenance-calendar.md` · `data/02-regulation-traceability-index.md`

---

## ⑧ G13 tri-perspective note / G13 三视角覆盖说明 {#case-06-g13}

**Architect / 架构**: sensors + manual redundancy + IP65 electronics + access-controlled minors' store — safety by layered defense. / 传感 + 人工冗余 + IP65 电子 + 受控未成年库——分层防御即安全。
**Operator / 商家**: maintenance gets clear alert paths; lifeguard schedule auto; compliance audit-ready. / 维保有清晰告警路径；救生员自动排；合规可审计。
**Member / 会员**: safer water, no device outage at lessons, kids' data protected. / 水更安全、课程不掉线、儿童数据受护。
No orphan touchpoint — safety redundancy is the through-line across all three views. / 无孤儿触点——安全冗余是贯穿三视角的主线。
