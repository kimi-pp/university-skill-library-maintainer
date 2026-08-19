---
name: slide-builder
description: Build or edit Python-generated PowerPoint slides and matplotlib charts for any course under ~/Courses/. Use when adding a new lecture deck, fixing a layout problem (table overflow, caption overlap, negative-bar labels, bullet wrap), or replacing illustrative chart data with real sourced data. Enforces the course-wide data policy (real data for real-world comparisons; never fabricate; warn on illustrative). Covers REAL3010's modular `_pptx_style.py` / `_charts.py` / `_data_fetch.py` system AND REAL1700's standalone `build_slides.py`.
---

# Slide Builder — Conventions for ~/Courses/

This skill captures the conventions, layout constants, data sources, and gotchas for building PowerPoint decks and matplotlib charts across all courses. **Read this skill end-to-end before editing any slide-builder file.**

## Data policy (BLOCKING — apply first)

Before writing any chart or table, decide whether it compares real-world entities or is a pure pedagogical example.

- **Real-world comparison** (sectors, companies, REITs, geographies, time series of real metrics) → **must use real data**, with a source line on the chart. Acceptable primary sources: NAREIT T-Tracker, NAREIT REITWatch, NCREIF NPI, FRED, yfinance, CoStar, SEC EDGAR, Census/ACS, GRESB published reports, peer-reviewed academic literature (cite paper + year + journal).
- **Pedagogical mechanics** (worked FFO calc for "ABC Apartment REIT", hypothetical $250M NOI walkthrough, stylized DCF) → fictitious OK. Label clearly: title or caption must say "Hypothetical", "Worked example", or "Stylized example — not a forecast for any specific REIT."
- **If you cannot locate real data for a real-world comparison**: stop. Ask Drew where to find it or for permission to download from a specific source. Do not synthesize values.
- **Warn when shipping an illustrative chart**: include a ⚠️ note in your turn summary listing which chart(s) don't use real data and what would be needed to swap to real data.

See `~/Courses/CLAUDE.md` for the full policy text.

## Course-by-course architecture

| Course | Builder | Style helpers | Chart helpers | Data fetchers |
|---|---|---|---|---|
| REAL3010 | `materials/build_reit_presentations.py` | `_pptx_style.py` (modular) | `_charts.py` | `_data_fetch.py` (yfinance + cached) |
| REAL1700 | `materials/build_slides.py` (49 KB, standalone) | inline | n/a (uses publisher slide copies) | n/a |
| CMGT4155, REAL4407 | no builder yet | — | — | — |

**Always rebuild** with the user's installed Python interpreter: `/Users/andrew.mueller/y/bin/python`.

## REAL3010 helper API (use this when adding lecture decks for any course)

Located at `~/Courses/REAL3010-course/materials/_pptx_style.py`. This is the reference implementation for modular slide-builder code. When starting a new course's slide builder, copy & adapt this file rather than reinventing.

### Slide types

```python
import _pptx_style as s

prs = s.new_presentation()                       # 16:9, 13.333" × 7.5"
s.title_slide(prs, title, subtitle)              # NAVY + TEAL header
s.section_divider(prs, "Section Name", subtitle="optional")  # full-teal slide
s.content_slide(prs, title, bullets=[...], callout={...}, slide_num=N)
s.two_column_slide(prs, title, left_header, left_bullets,
                   right_header, right_bullets, slide_num=N)
s.image_slide(prs, title, image_path, caption="...", slide_num=N)
s.table_slide(prs, title, headers, rows, col_widths=[...], slide_num=N)
s.closing_slide(prs, title, subtitle, next_topic="...", slide_num=N)
```

### Bullets

Pass `bullets=[...]` as a list of strings (level 0) or `(text, level)` tuples for indented sub-bullets. Hanging-indent is set automatically (see `_set_hanging_indent()` in `_pptx_style.py`).

```python
bullets=[
    "Top-level bullet",
    ("Sub-bullet under the previous one", 1),
    ("Another sub-bullet", 1),
    "Back to top level",
]
```

### Callouts

```python
callout={"title": "Key Insight", "body": "amber-bordered explainer text"}
```

## Critical layout constants (REAL3010 + REAL1700)

