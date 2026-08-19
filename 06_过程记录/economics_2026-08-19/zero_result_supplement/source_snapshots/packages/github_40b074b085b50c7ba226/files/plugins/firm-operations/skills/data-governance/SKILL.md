---
name: data-governance
description: >
  Contains verified WISP template outline (IRS Pub 5708 seven sections and six
  attachments), IRC 6501/6511 retention schedule by document type, and NIST 800-88
  destruction procedures. Information security, PII protection, record retention,
  breach response, client-vs-firm workpaper ownership, litigation hold, electronic
  storage standards (Rev Proc 98-25), engagement letter retention clauses, firm
  succession planning for client files. Consult when drafting or reviewing a WISP,
  determining how long to keep tax returns or workpapers, handling a suspected data
  breach (5071C letters, rejected e-files, unauthorized access), setting up MFA or
  encryption per IRS Pub 4557, destroying old hard drives or shredding records,
  onboarding or offboarding staff with PII access, switching to cloud storage,
  sharing workpapers with a successor accountant, or writing document retention
  clauses for engagement letters.
---

# Data Governance

Operational skill for information security, document lifecycle management, and
client data protection in a tax and accounting practice. The legal framework
(GLBA/FTC Safeguards Rule, IRC 7216, IRS Pub 4557) treats every tax preparer
as a financial institution with mandatory security obligations regardless of
firm size.

## Legal Obligations at a Glance

The firm operates under overlapping mandates:

- **FTC Safeguards Rule (GLBA)** -- Written information security plan required; MFA for all customer-information access; breach notification to FTC within 30 days if 500+ people affected
- **IRC Section 7216** -- Criminal penalties (up to $1,000 fine / 1 year imprisonment per violation) for unauthorized disclosure or use of tax return information; written taxpayer consent required for any non-preparation use
- **IRS Pub 1345** -- Six security/privacy standards for authorized e-file providers; additive to FTC requirements
- **IRS Pub 4557** -- Baseline security controls (anti-malware, encryption, MFA, backup, access controls, audit trails)
- **IRS Pub 5708** -- Official WISP template for tax and accounting practices

## Written Information Security Plan (WISP)

Every firm must maintain a written, accessible WISP scaled to its size and
data sensitivity. IRS Pub 5708 provides the baseline template.

### Required WISP Sections

1. **Objectives, Purpose, and Scope** -- Legal basis (GLBA, FTC Safeguards), what data is protected, plan boundaries
2. **Designated Qualified Individual** -- Data Security Coordinator (DSC) implements/supervises the plan; Public Information Officer (PIO) handles breach communications. In small firms the owner fills both roles.
3. **Risk Assessment** -- Catalog all data types handled (taxpayer PII, employee data, business financials); identify internal risks (employee error, theft) and external risks (hacking, phishing, physical theft, natural disaster); assess potential damage; define monitoring procedures
4. **Hardware Inventory** -- Every device storing/processing taxpayer data: computers, laptops, phones, tablets, printers, routers, external drives, USB. Record description, location, and data types per device.
5. **Safety Measures Policies** -- Data collection/retention, disclosure, network protection, user access control, electronic data exchange, Wi-Fi, remote access, connected devices, reportable incidents, employee code of conduct
6. **Implementation Clause** -- Date, firm name, compliance statement citing GLBA/FTC, signatures of principal and DSC

### Required WISP Attachments

- **A** -- Record Retention Policies (see Retention Schedule below)
- **B** -- Rules of Behavior and Conduct Safeguarding Client PII
- **C** -- Security Breach Procedures and Notifications
- **D** -- Employee/Contractor Acknowledgement of Understanding
- **E** -- Firm Hardware Inventory containing PII Data
- **F** -- Firm Employees Authorized to Access PII

### Annual WISP Review Checklist

Trigger: at least annually, or on any material change (new office, staff, technology).

- [ ] Update hardware inventory (Attachment E)
- [ ] Update authorized access list (Attachment F) for personnel changes
- [ ] Verify all employees completed annual security training
- [ ] Test incident response procedures
- [ ] Review and update security software
- [ ] Document the review and any changes made

## PII Definition

PII = first name (or initial) + last name of a taxpayer, spouse, dependent, or
guardian combined with any of:

- SSN, date of birth, or employment data
- Driver's license or state-issued ID number
- Income, tax filing, retirement plan, asset, or investment data
- Financial account numbers, credit/debit card numbers, access codes, passwords
- Email addresses, non-listed phone numbers, residential/mobile contact info

Publicly available information (phone directories, public records) is excluded.

## Security Controls

### Baseline Technical Requirements (IRS Pub 4557)

- Anti-malware/anti-virus on all devices, auto-update enabled
- Firewall and anti-spyware active
- Drive encryption on all devices storing client data
- MFA for all system access to customer information
- Strong passwords: min 8 characters (16 for admin), mixed case/numbers/symbols, unique per account
- Browsers and all software kept current
- Audit trails recording who did what and when
- Backup to encrypted external source not connected full-time to network

