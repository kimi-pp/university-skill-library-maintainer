# Regulation Traceability Index / 法规溯源索引

> **Cluster / 集群**: F (12-market compliance) · feeds / 供给: `tools/05` (repeal scan)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: every row "last-verified: 2026-07"; staleness 180d — re-run `tools/05` before citing exact articles.
> **Cross-references / 交叉引用**: `references/10` · `references/11` · `references/12` · `tools/05`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## How to use this index / 索引用法

This is the **machine-checkable** companion to `references/10`–`12`. For each of the 12 markets × four-pack, it records: law official name (EN + local/中文), regulator, official source domain, status as of 2026-07, key topics, and the anchor ID used in the references files.
本索引是 `references/10–12` 的**可机检**配套。对 12 市场 × 四件套，分别记录：法名（英+当地/中文）、监管机构、官方域名、2026-07 状态、关键主题、references 中的锚点 ID。

> **Honesty red line / 诚实红线**: official domains only (no news/blog). Article numbers are intentionally NOT stored — always retrieve via `tools/05` for article-level citation.
> **诚实红线**：只用官方域名（不用新闻/博客）。不存条款号——条款级引用一律经 `tools/05` 实取。

Status legend / 状态图例: `In force` 现行有效 · `Amended` 已修订 · `Pending 🔄` 待决/修订中.

---

## China mainland / 中国内地

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | PIPL 个人信息保护法 / Data Security Law 数据安全法 | CAC 国家网信办 | cac.gov.cn | In force / Amended | consent, cross-border, sensitive PI | #cn-pipl |
| ② Biometric/CCTV | PIPL (sensitive PI) + public-place imaging rules / 公共场所图像 | CAC / MPS 公安部 | cac.gov.cn · mps.gov.cn | In force | separate consent, signage, alt | #cn-cctv |
| ③ Payments/prepaid | 单用途预付卡管理办法 | Ministry of Commerce 商务部 | mofcom.gov.cn | In force / local rules 🔄 | filing, fund custody | #cn-prepaid-card |
| ④ Industry | 反电信网络诈骗法 / SMS rules / AIGC labeling | CAC / MIIT 工信部 | cac.gov.cn · miit.gov.cn | In force / evolving 🔄 | anti-spam, AI labeling | #cn-sms |

---

## Hong Kong (China) / 中国香港

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | Personal Data (Privacy) Ordinance 個人資料(私隱)條例 (PDPO) | PCPD 私隱專員公署 | pcpd.org.hk | In force / Amended 2021 | DPPs, breach notice, malicious-disclosure | #hk-pdpo |
| ② Biometric/CCTV | PDPO + PCPD CCTV/facial guidance | PCPD | pcpd.org.hk | In force / guidance 🔄 | consent, proportionality, signage | #hk-cctv |
| ③ Payments/prepaid | (no single statute; OFT/Consumer Council) | Consumer Council | consuhk.org.hk | Guidance | contract fairness | #hk-prepaid |
| ④ Industry | Consumer Council gym guidance | Consumer Council | consuhk.org.hk | Guidance | cooling-off, cancellation | #hk-gym |

---

## Taiwan (China) / 中国台湾

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | 個人資料保護法 (Personal Data Protection Act) | NDC / 國發會 | ndc.gov.tw | In force | explicit consent, sensitive | #tw-pipa |
| ② Biometric/CCTV | 個資法 + surveillance guidance | NDC | ndc.gov.tw | In force | consent, signage, alt | #tw-cctv |
| ③ Payments/prepaid | 健身中心定型化契約應記載及不得記載事項 | 行政院消保處 | cpc.ey.gov.tw | In force | model contract, refund | #tw-gym-contract |
| ④ Industry | 消保法 + 定型化契約 | 消保處 | cpc.ey.gov.tw | In force | cooling-off, termination | #tw-gym |

---

## Japan / 日本

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | Act on the Protection of Personal Information 個人情報保護法 (APPI) | PPC 個人情報保護委員会 | ppc.go.jp | In force / Amended 🔄 | purpose, consent, breach notice | #jp-appi |
| ② Biometric/CCTV | APPI + PPC guidelines | PPC | ppc.go.jp | In force / guidance 🔄 | consent, alt, signage | #jp-appi-biometric |
| ③ Payments/prepaid | 特定商取引法 (Act on Specified Commercial Transactions) | METI 経済産業省 | meti.go.jp | In force / Amended 🔄 | cooling-off, installment | #jp-tokutei |
| ④ Industry | 健身/消費契約 + 安全基準 | METI / 消費庁 | meti.go.jp · caa.go.jp | In force | contract fairness, safety | #jp-gym |

---

