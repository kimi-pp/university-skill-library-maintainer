---
name: schema-design-flow
description: Use when designing database schema, tables, columns, associations, or migrations in Rails before writing code. Walks the user through a Socratic interrogation (who owns this? who sees it? what lifecycle? what's unique?) before generating any migration. Applies to any app domain — content (blog, posts, articles), commerce (products, orders, cart), collaboration (todos, tasks, boards), directory (listings, profiles), transactional (bookings, reservations), social (comments, reviews, likes), or anything else. Covers new models, schema changes, adding columns, multi-tenancy / permission boundaries, state modeling (timestamps vs booleans), associations (belongs_to / has_many / has_many :through), indexes, foreign keys, NOT NULL discipline, default values, and reversible migration safety. Platform-agnostic — SQLite, MySQL, PostgreSQL. Triggers when user mentions schema, migration, database design, add column, new table, data model, `bin/rails g model`, `bin/rails g migration`, belongs_to, has_many, foreign key, index, or "think about the data before I code". Inspired by 37signals Fizzy state-as-records patterns.
---

# Schema Design Flow — Think in Questions, Not Tables

> People plan apps in stories. Developers think in tables. This skill bridges both: Claude asks the story questions, the user answers, Claude drafts the tables. **Never generate migrations without running the interrogation first** — regardless of what kind of app it is (blog, store, booking, directory, CRM, social, internal tool).

## Philosophy

> Schema is the hardest thing to change later. 20 minutes of questions upfront saves 2 hours of migrations and broken deploys. Always interrogate before you migrate.

**The rule:** Before writing a single `bin/rails generate migration`, run the Socratic flow. Capture answers in words (or update the PRD). Only then draft the schema.

## The Socratic Interrogation — Universal Questions

Works for **any domain** — blog posts, e-commerce products, bookings, directory listings, social comments, internal CRM records. Ask all that apply, in one batch, in plain language:

### The Core 7 (every new table)

1. **Who creates this record?** (owner, any authenticated user, admin only, system-generated, public?)
2. **Who can see it?** (public, owner only, their team / account, paying customers, logged-in users?)
3. **Who can edit or delete it?** (owner, admin, moderators, nobody?)
4. **Does it belong to something bigger?** (a user, a team, an account, a parent record, a category?)
5. **What's the lifecycle?** (just "exists," or draft → published → archived, or open → closed, or pending → paid → fulfilled?)
6. **What makes it unique?** (name, slug, code, email, SKU, combination of columns?)
7. **What happens when the parent is deleted?** (cascade delete, orphan, prevent delete?)

### Context-specific (add when relevant)

8. **Multi-tenant app?** → Every user-owned table needs `account_id` / `workspace_id` / `tenant_id`.
9. **Soft vs hard delete?** → Trash / undo, or gone forever?
10. **Audit trail?** → Do we care who changed what and when?
11. **Counts for display?** → Will we show "50 posts" or "3 unread" fast? (counter_cache)
12. **Attachments?** → Files / images? (Active Storage — no `image_url` column)
13. **Other associations?** → What else does this record point to or own?
14. **Search / filtering?** → Will we filter by status, date range, category? (drives indexes)

**Rule:** Ask all applicable questions in one message. Then wait for answers. Don't write code in the middle of the interrogation.

## How the Interrogation Adapts by Domain

Same 7 core questions, different answers reveal different schema shapes.

| Domain | Typical "who creates" | Typical "lifecycle" | Typical "unique" |
|---|---|---|---|
| **Content** (blog, article, page) | Author / admin | `draft → published → archived` | slug |
| **Commerce** (product, variant) | Admin / seller | `active → out-of-stock → discontinued` | SKU, slug |
| **Order / transaction** | Buyer | `pending → paid → fulfilled → refunded` | order number |
| **Collaboration** (todo, task, ticket) | Team member | `open → doing → done` | (none — title repeats OK) |
| **Directory** (listing, profile) | Owner | `pending review → published → hidden` | slug |
| **Booking / reservation** | Customer | `requested → confirmed → cancelled → completed` | (date + resource combo) |
| **Social** (comment, review) | Any user | `visible → flagged → hidden` | (none) |
| **Messaging** (message, notification) | Sender / system | `sent → read → archived` | (none) |

Use this as a cheat sheet when asking: *"Is this more like a content record, a transaction, or a collaboration record?"* — the answer narrows question #5.

## Example Interrogations (Three Domains, Same Flow)

### Example A — Content (Blog Post)

User: *"Create a table for blog posts."*

Claude (good):
```
Before I generate the migration, 7 quick questions:

1. Who creates posts — just you as the author, or multiple authors?
2. Who can read them — public, or logged-in users only?
3. Who can edit / delete — author only, or admin / editor roles?
4. Does a post belong to a category / tag? A User (belongs_to)?
5. Lifecycle — publish immediately, or draft → published flow?
6. What's unique — slug derived from title, or is ID alone enough?
7. If the author is deleted, do their posts vanish or stay (nullify author)?

Plus 2 extras: do you need a hero image (Active Storage)? A counter of
comments per post for fast display?
```

### Example B — Commerce (Product + Order)

User: *"I want to sell digital products. I need product and order tables."*

Claude (good):
```
Two tables. Let me ask per table:

PRODUCT:
1. Who creates — just you as admin, or multi-seller marketplace?
2. Who can view — public browsing, or members only?
3. Who can edit — admin only?
4. Does a product have a category? Attached files (Active Storage)?
5. Lifecycle — active / out-of-stock / discontinued?
6. Unique — slug derived from name, or SKU?
7. If a product is deleted, do historical orders that used it also vanish?

ORDER:
1. Who creates — the buyer at checkout, correct?
2. Who can view — buyer + admin only?
3. Who can edit — admin only (for refunds), buyer can't?
4. Order belongs_to a buyer (User) and one or more products — correct?
5. Lifecycle — pending → paid → fulfilled → refunded?
6. Unique — human-readable order_number, or UUID?
7. If the buyer is deleted, orders stay for financial audit → nullify or restrict.
```

### Example C — Booking (Reservation)

User: *"An app for booking photo studio slots by the hour."*

Claude (good):
```
Booking domain = conflict prevention matters. Questions:

1. Who creates a booking — customer via public form, or admin only?
2. Who can view — customer who booked + admin?
3. Who can cancel — customer up to 24h before, admin any time?
4. Booking belongs_to a customer + a studio? Does studio have an owner?
5. Lifecycle — requested → confirmed → completed → cancelled?
6. Unique — combination (studio_id, start_at, end_at) must not overlap?
   → this is a custom validation + index, not a standard DB unique constraint
7. If a studio is closed (deleted), what happens to past bookings?

Plus: do you need a buffer time between bookings? Pricing per hour on
the product, or per booking?
```

**Notice:** Same 7 questions. Different answers → different schema shapes. Same flow works whether the app is a blog, a store, a CRM, a booking tool, or an internal dashboard.

## The Schema Summary Template

After interrogation, draft the schema in **plain language** (not code yet). This is the user's last checkpoint before code:

```
Table: <plural_name>
- id (primary key)
- <parent>_id (references <parents>, NOT NULL / nullable)  ← "belongs to" from Q4
- <creator>_id (references users, NOT NULL)                 ← "who creates" from Q1
- <tenant>_id (references accounts, NOT NULL)               ← multi-tenancy Q8
- <business columns based on the domain>
- <status> (string, NOT NULL, default: "<initial>")         ← lifecycle from Q5
- <state>_at (datetime, nullable)                            ← timestamp states
- timestamps (created_at, updated_at)

Indexes:
- <tenant>_id                     ← every query scopes by tenant
- [<tenant>_id, <status>]         ← list by status fast
- <unique business key>           ← unique: true

Associations:
- belongs_to :<parent>
- belongs_to :<creator>, class_name: "User"
- has_many :<children>, dependent: :<destroy|nullify|restrict>

Cascade:
- <parent>.destroy → <this> <cascade decision from Q7>
```

Fill in the blanks for the domain. Then ask: *"Does this schema look right? If yes, I'll generate the migration. If anything should change, now's the time."*

## Worked Draft — Blog Post (Content Domain)

```
Table: posts
- id
- author_id (references users, NOT NULL)
- account_id (references accounts, NOT NULL)     ← multi-tenant blog platform
- title (string, NOT NULL, max 255)
- slug (string, NOT NULL, max 255)
- body (text, NOT NULL)
- published_at (datetime, nullable)               ← timestamp = lifecycle, no `published` bool
- comments_count (integer, NOT NULL, default 0)   ← counter_cache
- timestamps

Indexes:
- account_id
- [account_id, published_at]                      ← "published posts for this account"
- [account_id, slug] unique                       ← slug unique per account, not globally

Associations:
- belongs_to :author, class_name: "User"
- belongs_to :account
- has_many :comments, dependent: :destroy
- has_one_attached :hero_image                    ← Active Storage, no image column

Cascade:
- author.destroy → restrict (keep posts even if author gone, nullify author instead)
- account.destroy → destroy (whole workspace removal takes posts)
```

## Worked Draft — Order (Commerce Domain)

```
Table: orders
- id
- buyer_id (references users, NOT NULL)
- account_id (references accounts, NOT NULL)      ← multi-seller platform
- number (string, NOT NULL, max 20)                ← human-readable order number
- amount_cents (integer, NOT NULL)                 ← never float for money
- currency (string, NOT NULL, default "IDR", max 3)
- status (string, NOT NULL, default "pending")     ← pending|paid|fulfilled|refunded
- paid_at (datetime, nullable)
- fulfilled_at (datetime, nullable)
- refunded_at (datetime, nullable)
- timestamps

Indexes:
- account_id
- [account_id, status]
- [account_id, number] unique
- buyer_id

Associations:
- belongs_to :buyer, class_name: "User"
- belongs_to :account
- has_many :line_items, dependent: :destroy
- has_many :products, through: :line_items

Cascade:
- buyer.destroy → nullify buyer_id (keep order for financial audit)
- account.destroy → restrict (refuse to delete account with orders — force refund first)
```

## Worked Draft — Booking (Transactional Domain)

```
Table: bookings
- id
- customer_id (references users, NOT NULL)
- resource_id (references resources, NOT NULL)    ← studio, room, equipment, etc.
- start_at (datetime, NOT NULL)
- end_at (datetime, NOT NULL)
- status (string, NOT NULL, default "requested")  ← requested|confirmed|cancelled|completed
- confirmed_at, cancelled_at, completed_at (datetime, nullable)
- timestamps

Indexes:
- resource_id
- [resource_id, start_at, end_at]                 ← conflict detection queries
- customer_id

Associations:
- belongs_to :customer, class_name: "User"
- belongs_to :resource

Validations (not schema, but flag during interrogation):
- no overlapping bookings for same resource_id where status in [requested, confirmed]

Cascade:
- resource.destroy → restrict (refuse — redirect admin to cancel bookings first)
- customer.destroy → nullify (keep booking history for the resource owner)
```

## Migration Pattern — Reversible Skeleton

Every new table follows this shape regardless of domain:

```ruby
class Create<Records> < ActiveRecord::Migration[8.1]
  def change
    create_table :<records> do |t|
      # Required parents (NOT NULL + foreign key)
      t.references :<parent>, null: false, foreign_key: true

      # Required user relationships (aliased FK when name differs from model)
      t.references :<creator>, null: false, foreign_key: { to_table: :users }

      # Optional user relationships
      t.references :<other_user>, null: true, foreign_key: { to_table: :users }

      # Business columns
      t.string   :<name>,   null: false, limit: 255
      t.text     :<body>
      t.string   :<status>, null: false, default: "<initial>"
      t.integer  :<count>,  null: false, default: 0
      t.datetime :<event>_at                       # nullable timestamps for state
      t.decimal  :<money>,  precision: 10, scale: 2  # never :float for money

      t.timestamps
    end

    # Indexes matching real query shapes
    add_index :<records>, [:<tenant>_id, :<status>]
    add_index :<records>, :<unique_slug>, unique: true
  end
end
```

**Why these choices (apply to any domain):**
- `null: false` on everything required. Defaults at DB level, not app level.
- `limit: 255` on strings — explicit, works identically on SQLite / MySQL / Postgres.
- `status` as `string`, not `boolean` or integer enum. Readable in DB, swappable.
- State-carrying `*_at` columns over boolean flags.
- Composite indexes match the real query shapes (status lists, tenant scoping).
- `foreign_key: true` adds DB-level integrity (survives app bugs and raw SQL).

## Column Naming — The Golden Rules

### Timestamps over booleans (works for any domain)

| Boolean (avoid) | Timestamp (prefer) | What it captures |
|---|---|---|
| `published` | `published_at` | state + when it happened |
| `completed` | `completed_at` | state + when |
| `verified` | `verified_at` | state + when |
| `archived` | `archived_at` | state + when |
| `read` | `read_at` | state + when |
| `paid` | `paid_at` | state + when |
| `confirmed` | `confirmed_at` | state + when |
| `approved` | `approved_at` | state + when |

Query is just `where.not(<action>_at: nil)` — same ergonomics, more information.

### `*_at` suffix for moments in time

`created_at`, `published_at`, `last_signed_in_at`, `paid_at`. Always `datetime`, never `date` — unless it's truly a date with no time component (birthdays, due dates, events spanning a full day).

### Reserved names to avoid

- `type` — collides with Rails STI
- `class` — Ruby reserved
- `id` — already the primary key
- `user` / `post` / `order` — use `user_id`, `post_id`, `order_id` instead

### Count columns

`comments_count`, `line_items_count`, `bookings_count` — integer, default 0, NOT NULL. Managed via `counter_cache: true` on `belongs_to` or manually via `.increment!`.

### Money columns

`amount_cents` as integer (cents) + separate `currency` string. Never `:float`. If you prefer decimal: `decimal, precision: 12, scale: 2`.

## State Modeling — The Fizzy "State as Records" Pattern

37signals Fizzy teaches this: **separate records beat boolean flags** when state has history, metadata, or optional context. Applies across domains.

### When state as a column is enough

- Binary, no metadata, no undo → single timestamp: `completed_at`, `archived_at`
- Always-present workflow step → enum column: `status`

### When state deserves its own record

- State has **who / when / why / how** metadata
- State can be **undone** (deleting the state record reverts it)
- State is **rare** relative to the parent (don't bloat the main table)

### Cross-domain examples of state-as-records

| Parent | Flag you might add (avoid) | State record (prefer) |
|---|---|---|
| Post | `flagged boolean` | `Flag` record (flagged_by, reason, at) |
| Order | `refunded boolean` | `Refund` record (amount, reason, issued_by) |
| Comment | `hidden boolean` | `Moderation` record (hidden_by, reason, at) |
| Booking | `cancelled boolean` | `Cancellation` record (cancelled_by, reason, at) |
| User | `banned boolean` | `Ban` record (banned_by, expires_at, reason) |
| Task | `blocked boolean` | `Blocker` record (blocked_by_task_id, note) |

**Rule of thumb:** if you find yourself about to add `<state>_by`, `<state>_reason`, or `<state>_note` alongside a `<state>` boolean → reach for a state record instead.

## Associations — Domain-Agnostic Patterns

### belongs_to defaults

```ruby
belongs_to :<parent>                                              # required (Rails 5+ default)
belongs_to :<parent>, optional: true                              # explicit when nullable
belongs_to :<named>, class_name: "<Model>"                        # when column name differs
belongs_to :<named>, class_name: "<Model>", foreign_key: "<col>"  # when both differ
```

### has_many + dependent (cascade decision from interrogation Q7)

```ruby
has_many :<children>, dependent: :destroy                # cascade, run callbacks
has_many :<children>, dependent: :delete_all             # cascade, faster, no callbacks
has_many :<children>, dependent: :nullify                # orphan but keep
has_many :<children>, dependent: :restrict_with_error    # refuse delete if children exist
```

| Option | When |
|---|---|
| `:destroy` | Most common. Runs child callbacks (e.g., Active Storage purge). |
| `:delete_all` | Bulk cascade. No callbacks worth running. |
| `:restrict_with_error` | Parent is a system-of-record; children must be cleaned first. |
| `:nullify` | Child can exist meaningfully without parent (orphaned orders after user delete). |

### has_many :through for many-to-many

Always prefer over `has_and_belongs_to_many` — the join model can grow (roles, permissions, `invited_at`, `last_seen_at`).

```ruby
class <Parent_A> < ApplicationRecord
  has_many :<joins>
  has_many :<parent_bs>, through: :<joins>
end

class <Parent_B> < ApplicationRecord
  has_many :<joins>
  has_many :<parent_as>, through: :<joins>
end

class <Join> < ApplicationRecord
  belongs_to :<parent_a>
  belongs_to :<parent_b>
  # Room for role, permissions, invited_at, etc.
end
```

## Indexes — Match Your Queries

### The three types you'll actually use

```ruby
add_index :<records>, :<parent>_id                         # single column, scope queries
add_index :<records>, [:<parent>_id, :<status>]            # composite, filtered lists
add_index :<records>, :<unique_key>, unique: true          # unique constraint at DB level
```

### Composite index rule

**Leading column must match your `WHERE`.** Index `[:account_id, :status]` supports:
- `WHERE account_id = ?` ✅
- `WHERE account_id = ? AND status = ?` ✅
- `WHERE status = ?` ❌ (index not used — leading column missing)

Order the composite by selectivity: tenant first, then status/date.

### When to add an index

- Every foreign key (`t.references` adds it automatically)
- Every column you `WHERE`, `ORDER BY`, or `JOIN` on
- Unique business keys (email, slug, code, SKU, order number)

**Don't** index every column "just in case" — indexes cost write speed + disk.

## Multi-Tenancy — Always Scope by Tenant

If the app has multiple customers / teams / workspaces, **every user-owned table gets the tenant FK**. The tenant column is called `account_id`, `workspace_id`, `organization_id`, `tenant_id` — pick one name per app and use it everywhere.

```ruby
create_table :<records> do |t|
  t.references :account, null: false, foreign_key: true  # tenant anchor
  # ... rest of the table
end

add_index :<records>, [:account_id, :<status>]            # leading column = tenant
add_index :<records>, [:account_id, :<slug>], unique: true # unique scoped to tenant
```

In models:
```ruby
class <Record> < ApplicationRecord
  belongs_to :account
  # Optional: infer account from parent to avoid passing it manually
  # belongs_to :account, default: -> { <parent>.account }
end
```

Enforce at the controller via `Current.account`:
```ruby
Current.account.<records>.where(status: "active")  # all queries tenant-scoped
```

## Platform-Agnostic Column Types

Stick to these for SQLite ↔ MySQL ↔ PostgreSQL portability:

| Use | Type | Notes |
|---|---|---|
| Short text | `:string` | Default 255 in MySQL; explicit `limit: 255` is safest |
| Long text | `:text` | Unlimited on all three |
| Integer | `:integer` | 4-byte |
| Big integer | `:bigint` | 8-byte, for external IDs / large counts |
| Decimal money | `:decimal, precision: 10, scale: 2` | Never `:float` for money |
| Money (cents pattern) | `:integer` | `amount_cents` — portable + arithmetic-safe |
| Date only | `:date` | Birthdays, due dates, all-day events |
| Date + time | `:datetime` | `*_at` columns, bookings, events |
| Boolean | `:boolean, default: false, null: false` | Rare — prefer timestamps |
| Structured data | `:json` | All three support it (indexing is Postgres-only) |
| UUID token | `:string, limit: 36` | Generate via `SecureRandom.uuid`; portable |

**Avoid for portability:**
- `:jsonb` (Postgres-only — use `:json` if you need flexible data)
- `:citext` (Postgres-only — use `:string` + normalize via `.downcase` before save)
- `:inet`, `:array`, `:hstore` (Postgres-only)
- `t.uuid` native type (Postgres-only; use string UUID for portability)
- `algorithm: :concurrently` on indexes (Postgres-only)
- Partial indexes `where: "..."` (Postgres + SQLite only — MySQL ignores)

When Postgres-specific features are worth it, **commit to Postgres for the project** and document the decision. Don't mix portability claims with Postgres-only columns.

## Common Migration Operations

### Add a column

```ruby
class Add<Column>To<Records> < ActiveRecord::Migration[8.1]
  def change
    add_column :<records>, :<column>, :<type>
    add_index  :<records>, :<column>   # if it'll appear in WHERE/ORDER
  end
end
```

### Add a NOT NULL column to an existing table (safe 3-step)

Large tables need this pattern to avoid long locks:

```ruby
# Migration 1 — add as nullable
add_column :<records>, :<column>, :<type>

# Deploy + backfill in a rake task or Active Job
<Record>.in_batches.update_all(<column>: <default_value>)

# Migration 2 — enforce NOT NULL + default
change_column_null    :<records>, :<column>, false
change_column_default :<records>, :<column>, from: nil, to: <default_value>
```

Small tables (< 10K rows) — one migration is fine.

### Rename a column (two-deploy dance)

```ruby
# Deploy 1 — add new column, keep old, dual-write in app
add_column :<records>, :<new_name>, :<type>
# (backfill + update app to write to both)

# Deploy 2 — drop old
remove_column :<records>, :<old_name>, :<type>
```

Never rename in one shot on a production app — old web containers will 500 on the missing column during rollout.

### Drop a column

```ruby
class Remove<Column>From<Records> < ActiveRecord::Migration[8.1]
  def change
    remove_column :<records>, :<column>, :<type>, default: <original>, null: <original>
  end
end
```

Include the full original definition as the 3rd+ argument so `down` is reversible.

## NOT NULL Discipline

**Default to NOT NULL.** Every column should be NOT NULL unless nullability is a real business fact.

| Column | NOT NULL? | Reason |
|---|---|---|
| `title` on any content | Yes | No content without a title |
| `amount_cents` on order | Yes | Orders without totals are broken |
| `published_at` on post | No | `NULL` means draft |
| `completed_at` on task | No | `NULL` means open |
| `<parent>_id` (required) | Yes | Orphans are always a bug |
| `<parent>_id` (optional) | No | Only if "no parent" is meaningful |

**Rule:** if you'd say "the column *has* to have a value," add `null: false, default: X`.

## Anti-Patterns (Universal)

- ❌ Generating migrations before interrogation (defeats the skill's purpose)
- ❌ Boolean flags where a timestamp carries more info (`paid` vs `paid_at`)
- ❌ Nullable columns without thinking (`null: true` by default is lazy)
- ❌ Missing foreign key constraints (app-only integrity breaks in raw SQL / console bugs)
- ❌ Missing indexes on FK + query columns (slow at 10K rows)
- ❌ Storing money as `:float` (rounding errors — use `:integer` cents or `:decimal`)
- ❌ Postgres-only features (`jsonb`, `citext`, `gen_random_uuid()`) in a "portable" schema
- ❌ STI `type` column when a polymorphic or separate table would be cleaner
- ❌ `has_and_belongs_to_many` — always use `has_many :through` so the join can grow
- ❌ Renaming columns in one deploy (causes 500s during rollout)
- ❌ Changing a migration that already ran in production (create a new migration instead)
- ❌ `deleted_at` soft delete without thought — it's additive complexity; cascade-destroy is usually simpler

## How to Use This Skill

1. **User asks for a new model / table / schema change** (any domain).
2. **Run the interrogation** — core 7 + applicable context questions. One batch.
3. **Wait for answers.** Don't write code.
4. **Draft the schema summary in plain language** (template above, filled in for their domain).
5. **Confirm with the user.** "Does this schema look right?"
6. **Generate the migration.** Open the file, tighten defaults / nulls / indexes.
7. **Run `bin/rails db:migrate`.**
8. **Sanity-check reversibility:** `bin/rails db:rollback && bin/rails db:migrate`. Both succeed → schema is reversible.
9. **Commit.** Migrations are forever — git history proves intent.

## Related Skills

- **prd-writing** — PRD informs "who owns / who sees / what lifecycle" (feeds the interrogation)
- **rails-conventions** — models, validations, associations (the code after the schema)
- **auth-setup** — permission boundaries shape tenant / ownership schema decisions
- **active-storage** — file columns (don't add `image_url` strings — use `has_one_attached`)
- **rails-debug-helper** — diagnosing migration / schema drift issues
