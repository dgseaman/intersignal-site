INTERSIGNAL BRAID + FOUNDING MEMBERSHIP SITE UPDATE

What this adds
- A reproducibility/compatibility section explaining what technical users can do now.
- Clear language that completion LLMs do not have to match.
- Honest guidance that a matching embedding digest is the easiest first reproduction.
- A $99/year Braid Founding Member section.
- Live $99/year Stripe Payment Link preconfigured in site-config.js, with optional customer portal support.
- A safe post-checkout page that does not expose credentials or grant access.
- STRIPE_SETUP.md for product, checkout, portal, manual fulfillment, and later webhook automation.
- NATIVE_1_6_TURNKEY_REQUIREMENTS.md defining the generalized paste/file → send → fresh-query product workflow.

Before publishing
1. The live annual Payment Link is already inserted.
2. Add the optional public customer portal link to site-config.js when available.
3. Do not place Stripe secret keys, webhook secrets, relay tokens, or private Braid keys in the site.

Publish from a Mac with GitHub CLI or an existing GitHub SSH key:

  cd ~/Downloads/intersignal-kestrel-stripe-site-update
  ./publish.sh

The script clones a fresh repository copy, validates the HTML, copies only the site update files, commits, and pushes main.
