# hoa-analyzer

**Skill #71 — HOA Analyzer**

Review HOA documents for real estate investors. Analyzes CC&Rs, bylaws, financials, reserve funds, and rental restrictions to surface red flags before closing on a property in a homeowners association.

## Trigger Phrases
- "Analyze this HOA document"
- "Does this HOA allow rentals?"
- "Review the CC&Rs for this deal"
- "HOA red flag check"
- "What are the rental restrictions in this HOA?"
- "Is this HOA well-funded?"
- "Check the HOA budget and reserves"

## Inputs
- HOA documents (CC&Rs, bylaws, rules, financial statements, meeting minutes, reserve study)
- Deal type (flip-to-sell, buy-and-hold rental, short-term rental, primary residence)
- Purchase price and property details
- Investor's intended use

## Outputs
- Red flag summary
- Rental restriction classification
- HOA financial health assessment
- Reserve fund adequacy rating
- Special assessment risk score
- Key restrictions that affect the deal
- Questions to ask HOA/management company before closing

## Steps

### Step 1: Rental Restriction Analysis

**Check for and classify:**

**Full Rental Ban:**
- "No unit may be leased or rented" — Deal killer for buy-and-hold investors
- Age-restricted communities (55+) — may prohibit younger renters

**Cap Restrictions:**
- "No more than X% of units may be rented at any time"
- Owner-occupancy ratios (e.g., 80% owner-occupied required)
- Waiting list to become a rental unit
- **Impact:** If at the cap, you can't rent immediately — possible deal killer

**Short-Term Rental Restrictions:**
- Minimum lease terms (30 days, 60 days, 12 months — common)
- Airbnb/VRBO explicitly prohibited — look for "transient occupancy" language
- Hotel/motel use prohibited

**Application/Approval Process:**
- Tenant must be approved by HOA board
- Background check required for tenants
- Right of first refusal by HOA on rental or sale

**Classification Output:**
```
RENTAL RESTRICTION LEVEL:
🟢 No restrictions — investor-friendly
🟡 Moderate restrictions — lease terms or tenant approval required
🔴 Significant restrictions — rental cap or STR ban
⛔ Deal killer — rental prohibited
```

### Step 2: Financial Health Analysis

**Reserve Fund Assessment:**

The reserve fund covers major capital expenses (roof, pool, elevator, parking lot). A well-funded HOA should have 70-100%+ reserve funding.

**Reserve Funding Levels:**
- **>70% funded** — Healthy. Low special assessment risk.
- **50-70% funded** — Adequate. Monitor for deferred maintenance.
- **30-50% funded** — Underfunded. Special assessment likely within 5 years.
- **<30% funded** — Critically underfunded. Special assessment risk is HIGH.

**Monthly Dues Assessment:**
- Very low dues (<$100/month for a condo) may indicate underfunded reserves
- Dues that haven't increased in 5+ years is a red flag
- Compare dues to similar HOAs in the area

**Delinquency Rate:**
- >15% delinquency rate → HOA is financially stressed
- High delinquency can affect FHA/VA financing approval

**Pending Litigation:**
- Any active lawsuits against or by the HOA
- Builder defect cases — can affect value and insurance

### Step 3: Special Assessment Risk

Check meeting minutes and financials for:
- Mentions of planned capital projects (roof replacement, pool repairs, parking, etc.)
- Prior special assessments (pattern indicator)
- Deferred maintenance items
- Reserve study findings and recommendations
- Any pending or proposed assessments

**Special Assessment Risk Score:**
```
LOW: Reserves >70%, no major deferred maintenance, no pending projects
MEDIUM: Reserves 40-70%, some deferred items noted, older infrastructure
HIGH: Reserves <40%, major capital needs evident, assessments discussed in minutes
CRITICAL: Active special assessment disclosed or pending vote
```

### Step 4: Key Restrictions Review

**Common Deal-Affecting Restrictions:**