### Network and Remote Access

- Change default router credentials; use WPA-3 (never WEP)
- Rename SSID to non-identifying name; disable SSID broadcast; reduce broadcast power
- No business use on public Wi-Fi
- VPN required for all remote access
- Consider firm-issued laptops for remote workers

### Secure File Sharing and Client Portal

- Encrypt all files containing PII before transmission
- Use firm-managed client portal (not email) for PII exchange
- Portal access requires MFA
- Disable portal access for former clients or terminated engagements
- Log all portal upload/download activity

### Data Backup and Disaster Recovery

- Encrypt backups before storing
- Maintain backup copies in a separate physical location or cloud storage
- Monthly backup cadence minimum; increase frequency during filing season
- Test restore procedures at least annually
- Backups must not remain connected full-time to the production network
- After a breach: make full backups of all business data before remediation changes

## Data Breach Response

### Detection Indicators

Watch for these signs of compromised taxpayer data:

- E-filed returns rejected (SSN already filed)
- Clients receive IRS authentication letters (5071C, 4883C, 5747C) without filing
- Clients who haven't filed receive refunds or transcripts
- IRS online account notices about unauthorized access
- EFIN/PTIN filing counts exceed actual filings
- Clients respond to emails the firm never sent
- Slow/unusual computer behavior, unexpected lock-outs

### Notification Sequence

When a breach is confirmed, notify in this order:

1. **IRS** -- Contact local Stakeholder Liaison immediately
2. **FBI** -- Contact local field office if directed by IRS
3. **Local police** -- File a police report
4. **State tax agencies** -- Federation of Tax Administrators for state contacts
5. **FTC** -- Report at IdentityTheft.gov; mandatory within 30 days if 500+ people affected
6. **Security expert** -- Engage to determine cause, scope, and remediation
7. **Insurance carrier** -- Report to professional liability / cyber insurance carrier

### Recovery Procedure

- Update IRS Stakeholder Liaison with developments
- Determine intrusion vector; fix vulnerabilities before resuming operations
- May need new EFIN before resuming e-filing
- Review FTC guidance: "Data Breach Response: A Guide for Business"
- Develop or update business continuity plan

## Document Retention Schedule

### IRS Assessment Periods (Baseline Logic)

- **3 years** -- Standard period of limitations (IRC 6501(a)); minimum for returns and supporting docs
- **6 years** -- Gross income understated by >25% (IRC 6501(e)); unreported foreign financial accounts/assets
- **7 years** -- Deduction for worthless securities or bad debts claimed (IRC 6511(d))
- **Unlimited** -- Fraud or willful evasion (IRC 6501(c)(1)-(2)); failure to file a required return (IRC 6501(c)(3))
- **3 years from filing** -- Refund claims on amended returns

### Retention by Document Type

- **Filed tax returns** -- 7-year minimum, permanent recommended
- **Tax workpapers** -- 7 years from filing date
- **Source documents (receipts, invoices)** -- 7 years
- **Asset/depreciation records** -- Life of asset + 7 years after disposition
- **Employment tax records (payroll, W-2, 941)** -- 4-year minimum, 7 years recommended
- **Estimated tax payment records** -- 7 years
- **Entity formation documents (articles, EIN letter, bylaws)** -- Permanent (life of entity + 7 years after dissolution)
- **Board minutes and resolutions** -- Permanent
- **Contracts and agreements** -- 7 years after expiration/termination
- **Bank statements and reconciliations** -- 7 years
- **General ledger and journals** -- 7-year minimum, permanent if feasible
- **Financial statements** -- 7-year minimum, permanent recommended
- **Engagement letters** -- 7 years from engagement end, permanent recommended
- **IRS/state correspondence** -- 7 years
- **Form 5472 records** -- 7-year minimum, permanent recommended (high audit risk)
- **Florida sales tax records** -- 3 years from date tax became due or was paid

### State Considerations

- Retain for the longest applicable period across all jurisdictions
- Florida corporate income tax follows federal periods (3 years general, 6 years for substantial understatement, unlimited for fraud)
- California: 4 years general, 8 years for 25% understatement
- State-specific extensions may apply for amended returns, refund claims, or collection actions

## Client Documents vs. Firm Workpapers

### Ownership Rules

- **Client documents** (originals provided by the client) belong to the client; return promptly after scanning
- **Firm workpapers** (trial balances, lead schedules, tax computations, review notes, internal memos) are firm property; not required to provide to client unless court-ordered
- Workpapers may be provided to a successor accountant with written client consent
- Firm retains workpapers per retention policy regardless of client relationship status

### Gray Areas

- Adjusted trial balance from client data: firm workpaper
- Accounting system reports exported by firm: client data; provide copies on request
- Tax return copy: client entitled to a copy; firm retains its own
- IRS/state correspondence on behalf of client: provide copies on request
- Engagement letter: both parties retain signed copies

## Engagement Letter Retention Clauses

Include in every engagement letter:

