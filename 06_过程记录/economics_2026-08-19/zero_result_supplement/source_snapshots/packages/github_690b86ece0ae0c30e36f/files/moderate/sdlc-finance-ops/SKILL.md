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

# Finance & Operations

Unit economics, fundraising, financial planning, and operational infrastructure for software companies.

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

### Core Metrics

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

LTV:CAC Ratio
  = LTV / CAC (target: >3:1)

CAC Payback Period
  = CAC / (ARPU × gross margin) (target: <18 months)

NRR (Net Revenue Retention)
  = (start MRR + expansion - contraction - churn) / start MRR × 100

Gross Margin
  = (Revenue - COGS) / Revenue (target: >70% for SaaS)

Burn Multiple
  = Net Burn / Net New ARR (target: <2x)

Rule of 40
  = Revenue growth rate (%) + profit margin (%) > 40%
```

### Unit Economics Example

```
Scenario: B2B SaaS company

ARPU: $500/month
Gross margin: 80%
Monthly churn: 3%
LTV: $500 × 0.80 / 0.03 = $13,333

CAC: $3,000
LTV:CAC = $13,333 / $3,000 = 4.4:1 (healthy)

CAC Payback = $3,000 / ($500 × 0.80) = 7.5 months (great)

NRR: 115% (expansion outpaces churn)
```

### Cohort Analysis

```
Revenue cohorts show if unit economics improve over time:

Cohort Q1 2025: 100 customers, $50K MRR
  Q2 2025: $52K MRR (+4% expansion)
  Q3 2025: $54K MRR (+8% from start)
  Q4 2025: $56K MRR (+12% from start)
  → Healthy expansion revenue

Cohort Q1 2025: 100 customers, $50K MRR
  Q2 2025: $45K MRR (-10% churn)
  Q3 2025: $40K MRR (-20% from start)
  → Churn problem, investigate onboarding
```

## Step 2: Fundraising

### Funding Stages

| Stage | Amount | Traction | Valuation | Dilution |
|-------|--------|----------|-----------|----------|
| **Pre-seed** | $100K-$1M | Idea/prototype | $2-5M | 15-25% |
| **Seed** | $1M-$5M | PMF signal, early revenue | $5-20M | 15-25% |
| **Series A** | $5M-$20M | $1-5M ARR, proven GTM | $20-80M | 15-25% |
| **Series B** | $20M-$50M | $5-20M ARR, scaling | $80-300M | 10-20% |
| **Series C+** | $50M-$200M+ | $20M+ ARR, market leader | $300M+ | 10-15% |
| **IPO** | Public offering | $100M+ ARR, profitable path | Market decides | Varies |

### Fundraising Process

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
   □ Get feedback and interest level

4. Partner Meetings (1-2 weeks)
   □ Present to full partnership
   □ Deep dive on metrics, market, team

5. Due Diligence (2-4 weeks)
   □ Customer references
   □ Technical diligence
   □ Financial audit
   □ Legal review

6. Term Sheet (1 week)
   □ Negotiate terms (valuation, board seats, liquidation prefs)
   □ Sign term sheet
   □ Exclusivity period (30-60 days)

7. Close (4-8 weeks)
   □ Legal documentation
   □ Money wires
   □ Announcement
```

### Pitch Deck Structure

```
1. Title: Company name, one-line description, raise amount
2. Problem: What's broken? Who feels the pain?
3. Solution: How you fix it. Demo screenshot.
4. Market: TAM/SAM/SOM with sources
5. Business model: How you make money
6. Traction: Revenue, growth, key metrics (chart)
7. Competition: Positioning map (not feature matrix)
8. Team: Founders + key hires, relevant experience
9. Financials: Revenue projections, unit economics
10. Ask: How much, what you'll do with it, milestones
```

## Step 3: Financial Planning

### Financial Model Components

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
  - Break-even date
  - Revenue at break-even
```

### Runway Calculation

```
Runway = Cash in bank / Monthly net burn

Example:
Cash: $5M
Monthly revenue: $200K
Monthly expenses: $400K
Net burn: $200K/month
Runway: $5M / $200K = 25 months

Target: Always have 18-24 months of runway
Raise when: 9-12 months remaining (to allow 3-6 months for fundraising)
```

### Headcount Planning

```
Engineering team:
  Engineers: 60% of headcount
  Managers: 10% of headcount
  Product/Design: 15% of headcount
  QA/SDET: 10% of headcount
  DevOps/SRE: 5% of headcount

