---
name: performing-financial-analysis
description: Analyzes financial statements, profit & loss reports, and models pricing strategies for solo-founder SaaS products. Utilizes a comprehensive 5-phase structured analysis, quantitative ratio tracking, and Discounted Cash Flow (DCF) enterprise valuation with sensitivity analysis.
allowed-tools: [Read, Write, Edit, Glob]
---

# Performing Financial Analysis

## Goal
To audit financial metrics, evaluate P&L statements, perform quantitative ratio analysis, model Discounted Cash Flows (DCF), construct short-term rolling forecasts, and provide pricing proposals tailored for solo founders.

## When to Use This Skill
- When analyzing monthly profit and loss (P&L) statements or budgeting categories.
- When performing expert-level Discounted Cash Flow (DCF) valuations.
- When testing pricing tiers, seat allocation models, and rolling forecasts.
- When analyzing runway, burn rate, liquidity ratios, and variance margins.

### Do Not Use This Skill For:
- Complex public accounting or statutory corporate tax filing.

## The 5-Phase Financial Analysis Workflow

```text
       Scope                  Model                  Insight                 Report                Follow-up
 ┌───────────────┐      ┌───────────────┐      ┌───────────────┐        ┌───────────────┐      ┌───────────────┐
 │   Identify    │      │  Validate P&L │      │ Ratio Trends  │        │   Executive   │      │ Track Accuracy│
 │ Objectives &  │ ───▻ │ Input Schemas │ ───▻ │ Bull & Bear   │  ───▻  │   Summaries   │ ───▻ │    KPIs      │
 │ Frames (1)    │      │  & DCF (2)    │      │ Scenarios (3) │        │  & Tables (4) │      │  Revenues (5) │
 └───────────────┘      └───────────────┘      └───────────────┘        └───────────────┘      └───────────────┘
```

1. **Phase 1: Scoping**
   - Establish valuation or auditing parameters. Determine materiality thresholds, relevant tracking periods (MRR vs LTV), and choose analytical frameworks (CAPM, DCF, Du Pont).
2. **Phase 2: Data Analysis & Modeling**
   - Gather historical financial statement categories. Validate input JSON/CSV profiles ensuring there are no overlapping or mixed accounting periods.
   - Run ratio calculations. Ensure technical limits (e.g., Terminal Growth Rate $\le$ long-run nominal GDP growth) are rigidly satisfied.
3. **Phase 3: Insight Generation**
   - Diagnose root causes for material budget variances (favorable/unfavorable breakdowns).
   - Evaluate Bull/Bear pricing sensitivity ranges and ensure WACC variance meshes exceed $\pm15\%$ boundaries.
4. **Phase 4: Reporting**
   - Formulate executive reports, budget tables, sensitivity projections, and P&L summaries.
5. **Phase 5: Follow-up**
   - Document rolling forecasting parameters to track model error tolerances (aiming for $\pm5\%$ revenue and $\pm3\%$ overhead variance).

## Design Rules & Guidelines

### Metric Definition Constraints
- **Gross Margin** = (Revenue - Direct Server/Sub Costs) / Revenue
- **Net Margin** = (Revenue - Total Expenses including Ads) / Revenue
- **Burn Rate** = Total Expenses - Revenue [if expenses > revenue]
- **Current Ratio** = Current Assets / Current Liabilities (Liquidity Measure)
- **Terminal Value (DCF)** = $[Active\ Cash\ Flow \times (1 + g)] / [WACC - g]$ where $g \le$ long-run GDP growth rate (capped at 3.0%).

### Strategic Advisory Rules
- Never make blind assumptions about business metrics. Direct ad-spend that exceeds 50% of monthly revenue must trigger an immediate analytical risk alert.
- Always recommend per-seat pricing for corporate/HR SaaS platforms due to corporate user-scaling behavior, combined with a value-based incentive structure.
- Budget variance alerts must highlight any category experiencing variance $> 10\%$ vs. projection.

## Example Implementation Checklist
Copy this checklist during financial auditing sessions:

- [ ] Gather monthly revenue, category-wise expenses, and balance liabilities.
- [ ] Establish the scoping goal (e.g., DCF model, budget variance audit, P&L evaluation).
- [ ] Compute Gross Margin, Net Margin, Current Ratio, and monthly Burn Rate.
- [ ] Map historical statements to input spreadsheets cleanly with no overlapping periods.
- [ ] For valuations, build a WACC sensitivity table spanning $\pm15\%$ variance intervals.
- [ ] Highlight budget variance categories exceeding the $10\%$ target threshold.
- [ ] Validate that the terminal growth rate ($g$) is less than or equal to local central bank long-run nominal GDP forecasts.
- [ ] Propose flat vs. user-seat pricing options with pros, cons, and user expansion paths.
- [ ] Issue immediate margin efficiency warnings if ad spending exceeds $50\%$ of revenues.
- [ ] Compile the final analysis with a professional, objective, mathematically sound layout.