- "The firm will retain copies of workpapers and filed returns for [7] years from the date of filing"
- "Original client documents will be returned upon request; the firm retains copies"
- "Upon expiration of the retention period, records will be destroyed without further notice"
- "The client is responsible for maintaining their own copies of all tax returns and supporting documents"
- "In the event of firm dissolution, client records will be [transferred to successor firm / returned to client / destroyed per retention schedule]"

## Electronic Storage Standards

- Use PDF/A (ISO 19005) for long-term archival; avoid proprietary formats
- All electronic records containing PII must be encrypted
- Implement indexed storage with search and retrieval capability
- Access controls: only authorized personnel can access, modify, or delete
- Must be able to produce legible hardcopy on demand (IRS Rev. Proc. 98-25)
- Cloud storage acceptable if vendor meets security and availability requirements
- Maintain backup redundancy: cloud primary + local backup or vice versa

## Destruction Procedures

### Pre-Destruction Checklist

- [ ] Retention period has expired for all records in the batch
- [ ] No pending or reasonably anticipated litigation, audit, or investigation
- [ ] Records manager or firm principal has approved destruction
- [ ] Destruction manifest prepared (what, when, by whom, authorization)

### Destruction Methods by Media Type

- **Paper** -- Cross-cut shredding or incineration (strip shredding is not secure for PII)
- **Hard drives/SSDs** -- NIST 800-88 compliant sanitization; physical destruction is most certain
- **Electronic records** -- Secure deletion by overwriting or degaussing
- **Cloud-stored records** -- Delete from all locations including backups and recycling bins; verify with provider
- **Third-party vendors** -- Vet for NAID AAA certification

### Litigation Hold

A litigation hold overrides the retention schedule immediately. If litigation is
pending, threatened, or reasonably anticipated:

- Suspend all destruction of potentially relevant records
- Notify all relevant personnel and document the hold
- Destroying records under hold can result in adverse inference, sanctions, or criminal obstruction charges

### Destruction Cadence

Annual cycle recommended: every January, destroy records whose retention period
expired in the prior calendar year.

## Firm Succession Planning for Client Files

- Succession plan must address custody of all client records
- Options: transfer to acquiring firm (with client consent), return to clients, retain in escrow with third party
- Notify clients in advance of any firm transition
- Maintain professional liability tail coverage for transferred engagements
- Successor firm assumes no liability for predecessor work unless explicitly agreed
- Maintain a master inventory of all client files, locations, and retention expiration dates

## Decision Logic

**WISP template vs. custom:** Small firms start with IRS Pub 5708 template and customize. Larger firms may need a more comprehensive plan exceeding the template structure.

**7-year vs. permanent retention:** Electronic storage is cheap. The 7-year minimum covers most risk scenarios, but permanent retention for filed returns and entity documents eliminates doubt.

**Paper vs. electronic:** Move to all-electronic with paper destruction after scanning and quality verification. Reduces cost and improves searchability.

**Cloud vs. on-premise security:** Cloud solutions shift some security responsibility to the vendor, but the firm must verify vendor compliance and maintain its own access controls.

**Cyber insurance:** Consider separate cyber liability insurance in addition to E&O. Cyber policies cover breach response costs, notification expenses, and regulatory fines.

**Employee training cadence:** IRS recommends at least annual; quarterly security reminders during filing season are best practice.

## Supporting References

Read these for full-depth guidance on specific topics:

- `references/data-security.md` -- Legal framework (GLBA, FTC Safeguards Rule, IRC 7216, IRS Pub 1345), complete WISP outline per IRS Pub 5708 with all seven sections and six attachments, IRS Pub 4557 security controls (anti-malware, passwords, MFA, encryption, wireless, stored data), data theft detection indicators, breach reporting contacts and recovery steps, annual review checklist, PII definition, and decision points for WISP customization and cyber insurance. Read when drafting or reviewing a WISP, setting up security controls, or responding to a breach.

- `references/document-retention.md` -- IRS assessment periods (IRC 6501/6511) with all standard and extended limitation periods, retention schedule by document type with minimum and recommended periods, Florida and state-specific requirements, client document vs. firm workpaper ownership rules with gray-area guidance, electronic storage standards (IRS Rev. Proc. 98-25, PDF/A), destruction procedures by media type (NIST 800-88), litigation hold rules, engagement letter retention clauses, and firm succession planning for client files. Read when determining retention periods, drafting engagement letter language, planning file destruction, or advising on firm succession.

## Cross-Plugin References

For related firm-operations knowledge:
- Invoke `firm-operations:quality-compliance` for regulatory requirements, peer review standards, and professional liability management
- Invoke `firm-operations:engagement-management` for engagement letter preparation, client onboarding procedures, and engagement file organization standards

Cross-plugin consumers:
- `tax-prep:e-filing` -- Taxpayer data safeguarding requirements per IRS Pub 4557; EFIN security monitoring
- All plugins reference this skill for PII handling standards, retention rules, and secure file management procedures
