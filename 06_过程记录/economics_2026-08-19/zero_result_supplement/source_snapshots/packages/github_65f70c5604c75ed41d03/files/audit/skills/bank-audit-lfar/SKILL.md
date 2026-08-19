---
name: bank-audit-lfar
description: >
  Assist with bank branch audit and Long Form Audit Report (LFAR). Covers NPA
  classification, income recognition, advances review, concurrent audit findings,
  stock audit, and LFAR questionnaire responses. Covers RBI guidelines on income
  recognition and asset classification (IRAC).
when_to_use: >
  When conducting a bank branch statutory audit or concurrent audit. Use to review
  advances portfolio, classify NPAs per RBI IRAC norms, and draft the LFAR.
effort: high
model: claude-opus-4-7
allowed-tools:
  - mcp__memory_bank__get_client
  - mcp__memory_bank__get_firm_profile
  - Read
  - Write
---

# Bank Audit — LFAR and NPA Review

**FINANCIAL INTEGRITY**: Bank audit requires strict adherence to RBI's IRAC (Income Recognition and Asset Classification) norms. Incorrect NPA classification has regulatory consequences. All findings must be supported by evidence from branch records, RBI circulars, and master circulars.

## RBI IRAC Norms — Quick Reference

### Asset Classification

| Category | Description | Provision |
|---|---|---|
| Standard | No overdue; or overdue ≤ 30 days | 0.25–0.40% (general) |
| Sub-Standard (SMA) | NPA for ≤ 12 months | 15% (secured), 25% (unsecured) |
| Doubtful (D1) | NPA 12–24 months | 25% (secured), 100% (unsecured) |
| Doubtful (D2) | NPA 24–36 months | 40% (secured), 100% (unsecured) |
| Doubtful (D3) | NPA > 36 months | 100% |
| Loss Asset | Loss identified, not written off | 100% |

### NPA Triggers (90-day overdue)
- Term Loan: Interest or instalment overdue for > 90 days
- Cash Credit/OD: Out of order for > 90 days (outstanding > sanctioned limit, or no credit for 90 days)
- Bills: Overdue for > 90 days

## LFAR — Part A: Branch Advances

### High-Value Advances Review

For all accounts with sanctioned limit > Rs.2 crore (or as specified by statutory central auditor):

```
ACCOUNT REVIEW:
Account: [Name] | A/c No.: [XXXX] | Limit: Rs.X Cr | Outstanding: Rs.X Cr
Product: CC/OD/TL | Security: Stock + Book Debts + Property
Last Review Date: [date] | Next Review Due: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NPA Status: Standard / Sub-standard / Doubtful / Loss
Overdue days: [N] days
Irregularity: [Describe if any]
Provision required: [Calculate per IRAC]
Provision held: [As per bank records]
Provision shortfall: Rs.X [Report in LFAR]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## LFAR Questionnaire — Key Sections

### I. Deposits
- Inoperative accounts being properly segregated?
- Deposits with unusual fluctuations?
- Premature withdrawal penalties correctly applied?

### II. Advances
- Adequate documentation maintained (sanction letter, hypothecation, mortgage)?
- Stock statements obtained and verified for CC/OD accounts?
- Drawing power being calculated correctly?
- Insurance of securities current?
- Legal recovery initiated for NPAs?

### III. Other Assets and Liabilities
- Branch adjustment account cleared regularly?
- Inter-branch reconciliation up to date?

### IV. Income and Expenditure
- Interest income recognised as per IRAC norms?
- Interest reversed for NPAs?
- Penal interest correctly applied?

### V. Housekeeping
- Cash over/short entries explained?
- System of physical verification of cash?
- Currency chest compliance?

## Stock Audit

For CC accounts with drawing power based on stock:

```
STOCK AUDIT REPORT — [Borrower] | A/c: [XXXX] | Date: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stock as per borrower's statement : Rs.X,XX,XXX
Stock physically verified          : Rs.X,XX,XXX
Discrepancy                        : Rs.XX,XXX (if any)

Book Debts (as per statement)      : Rs.X,XX,XXX
Less: Debts > 180 days            : (Rs.XX,XXX)
Eligible Book Debts                : Rs.X,XX,XXX

Actual Drawing Power:
  75% of eligible stock + 75% of eligible debtors = Rs.X,XX,XXX
  Branch Drawing Power granted     : Rs.X,XX,XXX
  
  Status: [✓ Adequate / ⚠ Excess drawing power allowed]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## LFAR Adverse Observations Format

For each adverse finding:
```
ADVERSE OBSERVATION:
Section: [IV.2.a]
Finding: Interest on NPA account [A/c XXXX] not reversed — Rs.XX,XXX overstated in income
RBI Circular: DBOD.No.BP.BC.xxx — IRAC norms
Impact: Income overstated by Rs.XX,XXX | Provision understated by Rs.XX,XXX
Management Response: [Record if any]
```
