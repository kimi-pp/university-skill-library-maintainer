# Knowledge Graph Template (semantic backbone) / 知识图谱模板（语义骨架）

> **Cluster / 集群**: L (Architecture cross-reference mesh) + X (Methodology / G13)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Entity/relation schema is stable; the *instances* (which vendor in which market) refresh via `tools/04`; graph instance edits tracked in `_meta.json` (P4 pointer).
> **Cross-references / 交叉引用**: `data/03-software-vendor-directory.md`, `data/04-hardware-vendor-directory.md`, `data/10-hardware-fault-tree-library.md`, `data/13-inspection-and-maintenance-calendar.md`, `SKILL.md` (Pillar 1 mesh), `tools/00-intake-router.md`, `_meta.json` (P4).
> **Retrieval note / 检索提示**: Vendor/market instances 🔄 re-verify via tools/04; schema itself is static.
> 供应商/市场实例 🔄 经 tools/04 核验；schema 本身静态。

---

## 1. Purpose / 目的

This template defines the **semantic backbone** of the skill's cross-reference mesh. The router (`tools/00`) resolves questions to in-file anchors; the graph adds *multi-hop* reasoning so a symptom can be traced through zones, systems, devices, faults and vendors — not just by keyword.
本模板定义 skill 交叉引用网的**语义骨架**。路由器（`tools/00`）把问题解析到文件内锚点；图谱额外提供*多跳*推理，让症状能穿过空间/系统/设备/故障/供应商追溯，而非仅关键词匹配。

> **P4 pointer / P4 指向**: The live graph instances + `_meta.json` cross-reference mesh are generated in P4 (`workflows/00-build-roadmap.md` Phase 4). This file is the schema; P4 fills the nodes.
> 实时图谱实例与 `_meta.json` 交叉引用网在 P4 生成（见路线图第四阶段）。本文件是 schema，P4 填节点。

---

## 2. Entity types / 实体类型 {#entity-types}

| Entity / 实体 | Meaning / 含义 | Example / 示例 | Source file / 源文件 |
|---|---|---|---|
| Club | a fitness venue / 场馆 | 上海XX综合馆 | SKILL.md / `data/01` |
| Zone | physical area / 物理空间 | gym-floor, locker-room | `references/02` |
| System | software system / 软件系统 | MMS, booking, POS | `data/03`, `references/06` |
| Device | hardware unit / 硬件单元 | treadmill #12, gate lane A | `data/04`, `references/07` |
| Vendor | brand/supplier / 品牌供应商 | 舒华, Mindbody 🔄 | `data/03` / `data/04` |
| Market | APAC market / 亚太市场 | China, Japan, SG | `data/07-apac-regional-differences` |
| Regulation | law/rule / 法规 | PIPL, PDPA 🔄 | `data/02-regulation-traceability-index` |
| KPI | metric / 指标 | churn rate, fill rate | `data/01-kpi-benchmark-library` |
| FaultEntry | fault record / 故障记录 | C4-treadmill-E07-belt-slip | `data/10` |
| UseCase | AI/business case / 场景 | churn prediction | `data/09`, `references/04` |
| Template | doc template / 文档模板 | 3-quote template | `templates/` |
| Playbook | procedure / 规程 | 90-day onboarding | `playbooks/` |

---

## 3. Relation types / 关系类型 {#relation-types}

| Relation / 关系 | Direction / 方向 | Meaning / 含义 |
|---|---|---|
| LOCATED_IN | Device/System → Zone → Club | physical placement / 物理位置 |
| DEPENDS_ON | System/Device → System/Device | runtime dependency / 运行依赖 |
| INTEGRATES_WITH | System ↔ System | data/API link / 数据接口 |
| REGULATED_BY | System/Device → Regulation | compliance bound / 合规约束 |
| MEASURED_BY | KPI → System/Device | metric source / 指标来源 |
| FIXED_BY | FaultEntry → Playbook/Template | resolution path / 解决路径 |
| GOVERNED_BY_HI | any → HI-1..HI-8 | hard-invariant guard / 硬不变量守卫 |

> **Rule / 规则**: Every relation is typed and reversible in query. `GOVERNED_BY_HI` is mandatory on any node touching biometrics, minors, prepaid, fire, safety (HI-1..HI-8).
> 每个关系都带类型且可反向查询。`GOVERNED_BY_HI` 在涉及生物识别/未成年/预付/消防/安全的节点上必挂（HI-1..HI-8）。

