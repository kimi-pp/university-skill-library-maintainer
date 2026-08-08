# General CS Master Thesis Context

This reference defines transferable writing and review rules for computer science master's theses. It is not a topic-specific glossary, implementation plan, or university template. Use it to help students avoid common thesis problems: drifting terminology, claims that exceed evidence, mixed chapter responsibilities, implementation-manual prose, weak reproducibility, and limitation-first framing.

Applicable to:

- Computer science, software engineering, systems, AI, data, HCI, networking, security, parallel computing, and adjacent master's theses.
- Thesis planning, chapter revision, supervisor/reviewer feedback triage, and pre-defense self-review.
- Agent or skill workflows that need a general thesis-quality layer before project-specific terminology and evidence are applied.

Not applicable as:

- A replacement for university templates, course manuals, ethics rules, or supervisor instructions.
- A replacement for specialized domain methods such as formal verification, human-subject protocols, ML statistical evaluation, or security evaluation.
- A source of topic-specific conclusions, contributions, or results.

---

## 1. Fix the central research object first

Every thesis needs a clearly bounded research object. Early in the Introduction, the reader should be able to answer:

- What system, method, model, tool, dataset, algorithm, or process is studied?
- Which part of it does the thesis change?
- Which part of it remains unchanged?
- Is the thesis evaluating an implementation, design principle, experiment, user experience, or theoretical property?

Avoid:

- Replacing the research object with project history.
- Replacing the thesis object with repository structure.
- Opening with technology stacks, scripts, commands, or implementation steps.
- Treating "I built many things" as a contribution.

Stable pattern:

> This thesis studies X in the context of Y. It proposes Z, evaluates it with E, and limits the claim to S.

---

## 1a. Treat project context as the semantic gate

Many thesis projects maintain a current glossary, context file, supervisor-feedback ledger, evidence ledger, or agent memory. When such files exist, they are not background reading; they define the local thesis boundaries.

Before reviewing or rewriting, identify the relevant entries and check:

- canonical terms and forbidden synonyms;
- current versus historical, superseded, or planned facts;
- accepted evidence versus diagnostic evidence;
- chapter responsibility for definitions, design, method, evaluation, discussion, and future work;
- explicit "avoid" or "do not claim" constraints.

If the general checklist suggests a change that conflicts with the project context, the project context wins. Report the conflict instead of silently rewriting around it.

Avoid:

- using memory of an older thesis state when a current context file exists;
- turning a future-work item into a current contribution;
- moving material across chapter responsibilities without author approval;
- treating a glossary as optional style guidance.

---

## 2. Research questions must map to contributions

Research questions (RQs) are the thesis backbone, not decorative questions. Each RQ should have:

- a clear answer type: taxonomy, architecture, algorithm, measurement, comparison, design rationale, user evidence, and so on;
- a corresponding chapter or section;
- a corresponding contribution;
- an acceptable evidence type;
- a scope boundary.

Self-check:

- If a contribution has no matching RQ, delete it or demote it to implementation detail.
- If an RQ has no evaluation, argument, or literature synthesis behind it, rewrite or split it.
- If an RQ uses broad words such as "effective", "good", "better", or "efficient", name the dimension: latency, accuracy, robustness, usability, resource cost, maintainability, coverage, correctness, and so on.
- Do not keep obsolete RQ numbering or old question versions in the final thesis.

Suggested mapping table:

| RQ | Question | Answer type | Evidence | Main chapter |
|----|----------|-------------|----------|--------------|
| RQ1 | What problem/model/scope is appropriate? | conceptual model / taxonomy | literature + constraints | Background / Method |
| RQ2 | What design or method addresses it? | architecture / algorithm / process | design rationale + implementation | Design |
| RQ3 | What does the result support? | measured capability / qualitative finding | experiments / study / analysis | Evaluation |
| RQ4 | What is the cost or trade-off? | performance / effort / resource trade-off | comparative data / ablation | Evaluation / Discussion |

---

## 3. Give each chapter a limited job

Each chapter should answer a clear reader question. A single paragraph should not define concepts, introduce a method, report results, and discuss limitations at the same time.

Recommended responsibilities:

