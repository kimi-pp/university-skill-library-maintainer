# Case 08 · 22-Club Chain HQ (Owned + Franchise) — NOC & Master Data / 案例08 · 22 店连锁总部（直营+加盟）：NOC 与主数据

> **Cluster / 集群**: A (formats) · D (network/SD-WAN) · L (architecture) · R (governance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: SD-WAN/franchise compliance passes `tools/04`; cross-border data passes `tools/05`.
> **Cross-references / 交叉引用**: `references/02-club-formats-and-zones.md#format-chainhq` · `templates/46-hq-noc-dashboard-spec.md` · `references/08-network-and-infrastructure.md` · `data/21-anti-pattern-library.md` · `tools/06-roi-three-scenario.md`
> **Retrieval note / 检索提示**: 🔄 SD-WAN vendor SLA & franchise data-residency rules shift — verify via `tools/04`/`tools/05`. / 标注 🔄 的 SD-WAN 供应商 SLA 与加盟数据驻留规则会变——经 `tools/04`/`tools/05` 核验。

> **Honesty preamble / 诚实声明**: This is an archetypal composite case built from common industry patterns for teaching purposes — not a claimed real company. Numbers are directional. / 本案例为教学用途的原型合成案例，非真实公司；数字为方向性参考。

---

## ① Context card / 背景卡 {#case-08-context}

- **Format / 业态**: 22-club chain HQ — 14 owned + 8 franchise, mixed formats, 3 cities. / 22 店连锁总部——14 直营 + 8 加盟，混合业态，3 城。
- **Market / 市场**: India (multi-state). / 印度（跨州）。
- **FDMM start / 起点等级**: L4 target; needs proven replication playbook. / 目标 L4；需已验证复制打法。
- **Team / 团队**: CTO + 4 infra + 2 data + franchise-enablement lead. / CTO + 4 基础架构 + 2 数据 + 加盟赋能负责人。
- **Annual IT envelope / 年 IT 预算带**: directional ₹30M–₹60M opex (NOC + SD-WAN + BI) + ₹20M–₹40M capex (network core). / 方向性经营支出 3000–6000 万卢比（NOC+SD-WAN+BI）+ 资本开支 2000–4000 万（网络核心）。
- **Why this case / 为何选它**: Heaviest governance per `references/02#format-chainhq`; NOC, master-data cleanup, franchise negotiation, central procurement. / 按 `references/02#format-chainhq` 治理最重；NOC、主数据清理、加盟谈判、集采。

---

## ② The starting mess / 起初的一团乱 {#case-08-mess}

- Each club ran its own MMS, own chart of accounts, own Wi-Fi — HQ had no group view and no single member ID across clubs. / 每店各用各的 MMS、各套科目、各自 Wi-Fi——总部无集团视图、跨店无统一会员 ID。
- A franchisee's staff leaked a HQ dashboard screenshot to a local competitor group chat. / 一名加盟商员工把总部看板截图漏给本地竞对群。
- Franchisees resisted a "mandatory system swap" — they'd bought their own tools and feared cost + lock-in. / 加盟商抵制「强制换系统」——他们自购了工具，怕成本 + 锁定。
- Underlying cause / 根因: growth outran governance; HQ scaled clubs (L4 ambition) without master data or change-management (L7 violation: skipped L2/L3 foundations). / 根因：增长跑赢治理；总部扩店（L4 野心）却无主数据或变革管理（铁律 7 违例：跳过 L2/L3 地基）。

---

## ③ The journey (phase-by-phase) / 转型之路（分阶段） {#case-08-journey}

### Phase 1 — Master-data cleanup & single ID (Month 0–4) / 主数据清理与统一 ID {#case-08-journey-p1}
- `references/02#format-chainhq` + `templates/46-hq-noc-dashboard-spec.md` prep: built a master-member ID + chart-of-accounts standard across 22 clubs. / `references/02#format-chainhq` + `templates/46` 准备：建统一会员 ID + 跨 22 店科目标准。
- Reasoning / 理由: Iron Law 7 — L4 needs a single source before group BI; no ID, no brain. / 铁律 7——L4 在集团 BI 前需单一口径；无 ID 无大脑。
- Library used / 用到的库: `references/02#format-chainhq` · `templates/46` (NOC prep) · `tools/01-fdmm-maturity-assessment.md`. / 用到的库：`references/02#format-chainhq` · `templates/46`（NOC 准备）· `tools/01`（成熟度）。

### Phase 2 — NOC rollout (Month 3–9) / NOC 落地 {#case-08-journey-p2}
- Central NOC on SD-WAN per `references/08-network-and-infrastructure.md`; per-club health dashboards; alert routing to local + HQ. / 基于 `references/08` 的 SD-WAN 建中央 NOC；逐店健康看板；告警路由到本地 + 总部。
- Franchise sites connected via segmented IPsec tunnel, data-residency respected (`tools/05`). / 加盟店经分段 IPsec tunnel 接入，尊重数据驻留（`tools/05`）。
- Library used / 用到的库: `references/08` (network) · `data/11-network-fault-tree-library.md` · `tools/05` (residency). / 用到的库：`references/08`（网络）· `data/11`（网络故障树）· `tools/05`（驻留）。

### Phase 3 — Franchise mandatory-stack negotiation (Month 5–12) / 加盟强制栈谈判 {#case-08-journey-p3}
- Offered a "light mandatory core" (MMS + gate + reporting) free/subsidized, left POS/CRM choice to franchisee — reduced revolt. / 给「轻量强制核心」（MMS+闸机+报表）免费/补贴，POS/CRM 留给加盟商选——降低反弹。
- Change-management: pilot 2 franchisees, prove ROI via `tools/06`, then scale. / 变革管理：先试点 2 家加盟商，`tools/06` 证 ROI，再推广。
- Library used / 用到的库: `tools/06` (ROI) · `references/05-methodology-library.md` (change mgmt) · `data/21`. / 用到的库：`tools/06`（ROI）· `references/05`（变革管理）· `data/21`。

### Phase 4 — Central procurement savings (Month 9–15) / 集采降本 {#case-08-journey-p4}
- Pooled buy of gates/cardio/meters across 22 clubs; directional 10–20% unit discount via volume. / 22 店池化采购闸机/有氧/计量表；量采方向性单台折 10–20%。
- Library used / 用到的库: `references/07-hardware-landscape-and-vendors.md` · `data/15-procurement-and-cost-benchmark.md`. / 用到的库：`references/07`（硬件）· `data/15`（采购基准）。

### Phase 5 — Dashboard governance (Month 12–18) / 看板治理 {#case-08-journey-p5}
- Role-based dashboard access; franchisees see own club + benchmark, NOT others' raw data; watermark + audit log. / 按角色看板权限；加盟商看本店 + 基准，不看他人原始数据；水印 + 审计日志。
- Library used / 用到的库: `data/20-micro-details-ledger.md` (role keys) · `references/13-data-and-llm-engine.md` (access). / 用到的库：`data/20`（角色键）· `references/13`（访问）。

:::dynamic-hook topic="in-sdwan-franchise-residency-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
India's cross-state data-residency expectations and SD-WAN licensing change; verify franchise data boundary & SLA via `tools/05`/`tools/04` before rollout. / 印度跨州数据驻留预期与 SD-WAN 许可会变；推广前经 `tools/05`/`tools/04` 核验加盟数据边界与 SLA。
:::

---

## ④ What went wrong / 踩过的坑 {#case-08-setbacks}

### Setback 1 — Franchisee revolt over forced system swap / 加盟商抵制强制换系统
- A blanket "swap by Q3 or pay penalty" triggered 8 franchisees threatening to leave, risking the brand's expansion capex. / 一刀切「Q3 前换否则罚款」引发 8 家加盟商威胁退盟，危及品牌扩张资本开支。
- Fix / 修复: paused mandate; pilot 2 franchisees, proved ROI (`tools/06`), offered subsidized core; revolt cooled, 6/8 opted in within 2 quarters. / 暂停强制；试 2 家、`tools/06` 证 ROI、供补贴核心；反弹降温，2 季度内 6/8 自愿加入。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-franchise-revolt` (top-down forced swap). / 对应反模式：自上而下强制换。

### Setback 2 — One franchise leaked HQ dashboards / 一家加盟商泄露总部看板
- A franchisee staffer screenshotted a cross-club dashboard to a competitor, exposing rival clubs' fill rates. / 一名加盟商员工把跨店看板截图发给竞对，暴露了对手店的满课率。
- Fix / 修复: role-based access (see Phase 5) + watermark + audit log; franchisees see benchmark only, raw others' data hidden. / 改按角色权限（见第五阶段）+ 水印 + 审计日志；加盟商仅看基准，他人原始数据隐藏。
- Anti-pattern link / 反模式关联: `data/21-anti-pattern-library.md#ap-dashboard-leak` (over-broad dashboard share). / 对应反模式：看板过度共享。

---

## ⑤ Outcomes (6–18 months later, directional) / 结果（方向性） {#case-08-outcomes}

- Group view: from none to daily cross-club BI on a single member ID. / 集团视图：无 → 统一会员 ID 的每日跨店 BI。
- NOC: incident MTTR down directional 30–50% via central alerting. / NOC：事件平均修复时间方向性降 30–50%（集中告警）。
- Franchise opt-in: 6/8 after pilot vs 0 under mandate. / 加盟加入：试点后 6/8 vs 强制下 0。
- Procurement: directional 10–20% unit savings pooled. / 采购：池化方向性单台省 10–20%。
- Leak risk: role-scoped dashboards + watermark cut exposure to near-zero. / 泄露风险：按角色看板 + 水印把暴露降到近零。
- Honest caveat / 诚实提示: L4 group brain needs discipline of daily data entry at every club; tech alone won't sustain it, and franchisees need ongoing enablement. / L4 集团大脑需每店每日录入纪律；单靠技术撑不住，且加盟商需持续赋能。

---

## ⑥ Transferable lessons / 可迁移经验 {#case-08-lessons}

- L4 starts with master data + single ID, not with a shiny dashboard. / L4 从主数据 + 统一 ID 起，而非花哨看板。
- Franchise mandate fails top-down; pilot + ROI + subsidy wins. / 加盟强制自上而下必败；试点 + ROI + 补贴才赢。
- NOC needs SD-WAN + per-club health; alert routing local + HQ. / NOC 需 SD-WAN + 逐店健康；告警路由本地 + 总部。
- Dashboards must be role-scoped; franchisees see benchmark, not others' raw. / 看板须按角色；加盟商看基准而非他人原始。
- Central procurement only pays off at portfolio scale (≥10 clubs). / 集采仅在组合规模（≥10 店）才划算。
- Cross-border/multi-state data-residency verified via `tools/05` (HI-9 aware). / 跨州/跨境数据驻留经 `tools/05` 核验（结合 HI-9）。
- Change-management is a tech project, not a memo. / 变革管理是技术项目，不是一张通知。
- Watermark + audit log on shared dashboards prevents leak impact radius. / 共享看板加水印 + 审计日志，限制泄露波及面。

---

## ⑦ Related files / 相关文件 {#case-08-related}

- `references/02-club-formats-and-zones.md#format-chainhq` · `#zone-serverroom` · `#zone-facade` · `#zone-gate`
- `templates/46-hq-noc-dashboard-spec.md` · `references/08-network-and-infrastructure.md` · `references/13-data-and-llm-engine.md` · `tools/06-roi-three-scenario.md` · `tools/01-fdmm-maturity-assessment.md`
- `tools/05-regulation-traceability-verification.md` (data residency) · `references/07-hardware-landscape-and-vendors.md` · `data/15-procurement-and-cost-benchmark.md`
- `data/21-anti-pattern-library.md#ap-franchise-revolt` · `#ap-dashboard-leak` · `data/11-network-fault-tree-library.md` · `data/20-micro-details-ledger.md`
- `data/01-kpi-benchmark-library.md` (benchmark baselines)

---

## ⑧ G13 tri-perspective note / G13 三视角覆盖说明 {#case-08-g13}

**Architect / 架构**: master ID + SD-WAN NOC + role-scoped dashboards + segmented franchise IPsec tunnel. / 统一 ID + SD-WAN NOC + 按角色看板 + 分段加盟 IPsec tunnel。
**Operator / 商家 (HQ + franchise)**: HQ sees group brain; franchisee keeps POS/CRM choice, sees own + benchmark. / 总部看集团大脑；加盟商保留 POS/CRM 选择，看本店 + 基准。
**Member / 会员**: single ID works across clubs; data not over-shared between franchisees. / 统一 ID 跨店通用；数据不在加盟商间过度共享。
No orphan touchpoint — governance, cost, and member privacy all resolve in the role-scoped design. / 无孤儿触点——治理、成本、会员隐私全在按角色设计中解决。
