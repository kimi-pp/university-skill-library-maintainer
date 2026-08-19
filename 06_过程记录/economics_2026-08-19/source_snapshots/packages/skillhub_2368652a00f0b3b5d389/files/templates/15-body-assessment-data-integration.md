# 15 · Body-Composition & Posture Scanner Data Integration / 体测仪与体态扫描数据集成模板

> **Cluster / 集群**: C (Hardware C6) + B (Body software) + E (Health data) · Template / 模板 · System-Building tier (FDMM L2)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Health-data retention & medical-device class re-verify every 90 days via `tools/05`; device accuracy claims are volatile.
> **Cross-references / 交叉引用**: `references/07-hardware-landscape-and-vendors.md` (C6 body) · `tools/05-regulation-traceability-verification.md` · `data/21-anti-pattern-library.md#ap-034-bot-medical-answer` · `data/21#ap-002-no-data-export` · `templates/09-mms-selection-scorecard.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/05` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/05` 动态情报检索。

---

## ① Purpose & when to use (FDMM gate) / 用途与适用（FDMM 闸门）

**Purpose / 用途**: A template to integrate body-composition analyzers and posture scanners into the MMS as trend data — explicitly NOT diagnosis.
**用途 / 中文**：将体测仪与体态扫描作为「趋势数据」集成进 MMS 的模板——明确非诊断。

**When to use / 适用场景**:
- You operate InBody-class BIA or posture scanners — L2. / 运营 InBody 类生物电阻抗或体态扫描——L2。
- You want trends visible to member + coach in-app. / 想让会员与教练在 App 看趋势。
- **HI-1 gate / 闸门**: Recorded consent MUST be obtained BEFORE any scan; cite legal basis per market via `tools/05`. / 任何扫描前必须取得「已记录同意」；合规依据经 `tools/05` 按市场标注。
- **HI-6 gate / 闸门**: Never present results as medical diagnosis; refer to a qualified professional. / 绝不将结果表述为医疗诊断；转介专业人士。
- **HI-8 gate / 闸门**: Collect only body metrics needed; no surplus health inference. / 仅采所需体测指标；不做多余健康推断。

---

## ② Prerequisites checklist / 前置清单

- [ ] Body hardware chosen (`references/07` C6) with local medical-device class confirmed. / 体测硬件已选（C6）且本地医疗器械分级已确认。
- [ ] Consent legal basis per market drafted via `tools/05` (HI-1). / 各市场同意合规依据经 `tools/05` 拟（HI-1）。
- [ ] Retention & deletion schedule per market set (🔄 `tools/05`). / 各市场留存与删除计划已设（🔄 `tools/05`）。
- [ ] MMS ready to store measurement CSV per member. / MMS 可存每位会员测量 CSV。
- [ ] Coach trained to say "trend, not diagnosis" (HI-6). / 教练受训说"趋势非诊断"（HI-6）。

---

## ③ The template / 模板正文

### 3.1 Consent flow design (HI-1, recorded BEFORE scan) / 同意流程设计

> **Rule / 规则**: No scan starts without a stored, timestamped consent record linked to the member. / 无关联会员的带时间戳同意记录，绝不开始扫描。
> **What good looks like / 合格标准**: consent captured in-app with purpose + retention period shown; member can withdraw. / App 内采集同意，展示目的与留存期；会员可撤回。
> **Red flag / 红旗**: scanning first, asking later → unlawful in most APAC markets (HI-1). / 先扫后问 → 多数亚太市场不合规（HI-1）。

| Step / 步骤 | Action / 动作 | Recorded field / 记录字段 |
|---|---|---|
| 1 | Show purpose + retention / 展示目的+留存 | purpose, retention_days |
| 2 | Member taps Agree / 会员点同意 | consent=YES, timestamp |
| 3 | Scan proceeds / 开始扫描 | measurement_id linked to consent |
| 4 | Withdraw anytime / 随时撤回 | consent_revoked, timestamp |

### 3.2 Data schema mapping to MMS / 数据模式映射到 MMS

| Device field / 设备字段 | MMS field / MMS 字段 | Type / 类型 | Note / 注 |
|---|---|---|---|
| member_id | mms_member_id | string | Scan-to-link / 扫码关联 |
| weight_kg | body.weight | float | |
| fat_pct | body.fat_pct | float | Trend only / 仅趋势 |
| muscle_kg | body.muscle | float | |
| posture_score | body.posture | int | Not diagnosis / 非诊断 |
| measured_at | body.measured_at | datetime | |
| consent_id | body.consent_id | string | FK to consent / 外键 |

> **Rule / 规则**: every measurement row carries `consent_id` and `retention_until`. / 每条测量带 `consent_id` 与 `retention_until`。

### 3.3 Retention & deletion schedule per market (🔄 verify `tools/05`) / 分市场留存与删除计划

:::dynamic-hook topic="apac-health-data-retention-2026" staleness="180d" action="tools/05" fallback="treat as unverified"
As of 2026-07: health/body data is treated as sensitive personal data across APAC; many markets require purpose-limited retention (e.g. 1–3 years) and deletion on withdrawal. Exact period per market must be verified via tools/05 before go-live.
截至 2026-07：体测数据在亚太多被视为敏感个人信息；多市场要求限目的留存（如 1–3 年）且撤回即删。各市场确切期限上线前经 tools/05 核验。
:::

| Market / 市场 | Retention / 留存 | Delete on withdraw? / 撤回即删? | Basis (🔄) / 依据 |
|---|---|---|---|
| China 大陆 | purpose-limited / 限目的 | Yes / 是 | PIPL art.19 / 个保法19条 |
| Japan 日本 | ≤ necessary / 必要内 | Yes / 是 | APPI |
| Korea 韩国 | ≤ necessary / 必要内 | Yes / 是 | PIPA |
| EU-style ANZ | defined period / 定期限 | Yes / 是 | Privacy Act |
| India 印度 | minimal / 最小 | Yes / 是 | DPDPA |

> **Red flag / 红旗**: keeping body data forever "just in case" breaches HI-8 minimisation. / 为"以防万一"永久存体测数据违反 HI-8 最小化。

### 3.4 Coach workflow script / 教练工作流脚本

1. Member books body-test in app. / 会员 App 约体测。
2. Coach confirms consent on screen (HI-1). / 教练屏幕确认同意（HI-1）。3. Run scan; device posts CSV to MMS. / 扫描；设备传 CSV 至 MMS。
4. Coach shows **trend chart**, says: "This shows change over time — not a medical diagnosis. For health concerns, see a doctor." (HI-6). / 教练展示趋势图并说："这看变化，不是医疗诊断；健康问题看医生。"（HI-6）
5. Share PDF to member app; log the session. / 推 PDF 给会员 App；记录会话。

### 3.5 Accuracy-claim honesty note (HI-6) / 精度宣称诚实注记

> **Hard rule / 铁律**: Do NOT claim "hospital-grade", "diagnoses obesity", or "detects disease" without local certification + qualified oversight. / 无本地认证+专业背书，不得宣称"医院级""诊断肥胖""检出疾病"。
- BIA gives estimates; hydration/meal/time-of-day shift numbers. / BIA 是估算；饮水/进食/时段会影响。
- Posture score is a coaching aid, not a clinical screen. / 体态分是教练辅助，非临床筛查。
- If a member result looks clinically alarming, advise a clinician — never interpret it yourself (HI-6). / 结果疑似异常，建议看医生，绝不自行解读（HI-6）。

> **Red flag / 红旗**: `data/21#ap-034-bot-medical-answer` — an AI/chatbot giving medical interpretation of body data. / AI/聊天机器人对体测数据作医疗解读（见锚点）。

