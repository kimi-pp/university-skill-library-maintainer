---
name: israeli-web-accessibility
description: >
  Make websites accessible according to Israeli law — Israeli Standard 5568 (ת"י 5568,
  based on WCAG at level AA) — and generate a legally-required Hebrew accessibility
  statement (הצהרת נגישות). Use this skill EVERY time you build, modify, or review a
  website or web app for an Israeli audience, even if the user did not mention
  accessibility — Israeli law requires accessibility for virtually all business and
  public websites, so accessibility is part of "building a website" in Israel, not an
  optional add-on. Also use it whenever the user mentions: נגישות, הנגשה, הצהרת נגישות,
  תקן 5568, תקנה 35, WCAG, accessibility audit, accessibility statement, or asks whether
  their site complies with Israeli accessibility law.
---

# Israeli Web Accessibility (ת"י 5568 / WCAG AA)

This skill makes websites comply with Israeli accessibility law and produces the
Hebrew accessibility statement (הצהרת נגישות) the law requires. It has three parts:

1. **Build accessible by default** — rules to apply while writing any HTML/CSS/JS.
2. **Audit** — automated + manual checks to verify compliance.
3. **Accessibility statement** — generate the legally-required הצהרת נגישות page.

Work through all three whenever you create or substantially modify a site. For an
audit-only request, start at part 2.

## Legal context (read this once, it shapes everything)

Israeli law (חוק שוויון זכויות לאנשים עם מוגבלות + תקנה 35 לתקנות נגישות השירות)
requires most websites serving the Israeli public to conform to Israeli Standard 5568
at level AA. ת"י 5568 adopts WCAG — building to **WCAG 2.1 AA** (aiming at 2.2 where
cheap) is the safe interpretation. Non-compliance exposes the site owner to lawsuits
with statutory damages without proof of harm, and these suits are common in practice.

Two things agents often get wrong:

- **An accessibility overlay/widget is NOT compliance.** Third-party "accessibility
  toolbar" widgets do not satisfy the law and do not replace accessible code. Never
  tell a user that adding a widget makes their site legal. (An optional widget on top
  of accessible code is fine.)
- **The accessibility statement is mandatory**, not decoration. A site without a
  proper הצהרת נגישות is non-compliant even if the code is perfect.

Exemption thresholds (small-business turnover), coordinator requirements, and damage
amounts are indexed and amended over time. `references/legal.md` has the full picture
with amounts as last verified (noted per item) — read it before advising a user on
whether they are exempt, and tell users to verify current thresholds with נציבות שוויון זכויות לאנשים
עם מוגבלות (gov.il) for anything that matters legally. Always include the disclaimer
that you are not a lawyer and final legal responsibility sits with the site owner.

## Part 1 — Build accessible by default

Apply these while writing code. They cover the failures that cause the vast majority
of real-world violations. The full criterion-by-criterion checklist is in
`references/checklist.md` — read it when auditing or when handling a component type
not covered below.

**Document & language**

- `<html lang="he" dir="rtl">` for Hebrew sites (set `lang`/`dir` per actual language;
  mark inline language switches with `lang` on the element).
- Unique, descriptive `<title>` per page. Meaningful heading hierarchy: one `<h1>`
  recommended, avoid skipped levels, headings describe their sections. (Gapless
  headings are best practice, not a hard WCAG failure — what matters is that the
  hierarchy reflects the real structure.)
