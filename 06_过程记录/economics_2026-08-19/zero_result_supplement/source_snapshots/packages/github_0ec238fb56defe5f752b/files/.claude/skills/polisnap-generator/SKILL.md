---
name: polisnap-generator
description: "SKILL 3 of 4 — PoliSnap Generation Chain. Receives a PoliSnapNormalized document, creates any required new PoliElement .tsx files (Option A — NEW_ELEMENT_DEPENDENCY path), then constructs a complete PoliSnapConstructed JSON. Input is always PoliSnapNormalized — no freeform mode."
metadata:
    version: "1.0.0"
    owner: "vanguard-os"
    tags:
        - polisnap
        - polielement
        - react-native
        - code-generation
---

# Skill: polisnap-generator

**Chain Position:** Step 3 of 4 — PoliSnap Construction
**Input:** `NORM-{id}.json` from `apps/skill-execution/PoliSnaps/normalized/`
**Output:** `SNAP-{id}.json` → `apps/skill-execution/PoliSnaps/constructed/`
**Feeds into:** `polisnap-distributor`

---

## Scope Boundary

| OWNED by this skill | NOT owned — do not perform |
|---|---|
| New PoliElement `.tsx` file creation (Option A) | Content discovery |
| PoliSnap JSON construction (all SR rules) | Rep ID / policy area validation |
| Element reuse analysis (SR-10, using catalog) | `snapLibrary.ts` writing |
| Sentiment element composition (SR-13/14) | Congress.gov API calls |

---

## Authority

- **Component Naming Conventions:** `genotype/operations/SOP_COMPONENT_ARCHITECTURE_MASTER.md`
- **Theming and Styling:** `apps/mobile/constants/theme.ts`
- **Component Factory:** `apps/mobile/components/factories/component-factory.tsx`
- **Element Catalog:** `.github/skills/_polisnap-data/element-catalog.md`

---

## Input Contract

This skill accepts **only** a `PoliSnapNormalized` document. No freeform business intent. No dual-mode.

**Read from:** `apps/skill-execution/PoliSnaps/normalized/NORM-{id}.json`

**Fields consumed:**

| Field | Used for |
|---|---|
| `normId` | Reference back-link in output |
| `validatedRepresentativeId` | `metadata.representativeId` + `Header.Representative` data |
| `validatedPolicyArea` | `metadata.policyArea` |
| `snapCategory` | Snap `type` field |
| `canonicalBillId` / `billTitle` / `billStatus` | Element data population |
| `suggestedElements[]` | Element construction order and type selection |
| `sentimentEligible` | Whether to include `Interaction.Sentiment.Pulse` |
| `normalizedTitle` / `normalizedSubtitle` | Snap root `title` / `subtitle` |
| `trustVerificationLevel` | `Trust.Thread.data.verificationLevel` |
| `sourceUrl` / `sourceName` / `accessDate` | `Trust.Thread.data.sources[]` + snap root `sources[]` **only** — do NOT propagate to any other element |
| `rawSummary` | Body text for `Narrative.Insight.Summary` |
| `warnings[]` | Pre-flight check — see Element Creation Protocol |

---

## Element Creation Protocol (Option A — NEW_ELEMENT_DEPENDENCY)

When `warnings[]` contains one or more `NEW_ELEMENT_DEPENDENCY` entries, this skill creates the required `.tsx` files **before** constructing the snap JSON.

**Protocol:**

1. **Read each `NEW_ELEMENT_DEPENDENCY` warning.** Extract the `elementType` (e.g., `Interaction.NewThing`).
2. **Run SR-10 Extend vs New Analysis** against `.github/skills/_polisnap-data/element-catalog.md`. If score ≤ 7, extend an existing element instead of creating a new file.
3. **If NEW is confirmed (score ≥ 8):**
   - Run the **PoliElement Naming Convention Gate** (see below) to determine category and file name.
   - Create the `.tsx` file following SR-1, SR-2, SR-3.
   - Register in `apps/mobile/components/polisnap-elements/index.ts` (SR-3).
   - **Add the new type to `_polisnap-data/element-catalog.md`** so future normalizer runs detect it. Use the Catalog Curation Template below.
4. **Continue to snap construction.** The new element is now available. Note in the snap output that a mobile app release is required before the element renders fully.

> The app renders `ShadowFallbackMolecule` for unregistered types — **it does not crash**. Distributing a snap with a new element before the app release is valid and expected during development.
- **Component Factory:** `apps/mobile/components/factories/component-factory.tsx`
- **Element Catalog:** `.github/skills/_polisnap-data/element-catalog.md`

#### Catalog Curation Template

When creating a new element, append a row to the appropriate section of `_polisnap-data/element-catalog.md`:

```
| `{Category.ElementName}` | {one-line structural purpose} | {key data fields} | {content signals — use `active` / `historical` / `biographical` / `any`} | {jurisdictionScope} |
```

**`jurisdictionScope` values:**
- `federal` — specific to federal legislative / executive / judicial activity
- `state` — specific to state-legislature or state-executive activity
- `local` — county / city / school-district specific
- `federal+state` — applies to both federal and state levels
- `any` — applies across all civic jurisdiction levels

**Steps:**
1. Identify the correct section in `element-catalog.md` (Sentiment, Text Blocks, Voting, Numbers, Scoring, Finance, Identity, Actions, Visual).
2. If no section fits, add a new `### Section Name` heading.
3. Append the row using the template above.
4. Re-read the Reusability Decision Tree in `element-catalog.md` to confirm NEW was the right call.

---

## Input Contract

This skill accepts **only** a `PoliSnapNormalized` document. No freeform business intent. No dual-mode.

**Read from:** `apps/skill-execution/PoliSnaps/normalized/NORM-{id}.json`

**Fields consumed:**

| Field | Used for |
|---|---|
| `normId` | Reference back-link in output |
| `validatedRepresentativeId` | `metadata.representativeId` + `Header.Representative` data |
| `validatedPolicyArea` | `metadata.policyArea` |
| `snapCategory` | Snap `type` field |
| `canonicalBillId` / `billTitle` / `billStatus` | Element data population |
| `suggestedElements[]` | Element construction order and type selection |
| `sentimentEligible` | Whether to include `Interaction.Sentiment.Pulse` |
| `normalizedTitle` / `normalizedSubtitle` | Snap root `title` / `subtitle` |
| `trustVerificationLevel` | `Trust.Thread.data.verificationLevel` |
| `sourceUrl` / `sourceName` / `accessDate` | `Trust.Thread.data.sources[]` + snap root `sources[]` **only** — do NOT propagate to any other element |
| `rawSummary` | Body text for `Narrative.Insight.Summary` |
| `warnings[]` | Pre-flight check — see Element Creation Protocol |
| `snapRelationshipRole` | `"parent"` / `"child"` / `null` — determines whether `relationships[]` and `Navigation.SnapLinks` should be added to the snap |
| `suggestedChildSnaps[]` | (Parent snaps only) List of child snaps to reference. Used to populate `Navigation.SnapLinks` and `relationships[]`. Child `snapId` values will be backfilled after child snaps are distributed — see SR-15. |
| `parentSnapRef` / `drillDownRole` | (Child snaps only) The parent spawn reference and role key. Written to `relationships[]` on the child snap. |

