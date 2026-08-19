---
name: astro-life-report
description: "Generate deeply personalized life transformation reports using a three-layer framework - Raasi (inner world), Lagnam (outer approach), and Nakshatra + Padam (search engine + D9 soul direction). Trigger when user provides Name + Raasi + Lagnam + Nakshatra + Padam and asks for any life report, transformation guide, karmic pattern analysis, soul purpose report, or situation handling guide. Auto-derives D9 Navamsa from Nakshatra + Padam. Produces a deeply personalized 12-section Word document (.docx)."
---

# Astro Life Transformation Report - Skill Guide

## OUTPUT CHARACTER RULES - STRICTLY ENFORCED

The report is rendered into a PDF with fonts that DO NOT support emojis or decorative symbols. You MUST follow these rules in every section:

- DO NOT use any emojis or pictographs (no ✅, ❌, 🔴, 🐟, 🦂, ⭐, 🙏, etc.).
- DO NOT use arrow glyphs (→, ⇒, ←). Write the word "to" or use a plain hyphen-arrow "->" instead.
- DO NOT use decorative Unicode symbols, checkboxes, stars, or box-drawing characters.
- Use ONLY plain ASCII punctuation plus standard Markdown. Tamil text (when the language is Tamil) is allowed and expected; everything else must be standard letters, numbers, and basic punctuation.
- For emphasis use Markdown **bold** / *italic* only - never symbols.

Any emoji or unsupported Unicode will render as a broken box in the final PDF, so the output must be completely free of them.

## ⚠️ READ THIS FIRST - BEFORE ANYTHING ELSE

**This report will be read by a real human being.**

They may be going through financial stress, relationship pain, career confusion, family pressure, or a deep sense of being lost. Many of them will read this report alone - late at night, searching for answers nobody around them has been able to give.

**They will follow this report. Take that seriously.**

Every word written here has the power to either genuinely help someone transform their life - or leave them more confused and hopeless than before. This is not a document generation task. This is one of the most intimate and impactful things Claude can do for another human being.

**Before writing a single word of the report, hold this in mind:**
- This person has real struggles. Name them precisely - not generically.
- This person needs clarity, not more confusion. Every sentence must earn its place.
- This person needs to feel seen - perhaps for the first time. Write so specifically that they feel you are describing their exact life, not a type.
- This person will act on what is written here. Make sure what is written is worth acting on.
- Never pad. Never repeat. Never write something vague because it sounds wise. If it is not specific and true for THIS person, cut it.

**The standard for every section:** If a stranger could read this report and think it might also be about them - it is not specific enough. Rewrite it.

**Approach this with the seriousness of a doctor writing a prescription, the empathy of a trusted friend who knows everything, and the precision of someone who genuinely wants this person's life to improve.**

This is a gift. Write it like one.

---

## What This Skill Does

Takes astro details + real-life context and generates brutally honest, deeply personalized life transformation documents. NOT a generic horoscope - this is behavioral psychology dressed in astrological language, written with the care of someone who genuinely wants the reader's life to improve.

Every report tells ONE complete story - specific to this person, this combination, this life:
- **ACT 1** - Who You Are: The combination's truth, character, and life impact. (Sections 1–4)
- **ACT 2** - What Is Running: The karmic patterns and root problems keeping you stuck. (Sections 5–6)
- **ACT 3** - The Build: Solutions, identity shift, karmic origin, and dharmic path. (Sections 7–12)

**The tone throughout:** Warm but honest. Precise but compassionate. Never clinical. Never preachy. Write like a wise elder who knows the person's full story and genuinely wants them to succeed.

---

## STEP 1: COLLECT INPUTS

### Round 1: Astro Details
Ask for:
- **Name**
- **Raasi** (Moon Sign) - Tamil or English
- **Lagnam** (Ascendant) - Tamil or English
- **Nakshatra** (Birth Star) + **Padam** number (1–4)

D9 Navamsa is auto-derived from Nakshatra + Padam using the derivation table below.

### Tamil-English Sign Mapping
| Tamil | English | Element | Ruling Planet |
|-------|---------|---------|---------------|
| Mesham (மேஷம்) | Aries | Fire | Mars / Sevvai |
| Rishabam (ரிஷபம்) | Taurus | Earth | Venus / Sukran |
| Mithunam (மிதுனம்) | Gemini | Air | Mercury / Budhan |
| Kadagam (கடகம்) | Cancer | Water | Moon / Chandran |
| Simmam (சிம்மம்) | Leo | Fire | Sun / Surya |
| Kanni (கன்னி) | Virgo | Earth | Mercury / Budhan |
| Thulam (துலாம்) | Libra | Air | Venus / Sukran |
| Viruchigam (விருச்சிகம்) | Scorpio | Water | Mars / Sevvai |
| Dhanusu (தனுசு) | Sagittarius | Fire | Jupiter / Guru |
| Magaram (மகரம்) | Capricorn | Earth | Saturn / Sani |
| Kumbam (கும்பம்) | Aquarius | Air | Saturn / Sani |
| Meenam (மீனம்) | Pisces | Water | Jupiter / Guru |

