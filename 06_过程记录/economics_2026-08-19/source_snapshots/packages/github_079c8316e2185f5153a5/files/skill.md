---
name: hn-digest
description: Fetch Hacker News front page data, identify the topics drawing the most visible attention, optionally inspect selected comment threads for deeper discussion signals, explain them in plain language for business school PhD readers with limited technical background, and save a dated markdown digest.
tools: Bash, Write, AskUserQuestion
---

# HN Digest

Produce a dated Hacker News digest in markdown through a two-stage workflow that defaults to only two batch fetch-and-parse passes.

## Purpose

Use this skill when the user wants a fast, archived summary of the current Hacker News front page, written in plain language and saved as a local markdown file. The skill should normally use one batch pass for the Step 1 full numbered list and one batch pass for the selected deep-dive threads. Default to the smallest number of Bash calls that can complete the workflow reliably. In the normal path, this means one batch Bash call for Step 1 and one batch Bash call for Step 2.

Before using this skill, remind the user to turn on a VPN if Hacker News is not reachable from their current network.

## Trigger conditions

Use this skill when the user asks to:
- summarize Hacker News
- fetch today's Hacker News front page
- explain what Hacker News users care about most
- save an HN digest as markdown
- create a daily or one-off HN archive

Examples:
- `/hn-digest`
- `Summarize Hacker News and save an archive.`
- `Fetch HN, tell me what people care about most, and save a markdown digest.`
- `Give me a business-school-friendly summary of today's Hacker News.`

## Deep-dive focus types

Six focus types are available for targeted extraction in Step 2. They are grouped by mode:

| # | 中文 | English | Mode |
|---|------|---------|------|
| 1 | 事实与原话 | Facts and quotes | academic |
| 2 | 观点整合 | Opinion synthesis | always included |
| 3 | 研究切口 | Research angle | academic |
| 4 | 商业含义 | Business implications | academic |
| 5 | 技术选型与实现 | Tech stack and implementation | industry |
| 6 | 可以自己做什么 | Build ideas | industry |

Mode mapping:
- `academic`: opinion synthesis (always, placed first) + facts and quotes + research angle + business implications
- `industry`: opinion synthesis (always, placed first) + tech stack and implementation + build ideas
- `both`: all six types, with opinion synthesis placed first

When the user selects items in Step 2, they also specify a mode (`academic`, `industry`, or `both`). The mode determines which focus types appear in each item's extraction. The user may assign different modes to different items. Opinion synthesis is always included and always appears first under each item.

These same six types are also used in Step 1 to generate per-item suggested deep-dive directions. See Step 1 Format for details.

## Step 1

### Input

#### Input format
The user asks for a summary of the current Hacker News front page. The request may specify a language, and may imply that the result should be saved as a local archive.

#### Required parameters
- `source_url`: default to `https://news.ycombinator.com/`
- `language`: English or Chinese. If the user does not specify, ask with `AskUserQuestion` before drafting.

#### Optional parameters
- `archive_dir`: default to `~/Downloads/hn-digest/`
- `filename_pattern`: default to `hacker-news-digest-YYYY-MM-DD-HHMM.md`

#### Fixed parsing reference
Use a single batch Bash call with a small Python 3 script.

Reference template:

