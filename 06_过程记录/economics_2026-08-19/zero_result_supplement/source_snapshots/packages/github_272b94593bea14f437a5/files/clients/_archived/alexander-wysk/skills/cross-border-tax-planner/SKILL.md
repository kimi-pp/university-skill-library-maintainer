---
name: cross-border-tax-planner
version: 1.0.0
description: "Cross-border tax planning for clients with multi-jurisdiction assets: treaty analysis, FBAR/FATCA compliance, exit tax planning, foreign tax credits, PFIC rules, totalization agreements. Navigate the intersection of US and foreign tax regimes to minimize global tax burden while maintaining full compliance."
---

# cross-border-tax-planner

Design and execute cross-border tax strategies for HNW clients with assets, income, or residency spanning multiple jurisdictions. Analyze applicable tax treaties, coordinate foreign tax credits, ensure FBAR/FATCA compliance, evaluate PFIC exposure, model exit tax scenarios, and leverage totalization agreements for social security optimization. Cross-border tax planning is not about avoidance — it's about preventing double taxation and structuring holdings so clients pay what they owe, once, to the right jurisdiction, with full compliance.

## Trigger

- "Cross-border tax planning"
- "Foreign tax credit"
- "FBAR filing" / "FATCA reporting"
- "Tax treaty analysis"
- "Exit tax" / "expatriation tax"
- "PFIC rules" / "passive foreign investment"
- "I have assets in another country"
- "Dual citizen tax obligations"
- "Totalization agreement"
- "Foreign trust reporting"
- "Moving abroad tax implications"
- "Repatriation of foreign income"
- "Foreign real estate tax treatment"
- "Green card holder tax obligations"

## Inputs

### Required
- **Client profile:** US person status (citizen, green card holder, substantial presence), filing status, AGI, marginal bracket
- **Foreign jurisdictions:** Countries where client has assets, income, residency, or citizenship
- **Foreign asset inventory:** Bank accounts, investment accounts, real estate, business interests, retirement plans, trusts — by country with estimated values
- **Foreign income:** Types (employment, rental, dividends, capital gains, pensions) and amounts by jurisdiction

### Optional
- **Citizenship/residency history:** Dates of residency changes, citizenship acquisition/renunciation plans
- **Foreign tax paid:** Taxes paid or withheld by foreign jurisdictions (by type and country)
- **Existing treaty elections:** Any treaty positions currently taken (e.g., tie-breaker residence, reduced withholding)
- **Foreign retirement plans:** Pension, superannuation, RRSP, ISA, or equivalent plans by country
- **Business structures abroad:** Foreign corporations, partnerships, disregarded entities
- **Immigration status and timeline:** Visa type, green card application, planned departure
- **Estate plan:** Cross-border estate/gift tax exposure, foreign wills, succession laws
- **Foreign trusts:** Grantor/beneficiary status, reporting history
- **PFIC holdings:** Foreign mutual funds, ETFs domiciled outside US

## Methodology

### Step 1: US Person Classification & Filing Obligations

```
US Person Determination:
  
  US Citizen:
    Worldwide income taxable by US regardless of residence
    Filing required even if living abroad permanently
    FBAR required if foreign accounts > $10,000 aggregate at any point
    FATCA (Form 8938) thresholds:
      US resident: $50,000 (end of year) / $75,000 (any time)
      Foreign resident: $200,000 (end of year) / $300,000 (any time)
      MFJ doubles these thresholds
      
  Green Card Holder:
    Same worldwide taxation as citizen
    Remains US tax person until card formally abandoned (Form I-407)
    ⚠️ Living abroad does NOT end US tax obligations
    
  Substantial Presence Test:
    Present in US ≥ 31 days current year AND
    183-day weighted sum: (current year days) + (1/3 × prior year) + (1/6 × two years prior)
    Exceptions: Closer Connection (Form 8840), treaty tie-breaker
    
  Nonresident Alien:
    Taxed only on US-source income + ECI
    Different withholding rates, treaty benefits available
```

### Step 1b: Common Expat Tax Traps

These are the traps that catch even sophisticated clients and their local advisors. A US-qualified advisor in London may correctly apply UK tax law while being completely unaware of the US consequences. Each trap listed below must be checked against the client's asset inventory.

**Trap 1: UK ISA (Individual Savings Account)**
- **The trap:** UK ISAs are completely tax-free in the UK. US persons assume the same. **Wrong.** The US does not recognize ISA tax-exempt status.
- **US treatment:** All ISA income (interest, dividends, capital gains) is fully taxable to a US person annually.
- **Worse:** ISA funds are almost always UK-domiciled OEICs or unit trusts → **PFICs under US law** → punitive excess distribution regime (effective rates 40-50%+)
- **Double hit:** Taxable income + PFIC penalties + Form 8621 filing for each fund
- **Fix:** Liquidate UK ISA holdings, replace with US-domiciled ETFs. Hold in taxable brokerage account. Accept that ISA tax wrapper is useless for US persons.
- **Estimated annual tax drag vs. UK-only person:** $[X]K on $[X]K ISA balance

