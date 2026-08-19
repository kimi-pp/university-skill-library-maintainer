---
name: institutional-epistemic-sink-forensics
owner: AAA
description: "Diagnose whether an institution shows Calhoun's behavioral-sink pattern — role saturation without truth metabolism. Routes through arifOS judge with disciplined"
source: hermes-only
synthesized: 2026-08-08
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---
<!-- RENAMED 2026-08-13 per F13 directive: Calhoun-style institutional-failure vocabulary replaced with governance-effectiveness terms (governance drift, ceremonial control). -->


# Institutional Epistemic Sink Forensics

A class-level discipline for diagnosing whether a named institution exhibits the **Calhoun behavioral-sink pattern** — operational success that has blocked foundational revision, role saturation without truth metabolism, citation chain inertia, and institutional defense of the operating-system model.

**Subsumes:** The 8-channel institutional body language framework (capital posture, institutional breath, personnel movement, information posture, governance posture, maintenance behaviour, boundary behaviour, crisis reflex). Load `references/institutional-body-language-8-channels.md` for the full framework.

Distinct from:
- **Geological model artifacts** (`geological-artifact-publication`, `scientific-manuscript-forge`) — those forge publication PDFs. This one is forensic: scan the institution, hold the verdict, route through arifOS.
- **Capital allocation** (`wealth-capital-thermodynamics`) — that one models money flows. This one is institutional, not financial.
- **ML paper writing** (`research-paper-writing`) — wrong domain entirely.

## When to use

Use when the user names a specific institution and asks to test whether it shows the epistemic-sink pattern. Common phrasings:

- "Test the theory on [institution name]"
- "Run the WEALTH audit on [institution]"
- "Prompt opecnode / prompt WEALTH to test this theory" (where "opecnode" = WEALTH federation colloquial)
- "Is [institution] showing the Calhoun pattern?"
- "Does [institution] exhibit epistemic sink?"
- "Is [employer / agency / group] in role saturation without truth metabolism?"
- "Read the institutional body language of [institution]"
- "What's the state of [institution]?"
- "Run [institution] through the 8-channel framework"

Do NOT use when:
- The institution is well-documented in open corpus (Enron, Lehman, 1MDB) — the existing `wealth-collapse-signature` skill handles those. This skill is for **less-documented / sub-function / personal-experience cases** where the corpus does not yet have vocabulary.
- The user wants pure capital metrics — use `wealth-capital-thermodynamics`.
- The user wants a falsifiable scientific model manuscript — use `scientific-manuscript-forge`.

## The Pattern (proven 2026-07-03, Petronas Exploration Geoscience audit)

### Step 1 — Establish the meta-hypothesis (Calhoun translation)

Before driving any tool, write the meta-pattern in your own words. The Calhoun Universe 25 (1968-73) translation:

| Calhoun Universe 25       | Institutional equivalent                         |
|---------------------------|--------------------------------------------------|
| Unlimited food/water      | Budget, data rooms, seismic, reports, consultants|
| High-density enclosure    | Committees, departments, approval chains          |
| Social role breakdown     | Nobody owns first-principles questioning          |
| "Beautiful ones" withdraw | Smart staff become presentation polishers         |
| Reproduction collapse     | No new theories survive internal review           |
| Governance drift           | Citation sink / committee sink                    |

**Key thesis:** The collapse is not lack of resources. The collapse is **role saturation without truth metabolism.** Everyone has a role. Nobody has authority to break the false frame.

### Step 2 — GATHER public facts about the institution

Required before driving any WEALTH tool. The 4 mandatory checks demand real numbers, not vibes:

```
- Latest annual report (PAT, dividend, capex, headcount)
- 5-year trajectory (any sigmoid? any margin compression?)
- Public dissent / whistleblower signals
- Recent press coverage
- Industry analyst views
```

For sub-function analysis (e.g. one division of a healthy parent), document:
- 5 Graph-pattern observations: working network, output/exchange rate, meeting organiser ratio, matrix/line manager split, mobility reset frequency
- Specific evidence dossier: emails, meetings, decisions, dated with sources
- Rival explanations explicitly named (never fabricate)