---

### 3.6 Worked consent record / 同意记录实例

- member_id=M-882; purpose="progress trend"; retention_days=365; consent=YES @2026-07-28T10:02Z. / 会员 M-882；目的"进步趋势"；留存 365 天；同意@时间。
- measurement_id=B-55121 linked to consent_id=C-882 (FK). / 测量 B-55121 关联同意 C-882（外键）。
- Withdraw @2026-09-01 → row flagged consent_revoked; deletion job purges at retention end or on request (HI-8). / 9/1 撤回 → 标已撤；删除任务在留存期末或应请求清除（HI-8）。
- Coach line / 教练话术: "Your fat% moved 2 points in 8 weeks — a trend, not a diagnosis. See a clinician for health questions." (HI-6). / "8 周体脂动 2 点——是趋势非诊断；健康问题看医生。"（HI-6）

### 3.7 Go-live privacy checklist / 上线隐私清单

- [ ] Consent captured BEFORE scan, linked to every measurement (HI-1). / 扫描前已取得同意，关联每条测量（HI-1）。
- [ ] Retention & deletion schedule per market set (🔄 `tools/05`). / 各市场留存与删除计划已设（🔄 tools/05）。
- [ ] No diagnosis language in UI or coach script (HI-6). / UI 与教练话术无诊断用语（HI-6）。
- [ ] Only body metrics collected; no surplus inference (HI-8). / 仅采体测指标；无多余推断（HI-8）。
- [ ] Measurement CSV exportable from MMS (`data/21#ap-002`). / 体测 CSV 可导出 MMS。
- [ ] Deletion job tested: withdraw → purge within stated window. / 删除任务已测：撤回→窗口内清除。

