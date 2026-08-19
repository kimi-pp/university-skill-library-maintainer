---
name: saas-starter
description: Use this skill when the user is starting a new SaaS web app and wants a battle-tested, opinionated stack with the foundational decisions already made — auth, database, billing, transactional email, deploys, AI integration. Captures Next.js App Router + Supabase + Tailwind v4 + Stripe + Resend + Vercel as the core, with optional Gemini / Claude / AI SDK on top. Includes a concrete quickstart checklist, sample RLS migration, Stripe webhook skeleton, and a CLAUDE.md template so a Claude Code agent can work alongside the developer at full velocity from day one. Triggers on "new SaaS starter", "SaaS stack", "Next.js + Supabase starter", "what stack should I use", "ship a SaaS fast", "Tailwind v4 + Supabase", "Stripe subscriptions starter", "Claude Code project setup", "scaffold a SaaS", "modern SaaS boilerplate".
---

# SaaS starter

A battle-tested, opinionated stack for shipping any new SaaS web app in days. Every layer below is here because removing it would force you to either pick a worse alternative or pay an engineer to maintain a custom one.

**Core thesis**: the stack you pick is the team you don't have. Choose layers that compose, set up the boring foundations correctly once, then spend your real attention on the product.

## When to use this skill

- You're starting a new SaaS web app and want the foundational stack decisions already made.
- You want a stack that gets you from `git init` to deployed-and-billing in days, not weeks.
- You want Claude Code (or any coding agent) to be productive on the codebase from day one via a dense CLAUDE.md.
- You're building anything with auth + paid tiers + transactional email — almost every modern SaaS.

## When NOT to use this skill

- **Enterprise B2B with SSO / SOC 2 from day one.** Swap Supabase Auth for WorkOS or Clerk; the rest still applies.
- **Pure marketing / content site.** No auth, no payments — Astro or a static-site generator is lighter.
- **Pure native mobile app.** Build native first, treat the web as the marketing site.
- **You're not committed to TypeScript.** This stack assumes strict TS. If you're shipping in JS, most decisions still apply but the type-safety promises don't.

## The stack

### Framework
- **Next.js (App Router)**. Server components, streaming, edge previews, route handlers, middleware, cookies. The default for modern full-stack web.
- **TypeScript strict** from t=0 (`strict: true`, `noUncheckedIndexedAccess: true`, `noImplicitOverride: true`). Don't relax later — backfilling types is weeks.

### UI
- **Tailwind CSS v4**. Utility-first. Don't build a design-token system on top — trust the framework.
- **shadcn/ui** (Radix primitives + Tailwind) for accessible components you can copy + own. Don't add a heavyweight component lib.

### Data, auth, storage
- **Supabase**. Postgres + Auth + Storage + Edge Functions + optional pgvector in one platform. Replaces five vendors.
- **Row-Level Security (RLS)** as the integrity guarantee. Every table gets policies in the migration that creates it — not as an afterthought. A `select` from any tenant-scoped table should be physically incapable of returning another tenant's row.

### Billing
- **Stripe** subscriptions. Hosted customer portal so you don't build a billing UI. Webhook handler updates subscription state in Postgres on every event.

### Transactional email
- **Resend** + **React Email**. Templates that match your product. Locale-aware from t=0 even if you launch in one language.

### Deploys
- **Vercel**. Per-branch preview deploys, DNS, env management. Zero infra overhead.

