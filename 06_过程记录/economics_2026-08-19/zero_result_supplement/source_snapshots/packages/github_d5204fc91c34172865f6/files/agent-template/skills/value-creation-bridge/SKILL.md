---
name: value-creation-bridge
version: 2.0.0
description: "Bridge PE entry-to-exit returns into component drivers: revenue growth, margin expansion, multiple expansion, leverage paydown, FCF generation, and dividend recaps. Full attribution with benchmarking."
---

# value-creation-bridge

Build a comprehensive value creation attribution from scratch. This is the definitive post-investment return decomposition deliverable — whether you're analyzing a realized exit, marking an unrealized portfolio company, or benchmarking your value creation playbook against industry norms. A proper value creation bridge answers one question: **what specifically drove the returns, and which levers were skill vs. market?**

## Trigger

- "Value creation bridge for [DEAL]"
- "Return attribution for [COMPANY]"
- "What drove returns on [DEAL]?"
- "Entry to exit bridge"
- "MOIC decomposition"
- "IRR attribution"
- "PE return drivers"
- "Value bridge for [FUND] portfolio"

## Inputs

- **Deal:** company/deal name (required)
- **Entry data:** entry date, EV, equity, EBITDA, revenue, margins, debt, multiple (required)
- **Exit data:** exit date, EV, equity, EBITDA, revenue, margins, debt, multiple (required for realized)
- **Current data:** current financials for unrealized marks
- **Cash flows:** dividends, management fees, add-on investments during hold
- **Components:** growth / margin / multiple / leverage / FCF / all (default: all)

## Dependencies

- **financial-data-api** — data source stack (see `../financial-data-api/SKILL.md`)
- **sec-edgar-fetch** — for public company financials (see `../sec-edgar-fetch/SKILL.md`)

## ⚠️ DATA SOURCING MANDATE (NON-NEGOTIABLE)

**This hierarchy is MANDATORY. Violations = automatic grade downgrade.**

1. **SEC EDGAR XBRL (PRIMARY for public company financials at entry/exit):**
   - `web_fetch("https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK_PADDED_10}.json")` with header `User-Agent: Klade AI arjun@kladeai.com`
   - Extract: revenue, EBITDA components, total debt, cash, shares outstanding
   - Pull exact entry/exit period financials from historical XBRL filings
   - **If EDGAR has the number, you MUST use it.**

2. **Massive.com API (PRIMARY for market multiples and prices):**
   - `web_fetch("https://api.massive.com/v2/aggs/ticker/{TICKER}/prev?apiKey=${MASSIVE_API_KEY}")` for current/exit market values
   - Historical prices for entry/exit benchmarking

3. **FRED API (PRIMARY for macro context):**
   - `web_fetch("https://api.stlouisfed.org/fred/series/observations?series_id={ID}&api_key=${FRED_API_KEY}&file_type=json&limit=1&sort_order=desc")`
   - DGS10 (risk-free rates at entry vs exit — rate environment affects multiple expansion)
   - GDP growth during hold period for organic vs market-driven growth decomposition

4. **web_search (SUPPLEMENTARY ONLY):**
   - Use for: sector median multiples at entry/exit, comparable deal returns, PE benchmark data (Cambridge Associates, Bain PE report)
   - NEVER use for data that exists in EDGAR or FRED

## Methodology

### Step 0: EDGAR Data Pull (MANDATORY)
Before any web_search, run the EDGAR XBRL extraction for the target company:
```bash
python3 skills/sec-edgar-fetch/scripts/edgar_xbrl_extract.py TICKER --preset valuation
```
Use the extracted `summary` and `data` fields as PRIMARY source for all financial metrics.
Only use web_search for data NOT available in XBRL (analyst estimates, market sentiment, forward guidance, CDS spreads).
Cite all EDGAR-sourced numbers as "Source: SEC EDGAR XBRL".

### Step 1: Establish Entry and Exit Snapshots

Compile complete financial snapshots at both entry and exit:

| Metric | Entry (Date) | Exit (Date) | Change | CAGR |
|--------|-------------|-----------|--------|------|
| Revenue | $XM | $XM | +XX% | XX% |
| EBITDA | $XM | $XM | +XX% | XX% |
| EBITDA Margin | XX% | XX% | +X pp | — |
| EV | $XM | $XM | +XX% | — |
| EV/EBITDA Multiple | X.Xx | X.Xx | +X.Xx | — |
| Total Debt | $XM | $XM | ($XM) | — |
| Net Debt | $XM | $XM | ($XM) | — |
| Equity Value | $XM | $XM | +XX% | — |
| Equity Invested | $XM | — | — | — |

