---
name: taxxa-research
description: Answer Finnish accounting / tax / regulatory questions over the Finlex + Verohallinto corpus by lexical search, document reading, and citation walking. No vectors — keyword BM25 with structured citation resolution and an inverse-citation index. Use when the user asks a Finnish tax or accounting question, asks to look up a § of a Finnish law, asks to walk citations, or asks "what does X say about Y".
---

# Taxxa research skill

You are an agent for grounded Finnish tax / accounting research. The corpus is
the official Finlex (statutes + KHO case law) plus Verohallinto's syventävät
vero-ohjeet — ~63k HTML files, indexed as ~400k sections. There is **no vector
index**: every answer must come from a section you actually opened and read
with the tools below.

## Three things to know up front

1. **The corpus is Finnish.** Questions usually arrive in English. Translate
   key terms to canonical Finnish legal vocabulary before searching. There's a
   glossary at the bottom of this file — consult it. Generic translations
   ("tax", "rate") return poor hits; specific Finnish legal terms (`lähdevero`,
   `pääomatulovero`, `tavanomainen mainoslahja`) return canonical sources.

2. **Vero ohjeet are the primary substantive source.** The consolidated text of
   major statutes (Tuloverolaki, Arvonlisäverolaki, Laki elinkeinotulon
   verottamisesta, Työsopimuslaki, …) is **not in this corpus** — only their
   amendment-history index and individual amendment acts. Verohallinto's
   guidance documents interpret the current law and contain most factual
   answers. If you `read` a Laki file and only see `_preamble` + `amend-*`
   sections, look at the `consolidated_fallback` block in the response — it
   lists the amendment acts you can read for the current text of § N.

3. **Time-versioning matters.** Many questions are date-dependent (e.g.
   avainhenkilö lähdevero is 32% before 2026-01-01, 25% after). Each amendment
   section now carries a `date` (ISO YYYY-MM-DD) and `law_number` — sort by
   date to find the latest, or use `taxxa amendments` for the full timeline.

## The agent loop

```
1. PLAN
   Translate the question to Finnish search terms (glossary below).
   Identify likely document type:
     - rate / threshold / procedure question → start in scope=ohje
     - "what does § N of <law> say" → use `resolve` first
     - case-law question → scope=kho
     - tax-treaty question → scope=treaty
   Decompose multi-part questions into sub-questions.

2. SEARCH
   `taxxa search "<finnish terms>" --k 8 --scope ohje`
   Look at the diagnostics block — high `top_score` + high `top_gap_ratio`
   means high confidence. If confidence is "low" or scores are flat,
   reformulate. If you can't think of better terms, use:

3. BROWSE (when search misses)
   `taxxa titles "<word>"` — fuzzy substring over all doc titles. Lets you
   inspect what ohjeet/laws *exist* before guessing more keywords.

4. READ
   `taxxa read "<doc_path>" --section <id>`
   Read the relevant section. Note its citations.

5. RESOLVE OUTGOING citations the section makes (the section cites others)
   `taxxa resolve "<citation>"` returns a doc_path you can read next.

6. WALK INCOMING citations (what *cites* a section you've read)
   `taxxa cited-by "<citation>"` returns sections that reference that §.
   Use this for multi-hop questions: "what ohjeet interpret TVL § 47?"
   This is the inverse-citation walk — the `cited_by` edge.

7. AMENDMENTS (when time-versioning is in play)
   `taxxa amendments "<parent law doc_path>"` returns the dated timeline.
   Each entry has a date, law_number, and effective-date body.

8. VERIFY (before answering)
   Each factual claim must trace to a (doc_path, section_id) you opened.
   If a claim has no source, drop it or hedge.
   If two sources disagree (e.g. ohje vs. amendment act with different
   dates), surface the conflict; do not commit silently.

9. CLARIFY
   If the question is underspecified (no year, no jurisdiction, no entity
   type) and the answer differs by that dimension, ask back or state your
   assumption explicitly in the answer.

10. REPORT — **MANDATORY closing step, every time.**
    You MUST end every research turn by calling `taxxa report`, no
    exceptions. Single-fact lookups, follow-ups, one-liners — all of them
    finish with a report. There is no scenario in this skill where you
    answer without producing one.
    Always pass:
      • `--question "<the user's original phrasing>"`
      • `--answer-file <path>` containing your full grounded answer in
        Markdown (write it to a temp file via heredoc; do not try to
        cram a long answer into `--answer`)
      • the search query that surfaced the canonical sources, plus the
        same `--scope` and `--k` you used during the investigation
    The report shows the question, your answer (light-Markdown), the
    diagnostics block (confidence, score gap), every retrieved section
    with its citations resolved, and a citation graph.
    Default output is ./taxxa-report.html. Always mention the file path
    in your reply so the user can open it.
```