Revenue per employee target:
  Seed: $100K-$200K per employee
  Series A: $200K-$300K per employee
  Series B+: $300K-$500K per employee
  Public: $500K+ per employee
```

## Step 4: Cap Table & Equity

### Cap Table Example

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

### Equity Best Practices

```
Employee equity grants:
  Junior IC: 0.01-0.05%
  Senior IC: 0.05-0.25%
  Staff IC: 0.1-0.5%
  VP/Director: 0.5-1.5%
  C-level: 1-5%

Vesting: 4 years, 1-year cliff (standard)
Cliff: No equity until 1 year, then 25% vests
Monthly: Remaining 75% vests monthly over 3 years
Acceleration: Single trigger (acquisition) or double trigger (acquisition + termination)
```

## Step 5: Board Management

### Board Meeting Structure

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
   - Headcount, hiring, culture, key departures
   
6. Key Decisions (30 min)
   - Strategic decisions requiring board input
   
7. Executive Session (15 min)
   - Board meets without management
```

### Board Reporting Template

```
Key Metrics Dashboard:
┌───────────────────────────────────────────┐
│  ARR: $2.4M  ↑32% QoQ                    │
│  MRR: $200K  ↑$15K from last month        │
│  Customers: 450  ↑45 net new               │
│  NRR: 112%                                │
│  Burn: $180K/mo  Runway: 22 months        │
│  Headcount: 18  ↑3 this quarter           │
│  NPS: 62                                  │
└───────────────────────────────────────────┘
```

## Step 6: Vendor & Operations

### Vendor Evaluation

```
Criteria for SaaS vendor selection:
1. Security: SOC 2, GDPR compliance, data residency
2. Reliability: SLA, uptime history, incident response
3. Cost: Per-user vs flat rate, annual vs monthly, volume discounts
4. Integration: API quality, SSO, SAML, SCIM
5. Lock-in: Data export, migration support, contract terms
6. Support: Response time, dedicated CSM, escalation path
```

### Insurance Requirements

```
Essential for software companies:
1. General liability ($1M-$2M coverage)
2. Professional liability / E&O ($1M-$5M)
3. Cyber liability ($1M-$10M)
4. D&O (Directors & Officers) — required for board members
5. Workers' compensation — required by law
6. Employment practices liability (EPLI)
7. Key person insurance (for critical founders/employees)
```

## Step 7: Financial Modeling

### SaaS Financial Model Template

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
│ COGS (30%):     Hosting, support, payment processing│
│ R&D (40%):      Engineering headcount + tools        │
│ S&M (20%):      Marketing + sales team + events      │
│ G&A (10%):      Legal, finance, office, insurance    │
└─────────────────────────────────────────────────────┘

Key Outputs:
  Gross margin: 70%
  Burn rate: $150K/month
  Break-even: Month 18
  Revenue at break-even: $250K MRR
```

### Fundraising Financial Model

```
What investors want to see:

1. Revenue trajectory (3-5 year projection)
   - Bottom-up: customers × ARPU (not top-down "1% of $10B market")
   - Conservative, base, optimistic scenarios

2. Unit economics
   - LTV:CAC ratio (and trend)
   - CAC payback period
   - Gross margin per customer

3. Cost structure
   - Headcount plan by department
   - Infrastructure costs (scaling with usage)
   - Marketing spend efficiency

4. Cash management
   - Current burn rate
   - Runway (months remaining)
   - Use of funds breakdown

5. Key assumptions
   - Growth rate assumptions (and why)
   - Churn assumptions (and why)
   - Pricing assumptions (and why)
```

### Use of Funds Template

```
Series A: $15M raise

Engineering (50% — $7.5M):
  - 15 engineers over 18 months
  - Infrastructure scaling
  - Security and compliance

Sales & Marketing (30% — $4.5M):
  - 5 sales reps
  - Marketing campaigns
  - Events and conferences

Operations (15% — $2.25M):
  - G&A team expansion
  - Legal and compliance
  - Office and tools

Reserve (5% — $750K):
  - Unexpected costs
  - Bridge funding if needed
```

## Step 8: Accounting & Tax Basics

### SaaS Revenue Recognition

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
  Balance sheet liability until performance obligation met
```

### Key Tax Considerations

