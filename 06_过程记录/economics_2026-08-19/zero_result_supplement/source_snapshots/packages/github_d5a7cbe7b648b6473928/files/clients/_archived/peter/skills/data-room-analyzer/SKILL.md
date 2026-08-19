---
name: data-room-analyzer
version: 1.0.0
description: "Ingest and analyze a full virtual data room: auto-extract key docs, flag missing items, summarize findings by category, produce diligence memos for M&A transactions."
---

# data-room-analyzer

Systematically ingest, categorize, and analyze a virtual data room (VDR) for M&A due diligence. The VDR is the single most important artifact in any deal — it contains every document the buyer needs to underwrite an acquisition. This skill automates the grunt work: indexing every document, flagging gaps against a standard diligence checklist, extracting key findings by category, and producing a diligence summary memo that a deal team can immediately act on.

## Trigger

- "Analyze data room for [DEAL/COMPANY]"
- "Data room review"
- "VDR diligence summary"
- "What's missing from the data room?"
- "Data room gap analysis"
- "Diligence memo from VDR"
- "Index the data room"

## Inputs

### Required
- **Data room contents:** File listing or document index (CSV, directory listing, or VDR platform export)
- **Target company:** Name of the acquisition target
- **Deal type:** M&A buy-side / sell-side / refinancing / IPO (default: M&A buy-side)

### Optional
- **Diligence checklist:** Custom checklist (default: standard M&A diligence checklist)
- **Priority areas:** Specific focus areas (e.g., "IP ownership", "customer concentration", "environmental liabilities")
- **Transaction value:** Approximate deal size for materiality thresholds
- **Industry:** Target's industry for sector-specific diligence items
- **Timeline:** Expected close date (affects urgency flagging)

## Dependencies

- **financial-data-api** — data source stack (see `../financial-data-api/SKILL.md`)
- **sec-edgar-fetch** — SEC EDGAR integration for public company targets

## ⚠️ DATA SOURCING MANDATE (NON-NEGOTIABLE)

1. **VDR Documents (PRIMARY):** All analysis must reference specific documents from the data room. Never fabricate document contents or assume availability.
2. **SEC EDGAR (SUPPLEMENTARY for public targets):** Cross-reference VDR financials against public filings to identify discrepancies.
3. **web_search (CONTEXT ONLY):** Industry benchmarks, comparable deal terms, regulatory requirements. Never substitute for VDR document review.

## Methodology

### Step 1: Data Room Indexing

Ingest the full document listing and build a structured index:

**Standard VDR Categories (10 sections):**

| Section | Category | Key Documents |
|---------|----------|---------------|
| 1.0 | Corporate & Organizational | Charter, bylaws, org chart, cap table, board minutes, shareholder agreements |
| 2.0 | Financial | Audited financials (3-5 yrs), monthly management accounts, budget/forecast, AR/AP aging, debt schedule |
| 3.0 | Tax | Federal/state returns (3 yrs), tax provision workpapers, transfer pricing studies, NOL schedule |
| 4.0 | Legal & Litigation | Pending/threatened litigation, settlement history, consent decrees, regulatory investigations |
| 5.0 | Contracts & Commercial | Material contracts, customer agreements (top 20), supplier contracts, revenue backlog |
| 6.0 | Intellectual Property | Patent schedule, trademark registrations, license agreements, trade secret policies, IP assignment agreements |
| 7.0 | Real Estate & Assets | Lease schedule, owned property, environmental assessments, equipment lists, title insurance |
| 8.0 | HR & Employment | Employee census, compensation data, benefit plans, employment agreements, union contracts, WARN Act compliance |
| 9.0 | Regulatory & Compliance | Permits/licenses, industry-specific compliance, data privacy (GDPR/CCPA), anti-corruption policies |
| 10.0 | Insurance | Policy schedule, claims history, D&O coverage, key-man policies |

For each document found:
- Assign to category and sub-category
- Note file type, date, page count
- Flag if stale (>12 months old for time-sensitive docs)
- Flag if draft vs. executed version

### Step 2: Gap Analysis

Compare indexed documents against the standard diligence checklist:

