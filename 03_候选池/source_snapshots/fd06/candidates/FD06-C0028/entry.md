---

name: planning-courses

description: Top-down course architecture from outcomes to modules. Use when designing a new course or restructuring an existing one.

---



# Course Planning Skill



## Triggering Contexts



- User wants to create a new course from scratch

- User feels an existing course is drifting or inconsistent

- User needs to restructure a curriculum

- User asks "what should this course cover?"



## Core Principle



> **Outcomes first, topics second.**

> Never start with "what should we teach?" Always start with "what should students be able to DO?"



---



## Workflow



### Step 1: Define Course Identity



Ask for and document:



```markdown

## Course Identity

- **Course Name:**

- **Duration:** (weeks, total hours, # sessions)

- **Format:** (lecture / workshop / hybrid / online / project-based)

- **Domain:** (e.g., investing, Bitcoin, programming)

- **One-line promise:** "After this course, students will be able to ____"

```



### Step 2: Define Observable Outcomes



Outcomes must be **observable and measurable**, not vague.



| ❌ Vague | ✅ Observable |

|----------|--------------|

| "Understand technical analysis" | "Build a complete trading system using 3+ indicators" |

| "Learn about Bitcoin" | "Explain Bitcoin's monetary properties to a skeptic" |

| "Know risk management" | "Calculate position size given account size and stop loss" |



**Rule: Use action verbs.** Build, Calculate, Design, Evaluate, Compare, Demonstrate, Explain, Create.



Ask the user to define **3-5 core outcomes**. Fewer is better.



### Step 3: Create Student Personas



Define 2-3 student profiles that represent the audience:



```markdown

### Persona: [Name]

- **Background:** What they already know

- **Goal:** Why they're taking this course

- **Challenge:** What will be hardest for them

- **Success looks like:** What makes the course worth it for them

```



**Why this matters:** Every design decision should be checked against these personas. "Would Beginner Ben understand this? Would Advanced Amy be bored?"



### Step 4: Map Modules to Outcomes



Create a **module-outcome matrix**:



| Module | Outcome 1 | Outcome 2 | Outcome 3 | Outcome 4 |

|--------|-----------|-----------|-----------|-----------|

| Module 1: Foundations | ✅ Intro | ✅ Intro | | |

| Module 2: Core Skills | ✅ Build | | ✅ Intro | |

| Module 3: Application | | ✅ Build | ✅ Build | ✅ Intro |

| Module 4: Mastery | ✅ Assess | ✅ Assess | ✅ Build | ✅ Assess |



**Every outcome must appear at least twice:** once for learning, once for assessment.

**Every module must serve at least one outcome.** Modules with no outcomes get cut.



### Step 5: Sequence Modules



Check the sequence with these questions:



1. Does each module build on the previous one?

2. Are prerequisites taught before they're needed?

3. Is there a logical arc? (Foundation → Skill building → Application → Mastery)

4. Is the difficulty curve progressive, not flat or spiking?



### Step 6: Design Assessment Strategy



Map assessments to outcomes:



| Outcome | Assessment Type | When |

|---------|----------------|------|

| "Build a trading system" | Project | Module 4 |

| "Calculate position size" | Quiz / Exercise | Module 2 |

| "Explain to a skeptic" | Presentation | Module 3 |



**Rule:** Every outcome must have at least one assessment. If you can't assess it, it's not a real outcome.



---



## Output: Course Blueprint



The final deliverable is a `course-blueprint.md`:



```markdown

# [Course Name] Blueprint



## Course Identity

[From Step 1]



## Outcomes

1. [Observable outcome]

2. [Observable outcome]

3. [Observable outcome]



## Student Personas

[From Step 3]



## Module Structure

[Module-outcome matrix from Step 4]



### Module 1: [Name]

- **Sessions:** [N]

- **Outcomes served:** [list]

- **Key topics:** [brief]

- **Format mix:** [lecture %, workshop %, project %]



### Module 2: [Name]

...



## Assessment Map

[From Step 6]



## Prerequisite Chain

[Which modules depend on which]

```



---



## Red Flags to Call Out



- ⚠️ **Orphan topic:** Content that doesn't serve any outcome → Cut it

- ⚠️ **Unassessed outcome:** Outcome with no assessment → Add one

- ⚠️ **Persona neglect:** All content targets one persona → Rebalance

- ⚠️ **Front-loaded theory:** First 3+ sessions are all lecture → Add early hands-on

- ⚠️ **Missing prerequisites:** Module requires knowledge not taught yet → Resequence



## Cross-References



- After blueprint is done → Use `designing-classes` for each session

- After all sessions designed → Use `aligning-curriculum` to check consistency

