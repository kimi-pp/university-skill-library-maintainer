---
name: ssci-plots
description: >
  Publication-ready statistical figures for SSCI/SCI journals across psychology,
  economics, public health, sociology, political science, geography, methodology.
  Validated matplotlib styling, CVD-safe palettes (Tol, Okabe-Ito, ggsci,
  aesthetic sets), APA 7 formatting, 12 journal presets (APA, Elsevier, Wiley,
  SAGE, Psych Science, ASA, Nature, Science, NEJM, Lancet, BMJ, JAMA), 55+ chart
  types. Use when creating academic figures, path/SEM diagrams, heatmaps, forest
  plots, error-bar charts, mediation diagrams, event-study plots, RD plots,
  Kaplan-Meier curves, choropleths, causal DAGs, or any journal submission
  figure. Also use for publication-quality figures even without explicit "APA"
  or "SSCI" mention.

  Keywords: academic figure, APA figure, SSCI chart, path model, forest plot,
  heatmap, Kaplan-Meier, event-study, RD plot, DID, coefficient plot,
  choropleth, causal DAG, multi-panel, journal submission figure, 学术统计图,
  论文图表, APA格式, SSCI图表, 路径模型, 森林图, 热力图, 中介模型, 事件研究,
  断点回归, 生存曲线, 多面板图, 心理学可视化, 经济学图表, 公共卫生图表, 期刊投稿
---

# SSCI Academic Figure Style

## 1. Core Principles

Three design commitments guide every figure this Skill produces:

1. **Data-ink ratio**: Every pixel should convey data. Remove gridlines, 3D effects, and decorative elements -- they add visual noise without information value (Tufte, 1983). Use clean L-shaped axes (top and right spines off).

2. **Colorblind-safe and grayscale-compatible**: About 8% of male readers have red-green color vision deficiency. Categorical palettes default to validated CVD-safe sets (Tol, 2021; Wong, 2011; Okabe & Ito, 2008) and pair color with a redundant channel (line style, marker shape, or hatching) so every figure remains readable in grayscale print. Journal-anchored palettes (NPG, AAAS, NEJM, Lancet, BMJ, JAMA) are provided to match house style at submission and are flagged with their CVD grade in `list_palettes()`.

3. **Clean figure + separate text**: The saved image contains only the data visualization (axes, data, legend). Figure number, title, and Note are output as standalone Markdown text for the user to place in the manuscript. This matches APA 7th Edition requirements and most journal submission guidelines where captions are supplied separately from image files.

Initialize the style system at the start of every figure:

```python
from scripts.ssci_style import *
apply_style()                                # 70+ rcParams, colormaps, fonts
apply_style(journal='nejm')                  # Auto-loads matching palette + sizes
apply_style(journal='psych_science', mode='slides')  # Larger fonts for talks
```

---

## 2. Workflow

### Step 1 -- Confirm Requirements

Before writing code, identify:
- (a) Chart type from the decision table below (or its chart-family reference file)
- (b) Target journal, if the user specifies one (12 presets available)
- (c) Number of groups or conditions (determines palette size)
- (d) Error metric: SE, SD, or 95% CI

### Step 2 -- Initialize Style

Run `apply_style()` to set all rcParams, register colormaps, and embed fonts.

If the user specifies a target journal, pass it as an argument and read `references/journal-presets.md` for details:

```python
# Available journal keys (12):
#   apa, elsevier, wiley, sage, psych_science, asa,
#   nature, science, nejm, lancet, bmj, jama
apply_style(journal='lancet')
```

`apply_style(journal=...)` also auto-loads the matching default palette via `axes.prop_cycle` (e.g. `journal='nejm'` activates the `nejm` palette). For slide / poster usage, add `mode='slides'` to bump font sizes without touching the underlying preset.

### Step 3 -- Build the Figure

Open `references/chart-type-guide.md` first. It is the **Index** to the 55-chart catalog and routes you to one of the four chart-family files (`chart-types-core.md`, `chart-types-models.md`, `chart-types-causal-econ.md`, `chart-types-applied.md`) or the quick-reference file. Follow the design elements, parameters, and code patterns documented there.

