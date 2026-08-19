# Freshness Ledger / 保鲜账本（新鲜度台账）
> **Cluster / 集群**: P4 engine · feeds / 供给: `tools/04` (retrieval) · `tools/08` (hooks/DG) · `tools/09` (consensus) · `scripts/self_iterate.py` · `data/02` · `data/05`
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: every domain below carries a window (30/90/180d). A domain past its window is a "TO VERIFY" flag until `tools/04` re-runs. 🔄 = volatile.
> **Cross-references / 交叉引用**: `data/02` (regulator domains) · `data/05` (industry events/calendar) · `data/06` (term canon) · `tools/08` · `tools/09`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## 1 · Purpose / 用途
This ledger is the **single control sheet** for the self-iteration engine. It lists every volatile-knowledge domain in the library, the file that carries it, its staleness window, the verification channel that re-proves it, when it was last verified, when it is next due, and which dynamic gate (DG) owns its patrol.
本账本是自迭代引擎的**唯一控制表**。它列出库内每个易变知识域、承载文件、保鲜窗、复核通道、上次核验日、下次到期日，以及由哪个动态闸（DG）负责巡检。

> **Honesty red line / 诚实红线**: A "next-due" date is a scheduled re-check, NOT a promise the value is still true. The engine re-proves; it never assumes.
> 诚实红线：「下次到期」是计划复核日，不是「值仍正确」的保证。引擎只复核、不假设。

---

## 2 · Volatile-Knowledge Domain Table / 易变知识域台账

Columns / 列: **Domain / 域** · **Carrier files / 承载文件** · **Window / 保鲜窗** · **Verification channel / 复核通道 (tools/04 queries)** · **Last-verified / 末核** · **Next-due / 到期** · **Owner gate / 负责闸**.

### 2.1 Regulations × 12 markets / 法规 × 12 市场 (window 180d)
| Domain / 域 | Carrier files | Window | Verification channel | Last | Next | Owner gate |
|---|---|---|---|---|---|---|
| cn privacy & prepaid (PIPL/DSL + 单用途预付卡) | `data/02`#cn-pipl · `references/10` | 180d | CAC cac.gov.cn · MOCOM mofcom.gov.cn via `tools/04` | 2026-07 | 2027-01 | DG5 → `tools/09` |
| hk PDPO & gym guidance | `data/02`#hk-pdpo · `references/10` | 180d | PCPD pcpd.org.hk · Consumer Council consuhk.org.hk | 2026-07 | 2027-01 | DG5 → `tools/09` |
| tw PIPA & gym contract | `data/02`#tw-pipa · `references/10` | 180d | NDC ndc.gov.tw · 消保處 cpc.ey.gov.tw | 2026-07 | 2027-01 | DG5 → `tools/09` |
| jp APPI & tokutei | `data/02`#jp-appi · `references/10` | 180d | PPC ppc.go.jp · METI meti.go.jp | 2026-07 | 2027-01 | DG5 → `tools/09` |
| kr PIPA & installment | `data/02`#kr-pipa · `references/10` | 180d | PIPC pipc.go.kr · KFTC ftc.go.kr | 2026-07 | 2027-01 | DG5 → `tools/09` |
| au Privacy Act & spam | `data/02`#au-privacy-act · `references/11` | 180d | OAIC oaic.gov.au · ACMA acma.gov.au | 2026-07 | 2027-01 | DG5 → `tools/09` |
| nz Privacy Act | `data/02`#nz-privacy-act · `references/11` | 180d | NZ Privacy Commissioner privacy.org.nz | 2026-07 | 2027-01 | DG5 → `tools/09` |
| sg PDPA & spam | `data/02`#sg-pdpa · `references/11` | 180d | PDPC pdpc.gov.sg · IMDA imda.gov.sg | 2026-07 | 2027-01 | DG5 → `tools/09` |
| th PDPA | `data/02`#th-pdpa · `references/11` | 180d | PDPC pdpc.or.th · OCPB ocpb.go.th | 2026-07 | 2027-01 | DG5 → `tools/09` |
| my PDPA | `data/02`#my-pdpa · `references/11` | 180d | JPDP jpdp.gov.my · KPDN kpdn.gov.my | 2026-07 | 2027-01 | DG5 → `tools/09` |
| id PDP Law | `data/02`#id-pdp · `references/11` | 180d | Kominfo kominfo.go.id · OJK ojk.go.id | 2026-07 | 2027-01 | DG5 → `tools/09` |
| vn Decree 13 | `data/02`#vn-pdpd · `references/11` | 180d | MPS mps.gov.vn · MOCST mocst.gov.vn | 2026-07 | 2027-01 | DG5 → `tools/09` |
| in DPDP Act | `data/02`#in-dpdp · `references/11` | 180d | MeitY meity.gov.in · DPB dpb.gov.in · TRAI trai.gov.in | 2026-07 | 2027-01 | DG5 → `tools/09` |