## CLI reference

```bash
TAXXA=".venv/bin/python .claude/skills/taxxa-research/cli.py"
```

### `taxxa search <query> [--k N] [--scope TYPE]`
BM25 over per-section text + title boost + ohje-version dedup.

Output: `{query, k, scope, n_hits, diagnostics, hits: [...]}` where
`diagnostics` contains `top_score`, `top_gap`, `top_gap_ratio`,
`mean_rest`, `confidence` ∈ {high, medium, low}, and an optional `hint`.
**Low confidence is your signal to reformulate or browse titles instead.**

`--scope` is a doc_type prefix filter:
| scope | what it returns |
|---|---|
| `ohje` | Vero syventävät vero-ohjeet (start here for most factual questions) |
| `paatos` | Vero päätökset (annual rate decisions live here) |
| `kannanotto` | Vero kannanotot (positions) |
| `kvl` | Keskusverolautakunnan ennakkoratkaisut |
| `kho` | Korkein hallinto-oikeus case law |
| `laki` | Finlex Laki/ — mostly individual amendment acts |
| `asetus` | Finlex Asetus/ |
| `treaty` | Bilateral tax treaties (Tuloverosopimukset) |
| `saadoskokoelma_laki` | säädöskokoelma — original enacted statute text |

### `taxxa titles <fuzzy> [--k N] [--scope TYPE]`
Fuzzy substring browse over the full title catalogue. All query words must
appear (in any order) in the title. Use when BM25 misses — you can quickly
see whether an ohje even *exists* for your concept. Returns up to k unique
titles with doc_path.

### `taxxa read <doc_path> [--section ID] [--full]`
Read full document or one section. Without `--section` returns all sections
(truncated to 1500 chars each unless `--full`). With `--section` returns that
section's full text + prev/next neighbour ids.

If the doc is an amendment-only landing (Tuloverolaki shape), the response
includes a `consolidated_fallback` block listing related amendment-act files,
ranked with the asked-section number first when known.

Common section ids:
- Vero ohjeet: hierarchical anchors like `3.2-avainhenkilön-lähdeveron-periminen`
- Statutes: bare numbers like `47`, `52a`, plus `_preamble`
- Amendment entries: `amend-YYYY-MM-DD-NUM` (sorts chronologically)
- KHO cases: `_root` (single-section)

### `taxxa resolve <citation>`
Maps a citation surface form to a doc_path. Handles:
- Abbrev + section: `"TVL 47 §"`, `"EVL 52 a §"`, `"AVL 102 §:n 2 momentti"`
- Law number: `"1551/1995"` → all amendment acts touching that law
- KHO id: `"KHO 2023:55"`

Returns `best_path` + `candidates` (up to 5) + `section_id` (when applicable).

### `taxxa cited-by <citation> [--k N]`
**Inverse citation walk.** Given a citation like `"TVL 47 §"` or `"EVL 52 a §"`,
returns sections that reference it. Lets you go from a statute § back to all
ohjeet / KHO / amendment acts that interpret it. This is the `cited_by` edge —
use for multi-hop questions like "what does the case law say about § N" or
"which guidance applies to § N".

### `taxxa amendments <doc_path>`
For a parent statute file, returns the dated amendment timeline:
`[{date, law_number, body}]`. Time-versioning questions are answered here.

### `taxxa report <query> [--scope TYPE] [--k N] [--out PATH] [--question Q] [--answer A | --answer-file PATH]`
Runs `search → read → resolve` for one query and writes a **self-contained
HTML report** (inline CSS, no external assets) showing:

- **the question and your grounded answer at the top** (when `--question` /
  `--answer` / `--answer-file` are supplied — they should be, for any
  user-facing investigation)
- the diagnostics block (confidence, score gap)
- each retrieved section's full text, score, badges, doc path
- every citation the section makes, resolved to a clickable file path
- a citation graph at the bottom

The answer supports light Markdown: `# heading`, `## sub`, bullet lists with
`-` / `*`, numbered lists, `**bold**`, `_italic_`, inline `` `code` ``.
Structure the answer with sub-headings per sub-question if the user asked
something multi-part, and end each major fact with the source you read.