## South Korea / 韩国

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | 개인정보 보호법 (Personal Information Protection Act, PIPA) | PIPC 個人情報保護委員會 | pipc.go.kr | In force / Amended 🔄 | consent, sensitive, breach | #kr-pipa |
| ② Biometric/CCTV | PIPA + CCTV/face guidance | PIPC | pipc.go.kr | In force / strict 🔄 | strict biometric, signage, alt | #kr-pipa-biometric |
| ③ Payments/prepaid | 할부거래법 (Instalment Transactions Act) | KFTC 公取委 | ftc.go.kr | In force | installment, cooling-off | #kr-installment |
| ④ Industry | 健身/消費者契約 + 安全 | KFTC / 雇僱勞動部 | ftc.go.kr · mol.go.kr | In force | contract fairness, safety | #kr-gym |

---

## Australia & New Zealand / 澳大利亚与新西兰

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data (AU) | Privacy Act 1988 + APPs | OAIC | oaic.gov.au | In force / Reform 🔄 | APPs, breach notice | #au-privacy-act |
| ① Privacy/data (NZ) | Privacy Act 2020 + IPPs | NZ Privacy Commissioner | privacy.org.nz | In force | IPPs, breach notice | #nz-privacy-act |
| ② Biometric/CCTV | APPs / IPPs + OAIC guidance | OAIC / NZ PC | oaic.gov.au · privacy.org.nz | In force | sensitive, signage, alt | #au-cctv |
| ③ Payments/prepaid | Fair Trading Acts (state) + ACCC | ACCC | accc.gov.au | In force | unfair terms, BNPL | #au-prepaid |
| ④ Industry | Spam Act 2003 (AU) + state cooling-off | ACMA / state fair-trading | acma.gov.au · fairtrading | In force / state varies 🔄 | opt-in, cooling-off | #au-cooling-off |

---

## Singapore / 新加坡

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | Personal Data Protection Act (PDPA) | PDPC | pdpc.gov.sg | In force / Amended | consent, breach notice | #sg-pdpa |
| ② Biometric/CCTV | PDPA + advisory guidelines | PDPC | pdpc.gov.sg | In force / guidance 🔄 | consent, alt, signage | #sg-cctv |
| ③ Payments/prepaid | CaseTrust (gym) guidelines | CASE Singapore | case.org.sg | Guidance | trust account, insurance | #sg-casetrust |
| ④ Industry | Spam Control Act | IMDA / MDA | imda.gov.sg | In force | opt-in, unsubscribe | #sg-spam |

---

## Thailand / 泰国

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | PDPA B.E.2562 (2019) | PDPC Thailand | pdpc.or.th | In force (2022) | consent, 72h breach | #th-pdpa |
| ② Biometric/CCTV | PDPA + camera guidance | PDPC | pdpc.or.th | In force | consent, alt, signage | #th-cctv |
| ③ Payments/prepaid | (consumer protection) | OCPB | ocpb.go.th | In force | contract fairness | #th-prepaid |
| ④ Industry | 消費者保護法 + 安全 | OCPB | ocpb.go.th | In force | cooling-off, safety | #th-gym |

---

## Malaysia / 马来西亚

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | Personal Data Protection Act 2010 | JPDP | jpdp.gov.my | In force / Amendment pending 🔄 | 7 principles, consent | #my-pdpa |
| ② Biometric/CCTV | PDPA 2010 + guidance | JPDP | jpdp.gov.my | In force | consent, alt, signage | #my-cctv |
| ③ Payments/prepaid | (consumer protection) | KPDN | kpdn.gov.my | In force | contract fairness | #my-prepaid |
| ④ Industry | 消費者保護 + 安全 | KPDN | kpdn.gov.my | In force | cooling-off, safety | #my-gym |

---

## Indonesia / 印尼

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | Law No.27/2022 on PDP | Kominfo | kominfo.go.id | In force / PP rolling 🔄 | consent, breach, DPO | #id-pdp |
| ② Biometric/CCTV | PDP Law + PP guidance | Kominfo | kominfo.go.id | In force / PP 🔄 | consent, alt, signage | #id-cctv |
| ③ Payments/prepaid | (consumer protection) | KPPU / OJK | kppu.go.id · ojk.go.id | In force | contract fairness | #id-prepaid |
| ④ Industry | PP71 residency + safety | Kominfo / 相關部 | kominfo.go.id | In force / evolving 🔄 | localization, safety | #id-gym |

---

## Vietnam / 越南

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | Decree 13/2023/ND-CP on PDP | MPS 公安部 | mps.gov.vn | In force (2023) / Law draft 🔄 | consent, cross-border | #vn-pdpd |
| ② Biometric/CCTV | Decree 13 + guidance | MPS | mps.gov.vn | In force | consent, alt, signage | #vn-cctv |
| ③ Payments/prepaid | (consumer protection) | MOCST / 相關 | mocst.gov.vn | In force | contract fairness | #vn-prepaid |
| ④ Industry | Localization draft + safety | MPS / 相關 | mps.gov.vn | Draft 🔄 | in-country, safety | #vn-gym |