---

## 4. Worked mini-graph / 迷你图谱算例 {#mini-graph-example}

A treadmill fault traced end-to-end. / 一台跑步机故障的端到端追溯。

```text
Device: treadmill #12 (C4)
  LOCATED_IN → Zone: gym-floor (A)
  DEPENDS_ON → Power: circuit L3 (references/08 D2)
  DEPENDS_ON → IoT: FTMS gateway (references/09)
  FaultEntry: C4-treadmill-E07-belt-slip (data/10)
     FIXED_BY → Playbook: belt re-tension (data/13 inspection calendar)
  Vendor: 舒华 (data/04#cat-cardio-strength) 🔄
     GOVERNED_BY_HI → HI-2 (no lone-exerciser risk if stuck)
```

Plain words: the treadmill sits on the gym floor, needs power circuit L3 and the FTMS gateway to report data; when its belt slips the fault entry points to the re-tension playbook; the brand row lives in `data/04`; and any stuck-machine scenario is guarded by HI-2 (lone-exerciser safety).
说人话：跑步机在大操房，依赖 L3 电路与 FTMS 网关上报数据；跑带打滑时故障条目指向紧带规程；品牌行在 `data/04`；任何"卡住"场景受 HI-2（独自锻炼者安全）守卫。

---

## 5. How the router uses graph paths / 路由器如何用图谱路径 {#router-multi-hop}

**Question / 问题**: "Why do bookings fail when the internet is fine?" / "网明明好好的，为什么约课失败？"

Keyword search would stop at "internet fine → not network". The graph walks: / 关键词搜索会止于"网好=不是网络"。图谱走：

```text
Symptom: booking fails
  → System: booking DEPENDS_ON MMS (data/03#class-booking)
  → MMS DEPENDS_ON access-control sync (references/06 §4)
  → access-control DEPENDS_ON local network VLAN (data/04#cat-network-gear)
  → VLAN misconfig → gate reader offline but "internet" (WAN) fine
  → FaultEntry: C2-gate-E04-reader-fail (data/10)
```

Answer: the WAN is up but the **internal VLAN** that syncs member status to the gate/booking is down — a consumer-grade switch (no VLAN) is the usual root cause (see `data/04#cat-network-gear`). The graph caught what keywords missed.
结论：外网通，但同步会员状态到闸机/约课的**内部 VLAN** 断了——常见根因是消费级交换机无 VLAN（见 `data/04#cat-network-gear`）。图谱抓到了关键词漏掉的。

> **Multi-hop value / 多跳价值**: Each hop is an anchor the router can deep-link to, so answers stay traceable (Pillar 1).
> 每跳都是路由器可深链的锚点，答案因此可溯源（支柱1）。

---

## 6. _meta.json cross-reference mesh / _meta.json 交叉引用网 {#meta-json-mesh}

Per P4, `_meta.json` is auto-generated from **frontmatter + anchors** of every file: / 按 P4，`_meta.json` 由各文件**frontmatter + 锚点**自动生成：

- Each file's header block (Cluster, Cross-references) becomes a node attribute. / 文件头块（集群、交叉引用）成为节点属性。
- Each `## heading {#anchor}` becomes an addressable node (e.g. `data/03#vendor-mms-cn`). / 每个带锚标题成可寻址节点。
- `tools/00` router maps question → anchor; broken anchor = G12 failure. / `tools/00` 路由器把问题映射到锚点；断锚=G12 不通过。
- The G13 coverage matrix lives here too: every Architect/Operator/Member touchpoint must resolve to ≥1 node. / G13 覆盖矩阵也在此：每个架构/商家/会员触点须解析到 ≥1 节点。

> **Maintenance / 维护**: When you add an anchor, also update the file's Cross-references line; the P4 generator re-zips the mesh. Never leave a dangling `#anchor` in any file.
> 新增锚点时同步更新文件"交叉引用"行；P4 生成器重新拉链。任何文件都不得留悬空 `#anchor`。

---

## 7. Maintenance rules / 维护规则 {#maintenance-rules}

