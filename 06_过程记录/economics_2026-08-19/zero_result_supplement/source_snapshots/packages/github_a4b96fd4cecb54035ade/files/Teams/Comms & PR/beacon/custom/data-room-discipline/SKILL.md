<!--
Custom skill — built from scratch, synthesized from named published sources
(Feld & Mendelson 2019 + Berkus practitioner corpus + NVCA institutional +
AICPA institutional + SEC EDGAR regulatory + Reg FD inherited). Body follows
§11 required structure + §14.2 exact-heading compiler contract.

Custom new per §2 routing: catalog scaffold decision assigned data-room to beacon.
No marketplace match; Route D custom.

Route D per §8.2 (cited rubric).

Cross-agent §8.9 note: Feld & Mendelson 2019 supports data-room-discipline (this
skill) and any future echo pitch-materials skill whenever built — single
practitioner corpus grounds ≥2 skills across departments. Extract once, use twice.

Cross-agent §13.1 note: this skill INHERITS Reg FD legal fence from
`investor-cadence` (sibling), Buffett-discipline no-fabrication from
`investor-cadence`, Barcelona-measurement from herald's pr_analytics via
Comms & PR precedent. Not re-owned here.
-->
---
name: data-room-discipline
type: custom
status: built from scratch (Route D cited rubric)
sources_referenced:
  - "Feld, Brad & Mendelson, Jason (2019, 4th ed.). Venture Deals: Be Smarter Than Your Lawyer and Venture Capitalist. Wiley. ISBN 978-1119594826. Practitioner text per §8.9 — canonical text on VC due diligence + data-room expectations from the investor side."
  - "Berkus, Dave — Berkus Method + due-diligence checklists. Practitioner corpus at berkonomics.com. Named practitioner (early-stage angel investor + Tech Coast Angels founder)."
  - "NVCA (National Venture Capital Association) — Model Legal Documents + DD Checklist. Institutional. FREE at nvca.org."
  - "AICPA (American Institute of CPAs) — Auditing Standards on documentation (AU-C Section 230, Audit Documentation). Institutional standards for what backing evidence must exist and how retained."
  - "SEC EDGAR — public-filing document standards (institutional/regulatory reference for public-company data-room parallels)."
  - "SEC Regulation FD (17 CFR § 243) — inherited from investor-cadence for material-info tagging + access-control fence. Not re-owned here."
fulfills_catalog_entry: data-room-discipline (custom new per §2)
assigned_agent: beacon (Comms & PR / Investor Comms)
portable: true
date_added: 2026-07-31
tier: 3
description: Data-room organization + document-versioning + access-control + material-info tagging discipline for due-diligence readiness. Feld & Mendelson VC-DD grounding + Berkus practitioner + NVCA institutional + AICPA documentation standards + SEC EDGAR + Reg FD (inherited). Not a document repository itself — the RULES for what belongs, how it's versioned, who has access, and how it's structured for DD readiness. Trigger on "set up data room", "audit our data room", "DD checklist prep", "data-room versioning", "access-control for [document type]", "material-info tagging in data room", "prepare for due diligence", or "clean up stale documents in data room".
triggers:
  - set up data room
  - audit our data room
  - DD checklist prep
  - data-room versioning
  - access-control for
  - material-info tagging in data room
  - prepare for due diligence
  - clean up stale documents
  - shadow versions
  - single source of truth for
---

# Data-Room Discipline

## Introduction

This skill packages the discipline for the evidence backing store that supports
every investor-facing claim beacon ships: due-diligence-ready folder architecture +
document-version discipline + access-control tiers + material-info tagging +
evidence-backing links from `investor-cadence` (sibling) outputs to data-room
documents.

**Scope distinction:** this is the RULES for the data room — what belongs, how it's
versioned, who has access, how it's DD-ready. Not the tooling (which is
platform-specific: DocSend / Dropbox / SharePoint / a purpose-built VDR like
DealRoom / Intralinks / Firmex — tooling choice is operator + counsel scope).

Custom Route D per §8.2 — cited rubric grounded in named published sources; no
formula, no script.

## Purpose

Prevents six failure modes that show up when data-room discipline is absent:

1. **Shadow versions of key documents** — "final_v2_REAL_final.docx" alongside
   "final_v2.docx" alongside "FINAL_use_this_one.docx" creates DD contradictions.
   Investors doing diligence find the shadow versions + ask which is authoritative.
   Answer must be single-source-of-truth or the DD conversation stalls.
