---
name: finance-screen
description: European dividend and stock screener for German investors. Trigger phrases: "screen ETFs for dividends", "which ETFs pay dividends in Germany", "build me a dividend portfolio", "what should I invest in", "DAX dividend stocks", "UCITS ETF screener", "ausschüttende ETFs", "Dividendenstrategie", "European stock screener", "income investing Germany", "find me dividend ETFs", "Depot aufbauen". Collects investment goal, risk tolerance, sector preference, existing holdings, target yield range, distributing vs accumulating preference, and broker. Returns ETF screening results with ISINs and yields, individual stock watchlist, tax efficiency notes, and Freistellungsauftrag allocation recommendation. Output saved as FINANCE-SCREEN.md.
---

# Finance Screen — European Dividend & Stock Screener for German Investors

**DISCLAIMER: For educational and informational purposes only. Not financial advice. Not a recommendation to buy or sell any specific security. Always consult a licensed Finanzberater, Steuerberater, or Anlageberater before making investment decisions. All investments carry risk of loss. Past performance does not guarantee future results.**

---

## When to Run

- User types `/finance screen` or asks to screen ETFs, build a Depot, or find dividend-paying investments
- User asks "what should I invest in?", "welche ETFs zahlen Dividenden?", "Dividendenstrategie aufbauen", "ausschüttende ETFs empfehlen"
- User wants income-generating holdings for their Depot
- User wants to add European dividend exposure to existing positions
- User asks about DAX/MDAX dividend stocks or STOXX 600 income strategies

---

## Data Collection

Before screening, collect the following from the user. Ask for all missing items at once rather than one at a time.

1. **Investment goal** — income/dividend focus now, or total return (growth first, income later)?
2. **Risk tolerance** — conservative / moderate / aggressive (or 1–10 scale)
3. **Preferred sectors** — any sector preferences or exclusions (e.g., no fossil fuels, prefer utilities)?
4. **Already-held positions** — existing Depot holdings to avoid overlap and over-concentration
5. **Target dividend yield range** — e.g., "at least 3%", "3–5%", or "no preference"
6. **Distributing or accumulating preference** — distributing (ausschüttend, income now) vs. accumulating (thesaurierend, reinvest for growth)?
7. **Existing Depot broker** — Trade Republic, Scalable Capital, DKB, ING, Comdirect, Consorsbank, or other

---

## Screening Framework

> Before analysis, read `.claude/skills/shared/german-context.md` for 2026 German financial constants.

### 1. Core Layer: Distributing UCITS ETFs (Recommended First Layer)

Broad, diversified, low-cost distributing ETFs should form the foundation of any dividend-oriented Depot. All ETFs below are UCITS-compliant and EU-domiciled (IE or LU ISIN prefix), ensuring German investor protections and favorable withholding tax treatment via Irish ETF domicile rules.

| ETF Name | Ticker | ISIN | TER | Approx. Yield | Notes |
|---|---|---|---|---|---|
| Vanguard FTSE All-World High Dividend Yield UCITS ETF Dist | VHYL | IE00B8GKDB10 | 0.22% | ~3.5% | Global high-dividend, distributing |
| iShares STOXX Europe 600 UCITS ETF Dist | EXSA | DE0002635307 | 0.20% | ~3–4% | Broad European equities, distributing |
| iShares DJ Euro STOXX Select Dividend 30 UCITS ETF Dist | IDVY | IE0008194725 | 0.31% | ~4–5% | High-dividend Eurozone focus, distributing |
| SPDR S&P Euro Dividend Aristocrats UCITS ETF | EUDI | IE00B5M1WJ87 | 0.30% | ~3–4% | European companies with 10+ years dividend growth |

**Tax note on distributing vs. accumulating:**
- Accumulating ETFs (thesaurierend) are more tax-efficient for long-term growth: only the Vorabpauschale is taxed annually (small amount in low-rate environments), and the 30% Teilfreistellung applies to equity ETF gains
- Distributing ETFs (ausschüttend) generate taxable income each distribution period — use only if income is needed now, or to make use of remaining Freistellungsauftrag capacity
- Irish-domiciled ETFs (IE ISINs): 0% Irish withholding tax on ETF distributions due to Ireland's favorable ETF tax treaties — this is why EU-domiciled UCITS ETFs are preferred over investing in US-listed ETFs or direct foreign individual stocks

---

### 2. Satellite Layer: European Individual Dividend Stocks (DAX / MDAX / STOXX 600)

Individual stocks may be added as a satellite sleeve (typically 10–30% of portfolio) for higher yield or sector tilt. Screen candidates against all criteria below before including.

**DAX dividend payers (examples, not recommendations):**

