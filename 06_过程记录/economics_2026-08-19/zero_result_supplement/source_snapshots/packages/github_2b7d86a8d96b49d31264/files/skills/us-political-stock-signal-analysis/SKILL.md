---
name: us-political-stock-signal-analysis
description: Use when investigating U.S. political stock trade signals, including congressional STOCK Act trades, Trump or executive-branch OGE disclosures, cabinet officials, committee-to-sector overlap, policy-information advantages, Open Cabinet, TrumpTrades, Trump Tracker, Capitol Trades, Quiver, Unusual Whales, House/Senate PTRs, or official disclosure PDFs.
---

# US Political Stock Signal Analysis

Use this skill to research disclosed stock trading by U.S. political figures and evaluate whether the records create a useful market signal. It covers Congress, Donald Trump, executive-branch officials, cabinet nominees/appointees, and other public disclosure sources.

## Operating Rules

- Browse current disclosure and market sources. Filings, committee rosters, OGE records, earnings dates, catalysts, and prices change.
- Start with the user's named source or person. If none is named, choose the source path from the request type.
- Verify high-signal conclusions against primary records when possible: House/Senate PTR PDFs, Senate eFD, OGE PDFs, official committee pages, SEC/company IR, or agency releases.
- Do not call a trade "insider trading", "illegal", or "proof" unless primary legal findings support it. Use "policy-information advantage", "role-sector overlap", "conflict-risk signal", "timing concern", or "requires scrutiny".
- Treat disclosure amounts as ranges. Use midpoint only for aggregate estimates and label it as an estimate.
- Separate active stock or option trades from ETFs, mutual funds, bonds, preferreds, municipal securities, structured notes, RSUs, inheritances, trusts, spouse/child accounts, automatic reinvestment, mandatory divestiture, and broad portfolio rebalancing.

## Source Paths

### Congress

Use for senators, representatives, committees, STOCK Act disclosures, policy-information advantage, multi-member clusters, or CapitolTrades/Quiver/Unusual Whales requests.

1. Capitol Trades: `https://www.capitoltrades.com`
2. Quiver Quant congressional trading: `https://www.quiverquant.com/congresstrading`
3. Unusual Whales politics tools: `https://unusualwhales.com/politics`
4. Primary House Clerk PTR PDFs and Senate eFD records
5. Official committee rosters, hearing calendars, legislation pages, member press releases, agency actions, company IR, SEC filings, and market data

### Trump And Executive Branch

Use for Donald Trump, Trump administration officials, cabinet officials, nominees/appointees, OGE Form 278-T transaction reports, Open Cabinet, TrumpTrades, or Trump Tracker requests.

1. Open Cabinet: `https://open-cabinet.org`
2. TrumpTrades: `https://trumpstrades.com`
3. Trump Tracker: `https://trumptracker.org`
4. Primary OGE public financial disclosure portal and original PDFs
5. Agency budgets/contracts, policy announcements, tariffs/export controls, procurement notices, company IR, SEC filings, and market data

Read `references/source-guide.md` when source-specific navigation or validation cautions are needed.

## Workflow

1. **Define the hunt**
   - Identify person, role, ticker, company, sector/theme, chamber, committee, agency, date range, trade type, and named source.
   - For broad congressional hunts, default to the last 45-90 filing days and include both buys and sells.
   - For broad Trump/administration hunts, default to recent filings and purchases, but include sales if they materially change the interpretation.

2. **Collect transaction records**
   - Capture official/member, role, chamber or agency, party/state when relevant, committee or office, ticker/company, transaction type, trade date, filing date, amount range, owner/account, source URL, and primary report URL.
   - Keep trade date and filing date separate. Trade date measures positioning; filing date measures when the public could have followed.

3. **Validate and normalize**
   - Confirm ticker/company identity, share class, ADR/local listing, and common variants such as `BRK/B` vs `BRK.B` or `TSMC` vs `TSM`.
   - Correct secondary-source purchase/sale or amount-range errors with primary records when available.
   - Flag ETFs/funds, bonds, preferreds, structured notes, RSUs, automatic plans, trusts, spouse/child accounts, nominee holdings, divestitures, inherited positions, and compliance sales.

4. **Map role-to-sector overlap**
   - For Congress, verify committee/subcommittee assignments from official congressional pages and map jurisdiction to the ticker's business, customers, suppliers, regulatory exposure, procurement, or policy catalysts.
   - For executive branch, map the office, agency, cabinet role, nomination, or presidential policy theme to exposed sectors such as defense, energy, nuclear, AI/chips, crypto, space, drones, critical minerals, healthcare, banking, telecom, tariffs, procurement, or antitrust.
   - Do not assume overlap from a title alone. Explain the specific connection.

5. **Build the timing chain**
   - Compare: trade date -> filing date -> public catalyst date -> price reaction.
   - Catalysts can include earnings, customer announcements, grants/contracts, export controls, tariffs, regulation, hearings, budget marks, legislation, FTC/DOJ actions, agency rulemaking, defense procurement, or OGE filing events.
   - If the trade was disclosed after the move, label it as hindsight only. If disclosed before an unresolved catalyst, identify the remaining follow window.

6. **Rank signal quality**
   - Multiple political figures buying or selling the same ticker/sector in a short window is stronger than one isolated trade.
   - A direct committee, agency, or policy-role overlap is stronger than generic market exposure.
   - Active individual stock/options trades, larger amount ranges, repeated behavior, fresh filings, and buys near local lows raise signal quality.
   - Concentrated sells by relevant officials can be more important than buys when policy, earnings, customer, or regulatory risk is approaching.