| Constant | Value | Why |
|---|---|---|
| Slide size | 13.333" × 7.5" | 16:9 default |
| Printable width | 12.33" | leaves 0.5" margins L/R |
| Body content top | 1.85" | below title bar + teal underline |
| Image top | 1.90" | room for title |
| Footer divider | 7.10" | teal hairline above footer text |
| Footer text row | 7.15"–7.45" | course label left, slide # right |
| Caption reserve | 0.85" | handles 2-line caption at 12pt italic |
| Max image height | ~5.25" | when caption present |
| Max table height | 4.80" | before vertical compression |

**Never let any shape's bottom cross 7.10".** That's the teal footer divider. If you do, the caption/text overlaps it and looks broken.

## Layout gotchas — solved patterns

These bugs all bit us in the existing decks. The fixes are baked into `_pptx_style.py`; if you're writing a new builder, replicate them.

### 1. Table overflow on the right

If `sum(col_widths) > 12.33"`, the table extends past the printable area. `table_slide()` now clamps proportionally and prints a warning. When designing col_widths, sum them mentally first.

### 2. Caption overlapping footer divider

A long caption can wrap to 2 lines and cross the 7.10" divider. The fix in `image_slide()`:
- `caption_reserve = 0.85"` (handles 2-line wrap)
- `caption_height = 0.55"` textbox
- `footer_clearance = 0.10"` enforced

If image aspect makes the image too tall to fit with the caption reserve, `image_slide()` automatically shrinks the image.

### 3. Bullet wrap going under the bullet glyph (not under the text)

Symptom: a 2-line bullet's second line starts flush left, under the "▸", instead of aligning with the bullet text. Fix is paragraph-level `marL`/`indent`:

```python
# REAL3010 _pptx_style.py: _set_hanging_indent()
pPr = p._p.get_or_add_pPr()
pPr.set("marL", str(int(text_start_in * 914400)))   # EMUs
pPr.set("indent", str(int(-hang_in * 914400)))      # negative = hanging
```

Level 0 (▸): `text_start_in=0.22, hang_in=0.22` for 18pt Calibri.
Level 1 (•): `text_start_in=0.55, hang_in=0.18` for 15pt Calibri.

For REAL1700 (which has its own builder), use `_hanging_indent()` and `_bulleted_paragraphs()` helpers in `build_slides.py`. The `_bulleted_paragraphs()` helper splits multi-line descriptions on `\n` and applies hanging-indent only to lines beginning with `▸ ` or `• `.

### 4. Negative-bar labels unreadable on matplotlib bar charts

A single `offset` for positive AND negative bars puts label centers inside negative bars. Use baseline-aware vertical alignment:

```python
for bar, v in zip(bars, values):
    if v >= 0:
        ax.text(..., v + 2, label, ha="center", va="bottom", ...)
    else:
        ax.text(..., v - 2, label, ha="center", va="top", ...)
```

And extend `ax.set_ylim()` to give clearance for both top and bottom labels.

### 5. Stale .pptx vs. fresh script

The `.pptx` in `materials/powerpoint/` can drift from `build_*.py` if someone edited it by hand. Symptoms: extra blank slides, slides referencing files that don't exist. Always rebuild via the script — never hand-edit the .pptx; if a slide needs to change, change the script then rebuild.

## Chart conventions (matplotlib)

In `_charts.py`:

```python
NAVY = "#1F2A44"      # primary, dark
CHARCOAL = "#333333"  # body text
TEAL = "#2E86AB"      # accent, "good"
AMBER = "#E1A87C"     # warning, "weak" or "cyclical"
LIGHT_GRAY = "#F0F0F0"
MID_GRAY = "#BFBFBF"
```

Every chart function follows this skeleton:

```python
def chart_xyz(data, source=None):
    fig, ax = plt.subplots(figsize=(10, 4.8))   # typical
    # ... draw ...
    _setup_axes(ax)                              # removes top/right spines
    ax.set_title("Title", fontsize=13, color=NAVY, pad=12, loc="left")
    return _save("xyz.png", source=source)       # source baked into figure
```

`_save()` writes the source as italic gray text at the bottom-right of the PNG. **Always pass `source` from the data dict's `source` field** — the source citation is the trust signal that lets students take the chart seriously.

## Real data sources (use these — keep current)

These are the public sources we already have parsers / hardcoded data for in REAL3010. Reuse them.

