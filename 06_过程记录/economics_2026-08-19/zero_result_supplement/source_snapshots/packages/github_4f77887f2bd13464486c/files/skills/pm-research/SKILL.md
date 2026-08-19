---
name: pm-research
description: Search, download, and ingest Process Mining research papers from IEEE Xplore, ArXiv, Google Scholar, and Semantic Scholar into a Synthadoc knowledge base.
version: 0.2.2
type: script
scripts:
  - name: fetch_pm_papers.py
    description: Batch search and download PM papers from ArXiv and Semantic Scholar. Outputs structured JSON.
runtime: python3
timeout_sec: 300
permissions:
  - net
env_from_settings:
  - OPENROUTER_API_KEY
when_to_use: User asks to find, download, or collect Process Mining papers, or to populate/update the pm-research knowledge base with academic articles.
keywords:
  - process mining
  - research
  - papers
  - ieee
  - arxiv
  - scholar
  - synthadoc
---

# PM Research — Process Mining Literature Collector

This skill guides the agent through the full pipeline of finding, downloading, and ingesting Process Mining research papers into the `pm-wiki` Synthadoc knowledge base.

## Overview

The skill has two modes:

1. **Script mode (ArXiv + Semantic Scholar)** — call `skill_exec` to batch-search and download papers in a single tool call. The script handles API queries, deduplication, PDF download, and validation. Returns structured JSON.
2. **Agent mode (IEEE + Scholar + Synthadoc)** — the agent handles sources that require browser interaction (IEEE Xplore DOM scraping, Google Scholar `[PDF]` links) and Synthadoc ingestion (MCP tool).

**Always run the script first**, then handle remaining sources manually.

### Script usage

```
skill_exec(skill="pm-research", script="fetch_pm_papers.py", args=["--keywords", "process mining,conformance checking", "--since-year", "2025", "--max-papers", "20"])
```

The script outputs JSON with:
- `papers_found`: list of discovered papers
- `downloads`: download results (status: downloaded/exists/paywall/error)
- `errors`: API errors encountered
- `summary`: aggregate counts

After the script completes, the agent should:
1. Read the JSON output
2. Ingest new papers into Synthadoc via `synthadoc_ingest` (URL or file path)
3. Handle IEEE Xplore and Google Scholar sources manually (see protocols below)

## Search Keywords

Use the following keyword groups. Combine them with `site:` operators for targeted source queries.

### Core

```
"process mining", "process discovery", "conformance checking",
"process enhancement", "process model", "task mining"
```

### Logs and Traces

```
"event logs", "audit trail", "audit log analysis"
```

### Control and Audit

```
"process monitoring", "process compliance", "continuous auditing",
"internal audit", "deviation analysis", "compliance monitoring"
```

### Banking Context

```
"process mining banking", "financial auditing"
```

## Source-Specific Protocols

### IEEE Xplore

**Base search URL:**
```
https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={QUERY}&highlight=true&returnType=SEARCH&matchPubs=true
```

**Critical lessons learned:**

- **Open Access filter is unreliable via URL.** The `refinements=Open Access` parameter often returns empty results even when OA papers exist. Do not rely on it.
- **Validate PDF availability by download, not by metadata.** Many papers marked "Open Access" still redirect to a paywall. The only reliable check is to attempt the download and verify the response is a valid PDF (not HTML).
- **Use `curl` with User-Agent.** IEEE blocks headless requests without a browser User-Agent header. Always include `-H "User-Agent: Mozilla/5.0"` in download commands.
- **DOM scraping for search results.** Use `browser_action(action='evaluate')` with JavaScript (`document.querySelectorAll`) to extract article titles and document IDs (`arnumber`) from search result pages. Screenshot-based extraction (`analyze_screenshot`) does not work — the environment lacks a vision model.
- **PDF download URL pattern:**
  ```
  https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={ARNUMBER}
  ```
- **Validate downloaded files.** After download, run `file -b <path>` — if it returns `HTML document` instead of `PDF document`, the paper is paywalled and the download is invalid. Delete the file and skip.

