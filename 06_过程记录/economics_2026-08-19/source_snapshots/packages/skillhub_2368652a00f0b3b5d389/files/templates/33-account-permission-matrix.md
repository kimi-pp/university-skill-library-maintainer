# Account & Permission Matrix / 账号与权限矩阵

> **Cluster / 集群**: I (IT governance & money) + J (Resilience & responsibility)
> **Last verified / 最后核验**: 2026-07
> **Staleness rule / 保鲜规则**: Re-verify breach-notification and offboarding rules every 90 days via `tools/05`; vendor admin-role names shift — verify via `tools/04`.
> **Cross-references / 交叉引用**: `references/16-security-operations-and-emergency.md` (#j-offboarding-checklist, #j-password-manager-mfa) · `data/21-anti-pattern-library.md` · `data/14-repair-scripts-and-sla-library.md`
> **Retrieval note / 检索提示**: Facts marked 🔄 are volatile — run `tools/04` before relying on them.
> 标注 🔄 的事实易变——引用前先跑 `tools/04` 动态情报检索。

---

## ① Purpose & When to Use / 用途与使用时机

**English**: The printable grid that says who may touch what, the checklist to grant access on hire, and the **kill-list to revoke it on leave — same day, gate access FIRST**. Prevents the #1 insider breach: the leaver who still opens the back gate.
**中文**：可打印的「谁能动什么」矩阵、入职授权清单、以及**离职当天撤销的击杀清单——闸机访问置顶**。防头号内鬼：仍握后门闸机码的前员工。

> 💡 Least privilege = give the minimum role that gets the job done. A front-desk clerk does NOT need the gate-admin or finance console. Over-permission is a leak waiting to happen.
> 💡 最小权限 = 只给刚好够用的角色。前台绝不需要闸机后台或财务后台。过度授权是随时会漏的口子。

---

## ② Prerequisites / 前置条件

| # | Need / 需要 | Note / 说明 |
|---|---|---|
| 1 | List of systems in use / 在用系统清单 | MMS, POS, gate, email, Wi-Fi, CCTV, social, cloud… / 会籍、收银、闸机、邮箱、无线、监控、社媒、云盘… |
| 2 | Role definitions / 角色定义 | owner / manager / FD / coach / cleaner / 老板/店长/前台/教练/保洁 |
| 3 | Password manager live / 密码管理器已用 | see `#pm-rollout` below / 见下方 |
| 4 | JML one-pager signed at hire / 入职一页纸 | from `references/16#j-offboarding-checklist` |

---

## ③ THE TEMPLATE / 模板正文

### #role-grid System × Role Grid / 系统×角色矩阵

Legend / 图例: R=read 读 · W=write 写 · A=admin 管 · — = none 无

| System / 系统 | Owner | Manager | Front Desk | Coach | Cleaner |
|---|---|---|---|---|---|
| MMS / CRM | A | A | W | R | — |
| POS | A | A | W | — | — |
| Gate admin / 闸机后台 | A | A | — | — | — |
| Email / 邮箱 | A | W | W | R | R |
| Wi-Fi admin / 无线后台 | A | A | — | — | — |
| CCTV console / 监控台 | A | A | R | — | — |
| Social / ad accounts / 社媒广告 | A | W | — | — | — |
| Cloud / file shares / 云盘 | A | W | R | R | R |
| Payroll / HR / 人事薪酬 | A | — | — | — | — |
| Biometric templates / 生物模板 | A | — | — | — | — |

> Least-privilege defaults: start everyone at R; promote only with a written reason. Never share the `admin/admin123` account (→ `data/21#ap-009-shared-admin-login`).
> 最小权限默认：所有人从 R 起；升权须书面理由。绝不用 `admin/admin123` 共用（→ `data/21#ap-009`）。

### #onboarding-checklist Onboarding Grant Checklist / 入职授权清单

| Step / 步 | Account / 账号 | Role / 角色 | Granted by / 授权人 | Date / 日期 |
|---|---|---|---|---|
| 1 | Email / 邮箱 | W | ____ | ____ |
| 2 | MMS / 会籍 | W | ____ | ____ |
| 3 | POS | W | ____ | ____ |
| 4 | Wi-Fi (staff VLAN) / 员工无线 | R | ____ | ____ |
| 5 | CCTV (view only) / 监控(仅看) | R | ____ | ____ |
| 6 | Cloud share / 云盘 | R | ____ | ____ |
| 7 | Social (if role) / 社媒(若岗) | per role | ____ | ____ |

> Grant ONLY what the role grid allows. Tick each; unsigned = not granted. Log in the JML one-pager.
> 只授角色矩阵允许的。逐项勾；未签=未授。记入职一页纸。

### #offboarding-killlist OFFBOARDING Kill-List (same-day, gate FIRST) / 离职击杀清单（当天，闸机置顶）

> 🔄 Rule: kill access the SAME DAY the person leaves. A disabled account with a live token can still act via API — deactivate AND revoke tokens.
> 🔄 规矩：离职**当天**撤销。带有效令牌的停用账号仍能经 API 行动——须停用并撤销令牌。

| Order / 序 | System / 系统 | Action / 动作 | Done / 完成 | Who / 人 |
|---|---|---|---|---|
| **1** | **Gate / 闸机门禁** | **revoke credential + token** | □ | ____ |
| 2 | Access card / 门禁卡 | deactivate | □ | ____ |
| 3 | MMS / CRM | disable + revoke API key | □ | ____ |
| 4 | POS | disable | □ | ____ |
| 5 | Email / 邮箱 | convert/disable + revoke sessions | □ | ____ |
| 6 | Wi-Fi admin / 无线后台 | remove VLAN | □ | ____ |
| 7 | CCTV / 监控 | revoke console | □ | ____ |
| 8 | Social / 社媒 | rotate creds | □ | ____ |
| 9 | Cloud / 云盘 | remove share | □ | ____ |
| 10 | Payroll / HR | disable | □ | ____ |
| 11 | Biometric / 生物模板 | delete where lawful / 依法删 | □ | ____ |
| 12 | Devices / 配发设备 | recover phone/tablet/key | □ | ____ |

> Gate access FIRST — a leaver with the gate code is the classic insider breach (→ `data/21#ap-024-offboarding-checklist`, `data/21#ap-037-spare-key-ex-staff`).
> 闸机置顶——仍握闸机码的前员工是典型内鬼（→ `data/21#ap-024`, `#ap-037`）。

### #quarterly-audit Quarterly Audit Procedure / 季度审计流程

1. Export the role grid; compare to actual staff list. / 导出矩阵，与实际员工比对。
2. Flag any over-permission (coach with A on MMS?) and any leaver still active. / 标过度授权与仍活的离职者。
3. Revoke findings; log date + owner. / 撤销并记日期+人。
4. Rotate admin/service credentials. / 轮换管理员/服务凭据。

### #shared-account-ban Shared-Account Prohibition / 禁止共用账号

> **Never** one shared login for all staff. It kills accountability and voids insurer claims (→ `data/21#ap-009-shared-admin-login`). Use per-user accounts + SSO where possible; a shared *vault* (password manager) is fine, a shared *login* is not.
> **绝不**全员共用一个登录。它消灭追责且让保险拒赔（→ `data/21#ap-009`）。用按人账号+可行 SSO；共享*保险库*（密码管理器）可以，共享*登录*不行。

### #pm-rollout Password-Manager Rollout Mini-Guide / 密码管理器落地小指南

- **Week 1 / 第1周**: Owner picks a manager (≥3 options, see `references/16#j-password-manager-mfa`), imports top 10 accounts, MFA on email+CRM+POS.
- **Week 2 / 第2周**: Enroll managers then front desk; shared vault for club accounts — never speak the master password.
- **Week 3 / 第3周**: MFA everywhere possible; print ONE emergency backup-code sheet, sealed in the safe.

---

## ④ Common Mistakes / 常见错误

- **Shared admin login** → no accountability, insurer denies. → `data/21#ap-009-shared-admin-login`.
- **Offboarding forgotten** → leaver opens back gate. → `data/21#ap-024-offboarding-checklist`.
- **Spare closet key with ex-staff** → inside job enabled. → `data/21#ap-037-spare-key-ex-staff`.
- **Over-permission "everyone trusted"** → leak or lockout. → `data/13` permission audit.

---

## ⑤ Related Files / 相关文件

- `references/16-security-operations-and-emergency.md` — `#j-offboarding-checklist`, `#j-password-manager-mfa`, `#j-data-breach-72h`.
- `data/21-anti-pattern-library.md` — AP-009, AP-024, AP-037, AP-008.
- `templates/38-emergency-contact-card.md` — breach escalation contacts. / 泄露升级联系。

---

## ⑥ G13 Note / G13 三视角说明

**Architect / 架构师**: The matrix is the access-control layer of FDMM; least-privilege + same-day offboarding enforce HI-3 (funds access) and HI-1 (special-data access) at the identity boundary.
**运营者 / Operator**: A fill-in grid + kill-list means a non-IT manager can grant and revoke access correctly the day someone joins or leaves — no security hire needed.
**会员 / Member**: Per-user accountability + biometric deletion on leave protect member PII and body data from insider misuse (HI-1, HI-8).
