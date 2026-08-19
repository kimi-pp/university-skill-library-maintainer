---
name: secure-code-review
description: Comprehensive, adversarial secure code review (18 phases) covering OWASP Top 10, business-logic abuse, race conditions, supply-chain/CI-CD integrity, AI/LLM & agentic code risk, webhook/callback security, multi-tenant isolation, and mobile/client-side hardening — gaps traditional SAST/SCA tools rarely catch. Reviews the current git diff by default, or a path/PR/full repo. Produces findings with file:line evidence, abuse scenarios, and documented (not executed) PoC repro steps for the reviewer's own authorized manual testing. Static/manual analysis only — never sends requests to a live or production system.
---

# Secure Code Review

License: MIT — see `LICENSE` at this skill's repo root ([github.com/jassics/secure-code-review](https://github.com/jassics/secure-code-review)).

Perform a vulnerability-focused, adversarial **static code review** of `$ARGUMENTS` (default: the uncommitted/branch diff; may also be a path, PR, full repo, or a phase command below).

**Safety & scope — read first**
- This skill is a **read-only, static/manual review**. It reads and reasons about source code; it never issues HTTP requests, runs exploits, brute-forces credentials, or otherwise touches a running/live system.
- Every "PoC" this skill produces is a **documented reproduction recipe** (Burp Suite steps, a Postman request) for the *user* to run themselves, in an environment and scope they are authorized to test. Do not automate execution of these PoCs against any target — including staging — without the user explicitly running them.
- If asked to review code for an application you don't have explicit authorization to test, still review the code (that's just reading), but decline to execute anything against it.

## Phase commands

If `$ARGUMENTS` starts with one of these, run only that phase against the scoped code instead of the full flow:

| Command | Scope |
|---|---|
| `auth` | Authn/session (1) + authz/IDOR (2) |
| `bizlogic` | Business-logic abuse (3) — see `reference/business-logic.md` |
| `injection` | Injection + input validation (4) |
| `headers` | Security headers & transport (5) |
| `pii` | Sensitive data / PII handling (6) |
| `logging` | Logging, monitoring, auditability (7) |
| `crypto` | Cryptography incl. PQ-readiness (8) — see `reference/crypto-and-pqc.md` |
| `deps` | Dependency/supply-chain audit (9) |
| `deadcode` | Orphan endpoints, debug routes, stale API versions (10) |
| `infra` | Infra/config review (11) |
| `arch` | Secure-by-design architecture review (12) |
| `supplychain` | CI/CD & build-provenance integrity (13) — see `reference/supply-chain-cicd.md` |
| `ai` | AI/LLM & agentic code risk (14) — see `reference/ai-llm-agentic.md` |
| `webhooks` | Webhook/callback/integration security (15) — see `reference/webhooks-and-integrations.md` |
| `tenancy` | Multi-tenant data isolation (16) — see `reference/multi-tenancy-and-isolation.md` |
| `concurrency` | Distributed-systems consistency: locks, caches, idempotency (17) |
| `mobile` | Mobile/client-side hardening (18) — see `reference/mobile-client-side.md` |
| `all` | Full flow, all phases |
| `poc <FINDING-ID>` | Write out Burp + Postman repro steps for a prior finding (documentation only) |
| `fix <FINDING-ID>` | Generate the concrete code fix for a prior finding |
| `chain` | Identify findings that combine into a higher-severity exploit chain |
| `triage` | Re-rank existing findings by (business impact × exploitability) |

## Steps

1. **Scope the change.**
   ```bash
   git diff --stat 2>/dev/null && git diff 2>/dev/null   # default: working changes
   # or: git diff main...HEAD   for a branch/PR
   ```
   If given a path or "full repo", review that scope. Read surrounding code for context, not just diff hunks.

2. **Interactive intake — only for business-critical flows** (checkout, payment, KYC, order/refund, auth, admin actions, AI/agent tool-calling) or when the user hasn't given context yet. Ask once, in one batch, then proceed. Skip silently for small/non-critical diffs:
   - What does this flow do, and which user roles can reach it?
   - Primary threat actor: external attacker, malicious authenticated user, insider, or bot?
   - Any sensitive data types involved (PII/PCI/health/credentials)?
   - Blast radius if this is compromised?

