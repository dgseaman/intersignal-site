> **Retained a5 baseline QA.** This repack adds a macOS launcher-only fix.
> See `MAC_LAUNCHER_FIX1.md` and `evidence/mac-launcher-fix1/` for the new
> focused evidence; the full a5 suite was not rerun for this packaging change.

# Archangel 1.7.0a5 - verification and release boundaries

## Status

Runnable engineering alpha. Suitable for the next controlled cross-platform test round, not a declaration of stable/native platform certification. The release changes actual code and includes the wheel, launchers, offline-pack tooling, full source, patch, hashes, audit resolution and test evidence. It does not include private rig identities, pre-enrolled accounts or universal third-party dependency binaries.

Application wheel SHA-256:

```text
c828c1c19a2359181ebbbb3dd0bae6dc97b8745b1138702c4a3adcc98e3ec507
```

## Automated regression

**264 tests passed, plus six subtests.** See `evidence/full-final.txt`. The complete suite was executed on Linux, not inferred from the earlier a4 or a3 logs. Tests include cryptographic frames, receipt/finality invariants, replay, semantic indexing and persistence, numerical canonicalization, guarded conflict handling, card/route validation, mutual TLS admission, exact certificate/signing-identity binding, handshake stalls, resource bounds, supported/refused address categories, durable per-recipient outcomes and restart recovery, SQLite closure, receipt reconciliation, private-file failure behavior, offline integrity and profile backup/lock logic.

The old single-sided direct TLS tests are intentionally updated to require approved client certificates; revoked peers now fail before receiving a Braid protocol ACK. The old IPv6-loopback rejection case is replaced by positive support tests. The legacy positional ReceiverConfig order is also covered. These contract changes are documented rather than quietly weakening receipt or semantic assertions.

Embedding/completion test fixtures are deterministic substitutes, not real Ollama model weights. Real loopback TCP/TLS, certificates, signatures, receiver commits, indexing, replay and persisted files are exercised around those fixtures. Public/WAN security certification and actual Tailscale networking are not inferred from loopback tests.

## Installed-wheel and launcher evidence

`evidence/launcher-smoke.json` records **22 successful checks** against the exact wheel hash above, run from outside the source tree with source PYTHONPATH removed. A fresh isolated virtual environment installs the frozen dependency set from a local hash-verified pack, installs the wheel, serves real loopback HTTP, renders the substituted application version, starts with an empty inbox and paused receiver, passes pip dependency checks, refuses unauthenticated shutdown, excludes host site packages, rejects a duplicate profile launch, quits cooperatively and restarts with the same identity/database. It also checks OS lock reacquisition, a consistent desktop/trust snapshot, a cold offline no-pack failure with no package-index attempt, and bundle verification.

There is no hidden `.pth` bridge in that isolated test. Because network package downloads were unavailable in this build environment, the dependency wheels used for this smoke test were **test-only reconstructions of already installed distributions**, with wheel RECORDs and exact local hashes. They are not byte-for-byte upstream PyPI wheels, are not distributed as official dependency packs, and do not establish native macOS/Windows wheel availability. The offline pack generator itself successfully resolved this local cache without an index and verified the resulting pack. The separate physical UAT calls for generating real upstream packs on each target platform.

`evidence/launcher-host-smoke.json` records **nine successful checks** of the explicit alternative: reuse packages from an already active host virtual environment, persist that operator choice, stop/restart, and switch back to an isolated offline runtime. Its path-only `archangel-host-explicit.pth` is a deliberate, visible feature of explicitly selected host mode, not a silent install fallback. The isolated mode has no such file and excludes the host venv from sys.path.

Normal launcher shutdown was executed twice in the isolated lifecycle test and across host-mode transitions. The forced-fallback branch and native Windows signal/ACL behavior are not represented as physically proven. An externally killed process may not clean up; restart recovery is the safety boundary.

## Browser evidence

`evidence/browser/browser.json` records the actual production HTML, CSS and JavaScript running in Chromium. Partial outcomes preserve a successful recipient, reloads retain delivery locks, only the rejected recipient is retried, unknown outcomes remain locked, disabled keyboard sending does not create another attempt, settings/address controls are present, and a 390-pixel settings view has no horizontal overflow. No JavaScript errors were observed in that workflow.

Browser network navigation was administratively unavailable here. The UI was therefore loaded as an offline document, with an explicitly simulated fetch API and an about:blank UUID shim. Fresh documents were created for reload tests. This is **fixture-backed UI behavior, not a live-browser-to-live-server integration run**. The HTTP endpoints and lifecycle were tested separately using real loopback requests in the installed-wheel smoke. Screenshots are labeled fixtures and do not show live user rigs.

## Package checks

`evidence/package-verification.json` records application-wheel ZIP/RECORD integrity, metadata version, compile/shell/JavaScript syntax checks, source patch application against the exact a4 baseline, byte comparison of the patched source, and final release inventory. It also checks that no Python caches, test packages in the wheel, model weights, installed environments or private runtime identities were accidentally bundled. The ZIP preserves executable bits for POSIX launchers.

Setuptools' direct setup invocation emits a deprecation warning; the build, metadata and integrity checks still complete. The historical native packaging inputs retained in the source tree are not newly signed installers. No offline preview pretending to be a real network is substituted for the application.

## Not yet verified / intentionally bounded

Native macOS download/quarantine behavior and Windows GUI launcher, DACL, process-signal and file-lock behavior need execution on those operating systems. Standard CPython 3.10-3.13 is the declared target; this build environment actually ran CPython 3.13.5. Other Python minors are compatibility targets, not a completed interpreter matrix. No Developer ID signature, notarization or Windows Authenticode certificate is included.

Physical two-rig and multi-OS runs with actual Ollama embeddings/completion models, direct Ethernet/APIPA, Tailscale/Headscale, IPv6 ULA interfaces, firewall changes, Managed Relay/WAN and an independent adversarial review remain promotion gates. Scoped IPv6 link-local is deliberately not a portable card endpoint. Receipt/work limits mitigate load without claiming general denial-of-service immunity.

The universal release does not include Python, Ollama, model weights, every platform dependency pack, or optional camera/sensing extras. Initial offline setup requires a matching verified pack or explicit host dependency reuse. Source-local idempotency is not a global exactly-once delivery guarantee; an intentional New handoff, copied profile or restored backup can create another send. Access-controlled local files are not encrypted at rest by this UI. Bundle and pack hashes prove consistency, not publisher authenticity.

## Physical next step

Follow `UAT_ARCHANGEL.md` using the exact wheel above on each rig, refreshed cards in both directions and a complete external profile backup. Record results per OS, Python, architecture, network path and model digest. Do not promote unexecuted rows to a stable-release claim.