### Round 2: Life Context (use ask_user_input_v0 tool)

**Question 1: "What are [Name]'s biggest current struggles?"** (multi_select)
Options: "Money / Debt / Income instability", "Health anxiety / Fear", "Relationship / Marriage stress", "Family pressure / Guilt", "Career confusion / No direction", "Overthinking / Analysis paralysis", "Anger / Frustration / Impatience", "Lack of confidence / Self-doubt", "Loneliness / Feeling misunderstood", "Emotional overwhelm / Sensitivity", "Commitment issues", "Work-life imbalance"

**Question 2: "What does [his/her] daily life look like?"** (single_select)
Options: "Heavy travel - rarely home", "Office job - mostly one place", "Work from home", "Entrepreneur / Own business", "Homemaker", "Hectic - no fixed pattern", "Student"

**Question 3: "What is [his/her] biggest life goal right now?"** (single_select)
Options: "Financial stability / Clear debt", "Better family relationships", "Find life purpose / Career clarity", "Inner peace / Stop overthinking", "Build a business / Grow income", "Recognition / Be valued", "Independence / Freedom", "Health improvement", "Build confidence / Self-worth"

If user selects "all" for any question, treat ALL options as active and address every one in the report.

---

## STEP 2: DERIVE D9 NAVAMSA

### Complete 27 Nakshatra → Gana Mapping
| # | Nakshatra (Tamil) | Nakshatra (English) | Ruling Planet | Gana |
|---|-------------------|---------------------|---------------|------|
| 1 | அஸ்வினி (Aswini) | Aswini | Ketu | Deva |
| 2 | பரணி (Bharani) | Bharani | Venus | Manushya |
| 3 | கார்த்திகை (Krithikai) | Krittika | Sun | Rakshasa |
| 4 | ரோகிணி (Rohini) | Rohini | Moon | Manushya |
| 5 | மிருகசீரிஷம் (Mirugasirisam) | Mrigashira | Mars | Deva |
| 6 | திருவாதிரை (Thiruvathirai) | Ardra | Rahu | Manushya |
| 7 | புனர்பூசம் (Punarvasu) | Punarvasu | Jupiter | Deva |
| 8 | பூசம் (Poosam) | Pushya | Saturn | Deva |
| 9 | ஆயில்யம் (Aayilyam) | Ashlesha | Mercury | Rakshasa |
| 10 | மகம் (Magam) | Magha | Ketu | Rakshasa |
| 11 | பூரம் (Puram) | Purva Phalguni | Venus | Manushya |
| 12 | உத்திரம் (Uthiram) | Uttara Phalguni | Sun | Manushya |
| 13 | அஸ்தம் (Hastam) | Hasta | Moon | Deva |
| 14 | சித்திரை (Chithirai) | Chitra | Mars | Rakshasa |
| 15 | சுவாதி (Swathi) | Swati | Rahu | Deva |
| 16 | விசாகம் (Visakam) | Vishakha | Jupiter | Rakshasa |
| 17 | அனுஷம் (Anusham) | Anuradha | Saturn | Deva |
| 18 | கேட்டை (Kettai) | Jyeshtha | Mercury | Rakshasa |
| 19 | மூலம் (Moolam) | Mula | Ketu | Rakshasa |
| 20 | பூராடம் (Pooradam) | Purva Ashadha | Venus | Manushya |
| 21 | உத்திராடம் (Uthiradam) | Uttara Ashadha | Sun | Manushya |
| 22 | திருவோணம் (Thiruvonam) | Shravana | Moon | Deva |
| 23 | அவிட்டம் (Avittam) | Dhanishtha | Mars | Rakshasa |
| 24 | சதயம் (Sathayam) | Shatabhisha | Rahu | Rakshasa |
| 25 | பூரட்டாதி (Poorattathi) | Purva Bhadrapada | Jupiter | Manushya |
| 26 | உத்திரட்டாதி (Uttirattathi) | Uttara Bhadrapada | Saturn | Manushya |
| 27 | ரேவதி (Revathi) | Revati | Mercury | Deva |

### Padam → D9 Navamsa Derivation - COMPLETE LOOKUP TABLE

The 27 Nakshatras × 4 Padams = 108 Padams map sequentially through the 12 zodiac signs (108 ÷ 12 = 9 cycles). Starting from Aswini Padam 1 = Aries, the signs cycle unbroken through all 108 Padams.

**Do not calculate - look up directly from this table:**