| Chapter | Reader question | Should contain | Should avoid |
|---------|-----------------|----------------|--------------|
| Abstract | What is this thesis about and what was found? | scenario, action, evidence, scoped result | mechanism inventory, long limitation list |
| Introduction | Why does the problem matter and what are the RQs? | problem, gap, RQs, contributions | detailed taxonomy, implementation walkthrough |
| Background | What must the reader know first? | concepts, system context, terminology, assumptions | new results, evaluation claims |
| Related Work | What exists and where is the gap? | critical comparison by theme | paper-by-paper summary without synthesis |
| Method | How will the thesis answer the RQs? | research method, case selection, evidence plan | raw script logs, implementation chronology |
| Design | What is the proposed solution and why? | contracts, invariants, trade-offs | ports, filenames, helper functions, command traces |
| Implementation | How was the design instantiated? | implementation choices with architectural consequence | user manual, exhaustive file tour |
| Evaluation | What evidence supports the answers? | testbed, metrics, admission criteria, results | artifact path walkthrough, private hostnames |
| Discussion | What do results mean and where do they apply? | contribution-first interpretation, scope, threats | limitation-first self-rejection |
| Conclusion | What are the scoped answers? | RQ answers, contributions, future work | new concepts, new evidence, long audit |

---

## 4. Use Background as the terminology anchor

Terms that recur across chapters should normally receive their first clear definition in Background. Method, Design, and Evaluation can specialize those terms, but they should not be the first place where the reader learns their boundaries.

A useful term definition includes:

- term;
- plain-language definition;
- boundary: what it is not;
- role in this thesis;
- first-use rule: full name, acronym, citation, or source system.

Template:

```markdown
**Term**:
One-sentence definition in this thesis.
Role: why the term matters for the RQ or design.
Boundary: what this term does not mean.
Avoid: ambiguous synonyms or overloaded terms.
```

Avoid:

- Switching synonyms for the same concept across chapters.
- Using an acronym before the full term is introduced.
- Importing an external system's term without adapting it to this thesis.
- Introducing a new taxonomy in Discussion or Conclusion.

---

## 5. Claims must be bounded by evidence

A thesis claim must not be broader than the evidence that supports it. For every strong claim, answer:

- Where does the evidence come from?
- Which cases, datasets, workloads, participants, hardware, failure modes, or benchmarks does it cover?
- Which observations are diagnostic only and do not enter the main conclusion?
- Is the conclusion a proof, measurement, prototype evidence, case-study evidence, or plausibility argument?

Common claim levels:

| Claim strength | Acceptable evidence | Wording |
|----------------|---------------------|---------|
| Demonstrated in prototype | working implementation + selected tests | "demonstrates in the evaluated settings" |
| Measured improvement | repeated comparative measurements | "reduces X under Y by Z" |
| Supports a class of cases | explicit case selection rationale | "supports the selected cases" |
| Suggests broader applicability | structural or theoretical argument | "provides a basis for" |
| General guarantee | formal proof or exhaustive assumptions | use "guarantees" only when actually proven |

Avoid:

- Turning prototype evidence into a production-grade guarantee.
- Turning selected benchmarks into general performance conclusions.
- Turning a single case study into a universal property.
- Presenting future work as already supported.
- Repeating broad negative caveats after the relevant scope boundary has already been stated.

Capability-first framing:

- State what the thesis currently supports, demonstrates, measures, or explains.
- State the evidence boundary near the first claim that needs it.
- Put natural extensions in Future Work or the chapter responsible for scope, not as repeated local disclaimers.
- Do not weaken a contribution so much that the reader only sees what was not done.

---

## 6. Method explains how evidence answers the RQs

The Method chapter is not an implementation log. It should explain why the chosen cases, datasets, benchmarks, participants, measurements, or analysis steps can answer the RQs.

Method should state:

- case / dataset / workload / participant selection rationale;
- independent and dependent variables;
- measurement window, repetitions, baseline, comparison pairs;
- acceptance and exclusion criteria;
- qualitative coding or analysis procedure;
- validity threats considered in the research design.

Avoid:

- Only listing how scripts were run.
- Moving all repository artifacts into the thesis text.
- Using file names, commit hashes, and private paths as a substitute for method.
- Backfilling a method after seeing results without explaining the design rationale.

---

## 7. Design explains contracts, invariants, and trade-offs

The Design chapter should answer why the structure is reasonable, not merely how code executes.

Design prose should prioritize:

- abstraction: which conceptual objects make up the system;
- contract: what each object guarantees and depends on;
- invariant: what must remain true during execution;
- alternatives: what designs were considered and rejected;
- trade-off: cost, complexity, scalability, reliability, performance, and maintainability;
- scope: what the current design supports and does not support.

