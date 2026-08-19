---
name: influstudio-admin-access-governance
description: >
  Manages the complete admin access lifecycle in InfluStudio's Governance Hub:
  inviting new admins, assigning correct permission scopes, modifying roles,
  revoking access on departure, and maintaining the approved admin roster.
  Includes role definitions, permission templates, and escalation rules.
version: 1.0.0
authors:
  - InfluStudio IT Manager Agent
tags:
  - governance
  - access-control
  - admin-management
  - influstudio
  - security
---

# InfluStudio Admin Access Governance Skill

## Overview
This skill guides the IT Manager through every admin access lifecycle event
in the InfluStudio Governance Hub. It covers invitation workflows, permission
scope selection, modification protocols, and departure revocation — with
specific reference to the actual permission model discovered in the platform.

---

## Platform Context

### Governance Hub Location
Accessible within the Admin Panel at:
```
https://influstudio-staging--influstudio-staging.us-east4.hosted.app/admin/
→ Governance Hub section
```

### Available Admin Roles (Platform-Native)
| Role | Level | Who Gets This |
|------|-------|--------------|
| **Super Admin** | Highest | CEO, CTO only — full control |
| **Manager** | Mid | Operations leads — day-to-day admin work |
| **Analyst** | View-only | Reporting/data roles — read access only |

### Available Permission Scopes (Platform-Native)
These are the exact permission checkboxes found in the Governance Hub:

| Permission | What It Allows | Default |
|-----------|---------------|---------|
| **Analytics Hub Access** | View platform metrics, user demographics, performance data | OFF |
| **User Registry Access** | View and manage platform users (snooze, block, reactivate) | OFF |
| **Governance Control** | Manage other admin accounts, invite/revoke admins | OFF |
| **Financial Audit Access** | View financial data, subscription records, earnings | OFF |

---

## Admin Access Permission Templates

Use these templates when creating admin accounts. Always assign **minimum required permissions** — never grant more access than the role needs.

### Template 1: IT Manager Agent (this agent)
```
Role: Manager
Permissions:
  ✅ Analytics Hub Access
  ✅ User Registry Access
  ✅ Governance Control
  ❌ Financial Audit Access  ← Accountant / Head of Finance only
```

### Template 2: Head of Finance & Admin Agent
```
Role: Super Admin
Permissions:
  ✅ Analytics Hub Access
  ✅ User Registry Access
  ✅ Governance Control
  ✅ Financial Audit Access
```

### Template 3: Accountant Agent
```
Role: Manager
Permissions:
  ✅ Analytics Hub Access
  ❌ User Registry Access   ← Not needed for bookkeeping role
  ❌ Governance Control
  ✅ Financial Audit Access
```

### Template 4: Marketing/Analytics Human Staff
```
Role: Analyst
Permissions:
  ✅ Analytics Hub Access
  ❌ User Registry Access
  ❌ Governance Control
  ❌ Financial Audit Access
```

### Template 5: Creator Relations / Brand Relations Human Staff
```
Role: Analyst
Permissions:
  ✅ Analytics Hub Access
  ✅ User Registry Access   ← Needs to view user profiles
  ❌ Governance Control
  ❌ Financial Audit Access
```

### Template 6: CEO (human)
```
Role: Super Admin
Permissions:
  ✅ Analytics Hub Access
  ✅ User Registry Access
  ✅ Governance Control
  ✅ Financial Audit Access
```

---

## Workflow 1: Inviting a New Admin

### Trigger
- HR Specialist creates a task: "New hire [Name] requires admin access — Role: [ROLE]"
- Or: CEO/Head of Finance requests new admin access

### Pre-Invitation Checklist
Before creating the account:
- [ ] Verify the request came from an authorized approver (Head of Finance or CEO)
- [ ] Confirm the role justification (why does this person need admin access?)
- [ ] Identify the correct permission template from above
- [ ] Confirm the email address matches the company directory

### Invitation Steps
1. Navigate to Governance Hub → Admin Roster
2. Click **"Invite Administrator"**
3. Enter: Full name, Work email address
4. Select **Role** (Super Admin / Manager / Analyst)
5. Select **Permission scopes** using the correct template above
6. Send invitation

### Post-Invitation Documentation
Log this in the internal admin roster record:

```
ADMIN ACCOUNT CREATED
=====================
Date: [DATE]
Name: [FULL NAME]
Email: [EMAIL]
Role Assigned: [Super Admin / Manager / Analyst]
Permissions Granted:
  - Analytics Hub: [YES/NO]
  - User Registry: [YES/NO]
  - Governance Control: [YES/NO]
  - Financial Audit: [YES/NO]

Requested By: [Name + Role]
Approved By: [Name + Role]
Created By: IT Manager Agent
Invitation Sent: ✅
Access Confirmed Active: [DATE when confirmed]
```

---

## Workflow 2: Modifying Admin Permissions

