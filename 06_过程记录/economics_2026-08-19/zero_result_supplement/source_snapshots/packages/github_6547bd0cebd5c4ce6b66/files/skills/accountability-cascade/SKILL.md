---
name: accountability-cascade
description: Default prose style for all writing in this project. Traces how specific actors — corporations, regulators, physical systems, communities — make decisions that create consequences for the next actor in the chain. Applies chain-of-causation structure, named actors with active verbs, and the cascade reveal. Use for any section: capital flows, grid infrastructure, labor markets, utility regulation, material constraints, or environmental consequences. The style works for human actors and non-human constraints alike.
argument-hint: "[section to write or improve, or description of the chain being traced]"
---

# Accountability Cascade Narrative

The default prose style for this project. Traces how specific actors — corporations, regulators, physical systems, workers, communities — make decisions or impose constraints that create consequences for the next actor in the chain. Works equally for human choices (a hyperscaler signs a lease) and physical constraints (a transformer takes 18 months to manufacture). Named for two defining features: **accountability** (assigns agency, names the actor, reveals mechanism) and **cascade** (consequences travel through a chain, each step further from the original decision and closer to permanent exposure).

This style is the prose equivalent of a causal loop diagram. Every sentence names an actor, shows an action, and implies a consequence. Together they build the same picture as a systems dynamics model — but in language a non-specialist can follow.

## Practitioners to Study

| Writer | Work | What to learn |
|:---|:---|:---|
| Michael Lewis | *The Big Short*, *Flash Boys* | Character-driven mechanism — complex financial engineering explained through the specific choices of specific people |
| Bethany McLean | *The Smartest Guys in the Room* | Complicity through documents — revealed not by claiming bad intent but by showing what each party actually signed, approved, and accepted |
| Jesse Eisinger / ProPublica | *The Chickenshit Club*, investigative filings | Institutional indictment through the paper trail — "something someone, somewhere doesn't want you to know" |
| Matt Taibbi | Rolling Stone financial crisis coverage | Named actors, strong verbs, no euphemism — refusal to let institutions hide behind passive constructions |

---

## The Six Core Techniques

### 1. Named Actors + Active Verbs

The grammar assigns responsibility. The reader must always know who did what.

**Do not:**
> Short-term leases were signed, classifying the payments as operating expense.

**Do:**
> Microsoft and Meta are signing short-term leases, booking the payments as operating expense.

Every sentence should answer: who did this, and to what effect?

---

### 2. Chain of Causation

Each sentence advances the mechanism one step and creates the constraint for the next actor. The reader follows consequences as they travel outward. No sentence is self-contained — each one hands off to the next.

