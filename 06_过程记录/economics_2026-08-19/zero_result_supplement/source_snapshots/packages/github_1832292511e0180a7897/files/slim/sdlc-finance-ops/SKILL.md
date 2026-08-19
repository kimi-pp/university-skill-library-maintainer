---
name: sdlc-finance-ops
description: "Software company finance and operations: unit economics, SaaS metrics, fundraising (seed to IPO), financial planning, burn rate, runway, budgeting, cap table, equity, stock options, board management, vendor management, procurement, insurance."
version: 6.0.0-moderate
author: Dinoudon
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sdlc, finance, operations, unit-economics, fundraising, saas-metrics, burn-rate, runway, cap-table, equity, board-management]
    related_skills: [sdlc-product-growth, sdlc-gtm-strategy, sdlc-hiring-talent, sdlc-legal-compliance]
---

---
name: sdlc-finance-ops
description: "Software company finance and operations: unit economics, SaaS metrics, fundraising (seed to IPO), financial planning, burn rate, runway, budgeting, cap table, equity, stock options, board management, vendor management, procurement, insurance."
version: 6.0.0-moderate
author: Dinoudon
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sdlc, finance, operations, unit-economics, fundraising, saas-metrics, burn-rate, runway, cap-ta
## When to Use
Trigger when user:
- Calculates unit economics (LTV, CAC, payback period)
- Plans fundraising (seed, Series A/B/C, IPO)
- Creates financial model or projections
- Manages burn rate and runway
- Designs cap table or equity plan
- Prepares board meeting materials
- Evaluates vendor contracts or procurement
- Plans budget or headcount
## Step 1: SaaS Unit Economics
```
MRR (Monthly Recurring Revenue)
  = Σ (customers × monthly subscription)

ARR (Annual Recurring Revenue)
  = MRR × 12

ARPU (Average Revenue Per User)
  = MRR / paying customers

LTV (Customer Lifetime Value)
  = ARPU × gross margin × (1 / monthly churn rate)

CAC (Customer Acquisition Cost)
  = Total sales & marketing spend / new customers acquired

```
## Step 2: Fundraising
| Stage | Amount | Traction | Valuation | Dilution |
|-------|--------|----------|-----------|----------|
| **Pre-seed** | $100K-$1M | Idea/prototype | $2-5M | 15-25% |
| **Seed** | $1M-$5M | PMF signal, early revenue | $5-20M | 15-25% |
| **Series A** | $5M-$20M | $1-5M ARR, proven GTM | $20-80M | 15-25% |
| **Series B** | $20M-$50M | $5-20M ARR, scaling | $80-300M | 10-20% |
| **Series C+** | $50M-$200M+ | $20M+ ARR, market leader | $300M+ | 10-15% |
| **IPO** | Public offering | $100M+ ARR, profitable path | Market decides | Varies |
```
1. Preparation (2-4 weeks)
   □ Update pitch deck (10-12 slides)
   □ Financial model (3-year projections)
   □ Data room (metrics, contracts, legal docs)
   □ Target investor list (50-100 investors)
   □ Warm intros lined up

2. Outreach (1-2 weeks)
   □ Send intro emails (warm intros preferred)
   □ Schedule first meetings (aim for 30+ in 2 weeks)
   □ Track pipeline in CRM

3. First Meetings (2-3 weeks)
   □ 30-min pitch meeting
   □ Share deck + financial model
```
## Step 3: Financial Planning
```
Revenue Model:
  - New customers/month (from sales pipeline)
  - ARPU (average revenue per user)
  - Expansion revenue (upsells, cross-sells)
  - Churn (lost MRR)

Cost Model:
  - COGS (hosting, support, payment processing)
  - R&D (engineering headcount, tools)
  - S&M (marketing, sales team, events)
  - G&A (legal, finance, office, insurance)

Key Outputs:
  - Monthly burn rate
  - Runway (months of cash remaining)
```
## Step 4: Cap Table & Equity
```
Founder A: 40% (4,000,000 shares)
Founder B: 30% (3,000,000 shares)
Employee option pool: 15% (1,500,000 shares)
Seed investors: 10% (1,000,000 shares)
Angel investors: 5% (500,000 shares)
Total: 10,000,000 shares

After Series A (20% dilution):
Founder A: 32% (diluted from 40%)
Founder B: 24% (diluted from 30%)
Employee pool: 12% (refreshed to 15%)
Seed investors: 8%
Angel investors: 4%
Series A investors: 20%
Total: 100%
```
## Step 5: Board Management
```
Quarterly board meeting (2-3 hours):

1. CEO Update (15 min)
   - Key wins, challenges, strategic decisions
   
2. Financial Review (30 min)
   - Revenue, burn, runway, metrics dashboard
   
3. Product Update (20 min)
   - Roadmap progress, key launches, customer feedback
   
4. GTM Update (20 min)
   - Sales pipeline, marketing, customer success
   
5. People Update (15 min)
```
## Step 6: Vendor & Operations
```
Criteria for SaaS vendor selection:
1. Security: SOC 2, GDPR compliance, data residency
2. Reliability: SLA, uptime history, incident response
3. Cost: Per-user vs flat rate, annual vs monthly, volume discounts
4. Integration: API quality, SSO, SAML, SCIM
5. Lock-in: Data export, migration support, contract terms
6. Support: Response time, dedicated CSM, escalation path
```
## Step 7: Financial Modeling
```
Revenue Model (Monthly):
┌─────────────────────────────────────────────────────┐
│ Month        │ M1    │ M2    │ M3    │ ... │ M12   │
├──────────────┼───────┼───────┼───────┼─────┼───────┤
│ New customers│ 20    │ 25    │ 30    │ ... │ 50    │
│ Churned      │ -2    │ -3    │ -3    │ ... │ -5    │
│ Net new      │ 18    │ 22    │ 27    │ ... │ 45    │
│ Total cust.  │ 118   │ 140   │ 167   │ ... │ 450   │
│ ARPU         │ $500  │ $500  │ $500  │ ... │ $520  │
│ MRR          │ $59K  │ $70K  │ $84K  │ ... │ $234K │
│ ARR (MRR×12) │ $708K │ $840K │ $1M   │ ... │ $2.8M │
└──────────────┴───────┴───────┴───────┴─────┴───────┘

Cost Model (Monthly):
┌─────────────────────────────────────────────────────┐
```
## Step 8: Accounting & Tax Basics
```
ASC 606 (Revenue Recognition):

Recognized when:
1. Contract identified
2. Performance obligations identified
3. Transaction price determined
4. Price allocated to obligations
5. Revenue recognized when obligation satisfied

Example:
Annual contract: $12,000/year
Monthly recognition: $1,000/month
Not $12,000 upfront (even if paid in advance)

Deferred revenue: Cash received but not yet recognized
```
## Pitfalls
1. **Vanity metrics** — "10,000 signups" means nothing without activation and retention data.
2. **Raising too much** — More money = more dilution + pressure to grow faster than healthy.
3. **Raising too little** — Running out of money mid-raise is a death sentence. Raise 18-24 months.
4. **No financial model** — Investors expect a bottoms-up model, not a hockey stick in a slide deck.
5. **Ignoring unit economics** — Growing revenue while losing money on every customer is a Ponzi scheme.
6. **Premature scaling** — Hiring 50 engineers before PMF burns cash without returns.
7. **Cap table mess** — Clean up cap table before raising. Investors will find every issue.
8. **No board prep** — Board meetings are high-leverage. Prepare materials 1 week in advance.
9. **Equity over-promising** — Running out of option pool before Series B creates hiring problems.
10. **Cash flow blindness** — Profitable on paper but no cash in bank = bankruptcy. Track cash weekly.
## Step 12: Board Management
```
Board Meeting — [Company Name]
[Date] | [Duration: 2-3 hours]

1. CEO Update (15 min)
   - Key wins since last meeting
   - Challenges and how we're addressing
   - Strategic priorities for next quarter

2. Financial Review (30 min)
   - Revenue vs plan (trailing 3 months)
   - Cash position and runway
   - Key metrics dashboard
   - Forecast update

3. Product Update (20 min)
```
## Step 13: Fundraising Process
```
Folder structure:
  /data-room
    /01-company
      - Pitch deck
      - Executive summary
      - Cap table
      - Certificate of incorporation
      - Board minutes
      
    /02-financials
      - Historical P&L (3 years)
      - Monthly P&L (trailing 12 months)
      - Cash flow statement
      - Balance sheet
      - Financial model (3-5 year forecast)
```
## Step 17: Revenue Operations (RevOps)
```
Alignment:
  Marketing → Sales → Customer Success
  Shared metrics, shared data, shared process

Data unification:
  - Single CRM (Salesforce, HubSpot)
  - Marketing automation (Marketo, Pardot)
  - Customer success platform (Gainsight, ChurnZero)
  - Data warehouse (Snowflake, BigQuery)

Process standardization:
  - Lead scoring model (shared marketing + sales)
  - Opportunity stages (defined exit criteria)
  - Handoff process (marketing → sales → CS)
  - Renewal process (CS → sales for expansion)
```
## Step 18: Financial Reporting
```
Contents:
  1. Executive summary (1 page)
     - Key highlights and lowlights
     - Cash position
     - Runway
     - Revenue vs plan
     
  2. P&L statement (actual vs budget vs prior year)
     - Revenue by product/segment
     - COGS breakdown
     - OpEx by department
     - EBITDA and margins
     
  3. Balance sheet
     - Assets (current and non-current)
```
## Step 19: Treasury Management
```
Cash flow forecasting:
  - 13-week rolling forecast (weekly granularity)
  - Monthly forecast (12-month horizon)
  - Annual budget (3-5 year horizon)

Cash optimization:
  - Accelerate collections (net 30 to net 15)
  - Extend payables (negotiate net 60)
  - Inventory optimization (JIT)
  - Capital expenditure timing

Banking relationships:
  - Primary operating account (major bank)
  - Secondary account (backup)
  - Foreign currency accounts (if international)
```
## Step 20: Financial Systems
```
Core systems:
  - ERP: NetSuite, Sage Intacct, QuickBooks
  - Billing: Stripe, Chargebee, Zuora
  - Payroll: Gusto, Rippling, ADP
  - Expense management: Brex, Ramp, Expensify
  - AP automation: Bill.com, Tipalti, AvidXchange

Reporting:
  - FP&A: Mosaic, Jirav, Datarails
  - BI: Looker, Tableau, Power BI
  - Data warehouse: Snowflake, BigQuery

Compliance:
  - Audit: Workiva, AuditBoard
  - Tax: Avalara, Vertex
```
## Step 21: Fundraising Operations
```
Data room organization:
  /01-corporate: Cert of incorporation, bylaws, board minutes, cap table
  /02-financial: Historical financials, monthly P&L, financial model
  /03-product: Product roadmap, technical architecture, security certs
  /04-market: TAM/SAM/SOM, competitive landscape, case studies
  /05-team: Org chart, key bios, hiring plan, employee handbook

Timeline:
  - Pre-fundraise: 2-4 weeks to prepare
  - Active fundraise: 6-12 weeks
  - Due diligence: 2-4 weeks
  - Closing: 2-4 weeks
  - Total: 3-6 months
```
## Step 22: SaaS Metrics Deep Dive
```
Revenue metrics:
  ARR (Annual Recurring Revenue):
    = MRR x 12
    Growth: YoY and QoQ
    
  MRR (Monthly Recurring Revenue):
    = Sum of all monthly subscription revenue
    Components: New + Expansion + Churn + Contraction
    
  Net New ARR:
    = New ARR + Expansion ARR - Churned ARR - Contraction ARR
    
  ARPU (Average Revenue Per User):
    = MRR / Total paying customers
    
```
## Step 23: Fundraising Strategy
```
Pre-seed:
  Amount: $100K-$500K
  Stage: Idea/prototype
  Investors: Angels, accelerators (YC, Techstars)
  Terms: SAFE or convertible note
  Dilution: 5-10%

Seed:
  Amount: $500K-$3M
  Stage: MVP, early traction
  Investors: Seed funds, angels
  Terms: Priced round (SAFE less common at higher amounts)
  Dilution: 10-20%

Series A:
```
## Step 24: Cap Table Management
```
Pre-funding:
  | Shareholder | Shares | % |
  |-------------|--------|---|
  | Founder A   | 4,000,000 | 50% |
  | Founder B   | 3,200,000 | 40% |
  | Employee pool| 800,000 | 10% |
  | Total       | 8,000,000 | 100% |

Post seed round ($2M at $8M pre):
  | Shareholder | Shares | % |
  |-------------|--------|---|
  | Founder A   | 4,000,000 | 40% |
  | Founder B   | 3,200,000 | 32% |
  | Seed investors| 2,000,000 | 20% |
  | Employee pool| 800,000 | 8% |
```
## Step 25: Financial Modeling
```
Income Statement:
  Revenue
    - New business revenue
    - Expansion revenue
    - Churned revenue (negative)
  = Net Revenue
  
  Cost of Revenue
    - Hosting/infrastructure
    - Payment processing
    - Customer support
    - Professional services
  = Gross Profit
  
  Operating Expenses
```
## Step 26: Cost Accounting
```
Product A (Starter plan):
  ARPU: $49/month
  COGS: $12/month (hosting: $5, support: $4, payment: $3)
  Gross margin: 75.5%
  CAC: $150
  CLV: $49 x 0.755 x (1/0.03) = $1,233
  CLV:CAC: 8.2:1
  Payback: $150 / ($49 x 0.755) = 4.1 months

Product B (Pro plan):
  ARPU: $199/month
  COGS: $35/month (hosting: $15, support: $12, payment: $8)
  Gross margin: 82.4%
  CAC: $500
  CLV: $199 x 0.824 x (1/0.02) = $8,199
```
## Step 27: Investor Relations
```
Subject: [Company] Monthly Update — [Month Year]

Highlights:
  - [Big win 1]
  - [Big win 2]
  - [Big win 3]

Metrics:
  | Metric | This Month | Last Month | MoM Change |
  |--------|------------|------------|------------|
  | MRR | $X | $Y | +Z% |
  | Customers | X | Y | +Z |
  | Churn | X% | Y% | -Z% |
  | NPS | X | Y | +Z |
  | Cash | $X | $Y | -$Z |
```
## Step 28: Exit Planning
```
IPO:
  Requirements:
    - $100M+ ARR (typical threshold)
    - 3+ years of financials
    - Profitable or clear path to profitability
    - Strong governance (independent board)
  
  Process:
    1. Select underwriters (Goldman, Morgan Stanley, etc.)
    2. S-1 filing (confidential or public)
    3. SEC review and comments
    4. Roadshow (2-3 weeks)
    5. Pricing and allocation
    6. Trading begins
  
```
## Step 29: Financial Analysis
```
Gross margin analysis:
  Revenue: $10M
  COGS: $2.5M
  Gross profit: $7.5M
  Gross margin: 75%

  COGS breakdown:
    Hosting: $1M (40%)
    Payment processing: $500K (20%)
    Customer support: $750K (30%)
    Other: $250K (10%)

Operating margin analysis:
  Gross profit: $7.5M
  R&D: $3M (30% of revenue)
```
## Step 30: Financial Reporting Automation
```
Data collection:
  - Stripe: Revenue, subscriptions, churn
  - QuickBooks/NetSuite: Accounting, GL
  - Gusto/Rippling: Payroll, headcount
  - Brex/Ramp: Expenses, corporate cards
  - CRM (HubSpot/Salesforce): Pipeline, bookings

Data transformation:
  - dbt: SQL-based transformations
  - Fivetran: Data connectors
  - Airbyte: Open-source data integration
  - Custom scripts: API integrations

Reporting:
  - Looker/Tableau: Dashboards
```
## Step 31: Audit Preparation
```
Financial audit:
  □ Clean books (no material misstatements)
  □ Reconciliations complete (bank, AR, AP)
  □ Supporting documentation for all transactions
  □ Revenue recognition compliant (ASC 606)
  □ Expense categorization consistent
  □ Intercompany transactions documented
  □ Related party transactions disclosed
  □ Stock-based compensation calculated
  □ Lease accounting compliant (ASC 842)
  □ Tax provision calculated

Operational audit:
  □ Internal controls documented
  □ Segregation of duties
```
## Step 32: Financial Modeling Tools
```
Model structure:
  - Inputs tab (assumptions, drivers)
  - Calculations tab (formulas, logic)
  - Outputs tab (dashboards, charts)
  - Documentation tab (methodology, sources)

Formatting:
  - Blue font for inputs
  - Black font for calculations
  - Green font for links to other sheets
  - Consistent number formatting
  - Named ranges for key assumptions

Error prevention:
  - Data validation (dropdowns, ranges)
```
## Step 33: Financial Operations Automation
```
Invoice processing:
  1. Receive invoice (email, portal, mail)
  2. OCR extraction (amount, vendor, date, line items)
  3. Match to PO (3-way match: PO, receipt, invoice)
  4. Route for approval (based on amount, department)
  5. Schedule payment (optimize for terms)
  6. Record in GL (automatic posting)

Tools:
  - Bill.com: SMB AP automation
  - Tipalti: Global payments
  - AvidXchange: Mid-market AP
  - Coupa: Enterprise procurement
  - Stampli: AI-powered AP

```
## Step 34: Treasury Operations
```
Daily cash position:
  - Opening balance (all accounts)
  - Inflows (customer payments, investment income)
  - Outflows (payroll, vendor payments, CapEx)
  - Closing balance
  - 7-day forecast

Cash optimization:
  - Zero-balance accounts (sweep excess to master)
  - Notional pooling (offset balances across entities)
  - Cash concentration (centralize for visibility)
  - Investment of excess (money market, T-bills)

Banking relationships:
  - Primary bank: Operating accounts, credit facility
```
## Step 35: Investor Reporting
```
Format: 1-2 page email

Sections:
  1. Highlights (3-5 bullet points)
     - Key wins, milestones, partnerships
  
  2. Lowlights (2-3 bullet points)
     - Challenges, missed targets, risks
  
  3. Key metrics (table format)
     - MRR/ARR and growth
     - Customer count and churn
     - Cash position and runway
     - Headcount
  
```
## Step 36: Financial Compliance
```
Key controls:
  - Revenue recognition (ASC 606)
  - Expense authorization and approval
  - Segregation of duties
  - Access controls (financial systems)
  - Change management (financial applications)
  - Reconciliation (bank, AR, AP, GL)

Documentation:
  - Control descriptions
  - Process narratives
  - Risk-control matrices
  - Testing evidence
  - Remediation plans

```
## Step 37: Financial Planning and Analysis
```
Monthly variance report:
  | Category | Budget | Actual | Variance | % | Explanation |
  |----------|--------|--------|----------|---|-------------|
  | Revenue | $500K | $480K | -$20K | -4% | Slower enterprise deals |
  | COGS | $125K | $130K | +$5K | +4% | Higher hosting costs |
  | R&D | $200K | $195K | -$5K | -2.5% | Delayed hiring |
  | S&M | $150K | $160K | +$10K | +6.7% | Conference sponsorship |
  | G&A | $50K | $48K | -$2K | -4% | Under budget |

Variance investigation:
  - Materiality threshold: >5% or >$10K
  - Root cause analysis for material variances
  - Corrective action plans
  - Forecast adjustment if needed

```
## Step 38: Mergers and Acquisitions
```
Financial:
  □ Audited financials (3 years)
  □ Revenue recognition policies
  □ Customer concentration risk
  □ Contract analysis (terms, renewal rates)
  □ Working capital analysis
  □ Debt and liabilities
  □ Tax compliance and exposure

Operational:
  □ Customer metrics (churn, NPS, satisfaction)
  □ Employee metrics (turnover, satisfaction)
  □ Technology stack and technical debt
  □ IP portfolio (patents, trademarks)
  □ Litigation and legal risks
```
## Step 39: Financial Risk Management
```
Market risk:
  - Currency exposure (FX fluctuations)
  - Interest rate risk (debt costs)
  - Commodity risk (input costs)
  
Credit risk:
  - Customer default (AR collection)
  - Counterparty risk (vendor, partner)
  - Concentration risk (too few customers)
  
Liquidity risk:
  - Cash flow timing (mismatch)
  - Working capital constraints
  - Credit facility availability
  
```
## Step 40: Financial Operations Maturity
```
Level 1: Reactive
  - Manual processes
  - Spreadsheet-based reporting
  - No formal budgeting
  - Ad hoc analysis

Level 2: Defined
  - Basic automation (accounting software)
  - Monthly reporting
  - Annual budgeting
  - Standard metrics tracked

Level 3: Managed
  - Integrated systems (ERP, billing, payroll)
  - Rolling forecasts
```
## Related Skills
  - [sdlc-gtm-strategy](sdlc-gtm-strategy): Go-to-market strategy: market positioning, pricing, packaging, sales enablement, competitive analysi
  - [sdlc-legal-compliance](sdlc-legal-compliance): Software company legal and compliance: GDPR, SOC 2, CCPA, privacy policy, terms of service, data pro
  - [sdlc-hiring-talent](sdlc-hiring-talent): Technical hiring and team building: recruiting, interview design, coding assessments, system design
## Step 34: Financial Planning & Analysis
```
Responsibilities:
  - Budget planning and tracking
  - Forecasting (revenue, expenses, headcount)
  - Variance analysis (actual vs budget)
  - Scenario planning (best/base/worst case)
  - Board reporting and investor updates

Key deliverables:
  - Annual operating plan (AOP)
  - Quarterly forecasts
  - Monthly variance reports
  - Board deck financials
  - Investor update metrics

Tools:
```
## Step 35: Finance Operations Tools
```
Accounting:
  - QuickBooks (small business)
  - Xero (cloud accounting)
  - NetSuite (mid-market)
  - Sage (enterprise)

Billing:
  - Stripe (payments)
  - Chargebee (subscription billing)
  - Recurly (subscription management)
  - Zuora (enterprise billing)

FP&A:
  - Anaplan (enterprise planning)
  - Adaptive Insights (mid-market)
```