### ArXiv

**Base search URL:**
```
https://arxiv.org/search/?query={QUERY}&searchtype=all&order=-announced_date_first
```

**API endpoint (preferred for structured data):**
```
http://export.arxiv.org/api/query?search_query=all:{QUERY}&sortBy=submittedDate&sortOrder=descending&max_results=20
```

**Critical lessons learned:**

- **Do NOT use `browse_page` for the ArXiv API.** It is an XML endpoint, not a DOM-renderable page. Use `run_command` with `curl` instead. `browse_page` will timeout.
- **PDF download URL pattern:**
  ```
  https://arxiv.org/pdf/{ARXIV_ID}.pdf
  ```
- **ArXiv is 100% open access.** Every paper on ArXiv can be downloaded without authentication.
- **ArXiv IDs encode the submission year.** Format: `YYMM.NNNNN` where `YY` is the two-digit year. Filter by prefix to restrict to a date range.
- **Prefer ArXiv for paywall bypass.** Many IEEE/ACM papers have preprint versions on ArXiv, often with a note like "Accepted at ICPM/BPM/CAiSE". Use ArXiv as the fallback when IEEE or Scholar return paywalled results.

### Google Scholar

**Base search URL:**
```
https://scholar.google.com/scholar?q={QUERY}&as_ylo={YEAR}
```

**Critical lessons learned:**

- **Look for `[PDF]` links in results.** These indicate direct PDF links, usually to author homepages or preprint servers. Use `browser_action(action='evaluate')` to extract these links.
- **Most Scholar results point to paywalled publishers.** Expect a high ratio of paywalled papers. The `[PDF]` marker is the main signal for free access.
- **Download verification is mandatory.** After downloading, verify with `file -b`. HTML responses mean paywall or redirect — delete and skip.
- **Author homepage PDFs may have unpredictable naming.** Save them with descriptive names, not raw filenames.

### Semantic Scholar

**API endpoint:**
```
https://api.semanticscholar.org/graph/v1/paper/search?query={QUERY}&year=2025-2026&fieldsOfStudy=Computer+Science&limit=20&fields=title,externalIds,openAccessPdf,abstract,year
```

**Critical lessons learned:**

- **The API may block requests (403 Forbidden).** If this happens, use `web_search` with `site:semanticscholar.org` as a fallback, or search for the paper titles on ArXiv.
- **The `openAccessPdf` field is the key signal.** It contains a direct URL to the PDF when available. If it is `null`, the paper is paywalled.
- **Rate limits apply.** Add a small delay between API calls if making multiple requests.

### Alternative Open Access Sources

When a paper is paywalled on its primary source, try these alternatives in order:

1. **ArXiv** — search for the paper title on `arxiv.org`
2. **PubMed Central** — for healthcare/clinical process mining papers
3. **Springer Open / Nature Scientific Reports** — some papers are open access
4. **Author institutional repositories** — linked from Google Scholar profiles
5. **Preprint servers** (Preprints.org, TechRxiv, bioRxiv)

## Download Protocol

### Directory Structure

Downloaded PDFs are stored in the skill state directory (set automatically by the runtime):

```
$OUROBOROS_SKILL_STATE_DIR/downloads/
├── ieee_pdfs/       # IEEE Xplore downloads
├── arxiv_pdfs/      # ArXiv downloads
├── scholar_pdfs/    # Google Scholar / other downloads
```

The default output directory is `$OUROBOROS_SKILL_STATE_DIR/downloads` (resolved automatically).
For manual downloads outside the script, use `$OUROBOROS_SKILL_STATE_DIR/downloads/` as the base.

### Download Command Template

```bash
curl -s -L -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  -o "$OUROBOROS_SKILL_STATE_DIR/downloads/{SOURCE}_pdfs/{FILENAME}.pdf" \
  "{URL}"
```

### Validation Command