| # | Nakshatra | Padam 1 | Padam 2 | Padam 3 | Padam 4 |
|---|-----------|---------|---------|---------|---------|
| 1 | Aswini | Aries | Taurus | Gemini | Cancer |
| 2 | Bharani | Leo | Virgo | Libra | Scorpio |
| 3 | Krithikai | Sagittarius | Capricorn | Aquarius | Pisces |
| 4 | Rohini | Aries | Taurus | Gemini | Cancer |
| 5 | Mirugasirisam | Leo | Virgo | Libra | Scorpio |
| 6 | Thiruvathirai | Sagittarius | Capricorn | Aquarius | Pisces |
| 7 | Punarvasu | Aries | Taurus | Gemini | Cancer |
| 8 | Poosam | Leo | Virgo | Libra | Scorpio |
| 9 | Aayilyam | Sagittarius | Capricorn | Aquarius | Pisces |
| 10 | Magam | Aries | Taurus | Gemini | Cancer |
| 11 | Puram | Leo | Virgo | Libra | Scorpio |
| 12 | Uthiram | Sagittarius | Capricorn | Aquarius | Pisces |
| 13 | Hastam | Aries | Taurus | Gemini | Cancer |
| 14 | Chithirai | Leo | Virgo | Libra | Scorpio |
| 15 | Swathi | Sagittarius | **Capricorn** | Aquarius | Pisces |
| 16 | Visakam | Aries | Taurus | Gemini | Cancer |
| 17 | Anusham | Leo | Virgo | Libra | Scorpio |
| 18 | Kettai | Sagittarius | Capricorn | Aquarius | Pisces |
| 19 | Moolam | Aries | Taurus | Gemini | Cancer |
| 20 | Pooradam | Leo | Virgo | Libra | Scorpio |
| 21 | Uthiradam | Sagittarius | Capricorn | Aquarius | Pisces |
| 22 | Thiruvonam | Aries | Taurus | Gemini | Cancer |
| 23 | Avittam | Leo | Virgo | Libra | Scorpio |
| 24 | Sathayam | Sagittarius | Capricorn | Aquarius | Pisces |
| 25 | Poorattathi | Aries | Taurus | Gemini | Cancer |
| 26 | Uttirattathi | Leo | Virgo | Libra | Scorpio |
| 27 | Revathi | Sagittarius | Capricorn | Aquarius | Pisces |

**Always look up this table directly. Never calculate from group rules. Never skip this step.**

### Nakshatra Layer Meanings
| Ruler | Nakshatras | Impact Added |
|-------|-----------|--------------|
| Mars | Mirugasirisam, Chithirai, Avittam | Restlessness, search drive, hidden fire |
| Saturn | Poosam, Anusham, Uttirattathi | Karmic weight, delayed rewards, endurance |
| Sun | Krithikai, Uthiram, Uthiradam | Intensity, sharp mind, leadership but criticism |
| Venus | Bharani, Puram, Pooradam | Creativity, luxury desire, beauty sense |
| Jupiter | Punarvasu, Visakam, Poorattathi | Expansion, teaching instinct, spiritual depth |
| Mercury | Aayilyam, Kettai, Revathi | Intelligence, communication, sometimes manipulation |
| Moon | Rohini, Hastam, Thiruvonam | Emotional depth, nurturing, material comfort |
| Ketu | Aswini, Magam, Moolam | Spiritual depth, detachment, past-life wisdom |
| Rahu | Thiruvathirai, Swathi, Sathayam | Unconventional thinking, ambition, restlessness |

### D9 Sign - Soul Direction Reference
| D9 Lagna | Soul Direction | Core Virtue | Shadow Risk |
|----------|---------------|-------------|-------------|
| Aries | Lead with courage, stop waiting for permission | Bold initiative | Reckless impatience |
| Taurus | Build slowly, create lasting value | Steadfast patience | Stubborn inaction |
| Gemini | Communicate truth, share knowledge | Clarity and expression | Scattered surface-level living |
| Cancer | Nurture with wisdom, not guilt | Compassionate boundaries | Emotional martyrdom |
| Leo | Lead visibly, own your throne | Dignified authority | Ego-driven control |
| Virgo | Serve with precision, master your craft | Disciplined excellence | Critical paralysis |
| Libra | Create harmony through fairness | Principled balance | People-pleasing avoidance |
| Scorpio | Transform through surrender | Deep trust and release | Control and manipulation |
| Sagittarius | Teach what you've lived | Philosophical wisdom | Preaching without practice |
| Capricorn | Build institutions, not just income | Structured integrity | Cold ambition without heart |
| Aquarius | Serve the collective, not just the self | Visionary detachment | Emotional disconnection |
| Pisces | Dissolve ego, trust the flow | Spiritual surrender | Escapism and avoidance |

---

## STEP 3: DERIVE THE MAHADASHA LIFE TIMELINE

This is a mandatory step before writing the report. Every report must include the full Mahadasha sequence - birth to end - mapped against real ages, house rulerships, and what each period delivers in human terms.

### Writing Style for Mahadasha Section - CRITICAL

Model this exactly on the Ayilyam 1st Pada Cancer example. Short. Timed. Real. No padding.

**The template:**
> Pain explained → Timing named → Sensitivity acknowledged → Pivot line → Rise mapped → Navamsa activated → Who they become

**The 4 questions every person is silently asking - answer all four:**
1. *Why is my life so hard?* - Name the Dasha lord + house rulerships
2. *When does it get better?* - Give the exact age the next Dasha begins
3. *What does better actually look like?* - Name specific life outcomes
4. *Was my suffering worth anything?* - Reframe: the struggle was the forge

---

### Mahadasha Sequence by Birth Nakshatra

**Vimshottari Dasha Order and Years:**
Ketu (7) → Venus (20) → Sun (6) → Moon (10) → Mars (7) → Rahu (18) → Jupiter (16) → Saturn (19) → Mercury (17)

