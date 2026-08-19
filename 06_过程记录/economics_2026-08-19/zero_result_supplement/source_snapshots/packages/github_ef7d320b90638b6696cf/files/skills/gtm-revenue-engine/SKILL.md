---
name: "gtm-revenue-engine"
description: "Go-to-market and revenue operations engine covering market sizing (TAM/SAM/SOM), ICP definition, pricing strategy, PLG vs SLG decision framework, sales process design, channel strategy, B2B/B2C/marketplace GTM playbooks, enterprise sales, customer acquisition cost optimization, demand generation, content marketing, SEO/SEM, partnership strategy, expansion revenue, and international market entry. Includes India GTM stack with tier 1/2/3 city strategy, WhatsApp commerce, UPI integration, vernacular marketing, India SaaS benchmarks, D2C India playbook, India enterprise sales cycles, and government procurement (GeM portal). Use when user mentions go to market, GTM, sales, pricing, customer acquisition, CAC, LTV, funnel, pipeline, revenue, ARR, MRR, churn, retention, PLG, product led growth, sales led, enterprise sales, channel partner, marketplace, B2B, B2C, D2C, SaaS metrics, conversion, onboarding, activation, demand generation, SEO, content marketing, India market entry, WhatsApp business, UPI, GeM, or any revenue/growth activity."
license: MIT
metadata:
  version: 2.0.0
  author: TechKnowmad AI
  category: go-to-market
  domain: revenue-operations
  updated: 2026-03-22
  frameworks: gtm-strategy, revenue-ops, pricing-strategy, demand-generation
  data-sources: Reforge, First Round Capital, OpenView Partners, Point Nine Capital, SaaStr, Lenny Rachitsky, Kyle Poyar, Tomasz Tunguz, a16z, Bessemer Cloud Index, KeyBanc SaaS Survey, RedSeer India, Bain India Consumer
---

# GTM Revenue Engine

The startup go-to-market and revenue operations system. Data-backed frameworks for finding product-market fit, building repeatable revenue, and scaling from $0 to $100M ARR.

## Keywords

go to market, GTM, sales, pricing, price, customer acquisition, CAC, LTV, CLTV, funnel, pipeline, revenue, ARR, MRR, NRR, GRR, churn, retention, PLG, product led growth, sales led growth, SLG, enterprise sales, channel partner, marketplace, B2B, B2C, B2B2C, D2C, SaaS, conversion, onboarding, activation, demand generation, inbound, outbound, SDR, BDR, AE, account executive, quota, commission, territory, lead scoring, MQL, SQL, PQL, demo, trial, freemium, self-serve, SEO, SEM, content marketing, ABM, account based marketing, partnership, affiliate, referral, viral, network effects, expansion revenue, upsell, cross-sell, land and expand, TAM, SAM, SOM, market sizing, ICP, ideal customer profile, buyer persona, competitive positioning, value proposition, messaging, positioning, pricing model, usage based pricing, seat based, tiered pricing, India, WhatsApp commerce, UPI, GeM, tier 2, tier 3, vernacular, D2C India

---

## How to Use This Skill

This skill operates in **6 modes** based on GTM phase:

| Mode | Trigger | What It Does |
|------|---------|--------------|
| **Size** | "market sizing", "TAM analysis" | TAM/SAM/SOM, ICP definition, competitive mapping |
| **Design** | "GTM strategy", "how to sell" | GTM motion selection, pricing, channel strategy |
| **Build** | "sales process", "build pipeline" | Sales playbook, funnel design, tooling recommendations |
| **Optimize** | "improve conversion", "reduce CAC" | Funnel analysis, pricing optimization, retention |
| **Scale** | "scale sales team", "expand internationally" | Hiring plan, territory design, international expansion |
| **India** | "India market", "sell in India" | India-specific GTM with tier city strategy, payments, vernacular |

**Chain with existing skills:**
- `fundraising-command-center` for metrics investors want to see
- `talent-os` for sales team hiring and compensation
- `ops-scale-engine` for operational scaling behind revenue
- `financial-analysis-dcf-model` for revenue forecasting

