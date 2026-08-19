---
name: review
description: >
  Audit & Assurance dispatcher. Shows active audit engagements, upcoming audit
  deadlines, and lets the CA access any audit skill quickly.
when_to_use: >
  At the start of an audit session, to see active engagements, or to navigate
  to any audit skill.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__list_clients
  - mcp__memory_bank__get_due_dates
  - mcp__memory_bank__get_firm_profile
---

# Audit & Assurance — Dashboard

!`python3 ${CLAUDE_PLUGIN_ROOT}/../../shared/bin/get-firm-context.py 2>/dev/null`

## Audit Calendar

```
AUDIT DEADLINES (approximate)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sep 30  — Tax Audit Report (3CA/3CB + 3CD)
Oct 31  — Statutory Audit Report (for ITR filing)
Nov 30  — Consolidated financials for large companies
Dec 31  — AGM deadline (companies with Sep 30 balance sheet)
Sep 30  — AGM deadline for companies with Mar 31 balance sheet
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bank Audit: Appointment by Apr 30 | Report by Jun 30
Internal Audit: As per engagement scope
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Available Audit Skills

```
/audit:caro-review        → CARO 2020 clause-by-clause (21 clauses)
/audit:risk-matrix        → SA-315 audit risk matrix + materiality
/audit:bank-audit-lfar    → Bank branch audit + LFAR + NPA classification
/audit:internal-audit     → Internal audit plan + findings report
/audit:workpaper-draft    → Working papers + management representation letter
```
