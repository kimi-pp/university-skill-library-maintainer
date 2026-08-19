---
name: prompt-architect
description: >
  A meta-prompting skill that interviews the user and then generates a high-quality,
  ready-to-use prompt based on their use case. MANDATORY TRIGGER: this skill fires
  whenever the user mentions "prompt-architect" by name (e.g. "leverage on prompt-architect",
  "use prompt-architect", "run prompt-architect", "activate prompt-architect",
  "with prompt-architect"). Also trigger on: "write a prompt", "build a system prompt",
  "help me prompt", "create a prompt for", "draft a prompt", "design an agent prompt",
  "I need a good prompt for X". Trigger when iterating on an existing prompt or when
  describing an AI agent to build. Covers all of Koo's domains: commodity/energy intelligence,
  sales & client outreach, financial analysis, AI agent/product development (Elephant Gin).
  Always conduct the interview BEFORE generating.
---

# Prompt Architect

A structured meta-prompting skill that interviews the user to understand intent, then
generates a production-quality prompt using best practices from modern prompt engineering.

> **Core philosophy:** Advanced models do not need to be told *how* to work harder.
> They need to be told *what "done right" looks like.* Adding filler words like
> "be careful", "be comprehensive", "be thorough" is the #1 prompt failure mode —
> it lengthens the prompt without adding signal. Every prompt built by this skill
> must define success criteria, not effort instructions.

---

## MANDATORY GATE: Prompt Intent Framework

**This is a hard checkpoint. It runs before any interview or generation.**

Before proceeding, check whether the user's request — in whatever natural language form
they used — contains enough signal to satisfy all four parameters below.

Map their words to these four dimensions. If any are absent or too vague, HALT and ask
the user to fill the gap. Do not accept generic modifiers as substitutes.

### The Four Required Parameters

| # | Parameter | What to check for | What to reject |
|---|---|---|---|
| 1 | **Task Objective** | Specific, bounded goal — what exactly must be produced? | "help me with X", "do something about Y" |
| 2 | **Target Audience** | Who reads or acts on this output? Role, expertise level, context | "general audience", "anyone" |
| 3 | **Success Criteria** | What does a *correct, good* output look like? Describe the standard, not the method | "be comprehensive", "be accurate", "be careful" |
| 4 | **Constraints & Errors** | Specific boundaries, formats, or anti-patterns to avoid | "don't make mistakes", "don't be wrong" |

> **Critical rule on Success Criteria:** Do not accept instructions about *how* the model
> should work (effort, care, thoroughness). Force the user to define the *standard of the
> output itself* — the scenario, the reader, the judgment call. A good success criterion
> gives the model a scene and a bar, not a behavioural directive.
>
> ❌ Weak: "Be comprehensive and careful with the analysis"
> ✅ Strong: "A senior LNG trader reading this should be able to make a cargo decision
>    without needing to look up any additional data"

If all four are present (explicitly or clearly implied), proceed directly to Step 1.
If any are missing, ask once — clearly and specifically — before continuing.

---

## Core Workflow

### Step 1: Determine Prompt Type

After the gate clears, identify which type of prompt is needed:

| Type | Signals | Template to use |
|---|---|---|
| **System Prompt** (AI agent) | "system prompt", "agent", "assistant that…", "build a bot", "MCP", "tool" | → `references/system-prompt-template.md` |
| **Task Prompt** (one-off) | "write me a prompt to…", "research", "analyse", "summarise", "draft" | → `references/task-prompt-template.md` |

If unclear, ask: *"Is this for an AI agent's system prompt, or a one-off task prompt?"*

Also detect intent mode:
- **Creating new** → proceed to Step 2 Interview
- **Iterating / debugging** → run Step 1b Diagnosis FIRST, then Step 2

---

### Step 1b: Diagnosis (for iteration only)

If the user is fixing or improving an existing prompt, run the **Failure Mode Diagnostic**
before interviewing. Ask:

> "What's going wrong with the current prompt? Describe the symptom."

Then map their answer to the fix:

