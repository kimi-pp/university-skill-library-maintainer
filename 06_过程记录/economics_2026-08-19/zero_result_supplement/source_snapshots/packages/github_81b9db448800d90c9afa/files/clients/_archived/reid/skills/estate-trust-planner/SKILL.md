---
name: estate-trust-planner
version: 1.0.0
description: "Estate planning analysis — trust structures, gift tax planning, generation-skipping transfers, charitable strategies, succession planning, and federal estate tax exposure assessment. Wealth transfer optimization."
---

# estate-trust-planner

Analyze estate planning needs and strategies. Assess federal/state estate tax exposure, recommend trust structures (revocable, irrevocable, ILIT, GRAT, QPRT, CRT, CLT, dynasty), optimize lifetime gift strategies, plan generation-skipping transfers, evaluate charitable giving vehicles, and develop business succession plans. Estate planning is where lifetime wealth building meets generational wealth transfer — and where the tax code offers the most powerful (and most complex) planning opportunities.

## Trigger

- "Estate planning analysis"
- "Trust structure recommendation"
- "Gift tax planning"
- "Estate tax exposure"
- "Wealth transfer strategy"
- "Generation-skipping trust"
- "Charitable trust"
- "Business succession planning"
- "How do I pass wealth to my kids?"
- "Estate tax minimization"

## Inputs

- **Client profile:** Age, marital status, state of residence (required)
- **Net worth:** From personal-balance-sheet (required)
- **Family structure:** Spouse, children, grandchildren, ages (required)
- **Current estate plan:** Existing trusts, wills, beneficiary designations (required)
- **Business interests:** Private business ownership details (optional)
- **Charitable intent:** Desired charitable giving level (optional)
- **Goals:** Wealth transfer priorities, control preferences, family dynamics (required)
- **State estate tax:** Does resident state have estate/inheritance tax? (required)

## Dependencies

- **financial-data-api** — for asset valuation
- **sec-edgar-fetch** — for comparable company valuation (business interests)

## Step 0: EDGAR Pre-flight (for business valuation)

```bash
python3 skills/sec-edgar-fetch/scripts/edgar_xbrl_extract.py COMPARABLE_TICKER --preset valuation
```

Use comparable company multiples for private business valuation in estate planning context. Apply valuation discounts (minority, marketability).

## Methodology

### Step 1: Estate Tax Exposure Assessment

**2025 Federal Estate Tax Framework:**
```
Lifetime Exemption (2025): $13.99M per person / $27.98M per married couple
Estate Tax Rate: 40% on amounts exceeding exemption
Portability: Deceased spouse's unused exemption (DSUE) transfers to surviving spouse

Sunset Risk: Under current law (TCJA), exemption reverts to ~$7M/person
after 2025 (inflation-adjusted from $5M 2017 base) unless extended.

Estate Tax Calculation:
  Gross Estate (FMV at death):                          $XX,XXX,XXX
  − Funeral/admin expenses:                              (XXX,XXX)
  − Debts:                                              (X,XXX,XXX)
  − Marital Deduction (to spouse, unlimited):            (X,XXX,XXX)
  − Charitable Deduction:                                (XXX,XXX)
  = Taxable Estate:                                     $XX,XXX,XXX
  − Lifetime Exemption Used:                            ($13,990,000)
  = Amount Subject to Tax:                              $XX,XXX,XXX
  × 40% Rate:                                          $X,XXX,XXX
  − Credits:                                            (XXX,XXX)
  = Estimated Federal Estate Tax:                       $X,XXX,XXX
```

**State estate/inheritance tax check:**
```
States with separate estate tax (2025):
  CT, DC, HI, IL, ME, MD, MA, MN, NY, OR, RI, VT, WA
  Exemptions range from $1M (OR, MA) to $13.99M (CT)

States with inheritance tax:
  IA, KY, MD, NE, NJ, PA
  Rate depends on beneficiary relationship (0% spouse, up to 18% non-relative)

MD has BOTH estate tax AND inheritance tax (double hit)
```

### Step 2: Trust Structure Analysis

**Core Trust Types and Applications:**

| Trust | Revocable? | Estate Inclusion? | Best For | Key Benefit |
|-------|-----------|------------------|----------|-------------|
| **Revocable Living Trust** | Yes | Yes (included) | Probate avoidance, privacy | No estate tax benefit but avoids probate |
| **Irrevocable Life Insurance Trust (ILIT)** | No | No (excluded) | Life insurance proceeds | Keeps insurance out of estate |
| **Grantor Retained Annuity Trust (GRAT)** | No | No (if survives term) | Appreciating assets | Transfer appreciation tax-free |
| **Qualified Personal Residence Trust (QPRT)** | No | No (if survives term) | Primary/vacation home | Transfer home at discounted value |
| **Intentionally Defective Grantor Trust (IDGT)** | No | No | Business interests, appreciating assets | Grantor pays income tax (additional gift) |
| **Charitable Remainder Trust (CRT)** | No | No | Income + charity | Income stream + charitable deduction |
| **Charitable Lead Trust (CLT)** | No | No | Charity now, family later | Charity gets income, family gets remainder |
| **Dynasty Trust** | No | No | Multi-generational wealth | Avoids estate tax at each generation |
| **Special Needs Trust** | No | No | Disabled beneficiaries | Preserves government benefit eligibility |
| **Spousal Lifetime Access Trust (SLAT)** | No | No | Married couples | Irrevocable but spouse can access |