| Company | Ticker | Sector | Characteristic |
|---|---|---|---|
| Allianz | ALV | Insurance | Large-cap, consistent dividend history |
| Munich Re | MUV2 | Reinsurance | Stable earnings, high yield |
| BASF | BAS | Chemicals | Cyclical; high yield but watch payout ratio |
| Deutsche Post / DHL | DHL | Logistics / Infrastructure | Defensive growth |
| Mercedes-Benz | MBG | Automotive | Cyclical; yield varies with earnings cycle |
| BMW | BMW | Automotive | Cyclical; strong FCF in normal cycles |

**MDAX dividend payers (examples, not recommendations):**

| Company | Ticker | Sector |
|---|---|---|
| Hannover Rück | HNR1 | Reinsurance |
| Fresenius | FRE | Healthcare |
| Hugo Boss | BOSS | Consumer discretionary |

**Individual stock screening criteria — all must be checked:**

| Criterion | Threshold | Notes |
|---|---|---|
| Dividend yield | 2.5–6% | Above 6%: potential yield trap — investigate before including |
| Payout ratio | < 70% for cyclicals; < 90% for utilities/REITs | High payout ratios with cyclical earnings = dividend cut risk |
| Dividend history | 5+ consecutive years without cut preferred | Check investor relations page for history |
| Debt | Net Debt/EBITDA < 3× | Higher leverage acceptable for utilities/infrastructure |
| Sector stability | Utilities, insurance, infrastructure, consumer staples preferred | Avoid pure cyclicals for income strategy |

---

### 3. German and EU Dividend Tax Mechanics

Understanding withholding tax by country of domicile is critical for dividend investors in Germany.

**Domestic dividends / Inländische Dividenden (German stocks — e.g., DAX/MDAX):**
- 25% Kapitalertragsteuer (KapSt) + Solidaritätszuschlag (5.5% of KapSt) withheld automatically by German custodian
- Withheld amount is credited against the investor's Freistellungsauftrag
- No foreign withholding tax complications — simplest for German investors

**Foreign dividends (Ausländische Dividenden) — withholding tax (Quellensteuer) by country:**

| Source Country | Withholding Rate | DBA Treaty Maximum Creditable | Net Effect |
|---|---|---|---|
| France | 12.8% | 15% max creditable | Mostly offset; small residual |
| Netherlands | 15% | 15% (fully creditable via DBA) | Fully offset against German KapSt |
| UK | 0% | 0% (DBA = 0%) | Clean dividend; no withholding |
| USA | 15% | 15% max creditable | Fully creditable — but prefer EU ETFs over US individual stocks |
| Switzerland | 35% | Only 15% reclaimable via DBA; 20% permanently lost | **Avoid Swiss individual stocks for dividend strategy** |
| Ireland (ETF domicile) | 0% | N/A | 0% withholding on ETF distributions — key advantage of UCITS ETFs |

**Anrechnungsverfahren:** German brokers apply DBA treaty rates and credit foreign withholding against German KapSt owed (up to 15%). Withholding above the creditable amount requires filing an Erstattungsantrag directly with the foreign tax authority — a significant administrative burden.

**Practical conclusion:** For dividend income, prioritize:
1. German-listed stocks (no foreign withholding complexity)
2. Irish-domiciled UCITS ETFs (IE ISINs) — 0% Irish withholding, broad diversification
3. Eurozone stocks from Netherlands, France, UK (mostly or fully creditable)
4. Avoid Swiss individual dividend stocks (permanent 20% tax leakage)

---

### 4. Freistellungsauftrag Priority for Dividend Investors

The Sparerpauschbetrag (€1,000 single / €2,000 married/civil partnership in 2026) must be allocated via Freistellungsauftrag across all Depot-holding brokers. Total allocations cannot exceed the Sparerpauschbetrag.

**Allocation priority:**
- **Highest priority:** Distributing ETFs and individual dividend stocks — generate frequent taxable distributions that consume Freistellungsauftrag capacity most rapidly
- **Lower priority:** Accumulating ETFs — only the Vorabpauschale is taxed annually (typically much smaller than the actual distribution amount), so these consume less Freistellungsauftrag per year
- **Tagesgeld / Festgeld accounts:** Interest income also consumes Freistellungsauftrag — factor in alongside investment income

**Tip:** If using multiple brokers (e.g., Trade Republic for ETFs, DKB for cash), split the Freistellungsauftrag in proportion to expected annual income from each.

---

### 5. Yield Trap Warning Signals

Flag any candidate with these signals and investigate thoroughly before including.