### 3.8 Accuracy honesty deep-dive / 精度诚实详解

| Allowed / 允许 | Forbidden / 禁止 |
|---|---|
| "Your trend improved over 8 weeks" / "8 周趋势改善" | "Diagnoses obesity" / "诊断肥胖" |
| "Muscle mass up 1.2kg" / "肌肉增 1.2kg" | "Detects liver disease" / "检出肝病" |
| "Posture score 72/100, coach can help" / "体态分72，教练可帮" | "Replaces physiotherapist" / "替代康复师" |

> **Hard line / 红线**: any health-grade conclusion → refer to a qualified professional (HI-6). The Skill never diagnoses. / 任何医疗级结论→转介专业人士（HI-6）。本 Skill 不做诊断。

### 3.9 Withdrawal flow one-liner / 撤回流程一句话

> **Pass criterion / 通过判据**: "Member withdraws consent → all linked measurements flagged revoked → purged within the stated retention window, with a deletion log entry." / 「会员撤回同意→关联测量全标撤→窗口内清除并留删除日志」即为通过。

## ④ Common mistakes (anti-patterns) / 常见错误（反模式）

- `data/21#ap-034-bot-medical-answer` — medical interpretation by bot. / 机器人作医疗解读。
- `data/21#ap-002-no-data-export` — body CSV trapped in vendor cloud. / 体测 CSV 困在厂商云。
- `data/21#ap-005-face-entry-no-alt` — posture scanner doubling as face capture. / 体态扫描兼做人脸采集。
- `data/21#ap-029-autodelete-inactive` — auto-deleting inactive members' health data without retention rules. / 无留存规则自动删 inactive 会员健康数据。

---

## ⑤ Related files / 相关文件

- `references/07-hardware-landscape-and-vendors.md` (C6). / 体测硬件。
- `tools/05-regulation-traceability-verification.md` — consent & retention law. / 同意与留存法。
- `references/16-security-operations-and-emergency.md` (§S health boundary). / 医疗边界。
- `templates/09-mms-selection-scorecard.md` — MMS stores the CSV. / MMS 存 CSV。

---

## ⑥ G13 tri-perspective note / G13 三视角覆盖说明

This template serves **Architect** (schema + retention mapping + consent link), **Operator** (coach script + deletion runbook), and **Member** (informed consent, trend insight, data deletion right, no medical mislabel); the HI-1 consent-before-scan and HI-6 no-diagnosis clauses protect the member's bodily-data autonomy and safety — no orphaned touchpoint.
本模板覆盖**架构师**（模式+留存映射+同意关联）、**运营者**（教练脚本+删除手册）、**会员**（知情同意、趋势洞察、删除权、无医疗误标）；HI-1 先同意后扫与 HI-6 不诊断守护会员身体数据自主权与安全——无孤儿触点。