| Symptom | Root Cause | Fix |
|---|---|---|
| Output is too vague or generic | Under-specified role or context | Add domain grounding + specific entities |
| Output ignores key constraints | Constraints buried or implicit | Move constraints to explicit NEVER/ALWAYS block |
| Output format is inconsistent | No format spec | Add XML structure or schema + prefill |
| Output is too long / verbose | No length constraint | Add "Limit to X sentences/words" instruction |
| Model hallucinates facts | No grounding instruction | Add "Cite your source" or RAG instruction |
| Model misses the point on complex tasks | No reasoning instruction | Add CoT: "Think step by step before answering" |
| Structured output breaks (bad JSON, etc.) | No enforcement + no prefill | Add prefill + schema instruction |
| Inconsistent outputs across runs | Ambiguous success criteria | Add few-shot examples + define what "good" looks like |
| Self-review catches nothing | Model reviewing its own output | Switch to cross-model review (see Step 3b) |

After diagnosis, proceed to Step 2 — but now you know which dimensions need targeted work.

---

### Step 2: The Interview

Run the interview for the appropriate prompt type. Ask **all questions in a single message**
— do not ask one at a time. Keep the tone conversational but efficient.

The four Prompt Intent Framework parameters should already be known from the gate check.
The interview deepens them — do not re-ask what is already confirmed.

#### For SYSTEM PROMPTS (AI agents):

1. **Role & persona** — What is this agent's job? What should it sound like (tone, expertise level, formality)?
2. **Primary tasks** — What are the 2–4 main things this agent needs to do?
3. **Context & domain** — What domain/industry does it operate in? Any specific data sources, tools, or integrations?
4. **Inputs & outputs** — What does the agent receive as input? What should its outputs look like (format, length, structure)?
5. **Constraints & guardrails** — What should it never do? Any tone, scope, or compliance boundaries?
6. **Reasoning style** — Should it think step-by-step out loud (Chain-of-Thought), or deliver clean answers? Does it need to cite sources?
7. **Pipeline / downstream use?** — Will outputs be parsed by code, fed into another agent, or stored in a database? *(triggers XML + prefill decision)*
8. **Cross-model pipeline?** — Will this prompt operate inside a multi-agent workflow (e.g., Producer → Reviewer → Human)? *(triggers pipeline SOP section)*
9. **Examples** — Can you give one example of an ideal input → output pair? (optional but very helpful)

#### For TASK PROMPTS (one-off):

1. **Goal** — What do you want the AI to produce at the end?
2. **Context** — What background does the AI need to know? (topic, company, market, data)
3. **Audience** — Who will read or use the output? (carries over from gate if specified)
4. **Output format** — How structured does the result need to be? (bullets, prose, table, JSON, etc.)
5. **Constraints** — Length limits? Tone? Things to avoid?
6. **Complexity** — Is this straightforward, or does it require multi-step reasoning, comparisons, or synthesis across sources?
7. **Downstream use?** — Will this output feed into another step, get parsed, or land in a UI? *(triggers XML + prefill decision)*

---

### Step 3: Select Technique(s)

Based on interview answers, choose the right technique(s) from this decision tree:

```
Is the task complex / multi-step?
  YES → Use Chain-of-Thought (CoT): "Think step by step..."
    Does it need verification?
      YES → Add Self-Consistency: ask for multiple reasoning paths
      NO  → CoT alone is fine

Does the agent need to use tools / APIs?
  YES → Use ReAct pattern: [Thought → Action → Observation] loop

Are there known good examples of the output?
  YES → Add Few-Shot examples (2–4 input/output pairs)
  NO  → Zero-shot is fine if role + context are well-specified

Is the task long / multi-phase?
  YES → Split into Prompt Chain: break into sub-prompts with handoffs

Will the output be parsed by code, fed into another agent, or stored?
  YES → Use XML Structuring: wrap sections in semantic tags
        e.g. <context>, <analysis>, <output>, <citations>
        ALSO add Prefill: begin Claude's response with the opening tag
        e.g. prefill with `<output>` or `{` to enforce format from the start

Is the output highly structured (JSON, tables, citations)?
  YES → Specify schema explicitly + add format enforcement instruction
        + use Prefill to anchor the response format

Is this a high-stakes, reused, or production prompt?
  YES → Include cross-model pipeline SOP (see Step 3b)
```

---

### Step 3b: Cross-Model Pipeline Design (for high-stakes prompts)

Advanced models exhibit high self-bias. A model asked to review its own output
will miss errors it made, the same way a student cannot reliably grade their own paper.
For any production-grade, high-stakes, or reused prompt, recommend — and embed — a
cross-model review structure in the generated output.

**When to recommend this:**
- System prompts for agents that will run autonomously
- Prompts used inside multi-step pipelines (e.g., LNG Dashboard, CarbonIQ)
- Prompts generating outputs that feed code, UI, or external stakeholders
- Any prompt where "wrong" has a meaningful cost

**The three-stage pipeline to embed:**

```
Stage 1 — PRODUCER (primary generation)
  → Assign to strongest reasoning model for the task type:
      • Deep knowledge, architecture, multi-step → Claude Opus / Sonnet
      • Web research, scraping, data retrieval  → GPT-4o / Gemini Pro

Stage 2 — REVIEWER (cross-model audit)
  → Route output to a DIFFERENT model family
  → Reviewer command (embed this verbatim):
      "Act as a strict auditor. Review this output against the original
       Success Criteria and Constraints provided. Identify: logical flaws,
       missing edge cases, hallucinations, unfulfilled requirements.
       Do not rewrite. Flag only. Be specific about each failure."
  → Cap revision loop at TWO iterations maximum.
    (Two rounds catch the major issues; further rounds show diminishing returns.)

Stage 3 — HUMAN FINAL PASS
  → Deliver finalized output + audit log to the user for final decision
  → Model never makes final delivery decisions autonomously
```

**Model Routing Reference:**

| Task Type | Recommended Model | Rationale |
|---|---|---|
| Deep coding, architecture, long-context synthesis | Claude Opus / Sonnet | Strongest on structured reasoning |
| Web research, data scraping, terminal execution | GPT-4o / Gemini Pro | Strong at retrieval and execution |
| Knowledge doc integration, multi-source synthesis | Claude Opus / Sonnet | Context handling strength |
| Cross-model review / audit | Opposite family from producer | Eliminates self-review bias |

**Guardrails to embed in pipeline prompts:**
- No model reviews its own output for final delivery
- If a parameter is unspecified, the model returns a gap flag — it does not invent
- Revision loop hard cap: 2 iterations maximum

---

### Step 4: Generate the Prompt

Read the appropriate template file before generating:

- **System prompts** → read `references/system-prompt-template.md`
- **Task prompts** → read `references/task-prompt-template.md`

Produce the final prompt inside a clearly labeled code block so it can be copied directly.
The generated prompt **must always include an explicit Success Criteria section** — this
is non-negotiable regardless of prompt type. If the user's gate answers implied the criteria
but did not state it cleanly, crystallize and embed it.

Then append a **brief technique note** (2–3 lines max) explaining what techniques were
used and why.

Format:

```
---
🧠 GENERATED PROMPT
---

[prompt goes here — fully ready to use]

---
⚙️ TECHNIQUES USED
---
[2–3 line note]

---
✅ SUCCESS CRITERIA EMBEDDED
---
[Restate exactly what "correct output" means for this prompt — 2–4 lines]
```

If Step 3b applies, append:

```
---
🔁 CROSS-MODEL PIPELINE
---
Stage 1 — Producer: [recommended model + rationale]
Stage 2 — Reviewer: [different model family + audit command]
Stage 3 — Human Final Pass
Max review iterations: 2
```

---

### Step 4b: Define Eval Test Cases

After delivering the prompt, always offer a mini eval set. Propose 3 test cases.
Each test case must include a Pass/Fail criterion anchored to the Success Criteria —
not a subjective description of quality:

```
---
🧪 SUGGESTED TEST CASES
---

Test 1 — Typical input: [most common expected input]
✅ Pass if: [specific output standard from success criteria]
❌ Fail if: [concrete failure mode — what wrong looks like]

Test 2 — Edge case: [unusual but valid input]
✅ Pass if: [what should the model do differently here?]
❌ Fail if: [what would break the downstream use or audience trust?]

Test 3 — Adversarial: [input designed to break format or scope]
✅ Pass if: [model handles gracefully without hallucinating or ignoring constraints]
❌ Fail if: [model invents details, ignores constraints, or produces unusable output]
```

This step is especially important for:
- Agent system prompts (Petronas LNG dashboard, CarbonIQ pipeline)
- Prompts that feed downstream parsers or UIs
- Any prompt you plan to reuse across many inputs

---

### Step 5: Offer to Iterate

After delivering the prompt, test cases, and pipeline recommendation, always offer:

> "Want me to adjust the tone, add few-shot examples, run the diagnosis on a specific
> failure, sharpen the success criteria, or build out the cross-model review prompt?"

---

## XML Structuring Reference

When outputs need to be parsed, piped into agents, or consistently structured, XML tags
are Claude's most reliable formatting tool. Use these patterns:

### For structured analysis outputs:
```xml
<analysis>
  <summary>[2–3 sentence synthesis]</summary>
  <key_findings>
    <finding>[Finding 1]</finding>
    <finding>[Finding 2]</finding>
  </key_findings>
  <recommendation>[Action or conclusion]</recommendation>
</analysis>
```

### For citation-traced outputs (CarbonIQ, research agents):
```xml
<output>
  <claim>[Extracted or synthesised claim]</claim>
  <source tier="1">[Direct document citation]</source>
  <confidence>high | medium | low</confidence>
</output>
```

### For LNG / commodity intelligence agents:
```xml
<market_brief>
  <supply>[Supply dynamics]</supply>
  <demand>[Demand signals]</demand>
  <geopolitical>[Risk factors]</geopolitical>
  <price_direction>[Directional view]</price_direction>
</market_brief>
```

### For cross-model review audit outputs:
```xml
<audit>
  <flag id="1">
    <type>logical_flaw | hallucination | missing_requirement | edge_case</type>
    <description>[Specific issue found]</description>
    <original_requirement>[The success criterion it violates]</original_requirement>
  </flag>
</audit>
```

### Prefill instruction (add to end of prompt):
```
Begin your response with: <output>
```
Or for JSON:
```
Begin your response with: {
```
This prevents Claude from adding preamble and anchors the format from token 1.

---

## Domain-Specific Context

When generating prompts for Koo's use cases, apply this background automatically:

**Commodity / Energy Intelligence**
- Relevant entities: Trafigura, Vitol, TotalEnergies, Petronas, ADNOC, Aramco, Petrobras
- Relevant data: LNG, crude benchmarks, energy transition, chemicals, APAC demand
- S&P Global AIRD, Platts pricing, Commodity Insights platform context

**Sales & Client Outreach (S&P Global)**
- Role: Client Development Director, APAC enterprise accounts
- Clients: trading firms, NOCs, chemical/industrial accounts
- Tone: senior, peer-to-peer, value-led — never salesy
- Products: Commodity Insights, AIRD, Databricks integrations

**Financial Analysis & Portfolio**
- Wu Family Portfolio context; Ireland-domiciled UCITS ETFs, BDCs, SRS, CPF
- Safe withdrawal rates, CAPE analysis, Bitcoin position, Trion KL rental property
- Horizon: financial independence target ~2031–2032

**AI Agent / Product Development (Elephant Gin)**
- Building AI applications for commodity/energy markets
- Orchestration-first approach: Koo as "director", agents as executors
- Tools: Claude, MCP servers, Databricks, GitHub master-rules repo
- Products: CarbonIQ Agent, SRS/CPF optimizer, Singapore property intelligence agent
- Downstream parsing is common — default to XML structuring + prefill for agent outputs
- Cross-model pipeline SOP applies to all production agent prompts by default