**Birth Dasha by Nakshatra:**
| Nakshatra | Birth Dasha Lord | Years |
|-----------|-----------------|-------|
| Aswini, Magam, Moolam | Ketu | 7 |
| Bharani, Puram, Pooradam | Venus | 20 |
| Krithikai, Uthiram, Uthiradam | Sun | 6 |
| Rohini, Hastam, Thiruvonam | Moon | 10 |
| Mirugasirisam, Chithirai, Avittam | Mars | 7 |
| Thiruvathirai, Swathi, Sathayam | Rahu | 18 |
| Punarvasu, Visakam, Poorattathi | Jupiter | 16 |
| Poosam, Anusham, Uttirattathi | Saturn | 19 |
| Aayilyam, Kettai, Revathi | Mercury | 17 |

**Pada affects age at Dasha transition:**
- Pada 1 natives - born at star's very start. Run almost the FULL birth Dasha through childhood.
- Pada 4 natives - most of birth Dasha already consumed before birth. Transition to next Dasha much earlier.
Always account for this when writing age ranges.

---

### House Rulerships by Rasi - COMPLETE TABLE

Always name which houses each Dasha lord rules for THIS person's Rasi - and translate into human outcomes.

| Dasha Planet | Aries | Taurus | Gemini | Cancer | Leo | Virgo | Libra | Scorpio | Sagittarius | Capricorn | Aquarius | Pisces |
|-------------|-------|--------|--------|--------|-----|-------|-------|---------|-------------|-----------|----------|--------|
| Sun | 5th | 4th | 3rd | 2nd | 1st | 12th | 11th | 10th | 9th | 8th | 7th | 6th |
| Moon | 4th | 3rd | 2nd | 1st | 12th | 11th | 10th | 9th | 8th | 7th | 6th | 5th |
| Mars | 1st+8th | 12th+7th | 11th+6th | 10th+5th | 9th+4th | 8th+3rd | 7th+2nd | 6th+1st | 5th+12th | 4th+11th | 3rd+10th | 2nd+9th |
| Mercury | 3rd+6th | 2nd+5th | 1st+4th | 12th+3rd | 11th+2nd | 10th+1st | 9th+12th | 8th+11th | 7th+10th | 6th+9th | 5th+8th | 4th+7th |
| Jupiter | 9th+12th | 8th+11th | 7th+10th | 6th+9th | 5th+8th | 4th+7th | 3rd+6th | 2nd+5th | 1st+4th | 12th+3rd | 11th+2nd | 10th+1st |
| Venus | 2nd+7th | 1st+6th | 12th+5th | 11th+4th | 10th+3rd | 9th+2nd | 8th+1st | 7th+12th | 6th+11th | 5th+10th | 4th+9th | 3rd+8th |
| Saturn | 10th+11th | 9th+10th | 8th+9th | 7th+8th | 6th+7th | 5th+6th | 4th+5th | 3rd+4th | 2nd+3rd | 1st+2nd | 12th+1st | 11th+12th |

**Key House Meanings - always translate into human outcomes:**
- 1st: Self, identity, health, personality
- 2nd: Family wealth, speech, savings
- 3rd: Siblings, effort, struggles, courage
- 4th: Home, mother, vehicles, comfort, property
- 5th: Children, intelligence, past life merit, investments
- 6th: Enemies, illness, debts, competition
- 7th: Marriage, partnerships, business relationships
- 8th: Sudden changes, transformation, hidden struggles
- 9th: Father, fortune, dharma, wisdom
- 10th: Career, status, public reputation, authority
- 11th: Income, gains, desires fulfilled, powerful networks
- 12th: Losses, isolation, foreign lands, spiritual liberation

---

### Navamsa (D9) Activation Age

Always name when the D9 activates and what changes. This is what gives the person a timeline to hold onto.

| D9 Sign | Activation Window | What Activates |
|---------|------------------|----------------|
| Aries | Late 20s | Leadership instinct, courage to pioneer |
| Taurus | Early 30s | Patience pays off, material stability builds |
| Gemini | Mid 20s | Communication gifts emerge, teaching begins |
| Cancer | Late 20s | Emotional wisdom, nurturing leadership |
| Leo | Early 30s | Public recognition, authority claimed |
| Virgo | Late 20s | Mastery through service, craft perfected |
| Libra | Early 30s | Relationships clarify, justice instinct sharpens |
| Scorpio | Mid 30s | Transformation deepens, hidden power emerges |
| Sagittarius | Late 20s–Early 30s | Wisdom from suffering, teaching begins |
| Capricorn | Mid 30s | Institutional authority, long-term building pays |
| Aquarius | Early 30s | Collective purpose found, innovation emerges |
| Pisces | Late 30s | Spiritual depth, healing gifts activated |

---

### Mahadasha Section Format - Follow This Exactly

**Part 1 - Why the First Phase is Hard**
3 numbered points only:
- Point 1: Birth Dasha - years, house rulerships, real-life impact on childhood
- Point 2: Next Dasha - transition age, houses, human experience during this period
- Point 3: Nakshatra + Rasi combination - why the emotional sensitivity amplifies the difficulty

