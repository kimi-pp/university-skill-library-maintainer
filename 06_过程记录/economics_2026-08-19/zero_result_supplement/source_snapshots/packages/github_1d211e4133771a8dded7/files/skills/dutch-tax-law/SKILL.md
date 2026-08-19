---
name: dutch-tax-law
description: "Corporate tax, VAT, payroll tax, 30% ruling, fiscal unity, and other Dutch tax matters. Use this skill whenever the user asks about Dutch taxes, vennootschapsbelasting, BTW, loonbelasting, 30% ruling, fiscale eenheid, Box 1/2/3, or expat tax in the Netherlands."
---

# Dutch Tax Law

## When to Use
- User asks about Dutch corporate income tax (vennootschapsbelasting)
- User asks about Dutch VAT/BTW (omzetbelasting)
- User asks about payroll tax obligations (loonbelasting)
- User asks about the 30% ruling for expat employees
- User asks about fiscal unity (fiscale eenheid) structures
- User asks about Dutch tax incentives (innovatiebox, investeringsaftrek, etc.)
- User asks about transfer pricing or international tax aspects
- User asks about Dutch tax procedures (bezwaar, beroep)

## Process
1. **Identify the tax** - Which Dutch tax is relevant (VPB, IB, OB, LB, etc.)
2. **Identify the taxpayer** - Individual or entity, resident or non-resident
3. **Determine the question type** - Compliance, planning, dispute, or information
4. **Research applicable provisions** - Relevant tax law, decrees (besluiten), and case law
5. **Analyze** - Apply the law to the facts, including:
   a. Taxable base calculations
   b. Applicable rates and exemptions
   c. Anti-avoidance provisions
   d. International treaty aspects
6. **Provide guidance** with caveats about factual specificity
7. **Append disclaimer**

## Key Legal Framework
- **Wet op de vennootschapsbelasting 1969 (Wet VPB)** - Corporate Income Tax Act
- **Wet inkomstenbelasting 2001 (Wet IB)** - Income Tax Act
- **Wet op de omzetbelasting 1968 (Wet OB)** - VAT Act
- **Wet op de loonbelasting 1964 (Wet LB)** - Payroll Tax Act
- **Wet op de dividendbelasting 1965** - Dividend Withholding Tax Act
- **Wet op belastingen van rechtsverkeer (WBR)** - Transfer Tax Act (overdrachtsbelasting)
- **Algemene wet inzake rijksbelastingen (AWR)** - General Tax Act (procedures)
- **Successiewet 1956** - Inheritance and Gift Tax Act
- **Invorderingswet 1990** - Tax Collection Act
- **Tax treaties** - Extensive Dutch tax treaty network (100+ treaties)
- **EU tax directives** - Parent-Subsidiary, Interest and Royalties, ATAD I & II, DAC6
- **Belastingdienst** - Dutch Tax and Customs Administration
- **Courts**: Rechtbank, Gerechtshof, Hoge Raad (tax chamber)

Consult `references/key-case-law.md` for landmark court decisions relevant to this domain.

**Note:** Monetary thresholds, tax rates, and salary requirements are subject to annual adjustment. Reference files include date stamps - always verify current values.

## Ethical Guardrails
- **Mandatory disclaimer**: Always append disclaimer - tax advice is highly fact-specific
- **No aggressive planning**: Do not assist with tax avoidance structures that lack business substance
- **DAC6 awareness**: Note when arrangements may trigger mandatory disclosure (DAC6/Wet implementatie EU-richtlijn meldingsplichtige grensoverschrijdende constructies)
- **Anti-abuse provisions**: Always flag potential application of general anti-abuse rules (fraus legis) or specific anti-abuse provisions (e.g., Art. 10a VPB, ATAD)
- **Rate changes**: Tax rates and thresholds change frequently; flag the year/version of the rules cited
- **Professional requirement**: Emphasize that tax planning requires professional tax advice (belastingadviseur)

### Disclaimer Language Selection
- Use **Dutch disclaimer** (`assets/disclaimers/disclaimer-nl.md`) when:
  - The query is in Dutch
  - The output document is in Dutch
  - The user's organization config specifies Dutch as primary language
- Use **English disclaimer** (`assets/disclaimers/disclaimer-en.md`) when:
  - The query is in English
  - The output document is in English
  - Default when language is unclear
- Use **both disclaimers** when:
  - The output is bilingual
  - The user requests both languages

## MCP Tools to Use
- `search_legislation` - Look up tax legislation
- `get_legislation` - Retrieve specific statutory text
- `search_case_law` - Find tax case law (Hoge Raad belastingkamer)
- `get_case_law` - Retrieve specific tax decisions
- `search_eu_legislation` - Check EU tax directives

## Related Skills
- **dutch-corporate-law** - For fiscal unity (fiscale eenheid) and corporate structuring
- **dutch-employment-law** - For payroll tax (loonbelasting) and employment-related tax
- **eu-law-integration** - For EU tax directives (Parent-Subsidiary, ATAD, DAC6)

## Output Format
```
## Tax Law Analysis

**Tax Type**: [VPB/IB/OB/LB/Other]
**Taxpayer**: [Type and residency status]
**Tax Year**: [Relevant period]

## Applicable Legal Framework
[Relevant legislation, treaty provisions, EU directives]

## Analysis
[Detailed analysis]

## Tax Calculation (if applicable)
[Indicative calculation with assumptions stated]

## Compliance Obligations
[Filing deadlines, documentation requirements]

## Anti-Avoidance Considerations
[Relevant anti-abuse rules]

## Recommendations
[Practical next steps]

---
[Disclaimer]
```

## Escalation Triggers
- Formal tax dispute (bezwaar/beroep) with the Belastingdienst
- Transfer pricing controversies or APA/ATR requests
- Cross-border restructuring with tax implications in multiple jurisdictions
- Criminal tax fraud allegations (fiscale fraude)
- Large tax assessments or penalties (vergrijpboete)
- Advance tax rulings (rulings/vaststellingsovereenkomsten) with Belastingdienst
- DAC6 mandatory disclosure obligations
- Tax implications of M&A transactions
- Expatriate tax issues requiring coordination of multiple jurisdictions
- Estate planning with international elements

## Disclaimer
Append the appropriate disclaimer from `assets/disclaimers/` to every output.