---

## Element Creation Protocol (Option A — NEW_ELEMENT_DEPENDENCY)

When `warnings[]` contains one or more `NEW_ELEMENT_DEPENDENCY` entries, this skill creates the required `.tsx` files **before** constructing the snap JSON.
**Read Normalized File:** Load `NORM-{id}.json` from `apps/skill-execution/PoliSnaps/normalized/`. Confirm `suggestedElements[]` is populated.
2. **Check for NEW_ELEMENT_DEPENDENCY:** Scan `warnings[]`. If any `NEW_ELEMENT_DEPENDENCY` entries exist, execute the **Element Creation Protocol** above before continuing.
3. **Run Naming Convention Gate:** For any new element being created, validate the `componentType` per the gate below.
4. **Present Execution Summary & Await Approval:**
   - New `PoliElement` files to be created (if any).
   - Files to be modified (`index.ts` if new elements, `_polisnap-data/element-catalog.md` if new elements).
   - Full preview of the `PoliSnap` JSON to be constructed (elements in order, including sentiment and Trust Thread).
   - **The skill MUST wait for user approval before writing any files.**
5. **Create New Elements (if approved):** Execute Element Creation Protocol steps — `.tsx` files, `index.ts` registration, catalog update.
6. **Construct Snap JSON:** Build the complete `PoliSnap` JSON from the normalized data:
   - Use `suggestedElements[]` as the construction guide. Populate each element's `data` from normalized fields.
   - Apply SR-6 (Trust Thread), SR-8 (Vertical Rhythm), SR-9 (Rep Header), SR-11 (Title), SR-12 (No rep name repetition), SR-13/14 (Sentiment).
   - Set `createdAt` to `new Date().toISOString()`.
7. **Write Constructed Snap:** Save as `SNAP-{id}.json` to `apps/skill-execution/PoliSnaps/constructed/`. The `id` should be a descriptive kebab-case slug (e.g., `snap-sres45-thune-bill-position`).
8. **Handoff:** Present the snap file path and next step: `Distribute [snapId]`
**Validation:**
- The skill will prompt for a `componentType` string (`Category.ElementName`).
- It will verify the category exists.
- It will check if a file with the corresponding kebab-case name already exists in that category's directory. If it does, generation is blocked to prevent duplicates.

---

## File Output Contract

**For each new PoliElement:**

| File | Naming | Location |
|---|---|---|
| Component | `{element-name-kebab-case}.tsx` | `apps/mobile/components/polisnap-elements/{category}/` |
| Registration | `index.ts` (updated) | `apps/mobile/components/polisnap-elements/` |

---

## Template Resolution Protocol

**This pre-step executes BEFORE the Generation Procedure.** Its purpose is to check for an existing structural template that matches this snap type, and load it as the construction scaffold. If no match exists, a new template is auto-generated from the snap being constructed.

**Template Catalog Location:** `apps/skill-execution/PoliSnaps/templates/snap-template-catalog.json`
**Template Files Location:** `apps/skill-execution/PoliSnaps/templates/{templateId}.template.json`

### Resolution Steps

**TRP-1. Check for explicit `templateId` in NORM file.**
- If `NORM.templateId` is present, load `snap-template-catalog.json` and find the matching entry.
- If found → go to **TRP-4 (TEMPLATE MATCH)**.
- If not found → log warning: `TEMPLATE_NOT_FOUND: templateId '{{normTemplateId}}' not in catalog. Falling back to signature hash.` Continue to TRP-2.

**TRP-2. Compute signature hash from `suggestedElements[]`.**
- Join the elements array with `|` separator in declared order: `"Header.Bill|Data.FloorDebate|Narrative.Insight.Summary|Interaction.Sentiment.Pulse|Trust.Thread"`
- Search all catalog entries for a matching `signatureHash`.
- If found → go to **TRP-4 (TEMPLATE MATCH)**.
- If not found → continue to TRP-3.

**TRP-3. AUTO-GENERATE new template.**
When no catalog match exists, derive a new template from the snap being built:

1. **Infer `templateId`** from the leading element type + content type:
   - Leading element `Header.Bill` → prefix `bill-`
   - Leading element `Header.Representative` → prefix `rep-`
   - Append content slug from NORM `snapCategory` or `metadata.insightType`
   - Example: `Header.Bill` + `FloorVote` → `bill-floor-vote`
2. **Build template JSON** using `{{VAR}}` placeholder slots for every concrete data value in the snap.
3. **Build `productionSpec`** mapping each `{{VAR}}` to its source, type, and any validation rules.
4. **Add to catalog** — append a new entry to `snap-template-catalog.json` with:
   - `templateId`, `version: "1.0"`, `description`, `snapCategory`, `requiredElements[]`
   - `signatureHash` (computed hash from this snap)
   - `snapIdPattern`, `templateFile`, `addedDate`
5. **Include in Step 4 approval summary** (see Generation Procedure). The new template file and catalog update MUST be listed as files requiring approval before writing.

**TRP-4. TEMPLATE MATCH — load and use scaffold.**
1. Read `{templateId}.template.json`.
2. Use the `schema` block as the structural scaffold for the snap.
3. Fill all `{{VAR}}` slots from corresponding NORM file fields.
4. Apply all `productionSpec` rules (speaker selection, quote max chars, sentiment question rules, etc.).
5. Validate that all `required: true` vars are populated. If any are missing, add a `TEMPLATE_VAR_MISSING` warning and apply the template's `fallbackRules` where defined.
6. Continue to **Generation Procedure Step 1** — the template provides structure; the generation procedure still executes for element creation checks and approval.

### Template Resolution Summary (for Step 4 approval)

When presenting the Step 4 approval summary, include a **Template Resolution** section:

