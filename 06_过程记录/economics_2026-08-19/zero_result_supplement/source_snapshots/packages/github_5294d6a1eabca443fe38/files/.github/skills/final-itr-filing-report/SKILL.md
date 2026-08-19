---
name: final-itr-filing-report
description: 'Use when: producing the final Indian ITR filing report, ITR preparation sheet, filing-readiness report, final income statement, tax computation, schedule checklist, document reference, unresolved actions, or consolidated AY/FY tax filing summary from prepared tax artifacts.'
argument-hint: 'Provide the handoff path, assessment year, and final tax preparation artifacts'
user-invocable: true
---

# Final ITR Filing Report

## What This Skill Does
Use this skill to produce the final markdown ITR filing report after document analysis, discrepancy review, bank-statement audit, prior-year comparison when available, tax-rule analysis, and schedule preparation are substantially complete. This is the final output step in the ITR preparation workflow.

The report is a filing-preparation artifact. It consolidates verified document facts, reconciliation findings, final or provisional income figures, tax credits, tax computation, ITR schedule guidance, pre-filing actions, and document provenance. It does not file the return, guarantee correctness, or replace professional tax advice.

## Required Inputs
- Shared `handoff.md` path.
- Writable ITR work folder path and work subfolder paths from the handoff.
- Assessment year and financial year.
- Taxpayer profile and filing context.
- Document-analysis outputs: dashboard, structured entity mapping, discrepancy report, bank statement audit, and document provenance.
- Tax-preparation outputs: ITR form recommendation, tax-regime analysis, schedule-ready data, tax computation, bank coverage annotation, and open filing questions.
- Recorded user decisions for discrepancies, bank-audit items, missing documents, or assumptions.
- Prior-year comparison report when available.

If any required artifact is missing, read the handoff first to determine whether the workflow is intentionally provisional or blocked. Do not silently fill gaps.

## Report Principles
- Start from the handoff and existing artifacts; resume from recorded work instead of recreating analysis from scratch.
- Preserve attribution by artifact: document-derived facts come from document-analysis artifacts, tax-rule and schedule conclusions come from tax-preparation artifacts, and user choices come from recorded decision artifacts or the handoff.
- Use source-backed figures only. Mark unknown, estimated, provisional, or user-decided amounts visibly.
- Show filing blockers before routine checklist items.
- Separate taxable income, exempt income, deductions, tax credits, tax payable/refund, and pre-filing actions.
- Mask sensitive identifiers unless exact values are necessary and the user explicitly asked for them.
- Use Indian numbering and rupee amounts consistently, such as `₹1,26,452`. Use `—` only for genuinely unavailable values, not zero.
- Use status markers consistently:
  - `🟢 Verified match` for figures corroborated by all available expected sources.
  - `🔴 Discrepancy` for mismatches, missing material entries, filing blockers, or action-required items.
  - `🟡 Insufficient data` for single-source figures, pending certificates, estimates, or timing lags.
- If the environment or output channel cannot render symbols cleanly, use text labels `Verified match`, `Discrepancy`, and `Insufficient data` instead.

## Procedure
1. Read the shared handoff and identify the resume point, work folder, input document folder, work subfolders, final artifacts, blockers, and open decisions.
2. Verify that referenced final artifacts exist before relying on them. If an artifact is missing, mark the affected section as pending and explain the blocker.
3. Extract taxpayer profile facts, assessment year, financial year, regime, ITR form, residential status, filing deadline, bank account for refund, and contact/profile fields when available.
4. Build a legend for status markers and use the same markers throughout the report.
5. Consolidate cross-source reconciliation by income type and source: salary or pension, savings interest, FD or term-deposit interest, dividends, capital gains, business/profession, house property, exempt income, and tax credits as applicable.
6. For each reconciliation area, include tables comparing source documents, AIS/TIS, Form 26AS, bank credits, TDS/TCS, and current status. Include detailed sub-tables when one institution, employer, deductor, broker, or bank has many accounts or entries.
7. Add a reconciliation summary grouped into discrepancies requiring action, insufficient-data items, and verified matches.
8. Highlight critical omitted income, missing TDS, missing Form 16/Form 16A, missing bank statement periods, unexplained high-value bank credits, and filing blockers in their own subsection when present.
9. Prepare the final income statement under the selected tax regime. Group by ITR income category and source. Show gross amounts, statutory deductions, net taxable amounts, source, and status.
10. Prepare the TDS/TCS and tax-paid credit summary by deductor/collector/challan, including TAN when available, amount, source, and status.
11. Prepare the tax computation using rule-validated slab rates, surcharge, cess, rebate, deductions, credits, interest under sections such as 234A/234B/234C when available, self-assessment tax, and final payable/refund.
12. If material values are provisional, show separate scenarios only when they help the user decide what remains blocked. Label each scenario clearly and state which scenario is suitable for planning or filing.
13. Add refund or payment bank-account details when available and note pre-validation requirements.
14. Build an ITR filing checklist using actual form, regime, schedule names, and field labels from tax-preparation output. Include entries for general information, salary/pension, other sources, capital gains, exempt income, TDS/TCS, taxes paid, bank account, verification, and any schedules relevant to the case.
15. Build pre-filing action items with priority, action, why it matters, and whether the item blocks filing.
16. Add a document reference table listing each source artifact and what it confirms. Include missing required documents in the same table as `Missing` or `Not in folder`.
17. Add second-pass validation notes confirming that figures trace to source artifacts, discrepancies and user decisions are captured, tax-rule conclusions were used, and unresolved risks remain visible.