### 2.2 Platform policies / 平台政策 (window 30–90d, HIGH)
| Domain / 域 | Carrier files | Window | Verification channel | Last | Next | Owner gate |
|---|---|---|---|---|---|---|
| WhatsApp Business template & conversation pricing 🔄 | `references/17` · `data/06`#conversation-pricing | 30d | Meta Business Help Center via `tools/04` | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |
| LINE Official Account policy 🔄 | `references/17` · `data/06`#line-official | 30d | LINE for Business docs (linebiz) | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |
| KakaoTalk Bizboard policy 🔄 | `references/17` · `data/06`#kakao-talk-biz | 30d | Kakao Biz center | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |
| WeChat / WeChat Work messaging rules 🔄 | `references/17` · `data/06`#we-chat-work | 30d | WeChat Open Platform docs | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |
| Meta (Facebook/IG) ad & CAPI policy 🔄 | `references/19` · `data/06`#capi | 30d | Meta for Developers / Events Manager | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |
| Google Ads & GA4 policy 🔄 | `references/19` · `data/06`#roas | 30d | Google Ads Help / GA4 docs | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |
| Douyin / TikTok live-commerce rules 🔄 | `references/19` · `data/06`#live-commerce | 30d | Douyin Open Platform / TikTok Shop policy | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |
| Meituan / group-buy listing rules 🔄 | `references/19` · `data/06`#group-buy | 30d | Meituan merchant policy center | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |
| Zalo OA policy 🔄 | `references/17` · `data/06`#zalo-oa | 30d | Zalo Business docs | 2026-07 | 2026-08 | DG2+DG5 → `tools/09` |

### 2.3 Vendor landscapes / 供应商格局 (window 90d, MED)
| Domain / 域 | Carrier files | Window | Verification channel | Last | Next | Owner gate |
|---|---|---|---|---|---|---|
| APAC software SaaS vendors 🔄 | `references/06` · `data/03` | 90d | `tools/04` vendor scan (G2B review + official sites) | 2026-07 | 2026-10 | DG1+DG4 |
| APAC hardware vendors 🔄 | `references/07` · `data/04` | 90d | `tools/04` vendor scan | 2026-07 | 2026-10 | DG1+DG4 |
| FTMS / BLE standardization status | `references/09` · `data/08` | 90d | Standards bodies (IEEE/ISO/Bluetooth SIG) via `tools/04` | 2026-07 | 2026-10 | DG1+DG4 |
| Payment / PSP providers 🔄 | `references/06`§H · `data/03` | 90d | `tools/04` PSP scan | 2026-07 | 2026-10 | DG1+DG4 |

### 2.4 Pricing benchmarks / 价格基准 (window 90d, MED)
| Domain / 域 | Carrier files | Window | Verification channel | Last | Next | Owner gate |
|---|---|---|---|---|---|---|
| Membership price benchmarks by market 🔄 | `data/01` · `data/15` | 90d | `tools/04` market-price scan | 2026-07 | 2026-10 | DG1+DG4 |
| PT / class price benchmarks 🔄 | `data/01` · `data/15` | 90d | `tools/04` market-price scan | 2026-07 | 2026-10 | DG1+DG4 |
| Hardware unit costs 🔄 | `data/04` · `data/15` | 90d | `tools/04` hardware-price scan | 2026-07 | 2026-10 | DG1+DG4 |
| SaaS seat / transaction pricing 🔄 | `data/03` · `data/15` | 90d | `tools/04` SaaS-price scan | 2026-07 | 2026-10 | DG1+DG4 |
| Payment / BNPL fee benchmarks 🔄 | `data/15` · `references/19` | 90d | `tools/04` fee scan | 2026-07 | 2026-10 | DG1+DG4 |