---

## India / 印度

| Pack / 包 | Law (EN / 中文) | Regulator | Official domain | Status / 状态 | Topics | Anchor |
|---|---|---|---|---|---|---|
| ① Privacy/data | Digital Personal Data Protection Act 2023 | MeitY / Data Protection Board | meity.gov.in · dpb.gov.in | In force / Rules 🔄 | consent, breach, rights | #in-dpdp |
| ② Biometric/CCTV | DPDP + guidance | MeitY / DPB | meity.gov.in | In force / Rules 🔄 | consent, alt, signage | #in-cctv |
| ③ Payments/prepaid | (consumer protection) | CCPA / RBI | ccpa.gov.in · rbi.org.in | In force | contract fairness | #in-prepaid |
| ④ Industry | TRAI DND / telemarketing | TRAI | trai.gov.in | In force | DND, opt-in SMS | #in-dnd |

---

## How `tools/05` consumes this index / tools/05 如何消费本索引

1. **Resolve anchor / 解析锚点**: a deliverable cites `#jp-appi` → find the row → confirm law + regulator + domain. / 交付物引 `#jp-appi`→定位行→确认法名+机构+域名。
2. **Force check / 有效性**: read the Status column; if `Pending 🔄`, mark the citation "verify before use". / 读状态列；若「待决🔄」标「引用前核验」。
3. **Article retrieval / 条款实取**: official domain only → fetch the consolidated law → cite article + date. / 仅官方域名→取合并版本→引条款+日期。
4. **Conflict check / 冲突检查**: cross-border → compare origin & destination rows → stricter wins. / 跨境→比来源与目的地行→从严。
5. **Log / 记账**: write the verification result to `data/16-freshness-ledger.md`. / 结果写入 `data/16` 保鲜账本。

## Two-letter market codes / 双字母市场码

| Code / 码 | Market / 市场 |
|---|---|
| cn | China mainland / 中国内地 |
| hk | Hong Kong (China) / 中国香港 |
| tw | Taiwan (China) / 中国台湾 |
| jp | Japan / 日本 |
| kr | South Korea / 韩国 |
| sg | Singapore / 新加坡 |
| th | Thailand / 泰国 |
| my | Malaysia / 马来西亚 |
| id | Indonesia / 印尼 |
| vn | Vietnam / 越南 |
| in | India / 印度 |
| au | Australia / 澳大利亚 |
| nz | New Zealand / 新西兰 |

## Common cross-border pairs (stricter-rule watch) / 常见跨境组合（从严观察）

- **cn → hk / tw / sg / any**: CAC outbound pathway likely required. 🔄 / 很可能需网信办出境路径。
- **eu → any APAC**: GDPR outbound + local law inbound both apply. / GDPR 出境与本地法入境均适用。
- **in → offshore**: DPDP Rules transfer basis needed. 🔄 / 需 DPDP 细则传输依据。
- **vn → offshore**: Decree 13 consent + docs. 🔄 / 13 号议定同意+文件。
- **id → offshore**: check PP71 scope first. 🔄 / 先查 PP71 范围。

## Stale-row handling / 过期行处理

- Every row carries **last-verified: 2026-07** and a 180-day staleness window. / 每行带**最后核验 2026-07**与 180 天保鲜窗。
- A row older than 180 days OR marked `Pending 🔄` MUST be re-verified via `tools/05` before citation. / 超 180 天或标「待决🔄」的行，引用前必须经 `tools/05` 复核。
- Amendment/hook rows (🔄) are flagged "stored value, verify before use" per `tools/08`. / 修订/钩子行（🔄）按 `tools/08` 标「存值，引用前核验」。

## Anchor ID scheme (recap) / 锚点 ID 方案（回顾）

Pattern / 模式: `#{market-code}-{law-slug}[-{topic}]` — market codes / 市场码: cn, hk, tw, jp, kr, au, nz, sg, th, my, id, vn, in. Examples / 例: `#cn-pipl`, `#hk-pdpo`, `#tw-pipa`, `#jp-appi`, `#jp-appi-biometric`, `#kr-pipa`, `#au-privacy-act`, `#nz-privacy-act`, `#sg-pdpa`, `#sg-casetrust`, `#th-pdpa`, `#my-pdpa`, `#id-pdp`, `#vn-pdpd`, `#in-dpdp`. Biometric/CCTV detail anchors in `references/12`: `#face-entry-decision`, `#biometric-bans`, `#changing-room-ban`, `#minors-biometric`, `#cctv-signage`, `#dpias-lite`, `#illegal-camera-incident`.

