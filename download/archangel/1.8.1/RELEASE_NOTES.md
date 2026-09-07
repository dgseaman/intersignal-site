# Archangel 1.8.1 - release notes

## Complete integrated distribution

This release replaces the user-facing package, not individual installed files.
The composer correction is compiled into the application wheel. The same folder
contains the current launchers, manifests, complete source and current guides.
No differential-update files or historical fix bundles are included, including
inside the source archive.

The 1.8.0 wheel already contained the corrected composer. Its distribution still
included developer diffs and older repair documents, making the installation
contract unclear. This release removes that ambiguity; it does not claim those
diffs were previously required at runtime.

Version 1.8.1 is consistent in the wheel, package metadata, source, launcher,
sidebar and Settings. Its runtime is separate from older installed versions.
If an older version still owns the profile lock, the new launcher refuses to
open its window as a successful launch. The child also checks its installed
package version before starting the service.

## Unchanged

Corrected composer behavior and CSS, transport, signatures, receiver validation,
semantic field, channel policies, model adapters and durable delivery ledger are
unchanged from 1.8.0. The only application-file changes are the version module and
visible version badge. No new dependencies, hidden downloads, key rotation,
re-pairing requirement or automatic resend. Resilience remains a separate preview.

## Evidence boundary

The September 7 spending-constraint demonstration remains predecessor evidence.
The original answer returned 500 but omitted the second-server qualifier and
contained generic cautions. This release does not recast it as spending enforcement
or as a new physical 1.8.1 test. Native Safari/Windows, actual models, physical QR,
WAN and complete platform qualification remain separate tests.