```
TEMPLATE RESOLUTION
  Status: [MATCH_FOUND | AUTO_GENERATED | NO_TEMPLATE]
  Template: {templateId} ({templateFile})
  Method: [explicit templateId | signatureHash match | auto-generated]
  (If AUTO_GENERATED) New files to write:
    - apps/skill-execution/PoliSnaps/templates/{templateId}.template.json  [NEW]
    - apps/skill-execution/PoliSnaps/templates/snap-template-catalog.json  [UPDATED]
```

---

## Generation Procedure

1. **Read Normalized File:** Load `NORM-{id}.json` from `apps/skill-execution/PoliSnaps/normalized/`. Confirm `suggestedElements[]` is populated. **Then execute the Template Resolution Protocol above before proceeding.**
2. **Check for NEW_ELEMENT_DEPENDENCY:** Scan `warnings[]`. If any `NEW_ELEMENT_DEPENDENCY` entries exist, execute the **Element Creation Protocol** above before continuing.
3. **Run Naming Convention Gate:** For any new element being created, validate the `componentType` per the gate below.
4. **Present Execution Summary & Await Approval:**
   - **Template Resolution** block (see Template Resolution Protocol above).
   - New `PoliElement` files to be created (if any).
   - Files to be modified (`index.ts` if new elements, `_polisnap-data/element-catalog.md` if new elements).
   - New template files to be created (if auto-generated).
   - Full preview of the `PoliSnap` JSON to be constructed (elements in order, including sentiment and Trust Thread).
   - **The skill MUST wait for user approval before writing any files.**
5. **Create New Elements (if approved):** Execute Element Creation Protocol steps — `.tsx` files, `index.ts` registration, catalog update.
6. **Construct Snap JSON:** Build the complete `PoliSnap` JSON from the normalized data:
   - If a template was matched or auto-generated, use its `schema` block as the structural scaffold, filling `{{VAR}}` slots.
   - If no template applies, construct from `suggestedElements[]` directly.
   - Apply SR-6 (Trust Thread), SR-8 (Vertical Rhythm), SR-9 (Rep Header), SR-11 (Title), SR-12 (No rep name repetition), SR-13/14 (Sentiment), **SR-15 (Drill-Down Navigation)**.
   - Set `createdAt` to `new Date().toISOString()`.
7. **Write Constructed Snap (and template files if auto-generated):** Save `SNAP-{id}.json` to `apps/skill-execution/PoliSnaps/constructed/`. If TRP-3 ran, also write the new `.template.json` and update `snap-template-catalog.json`.
8. **Handoff:** Present the snap file path and next step: `Distribute [snapId]`.

---

## Element Reuse Catalog

> **See `.github/skills/_polisnap-data/element-catalog.md`** for the full catalog.
>
> The generator uses the catalog when executing SR-10 (Extend vs New Analysis) and when adding new element types after creation. The normalizer owns reuse analysis before the snap reaches this skill — `suggestedElements[]` in the NORM file already reflects the reuse decision. The generator defers to that suggestion unless SR-10 analysis reveals an extend opportunity that was missed.

---

## Structural Rules

### Sentiment & Public Opinion

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Color-coded opinion badge + summary text ("POSITIVE / MIXED / NEGATIVE") | `Narrative.SentimentSummary` | `sentiment` ("Positive"/"Negative"/"Mixed"), `summary` | "Public Sentiment", "Constituent Reaction" |
| Interactive agree/disagree poll with live stats **(2–4 options)** | `Interaction.Sentiment.Pulse` | `title`, `agreeLabel`, `disagreeLabel`, `options[]` (min 2, max 4), `stats.agree`, `stats.disagree` | "Do you support this bill?", "Public Support for S. Res 45" |
| Slider-based opinion capture (left–right spectrum) | `Interaction.Sentiment.Slider` | (slider-specific config) | "Rate your support" |
| Left–right political alignment gauge | `Universal.Gauge` (mode: `Spectrum`) | `title`, `value` (0–100), `leftLabel`, `rightLabel`, `insight` | "Policy Alignment", "Party Spectrum" |
| Rep vote vs constituent opinion gap indicator | `Metric.Scorecard.SentimentGap` | (embed inside `Metric.Accountability.Scorecard`) | — |
| District consensus score with ripple trend | `Data.Consensus.Ripple` | `district`, `consensusScore`, `respondents`, `capitalVolume`, `trend`, `clusters[]` | — |
| Sentiment over time line chart | `Visual.Chart.SentimentTrend` | `value` (chart data) | — |

### Text Blocks & Narrative

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| **Titled text block with left border, subtle bg, italic body + optional expand** | `Narrative.Insight.Summary` | `title` (**snap-specific**), `text`/`content`/`summary`, `isExpandable` | "About This Bill", "Key Background", "Analyst Note", "Policy Context", "What This Means", "Why It Matters" |
| Official congressional quote / floor statement | `Narrative.Congressional.Statement` | `quote`/`text`, `speaker`, `date`, `context`, `fullTranscriptId` | — |
| Congressional floor proceeding | `Narrative.Congressional.FloorStatement` | same as `Statement` | — |
| Debate exchange between two named speakers | `Narrative.Congressional.Debate` | (debate-specific structure) | — |
| Full hearing or session transcript | `Narrative.Congressional.Transcript` | (transcript-specific structure) | — |
| Scheduled event with date / location | `Narrative.Event.Details` | (event-specific structure) | — |

### Voting & Legislative

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Rep vote badge (Yea/Nay/Abstained) + bill name | `Data.BillVote` | `billName`, `vote`, `representativeName` *(omit when `Header.Representative` is present — see SR-12)* | — |
| Rep voting history / record table | `data.legislative.votingrecord` | (record-specific structure) | — |
| Bill progress through legislative stages | `Metric.Progress.Stepper` | (stepper-specific structure) | — |

### Numbers, Stats & Comparisons

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Two or more labelled metric tiles in a row | `Metric.Group` | `title`, `items[]` (each: `label`, `value`, `subtext`, `unit`, `color`) | "Key Figures", "Economic Impact" |
| Exactly two items side-by-side | `Metric.Dual.Comparison` | same as `Metric.Group` with two `items` | — |
| District spending / funding breakdown | `Metric.DistrictFunding` | (funding-specific structure) | — |
| Expandable tabular data set | `Data.Table.Expandable` | (table-specific structure) | — |
| Bullet or columnar list | `Data.List.Columnar` / `Data.List.Bullet` | `items[]` | — |