### 2.5 Industry-event dates / 行业事件日期 (window 30d, HIGH)
| Domain / 域 | Carrier files | Window | Verification channel | Last | Next | Owner gate |
|---|---|---|---|---|---|---|
| APAC fitness / tech conference calendar 🔄 | `data/05` | 30d | `tools/04` event-source scan (align `data/05`) | 2026-07 | 2026-08 | DG1 |
| Regulator consultation deadlines 🔄 | `data/02` · `data/05` | 30d | Regulator sites (sec.3) via `tools/04` | 2026-07 | 2026-08 | DG1 |
| Platform policy changelog dates 🔄 | `references/17`·`19` · `data/05` | 30d | Platform status/changelog pages | 2026-07 | 2026-08 | DG1 |

### 2.6 KPI benchmarks / KPI 基准 (window 90d, MED)
| Domain / 域 | Carrier files | Window | Verification channel | Last | Next | Owner gate |
|---|---|---|---|---|---|---|
| Churn / retention benchmark ranges 🔄 | `data/01` | 90d | `tools/04` benchmark scan | 2026-07 | 2026-10 | DG1+DG4 |
| Attendance / utilization ranges 🔄 | `data/01` | 90d | `tools/04` benchmark scan | 2026-07 | 2026-10 | DG1+DG4 |
| ARPU / LTV:CAC ranges 🔄 | `data/01` | 90d | `tools/04` benchmark scan | 2026-07 | 2026-10 | DG1+DG4 |

### 2.7 Trend statistics / 趋势数据 (window 90d, MED)
| Domain / 域 | Carrier files | Window | Verification channel | Last | Next | Owner gate |
|---|---|---|---|---|---|---|
| AI-in-fitness adoption stats 🔄 | `references/04` · `references/14` | 90d | `tools/04` trend scan (align `data/05`) | 2026-07 | 2026-10 | DG1+DG4 |
| APAC membership-market stats 🔄 | `references/04` · `data/01` | 90d | `tools/04` market-stat scan | 2026-07 | 2026-10 | DG1+DG4 |

---

## 3 · Verification Channel Map / 复核通道地图

### 3.1 Per-market official regulator domains / 各市场官方监管域名
> Aligns exactly with `data/02` official-domain allow-list. Only these are valid article-level retrieval sources.
> 与 `data/02` 官方域名白名单完全一致。仅这些可作条款级引用源。

| Market / 市场 | Regulator domains / 监管域名 | `tools/04` query hint / 检索提示 |
|---|---|---|
| cn | cac.gov.cn · mps.gov.cn · mofcom.gov.cn · miit.gov.cn | "PIPL article" "预付卡 办法" |
| hk | pcpd.org.hk · consuhk.org.hk | "PDPO amendment" "gym guidance" |
| tw | ndc.gov.tw · cpc.ey.gov.tw | "個資法 修正" "健身 定型化契約" |
| jp | ppc.go.jp · meti.go.jp · caa.go.jp | "APPI amendment" "特定商取引法" |
| kr | pipc.go.kr · ftc.go.kr · mol.go.kr | "PIPA amendment" "할부거래법" |
| au | oaic.gov.au · acma.gov.au · accc.gov.au | "Privacy Act reform" "Spam Act" |
| nz | privacy.org.nz | "Privacy Act 2020" |
| sg | pdpc.gov.sg · case.org.sg · imda.gov.sg · acra.gov.sg | "PDPA amendment" "Spam Control Act" |
| th | pdpc.or.th · ocpb.go.th | "PDPA notification" "consumer protection" |
| my | jpdp.gov.my · kpdn.gov.my | "PDPA amendment" "consumer protection" |
| id | kominfo.go.id · ojk.go.id · kppu.go.id | "PDP Law PP" "consumer protection" |
| vn | mps.gov.vn · mocst.gov.vn | "Decree 13" "PDP decree" |
| in | meity.gov.in · dpb.gov.in · trai.gov.in · rbi.org.in · ccpa.gov.in | "DPDP Rules" "TRAI DND" |

