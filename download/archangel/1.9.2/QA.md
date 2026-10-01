# Braid Archangel 1.9.2 — verification

The complete executed report is TEST_RESULTS.md. The combined collected suite
reported **605 passed, 1 failed, 1 skipped, 3 warnings and 48 passing subtests**.
All 24 new integration cases passed. The actual frozen macOS app passed 16
lifecycle/privacy checks, with 15 separate UI checks and saved screenshots.

Release qualification is incomplete: the unchanged address-change test requires
an unavailable loopback alias, standalone Chromium regression scripts are
blocked by this sandbox, and native Linux/Windows/signing qualification is not
claimed. Raw logs and machine-readable reports are delivered under verification/.
Older evidence remains date-labelled or under docs/history; it is not a new
1.9.2 pass. See packaging/QUALIFY_PLATFORMS.md and UAT.md for remaining work.