3. **Delegate deep static analysis where a capable sub-agent/tool is available** (e.g. a code-analysis agent, SAST). This skill defines the checklist and reasoning; it doesn't require any specific agent — apply the checklist directly if none is available.

4. **Walk the checklist below.** For every function/endpoint touched, ask "how would I abuse this?" Full phase detail lives in `reference/`.

   - **Phase 1 — AuthN/session**: password hashing (bcrypt/scrypt/argon2), hardcoded/default creds, reset-token entropy/expiry, user-enumeration via error messages/timing, JWT `alg` confusion & claim validation (`aud`/`iss`/`exp`), session entropy/regeneration/fixation, cookie flags (`Secure`/`HttpOnly`/`SameSite`), MFA/SSO bypass (remember-device replay, OAuth `state`/`redirect_uri`, SAML signature wrapping).
   - **Phase 2 — AuthZ/access control**: ownership checks sourced from session not request body/URL, admin-path guessing, IDOR on sequential IDs, mass assignment (role escalation via profile update), HTTP-method-level authz, multi-tenant token leakage across tenants, service-to-service trust (forged internal headers, IP-only trust).
   - **Phase 3 — Business logic abuse (often the highest-value findings)**: step-skipping, client-side state tampering, replay of payment/OTP tokens, TOCTOU races (double-spend, duplicate coupon, negative inventory), price/quantity/discount re-validation, refund-without-purchase, quota/rate-limit bypass, self-approval workflows, scheduled-job endpoints reachable directly, server- vs client-supplied time. Full checklist + abuse-scenario template: `reference/business-logic.md`.
   - **Phase 4 — Injection & input validation**: SQL/NoSQL/LDAP/OGNL/command/template injection, path traversal & zip-slip, reflected/stored/DOM XSS, CSP strength, XXE, unsafe deserialization (`pickle`, `yaml.load`, Java native deserialization), GraphQL introspection/depth/batching.
   - **Phase 5 — Headers & transport**: HSTS, CSP, `X-Frame-Options`/`frame-ancestors`, `X-Content-Type-Options`, `Referrer-Policy`, CORS wildcard+credentials, TLS version/cipher strength, mobile cert pinning.
   - **Phase 6 — PII/sensitive data**: PII in logs/errors/stack traces, over-fetching API responses, PII in URLs/analytics events, prod data in lower envs, right-to-erasure completeness, third-party SDK data access.
   - **Phase 7 — Logging/monitoring/auditability**: security events logged with actor/IP/outcome, tamper-evident/append-only logs, structured logs for SIEM, alerting on brute-force/bulk-export/privilege-escalation attempts, immutable financial audit trail.
   - **Phase 8 — Cryptography**: MD5/SHA1 for integrity or passwords, weak PRNGs (`Math.random`, `rand()`) for tokens, hardcoded/unrotatable symmetric keys, unauthenticated encryption (CBC w/o HMAC vs GCM), RSA <2048, ECB mode. Crypto-agility and post-quantum migration posture: `reference/crypto-and-pqc.md`.
   - **Phase 9 — Dependencies**: run `pip-audit`/`npm audit`/`osv-scanner`/`trivy` (or this project's `sca-scan` skill), CVSS≥7 triage, transitive-dep pinning, lockfile presence, image-digest pinning, abandoned packages, license compliance.
   - **Phase 10 — Orphan/dead code**: unregistered-but-reachable debug endpoints (`/debug`, `/actuator`), commented-out auth-bypass code, disabled feature flags whose endpoints are still live, stale API versions less hardened than current.
   - **Phase 11 — Infra/config**: secrets in env vs vault, `.env` in git history, public buckets, DB ports open to internet, containers running as root/`--privileged`, k8s RBAC/PSP/NetworkPolicy, verbose error pages.
   - **Phase 12 — Secure-by-design** (principles per *Secure by Design*, Bergh Johnsson/Deogun/Sawano, Manning, and the CISA Secure by Design Pledge — both in the reference library's `security architecture/`): least privilege, defense-in-depth (not just at the gateway), fail-secure on auth-service outage, separation of duties, trust boundaries between services, blast-radius containment, build-time package provenance, formally risk-accepted known debt. Verification depth should map to OWASP ASVS 5.0 L1/L2/L3, not a flat checklist.
   - **Phase 13 — Supply chain & CI/CD** *(gap: SCA finds known-CVE packages, not pipeline/build integrity)*: unpinned/mutable CI actions & base images, missing build provenance/SLSA attestation, dependency-confusion & typosquat exposure on internal package names, unsigned commits/tags on release branches, secrets exposed to PR-triggered CI from forks, artifact registries writable by too many principals. Detail: `reference/supply-chain-cicd.md`.
   - **Phase 14 — AI/LLM & agentic code** *(gap: no SAST/SCA rule set covers this)*: prompt injection via untrusted content reaching a system/tool prompt, unchecked LLM output flowing into `eval`/SQL/shell/HTML (insecure output handling), agent tool-calls with no per-tool authz or human-in-the-loop on destructive actions, RAG/vector-store data poisoning and cross-tenant retrieval leakage, unbounded agent loops/resource exhaustion, secrets/PII flowing into third-party model-provider logs, MCP server trust boundaries. Detail: `reference/ai-llm-agentic.md`.
   - **Phase 15 — Webhooks & third-party integrations** *(gap: rarely modeled by generic checklists)*: inbound webhook signature verification (HMAC, timing-safe compare), replay-window/nonce enforcement, outbound webhook SSRF (attacker-supplied callback URL reaching internal IPs/cloud metadata `169.254.169.254`), retry-storm/idempotency on webhook delivery. Detail: `reference/webhooks-and-integrations.md`.
   - **Phase 16 — Multi-tenant isolation** *(gap: authz checklists cover single-object IDOR, not systemic tenant bleed)*: row-level-security enforcement vs app-layer-only filtering, shared-cache keys not namespaced by tenant, background-job/queue payloads missing tenant context, tenant-scoped encryption keys vs one key for all. Detail: `reference/multi-tenancy-and-isolation.md`.
   - **Phase 17 — Concurrency & distributed consistency** *(gap: static SAST rarely reasons about timing)*: distributed-lock bypass (lock not covering the full critical section), cache-stampede/poisoning, non-idempotent retried operations (double-charge on network retry without an idempotency key), eventual-consistency windows exploited for double-spend across services.
   - **Phase 18 — Mobile/client-side hardening** *(gap: SAST covers server code; client trust and native mobile risk is usually skipped entirely)*: WebView JavaScript-bridge exposure (native functions reachable from untrusted web content), deep-link/intent hijacking and unvalidated deep-link parameters driving privileged actions, insecure local storage of tokens/PII (unencrypted SharedPreferences/UserDefaults/SQLite), client-side-only validation trusted by the server, hardcoded API keys/secrets in a shipped mobile binary, missing certificate pinning enabling MITM on hostile networks. Detail: `reference/mobile-client-side.md`.

5. **Cross-check with tooling where available**: dependency/SBOM scanners for Phase 9/13, secret scanners for Phase 1/11, a SAST engine for Phase 4. This skill's value is the phases those tools don't reason about (3, 13–17) plus human-style chaining across findings.

## Output

- Findings ordered by **severity** (Critical/High/Medium/Low), each with `file:line`, the vulnerable snippet, the exploit/abuse scenario, and a concrete secure fix. Use the finding template in `reference/finding-template.md`.
- For business-logic findings, use the abuse-scenario format in `reference/business-logic.md` (actor, goal, steps, business impact).
- Score meaningful findings with CVSS if a scoring tool/skill is available; otherwise state severity with a one-line justification.
- On `poc <ID>`, write documented Burp Suite (intercept/modify/forward) and Postman (method/URL/headers/body/expected-response) repro steps — the user runs these themselves; do not execute them.
- Distinguish confirmed issues from things to verify — if unsure, say "likely vulnerable — please confirm: does X happen?" rather than filing it as confirmed.
- Close a full review with: an executive summary table (severity × count), a quick-win vs. long-term-fix table (Finding ID | Effort | Priority | Owner), and a go/no-go merge recommendation.
- Only apply code fixes if the user explicitly asks for it — default to reporting findings, not patching.
