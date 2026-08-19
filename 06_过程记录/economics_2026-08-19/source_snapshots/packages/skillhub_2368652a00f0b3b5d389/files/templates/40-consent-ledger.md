# Consent Ledger (HI-7 Backbone) / 同意台账（HI-7 主干）

> **Cluster / 集群**: F (12-market compliance) + M (Messaging)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify per-market consent style and anti-spam law every 90 days via `tools/05`; channel rules (WhatsApp/LINE/Kakao/WeChat) shift — verify via `tools/04`.
> **Cross-references / 交叉引用**: `references/10`–`11` (12-market privacy) · `references/17-omnichannel-messaging.md` · `data/21-anti-pattern-library.md` · `references/18-integration-and-data-plumbing.md` (#consent-ledger) · `tools/05-regulation-traceability-verification.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: The single record that proves every member agreed to be contacted, for each purpose, on each channel. It is the backbone of **HI-7** (no consent, no send) and your defense in any spam complaint. Use it from the first marketing message you ever send.
**中文**：唯一一份记录——证明每位会员就每个用途、在每个渠道都同意被联系。它是 **HI-7**（无同意不发送）的主干，也是任何垃圾投诉中的护盾。从你发出第一封营销消息起就用。

> 💡 "Is everyone on this list opted in?" — if you can't answer yes from this ledger, don't send. One opted-out member + one bot call = a fine and a dead campaign (→ `data/21#ap-011-ai-outbound-no-consent`, `#ap-050-whatsapp-no-unsubscribe`).
> 💡 「这名单里每个人都同意了吗？」——若不能从台账答「是」，就别发。一个退订会员+一个机器人电话=罚款且活动腰斩（→ `data/21#ap-011`, `#ap-050`）。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | Consent captured at signup / 注册时征同意 | separate per purpose / 按用途分开 |
| 2 | Channel list / 渠道清单 | SMS/WA/LINE/WeChat/email / 短信/WA/LINE/微信/邮件 |
| 3 | `tools/05` market check / 市场核验 | anti-spam law per market / 各市场反垃圾法 |
| 4 | Withdrawal path / 撤回通道 | unsubscribe works <5 min / 退订<5分生效 |

---

## ③ THE TEMPLATE / 模板正文

### #consent-schema Consent Record Schema / 同意记录结构

One row per (member × purpose × channel):
每（会员 × 用途 × 渠道）一行：

| Field / 字段 | Value / 值 | Rule / 规则 |
|---|---|---|
| Member ID / 会员号 | M____ | not phone-only / 非仅手机 (AP-042) |
| Purpose / 用途 | marketing / biometric / photo / 营销/生物/照片 | separate opt-in / 分别同意 |
| Channel / 渠道 | WA / LINE / WeChat / SMS / email | per channel / 逐渠道 |
| Timestamp / 时间戳 | 2026-07-28 14:03 | immutable / 不可改 |
| Evidence / 证据 | screenshot of consent screen / 同意屏截图 | keep / 留存 |
| Withdrawn? / 撤回? | No / date / 否/日期 | within 72h / 72h内生效 |

> Biometric consent MUST be a separate, explicit opt-in with a non-biometric alternative (HI-1) — never bundled in general T&Cs (→ `data/21#ap-047-biometric-consent-bundled`, `#ap-005-face-entry-no-alt`).
> 生物识别同意必须是独立明确 opt-in 且提供非生物替代（HI-1）——绝不埋进总条款（→ `data/21#ap-047`, `#ap-005`）。

### #per-market-consent Per-Market Consent-Style Notes / 各市场同意风格

🔄 Verify current style via `tools/05` before a cross-market send. / 跨市场发送前经 `tools/05` 核验当前风格。

| Market / 市场 | Consent style / 风格 | Channel / 渠道 | Note / 备注 |
|---|---|---|---|
| CN | explicit opt-in / 明示同意 | WeChat / 微信 | unbundle biometric / 生物拆开 |
| SG/MY | opt-in + unsubscribe / 同意+退订 | WhatsApp / WA | PDPA-aligned / 合 PDPA |
| JP | opt-in, polite / 同意，礼貌 | LINE / LINE | consent log retained / 留同意日志 |
| KR | opt-in | Kakao / Kakao | ---
| AU/NZ | spam-act opt-in / 反垃圾同意 | SMS/email | strict / 严 |
| TH/VN/PH | opt-in | LINE/WA/Zalo | verify / 核验 |

### #campaign-preflight Campaign Pre-Flight Check / 活动发前核查

Before every send, answer:
每次发送前回答：

- [ ] List built ONLY from ledger rows with Purpose=marketing AND Channel=this one AND Withdrawn=No. / 名单仅取自台账「营销+本渠道+未撤回」。
- [ ] Unsubscribe link clicked on 3 devices pre-send. / 发前在3设备点过退订。
- [ ] DNC / opt-out list cross-checked (AI calls too). / 免联系名单已核（AI电话亦）。
- [ ] Screenshot of consent retained for the oldest 5% of list. / 最老5%名单留同意截图。

> "Is everyone on this list opted in?" — if any NO, remove before send (HI-7).
> 「名单里每个人都同意了吗？」——有「否」就先删再发（HI-7）。

### #withdrawal-sop Withdrawal-Processing SOP / 撤回处理 SOP

1. Member clicks unsubscribe / requests removal. / 会员点退订/申请删。
2. Log withdrawal timestamp in ledger. / 台账记撤回时间。
3. Propagate to ALL systems within 72h (MMS, SCRM, ad platform, AI caller). / 72h 内全系统生效（会籍、私域、广告、AI外呼）。
4. Confirm deletion of PII/photo/biometric where lawful. / 依法删 PII/照片/生物。
5. Keep the withdrawal record (proof). / 留撤回记录（证据）。

> Cross-system within 72h — a half-deleted member is still a breach (→ `references/18#consent-ledger`, HI-8).
> 全系统 72h 内——删一半的会员仍是泄露（→ `references/18#consent-ledger`, HI-8）。

---

## ④ Common Mistakes / 常见错误

- **AI outbound without consent/DNC** → fine, campaign killed. → `data/21#ap-011-ai-outbound-no-consent` (HI-7).
- **WhatsApp blast, dead unsub** → reputation dies. → `data/21#ap-050-whatsapp-no-unsubscribe`.
- **Biometric bundled in T&Cs** → invalid consent. → `data/21#ap-047-biometric-consent-bundled` (HI-1).
- **Withdrawal not propagated** → still breached. → `references/18#consent-ledger`.

---

## ⑤ Related Files / 相关文件

- `references/10`–`11` (12-market privacy) — per-market consent law. / 各市场同意法。
- `references/17-omnichannel-messaging.md` — channel templates. / 渠道模板。
- `references/18-integration-and-data-plumbing.md` — `#consent-ledger` cross-system sync. / 跨系统同意同步。
- `data/21-anti-pattern-library.md` — AP-011, AP-050, AP-047.

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: The ledger is the compliance backbone of Cluster F/M; it operationalizes HI-7 (no consent, no send) and HI-1 (separate biometric consent) at the data layer, with per-market style verified via `tools/05`.
**运营者 / Operator**: A fill-in schema + pre-flight check means a marketer can prove every send was permitted — no legal team on call; it is the operator's shield in any spam complaint.
**会员 / Member**: Members control their own contact preferences per purpose and channel, with a working withdrawal — trust protected by consent and minimization (HI-7, HI-8).
