---
name: ssa-disability-ea
description: >
  Deep knowledge of the Social Security Administration's disability determination
  business process and enterprise architecture for architects designing solutions
  that must align with SSA's operational and policy framework. Use this skill
  whenever someone asks about: SSA disability determination workflow, sequential
  evaluation, Listings of Impairments, Residual Functional Capacity (RFC),
  DDS operations, medical evidence evaluation, consultative examinations, SSA
  adjudicative levels, disability claim processing, SSA POMS policy, DDS quality
  assurance, or how SSA makes disability decisions. Also use when an architect
  needs to understand the business process context before designing a solution —
  especially for AI/ML, clinical decision support, health IT, or case processing
  modernization targeting SSA. This skill pairs with ssa-hit-architect, which
  covers the technical HIT integration layer. Use this skill first to understand
  the business problem; use ssa-hit-architect for integration specifics.
---

# SSA Disability Determination — Enterprise Architecture Knowledge Base

## Purpose

This skill provides the business process and policy foundation that any architect
must understand before designing solutions for SSA's disability determination
program. It covers how SSA decides whether someone is disabled, what evidence
is required at each step, how that evidence is evaluated, and what systems and
people are involved.

**Companion skill:** `ssa-hit-architect` covers the Health IT technical integration
layer — record collection channels, MEGAHIT, EDCS, CEF, eHEX protocol.
Use this skill first. Use `ssa-hit-architect` when you reach integration specifics.

## How to use this skill

- For the five-step determination process → see **Sequential Evaluation**
- For what clinical evidence SSA requires → see **Medical Evidence Framework**
- For how records are evaluated → see **Medical and RFC Evaluation**
- For the Listings of Impairments structure → see **Listings of Impairments**
- For adjudicative levels and workflow → see **Adjudicative Levels**
- For quality assurance and accuracy → see **Quality Assurance**
- For architect implications and design principles → see **Architect Guidance**

For detailed policy on each topic, read the relevant reference file:
- `references/sequential-evaluation.md` — five steps, RFC, Grid Rules, onset, CDR
- `references/evidence-framework.md` — evidence categories, MER policy, CE, representation
- `references/listings-structure.md` — Listings body systems, meeting vs. equaling, AI opportunity
- `references/adjudicative-levels.md` — DDS/OHO/AC workflow, system touchpoints, MEGAHIT gaps by level

---

## Program Scale and Context

SSA administers two disability programs under the Social Security Act:

**Title II — Social Security Disability Insurance (SSDI)**
- Pays benefits based on work history and Social Security tax contributions
- Claimant must be "insured" — sufficient quarters of coverage
- Date Last Insured (DLI) is a critical deadline — disability must be established before DLI

**Title XVI — Supplemental Security Income (SSI)**
- Pays benefits based on financial need, not work history
- No insured status requirement — anyone meeting medical and financial criteria qualifies
- Protective filing date governs the 12-month evidence window

**Scale:**
- 2 million+ initial disability claims annually
- 54 state DDS agencies make initial and reconsideration determinations
- 1,500+ ALJs conduct hearings nationwide
- 885,000+ claims backlogged as of early 2026
- 219 day average initial determination time — up 81% since 2019

**Definition of disability (statutory):**
Unable to engage in any Substantial Gainful Activity (SGA) due to a medically
determinable physical or mental impairment expected to last at least 12 months
or result in death. SSA does not award temporary or partial disability.

---

## Sequential Evaluation

SSA uses a five-step sequential evaluation process for adult initial claims.
Each step is evaluated in order. If a determination can be made at any step,
evaluation stops — the subsequent steps are not considered.

**Citation:** 20 CFR 404.1520 and 416.920 | DI 22001.001 (June 2024)

### Step 1 — Substantial Gainful Activity (SGA)
**Question:** Is the claimant currently working at SGA level?
- If **yes** → Not disabled. Evaluation ends.
- If **no** → Continue to Step 2.

SGA thresholds are set annually. Work activity is evaluated by earnings
and nature of work. SGA does not apply to Age 18 redeterminations.

