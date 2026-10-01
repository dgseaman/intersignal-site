# Braid 1.9.2 — one ZIP, three platform entry points

Folio 0.3.0 is built into Braid on every platform. Start Braid once, then choose
**Folio — Publish to Web** or **Publish with Folio**. No separate Folio launcher,
download, profile connection, or Python process is needed.

| Platform | Start | Requirements |
| --- | --- | --- |
| macOS, Apple silicon | Copy `Braid.app` to Applications and open it | Runtime included; no Python installation |
| Windows | Double-click `Start Braid.cmd` in the extracted folder | Standard CPython 3.10–3.13 with venv and pip |
| Linux | Run `Start Braid.sh` in the extracted folder | Standard CPython 3.10–3.13 with venv and pip |

Windows and Linux use the same wheel-and-launcher packaging approach as 1.9.1.
The launcher creates a private runtime and installs the pinned dependencies on
first launch. Keep the wheel, scripts, dependency list, and manifest together.
Internet access is needed for an unprepared first launch. See `docs/OFFLINE.md`
and `prepare_offline.py` for preparing a verified offline dependency pack.

On Linux, if the file manager does not execute shell scripts, make the launcher
executable and run `./Start\ Braid.sh` from the extracted directory. Python must
include `venv`/`ensurepip`; some distributions package those components separately.
On Windows, Python must be available through `py` or `python`.

Bring your own Ollama installation and local models for chat. Folio itself does
not require a model. Quit the old Braid version before starting 1.9.2 against an
existing profile; back up the complete profile first. Read `MIGRATION_NOTES.md`
for the retained Braid identities and separate Folio storage/migration rules.

The Mac app is ad-hoc signed, not Developer ID notarized. Windows/Linux native
binaries are not included. The shared application and platform code paths were
tested on the recorded Mac host; physical Windows/Linux execution still needs
verification on those systems. Exact evidence stays in `TEST_RESULTS.md`.