## Decision Points
- If ITR form, regime, or assessment year is missing, mark the final report blocked and request the missing fact through the coordinating workflow.
- If salary/pension/Form 16 data is incomplete, make income and tax computation provisional and put the missing employer/pension-bank document in filing blockers.
- If AIS/TIS/Form 26AS conflicts with source documents, preserve both values and use the discrepancy report or recorded user decision to state the filing treatment.
- If TDS appears expected but absent from Form 26AS, treat it as a discrepancy and do not count the credit unless a valid tax-credit source supports it.
- If income is visible in bank statements or source documents but absent from AIS/TIS/26AS, include it in income when tax-preparation output confirms it is taxable, and flag the omission.
- If a bank credit remains unexplained and material, keep it in pre-filing actions even if the tax computation can proceed.
- If final tax payable/refund depends on unresolved facts, show a provisional computation and state that the return should not be filed until the blocker is resolved.

## Output Format
Return a markdown report in this structure. Keep section numbers and headings; omit only subsections that are not applicable.

```markdown
# ITR Preparation Sheet — AY <assessment year> (FY <financial year>)
**Taxpayer:** <name> | **PAN:** <masked PAN or exact if allowed> | **Regime:** <tax regime> | **Form:** <ITR form>

## Report Provenance
| Field | Details |
|---|---|
| Prepared by | <report producer> |
| Skills used | final-itr-filing-report; <other skills used> |
| Source artifacts reviewed | <handoff, dashboard, discrepancy report, bank audit, tax-preparation output, prior-year comparison, user decisions> |
| Report path | <path> |
| Prepared / amended date | <date> |

*Prepared: <date>. All amounts in ₹ INR.*

---

## Legend

| Symbol | Meaning |
|---|---|
| 🟢 | **Verified match** — figures agree across all available expected sources |
| 🔴 | **Discrepancy** — mismatch, material omission, or action required before filing |
| 🟡 | **Insufficient data** — only partial evidence available; verify or obtain source document |

---

## 1. Taxpayer Profile

| Field | Details |
|---|---|
| Name | |
| PAN | |
| Aadhaar | |
| Date of Birth | |
| Age / Senior-citizen status | |
| Mobile | |
| Email | |
| Address | |
| Residential status | |
| ITR Form | |
| Tax Regime | |
| Filing deadline | |

> **Action needed:** <profile mismatch or missing profile confirmation, if any>

## 2. Cross-Source Reconciliation

### 2A. <Income or Credit Category>

| Institution / Payer | Account / TAN / Identifier | Source document amount | AIS/TIS amount | 26AS/TDS/TCS | Status |
|---|---|---:|---:|---:|---|
| | | | | | |

### 2B. <Detailed Institution / Category Breakdown>

Use detailed sub-tables for multi-account banks, employers, brokers, pension payers, or deductors.

### 2C. Reconciliation Summary

#### 🔴 Discrepancies — Action Required

| # | Issue | Detail | Action |
|---|---|---|---|
| | | | |

#### 🟡 Insufficient Data — Verify Before Filing

| # | Item | Available Source | Missing | Action |
|---|---|---|---|---|
| | | | | |

#### 🟢 Verified Matches

| # | Item | Verification |
|---|---|---|
| | | |

## 3. Final Income Statement (<Tax Regime>)

> **Status note:** <final/provisional/blocker note>

| Category | Institution / Source | Amount (₹) | Source | Status |
|---|---|---:|---|---|
| **Salary / Pension** | | | | |
| | Gross salary/pension | | | |
| | Less: Standard deduction u/s 16(ia) | | Statutory | |
| **Net Salary/Pension** | | | | |
| **Income from House Property** | | | | |
| **Capital Gains** | | | | |
| **Other Sources** | | | | |
| | Savings interest | | | |
| | FD / term-deposit interest | | | |
| | Dividend / other income | | | |
| **Gross Total Income** | | | | |
| **Deductions** | | | | |
| **Total Taxable Income** | | | | |
| **Exempt Income** | | | | |

## 4. TDS/TCS And Tax-Paid Credit Summary

| Deductor / Collector / Challan | TAN / BSR / CIN | Tax Credit (₹) | Source | Status |
|---|---|---:|---|---|
| | | | | |
| **Total Tax Credit Available** | | | | |

## 5. Tax Computation — <Tax Regime / Section>

**Note:** <regime-specific deductions, rebate, surcharge, cess, and limitation notes>

### Scenario A — <Final or Provisional Scenario Label>

| Line | Amount (₹) |
|---|---:|
| Gross Total Income | |
| Deductions allowed | |
| Total Taxable Income | |

| Slab / Component | Rate | Taxable Amount (₹) | Tax (₹) |
|---|---:|---:|---:|
| | | | |
| **Total Income Tax** | | | |
| Health & Education Cess | | | |
| Surcharge | | | |
| Interest u/s 234A/234B/234C | | | |
| **Total Tax Liability** | | | |
| Less: TDS/TCS/Advance/Self-Assessment Tax | | | |
| **NET TAX PAYABLE / REFUND** | | | |

> **Advance tax / self-assessment tax note:** <when applicable>

## 6. Refund Or Payment Bank Account

| Field | Details |
|---|---|
| Bank | |
| Account No. | |
| Account Type | |
| IFSC | |
| Name | |
| Pre-validation status | |

## 7. ITR Filing Checklist

- [ ] Confirm profile and contact details
- [ ] Select AY <assessment year> and <ITR form>
- [ ] Select <tax regime>
- [ ] Complete Part A — General Information
- [ ] Complete applicable income schedules
- [ ] Complete deductions and exempt income schedules
- [ ] Confirm TDS/TCS and taxes paid
- [ ] Pay self-assessment tax if payable
- [ ] Add or confirm validated bank account
- [ ] Submit and e-verify

## 8. Pre-Filing Action Items

| Priority | Action | Why | Filing impact |
|---|---|---|---|
| | | | |

## 9. Documents Reference

| Document / Artifact | What It Confirms | Status |
|---|---|---|
| | | |

## 10. Second-Pass Validation

- <Traceability check>
- <Discrepancy/user-decision check>
- <Advisor rule check>
- <Open risk check>
```

## Completion Checks
- The report starts with taxpayer, AY/FY, regime, ITR form, preparation date, and currency basis.
- The report includes provenance with prepared-by, skills-used, source artifacts reviewed, report path, and prepared or amended date when available.
- The legend exists and the same status labels are used consistently throughout the report.
- Taxpayer profile includes enough detail for filing review, with mismatches or missing profile fields called out.
- Cross-source reconciliation covers each material income source, tax credit source, and exempt-income source that appears in the final artifacts.
- Discrepancies, insufficient-data items, and verified matches are separated and action-oriented.
- Final income statement separates gross income, statutory deductions, net taxable income, exempt income, and source/status for each material line.
- Tax computation uses rule-validated rates and clearly labels final versus provisional scenarios.
- TDS/TCS/tax-paid credits are counted only when supported by Form 26AS, TDS certificates, challans, or tax-preparation evidence.
- Filing checklist uses the actual ITR form, regime, and applicable schedules for the taxpayer.
- Pre-filing action items identify file blockers separately from optional verification.
- Document reference table lists every material source artifact and missing required documents.
- Second-pass validation states whether unresolved risks remain and whether filing should proceed or wait.