Keep implementation details only when they have architectural consequences, for example:

- failure-domain granularity;
- concurrency model;
- consistency boundary;
- data ownership boundary;
- scheduling or placement policy;
- security or privacy boundary;
- measurement instrumentation boundary.

Avoid:

- Making function names the subjects of conceptual paragraphs.
- Explaining design through ports, helper names, message strings, or command traces.
- Turning workflow figures into execution traces.
- Using a prominent "What remains" negative list in Design instead of a scoped design boundary and Future Work.

---

## 8. Evaluation needs evidence admission, not an artifact log

Evaluation should explain which evidence is allowed to support conclusions and how it is aggregated.

Evaluation should state:

- testbed or study setting;
- number of accepted runs, samples, participants, or cases;
- baseline and treatment;
- metric definitions;
- admission rule;
- exclusion rule;
- aggregation method, such as mean, median, P95, confidence interval, effect size, or coding frequency;
- whether diagnostic evidence is explanatory only and excluded from main statistics.

Testbed or setting descriptions should include enough for reader-facing reproducibility:

- hardware / software / OS / library versions;
- cluster, device, browser, dataset, or participant setting;
- network, runtime, compiler, model, or toolchain conditions;
- public artifact location or appendix reference when appropriate.

Avoid:

- Replacing explanation with raw filenames, private hostnames, absolute local paths, or script options.
- Treating commit hashes, campaign directories, generated JSON files, or internal gate logs as the main evidence narrative.
- Reporting only favorable results without explaining rejected evidence.
- Mixing steady-state cost, recovery time, resource cost, accuracy, or usability without naming the dimension.
- Reporting only percentages without absolute values and context.

Useful distinction:

- Evidence admission belongs in Method/Evaluation: accepted runs, accepted measurements, inclusion/exclusion rules, aggregation, and diagnostic-only material.
- Artifact provenance belongs in a repository, appendix, or supplementary material unless the reader needs it to understand reproducibility.
- Traceability prose should name structured evidence categories, not walk through raw files or scripts.

---

## 9. Related Work must synthesize, not dump references

Related Work should build comparison axes around the RQs, not summarize one paper after another.

Useful comparison axes:

- problem setting;
- fault model, threat model, or user model;
- abstraction level;
- recovery or optimization mechanism;
- assumptions;
- evidence type;
- cost or limitations;
- relation to this thesis.

Each subsection should end by answering:

> Compared with these works, this thesis differs in X, adopts Y, or leaves Z out of scope.

Avoid:

- Mini-surveys of "Paper A did..., Paper B did...".
- Describing only strengths without explaining boundaries relative to this thesis.
- Citing unrelated work only to increase reference count.
- Related Work that never returns to the RQs.

---

## 10. Figures and tables are not substitutes for prose

Figure and table captions should identify the object and give only the minimum reading cue. Mechanism explanation, design rationale, experimental meaning, scope boundaries, and result interpretation belong in the surrounding prose.

Caption rules:

- Prefer one or two sentences.
- First state what the reader is looking at.
- Add only the essential reading cue.
- If the caption is long, the prose around the figure probably needs work.
- Use short captions for Lists of Figures / Tables when needed.

Figure/table self-check:

- Are title, units, legend, and axis labels clear?
- Can the reader distinguish baseline, treatment, and diagnostic evidence?
- Is the visual too crowded?
- Does unfinished work look like a completed path?
- Do all colors, line styles, and symbols have meaning?
- Does the rendered PDF remain readable at body-text size?
- Has the caption stayed short enough that explanation still lives in the prose?

---

## 11. Discussion should explain contribution before scope

Recommended Discussion order:

1. Result meaning: what the results show.
2. Why it matters: what this means for the RQs, system, method, or field.
3. Scope: the evaluated settings where the result holds.
4. Threats: factors that may affect interpretation.
5. Future work: extensions that naturally follow.

Avoid:

- Starting with "This does not prove...".
- Letting limitation lists overpower the contribution.
- Introducing new mechanisms or new data in Discussion.
- Writing Future Work as if it were part of the current design.

Stable pattern:

> The results show X under Y. This matters because Z. The conclusion is limited to S, since E does not cover T. Extending the result to T would require F.

---

## 12. Conclusion closes the thesis, it does not add a new one

