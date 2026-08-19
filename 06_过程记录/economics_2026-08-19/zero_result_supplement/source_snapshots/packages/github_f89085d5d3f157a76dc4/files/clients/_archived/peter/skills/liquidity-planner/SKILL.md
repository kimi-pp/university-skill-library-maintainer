---
name: liquidity-planner
version: 1.0.0
description: "Liquidity planning and cash management — emergency reserves, capital preservation, liquidity ladder construction (immediate/short/medium/long-term), liquid vs illiquid asset analysis, and cash flow stress testing. Ensure clients can meet obligations without forced asset sales."
---

# liquidity-planner

Analyze client liquidity position and build a comprehensive cash management plan. Construct a liquidity ladder segmenting assets by time-to-cash, evaluate emergency reserve adequacy, stress test for cash needs under adverse scenarios (job loss, business downturn, market crash, major expense), and recommend optimal cash positioning. Liquidity is the oxygen of financial planning — without it, even wealthy clients face forced sales, missed opportunities, and panic decisions.

## Trigger

- "Liquidity plan"
- "Cash management strategy"
- "Emergency fund analysis"
- "How liquid am I?"
- "Cash reserve planning"
- "Liquidity ladder"
- "Can I afford this without selling?"
- "Business downturn cash planning"
- "Liquidity stress test"
- "Capital preservation strategy"

## Inputs

- **Client profile:** Age, income sources, employment type (W-2/business owner/retired) (required)
- **Assets by type:** Cash, brokerage, retirement, real estate, private investments, business equity (required)
- **Annual expenses:** Fixed vs. discretionary breakdown (required)
- **Liabilities:** Debt balances, monthly payments, maturity dates (required)
- **Income stability:** Predictability of income streams (required)
- **Upcoming cash needs:** Known large expenses in 1-5 year horizon (optional)
- **Concerns:** Specific liquidity risks client is worried about (optional)
- **Business details:** If business owner — revenue stability, AR/AP cycles, credit lines (optional)

## Dependencies

- **financial-data-api** — for current money market/bond yields
- **personal-balance-sheet** — for comprehensive asset inventory

## Step 0: EDGAR Pre-flight (Yield Benchmarks)

```bash
python3 skills/sec-edgar-fetch/scripts/fred_bond_spreads.py --preset rates
```

Use current yields for cash, short-term bonds, and money market to set expected returns on liquidity reserves. Clients need to see that cash isn't "dead money" — it earns yield and serves a structural purpose.

## Methodology

### Step 1: Asset Liquidity Classification

```
Liquidity Ladder — Time-to-Cash Segmentation:

TIER 1: IMMEDIATE (0-7 days, no loss of value)
  Cash, checking, savings accounts
  Money market funds
  T-Bills (if held directly, sell same-day)
  Brokerage cash sweep
  Yield: Current money market rate (~4.0-5.0%)

TIER 2: SHORT-TERM (1-4 weeks, minimal friction/cost)
  Brokerage stocks/ETFs (T+1 settlement)
  Mutual funds (1-day redemption)
  CDs (early withdrawal penalty, typically 3-6 months interest)
  I-Bonds (after 1-year hold, 3-month interest penalty)
  Yield: Varies by investment

TIER 3: MEDIUM-TERM (1-6 months, moderate friction)
  Bond funds/individual bonds (may sell at loss if rates rose)
  Structured notes (may have liquidity windows)
  Tax-advantaged accounts (penalty + tax for early withdrawal)
  Home equity (HELOC draw, if pre-established)
  Yield: Bond/balanced returns

TIER 4: LONG-TERM / ILLIQUID (6+ months or restricted)
  Real estate equity (sale takes 3-6+ months)
  Private equity/venture capital (lock-up periods, typically 7-10 years)
  Business equity (valuation + sale process)
  Restricted stock/RSUs (vesting schedule)
  Annuities (surrender charges, typically 5-7 years)
  Collectibles, art, etc.
  Yield: Illiquidity premium expected
```

### Step 2: Emergency Reserve Sizing