```python
import urllib.request, re, html, json
from urllib.parse import urljoin

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 HN-Digest/1.0'
PAGE_URL = 'https://news.ycombinator.com/'


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')


def clean_text(raw: str | None) -> str | None:
    if raw is None:
        return None
    value = html.unescape(re.sub(r'<[^>]+>', ' ', raw))
    value = re.sub(r'\s+', ' ', value).strip()
    return value or None


def parse_page(page_url: str) -> list[dict]:
    text = fetch_text(page_url)
    rows = re.findall(
        r'<tr class="athing submission" id="(?P<id>\d+)">([\s\S]*?)</tr>\s*<tr[^>]*>\s*<td colspan="2"></td>\s*<td class="subtext">([\s\S]*?)</td>\s*</tr>',
        text,
    )

    items = []
    for offset, (item_id, story_row, subtext_row) in enumerate(rows):
        title_m = re.search(r'<span class="titleline">\s*<a href="([^"]+)"[^>]*>([\s\S]*?)</a>', story_row)
        domain_m = re.search(r'<span class="sitestr">([\s\S]*?)</span>', story_row)
        rank_m = re.search(r'<span class="rank">(\d+)\.</span>', story_row)
        score_m = re.search(r'<span class="score" id="score_\d+">(\d+) points?</span>', subtext_row)
        user_m = re.search(r'<a href="user\?id=[^"]+" class="hnuser">([\s\S]*?)</a>', subtext_row)
        comments_m = re.search(
            r'<a href="(item\?id=\d+)">\s*(\d+|discuss)\s*(?:&nbsp;|\s)comments?\s*</a>',
            subtext_row,
        )

        comments_path = None
        comments_raw = None
        if comments_m:
            comments_path = comments_m.group(1)
            comments_raw = comments_m.group(2)

        title = clean_text(title_m.group(2)) if title_m else None
        outbound_url = html.unescape(title_m.group(1)) if title_m else None
        comments_url = (
            urljoin('https://news.ycombinator.com/', comments_path)
            if comments_path
            else urljoin('https://news.ycombinator.com/', f'item?id={item_id}')
        )

        if comments_raw and comments_raw.isdigit():
            comment_count = int(comments_raw)
        elif comments_raw == 'discuss':
            comment_count = 0
        else:
            comment_count = None

        items.append({
            'display_number': 1 + offset,
            'visible_rank': int(rank_m.group(1)) if rank_m else None,
            'item_id': item_id,
            'title': title,
            'outbound_url': outbound_url,
            'source_domain': clean_text(domain_m.group(1)) if domain_m else None,
            'points': int(score_m.group(1)) if score_m else None,
            'comment_count': comment_count,
            'submitter': clean_text(user_m.group(1)) if user_m else None,
            'comments_url': comments_url,
        })
    return items


try:
    all_items = parse_page(PAGE_URL)
    errors = []
except Exception as e:
    all_items = []
    errors = [{'page': PAGE_URL, 'error': str(e)}]

print(json.dumps({'items': all_items, 'errors': errors}, ensure_ascii=False, indent=2))
```

The script should do all of the following in one pass:
- fetch `https://news.ycombinator.com/` with a normal browser-like user agent
- parse each visible submission row with its following metadata row
- build structured records before drafting any list text
- assign sequential display numbers starting from `1` based on visible order on the page
- extract display number, visible rank, title, outbound URL, source domain, points, comment count, submitter, and comments-page URL
- keep items with missing fields and mark those fields as missing
- use visible HN signals, especially comments, points, and rank, to help surface what drew attention
- return structured data so the assistant can present every visible item with a sequential numeric identifier

### Output

Step 1 outputs a full numbered topic list in chat, then stops for user selection.

### Format

For each visible item on the front page, include:
- a single display number
- exact title from HN
- HN signal with points, comments, and rank when visible
- source domain when visible
- a plain-language summary line
- a why-it-matters line
- 2–3 dynamically chosen deep-dive directions selected from the six focus types based on each item's content, each with a one-line reason explaining why this item suits that angle

The directions must vary across items based on content. Do not repeat the same set of directions for every item. These suggested directions are for reference only; the actual focus types included in any deep dive are determined by the user's chosen mode.

When the output language is Chinese, prefer this compact structure:

- `1. [准确标题]`
  - `HN 信号：X 分 · Y 条评论 · 排名 Z`
  - `来源：domain.com`
  - `这条在讲什么：一句话说明`
  - `为什么值得关注：一句话说明`
  - `可深入方向：[从六个焦点类型中根据内容动态选取 2–3 个，每个附一句话理由]`

Chinese dynamic direction example:
  - `可深入方向：研究切口（定价策略变化可能是平台经济学的好案例）· 商业含义（对下游 AI 创业公司成本结构有影响）`

When the output language is English, prefer this compact structure:

- `1. [Exact title]`
  - `HN signal: X points · Y comments · rank Z`
  - `Source: domain.com`
  - `What this is about: one-line explanation`
  - `Why it matters: one-line explanation`
  - `Suggested angles: [dynamically chosen 2–3 from the six focus types, each with a brief reason]`

English dynamic direction example:
  - `Suggested angles: Research angle (pricing change may offer a natural experiment for platform economics) · Build ideas (open-source tool, could fork and extend for personal use)`

After listing all items, ask which numbers to deepen and which mode to use (`academic`, `industry`, or `both`). The user may also decline to deep-dive any item; see the Procedure notes for the skip-Step-2 path. The user may assign different modes to different items, for example `4, 18 academic` or `4 industry; 18 both`. Because the option count will often exceed four, prefer asking in normal chat rather than `AskUserQuestion`.

