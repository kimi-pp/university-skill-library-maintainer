---
name: stripe-master
description: Manages payment processing, subscription lifecycles, checkout flows, and financial operations via Stripe. Use when user says "payment", "subscription", "checkout", "billing", "invoice", "Stripe", "pricing plan", "payment link", "refund", or needs any financial/payment infrastructure.
compatibility: Requires Stripe API keys and Stripe CLI. Uses Stripe MCP for API operations. Integrates with Clerk for customer identity and Supabase for financial audit trails.
metadata:
  author: Apex AI Fleet
  version: 2.0.0
  mcp-server: stripe
  category: payments
  tags: [stripe, payments, subscriptions, billing, checkout, financial, SaaS]
---

# Stripe Master: Financial Engineering

The financial engine. Orchestrates payments, subscriptions, and billing across all business tiers with audit trail compliance.

## Instructions

### Step 1: Identify the Financial Model

Before any Stripe implementation:

1. **What type?** (One-time payment, subscription, usage-based, marketplace)
2. **What plans?** (Free, Pro, Enterprise — define pricing tiers)
3. **What currency?** (USD default, multi-currency if international)
4. **Tax requirements?** (Stripe Tax for automatic calculation)

### Step 2: Product and Price Setup

Create products and prices in Stripe:

1. Define products with clear names and descriptions
2. Create prices for each billing interval (monthly, annual)
3. Use metadata to link Stripe products to internal plan IDs
4. Sync products to Supabase for local reference

Key rules:
- Never hardcode price IDs in application code — use environment variables
- Store only Stripe customer/subscription IDs locally (zero PII)
- Log all financial events to the audit trail

### Step 3: Checkout Integration

For subscription signups:

1. Create a Stripe Checkout session via API route
2. Configure success and cancel URLs
3. Include customer email from Clerk identity
4. Enable automatic tax calculation if applicable
5. Handle the `checkout.session.completed` webhook

For payment links:
1. Create via Stripe Dashboard or API
2. Embed in the appropriate page/email
3. Track conversions through metadata

### Step 4: Webhook Guardian Pattern

Every Stripe integration MUST handle webhooks:

1. Set up webhook endpoint at `/api/webhooks/stripe`
2. Verify webhook signature with Stripe secret
3. Handle critical events:
   - `checkout.session.completed` -> activate subscription
   - `invoice.paid` -> update billing status
   - `invoice.payment_failed` -> notify user, retry logic
   - `customer.subscription.deleted` -> deactivate access
4. Log every event to Supabase audit table
5. Return 200 immediately, process asynchronously if complex

### Step 5: Subscription Management

For upgrades/downgrades:

1. Retrieve current subscription via Stripe API
2. Update subscription items with new price ID
3. Handle proration (immediate or next billing cycle)
4. Sync new plan status to Clerk roles and Supabase

## Examples

### Example 1: SaaS Subscription Setup

User says: "Set up Pro and Enterprise subscription plans"

Actions:
1. Create "Pro" and "Enterprise" products in Stripe
2. Define monthly and annual prices for each
3. Create checkout API route with plan selection
4. Implement webhook handler for subscription lifecycle
5. Sync subscription status to Clerk roles for access control
Result: Full subscription system with automated access management

### Example 2: Process Refund

User says: "Refund the last payment for customer X"

Actions:
1. Look up customer by Clerk ID -> Stripe customer ID
2. Find the latest charge/payment intent
3. Create refund via Stripe API (full or partial)
4. Log refund to audit trail
5. Notify customer via email
Result: Refund processed with full audit trail

## Troubleshooting

### Webhook Signature Verification Fails
- Ensure you're using the raw request body, not parsed JSON
- Verify the webhook signing secret matches your environment
- Check that the endpoint URL matches what's configured in Stripe Dashboard

### Subscription Not Activating
- Verify `checkout.session.completed` webhook is firing (check Stripe Dashboard > Webhooks)
- Ensure the webhook handler updates both Supabase and Clerk
- Check for errors in the webhook handler logs

### Payment Failures
- Check Stripe Dashboard for specific decline codes
- Implement retry logic in the `invoice.payment_failed` handler
- Send clear communication to the customer about next steps
