# Intersignal Braid v1.5.2 — Linux

This is the production Linux packaging of the Braid v1.5.2 runtime, promoted from the RC1 that passed physical macOS→Linux UAT on both an ASUS Ascent and a Lenovo ThinkPad.

## Desktop behavior

- **Braid Client** opens the local visualizer and starts the trusted secure LAN receiver in a persistent terminal.
- **Braid Visualizer** opens only the local visualizer.
- Desktop launchers use absolute installed wrapper paths and do not depend on the interactive shell PATH.

## Install

```sh
chmod +x install-braid-linux.sh
./verify-braid-linux-package.sh
./install-braid-linux.sh
```

The installer creates an isolated runtime under `~/.local/share/braid/current`, installs `braid` and `braid-client` under `~/.local/bin`, installs the desktop entries, and runs `braid-client --version` plus `braid-client doctor`.

If `python3 -m venv` is unavailable on Debian/Ubuntu, install `python3-venv` and re-run the installer.

## Braid Trust

**Braid Trust** is the enrollment/bootstrap layer for authorized senders and semantic routes. It is not a permanent one-to-one machine pairing. The same trusted sender/route bundle may be enrolled on multiple receiving nodes when policy permits.

A receiver must use an authorized sender's exact frozen route plus the sender **public** key. Braid does not silently regenerate a supposedly equivalent route and never copies the private signing key.

On a trusted sender:

```sh
braid-trust-export
```

The exporter verifies the route and writes:

```text
~/Downloads/Braid-Trust.braidtrust
```

Copy only that `.braidtrust` file to receiving nodes you intend to enroll. Double-click **Braid Client**. The receiver verifies and imports the bundle, selects its declared embedding model (currently `all-minilm:latest` for the validated route), opens the visualizer, and starts `braid receive` on the detected LAN address and port 8745.

For compatibility, `braid-pair-export` and `braid-pair-import` remain aliases, and legacy `Braid-Pairing.braidpair` bundles can still be imported. Existing `~/.braid/pairing`, `~/.braid/mac-route`, or `~/.braid/route` trust state is migrated into `~/.braid/trust` when possible.

### Terminology

- **Braid Trust** — signer/route enrollment and local authorization bootstrap.
- **Conformance** — whether a route/model representation satisfies required invariants and gates.
- **Alignment** — measured semantic mapping/calibration between representation spaces.

## Receiver storage

Accepted and rejected transport artifacts remain under `~/.braid/inbox`, including receipts and receiver-local state/semantic lineage artifacts emitted by the Braid runtime.

## Validated portability

Physical UAT passed on two Linux hardware classes:

- ASUS Ascent: upgrade/migration path, desktop receiver launch, macOS→Linux accepted/validated/stored Semantic Capsule.
- Lenovo ThinkPad: fresh install, explicit pre-trust UX, Braid Trust enrollment, desktop receiver launch, macOS→Linux accepted/validated/stored Semantic Capsule.

Direct-IP LAN transport is the validated portability gate. Multicast discovery remains access-point/subnet dependent and should be treated separately.
