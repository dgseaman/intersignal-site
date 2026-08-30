# Stripe setup for Braid Founding Membership

This site bundle is ready for a Stripe-hosted annual subscription checkout. It intentionally contains no Stripe secret key, webhook secret, relay token, or private Braid key.

## 1. Create the product

In Stripe Dashboard, create:

- Product name: `Braid Founding Membership`
- Price: `$99 USD`
- Billing period: `Yearly / recurring`
- Description: `Braid Managed Relay access, guided onboarding, native 1.6 updates as released, and best-effort setup support. Experimental service; no production SLA. Core Braid LAN software remains free.`

Before launch, set your public business details, support email, privacy policy, subscription/cancellation language, and refund policy. This bundle does not choose a refund policy for Intersignal.

## 2. Create a Payment Link

Create a Payment Link for the recurring price. Recommended settings:

- Collect customer email.
- Enable automatic receipts.
- Add the annual-renewal and cancellation terms in Stripe's custom text.
- Redirect after checkout to:

  `https://intersignal.org/founding/thanks.html`

Stripe also supports a `{CHECKOUT_SESSION_ID}` placeholder in redirect URLs. Do not use a session ID in browser JavaScript as an authorization decision; verify payment server-side or in the Stripe Dashboard.

## 3. Public Payment Link (already inserted)

The live annual-subscription Payment Link is already present in `site-config.js`:

```js
window.INTERSIGNAL_SITE_CONFIG = Object.freeze({
  foundingPaymentLink: "https://buy.stripe.com/14A3cvb2ncYj2vyaZ88so00",
  customerPortalUrl: "",
  supportEmail: "hello@intersignal.ai"
});
```

Only public Stripe-hosted URLs belong here. Never put `sk_live_...`, `rk_live_...`, or `whsec_...` values in HTML or JavaScript.

## 4. Enable the Stripe customer portal

Use Stripe's no-code customer portal so subscribers can manage payment methods, invoices, and cancellations. Paste the portal URL into `customerPortalUrl` in `site-config.js`. The Manage billing button remains hidden until a valid Stripe portal URL is present.

## 5. Initial fulfillment: manual and controlled

For the first founding cohort:

1. Verify the active annual subscription in Stripe Dashboard.
2. Record the customer's email and access status in an internal ledger.
3. Provision Managed Relay enrollment separately.
4. Send onboarding instructions and a user-defined semantic-transfer starter guide.
5. Never send relay enrollment tokens through a public page or embed them in the site.
6. Revoke or expire managed access when a subscription is canceled or unpaid.

The Payment Link is a purchase gate, not a secure access-control system by itself.

## 6. Later automation

When manual provisioning becomes burdensome, add a server-side webhook handler. At minimum, handle and verify relevant Stripe events such as:

- `checkout.session.completed`
- `invoice.paid`
- `invoice.payment_failed`
- `customer.subscription.updated`
- `customer.subscription.deleted`

Make fulfillment idempotent, verify Stripe webhook signatures, and store secrets only in the server environment. Do not automate privileged Braid actions directly from untrusted customer-supplied text.

## 7. Test before live launch

- Use Stripe test mode first.
- Complete a test subscription checkout.
- Confirm the redirect reaches `/founding/thanks.html`.
- Confirm the receipt email arrives.
- Confirm the public site exposes no secrets.
- Confirm no access is provisioned merely because someone visits the success URL.
- Confirm cancellation and failed-payment handling before turning on automated provisioning.

Official Stripe references:

- https://docs.stripe.com/payment-links/create
- https://docs.stripe.com/payment-links/post-payment
- https://docs.stripe.com/no-code/customer-portal
- https://docs.stripe.com/checkout/fulfillment
- https://docs.stripe.com/billing/subscriptions/webhooks