---

## 1. Market Sizing Framework

### Bottom-Up TAM/SAM/SOM (Investors Want This, Not Top-Down)

```
TAM (Total Addressable Market):
= Total potential customers × Average revenue per customer per year
  (Everyone who COULD use your solution globally)

SAM (Serviceable Addressable Market):
= TAM filtered by geography, segment, and channels you can reach
  (Everyone you COULD sell to today given your model)

SOM (Serviceable Obtainable Market):
= SAM × Realistic market share in 3-5 years
  (What you'll actually capture — typically 1-5% in early years)
```

**How to Calculate (Bottom-Up Method):**
1. Start with your ICP (specific company profile or consumer segment)
2. Count the number of potential customers matching ICP
3. Estimate annual contract value (ACV) based on pricing
4. TAM = count × ACV
5. SAM = TAM × % you can actually reach
6. SOM = SAM × realistic capture rate (prove with current traction)

### Market Timing Assessment

| Signal | Score (1-5) | Assessment |
|--------|------------|-----------|
| **Technology enabler emerged** | | New tech makes solution possible/affordable |
| **Regulatory tailwind** | | New rules create demand or remove barriers |
| **Behavioral shift** | | Users/buyers changing habits toward your solution |
| **Economic catalyst** | | Market conditions favoring your category |
| **Incumbent vulnerability** | | Legacy players slow to adapt or over-serving |
| **Total** | | >20 = excellent timing, 15-20 = good, <15 = risky |

---

## 2. GTM Motion Selection

### PLG vs SLG vs Hybrid Decision Framework

```
Product-Led Growth (PLG) if:
├── Product value is self-evident (user can experience value in <5 minutes)
├── Low buyer complexity (individual or team decision, not committee)
├── Viral or network effect potential
├── <$5K ACV (typically)
├── Large addressable user base (100K+)
└── Examples: Slack, Notion, Figma, Calendly, Canva

Sales-Led Growth (SLG) if:
├── Complex buying process (multiple stakeholders, procurement)
├── High ACV (>$25K)
├── Requires customization or integration
├── Regulated industry (compliance requirements for buying)
├── Small addressable account base (<5,000 companies)
└── Examples: Salesforce, Snowflake (enterprise tier), Palantir

Hybrid (PLG + SLG) if:
├── PLG for acquisition + sales for expansion
├── Freemium/self-serve for SMB + enterprise sales for large accounts
├── Product qualifies leads that sales closes
└── Examples: Datadog, MongoDB, Twilio, Atlassian
```

### ACV-Based GTM Model

| ACV Range | GTM Motion | Sales Model | Quota:OTE Ratio |
|-----------|-----------|-------------|----------------|
| <$1K | Self-serve PLG | No sales (marketing + product) | N/A |
| $1-5K | PLG + inside sales | SDR → SMB AE | 4-5x |
| $5-25K | Inside sales | SDR → Mid-Market AE | 4-5x |
| $25-100K | Field sales | SDR → Enterprise AE + SE | 4-5x |
| $100K-500K | Enterprise | Named accounts + SE + CSM | 3-4x |
| $500K+ | Strategic | Exec-led, solution engineering | 2-3x |

---

## 3. Pricing Strategy Engine

### Pricing Model Selection

| Model | Best For | Advantages | Risks |
|-------|---------|-----------|-------|
| **Per-seat** | Collaboration tools, CRM | Predictable, easy to understand | Limits adoption, incentivizes fewer seats |
| **Usage-based** | API, infrastructure, data | Aligns with value, scales naturally | Unpredictable revenue, customer anxiety |
| **Tiered (Good/Better/Best)** | Most SaaS | Anchoring, upsell path | Feature packaging complexity |
| **Flat rate** | Simple tools | Easy to buy | Leaves money on table, no expansion |
| **Freemium** | PLG, consumer, developer | Viral, large funnel | Low conversion (2-5%), support cost |
| **Hybrid (seat + usage)** | Modern SaaS | Best of both worlds | Complexity in billing and forecasting |
| **Value-based** | Enterprise, consulting | Captures maximum willingness to pay | Requires strong value quantification |

