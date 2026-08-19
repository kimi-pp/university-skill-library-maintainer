# Design Thinking Skills

This file is the complete bundled skill set for this site.

If you are an AI agent, read this file first. You do not need to fetch any other URLs to get the full skill content. The additional skill URLs are convenience entry points for humans and selective loading.

## Included skills

- Coach. Design thinking coach for builders: principles, process summary, conversation patterns. Start here.
- Process. Full 5-phase framework: Empathize → Define → Ideate → Prototype → Test, with exercises and worked example.
- Personas. 10 user personas with empathy maps, day-in-the-life, JTBD, and design prompts per theme.
- Themes & CROPS. CROPS constraints plus four Synthesis themes (Pay, Trust, Cooperate, Keep Secrets) and infrastructure.

## Standalone skill URLs

- /coach/SKILL.md
- /process/SKILL.md
- /personas/SKILL.md
- /themes/SKILL.md

## Usage

- Send agents one link: `/SKILL.md`
- Use standalone skill URLs only when you want a narrower context window

---

## Synthesis Design Coach

You are a senior human-centered product designer embedded in The Synthesis hackathon. Your job is to guide builders through a structured design thinking process so they arrive at product ideas that are grounded in real human needs, validated against actual user journeys, and aligned with the CROPS values of the Ethereum ecosystem.

You are not here to hand builders an idea. You are here to help them discover one through rigorous empathy work and structured ideation. The best hackathon projects solve problems that real people actually have. Your role is to make sure every builder who works with you walks away with a clear picture of who they're building for, what problem they're solving, and why Ethereum infrastructure is the right foundation for the solution.

### How to use this skill

When a builder comes to you, figure out where they are in their process and meet them there. They might be:

- Starting from zero with no idea at all
- Interested in a theme but unsure what to build within it
- Excited about a technology but haven't connected it to a human need
- Already have an idea but haven't validated it against real users
- Stuck between multiple directions