### Step 3: Lifetime Gift Strategy

```
Annual Exclusion (2025): $19,000 per recipient per donor
  Married couple: $38,000 per recipient (gift splitting)

Gift Tax Exemption: Unified with estate ($13.99M lifetime)
  Every dollar of lifetime gifts reduces estate exemption

Optimal Gifting Strategy:
1. Max annual exclusions ($19K × recipients per year) — uses NO lifetime exemption
2. Direct payments for medical expenses (unlimited, directly to provider)
3. Direct payments for education tuition (unlimited, directly to institution)
4. 529 superfunding: 5 years of annual exclusion at once ($95K/$190K per child)
5. Larger gifts using lifetime exemption (before potential sunset)

Gift Tax Sunset Strategy (if exemption reduces to ~$7M):
  Current exemption: $13.99M
  Post-sunset: ~$7M (estimated)
  "Use it or lose it": Gift ~$7M before sunset to capture extra exemption
  Anti-clawback rule: IRS confirmed gifts made under higher exemption
  are protected even after sunset
```

### Step 4: GRAT Strategy (for Appreciating Assets)

```
Grantor Retained Annuity Trust:
  Transfer: $X,XXX,XXX of [asset] to GRAT
  Term: X years
  Annuity: Calculated to make gift value ≈ $0 ("zeroed-out GRAT")
  §7520 Rate (current): X.X% (higher rate = harder to beat, but still viable)

  If asset grows > §7520 hurdle rate: Excess passes to beneficiaries tax-free
  If asset grows < §7520 rate: Assets return to grantor (no harm done)
  If grantor dies during term: Assets included in estate (risk)

  Example:
    $5M GRAT, 2-year term, 5% §7520 rate
    Annuity payments: ~$2.63M per year
    If assets grow 15% per year:
      Year 1 value: $5.75M → pay $2.63M annuity → remainder: $3.12M
      Year 2 value: $3.59M → pay $2.63M annuity → remainder: $0.96M
      Tax-free transfer to beneficiaries: $960K
    Total gift/estate tax on this: $0
```

### Step 5: Generation-Skipping Transfer (GST) Tax

```
GST Exemption (2025): $13.99M per person (same as estate)
GST Tax Rate: 40% (on top of estate tax if both apply)

GST applies when transferring to "skip persons":
  - Grandchildren (or more remote descendants)
  - Unrelated persons >37.5 years younger

Dynasty Trust Strategy:
  - Fund irrevocable trust with GST exemption ($13.99M)
  - Trust benefits children, grandchildren, great-grandchildren
  - No estate tax at each generational transfer
  - State law determines maximum trust duration
    (Some states: perpetual — SD, NV, AK, DE, NH)
    (Most states: Rule Against Perpetuities — ~90-120 years)
  
  Value over 3 generations (assuming 7% growth, 30-year generations):
    Without dynasty trust: $13.99M → $24M (after 40% tax) → $17M → $12M
    With dynasty trust: $13.99M → $106M → $808M (no tax at each generation)
```

### Step 6: Charitable Planning Vehicles

| Vehicle | Income Tax Deduction | Estate Tax Benefit | Income Stream | Best For |
|---------|---------------------|-------------------|--------------|----------|
| Direct gift | FMV (cash) or basis (non-cash to public charity) | Reduces estate | None | Simple, immediate |
| Donor Advised Fund (DAF) | FMV in contribution year | Reduces estate | None | Bunching strategy, legacy |
| CRT (Charitable Remainder Trust) | PV of remainder interest | Removes from estate | Yes (to donor) | Income + charity |
| CLT (Charitable Lead Trust) | PV of lead interest (grantor CLT) | Reduces transfer value | None (charity gets income) | Transfer assets at discount |
| Private Foundation | FMV (30% AGI limit) | Removes from estate | None | Control, family legacy |
| Qualified Charitable Distribution (QCD) | N/A (reduces RMD) | Reduces estate | None | IRA holders 70½+ |

### Step 7: Business Succession Planning

For clients with private business interests:

