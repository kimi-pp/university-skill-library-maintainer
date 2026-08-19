---
name: cipher
description: >-
  Front-door orchestrator for ALL Cipher/Harbor security-task work. ALWAYS start
  here. Use whenever building a Harbor task, or whenever a grader check fails and
  you paste its log (Setup / Environment / Agent-run / Submission-gate checks like
  Oracle Check, Verifier Gameability, Prompt Hygiene, Fair task, Solvable,
  Difficulty, No cheating, etc.). This skill reads the situation, routes to the
  correct sub-skill (cipher-harbor-foundations, cipher-check-setup,
  cipher-check-environment, cipher-check-agentrun, cipher-difficulty), applies the real fix, and
  folds the technique back into the owning skill's decision log.
---

# Cipher — Orchestrator (start here every time)

You are the manager for Cipher/Harbor task work. The user does NOT need to know
which sub-skill to pick — **you decide and load it.** There are only two modes.

## Step 0 — figure out the mode

- The user pasted a **failing check log** → **Mode: FIX** (the common case).
- The user wants to **build a new task** from a repo/CVE/vuln idea → **Mode: BUILD**.

If it's unclear, ask one line: *"Fixing a failing check (paste the log) or building a new task?"*

## Mode: FIX  (paste a check log → route → real fix)

1. **Identify the failing check name** in the log. Match it in the router table.
2. **Load that ONE sub-skill** (read its SKILL.md; open its reference.md if you
   need the deep template/gauntlet/decision-log).
3. **Apply the minimal real fix.** Prefer a real fix. Only consider a bypass note
   if the same fix is getting repetitive — and **ask the user first**.
4. **Re-prove the invariant** where applicable: `scripts/validate.sh <repo> [py]`
   gives `vulnerable→0, solve→1, revert→0`. For Oracle Check, also do a clean
   `mktemp` extract of the 3 zips (no enclosing git).
5. **Fold the technique** into the owning sub-skill's "Decision / iteration log
   (newest first)" so the next occurrence is one lookup.
