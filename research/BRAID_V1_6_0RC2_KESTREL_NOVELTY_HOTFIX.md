# Braid v1.6.0rc2 — Kestrel exact-space novelty gate correction

## Physical finding

The first WAN Kestrel capsule reached the DigitalOcean relay and Node B over TLS 1.3,
validated cryptographically, and was stored, but Phase A rejected it:

`ERR_SUBSPACE: Residual 0.8863 > ceiling 0.4672`

## Root cause

The existing same-space route reused a 64-rank PCA/OOD gate fitted to the route
conformance corpus. Kestrel was intentionally novel situational material, so its valid
MiniLM embedding lay outside that narrow calibration distribution. The gate therefore
conflated semantic novelty with invalid route geometry.

## Correction

Route-distribution anomaly gates remain authoritative for:

- heterogeneous calibrated routes;
- opaque vectors without a signed Semantic Capsule;
- exact-space capsule receivers that do not enable strict local coherence verification.

For a signed, route-bound Semantic Capsule on a sealed exact-space identity map, the
receiver may retain subspace and Mahalanobis measurements as evidence only when strict
receiver-local capsule/vector coherence verification is enabled. The coherence check
runs before Phase B. A mismatched capsule/vector still fails closed.

## Executed evidence

- Python compileall: PASS
- Core conformance and OOD regression: PASS
- Heterogeneous route regression: PASS
- Ollama/Legend regression: PASS
- Legacy automated receiver regression: PASS
- Narrow-route Kestrel novelty acceptance test: PASS
- Capsule/vector mismatch fail-closed test: PASS
- Complete split regression: 130/130 PASS
- Wheel build: PASS
- Clean wheel install: version 1.6.0rc2, doctor ready=true

## Artifacts

- `braid_client-1.6.0rc2-py3-none-any.whl`
  - SHA-256: `f93473c00fd74ba8deb18402f8e27f0f03a73d4be108edfc6c359a89c993744a`
- `intersignal-braid-light-client-v1.6.0rc2-source-candidate.tar.gz`
  - SHA-256: `0bf31ed3888069ff3e3f6685ad5ea794d1a16b03183c04b4c44d7892e7681645`

## Subsequent physical result

A fresh Kestrel capsule then committed successfully on the remote Linux receiver. The
same local completion model moved from an incorrect pre-transfer decision to the correct
post-transfer decision in fresh inference calls. The committed object retained explicit
semantic material, a 384D receiver state, lineage, and separate query artifacts.

The core A-to-B situational-orientation proof passed. A separate tamper-negative and an
additional explicit authority-recovery query remain before final release promotion.

## Claim boundary

This correction and physical run demonstrate authenticated semantic-state transport,
receiver-owned commitment, and fresh receiver-side contextual reconstruction. They do
not claim transfer of transformer hidden activations, KV cache, weights, or native
internal model state.