### Scoring, Grades & Accountability

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Single letter grade with label + description | `Metric.Grade` | `label`, `grade`, `color`, `description` | "Accountability Grade" |
| Full rep report card (composite scorecard) | `Metric.Accountability.Scorecard` | (scorecard composite structure) | — |
| Intensity / support-level arc or radial gauge | `Universal.Gauge` (mode: `Friction`/`Radial`/`Linear`) | `title`, `value`, `intensity`, `insight` | "Support Level", "Friction Index" |
| Predictive scoring or outcome forecasting | `Metric.PredictiveScoring` / `Metric.PredictiveForecasting` | (predictive structure) | — |

### Finance & FEC

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Campaign finance summary tiles | `Metric.FEC.Details` | (FEC-specific structure) | — |
| Donor / contribution breakdown | `Metric.FEC.ContributionAnalysis` | (contribution-specific structure) | — |
| Influence correlation heatmap | `Data.Correlation.Heatmap` | (heatmap-specific structure) | — |
| Corruption risk index score (score badge + donor meta + embedded insight sub-section) | `Metric.CorruptionIndex` | (index-specific structure) | — Note: renders its own internal "ANALYST INSIGHT" box — this is NOT a `Narrative.Insight.Summary` element; do not add a separate one |
| Financial audit result | `Audit.Financial` | (audit-specific structure) | — |

### Identity & Context

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Representative profile card (photo, name, party, district) | `Identity.Rep.Brief` | (rep brief structure) | — |
| Snap header anchored to a single representative | `Header.Representative` | see SR-9 | — |
| Organization / committee header | `Identity.Organization.Header` | (org header structure) | — |
| Geographic / district context drill-down | `Context.Thread` | `refinementScore`, `activeTier`, `derivationSummary`, `lineage`, `oracleSource` | — |
| Provenance / source verification footer | `Trust.Thread` | see SR-6 | — |

### Actions & CTAs

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Single action button / watchlist / contact CTA | `Interaction.Action.Card` | `title`, `label`, `actionType`, `actionPayload` | "Contact Rep", "Add to Watchlist" |
| Community participation prompt | `Interaction.Participation.CTA` | (CTA-specific structure) | — |
| Voter audit / identity verification | `Interaction.VoterAudit` | (audit-specific structure) | — |

### Navigation

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Tappable list of linked child snaps | `Navigation.SnapLinks` | `title`, `links[]` (each: `snapId`, `label`, `thumbnailRepId`) | "Full Floor Speeches", "Individual Testimonies", "Related Bills" |

### Visual & Charts

| Structural purpose | Type | Key `data` fields | Example titles / context |
|---|---|---|---|
| Vertical or horizontal bar chart | `Visual.Chart.Bar` | `value` (chart data) | — |
| Line chart / trend over time | `Visual.Chart.Line` | `value` (chart data) | — |
| Animated ripple / live signal | `Visual.RipplePulse` | (ripple-specific structure) | — |
| Aggregate community pulse animation | `Visual.Aggregate.Pulse` | (aggregate-specific structure) | — |
| Multi-item status grid | `Metric.Status.Grid` | (grid-specific structure) | — |

> **Reuse example:** Both an "Analyst Note" in an Influence Correlation snap and "About This Bill" in a Vote snap use `Narrative.Insight.Summary` — same element, different `data.title`. The element is structurally a titled text block with accent bar. The title is never a reason to create a new element.

---

## Structural Rules

### SR-1 — Component File Structure

Every generated `PoliElement` `.tsx` file must contain:
1.  Imports from React, React Native, and PoliTickIt's theme constants.
2.  The component functional component definition.
3.  A `StyleSheet.create` call for the component's styles.
4.  A `ComponentFactory.register()` call to make the component available to the rendering engine.

### SR-2 — Component Registration

The `ComponentFactory.register` call is mandatory and must use the full `Category.ElementName` as the type string.

```typescript
// Example from rep-brief.tsx
ComponentFactory.register(
  "Identity.Rep.Brief",
  ({ value, presentation, extraProps }) => (
    <IdentityRepBrief
      data={value}
      presentation={presentation}
      navigationService={extraProps?.navigationService}
      extraProps={extraProps}
    />
  ),
);
```

### SR-3 — Central Index Update

The `apps/mobile/components/polisnap-elements/index.ts` file must be updated to import the new component file for its side effects (i.e., to trigger registration).

```typescript
// Add this line to index.ts
import "./{category}/{element-name-kebab-case}";
```

### SR-4 — Snap Distribution

> **Owned by `polisnap-distributor`.** This skill does not write to `snapLibrary.ts`. The generator outputs a `SNAP-{id}.json` file to `apps/skill-execution/PoliSnaps/constructed/` — the distributor handles all `snapLibrary.ts` writes, category routing, and prepend logic.

### SR-5 — Rep & Policy Area Validation

> **Owned by `polisnap-normalizer`.** By the time a NORM file reaches this skill, `validatedRepresentativeId` and `validatedPolicyArea` have already been validated. Trust them. Do not re-validate. If either field is `null`, check the NORM file's `warnings[]` for the relevant warning code.

### SR-7 — Element Reuse Gate

> **Owned by `polisnap-normalizer`.** The normalizer performs element reuse analysis against `_polisnap-data/element-catalog.md` and populates `suggestedElements[]` in the NORM file. The generator trusts this suggestion. The generator applies **SR-10 (Extend vs New)** only when creating a new element (i.e., when handling a `NEW_ELEMENT_DEPENDENCY` warning) to determine whether to extend an existing element or create a new file.

### SR-6 — Trust Thread Integration

The `Trust.Thread` element is the **sole provenance and source-reference anchor** for a PoliSnap. It displays a collapsible "SECURE TRUST THREAD™" footer. When present it is the **only** element in the snap that may carry any source reference — no other element (`Narrative.Insight.Summary`, `Data.BillVote`, etc.) may include a `sourceLink` or any equivalent source-reference field.

**Source Consolidation Rule (SCR):** If a `Trust.Thread` is included in a snap, consolidate ALL source references inside it. Remove `sourceLink` from every other element before writing the snap.

**When to include it:** Any snap whose data comes from a real-world source (a bill, a government document, a news article, a dataset URL). If the intent contains a URL or a named authoritative source, a `Trust.Thread` element is **required**.

**When to omit it:** Pure editorial/narrative snaps with no external source. Never fabricate a URL — if no source is provided in the intent, omit the element entirely.

**Element structure — single source (simple case):**

