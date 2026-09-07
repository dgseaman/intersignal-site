# Braid Archangel 1.8.1

## One complete download. Extract and launch.

The corrected composer, Channels, local chat, and Mac Python discovery are already
inside the application wheel. Do not apply another package or replace individual
scripts. No earlier release is required to install this one.

### Start

- **macOS:** open `Start Braid.command`.
- **Linux:** open a terminal in this folder and run `sh "Start Braid.sh"`.
- **Windows:** open `Start Braid.cmd`.

Use standard CPython **3.10-3.13**, local Ollama, and your local embedding and
completion models. These prerequisites are not bundled. First launch installs
pinned Python dependencies into an isolated, version-specific runtime and normally
needs Internet access. Run as your normal user, not root or Administrator.

The Mac launcher finds a supported installed Python and prints its selection.
On Linux or Windows, an unsupported default can be avoided with
`python3.12 start_braid.py` or `py -3.12 start_braid.py`, respectively, when that
interpreter is installed. Read `docs/OFFLINE.md` for a cold offline installation.

### Upgrading an existing public-line client

1. Quit the old application using **Settings & tools > Quit Archangel**, or
   Control-C in its launcher. Closing a browser tab does not stop it.
2. Make a complete private backup of the existing profile, including its semantic
   inbox and keys. The automatic desktop/trust snapshot is not a complete backup.
3. Extract this entire release into a **new folder** and launch from there.
4. Open the address printed by that launcher. The sidebar and Settings should show
   **1.8.1**. An old localhost tab is not the newly launched application.

The launcher reuses the standard existing profile and creates a separate 1.8.1
runtime. It preserves identity, contacts, channels and accepted notes. There is no
new protocol or database-schema migration. Existing compatible rig/channel cards
do not need recreation for this maintenance release. Do not run two versions
against the same live profile. Keep the experimental Resilience profile separate;
this is not a downgrade procedure for it.

If another version is still running, this launcher stops with an explanation. It
does not open the old version and pretend an upgrade succeeded.

### Compose

**Share summary** always opens a blank, editable message at **Write**. It does not
resume an old summary or delta. **Drafts** explicitly resumes saved work.

**New message** saves nonempty work and starts blank. **X**, **Escape** and
**Save draft** close without sending. **Discard draft** asks before discarding only
the draft; it does not erase received notes, Sent history, or delivery records.
There is one saved-draft slot; replacement asks for confirmation.

Accepted and uncertain recipients remain locked in the original handoff. Never
create a new message merely to bypass an uncertain delivery. Closing during a
running operation does not cancel or repeat it; a new composer waits until the
operation finishes.

### Next

Use `docs/CHANNELS_GUIDE.md` for pairing, channel permissions and local chat.
Use `docs/UAT.md` for a short check on your real machines. Verification results and
limits are in `docs/QA.md`. Full current source is included under `source/` for
inspection; extracting it is unnecessary to run Braid.

This package is not a notarized macOS app or an Authenticode-signed Windows
installer. Use per-item OS approval for a verified download, not global security
bypasses. Managed Relay remains forthcoming; installation does not provision it.

Optional read-only consistency check: `python3 verify_release.py .`.
