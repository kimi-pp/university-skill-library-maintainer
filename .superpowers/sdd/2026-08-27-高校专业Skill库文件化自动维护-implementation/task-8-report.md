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