### NAREIT T-Tracker (quarterly)

- **URL pattern**: `https://www.reit.com/sites/default/files/YYYY-MM/T_TrackerYYYYQN.xlsx`
- **Latest used**: Q1 2026 (file: `T_Tracker2026Q1.xlsx`)
- **What it gives you by sector**: FFO, NOI, Same-Store NOI growth, Implied Cap Rate, Occupancy, Debt/EBITDA, Dividends Paid, FFO Payout
- **Sectors**: Office, Industrial, Retail (+ Shopping Centers, Regional Malls, Free Standing), Residential (+ Apartments, Manufactured Homes, SFH), Diversified, Lodging/Resorts, Self Storage, Health Care, Timberland, Telecommunications, Data Centers, Gaming, Specialty
- **Sheet**: "Chart Data" has time series rows (`Same Store NOI` starts row 99, `Implied Cap Rate` starts row 297). Header row 2 has quarter floats (e.g., 2026.1 = 2026 Q1).
- **Parsing pattern**: see `references/parse_ttracker.py` in this skill.

### NAREIT REITWatch (monthly)

- **URL pattern**: `https://www.reit.com/sites/default/files/reitwatch/RWYYMM.pdf`
- **Latest used**: April 2026 (file: `RW2604.pdf`)
- **What it gives you per REIT**: 31-day price, 52-wk hi/lo, FFO 2026E/2027E, P/FFO 2026E/2027E, FFO growth, FFO Payout (2025 Q4 trailing), Debt/EBITDA, Total Return (QTD/YTD/1-yr/3-yr/5-yr), Dividend Yield, Equity Market Cap, Implied Market Cap, Debt Ratio, Issuer Rating
- **Per-sector AVERAGE rows on pages 36–48ish** (Office page 36, Industrial page 36, Retail page 37, Residential page 38, etc.)
- **Parsing**: pypdf + line scan — see `references/parse_reitwatch.py`.

### yfinance (live prices & financials)

```python
import yfinance as yf
t = yf.Ticker("PLD")
t.fast_info.last_price       # current price
t.fast_info.market_cap       # current market cap
t.fast_info.shares           # shares outstanding
t.financials                 # 4-year annual income statement (Total Revenue,
                             # Net Income, Operating Income, Reconciled
                             # Depreciation, Interest Expense, ...)
t.dividends                  # full dividend history
t.history(period="max")      # full price history
```

The REAL3010 `_data_fetch.py` already wraps yfinance with a 7-day JSON cache at `figures/_data_cache.json`. When adding a new live fetcher, follow that pattern (`_cache_get` / `_cache_set`).

### FRED (Treasury yields, macro)

```python
import pandas_datareader.data as pdr
dgs10 = pdr.DataReader("DGS10", "fred", start, end)
```

### GRESB (annual ESG real estate scores)

- **Public results page**: `https://www.gresb.com/2024-real-estate-assessment-results/` (changes each year)
- **2024 published averages**: Standing Investments 75.84, Development 85.76; 65% have net-zero target; 94% include climate resilience in strategy
- **Sources**: GRESB press releases + Measurabl / AESG industry write-ups

### Academic literature (cite paper + year + journal)

| Topic | Paper | Key result |
|---|---|---|
| Green building rent/sale premium | Eichholtz, Kok & Quigley (2010) "Doing Well by Doing Good?" AER 100(5) | +3% asking rent, +6% effective rent, +16% sale price (vs. otherwise-identical buildings) |
| REIT capital structure | Howe & Shilling (1988) JREFE — many follow-ups | (cite as needed) |
| Sustainable real estate returns | Kok & Jennen (2012) Energy Economics | Energy-efficient office rent premium |

When you cite an academic paper, the source line should read e.g.:
`Source: Eichholtz, Kok & Quigley (2010) "Doing Well by Doing Good? Green Office Buildings", AER 100(5)`

## Building a NEW course's slide builder

1. Create `~/Courses/COURSEXXXX-course/materials/` with these four files:
   - `_pptx_style.py` — copy from REAL3010, swap color palette if needed
   - `_charts.py` — copy from REAL3010 if you'll have charts; otherwise omit
   - `_data_fetch.py` — copy from REAL3010 if pulling live data
   - `build_COURSE_presentations.py` — the orchestrator that calls slide functions