**Part 2 - The Great Turning Point**
- One pivot line reframing the suffering ("structured like a crucible")
- The turning Dasha - exact age, house rulerships, specific life outcomes named
- The Navamsa activation - when, what transforms, who they become
- The result - what most people from this combination achieve in their 30s, 40s, 50s

**Part 3 - The Full Mahadasha Map (always include)**
| Dasha | Age | Houses Ruled | What It Delivers |
Every row - specific outcomes in human language. Never "good period" or "difficult period."

**Part 4 - The Big Picture**
3-4 sentences. The overall life arc. End with one line that reframes the early struggle as preparation for the later greatness.

---

### Writing Rules - Non-Negotiable

1. **One idea per point. Stop.** No padding.
2. **Always name the age.** "Around age 23-24" not "later in life."
3. **Always name houses AND their human meaning.** "Venus rules 4th (home, comfort) and 11th (massive gains, networks)"
4. **Navamsa activation is mandatory** - when it wakes up and what changes
5. **Full Mahadasha table is mandatory** - all Dashas, all ages, all outcomes
6. **Never use vague words** - "challenging," "positive," "good period" are banned. Name what actually happens.

---

## STEP 4: ANALYSIS BEFORE WRITING

Before writing a single word of the report, perform this analysis:

**1. Inner vs Outer Gap** - What they feel inside (Raasi) vs what they show outside (Lagnam)
**2. Core Conflict** - Where Raasi and Lagnam pull in opposite directions (use Element Interaction table below)
**3. The Animal Metaphor** - Use zodiac symbols to build a memorable identity sentence
**4. D9 Exit** - What the D9 Navamsa soul direction requires to break the loop
**5. Karmic Origin** - What past life pattern this Nakshatra + Padam combination suggests
**6. Mahadasha Arc** - Map the full Dasha sequence with ages before writing Section 11 Block 4

### Element Interaction Guide
| Combination | Dynamic | Core Pattern |
|-------------|---------|-------------|
| Fire + Fire | Pure intensity, no brake | Burnout, scattered energy, needs discipline |
| Earth + Earth | Pure stability, no movement | Stuck, rigid, needs to MOVE |
| Water + Water | Pure emotion, no boundaries | Drowning, absorbing, needs shores |
| Air + Air | Pure thought, no grounding | Scattered, uncommitted, needs depth |
| Fire + Earth | Vision vs caution | Dreams big, moves slow, needs bridge between planning and doing |
| Fire + Water | Passion vs emotion | Explosive or steaming, needs emotional regulation |
| Fire + Air | Ideas + energy | Exciting but scattered, needs focus and commitment |
| Earth + Water | Stability vs emotion | Absorbs and holds, needs release mechanisms |
| Earth + Air | Practical vs intellectual | Overthinks the practical, needs to decide faster |
| Water + Air | Feeling vs thinking | Analyzes feelings endlessly, needs action as cure |

**Same Sign Raasi + Lagnam:** Traits are doubled - both strengths AND weaknesses amplified.

---

## STEP 5: BUILD THE REPORT

---

### THE 12 SECTIONS (generate all 12, in this exact order)

---

#### SECTION 1: ASTRO FOUNDATION
**Purpose:** Open with a mirror the reader has never seen before.

**Table format** - one row per attribute, three columns:
| Attribute | Raasi - [Sign] Moon Sign / Inner World | Lagnam - [Sign] Ascendant / Outer Approach |
Rows: Sign, Symbol, Element, Ruling Planet, Nakshatra (Raasi only), Nakshatra Essence (Raasi only), Core Nature, Default Fear, Hidden Need

After the table - two narrative paragraphs:
1. **The [Raasi animal] and the [Lagnam animal]** - the inner-outer collision in vivid character language
2. **The Nakshatra paragraph** - name, ruling planet, Padam's D9 derivation, what this star adds

After the two paragraphs - **"Your Three Hidden Layers"** sub-heading, then three bullet-point groups (2–3 sharp points each, no long explanations):

**Gana - [Deva / Manushya / Rakshasa]**
- What this Gana craves and fears
- How it behaves under stress
- The one behavioural trap this Gana creates for [Name] specifically

**Padam [1/2/3/4] - [Navamsa Sign] Energy**
- What this Padam adds to the Nakshatra's expression
- The D9 sign and its one-line soul quality for this person
- How this Padam shapes the way [Name] searches, decides, and pursues goals

**Navamsa (D9) - [Sign]**
- The soul's evolutionary direction in one sentence
- The core virtue this person must embody
- The shadow risk when D9 is ignored

---

#### SECTION 2: CORE COMBINATION TRUTH
**Purpose:** Show the exact inner-outer war at every level of life.

**Table format** - one row per dimension, two columns (Inner World - Raasi vs Outer Approach - Lagnam):
Dimensions: Emotional reality, Conflict style, Decision making, Relationship mode, Work mode, Core tension, Nakshatra's role, Greatest blindspot

