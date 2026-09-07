# Archangel 1.8.1 - verification

## Release scope

Complete integrated maintenance release. The application already includes the
corrected composer and supported-Mac-runtime discovery. No differential update
files, older repair archives or optional composer layer are in the complete ZIP
or its source ZIP. No previous release is needed for installation.

The 1.8.0 application wheel already included the composer correction; its loose
developer diff and historical repair documents caused the distribution ambiguity.
This release cleans the package and gives it an unambiguous new runtime identity.
It does not claim a new protocol fix. Resilience is not merged.

## Actual checks on these bytes

- 349 Python regression tests and six subtests passed on Linux CPython 3.13.5.
  These include 338 retained cases and 11 release/launcher cases. Models are
  deterministic fixtures; local HTTP/TLS, signatures and file persistence are real.
- 32 corrected-composer browser checks passed using the assets extracted from the
  new wheel; three additional checks reproduce the original a6 behavior and the
  explicit-resume workaround (35 recorded observations total). Tests cover blank
  Share summary/N, Drafts resume, new identities, delta read-only behavior, X and
  Escape, draft replacement/cancellation, failed saves, discard, completed sends,
  accepted/uncertain recipient locks, in-flight dismissal and responsive widths.
- Retained delivery-browser assertions passed with wheel assets, including partial
  delivery and unknown-outcome locks. Its first invocation lacked the wheel import
  path and failed before testing; the corrected invocation explicitly selected the
  extracted wheel. The failure is retained in verification, not counted as a pass.
- 16 exact-installed-wheel lifecycle checks passed through the actual launcher:
  start, local HTTP, channel/thread persistence, duplicate launch, shutdown,
  restart, version-specific snapshot and bundle integrity.
- 13 real predecessor-to-new-release checks passed with temporary profiles: an
  actual 1.8.0 instance remains untouched when 1.8.1 refuses to open its old window;
  after cooperative shutdown, 1.8.1 starts in its own runtime, preserves identity
  and saved delta, and serves the exact integrated composer bytes over local HTTP.
- 16 retained Mac-discovery cases passed with simulated macOS paths on Linux.

## Important limits

Browser checks use Chromium with an offline document and explicit model/API
fixtures. They are not native Safari checks or physical transfers. Installed-wheel
and live upgrade tests deliberately use explicit host-dependency mode, which is
not an isolated installation. No fresh upstream dependency download, physical
Mac/Windows GUI/ACL test, live model inference, optical scan or WAN test is claimed.

The original spending-constraint demo remains predecessor evidence. It does not
certify the new 1.8.1 package or broader channel/transport matrix. Read UAT.md.
The automatic desktop/trust snapshot does not back up the complete semantic store.

The unchanged corrected JavaScript is embedded in the new wheel. The only changed
application files relative to 1.8.0 are __init__.py and static/messenger.html,
which identify 1.8.1. The launcher additionally rejects a running old version and
checks the installed child version before serving. All protocol, receiver, field,
channel and delivery-ledger implementation files are unchanged.

Hashes prove consistency with trusted expected bytes, not publisher authenticity.
The package is not Developer ID notarized or Windows Authenticode signed.

## Evidence and reproduction

See ../verification/ for logs in the complete release. In the source archive use:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH=. python -m pytest -q tests

Browser developer checks need Playwright/Chromium and BeautifulSoup. The original
a6 source is needed only for the optional historical regression reproduction, not
to build or run 1.8.1. Current composer tests execute the new wheel's assets.

From the complete release, `python3 verify_release.py .` performs a read-only
check of the wheel, source and support hashes. It does not run the application.
No live website, Drive object or user profile was altered by this build task.