### Step 3 — RUN the 4 mandatory checks (per wealth-collapse-signature skill)

Use the WEALTH federation tools via FastMCP Python client:

```python
from fastmcp import Client
import asyncio

async def audit():
    async with Client("http://127.0.0.1:18082/mcp") as c:
        # 1. Conservation: do the books balance?
        cons = await c.call_tool("wealth_conservation_check", {
            "assets": [...],   # list of {name, value, year}
            "liabilities": [...],
        })

        # 2. Flow: revenue/expense trajectory
        flow = await c.call_tool("wealth_flow_check", {
            "income": [...],    # list of {period, value, note}
            "expenses": [...],
        })

        # 3. Entropy / EMV: tail thickening
        emv = await c.call_tool("wealth_compute_emv", {
            "outcomes": [...],      # numeric
            "probabilities": [...], # must sum ~1.0
        })
        # ⚠ wealth_compute_emv needs preload wealth://reality/context.
        # If preload is broken, capture the failure and continue.

        # 4. Survival / runway
        runway = await c.call_tool("wealth_runway_check", {
            "liquid_assets": float,
            "monthly_burn": float,
        })
```

If any of these cannot be computed with real data, **defer the collapse claim** — collapse signature is a forensic tool, not a panic button.

### Step 4 — SCAN against 7 collapse signatures + Calhoun Phase C

```python
# Collapse signature (7-axis + Acemoglu×Calhoun 2D map)
collapse = await c.call_tool("wealth_collapse_signature_scan", {
    "scenario": "Full narrative text of the institution's current state, "
                "with named evidence_for and evidence_against",
    "capital_type": "institutional_sub_function",  # or "financial"
    "historical_priors": ["Enron", "PDVSA", "Pemex", "1MDB", "Suriname_beautiful_mouse"],
})

# Beautiful Mouse (Calhoun Phase C, 6 indicators)
mouse = await c.call_tool("wealth_beautiful_mouse_scan", {
    "text": "Narrative of the institution's public communications, "
            "including slogans, mission statements, recent PR",
    "historical_priors": ["Calhoun_Universe_25", "Suriname_beautiful_mouse"],
})
```

**Critical pitfall (proven 2026-07-03, CONFIRMED with real data 2026-07-07):** WEALTH's scanner vocabulary is calibrated to **state-level institutional collapse** (Enron, PDVSA, Pemex, 1MDB) and **terminal-stage Phase C narratives** (perfect-performance slogans, zero-failure marketing). It does NOT have vocabulary for **sub-function epistemic sink** (committee-density, citation-inertia, career-fear patterns), **earlier-stage institutional sink** (signals that haven't crystallized into terminal phrase-pool), OR **simulative exploitation** (external actors exploiting institutional weakness through legal/procedural means).

**Proven example (2026-07-07):** PETRONAS 2024-2026 case was run through `collapse_signature_scan` with full narrative (32% profit drop, 10% rightsizing, BOD at 7, RM1B Shell freeze, Sarawak MBR freeze, espionage leak). Result: **0.0 risk, MINIMAL, 0 signals across all 7 axes.** The scanner literally said "No institutional-collapse signature detected" for an institution in active multi-front crisis. Why? Because PETRONAS's collapse is SIMULATIVE (external exploitation), not EXTRACTIVE (internal theft). The scanner only knows extraction.

**New tools that fill the gap (built 2026-07-07):** `wealth_institutional_stress_index` (0.67 RED for PETRONAS), `wealth_external_exploitation_detect` (0.62 AGGRESSIVE for Shell MDS). At `/root/wealth/wealth_core/institutional/`.

**The honest meta-verdict you'll likely get:**
- `wealth_collapse_signature_scan` returns `INSUFFICIENT_SIGNAL` on all 7 axes — this is a **vocabulary gap**, not a falsification of the diagnosis.
- `wealth_beautiful_mouse_scan` returns `Phase C ABSENT` with "appears to be in healthy friction" — this means the institution hasn't yet reached terminal stage, NOT that there's no sink.

