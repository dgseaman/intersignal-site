# Native Braid 1.6 turnkey semantic-transfer acceptance criteria

This is the product boundary for the supported founding-member build. It is intentionally general and is not a Kestrel-specific demo.

## User outcome

A user with two approved Braid nodes can provide their own bounded text-based situational state on Node A, send it to Node B over LAN or Managed Relay, and ask fresh questions on Node B that are answered from committed receiver-owned state.

## Required workflow

1. **Paste or select text**
   - Accept user-authored facts, rules, observations, constraints, summaries, or project state.
   - Support direct paste and UTF-8 text-file selection.
   - Clearly display the current inline Semantic Capsule limit of 6,000 UTF-8 bytes and fail locally before transmission when exceeded.

2. **Choose an approved receiver**
   - Show trusted paired nodes and online/offline status.
   - Never expose relay enrollment tokens or private keys in the UI.

3. **Prepare the semantic route automatically**
   - Detect the local embedding model and exact digest.
   - Prefer the strict same-digest 384D fast path when both nodes match.
   - When embedding digests differ, use the signed Semantic Capsule and receiver-local re-embedding; never reinterpret unrelated vector coordinates as universal semantics.

4. **Send and show finality**
   - Present transport status separately from receiver acceptance.
   - Show `validated`, `stored`, `accepted`, object digest, and finality.
   - Do not label relay delivery as successful ingestion unless Node B commits.

5. **Query on Node B**
   - Let the user ask arbitrary fresh questions against one selected committed object.
   - Reconstruct context from digest-verified `material.txt`, `vector.npy`, and lineage for every query.
   - Retain each query artifact and indicate `fresh_context_reconstruction: true` and `phase_b_committed: true`.

6. **Optional generalized before/after check**
   - Let the user ask Node B a question before transfer, send their own state, and ask a newly phrased question afterward.
   - Do not hard-code Kestrel names, facts, thresholds, questions, or expected answers.

## Compatibility boundary

- Completion LLMs do not have to match.
- Matching embedding-model digests are the easiest and best-proven first path.
- Different embedding models require explicit signed semantic material and receiver-local re-embedding.
- Braid supplies context; it does not guarantee that every receiver model will reason correctly.

## Non-claims

The workflow does not transfer model weights, hidden activations, KV cache, consciousness, or native internal model state. It transfers authenticated semantic material and reconstructs receiver-local context.
