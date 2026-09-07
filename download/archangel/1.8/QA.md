# Archangel 1.8.0 - verification and release boundaries

Date: September 7, 2026.

## What changed

This is a public-line maintenance consolidation: 1.7.0a6+composer1 becomes 1.8.0. The existing corrected composer, Channels and Mac launcher-discovery fix are retained. No a7 Resilience merge, additional dependency, model download policy, backend schema migration or trust-policy change.

The new wheel contains 46 application files. 44 are byte-for-byte identical to the Composer Fix 1 wheel. The only two changed application files are `__init__.py` (version) and `static/messenger.html` (visible version badge). In particular, the corrected JavaScript and CSS, receiver/transport/channel/field implementations and delivery ledger are unchanged. The source launcher, project metadata, read-only verifier and version assertions are updated consistently.

## Executed on the 1.8 source and wheel

- **338 Python tests and six subtests passed** on Linux CPython 3.13.5 in 126.36 seconds. The suite exercises actual local HTTP/TLS, signatures, receiver commits, persistence and channel policies around deterministic model fixtures.
- **32 corrected-composer Chromium checks passed**, with three separate original-a6 reproduction/workaround observations (35 records total). Checks include blank Share summary/N, explicit Drafts resume, delta immutability, new IDs, X/Escape, one-slot replacement confirmation, save failures, discard preserving history, successful-send cleanup, accepted/uncertain recipient locks, in-flight behavior and 320-1280px layouts.
- Retained delivery-browser assertions passed with the already-corrected explicit Drafts resume path; no invented numeric count is assigned.
- **16 exact-installed-wheel launcher/HTTP/lifecycle checks passed**, using an explicitly selected host-dependency runtime outside the source tree, including duplicate-launch protection, cooperative stop/restart, persistent identity/channel/thread and the version-specific backup marker.
- **16 retained Mac interpreter-discovery tests passed**, using simulated macOS locations on Linux. These do not establish a physical Mac run.
- All 52 hashed wheel RECORD entries passed; all application bytes match the source; bundle support hashes, ZIP CRCs and final extraction are checked separately.

## Limits

The original Safari failure to dismiss was not reproduced in native Safari here. Browser tests use production assets in an offline Chromium document with explicit API fixtures and a UUID shim because live loopback browser navigation was blocked in the earlier workflow. Simulated browser sends are not a second physical handoff. Real HTTP/TLS and installed-launcher lifecycle are tested separately.

No fresh isolated upstream dependency download was performed; the installed test explicitly chose supported but non-isolated host reuse. Normal isolated installation and the frozen dependency set are unchanged. No native Windows GUI/ACL test, physical QR/camera run, WAN test, actual local model inference, public download or new 1.8 cross-OS run is claimed.

The September 7 spending screenshot shows the predecessor a6-line field answer returning 500. Its exact package/version and raw query JSON are not displayed. The output omitted `second server` and used generic caution; it does not establish a real conflict, spending enforcement, universal accuracy or an unchanged generation branch. That original result is preserved separately, not credited as a 1.8 physical run.

The earlier failed delta lacked its detailed error; this composer correction does not diagnose that separate preparation failure. Creating a new message must not be used to bypass an uncertain handoff's lock.

The application is not a signed/notarized native installer. A public 1.8 version number is not a claim of complete platform certification. The automatic upgrade snapshot covers desktop/trust material, not all semantic files. Use a complete external backup. Direct, signed-file, QR and channel scope remain as documented; signed files/QR are not encrypted solely because direct TLS is used. Managed Relay remains forthcoming and separately provisioned.

## Reproduce

From source with the declared dependencies and test tools installed:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. python -m pytest -q tests --disable-warnings
python tests/browser_composer_fix.py /path/to/original-a6-source ./composer-evidence
python tests/browser_archangel.py ./retained-browser
python tests/installed_channels_smoke.py /path/to/complete-1.8-release ./installed-evidence
```

The browser scripts require Playwright/Chromium. They use temporary fixtures, not a real user's profile. The retained Mac-discovery test is included in evidence/test_mac_launcher.py. The ordinary archive can be checked without starting Braid using `python3 verify_release.py . --report package-check.json`.

## Exact wheel

`braid_client-1.8.0-py3-none-any.whl`

SHA-256: `1adb6e3c90c9dcb50d9bf2de53c8576b07b4b8b7671b991bfe2ef363aa95a5db`

Hashes establish consistency with trusted expected bytes, not publisher identity if the bytes and manifest are both replaced. Historical native packaging scripts remain source inputs, not newly signed native packages.