```json
{
  "id": "trust-thread",
  "type": "Trust.Thread",
  "data": {
    "referenceId": "<short unique ref e.g. 'HR-1234' or domain slug>",
    "serialNumber": "<same as referenceId or a formatted PS-XXXX code>",
    "verificationLevel": "<one of: 'Tier 1' | 'Tier 2' | 'Tier 3' | 'VERIFIED'>",
    "sources": [
      {
        "name": "<human-readable source name e.g. 'Congress.gov'>",
        "url": "<canonical URL for the source>",
        "auditDate": "<ISO date string or human-readable date>"
      }
    ]
  }
}
```

**Element structure — multiple sources:**

```json
{
  "id": "trust-thread",
  "type": "Trust.Thread",
  "data": {
    "referenceId": "<short unique ref>",
    "serialNumber": "<PS-XXXX code>",
    "verificationLevel": "VERIFIED",
    "sources": [
      {
        "name": "Congress.gov",
        "url": "https://congress.gov/...",
        "auditDate": "2026-05-21"
      },
      {
        "name": "Clerk.House.gov — Roll Call Vote #185",
        "url": "https://clerk.house.gov/evs/2026/roll185.xml",
        "auditDate": "2026-05-21"
      }
    ]
  }
}
```

> **Backward compatibility:** The renderer also accepts the legacy flat-field format (`oracleSource` + `auditDate` at the top level) for existing snaps. New snaps MUST use `sources[]`.

**Multiple sources guidance:**
- Use multiple `sources` entries when the snap draws from 2+ distinct authoritative origins (e.g., a Congress.gov bill page AND the roll call XML from Clerk.House.gov)
- Set `verificationLevel` to `"VERIFIED"` when multiple Tier 3 primary-government sources are combined
- The renderer shows a `N SOURCES` count badge in the collapsed header when `sources.length > 1`

**Verification level guide:**

| Level | Use when |
|---|---|
| `Tier 3` | Primary government source (congress.gov, senate.gov, whitehouse.gov) |
| `Tier 2` | Established institutional source (CBO, GAO, FEC, SEC filings) |
| `Tier 1` | Reputable third-party source (major news outlet, verified NGO) |
| `VERIFIED` | Multiple primary-government sources combined |

**Placement rule:** Always the **last element** in the `elements` array so it anchors the bottom of the snap card as a footer.

**`sources` array on snap root:** The snap root `sources[]` must also be populated consistently with the Trust.Thread's `sources[]` — same names and URLs. The root array is used by the feed renderer; the Trust.Thread element is the in-card display. Both must be in sync.

### SR-8 — Vertical Rhythm (MANDATORY)

Every PoliSnap card follows a strict vertical rhythm system defined in `GlobalStyles` (from `apps/mobile/constants/theme.ts`). Generated elements **must** use these globals — never write inline padding/margin on a container that has a corresponding `GlobalStyles` entry.

**The Two Laws:**

1. **Zero-Margin Policy**: All element-level containers use `marginVertical: 0`. Elements never add external vertical spacing to each other — the snap card's internal `paddingTop: 15` / `paddingBottom: Spacing.md` provides the outer breathing room.
2. **15px Vertical Track**: All non-narrative element containers use `paddingTop: 15` as the internal top breathing room. This is a hard constant, not `Spacing.lg` (16) or `Spacing.md` (12).

**Container-to-GlobalStyles Mapping:**

| Element category | Correct `GlobalStyles` container | Background tint |
|---|---|---|
| `Metric.*`, `Data.BillVote`, `Data.VotingRecord` | `metricContainer` | solid white |
| `Metric.Group`, `Metric.Dual.Comparison` | `metricGroupContainer` | 5% gray |
| `Universal.Gauge`, `Metric.Alignment.Gauge` | `gaugeContainer` | solid white |
| `Metric.Progress.Stepper` | `stepperContainer` | solid white |
| `Data.Table.Expandable` | `dataTableContainer` | Slate 50 |
| `Data.Consensus.Ripple` | `consensusRippleContainer` | solid white |
| `Visual.Chart.*`, `Visual.RipplePulse` | `visualContainer` | 8% blue tint |
| `Visual.Chart.Bar` | `barChartContainer` | 8% blue tint |
| `Visual.Chart.SentimentTrend` | `sentimentTrendContainer` | 6% blue tint |
| `Visual.Aggregate.Pulse` | `aggregatePulseContainer` | 8% rose tint |
| `Metric.Status.Grid` | `statusGridContainer` | solid white |
| `Interaction.*`, `Interaction.Sentiment.Pulse` | `interactionContainer` | 2% rose tint |
| `Logic.Predictive`, `Metric.PredictiveScoring` | `predictiveScoringContainer` | 5% purple tint |
| `Narrative.*` | `narrativeContainer` | transparent, `paddingVertical: 0` |
| `Metric.Congressional.WeeklySummary`, Congressional records | `congressionalRecordContainer` | white, 4px left border (primary) |

**Generated component StyleSheet must include:**
```typescript
container: {
  ...GlobalStyles.metricContainer, // use the correct container for the category
  // then override only what is genuinely unique to this element
},
```

**Do NOT override `paddingTop` or `marginVertical`** on the root container. Any element that changes `paddingTop` away from 15 or sets `marginVertical` to a non-zero value breaks the rhythm of the entire snap card.

**Doubled-Rhythm Diagnostic:** If an element's gap to its neighbour appears visually doubled, the root cause is almost always one of:
1. `marginVertical` is non-zero on the element container (Zero-Margin Policy violation)
2. The element wrote its own `padding` instead of spreading `GlobalStyles.*Container` — introducing a wrong `paddingTop` value
3. Both violations present simultaneously (e.g., `marginVertical: Spacing.sm` + `padding: Spacing.md` instead of `paddingTop: 15`)

**Correct pattern** — spread the canonical container, then add only element-unique overrides:
```typescript
container: {
  ...GlobalStyles.metricContainer, // correct container for the category
  borderRadius: 8,                 // only override what is genuinely unique
},
```

### SR-9 — Representative Header Rule (MANDATORY)

Any snap whose `metadata.representativeId` targets a **single representative** must include `Header.Representative` as the **first element** in the `elements` array. This establishes the identity anchor before any data elements render.

**Element structure:**
```json
{
  "id": "rep-header",
  "type": "Header.Representative",
  "data": {
    "id": "<representativeId>",
    "name": "<full name>",
    "party": "<\"Republican\" | \"Democrat\" | \"Independent\">",
    "location": "<State, District N>",
    "position": "<\"Representative\" | \"Senator\">",
    "imgUri": "https://unitedstates.github.io/images/congress/225x275/<representativeId>.jpg",
    "tags": []
  }
}
```

