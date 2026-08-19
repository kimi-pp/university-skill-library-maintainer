---
name: financial-audit-preparer
description: >
  This skill prepares the company for financial audits including documentation, schedules,
  and auditor coordination. Use when asked to prepare for an annual audit, compile audit
  schedules, or coordinate with external auditors. Also consider when the company is
  approaching its first audit or when audit findings from prior years need remediation.
  Suggest when the user is planning a fundraise that will require audited financials.
department: finance
agent: controller-accounting
version: 1.0.0
complexity: complex
related-skills:
  - ../monthly-close-runner/SKILL.md
  - ../financial-systems-setup/SKILL.md
  - ../tax-compliance-manager/SKILL.md
triggers:
  - "prepare for audit"
  - "audit preparation"
  - "get audit ready"
  - "financial audit prep"
  - "external audit readiness"
---

# financial-audit-preparer

## Agent: Controller & Accounting Lead

L2 controller and accounting lead (1x) responsible for monthly close, accounts payable and receivable, payroll, audit preparation, tax compliance, and financial systems setup.

Department ethos: [ideal-finance.md](../../../../departments/finance/ideal-finance.md)

## Skill Description

Prepares the company for financial audits by compiling documentation, building audit schedules, coordinating with external auditors, and remediating prior-year findings.

## When to Use

- When the annual financial audit is approaching and preparation needs to begin (typically 2-3 months before auditor fieldwork).
- When the company is engaging auditors for the first time and needs to establish audit-ready processes.
- When prior-year audit findings require remediation before the next audit cycle.

## Workflow

1. **Audit Timeline Planning**: Coordinate with the audit firm on the engagement timeline including planning meeting, interim procedures, fieldwork dates, and report delivery. Align internal deadlines for schedule preparation. Deliverable: audit timeline with internal milestones.
2. **PBC List Management**: Receive the Prepared by Client (PBC) list from auditors. Assign each item to an internal owner with a deadline. Track completion and quality-review each deliverable before submission. Deliverable: PBC tracker with ownership and status.
3. **Audit Schedule Preparation**: Build the supporting schedules: revenue recognition detail (ASC 606 analysis by contract), deferred revenue rollforward, equity rollforward, debt schedule, lease schedule (ASC 842), related-party transactions, and subsequent events. Deliverable: completed audit schedules with supporting documentation.
4. **Revenue Recognition Documentation**: Prepare ASC 606 documentation for all material contracts: identify performance obligations, determine transaction price, allocate to obligations, and document the recognition pattern. Deliverable: ASC 606 workpapers by contract.
5. **Internal Control Documentation**: Document key financial controls (segregation of duties, approval authorities, reconciliation procedures, system access controls). Identify and remediate any gaps before auditor testing. Deliverable: internal control matrix with remediation status.
6. **Auditor Coordination**: Manage day-to-day auditor requests during fieldwork. Respond to inquiries within 24 hours. Track open items and escalate blockers. Host weekly status meetings. Deliverable: auditor request tracker with response log.
7. **Finding Remediation**: Address any audit findings or management letter comments. Build remediation plans with specific actions, owners, and deadlines. Confirm remediation before the next audit cycle. Deliverable: remediation plan with progress tracking.

## Anti-Patterns

- **Scrambling at fieldwork**: Waiting until auditors arrive to begin preparing schedules and documentation. *Why*: last-minute preparation produces errors, extends fieldwork, increases audit fees, and signals weak financial controls.
- **ASC 606 documentation after the fact**: Documenting revenue recognition judgments months after the transactions occurred rather than contemporaneously. *Why*: after-the-fact documentation is less credible and may not accurately capture the original assessment, creating audit risk.
- **Ignoring management letter comments**: Treating management letter observations as minor suggestions rather than mandatory remediation items. *Why*: unaddressed management letter comments escalate to formal findings in subsequent audits and signal control deficiencies to investors.
- **Withholding information from auditors**: Delaying responses or providing incomplete information to minimize auditor scrutiny. *Why*: auditors will find the issues eventually; obstruction damages the relationship and may result in a qualified opinion.

## Output

**On success**: Produces a complete audit preparation package including PBC deliverables, audit schedules, ASC 606 workpapers, internal control documentation, and remediation plan. Delivered per the audit timeline.

**On failure**: Report which PBC items are incomplete, what schedules cannot be prepared (e.g., missing source data), and the impact on the audit timeline. Provide a revised completion schedule with escalation to the CFO.

## Related Skills

- [`monthly-close-runner`](../monthly-close-runner/SKILL.md) -- Clean monthly closes throughout the year are the foundation of audit readiness.
- [`financial-systems-setup`](../financial-systems-setup/SKILL.md) -- Properly configured systems produce the audit trail that supports preparation.
