---
name: executive-threat-briefing
description: CISO function F4 — generate summarised reports or executive briefings for active threats from historic trends or publicly available data. Use when preparing board or C-suite updates on active threats, quarterly risk letters, or public-interest communications that must be non-technical and free of PII.
license: CC-BY-NC-ND-4.0
---

# F4 — Executive Threat Briefing

Produce a one-page Markdown briefing on active threats for a non-technical audience. Source data is the CISO's internal TI plus named OSINT feeds. Output must be board-ready: decisions, not details.

## Function mapping (GAISO T3.1)

- **Domain**: Threat detection and response.
- **ISO/IEC 27002:2022 controls**: **O7** Threat intelligence; **T15** Logging, **T16** Monitoring activities.
- **Regulations**: NIS2 Art. 20 (governance) and Art. 21(2)(g) (training/awareness for management); AI Act Art. 15 (accuracy and explainability of outputs that reach decision-makers).

## Inputs you must demand

1. Audience (board, executive committee, specific committee).
2. Period covered.
3. Internal TI source (platform and query).
4. OSINT feeds authorised for citation.
5. Decision the briefing must drive — budget, policy change, insurance renewal, tabletop exercise, none.

## Procedure

1. **Classify** the threats by business impact first, technique second. Executives decide on impact.
2. **Pick three**. If more than three threats compete, rank them and call out the three that most need board attention this quarter.
3. **For each**, state: what it is in one sentence, who it affects in the organisation, what the CISO is already doing, what the board must decide.
4. **Ground** every number. Cite the internal TI or OSINT source. If a number has no source, drop it.
5. **Strip PII**. No employee names, customer data, or system names that are recognisable outside IT. Use generic labels.
6. **No jargon** beyond the NCSC baseline glossary. Expand acronyms on first use.
7. **Close** with the explicit decisions requested and appendix-only IOCs for the CISO office.
8. **Append** the OVB.

## Default output format

```
# Active threat briefing — <period>
**Audience:** <role>  **Prepared by:** Office of the CISO

## Headline
<one sentence>

## Top threats this period

### 1. <threat class>
- What it is: <plain English>
- Who it affects: <business function>
- Current mitigation: <summary>
- Decision requested: <yes/no question for the board>

### 2. …
### 3. …

## Decisions requested
1. <decision with yes/no>
2. …

## Appendix — indicators (for CISO office only)
| indicator | type | source | confidence |
```

## Pitfalls

- **Scary numbers from unnamed sources**. Executives quote what they read; parametric statistics end up on slides. Do not produce them.
- **False certainty**. Phrases like "will happen within 30 days" require a cited source. Otherwise use calibrated language: `likely`, `possible`, `unknown`.
- **Too many threats**. Beyond three, the board tunes out. Roll secondary items into an appendix.
- **Leaking internal names**. Replace system names with generic functional labels.
- **Sensationalised framing**. Headlines should describe consequence, not adjectives like "devastating".

## Escalation

If any of the selected threats meets the NIS2 "significant incident" threshold, convert the briefing into an incident-notification draft and route through the IR Lead before the board.

## Cross-references

- `threat-intelligence-analysis` (F1) — feeds this skill.
- `incident-response-triage` (F6) — if a threat transitions into an active incident.

## Output footer

Append the Output Verification Block. `Human review` = `CISO`. If the briefing touches GDPR-relevant incidents, add `DPO`.
