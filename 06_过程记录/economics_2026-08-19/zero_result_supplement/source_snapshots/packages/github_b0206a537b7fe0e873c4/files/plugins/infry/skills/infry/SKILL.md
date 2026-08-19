---
name: infry
description: Use Cloudflare Registrar and DNS from Codex through the bundled Infry CLI. Use when a user wants to check domain availability, search domain ideas, register a domain, list registrations, inspect registration status, create Cloudflare zones, or manage DNS records from the command line.
---

# Infry

Infry is a Cloudflare domain-management helper for Codex. It assumes the user already has a Cloudflare account and uses Cloudflare's official API through the plugin's Cloudflare OAuth MCP connection.

Infry must use Cloudflare-backed checks for domain availability and DNS management. Do not fall back to WHOIS, RDAP, `dig`, or public DNS probes inside Infry commands; if Cloudflare auth is missing, run onboarding instead.

## Plugin Auth

Infry declares the official Cloudflare API MCP server in `.mcp.json`:

```text
https://mcp.cloudflare.com/mcp
```

When the plugin is installed or first used, the user should authenticate Cloudflare through the Codex plugin/MCP connection UI. Prefer this OAuth connection over environment variables.

Use the authenticated Cloudflare MCP tools for Cloudflare operations when they are available in the current thread. If those tools are not loaded yet, use `tool_search` for Cloudflare API MCP tools before falling back to the local CLI.

## Environment

The bundled CLI is a local fallback and development aid:

```bash
node /Users/tt/plugins/infry/scripts/infry.mjs <command>
```

CLI authentication:

- `CLOUDFLARE_API_TOKEN`
- Optional fallback: `wrangler login`, when `wrangler auth token --json` returns an OAuth/API token

Set `CLOUDFLARE_ACCOUNT_ID` only when the token cannot list exactly one account. Infry can discover the account via `/accounts` when the token has account-read access.

Recommended token permissions:

- Account: Cloudflare Registrar Edit or equivalent registrar permissions
- Account: Account Settings Read for account discovery
- Zone: Zone Read/Edit and DNS Read/Edit for zone and DNS commands

## Onboarding

Always start first-run flows with:

```bash
node /Users/tt/plugins/infry/scripts/infry.mjs doctor
```

If the Cloudflare MCP connection is unavailable or unauthenticated:

1. Ask the user to complete Cloudflare authentication from the Codex plugin/MCP connection UI.
2. If the connection UI is unavailable in the current session, use the local fallback flow below.

If the local CLI `doctor` reports no usable auth:

1. Prefer `wrangler login` over manually handling a token.
2. If Wrangler is installed but logged out, run:

```bash
node /Users/tt/plugins/infry/scripts/infry.mjs onboard --wrangler-login
```

3. If Wrangler is missing and the user accepts installation, install Wrangler and run the same onboarding command.
4. Use `CLOUDFLARE_API_TOKEN` only when OAuth/Wrangler onboarding is not practical.

When the browser login flow opens and the user wants help completing it, use Computer Use or Chrome browser assistance only for the login UI. Never read, print, or store token values.

If auth is still missing, stop at onboarding. Do not answer an Infry availability check from WHOIS/RDAP/DNS output, because that is not the Cloudflare purchase path.

## Safe Workflow

For domain purchases:

1. Run `check` immediately before `buy`.
2. Show the user the returned price, currency, tier, and reason if not registrable.
3. Only call `buy` when the user clearly wants to purchase.
4. Always pass `--confirm <domain>` exactly matching the domain.
5. Do not buy premium domains. The CLI also blocks premium results.

Cloudflare registration is billable and non-refundable after the workflow succeeds. If Cloudflare reports `extension_not_supported_via_api`, send the user to:

```text
https://dash.cloudflare.com/<account-id>/domains/registrations
```

## Common Commands

```bash
# Preferred: use the Cloudflare MCP OAuth connection exposed by the plugin.
# Search for Cloudflare MCP tools in the current thread when they are not visible.

# First-run diagnosis
node /Users/tt/plugins/infry/scripts/infry.mjs doctor

# Start Wrangler browser login when token auth is absent
node /Users/tt/plugins/infry/scripts/infry.mjs onboard --wrangler-login

# Verify token and account visibility
node /Users/tt/plugins/infry/scripts/infry.mjs accounts

# Use an existing Wrangler login if no CLOUDFLARE_API_TOKEN is set
wrangler login
node /Users/tt/plugins/infry/scripts/infry.mjs accounts

# Search candidate domains
node /Users/tt/plugins/infry/scripts/infry.mjs search infry --extensions com,app,dev,cloud

# Authoritative check, max 20 domains
node /Users/tt/plugins/infry/scripts/infry.mjs check infry.com infry.dev --json

# Buy, with a mandatory exact confirmation flag
node /Users/tt/plugins/infry/scripts/infry.mjs buy infry.dev --years 1 --confirm infry.dev

# List or inspect registrations
node /Users/tt/plugins/infry/scripts/infry.mjs registrations
node /Users/tt/plugins/infry/scripts/infry.mjs registration infry.dev
node /Users/tt/plugins/infry/scripts/infry.mjs registration-status infry.dev

# Cloudflare zones
node /Users/tt/plugins/infry/scripts/infry.mjs zones
node /Users/tt/plugins/infry/scripts/infry.mjs zone-create infry.dev

# DNS
node /Users/tt/plugins/infry/scripts/infry.mjs dns-list infry.dev
node /Users/tt/plugins/infry/scripts/infry.mjs dns-add infry.dev A @ 203.0.113.10 --proxied false
node /Users/tt/plugins/infry/scripts/infry.mjs dns-add infry.dev CNAME www infry.pages.dev --proxied true
```

## Notes

- `check` uses Cloudflare's real-time registry check and requires Cloudflare auth.
- `search` is useful for ideas but may be stale; run `check` before purchase.
- `buy` uses Cloudflare's default account address book when no `--contact-file` is provided.
- `--contact-file` accepts JSON shaped as Cloudflare's `contacts` object, for example `{ "registrant": { ... } }`.
- `dns-add` resolves a zone by domain name automatically. Use `--zone-id` when names are ambiguous.
