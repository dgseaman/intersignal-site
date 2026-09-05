# Archangel physical acceptance checklist

Use harmless test context, a separate backup and identical application wheel hashes. This file is a test plan, not a record of tests already executed.

## Matrix

Record OS version, CPU architecture, Python minor/build, Ollama version, embedding/model digest, application wheel SHA-256, address family/path, result and exact error. Run macOS -> Linux, Windows -> Linux, Linux -> Windows, and macOS -> macOS. Add overlay/private IPv6/direct-cable rows only where the actual network is configured. Managed Relay is a separate retained-path UAT, not inferred from LAN success.

## First install and a4 upgrade

Start a fresh profile; expect empty Inbox and receiving paused. Verify no global Python packages are changed. Stop with Settings > Quit; relaunch and confirm the profile lock is reacquired and session file is cleaned. Launch twice: only one profile instance may run.

Stop a4, make a complete external profile backup, then launch Archangel against its profile. Record the printed desktop/trust backup path. Verify names, identity fingerprints, route references and historical messages persist. Save/approve fresh cards in both directions. Existing a4 contacts do not imply permitted legacy mTLS downgrade.

On Windows 3.10-3.13, inspect the profile/file ACLs for the current account and SYSTEM, check clean shutdown/database rename, and confirm no missing-fchmod error. On macOS, test downloaded ZIP quarantine, preserved script mode, per-item approval and manual supported-Python launch. Do not infer success from Linux mocks.

## Delivery and semantics

Send one reviewed exact test fact, such as "Project Cobalt's launch color is amber." Require receiver-owned acceptance and independently confirmed indexing, not just reachability. Ask a fresh local question that needs the fact and inspect its retrieved evidence. Restart the receiver and repeat retrieval to verify persistence.

Send conflicting exact facts (73 and 75) with provenance; require both to survive reconciliation and the guarded answer to acknowledge unresolved conflict. Exercise the retained a3 field proof with the current wheel on each machine. Do not claim hidden-state transfer or universal latent coordinates.

For two recipients, create one accepted delivery and one explicit refusal. Retry the same handoff: the accepted recipient's core receive count must not increase. Refresh/reopen the draft and restart the sender; the same per-recipient outcome must remain. An uncertain/missing receipt must remain locked until the operator inspects receiver state. An intentional New handoff is not a resolution protocol.

Interrupt one send after submission. On restart it must be unknown, not automatically transmitted. For a prior successful handoff, repeat the API identity: return the stored outcome, not new signed frame bytes. Do not manipulate real sensitive payloads during these checks.

## Network changes and admission

Select another actually assigned private/overlay endpoint through Update address. Keys, route and history must remain unchanged. Import the revised signed card on the peer and reconnect. Try an older card: it must fail as stale. Rotate a certificate/route in a fixture: it must not be accepted as address-only maintenance.

Switch away from the saved interface and relaunch. Expect an actionable network warning, not wildcard/public fallback. Test Windows/macOS/Linux address discovery independently. IPv6 ULA and loopback are supported; scoped link-local remains outside the portable card contract.

Remove an approved rig and confirm its next direct connection is denied before frame parsing. Confirm an unapproved or legacy no-client-cert socket cannot reach the Braid parser. Close all test sockets afterward. Multi-host firewall and actual overlay reachability must be tested; numeric policy support does not configure them.

## Offline

On a connected equivalent OS/architecture/Python rig, generate a dependency pack from upstream wheels. Copy it and the release to the offline target. Disable outbound package-index access; install via --offline --wheelhouse. Verify pip check, actual installed application version and a fresh isolated sys.path. Provision Ollama/model files separately. Restart without the pack once the runtime is installed.

Modify a copied wheel byte, try a mismatched target, and introduce an unlisted wheel: each pack must be rejected. A cold offline launch with no pack must fail clearly without an index attempt. Explicit host-environment mode should state that it is not isolated; --isolated-runtime must restore isolation.

## Promotion gate

A stable/publicly certified claim requires these physical rows, matching wheel hashes, reproducible logs, a native packaging/signing decision and an independent security review. Archive the evidence; do not replace unknown or unexecuted rows with green checks.