**Trap 2: UK Pensions (SIPP/SSAS) — PFIC Exposure**
- **The trap:** UK Self-Invested Personal Pensions (SIPPs) and Small Self-Administered Schemes (SSAS) hold UK-domiciled funds → PFICs
- **US treatment:** Under the US-UK treaty (Article 18), contributions may get tax-favored treatment, BUT the underlying investments are still PFICs unless they're US-domiciled
- **Key nuance:** The treaty exempts the pension trust from US tax — it does NOT exempt the US-person beneficiary from PFIC reporting on the underlying funds
- **QEF election difficulty:** UK pension funds do not provide PFIC Annual Information Statements → QEF election unavailable → stuck with punitive excess distribution or MTM
- **Fix:** Where the pension scheme allows it, switch underlying investments to US-domiciled ETFs within the SIPP. If not possible, make MTM election on publicly traded funds. If funds are not publicly traded → file Form 8621 under excess distribution method.

**Trap 3: Canadian TFSA (Tax-Free Savings Account)**
- **The trap:** Canada's TFSA is tax-free in Canada. US does not recognize it.
- **US treatment:** All TFSA income taxable annually to US persons. The TFSA is treated as a foreign trust under IRC §671-679.
- **Filing burden:** Form 3520 (annual return of foreign trust) + Form 3520-A → penalties of $10,000+ per form per year for non-filing
- **PFIC exposure:** If TFSA holds Canadian mutual funds → PFICs → additional Form 8621
- **The TFSA is NOT covered by the US-Canada treaty** — no treaty relief available
- **Fix:** Liquidate TFSA. Do not contribute further as a US person. The compliance cost alone exceeds the Canadian tax benefit.

**Trap 4: Canadian RRSP/RRIF**
- **Less of a trap (but still complex):** US-Canada treaty (Article XVIII) provides for US tax deferral of RRSP/RRIF income IF the US person makes an annual election on Form 8891 (now automatic under Rev. Proc. 2014-55)
- **The trap that remains:** Underlying Canadian mutual funds in RRSP are still PFICs, but there is a PFIC exemption for "tax-favored retirement trusts" under proposed regulations → most practitioners take the position that RRSP PFICs are exempt from §1291 but Form 8621 filing may still be required
- **Fix:** Maintain RRSP; ensure US return claims treaty deferral. Consider switching underlying to US-domiciled ETFs if plan allows.

**Trap 5: Australian Superannuation**
- **The trap:** Australian super funds are tax-advantaged in Australia (15% concessional rate). US does not have a comprehensive super agreement in the US-Australia treaty.
- **US treatment:** Employer contributions may be taxable income to the US person in the year of contribution (not deductible on US return). Earnings within the fund are likely taxable annually (grantor trust rules).
- **PFIC exposure:** Australian managed funds within super → PFICs
- **Treaty gap:** The US-Australia treaty (Article 18) addresses pensions but the interaction with super's multi-component structure (concessional, non-concessional, earnings) creates ambiguity
- **Fix:** Report conservatively — include employer contributions in income, report earnings annually, file Form 3520/3520-A for the trust. Switch to index ETFs with US-domicile if super fund allows "member direct" investment.

**Trap 6: Foreign Life Insurance / Investment Bonds**
- **The trap:** UK/European investment bonds are common wealth management tools abroad — no annual tax in the jurisdiction, tax on withdrawal only.
- **US treatment:** IRC §7702 — if the policy doesn't meet the US definition of life insurance, the policyholder is taxed currently on inside build-up. Most foreign policies fail §7702 tests.
- **Additional hit:** If classified as a PFIC (foreign insurance company with excess passive income), the punitive regime applies
- **Fix:** Do not purchase foreign investment bonds as a US person. If already owned, model the cost of surrender vs. ongoing reporting burden.

### Step 2: Tax Treaty Analysis