**Standard `imgUri` pattern**: `https://unitedstates.github.io/images/congress/225x275/{id}.jpg` — this is the canonical congressional photo CDN. Use it for any rep whose ID is a valid Bioguide ID.

**When to omit it**: Snaps that cover multiple representatives (e.g., a leaderboard, a debate between two reps, a committee vote summary) should use `Identity.Organization.Header` or no header at all.

---

### SR-10 — Extend vs New Element Analysis Protocol (MANDATORY)

Before creating a new `PoliElement` file, apply this protocol. The reuse gate (SR-7) asks "does an existing element fit?" — SR-10 governs what to do when the fit is *partial*.

**Step 1 — Classify the gap type:**

| Gap type | Description |
|---|---|
| `Data gap` | Element renders correctly but needs an additional optional data field (e.g., `description` on `Data.BillVote`) |
| `Style variant` | Element renders the right structure but uses slightly different visual weight or colour in this context |
| `Layout gap` | Element needs a new layout mode (e.g., horizontal vs vertical) |
| `Semantic gap` | The structural intent is genuinely different — this is a fundamentally different kind of content |

**Step 2 — Score on 4 dimensions (1 = extend, 3 = new):**

| Dimension | Score 1 | Score 2 | Score 3 |
|---|---|---|---|
| Structural overlap | Identical | Mostly same | Fundamentally different |
| Data model diff | Extra optional field | Extra required field or reshape | Different data shape |
| Visual divergence | Same styles | Minor override | Requires new StyleSheet |
| Reuse breadth | Used in 3+ snap types | Used in 1-2 types | One-off |

**Step 3 — Apply threshold:**
- Total score **≤ 7** → **EXTEND** the existing element (add optional field, add mode, or accept existing behaviour)
- Total score **≥ 8** → **CREATE NEW** element (document reason in a catalog note)

**Step 4 — Present verdict block before acting:**
```
SR-10 Verdict: EXTEND | NEW
Gap type: <type>
Scores: structural=X, data=X, visual=X, breadth=X  Total=X
Rationale: <one sentence>
Action: <exactly what will be added/created>
```

**Step 5 — Act on verdict:**
- EXTEND: add the field/mode to the existing element and its catalog row; do not create a new file
- NEW: follow the full creation workflow (SR-1 through SR-4), add catalog row, document gap type

---

### SR-11 — Snap Title & Subtitle Composition (MANDATORY)

The snap root `title` field appears in feed listings, notification summaries, and share previews. It must be **categorical and action-oriented** — not a verbatim copy of the subject.

**Title rules:**
- Max ~50 characters
- Describes the *kind* of record, not the specific subject
- Formula: `[Action/category noun]` — e.g., "Bill Vote", "Campaign Finance Analysis", "District Economic Impact"
- Must NOT contain the full bill name, bill number, or the representative's name

**Subtitle rules:**
- Use `subtitle` on the snap root for the specific subject context
- Formula: the subject proper noun — the bill name, the topic, the district, the date range
- Omit `subtitle` only when the context is self-evident from the category (rare)

**Transformation examples:**

| ❌ Bad `title` | ✅ Good `title` | `subtitle` |
|---|---|---|
| `"Vote on American Infrastructure and Jobs Act of 2026"` | `"Bill Vote"` | `"American Infrastructure and Jobs Act of 2026"` |
| `"Mike Johnson's Campaign Finance Analysis"` | `"Campaign Finance Analysis"` | *(rep is in Header.Representative — no subtitle needed)* |
| `"Corruption Index — Louisiana District 4"` | `"Corruption Index"` | `"Louisiana District 4"` |
| `"H.R. 1192 — Judicial Reform Act Committee Vote"` | `"Committee Vote"` | `"H.R. 1192 — Judicial Reform Act"` |

---

### SR-12 — No Representative Name Repetition in Element Content (MANDATORY)

`Header.Representative` establishes the representative's identity at the top of every single-rep snap. No other element in the `elements` array may repeat the representative's name as a heading, label, data field, or body copy.

**Specific prohibitions:**
- `Data.BillVote.data.representativeName` — **omit entirely** when `Header.Representative` is the first element
- Any `Narrative.*` element whose `data.title` begins with the rep's name (e.g., `"Rep. Johnson's Record"`) — rephrase to be subject-focused (`"Voting Record"`)
- Any `Metric.*` label that reads `"Rep. [Name]'s [X]"` — rephrase to just `"[X]"`
- Any intro sentence in `text`/`content`/`summary` fields that opens with the rep's name as subject — begin with the subject matter instead

**Rationale:** The header is the identity anchor; repeating the name wastes screen space, creates stale-data risk if rep data changes, and dilutes the data signal the user came to read.

---

### SR-13 — Sentiment Cadence Gate (MANDATORY)

Before including `Interaction.Sentiment.Pulse` in any snap, the skill **MUST** evaluate all of the following criteria. All must pass — a single failure means the sentiment element is omitted.

**Eligibility criteria:**

| Criterion | Pass | Fail — omit sentiment |
|---|---|---|
| Snap content type | Active/open bill, contested resolution, policy vote in progress, pending legislation | Closed/historical vote, FEC/finance data, biographical record, career summary |
| Existing interaction elements | No `Interaction.*` element already present in the snap | Any other `Interaction.*` element is present (one interaction max per snap) |
| Narrative-only snap | Snap has at least one data or metric element | Snap is purely narrative/editorial with no civic action available |

**Placement rule (when included):** `Interaction.Sentiment.Pulse` must be placed as the **second-to-last element** — immediately before `Trust.Thread` if present, otherwise as the last element.

**Rationale:** Not every snap warrants a call for constituent opinion. Overusing sentiment prompts trains users to ignore them; restricting to genuinely active and contested content maximises response quality and signal value.

---

### SR-15 — Drill-Down Navigation Rule (MANDATORY)

When a snap has `snapRelationshipRole` set in its NORM file, apply the following.

#### Parent snaps (`snapRelationshipRole: "parent"`)

**Step A — Inject `fullSpeechSnapId` into speaker entries.**
For every entry in a `Data.FloorDebate.data.speakers[]` or similar multi-speaker element:
- Match the speaker's `representativeId` to an entry in `suggestedChildSnaps[]` from the NORM file.
- If a match exists, set `fullSpeechSnapId: null` as a placeholder (the actual snap ID is not yet known at generation time — the distributor backfills it after child snaps are distributed).
- If no child snap exists for a speaker, omit `fullSpeechSnapId` entirely for that speaker.

