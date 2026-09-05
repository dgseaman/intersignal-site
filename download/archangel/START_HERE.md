> **Mac launcher fix 1:** This repack adds supported-runtime discovery to
> `Start Braid.command`. The a5 application is unchanged. Read
> `MAC_LAUNCHER_FIX1.md` for the exact scope and test limits.

# Braid Messenger 1.7.0a5 - Archangel

## Your rigs. Clear receipts. A quieter network underneath.

Archangel preserves the small Messenger window and fixes delivery, storage, network admission, address changes, installation and shutdown around it. This is a runnable engineering alpha, not a signed native installer or a claim of completed physical cross-platform certification.

## Upgrading from a4

Quit a4 first. Extract the entire Archangel ZIP into its own directory; do not overlay files into the old release folder. Keep the original a4 bundle as a fallback.

The launcher automatically reuses the standard `messenger-a4` profile when its database exists. Otherwise it uses a new `messenger` profile. On macOS the base is `~/Library/Application Support/Intersignal/Braid/`; elsewhere it is `~/.braid/`. A custom profile can be selected with `--profile PATH`. The launcher prints the actual path.

Before opening an existing desktop database for the first time under Archangel, the launcher makes a consistent SQLite snapshot and copies the signing/TLS identity files and peer-route directory into `backups/pre-archangel-...`. This is a **desktop/trust snapshot, not a complete backup of the semantic inbox or model files**. Existing committed frames and fields stay in place and are not rewritten by this migration. Make a full profile backup separately for a complete rollback. Do not run a4 and a5 against the same live profile, and do not casually downgrade its delivery database: a4 does not know the new durable handoff rules.

After upgrading each rig, save a fresh Archangel rig card and approve it on the other rigs, in both directions. Compare the signing fingerprint on the source device. Archangel requires mutual TLS capability for the direct Messenger path; old a4 cards cannot be newly imported. Existing trust/history stays stored, but legacy peers are not silently granted a downgrade path. Incomplete or unexpected identity changes require deliberate repair, not key regeneration.

## Open Archangel

Use standard CPython **3.10 through 3.13**. Python 3.14, free-threaded builds and additional interpreter families are not in this release's validated dependency target. Python and local Ollama are prerequisites, not bundled runtimes.

After extracting the ZIP, use `Start Braid.command` on macOS, `Start Braid.cmd` on Windows, or run `sh "Start Braid.sh"` on Linux. The portable command, run inside the extracted directory, is:

```sh
python3 start_braid.py
```

On Windows, select a supported installed Python explicitly when needed:

```powershell
py -3.13 start_braid.py
```

`python3.12 start_braid.py` or `py -3.12 start_braid.py` are equally valid examples. If the default `python3` or `py -3` selects an unsupported version, use one of these explicit selectors. No global Python packages are installed by the normal launcher.

The first normal launch verifies the bundled application and support-file hashes, creates a version-specific isolated environment, and installs pinned binary dependencies. That first installation needs Internet access unless an offline pack or explicitly chosen existing environment is supplied. Subsequent launches reuse the local environment. The browser UI binds only to loopback and uses local assets and system fonts; no Electron, Node or UI asset CDN is required.

### macOS launch restrictions

This archive is not Developer ID signed or notarized. Archive tools can also lose a script's executable bit. Review the source and checksum, then run the Python command above from Terminal to avoid relying on double-click script launching. To restore a trusted launcher script's execute bit, run `chmod u+x "Start Braid.command"`. When macOS displays a trust warning, use the operating system's per-item Privacy & Security / Open Anyway process only after verifying what you downloaded. Do not disable Gatekeeper globally or recursively remove quarantine as a blanket workaround. Apple's current guidance: https://support.apple.com/en-us/102445

### Quit, restart and interrupted operations

Closing the browser window does not stop the service. Use **Settings & tools > Quit Archangel**, Control-C in the launcher, or:

```sh
python3 start_braid.py --stop
```

For a non-default profile, supply the same `--profile PATH`. The parent requests authenticated cooperative shutdown first, waits for work to drain, and uses forced termination only as a bounded fallback. Power loss, forced OS termination and blocked native calls cannot be made graceful; on restart, in-flight handoffs become **Receipt not confirmed**, never an automatic resend.

The OS-held profile lock controls exclusivity. A leftover `launcher.lock` filename is not evidence of a stuck process and should not be deleted to bypass a running instance. Relaunching a live profile opens its current window instead of starting another server. If an older version is running, quit it before upgrading.

## Offline and air-gapped setup

A fresh offline rig needs Python, the applicable Python dependency wheels, and any Ollama/model files already provisioned. **The universal Archangel ZIP does not contain prebuilt third-party wheel packs for every operating system.**

On a connected computer with the same OS, architecture and Python minor version as the destination, extract Archangel and run:

```sh
python3 prepare_offline.py ./archangel-offline-pack
```

The builder downloads the pinned binary dependency closure, records exact wheel hashes, and writes a target-bound manifest and hash-checked requirements file. It refuses to merge into a nonempty directory. Copy the whole generated directory and the Archangel release to the offline rig, then run:

```sh
python3 start_braid.py --offline --wheelhouse ./archangel-offline-pack
```

A local, trusted wheel cache can be used with `prepare_offline.py DEST --from-wheelhouse CACHE`. Use the matching Windows Python selector on Windows. Platform packs are not interchangeable. Model weights, Ollama itself, and the interpreter are separate from this wheel pack.