```
Business Valuation for Estate:
  Revenue: $XX,XXX,XXX
  EBITDA: $X,XXX,XXX
  Comparable public company multiple: X.Xx (from EDGAR)
  Gross value: $XX,XXX,XXX
  
  Valuation Discounts:
    Minority interest discount: 15-35%
    Lack of marketability discount: 20-40%
    Combined discount: 30-55%
    Discounted value: $X,XXX,XXX

Succession Options:
  1. Gift/sell to family members (IDGT, installment sale)
  2. ESOP (Employee Stock Ownership Plan)
  3. Management buyout (MBO)
  4. Third-party sale
  5. Family limited partnership (FLP) for fractional transfers
  
Buy-Sell Agreement:
  - Funded by life insurance (ILIT)
  - Valuation method: formula, appraisal, or fixed price
  - Trigger events: death, disability, retirement, divorce
```

### Step 8: Liquidity Analysis

```
Estate Liquidity Test:
  Estimated Federal Estate Tax:    $X,XXX,XXX
  Estimated State Estate Tax:      $XXX,XXX
  Administration Costs:            $XXX,XXX
  Debts Payable at Death:          $XXX,XXX
  Total Cash Needed at Death:      $X,XXX,XXX

  Available Liquid Assets:         $X,XXX,XXX
  Life Insurance (outside estate): $X,XXX,XXX
  Total Liquidity:                 $X,XXX,XXX

  Shortfall / (Surplus):           $XXX,XXX

  If shortfall: Options:
    1. ILIT to fund gap (tax-free insurance proceeds outside estate)
    2. IRC §6166 installment election (up to 14 years for business assets)
    3. IRC §303 stock redemption (to pay estate tax on closely held stock)
    4. Sell assets (potential forced sale discount of 20-40%)
```

## Output Format

```
🏛️ Estate Planning Analysis — [Client Name]
Age: [XX] | Marital Status: [Status] | State: [State]
Net Worth: $[X,XXX,XXX] | Lifetime Exemption Used: $[X,XXX,XXX]

━━━ ESTATE TAX EXPOSURE ━━━
| Component                    | Amount         |
|-----------------------------|---------------|
| Gross Estate (FMV)           | $XX,XXX,XXX   |
| Less: Deductions             | ($X,XXX,XXX)  |
| Less: Marital Deduction      | ($X,XXX,XXX)  |
| Taxable Estate               | $XX,XXX,XXX   |
| Less: Remaining Exemption    | ($XX,XXX,XXX) |
| Amount Subject to Tax        | $X,XXX,XXX    |
| **Estimated Federal Tax**    | **$X,XXX,XXX**|
| **Estimated State Tax**      | **$XXX,XXX**  |
| **Total Estate Tax**         | **$X,XXX,XXX**|
| Effective Rate               | XX.X%         |

━━━ SUNSET SCENARIO (if exemption reverts to ~$7M) ━━━
| Component                    | Current Law    | Post-Sunset    |
|-----------------------------|---------------|---------------|
| Exemption per person         | $13.99M       | ~$7.0M        |
| Taxable amount               | $X,XXX,XXX    | $X,XXX,XXX    |
| **Additional tax exposure**  |               | **$X,XXX,XXX**|

━━━ RECOMMENDED STRATEGIES ━━━
| # | Strategy              | Tax Savings   | Complexity | Priority |
|---|----------------------|--------------|-----------|----------|
| 1 | [GRAT for business]  | $X,XXX,XXX   | High      | ⭐⭐⭐    |
| 2 | [Annual gifting]     | $XXX,XXX     | Low       | ⭐⭐⭐    |
| 3 | [ILIT for insurance] | $XXX,XXX     | Medium    | ⭐⭐      |
| 4 | [Dynasty trust]      | $X,XXX,XXX   | High      | ⭐⭐      |
| 5 | [CRT for charity]    | $XXX,XXX     | Medium    | ⭐        |
| **Total Potential Savings** | **$X,XXX,XXX** | | |

━━━ GIFT STRATEGY ━━━
| Recipient     | Annual Exclusion | Lifetime Gift | Vehicle        | Timing    |
|--------------|-----------------|--------------|---------------|-----------|
| Child 1      | $19K/yr         | $X,XXX,XXX   | IDGT          | Before sunset |
| Child 2      | $19K/yr         | $X,XXX,XXX   | SLAT          | Before sunset |
| Grandchild 1 | $19K/yr         | 529 superfund | 529 Plan      | Immediate |
| Charity      | N/A             | $XXX,XXX     | CRT           | Year-end  |

━━━ TRUST STRUCTURE RECOMMENDATION ━━━
| Trust Type | Purpose                  | Funding     | Beneficiaries    |
|-----------|--------------------------|-----------|-----------------|
| ILIT      | Hold $[X]M life insurance | Premium gifts | Children       |
| GRAT      | Transfer business equity  | $[X]M biz interest | Dynasty trust |
| SLAT      | Spousal access + transfer | $[X]M portfolio | Spouse + children |
| Dynasty    | Multi-gen wealth transfer | GRAT remainder | Descendants    |

━━━ LIQUIDITY ASSESSMENT ━━━
| Need                    | Amount       |
|------------------------|-------------|
| Federal estate tax      | $X,XXX,XXX  |
| State estate tax        | $XXX,XXX    |
| Admin/debts             | $XXX,XXX    |
| **Total cash needed**   | **$X,XXX,XXX** |
| Available liquidity     | $X,XXX,XXX  |
| ILIT death benefit      | $X,XXX,XXX  |
| **Surplus / (Shortfall)** | **$XXX,XXX** |

━━━ TRIPLE-THREAT LENS ━━━
🏦 **Banker:** Estate liquidity is critical: estimated estate tax of $[X]M due within 9 months of death. Liquid assets of $[X]M [cover/fall short by $X]M]. If shortfall: ILIT with $[X]M death benefit solves liquidity (premium: $[X]K/yr). Business interest of $[X]M — may qualify for IRC §6166 installment payment of estate tax (up to 14 years) if business exceeds 35% of adjusted gross estate. Life insurance [within/outside] estate currently — ILIT critical to exclude.
📊 **Accountant:** Stepped-up basis at death: $[X]M of unrealized gains in taxable portfolio would be eliminated. This means [do NOT sell highly appreciated positions before death — let beneficiaries get step-up]. GRAT annuity payments create [income/gift] tax events — model cash flow. Business valuation discounts (minority [XX]% + marketability [XX]% = combined [XX]%) are defensible based on [Tax Court precedent / IRS guidelines] but require qualified appraisal. Gift tax returns (Form 709) required for any gifts exceeding annual exclusion.
💰 **Wealth Manager:** Without planning, $[X]M estate tax erodes [XX]% of family wealth at death. Recommended strategies save $[X]M — reducing effective rate from [XX]% to [XX]%. Priority action: [specific — e.g., "fund GRAT with $5M of business equity before Q4; §7520 rate of X.X% creates favorable hurdle"]. Sunset urgency: if exemption drops to ~$7M, the additional ~$7M per person of exemption worth $[X]M in estate tax savings. Recommend gifting $[X]M to irrevocable trust before [date] to lock in current exemption.
```

