---
name: cemak-design
description: Use this skill to generate well-branded interfaces and assets for CEMAK, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

CEMAK is an EU-based financial audit, accounting, HR, and procurement firm serving large enterprises. The voice is **trustworthy, understated, approachable to non-experts** — quiet expertise. Visual direction is neutral-first (slate + white) with the logo's teal → indigo gradient reserved as accent only.

Key files:
- `colors_and_type.css` — all design tokens as CSS custom properties
- `assets/logo.png` — primary mark (interlocking double-loop, teal→indigo gradient)
- `preview/*.html` — design system reference cards
- `ui_kits/marketing/` — public website
- `ui_kits/portal/` — client-facing dashboard
- `ui_kits/workspace/` — internal audit workspace

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.