**Step B — Add `Navigation.SnapLinks` element.**
When `suggestedChildSnaps[]` is non-empty, add a `Navigation.SnapLinks` element to the snap **immediately before `Interaction.Sentiment.Pulse`** (or immediately before `Trust.Thread` if no sentiment element is present).

```json
{
  "id": "nav-snap-links",
  "type": "Navigation.SnapLinks",
  "data": {
    "title": "Full Floor Speeches",
    "links": [
      {
        "snapId": null,
        "label": "Rep. Tim Walberg — Full Speech",
        "thumbnailRepId": "W000798"
      }
    ]
  }
}
```

> `snapId` values are `null` at generation time. The distributor backfills them after child snaps are distributed.

**Title guidance for `Navigation.SnapLinks`:**

| Drill-Down Role | Suggested `data.title` |
|---|---|
| `RepFullSpeech` / `RepFullStatement` | `"Full Floor Speeches"` |
| `WitnessTestimony` | `"Individual Testimonies"` |
| `BillDetail` | `"Related Bills"` |
| Mixed roles | `"See Full Details"` |

**Step C — Add `relationships[]` to the snap root.**
```json
"relationships": [
  {
    "type": "child",
    "snapId": null,
    "role": "Full speech — Rep. Tim Walberg",
    "drillDownRole": "RepFullSpeech",
    "entityId": "W000798"
  }
]
```

All `snapId` values in `relationships[]` are `null` at generation time and backfilled by the distributor.

#### Child snaps (`snapRelationshipRole: "child"`)

**Step A — Add `relationships[]` to the snap root** with the parent reference:
```json
"relationships": [
  {
    "type": "parent",
    "snapId": null,
    "role": "Floor Debate summary",
    "drillDownRole": "RepFullSpeech",
    "parentSpawnRef": "SPAWN-20260530-090001-hr2616-floor-debate"
  }
]
```

The parent `snapId` is `null` at generation time. The distributor backfills it when the parent is distributed.

**Step B — No `Navigation.SnapLinks` element.** Child snaps do not contain drill-down navigation. They are standalone accountability snaps.

#### Standalone snaps (`snapRelationshipRole: null`)

No `relationships[]` field. No `Navigation.SnapLinks` element. Standard construction.

---

### SR-16 — Snap Title for Child Snaps (MANDATORY)

Child snaps produced via drill-down follow all SR-11 title rules and additionally:

**Title formula for `RepFullSpeech` / `RepFullStatement`:** `"Floor Speech"` or `"Congressional Statement"`
**Title formula for `WitnessTestimony`:** `"Committee Testimony"`
**Subtitle:** `"[Rep Full Name] — [Bill ID or Topic]"` e.g., `"Rep. Tim Walberg — H.R.2616"`

The representative's name is allowed in `subtitle` but NOT in `title`. The `Header.Representative` element anchors identity; the subtitle is the disambiguation context.

---


When SR-13 determines sentiment is eligible, apply these rules to compose the `Interaction.Sentiment.Pulse` element.

**Question title formula:**
```
"[Public/Constituent] [Verb] on [Subject]"
```
Examples: `"Public Support for S. Res 45"`, `"Constituent Opinion on H.R. 1192"`, `"Public View on Arctic Drilling Ban"`

**Options rules:**

| Rule | Detail |
|---|---|
| Minimum | 2 options |
| Maximum | 4 options |
| Count guidance | Use 2 for binary civic issues (support / oppose). Use 3–4 for nuanced policy topics where a middle-ground or conditional position is meaningful. |
| Label length | 1–4 words per option |
| Label tone | Action-oriented, non-leading, non-overlapping. E.g., `"Support"`, `"Oppose"`, `"Needs Revision"`, `"Undecided"` |
| Relevance test | Every option must be directly answerable based on the snap's presented content. Do not add options that require knowledge not in the snap. |

**Forbidden question patterns:**
- Leading options (e.g., `"Obviously Support"`, `"Strongly Oppose"` as the only alternatives)
- Double-barreled titles (e.g., `"Support the bill and the senator?"`)
- Generic non-contextual titles (e.g., `"Do you care about this issue?"`)
- Options that overlap semantically (e.g., `"Agree"` and `"Support"` together)

**Example — 2-option (binary):**
```json
{
  "id": "sentiment-pulse",
  "type": "Interaction.Sentiment.Pulse",
  "data": {
    "title": "Public Support for S. Res 45",
    "options": [
      { "id": "support", "label": "Support" },
      { "id": "oppose",  "label": "Oppose" }
    ],
    "stats": { "agree": 0, "disagree": 0 }
  }
}
```

**Example — 4-option (nuanced):**
```json
{
  "id": "sentiment-pulse",
  "type": "Interaction.Sentiment.Pulse",
  "data": {
    "title": "Constituent Opinion on H.R. 1192",
    "options": [
      { "id": "support",   "label": "Support" },
      { "id": "oppose",    "label": "Oppose" },
      { "id": "revise",    "label": "Needs Revision" },
      { "id": "undecided", "label": "Undecided" }
    ],
    "stats": { "agree": 0, "disagree": 0 }
  }
}
```

---

## Forbidden Patterns