### Step 2 — Severity
**Question:** Does the claimant have a severe medically determinable impairment
(MDI) or combination of MDIs that meets the duration requirement?
- If **no** → Not disabled. Evaluation ends.
- If **yes** → Continue to Step 3.

An impairment is severe if it significantly limits basic work activities.
Must be established by objective medical evidence from an acceptable medical source.
Claimant's statements alone cannot establish an MDI — clinical signs, laboratory
findings, or diagnostic reports required.

### Step 3 — Listings of Impairments
**Question:** Does the impairment meet or medically equal a listing in Appendix 1
and meet the duration requirement?
- If **yes** → Disabled. Evaluation ends.
- If **no** → RFC is assessed, then continue to Step 4.

The Listings describe conditions severe enough to prevent any gainful activity.
Meeting a listing = automatic disability finding without vocational analysis.
RFC assessment occurs between Steps 3 and 4 regardless of Step 3 outcome.

### Step 4 — Past Relevant Work (PRW)
**Question:** Does the claimant's RFC allow them to perform any past relevant work
as actually performed, or as generally performed in the national economy?
- If **yes** (either question) → Not disabled. Evaluation ends.
- If **no** (both questions) → Continue to Step 5.

Past relevant work = substantial gainful activity within the past 15 years,
lasting long enough to learn the job.

### Step 5 — Other Work
**Question:** Can the claimant make a vocational adjustment to any other work
in the national economy, given RFC, age, education, and work experience?
- If **yes** → Not disabled.
- If **no** → Disabled.

Medical-Vocational Guidelines (Grid Rules) apply at Step 5.
Burden shifts to SSA at Step 5 — SSA must show other work exists.

### Why this matters for architects
Every AI/ML or decision support solution targeting SSA must map to this framework.
A solution that surfaces clinical evidence without connecting it to these five
questions provides limited examiner value. The highest-value intelligence layer
maps clinical findings to: (1) MDI establishment, (2) Listing criteria,
(3) RFC limitations. That is the business logic of disability determination.

---

## Medical Evidence Framework

### What SSA must develop (DI 22505.001, June 2025)

SSA must make "every reasonable effort" to obtain:
- Complete medical history covering at least 12 months prior to filing/DLI/PFD
- Evidence from all sources the claimant identifies or SSA discovers
- Records from all treating sources for alleged, documented, or discovered impairments

**12-month development period** is the baseline. Evidence outside this period
may be needed for: potential onset dating, severity/duration, longitudinal history.

### Categories of evidence (DI 24503.005, December 2024)

**1. Objective medical evidence**
Signs, laboratory findings from a medical source.
Does NOT include symptoms, diagnoses, or opinions.
Required to establish a Medically Determinable Impairment.

**2. Medical opinion**
Statement about what a claimant can still do despite impairments —
functional abilities and limitations. Under current rules (post-March 2017):
- Physical demands: sitting, standing, walking, lifting, carrying, pushing, pulling
- Mental demands: understanding, remembering, concentration, persistence, pace,
  carrying out instructions, responding to supervision/coworkers/pressure
- Other demands: seeing, hearing, handling workplace changes

**3. Prior administrative medical findings**
RFC assessments or findings from prior SSA adjudications.
Not binding on subsequent adjudicators but must be considered.

**4. Evidence from nonmedical sources**
Claimant, family, caregivers, employers, teachers. Cannot establish MDI alone
but relevant to symptom evaluation and functional limitations.

**5. Other evidence**
Statements about pain/symptoms, educational records, work history.

### What cannot establish disability
- Claimant's statements alone (symptoms require objective medical corroboration)
- Diagnosis label without clinical findings (e.g., alcoholism label alone)
- Medical opinion alone at Step 3 (medical equivalence requires MC/PC sign-off)

### Acceptable medical sources
Licensed healthcare workers practicing within scope of state/federal law.
Certified speech-language pathologists and school psychologists.
Note: Medical sources who are NOT acceptable medical sources can provide
evidence relevant to severity and functional limitations — but cannot
establish an MDI.

