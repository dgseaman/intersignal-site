# Archangel a6: physical Linux-to-Mac LAN handoff

## Result - September 7, 2026

The founder reports a successful physical run of the latest public release, **Braid Archangel 1.7.0a6**, from a Linux laptop to a MacBook Air. The supplied receiver photograph shows the exact text with **Received -> Accepted -> Indexed** completed.

This is a dated supplement to the original a6 build QA. It replaces the blanket statement that no physical a6 Mac/Linux run has been reported; it does not rewrite the historical build logs or certify every feature of a6.

## What was shared

```text
spend no more than 500 credits on our second server today
```

This sentence is the test payload. Its arrival does not execute a spending limit, authorize spending, or prove that a model used it in an answer.

## Physical observations

| Evidence | What it shows |
| --- | --- |
| [Linux composer](../../../assets/archangel/physical-a6-linux-mac-compose.jpg) | The sender selected Davids-MacBook-Air and entered the exact text above. The subject is a local label. The photo alone is the composition stage, not delivery confirmation. |
| [LAN contact](../../../assets/archangel/physical-a6-linux-mac-peer.jpg) | Davids-MacBook-Air is marked Reachable / LAN; the Channels heading is visible. The cropped Cobalt receipt is a different item and is not used as proof of this note's transfer. |
| [Mac receiver](../../../assets/archangel/physical-a6-linux-mac-receipt.jpg) | Sender davidseaman; received on Davids-MacBook-Air; matching text and all three receipt stages. The interface states accepted and indexed. The visible message time is September 7 at 11:36 AM; the Mac menu shows 11:37 AM. |

The three files are the original JPEG bytes, under descriptive filenames. No glare removal, generative enhancement, retouching, cropping, or interface reconstruction was applied. See [the machine-readable evidence manifest](PHYSICAL_RUN_2026-09-07.json) for file sizes and SHA-256 hashes.

## Release identity and scope

The operator identifies the run as the latest public release, a6. The photographs do not show a version readout, wheel checksum, expanded cryptographic receipt, model digest, or OS build number. Expected download hashes below identify the published artifact; they are **not measurements taken from the two test machines**.

- Complete public ZIP: `Braid-Archangel-1.7.0a6-Channels.zip`
- ZIP SHA-256: `98d2eb0c1656fcf972fa773797aba46c8f716bac9357c093141f70838dc1c3f8`
- Wheel SHA-256: `4e26a0830d61cb4781db2f40abacc182971c140fa68a5aa2c522a17aa4a389ea`

This run exercises **the ordinary Messenger summary handoff over LAN**. It does not show a signed channel note being sent, a Channel Chat answer, or a shared-notes count. Existing a5 handoff-and-answer evidence remains separately recorded in the [September 5 record](../PHYSICAL_RUN_2026-09-05.md).

## Remaining checks

The visible success does not close the remaining Channel Chat / channel-isolation tests, restart and failure-recovery tests, Windows native tests, physical QR scans, WAN/Managed Relay qualification, or a7 Resilience qualification. Complete the relevant rows in [UAT_CHANNELS.md](UAT_CHANNELS.md) when those specific operations are exercised.

The public release remains a6. A7 Resilience remains a separate optional, supported Founding Member Preview. This website update changes no installer, source code, dependencies, profile, relay, or membership configuration.

## Distribution observation

The user previously reported that a private Safari window downloaded the complete a6 archive, containing the wheel, source, and platform launchers. That is a user-reported anonymous-download result, separate from the new LAN result. It was not rerun by the assistant in this website update.
