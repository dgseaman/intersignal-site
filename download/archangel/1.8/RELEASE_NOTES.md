# Braid Archangel 1.8.0 - release notes

Date: September 7, 2026.

## Basis

Public a6 Channels + the existing Composer Fix 1, consolidated as 1.8.0. No a7 Resilience merge, new third-party dependency, protocol extension, channel permission change or automatic model/relay behavior.

## Composer corrections carried into 1.8

- Main Share summary, welcome compose and N open blank at Write with a fresh identity.
- Drafts explicitly resumes the saved content, mode and handoff identity.
- New message saves nonempty work then starts blank, rather than copying an old delta.
- X/Escape close without sending; an empty composer does not overwrite an older saved draft.
- Discard removes only the draft, with confirmation. History and durable delivery locks remain.
- One saved-draft slot remains, with replacement confirmation and save-error recovery.
- In-flight work cannot populate a subsequently opened message.

The sidebar identifies 1.8; the wheel, launcher, version-specific runtime and backend report 1.8.0. Mac supported-interpreter discovery remains included. The launcher takes a 1.8-specific desktop/trust snapshot before opening an existing database; no new database schema was added.

## Preserved behavior

Signed Channels, local chat, exact-context receipts, manual/topic-draft/explicit /note flows, receiver-owned acceptance, direct mTLS, signed-file and optical workflows, source-preserving fields and guarded queries are retained unchanged. No smart transport fallback, spending enforcement or third-party-chat interception is added.

## Evidence boundary

The spending demo is a6-line evidence: source restriction, accepted/indexed Mac receipt, then a different question returning 500. Its response dropped `second server` and used generic cautionary wording. It is not a monetary control, independent validation or proof of zero hallucinations. The separate failed delta's detailed cause was not supplied and is not diagnosed here.

Read QA.md for the exact 1.8 test results and UAT_1_8.md before broad rollout. The public version name is not native platform certification. Source/wheel checksums establish consistency, not publisher authenticity.
