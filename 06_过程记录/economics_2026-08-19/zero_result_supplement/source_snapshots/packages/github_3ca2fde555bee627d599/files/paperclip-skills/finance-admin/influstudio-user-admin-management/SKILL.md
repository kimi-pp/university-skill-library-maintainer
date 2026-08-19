---
name: influstudio-user-admin-management
description: >
  Manages InfluStudio platform admin accounts: creating, modifying, and revoking
  admin access; monitoring the governance hub; reviewing system activity logs;
  and managing subscription plans via the pricing engine. Use when onboarding
  new admin users, auditing platform activity, or managing the admin roster.
version: 1.0.0
authors:
  - InfluStudio Inc.
tags:
  - admin
  - governance
  - access-control
  - influstudio
  - platform-management
---

# InfluStudio Admin Account Management Skill

## Overview
This skill enables AI agents to manage the InfluStudio platform's administrative accounts and governance systems through the Admin Panel at:
`https://influstudio-staging--influstudio-staging.us-east4.hosted.app/admin/`

## Platform Admin Modules Available
1. **Analytics Hub** (`/admin/dashboard`) — Platform-wide metrics
2. **User Registry** (`/admin/users`) — Manage creator/brand accounts
3. **Platform Reports** (`/admin/reports`) — Aggregated reporting
4. **Pricing Engine** (`/admin/pricing`) — Subscription plan management
5. **Governance Hub** — Admin roster and permissions
6. **System Activity Ledger** — Audit trail of all admin actions

## Admin Account Operations

### Inviting a New Administrator
**When:** HR requests a new admin account after hiring
**Process:**
1. Navigate to Governance Hub → Admin Roster
2. Click "Invite Administrator"
3. Enter: Name, Email
4. Select permission scopes (assign minimum required access):
   - ☐ Analytics Hub Access — view-only platform metrics
   - ☐ User Registry Access — manage platform users
   - ☐ Governance Control — manage other admins
   - ☐ Financial Audit Access — view financial data
5. Send invitation
6. Log action in internal record:

```
Admin Created: [Date]
Name: [Name]
Email: [Email]
Role: [Super Admin / Manager / Analyst]
Permissions: [List]
Created By: [Agent/Admin name]
Approved By: [Human approver]
```

### Admin Roles & When to Assign
| Role | Use Case | Permissions |
|------|----------|-------------|
| **Super Admin** | Full platform control — CEO/CTO only | All permissions |
| **Manager** | Day-to-day operations team | Analytics + User Registry + Financial |
| **Analyst** | Read-only analytics review | Analytics Hub only |

### Revoking/Modifying Admin Access
**Trigger:** Employee departure, role change, security incident
**Process:**
1. Navigate to Governance Hub → Admin Roster
2. Find the admin by name/email
3. Click Actions → Revoke Access (for departures) or Edit Permissions
4. Confirm action — system logs automatically
5. Notify IT Manager via task
6. Document in offboarding record

### Reviewing System Activity Ledger
**Cadence:** Weekly review
**What to look for:**
- Unusual access times (outside business hours)
- Multiple failed login attempts
- Mass data exports
- User blocks/snoozes not in the task queue
- Any action by unauthorized admin accounts

**Report format:**
```
## Weekly Admin Activity Review — [Week of DATE]

### Summary
- Total admin actions: X
- Unique admins active: X
- Flags requiring review: X

### Flagged Activities
| Action | Admin | Target | Timestamp | Flag Reason |
|--------|-------|--------|-----------|-------------|
| [Action] | [Name] | [Target] | [Time] | [Reason] |

### Recommendation
[Agent's assessment and recommended action]
```

## User Registry Management

### When to Snooze a User
- Reported policy violations
- Suspicious payment activity
- Temporary account restriction requested by legal/compliance
- User reported for content violations

**Process:**
1. Navigate to User Registry
2. Search user by name or email
3. Click Actions → Snooze User
4. Document reason in internal log
5. Set review date (default: 7 days)
6. Notify relevant team (Creator Relations or Brands Relations)

### When to Block a User
- Confirmed fraud
- Repeated guideline violations after snooze
- Legal requirement
- Chargebacks/payment fraud confirmed

**⚠️ BLOCK REQUIRES HUMAN APPROVAL before execution**

Template for requesting approval:
```
Block Request — Requires Authorization

User: [Name] ([Email])
Account Type: [Creator/Brand-Agency]
Reason: [Specific policy violation / fraud evidence]
Evidence: [Link to evidence/report]
Recommended By: [Agent/Team]
Requires Approval From: Head of Finance + CEO

Action to Take: Block user account
Effect: User loses platform access, cannot log in
Historical Data: Preserved for audit
```

## Pricing Engine Management

### Subscription Plans in System
| Plan | Price | Target Users |
|------|-------|-------------|
| NONE | Free | Waitlist/incomplete registration |
| STARTER | $X/mo | Solo creators, small brands |
| PROPLUS | $X/mo | Professional creators, agencies |

### Plan Status Types
- **TRIALING** — In free trial period
- **PAYMENT_PENDING** — Trial ended, payment not collected
- **ACTIVE** — Paid and active
- **CANCELLED** — Churned

### When to Escalate Plan Issues
- User stuck in PAYMENT_PENDING > 7 days → notify Accountant for follow-up
- User requesting plan upgrade/downgrade → process in Pricing Engine
- Refund requests → escalate to Head of Finance for approval

## Escalation Matrix
| Situation | Escalate To |
|-----------|-------------|
| New Super Admin needed | CEO approval required |
| Security incident in logs | CTO + Head of Finance immediately |
| User block request | Head of Finance + CEO |
| Payment dispute | Accountant + Head of Finance |
| Admin access abuse | CEO + CTO immediately |