| ID | Pattern | Consequence |
|---|---|---|
| FP-01 | Hardcoded colors, font sizes, or spacing values. | All styling must use the `Colors`, `Typography`, and `Spacing` constants from `apps/mobile/constants/theme.ts`. |
| FP-02 | Creating a new component when a similar one exists. | The skill must encourage extension or reuse of existing components first. |
| FP-03 | Forgetting to register the component. | The component will not be renderable by the `PoliSnap` engine. The `ComponentFactory.register` call is mandatory. |
| FP-04 | Forgetting to update the central `index.ts`. | The component's registration code will never run. |
| FP-05 | Writing to `snapLibrary.ts` from this skill. | **Owned by `polisnap-distributor`.** The generator outputs a SNAP file to `constructed/` only. |
| FP-06 | Validating or rejecting a `representativeId` not in a hard-coded table. | **Owned by `polisnap-normalizer`.** Trust `validatedRepresentativeId` from the NORM file. |
| FP-07 | Validating or rejecting a `policyArea` not in a hard-coded list. | **Owned by `polisnap-normalizer`.** Trust `validatedPolicyArea` from the NORM file. |
| FP-11 | Overriding `paddingTop` away from `15` or setting `marginVertical` to a non-zero value on an element's root container. | Breaks the snap card's vertical rhythm — elements appear cramped or over-spaced relative to each other. Use the correct `GlobalStyles` container and do not fight it. |
| FP-12 | Omitting `Header.Representative` as the first element on a snap that targets a single `representativeId`. | The snap lacks identity context — users cannot immediately tell whose record is being displayed. |
| FP-10 | Creating a new `PoliElement` file when an existing element in the Element Reuse Catalog already serves the intent (e.g., creating a new "PublicSentiment" component instead of using `Narrative.SentimentSummary`). | Duplicate elements that diverge over time, inconsistent UI, and unnecessary code maintenance. Always check the catalog first. |
| FP-08 | Fabricating a URL in `Trust.Thread` or `sources` when no URL was provided in the intent. | Produces false provenance. If no source URL is in the intent, omit `Trust.Thread` entirely. |
| FP-09 | Placing `Trust.Thread` anywhere other than the last element in the `elements` array. | It acts as the snap's provenance footer — mid-array placement breaks visual hierarchy. |
| FP-13 | Creating a new `PoliElement` when SR-10 verdict is EXTEND (total score ≤ 7). | Unnecessary file proliferation; use the extension path instead. |
| FP-16 | Writing inline `padding`, `backgroundColor`, or `marginVertical` on an element root container instead of spreading the correct `GlobalStyles.*Container`. | Produces doubled or inconsistent vertical rhythm across snap cards. Spread the canonical container and override only what is genuinely unique to the element. |
| FP-14 | Setting `snap.title` to a verbatim copy of the bill name, subject proper noun, or any full proper noun from the snap's data (e.g., `"Vote on American Infrastructure and Jobs Act of 2026"`). | Clutters feed listings with wall-of-text titles. Use a categorical title + `subtitle` per SR-11. |
| FP-15 | Including the representative's name in any element's `data` (as a field value, label, title, or body copy) when `Header.Representative` is already the first element in the snap. | Redundant identity display — the header is the single source of truth for the rep's identity. See SR-12. |
| FP-17 | Including `Interaction.Sentiment.Pulse` in a snap that fails the SR-13 Sentiment Cadence Gate — i.e., snap covers a closed/historical event, already contains an `Interaction.*` element, or is purely narrative. | Degrades signal quality; users learn to ignore sentiment prompts that appear on irrelevant content. Apply SR-13 before every sentiment decision. |
| FP-18 | Including a `sourceLink`, `sourceUrl`, or any equivalent source-reference field in any element other than `Trust.Thread` when a `Trust.Thread` element is present in the snap. | Produces duplicate source display — the same URL appears in both the narrative body and the Trust Thread footer. Violates the Source Consolidation Rule (SR-6 SCR). All source references must live exclusively in `Trust.Thread.data.sources[]`. |
| FP-19 | Generating a `Navigation.SnapLinks` element or populating `fullSpeechSnapId` on speaker entries before the child snaps have been generated. | At generation time all `snapId` / `fullSpeechSnapId` values are `null` placeholders. The distributor performs the backfill — do not attempt to resolve them here. |

---

## Snap Construction Output

The generator outputs a **PoliSnapConstructed** JSON file ready for the distributor. It does NOT write to `snapLibrary.ts`.

**File:** `SNAP-{id}.json`
**Location:** `apps/skill-execution/PoliSnaps/constructed/`
**ID format:** Descriptive kebab-case slug (e.g., `snap-sres45-thune-bill-position`, `snap-warren-healthcare-vote`)

```json
{
  "id": "snap-sres45-thune-bill-position",
  "sku": "snap-sres45-thune-bill-position",
  "title": "Bill Position",
  "subtitle": "S. Res. 45 — Arctic Wilderness Protection",
  "type": "Accountability",
  "createdAt": "2026-05-30T14:35:00Z",
  "normRef": "NORM-20260530-143045-arctic-drilling-ban",
  "sources": [{ "name": "Congress.gov", "url": "https://www.congress.gov/bill/119th-congress/senate-resolution/45" }],
  "metadata": {
    "representativeId": "T000250",
    "policyArea": "Public Lands and Natural Resources",
    "insightType": "Legislative Status"
  },
  "relationships": [],
  "elements": [
    { "id": "header-rep", "type": "Header.Representative", "data": { "..." : "..." } },
    { "id": "summary", "type": "Narrative.Insight.Summary", "data": { "..." : "..." } },
    { "id": "progress", "type": "Metric.Progress.Stepper", "data": { "..." : "..." } },
    { "id": "sentiment", "type": "Interaction.Sentiment.Pulse", "data": { "..." : "..." } },
    { "id": "trust-thread", "type": "Trust.Thread", "data": { "..." : "..." } }
  ]
}
```

**Floor Debate parent snap with drill-down (SR-15 applied):**

```json
{
  "id": "snap-hr2616-floor-debate-20260520",
  "title": "House Floor Debate",
  "subtitle": "H.R.2616 — PROTECT Kids Act",
  "type": "Accountability",
  "createdAt": "2026-05-30T09:01:30Z",
  "relationships": [
    { "type": "child", "snapId": null, "role": "Full speech — Rep. Tim Walberg", "drillDownRole": "RepFullSpeech", "entityId": "W000798" },
    { "type": "child", "snapId": null, "role": "Full speech — Rep. Frank Pallone", "drillDownRole": "RepFullSpeech", "entityId": "P000034" }
  ],
  "elements": [
    { "id": "floor-debate", "type": "Data.FloorDebate", "data": {
        "speakers": [
          { "representativeId": "W000798", "name": "Tim Walberg", "quote": "...", "fullSpeechSnapId": null },
          { "representativeId": "P000034", "name": "Frank Pallone", "quote": "...", "fullSpeechSnapId": null }
        ]
    }},
    { "id": "nav-snap-links", "type": "Navigation.SnapLinks", "data": {
        "title": "Full Floor Speeches",
        "links": [
          { "snapId": null, "label": "Rep. Tim Walberg — Full Speech", "thumbnailRepId": "W000798" },
          { "snapId": null, "label": "Rep. Frank Pallone — Full Speech", "thumbnailRepId": "P000034" }
        ]
    }},
    { "id": "sentiment", "type": "Interaction.Sentiment.Pulse", "data": { "..." : "..." } },
    { "id": "trust-thread", "type": "Trust.Thread", "data": { "..." : "..." } }
  ]
}
```

---

## Handoff

After writing the constructed SNAP file, present:
1. The snap file path in `constructed/`
2. Any new element `.tsx` files created (if applicable)
3. Next step: `Distribute [snapId]`