Conclusion should be restrained. It answers the RQs, summarizes contributions, states future work, and closes with a scoped claim.

Conclusion should not:

- introduce new terms;
- report new data;
- add new related work;
- perform a long limitation audit;
- repeat Method or Evaluation details;
- replace scoped answers with slogans.

Suggested structure:

- one-paragraph problem and approach recap;
- scoped answers to RQs;
- key contributions;
- future work;
- closing claim with explicit scope.

---

## 13. Style: academic engineering, not a software manual

A CS thesis may discuss code and systems, but its main line must be concepts, design rationale, and evidence.

Prefer:

- abstract object before concrete function;
- invariant before implementation step;
- trade-off before tool choice;
- metric before raw log;
- reader-facing term before internal identifier.

Avoid:

- "The script then...";
- "The function does...";
- "The file contains...";
- "The command outputs...";
- "The framework is good/fast/robust" without a dimension.

Paragraph test:

> If removing function names, file names, commands, port numbers, and log strings leaves the paragraph nearly empty, it is an implementation note, not thesis prose.

---

## 14. Feedback triage workflow

Do not patch supervisor, examiner, or reviewer feedback line by line immediately. Classify the underlying issue first:

| Feedback type | Meaning | Correct response |
|---------------|---------|------------------|
| Undefined concept | reader lacks a terminology anchor | define in Background or first-use location |
| Flow issue | chapter or paragraph responsibilities are mixed | separate concept, design, evidence, and discussion |
| Too detailed | prose reads like a manual or log | abstract into contract, metric, or setting |
| Claim too strong | evidence boundary is unclear | downgrade claim or add evidence |
| Caption too long | figure/table is doing the prose's job | move explanation to surrounding prose |
| Limitation-first | contribution is being weakened upfront | use contribution-first scope framing |
| Missing reproducibility | reader cannot reconstruct the setting | add testbed, method, and admission rule |
| Stale fact | old plan or snapshot contradicts current context | verify against current source and update wording |
| Future-work confusion | extension reads like completed support | separate current support from future extension |

Processing order:

1. Update terminology or context rules first.
2. Rewrite chapter structure next.
3. Polish sentence-level wording last.

---

## 15. General self-review checklist

Before sending to a supervisor or examiner, check:

- Every RQ has a clear answer later in the thesis.
- Every contribution maps to an RQ.
- Background defines terms used repeatedly later.
- Every Related Work subsection relates back to the thesis.
- Method explains evidence design, not only scripts.
- Design explains contracts, invariants, and trade-offs.
- Evaluation states accepted evidence, excluded evidence, and aggregation.
- Figures and tables are readable, and captions do not replace prose.
- Discussion explains contribution before scope.
- Conclusion introduces no new concepts or data.
- Strong claims have scope qualifiers.
- Acronyms are expanded at first use.
- Terms do not drift across chapters.
- Code identifiers appear only when necessary.
- Future Work is not presented as a completed contribution.

---

## 16. Suggested skill behavior

When this reference is used inside a skill, trigger it for:

- thesis, chapter, or section review;
- supervisor or reviewer feedback triage;
- thesis structure, RQ, or evaluation planning;
- converting implementation work into thesis prose;
- checking claim scope, Related Work, Evaluation, Discussion, or Conclusion.

Expected skill output:

- issue classification;
- risk severity;
- concrete revision advice;
- replacement thesis prose when requested;
- evidence and scope boundaries;
- whether the glossary, Method, Evaluation, or Discussion also needs updating.

The skill must not:

- invent thesis content without reading the user's source;
- treat this template as the final conclusion;
- exaggerate the user's contribution;
- ignore university, supervisor, or course-specific requirements.

Severity labels:

- P0: factual, evidence, RQ, or project-boundary error.
- P1: contribution, terminology, evidence-admission, claim-scope, or chapter-responsibility risk.
- P2: reader-facing clarity issue that materially affects comprehension.
- P3: optional style preference that should not drive another rewrite loop by itself.

---

## 17. Shortest workflow under time pressure

When time is limited, work in this order:

1. Fix RQ-to-contribution mapping.
2. Fix core terminology and first-use order.
3. Downgrade all claims that exceed evidence.
4. Move implementation details out of conceptual chapters.
5. Add Evaluation testbed, metrics, and admission criteria.
6. Compress captions.
7. Rewrite Discussion and Conclusion as contribution-first.

These seven steps address most structural risks in CS master's theses.