```
Emergency Reserve Formula:
  Base Reserve = Monthly Essential Expenses × Coverage Months

  Coverage Months by Employment Type:
  ┌──────────────────────┬──────────────┬──────────────────────────────┐
  │ Employment Type       │ Months       │ Rationale                     │
  ├──────────────────────┼──────────────┼──────────────────────────────┤
  │ Dual-income W-2       │ 3-6 months   │ Diversified income, UI eligible│
  │ Single-income W-2     │ 6-9 months   │ Single point of failure        │
  │ Business owner        │ 9-12 months  │ Income volatile, no UI         │
  │ Commission/variable   │ 6-12 months  │ Income unpredictable           │
  │ Retired (pension+SS)  │ 6-12 months  │ Income stable but fixed        │
  │ Retired (portfolio)   │ 12-24 months │ Avoid selling in down markets  │
  │ High-net-worth        │ 12+ months   │ Lifestyle maintenance, no panic│
  └──────────────────────┴──────────────┴──────────────────────────────┘

  Essential Monthly Expenses:
    Housing (mortgage/rent + insurance + tax + utilities): $XX,XXX
    Food & groceries:                                     $X,XXX
    Healthcare (premiums + out-of-pocket):                $X,XXX
    Transportation:                                       $X,XXX
    Insurance (life, disability, umbrella):               $X,XXX
    Minimum debt payments:                                $X,XXX
    Children (school, childcare, essentials):              $X,XXX
    Total Essential Monthly:                              $XX,XXX

  Discretionary (cuttable in emergency):
    Dining out, travel, entertainment, subscriptions:     $X,XXX
    Charitable giving (non-pledged):                      $X,XXX
    Total Discretionary Monthly:                          $X,XXX

  Adjusted Reserve (reduced spending in emergency):
    Emergency Monthly Burn = Essential + (Discretionary × 30%)
```

### Step 3: Liquidity Ratio Analysis

```
Key Liquidity Ratios:
┌─────────────────────────────┬───────────────┬───────────────┬────────┐
│ Ratio                        │ Formula        │ Client Value  │ Target │
├─────────────────────────────┼───────────────┼───────────────┼────────┤
│ Current Ratio                │ Liquid / Annual│ X.Xx          │ >1.0x  │
│                              │ Expenses       │               │        │
│ Quick Ratio                  │ Tier 1 / Mo.  │ X.X months    │ >6 mo  │
│                              │ Essential Exp  │               │        │
│ Liquid Asset Ratio           │ Tier 1+2 /    │ XX.X%         │ >15%   │
│                              │ Total Assets   │               │        │
│ Illiquid Concentration       │ Tier 4 /      │ XX.X%         │ <50%   │
│                              │ Total Assets   │               │        │
│ Debt Service Coverage        │ Net Income /   │ X.Xx          │ >1.5x  │
│                              │ Debt Payments  │               │        │
│ Emergency Coverage           │ Tier 1 /      │ X.X months    │ Varies │
│                              │ Emergency Burn │               │  by type│
└─────────────────────────────┴───────────────┴───────────────┴────────┘
```

### Step 4: Cash Flow Stress Testing

```
Stress Scenarios:
  1. Income Loss — 50% income reduction for 12 months
     Monthly shortfall = Expenses - (Reduced Income after tax)
     Cash burn: $XX,XXX/month × 12 = $XXX,XXX
     Can Tier 1 cover? [Yes/No, for how many months]
     
  2. Market Crash — Portfolio down 30%, no income disruption
     Tier 2 assets (brokerage): Current $XXX,XXX → Stressed $XXX,XXX
     Should NOT sell equities in crash → effectively illiquid
     Available liquidity = Tier 1 only
     
  3. Combined Stress — Income loss + 20% market decline
     Monthly shortfall: $XX,XXX/month
     Available liquid assets (Tier 1): $XXX,XXX
     Months of coverage: XX months
     Forced liquidation point: Month XX (selling at depressed prices)
     
  4. Large Unplanned Expense — $XXX,XXX (medical, legal, property)
     Current Tier 1: $XXX,XXX
     After expense: $XXX,XXX
     Remaining emergency coverage: XX months
     
  5. Business-Specific (if applicable) — Revenue down 40%
     Business cash reserves: $XXX,XXX
     Monthly business burn: $XX,XXX
     Months before personal assets tapped: XX
     Personal + business combined runway: XX months
```

### Step 5: Liquidity Optimization Recommendations

