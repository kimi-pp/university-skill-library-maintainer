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

## Fix round 1 — source contract hardening

The review findings were verified against commit `ef13b490`. The repair adds 9 focused source-contract tests (16 total):

- `EvidenceRoot` is now an explicit, resolved and non-link/reparse evidence boundary. It rejects escapes and linked paths, uses exclusive ordinary-file creation, rereads the SHA-256, and returns source errors for directory, permission and immutable-content-conflict snapshot failures.
- The GitHub command-runner route parses JSON HTTP errors from `stderr`; a 422 is reported with `status_code=422` and the originating `query_id` after exactly one command invocation. It also resolves `owner/repo` or a GitHub discovery URL to repository metadata, resolves the default branch to a commit SHA, then snapshots that fixed commit archive.
- SkillHub, ClawHub and Hugging Face Spaces map native IDs (and supported discovery URLs) to their API endpoints. Their fixed-version snapshots are read-only metadata responses, persisted only inside the explicit `EvidenceRoot`; GitHub persists its fixed commit archive. Tests cover version and content hashes, HTTP errors and the no-write error path.
- Hugging Face incremental discovery now sorts newest-first and filters client-side strictly later than the stored watermark; an unparseable/missing timestamp returns `partial` so a watermark cannot advance. The actual REST endpoint accepts `sort=lastModified&direction=-1`, which is the wire-format equivalent of descending `last_modified`; the initially requested `sort=last_modified&direction=desc` was confirmed by the doctor probe to return HTTP 400 and was not retained as a non-working parameter spelling.
- Search-created `SourceError` objects now retain the originating `QueryJob.query_id`.

Fix-round TDD RED:

1. The new security-contract test initially failed because `EvidenceRoot` did not exist.
2. The baseline verification found direct review defects: raw identity URLs, arbitrary evidence directory writes, blank search error query IDs, ignored GitHub `stderr` 422 errors/retries, unsafe exception-union syntax, and Hugging Face's unsupported incremental parameter.
3. Changing the test to the endpoint's accepted REST spelling produced the expected two URL assertion failures before the final Hugging Face wire-format change.

Fresh fix-round verification with the locked Python runtime:

- focused source suite: 16/16 passed;
- complete workflow suite: 66/66 passed;
- `git diff --check`: clean.

The final doctor-only one-page, fixed-query smoke reported HTTP 200 for SkillHub, ClawHub, GitHub and Hugging Face Spaces. It supplies no `EvidenceRoot`, parses no candidates, writes no ledger rows, and keeps automation disabled.

## Fix round 2 — identity and concurrent-evidence closure

The re-review found that the GitHub search identity and snapshot interface did not form a closed loop, and that the evidence writer still surfaced a concurrent-create or search-page write failure as an uncaught exception. The repair adds 5 focused tests (21 source tests total):

- GitHub candidates now use `full_name` (`owner/repo`) as `native_id`; the numerical GitHub repository ID is retained only as `popularity["repository_id"]`. A search candidate is passed through `latest_version` and a fixed archive snapshot in one command-runner test.
- GitHub snapshots now reject blank refs, branch names, tags, short/long identifiers and non-hex values before calling `gh`. Only a full 40- or 64-hex commit SHA reaches the archive endpoint.
- `EvidenceRoot` handles a bounded exclusive-create race: after `EEXIST` it only reuses an existing file if two observations show stable, complete same-content bytes. It does not overwrite a competing file.
- Page-evidence persistence failures are converted to `SourceError` with the active `query_id`: no candidates yields `failed`; already discovered candidates yield `partial`. No exception escapes the source adapter.

Fix-round 2 RED (21-test focused run before repair): numerical GitHub identity `42` raised `ValueError` in `latest_version`; `main`, tags, short/long/non-hex refs each invoked the archive endpoint; concurrent `O_EXCL` raised `FileExistsError`; and an evidence directory collision escaped `search` as `ValueError`.

Fresh fix-round 2 verification with the locked Python runtime:

- focused source suite: 21/21 passed;
- complete workflow suite: 71/71 passed;
- `git diff --check`: clean.

The final doctor-only one-page probe again reported HTTP 200 for all four platforms and made no evidence, ledger or candidate writes.

## Fix round 3 — page-based partial coverage

`SearchBatch` failure classification now uses previously completed response pages (`SourceRequestEvent.response_sha256`) rather than the number of normalized candidates. This preserves the distinction between an empty but successfully covered page and a failed first page.

TDD RED added two empty-result pagination cases: an initial successful `items=[]; has_next=true` page followed by HTTP 503, and the same initial page followed by a second-page evidence-directory collision. Both were incorrectly `failed` under the candidate-count rule; both are now `partial`. An evidence failure on the first page remains `failed`, even if that page had candidate objects, because no completed/evidenced page exists.

Fresh fix-round 3 verification with the locked Python runtime:

- focused source suite: 23/23 passed;
- complete workflow suite: 73/73 passed;
- `git diff --check`: clean;
- doctor-only one-page fixed-query probe: HTTP 200 for all four platforms, with no writes and automation still disabled.
