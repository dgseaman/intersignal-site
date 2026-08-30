# Braid v1.6.0rc2 — Kestrel WAN situational-continuity proof

**Date:** August 30, 2026  
**Status:** Core A → B enrichment proof passed

## Plain-language result

A remote receiving LLM was tested before it had the Kestrel scenario. It confidently reached the wrong decision. A Mac then sent a signed Braid Semantic Capsule through the public Braid relay to an independent Linux node. After the receiving Braid instance verified and committed that state, the same local model answered two new questions correctly in fresh inference calls.

The result demonstrates that accepted situational state can cross a machine and network boundary, persist on the receiver, and improve later reasoning without depending on a continuing chat session.

## Test scenario

The scenario was invented for the test so it could not have appeared in model training data:

- Kestrel Run is Project Meridian's deployment protocol.
- Node Finch is the authoritative source for thermal telemetry.
- Project Meridian may proceed only after two consecutive Finch readings below 73.
- Both readings must be independently signed by Finch.
- Operator Vale received signed readings of 68 and 70.

## Before Braid

The receiver was asked whether Project Meridian should proceed. It invented a different interpretation of the threshold and answered **do not proceed**.

## Transfer path

```text
Mac Node A
  → signed Semantic Capsule
  → Braid Managed Relay / Jump Kit
  → TLS 1.3
  → remote Linux Node B
  → receiver-owned Phase B commit
  → persisted material + 384D vector + lineage
```

## After Braid

In a fresh query, the receiver correctly answered that Project Meridian **may proceed**, because 68 and 70 are both below 73, the two-reading condition is satisfied, and both readings were independently signed by Finch.

A second fresh query correctly explained why Finch's signatures matter to provenance and the deployment rule.

Both query artifacts recorded:

```json
{
  "fresh_context_reconstruction": true,
  "phase_b_committed": true
}
```

## Evidence identity

- Braid receiver version: `1.6.0rc2`
- Completion model: `qwen2.5:1.5b-instruct`
- Embedding model: `all-minilm:v2`
- Object digest: `5f81e8a4578f4b766644e95c08a26f8e22e82b6ff03bcad87c71b2efd49e08cb`
- Transport: relay-backed WAN over `TLSv1.3`
- Receiver bundle: `material.txt`, `vector.npy`, `lineage.json`, and two retained query artifacts

## What this proves

- A second AI node can gain usable situational orientation it did not previously possess.
- Accepted state can be queried in multiple fresh local inference calls.
- The 384-dimensional representation remains part of the committed semantic bundle.
- Transport does not create acceptance; the receiving Braid node owns finality.
- The receiver's local model performs the reasoning.

## What this does not claim

This test does not claim transfer of transformer hidden activations, KV cache, model weights, consciousness, or native internal model state. It demonstrates authenticated semantic-state transport plus receiver-side contextual reconstruction.

## Release artifacts

- `braid_client-1.6.0rc2-py3-none-any.whl`
  - SHA-256: `f93473c00fd74ba8deb18402f8e27f0f03a73d4be108edfc6c359a89c993744a`
- `intersignal-braid-light-client-v1.6.0rc2-source-candidate.tar.gz`
  - SHA-256: `0bf31ed3888069ff3e3f6685ad5ea794d1a16b03183c04b4c44d7892e7681645`

## Formal closure note

The core A-to-B orientation result passed. An additional explicit authority-recovery query and a separate material-tamper negative remain part of the broader release-candidate closure process.
