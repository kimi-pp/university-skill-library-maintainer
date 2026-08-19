---
name: identify-resale-targets
description: Identify items in the inventory worth selling rather than discarding or donating. Estimates resale value, suggests the right marketplace per item (geo-aware — e.g. Yad2/Facebook Marketplace IL for Israel, eBay/Craigslist/FB for US, Gumtree/eBay for UK), flags effort vs. payoff, and produces a prioritized sale list.
---

# Identify resale targets

## When to invoke

User wants to sell stuff, asks "what's worth selling", or runs after `find-duplicates` / `suggest-discards` to route flagged items to resale.

## Preconditions

Workspace + populated inventory. Geography and currency from `workspace.json`.

## Selection criteria

An item is a resale candidate if:

- `est_value` ≥ a minimum threshold worth the effort of listing (default: ILS 100 / USD 30 / GBP 25 / EUR 25 — configurable in `workspace.json` under `resale.min_value`).
- `condition` is `good` or better (allow `fair` for high-value items where the market accepts it).
- Not tagged `sentimental` / `keepsake`.
- Has a real second-hand market (electronics, furniture, designer clothing, musical instruments, books in some categories, collectibles, kitchen appliances, tools, sports gear).

## Marketplace recommendation (geo-aware)

Read `workspace.json.geography` and recommend platforms accordingly. Examples:

- **Israel**: Yad2 (general), Facebook Marketplace IL, Agora (auctions), Lastprice/Zap for pricing checks, dedicated Telegram groups for niche items.
- **US**: eBay (shippable + collectibles), Facebook Marketplace, Craigslist, OfferUp, Mercari (small items, clothing), Reverb (instruments), StockX (sneakers/streetwear).
- **UK**: eBay UK, Gumtree, Facebook Marketplace, Vinted (clothing), Music Magpie (media/electronics).
- **EU**: eBay Kleinanzeigen (DE), Vinted (clothing), Leboncoin (FR), Wallapop (ES).
- **Global / niche**: Reverb (instruments), Watchuseek/Chrono24 (watches), Discogs (records), AbeBooks (books), Bring a Trailer (cars).

For each item, pick 1–3 best-fit platforms and explain why in one line.

## Resale value estimate

Use the same valuation approach as `value-for-insurance` but bias toward **realistic sale prices**, not insurance replacement value. Sale price ≈ 50–70% of current second-hand market median for typical condition.

## Effort vs. payoff

For each item, estimate:

- **Effort**: `low` (post a photo, ship in box), `medium` (need to clean/photograph/answer questions), `high` (heavy item, local pickup only, may need to disassemble).
- **Payoff per hour**: estimated sale price ÷ estimated effort hours.

Sort the output by payoff/hour descending, so the user attacks the high-leverage items first.

## Output

Write `<workspace>/analysis/resale-targets.md` and `<workspace>/outputs/resale-targets.csv`.

CSV columns: `id, name, condition, location, est_sale_value, currency, recommended_platforms, effort, payoff_per_hour, notes`.

Print top 10 to chat. Offer to generate a PDF via `generate-action-list` and/or hype copy via `hype-giveaway-post` (re-purposable for sale listings).