Color selection:
- Categorical data: `get_palette(n)` returns n CVD-safe hex colors (default: Tol Bright). Use `category=` / `name=` for discipline- or journal-anchored alternatives.
- Emphasis focal + reference pair: `get_emphasis_pair(focal=..., reference=...)` returns two colors for "focal series vs neutral reference" patterns (treatment vs control, event-study, simple slopes).
- Heatmap: `get_diverging_cmap('BuRd')` with `TwoSlopeNorm(vcenter=0)` for zero-centered diverging data.
- Sequential data: `get_sequential_cmap('viridis')` (perceptually uniform); also `cividis / plasma / inferno / magma / Blues / Oranges / tailwind_slate`.
- Multi-panel composition: see `references/multi-panel.md` for `compose_grid` / `small_multiples` / `add_inset` / shared legend & colorbar / marginal histogram.
- Always pair color with redundant coding (`LINE_STYLES`, `MARKERS`, or `HATCHES` from `ssci_style`).

### Step 4 -- Validate

Check every item in the Quality Checklist (Section 6 below) before saving.

If the figure includes statistical annotations (p-values, effect sizes, CI, inline statistics), read `references/statistical-annotations.md` for exact formatting rules. For APA figure text formatting details (number, title, Note, multi-panel conventions, mediation diagram conventions), read `references/apa-figure-standards.md`.

### Step 5 -- Save and Output

Save the figure in multiple formats using `save_figure()`:

```python
save_figure(fig, 'fig_1')                          # Default: PDF + PNG (600 DPI)
save_figure(fig, 'fig_1', formats=('pdf', 'tiff')) # Journal submission (RGB TIFF)
```

Then output the figure description text separately as Markdown, using `format_apa_figure_text()`:

```python
text = format_apa_figure_text(
    figure_number=1,
    title="Mean Anxiety Scores by Treatment Condition and Time Point",
    note_text="N = 354. PSS = perceived stress scale; SWB = subjective well-being.",
    p_levels=[("*", ".05"), ("**", ".01"), ("***", ".001")],
    error_bar_type="95ci",                  # auto-emits standard error-bar statement
)
```

Output format:

**Figure 1**

*Mean Anxiety Scores by Treatment Condition and Time Point*

*Note.* N = 354. Error bars represent 95% confidence intervals. PSS = perceived stress scale; SWB = subjective well-being.

\*p < .05. \*\*p < .01. \*\*\*p < .001.

---

## 3. Chart Type Selection

The full catalog has **55 chart types** organized by family. Use this top-level table for routing; then load the chart-family file for the detailed 6-section spec.

### 3.1 By chart family

| Family | File | Chart sections (representative) |
|---|---|---|
| **Core distribution & relationship** | `chart-types-core.md` | §1 Grouped Bar, §2 Error Bar, §3 Line, §3.1 Annotated Time Series, §4 Scatter+Regression, §4.1 Scatter with Marginal Histogram, §5 Box, §6 Violin, §7 Correlation Heatmap |
| **Statistical model output** | `chart-types-models.md` | §8 Forest, §8.1 Coefficient/Dot-Whisker, §9 Path/SEM, §9.1 IV Diagram, §10 Mediation (incl. §10.1 Serial, §10.2 Parallel), §11 Interaction, §11.1 Categorical Moderator, §11.2 Continuous Marginal Effect, §12 Simple Slopes, §17 Scree+Parallel Analysis, §18 Profile (LPA/LCA), §19 Growth Curve, §32 Specification Curve, §33 Causal DAG |
| **Causal inference / econometrics** | `chart-types-causal-econ.md` | §22 Event-Study Coefficient Plot, §23 DID Parallel Trends, §24 Regression Discontinuity, §25 Binned Scatter (Binscatter), §26 Coefficient Plot multi-model, §38 IV Diagram |
| **Applied / specialty** | `chart-types-applied.md` | §14 Raincloud, §16 Funnel, §20 Kaplan-Meier (with at-risk table), §21 Bland-Altman, §27 Ridgeline/Joy, §28 Choropleth, §29 ROC + Calibration, §30 Mobility Transition Matrix, §31 Marginal Effects |
| **Quick reference (one-page each)** | `chart-types-quick-reference.md` | §15.1 Histogram, §15.2 Density (KDE), §15.3 Swarm/Beeswarm, §15.4 Factor Loading, §15.5 Johnson-Neyman, §15.6 CONSORT, §15.7 Lollipop, §15.8 Slope/Bump, §15.9 Dumbbell, §15.10 Population Pyramid, §15.11 Tornado/Butterfly |
| **Multi-panel composition** | `multi-panel.md` | `compose_grid`, `small_multiples`, `add_inset`, shared legend/colorbar, marginal histogram, subfigures |

