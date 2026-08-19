---
skill_id: prospect-theory
name: Prospect Theory (Loss Aversion · Reference Dependence · Probability Weighting)
version: 1.0.0
category: behavior-science
type: framework
frameworks: []
triggers:
  - apply prospect theory
  - loss aversion analysis
  - reference dependence framing
  - probability weighting
  - pricing psychology
collaborates_with:
  - behavioral-designer
  - conversion-optimizer
  - decision-architect
  - product-strategist
  - growth-hacker
ethics_required: true
priority: high
tags: [behavior-science, framework, decision-making, pricing, loss-aversion]
adr: ADR-007
created: 2026-05-19
updated: 2026-05-19
---

# Prospect Theory (Loss Aversion · Reference Dependence · Probability Weighting)

## Purpose
Apply Prospect Theory to design pricing, framing, and choice architecture that aligns with how humans actually make decisions under risk — NOT how classical economics assumes they do. The single most product-relevant finding: **losses loom roughly 2.25x larger than equivalent gains**. Mis-framing the choice (gain frame vs loss frame) routinely costs products 30–50% of available conversion.

## Frameworks & Standards
| Item | Value |
|---|---|
| Framework ID | `prospect-theory` |
| Category | Behavior Science — Decision Making Under Risk |
| Version | 1.0.0 |
| Originators | Daniel Kahneman & Amos Tversky (1979) · Cumulative Prospect Theory (1992) |
| Maturity | Established — Nobel Prize 2002 (Kahneman); foundational behavioral economics |
| Primary references | Kahneman & Tversky "Prospect Theory: An Analysis of Decision under Risk" *Econometrica* 47(2): 263–291 (1979) · *Thinking, Fast and Slow* Chap. 26–28 (2011) |

## The Three Core Phenomena

1. **Loss Aversion**
   - Losses are felt ~2.25x as intensely as equivalent gains
   - Implication: framing matters enormously. "Don't lose $X" beats "Save $X" by ~2x in most contexts.

2. **Reference Dependence**
   - Outcomes are evaluated relative to a reference point, not in absolute terms
   - Implication: anchor placement (the implied reference) is more important than the actual value
   - The reference point itself can be manipulated: previous price · competitor price · operator's first quote · status quo

3. **Probability Weighting**
   - People overweight small probabilities (lotteries · insurance · rare-but-catastrophic events)
   - People underweight medium-to-large probabilities (75% chance of success feels like ~63%)
   - Implication: probability framing in product copy ("99.9% uptime!" vs "1-in-1000 failure rate") triggers different intuitions

## The Value Function

Prospect Theory's value function is **S-shaped**, asymmetric around the reference point:
- **Concave for gains** (diminishing sensitivity — $100 → $200 feels bigger than $1000 → $1100)
- **Convex for losses** (diminishing sensitivity — losing $100 → $200 hurts proportionally more than losing $1000 → $1100)
- **Steeper for losses than gains** (the 2.25x ratio)

## Prompt Template
```
You are applying Prospect Theory.

CONTEXT:
- Decision under design: [[decision]]
- Stakes: gain · loss · mixed
- Probability characteristics: certain · medium probability · low probability · very low probability

PROSPECT ANALYSIS:
1. Reference point — what is the user's current implicit reference?
2. Frame — is the current framing gain-side or loss-side?
3. Probability — what's the actual probability vs how it will likely be perceived?
4. Asymmetry — is the design accounting for the 2.25x loss-aversion ratio?

FRAMING RECOMMENDATIONS:
- For voluntary positive behavior change → gain frame ("Save $X annually")
- For preventing loss / status-quo defense → loss frame ("Don't lose your existing $X")
- For premium tier positioning → loss frame against premium losing the premium ("Pro members keep their data backed up")
- For free-tier risk surfacing → loss frame WITHOUT manufactured urgency (ethics gate)

PRICING-SPECIFIC APPLICATIONS:
- Annual discount framing: "Save $X" (gain) vs "Don't pay 17% more" (loss) — usually loss frame wins
- Tier comparison: position the recommended tier as the reference point; others as "missing" something (loss)
- Anchor placement: highest price first creates downward reference; lowest first creates upward
- Decoy effect: add an inferior third option to make the target option look better by comparison

ANTI-PATTERN CHECK:
- Manufactured loss frames (false urgency · invented scarcity) = dark pattern
- Reference-point manipulation that misleads (fake "original price") = unethical
- Probability misframing on high-stakes risk = unethical

OUTPUT:
- Reference-point and frame diagnosis
- Specific framing recommendations
- Ethical-flag if any manufactured loss frames present
```