### AI (optional, when product calls for it)
- **AI SDK** (`ai` + provider packages). Provider-agnostic, so you can switch between Gemini / Claude / GPT without rewriting calls.
- **Gemini Flash** as a sensible default — cheap, fast, multimodal, generous free tier.
- **pgvector** for in-app RAG (chat / search grounded on the user's own data). Keep retrieval RLS-scoped.

### Build harness
- **Claude Code** with a dense `CLAUDE.md` that names every module, primitive, env var, migration. Treat the agent as a peer engineer joining tomorrow.

## Load-bearing decisions

These translate across every product. Get them right at t=0 and you won't repay them later.

### 1. Strict TypeScript, no escape hatches
A `tsconfig.json` with `strict: true` + `noUncheckedIndexedAccess: true` + `noImplicitOverride: true` is the cheapest insurance you'll buy. Don't add `// @ts-ignore` to make a stack trace go away — fix the type.

### 2. RLS on every tenant-scoped table
Tenancy at the database boundary, not the application. A forgotten filter in app code is a data breach; a missing RLS policy is caught the moment another user logs in.

```sql
-- Pattern for any user-scoped table
create table notes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  content text not null,
  created_at timestamptz not null default now()
);

alter table notes enable row level security;

create policy "users read their own notes"
  on notes for select
  using (auth.uid() = user_id);

create policy "users write their own notes"
  on notes for insert
  with check (auth.uid() = user_id);
```

### 3. Stripe webhook → DB is the source of truth
Don't query Stripe at request time. Process webhooks, write the resulting state to Postgres, read from Postgres for every check. Idempotency keyed on `stripe_event.id`.

### 4. Locale routing even at single-language launch
Set up `/[locale]/...` routes from t=0 even if `en` is your only locale. Adding locales later is a string-tables exercise; retrofitting locale-aware URLs is a re-architect.

### 5. Auth helpers, not auth checks
Centralise auth + role checks behind helpers (`requireUser()`, `requirePlan('pro')`). Pages and route handlers call helpers; they don't inline conditionals. Future you will change auth rules in one place.

### 6. Database migrations are code
Every schema change is a migration file in the repo. No "I ran this in the dashboard." If it's not in `supabase/migrations/`, it doesn't exist.

### 7. Env vars typed and validated at boot
A `lib/env.ts` that validates `process.env` with Zod at startup. A missing or misnamed env var should fail the build, not surface as a runtime 500 in week three.

### 8. CLAUDE.md as peer-engineer onboarding
Write a dense CLAUDE.md that enumerates every module, env var, migration, and critical rule. Treat the agent like a new hire who has to ship by Friday. The skill returns as ~30% velocity over months.

## Anti-patterns

- **Loose TypeScript "until it's needed."** It's needed now.
- **Application-layer tenancy filters.** A forgotten `.eq("tenant_id", ...)` is a data breach. RLS catches it at the boundary.
- **Querying Stripe at request time.** Slow, brittle, rate-limited. Webhook → DB → read.
- **Stuffing config in 50 env vars.** Group them: `STRIPE_*`, `SUPABASE_*`. Validate them once at boot.
- **Skipping migrations.** Every schema change is a file. No "I ran it in the dashboard."
- **Hiding context from Claude Code.** Write a dense CLAUDE.md. The skill returns as velocity.

## Quickstart checklist

10 numbered steps from empty directory to deployed-and-billing.

### 1. Bootstrap the Next.js app

```bash
npx create-next-app@latest my-saas --typescript --tailwind --app --turbopack
cd my-saas
```

Pin strict TS in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "moduleResolution": "bundler"
  }
}
```

### 2. Add core deps

```bash
npm install @supabase/ssr @supabase/supabase-js
npm install stripe @stripe/stripe-js
npm install resend react-email @react-email/components
npm install zod
npm install -D @types/node
```

### 3. Spin up Supabase

Sign up at supabase.com → create project → enable Auth providers you want (email, Google, GitHub).

Enable extensions you'll likely need:
```sql
create extension if not exists "pgcrypto";
create extension if not exists "vector"; -- only if you'll do RAG
```

### 4. Wire Supabase into the App Router

`lib/supabase/server.ts`, `lib/supabase/client.ts`, `lib/supabase/middleware.ts` — three clients (server component, client component, middleware-for-session-refresh). Pattern from supabase.com/docs/guides/auth/server-side/nextjs.

### 5. First migration — users + your first tenant table

`supabase/migrations/0001_init.sql` — extend `auth.users` with a `profiles` table for your app-specific fields, plus the RLS-pattern example above.

### 6. Stripe

Sign up at stripe.com → create products + prices (use Test mode). Add webhook endpoint `/api/stripe/webhook` in Stripe Dashboard. Copy webhook signing secret to `.env.local`.

Webhook handler skeleton:

```ts
// app/api/stripe/webhook/route.ts
import { headers } from "next/headers"
import Stripe from "stripe"

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function POST(req: Request) {
  const sig = (await headers()).get("stripe-signature")!
  const body = await req.text()
  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!,
    )
  } catch {
    return new Response("Bad signature", { status: 400 })
  }

  // Idempotency — skip if we've seen this event id.
  // Persist event → subscription state in Postgres.

  return new Response(null, { status: 200 })
}
```

### 7. Resend + React Email

```ts
// lib/email/send.ts
import { Resend } from "resend"
const resend = new Resend(process.env.RESEND_API_KEY!)
export async function sendEmail(/* ... */) { /* ... */ }
```

`emails/Welcome.tsx` is your first React Email template.

### 8. `lib/env.ts` — typed + validated env

```ts
import { z } from "zod"

