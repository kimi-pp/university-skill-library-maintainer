# User Personas for The Synthesis

These personas represent real categories of people who face real problems that agentic infrastructure can address. They are starting points, not endpoints. Builders should use them to spark empathy, then make them more specific based on their own knowledge and experience.

Each persona includes an empathy map, a day-in-the-life scenario, a JTBD statement, and design prompts tied to the hackathon themes.

## Table of Contents
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

## 1. Priya -- The Freelancer Who Automates Her Business

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

## 2. Marcus -- The Researcher Accessing Sensitive Data

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

## 3. Daniela -- The Small Business Owner in an Unstable Jurisdiction

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

## 4. Kai -- The Developer Building Multi-Agent Workflows

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

## 5. Amara -- The Person Who Just Wants AI to Handle Their Life

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

## 6. Tomasz -- The Activist or Journalist in a Hostile Environment

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

## 7. Lena -- The DAO Treasurer Managing Community Funds

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

## 8. Ravi -- The Gig Worker in an Emerging Economy

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

## 9. Sofia -- The Parent Managing Family Digital Infrastructure

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

## 10. Jin -- The Creator Licensing Work Through Agents

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