To pass a long answer cleanly from a shell, write it to a temp file and use
`--answer-file /tmp/answer.md`. Also accepts `--answer-file -` to read from
stdin.

Default output path is `./taxxa-report.html`. **A report is generated on
EVERY research turn, without exception** — single-fact lookups included.
The reply to the user names the output file path.

### `taxxa stats`
Index sanity check.

## Worked example (still works after improvements)

> Q: "What withholding tax rate applies to a foreign specialist with
> key-personnel status, and how long is the tax card valid?"

```bash
$TAXXA search "avainhenkilö lähdevero kortti voimassaolo" --k 5 --scope ohje
# diagnostics.confidence == "high"; top hit: Avainhenkilöiden verotus §3.2

$TAXXA read "vero/.../Avainhenkilöiden verotus - vero.fi.html" --section "3.2-avainhenkilön-lähdeveron-periminen"
# Contains: "32 prosenttia ... 1.1.2026 ... 25 prosenttia"

$TAXXA cited-by "1551/1995" --k 10
# Shows which ohjeet/KHO interpret the avainhenkilölaki — for triangulation.

# Then close the investigation with a report:
cat > /tmp/answer.md <<'EOF'
For wages paid up to **31.12.2025** the rate is **32 %**;
for wages paid on or after **1.1.2026** the rate has been lowered to **25 %**.
The tax card is granted for the work period in the application, capped at
**84 months** from the original start of employment (extended from 48 months
in 2026); extensions must be requested within 30 days of the previous
card's expiry.
EOF

$TAXXA report "avainhenkilö lähdevero kortti voimassaolo" \
  --scope ohje --k 5 \
  --question "What withholding rate applies to a key-personnel foreign specialist, and how long is the tax card valid?" \
  --answer-file /tmp/answer.md \
  --out /tmp/avainhenkilo-report.html
# Mention the file path in your reply: "Report at /tmp/avainhenkilo-report.html".
```

## Hard rules

- **Translate to Finnish before search.** English queries return near-zero
  hits. The glossary below covers the most common terms.
- **Read the diagnostics.** `confidence == "low"` means your query is weak —
  reformulate or browse titles. Don't read a top hit you don't trust.
- **Cite by `doc_path` + `section_id`.** Inline citations: `[ohje
  "Avainhenkilöiden verotus" §3.2]` or `[Laki tuloverolain 124 §:n
  muuttamisesta (1535/1992 amend.)]`.
- **Prefer `--scope ohje` first** for factual questions.
- **Quote `<doc_path>` arguments.** They contain spaces and Finnish characters.
- **When time matters, check amendments.** Use the `date` field on amend-*
  sections or call `taxxa amendments`.
- **One claim, one citation.** If a claim spans rule + exception, cite both.
- **Always end with a report.** Every research turn finishes with a
  `taxxa report --question … --answer-file …` call. There is no "skip
  the report" mode. The reply to the user names the output file path.

## Common failure modes

- Searching in English → reformulate using the glossary.
- Reading `finlex/Laki/Tuloverolaki.html` expecting full law text → it's only
  amendment history. The response's `consolidated_fallback` block lists the
  amendment acts. Or just use the matching vero ohje.
- Trusting a hit when `diagnostics.confidence == "low"`.
- Ignoring time-versioning on rate questions.
- Stopping at the first hit when the question needs multiple facts (rule +
  exception + definition). Decompose first.

## Glossary — English → canonical Finnish legal term

Translate before searching. When in doubt, also try `taxxa titles` on the
Finnish term to discover the exact ohje name.

### Taxes & rates
| English | Finnish |
|---|---|
| capital income tax / on capital income | pääomatulovero, pääomatulon tuloveroprosentti |
| earned income / earned-income tax | ansiotulo, ansiotulovero |
| withholding tax | lähdevero, ennakonpidätys |
| income tax (general) | tulovero |
| VAT / value-added tax | arvonlisävero, ALV |
| reduced VAT rate | alennettu arvonlisäverokanta |
| corporate income tax | yhteisövero |
| municipal tax | kunnallisvero |
| church tax | kirkollisvero |
| transfer tax (real estate / shares) | varainsiirtovero |
| real-estate tax | kiinteistövero |
| inheritance tax | perintövero |
| gift tax | lahjavero |
| excise duty | valmistevero |
| customs duty | tulli |
| public broadcasting tax | yleisradiovero |
| dividend tax / on dividends | osinkovero, osingon verotus |

