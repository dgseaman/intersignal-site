# Braid Archangel 1.9.4 — verification

[Executed test report](TEST_RESULTS.md): 662 passed, 48 passing subtests,
1 skipped, and one host-dependent failure also reproduced in unchanged 1.9.3.
All 28 new publication/handoff tests and all 51 packaged checks passed.

Mac arm64 requires macOS 13 or newer. The app is ad-hoc signed, not notarized.
Native Windows/Linux execution, real two-computer handoffs with installed models,
and historical-browser compatibility remain for hardware testing.

[Classic HTML feature vocabulary](CLASSIC_HTML.md).
Folio's state compares the draft with the latest local immutable export;
it does not check a separately hosted page.
