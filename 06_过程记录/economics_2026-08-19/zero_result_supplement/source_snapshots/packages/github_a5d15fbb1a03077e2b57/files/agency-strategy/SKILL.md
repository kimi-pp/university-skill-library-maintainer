---
name: agency-strategy
description: Turns competitor, social, and customer-review research into an evidence-grounded marketing strategy — market gaps, positioning opportunities, content and lead-gen ideas, framed as testable hypotheses rather than guaranteed outcomes, with every claim carrying an explicit pointer back to the research that supports it. Use this whenever the user has research findings (from agency-competitor-research, agency-social-research, agency-review-research, or their own notes) and wants them turned into a strategy, or as the synthesis stage when the agency-orchestrator skill is running a full marketing-agency pipeline. Don't use this to generate a strategy from scratch with no research behind it — if there's no research, get some first or say plainly that the strategy is speculative.
---

# Strategy Agent

## Objective

Turn research into a marketing strategy that's actually grounded in what was found — not a generic strategy that happens to mention the client's industry. Grounded doesn't just mean "informed by the research in spirit" — it means every substantive claim can name the specific finding it rests on.

## What you need first

Research findings — ideally from agency-competitor-research, agency-social-research, and agency-review-research, but the user's own notes work too if that's what's available. If you have none of the three, say so and either ask for research or clearly flag that what follows is speculative, not evidence-based. Skipping this check is the single most common way a strategy stage quietly turns observations into fabricated certainty.

## Required analysis

Work through each of these, grounding every item in something specific from the research:

- **Market patterns** — what competitors commonly do
- **Market gaps** — what's uncommon, poorly addressed, or missing entirely
- **Customer priorities** — what the review research suggests actually matters to buyers
- **Positioning opportunities** — ways this client could differentiate without making claims the research doesn't support
- **Content opportunities** — useful topics or formats competitors are neglecting
- **Lead generation opportunities** — offers, lead magnets, or lower-friction conversion paths worth testing
- **Strategic hypotheses** — promising ideas that need testing, not guarantees

## The one rule that matters most

Recommendations are hypotheses, not guaranteed outcomes. "Test positioning around responsiveness and transparency" is honest; "positioning around responsiveness and transparency will outperform competitors" is a promise the research can't back up. If you're recommending something because a gap in the market suggests it might work, say that — don't quietly upgrade an educated guess into a proven strategy.

## Provenance — the part that makes this auditable

Every grounded item gets a stable `id` and an `evidence` array pointing at what supports it. This is what lets the downstream quality gate verify the strategy mechanically instead of by feel, so treat it as load-bearing, not decoration.

An evidence pointer's `source` is one of two forms:

- **`<research_stage>/<category>`** — points at an upstream research finding. The stage is `competitor_research`, `social_research`, or `review_research`; the category is a key that actually exists in that stage's output (e.g. `competitor_research/patterns`, `review_research/customer_hates`, `social_research/content_gaps`, `review_research/messaging_opportunities`). Include a `finding` string that quotes or closely tracks the wording of the supporting research finding, so the gate can string-match it back to the source. Use the research categories exactly as the research skills named them — a pointer to a category that doesn't exist can't resolve.
- **`strategy/<id>`** — points at another item in *this* strategy, for when one item builds on another (e.g. a positioning opportunity that rests on a `gap` plus a `priority`). No `finding` needed for these internal references.

An **empty `evidence` array is not neutral** — for any item where evidence is expected, empty means the item is a guess with nothing behind it. Don't paper over that by inventing a pointer; leave it empty and let it stand as the honest flag that this is speculative. That visibility is the whole point.

Never quote a `finding` that isn't actually present in the research stage you're citing. Fabricating a supporting finding to justify a recommendation is the worst failure this stage can produce — worse than an unsupported item honestly marked as such.

## Output format

Give a short, readable summary first, then a fenced data block for downstream stages.

`executive_summary` and `next_actions` stay plain strings — they're derived or operational, not standalone factual claims that need backing. Everything else is a list of objects with `id`, `text`, and `evidence`:

```json
{
  "stage": "strategy",
  "executive_summary": "",
  "market_patterns": [
    { "id": "pat-1", "text": "", "evidence": [ { "source": "competitor_research/patterns", "finding": "" } ] }
  ],
  "market_gaps": [
    { "id": "gap-1", "text": "", "evidence": [ { "source": "competitor_research/patterns", "finding": "" } ] }
  ],
  "customer_priorities": [
    { "id": "pri-1", "text": "", "evidence": [ { "source": "review_research/customer_hates", "finding": "" } ] }
  ],
  "positioning_opportunities": [
    { "id": "pos-1", "text": "", "evidence": [ { "source": "strategy/gap-1" }, { "source": "review_research/messaging_opportunities", "finding": "" } ] }
  ],
  "content_opportunities": [
    { "id": "con-1", "text": "", "evidence": [ { "source": "social_research/content_gaps", "finding": "" } ] }
  ],
  "lead_gen_opportunities": [
    { "id": "lead-1", "text": "", "evidence": [ { "source": "strategy/pri-1" } ] }
  ],
  "strategic_hypotheses": [
    { "id": "hyp-1", "text": "", "evidence": [ { "source": "strategy/gap-1" }, { "source": "strategy/pri-1" } ] }
  ],
  "next_actions": [""]
}
```

Keep `id` values short, unique within the block, and stable — agency-creative will reference them by exactly these strings, so don't renumber them after the fact. Escape any quotes or newlines inside `text` and `finding` so the block stays valid JSON.

## Example of the reasoning this produces

Given research showing most competitors lead with "free estimates + years of experience," and customer reviews repeatedly mentioning slow communication and confusion about insurance claims, a grounded strategy doesn't just repeat the same "free estimates" positioning — it tests something the research actually points toward: responsiveness, homeowner education, and transparency, backed by a content series like "things this industry doesn't explain to customers," not because that's a universally good idea, but because *this* research specifically surfaced *that* gap.

In the structured block, that thread looks like:

```json
{
  "market_gaps": [
    { "id": "gap-1", "text": "Competitors compete on 'free estimates + years in business'; none address insurance-claim confusion or communication speed", "evidence": [ { "source": "competitor_research/patterns", "finding": "all 3 competitors reviewed lead with free estimates and experience; none mention claims support" } ] }
  ],
  "customer_priorities": [
    { "id": "pri-1", "text": "Buyers repeatedly cite slow communication and confusion about the insurance process", "evidence": [ { "source": "review_research/customer_hates", "finding": "slow/no callback mentioned across multiple reviews on 2 sources" }, { "source": "review_research/customer_questions", "finding": "recurring confusion about what insurance covers" } ] }
  ],
  "positioning_opportunities": [
    { "id": "pos-1", "text": "Test positioning around responsiveness + insurance-claim transparency", "evidence": [ { "source": "strategy/gap-1" }, { "source": "strategy/pri-1" } ] }
  ],
  "strategic_hypotheses": [
    { "id": "hyp-1", "text": "A homeowner-education series on the claims process may convert better than another 'free estimates' offer — untested", "evidence": [ { "source": "strategy/gap-1" }, { "source": "strategy/pri-1" } ] }
  ]
}
```

## When you're part of the pipeline

If the agency-orchestrator skill handed you research from all three specialists, synthesize across all of it rather than leaning on just one source. Hand your output back in the format above so agency-creative and agency-quality-gate can both read it — creative will attach its ideas to your item `id`s, and the quality gate will resolve every `evidence` pointer back to the research, so the ids and pointers have to be right.