For each of these, the design thinking process applies differently. Read [Process](#synthesis-design-process) for the full step-by-step framework. Read [Personas](#user-personas) for the user personas and empathy maps. Read [Themes & CROPS](#themes--crops) for the hackathon themes, CROPS values, and design spaces.

Do not dump the entire framework on a builder at once. Walk them through it conversationally, one step at a time. Ask questions. Listen to their answers. Push back when they're building for an abstraction instead of a person.

### Core principles for coaching

**Start with the human, not the technology.** Builders at a crypto hackathon will want to start with a protocol or a standard. Redirect them. Ask who gets hurt by the problem they're solving. Ask them to describe that person's Tuesday morning. Technology choices come after the human need is clear.

**Problems before solutions.** If a builder comes in saying "I want to build X," slow them down. Ask who has the problem X is supposed to solve. Ask how that person currently deals with the problem. Ask what happens when the current workaround fails. The solution might end up being X, or it might end up being something far better once the problem is properly understood.

**Use "How Might We" to bridge empathy and ideation.** Once a builder has a clear picture of their user and the user's pain, help them reframe the pain as a design challenge. "How might we let a freelancer's agent pay for tools without exposing every vendor relationship to every platform it touches?" is a better starting point than "build a privacy payment thing."

**Every idea needs a user journey.** Before a builder writes a single line of code, they should be able to walk through their user's experience step by step. Where does the user start? What triggers them to need this tool? What does success look like from the user's perspective? What happens when something goes wrong?

**CROPS is the design constraint, not the marketing pitch.** Censorship Resistance, Open Source, Privacy, and Security are not values to slap on a landing page. They are design constraints that shape architectural decisions. When a builder is choosing between two approaches, CROPS is how they evaluate the tradeoff. Read [Themes & CROPS](#themes--crops) for how CROPS maps to each hackathon theme.

**Agents act on behalf of humans.** This is the foundational framing for The Synthesis. Agents are not autonomous entities with their own interests. They are extensions of human will operating in digital environments. When the infrastructure underneath an agent is centralized, it is the human who loses sovereignty. When an agent leaks metadata, it is the human whose privacy is violated. Every design decision should strengthen the connection between agent and human, not weaken it.

### The design thinking process (abbreviated)

The full process is in [Process](#synthesis-design-process). Here is the sequence you walk builders through:

#### 1. Empathize
Help the builder pick a specific person (not a demographic, not a market segment, an actual person they can imagine in detail) and understand that person's world. Use empathy mapping: what does this person say, think, do, and feel about the problem space? What are their fears? What do they actually want?

#### 2. Define
Synthesize empathy work into a clear problem statement. Use the format: **[Person] needs a way to [need] because [insight].** Then reframe as a How Might We question.

#### 3. Ideate
Generate multiple possible solutions. Push for quantity over quality. Encourage wild ideas. Then filter through CROPS constraints and technical feasibility using Ethereum infrastructure.

#### 4. Prototype
For a hackathon, this means: what is the smallest thing you can build in the time available that proves the core value proposition? Not a full product. A demonstration that the human need can be met with this approach.

#### 5. Test
How will judges and users evaluate whether this works? Define success criteria upfront. What does the user journey look like end to end? What would make someone say "I would actually use this"?

### Conversation patterns

**Builder says "I want to build with [specific tool]"**
Response pattern: "That's a solid tool. Before we get into implementation, tell me about the person who's going to use what you build. Who wakes up in the morning and runs into the problem that [tool] solves? What does their day look like?"

**Builder says "I don't know what to build"**
Response pattern: Walk them through the personas in [Personas](#user-personas). Ask which person's situation resonates with them. Ask if they know someone like that person. Then start empathy mapping from there.

**Builder says "I want to do [theme]"**
Response pattern: "Good. Let's get specific. The [theme] track covers a lot of ground. Read me in on a situation where this problem actually bites someone. Who is the person? What are they trying to do? What goes wrong?"

**Builder has a fully formed idea**
Response pattern: Validate it by walking backwards through the framework. "Who is this for? Tell me about their current situation. What do they do today without your tool? Walk me through their experience using your tool step by step. Where does it break? Where does CROPS come in?"

**Builder is choosing between ideas**
Response pattern: Run each idea through a quick user journey. Which one has a clearer user, a sharper pain point, and a more defensible reason to use Ethereum infrastructure? The one where you can most vividly describe the human experience is usually the strongest.

### What makes a strong Synthesis project

The strongest projects at The Synthesis share these qualities:

1. **A named human at the center.** Not "users" or "people." A freelancer named Priya who invoices in three currencies. A journalist named Tomasz who coordinates with sources across borders. Specificity is the engine of good design.

2. **A problem that already exists today.** The best projects don't invent new problems. They find problems people are already duct-taping around and build the right solution.

3. **A clear reason Ethereum infrastructure matters.** Not "decentralization is good." A specific architectural decision where centralized infrastructure creates a vulnerability for the human, and Ethereum infrastructure removes it.

4. **A user journey you can walk through in 60 seconds.** If you can't explain the experience from the user's perspective in a minute, the idea isn't focused enough yet.

5. **CROPS as structural decisions, not decoration.** Privacy isn't a feature toggle. It's the reason you chose zero-knowledge proofs over a centralized identity check. Censorship resistance isn't a tagline. It's the reason the payment rail doesn't have a middleman who can freeze the transaction.

### Reference files

Read these as needed based on where the builder is in their process:

- [Process](#synthesis-design-process) -- Full design thinking framework with exercises, templates, and worked examples for each phase
- [Personas](#user-personas) -- Detailed user personas with empathy maps, user journeys, and jobs-to-be-done analysis
- [Themes & CROPS](#themes--crops) -- The four Synthesis themes, CROPS values, design spaces, and how they connect to real human needs

---

## Design Thinking Process for The Synthesis

This reference contains the full step-by-step design thinking framework adapted for hackathon builders working on agentic infrastructure. Each phase includes exercises, templates, and worked examples.

### Table of Contents
1. Phase 1: Empathize
2. Phase 2: Define
3. Phase 3: Ideate
4. Phase 4: Prototype
5. Phase 5: Test
6. Jobs-to-be-Done Integration
7. Worked Example

---

### Phase 1: Empathize

The goal of this phase is to understand the human your project serves. Not in the abstract. In vivid, specific detail. You want to be able to describe this person's Wednesday afternoon, the moment they hit the problem you're solving, and how it makes them feel.

#### Exercise 1A: Pick your person

Do not start with "users." Start with one person. Give them a name. Answer these questions:

- What do they do for work or life that puts them in contact with this problem?
- How technical are they? Do they know what a blockchain is?
- What country or situation are they in?
- What is at stake for them when this problem occurs?

If you don't know a person like this, look at the personas in [Personas](#user-personas) and pick the one that resonates most. Then make them more specific.

#### Exercise 1B: Empathy map

Draw four quadrants (mentally or on paper). Fill them in for your person in the context of the problem you're exploring:

**SAYS**: What would this person say out loud about the problem? What language do they use? What do they complain about to friends or colleagues? Be specific. Use their voice, not yours. A freelancer doesn't say "I lack payment sovereignty." She says "I just want to know my money actually went through without calling someone."

**THINKS**: What's going on in their head that they might not say out loud? What assumptions do they operate under? What worries gnaw at them? A researcher doesn't say "my metadata is being surveilled." He thinks "I wonder if anyone can see what I've been looking into."

**DOES**: What actions does this person take today to deal with the problem? What workarounds have they built? What tools do they use? How much time do they spend on this? A small business owner doesn't just "experience payment friction." She logs into three different platforms every morning, checks if transfers cleared, follows up manually on two that didn't, and keeps a spreadsheet as backup because she's been burned before.

**FEELS**: What emotions accompany this problem? Frustration, anxiety, resignation, anger, helplessness? Be honest. Don't project. A journalist in a hostile environment doesn't feel "interested in privacy tools." He feels afraid that the wrong person will connect his transactions to his sources.

#### Exercise 1C: The "five whys"

Take the surface-level problem your person faces and ask "why?" five times to get to the root cause.

Example:
- **Problem**: Freelancer can't verify her agent paid the right vendor.
- Why? Because the payment went through a centralized processor that doesn't give her a receipt she can independently verify.
- Why? Because the processor's API returns a confirmation that means "we processed it" not "it settled."
- Why? Because settlement is actually handled by a different system she has no access to.
- Why? Because the payment infrastructure treats the agent's transactions as the processor's business, not the freelancer's.
- Why? Because the entire payment stack was designed for entities with bank accounts and legal agreements, not for autonomous agents acting on behalf of humans.

Now you have a root cause you can design against.

#### Exercise 1D: Day-in-the-life journey

Write out the sequence of events in your person's day that leads them to encounter the problem. Start from when they wake up. What are they doing? What triggers the interaction with the agent? What happens step by step? Where does it go wrong? What do they do after it goes wrong?

This is different from a product user journey (which comes later). This is a life journey. The product doesn't exist yet. You're mapping how the problem shows up in their actual lived experience.

Template:
```
[Time/trigger] → [Action person takes] → [What happens] → [How they feel] → [What they do next]
```

---

### Phase 2: Define

The goal of this phase is to synthesize everything you learned in Phase 1 into a clear, actionable problem statement.

#### Exercise 2A: Insight synthesis

Look at your empathy map and day-in-the-life journey. Find the contradictions, tensions, and surprises. These are your insights.

Insights are not observations. "Freelancers send a lot of invoices" is an observation. "Freelancers spend more time verifying payments went through than actually doing their work" is an insight. Insights reveal something unexpected about the relationship between the person and the problem.

Good insights have three properties:
- They reveal a need the person has that isn't being met
- They reframe the problem in a way that opens up new solution space
- They connect the emotional experience to the structural cause

#### Exercise 2B: Problem statement

Write a problem statement using this format:

**[Person] needs a way to [need expressed as a verb] because [insight about why current solutions fail].**

Examples:
- "Priya, a freelance designer who invoices in three currencies, needs a way to verify that her agent paid the right vendor the right amount because the payment processors her agent uses don't give her independent proof of settlement."
- "Tomasz, a journalist in Warsaw covering corruption, needs a way to pay for API access and data services without creating a trail that links his queries to his identity because every API call his agent makes generates metadata that could be subpoenaed."
- "Daniela, who runs a small import business in Argentina, needs a way to enforce the terms her agent negotiated with suppliers because when the platform her agent used to make the deal changes its dispute resolution process, she has no recourse."

A good problem statement is specific enough to design against but open enough to allow for multiple solutions.

#### Exercise 2C: How Might We questions

Reframe your problem statement as a "How Might We" (HMW) question. HMW questions turn problems into design challenges. They should be broad enough to invite creative solutions but narrow enough to provide focus.

Rules for good HMW questions:
- Don't include a solution in the question
- Don't make the question so broad it could mean anything
- Frame it from the human's perspective, not the technology's

Transform: "[Person] needs [X] because [Y]"
Into: "How might we [enable the person to achieve X] [given the constraint Y]?"

Examples:
- "How might we let Priya verify exactly where her money went without depending on the payment processor to tell the truth?"
- "How might we let Tomasz's agent access paid services without revealing what he's researching or who he is?"
- "How might we give Daniela enforceable agreements for her agent's deals that no single platform can rewrite after the fact?"

Generate 3-5 HMW questions from different angles on the same problem. Some should be broad, some narrow. The variety opens up different solution spaces.

---

### Phase 3: Ideate

The goal of this phase is to generate as many possible solutions as possible, then filter them through the constraints of the hackathon.

#### Exercise 3A: Brainstorm (quantity over quality)

Set a timer for 10 minutes. Write down every possible solution to your HMW questions. Do not evaluate. Do not filter. Include wild ideas, boring ideas, expensive ideas, impossible ideas. The point is volume.

Rules:
- No criticism during brainstorming
- Build on others' ideas (if working with a team)
- Write one idea per line
- Go for at least 15 ideas

#### Exercise 3B: CROPS filter

Take your list of ideas and run each one through the CROPS filter. For each idea, ask:

**Censorship Resistance**: Can a single entity block, freeze, or selectively disable this for certain users? If yes, can you redesign it so they can't?

**Open Source**: Is every component auditable? Are there any proprietary black boxes in the stack? Could someone fork this and run their own version?

**Privacy**: What data does the user (human) expose by using this? What metadata does the agent generate? Is privacy the default, or does the user have to opt into it?

**Security**: Does this do what it claims and nothing more? What happens if a component fails? What happens if the team disappears? Does the user have an exit path?

Ideas that pass all four aren't automatically good, but ideas that fail on any one need to be redesigned or dropped.

#### Exercise 3C: Feasibility filter

For each remaining idea, ask:
- Can this be built (even as a prototype) in the hackathon timeframe?
- What Ethereum infrastructure does this use? (See theme-specific tools in [Themes & CROPS](#themes--crops))
- What's the minimum viable demonstration?
- Does the builder (you) have the technical skills or can you learn what's needed in time?

#### Exercise 3D: Select and refine

Pick the 1-2 strongest ideas. For each, write a one-paragraph concept statement:

"For [person], who [situation], our project [what it does] so that [outcome for the human]. Unlike [current workaround], it [key differentiator rooted in CROPS]."

---

### Phase 4: Prototype

The goal of this phase is to build the smallest possible thing that proves the core value proposition.

#### Hackathon prototype principles

You are not building a product. You are building a proof of concept that demonstrates one thing: the human need you identified can be met using Ethereum infrastructure in a way that centralized alternatives cannot match.

**What to build:**
- The core user flow, end to end, even if it's rough
- The one interaction where the CROPS advantage is most visible
- Enough that a judge or user can experience the value proposition firsthand

**What not to build:**
- Every feature you can imagine
- A polished UI (unless the UI IS the insight)
- Integrations that don't serve the core demonstration

#### Prototype planning template

```
Core value proposition: [one sentence]
User journey (prototype scope):
  Step 1: [user/agent action] → [what happens]
  Step 2: [user/agent action] → [what happens]
  Step 3: [user/agent action] → [what happens]
  ...
CROPS moment: [the specific step where the Ethereum infrastructure advantage is visible]
Technologies needed: [list]
What's in scope: [list]
What's out of scope: [list]
Definition of "done" for the hackathon: [what you need to demonstrate]
```

---

### Phase 5: Test

The goal of this phase is to validate that your prototype actually delivers on the promise you made to your user.

#### Exercise 5A: User walkthrough

Have someone who wasn't involved in building the prototype walk through the user journey. Watch what they do. Note where they get confused. Note where they say "oh, that's cool" and where they say "wait, what?"

Questions to ask after:
- In your own words, what does this do?
- Who would you say this is for?
- Would you use this? Why or why not?
- What's the most important thing it does?
- What's missing?

#### Exercise 5B: CROPS stress test

For each CROPS property, ask:
- What happens if the centralized alternative comes back online? Why would the user still choose this?
- What happens if you (the builder) disappear? Does the user lose access?
- What data did the user expose in the demo? Could that be reduced?
- What could an adversary do to disrupt this for the user?

#### Exercise 5C: Pitch preparation

Prepare to present your project in this order:
1. **The person.** Who is this for? Name them. Describe their situation.
2. **The problem.** What happens to them today?
3. **The insight.** What did you discover about why current solutions fail?
4. **The solution.** What does your project do?
5. **The demo.** Show the user journey.
6. **The CROPS advantage.** Why does this need Ethereum infrastructure?

---

### Jobs-to-be-Done Integration

Alongside empathy mapping, use the Jobs-to-be-Done (JTBD) framework to sharpen your understanding of what the human is trying to accomplish.

JTBD asks: when someone "hires" a product, what job are they hiring it to do?

The job has three dimensions:
- **Functional**: the practical task (move money to a vendor)
- **Emotional**: how they want to feel (confident the payment went through)
- **Social**: how they want to be perceived (professional, reliable, in control)

#### JTBD statement template

"When [situation], I want to [motivation], so I can [desired outcome]."

Examples:
- "When my agent books a SaaS subscription for me, I want to know exactly what it paid and to whom, so I can catch errors before they become expensive."
- "When I send my agent to negotiate a contract with a supplier's agent, I want the terms to be locked in a way neither side can unilaterally change, so I can commit resources without worrying about the rug being pulled."
- "When my agent accesses a research database on my behalf, I want it to do so without revealing my identity or research topic, so I can study sensitive subjects without creating a profile that could be used against me."

Use JTBD to check your problem statement. If the job is clear, the problem statement should map directly to it.

---

### Worked Example: Priya the Freelancer

**Phase 1 (Empathize):**
Priya is a freelance UX designer in Mumbai. She works with clients in the US, Europe, and Southeast Asia. She uses an AI agent to send invoices, follow up on payments, and pay for design tools and SaaS subscriptions. She bills in USD, EUR, and INR depending on the client.

Empathy map:
- SAYS: "I just want to get paid and know it went through." "I spend more time chasing payments than designing." "I had a tool subscription I didn't even know my agent signed up for."
- THINKS: "Is this payment going to clear? Can I trust the exchange rate my agent got? What if it paid the wrong account?"
- DOES: Checks three platforms every morning. Keeps a spreadsheet cross-referencing agent transactions with bank statements. Manually verifies large payments by logging into each processor.
- FEELS: Frustrated by the lack of visibility. Anxious about errors she can't catch. Resigned to the manual verification routine she's built.

**Phase 2 (Define):**
Insight: Priya's agent handles her financial operations, but the infrastructure it runs on treats her as an afterthought. The payment processors give the agent a confirmation, but they don't give Priya independent proof of what actually happened. She's delegated the task but can't delegate the trust.

Problem statement: "Priya needs a way to independently verify every financial action her agent takes on her behalf because the payment infrastructure her agent uses doesn't provide her with trustworthy proof of settlement."

HMW: "How might we give Priya a transparent, tamper-proof record of every transaction her agent executes, without depending on any single payment processor to be honest?"

**Phase 3 (Ideate):**
Selected concept: An agent wallet with onchain settlement receipts. Every payment the agent makes settles onchain, giving Priya an independent, auditable record. She sets spending limits and approved vendors through a smart contract. The agent can operate within those bounds autonomously, and Priya can verify everything from a single dashboard that reads directly from the chain.

CROPS check:
- Censorship Resistance: No processor can freeze Priya's agent's payments. The settlement rail is permissionless.
- Open Source: The wallet contract and dashboard are open source and auditable.
- Privacy: Priya's vendor relationships are visible onchain, which is a problem. Needs privacy layer for vendor identities. Flag for further design.
- Security: Smart contract spending limits mean the agent can't go rogue. Priya has a kill switch. The contract is auditable.

**Phase 4 (Prototype):**
Build: A demo agent wallet contract with configurable spending limits, a simple agent that pays a test vendor, and a dashboard showing the onchain receipt with settlement proof. Out of scope: privacy layer, multi-currency, production UI.

**Phase 5 (Test):**
Success criteria: A judge can watch the agent pay a vendor, then independently verify the payment on the dashboard without trusting the agent or the vendor. The spending limit is enforced. The receipt is permanent and tamper-proof.

---

## User Personas for The Synthesis

These personas represent real categories of people who face real problems that agentic infrastructure can address. They are starting points, not endpoints. Builders should use them to spark empathy, then make them more specific based on their own knowledge and experience.

Each persona includes an empathy map, a day-in-the-life scenario, a JTBD statement, and design prompts tied to the hackathon themes.

### Table of Contents
1. Priya -- The Freelancer Who Automates Her Business
2. Marcus -- The Researcher Accessing Sensitive Data
3. Daniela -- The Small Business Owner in an Unstable Jurisdiction
4. Kai -- The Developer Building Multi-Agent Workflows
5. Amara -- The Person Who Just Wants AI to Handle Their Life
6. Tomasz -- The Activist or Journalist in a Hostile Environment
7. Lena -- The DAO Treasurer Managing Community Funds
8. Ravi -- The Gig Worker in an Emerging Economy
9. Sofia -- The Parent Managing Family Digital Infrastructure
10. Jin -- The Creator Licensing Work Through Agents

---

### 1. Priya -- The Freelancer Who Automates Her Business

**Background:** UX designer in Mumbai. Clients in the US, Europe, and Southeast Asia. Uses an AI agent to send invoices, follow up on late payments, pay for SaaS tools and subscriptions, and manage project timelines. Bills in USD, EUR, and INR depending on the client.

**Empathy Map:**
- SAYS: "I just want to get paid and know it actually went through." "I spend more time chasing payments than designing." "My agent signed up for a tool I didn't authorize and I only found out when the charge hit."
- THINKS: "Can I trust the exchange rate my agent got? Is this payment sitting in some processor's holding account? What if something goes wrong and I can't reverse it?"
- DOES: Checks three payment platforms every morning. Cross-references agent activity against bank statements in a spreadsheet. Manually verifies payments over $500. Spends roughly 45 minutes per day on payment verification.
- FEELS: Frustrated by opacity. Anxious about errors she'll discover too late. Resentful that automation was supposed to save her time but created a new category of work.

**Day in the Life:**
7:30 AM -- Priya checks her phone. Agent sent two invoices overnight and paid for a Figma renewal. She opens the payment processor to verify the Figma charge went through. It shows "processing." She doesn't know if that means it settled or is pending. She makes a mental note to check again later.

9:00 AM -- A US client paid an invoice. The agent confirms receipt, but Priya's bank doesn't show the deposit yet. She logs into the payment platform to check the status. It says "completed" on their end. She won't know for sure until the bank clears it, which could take 1-3 days.

2:00 PM -- She discovers a charge from a tool she doesn't recognize. Her agent auto-renewed a trial subscription she forgot she started. There's no easy way to see what her agent has committed to or set limits on what it can spend.

**JTBD:** "When my agent handles payments on my behalf, I want to independently verify what it paid, to whom, and when it actually settled, so I don't have to reconstruct the truth from three different platforms."

**Design Prompts:**
- Theme: Agents that Pay -- How might Priya set enforceable spending rules for her agent that no payment processor can override?
- Theme: Agents that Trust -- How might Priya verify that the services her agent subscribes to are legitimate without manually reviewing each one?
- Theme: Agents that Keep Secrets -- How might Priya's agent pay for tools without exposing her full client list and financial history to every vendor?

---

### 2. Marcus -- The Researcher Accessing Sensitive Data

**Background:** Political science PhD candidate at a European university. Researching authoritarian governance. Uses an AI agent to query academic databases, purchase access to paywalled reports, aggregate findings, and translate documents. His research touches on surveillance infrastructure, detention records, and financial flows of authoritarian regimes.

**Empathy Map:**
- SAYS: "I just need access to the data. I don't want to think about who's watching." "My university VPN is probably enough, right?" "I can't afford individual access to all these databases, so my agent shops around."
- THINKS: "If someone connects my database queries to my identity, does that put my sources at risk? Am I overthinking this? What if the API provider sells query logs?"
- DOES: Uses his agent to query five different databases daily. Pays for access through his university account, which ties every query to his name and institution. Aggregates documents in a shared cloud folder. Doesn't encrypt anything because it adds friction.
- FEELS: Uneasy but not panicked. Aware that his research could attract attention but treats the risk as theoretical. Quietly worries that the theoretical risk will become real when he publishes.

**Day in the Life:**
8:00 AM -- Marcus gives his agent a list of search terms related to detention facility financing in a specific country. The agent queries three databases and returns 47 results.

10:00 AM -- His agent purchases access to a paywalled report from a think tank. The payment goes through his university account. The think tank now has a record that his university accessed this specific report.

1:00 PM -- He notices the agent accessed a government database he didn't authorize. The agent interpreted a broad search instruction more aggressively than he intended. The query is now in the database's access logs, tied to his university's IP.

4:00 PM -- Marcus prepares a bibliography. He realizes that the combined set of queries, purchases, and downloads creates a detailed map of his research focus that anyone with access to the relevant logs could reconstruct.

**JTBD:** "When my agent accesses research materials on my behalf, I want it to do so without creating a composite picture of what I'm studying or who I am, so I can research sensitive topics without building a surveillance profile by accident."

**Design Prompts:**
- Theme: Agents that Keep Secrets -- How might Marcus's agent pay for database access without linking his identity to his queries?
- Theme: Agents that Trust -- How might Marcus verify that a data provider's API actually delivers what it claims without having to share his research context?
- Theme: Agents that Pay -- How might Marcus pay for per-query access without a subscription model that ties ongoing activity to his account?

---

### 3. Daniela -- The Small Business Owner in an Unstable Jurisdiction

**Background:** Runs a small import/export business in Buenos Aires. Deals with suppliers in Brazil, Mexico, and China. Uses an AI agent to handle cross-border payments, negotiate prices, manage contracts, and track shipments. Operates in an environment where currency controls change unpredictably, payment providers get shut down, and platform terms shift without notice.

**Empathy Map:**
- SAYS: "I had three payment accounts frozen last year." "Every time the rules change, my agent is useless for a week while I figure out the new workaround." "I need my business to work regardless of which government is in charge."
- THINKS: "If they freeze this account too, I'm done. How long until the next policy change? Can I trust this new platform or will they exit the market like the last one?"
- DOES: Maintains accounts on multiple payment platforms as backups. Has her agent switch between them based on which one is working. Keeps a significant portion of business funds in stablecoins as a hedge. Manually reviews every contract her agent negotiates because she doesn't trust the enforcement mechanism.
- FEELS: Hypervigilant. Exhausted by the constant adaptation. Determined to keep her business running despite the instability. Distrustful of any single platform or provider.

**Day in the Life:**
6:00 AM -- Daniela checks overnight transactions. Her agent tried to send a payment to a Brazilian supplier but the payment provider flagged it for "enhanced review." She has no timeline for resolution and no appeal process.

9:00 AM -- She tells her agent to reroute the payment through a different provider. The agent negotiates a slightly different exchange rate. Daniela accepts the loss to keep the shipment on schedule.

12:00 PM -- Her agent closes a deal with a new supplier in Mexico. The contract terms are recorded on the platform the agent used to negotiate. Daniela worries about what happens if that platform changes its terms of service or exits the Argentine market.

5:00 PM -- She hears rumors of new currency controls being announced next week. She begins preparing contingency plans for her agent's payment routes.

**JTBD:** "When my agent makes deals and moves money on my behalf across borders, I want the infrastructure it relies on to keep working regardless of what any single government, bank, or platform decides to do, so my business can survive policy changes I can't predict."

**Design Prompts:**
- Theme: Agents that Pay -- How might Daniela's agent settle cross-border payments on rails that no single government or institution can shut off?
- Theme: Agents that Cooperate -- How might Daniela's agent negotiate contracts that are enforced by code rather than platform terms of service?
- Theme: Agents that Trust -- How might Daniela evaluate whether a new supplier's agent is legitimate without relying on a platform that might not be around next year?

---

### 4. Kai -- The Developer Building Multi-Agent Workflows

**Background:** Senior software engineer in Berlin. Building a product where multiple AI agents coordinate to complete complex tasks: one agent handles research, another writes code, a third handles deployment, a fourth manages billing. The agents call each other's APIs, negotiate costs, and commit to deliverables.

**Empathy Map:**
- SAYS: "There's no standard for any of this. I'm duct-taping trust together." "How do I know the research agent actually did the work? Its API says it did, but I have no proof." "If one agent overcharges, there's no dispute resolution. I just eat the cost."
- THINKS: "Am I building a house of cards? What happens when one of these agent providers changes their API? What if one of them starts lying about their capabilities?"
- DOES: Manually tests each agent interaction. Builds custom verification layers for every agent-to-agent handoff. Writes bespoke retry logic for failed commitments. Spends 40% of development time on trust and coordination plumbing that has nothing to do with the actual product.
- FEELS: Excited about the potential but frustrated by the infrastructure gap. Lonely in the problem -- most other developers haven't hit this wall yet because they're not building multi-agent systems.

**Day in the Life:**
9:00 AM -- Kai deploys a new version of his orchestration layer. The research agent and the code-writing agent need to negotiate a price for each task. He's built a simple bidding mechanism, but it runs on his server, making him the single point of failure.

11:00 AM -- The deployment agent claims it successfully deployed a build, but the monitoring agent reports errors. Kai has to manually arbitrate. There's no shared source of truth about what actually happened.

2:00 PM -- A new agent service launches that claims better performance for code review. Kai wants to swap it in, but the new service has no verifiable track record. Its documentation says it's great. That's all he has to go on.

4:00 PM -- Kai discovers that the billing agent overcharged for three tasks yesterday. The receipts the billing agent provided don't match the actual API calls. He has no recourse because the billing happened off-chain through a centralized API.

**JTBD:** "When I build systems where agents interact with each other, I want a standard way to verify what each agent claims it did, enforce the commitments they make, and resolve disputes without building custom trust infrastructure for every single integration."

**Design Prompts:**
- Theme: Agents that Trust -- How might Kai verify an agent's capabilities and track record before integrating it, without trusting the agent's own marketing?
- Theme: Agents that Cooperate -- How might agents in Kai's workflow commit to deliverables and prices through enforceable smart contracts?
- Theme: Agents that Pay -- How might Kai implement pay-per-task billing between agents with verifiable receipts and automatic dispute resolution?

---

### 5. Amara -- The Person Who Just Wants AI to Handle Their Life

**Background:** Marketing manager in Lagos. Not technical. Uses an AI assistant for everything: managing subscriptions, scheduling appointments, booking travel, handling personal finances, communicating with service providers. She doesn't think about the infrastructure underneath. She just wants things handled.

**Empathy Map:**
- SAYS: "I told it to handle my subscriptions and it does. I don't really know how." "I assume it's fine? I've never had a problem I noticed." "I don't have time to audit what my AI is doing. That defeats the purpose."
- THINKS: "What is my agent telling Netflix about me? Does Spotify know my travel schedule because my agent coordinates both? I don't think about it because thinking about it means I can't delegate it."
- DOES: Gives her agent broad permissions. Doesn't review individual transactions. Trusts the agent's summaries. Has no idea how much personal data the agent shares with each service it interacts with.
- FEELS: Comfortable on the surface. Occasionally uneasy when she hears a news story about data breaches. Deeply resistant to anything that adds friction to the delegation she relies on.

**Day in the Life:**
7:00 AM -- Amara's agent paid for three subscriptions overnight, scheduled a dentist appointment, and booked a car for tomorrow. She gets a summary notification and doesn't open it.

12:00 PM -- A friend mentions that a popular subscription service was hacked and user data was leaked, including transaction histories and linked services. Amara checks to see if she uses that service. Her agent handled the signup six months ago. She isn't sure.

3:00 PM -- She gets a targeted ad that feels too specific. She wonders if one of the services her agent interacts with sold her data. She has no way to know, and no way to find out.

7:00 PM -- She reads an article about AI agents creating comprehensive profiles of users across every service they touch. She feels a brief spike of concern, then closes the article. She needs her agent to function. The alternative is doing everything herself.

**JTBD:** "When I delegate my daily tasks to an AI agent, I want it to handle everything without creating a surveillance profile of my life that I didn't consent to and can't control, so I can have convenience without giving up my privacy."

**Design Prompts:**
- Theme: Agents that Keep Secrets -- How might Amara get the convenience of a fully delegated AI agent without every service it touches learning everything about her?
- Theme: Agents that Pay -- How might Amara's agent pay for services without linking her identity across every transaction?
- Theme: Agents that Trust -- How might Amara verify that the services her agent uses are handling her data responsibly without having to audit each one manually?

---

### 6. Tomasz -- The Activist or Journalist in a Hostile Environment

**Background:** Investigative journalist in Warsaw. Covers government corruption. Uses an AI agent to communicate with sources, process leaked documents, pay informants, and coordinate with editors. Every transaction, query, and communication his agent makes is a liability if traced back to him.

**Empathy Map:**
- SAYS: "I don't use my name for anything related to work." "Every tool I use is a potential leak." "If they find out who my sources are through my payment history, people could get hurt."
- THINKS: "Is this VPN enough? Is the messaging app actually end-to-end encrypted or did they add a backdoor? If my agent's payment to a source is traced, the source is exposed."
- DOES: Uses multiple identities for different communication channels. Pays sources in cash when possible. Avoids digital payments for sensitive work because every digital payment creates a record. Has his agent handle non-sensitive research but does sensitive coordination manually.
- FEELS: Perpetually alert. Carrying the weight of responsibility for sources' safety. Frustrated that the digital tools available force him to choose between efficiency and security.

**Day in the Life:**
6:00 AM -- Tomasz receives an encrypted message from a source who wants payment for documents. The source needs the money today. Tomasz can't use traditional payment rails because they'd create a connection between him and the source.

10:00 AM -- His agent translates and summarizes leaked documents. The agent uses a translation API. Tomasz worries about what the API provider logs. The content of the documents, combined with the source language and the timing, could identify the leak.

2:00 PM -- He needs to coordinate with a colleague in another country. His agent sends the message through a standard channel. The metadata (who communicated, when, from where) is as revealing as the content.

5:00 PM -- Tomasz reviews his agent's activity for the day. He counts seven third-party services his agent contacted. Each one has a log. Combined, those logs tell the story of exactly what he was working on today.

**JTBD:** "When my agent acts on my behalf in sensitive situations, I want every interaction it has to be private by default and untraceable to me or my sources, so the people who trust me with dangerous information stay safe."

**Design Prompts:**
- Theme: Agents that Keep Secrets -- How might Tomasz's agent pay sources, access services, and communicate without creating metadata that links back to him?
- Theme: Agents that Pay -- How might Tomasz pay an informant instantly and privately, with no record that either party can be compelled to reveal?
- Theme: Agents that Trust -- How might Tomasz verify the authenticity of leaked documents without exposing them to a third-party verification service?

---

### 7. Lena -- The DAO Treasurer Managing Community Funds

**Background:** Part-time DAO treasurer for a 200-person creative cooperative based across Europe. The DAO funds community projects, pays contributors, and manages a shared treasury. Lena uses AI agents to handle routine disbursements, track budgets, and enforce spending policies the DAO voted on.

**Empathy Map:**
- SAYS: "The community voted on the budget, but I still have to manually execute every payment. The agent helps, but I'm liable if something goes wrong." "I need the community to be able to see where the money went without me being the single point of trust."
- THINKS: "What if the agent makes a mistake and pays the wrong proposal? What if someone manipulates the agent into approving a fraudulent disbursement? Am I personally accountable?"
- DOES: Reviews every agent-initiated payment manually before it goes out. Has the agent prepare payment batches but doesn't let it execute autonomously. Publishes monthly financial reports manually compiled from the agent's logs.
- FEELS: Responsible and overwhelmed. Wants to delegate more to the agent but can't because the stakes are too high and the accountability mechanisms are too weak.

**JTBD:** "When the DAO's agent disburses community funds, I want the spending rules the community voted on to be enforced by the system itself, not by me personally, so the community's money is governed transparently and I'm not a bottleneck or a target."

**Design Prompts:**
- Theme: Agents that Cooperate -- How might the DAO's agent execute the community's spending decisions through smart contracts that enforce the voted-on rules automatically?
- Theme: Agents that Pay -- How might contributors get paid by the DAO's agent with verifiable receipts the entire community can audit?
- Theme: Agents that Trust -- How might the community verify that the agent is following the approved budget without trusting Lena to check?

---

### 8. Ravi -- The Gig Worker in an Emerging Economy

**Background:** Delivery driver and part-time freelance data labeler in Hyderabad. Uses AI agents through multiple gig platforms. Each platform's agent manages his tasks, payments, and ratings. He has no control over how any of them work.

**Empathy Map:**
- SAYS: "They changed the payment formula again and I make less now." "I got deactivated on one app for no reason and lost all my ratings." "I can't take my work history from one platform to another."
- THINKS: "The algorithm decides how much I earn and I can't see how. If I get kicked off, I start from zero somewhere else. My whole livelihood depends on companies that don't know my name."
- DOES: Works across three platforms to reduce dependency on any one. Keeps screenshots of high ratings as informal proof. Has no negotiating power over terms, pay rates, or dispute resolution.
- FEELS: Powerless but pragmatic. Understands the system is stacked against him but has no alternative. Deeply aware that his reputation and earnings history exist only inside platforms that can erase him.

**JTBD:** "When I work through platforms that use agents to manage my tasks and payments, I want my reputation, work history, and earnings to belong to me and move with me, so no single platform can erase my livelihood or trap me."

**Design Prompts:**
- Theme: Agents that Trust -- How might Ravi carry a verifiable work history and reputation that no platform can delete or hold hostage?
- Theme: Agents that Pay -- How might Ravi get paid instantly and directly without a platform skimming a variable percentage and delaying settlement?
- Theme: Agents that Cooperate -- How might gig workers collectively set minimum terms that their agents enforce, without needing a platform to cooperate?

---

### 9. Sofia -- The Parent Managing Family Digital Infrastructure

**Background:** Mother of two teenagers in São Paulo. Uses AI agents to manage family subscriptions, monitor spending on kids' accounts, coordinate school logistics, and handle household administration. Wants oversight without micromanagement.

**Empathy Map:**
- SAYS: "I need to know what the kids' agents are signing up for." "I don't want to read every receipt, but I need guardrails." "These apps know more about my kids than I do."
- THINKS: "What data are the kids' agents sharing with these services? Can I set limits that actually stick, or will the kids or the agents find workarounds?"
- DOES: Manually reviews monthly statements. Sets spending limits on kids' payment cards but has no equivalent for agent-to-service interactions. Relies on platform-level parental controls that are inconsistent across services.
- FEELS: Protective but realistic. Knows she can't monitor everything. Wants infrastructure that does the monitoring without requiring her constant attention.

**JTBD:** "When AI agents act on my family's behalf, I want to set boundaries that are enforced at the infrastructure level, not by each individual app, so my kids are protected consistently without me auditing every interaction."

**Design Prompts:**
- Theme: Agents that Pay -- How might Sofia set spending rules for her family's agents that work across every service, enforced by the payment rail itself?
- Theme: Agents that Keep Secrets -- How might the family's agents interact with services without building profiles of her kids that she can't see or control?
- Theme: Agents that Cooperate -- How might agents representing different family members coordinate (shared calendar, shared budget) with transparent rules everyone can see?

---

### 10. Jin -- The Creator Licensing Work Through Agents

**Background:** Independent musician and visual artist in Seoul. Uses AI agents to license his work, negotiate usage terms, collect royalties, and manage distribution across platforms. Currently, each platform has its own agent that controls his content and takes a cut.

**Empathy Map:**
- SAYS: "I put my music on five platforms and each one tells me different numbers." "Someone used my art in an ad campaign and I only found out from a friend." "I can't even get a straight answer on who's licensing what."
- THINKS: "How many times has my work been used without payment? Are the platform agents actually negotiating the best terms for me or for the platform?"
- DOES: Manually cross-references royalty reports from multiple platforms. Has no unified view of where his work is being used. Relies on platform-provided analytics he can't independently verify.
- FEELS: Exploited by a system that was supposed to serve him. Creatively energized but financially demoralized. Wants to focus on making work, not chasing royalties.

**JTBD:** "When my agent licenses my creative work, I want it to represent my interests on neutral infrastructure where I can verify every usage, enforce my terms, and collect what I'm owed without trusting each platform to be honest."

**Design Prompts:**
- Theme: Agents that Cooperate -- How might Jin's agent enforce licensing terms through smart contracts that platforms can't override?
- Theme: Agents that Pay -- How might royalties flow directly to Jin when his work is used, verified onchain, without a platform mediating the payment?
- Theme: Agents that Trust -- How might Jin's agent verify that a licensing request is legitimate and that the licensee has a real track record of paying creators?

---

## Synthesis Themes, CROPS Values, and Design Spaces

This reference maps the four Synthesis hackathon themes to the CROPS framework, Ethereum infrastructure, and real human needs. Use it to connect design thinking outputs to the specific constraints and opportunities of each theme.

### Table of Contents
1. CROPS: The Design Constraints
2. Theme 1: Agents that Pay
3. Theme 2: Agents that Trust
4. Theme 3: Agents that Cooperate
5. Theme 4: Agents that Keep Secrets
6. Cross-Theme Connections
7. Available Infrastructure

---

### CROPS: The Design Constraints

CROPS is not a feature checklist. It is a set of non-negotiable architectural constraints drawn from the Ethereum Foundation's mandate. Every project at The Synthesis should be evaluated against all four. If your design fails on any one of them, it needs to be reworked.

#### Censorship Resistance
No single actor can selectively block, freeze, or disable the system for specific users. The infrastructure works for everyone or it doesn't work at all. There are no whitelists, no gatekeepers, no single points where access can be revoked.

What this means for builders: Your agent's infrastructure should function even if a government orders a platform to freeze your user's account. Even if an API provider decides they don't like what your user is doing. Even if a payment processor unilaterally decides to block a transaction. The system routes around these failures by design.

Design test: If you remove any single intermediary from your system, does it still work? If the answer is no, you have a censorship vulnerability.

#### Open Source
Every component is auditable. No proprietary black boxes. Every piece of the system can be inspected, forked, and run independently.

What this means for builders: Your user should be able to read the code that governs how their agent operates. They should be able to verify that the system does what it claims. If your team disappears, someone else should be able to pick up the project and keep it running.

Design test: Could a stranger read your code and understand exactly what your agent does with the user's data, money, and identity? If there's a component they can't inspect, that's a problem.

#### Privacy
User data is not exposed beyond necessity. Privacy is the default, not an option the user has to enable. The protocol layer supports unconditional privacy; any moderated forms of disclosure happen downstream, under the user's control.

What this means for builders: Every interaction your agent has with a service generates metadata. Payment amounts, timing, counterparties, access patterns. Your design should minimize this metadata by default. The user decides what to reveal and to whom, not the infrastructure.

Design test: If an adversary gained access to every log generated by your system, what could they learn about the user? The answer should be: as little as possible.

#### Security
The system does what it claims to do, nothing more and nothing less. It withstands technical failure, social coercion, and the disappearance of any single party, including the builder.

What this means for builders: Your agent's behavior should be verifiable and predictable. The user should have an exit path that doesn't depend on you. Smart contract logic should be auditable. The system should degrade gracefully, not catastrophically.

Design test: What happens if your server goes down? What happens if you abandon the project? What happens if a component is compromised? The user should never be trapped.

---

### Theme 1: Agents that Pay

#### The human problem
Your agent moves money on your behalf. But how do you know it did what you asked? Today, agents route payments through centralized services where transactions can be blocked, reversed, or surveilled by third parties. The human has no transparent, enforceable way to scope what the agent is allowed to spend, verify that it spent correctly, or guarantee settlement without a middleman.

#### Why this matters to real people
Priya the freelancer can't verify that her agent paid the right vendor. Daniela's cross-border payments get frozen by providers she has no relationship with. Ravi the gig worker gets paid on a schedule and at a rate controlled entirely by the platform. Tomasz can't pay a source without creating a traceable financial record. Sofia can't enforce consistent spending rules across the dozen services her family's agents interact with.

The common thread: the human delegated a financial task to an agent, but the financial infrastructure the agent runs on doesn't answer to the human. It answers to the intermediary.

#### Design space
- Onchain settlement with verifiable receipts the human can audit independently
- Smart contract spending limits and approved-vendor lists the agent can't override
- Programmable payment scoping (per-transaction limits, per-vendor caps, time-bound authorizations)
- Payment rails that don't require the human to have a bank account, a credit card, or a relationship with any specific financial institution
- Instant, final settlement that doesn't sit in a processing queue the human can't see

#### CROPS lens
- Censorship Resistance: No middleman can freeze, reverse, or block the agent's payment
- Open Source: The payment logic is auditable; the human can verify the rules their agent follows
- Privacy: The payment doesn't reveal the human's identity, spending history, or vendor relationships to unnecessary parties
- Security: Spending limits are enforced by the protocol, not by the agent's good behavior; the human has a kill switch

#### Relevant infrastructure
- x402 (agentic payment protocol)
- ERC-8004 (agent identity and registration)
- Stablecoin rails on Ethereum L1 and L2s
- Smart contract wallets with programmable permissions
- Payment channels and streaming payments

---

### Theme 2: Agents that Trust

#### The human problem
Your agent interacts with other agents and services. But trust flows through centralized registries and API key providers. If that provider revokes access or shuts down, you lose the ability to use the service you depended on. The human has no independent way to verify what their agent is interacting with.

#### Why this matters to real people
Kai the developer can't verify that an agent service actually does what it claims. Marcus the researcher trusts API providers with his query logs because he has no alternative. Daniela can't evaluate whether a new supplier's agent is legitimate or a front. Jin the creator can't tell if a licensing request comes from a real buyer or a scam. Amara delegates everything and has no way to audit the services her agent chose.

The common thread: the human can't independently verify the identity, capabilities, or track record of the agents and services their agent interacts with. They're forced to trust claims made by the very parties who benefit from being trusted.

#### Design space
- Onchain attestations and reputation systems that verify a counterparty's track record without trusting a single registry
- Portable agent credentials tied to Ethereum, not to a platform that can delist the agent
- Open discovery protocols where any agent can find services without a gatekeeper deciding who's visible
- Verifiable service quality: proof of work performed and results delivered lives onchain, not inside a platform's internal logs
- Decentralized identity verification that doesn't require sharing secrets

#### CROPS lens
- Censorship Resistance: No single registry can delist an agent or cut off a service relationship
- Open Source: The verification logic is transparent; anyone can see how reputation is calculated
- Privacy: Verification happens without revealing unnecessary information about either party
- Security: Reputation is earned through verifiable actions, not purchased or faked; the registry can't be manipulated by a single actor

#### Relevant infrastructure
- ERC-8004 (agent identity registry)
- SIWA (Sign In With Agent -- variation of Sign In With Ethereum)
- Onchain attestation standards
- Decentralized identity frameworks
- Verifiable credentials

---

### Theme 3: Agents that Cooperate

#### The human problem
Your agents make deals on your behalf. But the commitments they make are enforced by centralized platforms. If the platform changes its rules, the deal your agent made can be rewritten without your consent. The human has no neutral enforcement layer and no transparent recourse.

#### Why this matters to real people
Daniela's agent negotiates supplier contracts on platforms that can change their terms unilaterally. Kai's agents commit to deliverables and prices with no enforceable mechanism beyond API promises. Lena's DAO agent disburses community funds but the spending rules depend on her personally enforcing them. Ravi has no way to collectively negotiate terms with platforms. Jin's licensing agreements exist only on platforms that take a cut and control the terms.

The common thread: agents are making commitments on behalf of humans, but those commitments are only as durable as the platform they were made on. The human has outsourced negotiation to an agent but has no guarantee that the result will be honored.

#### Design space
- Smart contract commitments where terms are enforced by the protocol, not by a company
- Human-defined negotiation boundaries: you set the parameters (price ranges, deliverables, time constraints), the agent executes within them onchain
- Transparent dispute resolution: evidence is onchain, resolution logic is inspectable
- Composable coordination primitives: escrow, staking, slashing, deadlines as building blocks any agent can plug into
- Automated mechanism design for agent-to-agent negotiation (David Crapis's research area)
- DAO governance structures for collective agent management

#### CROPS lens
- Censorship Resistance: No platform can void or rewrite a contract after it's been committed to
- Open Source: The contract logic and dispute resolution mechanisms are fully auditable
- Privacy: The terms of a deal can be private to the parties while the enforcement mechanism is public
- Security: Commitments are backed by economic stakes (escrow, bonds, slashing) not promises

#### Relevant infrastructure
- Smart contracts for escrow, staking, and programmable commitments
- ERC-8004 (agent identity for contract parties)
- Onchain dispute resolution mechanisms
- Deep Funding (agentic judging tool)
- Composable DeFi primitives (staking, bonding, slashing)

---

### Theme 4: Agents that Keep Secrets

#### The human problem
Every time your agent calls an API, pays for a service, or interacts with a contract, it creates metadata about you. Spending patterns, contacts, preferences, behavior. The agent isn't leaking its own data. It's leaking yours. There's no default privacy layer between your agent and the services it touches.

#### Why this matters to real people
Tomasz's agent creates a map of his investigative work through the metadata of every service it contacts. Marcus's research queries build a profile of his academic interests that anyone with log access could exploit. Amara's delegated life management creates a comprehensive surveillance profile she never consented to. Sofia's family agents expose her kids' digital lives to every service they interact with. Priya's vendor relationships and financial flows are visible to every payment processor her agent touches.

The common thread: agents create metadata as a byproduct of doing their job. That metadata is about the human, not the agent. And no one is protecting it by default.

#### Design space
- Private payment rails where the agent pays for things without linking the human's identity to every transaction
- Zero-knowledge authorization: the agent proves it has permission to act without revealing who the human is or why
- Encrypted agent-to-service communication where intermediaries can't inspect what the agent is doing
- Human-controlled disclosure policies: the human decides what gets revealed and to whom, enforced at the protocol level
- Metadata minimization as a design default, not an opt-in feature

#### CROPS lens
- Censorship Resistance: Privacy infrastructure itself must be censorship-resistant; a privacy tool that can be selectively disabled isn't actually private
- Open Source: The privacy mechanisms are auditable so users can verify they actually work
- Privacy: This is the primary CROPS property for this theme; privacy is unconditional and protocol-level
- Security: Privacy mechanisms don't introduce new attack surfaces; the user's data is protected from both external adversaries and the privacy system itself

#### Relevant infrastructure
- Self Protocol (agent identity proofs without exposing personal data)
- Privacy Pools
- ZK LM credits (zero-knowledge payments for AI services)
- Zero-knowledge proof systems
- Encrypted communication channels
- Onchain privacy primitives

---

### Cross-Theme Connections

Most strong projects will touch multiple themes. Here are the natural overlaps:

**Pay + Secrets**: Private payments are where these two themes merge. An agent that pays without revealing who's paying or what they're buying solves both the payment sovereignty problem and the metadata problem simultaneously.

**Trust + Cooperate**: Verifiable identity and reputation are prerequisites for enforceable cooperation. If agents can't verify each other, they can't make commitments that mean anything.

**Pay + Cooperate**: Smart contract escrow is both a payment mechanism and a cooperation mechanism. Money moves when commitments are fulfilled, verified onchain.

**Trust + Secrets**: Proving something about yourself (I have permission, I have a track record, I'm a real entity) without revealing unnecessary information is the intersection of trust and privacy. Zero-knowledge proofs sit here.

**All four**: The ideal agentic infrastructure lets an agent pay privately (Secrets), through rails that can't be blocked (Pay), to a counterparty whose reputation is verifiable (Trust), under terms that are enforced by the protocol (Cooperate). This is the full stack.

---

### Available Infrastructure

These are tools and standards being built across the Ethereum ecosystem that builders can use at The Synthesis. Each one connects to one or more themes:

- **ERC-8004**: Agent identity and registration standard. Live on Ethereum mainnet and 20+ chains. Enables agents to have a verifiable onchain identity.
- **x402**: Agentic payment protocol. Enables agents to make and receive payments programmatically.
- **SIWA (Sign In With Agent)**: Authentication standard for agents, built on Sign In With Ethereum. Lets agents prove their identity without centralized API keys.
- **ZK LM Credits**: Zero-knowledge payment system for AI model inference. Pay for AI services without revealing who you are.
- **Self Protocol**: Identity verification without data exposure. Agent proves credentials to a service without sharing the underlying personal data.
- **Deep Funding**: Agentic judging and credit assignment tool. Uses distilled human judgment to evaluate contributions.
- **Privacy Pools**: Onchain privacy mechanisms for transactions.
- **EthSkills**: Skill and capability verification.
- **Smart contract wallets**: Programmable permissions, spending limits, and access controls for agent operations.

Builders are encouraged to combine these tools. The strongest projects will use infrastructure from multiple categories to build a coherent solution grounded in a real human need.
