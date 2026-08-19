---
name: weekly-recap
version: 2.0.0
description: "Automated weekly market + portfolio + watchlist summary combining all monitoring skills into a single client-ready weekly report."
---

# weekly-recap

Automated weekly market + portfolio + watchlist summary combining all monitoring skills into a single client-ready weekly report. This is the weekly pulse check that keeps clients, PMs, and team members informed without requiring them to follow markets minute-by-minute. A proper weekly recap **tells the story of the week, connects it to the portfolio, and prepares the reader for what's next.**

## Trigger

- "Weekly recap"
- "Weekly summary"
- "What happened this week?"
- "Weekly market update"
- "Week in review"
- "Friday wrap-up"

## Inputs

- **Period:** last week (auto-detect Monday-Friday, default: most recent completed week)
- **Include:** market / portfolio / watchlist / week-ahead / all (default: all)
- **Audience:** internal team / client-facing / PM-only
- **Portfolio:** specific portfolio or all portfolios
- **Benchmark:** SPX / custom (default: SPX for equity, AGG for FI)
- **Depth:** brief (1 page) / standard (2-3 pages) / detailed (5+ pages)

## Dependencies

- **sector-heatmap** — sector performance data
- **economic-calendar** — macro events and data releases
- **portfolio-tracker** — portfolio performance and holdings
- **alert-engine** — watchlist alerts and triggers
- **earnings-summary** — earnings season coverage
- **financial-data-api** — market data

## ⚠️ DATA SOURCING MANDATE (NON-NEGOTIABLE)

**This hierarchy is MANDATORY. Violations = automatic grade downgrade.**

1. **Massive.com API (PRIMARY for all market prices and returns):**
   - `web_fetch("https://api.massive.com/v2/aggs/ticker/{TICKER}/range/1/day/{monday}/{friday}?apiKey=${MASSIVE_API_KEY}")` for weekly index/sector returns
   - Use for: SPX, NDX, DJIA, RUT, sector ETFs (XLK, XLF, XLE, etc.), VIX, bond yields (proxy ETFs)
   - Calculate weekly return from Monday open to Friday close

2. **FRED API (PRIMARY for rates and macro data):**
   - Treasury yields: DGS2, DGS10, DGS30
   - Fed funds: DFF
   - Credit spreads: BAMLH0A0HYM2 (HY OAS), BAMLC0A0CM (IG OAS)
   - Economic data releases: CPI, NFP, GDP, etc.

3. **Portfolio-tracker (PRIMARY for portfolio performance):**
   - Weekly returns, attribution, position changes
   - Must reconcile to custodian data

4. **web_search (SUPPLEMENTARY ONLY):**
   - Market narrative, policy decisions, geopolitical events
   - Earnings surprises, company-specific news
   - NEVER use for prices or returns

## Methodology

### Step 1: Market Overview

Compile the week's market performance across asset classes:
- **Equity indices:** S&P 500, Nasdaq, DJIA, Russell 2000, international (MSCI EAFE, EM)
- **Sector performance:** all 11 GICS sectors ranked by weekly return
- **Fixed income:** 2Y/10Y/30Y yields, weekly change, curve shape (2s10s spread)
- **Credit:** IG and HY spreads, weekly tightening/widening
- **Commodities:** WTI crude, gold, copper (risk barometer)
- **FX:** DXY, EUR/USD, USD/JPY (carry trade indicator)
- **Volatility:** VIX level and weekly change

### Step 2: Key Events Narrative

Write the story of the week — don't just list data, explain causation:
- **What drove markets this week?** (the 2-3 key themes)
- **Policy events:** Fed/ECB/BOJ decisions, speeches, minutes
- **Economic data:** which releases moved markets, beat/miss vs. consensus
- **Geopolitical:** trade developments, regulatory actions, elections
- **Earnings:** major companies reporting, aggregate beat/miss rates
- **Flow data:** fund flows, positioning data if available

### Step 3: Portfolio Update

Pull from portfolio-tracker for the reporting period:
- **Weekly P&L:** absolute and relative to benchmark
- **MTD and YTD context:** where does this week fit in the bigger picture
- **Top contributors:** 3-5 positions that drove positive performance
- **Top detractors:** 3-5 positions that dragged performance
- **Position changes:** any trades executed during the week with rationale
- **Cash position:** current cash level and any changes

### Step 4: Watchlist Review