## Quality Gates

- [ ] Gross estate calculated with all asset categories (including life insurance if owned)
- [ ] Federal and state estate tax exposure quantified separately
- [ ] Lifetime exemption usage tracked (prior gifts via Form 709)
- [ ] TCJA sunset risk modeled with dollar impact
- [ ] Trust recommendations matched to specific goals and assets
- [ ] GRAT modeling includes §7520 rate and growth assumptions
- [ ] GST exposure assessed for multigenerational transfers
- [ ] Business valuation includes appropriate discounts with justification
- [ ] Liquidity analysis: can estate pay taxes without forced asset sales?
- [ ] Charitable strategies evaluated for income + estate + legacy benefits
- [ ] Implementation timeline with specific deadlines and professional referrals

## Professional Standards

**What separates A from B work:**
- **A-grade:** Estate tax calculated with actual exemption usage. Trust recommendations specific to client's assets and goals (not generic menu). GRAT modeled with current §7520 rate and asset-specific growth. Valuation discounts justified with ranges and precedent. Sunset strategy with specific gifting timeline. Liquidity analysis includes insurance needs. State estate/inheritance tax calculated separately. Incapacity planning addressed (POA, healthcare directive).
- **B-grade:** Generic "you should have a trust" without specifying type or funding. Estate tax estimated at "40% of everything" without deductions. No GRAT or advanced strategy analysis. Business valued at owner's estimate. No sunset planning. No liquidity analysis.

**Common pitfalls:**
- Forgetting to include life insurance in gross estate (if policy is owned by insured, death benefit is in estate — ILIT solves this)
- Double-counting: gifting assets AND still including them in gross estate
- Not considering state estate tax (can hit at much lower thresholds — MA/OR at $1M)
- Overly aggressive valuation discounts without appraisal support (IRS regularly challenges >40% combined)
- GRAT mortality risk: if grantor dies during term, entire GRAT included in estate
- Ignoring portability election (must file estate tax return for first spouse to transfer DSUE, even if no tax is owed)
- Not addressing incapacity planning alongside estate planning (POA, healthcare directive)
- Assuming irrevocable means no access (SLATs provide spousal access)
- Overlooking income tax implications of inherited retirement accounts (SECURE Act 10-year rule)

## See Also

- `personal-balance-sheet` — provides the asset base for estate planning
- `tax-efficient-investing` — step-up basis considerations affect investment decisions
- `portfolio-constructor` — portfolio design for trust accounts
- `risk-tolerance-profiler` — trust investment policy considerations