**DO NOT promote to SEAL on sub-function patterns the corpus cannot quantify.** Hold the diagnosis at 0.50-0.60 confidence. Document the gap. Move on.

### Step 5 — Pair with capture_scan + power_audit

These two checks verify that **the diagnosis itself is clean** (not a vendetta, not a captured narrative):

```python
# Capture scan: is the diagnosis itself captured?
capture = await c.call_tool("wealth_capture_scan", {
    "advice_text": "The diagnosis text — paste the conclusion here",
    "source_model": "federation_we_geo_<date>",
})

# Power audit: is the power asymmetry documented?
power = await c.call_tool("wealth_power_audit", {
    "scenario": "Detailed description of the power play, with named actors",
    "actors": ["actor_a", "actor_b"],  # role names, never individual verdicts
    "context": {
        "evidence_basis": "list of evidence sources",
        "f6_maruah_check": "names role not individual verdicts",
        "refusal_surface": "preserved",
    },
})
```

**Pitfall (2026-07-03):** `wealth_power_audit` misses "dossier" / "task reassignment" patterns. It scans for capture dimensions (incentive asymmetry, rent extraction, coercion), not HR-style power asymmetry. Document the power pattern qualitatively; don't expect the scanner to detect it.

### Step 6 — SYNTHESIZE with omni_wisdom

```python
synthesis = await c.call_tool("wealth_omni_wisdom", {
    "mode": "synthesize",
    "decision_context": {
        "domain": "institutional_epistemic_sink",
        "subject": "<institution name>",
        "pattern": "Calhoun beautiful-mouse + epistemic sink",
        "evidence_for": int,
        "evidence_against": int,
        "confidence": 0.50-0.60,  # HOLD at sub-function tier
    },
    "institutional_trust": {
        "trust_level": "low_for_sub_function_high_for_group",
        "rationale": "group financials solid, sub-function shows role saturation",
    },
    "memory_query": "Calhoun epistemic sink <institution>",
})
```

`wealth_omni_wisdom` returns `HOLD` on under-specified context. Empty `decision_context` → `"synthesis": {"summary": "(no decision context provided)"}`. Always populate decision_context fully.

### Step 7 — Constitutional HANDOFF to arifOS

This is the **separation of powers** — WEALTH prepares, arifOS judges, Arif decides. WEALTH never declares the verdict.

```python
import json

# Build the handoff envelope
envelope_result = json.dumps({
    "verdict": "PARTIAL EUREKA" or "HOLD" or "DIAGNOSIS UNCERTAIN",
    "signatures_active": ["governance_sink", "narrative_centralisation", "talent_drain"],
    "signatures_absent": ["financial_sigmoid", "counterparty_contamination"],
    "confidence": 0.58,
    "blast_radius": "personal_career_not_group_collapse",
    "reversibility": "subject_reversible_group_irreversible",
})

# Call WEALTH judge_handoff
handoff = await c.call_tool("wealth_judge_handoff", {
    "tool_name": "wealth_collapse_signature_scan",
    "result": envelope_result,
    "intent": "Register collapse signature claim against <institution>",
    "capability": "register_collapse_signature_claim",
    "blast_radius": "MEDIUM",
    "reversibility_level": "PARTIAL",
})
# ⚠ wealth_judge_handoff needs preload wealth://handoff/arifos-schema,
# wealth://affordance/contracts. If preload is broken, capture failure
# and submit directly to arifOS judge instead.

# Submit to arifOS judge (port 8088)
async with Client("http://127.0.0.1:8088/mcp") as arifos:
    judge = await arifos.call_tool("arif_judge", {
        "actor": "Arif (F13 SOVEREIGN)",
        "intent": "Constitutional judgment on institutional epistemic sink diagnosis",
        "requested_capability": "judge_institutional_diagnosis",
        "domain": "capital_governance",
        "reversibility_level": "reversible",  # diagnosis is reversible
        "blast_radius": "personal_career",
        "evidence": [{"type": "wealth_collapse_signature_scan", "result": envelope_result}],
    })
```

The handoff correctly enforces: **WEALTH prepares, arifOS judges, Arif decides.** WEALTH never declares the verdict.