### Pricing Psychology (Backed by Research)

| Principle | Implementation | Impact |
|-----------|---------------|--------|
| **Anchoring** | Show enterprise plan first (left to right) | +15-20% plan selection |
| **Decoy effect** | Middle plan slightly better value than top | +30% middle plan uptake |
| **9-ending** | $99 vs $100, $299 vs $300 | +8-12% conversion |
| **Annual discount** | 20% off annual vs monthly | +40-60% annual adoption |
| **Social proof** | "Most popular" badge on target plan | +25% target plan selection |
| **Free trial > freemium** | 14-day trial (no credit card) | Higher conversion but smaller funnel |

### Pricing Benchmark Data (2025 SaaS)

| Metric | Bottom Quartile | Median | Top Quartile |
|--------|----------------|--------|-------------|
| Annual price increase | 0-3% | 5-7% | 8-12% |
| Freemium conversion | 1-2% | 2-5% | 5-10% |
| Free trial conversion | 8-15% | 15-25% | 25-40% |
| Net dollar retention | 95-100% | 105-115% | 120-140% |
| Expansion revenue % | 10-20% | 25-35% | 35-50%+ |

---

## 4. Sales Process Architecture

### B2B SaaS Sales Funnel

| Stage | Definition | Benchmark Conversion | Key Metric |
|-------|-----------|---------------------|-----------|
| **Visitor** | Website traffic | - | Unique visitors |
| **Lead** | Provides contact info | 2-5% of visitors | MQLs/month |
| **MQL** | Fits ICP, shows intent | 30-50% of leads | MQL:SQL ratio |
| **SQL/Meeting** | Qualified, discovery complete | 40-60% of MQLs | Discovery calls |
| **Opportunity** | In pipeline, proposal sent | 30-50% of SQLs | Pipeline value |
| **Closed Won** | Signed contract | 20-35% of opportunities | ARR added |

### Sales Team Scaling Model

| ARR | Typical Sales Team | Key Hires |
|-----|--------------------|-----------|
| $0-500K | Founder-led sales | Founders sell, learn the motion |
| $500K-2M | First 1-2 AEs | First sales hire (hunter, not farmer) |
| $2-5M | 3-5 AEs + 1 SDR | Sales manager, first SDR |
| $5-15M | 8-15 AEs + 3-5 SDRs | VP Sales, SE team, sales ops |
| $15-50M | 20-40 AEs + SDRs + CS | CRO, regional leaders, enablement |
| $50M+ | Full go-to-market org | CMO, CRO, CCO alignment |

### Founder-Led Sales Playbook (Stage 1: $0-$1M ARR)

1. **First 10 customers**: Founders sell. Learn objections, pricing sensitivity, buying process
2. **Discovery framework**: MEDDIC (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion)
3. **Document everything**: Record calls, capture objections, map buying committees
4. **Build the playbook**: Standardize what works before hiring first AE
5. **Quota for first AE**: Target 3-5x their OTE in annual bookings
6. **Don't hire VP Sales** until you have 2 AEs hitting quota consistently

---

## 5. Demand Generation Playbook

### Channel Selection Matrix

| Channel | Best For | CAC Range | Time to Results |
|---------|---------|-----------|----------------|
| **SEO/Content** | B2B SaaS, developer tools | Low ($50-200) | 6-12 months |
| **Paid Search (Google)** | High-intent categories | Medium ($100-500) | Weeks |
| **LinkedIn Ads** | B2B enterprise | High ($200-800) | Weeks |
| **Cold Email/Outbound** | Enterprise, high ACV | Medium ($100-400) | 1-3 months |
| **Product viral/referral** | PLG, consumer | Very low ($5-50) | 3-6 months |
| **Community/events** | Developer, niche B2B | Medium ($150-400) | 3-6 months |
| **Partnerships/affiliates** | Marketplace, fintech | Medium ($100-300) | 3-6 months |
| **Social (organic)** | B2C, brand-driven | Low ($20-100) | 3-6 months |