```bash
file -b "$OUROBOROS_SKILL_STATE_DIR/downloads/{SOURCE}_pdfs/{FILENAME}.pdf"
# Expected: "PDF document, version ..."
# If "HTML document" → paywall/redirect → delete and skip
```

### File Naming Convention

| Source | Pattern | Example |
|--------|---------|---------|
| IEEE | `{arnumber}_{Short_Title}.pdf` | `11389744_PROMSHA.pdf` |
| ArXiv | `{arxiv_id}_{Short_Title}.pdf` | `2501.13576_Federated_Conformance_Checking.pdf` |
| Scholar | `{Author}_{Short_Title}.pdf` | `Grohs_Beyond_Log_Model_Moves.pdf` |

Use underscores, no spaces. Keep titles under 50 chars.

## Synthadoc Ingestion Protocol

### Purpose Alignment

The `pm-wiki` purpose is:
> "This wiki covers: Process Mining knowledge base. Include: topics directly related to Process Mining knowledge base. Exclude: unrelated domains."

All Process Mining papers fall within scope. If ingestion fails with "out of scope", the paper URL may need to be ingested by title search or direct PDF path instead.

### Ingestion Methods

1. **URL ingestion** (preferred):
   ```
   synthadoc_ingest(source="https://arxiv.org/abs/2501.13576")
   ```

2. **PDF file ingestion** — ingest by file path for local PDFs that URL ingestion cannot reach.

### Deduplication

Before ingesting, check existing pages with:
```
synthadoc_list_pages()
synthadoc_search(terms="paper title keywords")
```

Skip papers that already have a page in the wiki. The wiki currently has 64+ pages. Always verify before adding.

### Post-Ingestion Verification

After ingestion, verify the page was created:
```
synthadoc_search(terms="paper title")
```

## Workflow: End-to-End Paper Collection

```
1. Run skill_exec to batch-search ArXiv + Semantic Scholar and download PDFs
2. Parse the JSON output; ingest new papers into Synthadoc via synthadoc_ingest
3. For IEEE Xplore (manual):
   a. Search with keywords + date filter
   b. Extract paper metadata via browser_action(DOM scraping)
   c. Check if paper already exists in synthadoc → skip if yes
   d. Attempt PDF download with curl + User-Agent
   e. Validate download (file -b → must be PDF, not HTML)
   f. If paywalled → try ArXiv preprint
   g. Ingest into synthadoc
4. For Google Scholar (manual):
   a. Search with [PDF] link extraction
   b. Download and validate as above
5. Report: new papers added, paywalled papers skipped, errors encountered
```

## Known Issues and Workarounds

| Issue | Workaround |
|-------|-----------|
| IEEE Open Access filter returns empty | Don't use URL filter; check PDF availability by download |
| IEEE blocks headless requests | Always use `curl -H "User-Agent: Mozilla/5.0"` |
| `analyze_screenshot` fails (no vision model) | Use `browser_action(action='evaluate')` for DOM scraping |
| `browse_page` times out on API endpoints | Use `run_command` with `curl` for XML/JSON APIs |
| Semantic Scholar API returns 403 | Use `web_search` with `site:semanticscholar.org` as fallback |
| ArXiv API times out in browser | Use `curl` directly, never `browse_page` |
| Shell operator chaining fails in `run_command` | Use `["sh", "-c", "cmd1 && cmd2"]` format |
| Synthadoc ingest skips IEEE URLs | Try the ArXiv version or search by title |
| `list_files(root='artifact_store')` errors | Use `run_command` with `find` or `ls` instead |
| Read-only subagents cannot use `curl` | Do not delegate download tasks to read-only subagents |

## Statistics (as of 2026-07-14)

| Metric | Value |
|--------|-------|
| Total PDFs on disk | 116 |
| IEEE papers | 8 |
| ArXiv papers | 99 |
| Scholar papers | 8 |
| Synthadoc wiki pages | 109 |
| Keywords defined | 18 |
| Script batch mode | v0.2.0 (ArXiv + Semantic Scholar) |
