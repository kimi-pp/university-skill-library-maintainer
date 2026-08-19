---
name: add-on-screening
version: 2.0.0
description: "PE add-on acquisition screening based on platform company criteria. Filter potential bolt-on targets by sector, size, geography, strategic fit, and financial profile with systematic scoring and outreach prioritization."
---

# add-on-screening

Build a comprehensive add-on acquisition target screen from scratch. This is the primary deal sourcing deliverable for any PE buy-and-build strategy — whether you're expanding a platform company's geographic footprint, adding product capabilities, or consolidating a fragmented market. A proper add-on screen answers one question: **which targets best fit the platform's strategy, and which should we approach first?**

## Trigger

- "Add-on targets for [PLATFORM COMPANY]"
- "Bolt-on screening for [COMPANY]"
- "Add-on acquisition list"
- "Find acquisitions for [COMPANY]"
- "Buy-and-build targets"
- "Tuck-in acquisition screen"
- "Roll-up candidates in [SECTOR]"
- "Consolidation targets for [PLATFORM]"

## Inputs

- **Platform company:** name and profile (required)
- **Platform financials:** revenue, EBITDA, margins, capabilities, geography
- **Criteria:** sector, size range, geography, capabilities sought (required)
- **Exclusions:** competitors already screened, PE-owned targets to avoid, size floor/ceiling
- **Budget:** max acquisition EV per target and total add-on capital available
- **Priority:** capability addition / geographic expansion / customer base / revenue synergy / cost synergy

## Dependencies

- **financial-data-api** — data source stack (see `../financial-data-api/SKILL.md`)
- **sec-edgar-fetch** — SEC EDGAR integration for public targets (see `../sec-edgar-fetch/SKILL.md`)

## ⚠️ DATA SOURCING MANDATE (NON-NEGOTIABLE)

**This hierarchy is MANDATORY. Violations = automatic grade downgrade.**

1. **SEC EDGAR XBRL (PRIMARY for public target financials):**
   - `web_fetch("https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK_PADDED_10}.json")` with header `User-Agent: Klade AI arjun@kladeai.com`
   - Extract: revenue, EBITDA, margins, cash, debt, segment data, geographic breakdown
   - Pull subsidiary and segment data for carve-out analysis
   - **If EDGAR has the number, you MUST use it.**

2. **Massive.com API (PRIMARY for public target market data):**
   - `web_fetch("https://api.massive.com/v2/aggs/ticker/{TICKER}/prev?apiKey=${MASSIVE_API_KEY}")` for current market values
   - Use for public company take-private or carve-out valuation benchmarks

3. **FRED API (PRIMARY for macro/industry context):**
   - `web_fetch("https://api.stlouisfed.org/fred/series/observations?series_id={ID}&api_key=${FRED_API_KEY}&file_type=json&limit=1&sort_order=desc")`
   - Industry-specific production/employment indices for sector health
   - DGS10 for acquisition financing cost context

4. **web_search (SUPPLEMENTARY ONLY):**
   - Use for: private company identification, ownership status, recent M&A transactions, industry maps, competitor landscapes
   - Sources: Crunchbase, PitchBook references, industry trade publications, LinkedIn
   - NEVER use for data that exists in EDGAR or FRED

## Methodology

### Step 0: EDGAR Data Pull (MANDATORY)
Before any web_search, run the EDGAR XBRL extraction for the target company:
```bash
python3 skills/sec-edgar-fetch/scripts/edgar_xbrl_extract.py TICKER --preset all
```
Use the extracted `summary` and `data` fields as PRIMARY source for all financial metrics.
Only use web_search for data NOT available in XBRL (analyst estimates, market sentiment, forward guidance, CDS spreads).
Cite all EDGAR-sourced numbers as "Source: SEC EDGAR XBRL".

### Step 1: Define Platform Strategy & Screening Criteria

Document the platform company's strategic priorities for acquisitions:

**Platform Profile:**
| Attribute | Current | Target Post-Add-Ons |
|-----------|---------|-------------------|
| Revenue | $XM | $XM (+XX%) |
| EBITDA | $XM | $XM (+XX%) |
| EBITDA Margin | XX% | XX% (+X pp) |
| Geographic Presence | [regions] | [target regions] |
| Product/Service Lines | [current] | [target additions] |
| Customer Segments | [current] | [target expansion] |
| End Markets | [current] | [diversification targets] |