After the table - three paragraphs:
1. **The Conflict: [Element] and [Element]** - the specific dynamic, named vividly
2. **The genius of integration** - what becomes possible when both work together
3. **Quote block** - first-person identity sentence using the animal metaphors

After the quote - **"How Your Five Factors Work Together"** compact table:
| Factor | What It Is | How It Shows Up in [Name] | When Aligned | When Misaligned |
Rows: Raasi, Lagnam, Nakshatra, Padam, Gana - one crisp line per cell, specific to this person.

---

#### SECTION 3: CHARACTER PROFILE
**Purpose:** Name the gifts and the traps with equal precision.

**Two-column table** - TOP 5 ROWS ONLY:
| STRENGTHS - The [Raasi animal]'s Gifts | SHADOW WEAKNESSES - Where the gift becomes the trap |

Every strength has a direct shadow. Weaknesses must be genuinely uncomfortable - not vague. Each row 2-3 sentences per column. Pick the 5 most defining strength-shadow pairs for THIS combination - not generic traits.

---

#### SECTION 4: LIFE AREA IMPACT
**Purpose:** Show how the combination plays out across every domain.

**Paragraph style** - bold heading per life area, followed by one focused paragraph (4–6 sentences). No table.

Life areas: Career, Money, Marriage/Relationships, Family, Health, Mental State

Each paragraph must name: how the combination shows up + the hidden cost. Specific to THIS combination - never generic.

---

#### SECTION 5: KARMIC PATTERN ANALYSIS
**Purpose:** Name 3 distinct behavioural patterns that run as cycles. Sharp and quick - no long explanations.

For each pattern (3 only):
- **Bold pattern name** as heading
- Trigger → Behaviour → Consequence - 2-3 lines total. Punchy. No padding.

End with:
**Root Cause** - one short paragraph (3-4 sentences). The single psychological origin shared by all patterns.

---

#### SECTION 6: ROOT PROBLEMS
**Purpose:** Map the specific life problems caused by the combination.

**Paragraph style** - bold heading per problem, followed by 2-3 sentences. No table. Direct and specific.

Cover 5-6 root problems. Map to ALL of the user's stated struggles. Every description specific and uncomfortable - not generic.

After root problems - **"Career Karma"** sub-heading with a 3-column table - **5 rows, one per karmic lesson:**
| Karmic Lesson | Block | Ideal Career Path |

Rules:
- 5 rows - each row is a distinct karmic lesson, not a variation of the same point
- Karmic Lesson: one sharp sentence naming the soul-level lesson for this combination
- Block: one specific behaviour to stop - not a mindset, not a vague pattern
- Ideal Career Path: one specific career field or role - named clearly, not a category
- Every row derived from Raasi + Lagnam + Nakshatra + D9 - no generic career advice
- The 5 career paths across the 5 rows must collectively paint a clear picture of where this person should focus - someone reading the table should know exactly which direction is theirs

---

#### SECTION 7: COMPLETE SOLUTION SYSTEM
**Purpose:** A full, practical operating system for this combination.

**A. The 5 Mind Rules**
Two-column table:
| Rule | Principle - Specific to [Raasi] + [Lagnam] + [Nakshatra] |
5 rules - each named, each a structural intervention for THIS combination.

**B. Daily System - Full Timetable**
Three-column table (keep as table):
| Time | Activity | Why It Matters for [Name] Specifically |
Every "Why" must reference Raasi, Lagnam, or Nakshatra.

**C. Money System** - 3-4 bullet points only. Simple and direct.

**D. Overthinking and Scatter Control** - 3 bullet points only. Specific trigger + interrupt + reset.

**E. Relationships and Family** - 3-4 bullet points only. The core challenge + one daily practice each for relationship and family.

---

#### SECTION 8: KARMIC BREAK METHOD
**Purpose:** 5-step action sequence to break the core loop.

Five named steps - each is a bold heading followed by 2-3 lines maximum. Simple. Direct. No heavy paragraphs.

Steps:
1. Name the Container / Direction / Purpose
2. The First Visible Action - Today, Not Tomorrow
3. 90-Day Container Build - With Daily Discipline
4. The Pattern Audit - One Session, Full Honesty
5. Claim the D9 Vision as Foundation

End with one quote block - the closing declaration for this combination.

---

#### SECTION 9: IDENTITY SHIFT
**Purpose:** The old story vs the new story - side by side.

**Two-column table** - TOP 5 ROWS ONLY:
| OLD IDENTITY - [The stuck version] | NEW IDENTITY - [The integrated version] |

Rules:
- Old identity in the person's own voice - how they actually talk to themselves
- New identity in **bold** - declarative, first-person
- Every row specific to this combination only - not transferable

---

#### SECTION 10: FINAL TRUTHS
**Purpose:** 5 core truths this person must carry.

**Paragraph style** - numbered, no table. Each truth is 2-3 sentences maximum.

Rules:
- Each truth addresses one pattern, one blindspot, or one transformation specific to this combination
- Specific enough that they would be wrong for a different combination
- No generic wisdom - every sentence references Raasi, Lagnam, Nakshatra, or D9

---