### Trigger
- Role change after promotion/demotion
- Security incident requiring immediate permission reduction
- New responsibility added to existing admin

### Modification Rules
- **Expanding permissions** → requires Head of Finance approval
- **Reducing permissions** → IT Manager can execute immediately (security action)
- **Role change (upgrade)** → requires CEO approval
- **Role change (downgrade)** → requires Head of Finance approval

### Steps
1. Navigate to Governance Hub → Admin Roster
2. Find the admin by name/email
3. Click Actions → Modify Permissions
4. Update permission scopes per the approved change
5. Confirm and save
6. Log the change:

```
ADMIN PERMISSIONS MODIFIED
===========================
Date: [DATE]
Admin: [NAME] ([EMAIL])
Change Made:
  Before: [Previous permissions]
  After: [New permissions]
Reason: [Why the change was made]
Requested By: [Name]
Approved By: [Name]
Executed By: IT Manager Agent
```

---

## Workflow 3: Revoking Admin Access (Departure)

### Trigger
- HR Specialist creates offboarding task for an admin-level employee
- Security incident requiring immediate access revocation
- Admin account showing suspicious activity

### Departure Revocation (Standard — Employee Leaving)
**Timeline:** Must be completed before or on the last day.

1. Navigate to Governance Hub → Admin Roster
2. Find the departing admin
3. Click Actions → **Revoke Access**
4. Confirm the action
5. Verify the account no longer appears in Active admin list
6. Log:

```
ADMIN ACCESS REVOKED
====================
Date: [DATE]
Admin: [NAME] ([EMAIL])
Reason: Employment ended / Role change / Security
Last Active: [DATE]
Access Revoked: ✅ [TIMESTAMP]
Verified By: IT Manager Agent
Notified: HR Specialist ✅ | Head of Finance ✅
```

### Emergency Revocation (Security Incident)
**Timeline:** Within 15 minutes of incident detection.

1. Immediately revoke access (no approval needed for security emergencies)
2. Simultaneously notify: CTO + Head of Finance via urgent task
3. Document with full incident details
4. Lock down: also check if any API keys or external access was issued

```
EMERGENCY ACCESS REVOCATION
============================
🚨 SECURITY INCIDENT
Time: [TIMESTAMP]
Admin Revoked: [NAME] ([EMAIL])
Reason: [Specific security reason]
Evidence: [What triggered this]
Revocation Time: [EXACT TIMESTAMP]
Executed By: IT Manager Agent (emergency protocol)
Notified: CTO + Head of Finance at [TIME]
Follow-up Required: Full security audit of this admin's activity
```

---

## Workflow 4: Quarterly Access Review

**Cadence:** Every 90 days
**Purpose:** Ensure all active admin accounts are still needed and correctly scoped.

### Review Steps
1. Pull the full Admin Roster from Governance Hub
2. For each admin on the roster:
   - Is this person still employed/active?
   - Is their role still the same?
   - Do their permissions still match their responsibilities?
   - Have they actually logged in and used the admin panel in the past 90 days?

### Inactive Admin Detection
If an admin account has not been active for 60+ days:
- Flag for review
- Confirm with HR Specialist they are still active
- If no confirmation within 5 business days → recommend revocation

### Quarterly Access Review Report

```markdown
## Quarterly Admin Access Review
**Quarter:** [Q1/Q2/Q3/Q4] [YEAR]
**Reviewed By:** IT Manager Agent
**Date:** [DATE]

### Current Admin Roster Status

| Name | Email | Role | Last Active | Permissions | Status | Action |
|------|-------|------|-------------|-------------|--------|--------|
| [Name] | [Email] | [Role] | [Date] | [List] | Active ✅ | None |
| [Name] | [Email] | [Role] | [Date] | [List] | Inactive ⚠️ | Review |

### Changes Made This Quarter
| Change | Admin Affected | Date | Reason |
|--------|---------------|------|--------|
| Access Revoked | [Name] | [Date] | [Reason] |
| Permissions Modified | [Name] | [Date] | [Reason] |
| New Admin Added | [Name] | [Date] | [Reason] |

### Recommendations
1. [Specific recommendation]

### Sign-off Required
→ Head of Finance & Admin: [Pending / Approved]
```

---

## Escalation Matrix for Governance Decisions

| Action | Can IT Manager Do It Alone? | Approval Needed From |
|--------|---------------------------|---------------------|
| Invite Analyst-level admin | No | Head of Finance |
| Invite Manager-level admin | No | Head of Finance + CEO |
| Invite Super Admin | No | CEO only |
| Reduce permissions | Yes (security) | Log within 1h |
| Expand permissions | No | Head of Finance |
| Revoke access (standard) | No | Head of Finance |
| Emergency revocation | Yes (immediate) | Notify CTO + Head of Finance within 15min |
| Quarterly review | Yes (review only) | Head of Finance sign-off on report |
