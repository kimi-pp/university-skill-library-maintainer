---
name: arbitrage-free-derivatives-pricing
description: "Arbitrage-free derivatives pricing workflows for consistent discounting, forward construction, and no-arbitrage valuation checks across asset classes. use when tasks involve production valuation models and pricing control frameworks."
---

# Arbitrage Free Derivatives Pricing
## objective
Build arbitrage-free pricing pipelines with explicit carry conventions and control-ready valuation diagnostics.

## workflow
1. define product payoff, discount curve, and forward construction rules.
2. implement valuation equations and numerical solvers with test fixtures.
3. run no-arbitrage checks across strikes, maturities, and structures.
4. compare model values against market and alternative valuation methods.
5. release only when pricing controls and reconciliations pass thresholds.

## required diagnostics
- pricing residual by product, strike, and maturity.
- curve-consistency and forward-construction diagnostics.
- no-arbitrage violations count and severity trends.
- sensitivity reconciliation across greeks and finite differences.
- daily model-versus-market control exceptions.

## risk controls
- enforce valuation tolerance thresholds per product class.
- enforce independent price verification and signoff workflow.
- enforce rollback to validated baseline model on control breach.

## outputs
- run `python scripts/arbitrage_free_derivatives_pricing_diagnostics.py input.csv --output diagnostics.json` and keep the json artifact.
- write an implementation memo using `references/arbitrage-free-derivatives-pricing-playbook.md` with assumptions, tests, limits, and rollout plan.

## resources
- use `scripts/arbitrage_free_derivatives_pricing_diagnostics.py` for deterministic diagnostics.
- use `references/arbitrage-free-derivatives-pricing-playbook.md` for the domain checklist and delivery structure.