**Criticality scoring:**
- 🔴 **Critical Missing** — Deal-blocker; must be produced before signing (e.g., audited financials, cap table, material contracts)
- 🟡 **Important Missing** — Should be produced before closing; absence creates risk (e.g., IP assignments, environmental Phase I)
- 🟢 **Nice-to-Have Missing** — Helpful but not deal-critical (e.g., org charts, employee handbook)

**Industry-specific gap items:**
- **Technology:** Source code escrow, OSS license audit, SOC 2 reports, data processing agreements
- **Healthcare:** HIPAA compliance, clinical trial data, FDA correspondence, provider agreements
- **Manufacturing:** Environmental permits, OSHA records, product liability history, supply chain mapping
- **Financial Services:** Regulatory examination reports, BSA/AML compliance, capital adequacy
- **Real Estate:** Phase I/II environmental, title reports, zoning compliance, rent rolls

### Step 3: Document-Level Analysis

For each major document category, extract key findings:

**Financial Analysis:**
- Revenue trend and composition (recurring vs. one-time)
- EBITDA margins and adjustments (management vs. audited)
- Working capital trends and seasonality
- CapEx requirements (maintenance vs. growth)
- Quality of earnings indicators (cash conversion, DSO/DPO/DIO trends)
- Audit opinion type (unqualified, qualified, going concern)

**Legal & Contractual Analysis:**
- Change of control provisions in material contracts
- Non-compete/non-solicit enforceability
- Key customer contract expiration schedule
- Litigation exposure (quantify probable + possible losses)
- Consent requirements for assignment

**IP & Technology Analysis:**
- IP ownership chain (employee invention assignments, contractor work-for-hire)
- Third-party license dependencies
- Patent expiration timeline
- Open-source license compliance risk
- Freedom-to-operate concerns

**HR & Employment Analysis:**
- Key employee retention risk
- Unfunded pension/OPEB obligations
- Employment agreement triggers on change of control
- Contractor misclassification risk
- WARN Act exposure

### Step 4: Red Flag Identification

Systematically scan for deal-risk indicators:

| Red Flag | Example | Impact |
|----------|---------|--------|
| Revenue concentration | Top 3 customers >50% of revenue | Key-person risk; negotiate earnout or escrow |
| Related-party transactions | Owner-related entities in supply chain | Require arm's length verification |
| Pending litigation | Material claims without reserves | Quantify exposure, adjust purchase price |
| Change of control triggers | Key contracts terminate on sale | Require consent; may reduce value |
| Environmental liability | Known contamination without remediation | Phase II study; indemnification |
| Tax exposure | Aggressive positions without reserves | Tax insurance or escrow |
| Stale financials | Most recent audit >18 months old | Require stub period review |
| Missing IP assignments | Founder-era code without assignment | Remediate pre-closing |

### Step 5: Diligence Memo Drafting

Produce a structured diligence summary memo organized by:
1. **Executive Summary** — Overall data room completeness, top 5 findings, recommended actions
2. **Category-by-Category Findings** — Key items, risks, and follow-up questions per section
3. **Gap List** — Complete list of missing items with criticality ratings
4. **Red Flags & Risk Items** — Prioritized list with estimated impact and mitigation
5. **Follow-Up Request List** — Specific additional documents or information needed from seller

### Step 6: Materiality Calibration

Set materiality thresholds based on deal size:
- **Contracts:** Material if >5% of revenue or >$X,000 annual value
- **Litigation:** Material if >1% of enterprise value
- **Related-party:** All related-party transactions flagged regardless of size
- **Tax positions:** Material if >$X00K exposure
- **Customer concentration:** Flag if any customer >10% of revenue

### Step 7: Comparable Transaction Benchmarks

When analyzing a target's data room, contextualize findings against precedent transactions in the same sector. This transforms raw data room analysis into deal-ready intelligence.

**Precedent Transaction Research:**
```
web_search("[INDUSTRY] M&A transactions acquisition multiples [YEAR-2] [YEAR-1] [YEAR]")
web_search("[INDUSTRY] precedent transactions enterprise value EBITDA revenue multiples")
web_search("[TARGET COMPANY] comparable acquisitions similar companies sold")
```

**Benchmark Table (include in every data room analysis with financial docs present):**