```
Optimization Framework:
  1. Emergency Reserve Target: $XXX,XXX (XX months of essential expenses)
     Current: $XXX,XXX → Gap: $XXX,XXX
     Vehicle: [HYSA at X.XX% / T-Bill ladder / Money market]
     
  2. HELOC Pre-establishment (if homeowner)
     Available equity: $XXX,XXX
     Recommended HELOC: $XXX,XXX (backup liquidity, costs nothing if undrawn)
     Purpose: Backstop — NOT primary emergency fund
     
  3. CD/T-Bill Ladder (for excess cash beyond immediate needs)
     $XXX,XXX in 3-month T-Bills (rolling)
     $XXX,XXX in 6-month CDs
     $XXX,XXX in 12-month CDs
     Blended yield: X.XX% (vs. X.XX% in checking)
     
  4. Illiquid Asset Rebalancing
     Current illiquid concentration: XX%
     Target: <50% of net worth
     Action: [Defer new illiquid commitments / Seek secondary market for PE / etc.]
     
  5. Income Diversification (if concentrated)
     Primary income source: XX% of total
     Risk: Single point of failure
     Options: [Spouse employment, rental income, dividend portfolio, consulting]
```

### Step 6: Opportunity Cost Analysis

```
Cost of Excess Cash:
  Cash above optimal reserve: $XXX,XXX
  Cash yield: X.XX%
  Portfolio expected return: X.XX%
  Opportunity cost: $XXX,XXX × (portfolio return - cash yield) = $XX,XXX/year
  Over 10 years (compounded): $XXX,XXX

Cost of Insufficient Cash:
  Forced equity liquidation in down market:
    Sell $XXX,XXX at −30% = realize $XXX,XXX loss
    Miss recovery = additional $XXX,XXX opportunity cost
    Tax impact of realized gains/losses: ±$XX,XXX
    Total estimated cost of forced sale: $XXX,XXX

  Optimal range: [$ floor] to [$ ceiling] in Tier 1
  Below floor = too much risk of forced sales
  Above ceiling = too much opportunity cost drag
```

## Output Format

```
💧 Liquidity Plan — [Client Name/Description]
Age: [XX] | Employment: [Type] | Annual Expenses: $[XXX,XXX]
Net Worth: $[X,XXX,XXX] | Liquid Assets: $[X,XXX,XXX] ([XX]% of NW)

━━━ LIQUIDITY LADDER ━━━
| Tier | Category | Assets | Value | % of NW | Yield |
|------|----------|--------|-------|---------|-------|
| 1 — Immediate | Cash, HYSA, MM | [list] | $XXX,XXX | XX% | X.X% |
| 2 — Short-term | Brokerage, CDs | [list] | $XXX,XXX | XX% | X.X% |
| 3 — Medium-term | Bonds, HELOC | [list] | $XXX,XXX | XX% | X.X% |
| 4 — Illiquid | RE, PE, Business | [list] | $X,XXX,XXX | XX% | — |
| **Total** | | | **$X,XXX,XXX** | **100%** | |

━━━ EMERGENCY RESERVE ASSESSMENT ━━━
| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Essential Monthly Expenses | $XX,XXX | — | — |
| Emergency Monthly Burn | $XX,XXX | — | — |
| Tier 1 Reserves | $XXX,XXX | $XXX,XXX | ($XX,XXX) |
| Coverage (months) | X.X mo | XX mo | X.X mo short |
| Reserve Vehicle | [Current] | [Recommended] | — |

━━━ LIQUIDITY RATIOS ━━━
| Ratio | Value | Target | Status |
|-------|-------|--------|--------|
| Current Ratio | X.Xx | >1.0x | 🟢/🔴 |
| Quick Ratio | X.X mo | >6 mo | 🟢/🔴 |
| Liquid Asset Ratio | XX% | >15% | 🟢/🔴 |
| Illiquid Concentration | XX% | <50% | 🟢/🔴 |
| Debt Service Coverage | X.Xx | >1.5x | 🟢/🔴 |

━━━ STRESS TEST RESULTS ━━━
| Scenario | Cash Burn/Mo | Tier 1 Coverage | Action Required? |
|----------|-------------|----------------|-----------------|
| 50% income loss (12 mo) | $XX,XXX | XX months | [Yes/No] |
| Market crash (−30%) | $XX,XXX | XX months | [Yes/No] |
| Combined stress | $XX,XXX | XX months | [Yes/No] |
| Large unplanned ($XXX,XXX) | One-time | Remaining: $XXX,XXX | [Yes/No] |
| [Business-specific] | $XX,XXX | XX months | [Yes/No] |

━━━ RECOMMENDATIONS ━━━
| # | Action | Amount | Vehicle | Priority | Timeline |
|---|--------|--------|---------|----------|----------|
| 1 | [Build/maintain emergency reserve] | $XXX,XXX | HYSA/T-Bills | ⭐⭐⭐ | Immediate |
| 2 | [Establish HELOC backstop] | $XXX,XXX | HELOC | ⭐⭐⭐ | 30 days |
| 3 | [Build CD/T-Bill ladder] | $XXX,XXX | Ladder | ⭐⭐ | 60 days |
| 4 | [Reduce illiquid concentration] | — | Rebalance | ⭐⭐ | 6 months |
| 5 | [Optimize excess cash] | $XXX,XXX | Portfolio | ⭐ | After reserves set |

━━━ OPPORTUNITY COST ANALYSIS ━━━
| Metric | Value |
|--------|-------|
| Excess cash above optimal reserve | $XXX,XXX |
| Annual opportunity cost | $XX,XXX |
| 10-year compounded cost | $XXX,XXX |
| Cost of forced liquidation in crash | $XXX,XXX |
| **Optimal Tier 1 range** | **$XXX,XXX – $XXX,XXX** |

━━━ TRIPLE-THREAT LENS ━━━
🏦 **Banker:** [Credit facility analysis — existing lines of credit, HELOC availability and terms, margin borrowing capacity. Debt service coverage under stress scenarios. Whether client could access bridge financing if needed. Collateral value of liquid assets. Business credit lines if applicable. Quantify total backstop borrowing capacity vs. stress scenario needs.]
📊 **Accountant:** [Tax implications of liquidity events — capital gains tax on forced brokerage sales, early withdrawal penalties on retirement accounts (10% + income tax), CD early termination penalties, wash sale rules if selling and rebuying. Tax-efficient liquidation order: which accounts to tap first to minimize tax drag. Estimated tax cost of each stress scenario's liquidation path.]
💰 **Wealth Manager:** [Strategic liquidity positioning — the client's liquidity profile relative to risk tolerance and life stage. Whether illiquid concentration is appropriate for net worth level. Insurance as liquidity substitute (disability income, business interruption). Behavioral perspective: having adequate liquidity prevents panic selling. Quantify the "sleep at night" premium — what excess cash costs vs. what it prevents. Specific rebalancing actions to improve liquidity without sacrificing long-term returns.]
```