### Criteria

#### Acceptance checks
A successful Step 1 must:
- fetch the HN front page: `https://news.ycombinator.com/`
- extract visible news item records before drafting the list text
- include every parsed visible item in a numbered list, with sequential display numbers starting from `1` based on the actual number of items present
- include the exact title from HN for every item
- use visible HN signals, especially comments, points, and rank, to help the user decide what drew attention
- show 2–3 dynamically chosen deep-dive directions per item
- return the full numbered list in chat
- stop and ask the user which numbers to deepen and which mode to use
- normally complete the whole step with one batch Bash pass

#### Validation rules
- Use `Bash` with a small local Python script, not `WebFetch`
- Use Python 3 and prefer standard-library modules
- Complete fetch and parse inside the same Bash execution during the normal path
- Avoid extra inspection calls unless the normal parser fails or the site markup has materially changed

#### Boundary conditions
- If the user does not specify a language, ask a short Chinese-or-English question first with `AskUserQuestion`
- If some fields are missing, say they are missing
- If the fetch result is incomplete, continue with the best visible data and state the limitation in the full numbered list or later digest
- If the user has not yet chosen which topics to deepen, stop after Step 1

## Step 2

### Input

#### Input format
Input to Step 2 is the user's selection from the Step 1 numbered list plus a mode (`academic`, `industry`, or `both`). The user may assign different modes to different items.

#### Required parameters
- `selected_threads`: the user-chosen items to inspect
- `mode`: `academic`, `industry`, or `both`, determining which focus types to apply per item. See the "Deep-dive focus types" table for the mapping.
- `source_url`: default to `https://news.ycombinator.com/`
- `language`: English or Chinese, inherited from Step 1

#### Optional parameters
- `archive_dir`: default to `~/Downloads/hn-digest/`
- `filename_pattern`: default to `hacker-news-digest-YYYY-MM-DD-HHMM.md`

#### Fixed parsing reference
Once the user selects items, the thread URLs are already known from Step 1. Reuse the parsed Step 1 records rather than rediscovering the URL pattern.

Use a single batch Bash call with a small Python 3 script that loops through all selected HN item or comment pages in one execution.

The script should follow this outline unless the HN markup has materially changed:
- fetch each selected thread page with a normal browser-like user agent
- pause at least 1 second between thread fetches
- if one thread fails, continue with the others and record the error
- extract thread-level metadata such as title, points, total visible comments, and thread URL
- extract visible comment rows first, then pull user, age, depth, and cleaned text from each row
- treat the thread as usable only if it yields at least one non-empty cleaned comment
- return up to 30 non-empty comments per thread to control output size
- return per-thread parse checks, including comment rows found, non-empty comments extracted, and the comments themselves

Reference template:

```python
import urllib.request, re, html, json, time

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 HN-Digest/1.0'


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')


def clean_comment_html(raw: str) -> str:
    raw = re.sub(r'<pre><code>[\s\S]*?</code></pre>', ' [code block] ', raw)
    raw = re.sub(r'<p>', '\n\n', raw)
    raw = re.sub(r'<a [^>]*>(.*?)</a>', r'\1', raw)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    raw = html.unescape(raw)
    raw = re.sub(r'[^\S\n]+', ' ', raw)
    raw = re.sub(r'\n{3,}', '\n\n', raw)
    return raw.strip()


def parse_thread(item_url: str) -> dict:
    text = fetch_text(item_url)
    title_m = re.search(r'<title>(.*?) \| Hacker News</title>', text)
    score_m = re.search(r'<span class="score" id="score_\d+">(\d+) points?</span>', text)
    total_comments_m = re.search(r'>(\d+)&nbsp;comments?<', text)
    blocks = re.findall(r'<tr class="athing comtr"[\s\S]*?</tr>\s*</table></td></tr>', text)

    comments = []
    for block in blocks:
        user_m = re.search(r'<a href="user\?id=[^"]+" class="hnuser">(.*?)</a>', block)
        age_m = re.search(r'<span class="age"[^>]*><a href="item\?id=\d+">(.*?)</a></span>', block)
        depth_m = re.search(r'<td class="ind" indent="(\d+)">', block)
        text_m = re.search(r'<div class="commtext(?: [^"]+)?">([\s\S]*?)</div><div class="reply">', block)
        if not text_m:
            text_m = re.search(r'<div class="commtext(?: [^"]+)?">([\s\S]*?)</div>', block)
        if not text_m:
            continue
        cleaned = clean_comment_html(text_m.group(1))
        if not cleaned:
            continue
        comments.append({
            'user': html.unescape(user_m.group(1)) if user_m else None,
            'age': html.unescape(age_m.group(1)) if age_m else None,
            'depth': int(depth_m.group(1)) if depth_m else None,
            'text': cleaned,
        })

    return {
        'item_url': item_url,
        'title': html.unescape(title_m.group(1)) if title_m else None,
        'points': int(score_m.group(1)) if score_m else None,
        'comments_total_visible': int(total_comments_m.group(1)) if total_comments_m else None,
        'comment_rows_found': len(blocks),
        'non_empty_comments_extracted': len(comments),
        'comments': comments[:30],
    }


# Fill THREADS from Step 1 results: list of (item_id, comments_url, title)
THREADS = [
    # ('12345678', 'https://news.ycombinator.com/item?id=12345678', 'Example Title'),
]

results = []
errors = []
for i, (item_id, url, title) in enumerate(THREADS):
    try:
        result = parse_thread(url)
        result['item_id'] = item_id
        result['requested_title'] = title
        results.append(result)
    except Exception as e:
        errors.append({'item_id': item_id, 'url': url, 'title': title, 'error': str(e)})
    if i < len(THREADS) - 1:
        time.sleep(1)

print(json.dumps({'threads': results, 'errors': errors}, ensure_ascii=False, indent=2))
```

