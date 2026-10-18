# Braid Archangel 1.9.4 — verification

[Executed test report](TEST_RESULTS.md): 662 passed, 48 passing subtests,
1 skipped, and one host-dependent failure also reproduced in unchanged 1.9.3.
All 28 new publication/handoff tests and all 51 packaged checks passed.

Mac arm64 requires macOS 13 or newer. The app is ad-hoc signed, not notarized.
Subsequent user-reported physical Braid 1.9.4 testing confirmed Windows
Nemotron Bolt in-chat inference, peer connectivity, and messaging on Orpheus,
plus Linux receipt, completed transport, receiver response, handoff acceptance,
and Channel indexing. See [the physical-test scope](PHYSICAL_WINDOWS_LINUX.md).
The report does not qualify every OS/hardware configuration, every network
direction, end-to-end note use in a generated answer, or a later release.
Historical-browser compatibility and the other unrecorded cases still need
verification.

[Classic HTML feature vocabulary](CLASSIC_HTML.md).
Folio's state compares the draft with the latest local immutable export;
it does not check a separately hosted page.