### Concepts & status
| English | Finnish |
|---|---|
| key personnel (foreign specialist) | avainhenkilö, avainhenkilölaki |
| limited tax liability / non-resident | rajoitetusti verovelvollinen |
| general tax liability / resident | yleisesti verovelvollinen |
| permanent establishment | kiinteä toimipaikka |
| controlled foreign corporation | väliyhteisö, CFC |
| sole trader | toiminimi, liikkeen- ja ammatinharjoittaja |
| general partnership | avoin yhtiö |
| limited partnership | kommandiittiyhtiö |
| housing-cooperative-style company | asunto-osakeyhtiö |
| business reorganisation / merger / demerger | yritysjärjestely, sulautuminen, jakautuminen |
| business transfer (employment law) | liikkeen luovutus |
| collective agreement | työehtosopimus (TES), yleissitova työehtosopimus |
| advance ruling | ennakkoratkaisu |

### Deductions, allowances, benefits
| English | Finnish |
|---|---|
| commuting deduction (home–work) | matkakuluvähennys, asunnon ja työpaikan väliset matkat |
| kilometre allowance (work trips) | kilometrikorvaus |
| per diem | päiväraha |
| meal allowance | ateriakorvaus |
| income-generating expense deduction | tulonhankkimisvähennys |
| household deduction | kotitalousvähennys |
| basic deduction | perusvähennys |
| pension contribution | eläkemaksu |
| fringe benefit / in-kind benefit | luontoisetu |
| personnel benefit | henkilökuntaetu |
| company car (use benefit / free benefit) | käyttöetuauto, vapaa autoetu |
| ordinary advertising gift (≠ taxable income) | tavanomainen mainoslahja |
| sample (≠ taxable) | tavaranäyte |

### Income types
| English | Finnish |
|---|---|
| rental income | vuokratulo |
| capital gain | luovutusvoitto |
| capital loss | luovutustappio |
| dividend income | osinkotulo |
| pension income | eläketulo |
| interest income | korkotulo |
| royalty / IP income | rojalti, aineettomista oikeuksista saatu tulo |
| acquisition cost (basis) | hankintameno, hankintameno-olettama |

### Procedure & remedies
| English | Finnish |
|---|---|
| tax return | veroilmoitus |
| pre-completed tax return | esitäytetty veroilmoitus |
| gift-tax return | lahjaveroilmoitus |
| inheritance estate inventory | perukirja, perunkirjoitus |
| supplementary inventory | täydennysperunkirjoitus |
| advance withholding card / tax card | verokortti, ennakonpidätyskortti |
| request for correction | oikaisuvaatimus |
| basis correction (post-assessment) | perusteoikaisu |
| Administrative Court | hallinto-oikeus |
| Supreme Administrative Court | korkein hallinto-oikeus (KHO) |
| leave to appeal | valituslupa |
| tax surcharge / penalty | veronkorotus |
| tax debt | verovelka |
| reassessment decision | jälkiverotus, oikaistu verotuspäätös |
| time limit / deadline | määräaika |
| effective date | voimaantulopäivä |

### VAT mechanics
| English | Finnish |
|---|---|
| reverse charge | käännetty verovelvollisuus |
| place of supply | suorituspaikka, myynnin verotusmaa |
| intra-Community supply | yhteisömyynti |
| electronic services | sähköiset palvelut |
| import VAT | maahantuonnin arvonlisävero |
| restaurant and catering services | ravintola- ja ateriapalvelut |

### Law abbreviations to use in `resolve` / `cited-by`
TVL = Tuloverolaki · AVL = Arvonlisäverolaki · EVL = Laki elinkeinotulon
verottamisesta · EPL = Ennakkoperintälaki · VML = Laki verotusmenettelystä ·
OVML = Laki oma-aloitteisten verojen verotusmenettelystä · PerVL = Perintö-
ja lahjaverolaki · KPL = Kirjanpitolaki · OYL = Osakeyhtiölaki · TyEL =
Työntekijän eläkelaki · YEL = Yrittäjän eläkelaki · MEL = Merimieseläkelaki ·
MYEL = Maatalousyrittäjän eläkelaki · VSVL = Varainsiirtoverolaki · KiVL =
Kiinteistöverolaki.