### Output

Step 2 outputs:
1. a saved markdown digest file
2. a short final chat response with the saved path and strongest themes

### Format

#### Final file type
- Markdown (`.md`)

#### Naming constraints
- Save under `~/Downloads/hn-digest/` unless the user explicitly requests another path
- Use the filename format `hacker-news-digest-YYYY-MM-DD-HHMM.md`
- Expand `~` to the real local home directory before writing

#### Required sections in the final saved digest
Use this order strictly. Do not add or remove sections.

1. Title
2. Source
3. Fetched at
4. `Part 1: Summary` / `第一部分：摘要 (Summary)`
5. `Part 2: Targeted extraction` / `第二部分：针对性提取 (Targeted extraction)`
6. Caveats

The final digest uses the user's selected mode only for Part 2 targeted extraction. Part 1 Summary should always summarize the hottest topics on the HN front page that day, not just the items the user selected.
#### Thread inspected field

In Part 2, each selected item includes a `Thread inspected` field. `yes` means the thread's comments were successfully fetched and parsed. `no` means the thread was selected but the fetch or parse failed; in that case, the extraction for that item is based only on Step 1 metadata and the item's title, not on comment evidence.

#### Per-item section structure in Part 2

Each selected item in Part 2 uses the following structure. Include only the sections determined by that item's mode. Opinion synthesis is always included and always appears first.

```
### N. [Exact title]
- Link: ...
- Source domain: ...
- HN signal: X points, Y comments, rank Z
- Mode: academic / industry / both
- Thread inspected: yes / no

- Opinion synthesis                          ← always included, always first
    - ...
    - ...
- Facts and original quotes                  ← academic and both only
    - ...
    - ...
- Research angle                             ← academic and both only
    - ...
    - ...
- Business implications                      ← academic and both only
    - ...
    - ...
- Tech stack and implementation              ← industry and both only
    - ...
    - ...
- Build ideas                                ← industry and both only
    - ...
    - ...
```

#### Digest template (English)