### Step 8 — Write the audit receipt

Save a Markdown audit receipt with:

```markdown
---
title: "WEALTH Audit — <institution> <date>"
epistemic_class: OBSERVED + DERIVED
source: WEALTH MCP :18082 + wealth-collapse-signature skill
confidence: high-on-tooling, medium-on-diagnosis
note: "Live MCP audit of <institution>. Result: ... Constitutional handoff to arif_judge prepared."
---

# WEALTH Audit Receipt — <institution>

## 1. Live Tool Receipts (MCP :18082)
... (paste JSON outputs)

## 2. 7-Signature Scan Result
... (collapse_signature result)

## 3. Beautiful Mouse Scan Result
... (beautiful_mouse result)

## 4. Capture Scan Result
... (capture result, confirm LOW)

## 5. Power Audit Result
... (power result)

## 6. Omni Wisdom Verdict
... (HOLD/SEAL)

## 7. Constitutional Handoff
... (judge_handoff result, READY/HOLD)

## 8. Meta-Verdict on the Audit Itself
... (consolidate findings, name scanner vocabulary gap)

## 9. Recommendation
... (HOLD at 0.58 confidence, do not seal, name falsification tests)

## 10. CAPSULE LINE
CAPSULE_ID: WEALTH_AUDIT_<INSTITUTION>_<DATE>::v1.0
STATUS: HOLD
ACCESS: <user> only. Sovereignty preserved.
```

### Step 9 — Sovereignty preservation (CRITICAL)

If the institution being audited is the user's employer, supervisor, or personal network:

- **NEVER push the audit receipt to a public repository.** Place it in a `.gitignore`-protected folder (e.g. `HAMPA/`, `LIFE/`, `PROPA/`).
- The `.gitignore` `*` rule with `!*.md` exception DOES NOT override nested paths under `*` — the pattern matches `*` first, then `!*.md` is overridden. HAMPA stays protected by design. **Do NOT force-add with `git add -f`.**
- Use the `git check-ignore -v <path>` command to verify which rule is protecting a path before considering commit.
- The git commit message can reference the local file's existence (in INDEX.md folder tree) without leaking the content.

### Step 10 — Falsification tests (what to wait for)

Name explicit falsification tests in the audit receipt. For a sub-function epistemic sink diagnosis:

| Test | Discriminates | Data source |
|---|---|---|
| MYPR outcome (next cycle) | Updates "career dependency" quantification | Internal HR system |
| Citation drift (Hutchison 1996 → Hall 2013 adoption rate) | Updates "narrative centralisation" | Internal literature reviews |
| AI tool flagging rate | Updates "competence control" threat signal | Internal IT logs |
| Task reassignment rate | Updates "matrix manager dossier pattern" | Project records |
| Tomography / KT-7 depth conversion | Updates geological sibling diagnosis | External data |

The discipline is: **the diagnosis is option value, not verdict.** Wait for the tests. Hold the confidence at 0.58. Do not seal.

## The 5 GEOX anti-Calhoun Rules

Per ChatGPT's institutional forensics (2026-07-03), the cure for epistemic sink is not the absence of institutions — it's institutions that:

1. **Every model must carry rivals** — corrected claim `9cf5ec26c45f40ed` named 4 explicit rivals. Strength, not weakness.
2. **Confidence must drop when contradictions increase** — 0.72 → 0.58 is strength. Lower-confidence claim with clean falsification tests beats high-confidence myth.
3. **No committee approval without falsification path** — every basin/institutional model must include: What observation kills this model? What observation upgrades it? What observation distinguishes it from rivals? No answer, no budget.
4. **Separate production truth from discovery truth** — production asks "Can we drill this safely and make money?" Discovery asks "Are we looking at the basin correctly?" Confusing these is the institutional failure.
5. **Reward the person who breaks the wrong model** — most institutions reward the person who defends the plan. GEOX-style institutions reward the person who kills a false premise early. Cheaper than drilling the lie.

## Pitfalls Discovered