### Step 2: Calculate Total Returns

**MOIC (Multiple on Invested Capital):**
- Gross MOIC = (Exit Equity + Total Distributions) / Total Equity Invested
- Net MOIC = (Exit Equity + Total Distributions - Carry - Fees) / LP Capital Invested

**IRR (Internal Rate of Return):**
- Build cash flow schedule: initial investment (negative), interim distributions (positive), exit proceeds (positive)
- Calculate IRR using exact dates (not just entry/exit)
- If interim add-on investments, include as additional negatives

**Cash flow timeline:**
| Date | Cash Flow | Description |
|------|----------|-------------|
| [entry date] | ($XM) | Initial equity investment |
| [date] | ($XM) | Add-on equity (if any) |
| [date] | $XM | Dividend recap |
| [date] | $XM | Management fee return |
| [exit date] | $XM | Exit equity proceeds |

### Step 3: Decompose Value Creation Components

**The five levers of PE value creation:**

#### 3a: Revenue Growth Contribution
- Revenue CAGR during hold period
- Organic vs acquisition-driven growth (separate add-ons)
- **Contribution to MOIC** = (Exit Revenue - Entry Revenue) × Entry Margin × Entry Multiple / Entry Equity

#### 3b: Margin Expansion Contribution
- EBITDA margin change (basis points)
- Sources: pricing power, cost optimization, procurement savings, operating leverage, SG&A reduction
- **Contribution to MOIC** = Exit Revenue × (Exit Margin - Entry Margin) × Entry Multiple / Entry Equity

#### 3c: Multiple Expansion/Contraction
- EV/EBITDA multiple change
- Distinguish: market-driven (sector re-rating) vs company-specific (quality improvement, growth acceleration, platform premium)
- **Contribution to MOIC** = Exit EBITDA × (Exit Multiple - Entry Multiple) / Entry Equity

#### 3d: Leverage/Deleveraging Contribution
- Net debt reduction during hold
- Sources: mandatory amortization, voluntary prepayment from FCF, refinancing gains
- **Contribution to MOIC** = (Entry Net Debt - Exit Net Debt) / Entry Equity

#### 3e: FCF / Cash Generation
- Cumulative free cash flow during hold period
- Dividends and distributions paid to equity
- Cash flow used for debt paydown (captured in leverage contribution)
- **Contribution to MOIC** = Total Distributions During Hold / Entry Equity

### Step 4: Attribution Reconciliation

The components MUST sum to total MOIC. Use the multiplicative decomposition for precision:

**Additive decomposition (approximate but intuitive):**
| Component | Contribution ($M) | Contribution to MOIC | % of Total |
|-----------|-------------------|---------------------|------------|
| Revenue Growth | $XM | X.Xx | XX% |
| Margin Expansion | $XM | X.Xx | XX% |
| Multiple Expansion | $XM | X.Xx | XX% |
| Deleveraging | $XM | X.Xx | XX% |
| Distributions | $XM | X.Xx | XX% |
| **Cross-effects** | $XM | X.Xx | XX% |
| **= Total Value Created** | $XM | X.Xx | 100% |

**Note on cross-effects:** When revenue grows AND margin expands AND multiple expands simultaneously, there are interaction terms. Attribute cross-effects proportionally or note them explicitly.

### Step 5: Benchmark Against Industry

Compare value creation mix to industry benchmarks:
```
web_search("PE value creation attribution benchmark 2024 Bain McKinsey")
web_search("[SECTOR] PE returns decomposition revenue margin multiple")
```

**Typical PE value creation mix (historical averages):**
| Component | Industry Avg | This Deal | Assessment |
|-----------|-------------|-----------|------------|
| Revenue Growth | ~30-35% | XX% | Skill vs market |
| Margin Expansion | ~15-20% | XX% | Operational improvement |
| Multiple Expansion | ~25-30% | XX% | Market timing |
| Leverage/Deleveraging | ~15-20% | XX% | Financial engineering |

**Skill vs. luck assessment:**
- Revenue growth: Was it organic or M&A? Above or below sector growth?
- Margin: Was it sustainable operational improvement or one-time cuts?
- Multiple: Was it sector-wide re-rating or company-specific quality improvement?
- Leverage: Was debt paydown from FCF discipline or just mandatory amortization?

### Step 6: Lessons & Repeatability Assessment

For each component:
- Was the value creation lever identified in the original investment thesis?
- Was it executed as planned, or was it opportunistic/accidental?
- Is the playbook repeatable for future deals?
- What would you do differently?