```md
# Hacker News Digest — YYYY-MM-DD HH:MM

Source: https://news.ycombinator.com/
Fetched at: YYYY-MM-DD HH:MM local time

## Part 1: Summary

### What was hottest today

- **[Exact title of topic cluster or news item]**
  - HN signal: cite points, comments, and rank for the most relevant high-signal posts.
  - What happened: explain the issue in plain language.
  - Opinion on HN: summarize the main opinions people expressed, using fetched comments when available for the hottest topics and visible HN signals otherwise.
  - Why it matters: explain the practical, organizational, market, or research significance.


## Part 2: Targeted extraction

### N. [Exact title]
- Link: ...
- Source domain: ...
- HN signal: X points, Y comments, rank Z
- Mode: academic / industry / both
- Thread inspected: yes / no

- Summary: explain the issue in plain language.
- Opinion synthesis
    - Viewpoint A: summarize who is arguing what, citing quotes when possible.
    - Viewpoint B: summarize the disagreement or alternative view.
    - What remains uncertain: state what the thread does not prove.
- Facts and original quotes
    - "Complete original quote from HN or source snippet." (Meaning: Explain what this quote means and why it matters.)
    - "Another complete original quote." (Meaning: Explain the claim, mechanism, or factual detail.)
- Research angle
    - Possible research question (with clear effect of interest): the impact of XX on XX
    - Potential Data source:...
    - Potential identification strategy hinted (IV/RDD/DID): ...
    - Literature gap or connection: ...
- Business implications
    - Market or organizational impact: ...
    - Strategic, regulatory, or labor angle: ...
- Tech stack and implementation
    - Technologies mentioned: ...
    - Architecture or approach: ...
    - Open source availability: ...
    - Feasibility for a solo developer: ...
- Build ideas
    - What you could build on top of this: ...
    - MVP scope: ...
    - Key resources or dependencies: ...

## Caveats

- This digest is a snapshot of the HN front page and selected comment threads at one point in time.
- HN comments and points are attention signals, not proof that a claim is true or important.
- Quoted comments reflect visible HN comments fetched during this run.
- Comments are capped at 30 per thread; some viewpoints may not be represented.
- Some news may require reading the original link before using them in research or teaching.
```

#### Digest template (Chinese)

```md
# Hacker News 摘要 — YYYY-MM-DD HH:MM

来源：https://news.ycombinator.com/
抓取时间：YYYY-MM-DD HH:MM 本地时间

## 第一部分：摘要 (Summary)

### 今天最火热的话题是什么 (What was hottest today)

- **[准确标题]**
  - HN 信号：引用相关高信号帖子的分数、评论数、排名。
  - 发生了什么：用大白话解释。
  - HN 上的看法：总结主要观点，尽量基于抓取到的评论。
  - 为什么重要：解释实际意义——商业、组织、市场或研究方面的影响。

## 第二部分：针对性提取 (Targeted extraction)

### N. [Exact title]
- Link: ...
- Source domain: ...
- HN signal: X points, Y comments, rank Z
- Mode: academic / industry / both
- 是否检查了评论区: yes / no

- 摘要：用通俗易懂的语言解释该issue/news。
- 观点综合
    - 观点A：总结谁在论证什么，尽可能引用原文。
    - 观点B：总结分歧或替代观点。
    - 仍不确定的部分：说明该讨论帖未能证明的内容。
- 事实与原文引用
    - "来自HN或信息源片段的完整原文引用。"（含义：解释这段引用的意思及其重要性。）
    - "另一段完整原文引用。"（含义：解释其中的论断、机制或事实细节。）
- 研究视角
    - 可能的研究问题（effect of interest）：XX对XX的影响
    - 潜在的数据来源：...
    - 潜在的识别策略（IV/RDD/DID）：...
    - 文献空白或关联：...
- 商业启示
    - 市场或组织影响：...
    - 战略、监管或劳动力视角：...
- 技术栈与实现
    - 提及的技术：...
    - 架构或方法：...
    - 开源可用性：...
    - 独立开发者的可行性：...
- 构建思路
    - 基于此可以构建什么：...
    - MVP（最小可行产品）范围：...
    - 关键资源或依赖：...

## 说明与局限

- 本摘要是 HN 首页和选中评论区在某一时刻的快照。
- HN 评论和分数是注意力信号，不等于事实或重要性的证明。
- 引用的评论来自本次抓取中可见的 HN 评论。
- 每个线程最多保留 30 条评论，部分观点可能未被覆盖。
- 某些新闻在用于研究或教学之前可能需要阅读原始链接。
```

#### Simplified digest format (skip Step 2)

When the user declines to deep-dive any item, save a simplified digest containing only the title, source, fetch time, Part 1 Summary, and Caveats. Omit Part 2 entirely.

In the simplified digest:
- The `What was hottest today` / `今天最火热的话题是什么` section is based solely on Step 1 signal data (points, comment count, rank) and item titles. Do not claim to know what commenters said.
- The `Main opinions from inspected threads` / `所选帖子中的主要观点` section is omitted because no threads were inspected.
- Add a line in Caveats noting that no comment threads were inspected in this run.

When mode is `both`, include all six focus type sections. When mode is `academic`, include only opinion synthesis, facts and original quotes, research angle, and business implications. When mode is `industry`, include only opinion synthesis, tech stack and implementation, and build ideas. Opinion synthesis always appears first under each item.