### Consultative Examinations (CE)
When existing evidence is insufficient, SSA purchases a CE from an
independent medical source. CE is SSA's tool of last resort for evidence gaps.
CEs are expensive (typically $200-500+) and add weeks to processing time.
Reducing CE rates is a documented SSA efficiency goal.
**Architect implication:** Solutions that improve completeness of treating source
records directly reduce CE costs and processing time.

---

## Medical and RFC Evaluation

### Medical Evaluation (DI 24501.002, January 2024)

Every disability determination must contain a medical evaluation unless
no medical evidence exists. Must address:
- All alleged and discovered impairments
- Full assessment period from POD through date of adjudication

Medical evaluation is documented on formal assessment forms in DCPS:
- **SSA-416** — Medical Evaluation
- **SSA-2506-BK** — Psychiatric Review Technique (PRT) — mental impairments
- **SSA-4734-F4** — Physical RFC Assessment
- **SSA-4734-F4-SUP** — Mental RFC Assessment (MRFC)
- **SSA-538** — Childhood Disability Evaluation Form

All signed electronically in DCPS. Paper versions require wet signature + scan to CEF.

### Residual Functional Capacity (RFC) (DI 24510.001, August 2017)

RFC = what a claimant can still do despite impairments.
Required at all levels when: severe impairment exists AND listing not met
AND SGA determination required.

RFC describes functional limitations in:
- **Exertional:** Sedentary / Light / Medium / Heavy / Very Heavy work levels
- **Nonexertional:** Postural, manipulative, visual, communicative, environmental
- **Mental:** Sustained concentration, social interaction, adaptation

RFC is an **administrative determination** — not a medical opinion.
MC/PC informs the RFC; examiner makes the final administrative finding.
New independent RFC required at each adjudicative level.

**Architect implication:** RFC is the output that drives Steps 4 and 5.
An AI system that extracts functional limitations from clinical records and
maps them to RFC work categories addresses the highest-value determina-
tion step — where most non-Listing cases are decided.

---

## Listings of Impairments

**Location:** POMS DI 34000 series | 20 CFR Part 404, Subpart P, Appendix 1
**Purpose:** Describe impairments severe enough to prevent any gainful activity.
Meeting a listing = automatic disability — no vocational analysis required.

### Structure

**Part A** — Adults (18+). Also applied to children when disease process similar.
**Part B** — Children under 18 only. Applied first; Part A used if Part B doesn't apply.

Each body system section contains:
1. Introductory text — definitions, key concepts, diagnostic requirements
2. Category of Impairments — required findings (symptoms, signs, lab findings)

SSA does not find a listing met solely because a diagnosis label matches.
Clinical findings must satisfy all specified criteria.

### Body Systems (Part A — Adults)

| Listing | Body System | Last Major Update |
|---------|-------------|-------------------|
| 1.00 | Musculoskeletal Disorders | February 2025 |
| 2.00 | Special Senses and Speech | — |
| 3.00 | Respiratory Disorders | — |
| 4.00 | Cardiovascular System | — |
| 5.00 | Digestive System | — |
| 6.00 | Genitourinary Disorders | — |
| 7.00 | Hematological Disorders | — |
| 8.00 | Skin Disorders | — |
| 9.00 | Endocrine Disorders | — |
| 10.00 | Congenital Disorders (children) | — |
| 11.00 | Neurological Disorders | — |
| 12.00 | Mental Disorders | — |
| 13.00 | Cancer (Malignant Neoplastic Diseases) | — |
| 14.00 | Immune System Disorders | — |

**Mental Disorders (12.00)** is particularly significant — largest single
category of disability claims. Includes: neurocognitive, schizophrenia,
depressive/bipolar, intellectual disorder, anxiety, somatic symptom,
personality/impulse control, autism, neurodevelopmental, eating disorders,
trauma/stressor-related.

### Meeting vs. Equaling a Listing

**Meets (DI 24508.005):** Impairment satisfies ALL criteria in the listing
including introductory text AND duration requirement.

**Medically equals (DI 24508.010):** Three pathways:
1. Described listing — has most but not all findings; other findings of equal significance
2. Unlisted impairment — analogous listing; findings of equal medical significance
3. Combination — no single listing met; combination equals a closely analogous listing

