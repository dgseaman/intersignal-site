# Archangel 1.7.0a5 - Mac launcher fix 1

This is a packaging-only correction for the MacBook Air startup report. The
Braid 1.7.0a5 application wheel, dependencies, protocol and Python support
range are unchanged. This is not a new protocol or application release.

## Run

Extract this ZIP into its own folder and open `Start Braid.command` there.
Do not replace just that file in the old release: its hash is covered by the
bundle manifest. This repack includes matching integrity metadata.

The launcher prints the interpreter it selects. It first checks the current
`python3`, then supported versioned interpreters on PATH, then standard
Homebrew (Apple Silicon and Intel), Python.org framework, MacPorts, user-local
and pyenv-shim locations. Unsupported defaults are skipped. This is bounded
discovery, not a scan of every environment anywhere on the disk.

A supported Python must already be installed. This fix does not install Python
or change system aliases. If none is found, the message explains the required
range and the optional `BRAID_PYTHON` explicit executable selector. An invalid
explicit selector fails without fallback. Free-threaded builds remain excluded.

For a read-only discovery check, run inside the extracted directory:

```sh
sh "Start Braid.command" --runtime-info
```

For an integrity check without installing or opening the profile:

```sh
sh "Start Braid.command" --check
```

The ordinary launch still uses the existing profile-selection behavior and
requires online dependencies or the existing offline setup on first install.
This launcher correction does not rotate identities, erase data, resend
messages, relax receiver checks, or enable unsupported Python versions.
Application failures are not retried using a second interpreter.

The original `Start Braid.sh` and `Start Braid.cmd` are unchanged; this fix
addresses the reported macOS launch path only.

## Verification

16 focused discovery/control-flow tests passed on Linux. Fixed macOS install
prefixes were redirected into temporary fixtures to simulate limited-PATH,
Homebrew and Python.org layouts. These are not physical macOS execution tests.
A real CPython 3.13 run of the corrected launcher passed `--runtime-info` and
the unchanged launcher's `--check` bundle-integrity check without installation.
The application wheel matches the original SHA-256 exactly:

`c828c1c19a2359181ebbbb3dd0bae6dc97b8745b1138702c4a3adcc98e3ec507`

The other evidence and a5 release documents are retained baseline evidence;
they are not a new full-suite or cross-platform test run for this repack.
Physical MacBook Air execution and real multi-rig tests remain outstanding.

Reproduce the focused tests from this directory:

```sh
ARCHANGEL_LAUNCHER="$PWD/Start Braid.command" python3 evidence/mac-launcher-fix1/test_mac_launcher.py
```

The source archive contains the corrected macOS launcher. The patch file
`Mac-Launcher-Fix1.patch` records that narrow launcher change against a5.