### Evidence and quote requirements

When extracting facts, quotes, mechanisms, technical details, or data sources:
- Use direct quotes for important factual claims and representative opinions.
- Quote enough surrounding text for the claim to be understandable. Do not reduce important quotes to vague paraphrase.
- After every quote, add a short `Meaning` / `含义` line explaining what the quote implies in plain language.
- Attribute quotes to the visible HN commenter when available.
- Keep quoted text in the original language. If the digest language is Chinese and the quote is English, preserve the English quote and explain it in Chinese.
- Do not invent quotes. If a source article or comment was not fetched, say so.
- Separate facts from insights. Label insights as `Insight` / `洞察`, not as fact.
- For opinion synthesis, integrate multiple visible viewpoints and disagreements, preserving the strongest original wording through quotes.

### Criteria

#### Acceptance checks
A successful Step 2 must:
- fetch the selected HN comment threads after the user chooses
- parse all selected threads inside one batch Bash execution during the normal path
- pause at least 1 second between thread fetches
- extract non-empty visible comment text from at least one selected thread before drafting the digest
- include a per-thread parse check such as total comment rows found, non-empty comments extracted, and a short sample of cleaned comments
- include the exact title from HN for every selected item in the digest
- apply the correct mode-determined focus types per item
- save a markdown file locally
- return the saved file path in the final response
- normally complete the whole step with one batch Bash pass

#### Validation rules
- Parse comments in a way that tolerates minor class-name variation or wrapper changes in HN markup
- Treat a selected thread as usable only if it yields at least one non-empty cleaned comment
- Keep the saved markdown fully consistent with the selected language

#### Boundary conditions
- If a thematic pattern is not supported by the extracted news, omit that pattern rather than forcing one
- If Step 2 fetches selected threads successfully but every selected thread yields zero usable comments, treat the parse as failed rather than silently continuing
- If the normal batch parser fails, fall back to minimal debugging or recovery steps, but treat that as an exception rather than the default flow
- If Step 2 parsing fails, report the limitation explicitly instead of pretending the digest was grounded in comment evidence
- If one thread fails but others succeed, continue with the successful threads and note the failure in the digest

## Procedure notes

Normal flow:
1. Confirm or ask for the output language.
2. Remind the user to turn on a VPN if Hacker News may be unreachable from their network.
3. Run Step 1 with one batch Bash fetch-and-parse pass over the front page, then show the full numbered list.
4. Ask which items to deepen and which mode to use (`academic`, `industry`, or `both`). The user may assign different modes to different items.
5. If the user declines to deep-dive any item, skip Step 2: draft a simplified digest containing only Part 1 Summary and Caveats (no Part 2), save it with `Write`, and return the archive path.
6. Otherwise, reuse Step 1 thread URLs and run Step 2 with one batch Bash fetch-and-parse pass.
7. If every selected thread yields zero usable comments, stop and treat it as a parser failure.
8. Draft the full digest. Part 1 Summary and Part 2 Targeted extraction are both written after Step 2 completes. Part 1 should summarize the hottest topics on the HN front page that day as a whole, not just the user-selected items. It may use comment data fetched in Step 2 when those threads overlap with the hottest topics, but it should not be constrained by the user's selection. Save the digest with `Write`, and return the archive path plus the strongest themes.

Normal execution should use two Bash calls total: one for Step 1 and one for Step 2. Extra calls are only for failure recovery. One batch Bash call for Step 1 and one batch Bash call for Step 2 is the target in all normal cases.

## Audience and writing guidance

Write for smart readers with limited technical background.

- Use plain language in the chosen output language.
- Avoid jargon when possible.
- When a news item is technical, explain the practical meaning first.
- Focus on business relevance, organizational implications, labor, markets, incentives, regulation, AI adoption, entrepreneurship, or research opportunities when relevant.
- Do not overclaim from headlines alone.
- Keep sentences fairly short.
- Prefer concrete explanation over hype.

If writing in Chinese:
- write natural Chinese, not translation-like Chinese
- explain technical topics in everyday terms first
- keep headings and bullets in Chinese

## Safety and non-goals

- This skill is for quick daily digestion and archiving.
- It is not a substitute for reading source articles.
- It is not a full news crawler.
- It is not a historical database.
- It should not default to multi-step exploratory parsing when a two-pass batch workflow is sufficient.