## Core Principles
- **Loss frames are roughly 2x more persuasive than gain frames** — but only when honest about what is actually at stake.
- **Reference point dominates absolute value.** A $99 product feels expensive next to a $50 reference and cheap next to a $200 reference. Reference engineering > price engineering.
- **Probability weighting biases stay constant.** Insurance markets and lottery sales exist because of probability weighting — and so do most "fear of missing out" product flows.
- **Endowment effect.** People value things they already own ~2x more than equivalent things they don't. Free trials work because they create endowment; cancellation flows fail because they extract endowment.
- **Status quo bias.** Reference dependence makes change feel like loss. Defaults dominate disproportionately.

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|---|---|---|
| Pricing tier presentation | Loss-frame premium ("Free users miss out on...") | Higher upgrade rate |
| Annual billing prompt | "Lock in this year's price" beats "Save 17%" usually | Higher annual conversion |
| Cancellation flows | Reference user's endowed benefit ("You'll lose your...") | Lower churn (must be honest) |
| Free trial design | Long enough to create endowment (≥14 days) | Higher trial-to-paid conversion |
| Insurance / risk products | Lean into probability overweighting honestly | Higher conversion without manipulation |
| A/B test framing | Test gain vs loss frame on every meaningful CTA | Discover the 30–50% missed conversion |
| Negotiation | Set high anchor first; concessions feel like operator-side losses | Better terms |

## Reference Materials
- Kahneman, D. & Tversky, A. (1979). "Prospect Theory: An Analysis of Decision under Risk." *Econometrica* 47(2): 263–291.
- Tversky, A. & Kahneman, D. (1992). "Advances in Prospect Theory: Cumulative Representation of Uncertainty." *Journal of Risk and Uncertainty* 5(4): 297–323.
- Kahneman, D. (2011). *Thinking, Fast and Slow.* Chapters 26–28.
- Camerer, C. (2000). "Prospect Theory in the Wild: Evidence from the Field." *Choices, Values, and Frames* (Kahneman & Tversky, eds.)

## Usage Guidelines
- **Identify the reference point first.** Without knowing the reference, framing recommendations are guesses.
- **Test gain vs loss frame on every meaningful CTA.** The default "save $X" copy is usually leaving 30–50% conversion on the table.
- **Account for the 2.25x asymmetry** when designing incentive structures. A $5 reward needs to overcome a $5 loss ~2.25x for the same intuitive force.
- **Use probability weighting honestly.** Don't manufacture rare-but-catastrophic fears; do surface real low-probability risks (security · data loss · regulatory exposure) — they will be felt more strongly than their probability suggests.
- **Pair with Cialdini's 6 Principles** — loss frames pair powerfully with scarcity (real, not manufactured) and authority.

## Collaboration Protocol
- Inbound from: `behavioral-designer` · `decision-architect` · `pricing-strategist` (CPO) · `growth-hacker`
- Outbound to: same agents + `conversion-optimizer` for funnel A/B tests
- Cross-framework: pairs with Dual Process Theory (loss aversion is System 1), Cialdini (Authority + Scarcity), TTM (loss frames work differently by stage)

## Ethical Guidelines
- **Bright line:** Manufactured loss frames are dark patterns. "Last 2 items!" when stock is 200 = unethical regardless of conversion lift.
- **Reference manipulation must be honest.** Fake "original price" anchors are legally + ethically problematic (FTC + most jurisdictions).
- **Probability misrepresentation on stakes-bearing decisions** (health · finance · legal) is unethical.
- **Endowment-effect exploitation in cancellation flows** is acceptable IF the surfaced benefits are real; not if they're fabricated.

## Success Metrics
- A/B test lifts on framing changes (typical: 15–50% on tier upgrade / annual conversion)
- Decision regret rate at 30/90 days (high regret = loss-frame exploitation)
- Pricing elasticity vs reference-point shifts (controlled experiments)

## Related Skills
- `composable-skills/frameworks/dual-process-theory/SKILL.md` — loss aversion is a System 1 phenomenon
- `composable-skills/frameworks/cialdinis-6-principles/SKILL.md` — scarcity (loss frame) + authority (reference anchor)
- `composable-skills/frameworks/anchoring-bias/SKILL.md` — reference-point engineering
- `composable-skills/frameworks/fogg-behavior-model/SKILL.md` — Motivation × Ability × Prompt; loss frame can boost Motivation
- `composable-skills/frameworks/east-framework/SKILL.md` — make loss frame Easy + Attractive + Timely

## Testing Strategy
- A/B test gain vs loss frame on highest-impact CTAs (pricing · upgrade · cancellation · annual)
- Measure conversion AND regret (post-decision survey at 7/30/90 days)
- High-regret loss-frame wins = ethical flag; loss-frame won on manipulation, not honest preference
- Pair with reference-point experiments — test "high anchor first" vs "low anchor first" on the same offer set

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1. Shipped in WS6a of v1.2.0 sprint (2026-05-19). One of 4 HIGH-priority behavioral frameworks per FRAMEWORK_ROADMAP § v1.2.E._
