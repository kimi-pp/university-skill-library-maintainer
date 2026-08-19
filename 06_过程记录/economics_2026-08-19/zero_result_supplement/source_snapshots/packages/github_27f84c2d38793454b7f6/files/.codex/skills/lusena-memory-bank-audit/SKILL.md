---
name: lusena-memory-bank-audit
description: Periodic deep audit of the entire memory bank. Verifies all content against the codebase, fixes stale information missed by branch-level syncs, evaluates whether the documentation structure still fits, and creates/restructures docs as needed. Run after ~10 merges to main.
---

# Memory bank audit (periodic deep review)

## Purpose

Comprehensive two-pass review of the entire memory bank:
1. **Content verification** — ensure every doc accurately reflects the current codebase
2. **Structural review** — evaluate whether the doc structure still fits the project

This catches everything the branch-level syncs (`lusena-worktree-sync`) missed: cross-cutting staleness, drifted references, docs that no single branch thought to update, and structural shifts that only become visible after several merges.

## When to use

- After ~10 squash-merges to main since the last audit
- When starting a major new phase and wanting a clean documentation baseline
- When the user explicitly requests a full memory bank review
- After significant architectural changes that touched many areas

## Tracking: git tags

Each audit tags main after completion: `memory-bank-audit/YYYY-MM-DD`

On the next audit, diff from the last tag to current HEAD to see what changed.

## Workflow

### Phase 1 — Determine audit range

1. **Confirm you are on main** (or can read main):
   ```bash
   git branch --show-current
   ```

2. **Find the last audit tag:**
   ```bash
   git tag --list "memory-bank-audit/*" --sort=-creatordate
   ```

3. **If no tag exists**, find the last audit commit as fallback:
   ```bash
   git log --oneline --all --grep="memory bank audit" -1
   ```
   If neither exists, audit the entire memory bank without a diff range (full baseline).

4. **Get the change range:**
   ```bash
   git log <last-audit-tag>..HEAD --oneline
   git diff <last-audit-tag>..HEAD --stat
   git diff <last-audit-tag>..HEAD --name-only
   ```

5. **Summarize** how many merges, which areas of the store were touched. Present to user.

### Phase 2 — Read the entire memory bank

Read ALL memory bank files. Use parallel reads where possible.

**Core files (always read):**
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`
- `memory-bank/systemPatterns.md`
- `memory-bank/techContext.md`
- `memory-bank/productContext.md`
- `memory-bank/projectbrief.md`

**Feature docs (read all):**
- `memory-bank/doc/features/*.md`

**Pattern docs (read all):**
- `memory-bank/doc/patterns/*.md`

**Product docs (read if product-related changes in range):**
- `memory-bank/doc/products/*.md`

**Strategy docs (read if bundle/upsell changes in range):**
- `memory-bank/doc/bundle-strategy.md`
- `memory-bank/doc/upsell-strategy.md`
- `memory-bank/doc/color-strategy.md`

**Instruction files:**
- `CLAUDE.md`

### Phase 3 — Content verification (Pass 1)

For EACH memory bank file, cross-reference against the actual codebase:

1. **File paths** — do referenced files still exist? Use Glob to verify.
2. **Section inventories** — do listed sections match what is actually in `sections/` and `templates/`?
3. **CSS/JS sizes** — are stated sizes still accurate? Check with Glob + file sizes.
4. **Status markers** — are items marked "done" actually done? Are "pending" items still pending?
5. **Numeric values** — thresholds, prices, percentages. Cross-check against the codebase (e.g., free shipping threshold in Liquid vs docs).
6. **Architecture descriptions** — do they match the current code patterns?
7. **Known issues** — are any resolved? Are there new ones not documented?

Build a checklist:
```
Content fixes needed:
  - techContext.md:42 — lusena-comparison.liquid listed as active, but it's in the unused catalog
  - systemPatterns.md:108 — PDP CSS stated as ~34KB, actual is ~42KB
  - progress.md:23 — "Cart page" still marked pending, but it shipped
  - doc/features/pdp.md:67 — missing cross-sell checkbox section

No fixes needed:
  - projectbrief.md — still accurate
  - doc/patterns/spacing-system.md — still accurate
```

Present the checklist to the user before proceeding.

### Phase 4 — Structural review (Pass 2)

Zoom out and evaluate the documentation architecture:

1. **Missing docs** — has anything been built that has no documentation?
   - New pages, major features, architectural patterns
   - Check `templates/*.json` for pages without corresponding feature docs
   - Check `sections/lusena-*.liquid` for sections not documented anywhere

2. **Docs that should be split** — has any file grown too large or covers too many concerns?
   - Feature docs covering multiple unrelated features
   - Pattern docs mixing architecture with implementation details

3. **Docs that should be merged** — are any docs too small or redundant?
   - Near-duplicate information across files
   - Stub files that could be folded into a parent doc

4. **Structural shifts** — has the project's shape changed?
   - Did 10 branches collectively shift the project focus?
   - Are the "next steps" still the right next steps?
   - Has the architecture evolved enough to warrant new pattern docs?

5. **activeContext.md cleanup** — has "Recent completed work" grown stale?
   - Entries from many branches ago should graduate to `progress.md`
   - Keep only the last ~3-5 branches' work in activeContext

Present structural recommendations to the user:
```
Structural changes proposed:
  - CREATE doc/features/search-page.md — search was migrated but has no feature doc
  - SPLIT doc/features/pdp.md — now covers standard PDP, bundle PDP, and cross-sell; split into 3
  - MERGE doc/bundle-implementation.md into doc/bundle-strategy.md — redundant separation
  - UPDATE activeContext.md — graduate old entries to progress.md

No structural changes needed:
  - doc/patterns/ — still well-organized
```

Get user approval before executing structural changes.

### Phase 5 — Execute all updates

Apply all content fixes and approved structural changes.

Follow these rules per file:

#### `activeContext.md`
- Set `*Last updated:` to today's date
- `## Current focus` — 1-line bold summary of where the project stands NOW
- `## Recent completed work` — keep only last ~3-5 branches' work. Graduate older entries to progress.md
- `## Next steps` — re-evaluate and re-prioritize based on current state
- `## Known issues` — remove resolved, add newly discovered
- `## Architecture note` — update only if architecture changed

#### `progress.md`
- Check/uncheck page status items
- Absorb graduated entries from activeContext
- Update infrastructure completed list
- Update cleanup backlog

#### All other files
- Fix every stale reference identified in Pass 1
- Execute approved structural changes from Pass 2
- When creating new files, follow the structure of existing similar files

### Phase 6 — Tag and commit

1. Stage all changes:
   ```bash
   git add memory-bank/ CLAUDE.md
   ```

2. Commit with the audit range in the message:
   ```bash
   git commit -m "docs: memory bank audit — covers <last-tag>..HEAD (<N> merges)"
   ```

3. Tag the commit:
   ```bash
   git tag "memory-bank-audit/YYYY-MM-DD"
   ```

4. Present summary to user:
   - Files updated (with brief description of what changed)
   - Files created or restructured
   - Audit tag created
   - Next audit recommended after ~10 more merges

## Rules

- NEVER fabricate or guess information — only document what is actually in the codebase
- NEVER delete a doc without user approval — propose deletions, wait for confirmation
- Cross-reference against actual files, not just other docs (docs can be wrong too)
- Keep entries concise — memory bank is for quick orientation, not detailed history
- Use past tense for completed work, imperative for next steps
- Document "why" decisions were made, not just "what"
- When creating new files, follow the structure of existing similar files
- If unsure whether a doc needs updating, err on the side of updating it
