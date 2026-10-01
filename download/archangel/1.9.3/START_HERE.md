# Start Braid Archangel 1.9.3

Extract the complete **Braid-1.9.3.zip** before starting. Keep its contents together.

- **macOS, Apple silicon:** copy **Braid.app** to Applications and open **Braid**.
  Its runtime is included; no Python installation is needed.
- **Windows:** double-click **Start Braid.cmd**. Standard CPython 3.10–3.13 must
  already be installed and available through `py` or `python`.
- **Linux:** run `sh "Start Braid.sh"` with standard CPython 3.10–3.13 available as
  `python3`, including `venv` and `pip`. See **PLATFORMS.md** for file-manager setup.

Windows and Linux retain the 1.9.1 launcher approach: the first launch creates a
private runtime and installs pinned dependencies. An unprepared first launch
needs internet access. Offline preparation is available through
**prepare_offline.py** and **docs/OFFLINE.md**.

In Braid's sidebar choose **Folio — Publish to Web**, or choose **Publish with
Folio** on a conversation or note. The same Braid instance opens the studio at
**/folio**; no separate Folio install, launch, or connection setup is needed.
Selected material becomes a private draft. In **Redaction studio**, toggle
original source blocks beside the public preview, or edit their public excerpts.
Amber marks are local advisory warnings. The state banner compares the current
public content with the latest immutable export. Edit, review the exact public edition,
explicitly approve, then export. Nothing publishes automatically.

Ollama and your own local models are needed for chat, not for Folio. Use
**Settings & tools → Quit Archangel** to stop Braid and Folio together. Closing
the browser alone leaves the local application running.

Do not run two versions against a live profile. Back up the complete profile,
quit the previous application, then launch the new version. An older running
version is rejected rather than silently reopened. Existing identities, WAN
choices, Channels, grants, and history remain in their current profile.
Read **MIGRATION_NOTES.md**, **PLATFORMS.md**, and **TEST_RESULTS.md** in the release
root. Windows/Linux launchers are included; native binaries and physical testing
on those systems are not claimed. The Mac app is ad-hoc signed, not notarized.