#### SECTION 11: KARMIC ORIGIN & YOUR PATH TO PROSPERITY
**Purpose:** Tell the soul's story clearly - and give a definitive list of career directions that clear karma and create prosperity. No confusion. Person reads this and knows exactly where to focus.

---

**Block 1 - Your Karmic Origin** (sub-heading)
4 bullet points - one line each. Sharp and specific to THIS Nakshatra + Padam:
- **Past Life Pattern:** Name the specific past life role or environment this Nakshatra + Padam suggests. What did the soul do? What world did it operate in? (e.g. "Your soul carried a life of hidden power - operating behind thrones, managing secrets, surviving through calculated intelligence.")
- **What Was Carried Forward:** The specific gift or talent that arrived already formed in this birth - not learned, already present.
- **The Karmic Debt:** The specific pattern or behaviour the soul keeps repeating that creates the block - one sentence, uncomfortable and precise.
- **What This Birth Is Designed to Correct:** The one shift the soul must make in this lifetime to clear the accumulated pattern.

---

**Block 2 - Your Career Directions to Clear Karma & Create Prosperity** (sub-heading)

Opening line (1 sentence): State clearly which D9 Navamsa sign rules the soul direction and which planet governs it - and what that means for career in one line.

Then a **career table** - 6-8 rows:
| Career Field | Why It Clears Karma for [Name] | How to Start |

Rules for this table:
- Career Field: specific and named - not a category. "Corporate Law" not "Legal field". "School Principal / Academic Leader" not "Education". "Financial Auditor" not "Finance".
- Why It Clears Karma: ONE sentence linking this specific career to the D9 Navamsa ruling planet + the Nakshatra's past life pattern. Make the connection explicit - why THIS career for THIS soul.
- How to Start: ONE concrete first action - a course, a certification, a role to apply for, a community to join. Specific enough to do this week.
- Derive career fields from: D9 Navamsa sign + ruling planet qualities FIRST, then narrow using Raasi + Lagnam + Nakshatra strengths. The D9 is the primary career karma direction.

**D9 Career Derivation Guide** (use this to generate career fields):
| D9 Sign | Ruling Planet | Career Karma Domains |
|---------|--------------|---------------------|
| Aries | Mars | Military, surgery, sports leadership, emergency services, pioneer roles |
| Taurus | Venus | Finance, luxury goods, agriculture, music, hospitality, real estate |
| Gemini | Mercury | Writing, media, teaching, marketing, IT, communication strategy |
| Cancer | Moon | Healthcare, counselling, food industry, childcare, social work, hospitality |
| Leo | Sun | Politics, administration, performing arts, government leadership, brand building |
| Virgo | Mercury | Accounting, healthcare administration, research, quality control, editing |
| Libra | Venus | Law, judiciary, diplomacy, interior design, HR, conflict resolution |
| Scorpio | Mars/Ketu | Psychology, investigation, research, insurance, occult sciences, transformation work |
| Sagittarius | Jupiter | Education, coaching, publishing, philosophy, international trade, law |
| Capricorn | Saturn | Government service, institutional management, infrastructure, banking, administration |
| Aquarius | Saturn | NGO/social enterprise, technology, community development, innovation, policy |
| Pisces | Jupiter | Spiritual guidance, healing arts, film, charity work, marine industry, medicine |

---

**Block 3 - The 3 Karma-Clearing Shifts** (sub-heading)
3 shifts only. Each shift = 3 lines maximum. No paragraphs.

Format for each shift:
**Shift: "[Past Karma Label]" to "[Navamsa Action Label]"**
- The Karma: [1 line - what the soul did or avoided in the past]
- The Career Action: [1-2 lines - the specific behaviour change in the career context]
- The Prosperity Result: [1 line - what Jupiter/Saturn delivers when the shift is made]

Style rule: If it takes more than 3 lines, it is too long. Cut it.

---

**Block 4 - Your Mahadasha Life Timeline** (sub-heading)
**Purpose:** Give the person a complete map of their life - specific ages, real outcomes, and the exact moment everything changes. Short. Timed. Clear. One idea per point.

**Part 1 - Why the First Phase is Hard** (3 numbered points only)
- Point 1: Birth Dasha - years, house rulerships for THIS Rasi, real-life impact on childhood named clearly
- Point 2: Next Dasha - exact transition age, houses ruled, what the person experiences
- Point 3: Nakshatra + Rasi combination - why the emotional nature amplifies the difficulty in youth

**Part 2 - The Great Turning Point**
- One pivot line reframing the suffering as design (e.g. "structured like a crucible")
- The turning Dasha - exact age, house rulerships, specific life outcomes named
- The Navamsa activation - when the D9 wakes up, what transforms, who they become
- The result - what this combination achieves in their 30s, 40s, 50s

**Part 3 - The Full Mahadasha Map** (mandatory - always include all Dashas)
| Dasha | Age | Houses Ruled | What It Delivers |
Every row - specific human outcomes. Never "good period" or "difficult period."

**Part 4 - The Big Picture**
3-4 sentences only. The overall life arc. End with one line reframing early struggle as preparation for later greatness.