| Transaction | Date | Target | Acquirer | EV ($M) | EV/Revenue | EV/EBITDA | EV/EBIT | Premium |
|-------------|------|--------|----------|---------|------------|-----------|---------|---------|
| [Deal 1] | [Date] | [Target] | [Buyer] | $XXX | X.Xx | XX.Xx | XX.Xx | XX% |
| [Deal 2] | [Date] | [Target] | [Buyer] | $XXX | X.Xx | XX.Xx | XX.Xx | XX% |
| [Deal 3] | [Date] | [Target] | [Buyer] | $XXX | X.Xx | XX.Xx | XX.Xx | XX% |
| [Deal 4] | [Date] | [Target] | [Buyer] | $XXX | X.Xx | XX.Xx | XX.Xx | XX% |
| [Deal 5] | [Date] | [Target] | [Buyer] | $XXX | X.Xx | XX.Xx | XX.Xx | XX% |
| **Median** | | | | | **X.Xx** | **XX.Xx** | **XX.Xx** | **XX%** |
| **Mean** | | | | | **X.Xx** | **XX.Xx** | **XX.Xx** | **XX%** |

**Context Application:**
- Compare target's implied valuation (if available) against precedent medians
- Flag if data room financials suggest metrics materially different from precedent targets (e.g., lower margins, higher growth)
- Note deal structure differences (stock vs. cash, earnout %, escrow) that affect comparability
- Identify if target is trading at a premium or discount to precedents and why

**Minimum standard:** 5 named precedent transactions with specific multiples. No ranges without underlying data. If fewer than 5 are available in the exact sub-sector, expand to adjacent sectors with explicit notation.

### Step 8: Post-Close Integration Red Flags

Data room analysis should proactively identify integration risks — these are the issues that destroy value after closing. Scan every data room against this checklist:

**IT Systems & Technology Integration:**
- [ ] ERP system: identify platform (SAP, Oracle, NetSuite, custom) — different platforms = $X00K–$XM migration cost
- [ ] CRM system: Salesforce, HubSpot, custom — customer data migration risk
- [ ] Data hosting: on-premise vs. cloud; if on-premise, assess migration timeline
- [ ] Cybersecurity: SOC 2 report present? Penetration testing? Incident history?
- [ ] Custom software: any proprietary systems without documentation = integration nightmare
- [ ] IT contracts: check for change-of-control termination provisions in SaaS/hosting agreements

**Key Person Dependencies:**
- [ ] Founder/CEO centrality: does revenue depend on personal relationships?
- [ ] Top salesperson concentration: if top rep generates >20% of revenue, retention is critical
- [ ] Technical key persons: is critical IP knowledge concentrated in 1-2 engineers?
- [ ] Non-compete scope: do key employees have enforceable non-competes?
- [ ] Employment agreement change-of-control triggers: golden parachutes, acceleration, termination rights
- [ ] Retention packages: are stay bonuses budgeted? Typical = 6-24 months salary for key employees

**Customer Overlap & Revenue Risk:**
- [ ] Customer overlap with acquirer: shared customers may consolidate spend (revenue at risk)
- [ ] Customer consent requirements: do contracts require customer consent for assignment?
- [ ] Key customer reaction risk: will top customers re-bid if ownership changes?
- [ ] Revenue portability: how much revenue follows the company vs. follows individuals?
- [ ] Contract assignability: check every material contract for assignment restrictions

**Regulatory & Compliance Integration:**
- [ ] HSR/antitrust: deal size threshold ($111.4M in 2024) — filing required?
- [ ] Industry-specific approvals: FCC, state insurance, banking regulators, CFIUS
- [ ] License transferability: are permits/licenses transferable or must they be re-applied?
- [ ] Data privacy: GDPR/CCPA consent requirements for customer data transfer
- [ ] Environmental: Phase I complete and current? Known contamination = buyer liability post-close

**Cultural & Operational Integration:**
- [ ] Compensation philosophy mismatch: target pays commission-heavy, acquirer is salary-based (or vice versa)
- [ ] Remote vs. in-office policy differences
- [ ] Benefits gap: target has better/worse health/retirement plans — harmonization cost
- [ ] Union/labor agreements: do they survive change of control?
- [ ] Facility consolidation: lease terms, break clauses, overlap assessment