- Use semantic landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`. Add a skip link
  ("דלג לתוכן הראשי") as the first focusable element.

**Text & visuals**

- Contrast ≥ 4.5:1 for normal text, ≥ 3:1 for large text (≥24px, or ≥18.66px bold)
  and UI components. Verify computed colors, not intentions.
- Never convey information by color alone. Text must be resizable to 200% without loss
  of content (avoid fixed px heights that clip text; prefer rem).
- Every `<img>` gets `alt`: descriptive for informative images, `alt=""` for decorative
  ones. Icon-only buttons get `aria-label` in the page language.

**Keyboard & focus**

- Everything operable by keyboard: real `<button>`/`<a href>` elements, not clickable
  `<div>`s. Logical tab order, no keyboard traps.
- Visible focus indicator — never `outline: none` without an equal-or-better
  replacement (`:focus-visible` styling).
- Modals: trap focus inside, close on Escape, return focus to the trigger.

**Forms**

- Every input has a programmatically-associated `<label>` (or `aria-label` when a
  visible label truly can't exist). Placeholder is not a label.
- Errors: identified in text (not color alone), associated to the field via
  `aria-describedby`, with `aria-invalid` on the field. Required fields marked in an
  accessible way. Autocomplete attributes on personal-data fields.

**Dynamic content & media**

- Announce async updates with `aria-live` regions where users need to know.
- Video: captions (כתוביות) required, plus audio description (or a full text/media
  alternative) when visual content isn't conveyed by the soundtrack (WCAG 1.2.3/1.2.5).
  Audio-only content needs a transcript; video-only needs a text or audio alternative.
- No content flashing more than 3 times/second. Anything auto-moving longer than 5
  seconds needs a pause control. No autoplaying audio over 3 seconds without control.

**RTL specifics (Hebrew sites)**

- Use logical CSS properties (`margin-inline-start`, `padding-inline-end`, `text-align:
  start`) so layout survives direction changes.
- Directional icons (arrows, chevrons, "back") must point correctly in RTL.
- Mixed Hebrew/English/numbers: use `dir="ltr"` spans or `<bdi>` for phone numbers,
  emails, and Latin product names inside Hebrew text.

**Documents & PDFs**

- PDFs published on the site must themselves be accessible (tagged, real text, reading
  order, alt text) — or provide an accessible HTML equivalent. This is an explicit
  legal requirement for documents published since 2017.

**Accessibility menu (תפריט נגישות) — include it by default**

Israeli users expect a visible accessibility menu, so include one on every site you
build with this skill (skip only if the user explicitly declines). Use the ready
implementation in `assets/a11y-widget-snippet.html` — a self-contained menu (no
third-party scripts) offering a text-size stepper, high contrast, grayscale, link
highlighting, readable font, reduced motion, large cursor, and a reading guide, with
proper widget accessibility built in: focus trap, Esc-to-close with focus return,
aria-expanded/aria-pressed states, and screen-reader announcements. Paste its three
blocks before `</body>` on every page, adapt the CSS custom properties to the site
palette (keep contrast ≥ 4.5:1), fix the statement link href, and add the menu to
the statement's adjustments list.

Be clear with the user about its status: the menu is a usability layer on top of
accessible code, not a substitute for it (see `references/legal.md`). Include it
only once the site passes the audits, never replace it with a third-party overlay
script, and never describe it as what makes the site compliant.

## Part 2 — Audit

Run both automated layers, then the manual pass. Automation catches roughly a third
to half of WCAG failures — never present an automated pass as full compliance.

Script paths below are relative to this skill's folder.

**Layer 1 — static scan (no browser needed):**

```bash
python3 scripts/static_check.py path/to/site-or-file [more paths...]
```

Scans HTML files for the most common violations (missing lang/alt/labels, empty
links/buttons, skipped headings, positive tabindex, outline:none, missing skip link,
etc.) and prints a report with file:line references. Works on any HTML — static
sites, build output (`dist/`), or exported pages.

**Layer 2 — rendered scan with axe-core (needs a browser; catches contrast, computed
ARIA, and JS-rendered content):**

```bash
node scripts/axe_audit.mjs <url-or-file> [more urls...]
```

Requires Node 18+ and Playwright (`npm i playwright axe-core`; if they're installed
elsewhere, set `NODE_PATH`; if Playwright's own browser download is unavailable, set
`CHROMIUM_PATH` to an existing Chrome/Chromium binary — the script also auto-detects
common locations and prints which browser it used). It reports two buckets:
**violations** (WCAG 2.0/2.1 A+AA — the legal baseline, drive the exit code) and
**advisory** (WCAG 2.2 + best practices — fix when cheap, but they are not ת"י 5568
failures; don't report them to the user as legal violations).

Run it against every distinct page template (home, content page, form page), not just
the homepage. The script audits each page as loaded — modals, open menus, and form
error states need either a small custom Playwright script that opens them and runs
axe there, or coverage via the manual pass.

**Layer 3 — manual pass (required, automation cannot check these):**

Go through the manual section of `references/checklist.md`. The critical ones: full
keyboard walkthrough of every flow (including modals and menus), focus visibility,
screen-reader sanity check of names/roles for custom components, captions on videos,
error-message experience on forms, and zoom to 200%.

**Report format** — after an audit, always report three buckets: (1) violations found
and fixed, (2) violations found and NOT fixed (with why and what's needed), (3) items
that require human/manual verification (screen-reader testing with real users, caption
accuracy, etc.). Bucket 3 is never empty — saying so would be dishonest.

## Part 3 — Accessibility statement (הצהרת נגישות)

Generate the statement **after** the site actually conforms — it declares facts, not
hopes. Full template with fill-in instructions: `references/statement-template.md`.

You need from the user (ask, don't invent): business name; accessibility contact
person — name, phone, email (this is the רכז נגישות if the org must appoint one);
whether the business has a physical location serving the public (if yes, its physical
accessibility arrangements); any parts of the site that are not accessible and the
alternative offered; any exemption the business relies on. If you're working
unattended and a detail is missing, insert a clearly-flagged placeholder (e.g.
`[להשלמה: שם העסק]`) and list every placeholder in your final report — never invent
real-looking details, and never ask the user for facts you produced yourself (which
tools you tested with, what adjustments you made — fill those from your own audit).

Rules:

- The statement is a dedicated page, in Hebrew, reachable from a clearly-labeled link
  ("הצהרת נגישות" or "נגישות") on every page — put it in the site footer.
- It must state the conformance level (ת"י 5568, רמה AA / WCAG 2.1 AA), list the
  adjustments actually made, name the contact for accessibility issues with real
  contact details, describe physical accessibility arrangements where relevant,
  disclose known gaps and their workarounds, and carry a last-updated date.
- Only list adjustments that are actually true for this site. Remove template items
  that don't apply. An inflated statement is a legal liability, not a safety net.
- Refresh the statement (and its date) whenever the site changes materially.
- The statement is the site owner's legal declaration, not yours. Generating it does
  not contradict the honesty rules below: you produce the draft because the site now
  passes the checks you can run, and you tell the owner to publish it only once
  they stand behind it — ideally after review by a מורשה נגישות.

## Honesty requirements

When you finish, tell the user plainly: what was made accessible, what automated
checks passed, what still needs human verification, and that full legal certainty
requires review by a certified accessibility expert (מורשה נגישות השירות) — required
by law in some cases and cheap insurance in the rest. Never claim "the site is now
legally compliant"; claim "the site conforms to the checks I can run, here is what
remains." This protects the user, and it is also simply the truth.