```
Treaty Framework:
  US has income tax treaties with ~65 countries
  
  Key Treaty Provisions to Analyze:
  
  1. Residence Tie-Breaker (Article 4):
     Order: Permanent home → Center of vital interests → Habitual abode → Nationality
     Impact: Determines which country has primary taxing right
     ⚠️ Treaty tie-breaker does NOT change US citizen obligations (saving clause)
     
  2. Business Profits (Article 7):
     Generally taxable only in residence country unless PE in other country
     Permanent Establishment definition: Fixed place of business, 
       agent with contracting authority, construction > 12 months
       
  3. Dividends (Article 10):
     Default US withholding: 30%
     Treaty-reduced rates: Typically 15% (portfolio) / 5% (substantial holding ≥10%)
     Some treaties: 0% for pension funds
     
  4. Interest (Article 11):
     Default US withholding: 30%
     Treaty-reduced: Typically 0-15% depending on treaty
     
  5. Capital Gains (Article 13):
     Real property: Taxable where property is located (FIRPTA for US property)
     Business property/PE: Taxable where PE is
     Other property: Generally residence country only
     
  6. Pensions (Article 18):
     Varies significantly by treaty
     Some treaties: Taxable only in residence country
     Others: Source country retains right (e.g., US Social Security)
     
  7. Saving Clause (Article 1):
     US reserves right to tax its citizens/residents as if treaty did not exist
     Exceptions: Certain pension, social security, diplomatic provisions
     
  Treaty Analysis Template:
    Treaty: US-[Country] | In Force: [Date] | Protocol: [Date]
    | Income Type    | Treaty Rate | Domestic Rate | Savings | Saving Clause? |
    |---------------|-------------|---------------|---------|---------------|
    | Dividends      | XX%         | 30%           | XX%     | [Yes/No]      |
    | Interest       | XX%         | 30%           | XX%     | [Yes/No]      |
    | Royalties      | XX%         | 30%           | XX%     | [Yes/No]      |
    | Capital Gains  | [Rule]      | [Rule]        | [Rule]  | [Yes/No]      |
    | Pensions       | [Rule]      | [Rule]        | [Rule]  | [Yes/No]      |
```

### Step 2b: Treaty Article Reference (Major Treaty Partners)

When citing treaty provisions, always include the specific article number. General statements like "the treaty reduces withholding" are insufficient. Below are the key articles for the 6 most common treaty partners of US expat clients.

**US-UK Treaty (Convention signed July 24, 2001; Protocol signed July 19, 2002):**

| Provision | Article | Key Rule |
|-----------|---------|---------|
| Residence / Tie-breaker | Article 4(1)-(5) | Permanent home → vital interests → habitual abode → nationality → mutual agreement |
| Business Profits / PE | Article 7 | Profits taxable only in residence country unless PE in other; PE defined in Art. 5 |
| Dividends | Article 10(2) | 15% (portfolio); 5% if ≥10% voting stock; 0% for pension funds (Art. 10(3)) |
| Interest | Article 11(2) | 0% withholding (full exemption from source-country tax) |
| Capital Gains | Article 13 | Real property: source country (Art. 13(1)); shares deriving >50% from real property: source (Art. 13(2)); other: residence only (Art. 13(6)) |
| Pensions / Social Security | Article 17 (pensions), Article 18 (Social Security) | Art. 17: Pensions generally taxable only in residence country. Art. 18: Social Security taxable ONLY in residence country |
| Saving Clause | Article 1(4) | US reserves right to tax its citizens as if no treaty — exceptions in Art. 1(5): includes Art. 17 (pensions), Art. 18 (SS) |
| Limitation on Benefits | Article 23 | Comprehensive LOB — check eligibility before claiming treaty benefits |

**US-Canada Treaty (Convention signed September 26, 1980; 5th Protocol 2007):**

| Provision | Article | Key Rule |
|-----------|---------|---------|
| Residence / Tie-breaker | Article IV | Standard tie-breaker; note Paragraph 2 — mutual agreement procedure if individual remains dual |
| Dividends | Article X(2) | 15% (portfolio); 5% if ≥10% voting stock (Art. X(2)(a)); 0% for certain exempt organizations |
| Interest | Article XI(2) | 0% withholding (full exemption per 5th Protocol) |
| Capital Gains | Article XIII | Real property: source country (Art. XIII(1)); substantial interest in corp (>25%): source (Art. XIII(4)) |
| Pensions (RRSP/RRIF) | Article XVIII | Para 1: Pensions generally taxable only in residence country. Para 7: RRSP tax deferral available if electing (now automatic per Rev. Proc. 2014-55) |
| Social Security | Article XVIII(5) | Benefits taxable only in residence country — cross-border SS is fully source-exempt |
| Saving Clause | Article XXIX(2) | Exceptions in Para 3: includes Art. XVIII (pensions), XXV(3) (competent authority) |
| TFSA | **NOT COVERED** | No treaty provision exempts TFSA income — fully taxable + foreign trust reporting |

**US-Australia Treaty (Convention signed August 6, 1982; Protocol 2001):**

| Provision | Article | Key Rule |
|-----------|---------|---------|
| Residence / Tie-breaker | Article 4 | Standard tie-breaker; note dual-resident companies resolved by mutual agreement |
| Dividends | Article 10(2) | 15% (portfolio); 5% if ≥10% voting stock; no pension fund 0% rate |
| Interest | Article 11(2) | 10% withholding (NOT 0% — higher than many treaties) |
| Capital Gains | Article 13 | Real property: source country (Art. 13(1)); business property: per PE rules; other: residence only |
| Pensions / Superannuation | Article 18 | Para 1: Pensions generally residence-only. **Superannuation: treaty coverage is ambiguous** — employer contributions may be taxable in US despite treaty |
| Saving Clause | Article 1(2) | Exceptions: Art. 18 (pensions), Art. 19 (government service) |

**US-France Treaty (Convention signed August 31, 1994; Protocol 2009):**

