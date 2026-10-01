# Final combined-package verification

Braid 1.9.2 combined package — final packaging verification
ZIP: Braid-1.9.2.zip (79879548 bytes)
SHA256: 1c4da95bf4d59db467708d2d59789cd5dcd200448f9d74086a04d1cbf08c2aec
Source SHA256: 5aa9582a50d69a0e55c8b1c00982fb4af4a430d47f4a6f68cc22af30c726a797

The roughly 1 MB 1.9.1 package was a Python launcher/wheel bundle and installed
dependencies at setup. The first 1.9.2 native Mac build bundled Python and
libraries twice, once for the GUI and once for the CLI. Sharing 126 byte-identical
immutable files inside the .app reduces the combined ZIP from 141.5 MB to 79.9 MB.
No runtime, module or feature was removed. The app was re-signed ad-hoc and its
signature and relative links verified after extraction.

Full collected suite: 612 passed, 1 failed, 1 skipped, 3 warnings,
48 subtests passed in 193.95 seconds. The one failure is unchanged from baseline:
test_address_change_keeps_identity_route_and_history needs an unassigned 127.0.0.2
loopback alias. No existing test assertions were weakened. Seven new packaging
tests passed. Release qualification remains incomplete.

Extracted compact Mac app: 16 checks passed, including /folio,
review/approval, privacy sentinel exclusion, handoff, persistence and restart.
Frozen CLI: 6 checks passed, including synthetic sign/receive,
OpenCV PNG decoding through the shared libraries, and clean shutdown. No camera
or Bluetooth hardware was accessed. No external Python discovery path was used.

Default isolated POSIX launcher: 15 checks passed on the Mac host,
with pinned dependencies actually installed into a fresh private runtime.
Windows x64 and Linux x86_64 CPython 3.12: all 10 pinned dependency wheels
successfully downloaded for each target. This verifies availability, not execution.
Native Windows/Linux execution remains pending on those hosts.

Archive integrity: 1133 file checksums passed; all 126 shared payload hashes
and relative contained links passed. Mac discovery: 16 passed using a physical
/private/tmp fixture. An earlier /var alias fixture caused one cwd string mismatch;
no assertions were changed to resolve it.

The ZIP contains Braid.app for macOS arm64, Start Braid.cmd for Windows and
Start Braid.sh for Linux. Windows/Linux use the 1.9.1-style private-runtime
launchers and require CPython 3.10–3.13. Folio is integrated in every entry point.
Old native/source artifacts were retained. The homepage no longer shows test counts.


---

# Earlier native-build evidence (preserved)

# Braid Archangel 1.9.2 — exact executed results

Prepared 2026-10-01. Runs span 2026-09-30 and 2026-10-01 on macOS 15.5 arm64,
CPython 3.12.14. This is a built local release with incomplete qualification.
It is not an all-green or notarized production release. No production service,
live Intersignal website, user profile, real membership, or real rig pairing
was modified. All startup/upgrade/migration fixtures used disposable profiles.

## Complete collected suites

Command, from the delivered source root, with the recorded modern test runtime:

```sh
python -m pytest -q --junitxml=full-tests-final.xml
```

| Suite | Passed | Failed | Skipped | Total cases |
| --- | ---: | ---: | ---: | ---: |
| Existing Braid | 464 | 1 | 1 | 466 |
| Existing Folio 0.3.0 | 117 | 0 | 0 | 117 |
| New Archangel/Folio integration | 24 | 0 | 0 | 24 |
| Combined | **605** | **1** | **1** | **607** |

Pytest's exact summary: **1 failed, 605 passed, 1 skipped, 3 warnings,
48 subtests passed in 192.62s**. Subtests are reported separately and are not
added to the case count. Raw output and JUnit XML accompany this release under
`verification/full-tests-final.log` and `verification/full-tests-final.xml`.

The failure is
`tests/test_v1_7_0a5_archangel.py::test_address_change_keeps_identity_route_and_history`.
It calls `update_address('127.0.0.2')`; macOS has only `127.0.0.1` assigned here.
The existing production check rejects unassigned interface addresses. The same
failure occurred in the untouched input baseline. Privileged interface
configuration is unavailable in this sandbox. Neither the address check nor
this test was bypassed, relaxed, mocked into a pass, or newly skipped.
Provision the test-only alias on an authorized macOS qualification host and
rerun the unchanged test; instructions are in packaging/QUALIFY_PLATFORMS.md.

The existing skip is
`tests/test_v1_7_0a5_archangel.py::test_many_database_operations_do_not_hold_descriptors`,
reason **Linux FD counter**. The three warnings are NumPy determinant
**divide by zero**, **overflow**, and **invalid value** in the existing
heterogeneous calibration fixture.

Untouched source baselines were also run: Braid **463 passed, 2 failed,
1 skipped, 3 warnings, 6 subtests passed in 183.88s**; Folio **117 passed,
42 subtests passed**. Besides the same address failure, Braid's baseline
failed a Mac sibling-launcher check because its input ZIP lost executable
permissions. Those source launcher permissions were restored. Historical
assertions were retained; literal version expectations changed to 1.9.2.
Folio's cross-test fixture import was namespaced after embedding its tests.
Its browser harness now discovers Chromium portably instead of assuming
`/usr/bin/chromium`; its browser assertions are unchanged.
Smoke reports were corrected to record their actual host instead of retaining
an inherited Linux label. No assertion was weakened for a green result.

## Integration coverage

