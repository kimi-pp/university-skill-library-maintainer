---
name: write-to-publish
description: >
  A 3-step pipeline for writing complete books, reports, and long-form documents with consistency and quality: (1) deep interview to understand the vision, (2) build a comprehensive "bible" â the source-of-truth document covering structure, characters, themes, style rules, and chapter outline, (3) produce chapter-by-chapter writing scripts with built-in consistency checks. Use this skill whenever the user wants to write a book, novel, ebook, clinical report, literature review, case study, long-form guide, training manual, or any multi-chapter document. Trigger on phrases like "write a book", "help me with my novel", "I have a story idea", "write a report", "clinical literature review", "build out this manuscript", "chapter by chapter", or "long-form writing project". Also trigger for fixes and revisions â "rewrite chapter 3", "fix the plot hole", "the ending doesn't work", "add a new character."
---

# Write-to-Publish: The Long-Form Writing Pipeline

You are guiding the user through a proven 3-step process for producing complete, consistent, high-quality long-form documents. This process is called the "Genie Method" â instead of the user burning their wishes on vague asks, the system front-loads all the thinking into a bible/blueprint, then writes methodically chapter by chapter against that source of truth.

This is the same structural approach as building software with spec-to-scripts, adapted for writing. The bible IS the spec. The chapter scripts ARE the modules. The smoke tests ARE consistency checks. The principle is identical: separate thinking from writing, and never let the AI improvise decisions that should have been made upfront.

The three steps are:
1. **Interview** â Understand the vision, story, audience, and goals deeply
2. **The Bible** â A comprehensive source-of-truth document (story bible for fiction, project bible for nonfiction) that locks in every decision before writing begins
3. **Chapter-by-Chapter Scripts** â Verbatim prompts that produce each chapter, with consistency checks after each one

Why this works: AI writes great individual chapters. What it can't do reliably is maintain consistency across a whole book â character details drift, themes get lost, plot threads get dropped. The bible solves this by giving every chapter the same source of truth. And the consistency checks after each chapter catch drift before it compounds.

---

## Step 1: The Interview

Before building the bible, deeply understand what the user wants to create. Adapt your questions based on whether this is fiction or nonfiction.

### For Fiction (Books, Novels, Short Stories)

