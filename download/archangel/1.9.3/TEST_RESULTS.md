Braid Archangel 1.9.3 — executed verification (October 1, 2026)

Delivered features: dual-view Redaction & Selective Inclusion Studio; immutable
originals, click/keyboard inclusion toggles, public excerpt editing; local
advisory highlights; prominent draft/changes/approval/latest-export indicators.
The latest export comparison does not verify a separately hosted live page.
Existing approval invalidation, optimistic save conflicts, exact-preview
approval binding, capsule exclusion and immutable exported bytes are preserved.

Current full suite: 634 passed, 1 failed, 1 skipped; 48 passing subtests.
All 22 new studio/scanner/state tests pass. The sole current failure is unchanged:
test_address_change_keeps_identity_route_and_history requires 127.0.0.2 assigned
to this Mac. The interface alias is absent. The same test fails in the untouched
1.9.2 source on this host. No transport code/assertion was weakened or skipped.
Three unchanged numerical warnings occur in synthetic calibration tests.
An earlier full run had one HTTP error-body connection reset; the isolated
recheck and current full run pass that test. Earlier logs are retained.

Mac build: self-contained Apple silicon Braid.app, windowed normal launcher,
plus its frozen CLI. No host Python is needed for the native application.
The runtime retains camera/Bluetooth modules and shared-library compaction.
Actual frozen HTTP/lifecycle validation covers first/duplicate launch, private
Folio capability, public approval/export boundary, immutable bytes, handoff,
shutdown/restart, persistence, rotated tokens, and stop. Final extracted package
checks and CLI diagnostics are recorded separately with the release artifacts.

Browser verification: Codex in-app browser against the actual frozen app on a
separate disposable profile. Imported source warnings, click and keyboard
inclusion, redaction, original preservation, clean public preview, Compose,
explicit approval, export, edit invalidation and reapproval/re-export states
were checked. Desktop source is left and public preview right. Layout fits
1600, 1100, 800 and 390 pixels; no browser warnings/errors were recorded.
Standalone headless Chromium cannot start in this sandbox (Mach-port bootstrap
permission denied). Its blocked run is not counted as a passing browser test.
The in-app browser did not provide a Blob download-event path within its wait;
the export visibly completed and its archive is checked through the local API.

Linux/Windows: current Python launchers and same 1.9.3 wheel included. Pinned
binary dependency wheels downloaded successfully for x86_64 Windows and Linux
on each supported CPython 3.10, 3.11, 3.12 and 3.13 (8 combinations, 10 wheels
each). Script syntax, manifest/checksums and actual POSIX launcher on this Mac
are checked. Native Linux/Windows execution is not possible here: neither OS,
a Windows runner, nor a container/virtual machine runtime is available.
First setup on those platforms still requires internet unless an offline pack
is prepared. Python must include venv/pip; free-threaded Python is unsupported.

Limits: Mac arm64 only, macOS 13 or newer; ad-hoc signed, not Developer ID
notarized. Native Windows/Linux binaries, Intel Mac runtime, fresh Finder/
Gatekeeper acceptance, physical two-rig/model/camera/Bluetooth and production
WAN/hosting deployment are not claimed. No live website or service was changed.
The finalized combined ZIP must be below 100,000,000 bytes. Package manifests,
checksums, source ZIP and final archive checks identify the delivered bytes.

Final delivered files

Combined ZIP: 79,952,058 bytes (79.95 MB).
SHA-256: c75998db99090d48d92a6993b4fb1f92d7ff69bafcb6c8769e58354e5c0e6870
Final extracted native app: 16 checks passed.
Final frozen CLI: 6 checks passed, including synthetic optical decode.
Final actual POSIX launcher: 15 checks passed, using isolated setup.
Archive validation: 1147 file checksums and 485 contained links checked.
Mac signature, app identity, UI/source/wheel consistency and launcher modes pass.
Separate Windows/Linux launcher ZIPs each occupy about 1.3 MB. They contain the
same 1.9.3 wheel and source, with platform-specific setup instructions. The
source ZIP contains the updated local project and its full tests/build recipes.

Windows: double-click Start Braid.cmd after extracting.
Linux: run sh "Start Braid.sh" from the extracted directory. Executable bits
are preserved; file-manager double-click handling is system-dependent.
Mac: copy Braid.app to Applications and open it; ordinary launch is windowed.
