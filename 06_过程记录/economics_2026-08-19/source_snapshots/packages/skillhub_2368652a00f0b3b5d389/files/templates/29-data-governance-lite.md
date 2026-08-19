# Data Governance for Non-IT People / 给非 IT 人员的数据治理

> **Cluster / 集群**: K (AI governance) + F (compliance) + I (IT governance)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Retention/deletion & member-rights rules 🔄 re-verify via `tools/05` per market before acting; vendor DPO claims via `tools/04`.
> **Cross-references / 交叉引用**: `references/13-data-and-llm-engine.md#k-11-consent-ledger` · `references/10`+`references/11` (12-market compliance) · `data/21-anti-pattern-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04`/`tools/05` before relying on them.

---

## ① Purpose & when to use / 用途与适用时机

**Use this lite governance pack to run data responsibly without a data team** — classify data, assign owners, set retention, and handle member access/deletion requests correctly.
**用此轻量治理包在无数据团队时负责任管数据**——分类、定负责人、设留存、正确处理会员查询/删除请求。

> **FDMM gate / FDMM 门槛**: Lightweight governance (classification + consent + deletion handling) applies from **L1**. A formal program (registry, residency ledger, annual review) matures at **L3+** (`references/13#k-5-ai-governance`).
> **FDMM 门槛**：轻量治理（分类+同意+删除处理）**L1 起**即适用。正式项目（注册表、驻留账、年审）于 **L3+** 成熟（`references/13#k-5-ai-governance`）。

> **If below L3 / 若低于 L3**: use only §3.1–§3.4 (classify, assign owners, set retention, handle requests). Do not stand up a registry you cannot maintain. Scale the program as you grow.
> **若低于 L3**：仅用 §3.1–§3.4（分类、定负责人、设留存、处理请求）。勿建维护不了的注册表。随成长扩展项目。

---

## ② Prerequisites checklist / 前置条件清单

- [ ] **Data inventory** exists (start from `templates/28#d1-source-inventory`). / 数据清单存在（从 `templates/28#d1-source-inventory` 起步）。
- [ ] **A named owner** for each data class. / 每数据类有具名负责人。
- [ ] **Consent records** captured (marketing/biometric/health separate). / 同意记录已采（营销/生物/健康分开）。
- [ ] **Market identified** for residency/retention rules. / 已定市场以明驻留/留存规则。
- [ ] **Deletion-request channel** members can reach. / 会员可触达的删除请求通道。

---

## ③ THE TEMPLATE / 模板

### 3.1 Data classification table / 数据分类表 {#g1-classification}

| Class / 类别 | Examples / 示例 | Risk / 风险 | Who can see / 可见人 |
|---|---|---|---|
| Public / 公开 | class schedule, prices / 课表、价格 | low / 低 | anyone / 任何人 |
| Internal / 内部 | revenue, roster / 营收、排班 | med / 中 | staff only / 仅员工 |
| Personal / 个人 | name, phone, email, attendance / 姓名手机邮箱出勤 | high / 高 | owner + consented staff / 负责人+同意员工 |
| Sensitive-biometric-health / 敏感-生物-健康 | face template, body-scan, health flag / 人脸模板、体测、健康标记 | **highest / 最高** | strictly gated, legal basis (HI-1/HI-6/HI-8) |

> HI-8: collect the minimum; sensitive classes only with explicit, purpose-bound consent. / HI-8：最小化采集；敏感类仅经明确、目的绑定同意。

### 3.2 Owner & steward assignment sheet / 负责人与管家分配表 {#g2-owners}

| Data class / 数据类 | Owner / 负责人 | Steward / 管家 | Review cadence / 复核节奏 |
|---|---|---|---|
| Personal / 个人 | club manager / 店长 | front-desk lead / 前台主管 | quarterly / 季 |
| Sensitive-biometric / 敏感生物 | data owner + legal / 数据负责人+法务 | — | per market law / 按市场法 |
| Internal / 内部 | ops lead / 运营主管 | — | half-year / 半年 |

- One named human per class — never "the system". / 每类一个具名自然人——绝不说「系统」。

### 3.3 Retention & deletion schedule per class × market 🔄 / 按类×市场的留存与删除排期 {#g3-retention}

:::dynamic-hook topic="retention-deletion-per-market" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07: retention periods differ by market and data class — e.g. CN PIPL requires personal info minimized and deleted when purpose fulfilled; SG PDPA reasonable retention; IN DPDP 2023 rules pending; AU APPs. Verify the exact maximum retention + deletion clock for YOUR market via tools/05 before publishing this schedule. / 截至 2026-07：留存期因市场与数据类而异——如中国 PIPL 要求个人信息最小化、目的达成即删；新加坡 PDPA 合理留存；印度 DPDP 2023 细则待定；澳洲 APP。发布本排期前经 tools/05 核验你市场的确切最长留存+删除时限。
:::

| Data class / 数据类 | CN / 中国 | SG / 新加坡 | JP / 日本 | AU / 澳洲 | IN / 印度 |
|---|---|---|---|---|---|
| Personal / 个人 | per PIPL / 依PIPL | reasonable / 合理 | APPI | APPs | DPDP pending |
| Biometric / 生物 | onshore, delete on exit / 本地、退出即删 | consent-based | APPI | health-privacy | DPDP pending |
| Health flag / 健康 | only if given / 仅经同意 | consent | APPI | health-privacy | DPDP pending |

