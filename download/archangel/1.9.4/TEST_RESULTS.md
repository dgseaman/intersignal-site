Braid Archangel 1.9.4 — final test build
Folio 0.4.0

Combined Mac + Windows/Linux launcher ZIP: 80,066,290 bytes (80.07 MB).
SHA-256: a5991c06eb7d527cbe6d7fb25eaee49626ef1360adb299050790e55a1ddd2044

Full source suite: 662 passed, 48 passing subtests, 1 skipped, 1 host-dependent
failure, 3 warnings. All 28 new publication/handoff tests pass. The final layout
and release identity recheck passed all 41 tests.

Remaining failure: test_address_change_keeps_identity_route_and_history needs
127.0.0.2 assigned to an interface. The same failure was reproduced against
unchanged released 1.9.3. Braid correctly refuses an unassigned local address.

Final extracted Mac app: 16 launch/lifecycle/privacy checks passed.
New frozen 1.9.4 features: 14 checks passed, including demo, rich
formatting, local PNG export, Classic HTML, related links, license, re-approval,
immutable archives and the queued handoff presentation.
Frozen command-line companion: 6 checks passed, including synthetic
signatures/receiver and raster QR decoding. No camera/Bluetooth hardware access.
Actual packaged POSIX launcher: 15 checks passed, including isolated
pinned runtime setup, spaces in paths, duplicate launch, restart and shutdown.
Total packaged launch/feature checks: 51.

Archive: CRC pass, 1154 file checksums, 485 contained links.
Ad-hoc Mac signature and application identity verified after extraction.
Runtime wheel and both frozen surfaces contain exactly the current UI bytes.
Windows/Linux package integrity verifiers passed; each uses the same wheel hash.
Eight x86_64 dependency packs (Python 3.10–3.13 on each OS) were reverified
against current pins, SHA-256, wheel compatibility tags and ZIP CRC. No dependency
versions changed from 1.9.3. Each separate launcher package is about 1.3 MB.

Browser: isolated fictional demo, source/public selection, formatting, layout,
related-edition selection, explicit approval/export, local image attachment,
390px phone and Print reading preview, actual exported images and four-step
handoff display checked. No browser errors were reported in those flows.
Classic phone output has no page-wide horizontal overflow for the sample.
Synthetic UI receipts are clearly labeled; they do not claim real network sends.
Actual signed mutual-TLS loopback handoffs use local embedding test fixtures and
verify receiver/publisher permissions. They are not real-model/physical-rig tests.

Limitations for your testing:
- Mac is Apple silicon macOS 13+, self-contained and windowed. It is ad-hoc
  signed, not notarized; no Developer ID signing identity exists on this host.
- Windows/Linux require standard CPython 3.10–3.13 with pip/venv. Their first
  isolated setup needs internet or a prepared offline dependency pack. Native
  Windows/Linux execution remains untested on this Mac build host.
- Test a real two-computer handoff and installed Ollama models on your rigs.
- Classic uses a conservative pre-2010 feature vocabulary; historical browsers
  and formal HTML4 DTD conformance are not certified by this build.
- Browser automation blocks file: URLs. The extracted publication pages passed
  via a loopback HTTP server; directly opening index.html remains for your test.
- Print reading preview does not certify browser-specific paper pagination.

Quit a previous Braid version before testing the new package on its profile.
No production profile, public website, relay deployment or X campaign changed.
Start with Try a sample conversation, then test the Folio layouts and export.
