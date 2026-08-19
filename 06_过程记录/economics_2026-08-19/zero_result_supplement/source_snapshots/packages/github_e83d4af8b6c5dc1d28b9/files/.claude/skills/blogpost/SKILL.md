---
name: blogpost
description: Add an entry to the running list of links at content/blog/ on dylanwgroves.com. Use whenever Dylan sends a URL, a quotation, a poem, a song, or an image he wants on the blog — including a bare link with no other request — or says post this, blog this, add this to the links, or put this on the site. Also use when he asks to edit or amend an entry already in content/blog/. Do not use for the writing/, research/, teaching/, or cv pages.
---

# Blog post

The blog is a **running list of links** — a commonplace book, not an essay site. Entries
are short: usually front matter alone, sometimes one line of reaction or a pulled quote.
The median post is 8 lines. Never write an essay.

## Workflow

1. **Fetch the source.** WebFetch the URL to get the real title, publication, and author.
   Never guess these from the slug. If the fetch fails (paywall, bot block), say so and ask
   Dylan for the title and source rather than inventing them.
2. **Write the file** to `content/blog/<slug>.md` per the format below.
3. **Show him the result** — the full file contents — and, if you are proposing tags,
   say so explicitly: *"Proposing tags: [...] — ok?"* Tags are never silently added.
4. **Wait for approval, then publish.** Do not touch git before he says yes. Once he
   approves ("good", "post", "yes"), go all the way: commit *and* push. He has been
   explicit that approval means the entry should appear on the website, not sit in a
   local commit. Then confirm it is actually live (see below) rather than assuming the
   Netlify build succeeded.

## File format

`content/blog/<slug>.md`, where `<slug>` is kebab-case, derived from the title, no type
prefix, and short — trim to the distinctive part (`west-africa-has-become-a-huge-cocaine-trading-hub`
is at the long end; `creatine`, `fruit-stickers`, `elite-failure` are typical).

```markdown
---
title: "Article: Narendra Modi's party discovers the limits of propaganda"
date: 2026-07-28T15:50:46-04:00
draft: false
link: "https://www.economist.com/..."
source: "The Economist"
tags: []
---
```

- **`title`** — a type prefix, then the source's own headline verbatim. See the prefix list below.
- **`date`** — current local time, ISO 8601 with offset. Get it, don't guess:
  `date +%Y-%m-%dT%H:%M:%S%:z` (Eastern; `-04:00` in DST, `-05:00` otherwise).
- **`draft`** — always `false`.
- **`link`** — the canonical URL. Omit the key entirely for entries with no source URL
  (loose quotations). If Dylan supplies an NYT gift link with `unlocked_article_code`,
  keep it intact — that is deliberate.
- **`source`** — the publication. Add the author in parens when the piece is
  bylined-and-personal: `"The New York Times (Kapil Komireddi)"`, `"Gojiberries (Gaurav Sood)"`.
  Plain publication name for wire-style or institutional pieces: `"The Economist"`.
  For a Substack, use the newsletter name and author: `"One Useful Thing (Ethan Mollick)"`.
- **`tags`** — default `[]`. See tagging below.

## Type prefixes

Reuse an existing prefix when one fits. In rough frequency order:

`Article:` · `Blog Post:` · `Quotation:` · `News Story:` · `Music:` · `Book Review:` ·
`Poem:` · `Podcast:` · `Paper:` · `Academic Paper:` · `Interview:` · `Profile:` ·
`Review:` · `Movie Review:` · `Movie:` · `Painting:` · `Photography:` · `Website:` ·
`Wikipedia Entry:` · `Editorial:` · `Opinion:` · `Open Letter:` · `Manifesto:` ·
`Statement:` · `Slides:` · `Guide:` · `Insight:` · `Evidence Review:` · `Link:`

Coining a new one is fine when nothing fits — `Magnificent Corner of the Internet:` and
`Etiquette Guide:` are both real. Keep it deadpan and descriptive.

