# Task 8 report — global deduplication and fixed-version retention

## Scope

- Added conservative global deduplication for normalized candidates. It issues deterministic stable IDs, keeps every accepted source occurrence as a persistable `来源别名` row, and counts a cross-platform upstream Skill once.
- Automatic merge evidence is strictly ordered: normalized canonical source, matching upstream identity plus Skill entry path, and only then a fixed content fingerprint when no stronger identity conflicts. Safe URL normalization removes only scheme/host case, a terminal slash and a terminal `.git` suffix.
- Same-name/different-function items stay separate. Similar names without proven relationship produce a `manual_review` / `possible_duplicate` observation and never merge.
- Added version decisions: unchanged content does nothing; a new tag with the same hash writes only a version-alias observation; changed content is `full_review_required`; rejected updates preserve the current fixed version; unavailable/deleted upstream is an attention observation that retains the existing current row and snapshot.
- Accepted changes derive their history fields internally. They append a deterministic immutable `版本历史` row before changing `当前Skill`; an append exception therefore leaves the current row unchanged. Re-runs are idempotent, while an existing history identity paired with an old current row is rejected as an inconsistent ledger.

## TDD record

1. RED: the new Task 8 suite first failed with `ModuleNotFoundError: No module named 'skill_maintainer.dedup'`.
2. GREEN: the minimal deduplication and version-retention modules made the focused suite pass.
3. A regression showed that a matching content hash could merge entries whose already-known canonical sources/upstream identities conflicted. The root cause was an over-broad fingerprint fallback; it now operates only when stronger evidence does not conflict.
4. A duplicate-history regression showed that the idempotency branch could silently accept a history row while the current row had reverted to the old version. It now accepts that identity only when the current row already matches the target version; otherwise it rejects the inconsistent state.

## Fresh verification

Using the project Python with `PYTHONPATH=07_自动维护工作流/src`:

- `python -m unittest 07_自动维护工作流/tests/test_dedup_versioning.py -v` — 11/11 passed.
- `python -m unittest discover -s 07_自动维护工作流/tests -v` — 113/113 passed.
- `git diff --check` — no whitespace errors.

## Boundaries

- No network access occurred. Candidate Skills were not installed, imported, executed, or sent to candidate-controlled commands.
- `cli.py` was deliberately not changed. Task 9 owns the staged single-writer coordination that persists dedup aliases and invokes version decisions; Task 13 owns CLI wiring.

## Independent-review repair

- URL normalization now retains query and fragment identity exactly; it only normalizes the scheme/host case, a terminal slash and a terminal `.git` suffix.
- Deduplication is group-safe and order-independent. It rejects known source, upstream/entry or function conflicts before a merge; a bridge candidate cannot transitively join incompatible groups. Existing current/alias ledger identities are the only source of stable-ID reuse, while a conflicting candidate-supplied ID becomes `manual_review`.
- Content-hash fallback and version comparison accept only an exact 64-hex SHA-256. Empty tags do not create alias observations.
- Version promotion now requires a capability-issued `VersionDecision.approve` carrying a valid Task 7 `ReviewDecision` and `ReviewPacket`. Application revalidates both and exactly binds their identity, version, source, licence, security grade and evidence to the persisted full current row and observed version.
- Promotion writes on a shadow `LedgerStore` cloned from an in-memory workbook byte snapshot. History append and current-row update both run there; any failure discards the shadow and leaves the original workbook object, all in-memory rows and the source-ledger file bytes unchanged. Only a successful pair swaps in the shadow workbook.

Fresh repair verification:

- Focused Task 8 suite: 20/20 passed.
- Full workflow suite: 122/122 passed.

## Independent-review repair round 2 — non-forgeable approval boundary

- Removed the public `VersionDecision.approve` self-signing factory. Changed-content acceptance is created only with `VersionDecision.accept_from_applied_review`, which verifies a Task 7 receipt both when constructed and immediately before use.
- The receipt is issued only after Task 7 validates a registered review packet and applies its formal decision to the caller-owned staged ledger. It binds candidate/stable ID, fixed version, canonical source, licence, security grade, evidence paths and the exact observed 64-hex fixed-content SHA-256.
- Version promotion rechecks that binding against the complete persisted current row and observation. The receipt is consumed only after the shadow workbook has successfully appended history and swapped current; history/upsert failure leaves it usable for the retry. Forged, modified and reused receipts are rejected.
- A discovery that resolves to more than one pre-existing ledger stable ID is now excluded from both automatic `skills` and aliases, producing deterministic `manual_review` / `inconsistent_ledger` output instead of inventing a third ID.

Fresh verification after this round:

- Focused Task 7 suite: 30/30 passed.
- Focused Task 8 suite: 23/23 passed.
- Full workflow suite: 127/127 passed.
- `git diff --check`: no whitespace errors.