```
1. R&D Tax Credit: 20% of qualifying R&D expenses
   - Engineering salaries
   - Cloud infrastructure for development
   - Contractor costs for R&D
   
2. State Nexus: Sales tax obligations by state
   - Economic nexus thresholds (typically $100K+ revenue or 200+ transactions)
   - SaaS taxability varies by state
   
3. International: VAT/GST for non-US customers
   - EU: Digital services VAT (typically 20%)
   - Use tax automation (Stripe Tax, Avalara, TaxJar)
   
4. Equity: 409A valuation for stock options
   - Required before granting options
   - Updated every 12 months or after material events
   - Cost: $5K-$15K per valuation
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

### Board Meeting Agenda Template

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
   - Product roadmap progress
   - Key launches and metrics
   - Customer feedback themes

4. Go-to-Market Update (20 min)
   - Sales pipeline and conversion
   - Marketing performance
   - Customer success metrics

5. People Update (15 min)
   - Headcount plan vs actual
   - Key hires and departures
   - Culture/engagement metrics

6. Strategic Discussion (30 min)
   - [Topic 1: e.g., pricing change]
   - [Topic 2: e.g., international expansion]
   - [Topic 3: e.g., fundraising timeline]

7. Executive Session (15 min)
   - Board only (management exits)
   - CEO performance review
   - Compensation discussion

8. Action Items & Next Steps (5 min)
```

### Board Deck Best Practices

```
Format:
  - PDF, 15-25 slides max
  - Send 48-72 hours before meeting
  - Use appendix for detailed data
  - Consistent design template

Slide structure:
  1. Title slide
  2. Executive summary (1 page)
  3. Key metrics dashboard
  4. Financial summary
  5-7. Department updates
  8-10. Strategic discussion topics
  11. Appendix (detailed data)

Anti-patterns:
  ❌ Wall of text (use charts)
  ❌ Too many metrics (focus on 5-7)
  ❌ No context (show trends, benchmarks)
  ❌ Surprises (bad news shared before meeting)
  ❌ No discussion topics (board wants strategy, not status)
```

## Step 13: Fundraising Process

### Data Room Checklist

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
      - Revenue breakdown by customer
      
    /03-product
      - Product roadmap
      - Technical architecture
      - Security certifications
      - Patent applications
      
    /04-market
      - TAM/SAM/SOM analysis
      - Competitive landscape
      - Customer case studies
      - Analyst reports
      
    /05-team
      - Org chart
      - Key team bios
      - Hiring plan
      - Employee handbook


- Bessemer Cloud Atlas: https://www.bvp.com/atlas
- OpenView SaaS Benchmarks: https://openviewpartners.com/blog/
- a16z Startup School: https://a16z.com/startup-school/
- Carta (cap table): https://carta.com/
- Holloway Equity Guide: https://www.holloway.com/g/equity-compensation
- SaaStr (SaaS metrics): https://www.saastr.com/
- Christoph Janz (SaaS metrics): https://christophjanz.blogspot.com/
- Tomasz Tunguz (SaaS): https://tomtunguz.com/
- YC Fundraising Guide: https://www.ycombinator.com/library
- Brad Feld, Venture Deals: https://www.feld.com/archives/2019/06/venture-deals-4th-edition.html


## Step 17: Revenue Operations (RevOps)

### RevOps Framework

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

Reporting:
  - Revenue dashboard (real-time)
  - Pipeline forecast (weekly)
  - Cohort analysis (monthly)
  - Board reporting (quarterly)
```

### Pipeline Management

```
Pipeline stages:
  1. Prospect (10%): Initial contact, qualifying
  2. Discovery (20%): Needs assessment, demo scheduled
  3. Evaluation (40%): Demo completed, proposal sent
  4. Negotiation (60%): Terms discussed, legal review
  5. Commit (80%): Verbal agreement, contract in process
  6. Closed Won (100%): Contract signed
  7. Closed Lost (0%): Lost to competitor, no decision

Pipeline hygiene:
  - Weekly pipeline review (sales manager + reps)
  - Stale deal cleanup (no activity in 30 days)
  - Stage validation (must meet criteria to advance)
  - Win/loss analysis (monthly)
  - Forecast accuracy tracking

