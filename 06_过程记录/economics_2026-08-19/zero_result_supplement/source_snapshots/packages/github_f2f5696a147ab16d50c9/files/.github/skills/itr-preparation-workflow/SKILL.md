---
name: itr-preparation-workflow
description: 'Use when: coordinating end-to-end Indian ITR preparation across document-analysis, tax-preparation, and user-decision workstreams; collecting applicable tax documents including last year filed ITR; routing bank statement audit and discrepancy reporting; comparing prior-year ITR with current-year data; capturing user decisions; preparing ITR form/schedule data; and producing final ITR filing reports or filing-readiness outcomes.'
argument-hint: 'Provide the assessment year, filing goal, available documents, and known income sources'
user-invocable: true
---

# ITR Preparation Workflow

## What This Skill Does
Use this skill to coordinate the end-to-end ITR preparation workflow across document-analysis, tax-preparation, and user-decision workstreams. The workflow starts by collecting applicable documents, including last year's filed ITR for comparison when available. Document-analysis work produces the document dashboard and structured income evidence. After entity mapping is complete, bank statement audit and discrepancy reporting are prepared from the entity mapping and related documents. User decisions for judgement items are collected through the coordinating workflow and recorded in the relevant reports. The workflow also produces a prior-year comparison report when last year's ITR is available. Finally, tax-preparation work consumes the dashboard, structured entities, bank statement audit, discrepancy report, prior-year comparison report, and user decisions to recommend the ITR form, prepare schedule-ready data, annotate bank transaction ITR coverage, and identify remaining filing questions.

This skill is for coordination and filing preparation. It does not file the return, guarantee correctness, or replace professional tax advice.

## Workstream Routing
- Use document-analysis work for structured entity mapping, dashboard reports, bank-credit/AIS/TIS reconciliation, source-document provenance, and review of document-derived facts.
- Use tax-preparation work for current Indian tax-rule research, ITR form selection, tax treatment, schedule-ready ITR data, and rule-based filing-readiness checks.
- Use `bank-statement-itr-coverage-audit` after entity mapping is complete. First prepare the initial bank transaction audit, then annotate actual ITR coverage after return preparation.
- Use `prior-year-itr-comparison` to compare last year's filed ITR with current-year dashboard/entities/tax-preparation output and highlight changes.
- Use `final-itr-filing-report` as the final workflow step to produce the user-facing ITR preparation sheet, tax computation, filing checklist, action items, and document reference.
- Use the coordinating workflow to collect user decisions for discrepancies, route follow-up questions between workstreams and the user, track progress, and combine outputs.
- Use this workflow to decide sequencing, collect missing inputs, track progress, record user decisions, and combine outputs.

## Required Intake
Collect or confirm these before final recommendations:

- Writable ITR work folder where workstreams can create subfolders, generated outputs, intermediate files, and handoff documents.
- Read-only input documents folder containing source tax documents. No generated output should be written to this folder.
- Last year's filed ITR, acknowledgement, return JSON/PDF, or computation, if available. Ask for it if not already present in the input documents folder.
- Assessment year and financial year.
- Filing goal: document dashboard, ITR form selection, schedule-ready data, review, or full preparation workflow.
- Taxpayer residential status.
- Known income sources: salary, interest, dividend, capital gains, house property, business/profession, foreign assets/income, exempt income, agricultural income, or other sources.
- Tax regime preference or uncertainty, if relevant.
- Whether the user wants to work from raw documents, redacted documents, extracted text, or prior summaries.

If a missing fact blocks the next specialist step, ask only the minimum questions needed to continue.

## Handoff And Resume Protocol
- At the start of every new or resumed ITR preparation session, read the shared handoff document before doing specialist work or delegating specialist work.
- If the user provides a handoff path, use that path. Otherwise, use `handoff.md` inside the writable ITR work folder once that folder is known.
- The handoff must record the writable ITR work folder path, read-only input documents folder path, shared handoff document path, each workstream's assigned work subfolder path, current workflow status, completed artifacts, blockers, open decisions, and the exact resume point.
- Treat the writable ITR work folder path in the handoff as the workspace where workstreams keep their work-in-progress. Generated reports, extracted text, decrypted working copies, calculations, and intermediate files should stay inside the relevant workstream subfolder there.
- If a handoff exists, resume from its recorded status instead of restarting analysis from scratch. Verify referenced artifacts exist before relying on them, and only redo work when the handoff says it is incomplete, stale, contradicted, or missing required evidence.
- If the handoff is missing, unreadable, or lacks required paths, pause the affected work and ask for the writable ITR work folder or corrected handoff path before creating outputs.

## Applicable Document Checklist
Ask the user to provide documents only if applicable to their facts. Not every document is mandatory.

