---

name: aligning-curriculum

description: Review course consistency by checking that outcomes, content, and assessments align. Use after designing sessions.

---



# Curriculum Alignment Check



## Triggering Contexts



- User has completed (or partially completed) session designs

- User feels the course is "drifting" or inconsistent

- User wants to verify course quality before teaching

- User asks "does this course make sense as a whole?"



## Core Principle



> **Alignment = Every piece connects to the whole.**

> If a topic doesn't serve an outcome, cut it.

> If an outcome has no assessment, add one.

> If a session has no purpose, redesign it.



---



## Alignment Checks



### Check 1: Outcome Coverage Matrix



Map every session to the outcomes it serves:



| Session | Out. 1 | Out. 2 | Out. 3 | Out. 4 | Out. 5 |

|---------|--------|--------|--------|--------|--------|

| S1 | I | | | | |

| S2 | P | I | | | |

| S3 | P | P | I | | |

| S4 | | P | P | I | |

| S5 | A | | P | P | I |

| S6 | | A | A | P | P |

| S7 | | | | A | A |



**Legend:** I = Introduce, P = Practice, A = Assess



**Red flags:**



- ❌ Outcome column is empty → Outcome never taught

- ❌ Outcome has I but no P → Introduced but never practiced

- ❌ Outcome has no A → Never assessed

- ❌ Session row is empty → Session serves no outcome (cut it)

- ⚠️ A appears before P → Assessing before students practiced



### Check 2: Prerequisite Chain



Verify no session requires knowledge not yet taught:



```

Session 3 requires: [concept from S1] ✅, [concept from S2] ✅

Session 5 requires: [concept from S3] ✅, [concept from S7] ❌ NOT YET TAUGHT

```



**Fix:** Resequence sessions or move prerequisites earlier.



### Check 3: Difficulty Progression



Plot the difficulty curve:



```

Difficulty

  ▲

  │          ╱──╲

  │      ╱──╱    ╲──╲

  │  ╱──╱              ╲

  │╱                     

  └──────────────────────→ Sessions

  S1  S2  S3  S4  S5  S6

```



**Red flags:**



- ❌ Flat line → No progression, students get bored

- ❌ Spike → Session is too hard relative to neighbors

- ❌ Drop after spike → Inconsistent difficulty

- ✅ Gradual incline with occasional plateaus → Healthy



### Check 4: Format Distribution



Count format types across all sessions:



| Format | Count | % of Total | Assessment |

|--------|-------|------------|------------|

| Lecture | 12 | 40% | ⚠️ Too high if > 40% |

| Workshop | 8 | 27% | ✅ Good |

| Discussion | 4 | 13% | ✅ OK |

| Project | 3 | 10% | ✅ Good |

| Assessment | 3 | 10% | ✅ Good |



**Red flags:**



- ⚠️ Lecture > 40% → Course is too passive

- ⚠️ Workshop < 20% → Not enough practice

- ⚠️ Assessment < 5% → Not enough feedback loops



### Check 5: Persona Balance



For each persona, check their experience across the course:



```markdown

### Beginner Persona: [Name]

- Sessions where they might struggle: [list]

- Sessions where they'll feel confident: [list]

- Overall: ✅ Balanced / ⚠️ Too hard / ⚠️ Too easy



### Advanced Persona: [Name]

- Sessions where they might be bored: [list]

- Sessions where they'll be challenged: [list]

- Overall: ✅ Balanced / ⚠️ Under-challenged / ⚠️ Frustrated

```



### Check 6: Assessment Coverage



| Outcome | Assessment Type | Session | Format |

|---------|----------------|---------|--------|

| Outcome 1 | Project | S5 | Individual |

| Outcome 2 | Quiz | S4 | Written |

| Outcome 3 | Presentation | S6 | Group |

| Outcome 4 | ❌ MISSING | — | — |



**Every outcome must be assessed.** No exceptions.



### Check 7: Coherence Test



Answer these questions:



1. Can you explain the course in one sentence?

2. Does every session advance that sentence?

3. If you removed any session, would students miss a critical step?

4. Does the final session/assessment prove the one-sentence promise?



If any answer is "no," the curriculum needs adjustment.



---



## Output: Alignment Report



```markdown

# Alignment Report: [Course Name]



## Overall Score: [X/7 checks passed]



### ✅ Passed Checks

- [List]



### ⚠️ Issues Found

1. [Issue]: [Description] → [Recommended fix]

2. [Issue]: [Description] → [Recommended fix]



### Action Items

- [ ] [Specific fix with session/outcome reference]

- [ ] [Specific fix]

```



---



## When to Run This Check



- ✅ After completing all session designs (full review)

- ✅ After modifying any session (targeted review)

- ✅ Before teaching the course (final validation)

- ✅ After teaching, using student feedback (iterative improvement)



## Cross-References



- Issues with course structure → Back to `planning-courses`

- Issues with specific sessions → Back to `designing-classes`

