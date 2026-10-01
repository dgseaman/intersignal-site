# Braid Archangel 1.9.3

Folio adds a Redaction & Selective Inclusion Studio. Open a folio or import a
conversation to see immutable originals on the left and the rendered public
article on the right. Click an original block to include/exclude it. Use
**Edit public excerpt** to redact its public text. Compose retains title,
speaker, order, theme, introduction, conclusion, sources, and connection editing.
Exclusion also removes capsule references. Re-inclusion does not silently
restore capsule selections. Empty selections still require publication text.

Amber advisory marks identify obvious local file paths, private/internal IPs,
machine hostnames, credential-like strings, emails, and phone numbers. Scanning
runs in the local Braid/Folio process, without external calls or telemetry.
Originals are marked in the private source pane; review findings cover only
public fields and enabled capsule contents. Marks and private originals never
enter exported files. Warnings are advisory and can miss sensitive details.
Explicit approval remains available after a human review of flagged material.

A prominent content-bound banner appears across all editing steps:

- **PRIVATE DRAFT — review before export**: no current approval/export.
- **LOCAL CHANGES — re-approval required**: unsaved edits or a changed exported
  draft. Saved private-only edits preserve the existing public approval.
- **APPROVED — newer than latest export**: the current public digest is approved,
  but differs from the latest bundle. First approval says ready for first export.
- **PUBLISHED — matches latest export**: an explicitly approved current public
  digest exactly matches the latest immutable exported edition.

The comparison is to the latest local export, including its theme, public
labels, capsule and connection choices. It does not verify deployment or
separately hosted live content. Existing exported bytes remain immutable.
Editing, including reverting to an older public edition, follows the existing
approval invalidation rules. Stale preview approvals and concurrent saves are
still rejected. The preview clears while edits save and refuses stale responses.

The Mac application remains self-contained and windowed: normal launch opens
Braid without a Terminal window. Windows/Linux retain their Python launchers,
using the same 1.9.3 wheel and pinned dependency list. Mac signatures are ad-hoc;
Developer ID notarization and native Windows/Linux qualification are pending.
See TEST_RESULTS.md for executed checks and exact limits.