2. **Material info surfaced without Reg FD-safe access control.** Data room
   containing material non-public information accessible to a broad investor group
   without Reg FD-simultaneous-public-disclosure = securities-law violation for
   public companies + trust damage at any stage. Access control is legal fence.
3. **Broad-grant access to sensitive DD materials.** Extending data-room access to
   too-broad a group (or too-early in the DD process) leaks strategic info + puts
   negotiation leverage at risk. Standard: access grows narrower → broader across
   DD stages (initial → active-DD → closing).
4. **Silent deletion / edit of prior document versions.** Investors doing DD
   remember what they saw last week. Silent replacement without change-log = trust
   damage + potential fraud allegation. Audit-trail preservation is discipline.
5. **Fabricated / speculative content in DD-backing documents.** Buffett-discipline
   inherited from `investor-cadence`. Aspirational projections without operating-plan
   backing = securities-fraud exposure; case studies / metrics / customer
   references must be actual not fabricated.
6. **Individual crisis DURING DD-preparation crunch.** Team members preparing data
   room under closing pressure + personal distress can coincide. HARD BOUNDARY per
   Universal Principle 3 — individual crisis signal blocks all processing regardless
   of DD-timing pressure.

beacon uses this skill as the operational entry point for all data-room setup,
audit, and maintenance work. Coordinates upstream with `investor-cadence` (sibling
— every claim in cadence outputs needs backing here) and with echo (Executive
Office — pitch materials + board prep coordinate with data room for evidence
consistency).

## When to Use

Trigger on:

- "Set up data room" / "new data room for [round / event]" / "data-room initial architecture"
- "Audit our data room" / "data-room cleanup" / "stale documents in data room"
- "DD checklist prep" / "due-diligence readiness" / "prepare for due diligence"
- "Data-room versioning" / "document-versioning discipline" / "single source of truth for [document]"
- "Access-control for [document type]" / "grant access to [investor group]" / "revoke access"
- "Material-info tagging in data room" / "Reg FD-safe data room" / "sensitive documents access"
- "Shadow versions" / "duplicate documents" / "which is the authoritative version"
- "Clean up stale documents" / "prune data room"

Do NOT use for:

- **Data-room platform selection / tooling procurement** → operator + counsel
  (tooling scope; this skill is discipline-agnostic across platforms).
- **Investor-cadence artifacts themselves** (quarterly letter drafts, monthly
  notes, quarterly call prep) → `investor-cadence` (sibling).
- **Pitch decks + fundraising materials + board decks** → echo (Executive Office).
- **Crisis-adjacent DD-timing** (crisis-response with DD dimension) →
  `crisis-comms` (sibling — but coordinates with this skill for material-info
  fence).
- **Legal formalization of DD contract obligations, NDA scope, disclosure
  schedules** → operator + securities/M&A counsel FIRST; this skill coordinates
  data-room discipline only AFTER counsel scopes the legal obligations.
- **Financial audit workpaper preservation** (AICPA-mandated audit workpapers) →
  external auditor + CFO scope; this skill coordinates data-room integration but
  does NOT own audit-workpaper retention.
