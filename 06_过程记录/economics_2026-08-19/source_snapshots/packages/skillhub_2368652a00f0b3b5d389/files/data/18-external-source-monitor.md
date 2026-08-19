# External Source Monitor / 外部信源监控（外界观察名单）
> **Cluster / 集群**: P4 engine · feeds / 供给: `tools/04` (retrieval) · `data/16` (freshness) · `data/17` (consistency) · `data/05` (events) · `scripts/self_iterate.py`
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: registry reviewed monthly; any new source added via `tools/09` L2. Breaking news triggers immediate patrol (see §3).
> **Cross-references / 交叉引用**: `data/02` (regulator domains) · `data/05` (events) · `data/16` · `data/17` · `tools/04` · `tools/09`
> **Retrieval note / 检索提示**: monitored sources are the engine's eyes outward — all marked 🔄 are HIGH-churn.
> 监控信源是引擎对外之眼——标 🔄 者高变。

---

## 1 · Purpose / 用途
`data/16` decides *what* to re-verify; this file decides *where the engine watches* and *what makes it fire*. It is the **monitored-source registry + event trigger rules** for the outside world. When a regulator amends a law or a platform changes pricing, this monitor raises the flag that starts an out-of-cycle patrol.
`data/16` 决定复核「什么」；本文件决定引擎「盯哪里」「什么让它开火」。它是**监控信源登记 + 事件触发规则**。监管修法或平台改价，本监控即举旗，启动计划外巡检。

> **Honesty red line / 诚实红线**: This registry lists *official and first-party* sources only (regulators, platform policy pages, vendor changelogs, standards bodies). It never trusts news aggregators as a verification source — they are at most a **trigger**, never proof.
> 诚实红线：本登记只列*官方与一手*源（监管、平台政策页、供应商 changelog、标准机构）。绝不把新闻聚合站当核验源——至多作**触发**，不作证明。

---

## 2 · Monitored Source Registry / 信源监控登记

Columns / 列: **Source / 信源** · **Type / 类型** (regulator/platform/vendor/industry) · **Monitoring question / 监控问题** · **Trigger keywords / 触发词** · **Affected carrier files / 受影响承载** · **Check freq / 频次** · **Escalation / 升级路径**.

### 2.1 Regulators × 12 markets / 12 市场监管 (align `data/02`)
| Source / 信源 | Type | Monitoring question | Trigger keywords | Affected files | Freq | Escalation |
|---|---|---|---|---|---|---|
| CAC / MPS / MOFCOM (cn) cac.gov.cn · mps.gov.cn · mofcom.gov.cn | regulator | Has PIPL/DSL or prepaid rule been amended? / 个保法或预付规则有无修订？ | 修订, amendment, 征求意见稿, draft | `data/02`#cn-* · `references/10` | 30d | DG5 → `tools/09` |
| PCPD (hk) pcpd.org.hk | regulator | New PDPO guidance or amendment? / 有新指引或修订？ | amendment, guidance, malicious-disclosure | `data/02`#hk-* | 30d | DG5 → `tools/09` |
| NDC / 消保處 (tw) ndc.gov.tw · cpc.ey.gov.tw | regulator | PIPA or gym contract updated? / 个资法或健身契约更新？ | 修正, 定型化契約 | `data/02`#tw-* | 30d | DG5 → `tools/09` |
| PPC (jp) ppc.go.jp · METI meti.go.jp | regulator | APPI / tokutei amended? / APPI或特定商取引法修订？ | 改正, amendment, ガイドライン | `data/02`#jp-* | 30d | DG5 → `tools/09` |
| PIPC (kr) pipc.go.kr · KFTC ftc.go.kr | regulator | PIPA or installment law changed? / PIPA或分期法改动？ | 개정, amendment, 가이드라인 | `data/02`#kr-* | 30d | DG5 → `tools/09` |
| OAIC (au) oaic.gov.au · ACMA acma.gov.au | regulator | Privacy Act reform / Spam Act change? / 隐私法改革或反垃圾法改动？ | reform, amendment, Spam Act | `data/02`#au-* · #nz-* | 30d | DG5 → `tools/09` |
| PDPC (sg) pdpc.gov.sg · IMDA imda.gov.sg | regulator | PDPA / Spam Control amended? / PDPA或反垃圾法修订？ | amendment, advisory, Spam Control | `data/02`#sg-* | 30d | DG5 → `tools/09` |
| PDPC (th) pdpc.or.th · OCPB ocpb.go.th | regulator | PDPA notification or consumer rule? / PDPA通知或消保规则？ | แจ้งเตือน, notification, amendment | `data/02`#th-* | 30d | DG5 → `tools/09` |
| JPDP (my) jpdp.gov.my · KPDN kpdn.gov.my | regulator | PDPA amendment / consumer rule? / PDPA修订或消保规则？ | pindaan, amendment, consumer | `data/02`#my-* | 30d | DG5 → `tools/09` |
| Kominfo (id) kominfo.go.id · OJK ojk.go.id | regulator | PDP Law PP / consumer rule? / PDP法实施细则或消保？ | PP, peraturan, amendment | `data/02`#id-* | 30d | DG5 → `tools/09` |
| MPS (vn) mps.gov.vn · MOCST mocst.gov.vn | regulator | Decree 13 / localization draft? / 13号议定或本地化草案？ | nghị định, dự thảo, decree | `data/02`#vn-* | 30d | DG5 → `tools/09` |
| MeitY/DPB (in) meity.gov.in · dpb.gov.in · TRAI trai.gov.in | regulator | DPDP Rules / DND change? / DPDP细则或DND改动？ | rules, amendment, DND, TRAI | `data/02`#in-* | 30d | DG5 → `tools/09` |