const schema = z.object({
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1),
  STRIPE_SECRET_KEY: z.string().min(1),
  STRIPE_WEBHOOK_SECRET: z.string().min(1),
  RESEND_API_KEY: z.string().min(1),
})

export const env = schema.parse(process.env)
```

Importing `env` at boot crashes the build if anything's missing — the failure mode you want.

### 9. CLAUDE.md

```markdown
# CLAUDE.md

## Project

<one-line description of the SaaS>

## Stack

- Next.js (App Router) + TypeScript strict
- Supabase (Postgres + Auth + Storage)
- Stripe subscriptions, webhook at /api/stripe/webhook
- Resend transactional email
- Vercel deploys

## Layout

- app/                  — App Router routes
- lib/supabase/         — server, client, middleware
- lib/email/            — Resend wrapper + templates
- supabase/migrations/  — schema as code
- emails/               — React Email templates

## Env vars

- NEXT_PUBLIC_SUPABASE_URL
- NEXT_PUBLIC_SUPABASE_ANON_KEY
- SUPABASE_SERVICE_ROLE_KEY
- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET
- RESEND_API_KEY

## Critical rules

- Every tenant-scoped table gets RLS in the same migration.
- Webhook → DB → read. Never query Stripe at request time.
- No schema changes outside supabase/migrations/.
- Strict TS — no @ts-ignore.
```

### 10. Vercel + ship

```bash
npx vercel
```

Add the same env vars in Vercel Dashboard. Push to GitHub → branch deploys live automatically. Ship something user-facing in week one. Don't pre-build admin tooling — add it when you have something to administer.

## Optional layers

Add when the product calls for them, not before.

- **AI SDK + Gemini / Claude** — when you have a real inference use case (chat, extraction, search ranking). Build a provider-agnostic abstraction so you can swap models.
- **pgvector + embeddings** — when you want RAG (chat grounded on the user's own data). Embedding model: `gemini-embedding-001` (768 dims) or OpenAI `text-embedding-3-small`. HNSW index, RLS-scoped retrieval.
- **Multi-currency Stripe** — when you have customers across currencies. Set up at t=0 if you know you will; deferring isn't expensive either.
- **Native mobile (PWA → iOS/Android)** — when conversion data justifies the maintenance cost.
- **Internationalisation (next-intl)** — locale-routed paths from t=0 even at single-language launch.

## Migration paths

The stack is opinionated, not religious. Diverge where your product shape demands it.

- **Enterprise B2B with SSO / SOC 2.** Swap Supabase Auth for WorkOS or Clerk; keep Postgres, Stripe, Vercel, the rest.
- **Self-host.** Postgres + PocketBase / Supabase self-hosted. Keep RLS as the integrity guarantee.
- **No subscriptions, just one-time payments.** Stripe still works — swap subscription objects for `payment_intents`.
- **No AI at all.** Drop the AI SDK / pgvector — the rest of the stack still ships a great SaaS.

## What this skill is NOT

- A drop-in code repo (yet — see "GitHub repo" below).
- A framework. It's a stack + decisions + a quickstart checklist.
- A guarantee against bad product decisions. Nothing replaces talking to users.

## GitHub repo

A reference implementation lives at [github.com/darrenhead/saas-starter](https://github.com/darrenhead/saas-starter) (push pending — when it lands you can `git clone` and skip steps 1-2 of the quickstart). Until then, the checklist above is enough to be productive from `npx create-next-app` forward.