| Signal | Risk |
|---|---|
| Dividend yield above 6% | May indicate covered dividend or pending cut; check payout ratio and FCF yield |
| Yield spike driven by falling stock price | Company may be in fundamental trouble, not offering a bargain |
| Dividend cut or freeze in recent 5-year history | Breaks the consistency requirement; investigate reason before including |
| Net Debt/EBITDA above 3× (non-utility) | High debt threatens dividend sustainability in a downturn |
| Payout ratio above 80% for cyclical companies | One bad year can force a cut |

---

## Output

Save results to `FINANCE-SCREEN.md` using this structure:

```markdown
# European Dividend Screen — [Date]

**Investment Goal:** [Income now / Total return / Hybrid]
**Risk Profile:** [Conservative / Moderate / Aggressive]
**Target Yield Range:** [X–Y%]
**Distribution Preference:** [Ausschüttend / Thesaurierend / Mixed]
**Broker:** [Name]

> **DISCLAIMER:** For educational and informational purposes only. Not financial advice. Not a recommendation to buy or sell any specific security. Consult a licensed Finanzberater or Steuerberater before making investment decisions.

---

## ETF Screening Results

| ETF | Ticker | ISIN | TER | Approx. Yield | Domicile | Suggested Weight |
|---|---|---|---|---|---|---|
| [Name] | [Ticker] | [ISIN] | [TER] | [Yield] | [IE/LU/DE] | [X%] |

## Individual Stock Watchlist

| Company | Ticker | Yield | Payout Ratio | Net Debt/EBITDA | Dividend History | Verdict |
|---|---|---|---|---|---|---|
| [Name] | [Ticker] | [X%] | [X%] | [X×] | [X yrs no cut] | [Include / Watch / Exclude] |

## Yield Trap Flags

[List any candidates flagged with reason]

## Tax Efficiency Notes

- [Withholding tax implications for each foreign stock in watchlist]
- [Irish-domiciled ETF advantage summary]
- [Swiss stock exclusions if applicable]

## Freistellungsauftrag Allocation Recommendation

- **Total Sparerpauschbetrag available:** €[1,000 or 2,000] (2026)
- **Estimated annual distributions from recommended ETFs:** €[X]
- **Estimated annual dividends from individual stocks:** €[X]
- **Estimated Vorabpauschale on accumulating ETFs:** €[X]
- **Recommended allocation at [Broker A]:** €[X]
- **Recommended allocation at [Broker B]:** €[X]
- **Priority:** Allocate to distributing ETFs and dividend stocks first

## Portfolio Summary

| Layer | Holdings | Weight | Expected Yield |
|---|---|---|---|
| Core UCITS ETFs | [Names] | [X%] | [X%] |
| Satellite European stocks | [Names] | [X%] | [X%] |
| **Blended portfolio yield** | | **100%** | **[X%]** |

## Rebalancing Rules

- Review annually or when any holding drifts more than 5 percentage points from target weight
- Rebalance with new Sparplan contributions first to minimize taxable events
- Revisit dividend yield figures annually — yields change with stock price movements

## Risks to Understand

1. **Dividend cut risk** — individual stocks can and do cut dividends; diversification via ETFs reduces this
2. **Currency risk** — non-EUR holdings (UK, Switzerland) introduce FX exposure
3. **Concentration risk** — check overlap between ETFs (e.g., VHYL and EXSA share many European large-caps)
4. **Interest rate risk** — high-yield stocks often sensitive to rising rates (utilities, infrastructure)
5. **Behavioral risk** — will you hold through a 30–40% drawdown to collect dividends?

---

**DISCLAIMER:** For educational and informational purposes only. Not financial advice. ISINs and tickers are examples of instruments meeting the screen criteria — equivalent alternatives exist. Always consult a licensed Finanzberater, Steuerberater, or Anlageberater before making investment decisions. Past performance does not guarantee future results. All investments carry risk of loss.
```

---

## Quality Standards

- Every ETF recommendation must include ISIN, TER, approximate yield, and domicile country
- Every individual stock entry must show yield, payout ratio, Net Debt/EBITDA, and dividend history length
- Flag any yield above 6% explicitly as a potential yield trap requiring further investigation
- Always explain the Irish domicile advantage (0% withholding) when recommending UCITS ETFs
- Always warn against Swiss individual stocks for dividend strategies (35% withholding, only 15% reclaimable)
- Freistellungsauftrag section must use the correct 2026 Sparerpauschbetrag values from german-context.md
- Apply 30% Teilfreistellung rule when calculating effective tax on equity ETF gains

---

## Handoff

After delivering FINANCE-SCREEN.md:
- If user wants to model retirement income from dividend portfolio → suggest `/finance retirement`
- If user wants to track net worth including Depot value → suggest `/finance networth`
- If user wants to optimize tax efficiency further (Vorabpauschale, Günstigerprüfung) → suggest `/finance taxes`
- If user wants to set savings/investment goals → suggest `/finance goals`