**Screening Criteria Matrix:**
| Criterion | Required | Preferred | Exclude |
|-----------|----------|-----------|---------|
| Revenue Range | $XM - $XM | $XM - $XM | <$XM or >$XM |
| EBITDA Margin | >X% | >XX% | Negative EBITDA |
| Geography | [specific] | [adjacent] | [incompatible] |
| Sector | [exact match] | [adjacent] | [unrelated] |
| Ownership | Any | Founder/family | [exclude if specified] |
| Growth Rate | >X% | >XX% | Declining revenue |

### Step 2: Source Target Universe

Build a comprehensive target list using multiple channels:

**Public companies:**
- Screen EDGAR by SIC code for companies in target sectors
- Filter by revenue range and geographic presence
- Check for carve-out candidates (divisions of larger companies)

**Private companies:**
```
web_search("[SECTOR] companies [GEOGRAPHY] [SIZE RANGE] revenue")
web_search("[SECTOR] private companies acquisition targets")
web_search("[SECTOR] industry map competitors landscape")
web_search("[PLATFORM COMPETITOR] acquisitions recent") (to see what comps are buying)
```

**Ownership research per target:**
```
web_search("[TARGET COMPANY] ownership founder private equity backed")
web_search("[TARGET COMPANY] revenue employees size")
```

### Step 3: Strategic Fit Scoring

Score each target on a 10-point framework:

| Factor | Weight | Scoring Criteria | Max Points |
|--------|--------|-----------------|-----------|
| **Capability Addition** | 20% | Adds product/service platform lacks | 10 |
| **Customer Overlap** | 15% | Cross-sell opportunity to platform's customers | 10 |
| **Geographic Expansion** | 15% | Opens new markets for platform | 10 |
| **Revenue Synergy** | 15% | Combined offering creates upsell | 10 |
| **Cost Synergy** | 10% | G&A elimination, procurement leverage | 10 |
| **Cultural Compatibility** | 10% | Management quality, retention likelihood | 10 |
| **Market Position** | 10% | #1-3 in niche, defensible position | 10 |
| **Integration Complexity** | 5% | Ease of integration (higher = easier) | 10 |

**Weighted Fit Score** = Σ(Factor Score × Weight) → normalize to 10-point scale

### Step 4: Financial Quick-Screen

For each target, compile financial profile:

| Target | Revenue | Growth | EBITDA | Margin | EV Est. | EV/EBITDA | Owner | Fit Score |
|--------|---------|--------|--------|--------|---------|----------|-------|-----------|

**Financial red flags to screen for:**
- Declining revenue (>2 consecutive years)
- Negative or <10% EBITDA margin (integration burden)
- Customer concentration (>25% from single customer)
- Capex intensity (>15% of revenue = capital-heavy)
- Working capital intensity (inventory/receivables growing faster than revenue)
- Significant contingent liabilities or litigation

**Valuation benchmarks:**
```
web_search("[SECTOR] M&A transaction multiples 2024 2025")
web_search("[SECTOR] bolt-on acquisition EV/EBITDA range")
```

Typical add-on multiples:
| Type | EV/EBITDA Range | Notes |
|------|----------------|-------|
| Small bolt-on (<$5M EBITDA) | 4-7x | Founder-owned, less competitive |
| Mid-size add-on ($5-15M EBITDA) | 6-9x | More competitive, may be brokered |
| Strategic/scale add-on (>$15M EBITDA) | 8-12x | Auction process, PE competition |
| Platform-creating acquisition | 10-15x | Premium for market leadership |

### Step 5: Synergy Estimation

For top-priority targets, estimate synergy potential:

**Revenue Synergies (harder, take longer):**
- Cross-selling platform products to target's customers (and vice versa)
- Combined offering enables new contract types
- Geographic expansion enables new customer access
- Estimated realization: 12-24 months, 30-50% probability of full estimate

**Cost Synergies (more reliable, faster):**
- G&A elimination (back office, finance, HR, IT): typically 3-8% of target revenue
- Procurement savings (combined purchasing power): 1-3%
- Facility consolidation: case-specific
- Estimated realization: 6-12 months, 70-90% probability

**Net synergy impact on deal economics:**
| Synergy Type | Gross Annual | Realization Cost | Net Annual | PV (at X%) |
|-------------|-------------|-----------------|-----------|-----------|

### Step 6: Prioritize & Outreach Recommendations

Rank targets by combination of strategic fit, financial attractiveness, and actionability:

**Priority tiers:**
- **Tier 1 (Act Now):** High fit score, favorable ownership, accretive valuation, low integration risk
- **Tier 2 (Develop):** Good fit but needs relationship building, timing isn't right, or valuation needs work
- **Tier 3 (Monitor):** Interesting longer-term, but not actionable now (PE-owned with hold period, public company not for sale)

