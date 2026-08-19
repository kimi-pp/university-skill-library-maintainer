---
name: perception-bootstrap
description: >
  MASTER ORCHESTRATOR for the Perception UI Design System — a Bootstrap-like component framework.
  This is the FIRST skill to read for ANY UI generation task. It routes to the correct sub-skills
  based on what the user is building. Use this skill whenever the user asks to create, design, build,
  style, or modify ANY visual UI — buttons, cards, inputs, modals, navbars, layouts, pages, dashboards,
  forms, tables, alerts, badges, tooltips, charts, loading states, or any other component. Also trigger
  when the user mentions colors, themes, surface modes, dark mode, light mode, accessibility, contrast,
  WCAG, design system, color palette, component library, or Bootstrap. This skill defines the architecture,
  routing logic, and generation workflow for an entire design system with 7 hues, 5 surface modes,
  6 sizes, and strict WCAG AA compliance. Every UI element produced under this system MUST follow
  the MC Perception rules. There are NO exceptions. If in doubt, read this skill.
---

# MC Perception — Master Orchestrator

## Architecture Overview

This design system has **4 layers**. Each layer builds on the ones below it. When generating UI, Claude MUST read skills **from the bottom up** — foundation first, then the relevant component/composition skill.

```
┌─────────────────────────────────────────────────────┐
│  LAYER 4: COMPOSITIONS (domain-specific assemblies)  │
│  dashboard · data-viz · financial-ux · presentation  │
├─────────────────────────────────────────────────────┤
│  LAYER 3: COMPONENTS (individual UI elements)        │
│  buttons · forms · selection · navigation            │
│  tables · loading · [future: modals, cards, alerts]  │
├─────────────────────────────────────────────────────┤
│  LAYER 2: PRINCIPLES (quality & decision rules)      │
│  design-principles · ui-design-rules · simplify      │
├─────────────────────────────────────────────────────┤
│  LAYER 1: FOUNDATION (color, surface, tokens)        │
│  palette · surface-modes · perception-ui-system      │
└─────────────────────────────────────────────────────┘
```

---

## Layer 1: FOUNDATION (Always Read)

These define the color system and are **mandatory for every UI task**. Read BEFORE any component work.

| File | Path | What It Defines |
|------|------|-----------------|
| **palette** | `references/foundation/skill-palette.md` | All 7 hue families × 10 steps, exact hex values, contrast ratios, JSON tokens |
| **surface-modes** | `references/foundation/skill-surface-mode.md` | 5 surface modes, pairing tables, interactive states, avoid lists |
| **perception-ui-system** | `references/foundation/skill-perception-ui-system.md` | Master rules: 7 hues × 5 modes × 6 sizes, WCAG requirements, forbidden actions, resolveMode/resolveSize functions |

### CRITICAL: The Variant Matrix

Every component MUST produce:
```
7 hues × 5 surface modes × 6 sizes = 210 variants
```

