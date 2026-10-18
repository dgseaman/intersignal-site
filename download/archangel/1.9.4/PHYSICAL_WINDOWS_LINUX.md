# Braid 1.9.4 — reported Windows/Linux physical testing

Report recorded: October 18, 2026. The user supplied these results in the Braid
1.9.5 work request. The exact test dates, OS versions, hardware specifications,
model digest, and test-artifact hashes were not supplied with that report.

## Reported results

| System | Result reported by the user |
| --- | --- |
| Orpheus — Windows | Braid 1.9.4 operational; successful Nemotron Bolt in-chat inference; successful peer connectivity and messaging |
| Linux | Braid 1.9.4 operational; successful cross-platform message receipt; transport confirmed; receiver response recorded; handoff accepted; message indexed and available within the Channel |

These observations support the statement that Braid 1.9.4 has been physically
tested across Windows and Linux systems. Transport, receiver response,
acceptance, and indexing remain separate outcomes. An indexed message available
within a Channel does not itself prove that a model used it in a generated
answer.

## Scope and remaining checks

The report applies to the tested 1.9.4 systems and workflows. It does not certify
every computer, OS version, architecture, model, direction of delivery, or network
configuration. It does not establish that all inference happened across rigs,
that every platform pairing was tested, or that all existing features were
retested. It does not claim physical testing of Braid 1.9.5.

The earlier build-host checks remain in `TEST_RESULTS.md`. The Windows/Linux
packages still use the existing Python launchers; this report does not add
native Windows/Linux binaries or change first-setup requirements. The Mac app
remains ad-hoc signed and not Developer ID notarized.

Record separate results for the 1.9.5 acceptance cases: Mariana's DeepSeek V4
Flash through its existing vLLM endpoint; coexistence with its independent web
interface; a Windows Nemotron Bolt regression check; Linux and Windows
networking/handoffs after the update; macOS regression; visual behavior and
reduced motion on actual platforms. Physical camera/Bluetooth behavior,
additional network paths and directions, historical browsers, and broader
hardware/endurance coverage remain unqualified unless separately recorded.

Older release documentation remains evidence for its named release and is not
retroactively promoted by this report. The published 1.9.4 artifact identity and
download URL are unchanged.