### Content-Led Growth Framework (Most Cost-Effective for Startups)

**The PESO Model:**
- **P — Paid**: Amplify best content, retargeting
- **E — Earned**: PR, guest posts, podcast appearances
- **S — Shared**: Social distribution, community engagement
- **O — Owned**: Blog, newsletter, documentation, YouTube

**Content Funnel:**
| Funnel Stage | Content Type | Goal |
|-------------|-------------|------|
| **TOFU (Awareness)** | Blog, social, podcast, video | Drive traffic, build authority |
| **MOFU (Consideration)** | Case studies, comparisons, webinars | Build trust, educate on solution |
| **BOFU (Decision)** | ROI calculator, demo, free trial, proposal | Convert to customer |

---

## 6. Customer Retention & Expansion

### Retention Metrics Framework

| Metric | Definition | Target (SaaS) |
|--------|-----------|---------------|
| **Logo Churn** | % of customers lost per period | <5% annual (SMB), <2% (enterprise) |
| **Revenue Churn** | % of revenue lost per period | <7% annual gross |
| **Net Revenue Retention (NRR)** | Revenue from existing customers (expansion - churn) | >110% (good), >120% (great), >130% (elite) |
| **Gross Revenue Retention (GRR)** | Revenue kept without expansion | >85% (good), >90% (great) |
| **Time to Value** | Time from signup to first value moment | <5 minutes (PLG), <30 days (enterprise) |
| **DAU/MAU Ratio** | Daily to monthly active user ratio | >25% (engaged), >50% (highly engaged) |

### Expansion Revenue Playbook

| Lever | Description | Typical Impact |
|-------|-------------|---------------|
| **Upsell** | Higher plan/tier | 15-30% of expansion |
| **Cross-sell** | Additional products | 10-20% of expansion |
| **Seat expansion** | More users on same plan | 30-50% of expansion |
| **Usage expansion** | More API calls, storage, etc | 20-40% of expansion |
| **Price increase** | Annual price adjustment (5-10%) | 5-10% of expansion |

---

## 7. India GTM Stack

### India Market Sizing (2025-2026)

| Segment | Market Size | Growth Rate | Key Insight |
|---------|-----------|-------------|------------|
| **India SaaS** | $18-22B revenue | 25-30% CAGR | 5th largest SaaS market globally |
| **India D2C** | $100B+ by 2026 | 35-40% CAGR | 800M+ internet users |
| **India Enterprise Tech** | $50B+ | 15-20% CAGR | Digital India push |
| **India Fintech** | $150B+ | 20-25% CAGR | UPI processed 15B+ txns/month |

### India Tier City Strategy

| Tier | Cities | Strategy | Pricing Sensitivity |
|------|--------|----------|-------------------|
| **Tier 1** | Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Pune, Kolkata | Direct sales, events, enterprise | Lower — willing to pay for quality |
| **Tier 2** | Jaipur, Lucknow, Kochi, Chandigarh, Indore, Coimbatore, Vadodara | Inside sales, digital marketing | Medium — value-conscious |
| **Tier 3** | Smaller cities, semi-urban | Self-serve, WhatsApp, vernacular | High — price is #1 factor |

### India-Specific GTM Channels

| Channel | Reach | Best For | Cost |
|---------|-------|---------|------|
| **WhatsApp Business API** | 500M+ users | D2C, SMB SaaS, commerce | INR 0.50-1.50 per message |
| **Google Ads (India)** | 600M+ searchers | All categories | CPC: INR 5-50 (varies) |
| **Instagram/Meta** | 350M+ users | D2C, lifestyle, consumer | CPM: INR 50-200 |
| **YouTube India** | 500M+ users | Education, consumer, brand | CPV: INR 0.50-2 |
| **LinkedIn India** | 100M+ users | B2B, enterprise, hiring | CPC: INR 50-200 |
| **GeM (Government e-Marketplace)** | Government buyers | B2G, SaaS for govt | Registration required |
| **Vernacular Content** | 500M+ non-English | Tier 2/3, mass market | Low production cost |

### India Payment Integration