1. **Schema frozen / schema 冻结**: Entity & relation types above are stable; do not rename without P4 regeneration. / 实体与关系类型稳定；改名须 P4 重生成。
2. **Instances volatile / 实例易变**: Vendor/Market nodes 🔄 refresh via `tools/04` every 90 days; staleness >180d → TO VERIFY flag. / 供应商/市场节点 🔄 每 90 天经 tools/04 刷新；超 180 天标"待复核"。
3. **Anchor integrity / 锚点完整**: Every referenced anchor must exist (G12). Renaming a heading breaks links — update all referrers. / 被引锚点须存在（G12）。改名断链须同步改所有引用方。
4. **HI guard mandatory / HI 守卫必挂**: Any node touching HI-1..HI-8 carries `GOVERNED_BY_HI`. / 涉及 HI-1..HI-8 的节点必挂 `GOVERNED_BY_HI`。
5. **Mesh regen / 网状重生成**: After any file edit in P2–P4, re-run the P4 generator so `_meta.json` stays consistent (semantic scan `data/17`). / P2–P4 任意文件改动后重跑 P4 生成器，保持 `_meta.json` 一致（语义扫描见 `data/17`）。

---

## 4.1 Churn graph (AI scenario) / 流失图谱（AI 场景） {#mini-graph-churn}

```text
UseCase: churn prediction (data/09#algo-churn)
  MEASURED_BY → KPI: churn rate (data/01)
  DEPENDS_ON → System: MMS visit log (data/03#vendor-mms-cn)
  DEPENDS_ON → System: SCRM consent (HI-7)
  GOVERNED_BY_HI → HI-7 (no spam), HI-8 (min data)
  FIXED_BY → Playbook: outreach (references/19)
```

## 4.2 CCTV compliance graph / 监控合规图谱 {#mini-graph-cctv}

```text
Device: camera in gym-floor (data/04#cat-cctv)
  LOCATED_IN → Zone: gym-floor (NOT changing room / 非更衣室)
  REGULATED_BY → Regulation: retention law (data/02, references/12)
  GOVERNED_BY_HI → HI-5 (no camera in changing room)
  INTEGRATES_WITH → VMS (references/06 §18)
```

## 4.3 Booking-fail graph / 约课失败图谱 {#mini-graph-booking}

(See §5 multi-hop walk; duplicated here as a node path for the mesh.)
（见 §5 多跳；此处作为网状节点路径重复一份。）

```text
Symptom: booking fails
  → booking DEPENDS_ON MMS DEPENDS_ON access-control
  → access-control DEPENDS_ON VLAN (data/04#cat-network-gear)
  → FaultEntry: C2-gate-E04-reader-fail (data/10)
```

---

## 8. Entity volatility tagging / 实体易变标记

Not all entities refresh at the same rate. The mesh generator tags each instance: / 实体刷新频率不同。网状生成器给每个实例打标：

| Entity / 实体 | Refresh / 刷新 | Hook / 钩子 |
|---|---|---|
| Vendor | 90d | tools/04 🔄 |
| Market | stable | — |
| Regulation | on change | tools/05 |
| KPI threshold | 180d | data/01 |
| FaultEntry | stable | data/10 |
| UseCase | 90d | tools/04 🔄 |

---

## 9. Query examples / 查询示例

- "Which vendors serve Japan MMS?" → Vendor(hacomona) LOCATED_IN Market(Japan) via `data/03#vendor-mms-jp`. / 哪些厂商做日本 MMS？→ `data/03#vendor-mms-jp`。
- "Is camera allowed in locker room?" → Device(camera) GOVERNED_BY_HI HI-5 → NO. / 更衣室能装摄像头吗？→ HI-5 → 否。
- "What maintains treadmill #12?" → Device DEPENDS_ON FaultEntry(C4-E07) FIXED_BY data/13. / 跑步机#12 谁维护？→ 故障条目 FIXED_BY data/13。
- "Why did bookings fail?" → see `data/08#router-multi-hop`. / 约课为何失败？→ 见 `data/08#router-multi-hop`。

---

## G13 Tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: entity/relation schema + router multi-hop design + `_meta.json` mesh.
- **Operator / 运营者**: fault→playbook resolution path (FIXED_BY) keeps firefighting traceable.
- **Member / 会员**: GOVERNED_BY_HI ensures safety/compliance nodes are never orphaned from their invariant. The graph is the guarantee that no symptom, device, or regulation is disconnected.
本文件覆盖架构师（实体/关系 schema+路由器多跳+_meta.json 网）、运营者（故障→规程解析路径 FIXED_BY，救火可溯源）、会员（GOVERNED_BY_HI 保证安全/合规节点不脱离不变量）。图谱保证"无症状、无设备、无法规被孤立"。
