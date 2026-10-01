# Braid Archangel 1.9.3 — verification

The executed report is [TEST_RESULTS.md](TEST_RESULTS.md). The full suite recorded
634 passed, 1 failed, 1 skipped, and 48 passing subtests. All 22 new
studio/scanner/state tests passed. The final extracted Mac app passed 16 checks,
the frozen CLI passed 6, and the actual POSIX launcher passed 15 on this Mac.

The unchanged failure needs the unavailable 127.0.0.2 loopback alias and also
fails in the untouched 1.9.2 source on this host. Native Windows/Linux execution
and fresh Finder/Gatekeeper acceptance remain unverified. Mac arm64 requires
macOS 13 or newer; the app is ad-hoc signed, not Developer ID notarized.

Folio's published-state banner compares the current public content with the
latest immutable local export. It does not check a separately hosted page.
