# Braid Archangel 1.9.2

## Major feature: integrated Folio publishing

Install and launch Braid once. Folio 0.3.0 is included as a local studio on the
same running server at `/folio`. The left sidebar's **Folio — Publish to Web**
opens it directly. **Publish with Folio** on completed conversations and saved
Channel notes creates a private, unapproved draft and opens that draft in the
studio. There is no separate Folio connection or runtime setup in this journey.

The release includes a self-contained macOS arm64 Braid.app, its companion
console tools, a complete source package, the integrated Python wheel, checksums,
release/migration notes, raw test logs, machine-readable test reports, and
browser proof. Native Linux and Windows build recipes are included in source;
actual Linux/Windows native binaries and native OS runs require those hosts.

The updated **Braid-1.9.2.zip** brings the Mac app and the Windows/Linux launchers
together in one download. **Start Braid.cmd** and **Start Braid.sh** use the same
private-runtime, wheel-based approach as 1.9.1, with the integrated 1.9.2 wheel.
Standard CPython 3.10–3.13 is required on Windows/Linux; pinned dependencies are
installed on first launch. These are usable launcher distributions, not just
native build recipes. See **PLATFORMS.md** for prerequisites and exact limits.

## Approval and privacy

Folio retains its own storage, private originals, review/approval, immutable
editions, publication identity, permalinks, themes, capsules, export kits, and
privacy filtering. Its adapter automatically belongs to the current Braid
instance and permits only bounded views and public publication registration.
Private content is never passed into the registration or ordinary Braid state.

Streams always prepare review drafts in Archangel. Legacy Broadcast settings
are retained but do not auto-approve or publish. Legacy approvals require a new
studio review. Public edits invalidate approval; reviewed past editions remain
immutable. Legacy stream-site rebuilding is also guarded by explicit review
receipts. Separate Folio authentication, same-origin/Host checks, request limits,
and no-store/CSP headers remain in force. Windows private files use protected
DACLs instead of relying on POSIX modes.

## Invitations and lifecycle

Public publication pages/referrals never grant Braid authority. A reader's
request, publisher acceptance, each card-sharing decision, fingerprint review,
and scoped Channel grants remain explicit. Integration tests rehearse the full
flow against a local synthetic rendezvous; no live enrollment or website change
is performed.

Leaving the Folio surface returns to Braid. Quit Archangel drains local HTTP
work, stops Folio's scheduler, closes Braid jobs, releases profile ownership,
and removes the session marker. Restart preserves drafts/editions and rotates
ephemeral tokens. The standalone Folio launcher remains in source solely for
developer/compatibility use.

## Qualification

Read `TEST_RESULTS.md` for exact results and unresolved platform qualification.
The macOS app is ad-hoc signed; no Developer ID notarization is claimed. The
unaltered address-change regression needs a `127.0.0.2` loopback alias which this
restricted host does not provide. A remaining failure is reported, not hidden
or converted into a pass. Production deployment qualification therefore remains
open. Existing assertions were retained except literal release-version updates;
the source ZIP's missing executable permissions were restored.