- **Employee / customer PII handling** → operator + counsel + Cybersecurity
  (warden's data-protection scope); PII in the data room requires specific
  redaction + access-control discipline coordinated cross-department.
- **Individual mental-health crisis signals** → HARD BOUNDARY escalation to
  manager + HR Ops + EAP per Universal Principle 3.

## Structure / Protocol

The data-room-discipline workflow combines architecture + versioning + access-
control + tagging + backing-links + audit streams:

```
DATA-ROOM ARCHITECTURE (folder structure by DD-checklist)

  Standard top-level folders (NVCA-DD-checklist-aligned):

  01_Corporate/           Certificate of incorporation, bylaws, board minutes,
                          cap table, shareholder agreements
  02_Financial/           Historical financials, projections, budgets, tax returns,
                          audit reports
  03_Commercial/          Customer contracts, revenue-by-customer, pipeline,
                          material customer references
  04_Legal/               Litigation status, IP assignments, material contracts,
                          regulatory filings, compliance
  05_HR_People/           Org chart, key-employee contracts, equity plan,
                          benefits, employment-law compliance summary
  06_IP_Technology/       Patent + trademark filings, source-code escrow,
                          open-source compliance, security posture
  07_Regulatory/          Industry-specific regulatory (FDA / HIPAA / SOC / etc.)
  08_Insurance/           D&O, E&O, cyber, general liability policies
  09_Real_Estate/         Leases, property agreements (if applicable)
  10_Prior_Rounds/        Prior investment documents (SAFEs, notes, prior-round docs)


DOCUMENT-VERSIONING DISCIPLINE (single source of truth)

  Rule 1: One authoritative version per document. Superseded versions ARCHIVED
          not deleted, and clearly labeled as superseded with date.

  Rule 2: Naming convention — [DocumentType]_[Descriptor]_[YYYY-MM-DD].[ext]
          Example: MSA_AcmeCorp_2025-03-14.pdf (authoritative)
          Superseded: /_archive/MSA_AcmeCorp_2024-11-02.pdf (with SUPERSEDED tag)

  Rule 3: No "final" in filenames. Every document is potentially superseded;
          "final" is a lie that ages badly. Date + version discipline instead.

  Rule 4: Change-log per folder — /01_Corporate/_change_log.md tracks every
          add / supersede / archive with date + reason + operator name.


ACCESS-CONTROL TIERS

  Tier A: BOARD + OPERATOR ONLY
          Sensitive board materials, unfiled material info, unannounced
          strategic decisions

  Tier B: BOARD + STRATEGIC-INVESTOR SUBSET (post-NDA, active DD)
          Financial projections, customer names, pipeline detail, cap table

  Tier C: ALL CURRENT INVESTORS (post-NDA)
          Quarterly financials, org chart, product roadmap summary, historical
          board minutes with sensitive items redacted

  Tier D: PUBLIC OR NEAR-PUBLIC
          Public filings, marketing materials, public product info

  Access-control drift (granting Tier A to a Tier C recipient without operator +
  counsel sign-off) = LOAD-BEARING REFUSAL.


MATERIAL-INFO TAGGING (Reg FD fence)

  Every document tagged at ingest with material-info flag:

  [MATERIAL-NPI]     Contains material non-public information; Tier A/B access
                     only; Reg FD-simultaneous-disclosure required BEFORE
                     broader access
  [MATERIAL-PUBLIC]  Contains material info but already publicly disclosed
                     (e.g., 8-K attachment, press release supporting doc)
  [NON-MATERIAL]     No material-info content

  Access-control tier + material-info flag together determine who can see what.
  Reg FD fence: broadening Tier A/B [MATERIAL-NPI] to Tier C requires simultaneous
  public disclosure per investor-cadence sibling Phase 4.


EVIDENCE-BACKING LINKS

  Every quantitative claim in investor-cadence outputs (quarterly letter,
  monthly note, material-info alert) links to backing document in data room:

  Claim: "Q3 revenue grew 34% YoY to $12.4M"
  Backing: /02_Financial/Q3_2026_Financials_2026-10-15.xlsx (authoritative)

  Broken evidence-backing link = DD contradiction risk. Audit continuously.


DATA-ROOM OPERATIONAL SEQUENCE (this skill's phase-by-phase):

  Phase 1: ARCHITECTURE SETUP (initial or major-restructure)
  Phase 2: DOCUMENT-VERSIONING DISCIPLINE (continuous)
  Phase 3: ACCESS-CONTROL TIER MANAGEMENT (continuous + on grant/revoke request)
  Phase 4: MATERIAL-INFO TAGGING + REG FD FENCE (continuous)
  Phase 5: EVIDENCE-BACKING LINK MAINTENANCE (continuous + on every cadence output)
  Phase 6: PERIODIC DATA-ROOM AUDIT (quarterly + pre-DD-event + annual)
```

## Instructions

### Phase 1 — Architecture setup (initial or major-restructure)

- **Confirm scope.** VC round / M&A DD / IPO prep / recurring investor data room —
  scope determines depth. NVCA DD checklist is starting point; customize based on
  industry (regulated industries add regulatory folders; SaaS adds specific
  commercial subfolders; hardware adds IP + supply-chain).
- **Instantiate 10-folder architecture** (Structure/Protocol above). Empty folders
  with README explaining what belongs.
- **Instantiate change-log** — `/[folder]/_change_log.md` in each top-level folder.
- **Instantiate access-control matrix** — spreadsheet or purpose-built VDR
  feature: rows = investors/parties; columns = folders; cells = tier grant.
  Operator + counsel-approved baseline.
- **Instantiate material-info register** — `_material_info_register.md` at data-
  room root. Every [MATERIAL-NPI] document listed with tag date + expected
  public-disclosure date.

### Phase 2 — Document-versioning discipline (continuous)

**Every document at ingest goes through the versioning gate:**

- **Name per convention** (Structure/Protocol Rule 2). Reject uploads not matching.
- **Verify authoritative-vs-superseded status.** If replacing prior version, move
  prior to `/[folder]/_archive/` with SUPERSEDED tag; do NOT delete.
- **Update change-log** — entry with date + reason + operator name + link to
  superseded version if applicable.
- **Verify no "final" in filename** — reject or rename per Rule 3.

**Continuous audit:** monthly scan for shadow-version drift. Investigate any
document appearing to have multiple candidates. Resolve to single source of
truth + archive the rest.

### Phase 3 — Access-control tier management (continuous + on request)

**On access-grant request:**

1. **Verify NDA in place** — Tier B/C access requires signed NDA per counsel
   template.
2. **Verify tier appropriateness** — is the requester's DD stage + relationship
   consistent with the tier requested? Broadening access without corresponding
   DD-stage advancement = LOAD-BEARING REFUSAL.
3. **Verify material-info content** — any Tier A/B document broadening to Tier C
   scope triggers Reg FD fence (Phase 4).
4. **Grant + log** — access-control matrix updated; grant logged with date +
   operator + reason.

**On access-revoke request** (DD terminated, party exited):

1. **Verify revoke authority** — operator + counsel sign-off.
2. **Revoke immediately** across all folders + tiers.
3. **Verify no residual access** — check platform confirms revocation propagated.
4. **Log revocation** — access-control matrix updated; revocation logged.

**Continuous audit:** monthly access-control matrix review. Any drift from
approved baseline = investigation + rectification.

### Phase 4 — Material-info tagging + Reg FD fence (continuous)

**Every document at ingest tagged:**

- `[MATERIAL-NPI]` — contains material non-public info; Tier A/B only until public
  disclosure
- `[MATERIAL-PUBLIC]` — contains material info already publicly disclosed
- `[NON-MATERIAL]` — no material-info content

**On material-info trigger event** (per `investor-cadence` sibling Phase 4):

1. Documents supporting the material-info alert reviewed for tagging status
2. Documents currently `[MATERIAL-NPI]` remain Tier A/B until simultaneous public
   disclosure per Reg FD
3. On simultaneous public disclosure: retagged `[MATERIAL-PUBLIC]`; access can
   broaden per operator + counsel approval

**Material-info register audit:** monthly review of `_material_info_register.md`
for stale tags (documents tagged [MATERIAL-NPI] whose underlying info is now
public should be retagged; documents tagged [NON-MATERIAL] whose status changed
should be retagged upward).

### Phase 5 — Evidence-backing link maintenance (continuous)

**Every quantitative claim in investor-cadence outputs links to backing document:**

- Quarterly letter draft — every number links to authoritative source doc (financials,
  operating data, customer references)
- Monthly investor note — every progress statement links to authoritative source
- Material-info alert — every fact links to authoritative source

**Backing-link audit** at cadence-output pre-release gate:

1. Every claim ↔ backing-link verified
2. Backing link resolves to authoritative-version document (not superseded)
3. Backing document access-tier compatible with claim's disclosure audience

**Broken evidence-backing link = pre-release hold.** Do NOT ship cadence output
with broken backing link — DD contradiction risk downstream.

### Phase 6 — Periodic data-room audit (quarterly + pre-DD-event + annual)

**Quarterly audit** (aligned with `investor-cadence` quarterly rhythm):

- Shadow-version scan (Phase 2)
- Access-control drift check (Phase 3)
- Material-info register stale-tag review (Phase 4)
- Broken backing-link scan (Phase 5)
- Stale-document identification (documents unchanged > 12 months in
  active-DD-relevant folders; investigate whether still current)

**Pre-DD-event audit** (before a new investor round / M&A DD / IPO):

- Full data-room walk-through with DD-checklist alignment
- Investor-perspective review — what would a due-diligence-team ask that isn't
  answered?
- Sensitivity-review — any content that should be redacted / access-tier-lowered
  before broader access?

**Annual audit:**

- Data-room architecture review — does current folder structure still match DD
  needs?
- Access-control baseline refresh — revoke stale grants; confirm current grants
  still appropriate
- Change-log completeness — sample review for change-log coverage
- Retention-policy compliance — any documents past retention obligation to be
  archived off-platform?

## Output Format

Each invocation produces one or more of:

- **Data-room architecture setup plan** — 10-folder structure + change-log
  templates + access-control matrix baseline + material-info register template
- **Versioning-audit report** — shadow-version findings + rename/archive
  recommendations + change-log updates
- **Access-control grant/revoke decision** — tier appropriateness verification +
  NDA status + material-info fence check + grant/revoke log entry
- **Material-info tagging decision** — [MATERIAL-NPI] / [MATERIAL-PUBLIC] /
  [NON-MATERIAL] + Reg FD fence status + coordination with `investor-cadence`
- **Evidence-backing link audit** — claim ↔ backing-link verification for a
  cadence-output pre-release gate
- **Data-room audit report** — quarterly / pre-DD-event / annual audit findings
  + remediation plan

## Principles

1. **Single source of truth per document.** Superseded versions ARCHIVED not
   deleted; authoritative version is always identifiable. Shadow-version drift =
   DD contradiction risk. No "final" in filenames.
2. **Reg FD legal fence via access-control tiers.** [MATERIAL-NPI] documents
   Tier A/B only until simultaneous public disclosure. Broadening without Reg FD
   compliance = LOAD-BEARING REFUSAL. Inherited from `investor-cadence` Principle 1.
3. **Access grows narrower → broader across DD stages.** Initial DD → active DD →
   closing. Broadening access without DD-stage advancement = LOAD-BEARING REFUSAL.
4. **Audit-trail preservation.** No silent deletion / edit of prior versions.
   Change-log per folder tracks every add / supersede / archive with date +
   reason + operator. Silent replacement = trust damage + potential fraud
   allegation.
5. **No fabricated / speculative content in DD-backing documents.** Buffett-
   discipline inherited from `investor-cadence` Principle 3. Aspirational
   projections without operating-plan backing = securities-fraud exposure;
   customer references / case studies / metrics must be actual not fabricated.
6. **NDA-first for Tier B/C access.** No data-room access without counsel-approved
   NDA in place.
7. **Evidence-backing link discipline.** Every quantitative claim in cadence
   outputs links to authoritative-version backing document. Broken backing link =
   pre-release hold.
8. **PII redaction discipline.** Employee / customer PII in data room requires
   redaction + access-control coordination cross-department (warden's
   data-protection scope + operator + counsel).
9. **Aggregate-only for HR/people data** — Universal Principle 2 inherited.
   Individual employee perf / demographic / comp data NEVER surfaced in data-room
   documents without operator + counsel + HR Lead (hire) sign-off.
10. **Individual crisis signals during DD-crunch work** — HARD BOUNDARY per
    Universal Principle 3 inherited. Escalate to manager + HR Ops + EAP without
    exception, regardless of DD-timing pressure.
11. **§0.6 flag.** Feld & Mendelson 2019 + Berkus + NVCA + AICPA + SEC EDGAR + Reg
    FD are Tier B (canonical sources cited but not book-page-cited from
    `Agents/_books/`). Downgrade to Tier A when Feld & Mendelson 2019 is placed
    and a `Shared OS/logical/data_room_discipline.md` Route-D asset is built per
    §8.9.

## Fallback

- **Shadow-version drift discovered mid-DD.** STOP. Identify authoritative version
  with operator + document-owner. Archive shadow versions per Rule 3. Notify
  active-DD investors of authoritative version via cadence coordination. Update
  change-log with root-cause + prevention.
- **Uncertainty about material-info classification.** Route to operator + CFO +
  securities counsel per Reg FD fence. Tag `[MATERIAL-NPI]` default until counsel
  clarifies — safer to over-restrict than under-restrict.
- **Access-broadening pressure without corresponding DD-stage advancement.**
  Decline per Principle 3. Escalate to operator + counsel for approval. Broaden
  only with explicit sign-off + log entry.
- **NDA-not-in-place + access-request pressure.** Decline per Principle 6. Route
  requester to counsel-approved NDA template. Tier D public materials OK to share
  without NDA if truly public.
- **Silent-deletion request from document owner.** Decline per Principle 4.
  Superseded versions archive not delete; change-log entry required. If owner
  claims regulatory requirement (retention-policy-driven purge), verify with
  counsel BEFORE any deletion.
- **Broken evidence-backing link discovered pre-release.** HOLD cadence output.
  Resolve backing to authoritative version OR restate claim with different backing.
  Do NOT ship cadence output with broken backing link.
- **Fabricated / speculative content detected in DD-backing document.** Reject.
  Route to document owner + operator for rework with actual data. Aspirational
  projections without operating-plan backing = securities-fraud exposure per
  Principle 5.
- **PII discovered in data-room document without redaction.** Suspend access to
  document. Route to warden (Cybersecurity data-protection) + operator + counsel
  for redaction + re-upload.
- **Individual perf / demographic / comp data request for DD backing.** Route
  through hire (P&C Lead) + operator + counsel per Principle 9. Aggregate-only at
  publication surface (Universal Principle 2) — individual-identifiable data
  requires specific sign-off chain.
- **Individual crisis signal during DD-prep conversation.** STOP. Route per
  Universal Principle 3 (inherited) to manager + HR Ops + EAP. HARD BOUNDARY
  overrides all DD-timing pressure.
- **Crisis-adjacent DD-timing** (crisis-response with DD dimension). Route to
  `crisis-comms` (sibling) for crisis-response content + Reg FD timing
  coordination via `investor-cadence` (sibling); this skill coordinates data-room
  discipline but does NOT own crisis-response content.
- **Audit-workpaper retention question (AICPA scope).** Route to CFO + external
  auditor + operator. This skill coordinates data-room integration for
  audit-workpapers but does NOT own AICPA retention obligation scoping.

## Boundaries with Other Skills

| Hands off to / from | For | Direction |
|---|---|---|
| `investor-cadence` (custom, beacon — sibling) | Evidence-backing links from every cadence claim to authoritative backing document; Reg FD fence coordination | Bidirectional — cadence writes claims; data-room backs them |
| `crisis-comms` (custom, beacon — sibling) | Crisis-adjacent DD-timing; material-info fence during acute crisis | Coordination |
| `echo` (Executive Office) | Pitch materials + board prep coordination for evidence consistency; pitch-deck claims link to data-room backing | Cross-department |
| `press-kit` (custom, herald — Comms & PR sibling) | Publicly-releasable data-room documents feeding into press-kit canonical library; consistency check | Coordination |
| `hire` (P&C Lead) + `payroll-and-eor` | Key-employee contracts + equity plan + org chart in `/05_HR_People/`; individual data aggregate-only per Principle 9 | Cross-department coordination |
| `warden` + `veil` + `bastion` (Cybersecurity) | PII redaction + data-protection compliance for data-room documents; access-control platform-security coordination | Cross-department |
| `board` + `sentinel` (Governance) | Board-minute retention in `/01_Corporate/`; governance audit-trail coordination | Coordination |
| `precedent` (Governance) | Prior DD decisions + precedent-tracking for data-room architecture evolution | Coordination |
| CFO + external auditor | Audit-workpaper coordination in `/02_Financial/` (AICPA scope) | Cross-department |
| Operator + securities/M&A counsel | Reg FD compliance; NDA scope; disclosure schedules; material-info classification | Escalation — LOAD-BEARING legal fence Principle 2 + 5 |
| Manager + HR Ops + EAP | Individual mental-health signal during DD-prep conversation — HARD BOUNDARY | Escalation — Universal Principle 3 |
| `Shared OS: verification-before-completion` | Evidence gate on every data-room decision before shipping | Cross-cutting |

## References (public / verifiable)

- [Feld, Brad & Mendelson, Jason — Venture Deals (Wiley book page)](https://www.wiley.com/en-us/Venture+Deals%3A+Be+Smarter+Than+Your+Lawyer+and+Venture+Capitalist%2C+4th+Edition-p-9781119594826)
- [Berkus, Dave — Berkonomics (practitioner blog + Berkus Method)](https://berkonomics.com/)
- [NVCA — Model Legal Documents (FREE)](https://nvca.org/model-legal-documents/)
- [AICPA — AU-C Section 230, Audit Documentation](https://us.aicpa.org/research/standards/auditattest/downloadabledocuments/au-c-00230.pdf)
- [SEC EDGAR — Public Filing System](https://www.sec.gov/edgar)
- [SEC — Regulation FD Final Rule (17 CFR § 243)](https://www.sec.gov/rules/final/33-7881.htm)
