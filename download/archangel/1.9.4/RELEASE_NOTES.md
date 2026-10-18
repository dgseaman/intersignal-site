# Braid Archangel 1.9.4 — Folio 0.4.0

This test build makes the first publication possible without a model or another
computer, improves the pages you share, and makes handoff receipts easier to read.

## Try the harmless demo

Open Braid, choose **Try a sample conversation**, and edit the fictional garden
conversation in Folio. An unrelated aside starts excluded. The sample includes a
quote, a table, code, a local illustration, and a contents list. It contains no
real conversation or private workspace data and never calls a model. Review and
approve your exact edition, then export its ZIP. Return to Braid to add a rig
when you want to try a real two-computer handoff.

## Publication choices

Compose now offers **Editorial** and **Retro** layouts independently of export
compatibility. Existing Paper/Rose/Midnight colors remain available for Modern
HTML. Classic HTML uses its own restrained light palette. **Classic HTML** emits
HTML 4.01 with a conservative CSS subset available in the 2009 CSS 2.1 candidate
specification: fixed font sizes, ordinary block flow, system fonts, local PNGs,
and links. No required scripts, remote fonts, connection service, CSS Grid/Flex,
custom properties, or modern semantic tags. This is a historical feature subset,
not certification against every 2010 browser. The output has been checked in the
current browser. Keep the entire extracted folder together to retain its images.

Formatted text is opt-in for existing drafts and on for new authored drafts.
Supported Markdown: headings, bold/emphasis, links, quotes, simple lists, fenced
code, pipe tables, and local image lines. Raw HTML remains literal. Remote image
URLs never load. Attach PNG/JPEG/WebP in Compose; the browser resizes to 1200px
and converts to PNG locally. The server keeps pixel chunks and strips ancillary
metadata. Images must fit the 1 MiB each / 4 MiB total document bounds; only
images referenced in included public writing enter the export. Review the visible
pixels as well as captions. Removing an image used by a passage blocks approval
until its image line is removed or the image is attached again.

Headings receive stable anchors. An optional contents list, public byline,
sharing description, license statement, and up to six related edition links are
included in the approved content. Related edition choices use immutable exported
titles and subtitles, never newer private draft names. Enter the actual hosted
page URL; Folio does not infer or verify hosting. Related links are chosen by you.

Review offers Desktop, Tablet, Phone, and Print reading previews of the same saved
publication. Advisory highlights can be toggled separately. Print preview is a
reading approximation; actual pagination depends on the browser print settings.

## Handoff receipts

Inbox and Channel notes show **Sent → Received → Accepted → Available to chat**.
Each step reports its own evidence. A WAN relay queue does not claim receiver
arrival. Legacy acceptance receipts do not prove commitment or indexing. A
missing receipt can mean an already accepted handoff; no automatic retry was
introduced. Local indexed Channel notes show whether current publisher and
Channel permissions allow them in chat. For remote receipts, indexing is shown
while the receiving rig's chat permissions remain explicitly unconfirmed.
Availability never claims that a model actually used a note in an answer.
Plain guidance covers clocks, Channel permissions, certificates, connection,
and model/index problems; exact receipt JSON remains inspectable.

## Retained boundaries and migration

Editing any public content, layout, compatibility, related link, referenced image,
or metadata invalidates approval. Prior export ZIPs remain byte-preserved. Default
legacy plain-text draft bodies keep their content hashes. Private originals,
excluded passages, unused images, private source records, and local advisory
marks remain outside exports. Imports become unapproved drafts. Classic HTML
requires disabling optional connection requests; it never silently changes them.
Existing identities, Channels, and Folio libraries retain the 1.9.3 migration
rules. Quit the previous Braid version before launching this build on its profile.

## Platforms

Apple silicon macOS 13+: self-contained windowed app; no Terminal for ordinary
launch. Ad-hoc signed. No Developer ID identity was available on this build host,
so notarization remains unavailable. Windows and Linux packages retain the private
Python launcher setup and require standard CPython 3.10–3.13. First setup downloads
pinned dependencies unless an offline pack has been prepared. Subsequent
user-reported physical Braid 1.9.4 testing confirmed Windows Nemotron Bolt
in-chat inference, peer connectivity, and messaging on Orpheus. Linux testing
confirmed cross-platform message receipt, completed transport, a receiver
response, handoff acceptance, and an indexed message available within the
Channel. See `PHYSICAL_WINDOWS_LINUX.md` for the report and remaining checks.
These results cover the tested systems and workflows, not every configuration
or a later release. No production profile, paid account, or relay service was
updated by this build. The compatibility website update is prepared separately.