**The Core**
- What's the story about in 2-3 sentences? (The elevator pitch)
- What genre? (Thriller, romance, sci-fi, literary, YA, children's, etc.)
- What's the tone? (Dark and gritty, lighthearted, suspenseful, lyrical, humorous)
- Who's the target reader? (Age range, what other books do they read)

**Story Architecture**
- Who are the main characters? (Names, ages, key traits, relationships)
- What's the central conflict?
- Do you know how it ends? (Even a rough idea helps enormously)
- What's the setting? (Time period, locations, world rules if speculative)
- Are there plot twists or reveals you have in mind?
- How long should it be? (Number of chapters, approximate word count)

**Style**
- First person or third person? Past tense or present?
- Any authors whose style you admire or want to emulate?
- Any topics or content to include or avoid?

**What Exists Already**
- Have you written any of it? (Outline, chapters, notes)
- Is this based on real events or people?
- Are there reference materials? (Research, photos, maps, timelines)

### For Nonfiction (Reports, Literature Reviews, Guides, Case Studies)

**The Core**
- What is this document? (Clinical report, literature review, business guide, training manual, etc.)
- Who reads it? (Insurance adjusters, patients, students, colleagues, general public)
- What's the goal? (Persuade, educate, document, sell)
- What's the required or ideal length?

**Content**
- What are the main topics/sections?
- What evidence, data, or sources should be included?
- Are there specific claims or conclusions to support?
- Any regulatory or formatting requirements? (APA, AMA, legal standards)

**Tone & Style**
- Formal or conversational?
- Technical or accessible?
- Are there existing documents in this style to reference?

### Interview Tips

- If the user has a rough idea but not details, help them develop it. Ask "what if" questions. Propose options.
- If they uploaded reference material (outlines, notes, prior drafts), read those first and pull context from them before asking questions.
- For fiction: push on the ending. An unclear ending leads to a wandering middle. Even "I think she discovers the truth and forgives him" is enough to aim toward.
- For nonfiction: push on the audience. A literature review for insurance adjusters reads completely differently than one for clinicians.
- Don't let scope run wild. A 50-chapter epic is a different project than a 12-chapter novella. Help them scope to something completable.

---

## Step 2: The Bible

The bible is the source-of-truth document that every chapter is written against. It's the single most important output of this process â a bad bible produces an inconsistent book, no matter how good the individual chapters are.

Save this as a `.md` file (or `.docx` using the docx skill if the user prefers a formatted document).

### Fiction Bible Structure

```
# [Title] â Story Bible

## Premise
One paragraph. What is this book about? What's the hook?

## Genre & Tone
Genre, subgenre, tone, comparable titles ("X meets Y").
Reading level and target audience.

## Point of View & Tense
POV (first person, third limited, third omniscient, alternating).
Tense (past, present).
If alternating POV: whose chapters and in what pattern.

## Setting
Time period. Primary locations with brief descriptions.
World rules (if speculative/fantasy/sci-fi).
Sensory palette â what does this world feel, smell, sound like?

## Characters

### [Character Name] â [Role: Protagonist/Antagonist/Supporting]
- Age, appearance (brief, key details only)
- Personality: 3-5 defining traits
- Motivation: what do they want? What do they NEED (which may differ)?
- Arc: how do they change from beginning to end?
- Voice: how do they speak? Verbal tics, vocabulary level, speech patterns
- Key relationships: connection to other characters
- Secret/flaw: the thing that drives conflict or growth

[Repeat for each significant character]

### Character Relationship Map
Brief description of how characters connect â who knows who, who's in conflict with who, alliances and tensions.

## Plot Structure

### Act 1: Setup (Chapters X-Y)
- What's the status quo?
- What's the inciting incident that disrupts it?
- What's the first major decision the protagonist makes?

### Act 2: Confrontation (Chapters X-Y)
- What escalating obstacles does the protagonist face?
- What's the midpoint shift (where the story pivots)?
- What's the "all is lost" moment?

### Act 3: Resolution (Chapters X-Y)
- What's the climax?
- How is the central conflict resolved?
- What's the final image/feeling the reader is left with?

## Chapter Outline

### Prologue (if applicable)
- Scene summary (2-3 sentences)
- POV character
- Purpose: what does this chapter accomplish for the story?
- Key moments/beats

### Chapter 1: [Title]
- Scene summary (2-3 sentences)
- POV character
- Purpose: what does this chapter accomplish?
- Key moments/beats
- Ends with: [the hook/cliffhanger/transition that pulls into next chapter]

[Repeat for every chapter]

### Epilogue (if applicable)
- Scene summary, POV, purpose, key moments

## Themes
The 2-3 big ideas running through the story.
How each theme manifests in the plot and characters.

## Style Guide
- Target word count per chapter (e.g., 2,500-3,500 words)
- Prose style notes (short punchy sentences? Lush descriptions? Dialogue-heavy?)
- Things to ALWAYS do (e.g., "end every chapter on a cliffhanger")
- Things to NEVER do (e.g., "never use the character's full name in dialogue â people don't talk like that")
- Vocabulary or terminology notes (jargon, slang, period-appropriate language)

## Timeline
Chronological sequence of events, including backstory events referenced in the narrative.
Especially important for thrillers, mysteries, and stories with flashbacks.

## Continuity Tracker
This section gets updated as chapters are written:
- What has each character learned/experienced so far?
- What plot threads are open vs. resolved?
- What promises has the narrative made to the reader that must be paid off?
```

### Nonfiction Bible Structure

```
# [Title] â Project Bible

## Purpose & Audience
What is this document? Who reads it? What should they think/feel/do after reading?

## Thesis / Central Argument
The one-sentence claim this document supports.
For literature reviews: the research question.
For reports: the conclusion.

## Tone & Voice
Formal/conversational, technical/accessible, authoritative/exploratory.
Sample sentence showing the target voice.

## Structure Overview
List of all sections/chapters with one-line descriptions.

## Chapter/Section Outline

### Chapter 1: [Title]
- Key points to cover
- Evidence/sources to cite
- How this connects to the next section
- Target length

[Repeat for each chapter/section]

## Source Library
Key sources with brief annotations â what each source contributes.
Organized by topic or chapter.

## Style Guide
- Citation format (APA, AMA, Chicago, none)
- Target word count per section
- Formatting rules (headers, lists, callouts)
- Terminology decisions (e.g., always say "subluxation" not "misalignment")
- Things to include in every section (e.g., "always reference NJ-specific regulations")
- Things to avoid (e.g., "never make claims without citation")

## Continuity Tracker
Updated as sections are written:
- What claims have been established?
- What sources have been cited where?
- What threads need to be connected across sections?
```

### Bible Writing Principles

**The bible is a living document.** It gets updated as chapters are written. If writing chapter 8 reveals that a character needs a different backstory, update the bible FIRST, then check whether earlier chapters need revision. The bible is always the current truth.

**Be specific on character voice.** "Sarcastic" is not enough. "Uses rhetorical questions when nervous, drops contractions when angry, never swears but uses creative PG insults" gives the AI something to actually work with.

**The chapter outline is the backbone.** Each chapter entry should answer: what happens, whose POV, what's the purpose, and how does it end. A chapter without a clear purpose gets cut or merged.

**Lock in the ending early.** For fiction: knowing the ending means every chapter can plant seeds and build toward it. For nonfiction: knowing the conclusion means every section can support it. Writing toward a known destination produces dramatically tighter work than discovering the ending along the way.

---

## Step 3: Chapter-by-Chapter Writing Scripts

Generate a series of verbatim prompts that the user feeds to Claude (in Cowork, Claude Code, or fresh chat sessions) to produce each chapter. Each prompt includes everything Claude needs â the relevant bible context, what's been written so far, and the specific instructions for this chapter.

Save this as a `.md` file.

### Script Structure

```markdown
# [Title] â Chapter-by-Chapter Writing Scripts

Write each chapter in order. After each chapter, run the consistency check.
If changes affect the bible, update the bible FIRST, then check earlier chapters.

---

## Before You Start: Build the Bible

Paste this into your first session:

\```
I'm writing [Title], a [genre/type] about [one-line premise].
Here is the complete story bible / project bible:

[PASTE THE FULL BIBLE HERE]

Read this carefully. This is the source of truth for every chapter.
Confirm you understand the characters, plot structure, themes, and style guide.
Ask me any clarifying questions before we start writing.
\```

---

## Chapter 1: [Title]

**Paste this:**

\```
We're writing [Title]. Here's the bible for reference:
[PASTE RELEVANT BIBLE SECTIONS â character details, chapter 1 outline,
style guide, setting details needed for this chapter]

Write Chapter 1. Here's what this chapter must accomplish:
- [Purpose from the bible]
- [Key moments/beats]
- [POV character and their emotional state entering this chapter]
- [How the chapter ends â the hook into chapter 2]

Style reminders:
- [Key style rules from the bible]
- Target length: [X] words
- [Any chapter-specific instructions]

Do NOT resolve [ongoing tension/mystery]. That pays off in Chapter [X].
Do NOT introduce [character/element] yet. They appear in Chapter [X].
\```

**After the chapter is written, run this consistency check:**

\```
Review Chapter 1 against the bible. Check:
1. Are all character details consistent with the bible? (names, ages, appearance, speech patterns)
2. Does the chapter accomplish its stated purpose?
3. Are there any continuity errors with the established timeline?
4. Does the tone match the style guide?
5. Are there any plot threads opened that aren't in the bible? (Flag them â they may need to be added to the bible or removed from the chapter)
6. Rate the chapter 1-10 for: prose quality, pacing, character voice, contribution to overall story.

If anything is inconsistent, tell me what needs to change.
Update the Continuity Tracker section of the bible with what's now been established.
\```

---

[Repeat for each chapter...]

---

## After All Chapters: Full Manuscript Review

\```
All [N] chapters are complete. Do a full-manuscript review:

1. Read the entire manuscript start to finish.
2. Check for:
   - Character consistency (does anyone change eye color, forget a skill, act out of character?)
   - Plot holes (are all threads resolved? Any promises to the reader left unfulfilled?)
   - Pacing (any chapters that drag or rush?)
   - Theme (do the themes build and pay off?)
   - Timeline (do dates, ages, and sequences of events all add up?)
   - Tone (any chapters that feel like they're from a different book?)
3. List every issue found, organized by severity (critical / minor / nitpick).
4. Suggest specific fixes for each critical issue.
\```
```

### Script Writing Rules

**Always include bible context in every chapter prompt.** Don't assume Claude remembers the bible from a previous session. Each chapter prompt should include the relevant sections â at minimum the character details, the chapter outline entry, and the style guide. For complex stories, include the continuity tracker showing what's been established so far.

**Tell Claude what NOT to reveal yet.** In mysteries, thrillers, or any story with reveals: explicitly state what the reader should NOT know yet at this point. "The reader suspects X but does NOT know Y yet. Do not reveal Y â that's Chapter 14." This prevents AI from unconsciously foreshadowing too heavily or spoiling its own twists.

**Include the chapter's emotional trajectory.** "This chapter starts tense and ends hopeful" or "The reader should feel uneasy throughout â something is wrong but they can't name it." Emotional direction produces better prose than pure plot instructions.

**Run the consistency check after EVERY chapter.** This is the smoke test. It catches drift early. If chapter 5 accidentally gives a character the wrong hair color, you want to know before you write 20 more chapters on that foundation.

**When changes affect the bible, update the bible first.** If writing chapter 10 reveals that the villain's motivation needs to change, don't just patch chapter 10. Update the bible, check which earlier chapters are affected, revise those, then continue forward. The bible is always the current truth. This backward propagation is what keeps a 26-chapter book feeling like one coherent story instead of a patchwork.

**For nonfiction, the consistency check is different.** Instead of character details and plot threads, check: are claims supported by cited sources? Are there contradictions between sections? Does each section build on the previous one? Is the argument getting stronger or wandering?

---

## Handling Revisions and Fixes

When the user wants to revise an existing manuscript (not write from scratch):

### Step 1: Understand the Problem
- What's wrong? (Plot hole, flat character, pacing issue, inconsistency, tone mismatch)
- Which chapters are affected?
- What does "fixed" look like?

### Step 2: Update the Bible
- Modify the bible to reflect the desired change
- Identify every chapter that's affected by the change (this is why the bible exists â you can trace impacts)

### Step 3: Generate Targeted Revision Scripts
- Produce revision prompts only for the affected chapters
- Each prompt includes the UPDATED bible context and specifies exactly what to change
- Run consistency checks after each revision
- Include a final cross-check to make sure the revision didn't create new inconsistencies

---

## Delivering the Output

After completing all three steps, present the user with:

1. **The Bible** â saved as `.md` or `.docx`
2. **The Chapter Scripts** â saved as `.md`
3. **A quick-start summary** explaining:
   - Total chapters and estimated word count
   - Suggested approach (one chapter per session, consistency check after each)
   - Reminder: if you change the bible, check backward before writing forward

If the user wants the full manuscript assembled into a single document after all chapters are written, use the docx skill to produce a formatted `.docx` file with proper chapter headings, page breaks, and typography.
