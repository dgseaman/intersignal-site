# Braid Archangel 1.8

Release version: **1.8.0**. Channels, ordinary local chat, and a corrected new-message composer.

This is the public a6 Channels line with Composer Fix 1 integrated and a clear new release identity. It does not incorporate the optional a7 Resilience preview. No transport, receiver, field, channel-permission or delivery-ledger logic was changed from the corrected a6 baseline.

## Upgrade from a6 or a6 Composer Fix 1

1. Quit the existing client using **Settings & tools > Quit Archangel** or Control-C in its launcher. Closing the browser tab is not enough.
2. Back up your complete profile, including the semantic inbox and private identity. The automatic desktop/trust snapshot is not a full-profile backup. Do not share backup keys.
3. Extract the **whole 1.8 ZIP into a new folder**; do not replace individual files in the old release. Keep the previous bundle and backup.
4. Start using the launcher below as your normal user, not root or Administrator. Open the URL printed by this launch, not an old localhost tab.
5. Confirm **1.8** beside Settings & tools and **1.8.0** in the backend/launcher output. Click **Share summary**: the subject and source should both be empty at Write.

The standard profile path remains `~/Library/Application Support/Intersignal/Braid/messenger` on macOS and `~/.braid/messenger` elsewhere; the existing `messenger-a4` preference is retained when that database exists. Custom profiles use `--profile PATH`.

The launcher creates a version-specific 1.8 runtime, snapshots desktop/trust data before opening an existing profile, and reuses your identity, contacts, channels and accepted notes. No new backend schema migration or key rotation is added. Existing a6 rig and channel cards do not need recreating solely for this update. Do not run two versions against the same live profile. This upgrade path is for a6/a6-c1, not an instruction to downgrade a live a7 preview profile; retain a7 separately and use its corresponding full backup when reverting.

## Launch

Prerequisites: standard CPython **3.10-3.13**, local Ollama, and local embedding/completion models. Python 3.14 and free-threaded builds are not in this dependency target. Python, Ollama and model weights are not included in this small ZIP.

- **macOS:** open `Start Braid.command`. The Mac runtime-discovery fix is included: it skips unsupported defaults and prints the supported Python it selects. It does not alter global Python aliases. `BRAID_PYTHON` can select an explicit supported executable.
- **Linux:** open a terminal in the extracted folder and run `sh "Start Braid.sh"`.
- **Windows:** open `Start Braid.cmd`, or run `py -3.12 start_braid.py` when that runtime is installed.

Linux/Windows keep their existing launcher behavior. If the default Python is unsupported, use `python3.12 start_braid.py` or the explicit Windows selector. First launch installs pinned dependencies in an isolated runtime and normally requires Internet access. Local browser UI remains loopback-only.

The archive is not a signed/notarized macOS app or an Authenticode-signed Windows installer. Use per-item OS approval after verifying the source/hash; do not disable Gatekeeper globally. A script missing its execute bit can be launched with `sh "Start Braid.command"`.

## New message means new message

**Share summary**, the welcome action and keyboard **N** start a blank message with a fresh handoff identity. They do not silently reopen the saved delta or old summary.

**Drafts > saved item** explicitly resumes that draft with its original identity, mode and delivery locks. **New message** inside the composer saves nonempty work and opens a blank composer. **X**, **Escape** and **Save draft** close without sending. Closing an empty new message preserves an older saved draft.

**Discard draft** asks before removing only the draft; it does not remove received notes, Sent history or delivery records. There is still one saved Messenger draft slot. Replacing a different saved draft requires confirmation; declining keeps both the older draft and the current open text available. Save failures keep the current text visible.

During an in-flight send or summarization, closing does not cancel or restart the job. Another composer cannot open until it finishes. Accepted and uncertain recipients remain locked. A new message is not a workaround for an uncertain previous send.

## First useful check

After launch, click Share summary, verify it is blank, close it, and reopen it. Then resume Drafts deliberately to confirm the older draft remains available. Send a genuinely new harmless note to an approved receiving rig, inspect Accepted & indexed, and ask a fresh question from the receiver's Shared field.

For project Channels, follow `CHANNELS_GUIDE.md`: create one channel identity, import its card on the other rig, independently authorize send/receive/chat use, publish a reviewed note, and ask in Channel Chat. Legacy non-channel handoffs remain in Shared field; they are not silently added to a channel.

## What the September 7 demo established

The founder reported a Linux-to-Mac handoff of `spend no more than 500 credits on our second server today`. The supplied Mac receipt photograph shows Received, Accepted and Indexed. A subsequent supplied field-answer screenshot shows one indexed item/object and a fresh question returning **500**.

Those images document the preceding a6 test session, not a physical 1.8 test. The answer omitted the source's `second server` qualifier and included generic cautions about possible conflicts. No full query JSON/model trace was supplied for this follow-up. The demonstration establishes return of the supplied numeric value, not enforced spending limits, a detected conflict, universal accuracy, or coverage of every channel/platform/transport. See `DEMO_SPENDING_2026-09-07.md` for the exact record.

## Retained boundaries

Models receive selected text evidence; no weights or KV caches are transferred. Signed material conveys provenance, not truth. Indexing does not prove a subsequent answer used it. The shared-notes count describes exact semantic atoms supplied to a successful completion, not attention or certified facts. Only Archangel chat consults its channels automatically; unrelated chat applications are not intercepted.

Managed Relay remains forthcoming and separately provisioned. This ZIP does not create accounts, change billing or select alternative transports automatically. a7 receipt recovery and its other preview hardening are not included in 1.8. A previous `Not sent - preparation failed` delta requires its detailed receipt error for diagnosis; the composer correction is not a claim to fix that separate preparation failure.

## Offline setup and verification

On a matching connected target, run `python3 prepare_offline.py ./offline-pack`; copy the pack with the release and run `python3 start_braid.py --offline --wheelhouse ./offline-pack`. Packs are specific to OS, architecture and Python minor. Explicit `--use-existing-env` is available but not isolated; `--isolated-runtime` restores the normal choice.

Read-only release check: `python3 verify_release.py . --report package-check.json` or the platform launcher with `--check`. Hashes establish byte consistency against trusted expected values, not publisher authenticity. The source ZIP is for developers; the complete ZIP includes the prebuilt wheel and launchers.

See QA.md for tests actually executed and UAT_1_8.md for the remaining physical checklist. A public version number does not turn unexecuted platform tests into certification.