### 2.2 APAC platform policy feeds / 平台政策流 (HIGH, 🔄)
| Source / 信源 | Type | Monitoring question | Trigger keywords | Affected files | Freq | Escalation |
|---|---|---|---|---|---|---|
| Meta / WhatsApp Business Help Center 🔄 | platform | Did conversation pricing or template rules change? / 会话计费或模板规则改了？ | pricing, conversation, template policy | `references/17` · `data/06` | 30d | DG2+DG5 → `tools/09` |
| LINE for Business 🔄 | platform | Message quota / OA policy changed? / 配额或OA政策改？ | policy, quota, 配信 | `references/17` | 30d | DG2+DG5 → `tools/09` |
| Kakao Biz 🔄 | platform | Bizboard guideline updated? / 指南更新？ | 가이드라인, policy | `references/17` | 30d | DG2+DG5 → `tools/09` |
| WeChat Open / WeChat Work 🔄 | platform | Template / group-send rule changed? / 模板或群发规则改？ | 模板消息, 群发, 规则 | `references/17` · `references/19` | 30d | DG2+DG5 → `tools/09` |
| Meta Ads / CAPI 🔄 | platform | CAPI / event-measurement policy? / CAPI或事件度量政策？ | CAPI, aggregation, policy | `references/19` | 30d | DG2+DG5 → `tools/09` |
| Google Ads / GA4 🔄 | platform | Consent mode / ads policy change? / 同意模式或广告政策改？ | consent mode, policy | `references/19` | 30d | DG2+DG5 → `tools/09` |
| Douyin / TikTok Shop 🔄 | platform | Live-commerce / shop policy? / 直播带货或店铺政策？ | 直播, shop, policy | `references/19` | 30d | DG2+DG5 → `tools/09` |
| Meituan merchant 🔄 | platform | Group-buy listing / settlement rule? / 团购上架或结算规则？ | 团购, 结算, 规则 | `references/19` | 30d | DG2+DG5 → `tools/09` |
| Zalo OA 🔄 | platform | OA message policy changed? / OA消息政策改？ | OA, chính sách, policy | `references/17` | 30d | DG2+DG5 → `tools/09` |

### 2.3 Vendor changelogs / status pages (MED, 🔄)
| Source / 信源 | Type | Monitoring question | Trigger keywords | Affected files | Freq | Escalation |
|---|---|---|---|---|---|---|
| SaaS club platforms (e.g. Glofox/Mindbody/Keep/乐刻-style) 🔄 | vendor | New feature / pricing / outage? / 新功能/价格/故障？ | changelog, pricing, incident | `references/06` · `data/03` | 90d | DG1+DG4 |
| Hardware / FTMS vendors (treadmill, lockers, gates) 🔄 | vendor | New model / API / EOL? / 新机型/接口/停产？ | firmware, EOL, API | `references/07` · `data/04` | 90d | DG1+DG4 |
| PSP / payment providers 🔄 | vendor | Fee / API / compliance change? / 费率/接口/合规改？ | fee, API, PCI | `references/06`§H · `data/03` | 90d | DG1+DG4 |
| Cloud / IoT platform status 🔄 | vendor | Outage / region change? / 故障/区域改？ | status, outage, region | `references/08` · `references/09` | 90d | DG1+DG4 |

### 2.4 Industry associations & standards bodies (MED)
| Source / 信源 | Type | Monitoring question | Trigger keywords | Affected files | Freq | Escalation |
|---|---|---|---|---|---|---|
| IHRSA / local fitness associations | industry | New benchmark survey / guidance? / 新基准调查或指引？ | benchmark, survey, report | `data/01` · `data/05` | 90d | DG1 |
| Bluetooth SIG / IEEE / ISO (FTMS, BLE) | standards | Standard revised? / 标准修订？ | FTMS, BLE, revision, standard | `references/09` · `data/08` | 90d | DG1+DG4 |
| Fitness trade press (Club Industry, WellToDo APAC…) | industry | Market trend / M&A shift? / 趋势或并购变？ | trend, M&A, market | `references/04` · `references/14` | 90d | DG1 |
| `data/05` event sources | industry | Conference / deadline dates moved? / 会议或截止日挪动？ | date, event, deadline | `data/05` · `data/16` | 30d | DG1 |

---

