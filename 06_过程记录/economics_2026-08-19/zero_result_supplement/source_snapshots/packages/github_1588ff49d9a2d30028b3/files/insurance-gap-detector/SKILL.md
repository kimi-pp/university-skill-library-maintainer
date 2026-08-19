# insurance-gap-detector

**Skill #157 — Insurance Gap Detector**

Analyzes all properties in the portfolio for coverage gaps, policy lapses, amounts vs. current values, and wrong policy types. Flags underinsured properties before a claim reveals the problem.

## Trigger Phrases
- "Check my insurance coverage"
- "Am I underinsured on any properties?"
- "Insurance gap analysis"
- "Audit my insurance portfolio"
- "Which properties have coverage gaps?"
- "Do I have the right policy type on my rentals?"
- "Insurance review"
- "Check if I need landlord policies vs. homeowner"
- "Flag any insurance lapses"
- "Insurance coverage audit"

## Inputs
- Property list (address, property type, estimated value, occupancy status)
- Current policies for each property:
  - Carrier name
  - Policy type (homeowner/HO-3, landlord/DP-3, commercial, vacant, STR/Airbnb)
  - Dwelling coverage amount
  - Liability coverage amount
  - Deductible
  - Renewal date
  - Annual premium
- Loan requirements (lender-required coverage minimums, if applicable)
- Optional: replacement cost estimates (from recent appraisals or contractor)

## Gap Detection Framework

### Type 1 — Wrong Policy for Property Use
| Situation | Required Policy | Common Mistake |
|-----------|----------------|----------------|
| Tenant-occupied rental | DP-3 (Landlord/Dwelling) | HO-3 (Homeowner) — VOIDS claims |
| STR/Airbnb | STR endorsement or specialty policy | Standard DP-3 — usually excluded |
| Vacant property | Vacant dwelling policy | Standard HO or DP — typically lapses after 30-60 days vacant |
| Commercial rental | Commercial Property (CP) | Residential DP-3 — wrong form |
| Mixed-use | Commercial + liability umbrella | Residential only |

**Flag**: Any rental property with an HO-3 policy → High risk, claim denial likely

### Type 2 — Underinsurance
80% Rule: Dwelling coverage must be ≥80% of replacement cost or insurer can pro-rate claims.

**Calculation:**
```
Replacement cost estimate: $275,000
80% threshold: $220,000
Current coverage: $180,000 → UNDERINSURED by $40,000
```

Replacement cost benchmarks (rough):
- Standard residential: $150-225/sq ft (varies by market)
- High-end/custom: $225-400/sq ft
- Commercial: $200-350/sq ft
- Use local contractor estimate or Marshall & Swift (professional standard)

Flag: Any property where insured value < 80% of estimated replacement cost

### Type 3 — Liability Gaps
Minimum recommended liability coverage:
- Single-family rental: $300,000 per occurrence
- Multi-family (2-4 units): $500,000
- 5+ units: $1M commercial + umbrella
- Commercial: $1M per occurrence + umbrella

Flag: Any property below threshold OR any portfolio with no umbrella policy

### Type 4 — Lapse Risk
Flag properties where:
- Renewal date < 30 days away (with no renewal confirmation)
- Policy lapsed (renewal date in past, no new policy on file)
- Vacancy exceeds policy's vacancy clause (typically 30-60 days)

### Type 5 — Missing Coverages
Check each policy for:
- [ ] Loss of rents / fair rental value coverage (when tenant can't occupy due to covered loss)
- [ ] Water backup / sewer endorsement
- [ ] Equipment breakdown (HVAC, water heater)
- [ ] Umbrella / excess liability
- [ ] Flood (if in flood zone — check FEMA FIRM maps)
- [ ] Earthquake (if in seismic zone)
- [ ] Builder's risk (if under active rehab)

## Output Format

**Summary:**
> "Portfolio insurance audit — 12 properties. 3 gaps found: (1) 456 Oak Ave has homeowner policy on a tenant-occupied rental — high risk. (2) 789 Elm has dwelling coverage at $145K vs. $210K replacement cost estimate — underinsured 31%. (3) Two policies renew April 15 — no confirmation on file."

**Gap Report Table:**
| Property | Gap Type | Severity | Action Required |
|----------|----------|----------|----------------|
| 456 Oak Ave | Wrong policy type (HO-3 on rental) | 🔴 Critical | Convert to DP-3 immediately |
| 789 Elm St | Underinsured — 31% gap | 🟡 Medium | Increase dwelling coverage |
| 101 Pine — 312 Cedar | Renewal in 14 days | 🟡 Medium | Confirm renewal with carrier |

**Action List** (prioritized):
1. Convert 456 Oak Ave to DP-3 landlord policy — call current carrier or shop
2. Get replacement cost estimate on 789 Elm, increase coverage
3. Confirm April 15 renewals
4. Add loss-of-rents rider to 5 properties missing it
5. Get umbrella quote — 4 properties exceed recommended per-occurrence limits

## Integration with Insurance Tracker (Skill #51)
This skill performs analysis. Skill #51 (`re-insurance-tracker`) handles ongoing tracking and renewal alerts. Run Skill #157 for periodic audits (quarterly or after portfolio changes), Skill #51 for daily monitoring.

## Notes
- Skill #157 in the AI Skills Directory
- Run at: portfolio acquisition, annual audit, before renewals
- Related: Skill #51 Insurance Policy Tracker (re-insurance-tracker)
- FEMA flood zone check: https://msc.fema.gov/portal/search