**Outreach approach per target:**
| Target | Owner Type | Best Approach | Intermediary | Timeline |
|--------|-----------|--------------|-------------|---------|
| [Target A] | Founder, age 60+ | Direct relationship | Industry advisor | Immediate |
| [Target B] | Family-owned, G2 | Warm intro via [X] | Investment bank | 3-6 months |
| [Target C] | PE-backed | Wait for process | [PE firm] | When fund matures |

## Output Format

```
🎯 Add-On Screening — [Platform Company]
Prepared: [Date] | Platform: $[XX]M Revenue / $[XX]M EBITDA
Sources: EDGAR, web research, industry databases

━━━ EXECUTIVE SUMMARY ━━━
[2-3 sentence summary: how many targets identified, top priorities, estimated total addressable M&A opportunity, and recommended next steps]

━━━ PLATFORM PROFILE & ACQUISITION STRATEGY ━━━
Platform Revenue: $[XX]M | EBITDA: $[XX]M | Margin: [XX]%
Strategy: [buy-and-build thesis — what are we trying to create?]
Target Profile: [sector] | $[X-XX]M revenue | [geography] | [capabilities sought]
Add-On Budget: $[XX]M total | $[X-XX]M per deal | [X-X] acquisitions targeted

━━━ SCREENING CRITERIA ━━━
| Criterion      | Must Have        | Preferred        | Exclude          |
|----------------|-----------------|-----------------|------------------|
| Revenue        | $[X-XX]M         | $[X-XX]M         | <$[X]M           |
| EBITDA Margin  | >[X]%            | >[XX]%           | Negative          |
| Geography      | [required]       | [preferred]      | [excluded]        |
| Sector         | [required]       | [adjacent]       | [unrelated]       |
| Growth         | Stable           | >X%              | Declining 2+ yrs |

━━━ TARGET UNIVERSE ━━━
Total Identified: [N] | After Filters: [N] | Scored: [N]

━━━ PRIORITY TARGETS ━━━
| Rank | Target       | Revenue | Growth | EBITDA Mrg | EV Est. | Fit Score | Owner      | Priority |
|------|-------------|---------|--------|-----------|---------|-----------|-----------|----------|
| 1    | [Target A]  | $[XX]M  | +XX%   | XX%       | $[XX]M  | [X.X]/10  | Founder   | 🔴 HIGH  |
| 2    | [Target B]  | $[XX]M  | +XX%   | XX%       | $[XX]M  | [X.X]/10  | Family    | 🔴 HIGH  |
| 3    | [Target C]  | $[XX]M  | +X%    | XX%       | $[XX]M  | [X.X]/10  | PE-backed | 🟡 MED   |
| 4    | [Target D]  | $[X]M   | +XX%   | XX%       | $[X]M   | [X.X]/10  | Founder   | 🟡 MED   |
| 5    | [Target E]  | $[XX]M  | +X%    | XX%       | $[XX]M  | [X.X]/10  | Public    | 🟢 WATCH |

━━━ TARGET DEEP DIVES (TOP 3) ━━━

📋 [TARGET A] — Fit Score: [X.X]/10 — 🔴 HIGH PRIORITY
Profile: [1-2 sentence description]
Revenue: $[XX]M | Growth: +XX% | EBITDA: $[X]M (XX%) | Est. EV: $[XX]M ([X]x EBITDA)

Strategic Rationale:
• [Why this target fits — capability, customer, geography]
• [Specific synergy opportunity]
• [Market position strength]

| Fit Factor            | Score | Rationale                          |
|-----------------------|-------|-----------------------------------|
| Capability Addition   | [X]   | [specific capability it adds]      |
| Customer Overlap      | [X]   | [cross-sell opportunity]           |
| Geographic Expansion  | [X]   | [new markets opened]              |
| Revenue Synergy       | [X]   | [combined offering potential]      |
| Cost Synergy          | [X]   | [G&A, procurement savings]        |
| Cultural Compatibility| [X]   | [management quality, retention]    |

Synergy Estimate: $[X-X]M annual ($[X]M revenue + $[X]M cost)
Implied EV with Synergies: [X.X]x EBITDA (vs [X.X]x standalone)

Ownership: [details] | Approach: [recommended]
Risks: [integration, key person, customer concentration]

━━━ SYNERGY SUMMARY (ALL TARGETS) ━━━
| Target      | Rev Synergy | Cost Synergy | Total Annual | Realization |
|-----------|------------|-------------|-------------|-------------|
| [Target A]| $[X]M      | $[X]M       | $[X]M       | 12-18 mo    |
| [Target B]| $[X]M      | $[X]M       | $[X]M       | 6-12 mo     |
| Portfolio | $[XX]M     | $[XX]M      | $[XX]M      |             |

━━━ MARKET CONTEXT ━━━
Sector M&A Multiple Range: [X-X]x EBITDA (source)
Recent Comparable Transactions:
| Acquirer  | Target   | EV    | Multiple | Date   |
|-----------|---------|-------|---------|--------|
| [Comp]    | [Target]| $[X]M | [X.X]x  | [date] |

━━━ OUTREACH RECOMMENDATIONS ━━━
| Target     | Owner Type   | Best Approach       | Intermediary    | Timeline    |
|-----------|-------------|--------------------|-----------------|-----------  |
| [Target A]| [Founder]    | [Direct/advisor]    | [Name if known] | [Immediate] |
| [Target B]| [Family]     | [Warm intro]        | [Name]          | [3-6 mo]    |

━━━ TRIPLE-THREAT LENS ━━━
🏦 Banker: [M&A execution perspective — should we run bilateral or auction? Optimal deal structure (cash, stock, earnout)? Acquisition financing options (revolver draw, incremental term loan, equity co-invest from LP)? Stapled financing opportunity? Roll-up valuation arbitrage (buy at 6x, platform trades at 10x)?]
📊 Accountant: [Due diligence focus areas — quality of earnings normalization for private targets (owner comp, personal expenses, one-time items). Purchase price allocation implications (goodwill, intangibles, amortization). Working capital peg negotiation. Tax structure (asset vs stock deal)? 338(h)(10) election considerations?]
💰 Wealth Manager: [Return impact perspective — how do add-ons affect fund-level returns? Buy-and-build strategies can generate 200-300bps of additional IRR through multiple arbitrage. What's the total return attribution from add-ons vs organic growth? Are we creating real value or just financial engineering through consolidation?]

━━━ SOURCES ━━━
[List every data source with filing reference, API endpoint, or URL]
```