### Core Tax Statements
- Form 16 from all employers.
- Form 16A for non-salary TDS, if any.
- Form 26AS.
- AIS and TIS statements.
- Challans for advance tax or self-assessment tax, if paid.
- Last year's filed ITR, acknowledgement, return JSON/PDF, or computation for prior-year comparison.
- Prior-year carry-forward details, if relevant.

### Salary And Employment
- Salary slips, especially for multiple employers, reimbursements, perquisites, arrears, bonus, gratuity, leave encashment, or deductions that are unclear in Form 16.
- Full-and-final settlement statements, if employment changed.
- EPF passbook or employer PF statement, if relevant.

### Bank, Interest, And Other Sources
- Bank statements for accounts where income was credited.
- Interest certificates from banks, post office, NBFCs, bonds, or other payers.
- Fixed deposit, recurring deposit, savings interest, tax refund interest, and bond/NCD holding or cashflow statements where applicable.
- Dividend statements or broker reports for dividend income.

### Investments And Capital Gains
- Demat statements, broker capital-gains reports, contract notes, and mutual fund capital-gains statements.
- Consolidated Account Statement, if available.
- Foreign equity, RSU, ESOP, ESPP, foreign brokerage, or foreign asset statements, if applicable.
- Crypto or virtual digital asset statements, if applicable.

### Retirement, Deductions, And Exemptions
- PPF statements or contribution proofs.
- EPF and NPS statements or contribution proofs.
- ELSS, life insurance, tuition fee, principal repayment, or other section 80C proofs.
- Health insurance, medical expenditure, education loan interest, donation receipts, rent receipts, home-loan interest certificate, and other deduction proofs where applicable.

### Property, Business, And Other Special Cases
- Rent agreements, rent receipts, municipal tax receipts, and home-loan certificates for house property.
- Sale/purchase deeds, stamp-duty values, improvement cost evidence, and exemption investment proofs for property capital gains.
- Books, P&L, balance sheet, invoices, Form 3CB/3CD, or presumptive-income details for business/profession, if applicable.
- Agricultural income evidence, exempt income records, or foreign tax documents when relevant.

## Workflow
1. Start with intake: writable ITR work folder, read-only input documents folder, assessment year, filing goal, known income sources, residency, tax regime context, and available documents.
2. Read the existing handoff first when resuming. Create or update `handoff.md` in the writable ITR work folder. Record folder paths, workflow status, workstream assignments, completed work, blockers, next actions, and the resume point.
3. Build a progress checklist with items for document collection, prior-year ITR collection, document analysis, bank statement audit, discrepancy report, user decisions on discrepancies, prior-year comparison, tax preparation, bank coverage annotation, review, handoff update, and final outcome.
4. Ask for applicable missing documents using the checklist above. Always check whether last year's filed ITR is present in the input documents folder; if not, ask the user to provide it or confirm it is unavailable. Explain that unavailable or inapplicable documents can be skipped, but prior-year comparison will be limited without last year's ITR.
5. If raw documents are sensitive, ask whether the user wants to provide redacted copies or extracted text before analysis.
6. Route document-analysis work with the writable ITR work folder and read-only input documents folder. Use a dedicated subfolder and update `handoff.md` after major steps. Request a dashboard report that uses `tax-document-entity-mapping` and `tax-entity-dashboard-report`.
7. After entity mapping is complete, route initial bank statement audit preparation. The audit must use `bank-statement-itr-coverage-audit` and the entity mapping as the evidence layer.
8. After document analysis is complete, route discrepancy report preparation. The discrepancy report must use the structured entity mapping and the `tax-document-discrepancy-report` skill.
9. Review the analyst output, bank statement audit, and discrepancy report for missing documents, empty fields, partial matches, conflicts, user-decision-needed items, unexplained bank transactions, and open questions.
10. For each discrepancy or bank transaction that needs user judgement, collect the user's decision through the coordinating workflow and record it in the relevant discrepancy report or bank audit report. Example: user chooses to accept a Form 16 entry despite it being missing from AIS, or confirms a large bank credit is a transfer from own account.
11. Ask the user for only the missing facts, missing documents, discrepancy decisions, or bank transaction explanations that materially affect ITR selection or schedule preparation.
12. If last year's filed ITR is available, produce a comparative report using `prior-year-itr-comparison` after the current-year dashboard/entities and discrepancy report are available. If it is unavailable, record the limitation.
13. Route tax-rule and filing-preparation work with the writable ITR work folder and read-only input documents folder. Use a dedicated subfolder and update `handoff.md` after major steps. Use the dashboard, structured entities, bank statement audit, discrepancy report with user decisions, prior-year comparison report if available, known facts, and open questions as input.
14. After return preparation is complete, annotate the bank statement audit using `bank-statement-itr-coverage-audit`, marking which transactions are covered in the ITR and where, and flagging high-value unexplained transactions not covered by ITR values.
15. If follow-up questions affect discrepancies or bank transactions, route them through the coordinating workflow; record the user's answers or decisions in the discrepancy report or bank audit report when they resolve or affect a discrepancy or bank transaction, then return the updated context to the relevant workstream.
16. Use `final-itr-filing-report` to combine final outputs into the ITR preparation sheet and filing-readiness report with clearly attributed findings.
17. Perform a second pass: verify that document-derived facts came from document-analysis artifacts, user discrepancy/bank-audit decisions were captured in the relevant reports or handoff, prior-year comparison findings were considered when available, tax-rule conclusions and bank coverage annotations came from tax-preparation artifacts, `handoff.md` is current, and unresolved risks remain visible.

