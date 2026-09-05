# Braid Archangel 1.7.0a6 - Channels

**One field. Any path.** Channels organize deliberately shared notes. Ordinary local chat can use those notes and show an inspectable **Using N shared notes** receipt under each answer.

This is a runnable engineering alpha. The prior a5 Mac-to-Linux demonstration is evidence for a5, not physical certification of these new a6 bytes. Keep the working a5 download in place until the a6 physical checklist is completed.

## Upgrade without disturbing your working rigs

1. Quit the old client using Settings & tools > Quit Archangel. Closing its browser tab is not enough. Do not run two versions against one profile.
2. Make a complete external backup of your profile (including the semantic inbox). The launcher's automatic snapshot covers the desktop database, signing/TLS identities and peer routes, not the complete semantic store or models.
3. Extract this whole ZIP into a new directory. Do not overlay one script on an older bundle. All required support-file hashes match this release.
4. Start with the platform launcher below. It reuses the existing standard `messenger-a4` profile when that exists; otherwise the standard `messenger` profile. It does not rotate your keys or erase accepted a5 state. An a5 upgrade marker no longer skips the a6 desktop/trust snapshot. A custom profile uses `--profile PATH`.
5. Save fresh a6 rig cards and approve them in both directions. Identity fingerprints should stay the same. The refreshed cards advertise `channels.v1`; direct channel sharing does not silently fall back to a5.

Mac profile base: `~/Library/Application Support/Intersignal/Braid/`. Linux/Windows profile base: `~/.braid/`. The launcher prints the chosen profile. Backups remain local and are not uploaded.

## Start the application

Use standard CPython **3.10 through 3.13**, local Ollama, and your already-installed embedding/completion models. Python 3.14 and free-threaded builds are outside this dependency target. The ZIP does not contain Python, Ollama, model weights or every platform's dependency wheels.

**macOS:** open `Start Braid.command`. It retains Mac Launcher Fix 1: skips unsupported default interpreters, checks supported versions and common install locations, and prints its choice. `BRAID_PYTHON` may select an explicit supported executable. No global aliases or Python installations are changed.

**Linux:** open a terminal inside this folder and run:

```sh
sh "Start Braid.sh"
```

**Windows:** open `Start Braid.cmd`. An explicit supported runtime can also launch it:

```powershell
py -3.12 start_braid.py
```

Linux and Windows retain their original launcher selection behavior. When their default interpreter is unsupported, explicitly run `python3.12 start_braid.py` or `py -3.12 start_braid.py`. The macOS discovery logic is not silently claimed for other platforms.

The normal first launch creates its version-specific isolated environment and installs pinned dependencies, requiring Internet access or a prepared offline wheel pack. Run as your own user, not root or Administrator. This archive is not Developer ID signed/notarized or Authenticode signed. Use OS per-item approval only after verifying the download. Never disable Gatekeeper globally. Terminal launch is an alternative to a lost script execute bit.

Offline commands and host-environment opt-in are retained:

```sh
python3 prepare_offline.py ./offline-pack
python3 start_braid.py --offline --wheelhouse ./offline-pack
# Deliberately non-isolated alternative only when required:
python3 start_braid.py --offline --use-existing-env
```

An offline pack must match the target OS, architecture and Python minor. It does not contain model weights. `--isolated-runtime` explicitly returns to isolation. `--check` verifies the release bundle without starting the profile.

## First channel - Mac to Linux

### A. Prepare and approve the rigs

Start Ollama locally. The existing proof embedding model is `all-minilm`; provision it once with `ollama pull all-minilm` when needed. Install a local completion model separately.

In **Add rig > This rig**, keep/select your intended private or overlay address and prepare the route if not already ready. Save each a6 `.braidrig` card. Import under **Other rig**, compare the complete fingerprint with the owning device, and approve in both directions. A fingerprint alone is not a connection card. Start receiving on the receiving rig. The loopback browser URL is not its peer address.

### B. Create one channel identity, not two names

On the Mac, click **+ beside Channels**. Create **Cobalt** with a short description. In **Channel settings**:

- Enable **Send to** for Linux.
- Choose independently whether notes may be **used in local chat**.
- Leave **Review each note** selected for this first test.
- Save settings, then use **Save channel card** to export the signed `.braidchannel` file.

On Linux, click **+ beside Channels > Import channel card**. Verify the full channel ID and creator fingerprint through your trusted channel. Import the Mac's card; do not independently create another Cobalt channel. Two channels with the same display name are intentionally different identities.

On Linux's **Channel settings**, enable **Receive from** for the Mac and **Allow this channel's notes in local chat**. Save. Reverse-direction send/receive checkboxes are optional until you test that direction. Importing a card grants no send, receive, or chat permission automatically. The settings on one rig do not edit the settings on another.

### C. Send one reviewed note

On the Mac open **#Cobalt > Share a note**. Enter a title and this exact text:

```text
Project Cobalt's launch color is amber.
```

Click **Review destinations**. The text is fixed for that handoff. Check the destination list, then click **Confirm & share note** once. A local commit occurs through the same signature/route/Phase B machinery before remote dispatch. Inspect local and per-recipient receipts separately. Local indexing does not prove remote delivery.

On Linux open **#Cobalt > Notes & activity**. The received note should be indexed. The original Inbox receipt remains accessible. If a receipt is unconfirmed, inspect the receiver; never make a new note merely to bypass a locked uncertain delivery. Accepted and unknown recipients remain locked in the durable sender ledger.

No destinations selected means an explicitly reviewed note is recorded **locally only**. Drafts are not indexed or sent. Editing a frozen note requires a new deliberate note, not mutation of a signed handoff.

### D. Use the note in ordinary chat

