# Task 7 report — fixed-version snapshots and static review gates

## Scope

- Added a read-only fixed-version snapshot builder. It accepts only local directories, ZIP, or TAR evidence; rejects traversal, links/reparse points and non-ordinary files; enforces file-count, aggregate-byte and per-file-byte limits before reading archive member contents; and hashes only text, code, and configuration files.
- Added immutable review models that separate observed facts, project judgments, and derived fields. Review packets include the relevant workflow/protocol versions and fixed-version snapshot evidence paths.
- Added field-level review errors for remote-endpoint conflicts, local Abaqus-style software/API boundaries, formal-license and verification gates, SB-A direct deployment, relevance display, and derived-score tampering.
- Implemented the Task 13-consumable `apply_reviews_from_stream(stream, staged_ledger)` contract: UTF-8 JSON is decoded and validated in memory, accepted supplied ledger rows are applied to the caller-owned staged `LedgerStore`, and no review JSON artifact is written. Full CLI wiring remains intentionally out of scope for Task 13.

## TDD record

1. RED: the new Task 7 suite failed because `skill_maintainer.snapshots` did not exist (`ModuleNotFoundError`).
2. GREEN: after the minimal snapshot and review implementations, the focused suite passed.
3. A nested archive regression was added, failed due to strict resolution before creating safe nested output directories, then passed after safe parent creation.
4. An oversized ZIP member regression was added, failed because contents were read before limit checks, then passed after metadata-first budgeting.
5. A malformed string-boolean stdin regression was added, failed because JSON strings were coerced with `bool()`, then passed after strict JSON boolean validation.

## Fresh verification

Using the project Python with `PYTHONPATH=07_自动维护工作流/src`:

- `python -m unittest discover -s 07_自动维护工作流/tests -p test_snapshots_review.py -v` — 20/20 passed.
- `python -m unittest discover -s 07_自动维护工作流/tests -v` — 94/94 passed.
- `git diff --check` — no whitespace errors.

## Boundaries and concern

- No candidate content was installed, imported, executed, or passed to a candidate-controlled command. No network activity occurred.
- The task brief does not define a single concrete snapshot-input type. The principal contract is `SnapshotCandidate`; the builder also accepts compatible source-adapter-style objects/mappings when they explicitly provide a fixed version and local snapshot path.
- `cli.py` was deliberately not changed. Task 13 should attach its `apply-reviews --run <run-id> --stdin` parser/handler to `apply_reviews_from_stream` and provide the staged ledger it owns.

## Review-fix round

The independent Task 7 review reproduced three security and consistency defects and this follow-up corrects them.

- Snapshot destinations are now checked in their original lexical form, component by component, before any `resolve()`-like normalization or directory creation. A Windows-compatible symbolic-link regression confirms an external target receives no output.
- `apply_reviews_from_stream` now requires a trusted `candidate_id -> ReviewPacket` mapping. The packet binds candidate identity, fixed version, canonical source, license, security grade and evidence paths. Derived ledger values are checked field-by-field against those facts, the project decision and the recomputed quality score before either ledger sheet changes.
- Review tiers are restricted to `正式推荐`, `条件候选` and `需适配候选`. The JSON parser alone normalizes the legacy `正式` value to `正式推荐`; direct model construction cannot bypass the new enum. Conditions and adaptation candidates cannot be directly deployable. Formal recommendations route to `当前Skill`; the other two tiers route exclusively to `候选观察`.

Review-fix TDD RED covered the destination-link escape, missing/wrong packets, re-signed facts/ledger-row tampering, unknown tiers, direct conditional/adaptation deployment and sheet routing. GREEN verification after the repair:

- Focused Task 7 suite: 27/27 passed.
- Full workflow suite: 101/101 passed.
- `git diff --check`: no whitespace errors.

## Review-fix round 2

A final identity-binding regression showed that the service previously trusted only the outer `review_packets` mapping key. It now rejects any packet whose embedded `candidate_id` differs from the candidate ID in the transient review decision, even when version, source, license, safety and evidence fields otherwise match. The new test was RED before the check and is included in the focused suite.
