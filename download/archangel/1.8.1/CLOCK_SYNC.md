# A message arrived, but its timestamp was rejected

**Applies to Braid Archangel 1.8.1 and the separate 1.8.2 clock-guidance maintenance build.**

Open the failed message and expand **Receipt & provenance**. Only use these steps as the explanation for a receipt whose reason is `ERR_FUTURE_TIMESTAMP`. Other rejections can have other causes. In 1.8.1 the reason is in the technical receipt; 1.8.2 adds visible clock guidance without changing the validation policy. Publishing this guide does not update an installed application.

## Synchronize both computers

On Windows, open Settings > Time & language > Date & time. Enable **Set time automatically**, select **Sync now**, and check for successful synchronization.

On Mac, open System Settings > General > Date & Time. Enable **Set time and date automatically** and check the selected network time server. Leave automatic time enabled. On Linux, use your system's automatic network-time setting. Network-time access or administrator policy can affect synchronization; resolve a failed sync rather than declaring it fixed.

Braid compares timestamps, not the time-zone labels shown in the two menu bars. A future-timestamp receipt establishes disagreement, not which clock is correct.

## Make one fresh test only after explicit rejection

When the original receipt explicitly confirms rejection before commit, and synchronization succeeded, use **New message** for one fresh harmless note. Inspect the new receiving message: acceptance and field indexing must be confirmed before treating the note as shared-field knowledge. The original rejected record remains rejected.

An unconfirmed or missing receipt is different: the receiver may already have committed it. Inspect receiver state before retrying; do not bypass that uncertainty by creating another handoff.

Do not remove trust, change the rig addresses, loosen timestamp/expiry/signature/replay checks, or index rejected material just to clear this error. Braid does not change system clocks or automatically resend. The 12-second difference in the September 7 test is an observation, not a new acceptance threshold.

## Official operating-system references

- Microsoft, Date and Time settings (Step 6): https://support.microsoft.com/en-us/windows/deployment/updates-lifecycle/troubleshoot-problems-updating-windows
- Apple, automatic date/time and time server: https://support.apple.com/en-au/guide/mac-help/mchlp2996/mac

## Physical example

[September 7 Windows-to-Mac test record](PHYSICAL_WINDOWS_MAC_2026-09-07.md)