### Step 9: Missing Documents Escalation Framework

Not all missing documents are equally important. Weight each gap by materiality to focus the deal team's follow-up requests.

**Materiality Scoring Matrix:**

| Weight | Category | Criteria | Examples |
|--------|----------|----------|----------|
| **10 — Deal-Breaker** | Cannot close without this | Required for legal closing conditions; absence creates unquantifiable risk | Cap table, audited financials (3yr), material contract originals, IP assignment chain |
| **8 — Price-Affecting** | Absence should reduce purchase price or require indemnification | Missing item creates quantifiable risk that should be reflected in economics | Environmental Phase I, tax returns, litigation detail, insurance claims history |
| **6 — Diligence-Critical** | Required for complete diligence opinion | Missing item means diligence cannot be completed in a category; may require rep/warranty coverage | Customer contract detail, employee census, benefits plan documents, regulatory correspondence |
| **4 — Important Context** | Would materially improve analysis quality | Available information is sufficient but incomplete; adds risk to conclusions | Board minutes, detailed budget/forecast, supplier contracts, organization chart |
| **2 — Nice-to-Have** | Helpful but not material to deal economics | Absence is noted but does not change the analysis or recommendation | Employee handbook, marketing materials, office lease details for non-material locations |

**Escalation Protocol:**

1. **Weight 10 items:** Immediate escalation to deal lead + counsel. Include in "Conditions to Closing" tracker. Set 48-hour response deadline.
2. **Weight 8 items:** Include in first follow-up request list. Flag as "purchase price adjustment items" if not produced within 1 week.
3. **Weight 6 items:** Include in follow-up request list with specific rationale for why each item is needed.
4. **Weight 4 items:** Batch into second-round diligence request.
5. **Weight 2 items:** Request if time permits; note absence in diligence memo as a limitation.

**Missing Document Impact Template (add to output):**

```
━━━ MISSING DOCUMENTS — MATERIALITY-WEIGHTED ━━━
| # | Missing Item | Category | Weight | Impact if Missing | Deadline |
|---|-------------|----------|--------|-------------------|----------|
| 1 | [Item]      | X.X      | 10     | [Specific risk]   | 48 hours |
| 2 | [Item]      | X.X      | 8      | [Specific risk]   | 1 week   |
| 3 | [Item]      | X.X      | 6      | [Specific risk]   | 2 weeks  |

Total materiality-weighted gap score: XX / [possible]
Assessment: [Deal can proceed with caveats / Critical items must be produced / Data room incomplete for closing]
```

## Output Format