## Quality Gates

- [ ] All assets classified into liquidity tiers with time-to-cash estimates
- [ ] Emergency reserve sized appropriately for employment type and risk profile
- [ ] Liquidity ratios calculated and benchmarked
- [ ] At least 3 stress scenarios modeled with month-by-month cash burn
- [ ] HELOC and credit facilities evaluated as backup liquidity
- [ ] Opportunity cost of excess cash quantified (not just "cash drag")
- [ ] Tax implications of forced liquidation calculated
- [ ] Illiquid asset concentration flagged if >50% of net worth
- [ ] Specific vehicle recommendations with current yields
- [ ] Business-specific liquidity analysis included for business owners
- [ ] Action items prioritized with timeline

## Professional Standards

**What separates A from B work:**
- **A-grade:** Liquidity ladder with actual dollar amounts per tier and current yields. Stress tests with month-by-month cash burn showing exactly when reserves run out. Opportunity cost analysis that quantifies the cost of both too much AND too little cash. Tax-efficient liquidation ordering. HELOC pre-establishment recommendation with specific terms. Business-specific analysis for entrepreneurs separating personal and business liquidity.
- **B-grade:** "Keep 6 months expenses in savings." No tiered analysis. No stress testing. Ignoring illiquid concentration. No tax consequences of forced liquidation. Treating all non-cash assets as equally accessible.

**Common pitfalls:**
- Counting retirement accounts as "liquid" (10% penalty + income tax makes them expensive liquidity)
- Ignoring settlement times (stocks settle T+1, real estate takes months)
- Not pre-establishing HELOC — by the time you need it, you may not qualify
- Confusing net worth with liquidity (a $10M net worth with $5M in real estate and $4M in business equity may have a liquidity crisis)
- Forgetting that brokerage accounts in a crash are effectively illiquid (you shouldn't sell at −30%)
- Not factoring in COBRA/ACA costs when modeling job loss scenarios
- Treating checking account balances as "reserves" when they're just float for next month's expenses

## See Also

- `personal-balance-sheet` — provides asset inventory for liquidity classification
- `wealth-scenario-modeler` — stress scenarios overlap with liquidity stress tests
- `retirement-projector` — retirement-specific withdrawal sequencing
- `risk-tolerance-profiler` — risk capacity affects reserve sizing
- `portfolio-constructor` — allocation affects liquid/illiquid mix