## Decision Points
- If assessment year or financial year is missing, ask before final ITR advice.
- If income sources are unknown, ask broad income-source questions before requesting many documents.
- If documents are missing but not material to the known income profile, continue and mark the gap.
- If documents are missing and material, pause the affected recommendation and ask for them.
- If last year's filed ITR is missing, ask the user to provide it or confirm it is unavailable; continue without prior-year comparison only after recording the limitation.
- If AIS/TIS/Form 26AS conflicts with source documents or bank credits, route back through document-analysis reconciliation before relying on the figure.
- If the bank statement audit flags `Needs user decision` or `Unexplained`, collect user context and record the answer in the bank audit report before tax-preparation work relies on the transaction.
- If bank transactions appear high-value and unexplained after ITR preparation, route the annotated audit through the coordinating workflow for user clarification.
- If the discrepancy report flags `Needs user decision`, collect the user's filing treatment decision and record that decision before tax-preparation work relies on the value.
- If ITR form eligibility depends on a rule, route through tax-preparation work with the exact fact pattern and ask for source-backed reasoning.
- If a tax-preparation follow-up question affects a discrepancy, route it through the coordinating workflow, record the user response in the discrepancy report, and then return the updated discrepancy context to tax-preparation work.
- If specialist outputs conflict, do not average or choose silently. State the conflict and send a focused follow-up to the appropriate specialist.

## Output Format
Return a markdown workflow report with these sections when applicable:

- **Report Provenance**: prepared by, skills used, source artifacts reviewed, report path, and prepared or amended date when available.
- **Workflow Status**: completed, in-progress, blocked, and pending items.
- **Workspace And Handoff**: writable ITR work folder, read-only input documents folder, workstream subfolders, handoff document path, and resume point.
- **Documents Requested**: applicable documents requested, received, missing, and skipped as not applicable.
- **Document Analysis Status**: document-analysis output, dashboard status, unresolved document questions, and mismatches.
- **Discrepancy Report Status**: discrepancy report status, unresolved discrepancies, user-decision-needed items, and user decisions already recorded.
- **Bank Statement Audit Status**: bank audit report status, transactions covered in ITR, transactions needing ITR coverage annotation, high-value unexplained transactions, and user explanations recorded.
- **Prior-Year Comparison Status**: last year ITR availability, comparison report status, new items, missing recurring items, and material changes.
- **ITR Advisory Status**: tax-preparation output, ITR form direction, schedule-ready data status, and missing filing facts.
- **Questions For User**: the smallest set of questions needed to continue.
- **Risks And Open Items**: missing documents, mismatches, unsupported values, rule uncertainties, or schedule fields needing confirmation.
- **Final Outcome**: filing-readiness summary, next steps, and second-pass validation.

## Completion Checks
- Applicable document collection has been requested or explicitly marked skipped/not available.
- Last year's filed ITR has been requested if not present in the input documents folder, or its absence has been recorded.
- Writable ITR work folder and read-only input documents folder have been recorded.
- The handoff records the workspace path where workstreams keep work-in-progress, the shared handoff path, each workstream subfolder path, and a current resume point.
- Each workstream has used its own subfolder inside the writable ITR work folder.
- `handoff.md` has been updated after major workflow steps and contains enough status to resume later.
- No generated files or decrypted working copies have been written into the read-only input documents folder.
- The document dashboard or structured entity output has been produced before schedule-ready data, unless the user already provided equivalent structured input.
- The bank statement audit has been produced after entity mapping and annotated after return preparation when bank statements are available.
- High-value unexplained bank transactions have been flagged and routed to the user through the coordinating workflow.
- The discrepancy report has been produced after document analysis and before schedule-ready data, unless the user explicitly skips discrepancy review.
- User decisions for discrepancy items are recorded in the discrepancy report before those choices are used for ITR preparation.
- Prior-year comparison has been produced when last year's filed ITR is available, or the absence of prior-year comparison has been recorded.
- ITR form recommendation and schedule-ready data are backed by tax-preparation output.
- Tax-preparation work has used the discrepancy report and recorded user decisions when preparing ITR values.
- Missing documents and missing facts are visible; they are not treated as completed.
- Sensitive identifiers are masked unless exact values are necessary and explicitly requested.
- The final report separates document facts, tax-rule conclusions, user assumptions, and unresolved questions.