## 3 · Event-Triggered Rules / 事件触发规则
1. **Breaking regulation news / 突发法规**: Any regulator in §2.1 publishes an amendment, draft, or enforcement action → **immediate out-of-cycle patrol** (bypass the monthly RRULE). Start: `tools/04` retrieval on that market's domain → propose diff in `data/16` → `tools/09` gate.
   **突发法规**：§2.1 任一监管发布修订/草案/执法行动 → **立即计划外巡检**（跳过月度 RRULE）。起手：`tools/04` 对该市场域名实取→`data/16` 提差异→`tools/09` 闸门。
2. **Platform pricing/policy flip / 平台价策翻转**: A §2.2 source changes conversation pricing or template rules → immediate L1 patrol + DG5 if it flips any deliverable advice.
   §2.2 源改动会话计费或模板规则 → 立即 L1 巡检；若翻转任何交付建议则 DG5。
3. **Vendor EOL / breach / 供应商停产或事故**: §2.3 status/changelog flags EOL or outage affecting a carrier → DG4 write-back + notify operator channel.
   §2.3 标停产或故障影响承载 → DG4 回写 + 通知运营渠道。
4. **Cross-link to other ledgers / 跨账本联动**: A monitor hit that changes a compliance/safety claim → also raise a `data/17` Tier-1 contradiction scan on that anchor before apply.
   监控命中改动合规/安全论断 → 应用前还在该锚点触发 `data/17` Tier-1 矛盾扫描。

> Escalation ladder / 升级阶梯: routine finding → DG gate in `data/16` → on conclusion-flip or HI-adjacent → `tools/09` consensus gate (L1–L4) → quarantine if unresolved.
> 升级阶梯：常规发现→`data/16` 的 DG 闸→翻转结论或HI相关→`tools/09` 共识门（L1–L4）→未决则隔离。

---

## 4 · Report Log Template / 报告日志模板
| Field / 字段 | Meaning / 含义 |
|---|---|
| **Monitor ID / 编号** | `MON-YYYYMM-###` (e.g. `MON-202607-001`) |
| **Source / 信源** | which registry row fired / 哪个登记行触发 |
| **Signal / 信号** | the observed change (quote + date) / 观察到的改动（引文+日期） |
| **Trigger keywords / 触发词** | matched terms / 命中词 |
| **Affected files / 受影响文件** | carrier files to patch / 待修承载文件 |
| **Action taken / 已采取行动** | patrol run / diff proposed / quarantined / 巡检/提差异/隔离 |
| **Gate route / 网关路由** | L0–L4 per `tools/09` |
| **Status / 状态** | OPEN \| PATROLLED \| QUARANTINED \| RESOLVED \| EXAMPLE |

---

## 5 · Report Log (initial seed) / 报告日志（初始种子）
> 3 EXAMPLE rows show the shape; they are NOT real signals. The first live monitor run populates real rows.
> 3 个 EXAMPLE 行仅示范形态，非真实信号。首个真实监控运行填入实行。

| Monitor ID / 编号 | Source / 信源 | Signal / 信号 | Trigger / 触发词 | Affected files | Action / 行动 | Gate / 路由 | Status / 状态 |
|---|---|---|---|---|---|---|---|
| MON-202607-EX1 | PPC (jp) ppc.go.jp | (example) APPI guideline draft published 2026-07 / （示例）APPI指南草案发布 | 改正, draft, ガイドライン | `data/02`#jp-appi · `references/10` | patrol + `tools/05` verify / 巡检+核验 | DG5 → `tools/09` | EXAMPLE |
| MON-202607-EX2 | Meta WhatsApp 🔄 | (example) conversation pricing tier added / （示例）新增会话计费档 | pricing, conversation | `references/17` · `data/06` | L1 patrol / L1巡检 | DG2+DG5 | EXAMPLE |
| MON-202607-EX3 | Bluetooth SIG | (example) FTMS revision note / （示例）FTMS修订说明 | FTMS, revision | `references/09` · `data/08` | DG4 write-back / 回写 | DG1+DG4 | EXAMPLE |

---

## 6 · Health status / 健康状态 (as of 2026-07)
- All §2.1 regulator rows: check freq 30d; next patrol 2026-08. / §2.1 监管行：频次30天，下次2026-08。
- All §2.2 platform rows: 30d, HIGH 🔄; §2.3–2.4: 90d, MED. / §2.2 平台行30天高变；§2.3–2.4 90天中变。
- No live signal logged yet (seed only). / 暂无真实信号（仅种子）。

> **G13 tri-perspective note / 三视角注记**: Architect — this monitor is the library's outward sensor; a missing source = a blind spot where law or pricing can drift unseen. Operator — the escalation ladder tells you exactly who acts when a flag fires. Member — members benefit because a silent regulatory change never silently erodes their rights in any of the 12 markets.
> **G13 三视角**：架构师——本监控是库的对 sensors，缺源=盲点，法规或价格可暗中漂移；运营者——升级阶梯明确举旗时谁出手；会员——受益于此，监管静默改动永不会在 12 市场中暗中侵蚀其权益。