6. **Report TERSELY.** The user does NOT want the deep technical write-up
   (root-cause narrative, repro steps, per-test counts). Give at most: a one-line
   what-was-wrong, a one-line what-was-fixed, the 0→1→0 pass/fail result, and —
   **always state explicitly whether you rebuilt the zips** (which ones, or "no
   zip changes needed"). Keep it to a few lines unless the user asks for detail.

### Router — check name → sub-skill

| Failing check | Load |
|---|---|
| Source Metadata · Prompt Word Count · Prompt Conciseness · Category Alignment · Text Validity · Originality · Verifier Harness · Verifier Bundle · **Prompt Hygiene** · Task & Verifier Quality · AI Trace Cleanup · **Verifier Alignment** · **Verifier Gameability** · (`valid_test_patch`/`reward_semantics`/`security_signal`/`shortcut_resistance`) | **cipher-check-setup** |
| Environment Dockerfile · Reference Solution · Verify Build · No-op Check · **Oracle Check** · Task Realism · Reference Quality | **cipher-check-environment** |
| Fair task · **Solvable** · **Difficulty** (diagnose the spread) · **No cheating** · No environment blockers · **Cross-Run Analysis** | **cipher-check-agentrun** |
| **Difficulty TUNING** — move the solve rate (Nova too easy/too hard; "make it harder"/"make it easier") | **cipher-difficulty** |
| (template/layout/invariant question, or check name not above) | **cipher-harbor-foundations** |

### Cross-routing (when a verdict points elsewhere)

In **cipher-check-agentrun**, read the fault flag first and re-route:
- `environmentFault` (No environment blockers) → fix in **cipher-check-environment**.
- `cheating` (No cheating) → harden in **cipher-check-setup**.
- `agentFault` with a healthy pass/fail spread → usually **nothing to fix** (good difficulty).
- `taskFault` → the task is broken; fix it (often back to setup or environment).
- Difficulty off-target (too easy / too hard) and you need to **move the solve
  rate** → diagnose the spread in agentrun, then apply the lever ladder in
  **cipher-difficulty** (de-hint → add an Nth gated gap → restructure the verifier).

## Mode: BUILD  (new task from scratch)

1. **cipher-harbor-foundations** → pick the pattern (Python service / Go OSS),
   copy templates, write `environment/ + tests/ + solution/`, prove `0→1→0`.
2. Pre-empt graders before submit, in dashboard order:
   **cipher-check-setup** (hygiene, gameability, literal reward writes) →
   **cipher-check-environment** (solve.sh root-resolution, bake `pytest`/`patch`,
   no baked secrets).
3. Submit → then you're in Mode: FIX for whatever the dashboard flags.

## Workflow order (the dashboard gates top-to-bottom)

```
Setup checks ─► Environment checks ─► Agent runs ─► Submission gate
 (~13, cheap)     (~7, slow build)   (screening,    (re-runs all;
(cipher-check-     (…-environment)    ~12 energy)    Cross-Run)
 setup)                              (…-agentrun)
```
Fix Setup first — downstream stages don't run meaningfully until Setup is green.

## Platform mechanics (cross-cutting — true no matter which check failed)

These are harness/platform facts that bite across every task. Carry them into
every BUILD and every FIX; they explain a lot of "my solve worked but the check
says fail" confusion.

- **The `/tmp/cipher-baseline` source leak (design around it).** Before the agent
  runs, the harness snapshots the workdir (and any dir named in `task.toml`) to a
  `.tar` at `/tmp/cipher-baseline` to diff the agent's changes. The snapshot
  includes root-owned files **with contents, and your `chmod` perms are NOT
  enforced on the copy** — so the `player` agent can read your source straight out
  of the tar and skip the intended attack. **Fix: keep source + sensitive files
  OUT of the workdir**, in a root-owned `700` dir like `/opt/<task>/`; leave
  `workdir = "/app"` as a throwaway. Runtime-generated secrets (`os.urandom`) are
  safe (never on disk at snapshot time); **source files and anything written at
  build time leak.** For pwn: suid binary + source live outside the workdir.
- **`task.toml` reverts on every env re-upload.** Re-uploading the environment zip
  flips `[agent] user` back to `root` and drops the `[verifier]` block. **Re-add
  `[agent] user = "player"` and `[verifier] user = "root"` and re-validate every
  single time** after a re-upload. Agent must be unprivileged or the "can't read
  the secret/source" premise collapses; verifier root so it can grade against
  root-owned reference files.
- **Everything re-stales on any change** — prompt edit, env re-upload, task.toml
  edit all re-stale the whole gate. **Batch your edits**; a "quick tweak" can cost
  a full re-run of setup + env + screening.
- **The AI-like % badge is cached** — it does NOT recompute on edit; re-run setup
  to refresh. Real typing/pasting triggers a re-score; a scripted paste may not.
  To drive it down: first-person, contractions, kill the balanced "on one hand /
  on the other" cadence, cut em-dashes, sound like an annoyed human.
- **Energy economics.** Setup is cheap (fractions); environment is several points;
  the screening is the big spend (~12) and you get ~3/hour; the submission gate
  re-judges and costs ~6. Runs are slow (the screening can take hours — 3–5h is
  normal). **Sanity-check the env + reference locally before spending a
  screening** — an env check dying on a dumb bug is wasted energy.
- **`instruction.md` + `task.toml` are GENERATED, not hand-written.** They
  regenerate from the overview/prompt tab (title + prompt + category) — edit those,
  don't author the files directly. On the Harbor tab you upload the `environment/ +
  tests/ + solution/` zips and hit **Validate package** (mostly structural + a
  build; the real "does the reference solve it" proof happens later in Oracle
  Check). You can also lay the bundle out in this same structure, push to GitHub,
  and import the repo directly into Shipd.
- **Transient infra errors ≠ your bug.** "cannot create a sandbox" / Modal errors
  (Shipd runs sandboxes on Modal) and `[CONVEX M(...)] Server Error` are usually
  transient — wait and retry; re-run individual agents when infra is back. A stale
  "Launching" batch may show results from a pre-upload env — re-run fresh.

## The screening (Nova) — what "good difficulty" means

The screening runs **3 Nova + 3 Nova-plus agents**. Tiers: **Nova** = screening
tier (decides too-easy vs good), **Orion** another tier, **Vega** the strongest
feasibility check. Underlying models are community guesswork — tune to the bar,
not the model.

- **Aim: Nova solves ≤ ~2/6.** More → flagged "too easy". **0/6 is fine** as long
  as the reference + a stronger tier prove it's solvable — feasibility carries it.
- **Too easy is the only fatal outcome**, not too hard. When tuning, err harder —
  as long as your reference still reliably solves within the env-check time limit
  (aim the shadow run to time out or solve at ~40+ min).
- **Read the trajectories, not just the score.** Confirm: (1) solvers used the
  intended attack, not a cheese; (2) failers failed for a fair reason, not a
  blocker/missing hint; (3) nobody read your source out of the baseline tar.
  A "solve" that stumbled onto something you left open is a fix, not a win.

## Realism (the system will literally say "not realistic enough")

- Frame it as a **service to probe** (registry, notary, KMS, license server) with a
  reason to exist — not a riddle. A 30-line toy gets flagged; build a few endpoints
  + plausible scaffolding. Realism is graded, not vibes.
- **No flags, ever.** Win condition = recovering the real thing (secret, forged
  signature, key); the verifier checks that, not a magic string.
- Steal the badger-merkle sample for tone/structure — but don't reskin it closely
  (Originality check).

## Non-negotiables (carry into every fix)

- Reward = single byte `0`/`1`, **literal** `echo 1 > /logs/verifier/reward.txt`
  (never an unexpanded `$VAR` that can land blank), every path, before exit.
  Default to `0`, flip to `1` only on a real pass.
- No installs / no network in the verifier; deps pre-baked.
- Tests assert security behavior, not formatting/internals. Verifier must be
  **self-contained and opaque** — verify the real property with a real library
  (e.g. `pub.verify(sig, msg)`), never a string-match the agent can fake or a
  transparent check it can satisfy directly.
- Non-root agent (`player`); verifier root; `/logs` root-owned.
- **Source + secrets OUT of the workdir** (root-`700` dir) — the
  `/tmp/cipher-baseline` snapshot leaks anything in the workdir regardless of
  perms. Re-add `[agent]`/`[verifier]` users after every env re-upload.
- Real fix first; bypass only when repetitive, and only after asking.