| Provision | Article | Key Rule |
|-----------|---------|---------|
| Residence / Tie-breaker | Article 4(2) | Standard tie-breaker |
| Dividends | Article 10(2) | 15% (portfolio); 5% if ≥10% voting stock; 0% for pension funds (Art. 10(3)) |
| Interest | Article 11(2) | 0% withholding (full exemption) |
| Capital Gains | Article 13 | Real property: source country; PEA (Plan d'Épargne en Actions): not treaty-exempt for US persons |
| Pensions | Article 18 | Taxable only in residence country; includes French state pension (régime général) |
| Social Security | Article 18(2) | Taxable only in residence country |
| Assurance Vie | **Art. 10 or 11** | French life insurance — US treatment depends on §7702 classification; dividends or interest article may apply to withdrawals |

**US-Germany Treaty (Convention signed August 29, 1989; Protocol 2006):**

| Provision | Article | Key Rule |
|-----------|---------|---------|
| Residence / Tie-breaker | Article 4 | Standard tie-breaker |
| Dividends | Article 10(2) | 15% (portfolio); 5% if ≥10% voting stock; 0% for pension funds |
| Interest | Article 11(2) | 0% withholding |
| Capital Gains | Article 13 | Real property: source country; Riester-Rente / Rürup: pension treatment under Art. 18 |
| Pensions | Article 18A | Private pensions taxable only in residence country |
| Social Security | Article 18(1) | German Rentenversicherung: taxable only in residence country |

**US-Japan Treaty (Convention signed November 6, 2003; Protocol 2013):**

| Provision | Article | Key Rule |
|-----------|---------|---------|
| Residence / Tie-breaker | Article 4 | Standard tie-breaker |
| Dividends | Article 10(2) | 10% (portfolio — higher than most); 5% if ≥10% voting; 0% for pension funds |
| Interest | Article 11(2) | 0% withholding |
| Capital Gains | Article 13 | Real property: source; note Japan exit tax on departure may create double tax — US FTC coordination needed |
| Pensions | Article 17 | Pensions taxable only in residence country |

**Usage Rule:** When recommending a treaty position, ALWAYS cite the specific article and paragraph. Example: "Under Article X(2)(a) of the US-Canada Treaty, withholding on dividends from Canadian Corp to US shareholder is reduced from 25% to 5% based on ≥10% ownership. This position is NOT subject to the Saving Clause per Article XXIX(3)."

### Step 3: Foreign Tax Credit Optimization (Form 1116)

```
FTC Framework:
  
  Purpose: Prevent double taxation by crediting foreign taxes against US liability
  
  Credit vs. Deduction:
    Credit: Dollar-for-dollar offset of US tax (almost always better)
    Deduction: Reduces taxable income (only better if in AMT or very low bracket)
    
  FTC Limitation Formula:
    FTC Limit = US Tax × (Foreign Source Taxable Income / Worldwide Taxable Income)
    
    If foreign tax paid < FTC Limit: Credit all foreign tax, some US tax remains
    If foreign tax paid > FTC Limit: Excess credit carries back 1 year / forward 10 years
    
  Income Category Baskets (must compute separately):
    - General category (most active income, business profits)
    - Passive category (dividends, interest, rents, royalties, capital gains)
    - Section 901(j) (sanctioned countries — no credit)
    - Foreign branch income (separate basket post-TCJA)
    - Global intangible low-taxed income (GILTI)
    - Treaty-resourced income
    
  High-Tax vs. Low-Tax Jurisdiction Planning:
    High-tax country income: Excess credits generated → carry to offset low-tax country
    ⚠️ Cannot cross baskets (passive excess cannot offset general, and vice versa)
    
  FTC Optimization Strategies:
    1. Timing income recognition to maximize basket utilization
    2. Expense allocation (interest, G&A) — directly impacts FTC limit
    3. Treaty-based re-sourcing of income (e.g., US-source income treated as foreign)
    4. Electing to credit vs. deduct on country-by-country basis
    5. Coordination with AMT foreign tax credit (separate computation)
    
  ⚠️ TCJA Changes:
    - Separate basket for foreign branch income
    - GILTI basket (§951A)
    - No carryback for GILTI/branch baskets
```

### Step 3b: FTC Expense Allocation (§861 Allocation)

The FTC limitation depends on "foreign source taxable income" — and deductions must be allocated between US and foreign source income under IRC §861. This allocation directly reduces the FTC limit and is one of the most overlooked areas in cross-border planning. Getting this wrong can cost clients tens of thousands in unusable foreign tax credits.

**The §861 Allocation Concept:**
```
FTC Limit = US Tax × (Foreign Source Taxable Income / Worldwide Taxable Income)

Foreign Source Taxable Income = Foreign Source Gross Income − Allocated Deductions

The MORE deductions allocated to foreign source income, the LOWER the FTC limit,
and the MORE excess credits (which may expire unused).
```

**Deductions That Must Be Allocated:**

| Deduction Type | Allocation Method | Impact on FTC |
|---------------|-------------------|---------------|
| **Interest expense** | Asset-based allocation (§864(e)) — ratio of foreign assets to total assets | HIGH IMPACT — largest allocation item for most clients with mortgages |
| **State/local taxes** | Allocated to the income that generated the tax | Moderate — reduces domestic source income, improving FTC ratio |
| **Investment advisory fees** | Allocated based on income type (domestic vs. foreign portfolio) | Moderate for HNW clients with large advisory fees |
| **Home mortgage interest** | Allocated to ALL income (not just US real estate) based on asset allocation | HIGH IMPACT — mortgage interest allocated to foreign income reduces FTC limit |
| **Charitable contributions** | Generally allocated to income class that generated the deduction | Low to moderate |
| **Standard deduction** | Allocated ratably between US and foreign source income | Fixed — affects every client |
| **CPA/legal fees** | Specific to the income type (foreign trust fees → foreign source) | Low |

**§861 Allocation Example — Interest Expense:**
```
Client has:
  Total assets: $5,000,000
  Foreign assets: $1,500,000 (30%)
  Domestic assets: $3,500,000 (70%)
  Total interest expense (mortgage + margin): $80,000

§864(e) asset-based allocation:
  Interest allocated to foreign source: $80,000 × 30% = $24,000
  Interest allocated to domestic source: $80,000 × 70% = $56,000

Impact on FTC:
  Foreign source gross income: $200,000
  Less allocated interest: ($24,000)
  Foreign source taxable income: $176,000
  
  FTC Limit WITHOUT allocation: US Tax × ($200K / $500K) = 40% of US tax
  FTC Limit WITH allocation: US Tax × ($176K / $476K) = 37% of US tax
  
  Difference: 3% of US tax liability = $[X]K of additional excess FTC (unusable)
```

**Optimization Strategies for §861 Allocation:**

1. **Minimize allocated interest:** Pay down mortgages with domestic assets, concentrate debt on US properties. Foreign-source-reducing allocations are largest for interest.

2. **Asset characterization:** Assets that generate exempt income (tax-exempt bonds) may absorb interest allocation → removing that allocation from the foreign/domestic calculation. §265 interaction.

3. **Timing of asset values:** §861 allocation uses average asset values for the tax year. If possible, increase domestic assets relative to foreign at year-end to reduce the foreign allocation percentage.

4. **Elective allocation methods:** Under Reg. §1.861-9T, taxpayers can elect either fair market value or tax book value for the asset ratio. **Always model both** — FMV may be favorable if foreign real estate has appreciated less than domestic equities.

5. **Separate limitation categories:** Allocations apply separately to each FTC basket. A client with mostly passive foreign income benefits from concentrating deductible expenses against general category income.

**FTC Expense Allocation Worksheet:**

| Deduction | Total Amount | Foreign Allocation % | Allocated to Foreign | Allocated to Domestic | Method |
|-----------|-------------|---------------------|---------------------|---------------------|--------|
| Mortgage interest | $[X] | [X]% (asset ratio) | $[X] | $[X] | §864(e) FMV/Book |
| Investment interest | $[X] | [X]% (income ratio) | $[X] | $[X] | Direct allocation |
| Advisory fees | $[X] | [X]% (portfolio ratio) | $[X] | $[X] | Direct/Apportionment |
| Charitable | $[X] | [X]% (ratable) | $[X] | $[X] | Ratable |
| Standard ded / other | $[X] | [X]% (ratable) | $[X] | $[X] | Ratable |
| **Total Allocated** | **$[X]** | | **$[X]** | **$[X]** | |

**Net Impact on FTC:**
- Foreign source gross income: $[X]
- Less: allocated deductions: ($[X])
- **Foreign source taxable income: $[X]**
- FTC Limit at this level: $[X]
- Foreign tax paid: $[X]
- **Excess FTC: $[X]** → carries forward 10 years (monitor utilization)

### Step 4: FBAR & FATCA Compliance Check

```
FBAR (FinCEN Form 114):
  
  Who: US persons with financial interest/signature authority over foreign accounts
  Threshold: Aggregate balance exceeds $10,000 at ANY point during year
  Due: April 15 (auto-extension to October 15)
  Penalties:
    Non-willful: Up to $12,500 per violation per year
    Willful: Greater of $100,000 or 50% of account balance per violation
    Criminal: Up to $250,000 fine and/or 5 years imprisonment
    
  What Counts as Account:
    ✓ Bank accounts (checking, savings, fixed deposits)
    ✓ Securities/brokerage accounts
    ✓ Mutual funds held at foreign institution
    ✓ Insurance policies with cash value (foreign issuer)
    ✓ Retirement accounts (some exceptions by treaty)
    ✗ Real property (directly held)
    ✗ Tangible personal property
    ✗ Stock in foreign corporation (reported elsewhere)
    
FATCA (Form 8938):
  
  Higher thresholds than FBAR, broader asset scope:
    ✓ All FBAR accounts PLUS
    ✓ Stock/securities in foreign entities (not in US account)
    ✓ Foreign partnership interests
    ✓ Foreign financial instruments/contracts
    ✓ Interest in foreign trust/estate
    
  Thresholds (must file if exceeds):
    | Filing Status  | US Resident    | Foreign Resident |
    |---------------|----------------|-----------------|
    | Single         | $50K/$75K      | $200K/$300K     |
    | MFJ            | $100K/$150K    | $400K/$600K     |
    (end-of-year / any-time-during-year)
    
Additional Reporting Forms:
  Form 3520: Foreign trust transactions, gifts from foreign persons > $100K
  Form 3520-A: Annual return of foreign trust with US owner
  Form 5471: US shareholders of CFCs (≥10% ownership)
  Form 8865: US persons with interests in foreign partnerships
  Form 8621: PFIC annual information statement
  Form 8858: Foreign disregarded entities and foreign branches
```

### Step 5: PFIC Analysis (Passive Foreign Investment Company)

```
PFIC Rules:
  
  Definition: Foreign corporation where:
    Income Test: ≥75% of gross income is passive, OR
    Asset Test: ≥50% of assets produce or are held to produce passive income
    
  Common PFICs (often unexpected):
    - Foreign mutual funds (even broad-market index funds)
    - Foreign ETFs (domiciled outside US)
    - Foreign holding companies with investment portfolios
    - Foreign insurance companies (excess passive income)
    - Foreign REITs (some qualify)
    
  Default PFIC Tax Regime (Excess Distribution):
    "Punitive" regime if no election made:
    1. Gain/excess distribution allocated over holding period
    2. Prior-year amounts taxed at highest rate for that year
    3. Interest charge added (essentially compounding penalty)
    Result: Effective rates often 40-50%+
    
  QEF Election (Qualified Electing Fund):
    - Client includes pro-rata share of PFIC's income annually (even if not distributed)
    - Income taxed at ordinary/capital gains rates (normal rates, no penalty)
    - Requires PFIC to provide annual information statement
    - ⚠️ Most foreign funds will NOT provide QEF statement
    
  Mark-to-Market Election:
    - Recognize gain/loss annually based on FMV change
    - Gains taxed as ordinary income (not capital gains)
    - Losses limited to prior mark-to-market gains
    - Available for PFIC stock regularly traded on qualified exchange
    
  PFIC Mitigation Strategies:
    1. Sell PFIC holdings, replace with US-domiciled equivalents
       (e.g., UK OEIC → US-listed ETF tracking same index)
    2. Make QEF election where information statement available
    3. Make Mark-to-Market election for publicly traded PFICs
    4. Purging election: Treat as sale, restart holding period
    5. For foreign retirement plans: Check treaty exemption (e.g., US-UK treaty)
```

### Step 6: Exit Tax & Expatriation Planning (§877A)

```
Covered Expatriate Determination:
  
  Who: US citizens renouncing or long-term residents (8 of 15 years) abandoning green card
  
  Covered Expatriate if ANY of:
    1. Net worth ≥ $2,000,000 on date of expatriation
    2. Average annual net income tax liability ≥ $201,000 (2025, indexed) for 5 years preceding
    3. Failure to certify 5-year tax compliance on Form 8854
    
  Mark-to-Market Exit Tax:
    All worldwide assets treated as sold at FMV on day before expatriation
    Exclusion: $886,000 (2025, indexed) of gain exempt
    Tax: Net gain above exclusion taxed at applicable capital gains rates
    
  Deferred Compensation:
    Eligible deferred comp (US payer): 30% withholding on payment
    Ineligible deferred comp: Present value included in income at expatriation
    
  Specified Tax Deferred Accounts (IRAs, 401(k)):
    Treated as fully distributed on day before expatriation
    Full balance taxable as ordinary income (early withdrawal penalty may not apply)
    
  Trust Interests:
    Direct/indirect interests trigger special rules
    May require trust to withhold 30% on distributions to covered expatriate
    
  Exit Tax Planning Strategies:
    1. Reduce net worth below $2M threshold before expatriation
       (Gifting to US-person family members, charitable contributions)
    2. Reduce 5-year average tax liability below threshold
       (Timing of income recognition)
    3. Basis step-up planning (harvest losses before expatriation date)
    4. Installment election: Defer exit tax, post adequate security, pay interest
    5. Dual-status year planning: Optimize split-year return
    6. ⚠️ Pre-expatriation gifts: Subject to transfer tax (gift/estate) at 40%
       with NO applicable exclusion amount for US-person recipients
       
  Timeline Considerations:
    Expatriation date = date of renunciation/abandonment
    Form 8854: Due with final US tax return
    Cannot be undone — permanent US tax consequences
```

### Step 7: Totalization Agreement Analysis

```
Social Security Totalization Agreements:
  
  Purpose: Prevent double social security taxation and preserve benefit eligibility
  US has agreements with ~30 countries
  
  Key Principles:
    - Worker pays social security in country of employment (generally)
    - Detached worker rule: Posted abroad ≤5 years → continue home country coverage
    - Totalization of credits: Combine work credits from both countries to qualify for benefits
    
  Coverage Rules:
    | Situation                           | Coverage          | Certificate     |
    |------------------------------------|-------------------|-----------------|
    | Self-employed, US resident          | US only           | N/A             |
    | Employed in foreign country         | Foreign country   | N/A             |
    | Detached worker (≤5 years)          | US only           | Certificate of Coverage |
    | Self-employed, dual residence       | Per agreement     | Varies          |
    | Government employee abroad          | US only           | N/A             |
    
  Benefit Totalization:
    US requires 40 credits (10 years) for retirement benefits
    If client has 30 US credits + 15 foreign credits:
      → Qualifies under totalization (≥6 US credits required)
      → US benefit calculated on US earnings only (pro-rata)
      → Foreign benefit calculated on foreign earnings only
      
  Tax Treatment of Foreign Social Security:
    Some treaties: Foreign social security taxable only by paying country
    Others: US taxes foreign SS (with FTC for any foreign tax)
    FICA exemption: Workers covered under foreign system via totalization
      → Certificate of Coverage exempts from US FICA (save 7.65%/15.3%)
      
  Totalization Savings Analysis:
    | Scenario              | Without Agreement | With Agreement    | Savings        |
    |----------------------|-------------------|-------------------|----------------|
    | FICA on $XXX,XXX     | $XX,XXX           | $0 (exempt)       | $XX,XXX/year   |
    | Foreign SS on same   | $XX,XXX           | $XX,XXX           | —              |
    | Dual SS tax          | $XX,XXX           | $XX,XXX           | $XX,XXX/year   |
    | Benefit qualification| [No/Yes]          | [Yes]             | [Benefit value]|
```

### Step 8: Cross-Border Strategy Integration

```
Global Tax Optimization Framework:
  
  Jurisdiction-by-Jurisdiction Analysis:
  
  | Jurisdiction | Income Type  | Local Tax | US Tax (pre-FTC) | FTC Applied | Net US Tax | Total Tax |
  |-------------|-------------|----------|-----------------|------------|-----------|----------|
  | [Country 1] | Dividends    | $XX,XXX  | $XX,XXX          | $XX,XXX    | $XX,XXX   | $XX,XXX  |
  | [Country 2] | Rental       | $XX,XXX  | $XX,XXX          | $XX,XXX    | $XX,XXX   | $XX,XXX  |
  | US          | Employment   | N/A      | $XX,XXX          | N/A        | $XX,XXX   | $XX,XXX  |
  | **Total**   |              |**$XX,XXX**|**$XX,XXX**      |**$XX,XXX** |**$XX,XXX**|**$XX,XXX**|
  
  Effective Global Tax Rate: XX.X% vs. Domestic-Only Rate: XX.X%
  
  Foreign Earned Income Exclusion (§911) — if applicable:
    Exclusion amount: $130,000 (2025, indexed)
    Housing exclusion: Additional amount (varies by city, IRS-published limits)
    Requirements: Tax home in foreign country + bona fide residence or physical presence test
    ⚠️ Cannot take FTC on excluded income — must choose exclusion vs. credit
    Planning: High-tax country → FTC usually better; Low/no-tax → §911 better
```

## Output Format

```
🌐 Cross-Border Tax Plan — [Client Name]
Status: [US Citizen / Green Card / Substantial Presence] | AGI: $XXX,XXX
Jurisdictions: [Country List] | Filing: [Status] | Bracket: XX%

━━━ FILING OBLIGATIONS ━━━
| Form        | Required | Threshold Met | Deadline    | Penalty Risk       |
|------------|---------|--------------|------------|-------------------|
| 1040        | Yes     | N/A          | April 15   | —                 |
| FBAR (114)  | [Y/N]  | $[X] vs $10K | Oct 15     | Up to $[X]/acct   |
| Form 8938   | [Y/N]  | $[X] vs $[X] | With 1040  | $10K+             |
| Form 5471   | [Y/N]  | [Details]    | With 1040  | $10K/form         |
| Form 8621   | [Y/N]  | [PFIC count] | With 1040  | Loss of election  |
| Form 3520   | [Y/N]  | [Details]    | With 1040  | 35% of amount     |

━━━ TREATY ANALYSIS: US-[COUNTRY] ━━━
| Income Type   | Treaty Rate | Domestic Rate | Annual Savings |
|--------------|-------------|---------------|----------------|
| Dividends     | XX%         | 30%           | $XX,XXX        |
| Interest      | XX%         | 30%           | $XX,XXX        |
| Capital Gains | [Rule]      | [Rule]        | $XX,XXX        |
| Pensions      | [Rule]      | [Rule]        | $XX,XXX        |

━━━ FOREIGN TAX CREDIT ANALYSIS ━━━
| FTC Basket   | Foreign Tax | FTC Limit  | Credit Used | Excess/Shortfall |
|-------------|------------|-----------|------------|-----------------|
| General      | $XX,XXX    | $XX,XXX   | $XX,XXX    | ($XX,XXX)       |
| Passive      | $XX,XXX    | $XX,XXX   | $XX,XXX    | ($XX,XXX)       |
| **Total**    |**$XX,XXX** |**$XX,XXX**|**$XX,XXX** |**($XX,XXX)**    |

━━━ PFIC EXPOSURE ━━━
[List of PFIC holdings with recommended election and tax impact]

━━━ GLOBAL TAX SUMMARY ━━━
| Jurisdiction | Income     | Local Tax  | US Tax     | FTC      | Total Tax  |
|-------------|-----------|-----------|-----------|---------|-----------|
| [Country]   | $XXX,XXX  | $XX,XXX   | $XX,XXX   | ($XX,XXX)| $XX,XXX   |
| US          | $XXX,XXX  | N/A       | $XX,XXX   | N/A      | $XX,XXX   |
| **Total**   |**$XXX,XXX**|**$XX,XXX**|**$XX,XXX**|**($XX,XXX)**|**$XX,XXX**|
| Effective Global Rate: XX.X% |

━━━ TRIPLE-THREAT LENS ━━━
🏦 **Banker:** Global tax liability of $[X]K on $[X]K worldwide income represents a [X.X]% effective rate. FTC optimization recovers $[X]K of double taxation. Key opportunity: [restructuring/treaty/PFIC cleanup] saves an additional $[X]K annually. Exit tax exposure currently $[X]K if client expatriates — recommend [specific mitigation]. Repatriation of $[X]K from [country] accounts can be structured via [method] to minimize withholding to [X]%.

📊 **Accountant:** Filing compliance requires [X] additional forms beyond standard 1040. FBAR aggregate balance of $[X]K triggers reporting — verify all [X] accounts included. PFIC holdings of $[X]K require Form 8621 with [QEF/MTM] election to avoid punitive excess distribution regime. Form 5471 Category [X] filer for [entity] — 30-day filing window. ⚠️ Penalties for non-filing: FBAR up to $[X]K, 8938 up to $[X]K, 5471 $10K per form per year. Recommend [specific compliance catch-up procedure if applicable].

💰 **Wealth Manager:** Cross-border holdings of $[X]M across [X] jurisdictions create $[X]K in annual tax drag versus domestic-only portfolio. Recommended restructuring: (1) Replace [X] PFIC positions with US-domiciled equivalents — saves $[X]K annually in excess tax, (2) Claim treaty benefits on [income type] — saves $[X]K, (3) [Totalization/§911] election saves $[X]K in social security. If client plans relocation to [country]: model the exit tax now, begin [X]-year optimization before departure. Net improvement from full cross-border optimization: $[X]K/year.
```

## Quality Gates

- [ ] US person status correctly classified (citizen, green card, substantial presence)
- [ ] All applicable filing obligations identified with penalty exposure quantified
- [ ] FBAR threshold tested with aggregate foreign account balances
- [ ] FATCA threshold tested against correct category (US vs. foreign resident, filing status)
- [ ] Applicable tax treaty analyzed with specific article references
- [ ] Saving clause impact assessed for each treaty benefit claimed
- [ ] Foreign tax credit computed by basket with limitation formula applied
- [ ] Excess FTC carryforward/carryback potential identified
- [ ] PFIC holdings identified with recommended election (QEF, MTM, or liquidate)
- [ ] Exit tax exposure modeled if expatriation is a possibility
- [ ] Totalization agreement reviewed if client has foreign employment
- [ ] §911 vs. FTC election analyzed for foreign earned income
- [ ] All compliance forms listed with deadlines and penalty amounts
- [ ] Triple-threat lens provides specific dollar savings from optimization
- [ ] No tax advice given on jurisdictions without confirmed treaty/rate research

## Data Sourcing

- **Tax treaties:** IRS.gov Treaty Table, specific treaty text (not summaries)
- **FBAR/FATCA thresholds:** FinCEN and IRS Form 8938 instructions (current year)
- **§7520 rate:** IRS Revenue Rulings (monthly, for CRT/CLT if relevant)
- **PFIC determination:** Fund prospectuses, annual reports, IRS PFIC guidance
- **Totalization agreements:** SSA.gov bilateral agreement texts
- **Exit tax thresholds:** IRC §877A, indexed amounts per IRS guidance
- **Foreign tax rates:** Verify with jurisdiction's official tax authority or Big 4 summaries
- **⚠️ Never assume treaty provisions — always verify against actual treaty text**

## See Also

- `estate-trust-planner` — cross-border estate and gift tax (situs rules, foreign trusts)
- `tax-planning-calendar` — FBAR/FATCA/Form 5471 deadlines
- `holding-period-analyzer` — PFIC holding period and basis tracking
- `charitable-giving-optimizer` — cross-border charitable deductions and treaty interactions
- `rmd-calculator` — foreign pension coordination with US retirement distributions