The 7 hues: `neutral`, `red`, `green`, `blue`, `yellow`, `magenta`, `teal`
The 5 modes: White (#FFFFFF), Black (#0A0A0A), Light (step 100), Dark (step 800), Mid (step 500)
The 6 sizes: `xs`, `sm`, `md`, `lg`, `xl`, `xxl`

---

## Layer 2: PRINCIPLES (Read for Quality)

These are cross-cutting quality rules. Read when you want to **elevate** the output beyond just "correct colors".

| File | Path | When to Read |
|------|------|--------------|
| **design-principles** | `references/principles/skill-design-principles.md` | Trade-off decisions, simplification, error prevention, progressive disclosure |
| **ui-design-rules** | `references/principles/skill-ui-design-rules.md` | The 58-rule checklist: empathy, layout, essentialism, guidance, aesthetics, novelty, consistency, engagement |
| **simplify-design** | `references/principles/skill-simplify-design.md` | Reducing complexity, decluttering, information hierarchy |

### When to Read Layer 2
- Building a **full page or layout** → read `ui-design-rules`
- Making **trade-off decisions** (feature scope, complexity) → read `design-principles`
- UI feels **cluttered or complex** → read `simplify-design`
- For simple single-component tasks (just a button), Layer 2 can be skipped

---

## Layer 3: COMPONENTS (Read Per Task)

Read the **specific component skill** for what the user is building. Always read Layer 1 first.

| Component | File | Triggers |
|-----------|------|----------|
| **Buttons** | `references/components/skill-button-design.md` | button, CTA, submit, action, fab, icon button |
| **Text Fields & Forms** | `references/components/skill-text-fields-forms-design.md` | input, form, text field, login, registration, search, dropdown, date picker |
| **Selection Controls** | `references/components/skill-selection-controls-design.md` | checkbox, radio, toggle, switch, segmented control, chips |
| **Navigation** | `references/components/skill-navigation-design.md` | navbar, sidebar, menu, tabs, breadcrumbs, bottom bar, hamburger |
| **Data Tables** | `references/components/skill-data-tables-design.md` | table, grid, data grid, sortable, filterable, pagination |
| **Loading & Progress** | `references/components/skill-loading-progress-indicators.md` | spinner, skeleton, progress bar, loading state, shimmer |

### Future Components (not yet created — use foundation rules)
- Cards, Alerts/Toasts, Modals/Dialogs, Badges/Tags, Tooltips/Popovers, Avatars, Pagination, Tabs, Accordions, Breadcrumbs, Steppers

For components without a dedicated skill, follow the **perception-ui-system** rules from Layer 1 (7 hues × 5 modes × 6 sizes + WCAG).

---

## Layer 4: COMPOSITIONS (Read for Domain Pages)

These assemble multiple components into domain-specific layouts. Read Layer 1 + relevant Layer 3 skills + the composition skill.

| Composition | File | Triggers |
|-------------|------|----------|
| **Dashboards** | `references/compositions/skill-dashboard-design.md` | dashboard, analytics, admin panel, overview, KPI, metrics |
| **Data Visualization** | `references/compositions/skill-data-visualization-design.md` | chart, graph, bar chart, line chart, pie chart, scatter, sparkline, recharts, d3 |
| **Financial UX** | `references/compositions/skill-financial-ux-design.md` | banking, fintech, trading, investment, payment, loan, insurance |
| **Presentations** | `references/compositions/skill-presentation-design.md` | slides, pitch deck, keynote, pptx, presentation |

---

## Routing Logic — Which Skills to Read

Use this decision tree for every request:

```
User request arrives
│
├─ Is it UI-related? ──No──→ Don't use this skill
│
Yes
│
├─ ALWAYS read: palette + surface-modes (Layer 1 foundation)
│
├─ What are they building?
│  │
│  ├─ Single component (button, input, toggle...)
│  │  └─ Read: perception-ui-system + matching component skill
│  │
│  ├─ Full page/layout (dashboard, login page, settings...)
│  │  └─ Read: perception-ui-system + relevant component skills + ui-design-rules
│  │     └─ If domain-specific: + matching composition skill
│  │
│  ├─ Design review/critique
│  │  └─ Read: ui-design-rules + design-principles + simplify-design
│  │
│  └─ Color/theme only
│     └─ Read: palette + surface-modes (already loaded)
│
└─ Generate output following the variant matrix
```

### Example Routing

| User Says | Skills to Load |
|-----------|----------------|
| "Create a button" | palette → surface-modes → perception-ui-system → button-design |
| "Build a login form" | palette → surface-modes → perception-ui-system → text-fields-forms → button-design |
| "Design a dashboard" | palette → surface-modes → perception-ui-system → dashboard-design → data-viz → navigation → data-tables |
| "Create a settings page" | palette → surface-modes → perception-ui-system → navigation → text-fields-forms → selection-controls → button-design |
| "Make a trading interface" | palette → surface-modes → perception-ui-system → financial-ux → dashboard-design → data-viz → data-tables |
| "Create a sidebar nav" | palette → surface-modes → perception-ui-system → navigation-design |
| "Add loading states" | palette → surface-modes → perception-ui-system → loading-progress-indicators |

---

## Component Generation Workflow

For EVERY component, follow this exact sequence:

### Step 1: Load Foundation
```
Read palette → get exact hex values
Read surface-modes → get pairing rules + interactive states
```

### Step 2: Define the Component API
```typescript
interface ComponentProps {
  hue: "neutral" | "red" | "green" | "blue" | "yellow" | "magenta" | "teal";
  mode: 1 | 2 | 3 | 4 | 5;
  size: "xs" | "sm" | "md" | "lg" | "xl" | "xxl";
  variant?: "filled" | "outlined" | "ghost" | "text";  // component-specific
  state?: "default" | "hover" | "pressed" | "focused" | "disabled";
  // ... component-specific props
}
```

### Step 3: Implement Color Resolution
```
resolveMode(hue, mode) → { bg, text, secondary, accent, btnBg, btnText, outline, icon, divider }
resolveSize(size) → { fontSize, py, px, radius, icon, minH }
resolveState(mode, state) → { color overrides for hover/pressed/focus/disabled }
```

### Step 4: WCAG Verification
For EVERY foreground/background pair, compute:
```
contrastRatio(fg, bg) using the WCAG luminance formula
Assert: text pairs ≥ 4.5:1, UI pairs ≥ 3.0:1
```

### Step 5: Render Preview
Show a representative grid:
- Rows = surface modes (at minimum: M1 White + M2 Black + one hue mode)
- Columns = sizes (at minimum: sm, md, lg)
- Show at least 2-3 hues

### Step 6: Output Complete Code
- Include the full palette as design tokens
- Include resolveMode + resolveSize functions
- Include the component with all props
- Include a showcase/storybook-style preview

---

## Design Token Structure

All components share these tokens:

### Color Tokens (from palette)
```
--perception-{hue}-{step}     e.g. --perception-blue-500: #5252ff
--perception-white: #FFFFFF
--perception-black: #0A0A0A
```

### Semantic Tokens (resolved per mode)
```
--surface-bg
--text-primary
--text-secondary
--accent
--btn-bg
--btn-text
--outline
--icon
--divider
--hover
--pressed
--focus-ring
--disabled
```

### Size Tokens
```
--font-xs: 11px    --py-xs: 4px     --px-xs: 8px     --radius-xs: 4px
--font-sm: 12px    --py-sm: 6px     --px-sm: 12px    --radius-sm: 5px
--font-md: 14px    --py-md: 8px     --px-md: 16px    --radius-md: 6px
--font-lg: 16px    --py-lg: 10px    --px-lg: 20px    --radius-lg: 7px
--font-xl: 18px    --py-xl: 12px    --px-xl: 24px    --radius-xl: 8px
--font-xxl: 20px   --py-xxl: 14px   --px-xxl: 28px   --radius-xxl: 10px
```

---

## Semantic Hue Mapping

When components have semantic meaning, map to hues:

| Semantic Role | Default Hue | Usage |
|---------------|-------------|-------|
| **Primary** | Blue | Default actions, links, primary buttons |
| **Success** | Green | Confirmations, positive states, completion |
| **Danger** | Red | Errors, destructive actions, alerts |
| **Warning** | Yellow | Caution, attention needed, pending |
| **Info** | Teal | Informational, neutral notifications |
| **Premium** | Magenta | Special features, premium tier, highlights |
| **Default** | Neutral | Chrome, borders, secondary elements |

Components CAN override hue via props — this mapping is the default.

---

## File Manifest

```
perception-bootstrap/
├── SKILL.md                                          ← YOU ARE HERE (orchestrator)
└── references/
    ├── foundation/
    │   ├── skill-palette.md                          ← All hex values + contrast ratios
    │   ├── skill-surface-mode.md                     ← 5 mode pairing tables
    │   └── skill-perception-ui-system.md             ← Master rules + variant matrix
    ├── principles/
    │   ├── skill-design-principles.md                ← 10 foundational principles
    │   ├── skill-ui-design-rules.md                  ← 58 UI quality rules
    │   └── skill-simplify-design.md                  ← 21 simplification rules
    ├── components/
    │   ├── skill-button-design.md                    ← Button patterns + hierarchy
    │   ├── skill-text-fields-forms-design.md         ← Forms + input UX
    │   ├── skill-selection-controls-design.md         ← Checkboxes, radios, toggles
    │   ├── skill-navigation-design.md                ← Navbars, sidebars, menus
    │   ├── skill-data-tables-design.md               ← Tables, grids, pagination
    │   └── skill-loading-progress-indicators.md      ← Spinners, skeletons, progress
    └── compositions/
        ├── skill-dashboard-design.md                 ← Dashboard layouts + KPIs
        ├── skill-data-visualization-design.md        ← Charts + data-ink rules
        ├── skill-financial-ux-design.md              ← Fintech/banking patterns
        └── skill-presentation-design.md              ← Slide decks + storytelling
```

---

## Quick Start Examples

### "Create a button component"
```
Load: palette → surface-modes → perception-ui-system → button-design
Output: Button with props { hue, mode, size, variant }
Variants: filled, outlined, ghost, text, icon-only
States: default, hover, pressed, focused, disabled
Preview: grid of (3 hues × 5 modes × 3 sizes)
```

### "Build a complete form"
```
Load: palette → surface-modes → perception-ui-system → text-fields-forms → button-design → selection-controls
Output: Form with text inputs, dropdowns, checkboxes, submit button
Each sub-component respects { hue, mode, size }
Preview: form rendered in M1 (light) and M2 (dark)
```

### "Create a financial dashboard"
```
Load: palette → surface-modes → perception-ui-system → ui-design-rules → financial-ux → dashboard-design → data-viz → navigation → data-tables → button-design
Output: Full dashboard with nav, KPI cards, charts, data table
Layout follows 58-rule checklist + financial UX patterns
All components use consistent hue + mode
```