`Article:` is for reported journalism; `Blog Post:` for personal/independent sites;
`Paper:`/`Academic Paper:` for journal work; `Opinion:`/`Editorial:` for op-eds.

## Body

**Default to nothing.** If Dylan sends a bare link, the file is front matter and nothing
else. Do not fill the space.

Write a body only when he gives you the material for one:

- **His reaction** — use his words, lightly cleaned up. One line, lowercase-casual is fine:
  `I always new the amount of ice Starbucks serves is bogus`. Never invent a reaction in
  his voice, and never editorialize on his behalf.
- **A quote he points to** — one striking sentence, with the speaker named inline:
  `Angelo Carusone, president of Media Matters for America, on Candace Owens: "She can create a story line and then push it."`
- **Related links** he mentions — one per line:
  `See also: [Wanted drug trafficker puts Sierra Leone's development aid at risk](https://www.ft.com/...)`

### Block quotations

For a substantial passage — an epigraph, a poem's context, an extended excerpt — use raw
HTML with an attribution footer (`unsafe = true` is on in `hugo.toml`):

```html
<blockquote>
<p>“The ability to be wrong is one of the most important virtues…”</p>
<footer class="attribution">– Alan Levinovitz</footer>
</blockquote>
```

Link the attribution when there's a URL:
`<footer class="attribution">Daniel Ellsberg — <a href="https://sriramk.com/..." target="_blank" rel="noopener">via sriramk.com</a></footer>`

### Poems

Markdown `>` blockquote, two trailing spaces for line breaks, `&nbsp;&nbsp;&nbsp;&nbsp;`
for indented lines. See `content/blog/gods-grandeur.md`.

### Images

Save to `static/blog/<slug>.<ext>` and reference as `/blog/<slug>.<ext>`. Write a real
alt text — for a chart, put the actual numbers in it:

```markdown
![Number of crawl requests per web traffic referral: Anthropic 2,800, OpenAI 331, … Source: Cloudflare, July 1–7, 2026.](/blog/anthropic-crawl-referrals.svg)
```

If Dylan hasn't sent the image file yet, leave an HTML comment placeholder naming the exact
path you expect, as in `content/blog/dagna-bembeya-jazz-national.md`.

## Tags

Two thirds of posts have `tags: []`. That is the correct default — reach for a tag only
when the entry clearly belongs to a running thread.

**Always state proposed tags explicitly and get approval.** Never add them silently.

Tags already in use: `political economy` (by far the most common), `visual culture`,
`AI`, `development economics`, `behavioral economics`, `public opinion`,
`political psychology`, `international law`, `electoral systems`, `Italy`, `labor`,
`religion`, `data visualization`, `elections`. Prefer one of these. A new tag is allowed
but needs his explicit yes.

Lowercase except proper nouns. Tags are metadata only — `[taxonomies]` is empty in
`hugo.toml`, so there are no tag browsing pages and nothing renders them.

## Committing

After he approves:

```
git add content/blog/<slug>.md
git commit -m "blog: <full title including prefix> (<source, publication only>)"
```

The subject drops the author parens from `source`, and uses the author's name instead of
the newsletter for Substacks — matching existing history:

- `blog: Article: Bullshit Jobs and Chickenshit Jobs (Arrowsmith Press)`
- `blog: Guide: An opinionated guide to which AI to use to do stuff (Ethan Mollick)`

For an edit to an existing entry, describe the change instead:
`blog: add See also links to West Africa cocaine trading hub post`

Then `git push origin main`, which triggers the Netlify build.

## Checking your work

**Confirm the entry is live.** A push is not a publication — Netlify still has to build.
After pushing, wait for the deploy and verify, rather than reporting success on the
strength of the push alone:

```bash
until curl -s https://dylanwgroves.com/blog/ | grep -q "<distinctive words from the title>"; do sleep 5; done
```

Builds take well under a minute. Then report the entry as live.

For an entry whose body has raw HTML, an image, or a poem, preview locally first with the
`hugo-server` config in `.claude/launch.json` (port 1313) and look at `/blog/`. Skip that
for a front-matter-only post.