Medical equivalence requires sign-off from a Medical Consultant or Psychological
Consultant — examiner alone cannot find medical equivalence.

### Architect implication
The Listings are the clinical criteria backbone of SSA disability determination.
An AI intelligence layer that maps incoming clinical evidence to Listing criteria
by body system is the highest-value analytical capability SSA could deploy.
Currently this mapping is done entirely by human MCs and PCs reading images.

---

## Adjudicative Levels

SSA disability claims move through up to four administrative levels before
federal court. Each level is an independent determination — prior findings
are not binding but must be considered.

### Level 1 — Initial (DDS)
**Who:** Disability Examiner (DE) + Medical Consultant (MC) or
Psychological Consultant (PC)
**System:** DCPS (case management) + eView (evidence review) + CEF (record folder)
**Timeline:** ~219 days average (FY2023)
**Evidence:** MEGAHIT automated request fires at FO→DDS transfer

### Level 2 — Reconsideration (DDS)
**Who:** Different DE than initial — independent review
**System:** Same as initial — DCPS, eView, CEF
**Evidence:** MEGAHIT does NOT auto-fire at reconsideration if no initial HIT
request was made — DDS must create User Trigger manually
**Note:** Some states use a single decision-maker process — no reconsideration

### Level 3 — Hearing (OHO / ALJ)
**Who:** Administrative Law Judge (ALJ), independent of DDS
**System:** DCPS, separate OHO case management
**Evidence:** Claimant may submit new evidence; representatives can request
HIT via ERE through hearing office (cannot trigger directly)
**New 827 required:** Cannot reuse DDS-level authorization
**Timeline:** 12-24+ months backlog typical

### Level 4 — Appeals Council (AC)
**Who:** Appeals Council, Falls Church VA
**Evidence:** Existing record travels on CD/CEF — NO new HIT requests can be
triggered. Most complex cases have least ability to supplement record.
**Outcome:** AC can affirm, reverse, remand to ALJ, or dismiss

### Federal Court
Outside SSA administrative process. Record is fixed at AC level.

### Key workflow facts for architects

- Each level creates a **new independent RFC** assessment
- Evidence collected at prior levels travels forward in CEF
- Medical assessments (RFC, PRT) are created in DCPS at each level
- ALJ and AC must consider DDS-level MC/PC RFC assessments (not binding)
- Hearing representatives submit evidence via ERE — hearing office staff
  execute any HIT requests on their behalf

---

## Quality Assurance

### DDS QA Framework (DI 30001.010, 1993 / ongoing)

DDS Administrator designs QA function suited to agency needs.

**QA roles:**
- **DDS Administrator** — overall accountability; implements corrective actions
- **Supervisor** — in-line quality review; approves CEs; certifies determinations
- **QAU Staff** — random sample reviews; high-risk case reviews; special studies
- **MC/PC** — reviews QA cases with medical issues; peer reviews
- **Vocational Specialist** — ensures RFC + vocational factor integration

**QA reviews:**
- Random sample of cases
- High-risk cases (compassionate allowances, QDDs, military casualty, presumptive)
- Special workloads: CAL (Compassionate Allowance), QDD (Quick Disability Determination)

### Federal oversight
SSA conducts its own Quality Assurance reviews of DDS determinations.
Error rates are tracked and DDS agencies with high error rates receive
additional oversight and corrective action plans.

### Architect implication
Any AI decision support tool must be designed with QA accountability in mind.
Examiners remain legally responsible for determinations — AI assists, does not decide.
Output must be auditable, explainable, and traceable to source evidence.
"Black box" recommendations are incompatible with QA and legal defensibility requirements.

---

## What This Means for Solution Design

### The core insight
SSA built a sophisticated electronic collection pipeline and then immediately
destroys the value of what it collected — converting structured records to images,
presenting them to examiners with no analytical support, and requiring manual
mapping to a complex five-step legal framework with detailed clinical criteria.

