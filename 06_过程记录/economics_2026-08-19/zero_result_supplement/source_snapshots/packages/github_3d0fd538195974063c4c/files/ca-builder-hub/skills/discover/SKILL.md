---
name: discover
description: >
  Discover and recommend which claude-for-ca plugins and skills are relevant
  for a given query or task. Acts as the CA's entry point — routes to the right
  plugin when they don't know which skill to use.
when_to_use: >
  When a CA doesn't know which plugin or skill handles their task. Also shown
  on first launch as a navigation guide for the full plugin suite.
effort: low
model: claude-haiku-4-5
allowed-tools:
  - mcp__memory_bank__get_firm_profile
  - mcp__memory_bank__list_clients
---

# ca-builder-hub — Plugin Discovery

## Plugin Suite Overview

```
CLAUDE-FOR-CA — Plugin Suite Navigator
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE
  /cold-start:onboard-firm        → First-time firm setup
  /cold-start:add-client          → Register a new client

DOCUMENT PROCESSING
  /document-intake:email-invoice-fetch    → Fetch invoices from email
  /document-intake:pdf-data-extractor     → Extract data from PDF
  /document-intake:bank-statement-processor → Process bank statements
  /document-intake:tally-import-builder   → Build Tally import file

GST COMPLIANCE
  /gst-compliance:gstr1-review    → Review GSTR-1 before filing
  /gst-compliance:gstr3b-review   → Review GSTR-3B
  /gst-compliance:itc-recon       → ITC reconciliation (2A vs 2B vs books)
  /gst-compliance:notice-triage   → GST notice analysis
  /gst-compliance:annual-return   → GSTR-9 / GSTR-9C
  /gst-compliance:gst-audit       → GST audit (Section 65/66)

INCOME TAX
  /income-tax:itr-review          → ITR review before filing
  /income-tax:notice-analysis     → IT notice analysis
  /income-tax:advance-tax         → Advance tax computation
  /income-tax:capital-gains       → Capital gains computation
  /income-tax:tax-audit-3cd       → Form 3CD tax audit

TDS / TCS
  /tds-compliance:default-check   → TDS default check
  /tds-compliance:26as-recon      → 26AS vs books reconciliation
  /tds-compliance:form-16-generator → Form 16 / 16A drafting
  /tds-compliance:quarterly-return  → 24Q/26Q return review

AUDIT & ASSURANCE
  /audit:caro-review              → CARO 2020 all 21 clauses
  /audit:risk-matrix              → SA-315 risk assessment
  /audit:bank-audit-lfar          → Bank audit / LFAR
  /audit:workpaper-draft          → Lead schedules + completion checklist
  /audit:internal-audit           → Risk-based internal audit

MCA / SECRETARIAL
  /mca-secretarial:filing-tracker → ROC due dates + late fee
  /mca-secretarial:resolution     → Board resolution drafting
  /mca-secretarial:annual-compliance → AGM / Directors' Report
  /mca-secretarial:charge-registry → Charge creation/satisfaction

TRANSFER PRICING
  /transfer-pricing:form-3ceb     → Form 3CEB + ALP analysis
  /transfer-pricing:tp-documentation → TP documentation (Rule 10D)

FEMA
  /fema-compliance:fdi-compliance → FC-GPR, FC-TRS, FLA return
  /fema-compliance:odi-compliance → ODI / APR annual return

PAYROLL
  /payroll-compliance:pf-recon    → PF ECR generation
  /payroll-compliance:esic-recon  → ESIC half-yearly return
  /payroll-compliance:professional-tax → State-wise PT calculator

ADVISORY
  /advisory-ca:tax-planning       → Old vs new regime comparison
  /advisory-ca:msme-advisory      → Udyam, 43B(h), MSME-1

CLIENT MANAGEMENT
  /client-onboarding:kyc-checklist → KYC documents checklist
  /client-onboarding:engagement-letter → SA-210 engagement letter

CA STUDENT
  /ca-student:articleship-log     → Daily diary, area-wise hours
  /ca-student:exam-prep           → CA exam revision help

FIRM MANAGEMENT
  /firm-management:fee-tracker    → Outstanding fees, collection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Quick Route by Task

Tell me what you need and I'll tell you the exact skill to use:

- "File GST return" → `/gst-compliance:gstr3b-review`
- "Check TDS default" → `/tds-compliance:default-check`
- "Draft board resolution" → `/mca-secretarial:resolution`
- "Analyse IT notice" → `/income-tax:notice-analysis`
- "New client onboarding" → `/client-onboarding:review`
- "Log articleship hours" → `/ca-student:articleship-log`