> All rows: **last-verified: 2026-07**; staleness 180d. Before any citation, run `tools/05` for article-level verification and repeal scan.
> 所有行：**最后核验 2026-07**；保鲜 180 天。引用前跑 `tools/05` 做条款级核验与废止扫描。

## Verification log template / 核验日志模板

Use this shape when `tools/05` records a check (write to `data/16-freshness-ledger.md`) / `tools/05` 记录检查时用此形态（写入 `data/16`）:

```
- anchor: #jp-appi
  law: Act on the Protection of Personal Information (APPI)
  regulator: PPC (ppc.go.jp)
  status: In force / Amended 🔄
  article retrieved: <fill via tools/05>
  retrieved: YYYY-MM-DD
  result: confirmed-in-force | amended | superseded
  action: cite | update | quarantine
```

## Pack-coverage matrix (12 × 4 = 48 rows) / 四件套覆盖矩阵

This index holds one row per market × pack (① privacy ② biometric/CCTV ③ payments/prepaid ④ industry). Count / 计数:
- East Asia & Oceania (6 markets): 24 rows — see `references/10`. / 见 `references/10`。
- South & SE Asia (6 markets): 24 rows — see `references/11`. / 见 `references/11`。
- Total / 合计: **48 four-pack rows** mapped to anchors above.
Every row carries **last-verified: 2026-07** and a 180-day staleness window.

## Quick anchor directory (key IDs) / 锚点速查（关键 ID）

`#cn-pipl` `#cn-cctv` `#cn-prepaid-card` `#cn-sms` · `#hk-pdpo` `#hk-cctv` `#hk-gym` · `#tw-pipa` `#tw-gym-contract` · `#jp-appi` `#jp-appi-biometric` `#jp-tokutei` `#jp-gym` · `#kr-pipa` `#kr-pipa-biometric` `#kr-installment` `#kr-gym` · `#au-privacy-act` `#nz-privacy-act` `#au-cctv` `#au-prepaid` `#au-cooling-off` · `#sg-pdpa` `#sg-cctv` `#sg-casetrust` `#sg-spam` · `#th-pdpa` `#th-cctv` `#th-gym` · `#my-pdpa` `#my-cctv` `#my-gym` · `#id-pdp` `#id-cctv` `#id-gym` · `#vn-pdpd` `#vn-cctv` `#vn-gym` · `#in-dpdp` `#in-cctv` `#in-dnd`. Biometric/CCTV detail in `references/12`: `#face-entry-decision` `#biometric-bans` `#changing-room-ban` `#minors-biometric` `#cctv-signage` `#dpias-lite` `#illegal-camera-incident`.

## Official-domain allow-list (index-only) / 官方域名白名单（仅索引）

Only these official domains are valid retrieval sources for article-level citation / 仅以下官方域名可作条款级引用来源:

| Market / 市场 | Domains / 域名 |
|---|---|
| China mainland / 中国内地 | cac.gov.cn · mps.gov.cn · mofcom.gov.cn · miit.gov.cn |
| Hong Kong (China) / 中国香港 | pcpd.org.hk · consuhk.org.hk |
| Taiwan (China) / 中国台湾 | ndc.gov.tw · cpc.ey.gov.tw |
| Japan / 日本 | ppc.go.jp · meti.go.jp · caa.go.jp |
| South Korea / 韩国 | pipc.go.kr · ftc.go.kr · mol.go.kr |
| Singapore / 新加坡 | pdpc.gov.sg · case.org.sg · imda.gov.sg · acra.gov.sg |
| Thailand / 泰国 | pdpc.or.th · ocpb.go.th |
| Malaysia / 马来西亚 | jpdp.gov.my · kpdn.gov.my |
| Indonesia / 印尼 | kominfo.go.id · ojk.go.id · kppu.go.id |
| Vietnam / 越南 | mps.gov.vn · mocst.gov.vn |
| India / 印度 | meity.gov.in · dpb.gov.in · trai.gov.in · rbi.org.in · ccpa.gov.in |
| Australia/NZ / 澳新 | oaic.gov.au · privacy.org.nz · accc.gov.au · acma.gov.au |

> Never cite news/blogs/aggregators for article numbers — use the official domain + `tools/05`.
> 条款号绝不引用新闻/博客/聚合站——用官方域名 + `tools/05`。

> **G13 tri-perspective note / 三视角注记**: Architect — consume this index to auto-validate every citation anchor in deliverables. Operator — treat "Pending 🔄" rows as "verify before launch". Member — benefits from the uniform consent + alternative + no-HI-5-zone guarantees this index enforces across all 12 markets.
> **G13 三视角**：架构师——用本索引自动校验交付物中每个引用锚点；运营者——把「待决 🔄」行视为「上线前必核」；会员——受益于本索引在 12 市场统一强制的同意 + 替代 + HI-5 禁区保障。