The business process has not changed since the paper era.
Electronic records are bolted on top of a paper workflow.

### Where AI/ML creates genuine value — ranked by impact

**1. RFC functional limitation extraction (highest)**
Map clinical language → physical/mental RFC work categories.
This is what MCs and PCs spend most of their time doing.
Directly accelerates Steps 4 and 5 determinations for the majority of cases.

**2. Listings criteria mapping (very high)**
Map clinical findings → Listing body system criteria.
Step 3 determinations = automatic disability — no vocational analysis needed.
Currently 100% manual MC/PC review.

**3. MDI establishment support (high)**
Identify objective medical evidence (signs, labs) vs. symptoms vs. opinions.
Help examiners distinguish what can establish an MDI from what cannot.

**4. Longitudinal timeline construction (high)**
Assemble evidence across providers, time periods, and channels into
coherent chronological narrative aligned to POD through adjudication date.
Currently done manually — no system does this.

**5. CE reduction (significant)**
Better completeness from treating sources → fewer consultative exams.
Each CE avoided saves $200-500 and weeks of processing time.

**6. Identity resolution (significant)**
15% of HIT requests fail due to identity mismatch.
Probabilistic matching before MEGAHIT fires saves the entire downstream failure.

### Design principles for SSA solutions

1. **Examiners decide — AI assists.** The DE makes the determination.
   MC/PC signs medical assessments. AI must support, not replace, this accountability.

2. **Audit trail is non-negotiable.** Every AI output must be traceable to
   source evidence in CEF. Examiners annotate findings in DCPS case notes.

3. **Policy is the constraint.** POMS governs what examiners can consider and how.
   A technically correct AI output that contradicts POMS policy will be rejected.

4. **QA will review AI-assisted determinations.** Design for explainability —
   QA reviewers need to understand why a recommendation was made.

5. **Each level is independent.** Don't design for "the claim" — design for
   the determination at a specific adjudicative level with its specific
   evidence record and its specific examiner accountability.

6. **The policy constraints that technology cannot override:**
   - PDF/TIFF conversion of all incoming records (POMS DI 81020.060)
   - 100% completeness requirement before accepting digital records
   - SSA-827 expiration and cross-level reuse prohibition
   - Graphical evidence requires traditional request regardless of HIT connectivity
   - Appeals Council cannot initiate new HIT requests

---

## Sources

- DI 22001.001 Sequential Evaluation (June 2024): https://secure.ssa.gov/apps10/poms.nsf/lnx/0422001001
- DI 24501.002 Medical Evaluation (January 2024): https://secure.ssa.gov/apps10/poms.nsf/lnx/0424501002
- DI 24501.020 Establishing MDI (March 2017): https://secure.ssa.gov/apps10/poms.nsf/lnx/0424501020
- DI 24503.005 Categories of Evidence (December 2024): https://secure.ssa.gov/apps10/poms.nsf/lnx/0424503005
- DI 24508.005 Impairment Meets a Listing (April 2018): https://secure.ssa.gov/apps10/poms.nsf/lnx/0424508005
- DI 24508.010 Medical Equivalence (October 2023): https://secure.ssa.gov/apps10/poms.nsf/lnx/0424508010
- DI 24510.001 RFC Assessment (August 2017): https://secure.ssa.gov/apps10/poms.nsf/lnx/0424510001
- DI 22505.001 Medical and Nonmedical Evidence (June 2025): https://secure.ssa.gov/apps10/poms.nsf/lnx/0422505001
- DI 22505.008 Supplemental Development (March 2016): https://secure.ssa.gov/apps10/poms.nsf/lnx/0422505008
- DI 30001.010 QA Authority (November 1993): https://secure.ssa.gov/apps10/poms.nsf/lnx/0430001010
- DI 34001.001 Listings Purpose (September 2000): https://secure.ssa.gov/apps10/poms.nsf/lnx/0434001001
- DI 34001.010 Musculoskeletal Disorders 1.00 (February 2025): https://secure.ssa.gov/apps10/poms.nsf/lnx/0434001010

Knowledge current as of April 2026.
Companion skill: ssa-hit-architect