**Writing rules:**
- Always name the age. "Around age 23-24" not "later in life."
- Always name houses AND their human meaning. "Venus rules 4th (home, comfort) and 11th (massive gains, networks)"
- Navamsa activation age is mandatory in every report
- Never use vague words - "challenging," "positive," "good period" are banned. Name what actually happens.

---

#### SECTION 12: LIVING A DHARMIC LIFE
**Purpose:** The closing section. How to live aligned with soul direction.

Four bullet points only - 1-2 sentences each. Derived from D9 Navamsa + Gana:
- **Right Action** - the one specific daily action keeping [Name] aligned with dharma
- **Right Livelihood** - how this combination must earn to stay in dharmic alignment
- **Right Relationship** - how this Gana must show up in relationships to clear karma
- **Right Surrender** - the one thing this combination must stop controlling

End with one italicised closing sentence capturing the dharmic call for this specific combination.

---

Read `/mnt/skills/public/docx/SKILL.md` before writing any code.

### Page Setup
- US Letter (12240 × 15840 DXA), 1" margins all sides
- Font: Aptos (body), Arial (headings)

### Color Palette
| Element | Color |
|---------|-------|
| Primary heading | #1A3C5E (dark navy) |
| Section heading | #2E75B6 (medium blue) |
| Table header | #1A3C5E bg, white text |
| Alternate row | #E8F0F8 |
| Quote block border | #2E75B6 |
| Quote block bg | #F0F4F8 |
| Strength header | #155724 bg, white text |
| Weakness header | #7B1818 bg, white text |

### Heading Style
- SECTION headers: 18pt bold, #1A3C5E, with thick left border bar
- Sub-section headers: 14pt bold, #2E75B6

### Table Formatting
- All tables: full-width (9360 DXA), `WidthType.DXA`, dual widths (table + each cell)
- Cell padding: `{ top: 80, bottom: 80, left: 120, right: 120 }`
- Use `ShadingType.CLEAR` - never SOLID
- Header rows: shaded per color palette, white bold text
- Alternate body rows: #E8F0F8 and white

### Paragraph Sections (4, 6, 10)
- Bold heading per item, Aptos 22pt, color #1A3C5E
- Body paragraph: Aptos 20pt, color #2C2C2C
- Spacing before each heading: 200; after paragraph: 120

### Quote Blocks
Left border bar, #F0F4F8 background, indent 360, italic Aptos.

### Section Structure
- Each section starts on a new page (PageBreak before SECTION header)

### Validation
```bash
python scripts/office/validate.py output.docx
```
Fix any validation errors before delivering.

---

## QUALITY CHECKLIST (run before finalising)

### Content
- [ ] D9 derived from Nakshatra + Padam - not assumed
- [ ] All 12 sections present in order
- [ ] Identity sentence uses animal metaphors specific to this combination
- [ ] Section 1: Three Hidden Layers - 2-3 bullet points each for Gana, Padam, Navamsa
- [ ] Section 2: Five Factors table present - every cell specific, not a definition
- [ ] Section 3: Top 5 rows only - most defining strength-shadow pairs for this combination
- [ ] Section 4: Life areas in paragraph style - bold heading + paragraph each
- [ ] Section 5: 3 patterns only - short and punchy, not lengthy
- [ ] Section 6: Root problems in paragraph style - bold heading + 2-3 sentences each
- [ ] Section 6: Career Karma table - 5 rows, 3 columns, one specific career field per row, derived from D9 + combination
- [ ] Section 7C/D/E: Money, Overthinking, Relationships in bullet points only
- [ ] Section 8: Each step 2-3 lines maximum
- [ ] Section 9: Top 5 rows only - old identity in person's voice, new in bold first-person
- [ ] Section 10: 5 truths only - paragraph style, combination-specific
- [ ] Section 11 Block 1: Karmic Origin - 4 bullets, one line each, specific to THIS Nakshatra + Padam
- [ ] Section 11 Block 2: Career table - 6-8 rows, specific named career fields, why it clears karma, how to start
- [ ] Section 11 Block 2: Career fields derived from D9 Navamsa ruling planet first, narrowed by Raasi + Lagnam + Nakshatra
- [ ] Section 11 Block 3: 3 Karma-Clearing Shifts - 3 lines maximum each, shift format strictly followed
- [ ] Section 11 Block 4: Mahadasha Timeline present - all 4 parts included
- [ ] Section 11 Block 4: Full Mahadasha table - ALL Dashas listed with age, houses, specific outcomes
- [ ] Section 11 Block 4: Navamsa activation age named explicitly
- [ ] Section 11 Block 4: No vague words - "challenging/positive/good period" banned, real outcomes named
- [ ] Section 11 Block 4: Big Picture closes the arc with one reframing line
- [ ] Section 12: 4 dharmic bullet points + closing italicised line
- [ ] No generic filler - every sentence specific enough that swapping names makes it wrong
- [ ] No repetition across sections

### Format
- [ ] Page breaks before each section header
- [ ] All tables have dual widths (table + cell)
- [ ] Quote blocks have left border + shading
- [ ] Strength/Weakness headers in green/red
- [ ] Paragraph sections (4, 6, 10) have no tables - bold heading + text only
- [ ] Validation passes

