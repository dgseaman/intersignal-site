# Braid Archangel 1.9.3 migration

Your Braid identity, trust, Channels, history, WAN opt-ins, and receiver inbox
stay in the existing profile. The existing upgrade launcher/native entry takes
a consistent desktop/trust backup before upgrading. Semantic stores are kept
in place. Data is never reset to make the new studio appear empty.

Folio's integrated library lives at `<Braid profile>/folio/folio.sqlite3`, with
its own private `exports` directory. The ordinary macOS Braid profile is under
`~/Library/Application Support/Intersignal/Braid/messenger`; an existing
`messenger-a4` database continues to be selected. The existing Linux and
Windows Braid profile location `~/.braid/messenger` is retained for compatibility.

On the first start of a standard Braid profile, Archangel automatically copies
the legacy Folio library if an integrated library does not already exist:

- macOS: `~/Library/Application Support/Intersignal/Folio`
- Linux: `$XDG_DATA_HOME/intersignal/folio`, defaulting to `~/.local/share/intersignal/folio`
- Windows: `%LOCALAPPDATA%/Intersignal/Folio`, defaulting to `~/AppData/Local/Intersignal/Folio`

Migration uses SQLite's backup API, checks database integrity, copies export
archive bytes unchanged, and atomically places the completed copy. Draft IDs,
private originals, publication identity/lineage, preferences/pins, stream
configuration, and immutable edition archives are retained. A private
`migration.json` receipt records the copy. The source library and its exports
are not deleted, rewritten, or merged. If a destination already exists it is
retained, and migration is not repeated. An interrupted staged copy is cleaned
up; a completed destination is never overwritten.

Close a running standalone Folio compatibility app before this first migration.
Its profile ownership lock prevents copying a library during an active write.
If the legacy library is busy, startup reports that specific condition and
leaves the library unchanged. After it is closed, launch Braid again. Custom
Braid profiles start with their own isolated Folio library. Developers may set
`BRAID_FOLIO_LEGACY_HOME` to explicitly select a legacy source for a custom
profile; this is not a normal user setup step.

Legacy Broadcast settings stay in the copied database, but Archangel executes
them as Review queue. No automatic approval or release occurs. Because older
automatic approvals cannot reliably be distinguished from human approvals,
all legacy drafts require a fresh review in the integrated studio. The old
approved_digest remains in the copied database until an explicit later edit;
the studio treats it as unapproved without changing the legacy source.

Existing edition archives remain downloadable and byte-identical. An existing
static stream site is not removed. Rebuilding a legacy stream site requires
review receipts for every edition being copied to that site. Review the legacy
draft and approve the exact body before retrying. If a draft has changed since
an older edition, that older body must be reconstructed and reviewed before
it can be included in a newly rebuilt site; its original archive remains safe.

Folio's private original storage is local plaintext protected by POSIX private
modes or Windows protected DACLs. Protect the operating-system account and
backups. The scanner is a heuristic; approval remains the user's decision.
Importing a draft, enabling a connection invitation, accepting a request, and
approving a rig card are distinct operations.

To return to Folio 0.3.0 for compatibility, use its retained original library.
Do not point an older standalone app at the new integrated library: it does not
know Archangel's additional review receipts. New integrated work is not silently
synchronized back to the retained legacy profile. Back up the complete Braid
profile before an intentional rollback.

## Folio studio in 1.9.3

No Folio database schema migration is needed for the new studio or state banner.
The banner is derived from the current public content digest, the current
approval receipt, and the latest saved edition digest. Private originals,
existing editions and approval invalidation rules retain their existing model.
Reopening/importing a folio enters the Redaction studio; new writing still opens
Compose. Public fields, capsule, themes and connection choices remain in review.
