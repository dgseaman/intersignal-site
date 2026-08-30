# Kestrel Run — Braid Queryable State UAT

Purpose: prove that committed Braid Semantic Capsule state can orient a receiver-local completion model across fresh inference calls without relying on chat-session memory.

## Synthetic state

Use information created for this test so pretraining cannot supply the answer:

- Kestrel Run is Project Meridian's deployment protocol.
- Node Finch is authoritative for thermal telemetry.
- Launch requires two consecutive Finch readings below 73.
- Both readings must be independently signed.
- Operator Vale has received signed Finch readings of 68 and 70.

## Control A — no Braid state

Start the receiver completion model in a fresh session and ask:

`Given Vale's Finch readings of 68 and 70, should Project Meridian proceed with Kestrel Run, and why?`

PASS: model states that it lacks the Kestrel/Finch policy context, or otherwise does not correctly infer the test-specific rule.

## Transfer

Create a fresh signed Semantic Capsule on the sender containing the synthetic state and send it to a receiver configured with strict same-model coherence verification (`--semantic-verify-fast-path`). Receiver PASS requires Phase B committed and `semantic_transfer` accepted.

If the signed 384D state falls outside the route's narrow calibration corpus, PASS additionally requires:

- `distribution_gate_policy.mode: diagnostic`;
- `distribution_gate_policy.reason: receiver_verified_exact_space_capsule_vector_coherence`;
- the measured residual/Mahalanobis values retained in the receipt;
- `exact_space_coherence_verified: true` at or above the configured cosine threshold.

A control run without strict coherence must preserve the historical hard OOD rejection, and an intentionally incoherent signed capsule must fail before Phase B with `ERR_CAPSULE_FAST_PATH_COHERENCE`.

The receiver now persists the canonical signed semantic material beside `vector.npy` and `lineage.json` under:

`<output-dir>/semantic/<object_digest>/material.txt`

The material is re-hashed against `semantic_content_sha256` before any later query.

## Query B — fresh inference from committed Braid state

Inspect:

`braid-client state <object_digest> --output-dir <receiver-inbox>`

Query:

`braid-client query <object_digest> "Given the two readings, what operational decision follows and why?" --model <local-completion-model> --output-dir <receiver-inbox>`

PASS requires:

- `phase_b_committed: true`
- `fresh_context_reconstruction: true`
- receiver-local completion model and digest recorded
- answer correctly applies the two-reading, below-73, Finch-authority rule
- query result retained under `<bundle>/queries/*.json`

## Query C — relational paraphrase

Run a second fresh query:

`braid-client query <object_digest> "Why does Vale care that Finch signed both measurements?" --model <local-completion-model> --output-dir <receiver-inbox>`

PASS: response identifies Finch as the authoritative telemetry source and signature provenance as part of the deployment rule, without requiring the original wording.

## Negative integrity test

Modify `material.txt` after commit and issue another query.

PASS: query fails closed with `ERR_CAPSULE_QUERY_MATERIAL_DIGEST`.

## Claim boundary

This UAT demonstrates persisted semantic-state transport plus receiver-side contextual hydration into fresh local inference. It does not claim transfer of transformer hidden activations, KV cache, weights, or native internal model state.