**Pattern:**
> [Actor A] [verb] [action that creates the constraint for B].
> [Actor B] [verb] [action], because [why B accepted A's terms].
> [Actor B's action] reaches [Actor C], who [verb] [outcome].
> [Actor D] now holds [the permanent consequence].

The reader should feel the mechanism clicking into place, not just observe a list of facts.

---

### 3. The Cascade Reveal

Sequence actors from most powerful / closest to the decision → most powerless / furthest from it. The final actor in the chain — the one with the least visibility and the most permanent exposure — appears last. The structural position of that sentence does the moral work. You do not need to editorialize.

**Closing contrast (the cascade's end):**
> The entities who made the forecast can exit. The entities who financed the physical asset cannot.

Two sentences. No adjectives. The contrast between "can exit" and "cannot" is the argument.

---

### 4. Complicity Without Innocence

Middlemen are not passive conduits. They are willing participants who accepted unfavorable terms because they needed the upstream relationship. This is the most important distinction between accountability cascade narrative and standard explanatory journalism: the intermediaries knew, and chose anyway.

**Do not:**
> The neocloud borrowed against projected renewals.

**Do:**
> The neoclouds who build against those leases know the terms and accept them anyway, because the alternative is no hyperscaler contract at all.

The phrase "know the terms and accept them anyway" does the work. It removes the possibility of innocent error without making a claim about motives.

---

### 5. Evidence Over Assertion

Build the argument from what parties did — what they signed, borrowed, packaged, sold, granted — not from claims about their character or intentions. The reader draws the moral conclusion; the writer provides the evidence trail.

**Do not:**
> Meta found a way to avoid long-term liability by exploiting off-balance-sheet structures.

**Do:**
> Meta agreed to "rent" the facility through a series of 10-year leases, classifying the arrangement as operating cost rather than debt.

The facts indict. The writer does not need to.

---

### 6. Designed, Not Emergent

Frame structural outcomes as the product of deliberate choices, not drift or accident. This is what separates accountability narrative from explanatory journalism. Explanatory journalism says "this is how the system works." Accountability narrative says "someone designed it this way."

**Do not:**
> Risk ended up concentrated among pension funds and rural communities.

**Do:**
> The hyperscalers build without owning. They are signing short-term leases, booking the payments as operating expense, and setting themselves up to walk away when the contract ends.

The present continuous tense ("are signing", "are setting themselves up") signals ongoing, deliberate behavior — not a historical accident.

---

## Structural Template

```
[Opening: name the powerful actor and their deliberate structural choice]
[Their choice transfers the constraint to the next party]
[That party accepts because they need the upstream relationship]
[They pass the exposure further — how and to whom]
[The next party received something that sounds like an asset]
[The final party holds permanent exposure from a decision they never saw]

[Two-sentence close: the stark contrast between who chose and who pays]
```

---

## Anti-Patterns

| Pattern | Problem | Fix |
|:---|:---|:---|
| Em-dash as clause splice | Connects two things that should be separated | Use a period. One em-dash per paragraph maximum, only for genuine parentheticals. |
| Passive voice | Hides the actor | Name who did it: "leases were signed" → "Microsoft signed leases" |
| "Not X, but Y" opener | Delays the point | Start with Y |
| Three-item lists | Creates enumeration feeling | Restructure as sentences with causal connectors |
| Motive claims | Unprovable, invites rebuttal | Show what they did; let the reader conclude |
| "It is worth noting / notably / moreover" | Throat-clearing | Cut entirely; start the sentence with the substance |
| Describing what a chart shows | Wastes a sentence the reader already read | Interpret and move on: "This means..." not "As the chart shows..." |
| Tense inconsistency | Loses the distinction between ongoing design and historical consequence | Present continuous for current deliberate behavior; simple past for downstream consequences that are already locked in |

---

## Plain Language

This project is read by people who are not insiders. Every piece of jargon — every financial abbreviation, energy-industry acronym, or insider shorthand — is a small tax on the reader. Enough taxes and they stop reading.

Plain language is not dumbing down. It is precision applied to the reader's context rather than the author's. A specialist can read "infrastructure spending" just as easily as "capex." The generalist can only read one of them.

**Rules:**
1. **Spell out abbreviations on first use, always.** Even common ones: "Amazon Web Services (AWS)", "Lawrence Berkeley National Laboratory (LBNL)", "Federal Energy Regulatory Commission (FERC)". Define it once, then use the short form freely.
2. **Replace insider terms with plain equivalents.** Use the short form only after the reader has been given it.
3. **Name the things.** "Data center companies — CoreWeave, Nebius, Nscale" is more grounded than "neoclouds". Institutions are more credible when named than when labeled.

**Term replacements — default to the plain column:**

| Insider term | Plain equivalent |
|:---|:---|
| capex / capital expenditure | infrastructure spending |
| hyperscaler | major cloud company (first use: "Amazon, Google, Microsoft, Meta") |
| neocloud | data center company (name them: CoreWeave, Nebius, Nscale) |
| guidance / guiding to | spending forecast / plans to spend |
| SPV / special purpose vehicle | shell company |
| off-balance-sheet | off-the-books |
| interconnection queue | grid connection waiting list |
| commercial operation | full operation / coming online |
| energization | live power connection |
| dispatchable power | on-demand power |
| 10-K (first use) | annual report |
| S-1 (first use) | IPO prospectus |
| GW (first use) | gigawatts (GW) |
| AEP | American Electric Power |
| LBNL | Lawrence Berkeley National Laboratory |
| FERC | Federal Energy Regulatory Commission (FERC) |

**Test:** Read the sentence aloud to someone outside the industry. If they would pause at a word, replace it.

---

## Connection to This Project

This project's analytical arc — COMMIT → CONVERT → LAND → DISTRIBUTE — maps directly onto the cascade structure. Every deep dive is the same question asked at a different stage: who made this decision, and who bears the consequence?

| Deep dive | The chain being traced |
|:---|:---|
| DD-001 Capital Reality | Hyperscalers commit capital → neoclouds build assets → bondholders hold exposure → communities absorb permanent load |
| DD-002 Grid Modernization | Generators interconnect → ISOs queue them → utilities upgrade transmission → ratepayers fund the grid or bypass it |
| DD-003 Labor Markets | AI capital flows → hiring concentrates in specific occupations and geographies → displaced workers in adjacent roles have no exit |
| DD-004 Utility Regulation | Data centers trigger load additions → utilities file for cost recovery → regulators classify costs → ratepayers or developers pay |

**Human actors and physical constraints use the same structure.** A transformer backlog is still a chain: manufacturers face a 3-year order queue → utilities cannot energize new substations → data center projects stall → the capital commitment does not convert to operating capacity. The actor is a physical bottleneck, not a corporation, but the sentence structure is identical.

Writing that traces this arc should feel like following a paper trail or a causal loop diagram in prose form. Every claim is anchored to a specific action — a lease signed, a bond sold, a tax incentive granted, a queue position held — not to a structural abstraction.

The governing question for every paragraph: **who did this, to whom, and what does that actor now have no choice but to do?**