0. **Over-cynical reading of genuine human moments (2026-07-06).** When Arif describes a session as "orang kampung style," "like father and sons," "just being honest" — do NOT default to Acemoglu/Calhoun strategic frameworks. Witness first, analyze only if asked. Reaching for power-play analysis on a genuine human connection is a category error. Arif's correction: "Hang betul. Aku terlalu cynical tadi." See `references/witness-before-analyze.md` for the full protocol.
-0.5. **Lived-reality reading (2026-07-12).** When the user IS inside the institution (employer, client, partner), the most powerful reading combines tool outputs with their lived experience. Tools return 0.0 GREEN; their life returns rightsizing, MSS traps, boss being moved, capability erosion. The user's body IS the institutional body language. Don't just run tools — ask what the institution's treatment of its own people reveals about what it actually values. The contradiction between "People are our greatest asset" and "10% rightsizing, Bain engaged" IS the diagnosis.
1. **Scanner vocabulary mismatch.** Sub-function epistemic sink AND simulative exploitation are NOT in the WEALTH corpus. `INSUFFICIENT_SIGNAL` or `0.0 risk MINIMAL` is a vocabulary gap, not a falsification. **Proven 2026-07-07:** PETRONAS active crisis returned 0.0 on collapse_signature_scan. New tools (`wealth_institutional_stress_index`, `wealth_external_exploitation_detect`) fill this gap. Use them when collapse_signature_scan returns 0.0 but you KNOW the institution is under stress. Document, don't promote to SEAL.
2. **Preload gate may block handoff.** The `wealth://` preload reads currently return `NoneType` errors from the FastMCP client. The daemon may still apply the gate even when your read failed. Workaround: prioritize the diagnosis tools (no preload), only attempt handoff if preloads confirmed.
3. **F6 MARUAH violation risk.** Never name a specific individual as the cause of institutional failure. Reference roles (matrix manager, dossier-builder, escalation layer), not people. Maintain refusal surface (no verdicts on named staff).
4. **Power asymmetry is multi-layer.** Dossier-builder (Laletha) + escalation layer (Kak Su) = two-layer institutional response. Document both layers; don't reduce to a single actor.
5. **Don't promote on weak evidence.** The discipline is HOLD at 0.58 confidence until falsification tests resolve. The constitution honors this — `arif_judge` returns HOLD when evidence is insufficient, and that's correct.
6. **The F13 escalation is correct behavior.** When an irreversible+federation-wide diagnosis is staged, arifOS demands F13 SOVEREIGN cryptographic signature. Don't fight it. Escalate to Arif.
7. **Tool-behavior-as-diagnostic (2026-07-12).** When WEALTH tools return 0.0 GREEN with missing fields, INSUFFICIENT_SIGNAL on all axes, or ERROR on text — the tool failures THEMSELVES are institutional body language signals. SILENT_DEFAULT_RISK = "if you don't provide data, we assume everything is fine." INSUFFICIENT_SIGNAL = "if our vocabulary doesn't match your risk, you're clean." NEUTRAL on exploitation = "we only see theft, not extraction." Document the tool behavior as part of the audit, not just the tool outputs. See `references/wealth-tool-body-language-gaps.md`.

## Falsification Discipline — The YELLOW Band Posture

The audit pattern deliberately lands at **YELLOW band** rather than GREEN/RED:

- GREEN = SEAL-able, evidence + rivals + tests all aligned. Not realistic for sub-function epistemic sink.
- YELLOW = plausible, evidence mixed, scanners off-vocabulary, falsification tests pending. **This is the honest posture for any novel institutional diagnosis.**
- RED = falsified or denied. Not applicable — the diagnosis is qualitatively real even if scanners are silent.

**The verdict pattern:** "PARTIAL EUREKA — confidence 0.58, scanners off-vocabulary, falsification tests pending, do NOT seal." That's the right answer for any novel institutional diagnosis until the WEALTH corpus catches up.

## Cross-References