## Quality Gates

- [ ] Platform strategy documented with clear acquisition objectives
- [ ] Screening criteria derived from platform gaps (not generic M&A criteria)
- [ ] Target universe from multiple sources (EDGAR, web research, industry databases)
- [ ] Fit scoring uses weighted, systematic framework (not subjective ranking)
- [ ] Financial data from EDGAR for public targets (not estimates)
- [ ] Size appropriate for bolt-on: target revenue typically 10-50% of platform revenue
- [ ] Ownership status verified (PE-backed targets may not be available)
- [ ] Synergy estimates distinguish revenue (harder) from cost (easier) with realization probability
- [ ] Valuation benchmarks from comparable transactions with dates
- [ ] Outreach approach tailored to owner type (founder vs PE vs public)
- [ ] Integration risk assessed per target (not assumed to be easy)
- [ ] Every number has a source citation

## Professional Standards

**What separates A from B:**
- **A-grade:** Fit scoring is systematic and weighted, not subjective. Targets sourced from multiple channels (EDGAR, web, industry, competitive analysis). Synergy estimates separate revenue from cost with realization timelines and probability. Comparable transaction multiples from recent, same-sector deals. Outreach strategy tailored to ownership type with specific intermediary recommendations. Integration risk explicitly assessed.
- **B-grade:** Target list without systematic scoring. "Strategic fit" stated but not quantified. No synergy estimates. Generic approach recommendation. No comparable transaction data.

**Common pitfalls:**
- Screening for add-ons that are too large (transformative acquisitions, not bolt-ons, require different diligence and risk profile)
- Revenue synergies are harder than cost synergies — most PE firms over-estimate revenue synergies by 2-3x
- Cultural fit matters more for small add-ons where integration is intensive and key person risk is high
- Founder-owned targets may prefer PE platform sale over stand-alone (perceived partnership, growth resources)
- PE-backed targets on year 4-5 of hold period are more actionable than year 1-2
- Not tracking competitor acquisition activity (if competitors are buying similar targets, the market is competitive)
- Ignoring anti-trust risk for larger add-ons in concentrated markets
- Assuming the target's reported EBITDA is real — private company EBITDA adjustments can swing ±30%

## See Also

- `lbo-quick-screen` — return analysis for add-on acquisitions
- `due-diligence-checklist` — DD framework for identified targets
- `comps-builder` — valuation benchmarking
- `value-creation-bridge` — return attribution from add-on strategy