From alert-engine and watchlist-manager:
- **Earnings this week:** results for any watchlist companies, beat/miss summary
- **Price alerts triggered:** stocks hitting target/stop levels
- **Filing activity:** material SEC filings for watchlist companies
- **Insider activity:** notable insider buys/sells
- **News events:** significant developments for tracked names
- **Rating changes:** analyst upgrades/downgrades for watchlist companies

### Step 5: Week Ahead Preview

Prepare the reader for the coming week:
- **Economic calendar:** key data releases with consensus estimates and significance
- **Earnings calendar:** major companies reporting with consensus expectations
- **Fed/central bank:** scheduled speakers, meetings, minutes releases
- **Known catalysts:** ex-dividend dates, index rebalances, options expiration
- **Geopolitical:** scheduled events (summits, elections, policy deadlines)

### Step 6: Compile and Format

Structure the final report:
- **Lead with what matters most** — biggest market mover or portfolio event gets top billing
- **Three pages maximum** for standard depth — brevity is professional
- **Consistent formatting** week over week (readers expect familiar structure)
- **Clear section breaks** — reader should be able to scan in 2 minutes

## Output Format

```
📋 Weekly Recap — Week of [Monday Date] to [Friday Date]
Prepared: [Date] | Markets as of [Friday Close Date]

━━━ EXECUTIVE SUMMARY ━━━
[3-4 sentence summary: what drove markets, how portfolio performed,
what to watch next week. This is the TL;DR.]

━━━ MARKET DASHBOARD ━━━
Equities:
| Index      | Close    | Weekly Δ | MTD    | YTD    |
|------------|----------|----------|--------|--------|
| S&P 500    | X,XXX.XX | +X.XX%   | +X.XX% | +X.XX% |
| Nasdaq     | XX,XXX   | +X.XX%   | +X.XX% | +X.XX% |
| DJIA       | XX,XXX   | +X.XX%   | +X.XX% | +X.XX% |
| Russell 2K | X,XXX    | +X.XX%   | +X.XX% | +X.XX% |
| MSCI EAFE  | X,XXX    | +X.XX%   | +X.XX% | +X.XX% |

Rates & Credit:
| Metric     | Level  | Weekly Δ  |
|------------|--------|-----------|
| 2Y UST     | X.XX%  | +/-Xbps   |
| 10Y UST    | X.XX%  | +/-Xbps   |
| 2s10s      | +/-Xbps| +/-Xbps   |
| IG OAS     | XXXbps | +/-Xbps   |
| HY OAS     | XXXbps | +/-Xbps   |
| VIX        | XX.XX  | +/-X.XX   |

Sector Heatmap (weekly):
| Rank | Sector         | Return  |
|------|---------------|---------|
| 1    | [Best]        | +X.XX%  |
| 2    | [Second]      | +X.XX%  |
| ...  | ...           | ...     |
| 10   | [Tenth]       | -X.XX%  |
| 11   | [Worst]       | -X.XX%  |

Commodities & FX:
| Asset    | Level    | Weekly Δ |
|----------|----------|----------|
| WTI      | $XXX.XX  | +X.XX%   |
| Gold     | $X,XXX   | +X.XX%   |
| DXY      | XXX.XX   | +X.XX%   |

━━━ THE WEEK'S STORY ━━━
[2-4 paragraphs: narrative of what happened and WHY. Not a data dump —
connect events to market moves. What were the 2-3 themes that defined
this week? How do they connect to the bigger picture?]

━━━ PORTFOLIO UPDATE ━━━
| Metric            | This Week | MTD    | YTD    |
|-------------------|-----------|--------|--------|
| Portfolio Return  | +X.XX%    | +X.XX% | +X.XX% |
| Benchmark Return  | +X.XX%    | +X.XX% | +X.XX% |
| Alpha             | +X.XX%    | +X.XX% | +X.XX% |

Top Contributors:
| Position   | Weight | Return  | Contribution | Driver |
|------------|--------|---------|-------------|--------|
| [Name]     | X.X%   | +XX.X%  | +X.XX%      | [Why]  |

Top Detractors:
| Position   | Weight | Return  | Contribution | Driver |
|------------|--------|---------|-------------|--------|
| [Name]     | X.X%   | -XX.X%  | -X.XX%      | [Why]  |

Trades This Week:
- [ADDED/INCREASED]: [Position] — [Rationale]
- [TRIMMED/SOLD]: [Position] — [Rationale]

━━━ WATCHLIST ALERTS ━━━
Earnings Results:
| Ticker | Revenue vs Est | EPS vs Est | Guidance | Stock Reaction |
|--------|---------------|------------|----------|----------------|
| [TICK]  | Beat/Miss $XM | Beat/Miss  | Raised   | +X.X%          |

Notable Events:
- [TICKER]: [Material development — filing, insider activity, analyst action]

━━━ WEEK AHEAD ━━━
Economic Calendar:
| Day  | Event            | Consensus | Prior   | Significance |
|------|-----------------|-----------|---------|-------------|
| Mon  | [Release]       | X.X%      | X.X%    | High/Med/Low |
| Wed  | [Release]       | X.X%      | X.X%    | High/Med/Low |
| Fri  | [Release]       | XXXk      | XXXk    | High/Med/Low |

Earnings Calendar:
| Day  | Company  | EPS Est | Rev Est  |
|------|---------|---------|----------|
| Tue  | [Name]  | $X.XX   | $X.XXB   |
| Thu  | [Name]  | $X.XX   | $X.XXB   |

Other Events:
- [Fed speaker / policy event / geopolitical event]

━━━ TRIPLE-THREAT LENS ━━━
🏦 Banker: [Deal flow implications — are markets receptive to new issuance?
M&A conditions (spreads, multiples, financing availability)? IPO window
open or closed? What sectors are seeing the most transaction activity?]

📊 Accountant: [Earnings season quality — are companies beating on real
growth or financial engineering? Working capital trends across reporting
companies? Any accounting red flags in this week's filings? Tax policy
developments affecting effective rates?]

💰 Wealth Manager: [Client communication angle — what should advisors
proactively tell clients this week? Any rebalancing triggers hit?
Tax-loss harvesting opportunities after this week's moves? Is the
risk environment changing in a way that affects asset allocation?]

━━━ SOURCES ━━━
[Market data: Massive.com | Rates: FRED | Portfolio: [custodian] | News: [sources]]
```