### 3.2 By discipline (decision shortcut)

| Discipline | Primary chart-family file |
|---|---|
| Psychology — descriptive | `chart-types-core.md` |
| Psychology — modeling (SEM, mediation, forest, simple slopes, growth) | `chart-types-models.md` |
| Economics — causal (event-study, DID, RD, IV, binscatter) | `chart-types-causal-econ.md` |
| Public health & medicine (KM, ROC, funnel, Bland-Altman) | `chart-types-applied.md` |
| Sociology (mobility matrix, ridgeline) | `chart-types-applied.md` |
| Political science (annotated time series, ideological scaling, choropleth) | `chart-types-applied.md` + `chart-types-core.md` §3.1 |
| Geography (choropleth, spatial overlays) | `chart-types-applied.md` |
| Methodology / robustness (specification curve, DAG) | `chart-types-models.md` |

### 3.3 Cross-cutting routing table

| Data / Analysis | Recommended chart | Section anchor |
|---|---|---|
| Group mean comparison (t-test, ANOVA) | Grouped bar + error bars | core §1 |
| Group means with uncertainty (cleaner than bars) | Error bar / dot-and-whisker | core §2 |
| Trend over time / repeated measures | Line chart with CI bands | core §3 |
| Time series with event markers (policy, intervention) | Annotated time series | core §3.1 |
| Two continuous variables (r, regression) | Scatter + regression line | core §4 |
| Distribution shape comparison | Box plot | core §5 |
| Distribution with density | Violin plot | core §6 |
| Multi-variable correlation matrix | Lower-triangle heatmap | core §7 |
| Meta-analysis effect sizes | Forest plot | models §8 |
| Multi-model coefficients side-by-side | Coefficient / dot-whisker plot | models §8.1, econ §26 |
| SEM / CFA path structure | Path diagram | models §9 |
| Instrumental variable identification | IV diagram | models §9.1 / econ §38 |
| Mediation pathway (a, b, c') | Mediation diagram | models §10 |
| Moderation / interaction | Interaction / simple slopes | models §11, §12 |
| Continuous moderator marginal effect | Marginal effects plot | applied §31 |
| Factor structure (EFA/PCA) | Scree + parallel analysis | models §17 |
| Latent profile / class structure | Profile plot (LPA/LCA) | models §18 |
| Individual trajectories | Growth curve | models §19 |
| Robustness across specifications | Specification curve | models §32 |
| Causal assumptions diagram | DAG | models §33 |
| Difference-in-differences design | Event-study or DID parallel trends | econ §22, §23 |
| Sharp cutoff design | Regression discontinuity plot | econ §24 |
| Large-N continuous-X relationship | Binned scatter (binscatter) | econ §25 |
| Full distribution + mean + density | Raincloud plot | applied §14 |
| Publication bias / small-study effects | Funnel plot | applied §16 |
| Time-to-event analysis | Kaplan-Meier survival curve | applied §20 |
| Method comparison agreement | Bland-Altman plot | applied §21 |
| Multi-group distribution stack | Ridgeline / joy plot | applied §27 |
| Geographic distribution | Choropleth map | applied §28 |
| Diagnostic / prediction performance | ROC + calibration | applied §29 |
| Categorical transition / mobility | Mobility transition matrix | applied §30 |
| Multi-panel composite | Multi-panel composition | `multi-panel.md` |

When NOT to use:
- Bar chart for continuous distributions -- use violin, box, or raincloud instead (Weissgerber et al., 2015)
- Rainbow / jet colormap -- use viridis, cividis, or Tol diverging schemes
- Pie chart -- use grouped bar chart (APA does not define pie chart standards)
- 3D charts -- use 2D with faceting or color encoding
- Sankey -- use mobility transition matrix (zero new deps; sociology-standard alternative)

---

## 4. Quick Reference: Core Style Parameters

Set automatically by `apply_style()`. Override via `plt.rcParams[...]` after the call. **All numeric defaults live in `scripts/ssci_style.py`; never copy them across docs (SSOT).**

| Parameter | Rationale |
|---|---|
| `font.family` (sans-serif) | APA 7th recommends sans-serif for figures |
| `font.size` (8 pt body) | APA range 8--14 pt; 8 pt is legible at print column width |
| `axes.spines.top / right = False` | L-shaped axes maximize data-ink ratio |
| `axes.linewidth` | Exceeds APA minimum 0.5 pt; clear at print |
| `savefig.dpi` | Meets APA, Wiley, OUP, ASA line-art requirements |
| `pdf.fonttype = 42` | TrueType embedding; journals reject Type 3 fonts |
| `mathtext.fontset = 'custom'` (Arial italic) | Render *r*, *t*, *F*, *p* in body font (P0 fix) |
| `errorbar.capsize` | Visible cap without visual clutter |
| `constrained_layout` enabled | Prevents label clipping in multi-panel figures |

Full parameter set: `scripts/ssci.mplstyle` (loaded by `apply_style()`).

### Color Palettes

**21 categorical palettes are registered** (`_PALETTE_REGISTRY` in `scripts/ssci_style.py`). HEX values live exclusively in the SSOT; the table below references palettes by **name** only. Discover at runtime via `list_palettes(category=..., publication_grade=...)`.

| Category | Palettes |
|---|---|
| **General CVD-safe** (default) | `tol_bright` (default), `okabe_ito`, `high_contrast`, `ibm`, `tol_vibrant` |
| **Journal-anchored** (ggsci R, GPL-3 credit) | `nature_npg`, `science_aaas`, `nejm`, `lancet`, `jama`, `bmj` |
| **Discipline-anchored** | `economics` (Stata s2color), `tailwind_slate` (modern slate scale) |
| **Aesthetic publication-grade** | `tol_muted`, `tol_light`, `tol_medium_contrast`, `metbrewer_hiroshige`, `metbrewer_cassatt2`, `uk_gov_af`, `economist_chart`, `bbc_bbplot` |
| **Aesthetic supplement (deferred, opt-in)** | 17 candidates in `AESTHETIC_PALETTES`; opt-in via `register_aesthetic_palette(name)` which emits a warning that they are not publication-grade |

| Colormap | Use | API |
|---|---|---|
| `ssci_BuRd` | Correlation heatmap (blue-white-red, zero-anchored) | `get_diverging_cmap('BuRd')` |
| `ssci_PRGn` | CVD-safer diverging alternative | `get_diverging_cmap('PRGn')` |
| `ssci_sunset` | Tol Sunset diverging | `get_diverging_cmap('sunset')` |
| `viridis / cividis / plasma / inferno / magma` | Sequential (perceptually uniform) | `get_sequential_cmap('viridis')` etc. |
| `ssci_Blues / ssci_Oranges / ssci_tailwind_slate` | Single-hue sequential | `get_sequential_cmap('Blues')` etc. |
| Grayscale | B&W-only output | `get_grayscale(n)` (n ∈ {2,3,4,5}) |

Pair every color encoding with a redundant channel: line style (`LINE_STYLES`), marker shape (`MARKERS`), or hatching (`HATCHES`).

Full palette catalog, academic citations, license credits, decision tree, and journal/discipline anchoring: `references/color-system.md`.

### Figure Sizes

`FIGURE_SIZES` in `scripts/ssci_style.py` registers **30 named sizes**: 3 generic layouts (`single_column`, `one_half_column`, `full_width`) + 27 chart-type-specific keys. Use the key, not the literal inches:

```python
fig, ax = plt.subplots(figsize=FIGURE_SIZES['event_study'])
fig, ax = plt.subplots(figsize=FIGURE_SIZES['km_plot'])
compose_grid("ABCD", figsize='full_width')
```

For one-off dimensions, `fig_size(width_cm, height_cm)` converts to inches.

Journal-specific column widths differ across the 12 presets; calling `apply_style(journal=...)` selects the right dimensions automatically (see `JOURNAL_PRESETS` in `ssci_style.py` for exact mm / DPI per preset). Full table: `references/journal-presets.md`.

---

## 5. Key Helper Functions

All 27 public helpers defined in `scripts/ssci_style.py`. Full NumPy-style docstrings (Parameters / Returns / Raises / Examples) live with each function.

### 5.1 Style & save (3)

| Function | Purpose |
|---|---|
| `apply_style(journal=None, *, mode='paper')` | Apply 70+ rcParams, register colormaps, set font embedding. `journal` ∈ 12 keys (auto-loads matching palette + sizes); `mode='slides'` bumps fonts for talks. |
| `fig_size(width_cm, height_cm)` | Convert centimetres to inches for matplotlib figsize |
| `save_figure(fig, name, output_dir='.', dpi=600, formats=('pdf','png'))` | Save in multiple formats; TIFF support via Pillow (RGB on white background) |

### 5.2 Palette access (7)

| Function | Purpose |
|---|---|
| `get_palette(n, name='tol_bright', *, category=None, return_emphasis=False)` | Return n CVD-safe categorical hex colors; optional category filter; `return_emphasis=True` returns (focal, reference) pair |
| `get_grayscale(n)` | Return n grayscale hex values (n ∈ {2..5}) |
| `get_diverging_cmap(name='BuRd', N=256)` | Diverging colormap object: `'BuRd' | 'PRGn' | 'sunset'` |
| `get_sequential_cmap(name='viridis', N=256)` | Sequential colormap: built-ins or single-hue (Blues / Oranges / tailwind_slate) |
| `list_palettes(category=None, publication_grade=None)` | Introspect registered palettes; returns list of dicts with name / category / publication_grade / cvd_grade / max_colors / source |
| `get_emphasis_pair(focal=None, *, reference=...)` | Return (focal, reference) pair for "treatment vs control" patterns; default reference is neutral gray (see SSOT); named focals: `blue / red / green / orange / purple / navy / maroon` |
| `register_aesthetic_palette(name, hex_list=None, *, acknowledge_non_publication_grade=True)` | Opt-in registration of aesthetic / mood palettes; emits warning that they are not publication-grade |

### 5.3 APA p-value & note formatting (3)

| Function | Purpose |
|---|---|
| `format_p_value(p, style='apa')` | APA p-value string: `'apa' | 'stars' | 'exact'` |
| `p_to_stars(p)` | Convert p to `'***'` / `'**'` / `'*'` / `'n.s.'` |
| `format_apa_figure_text(figure_number, title, note_text=..., specific_notes=..., p_levels=..., *, error_bar_type=None, model_fit=None, zwsp=True)` | Generate APA figure description as Markdown; `error_bar_type ∈ {'se','sd','95ci','within_subject_ci'}`; `model_fit` for SEM stats |

### 5.4 Annotation helpers (4)

| Function | Purpose |
|---|---|
| `add_significance_bracket(ax, x1, x2, y, p_value, height=0.02, ...)` | Draw significance bracket with auto p-to-stars (emits `'n.s.'` for non-significant) |
| `annotate_effect_size(ax, d, ci=None, x=0.95, y=0.95, label='d', ...)` | Annotate effect size (Cohen's d/g/r) with optional CI on axes |
| `add_inline_stats(ax, items, position='top_left', *, fontsize=None, bbox=False, italic_latin=True)` | Position-preset inline statistic block (dict or list of `(key, value)` / `(key, value, ci)`); auto-italicises Latin symbols (*r*, *t*, *F*, *p*, *d*) |
| `add_reference_line(ax, value, orientation='horizontal', *, color=None, linestyle='--', label=None, label_position='right_top', zorder=0.5)` | Add zero-line / threshold reference; default color from `NEUTRAL['reference']`; label positions `right_top / right_bottom / left_top / left_bottom / center` |

### 5.5 Layout / axes / multi-panel (7)

| Function | Purpose |
|---|---|
| `remove_spines(ax, keep=('bottom','left'))` | Remove spines except those listed (L-shaped axes by default) |
| `setup_legend(ax, loc='best', ncol=1, frameon=False, title=None, ...)` | Clean legend following APA conventions |
| `add_panel_labels(axes, labels=None, style=None, fontsize=None, *, journal=None, prefix='', suffix='', overlay_bg=None)` | Add A, B, C panel labels; auto-styled per `_ACTIVE_PRESET` (e.g. Nature uses lowercase a/b/c, Science uses uppercase A/B/C); `prefix='('` + `suffix=')'` add parentheses for any journal that requires them; `journal=` overrides for one-off mixing |
| `compose_grid(layout, figsize='full_width', *, width_ratios=None, height_ratios=None, share=False, panel_labels='auto', ...)` | Asymmetric mosaic via subplot_mosaic; pre-validates rectangular layout (raises `SSCIPlotsMosaicError` on L-shape) |
| `small_multiples(n_rows, n_cols, figsize='full_width', *, share='all', panel_labels='auto', ...)` | Isomorphic grid for repeated comparisons |
| `add_inset(ax, bbox=(0.55,0.55,0.4,0.4), *, xlim=None, ylim=None, zoom_indicator=False, hide_ticks=False)` | Inset axes with optional zoom indicator (NEJM-style) |
| `add_marginal_hist(ax, x, y, *, bins=30, size='20%', kind='hist', hide_inner=True)` | Top + right marginal axes for scatter (kde requires scipy) |
| `add_shared_colorbar(fig, mappable, axes=None, *, label=None, location='right', shrink=0.7, extend='neither')` | Single colorbar spanning multiple panels |
| `add_shared_legend(fig, handles_or_axes, labels=None, *, loc='lower center', ncol=None, region=None, deduplicate=True)` | Single figure-level legend with deduplicated handles |
| `compose_subfigures(n_rows, n_cols, figsize='full_width', *, per_subfig_suptitle=None, ...)` | Wrap `Figure.subfigures` for Nature-style grouped panels |

(Count check: 3 style/save + 7 palette + 3 APA + 4 annotation + 10 layout = **27** public helpers. See `_ssot_signature_lock.md` for the exact accounting.)

---

## 6. Quality Checklist

Before saving any figure, verify every item:

- [ ] Top and right spines removed (L-shaped axes)
- [ ] Font is sans-serif (Arial / Helvetica), all text 8--14 pt at final print size
- [ ] Colors are from a validated CVD-safe palette (not custom RGB guesses)
- [ ] Redundant coding present (line styles / markers / hatching supplement color)
- [ ] Error bars included where applicable; type (SE, SD, or 95% CI) stated in planned Note text
- [ ] Axis labels use Title Case, parallel to their axis
- [ ] Legend inside figure area or below; Title Case entries; `frameon=False`
- [ ] No gridlines, no 3D effects, no decorative elements
- [ ] Multi-panel labels bold, top-left of each panel; case (A/B/C vs a/b/c) and font size follow the active journal preset's `panel_label_case` / `panel_label_size` (APA default: uppercase 12 pt; Nature: lowercase 9 pt; see `journal-presets.md`)
- [ ] Figure saved as both PDF (vector) and PNG or TIFF (600 DPI raster)
- [ ] `pdf.fonttype = 42` confirmed (TrueType embedding)
- [ ] Figure text (number, title, Note) output as separate Markdown, not embedded in the image
- [ ] **Figure Note 未嵌入图片本体**：`*Note.*`、`*p < .05.*`、解释性 caption 等应作为 Markdown 文本通过 `format_apa_figure_text()` 输出，**不要**用 `fig.text(...)` / `ax.text(...)` 嵌入 PNG。inline stats 簇（如 "*r* = .45, *p* < .001"）是允许的，但完整的"Note. ..."段落违反 APA §7.28 + Skill §9 输出原则。

For APA formatting details: `references/apa-figure-standards.md`.
For statistical annotation rules: `references/statistical-annotations.md`.

---

## 7. Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Fonts show as boxes or wrong glyphs | Arial not installed | DejaVu Sans is configured as fallback in `apply_style()` |
| Text cut off when saving | tight_layout failure with complex layouts | `constrained_layout` is enabled by default; do not mix with `tight_layout` |
| Colors look different in print | RGB-to-CMYK gamut shift | Stick to Tol / Okabe-Ito palettes (mid-saturation, CMYK-safe) |
| PDF rejected ("Type 3 fonts") | `pdf.fonttype` not 42 | Ensure `apply_style()` was called before any plotting |
| Heatmap zero-point not white | Missing TwoSlopeNorm | Use `TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)` |
| Error bars invisible on bar chart | Error bar color same as fill | Use `NEUTRAL['error_bar']` (black) with `capsize=3` |
| Figure text too small after resize | Font < 8 pt at final column width | Design at target width (85 mm); text at 8 pt stays legible |
| TIFF output needed | matplotlib lacks native TIFF | `save_figure(fig, name, formats=('tiff',))` handles conversion via Pillow |
| Italic *r* / *t* renders as DejaVu Sans Oblique | mathtext fontset mismatch | Already fixed: `apply_style()` sets `mathtext.fontset='custom'` with Arial |
| `compose_grid` rejects L-shape | subplot_mosaic only supports rectangular | Restructure layout or split into two figures (`SSCIPlotsMosaicError` is informative) |
| Aesthetic palette unavailable | Deferred / opt-in by design | `register_aesthetic_palette('studio_ghibli')` (emits warning that palette is not publication-grade) |
| Note 段落嵌在图片里 | `fig.text(0.5, 0.02, "*Note.* ...")` 嵌图违反 APA §7.28 | 删除该调用；用 `format_apa_figure_text(note_text="...")` 生成 Markdown 文本同步输出 |

---

## 8. Reference Files

Load each file only when needed (progressive disclosure). The chart catalog is split across 5 files; load the **family** file matching the requested chart type, not the whole catalog.

| File | Content | Load when... |
|------|---------|-------------|
| `references/chart-type-guide.md` | **Index**: TOC across 4 chart families + quick reference + cross-cutting Y-axis baseline rule + old-anchor redirects | Step 3: looking up which chart-family file to open |
| `references/chart-types-core.md` | Core distribution & relationship: §1-§7 + §3.1 + §4.1 + §16 Histogram | Building any §1-§7 figure or the new annotated time series / marginal-histogram subsections |
| `references/chart-types-models.md` | Statistical model output: §8-§12, §17-§19, §32, §33 | Forest, SEM, mediation, interaction, simple slopes, scree, profile, growth, specification curve, DAG |
| `references/chart-types-causal-econ.md` | Causal inference / econometrics: §22-§26, §38 | Event-study, DID parallel trends, RD, binscatter, multi-model coefficient plot, IV diagram |
| `references/chart-types-applied.md` | Applied / specialty: §14, §16, §20, §21, §27-§31 | Raincloud, funnel, Kaplan-Meier, Bland-Altman, ridgeline, choropleth, ROC+calibration, mobility matrix, marginal effects |
| `references/chart-types-quick-reference.md` | 11 one-page references (§15.1-§15.11) + per-discipline decision matrix | Quick lookups for histogram, density, swarm, factor loading, Johnson-Neyman, CONSORT, lollipop, slope/bump, dumbbell, population pyramid, tornado |
| `references/multi-panel.md` | Multi-panel composition: `compose_grid` / `small_multiples` / `add_inset` / shared legend & colorbar / marginal histogram / subfigures + cross-panel consistency checklist | Step 3 for any A/B/C or N×M figure, inset zooms, shared colorbar across panels |
| `references/color-system.md` | Full 21-palette catalog (general / journal-anchored / discipline-anchored / aesthetic publication-grade / deferred aesthetic), license credits, decision tree, redundant coding, semantic conventions | Choosing non-default colors, needing > 7 groups, journal-anchoring, or aesthetic palettes |
| `references/apa-figure-standards.md` | APA 7th Figure number / title / Note format, font and italic rules, multi-panel specs, accessibility, §11 Mediation Diagram Conventions (SEM notation rules) | Step 4: validating APA compliance; writing Figure text output; mediation diagram setup |
| `references/journal-presets.md` | Size / DPI / format requirements per publisher (APA, Elsevier, Wiley, SAGE, Psych Science, OUP/ASA, Nature, Science, NEJM, Lancet, BMJ, JAMA) | Step 2: when user specifies a target journal |
| `references/statistical-annotations.md` | p-value, effect size, CI formatting; statistical symbol italic rules; decimal place conventions; `add_inline_stats` / `add_reference_line` usage | Step 4: when figure includes statistical annotations |
| `references/complexity-elements-catalog.md` | Catalog of "publication-quality complexity elements" (white-halo lines, inset zooms, descriptor matrices, at-risk tables, CI ribbons, etc.) and which chart types use which elements | Stepping up an existing figure from "course assignment" feel to "top-SSCI" feel; choosing which complexity elements to layer onto a base chart |
| `references/multi-figure-gallery-pitfalls.md` | 11 high-frequency cross-figure pitfalls + 60-second self-check sweep + 3 cognitive traps. Non-binding companion distilled from Phase 7 polish (88 P0 fixes on an 18-figure gallery) | **Strongly recommended when generating ≥ 3 figures for the same surface** (README gallery, paper figures, slide deck). Single-figure use can skip |