### Step 7: Cross-Deal Comparison (Portfolio Level)

If analyzing multiple deals, compare value creation patterns:
| Deal | MOIC | IRR | Growth % | Margin % | Multiple % | Leverage % |
|------|------|-----|----------|----------|-----------|-----------|

Identify fund-level patterns: do we consistently create value through operations (growth + margin) or financial engineering (multiple + leverage)?

## Output Format

```
🔄 Value Creation Bridge — [Company]
Prepared: [Date] | All figures in $M unless noted
Sources: SEC EDGAR, management reporting, Massive.com, FRED

━━━ EXECUTIVE SUMMARY ━━━
[2-3 sentence return thesis: what drove the return? Was it primarily operational or financial engineering? How does it compare to fund/industry norms?]

━━━ DEAL OVERVIEW ━━━
Entry Date: [date] | Exit Date: [date] | Hold Period: [X.X] years
Entry EV: $[XXX]M | Exit EV: $[XXX]M | EV Growth: +XX%
Equity Invested: $[XX]M | Exit Equity: $[XXX]M
Gross MOIC: [X.X]x | Gross IRR: [XX]%
Net MOIC: [X.X]x | Net IRR: [XX]%

━━━ FINANCIAL SNAPSHOT ━━━
| Metric           | Entry      | Exit       | Δ Change   | CAGR    |
|-----------------|-----------|-----------|-----------|---------|
| Revenue          | $[XXX]M   | $[XXX]M   | +$[XX]M   | [XX]%   |
| EBITDA           | $[XX]M    | $[XX]M    | +$[XX]M   | [XX]%   |
| EBITDA Margin    | [XX.X]%   | [XX.X]%   | +[X.X] pp | —       |
| EV/EBITDA        | [X.X]x    | [X.X]x    | +[X.X]x   | —       |
| Total Debt       | $[XXX]M   | $[XX]M    | -$[XX]M   | —       |
| Net Debt         | $[XXX]M   | $[XX]M    | -$[XX]M   | —       |
| Net Debt/EBITDA  | [X.X]x    | [X.X]x    | -[X.X]x   | —       |

━━━ VALUE CREATION BRIDGE ━━━
| Component          | Entry   | Exit    | Value ($M) | MOIC Contrib. | % of Total |
|-------------------|---------|---------|-----------|---------------|------------|
| Revenue Growth     | $[XXX]M | $[XXX]M | $[XX]M    | [X.Xx]        | [XX]%      |
| Margin Expansion   | [XX]%   | [XX]%   | $[XX]M    | [X.Xx]        | [XX]%      |
| Multiple Expansion | [X.X]x  | [X.X]x  | $[XX]M    | [X.Xx]        | [XX]%      |
| Deleveraging       | [X.X]x  | [X.X]x  | $[XX]M    | [X.Xx]        | [XX]%      |
| Distributions      | —       | —       | $[XX]M    | [X.Xx]        | [XX]%      |
| Cross-Effects      | —       | —       | $[X]M     | [X.Xx]        | [X]%       |
| = Total            |         |         | $[XXX]M   | [X.Xx]        | 100%       |

━━━ CASH FLOW TIMELINE ━━━
| Date       | Cash Flow | Type              | Cumulative |
|------------|----------|-------------------|-----------|
| [date]     | ($[XX]M) | Initial Investment | ($[XX]M)  |
| [date]     | ($[X]M)  | Add-on Investment  | ($[XX]M)  |
| [date]     | $[X]M    | Dividend Recap     | ($[XX]M)  |
| [date]     | $[XXX]M  | Exit Proceeds      | $[XXX]M   |
| Net P&L    | $[XXX]M  |                   |           |

━━━ BENCHMARK COMPARISON ━━━
| Component          | This Deal | Fund Avg | Industry Avg | Assessment     |
|-------------------|-----------|----------|-------------|----------------|
| Revenue Growth     | [XX]%     | [XX]%    | ~30-35%     | [above/below]  |
| Margin Expansion   | [XX]%     | [XX]%    | ~15-20%     | [above/below]  |
| Multiple Expansion | [XX]%     | [XX]%    | ~25-30%     | [skill/luck]   |
| Deleveraging       | [XX]%     | [XX]%    | ~15-20%     | [above/below]  |

Operational Value Creation (Growth + Margin): [XX]% of total
Financial Engineering (Multiple + Leverage): [XX]% of total
Assessment: [operationally-driven / financially-engineered / balanced]

━━━ ORGANIC VS INORGANIC GROWTH ━━━
Total Revenue Growth: $[XX]M (+XX%)
| Source           | Revenue Add | % of Growth | MOIC Contrib |
|-----------------|------------|-------------|-------------|
| Organic Growth   | $[XX]M     | [XX]%       | [X.Xx]      |
| Add-on Acq. #1  | $[X]M      | [XX]%       | [X.Xx]      |
| Add-on Acq. #2  | $[X]M      | [XX]%       | [X.Xx]      |
| Pricing/Mix      | $[X]M      | [XX]%       | [X.Xx]      |

━━━ SKILL VS MARKET ASSESSMENT ━━━
| Lever               | Company-Specific | Market/Sector | Assessment |
|---------------------|-----------------|---------------|-----------|
| Revenue growth       | +XX% (vs sector +XX%) | +XX% | [skill/market] |
| Margin improvement   | +X pp           | Sector flat   | [skill]   |
| Multiple expansion   | +X.Xx           | Sector +X.Xx  | [market]  |
| Rate environment     | Entry: X.XX%    | Exit: X.XX%   | [tailwind/headwind] |

━━━ LESSONS LEARNED ━━━
✅ What worked: [specific operational initiatives that drove value]
⚠️ What didn't: [initiatives that underperformed or failed]
🔄 Repeatable playbook: [which levers can be applied to future deals]
💡 Key insight: [the most important takeaway from this investment]

━━━ TRIPLE-THREAT LENS ━━━
🏦 Banker: [Deal structuring retrospective — was the capital structure optimal? Could a different debt/equity mix have improved returns? Was the exit process well-run (auction vs bilateral)? Did dividend recaps appropriately return capital? Would continuation fund or secondary have been better?]
📊 Accountant: [Quality of earnings perspective — were EBITDA adjustments at entry/exit consistent? How much of "margin expansion" was real operational improvement vs add-back reclassification? Working capital normalization? Tax structure optimization contribution to returns?]
💰 Wealth Manager: [LP perspective — how does this deal's return compare to public market alternatives over the same period (PME)? What was the actual DPI trajectory? How does the risk-adjusted return look? Would the LP have been better off in the S&P 500 over this hold period?]

━━━ SOURCES ━━━
[List every data source with filing reference, API endpoint, or URL]
```

