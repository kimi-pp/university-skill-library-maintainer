---
name: insurance-ontology-starter
description: Prebuilt, governed insurance (P&C + life) ontology to adapt instead of building from scratch — entity spine (policyholders, policies, coverage, premium, claims, producers), NAIC line-of-business + peril classification, and governed metric surfaces (earned premium, loss ratio, combined ratio, claim frequency, claim severity, reserves, retention, new business, policies in force). Use when a P&C carrier, life insurer, MGA, or broker wants a ready-to-run ontology for policy/claims data in TextQL/Ana.
---

# Insurance Ontology Starter (P&C + Life)

When an insurance customer needs a TextQL ontology, **start here instead of a blank page.** A
governed ontology you connect, point at the carrier's book of record, and adapt — entity spine,
governed metrics, classification, governance, all already built. Sibling of the Healthcare, Banking
& Payments, and Wealth & Asset Management starters (same framework, different spine).

## When to use this
- The customer is a **P&C carrier, life/health insurer, MGA, reinsurer, or broker** with policy +
  claims data.
- They want governed metrics fast (loss ratio, combined ratio, frequency/severity, reserves,
  retention).
- They want claims/policies grouped into meaningful concepts (NAIC line of business, peril groups)
  without building crosswalks by hand.

P&C-leaning; life/health extend the same spine (face amount, in-force, lapse — see `notes/glossary.md`).

## How to use it (full walkthrough in `GETTING_STARTED.md`)
1. **Connect this repo to Ana** via the Git connector.
2. **Connect the carrier's warehouse** (policy admin / claims; read-only).
3. **Validate + adapt (required):** follow `MIGRATION.md` — run `validation/dry-run-prompt.md`,
   repoint `ontology/schema.tql` (the only file with physical names), run `validation/validate_tql.py`
   until clean.
4. **Ask questions** — metrics, classification, governance work; terminology federates in Ana's
   Python sandbox (zero warehouse writes).

## What's inside (six layers)
- **Entity spine** — `ontology/schema.tql`, `ontology/relations/` (policyholder, policy, coverage,
  premium, claim, claim_transaction, producer; keys policy_id/policyholder_id/claim_id).
- **Metrics** — `ontology/queries/*.tql` (9 governed surfaces, statically validated).
- **Classification** — `ontology/dimensions/`, `ontology/filters/`, `reference/terminology/` (NAIC
  lines, peril taxonomy; licensed ISO/PCS codes structural only).
- **Governance** — `ontology/notes/governance-pii.md`, `config/org_context.md` (PII, suppression,
  fair-pricing/redlining, medical-claim sensitivity, reserve MNPI).
- **Decision records** — `ontology/notes/` (loss-ratio basis, written-vs-earned, reserves, grain,
  identity, glossary).
- **Validation** — `validation/` (`validate_tql.py`, dry-run, golden-query fixtures).

## Adapting to a customer
- Follow `MIGRATION.md`: repoint `schema.tql`, resolve party/identity, run the validator, tune
  governance (`min_cell_size`, identifier inventory, fair-pricing), localize the glossary, pin goldens.

## Pairs with
- **ontology-builder** (skills-pack) — recipes to extend or build ontology slices.
- The **Healthcare**, **Banking & Payments**, and **Wealth & Asset Management** starters — same
  framework, different spine.
