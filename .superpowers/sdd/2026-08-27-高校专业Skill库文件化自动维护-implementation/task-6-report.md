# Task 6 report — four read-only source adapters and Excel watermarks

## Scope and implementation

- Added the `skill_maintainer.sources` package with normalized candidates, request events, source errors, version observations, immutable snapshots, and the `SourceAdapter` protocol.
- Added read-only paged adapters for SkillHub, ClawHub, GitHub, and Hugging Face Spaces. HTTP adapters use `urllib.request` with an explicit timeout. The production GitHub route invokes `gh api --method GET <endpoint>` through an argument list only; candidate content is never executed.
- Search records byte SHA-256 evidence; optional evidence persistence is immutable and caller-directed, so it can only be aimed at the project evidence area rather than the Excel master ledger.
- Added retry/partial semantics: transient network/5xx/429 failures retry only to the configured bound; a failure after prior pages returns `partial`; GitHub HTTP 422 returns a source error without retries; searches exceeding GitHub's visible 1,000-result ceiling return `partial`.
- Added `SourceWatermarkStore` using named columns in the Excel `来源水位` sheet. It advances only a completed platform/query batch, preserves old values for failed or partial batches, and supplies a one-run full-recheck decision without deleting the stored incremental watermark.
- Added `doctor_smoke`: fixed harmless `university skill` query, exactly one page, no candidate parsing, no ledger update and no evidence write. CLI wiring remains intentionally out of scope for Task 13.

## TDD record

1. Initial contract test run was RED because `skill_maintainer.sources` did not exist (`ModuleNotFoundError`).
2. The doctor-only smoke contract was then added and verified RED because `doctor_smoke` was absent (`ImportError`).
3. The resulting focused suite is GREEN: 7/7 tests passed.

## Fresh verification

Using the project-locked Python 3.12.13 runtime with `PYTHONPATH=07_自动维护工作流/src`:

- `python -m unittest 07_自动维护工作流/tests/test_sources.py -v` — 7 tests passed.
- `python -m unittest discover -s 07_自动维护工作流/tests -v` — 57 tests passed.
- `git diff --check` — clean before the implementation commit.

Doctor-only network smoke ran after the focused test and fetched exactly one fixed-query page per platform, with no evidence or ledger destination configured:

| Platform | Endpoint/authentication result |
| --- | --- |
| SkillHub | ok |
| ClawHub | ok |
| GitHub | ok |
| Hugging Face Spaces | ok |

Automation settings were not changed or enabled. No candidate rows, ledger rows, or source evidence files were written during that smoke check.

## Commit

- `ef13b490` — `feat: add four read-only source adapters`

## Boundary note

The Task 6 protocol exposes the doctor-only probe but does not wire it into the placeholder CLI. That wiring is explicitly scheduled for Task 13; changing `cli.py` here would cross the approved task boundary.