Open **#Cobalt > Chat** on Linux. Choose an installed generation model in **Local model** (or **Find models**). Do not choose the embedding model. Enable **Use shared notes** and ask:

```text
What is Project Cobalt's launch color?
```

Below the answer, expand **Using 1 shared note**. It shows the exact source material, channel, originating rig, source object digest, arrival time, generation branch and full answer record. The expected answer identifies amber, but inspect both the note evidence and the receipt rather than accepting a plausible answer alone.

You can keep chatting in the same conversation or use **New chat**. Recent conversation history is bounded. Earlier shared evidence needed by retained turns is carried explicitly and counted again when supplied. Changing channel permissions or turning shared context off resets the supplied conversation window; old turns stay visible but are not silently injected under the new permissions.

This integrates chat **inside Archangel**. Independent LM Studio windows, Ollama terminal chats, and other applications are not automatically intercepted or populated. No model weights or KV caches change.

## What the shared-notes metric means

A note in this receipt is one unique exact semantic atom supplied to the successful completion request, including retained-history grounding and supplemental conflict siblings. A long handoff can yield multiple atoms; identical atoms can have several source objects and count once. It is not the number of all stored notes, search candidates, trusted truths, or an estimate of the model's internal attention.

An answer that used no shared input says **No shared notes used**. Failed/incomplete turns do not invent a successful receipt. The evidence discloses when the bounded completion guard replaced the model draft. Conflicts that cannot be represented within the bounded evidence window stop generation rather than silently dropping the opposing claim.

## Topic suggestions and carefully scoped automation

There are three channel modes:

**Review before sharing:** write a note, review it, and explicitly publish. This is the default.

**Suggest topic notes:** configure up to 12 literal, case-insensitive topic phrases. In a channel conversation, enable **Suggest topic notes**. A match in your newly typed message creates a local draft, not a transmission. The suggestion copies that source message without model rewriting. Review it before sharing. Matching is phrase-based in this release, not an AI classification guarantee.

**Automatic marked notes:** select the destination rigs, a limit of 1-12 notes/hour, and explicitly authorize the policy. Then, separately enable **Allow automatic /note sends in this chat**. Only a new message you type beginning with `/note ` can publish automatically after the local response succeeds. Example:

```text
/note Project Cobalt's launch color is amber.
```

Only the marked user-authored text is transmitted. Model output, ordinary chat, incoming notes, other apps, and topic matches alone never auto-send. Automatic sends have a durable once-attempted event record, an hourly cap and a minimum five-second spacing. Startup does not drain/replay unfinished automatic work. An uncertain outcome remains locked. A rate-limited note stays available locally for deliberate review.

**Pause outgoing sharing** works without granting additional permission. An already-started network call may finish. Resuming automatic mode or expanding its scope requires fresh authorization. Closing a browser tab does not stop the service; use Quit or Control-C. Automation is not a perpetual filesystem watcher or an external-app agent.

## Conflicts and scope

**Explore conflicts** examines only locally permitted objects in that channel. Chat preserves relevant conflicting alternatives and shows unresolved-conflict indicators. It does not automatically decide which source is correct or create a supersession record. Formal conflict-resolution authoring is not part of this release.

Revoking a channel publisher or disabling use-in-chat excludes its objects from later channel prompts and resets incompatible retained-history context. Prior answers and original evidence remain visible for audit; revocation is not deletion or erasure from a model already processing an earlier request. A permission change detected during generation withholds the new answer.

Legacy a5 handoffs remain in Inbox/Shared field and are not silently assigned to a channel. The retained advanced all-field view is an explicit operator tool; channel automatic retrieval is scoped. To carry older material into a channel, deliberately review and publish a new note; do not imply its channel label was part of the earlier sender signature.

## One field, supported paths

Channel identity and note identity are inside the signed frame, not just local UI labels. The same accepted semantic store backs the channel chat.

- **Direct approved a6 peers:** LAN or an already-configured supported private/overlay endpoint, retaining mTLS and certificate-to-signer binding. a6 does not configure your VPN or router.
- **Signed file:** after a local note commit, use **Export signed note**. On another a6 rig with the same channel card, approved publisher and receive permission, use **Import signed note** in channel settings. Exporting a file is not proof that anyone accepted it.
- **QR reel/chunks:** choose **Save QR reel** beside a committed note in **Notes & activity**. Open the downloaded offline HTML file and press **Start reel**; it cycles the same signed payload as QR chunks. On the receiving a6 rig, use **Advanced workspace > Receive by camera**. Reconstructed channel frames enter the same a6 channel acceptance gate. Pausing, chunk stepping and speed controls are local; displaying a reel is not a receipt. Software chunk reassembly is tested; camera/display scans require physical testing and optional decoder dependencies.

An already accepted note cannot be smuggled in again merely by switching path or reminting the outer frame. Channel-note identities are deduplicated per publisher, in addition to the existing frame replay controls. No globally exactly-once networking is claimed.

Managed Relay is not silently provisioned or billed. Direct channel dispatch deliberately refuses legacy/relay contacts without channel capability. Production Managed Relay channel routing remains a separate integration/physical test, not a new service activated by this ZIP.

## Stop, diagnose and preserve evidence

Use **Settings & tools > Quit Archangel**, Control-C in its launcher, or `python3 start_braid.py --stop` with the same profile. Do not delete an OS lock file to bypass a running process.

For a snag, retain the OS/Python/model versions, channel ID, local policy, exact action, answer evidence and per-recipient outcome. Do not send private keys or full private conversations to support. Read `QA.md`, `RELEASE_NOTES_A6.md`, and `UAT_CHANNELS.md` before replacing the public download.