7. **Report**
   - Lead with the direct conclusion and signal quality: high, medium, low, or weak/no signal.
   - Include a transaction table, role-sector overlap table, catalyst timeline, and caveats when multiple records are involved.
   - If the user asks for trading implications, discuss risk-controlled scenarios, not certainty or blind copy-trading.

## Signal Score

Use this 100-point framework when ranking opportunities.

| Component | Points | What to check |
|---|---:|---|
| Multi-official cluster | 0-20 | Same ticker/sector bought or sold by multiple lawmakers or officials within 30-60 days. |
| Role relevance | 0-25 | Committee, subcommittee, agency, cabinet role, nomination, or policy jurisdiction directly overlaps the ticker's business or catalyst. |
| Timing vs catalyst | 0-20 | Trade before public news, filing before remaining catalyst, or buy near local low before repricing. |
| Transaction quality | 0-15 | Active individual stock/option trade, larger amount range, repeated behavior, not ETF/RSU/automatic. |
| Disclosure freshness | 0-10 | Recently filed and still actionable; late filings are flagged but not ignored. |
| Contrarian sell warning | 0-10 | Relevant officials selling ahead of adverse policy, earnings, customer, or regulatory risk. |

Interpretation:

- 75-100: High-signal cluster. Requires primary-source verification and catalyst follow-up.
- 55-74: Medium signal. Useful watchlist candidate, but needs more confirmation.
- 35-54: Low signal. May be coincidence, generic sector exposure, or stale disclosure.
- Below 35: Weak/no signal. Usually not actionable.

## Committee And Policy Checklist

Verify current jurisdiction before scoring.

- Financial Services / Banking: banks, brokers, payments, fintech, crypto, stablecoins, exchanges, insurance, housing finance, AI in finance.
- Energy & Commerce: telecom, internet platforms, privacy, healthcare, energy markets, data-center power, consumer protection.
- Science, Space, and Technology: AI R&D, semiconductors, NSF/NIST/DOE labs, space, quantum, advanced manufacturing.
- Armed Services / Intelligence: defense primes, drones, space, cybersecurity, satellites, AI for defense, contractors.
- Appropriations / Budget: agencies, procurement, grants, infrastructure spending, defense and energy funding.
- Commerce, Science, and Transportation: telecom, chips, space, autos, aviation, maritime, broadband, data-center infrastructure.
- Judiciary: antitrust, IP, platform regulation, mergers, biotech patents, copyright and AI.
- Energy and Natural Resources / Environment: power, nuclear, utilities, LNG, mining, permitting, critical minerals.
- Agriculture: commodities, food, agtech, crop inputs, CFTC-regulated crypto/derivatives.
- Ways and Means / Finance: taxes, tariffs, healthcare reimbursement, trade, credits/subsidies.
- Executive branch / White House: tariffs, export controls, procurement, antitrust, sanctions, energy permitting, healthcare policy, crypto regulation, industrial policy, national security, and agency budgets.

## Trump And Administration Watchlist

When the user asks for Trump/administration trade themes, use these themes and tickers as search seeds, then verify current disclosures:

- AI: `DELL`, `MU`, `SNDK`, `WDC`
- Chips: `INTC`, `AMD`, `NVDA`, `TSMC`/`TSM`, `ARM`
- Space: `RKLB`, `PL`, `ASTS`
- Crypto: `HOOD`, `CRCL`, `PURR`
- Energy: `BE`, `GEV`, `FCEL`, `TE`
- Drones: `UMAC`, `ONDS`, `AVEX`
- Nuclear: `XE`, `CCJ`, `OKLO`, `UUUU`
- Robotics: `OUST`, `AEVA`
- Quantum: `IONQ`, `QBTS`, `RGTI`, `INFQ`
- Battery: `FLNC`, `AMPX`, `KULR`
- Medical: `OSCR`, `CLOV`
- Optics: `AXTI`, `AAOI`, `LITE`, `CRDO`
- Rare earths: `USAR`, `CRML`, `TMC`
- Manufacturing: `STRL`, `CDNL`
- Critical minerals: `TMQ`, `MP`, `LAC`

Do not assume these tickers were actually purchased in the requested period.

## Output Templates

For a ticker or person:

- Verdict: signal score, strength, and one-sentence reason.
- Transaction table: official/member, role/committee/agency, trade date, filing date, type, amount range, owner/account, source.
- Role-sector overlap: exact committee, office, agency, or policy link and why it matters.
- Catalyst timeline: trade date, filing date, public catalyst, price move, remaining catalyst window.
- Caveats: disclosure lag, range uncertainty, owner/account, secondary-source errors, no proof of illegality.

For a broad hunt:

- Rank tickers by signal score.
- Group by sector and committee/agency/policy theme.
- Separate buy clusters from sell clusters.
- Highlight newly disclosed trades first.
- Separate confirmed trades from watchlist tickers without confirmed purchases.
- List records needing primary PDF verification.

## Common Mistakes

- Treating every political trade as active intent. Many are spouse, child, trust, ETF, RSU, automatic, compliance, or portfolio-rebalancing transactions.
- Ignoring sell clusters. Concentrated selling can warn about adverse policy, contract, regulatory, or earnings risk.
- Ranking by dollar amount alone. A small purchase by a directly relevant committee member or official can matter more than a larger unrelated trade.
- Using only trade date. A trade can be early but publicly disclosed too late for follow-trading.
- Overstating legality. Public disclosures reveal timing and conflicts; they do not prove illegal insider trading by themselves.
