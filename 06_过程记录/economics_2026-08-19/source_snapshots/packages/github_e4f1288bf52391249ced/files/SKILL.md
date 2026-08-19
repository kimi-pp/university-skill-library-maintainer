---
name: 论文workflow
description: 经济学实证论文 9 阶段标准工作流。Use when user starts a new empirical economics paper (course / dissertation / journal). Triggers on /论文workflow, "paper workflow", "empirical econ paper", or descriptions of starting an econ paper task with deadline + word count.
---

# 论文workflow — Empirical Economics Paper Workflow

This is the **Anthropic Skill** version of this workflow, for use with Claude Code's `Skill` tool, the Claude Agent SDK, or any platform that supports the Anthropic skill format.

For the **Codex / generic agent** version, see [`AGENTS.md`](AGENTS.md).
For the **Claude Code slash command** version, see [`commands/论文workflow.md`](commands/论文workflow.md).

All three files describe the same workflow with the same 9 phases. Pick whichever your platform reads natively.

---

## Activation

When invoked, **do not improvise**. Follow the 9 phases below in order. Confirm context first (Phase 0).

## Phase 0 — Context confirmation (MANDATORY)

Ask the user these 7 questions verbatim. Do not assume answers:

```
1. 论文类型：课程论文 / 毕业论文 / 期刊投稿？
2. 字数范围 + 截止日期？
3. 主题状态：
   (a) 从零选题（我给你 5 个候选）
   (b) 已定主题（你告诉我）
   (c) 续写已有项目（在哪个目录？）
4. 引用格式：Harvard Manchester / APA 7 / AER 传统 / 其他？
5. 计量方法：你课程教过哪些（DID / IV / RDD / FE / 其他）？
6. 数据约束：必须公开数据？还是可以用机构访问？
7. 工具栈：R / Stata / Python？
```

If user says "按之前的" / "same as last time", apply defaults:
- Harvard Manchester citations
- R + public data
- `~/Desktop/econ-papers/<paper-name>/`
- TWFE event study + Callaway-Sant'Anna robust

## Phase 1 — Topic + econometric setting (~30 min)

Brainstorm 5 candidate topics (each must satisfy: ≤1 day data, ≤3 day identification, anchor paper exists, scope-tractable, R packages mature). Output comparison table. Lock topic. Generate daily-milestone calendar in `docs/WORKFLOW.md`.

## Phase 2 — Literature review (~1.5 h)

Download anchor + critique PDFs. `pdftotext -layout` + grep appendix tables. Identify 5+ related papers. Write `Notes/lit_review.md`.

## Phase 3 — Data acquisition (~1 h)

Public direct links first. Try R-package hardcoded URLs. Hardcode anchor's appendix parameters. Document every URL in `Notes/DATA_ACQUISITION.md`. Avoid 24-48h registration loops.

## Phase 4 — R analysis (~2.5 h)

6 R scripts: `00_setup.R`, `01_clean_<source>.R`, `02_compute_distance.R`, `03_main_regression.R`, `04_robustness.R`, `05_tables_figures.R`. Use `fixest` + `did`. Wrap encoding-prone reads in `tryCatch` with `latin1`/`windows-1252` fallback. For invalid GADM polygons: `st_make_valid()` + `sf_use_s2(FALSE)`.

**Preferred-spec selection: NEVER use max |t|.** Use ex ante criterion (sample median, pre-registered, theoretical motivation).

Default specification: TWFE event study + region FE + country×round FE + Callaway-Sant'Anna robust + 300-permutation placebo + heterogeneity (gender/urban/age) + exogenous-shock interaction.

## Phase 5 — Writing (~2 h)

Markdown source + YAML frontmatter → Pandoc → docx. **Don't write LaTeX directly.** Don't double-number sections. Structure: IMRAD + Lit Review.

## Phase 6 — Multi-layer review (~1 h)

Three independent passes:
1. Content (OVB, identification threats) via `claesbackman/AI-research-feedback` 2-agent
2. Format (missing citations, double numbering, broken refs) via `oceangis/skill_academic-writing-skills`
3. References (DOI verification per cited paper) → `Paper/references_verified.csv`

## Phase 7 — Word-count adjustment (~30 min)

Per-section count via `awk`. Each added paragraph must contain ≥1 of: number, citation, mechanism, limitation, future work. **No filler.**

## Phase 8 — Reference-format adaptation (~30 min)

Apply target style. Harvard Manchester defaults:
- Single quotes around article titles
- `pp.` prefix for page ranges
- `doi:` lowercase
- `Available at:` for grey literature
- `(Accessed: <date>)` for websites

## Phase 9 — Version archive

Immutable `Paper/full_paper_v1.md` → `v9.md`. Never overwrite. Generate `.docx` per version.

## Departures from default

- **Long-form (≥10,000 words)**: expand §3 descriptives, §4 derivations, §5 sub-sample/mechanism, §6 external validity, full robustness appendix
- **Short brief (<3,000 words)**: collapse phases 5-9 into single editorial pass
- **Non-DID** (RDD/IV/RCT replication): Phase 4 changes; ask user about identification setup first

## Anti-patterns (never do)

- Skip Phase 0 questions
- Use max |t| for preferred spec
- Fabricate numbers
- Pad word count with filler
- Write LaTeX directly
- Double-number sections
- Skip reference DOI verification
- Overwrite `full_paper_vN.md`

## See also

- [`docs/WORKFLOW.md`](docs/WORKFLOW.md) — full per-phase playbook
- [`templates/Code/`](templates/Code/) — R script starters
- [`templates/Paper/full_paper_template.md`](templates/Paper/full_paper_template.md) — paper template
- [`examples/case_studies.md`](examples/case_studies.md) — two validated runs