### 3.2 Platform policy pages / 平台政策页
| Platform / 平台 | Policy / 状态页 | `tools/04` query hint |
|---|---|---|
| WhatsApp | business.whatsapp.com · Meta Business Help Center | "conversation pricing" "template policy" |
| LINE | linebiz.com (LINE for Business) | "Official Account policy" "message quota" |
| Kakao | biz.kakao.com | "Bizboard policy" "message guideline" |
| WeChat / WeCom | open.weixin.qq.com · work.weixin.qq.com | "template message" "群发 规则" |
| Meta Ads | facebook.com/business · developers.facebook.com | "CAPI" "aggregated event measurement" |
| Google | support.google.com/ads · support.google.com/analytics | "ads policy" "GA4 consent mode" |
| Douyin/TikTok | open.douyin.com · seller-us.tiktok.com | "live-commerce" "shop policy" |
| Meituan | e.meituan.com ( merchant) | "入駷 规则" "group-buy policy" |
| Zalo | zalo.me/business · zalo.vn/oa | "OA policy" "message quota" |

### 3.3 Industry sources / 行业来源 (align `data/05`)
> `data/05-industry-events-and-media-calendar.md` is the canonical event/calendar carrier. The engine pulls conference dates, association reports, and standards-body releases from the sources listed there.
> `data/05` 是事件/日历的权威承载。引擎从其列出的会议、协会报告、标准机构发布处抽取。

| Source type / 类型 | Example carriers / 示例 | `tools/04` query hint |
|---|---|---|
| Fitness trade press / 健身行业媒体 | Club Industry, Health Club Management, WellToDo (APAC) | "APAC fitness trends 2026" |
| Tech/AI press / 科技媒体 | IEEE, Bluetooth SIG, ISO for FTMS | "FTMS standard update" |
| Market-research / 市研 | Statista, local market reports (per market) | "<market> gym market size" |
| Standards bodies / 标准机构 | IEEE 802.11, Bluetooth SIG, ISO | "BLE fitness standard" |
| Association / 协会 | IHRSA/HRSA affiliates, local fitness associations | "industry benchmark survey" |

---

## 4 · Monthly Patrol Procedure / 月度巡检流程
`scripts/self_iterate.py` (P4) walks this ledger on an RRULE monthly schedule + event triggers. Zero human intervention at L0–L3 (see `tools/09`). Steps:
`scripts/self_iterate.py`（P4）按 RRULE 月度 + 事件触发巡检。L0–L3 零人为干预（见 `tools/09`）。步骤：

1. **Parse hooks / 解析钩子**: Read every `:::dynamic-hook` block across `data/` & `references/`; build a per-domain queue from §2 above. / 读取所有 `:::dynamic-hook` 块，按 §2 建域队列。
2. **Check staleness / 查保鲜**: For each domain, compare `last-verified` + `window` against today. Domains past `next-due` → flagged "TO VERIFY". HIGH (30d) re-retrieved in full; MED (90d) sampled. / 比对 `last-verified`+`window` 与今日，超期标「待复核」；高时效全量复取，中时效抽检。
3. **Retrieve / 实取**: Call `tools/04` per the §3 channel map with the listed query hint. Record raw retrieved value + retrieval date. / 按 §3 通道地图调 `tools/04`，记录实取值+检索日。
4. **Propose diff / 提差异**: Compare retrieved vs stored. If drift ≥ threshold (defined per domain), draft a diff patch (old→new, with source). / 比实取与存值，漂移超阈值的拟差异补丁（旧→新+来源）。
5. **Consensus gate / 共识门**: Route the diff to `tools/09` 4-agent council (L1 = lite 2-agent; L2 = full 4-agent). Hard invariants HI-1~HI-8 one-vote veto. Pass = multi-source consensus N≥2 + confidence ≥0.6 + zero HI violation. / 差异送 `tools/09` 四 Agent 理事会（L1 轻量2员，L2 全4员）。HI-1~8 一票否决。通过=多源共识≥2+置信≥0.6+零 HI 违。
6. **Apply or quarantine / 应用或隔离**: On pass → write-back: update the carrier file value + this ledger's `last-verified`/`next-due`; append SHA-256(prev_hash + diff) to the hash chain (`scripts/`). On fail/conflict → park in `quarantine/` with full context; library keeps serving the prior value + "disputed" flag (non-blocking). / 通过→回写：更新承载文件值与本账本 `last-verified`/`next-due`，并向哈希链追加 SHA-256(前哈希+差异)。失败/冲突→停放 `quarantine/` 带上下文；库以旧值+「存疑」标继续服务（非阻塞）。
7. **Log to hash chain / 哈希链记账**: Every applied change, every quarantine, every "no-drift" pass is appended to the tamper-evident audit log (`scripts/self_iterate.py` + `backups/`). Golden-QA regression (`data/19`) runs after L2/L3 applies. / 每次应用、每次隔离、每次「无漂移」通过，均追加到防篡改审计日志。L2/L3 应用后跑黄金问答回归（`data/19`）。

