---
name: regulatory-ops-intel
description: This skill should be used when generating a daily brief or when the user asks about "regulatory updates", "SEC rules", "CFTC rules", "fund admin news", "operational intel", "ILPA updates", "PE technology news", "compliance deadlines", "vendor changes", "AIFMD", "SFDR", "FCA rules", "fund compliance", "ASC 820", or "accounting standards for PE". Collects regulatory actions, compliance deadlines, and operational/technology developments relevant to PE and credit fund CFOs.
---

# Regulatory & Operational Intelligence

Collect regulatory actions, compliance deadlines, fund administration news, and PE technology developments. Report only confirmed facts with sources and deadlines.

## CRITICAL: Search Efficiency Rules

**Budget: 5 web searches maximum** for this entire skill.

- **DO NOT** search for each regulator separately (SEC, CFTC, FCA, ESMA)
- **DO NOT** search for individual vendor/technology companies one by one
- **DO** use broad searches that return multiple regulatory and industry items per query
- Only report what searches actually return — do not go hunting for stories

### Recommended Search Strategy (5 searches)

1. **Search 1 — SEC/CFTC regulatory actions**: "SEC CFTC private fund rules proposed final rule [date or this week]" → captures proposed rules, final rules, enforcement actions, no-action letters
2. **Search 2 — EU/UK fund regulation**: "AIFMD SFDR FCA private fund regulation [date or this week]" → EU and UK regulatory changes affecting alternative fund managers
3. **Search 3 — Fund admin & PE technology news**: "private equity fund administration technology news [date or this week]" → vendor M&A, platform changes, new products
4. **Search 4 — ILPA, accounting standards, compliance**: "ILPA guidelines accounting standards PE fund compliance [date or this week]" → DDQ updates, ASC 820, audit requirements, GAAP/IFRS changes
5. **Search 5 — PE operational trends**: "PE fund operations cybersecurity insurance outsourcing trends [date or this week]" → only if searches 1-4 suggest something noteworthy; otherwise skip

## What to Collect

### Regulatory Watch

**SEC & CFTC (US)**
- Proposed and final rules affecting PE/credit fund managers
- Comment period openings with deadlines
- Enforcement actions relevant to fund operations (fee disclosures, conflicts, marketing rule)
- No-action letters and staff guidance
- Exam priorities and risk alerts

**EU & UK**
- AIFMD II implementation milestones and deadlines
- SFDR disclosure requirements and level 2 measures
- FCA authorisation and reporting changes
- Cross-border marketing (NPPR) developments
- EU taxonomy and ESG reporting requirements

**Tax & Other**
- Carried interest tax treatment changes
- International tax treaties affecting fund structures
- State-level regulatory changes (blue sky, ESG mandates)
- Transfer pricing rules affecting management companies

**Format per item:**
```
**[Regulator] [Action Type]: [Headline]** — [Description with affected parties, fund size thresholds, effective dates, deadlines, and required CFO actions.] Source: [source].
```

### Operational Intel

**Fund Administration Platforms**
- Allvue, eFront, Burgiss, Investran, iLevel, Juniper Square product changes
- Vendor M&A (consolidation in PE tech stack)
- Migration timelines for platform changes
- New product launches (AI features, reporting tools, data integrations)

**Industry Standards**
- ILPA DDQ template updates
- ILPA reporting guidelines and best practices
- Institutional Limited Partners Association governance changes
- UNPRI reporting framework updates

**Accounting & Audit**
- ASC 820 fair value measurement updates
- GAAP/IFRS changes affecting fund accounting
- Audit quality and inspection results (PCAOB)
- Valuation practice guidance

**Cybersecurity & Insurance**
- Cybersecurity incidents affecting fund services providers
- SEC cybersecurity disclosure requirements
- D&O, cyber, E&O insurance market changes for fund managers
- SOC 2 and other compliance certifications

**Outsourcing & Services**
- NAV calculation outsourcing trends
- Tax compliance service changes
- ESG reporting service providers
- Middle/back-office automation developments

**Format per item:**
```
**[Headline]** — [Description with timeline, affected parties, and what CFOs should do.] Source: [source].
```

## Output Format

Organize into two sections:

### Section 1: Regulatory Watch
- 2-4 items, sorted by urgency (nearest deadlines first)
- If no significant regulatory news: "No significant regulatory developments today."

### Section 2: Operational Intel
- 2-3 items
- If no significant operational news: "No significant operational developments today."

Each item must include:
- Specific deadlines or effective dates when applicable
- Which fund types/sizes are affected
- Actionable guidance — what should a CFO do?
- Source attribution

## Deduplication Rules

- **Regulatory actions with market impact** (e.g., new banking capital rules affecting credit markets) → report here for the regulatory angle, let geopolitical-monitor cover the market reaction
- **Technology news that is purely market data** (e.g., "fintech stock prices") → geopolitical-monitor, not here
- **Upcoming regulatory deadlines** → here (not event-calendar), since context and guidance are needed

## Data Sources

Use web search as primary. Cross-reference with official regulator websites (sec.gov, esma.europa.eu, fca.org.uk) for policy actions. Industry sources: ILPA.org, PEI Media, Institutional Investor, Private Funds CFO.