| Method | Market Share | Integration | Best For |
|--------|-------------|-------------|---------|
| **UPI** | 70%+ of digital payments | Razorpay, Cashfree, PhonePe biz | All segments |
| **Credit/Debit Card** | 15-20% | Stripe India, Razorpay | Premium/enterprise |
| **Net Banking** | 5-10% | Standard payment gateways | Enterprise |
| **EMI/BNPL** | Growing fast | Simpl, LazyPay, ZestMoney | Consumer, D2C |
| **Cash on Delivery** | Still 30%+ for e-com | Logistics integration | D2C, Tier 2/3 |

### India Enterprise Sales Specifics

- **Sales cycle**: 3-6 months (SMB), 6-18 months (enterprise), 12-24 months (government)
- **Decision making**: Consensus-driven, involve multiple stakeholders early
- **Procurement**: Large companies have formal RFP/vendor registration
- **Government**: GeM registration mandatory, payment cycles: 60-120 days
- **Pricing**: India-specific pricing needed (typically 30-60% of US pricing)
- **Support**: Local language support critical for Tier 2/3
- **Trust signals**: Indian case studies, local references, ISO/SOC certifications valued highly

---

## Reference Files

For detailed playbooks, load:
- [`reference/sales-playbook-templates.md`](reference/sales-playbook-templates.md) — Discovery scripts, objection handling, proposal templates
- [`reference/india-gtm-playbook.md`](reference/india-gtm-playbook.md) — Deep India market entry guide with state-by-state analysis

## Network Science & Pricing Science Layer

### Network Effects Taxonomy (NFX)

Network effects drive 70% of all tech value since 1994. Map your product to 2-4 types:
```
STRONGEST: Physical > Protocol > Personal Utility > Personal
TWO-SIDED: Market Network > Marketplace > Platform > Asymptotic
DATA: Data > Tech Performance
SOCIAL: Language > Belief > Tribal > Expertise > Hub-Spoke
```

### Viral Coefficient Engineering

```
K = i (invites/user) x c (conversion rate)
K>1.0 = true viral (rare) | K=0.5-0.9 = strong | K<0.3 = negligible
CYCLE TIME MATTERS MORE THAN K. Compress join-to-first-invite window.
Levers: embed sharing in core workflow, make invitation valuable to recipient.
```

### Cold Start Solutions (Andrew Chen)

```
1. Come for Tool, Stay for Network (Instagram: filters → social)
2. Win Hard Side First (Uber: guaranteed driver minimums)
3. Atomic Network (Facebook: one campus, not "all students")
4. Concierge Marketplace (DoorDash: founders delivered food)
5. Single-Player Mode (OpenTable: restaurant mgmt → reservations)
```

### Pricing Science

**Van Westendorp:** 4 questions to find optimal price range (too expensive / expensive but consider / bargain / too cheap). Plot curves → intersections reveal optimal price.

**Pricing Psychology:** Decoy effect (3 tiers, middle is target), charm pricing ($49 vs $50), annual framing ($29/mo vs $348/yr), usage-based alignment.

### Category Design (Play Bigger)

Category queens capture 76% of market cap. Protocol: Name the category → Define problem in YOUR terms → Evangelize (thought leadership) → Be the obvious solution.

### Community-Led Growth

```
Level 1: Community as support (reactive)
Level 2: Community as content engine (UGC)
Level 3: Community as acquisition (referrals)
Level 4: Community IS the product (the value)
```

### Forensic User Research (Cognitive Interview)

4 techniques from forensic psychology (3-5x richer data than standard interviews):
1. Context reinstatement: "Take me back to the exact moment..."
2. Report everything: "Tell me every step, even trivial ones"
3. Reverse order: "Walk me through it backward"
4. Perspective change: "How would your boss describe this?"

**Statement Analysis Red Flags:** "I would pay" (conditional = low commitment), pronoun distancing, narrative gaps at decision moments.

### Hitchcock Pitch Technique

Open with the "bomb" (market urgency). Let tension build for 15 minutes. Show how your product defuses the bomb. Investors leave with urgency AND safety. The bomb must never explode in your narrative.