The 24 new cases in `tests/test_archangel_folio192.py` cover:

- One server and one port; `/folio`, assets and API routing; independent Folio
  capability; Braid CSRF isolation; same-origin/Host validation and route denial.
- Direct note and completed-conversation handoff; rejected
  invalid handoffs; unapproved private draft creation and durable storage.
- Explicit confirmation, approval invalidation, immutable reviewed editions,
  private-original and excluded-block sentinel exclusion from previews, exports,
  publication registration, Braid state and its desktop database.
- Allowlisted internal views, identity/readiness/publication operations without
  an HTTP connection, generic send operation or trust approval.
- Return to Braid; scheduler shutdown, ownership release, persistence and
  session-token rotation on restart.
- Legacy database backup and byte-preserved archives/preferences/identity;
  original retention, no destination overwrite, busy-profile lock rejection;
  legacy Broadcast never auto-approves; site rebuilding requires review history.
- macOS/Linux/XDG/Windows legacy locations, spaces in paths, and Windows DACL
  and byte-range lock branches through synthetic platform adapters.
- A real local synthetic rendezvous with deliberate request, acceptance,
  each rig-card exchange, fingerprint approval, publication Channel grant and
  rejection of unrelated authority. No public page itself creates authority.

## Additional executed checks

| Check | Exact result | Evidence / method |
| --- | --- | --- |
| Actual frozen macOS Braid app | **16 checks passed** | `verification/native/native-results.json`; native executable, no Python on PATH, real local HTTP and lifecycle, `--http-only` |
| Actual native UI | **15 recorded checks passed** | `verification/browser/results.json` and screenshots; Codex in-app browser against frozen app |
| Installed developer wheel | **22 checks passed** | `verification/installed/installed-smoke.json`; actual compatibility launcher, host dependencies, loopback, duplicate launch and restart |
| Installed operator CLI | **12 checks passed** | `verification/operator/operator-smoke.json`; disposable local state; no server deployment |
| Real rc1 → 1.9.2 launcher upgrade | **18 checks passed** | `verification/upgrade-rc1/upgrade.json`; actual predecessor wheel, paused synthetic activation |
| Real 1.8.1 → 1.9.2 launcher upgrade | **15 checks passed** | `verification/upgrade-181/upgrade-check.json`; actual predecessor, retained signing identity and saved draft |
| Folio bridge against untouched Braid 1.9.1 | **15 checks passed** | `verification/folio-braid191.json`; original Braid service, synthetic saved notes/turns, no field writes |
| Standalone Folio compatibility launcher | **12 checks passed** | `verification/folio-launcher.json`; real POSIX process lifecycle and Mac/Linux launcher discovery |
| Actual 1.9.0rc1 relay compatibility | **3 passed in 4.84s** | `verification/compatibility-rc1.log` and XML; predecessor wheel supplied explicitly |
| Mac command runtime discovery | **16 passed in 2.32s** | `verification/mac-discovery-final.log` and XML; unchanged cases with `TMPDIR=/private/tmp` |
| JavaScript and Python syntax | **passed** | JavaScript syntax check on Folio app.js and Braid channels.js; compileall on modules and entry points |
| Native console companion | **passed** | Version 1.9.2; successful environment command in `verification/native/cli-environment.json` |
| Native signature integrity | **passed** | `codesign --verify --deep --strict`; ad-hoc signature, not Developer ID notarization |

Native checks verify startup of both surfaces from one executable, reuse on a
second launch, frozen review-history schema, private-preview filtering,
unapproved-export refusal, confirmed approval, sentinel-free immutable export,
approval invalidation, absence of private Folio originals from Braid state,
direct unapproved handoff, cooperative quit, persistence, token rotation and
native stop. Browser checks exercise the sidebar, no connection setup, direct
note action, review rendering, disabled export before approval, inherited
Channel picker, Review queue only, Back to Braid, no observed console errors,
and 390/800/1280px layouts. Screenshots contain only synthetic fixture content.

The Mac discovery fixture initially failed one cwd assertion because `/var`
and `/private/var` refer to the same temp directory on this host. The recorded
final run uses canonical `TMPDIR=/private/tmp`; the test itself is unchanged.

## Blocked and unclaimed qualification

The existing standalone Playwright scripts `browser_archangel.py`,
`browser_channels_a6.py`, `browser_composer.py`, `browser_polish191.py` and
`browser_wan19.py`, plus Folio's `folio_tests/browser_check.py`, were each
attempted. All exited before their browser
assertions because this sandbox denies Chromium's Mach-port bootstrap
(`bootstrap_check_in ... Permission denied (1100)`). The new native harness's
Chromium mode hit the same restriction. Logs are included under
`verification/browser-legacy-attempts/`; these are **blocked runs**, not passes.
The separate native UI inspection does not stand in for every old browser
assertion. Rerun those scripts on a host where Chromium subprocesses can launch.

Only the macOS arm64 native application was built and run. Linux-compatible
paths/entry points and Windows-compatible paths, DACL/lock adapters and build
branches are source/code-path coverage, not native Linux or Windows execution.
Native Finder/Gatekeeper acceptance, Developer ID signing/notarization, native
Windows/Linux packaging and restart, physical camera/Bluetooth hardware,
real model inference and physical two-rig/WAN soak qualification are unclaimed.
Native target build and qualification instructions are provided in source.

These remaining limitations must be resolved before calling the release fully
qualified. No failure, skipped test or blocked browser run is reported as green.