## Quality Gates

- [ ] Entry and exit financial snapshots verified against EDGAR/management data
- [ ] MOIC calculation: (exit equity + distributions) / invested equity = stated MOIC
- [ ] IRR uses exact cash flow dates (not simplified annual periods)
- [ ] Value creation components sum to total return (reconciliation check)
- [ ] Cross-effects quantified and attributed (not ignored)
- [ ] Organic vs inorganic growth separated for add-on acquisitions
- [ ] Multiple expansion decomposed into market-driven vs company-specific
- [ ] Benchmark comparison uses contemporaneous industry data (not stale averages)
- [ ] Skill vs market assessment uses sector performance during same hold period
- [ ] Distributions and interim cash flows included in IRR calculation
- [ ] Lessons learned are specific and actionable (not generic)
- [ ] Every number has a source citation

## Professional Standards

**What separates A from B:**
- **A-grade:** Components sum to total return with explicit cross-effect attribution. Organic vs inorganic growth separated. Multiple expansion decomposed into market vs company-specific drivers using sector benchmark at entry and exit. Cash flow timeline uses exact dates for precise IRR. Skill vs market assessment compares company performance to sector peers during same period. Lessons learned are specific enough to inform future deal underwriting.
- **B-grade:** MOIC and IRR correct but components don't reconcile. No organic/inorganic split. Multiple expansion attributed entirely to "market" or entirely to "skill" without analysis. No benchmark comparison. Generic lessons learned.

**Common pitfalls:**
- Revenue growth is the most sustainable return driver — if most value came from multiple expansion, acknowledge the market dependence
- Multiple expansion in a declining rate environment is partially luck (lower rates → higher multiples)
- "Margin expansion" from aggressive EBITDA add-backs at exit (but not at entry) is not real value creation
- Ignoring management fees, carry, and fund expenses when presenting "net" returns
- Not adjusting for additional equity invested in add-on acquisitions (increases denominator)
- Treating dividend recaps as "value creation" when they're just capital structure optimization
- Confusing gross MOIC with net MOIC in LP communications
- Not comparing to public market equivalent (PME) — a 2.0x MOIC over 7 years may underperform the S&P 500

## See Also

- `lbo-quick-screen` — LBO return framework and modeling
- `fund-performance` — fund-level return attribution
- `portfolio-company-dashboard` — operational KPI tracking during hold
