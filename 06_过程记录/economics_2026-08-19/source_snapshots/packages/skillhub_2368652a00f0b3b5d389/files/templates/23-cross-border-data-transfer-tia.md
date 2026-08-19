# Cross-Border Data Transfer Assessment (TIA-lite) / 跨境数据传输评估（轻量 TIA）

> **Cluster / 集群**: F (12-market compliance) + K (AI governance & cloud sovereignty)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Transfer mechanisms are HIGHLY volatile — every market's rule re-verify via `tools/05` before citing; no article numbers are asserted as final. Prices 🔄 via `tools/04`.
> **Cross-references / 交叉引用**: `references/10`/`references/11` (market compliance), `references/12` (biometric/CCTV), `data/02-regulation-traceability-index.md`, `SKILL.md` HI-9 (data sovereignty), `templates/20` (data residency clause).
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/05` before relying on them; do NOT invent article numbers.
> 标注 🔄 的事实易变——引用前先跑 `tools/05`；不得编造条款号。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用时机（FDMM 闸门）

Use this TIA-lite to decide **whether and how member data may cross a border** across your APAC chain (HQ cloud in one market, members in another). It is the compliance gate before any cross-border sync, backup, or group-BI feed.
本轻量 TIA 用于决定**会员数据能否及如何跨境**（总部云在一国、会员在另一国）。是任何跨境同步、备份、集团 BI 前的合规闸门。

- **FDMM gate / 等级闸门**: L4 (chain expansion / cross-border). Single-market L1–L3 rarely triggers; but a cloud vendor storing data offshore still does.
  L4（连锁扩张/跨境）。单市场 L1–L3 少触发；但云商境外存数据仍触发。
- **Trigger / 触发**: members in market A, servers/Group in market B; or "our SaaS is hosted in [foreign region]".
  会员在 A 市、服务器/集团在 B 市；或"我们 SaaS 托管在[境外]"。

---

## ② Prerequisites checklist / 前置清单

- [ ] Data inventory & flow map done (§3.1). / 数据清单与流向图已完成（§3.1）。
- [ ] Each market's privacy law identified via `tools/05` (`data/02`). / 各市场隐私法经 `tools/05` 识别（`data/02`）。
- [ ] Biometric/health data flagged (HI-1, HI-9 local-first). / 生物/健康数据已标（HI-1、HI-9 本地优先）。
- [ ] Transfer mechanism per market verified — NOT assumed (`tools/05`). / 各市场传输机制已核验——勿假定。
- [ ] Approval cadence set (§3.5). / 审批节奏已定（§3.5）。

---

## ③ THE TEMPLATE / 模板正文

### 3.1 Data inventory & flow map / 数据清单与流向图

| Data type / 数据类型 | Example / 例 | Origin market / 来源市 | Stored where / 存于 | Crosses border? / 跨境? |
|---|---|---|---|---|
| Member PII 会员个人信息 | name/phone/email | `____` | `____` | Y/N |
| Biometric 生物识别 | face template | `____` | `____` | Y/N (prefer N) |
| Health 健康 | body-scan | `____` | `____` | Y/N (prefer N) |
| Payment 支付 | card/txn | `____` | `____` | Y/N |
| Consent logs 同意记录 | opt-in | `____` | `____` | Y/N |

> **Guidance / 指引**: Draw the arrow: member → local club → [border?] → HQ cloud. Count every crossing. Minimise; biometric templates local-first where the market demands (HI-9, HI-8).
> 画箭头：会员→本店→[跨境?]→总部云。数清每次跨越。最小化；生物模板按市场本地优先（HI-9、HI-8）。

### 3.2 Per-market transfer mechanism table / 各市场传输机制表

:::dynamic-hook topic="apac-cross-border-transfer-mechanisms-2026" staleness="90d" action="tools/05" fallback="treat as unverified"
Mechanisms differ by market and change often — verify the exact current route (SCC / assessment / adequacy / binding rules) via `tools/05` before relying. Below are POSITIONS TO VERIFY, not fixed legal statements.
各市场机制差异大且常变——引用前经 `tools/05` 核验确切路径（标准合同/评估/充分性/约束性规则）。以下为"待核验立场"，非固定法律结论。
:::

| Market / 市场 | Likely mechanism (VERIFY 🔄) / 可能机制（核验） | Local residency requirement / 本地驻留要求 | Action / 动作 |
|---|---|---|---|
| Chinese Mainland 中国大陆 | PIPL: standard contract (SCC) filing OR security assessment OR certification — verify exact route & threshold via `tools/05` | biometric/health local-first; cross-border needs declared basis | run TIA + file/assess |
| Hong Kong (China) 中国香港 | transfer under PDPO; verify ORO requirement via `tools/05` | generally permitted with safeguards | DPIA + notice |
| Singapore 新加坡 | PDPA: rely on consent / comparable protection; verify transfer provisions via `tools/05` | no absolute residency; need comparable protection | consent + clauses |
| Japan 日本 | APPI: same-purpose / consent / take measures; verify article via `tools/05` | allowable with safeguards | measures + notice |
| South Korea 韩国 | PIPA: separate consent + safety measures; verify via `tools/05` | strict; separate consent | consent + encryption |
| Australia 澳洲 | Privacy Act: APP 8 cross-border accountability; verify via `tools/05` | accountability for overseas recipient | recipient contract |
| Others (SEA/India/NZ) 其他 | verify each via `tools/05` | varies | per-market |

> **Honesty note / 诚实提示**: No article numbers asserted above are final. Exact clauses MUST be re-verified against the effective version on the retrieval day via `tools/05`; major matters require licensed counsel (`SKILL.md` Freshness Law + HI-1).
> 上表未断言任何最终条款号。确切条款须经 `tools/05` 按检索日有效版本复核；重大事项须持证法律顾问。

### 3.3 Risk scoring / 风险评分

Score each transfer 1–5 (5 = highest risk); sum to decide mitigations.
对每个传输按 1–5 评分（5=最高风险）；合计定缓释。

| Factor / 因子 | Weight / 权重 | Score / 分 |
|---|---|---|
| Data sensitivity 敏感性 (biometric=5) | 30% | `____` |
| Volume 量级 | 20% | `____` |
| Mechanism maturity 机制成熟度 | 25% | `____` |
| Recipient jurisdiction 接收方法域 | 15% | `____` |
| Reversibility 可逆性 | 10% | `____` |
| **Risk level 风险级** | | `____` (low/med/high) |

> High = block or pseudonymise + SCC/assessment before any flow. / 高=先阻断或假名化+标准合同/评估再放行。

### 3.4 Safeguards checklist / 缓释措施清单

- [ ] Minimum necessary data only (HI-8). / 仅最小必要（HI-8）。
- [ ] Encryption in transit + at rest. / 传输+静态加密。
- [ ] Pseudonymisation for analytics feeds. / 分析流假名化。
- [ ] Biometric/health local-first where required (HI-9, HI-1). / 生物/健康按需本地优先。
- [ ] Member consent + transparent notice (HI-7). / 会员同意+透明告知（HI-7）。
- [ ] Data-export & deletion clause in vendor contract (`templates/20`). / 供应商合同含导出与删除条款。
- [ ] Incident response for cross-border breach. / 跨境泄露应急响应。

### 3.5 Approval & review cadence / 审批与复核节奏

- Approver: `____` (DPO / legal / owner). / 审批人：`____`（数据官/法务/老板）。
- Review: every `____` months OR on any law change (tools/05 trigger). / 复核：每 `____` 月或法规变动（tools/05 触发）。
- Re-run TIA before entering any NEW market. / 进新市场前重跑 TIA。
- Log decision + dissent in the vendor decision record (`templates/21`). / 决策+异议记入供应商决策记录。

---

## ④ Common mistakes / 常见错误

1. Assuming "cloud is global" = compliant. / 以为"云是全球的"=合规。
2. Inventing article numbers without verify. / 编造条款号未核验。→ use `tools/05`
3. Biometric template shipped offshore by default. / 生物模板默认出境。→ HI-9, HI-1
4. No consent for cross-border transfer. / 跨境传输无同意。→ HI-7
5. One TIA for all markets (ignores divergence). / 全市场用一份 TIA（忽视差异）。

---

## ⑤ Related files / 相关文件

- `references/10-apac-compliance-east-asia-oceania.md` — EA/Oceania rules / 东亚大洋洲
- `references/11-apac-compliance-south-southeast-asia.md` — S/SE Asia rules / 南亚东南亚
- `references/12-biometrics-and-cctv.md` — biometric local-first / 生物本地优先
- `data/02-regulation-traceability-index.md` — article traceability / 条款溯源
- `tools/05-regulation-traceability-verification.md` — verify before cite / 引前核验
- `templates/20-rfp-technical-spec.md` — data residency clause / 数据驻留条款

---

## ⑥ G13 tri-perspective note / 三视角覆盖说明

This template serves **Architect** (flow map + mechanism table + safeguards), **Operator** (risk scoring + review cadence + consent ops), and **Member** (data sovereignty, biometric local-first, transparent cross-border notice, deletion right); every market cell is flagged 🔄 to enforce `tools/05` verification rather than assumed compliance.
本模板覆盖**架构师**（流向图+机制表+缓释）、**运营者**（风险评分+复核节奏+同意运营）、**会员**（数据主权、生物本地优先、透明跨境告知、删除权）；每市场格标 🔄，强制 `tools/05` 核验而非假定合规。