- **`references/institutional-body-language-8-channels.md`** — PRIMARY: the 8-channel institutional body language framework. Load for any institutional reading.
- **`references/wealth-tool-body-language-gaps.md`** — WEALTH tool capabilities vs 8-channel gaps. Load when running WEALTH tools against an institution.
- **`references/witness-before-analyze.md`** — CRITICAL: when NOT to decode. The over-cynical pitfall, witness-before-analyze protocol, MSS moment pattern, recalibration protocol. Load this FIRST when Arif shares a personal/vulnerable moment.
- **`references/people-research-and-cultural-decoding.md`** — institutional people forensics, communication style decoding, PETRONAS DNA context
- **`references/media-contradiction-mapping.md`** — Lightweight media contradiction mapping + PR narrative forensics. 6-phase pipeline: internal intelligence → external sweep → contradiction grid → timeline reconstruction → PR coordination detection → "prove me wrong" test. Use when the question is "what is media saying and who is coordinating it?" (vs the WEALTH-tool financial audit path below). Proven on SEARAH Eni-PETRONAS audit 2026-07-22. No WEALTH tools required.
- **`wealth-capital-thermodynamics`** — for pure capital allocation questions
- **`wealth-law-anthropology`** — when the collapse touches legal doctrine (pusaka / corporate / regulatory)
- **`geox-federation-mcp-driver`** — for the FastMCP Python client pattern, schema discovery via Pydantic errors, evidence/claim workflows
- **`geological-artifact-publication`** — when the diagnosis becomes a publication (e.g. Kinabalu two-oceanics + Calhoun paired manuscript)
- **`scientific-manuscript-forge`** — for the manuscript forge pipeline including YELLOW band tightening discipline
- **`/root/AAA/docs/FEDERATION_COCKPIT.md`** — AAA agent cards + A2A routing
- **`/root/AGENTS.md` §10.5 Dynamic-State Principle** — probe T₁ immediately before any irreversible call (judge, seal, vault_write)
- **`references/institutional-body-language-framework.md`** — 8-channel institutional body language framework. Load for any institutional reading.
- **`references/petronas-cadence-monitor-findings.md`** — PETRONAS cadence readings (2024-2026). Load when analyzing institutional breath or cadence.

## Files

- `references/institutional-body-language-8-channels.md` — **PRIMARY FRAMEWORK**: 8-channel institutional body language (capital posture, breath, personnel, information, governance, maintenance, boundary, crisis reflex), signal hierarchy, regulatory states, four-reading discipline, 10 revealing questions. Load this FIRST for any institutional reading.
- `references/wealth-tool-body-language-gaps.md` — WEALTH tool capabilities mapped against 8-channel framework. Documents tool failures as diagnostic signals, SILENT_DEFAULT_RISK mechanism, simulative vs extractive exploitation vocabulary gap, build priority for embedding remaining channels.
- `references/petronas-exploration-audit-2026-07-03.md` — full real audit receipt (proven pattern, copy as template) with the 11-tool WEALTH output and the Python recipe
- `references/people-research-and-cultural-decoding.md` — how to research and profile institutional personnel, decode communication styles ("orang kampung style", "father and sons"), and connect individual behavior to institutional DNA signals. Includes the PETRONAS founding values reference and Arif-specific patterns.
- `references/calhoun-institution-translation-table.md` — extended Calhoun → Institution mapping including 9 collapse types (7 originals + Type 8 sub-function sink + Type 9 wealth-capture-sink loop)
- `references/9-signal-envelope-vocabulary.md` — the 9 constitutional verdict states (KUKUH/RETAK/SYUBHAH/BIJAK/AMANAH/etc) and how to read arifOS + WEALTH envelopes honestly
- `templates/audit-receipt-template.md` — Markdown template for audit receipts (10 sections + capsule line)
- `scripts/run_wealth_audit.sh` — bash wrapper that probes WEALTH liveness, activates GEOX venv, and runs the audit Python script
- `references/institutional-body-language-framework.md` — 8-channel institutional body language framework. Signal hierarchy, reading discipline, channel specifications, regulatory states.
- `references/petronas-cadence-monitor-findings.md` — PETRONAS cadence readings (2024-2026). Component breakdown: approval centralization, payment stretching, decision backlog, contract velocity, budget release.