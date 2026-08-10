---
name: cs-thesis-reviewer
description: Review, plan, and revise computer science master thesis writing using general thesis rules for RQs, contributions, terminology, claim scope, method, design, evaluation, related work, discussion, conclusion, and supervisor/reviewer feedback. Use when Codex is asked to review a CS thesis chapter or section, improve thesis prose, triage thesis feedback, design or audit RQs and contributions, convert implementation work into academic thesis prose, check evaluation evidence boundaries, or create a thesis revision plan.
---

# CS Thesis Reviewer

## Core Rule

Treat a CS master thesis as an argument from research questions to scoped evidence-backed answers. Keep the thesis academic: concepts, design rationale, method, evidence, and scope come before implementation chronology, scripts, logs, and file names.

Project-specific semantic context is binding. If the project provides a glossary, context file, supervisor rule set, evidence ledger, or current-memory file, treat it as the semantic gate for terminology, claim scope, chapter responsibility, and accepted evidence before applying this general checklist.

For a full review, feedback triage, RQ/evaluation planning, or substantial rewrite, read `references/general-context.md`. For a small local wording question, use the workflow below without loading the reference unless a boundary is unclear.

## Workflow

1. Identify the task type: chapter review, rewrite, RQ planning, evaluation audit, related-work audit, feedback triage, or implementation-to-thesis conversion.
2. Gather the source: thesis text, chapter file, feedback note, RQ list, evaluation summary, or project-specific context. If the user gives a path, inspect it before giving thesis-level advice.
3. Apply project-specific instructions first: university rules, advisor feedback, existing glossary, required language, citation style, current facts, and factual implementation status override this general skill.
4. Run the semantic gate: identify the relevant project-context entries, check their avoid/constraint rules, and distinguish current facts from historical notes, plans, and future work. If the requested edit conflicts with the project context, surface the conflict before rewriting.
5. Check the thesis argument in this order:
   - research object is clear;
   - each RQ maps to a contribution and evidence type;
   - recurring terms are defined before heavy use;
   - same-scope terms do not drift for stylistic variety;
   - claims do not exceed evidence;
   - Method explains evidence design, not only scripts;
   - Design explains contracts, invariants, and trade-offs;
   - Evaluation states setting, metrics, admission criteria, accepted/excluded evidence, and aggregation;
   - raw artifact provenance is not substituted for reader-facing evidence rules;
   - Discussion is contribution-first, scope-second, future-work-last;
   - Conclusion adds no new concepts or evidence.
6. Produce the requested output: findings, rewrite, outline, checklist, or revision plan. Keep findings concrete and tied to text locations when possible.

## Review Priorities

Report high-impact problems before style:

- Project-context conflict or stale/historical fact used as current truth.
- RQ/contribution mismatch.
- Undefined or drifting terminology.
- Claim stronger than evidence.
- Related Work without synthesis or relation to the thesis.
- Method that reads as a script log.
- Design that reads as an implementation manual.
- Evaluation without accepted evidence, rejected evidence, metric definitions, or aggregation rules.
- Evidence admission replaced by raw paths, scripts, logs, private hostnames, or artifact inventories.
- Captions that carry mechanism explanation or result interpretation.
- Limitation-first Discussion or Conclusion.
- Future Work presented as completed contribution.

## Output Patterns

For a review, use this shape:

```markdown
**Findings**
- [Severity] Location: issue, why it matters, concrete fix.

**Open Questions**
- Facts or evidence needed before rewriting.

**Suggested Revision**
- Minimal changes or replacement prose if the user asked for rewrite-ready output.
```

For feedback triage, classify each comment:

```markdown
| Feedback | Underlying issue | Correct response | Target section |
|----------|------------------|------------------|----------------|
```

For RQ or contribution planning, use:

```markdown
| RQ | Answer type | Contribution | Evidence | Chapter |
|----|-------------|--------------|----------|---------|
```

For rewrites:

- Preserve the user's factual claims, citations, terminology, and intended scope.
- Do not invent results, references, experiments, or implementation status.
- Do not change RQs, fault/scope boundaries, metric definitions, admitted evidence, or chapter responsibility unless the user explicitly asks for that change.
- Replace implementation identifiers with reader-facing abstractions unless the section is explicitly about implementation details.
- Add scope qualifiers when evidence is bounded.
- Prefer capability-first scope framing: state the current supported contribution first, then state boundaries or future extensions where they belong.
- Keep necessary scope anchors, but remove repeated defensive caveats once the boundary is clear.
- Keep code identifiers, commands, logs, and paths only when they are necessary evidence or exact artifact references.

## Chapter Checks

- Abstract: scenario, action, evidence, scoped result. Avoid mechanism inventory and limitation lists.
- Introduction: problem, gap, RQs, contributions. Avoid detailed taxonomy and implementation walkthrough.
- Background: first formal definitions of recurring concepts and acronyms.
- Related Work: compare by themes and end each subsection by relating it to this thesis.
- Method: justify case/dataset/workload selection, variables, repetitions, acceptance/exclusion rules, and validity boundaries.
- Design: state abstractions, contracts, invariants, alternatives, current support, and trade-offs. Keep future mechanisms as scoped extensions, not local limitation lists.
- Implementation: include only details that explain how the design was instantiated or constrained.
- Evaluation: report setting, metrics, accepted evidence, excluded/diagnostic evidence, aggregation, and reader-facing results. Keep raw provenance in repositories, appendices, or supplementary material unless it directly supports reproducibility.
- Discussion: explain result meaning first, then evaluated scope, threats, and natural future work.
- Conclusion: answer RQs and close the thesis without new evidence, new umbrella terms, or long limitation audits.

## Severity Labels

- P0: factual, evidence, RQ, or project-boundary error.
- P1: contribution, terminology, evidence-admission, claim-scope, or chapter-responsibility risk.
- P2: reader-facing clarity issue that materially affects comprehension, such as implementation-manual prose, term drift, overloaded captions, or repeated defensive framing.
- P3: optional style preference. Do not keep rewriting solely for P3 issues.

## Reference

Use `references/general-context.md` for the complete checklist and detailed rule set when the task touches multiple chapters, supervisor feedback, RQ design, evaluation evidence, or claim scope.