```
📁 Data Room Analysis — [Target Company]
Prepared: [Date] | Transaction: [Deal Type] | Data Room as of: [Date]
Total Documents Indexed: XXX | Categories Covered: X/10

━━━ EXECUTIVE SUMMARY ━━━
Data room completeness: XX% (XX/XX standard items present)
Critical gaps: X items requiring immediate production
Red flags identified: X items requiring investigation
Overall assessment: [Well-organized / Adequate / Significant gaps / Incomplete]

Top 5 Findings:
1. [Finding — e.g., "Revenue concentration: top 3 customers = 62% of revenue with contracts expiring within 18 months"]
2. [Finding]
3. [Finding]
4. [Finding]
5. [Finding]

━━━ DATA ROOM INDEX ━━━
| Section | Category              | Docs Found | Expected | Status |
|---------|-----------------------|-----------|----------|--------|
| 1.0     | Corporate & Org       | XX        | XX       | 🟢/🟡/🔴 |
| 2.0     | Financial             | XX        | XX       | 🟢/🟡/🔴 |
| 3.0     | Tax                   | XX        | XX       | 🟢/🟡/🔴 |
| 4.0     | Legal & Litigation    | XX        | XX       | 🟢/🟡/🔴 |
| 5.0     | Contracts & Commercial| XX        | XX       | 🟢/🟡/🔴 |
| 6.0     | Intellectual Property | XX        | XX       | 🟢/🟡/🔴 |
| 7.0     | Real Estate & Assets  | XX        | XX       | 🟢/🟡/🔴 |
| 8.0     | HR & Employment       | XX        | XX       | 🟢/🟡/🔴 |
| 9.0     | Regulatory & Compliance| XX       | XX       | 🟢/🟡/🔴 |
| 10.0    | Insurance             | XX        | XX       | 🟢/🟡/🔴 |

━━━ CRITICAL GAPS (🔴) ━━━
| # | Missing Item                    | Category | Impact | Recommended Action |
|---|--------------------------------|----------|--------|--------------------|
| 1 | [Item]                         | X.X      | [Impact] | [Action + timeline] |
| 2 | [Item]                         | X.X      | [Impact] | [Action + timeline] |

━━━ IMPORTANT GAPS (🟡) ━━━
| # | Missing Item                    | Category | Impact |
|---|--------------------------------|----------|--------|
| 1 | [Item]                         | X.X      | [Impact] |

━━━ RED FLAGS ━━━
| # | Finding | Category | Severity | Est. Impact ($) | Mitigation |
|---|---------|----------|----------|-----------------|------------|
| 1 | [Flag]  | X.X      | High/Med/Low | $X,XXXK  | [Action]   |

━━━ CATEGORY FINDINGS ━━━

**1.0 Corporate & Organizational**
- Cap table: [Key findings — fully diluted ownership, option pool, any unusual structures]
- Governance: [Board composition, voting agreements, drag-along/tag-along rights]
- Follow-up: [Specific questions or missing items]

**2.0 Financial**
- Revenue quality: [Recurring %, customer concentration, trend analysis]
- EBITDA bridge: [Reported vs. adjusted, nature of add-backs]
- Working capital: [Trends, seasonality, normalization issues]
- Follow-up: [Specific questions]

[Continue for sections 3.0–10.0]

━━━ FOLLOW-UP REQUEST LIST ━━━
| # | Request | Priority | Category | Rationale |
|---|---------|----------|----------|-----------|
| 1 | [Specific document/information] | Critical/High/Medium | X.X | [Why needed] |

━━━ TRIPLE-THREAT LENS ━━━
🏦 **Banker:** [Data room quality assessment for deal execution — will this pass buyer diligence? What needs remediation before going to market? Are there deal structure implications (escrow, earnout, reps & warranties)?]
📊 **Accountant:** [Quality of earnings implications — are the financials audit-ready? What adjustments are likely in a QoE report? Working capital normalization issues?]
💰 **Wealth Manager:** [For a buyer: what's the real risk here? Hidden liabilities? Integration complexity? Post-close surprises to budget for?]
```

## Quality Gates

- [ ] All 10 standard VDR categories assessed with document counts
- [ ] Gap analysis uses three-tier criticality scoring (🔴🟡🟢)
- [ ] Red flags quantified with estimated dollar impact where possible
- [ ] Industry-specific diligence items included based on target's sector
- [ ] Materiality thresholds documented and consistently applied
- [ ] Follow-up request list is specific (not generic) — references actual gaps found
- [ ] Change of control provisions identified across contracts
- [ ] Financial data cross-referenced against public filings (if public target)
- [ ] Stale documents flagged with date stamps
- [ ] Triple-threat lens references specific findings from the analysis
- [ ] Every finding traces to a specific document or identified gap

## Professional Standards

**What separates A from B:**
- **A-grade:** Every gap has a specific recommended action with timeline. Red flags quantified with dollar impact. Industry-specific items beyond the standard checklist. Cross-references between categories (e.g., employment agreements flagged in HR section also noted in change-of-control analysis). Materiality calibrated to deal size.
- **B-grade:** Generic checklist comparison without prioritization. No dollar quantification of risks. Missing industry-specific items. No cross-referencing between sections.

**Common pitfalls:**
- Treating all gaps equally — a missing org chart is not the same as missing audited financials
- Not checking document dates — a 3-year-old environmental assessment is essentially useless
- Ignoring draft vs. executed status — a draft contract has no legal weight
- Missing change-of-control provisions — the #1 post-close surprise in middle-market M&A
- Not cross-referencing financial data room docs against public filings for inconsistencies
- Failing to flag related-party transactions that may not survive post-acquisition

## See Also

- `vendor-due-diligence` — sell-side financial diligence report
- `letter-of-intent-analyzer` — LOI terms that drive diligence scope
- `credit-analysis` — credit-focused diligence for financing