> **Escalation shortcut / 升级捷径**: a retrieved change that *flips a conclusion* (e.g. a market bans face-entry) jumps straight to `tools/09` DG5 regardless of window. / 实取值若翻转结论（如某市场禁用人脸入场），无论保鲜窗直接进 `tools/09` DG5。

---

## 5 · Owner-Gate Map / 负责闸映射
| Change level / 变更级 | Scope / 范围 | Gate path / 闸门路径 |
|---|---|---|
| L0 | Freshness metadata (dates, ledger) / 新鲜度元数据 | Auto-apply by `scripts/`; DG1 integrity only. |
| L1 | Fact refresh inside a hook / 钩内事实刷新 | DG1–DG6 + consensus lite (2 agents) → `tools/09`. |
| L2 | Library content edits (new fault-tree, vendor row) / 库内容增改 | Full 4-agent consensus (`tools/09`) + DG4 ledger write-back. |
| L3 | Structural change (new file, cluster remap) / 结构变更 | Full consensus + golden-QA regression (`data/19`). |
| L4 | Mechanism change (gates/invariants/pipeline) / 机制变更 | **Human required** — the ONLY human-mandatory level. |

---

## 6 · Hash-chain & backup pointer / 哈希链与备份指针
- Audit log: `scripts/self_iterate.py` appends `SHA-256(prev_hash + diff + timestamp + gate_result)`.
- 审计日志：`scripts/self_iterate.py` 追加 `SHA-256(前哈希 + 差异 + 时间戳 + 闸门结果)`。
- Backups: timestamped snapshot before every L2+ apply; pruned by monthly patrol. / L2+ 应用前快照，月度巡检清理。
- Quarantine: `quarantine/` holds rejected/unresolved diffs with context. / 隔离区存被拒/未决差异及上下文。

---

## 7 · Ledger health status / 账本健康状态 (as of 2026-07)
- All regulatory rows: last-verified 2026-07, next-due 2027-01 (180d). / 所有法规行：末核 2026-07，到期 2027-01。
- All platform/vendor/pricing/event/KPI/trend rows: last-verified 2026-07; next-due per §2.2–2.7. / 所有平台/供应商/价格/事件/KPI/趋势行：末核 2026-07，到期见 §2.2–2.7。
- No domain is currently past `next-due`. / 当前无域超期。

> **G13 tri-perspective note / 三视角注记**: Architect — this ledger is the engine's control plane; a missing domain row = a blind spot the patrol cannot see. Operator — watch the "next-due" column like a service calendar; a red row means "verify before you act". Member — the patrol protects members because stale consent/biometric rules would otherwise silently break their rights across 12 markets.
> **G13 三视角**：架构师——本账本是引擎控制面，缺域行=巡检盲点；运营者——把「到期」列当服务日历看，红行即「行动前先核」；会员——巡检保护会员，因为过期的同意/生物识别规则会悄悄侵蚀其 12 市场权益。