## Quality Gates

- [ ] All market data current through Friday close (no stale Thursday data)
- [ ] Weekly returns calculated correctly (Monday open to Friday close, or close-to-close)
- [ ] Portfolio data reconciled to custodian/source system
- [ ] Watchlist coverage comprehensive (no missed earnings or material events)
- [ ] Week-ahead calendar verified against multiple sources (no missed events)
- [ ] Narrative tells a story (not just lists data points)
- [ ] Three pages maximum for standard depth (discipline, not padding)
- [ ] Consistent formatting with prior weeks (readers expect the same structure)
- [ ] Sector performance uses actual ETF/index data (not approximations)
- [ ] Credit spreads from FRED (not approximated from web search)
- [ ] Triple-threat lens provides actionable insights (not generic observations)
- [ ] Report delivered by Saturday morning (timeliness = relevance)

## Professional Standards

**What separates A from B:**
- **A-grade:** Recap tells the story of the week in a compelling narrative. Market moves connected to causes (not just "stocks rose"). Portfolio attribution explains WHY positions contributed/detracted. Week-ahead identifies specific catalysts with consensus estimates. Consistent formatting makes it easy to compare week-over-week. Delivered before the weekend.
- **B-grade:** Data dump without narrative. Sector performance listed without context. Portfolio return stated without attribution. Week-ahead is a calendar copy-paste without significance ratings. Inconsistent formatting. Delivered Monday (when it's already stale).

**Common pitfalls:**
- Writing a market recap instead of a portfolio-relevant recap (everything should connect to positions)
- Including too many data points without prioritization (everything is important = nothing is important)
- Generic narrative ("markets were volatile amid mixed economic data") instead of specific causation
- Missing Friday afternoon developments (report pulled from Thursday's data)
- Not connecting this week's events to the portfolio's positioning thesis
- Week-ahead that lists events without indicating which ones actually matter for the portfolio
- Inconsistent week-over-week formatting (readers lose trust when the format keeps changing)

## See Also

- `morning-brief` — daily version of market summary
- `portfolio-tracker` — portfolio data source
- `watchlist-manager` — watchlist configuration
- `sector-heatmap` — sector performance data
- `economic-calendar` — macro event calendar
- `quarterly-review` — quarterly deep-dive version
