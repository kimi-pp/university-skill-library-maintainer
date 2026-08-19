---
name: legal
description: >
  Use this skill whenever the user asks about contracts, legal compliance,
  legal risk, or regulatory requirements. Triggers include: 'review this contract',
  'NDA', 'nondisclosure agreement', 'compliance check', 'legal risk', 'legal risk
  assessment', 'vendor vetting', 'legal brief', 'signature request', 'meeting
  briefing', 'regulatory compliance', 'indemnification', 'liability', 'governing
  law', 'force majeure', 'IP ownership', or requests to review agreements, assess
  legal risk, triage NDAs, check regulatory compliance, draft legal responses,
  or prepare legal meeting briefings. Requires legal-domain framing — risk assessment
  methodology, regulatory reference, contractual interpretation. Composes with
  review-critique skill (which provides evaluation framework) and loan-agency skill
  (which provides credit agreement domain knowledge). Outputs are analytical
  frameworks — not legal advice. Do NOT use for financial audits (use
  finance-accounting). Do NOT use for general business risk (use review-critique).
---

# Legal

Legal analysis frameworks for contracts, compliance, and risk assessment. All outputs are analytical frameworks — not legal advice. Material provisions should be reviewed by qualified counsel.

## Routing

| If the user wants to... | Read |
|---|---|
| Assess legal risk of a decision, initiative, or transaction | `references/legal-risk-assessment.md` |
| Review a contract — red flags, key provisions, suggested edits | `references/review-contract.md` |
| Check regulatory compliance for a product, feature, or initiative | `references/compliance-check.md` |
| Triage an NDA — standard vs. non-standard terms, risk areas | `references/triage-nda.md` |
| Vet a vendor — legal, compliance, and risk dimensions | `references/vendor-check.md` |
| Prepare a briefing for a legal meeting or negotiation | `references/meeting-briefing.md` |
| Process a signature request — authority, workflow, tracking | `references/signature-request.md` |
| Draft or structure a legal brief or memorandum | `references/brief.md` |
| Draft a legal response or position statement | `references/legal-response.md` |

## Gotchas

- Never provide actual legal advice — frame outputs as analysis to discuss with qualified counsel.
- Contract review should flag ambiguous terms, not just obviously problematic ones.
- Compliance checks must reference specific regulations and their effective dates.
- NDA triage should assess both legal risk and business relationship impact.
- "Standard" contract terms vary by industry, deal size, and party sophistication. What's standard for enterprise SaaS ≠ standard for private credit.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
