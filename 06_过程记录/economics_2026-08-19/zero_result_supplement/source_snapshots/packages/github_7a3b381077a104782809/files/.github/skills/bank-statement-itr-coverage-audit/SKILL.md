---
name: bank-statement-itr-coverage-audit
description: 'Use when: auditing bank statements after tax-document-entity-mapping, tabulating bank transactions, linking transactions to income entities and ITR coverage, identifying pension/salary/interest/dividend/refund/capital-gains credits, annotating where transactions are covered in ITR schedules, and flagging high-value unexplained transactions.'
argument-hint: 'Provide bank statements, entity mapping, discrepancy report, and final ITR schedule-ready data when available'
user-invocable: true
---

# Bank Statement ITR Coverage Audit

## What This Skill Does
Use this skill to audit provided bank statements after `tax-document-entity-mapping` is complete. The output is a markdown table of bank transactions with an additional ITR coverage view: whether each transaction is covered in the ITR preparation data, where it is covered, and what remains unexplained.

This skill has two phases:

1. **Initial bank audit**: use bank statements and entity mapping to identify transactions, likely income/tax relevance, source evidence, and candidate ITR coverage areas.
2. **Final ITR coverage annotation**: after ITR form and schedule-ready data are prepared, annotate which transactions are actually covered in the ITR and where, and flag high-value unexplained transactions.

## Inputs
Use these inputs when available:

- Bank statements or extracted bank transaction tables.
- Structured entities from `tax-document-entity-mapping`.
- Dashboard report from `tax-entity-dashboard-report`.
- Discrepancy report from `tax-document-discrepancy-report`.
- Recorded user decisions from the handoff, discrepancy report, or bank-audit decision log.
- Human-fillable schedule data from tax-preparation artifacts.
- Assessment year, financial year, and known income sources.

If bank statements are missing and this audit is material, request them through the coordinating workflow.

## Transaction Classification Guidance
Classify bank transactions cautiously using narration, counterparty, amount, date, entity mapping, and supporting documents. Use empty or `Needs review` status when evidence is insufficient.

Common categories:

- Salary or pension credit.
- Interest credit.
- Dividend credit.
- Capital gains, broker payout, redemption, or sale proceeds.
- Rent received.
- Business or professional receipt.
- Tax refund or tax refund interest.
- TDS/TCS, advance tax, self-assessment tax, or challan payment.
- Transfer between own accounts.
- Investment contribution or redemption.
- Loan, reimbursement, gift, or non-taxable receipt needing review.
- Cash deposit or cash withdrawal.
- Other or unexplained.

## Procedure
1. Confirm entity mapping is available. If not, first request or produce `tax-document-entity-mapping` output.
2. Identify bank statement files, account identifiers, bank names, statement periods, and whether statements cover the full financial year.
3. Extract bank transactions with date, amount, debit/credit direction, narration, balance if available, and source statement reference.
4. Match transactions to structured entities using amount, date, narration, payer/reporting entity, source document, AIS/TIS, and bank-credit info.
5. For each transaction, record likely income type or non-income classification, match confidence, source evidence, and candidate ITR coverage area.
6. Mark transactions as `Covered candidate`, `Likely non-taxable/transfer`, `Needs user decision`, `Needs ITR coverage annotation`, `Unmatched`, or `Unexplained`.
7. After ITR schedule-ready data is available, annotate each relevant transaction with actual ITR coverage: ITR form, schedule/part, field/table/row label, value included, and status.
8. Flag high-value unexplained transactions. If the user has not supplied a threshold, use `Needs review` and state that the threshold was not provided rather than inventing a fixed rule.
9. Preserve transaction provenance: bank, account identifier, transaction date, narration, amount, and source statement reference.
10. Perform a second pass to ensure every coverage claim is supported by entity mapping, discrepancy report, user decision, or schedule-ready data.

## Output Format
Return a markdown report with these sections:

- **Report Provenance**: prepared by, skills used, source artifacts reviewed, report path, and prepared or amended date when available.
- **Audit Summary**: bank accounts reviewed, statement periods, total credits/debits reviewed, matched items, uncovered items, and high-value unexplained items.
- **Bank Transaction Coverage Table**: transaction-level table using the shape below.
- **Likely Covered Transactions**: items with strong mapping or confirmed ITR coverage.
- **Needs User Decision**: transactions requiring the supervisor to ask the user for context.
- **Needs ITR Coverage Annotation**: transactions waiting for final ITR schedule mapping.
- **High-Value Unexplained Transactions**: material credits/debits not explained by the ITR data or user decisions.
- **Second-Pass Validation**: checks performed, assumptions, and unresolved uncertainty.

Use this table shape:

| ID | Bank / account | Date | Credit / debit | Amount | Narration | Likely category | Entity / document match | ITR coverage status | ITR form / schedule / field | Covered value | Evidence | Follow-up |
|---|---|---|---|---:|---|---|---|---|---|---:|---|---|

Use these `ITR coverage status` values consistently:

- `Covered in ITR`
- `Partially covered in ITR`
- `Not covered in ITR`
- `Likely non-taxable/transfer`
- `Needs user decision`
- `Needs ITR coverage annotation`
- `Unexplained`

## Completion Checks
- The audit includes provenance with prepared-by, skills-used, source artifacts reviewed, report path, and prepared or amended date when available.
- Entity mapping was used as the primary evidence layer.
- Bank transactions are tied back to source statement references.
- ITR coverage is not marked `Covered in ITR` unless schedule-ready data or a reliable ITR mapping supports it.
- Pension payments are mapped to the relevant salary/pension schedule coverage when supported.
- High-value unexplained transactions are visible and not buried in generic notes.
- User decisions and discrepancy IDs are referenced when they explain coverage.