> Fill the cells with your verified periods; do not invent numbers. / 用你核验过的期限填格；勿编数字。

### 3.4 Access-request & deletion-request SOP forms / 查询与删除请求 SOP 表单 {#g4-sop}

**Access request (member asks "what do you hold on me?") / 查询请求（会员问「你们存了我什么？」）**
```
1. Verify identity (phone+email match). / 核验身份（手机+邮箱一致）。
2. Compile only that member's data, redacted of others. / 仅汇编该会员数据，脱去他人。
3. Respond within market clock (verify via tools/05). / 在市场时限内回复（经tools/05核）。
4. Log request + response date. / 记请求+回复日。
```

**Deletion request (member asks "delete my data") / 删除请求（会员说「删我数据」）**
```
1. Verify identity. / 核验身份。
2. Delete personal data; wipe biometric template per market law (HI-1). / 删个人数据；按市场法擦除生物模板（HI-1）。
3. Keep only legally-required minimum records, flagged. / 仅留法定必需最小记录并标注。
4. Confirm deletion to member; log it. / 向会员确认删除并记。
```
> PIPL/DPDP-style rights: access, correction, deletion, portability — honour within the market's clock. / PIPL/DPDP 式权利：查询、更正、删除、可携——在市场时限内履行。

### 3.5 Quality rules top-10 / 质量规则 Top-10 {#g5-quality-rules}

1. Every member has one stable ID (no duplicates). / 每会员一个稳定 ID（无重复）。
2. One churn definition across stores. / 各店一个流失定义。
3. No raw PII into any LLM — redact first. / 原始 PII 不进大模型——先脱敏。
4. Consent separate: marketing / biometric / health. / 同意分离：营销/生物/健康。
5. Biometric templates local-first, reference only. / 生物模板本地优先、仅存引用。
6. Retention clock per class × market enforced. / 按类×市场执行留存时钟。
7. Deletion request honoured within market clock. / 删除请求在市场时限内履行。
8. No collection without stated purpose (HI-8). / 无声明目的不采集（HI-8）。
9. Access logged; least-privilege by role. / 访问留痕；按角色最小权限。
10. Residency ledger updated when rules change. / 规则变时更新驻留账。

### 3.6 Annual review checklist / 年度复核清单 {#g6-annual-review}

- [ ] Re-verify retention/deletion rules via `tools/05` (🔄). / 经 tools/05 复核留存/删除规则。
- [ ] Confirm every data class has a living owner. / 确认每数据类有在世负责人。
- [ ] Audit consent ledger completeness. / 审计同意中枢完整性。
- [ ] Test one deletion request end-to-end. / 端到端测一次删除请求。
- [ ] Residency ledger vs actual storage match. / 驻留账 vs 实际存储一致。
- [ ] Bias audit refreshed for any production model. / 刷新任何量产模型的偏见审计。

### 3.7 Breach notification (if PII leaks) / 泄露通知（若 PII 泄露） {#g7-breach}

> If personal/sensitive data leaks, several APAC regimes impose a notification clock — act fast and document.
> 若个人/敏感数据泄露，多个亚太法域设通知时限——快行动并留档。

1. Contain: revoke access, isolate the store. / 遏制：撤权、隔离存储。
2. Assess scope: which members, which classes. / 评估范围：哪些会员、哪些类。
3. Notify per market clock (verify via `tools/05`, e.g. some regimes ~72h). / 按市场时限通知（经 tools/05 核，部分法域约 72h）。
4. Post-mortem logged; fix root cause. / 根因复盘留档并修复。

---

## ④ Common mistakes / 常见误区

- **No classification** → sensitive data treated like public. / 无分类→敏感数据当公开。
- **"The system" owns data** → no accountability. / 「系统」管数据→无问责。
- **Invented retention numbers** → compliance liability. / 编留存数字→合规负债。
- **Ignoring deletion requests** → direct violation (HI-1/HI-8). / 忽视删除请求→直接违规（HI-1/HI-8）。
- **Raw PII to LLM** → leak. / 原始 PII 进大模型→泄露。

> Full remedy catalogue: `data/21-anti-pattern-library.md`.
> 完整对策：见 `data/21-anti-pattern-library.md`。

---

## ⑤ Related files / 相关文件

- `references/13-data-and-llm-engine.md#k-11-consent-ledger` — consent separation. / 同意分离。
- `references/13-data-and-llm-engine.md#k-12-residency-ledger` — residency ledger. / 驻留账。
- `references/10`+`references/11` — 12-market compliance mapping. / 12 市场合规映射。
- `templates/28-data-platform-blueprint.md` — source inventory start. / 源清单起点。

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

- **Architect / 架构师**: classification → owner → retention × market → SOP forms, all traceable to HI-1/HI-6/HI-8 and market law via tools/05.
- **Operator / 运营者**: plain-language sheets, top-10 rules, annual checklist — runnable without a data team.
- **Member / 会员**: explicit consent, access/deletion rights honoured, biometric deleted on exit, no over-collection (HI-8), data minimised and protected.
本文件覆盖架构师（分类→负责人→按市场留存→SOP 表单，全可追溯至 HI-1/HI-6/HI-8 与市场法经 tools/05）、运营者（说人话的表、Top-10 规则、年审清单——无数据团队可运转）、会员（明确同意、查询/删除权履行、退出删生物特征、不过采 HI-8、最小化受护）。