Key metrics:
  - Pipeline coverage: Pipeline value / quota (3-4x healthy)
  - Win rate: Closed won / (closed won + closed lost)
  - Average deal size: Total revenue / # deals
  - Sales cycle: Average days from opportunity to close
  - Pipeline velocity: (# opportunities × win rate × avg deal) / cycle
```

## Step 18: Financial Reporting

### Monthly Financial Package

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
     - Liabilities (current and long-term)
     - Equity
     
  4. Cash flow statement
     - Operating activities
     - Investing activities
     - Financing activities
     
  5. Key metrics dashboard
     - ARR/MRR and growth
     - Gross margin
     - Burn rate and runway
     - Headcount and cost per employee
     
  6. Variance analysis
     - Revenue variances (volume, price, mix)
     - Expense variances (spending, timing, headcount)
     - Action items for significant variances
```

### Board Reporting Template

```
Quarterly board deck (15-20 slides):

1. CEO update (2 slides)
   - Quarter highlights
   - Strategic priorities
   
2. Financial summary (3 slides)
   - Revenue and growth
   - Profitability metrics
   - Cash position and runway
   
3. Product update (3 slides)
   - Roadmap progress
   - Key metrics (usage, engagement)
   - Customer feedback themes
   
4. GTM update (3 slides)
   - Sales performance
   - Marketing metrics
   - Customer success metrics
   
5. People update (2 slides)
   - Headcount and hiring
   - Culture and engagement
   
6. Strategic discussion (2-3 slides)
   - Key decisions needed
   - Market opportunities
   - Risk assessment


## Step 19: Treasury Management

### Cash Management

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
  - Credit facility (revolving line of credit)

Investment policy:
  - Overnight: Fed funds, reverse repo
  - Short-term: T-bills, money market
  - Medium-term: Corporate bonds, CDs
  - Risk tolerance: Conservative (preserve capital)
```

### Working Capital Management

```
Working capital = Current assets - Current liabilities

Components:
  Accounts receivable (AR):
    - DSO (Days Sales Outstanding) target: <30 days
    - Aging buckets: Current, 30, 60, 90+ days
    - Collection process: Reminder then Escalation then Collections agency
    
  Accounts payable (AP):
    - DPO (Days Payable Outstanding) target: 45-60 days
    - Early payment discounts: Evaluate 2/10 net 30
    - Vendor payment terms: Negotiate extended terms
    
  Inventory (if applicable):
    - DIO (Days Inventory Outstanding) target: <30 days
    - Safety stock: 2 weeks of demand
    - Just-in-time ordering

Cash conversion cycle:
  CCC = DSO + DIO - DPO
  Target: <30 days (or negative for SaaS)
```

## Step 20: Financial Systems

### Tech Stack for Finance

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
  - Revenue recognition: Softrax, RevPro

Integration:
  - iPaaS: Workato, Tray.io, Zapier
  - API connectors: Plaid (banking), Codat (accounting)
  - Custom: REST APIs, webhooks
```

## Step 21: Fundraising Operations

### Due Diligence Preparation

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

### SaaS Dashboard Metrics

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
    
  Net Revenue Retention (NRR):
    = (Beginning MRR + Expansion - Churn - Contraction) / Beginning MRR x 100
    Good: >100% (expansion > churn)
    Excellent: >120%

Efficiency metrics:
  CAC (Customer Acquisition Cost):
    = Total S&M spend / New customers acquired
    
  CLV (Customer Lifetime Value):
    = ARPU x Gross margin x (1 / Monthly churn rate)
    
  CLV:CAC Ratio:
    = CLV / CAC
    Good: >3:1
    
  CAC Payback Period:
    = CAC / (ARPU x Gross margin)
    Good: <12 months
    
  Magic Number:
    = Net new ARR / S&M spend (prior quarter)
    Good: >0.75
    Excellent: >1.0
    
  Burn Multiple:
    = Net burn / Net new ARR
    Good: <2
    Excellent: <1
```

### Revenue Recognition

```
ASC 606 (Revenue from Contracts):
  Step 1: Identify the contract
  Step 2: Identify performance obligations
  Step 3: Determine transaction price
  Step 4: Allocate price to obligations
  Step 5: Recognize revenue when obligations satisfied

SaaS-specific:
  Subscription revenue: Recognized ratably over term
  Setup fees: Recognized over expected customer life
  Usage fees: Recognized when consumed
  Professional services: Recognized on completion or over time

Example:
  Annual contract: $120,000
  Monthly recognition: $10,000
  Setup fee: $24,000 over 24-month expected life = $1,000/month
  
  Total monthly revenue: $11,000

Tools:
  - Softrax, RevPro, Zuora RevRec
  - NetSuite Advanced Revenue Management
  - Sage Intacct Revenue Recognition
```

## Step 23: Fundraising Strategy

### Funding Stages

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
  Amount: $5M-$20M
  Stage: Product-market fit, repeatable revenue
  Investors: VC firms (a16z, Sequoia, Accel)
  Terms: Priced round with board seat
  Dilution: 15-25%

Series B:
  Amount: $20M-$50M
  Stage: Scaling, market expansion
  Investors: Growth-stage VCs
  Terms: Priced round, multiple board seats
  Dilution: 10-20%

Series C+:
  Amount: $50M+
  Stage: Market leadership, profitability path
  Investors: Growth equity, crossover funds
  Terms: Priced round, governance provisions
  Dilution: 5-15%
```

### Investor Pitch Structure

```
Slide 1: Title (company name, one-liner, your name)
Slide 2: Problem (what pain exists, who feels it)
Slide 3: Solution (what you built, how it works)
Slide 4: Market (TAM, SAM, SOM with sources)
Slide 5: Product (demo screenshots, key features)
Slide 6: Traction (revenue, growth, customers, metrics)
Slide 7: Business model (how you make money)
Slide 8: Competition (positioning matrix)
Slide 9: Team (founders + key hires, relevant experience)
Slide 10: Financials (3-year projections, key assumptions)
Slide 11: Ask (amount raised, use of funds, milestones)
Slide 12: Appendix (detailed financials, customer testimonials)

Tips:
  - 10-12 slides, 20 minutes max
  - One idea per slide
  - More visuals, less text
  - Practice 10+ times
  - Have backup slides for deep-dive questions
```

## Step 24: Cap Table Management

### Cap Table Structure

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
  | Total       | 10,000,000 | 100% |

Dilution impact:
  Each round dilutes existing shareholders
  Series A (20% dilution): Founders go from 72% to ~58%
  Series B (15% dilution): Founders go from 58% to ~49%
  
  Employee pool: Typically expanded each round (10-15% of total)

Tools:
  - Carta: Cap table management (most popular)
  - Pulley: Cap table + equity management
  - Shareworks: Enterprise equity management
  - AngelList Stack: Early-stage cap table


## Step 25: Financial Modeling

### Three-Statement Model

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
    - R&D (engineering, product, design)
    - S&M (sales, marketing, CS)
    - G&A (admin, legal, finance, HR)
  = Operating Income (EBITDA + SBC)
  
  Other Income/Expenses
    - Interest income/expense
    - Foreign exchange gains/losses
  = Income Before Tax
  
  Tax
  = Net Income

Balance Sheet:
  Assets
    - Cash and equivalents
    - Accounts receivable
    - Prepaid expenses
    - Property and equipment
    - Intangible assets (IP, goodwill)
  
  Liabilities
    - Accounts payable
    - Accrued expenses
    - Deferred revenue
    - Debt
  
  Equity
    - Common stock
    - Additional paid-in capital
    - Retained earnings

Cash Flow Statement:
  Operating Activities
    - Net income
    - Adjustments (D&A, SBC, changes in working capital)
  
  Investing Activities
    - CapEx
    - Acquisitions
    - Investments
  
  Financing Activities
    - Debt proceeds/repayment
    - Equity issuance
    - Dividends
```

### Scenario Planning

```
Base case:
  - Revenue growth: 50% YoY
  - Gross margin: 75%
  - Operating margin: -20% (investing in growth)
  - Cash runway: 24 months
  - Hiring: 50 new employees

Bull case:
  - Revenue growth: 80% YoY (strong market, product-market fit)
  - Gross margin: 78%
  - Operating margin: -10%
  - Cash runway: 30 months
  - Hiring: 70 new employees

Bear case:
  - Revenue growth: 20% YoY (market slowdown)
  - Gross margin: 72%
  - Operating margin: -35%
  - Cash runway: 18 months
  - Hiring: 20 new employees

Worst case:
  - Revenue growth: -10% YoY (churn spike)
  - Gross margin: 68%
  - Operating margin: -50%
  - Cash runway: 12 months
  - Hiring: Freeze
  - Action: Cost reduction plan, bridge round
```

## Step 26: Cost Accounting

### Unit Economics by Product Line

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
  CLV:CAC: 16.4:1
  Payback: $500 / ($199 x 0.824) = 3.0 months

Product C (Enterprise):
  ARPU: $2,000/month
  COGS: $300/month (hosting: $100, support: $120, payment: $80)
  Gross margin: 85%
  CAC: $15,000
  CLV: $2,000 x 0.85 x (1/0.01) = $170,000
  CLV:CAC: 11.3:1
  Payback: $15,000 / ($2,000 x 0.85) = 8.8 months

Insight: Product B has best unit economics (highest CLV:CAC)
Action: Increase marketing spend on Pro plan acquisition
```

## Step 27: Investor Relations

### Monthly Investor Update Template

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
  | Runway | X months | Y months | |

Lowlights:
  - [Challenge 1 + mitigation plan]
  - [Challenge 2 + mitigation plan]

Asks:
  - [Specific ask from investors: intros, advice, hiring]

Next month priorities:
  1. [Priority 1]
  2. [Priority 2]
  3. [Priority 3]
```

### Board Reporting Best Practices

```
Frequency: Monthly update (email), Quarterly board meeting

Monthly update:
  - 1-2 pages max
  - Key metrics dashboard
  - Highlights and lowlights
  - Specific asks

Quarterly board meeting:
  - 15-20 slides
  - Send 48-72 hours in advance
  - CEO presents, team presents their areas
  - 2-3 hours total
  - Strategic discussion (not just status update)
  - Action items with owners and deadlines

Anti-patterns:
  - Surprises (bad news shared before meeting)
  - Wall of text (use charts and visuals)
  - Too many metrics (focus on 5-7)
  - No discussion topics (board wants strategy)
  - No follow-up (action items tracked)
```

## Step 28: Exit Planning

### Exit Types

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
  
  Timeline: 12-18 months
  Costs: $5-10M (legal, accounting, underwriting)

Acquisition:
  Types:
    - Strategic: Buyer wants technology/market position
    - Financial: PE firm buying for returns
    - acqui-hire: Buying team, not product
  
  Process:
    1. Investment banker engagement
    2. Buyer outreach and interest
    3. Letter of intent (LOI)
    4. Due diligence (60-90 days)
    5. Purchase agreement
    6. Closing
  
  Timeline: 6-12 months
  Costs: 1-3% of deal value (banker fees)

Secondary sale:
  - Sell shares to secondary market
  - Platforms: Forge, EquityZen, Nasdaq Private Market
  - Typically 20-40% discount to last round valuation
  - Requires company approval


## Step 29: Financial Analysis

### Profitability Analysis

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
  S&M: $2.5M (25% of revenue)
  G&A: $1M (10% of revenue)
  Operating income: $1M
  Operating margin: 10%

Improvement levers:
  - Reduce hosting costs (optimize infrastructure)
  - Improve payment processing rates (negotiate)
  - Automate support (reduce ticket volume)
  - Increase revenue without proportional cost increase
```

### Cash Flow Analysis

```
Operating cash flow:
  Net income: $1M
  Add back: D&A: $200K
  Add back: SBC: $500K
  Working capital changes:
    AR increase: -$300K
    AP increase: $100K
    Deferred revenue: $400K
  Operating cash flow: $1.9M

Free cash flow:
  Operating cash flow: $1.9M
  CapEx: -$500K
  Free cash flow: $1.4M

Cash flow metrics:
  FCF margin: 14%
  FCF conversion: 140% (of net income)
  Cash burn rate: N/A (positive FCF)
  Runway: Infinite (profitable)
```

## Step 30: Financial Reporting Automation

### Reporting Stack

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
  - Google Sheets: Quick analysis
  - Mosaic/Jirav: FP&A platforms
  - Notion/Airtable: Collaborative reporting

Automation:
  - Scheduled data pulls (daily)
  - Automated report generation (weekly)
  - Email distribution (monthly)
  - Alert triggers (anomaly detection)
```

### Board Reporting Package

```
Monthly board update:
  1. Executive summary (1 page)
     - Key highlights and lowlights
     - Cash position and runway
     - Revenue vs plan
  
  2. Financial dashboard (1 page)
     - ARR/MRR and growth
     - Gross margin trend
     - Burn rate and runway
     - Headcount and cost per employee
  
  3. Business metrics (1 page)
     - Customer acquisition
     - Retention and churn
     - NPS and satisfaction
     - Product usage
  
  4. Key decisions needed (1 page)
     - Strategic questions for board
     - Resource allocation decisions
     - Partnership/investment opportunities

Quarterly board meeting:
  - 15-20 slides
  - Deep dive on strategy
  - Financial model review
  - Market and competitive analysis
  - Team and culture update
```

## Step 31: Audit Preparation

### Audit Readiness Checklist

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
  □ Approval workflows in place
  □ Access controls reviewed
  □ Vendor contracts current
  □ Insurance policies current
  □ Compliance certifications valid

Preparation timeline:
  - 3 months before: Clean up books, reconciliations
  - 2 months before: Prepare schedules, documentation
  - 1 month before: Pre-audit meeting, scope agreement
  - Audit period: Support auditor requests
  - Post-audit: Address findings, implement recommendations
```

## Step 32: Financial Modeling Tools

### Spreadsheet Best Practices

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
  - Conditional formatting (alerts)
  - Error checks (IFERROR, ISERROR)
  - Cross-footing (row and column totals match)
  - Version control (save with dates)

Tools:
  - Excel/Google Sheets: Standard
  - Causal: Collaborative financial modeling
  - Mosaic: FP&A automation
  - Jirav: Financial planning
  - Datarails: Excel-based FP&A


## Step 33: Financial Operations Automation

### Accounts Payable Automation

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

Benefits:
  - 80% reduction in manual processing
  - Early payment discounts captured
  - Fraud detection (duplicate invoices)
  - Audit trail (complete history)
  - Cash flow visibility
```

### Accounts Receivable Automation

```
Invoice generation:
  1. Usage data collected (API calls, storage, seats)
  2. Billing rules applied (tiers, discounts, proration)
  3. Invoice generated (PDF, email)
  4. Payment processed (auto-charge, manual)
  5. Reminders sent (overdue notices)
  6. Collections escalated (if needed)

Tools:
  - Stripe Billing: Subscription and usage billing
  - Chargebee: Subscription management
  - Zuora: Enterprise billing
  - Recurly: Subscription billing
  - Maxio: SaaS billing

Dunning strategy:
  Day 1: Payment failed notification
  Day 3: Retry payment + email
  Day 7: Second retry + warning
  Day 14: Account downgrade notice
  Day 30: Account suspension notice
  Day 60: Collections agency referral
```

## Step 34: Treasury Operations

### Cash Management

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
  - Secondary bank: Backup, diversification
  - International banks: Local currency accounts
  - Review annually: Fees, service, relationship

FX management:
  - Natural hedging (match revenue and costs by currency)
  - Forward contracts (lock in rates for known exposures)
  - Options (protect against adverse moves)
  - Netting (offset intercompany flows)
```

## Step 35: Investor Reporting

### Monthly Investor Update

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
  
  4. Asks (1-3 specific requests)
     - Introductions, advice, hiring help
  
  5. Next month priorities (3-5 items)

Frequency: Monthly (1st week of month)
Length: 500-800 words
Tone: Transparent, honest, concise
```

### Board Meeting Preparation

```
Pre-meeting (2 weeks before):
  □ Schedule meeting and send calendar invite
  □ Request agenda items from board members
  □ Prepare financial package
  □ Draft strategic discussion topics
  □ Send materials 48-72 hours in advance

Meeting structure (2-3 hours):
  1. CEO update (15 min)
  2. Financial review (30 min)
  3. Product update (20 min)
  4. GTM update (20 min)
  5. People update (15 min)
  6. Strategic discussion (30-45 min)
  7. Executive session (15 min, board only)

Post-meeting (1 week after):
  □ Send meeting notes and action items
  □ Track action item completion
  □ Update board on progress (next monthly update)
```

## Step 36: Financial Compliance

### SOX Compliance (if applicable)

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

Timeline:
  - Annual risk assessment
  - Quarterly control testing
  - Continuous monitoring
  - External audit (annual)
```

### Tax Planning

```
R&D tax credit:
  - Qualifying expenses: wages, supplies, contract research
  - Credit: 6-8% of qualifying expenses
  - Startup provision: Offset payroll tax (up to $500K)
  - Documentation: Time tracking, project records

Transfer pricing:
  - Arm's length principle
  - Documentation requirements
  - Country-by-country reporting
  - Advance pricing agreements

Tax-efficient structure:
  - IP holding company (Ireland, Singapore)
  - Cost-sharing arrangements
  - Stock-based compensation deductions
  - Net operating loss utilization


## Step 37: Financial Planning and Analysis

### Budget Variance Analysis

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

Reporting cadence:
  - Weekly: Flash report (revenue, cash)
  - Monthly: Full variance analysis
  - Quarterly: Forecast update
  - Annually: Budget for next year
```

### Rolling Forecast

```
12-month rolling forecast:
  - Update monthly (add new month, drop oldest)
  - Level of detail: Monthly for next 3 months, quarterly for rest
  - Drivers: Revenue (pipeline), Expenses (headcount plan)
  - Scenarios: Base, upside, downside

Forecast accuracy tracking:
  - Measure: Actual vs forecast (MAPE - Mean Absolute Percentage Error)
  - Target: <10% MAPE for revenue, <5% for expenses
  - Improvement: Track accuracy over time, adjust methodology

Tools:
  - Mosaic: Automated forecasting
  - Jirav: Financial planning
  - Datarails: Excel-based FP&A
  - Adaptive Planning: Enterprise planning
```

## Step 38: Mergers and Acquisitions

### Due Diligence Checklist

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

Valuation:
  □ DCF model (discounted cash flow)
  □ Comparable company analysis
  □ Precedent transactions
  □ Synergy analysis
  □ Accretion/dilution analysis
```

### Post-Merger Integration

```
Integration phases:
  Day 1: Legal close, announce, leadership alignment
  Week 1: Systems access, communication, team introductions
  Month 1: Process alignment, tool consolidation, org design
  Month 3: Cultural integration, metric alignment, synergy tracking
  Month 6: Full integration, synergy realization, performance review

Key workstreams:
  - Technology: System integration, data migration
  - People: Org design, retention, culture
  - Process: Workflow alignment, tool consolidation
  - Customers: Communication, account management
  - Finance: Reporting consolidation, synergy tracking

Synergy tracking:
  - Revenue synergies: Cross-sell, upsell, market expansion
  - Cost synergies: Headcount, vendor consolidation, real estate
  - Timeline: When synergies are expected to materialize
  - Accountability: Owner for each synergy initiative
```

## Step 39: Financial Risk Management

### Risk Categories

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
  
Operational risk:
  - Fraud (internal, external)
  - System failure (accounting, billing)
  - Process failure (errors, omissions)

Risk mitigation:
  - Hedging: FX forwards, interest rate swaps
  - Insurance: D&O, E&O, cyber, key person
  - Diversification: Customer, vendor, market
  - Controls: Segregation of duties, approval workflows
```

## Step 40: Financial Operations Maturity

### Maturity Model

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
  - Variance analysis
  - KPI dashboards

Level 4: Optimized
  - Advanced analytics (predictive, prescriptive)
  - Real-time reporting
  - Automated compliance
  - Strategic FP&A partnership

Level 5: Leading
  - AI-powered insights
  - Continuous planning
  - Proactive risk management
  - Financial innovation

Assessment:
  - Evaluate current state per dimension
  - Identify gaps
  - Prioritize improvements
  - Create roadmap
```

## Related Skills

  - [sdlc-gtm-strategy](sdlc-gtm-strategy): Go-to-market strategy: market positioning, pricing, packaging, sales enablement, competitive analysi
  - [sdlc-legal-compliance](sdlc-legal-compliance): Software company legal and compliance: GDPR, SOC 2, CCPA, privacy policy, terms of service, data pro
  - [sdlc-hiring-talent](sdlc-hiring-talent): Technical hiring and team building: recruiting, interview design, coding assessments, system design 


## Step 34: Financial Planning & Analysis

### FP&A Function

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
  - Excel/Google Sheets (modeling)
  - Anaplan/Adaptive (enterprise planning)
  - Mosaic/Runway (startup FP&A)
  - QuickBooks/Xero (accounting)
  - Stripe/Chargebee (billing)
```

### Financial Reporting Package

```
Monthly close package:
  - Income statement (actual vs budget)
  - Balance sheet
  - Cash flow statement
  - Key metrics dashboard
  - Variance analysis commentary

Quarterly board package:
  - Financial summary (YTD + forecast)
  - Key metrics trends
  - Cash runway analysis
  - Scenario analysis
  - Capital allocation update

Annual planning package:
  - Revenue model (bottom-up)
  - Expense budget (by department)
  - Headcount plan
  - Capital expenditure plan
  - Funding requirements


## Step 35: Finance Operations Tools

### Tool Stack

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
  - Mosaic (startup FP&A)
  - Runway (startup planning)

Expense management:
  - Brex (corporate card + expenses)
  - Ramp (expense management)
  - Expensify (expense reporting)
  - Divvy (budget management)
