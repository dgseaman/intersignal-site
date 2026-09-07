# Windows to Mac: physical Shared field test

**September 7, 2026 | Braid Archangel 1.8.1 | Private LAN**

## Result

David Seaman reports a successful physical transfer from Avalon-core (Windows laptop) to his MacBook Air. After the fresh handoff, the receiving Mac answered a differently worded question with the newly supplied **blue group** detail. The supplied screenshot shows **2 indexed items, 2 indexed objects, 384 dimensions**; the prior field screenshot showed one item and one object. These are total field counts, not two new successful handoffs.

**Shared text:** Second Kestrel run should involve blue group only

**Fresh receiver-local question:** Which team or group should the second Kestrel run involve?

**Displayed answer, opening sentence:** The second Kestrel run should involve the blue group, according to the evidence provided.

[Unaltered screenshot](../../../assets/archangel/physical-1.8.1-windows-mac-kestrel.png)

The full screenshot preserves the response's subsequent cosine-score, evidence and authority caveats. Similarity is not proof of truth; this record reports that the new detail was returned, not that every explanation in the generated answer is warranted.

## A useful failure, then a fresh test

An earlier attempt reached the Mac but was explicitly rejected before Phase B. The user supplied that earlier receipt, including:

```text
transport_completed: true
accepted: false
field_indexed: false
finality: rejected
result_summary: REJECTED_BEFORE_PHASE_B
ERR_FUTURE_TIMESTAMP: Timestamp in future beyond clock skew: 1788822158 (Now: 1788822146)
```

The message timestamp was 12 seconds ahead of the receiver's recorded time. That does not identify which machine's clock was correct. A file preserved under rejected storage remained visible in the Inbox but was not admitted into the shared field. After clock synchronization, the user sent a fresh test and supplied the successful field-answer screenshot. The earlier rejected receipt is not the successful attempt's receipt. No security check was relaxed.

[Clock-sync steps](CLOCK_SYNC.md)

## Evidence scope

This is a founder-reported physical Windows-sender / Mac-receiver test, supported by the sequential troubleshooting screenshots, the prior failure receipt, and the later field-answer screenshot. The successful raw receipt, exact physical runtime/model hashes and expanded retrieval evidence were not supplied. The screenshot alone does not expose the sender; the direction is established by the user's accompanying report and earlier Windows/Mac screenshots.

No result is inferred for Windows receiving, restart persistence in this run, Channel Chat, WAN/Managed Relay, native installer certification, or hidden-state/model-weight transfer. The earlier Linux/Mac tests remain distinct. The public 1.8.1 installer and source bytes are unchanged; this is a dated addition to the test record, not a rewritten build report.

## Screenshot integrity

- Dimensions: 1540 x 1488
- SHA-256: `8acea7b1e01bc4b1dc5fe1a88ac7b9dfa926e8b74491b191fafec3886afca3e9`
- No crop, annotation, retouching or text replacement.

[Machine-readable record](PHYSICAL_WINDOWS_MAC_2026-09-07.json)