2. Add `figures/` for chart PNGs and `powerpoint/` for output `.pptx` files.
3. In each `image_slide()` call, ensure the caption is ≤ 2 lines.
4. In each `table_slide()` call, verify `sum(col_widths) ≤ 12.33`.
5. Run `/Users/andrew.mueller/y/bin/python build_*.py` and open the output to spot-check.

## Building an EXERCISE workbook (real-data Excel template)

Pattern from `~/Courses/REAL3010-course/assignments/_build_nav_exercise.py`:

- Create a builder script that takes `student_mode: bool` and writes two files: `_student.xlsx` (formulas blank, inputs filled, pale-amber input cells) and `_complete.xlsx` (formulas filled, pale-teal result cells).
- Inputs: real data from yfinance / 10-K / supplemental, cited in a "Sources" section on an Overview sheet.
- One sheet per concept (Overview → Income Stmt → FFO → AFFO → NAV).
- Use cell colors as visual semantic: pale amber = inputs, pale teal = formula cells, NAVY/TEAL fills = section headers.
- Cross-sheet links via `='OtherSheet'!B9`.
- Always write the matching student instruction sheet as `ASSIGNMENT_sheet.md`.

## Build & verification commands

```bash
# REAL3010 (rebuilds all 4 decks + 17 chart PNGs):
cd ~/Courses/REAL3010-course/materials && /Users/andrew.mueller/y/bin/python build_reit_presentations.py

# REAL1700:
cd ~/Courses/REAL1700-course/materials && /Users/andrew.mueller/y/bin/python build_slides.py

# Quick slide-title audit (no Python needed):
cd /tmp && rm -rf inspect && mkdir inspect && cd inspect && \
unzip -q ~/Courses/REAL3010-course/materials/powerpoint/REAL3010_8_1_REIT_metrics_v2.pptx -d 8_1 && \
for f in $(ls 8_1/ppt/slides/slide*.xml | sort -V); do
  title=$(grep -oE '<a:t>[^<]*</a:t>' $f | head -1 | sed 's/<[^>]*>//g')
  echo "$(basename $f): $title"
done

# Position audit (where each shape sits — use to verify no overlaps):
/Users/andrew.mueller/y/bin/python -c "
from pptx import Presentation
prs = Presentation('PATH.pptx')
for i, s in enumerate(prs.slides, 1):
    for shape in s.shapes:
        if shape.top is None: continue
        print(i, shape.left/914400, shape.top/914400, shape.width/914400, shape.height/914400, shape.shape_type)
"
```

## When asked to "fix" or "update" a slide

1. **Find the slide** — open the .pptx XML directly (unzip + grep) or use the position-audit one-liner above. Map the slide number to the builder function in `build_*.py`.
2. **Check the chart, if any** — the chart PNG lives in `materials/figures/`; the function is in `_charts.py`. Real-data charts take a `data` dict from `_data_fetch.py`.
3. **Fix in the script, not the .pptx** — never hand-edit the .pptx. Always edit the builder and rebuild.
4. **Rebuild and re-audit** — run the build script, then verify with the position-audit one-liner to confirm no shape crosses the footer divider at 7.10".
5. **If the user mentions slide N and the slide structure has drifted**, the `.pptx` is older than the script. Note this in your reply and rebuild as the first step.

## When asked to create a new chart with real data

1. Decide source: NAREIT T-Tracker (sector aggregates), REITWatch (per-REIT and sector averages), yfinance (live prices + macro), academic paper (peer-reviewed result).
2. Add a constant + getter to `_data_fetch.py`:
   ```python
   MY_DATA = {...}
   MY_SOURCE = "Source: ... | as of ..."
   def get_my_data():
       return {**MY_DATA, "source": MY_SOURCE}
   ```
3. Add a chart function to `_charts.py` that takes `(data, source=None)` and ends with `return _save("name.png", source=source)`.
4. Wire it into `generate_all()` in `_charts.py`.
5. Update the calling slide's caption in `build_*.py`.
6. Rebuild.

## Reference files in this skill

- `references/parse_ttracker.py` — example script that opens T-Tracker XLSX and prints same-store NOI / cap rates by sector
- `references/parse_reitwatch.py` — example script that pulls per-REIT and sector AVG metrics out of the REITWatch PDF