**Property Use:**
- Home business restrictions (relevant if investor uses property as office)
- No home-based businesses visible to neighbors
- Parking rules (tenants with multiple vehicles, commercial vehicles)
- Pet restrictions (type, size, number) — affects rental appeal

**Exterior/Modification:**
- Approval process for exterior changes (paint colors, landscaping, additions)
- This matters for flippers — can they make changes quickly?
- Approved vendor lists or contractor requirements

**Sale Restrictions:**
- Right of first refusal by HOA on sale
- Minimum ownership period before selling
- Required HOA approval of buyers

**Investment-Specific:**
- Sign restrictions (For Sale, For Rent signs)
- Lockbox restrictions (some HOAs ban them)
- Access restrictions (showing hours, guest policies)

### Step 5: Output Analysis Report

```
HOA ANALYSIS — [Property Address]
HOA Name: [Name]
Monthly Dues: $[Amount]
Management Company: [Name]

RENTAL RESTRICTIONS: [Green/Yellow/Red/Deal Killer]
[Specific restriction details]

FINANCIAL HEALTH: [Healthy / Adequate / Underfunded / Critical]
Reserve Funding Level: [X]%
Reserve Balance: $[Amount]
Annual Budget: $[Amount]
Delinquency Rate: [X]% (if disclosed)

SPECIAL ASSESSMENT RISK: [Low / Medium / High / Active]
[Details of any known or pending assessments]

RED FLAGS:
1. [Flag 1]
2. [Flag 2]
3. [Flag 3]

KEY RESTRICTIONS AFFECTING YOUR DEAL:
• [Restriction 1]
• [Restriction 2]

RECOMMENDATION: [Proceed / Proceed with Caution / Do Not Proceed]
Reason: [Brief rationale]

QUESTIONS FOR HOA/MANAGEMENT COMPANY:
1. [Question 1]
2. [Question 2]
3. [Question 3]
```

## Example Prompts

### Pre-Close HOA Review
```
I'm under contract on a condo in Denver. The HOA documents just came in. I want to buy this as a rental. Can you review the CC&Rs and financials for red flags?

[paste CC&R text or financial summary]
```

### Rental Restriction Check
```
I'm looking at a townhome in an HOA. Here's the rental restriction section from the CC&Rs. Can you tell me if I can rent this out and what the restrictions are?
```

### Financial Health Check
```
Here's the HOA budget and reserve study for a condo I'm buying. Is this HOA financially healthy? Am I at risk for a special assessment?
```

## Scripts

### Red Flag Classifier
When reviewing CC&Rs, automatically flag:
- "No rental" or "Owner must occupy" → Deal Killer
- Rental cap percentage → Flag and calculate current saturation if possible
- "Transient occupancy" prohibition → STR banned
- Reserve funding under 50% → Special assessment risk
- Any active litigation mention → Flag as significant risk
- HOA dues more than 1.5% of property value/year → High carrying cost

### Rental Restriction Extractor
Parse CC&Rs specifically for:
1. Is renting allowed? (Yes/No/Conditional)
2. Minimum lease term
3. STR allowed? (Yes/No)
4. Tenant approval process required?
5. Rental cap? (X% of units)
6. Right of first refusal on rental?

### 5 Questions to Ask HOA Before Closing
1. What is the current rental cap, and are there units on the waitlist?
2. Are there any pending or planned special assessments?
3. What is the current delinquency rate on dues?
4. Are there any active lawsuits against the HOA?
5. What is the reserve fund balance and the most recent reserve study date?

## Notes
- HOA documents can be dense — focus on Article sections covering "Use Restrictions," "Leasing," and "Amendments"
- Meeting minutes often reveal what's not in the CC&Rs (planned repairs, neighbor disputes, financial struggles)
- For FHA/VA financing, HOAs must meet approval requirements — high delinquency rates disqualify
- Always get HOA estoppel certificate at closing to confirm no outstanding violations or dues owed