Offline verification rejects wrong targets, a changed dependency specification, missing or changed bytes, unlisted wheels, symlinks and requirements-file directives. Installation uses `--no-index`, exact hashes and the isolated runtime. An offline first launch without a usable pack fails with guidance instead of silently trying PyPI.

For an operator who deliberately prefers already-installed host dependencies:

```sh
python3 start_braid.py --offline --use-existing-env
```

This validates required imports and minimum versions before creating an explicitly host-linked runtime. A visible, path-only `archangel-host-explicit.pth` file links the selected interpreter's package directories, including when it is itself a virtual environment; the normal isolated path never creates that link. **This choice is not isolated** and is saved for later launches of that profile. It never activates silently as a failed-install fallback. Return to the isolated path with `--isolated-runtime`, adding `--wheelhouse PATH` for a cold offline installation. Both paths still install the verified application wheel. Hashes detect accidental changes; neither the bundle manifest nor an offline-pack manifest is a publisher signature or protection against an attacker replacing both files and hashes.

## Pair your rigs

Start Ollama locally and provision the usual embedding model once:

```sh
ollama pull all-minilm
```

In **Add rig > This rig**, name the rig, select its actual private/overlay interface and press Prepare. An already calibrated route can be selected through the retained advanced route option. Save the public `.braidrig` card, move it through a trusted channel, import it under **Other rig**, compare the full fingerprint, and approve. Repeat in reverse. Cards contain public identity, certificate, endpoint, capabilities and route material, not private keys or conversations.

Start receiving on each rig, then check connections. Default direct-receiver port: **8746**. Permit it only on the intended private or authenticated overlay network. Never publish the loopback UI or blindly forward the listener to the public Internet. The address category itself does not prove that a VPN is secure or correctly configured.

Supported direct endpoints are numeric private IPv4, loopback, the overlay/CGNAT block `100.64.0.0/10`, usable IPv4 link-local addresses, and IPv6 ULA/loopback. Known metadata endpoints, public/wildcard/multicast addresses and DNS names are refused. IPv6 link-local addresses with host-specific scope IDs are intentionally not portable card endpoints; choose IPv6 ULA, overlay IPv4 or direct-link IPv4 instead.

A green contact means a recent explicit reachability check succeeded. It is not a receiver commit and does not mean a model consumed any context. Relay/Jump Kit enrollment and NAT traversal remain separate existing workflows; Archangel does not create a relay account, alter billing or automatically punch through a router.

### A rig changed networks

Open **Settings & tools > Network address**, choose a currently assigned interface and press **Update address**. Braid checks the address, pauses/restarts the listener as needed, and preserves signing identity, TLS identity, route, inbox and history. Export the new card and approve it on the other rigs. A valid address-only update replaces the endpoint in place. Signed card revision high-water marks reject stale address rollback, including after removing and re-adding a contact. A certificate or route change is not treated as a harmless address update.

## Share once; retry deliberately

The workflow remains **Write > Review > Share**. Use a local model for a summary or choose exact text; review numbers, negations, uncertainties and sensitive material before sharing. The inline limit is 6,000 UTF-8 bytes. An extractive fallback is labeled explicitly. A subject is a local Sent label, not additional signed semantic content.

Every reviewed handoff now has a stable identity and a durable result for each recipient. The database reserves a recipient before network work. Refreshing, reopening a draft, double-clicking, repeating an API request or restarting cannot make a known successful recipient receive that same handoff again from this sender's delivery ledger.

After partial success, accepted recipients are unchecked and locked; only explicitly rejected or preparation-failed recipients are eligible to retry. **Receipt not confirmed** is also locked because the receiver may already have committed the object. Inspect Sent and the receiver before taking any further action. There is no claim of globally exactly-once networking or an atomic multi-rig broadcast.

Reviewed content is fixed once an attempt exists. **New handoff** deliberately creates a new identity and warns that it does not resolve an uncertain receipt. That explicit action can send the same text again; do not use it as an automatic workaround. Duplicating, deleting or restoring profiles can also bypass sender-local history and must be handled deliberately.

The receipt distinctions remain: received bytes are not acceptance; receiver-owned Phase B commit is acceptance; indexing is a separate confirmed fact. Reading and archiving do not retract committed state. The compact display shows the newest 500 messages; the durable database and protocol artifacts remain on disk. Receipt ingestion is live plus bounded periodic reconciliation, so older retained receipts can appear progressively after a large backlog.

## Semantic field and the full client

The receiver-local 384D field, exact semantic atoms, conflict-preserving reconciliation, guarded questions and signed deltas remain available. Indexing does not prove truth, agreement, native hidden-state interchange or use by a subsequent model answer. The new UI does not silently ingest another chat application's conversation.

Advanced workspace and the full CLI remain included. Optional camera/sensing dependencies are not in the core offline pack. Signed deltas in the Messenger composer remain a direct approved-peer feature; use the retained explicit CLI for delta workflows over Managed Relay. Archangel's direct-listener mTLS policy does not silently change every legacy optical, manual, relay or advanced intake path.

## Checks and support evidence

```sh
python3 start_braid.py --check
```

Read `QA.md`, `AUDIT_RESOLUTION.md` and `UAT_ARCHANGEL.md`. Automated Linux loopback, installed-wheel and fixture-backed UI evidence is included. Native macOS/Windows ACL, installer, real-model and physical multi-rig/WAN tests are still required before stable promotion. This build has no added telemetry or auto-update agent.
