# Archangel 1.7.0a6 Channels - verification and boundaries

## Release status

Runnable engineering alpha built from the supplied a5 Mac-Launcher-Fix1 source. The app, source, patch, release scripts and verification evidence are included. This task does not change the public website/download, Stripe, relay provisioning, or the user's installed rigs.

The same bundle is used on each rig. No private rig identities, signed user channel cards, live chat logs, credentials, model weights or installed runtimes are included. No new third-party Python dependencies were added.

## Executed checks

The final regression log is `evidence/final-regression.txt`. **338 tests and six subtests passed** in the final full regression run, including **74 new a6 cases** and the 264 retained cases. It covers:

- Signed channel descriptor identity and tamper checks; same-name isolation; exact note-content binding.
- Default-deny local permissions, revision-controlled changes, safe pause/re-enable authorization, legacy-peer refusal and archive behavior.
- Real loopback mTLS channel handoff, local receiver commit/indexing, signed-file transfer, channel publisher revocation, durable unknown-delivery locks, persistence and interrupted-work recovery.
- Scoped field filtering before search/reconciliation; actual prompt atom counts, duplicate-source deduplication, conflict siblings, guard fallback, unfit-conflict refusal, history reset and invalid/revoked historical evidence exclusion.
- Ordinary-chat request idempotency, concurrent-turn guards, permission change during generation, no automatic sending after model failure, phrase-match drafts and double-opt-in marked-note rules.
- Real loopback HTTP/static assets/session controls, channel create/query with a local fixture Ollama, QR chunk reconstruction through the channel admission path, offline reel matrix generation, and export transport-hash integrity.
- a5-to-a6 snapshot marker behavior, plus retained transport/crypto/route/replay/FP16/storage/lifecycle/offline/guard tests.

The Mac runtime-discovery suite was rerun: **16 cases passed** using simulated macOS installation locations on Linux. The fixed discovery logic is retained; there is no new physical Mac run in this build task.

The channel UI passed **26 Chromium checks** using the production HTML/CSS/JavaScript and a direct test bridge into the actual service/SQLite. These include creation and policy editing, exact-context receipts, optout/history reset, note review, and 320/390/768/1024/1280-pixel layouts. The retained delivery-UI regressions also passed, including successful-recipient locks, unknown-outcome locks, refresh and mobile settings.

The exact installed wheel was exercised with the real launcher in **explicit host-dependency mode**: **16 checks** of version, empty default state, paused receiving, static assets, default-deny channel creation, persistent chat thread, duplicate launch, cooperative shutdown/restart, identity/channel retention, a6 backup and bundle verification. This is a supported explicitly non-isolated mode; it is not a claim of a fresh isolated dependency download.

Python compilation, POSIX shell syntax, JavaScript syntax, wheel ZIP/RECORD hashes, source-to-wheel contents, support-file hashes and source patch reconstruction are recorded in the package evidence. Native Windows shell/ACL behavior is not inferred from syntax review or Linux testing.

## Model and browser limits

Model tests use deterministic fixture embedding/completion services, not live Ollama weights. Cryptographic frames, TLS sockets, receiver commits, persisted artifacts and HTTP routes are real around those fixtures. The screenshots are interface tests with synthetic source records, not a second on-camera Mac/Linux demonstration.

This environment blocks browser navigation to loopback HTTP (`ERR_BLOCKED_BY_ADMINISTRATOR`). Browser tests therefore execute an offline document with an explicit bridge; actual HTTP calls, transport and installed-launcher lifecycle are tested separately. Safari, Firefox, native phone browsers and browser-to-live-server integration were not executed. No full-model performance or latency benchmark is claimed.

Software QR encoding/matrices/chunk reconstruction were tested. Physical camera/display scans, optical reliability, local browser camera permission behavior and optional camera dependencies remain UAT. Reel display is not a receiver receipt. An exact transport hash is checked before exporting a committed note, in addition to its object identity and signature.

## Scope and claims

Channel Chat is integrated inside Archangel. Unrelated LM Studio windows or Ollama terminal chats are not intercepted. Models still receive ordinary text prompts. Counts describe unique exact source atoms supplied, not verified truth, search candidates, model attention or weights/KV-cache transfer.

Local rules never automatically forward incoming notes, model responses or arbitrary external activity. Automatic mode only handles explicitly marked newly typed user /note messages after channel and per-chat authorization, with rate and durable-attempt limits. Literal phrase matches create local drafts only. This is not an unrestricted autonomous agent or semantic-classifier guarantee.

The retained Advanced all-field/CLI workflows remain explicit operator tools, not automatic channel subscriptions. Unscoped a5 content is not silently relabeled. Formal conflict-resolution authoring and production channel-aware Managed Relay remain outside this release. No relay account or billing configuration was created.

## Required before promotion

Follow `UAT_CHANNELS.md` on physical Mac/Linux/Windows rigs with the same wheel hash. Recheck native installation/quarantine/permissions/lifecycle, real models, refreshed cards, channel subscription isolation, restart persistence, reverse direction, optical camera transfer and actually configured overlay networking. Keep the demonstrated a5 public download in place until the new byte-specific results justify promotion.

Bundle SHA-256 values prove byte consistency, not publisher authenticity. This archive is not a notarized macOS application or Authenticode-signed Windows installer. Local access controls are not encryption at rest or a multi-user isolation boundary.

## Frozen application identity

Wheel: `braid_client-1.7.0a6-py3-none-any.whl`

SHA-256: `4e26a0830d61cb4781db2f40abacc182971c140fa68a5aa2c522a17aa4a389ea`

The outer ZIP has its own SHA-256 sidecar. Source commits, per-file checksums, and package reconstruction results accompany the release. The wheel's 46 application files were compared byte-for-byte with the source.

## Reproduce locally

Extract the included source archive. Install the declared application dependencies and development test tools into a separate development environment; these tools are not an extra end-user runtime requirement. From the source root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. python -m pytest -q tests --disable-warnings
PYTHONPATH=. python tests/browser_channels_a6.py ./browser-results
PYTHONPATH=. python tests/browser_archangel.py ./browser-retained
python tests/installed_channels_smoke.py /path/to/extracted/release ./installed-evidence
```

The browser scripts require Playwright and Chromium. The installed smoke uses fresh temporary profiles and explicit host-dependency mode, not a user's existing profile. It never requires a real model. Check the distributed bundle without executing it using:

```sh
python verify_release.py . --report wheel-check.json
```

The recorded Mac discovery tests also accompany the evidence. They simulate macOS install prefixes on Linux; their names do not establish physical platform coverage.
