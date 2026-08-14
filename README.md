# Braid v1.5.2 Linux installer

Production packaging for the Intersignal Braid light client:

```bash
curl -fsSL https://intersignal.org/install-braid.sh | bash
```

The installer supports Linux `x86_64`/`amd64` and `aarch64`/`arm64`, requires
Python 3.9+, and installs into an isolated virtual environment. Normal users get:

```text
~/.local/share/braid/releases/1.5.2/
~/.local/share/braid/current -> releases/1.5.2/
~/.local/bin/braid-client
~/.local/bin/braid
~/.local/share/applications/braid-client.desktop
```

Running the installer as root uses `/opt/braid` and `/usr/local/bin`; it does not
write a desktop entry into root's home directory.

## Release procedure

1. Build the final artifacts named `braid-1.5.2-linux-amd64.tar.gz` and
   `braid-1.5.2-linux-arm64.tar.gz`.
2. Put them in `release/v1.5.2/` and run:

   ```bash
   scripts/prepare-release.sh release/v1.5.2
   ```

3. Review the generated `SHA256SUMS` and the two pinned digests in
   `install-braid.sh`. The installer intentionally refuses to run while digest
   placeholders remain. Then run:

   ```bash
   scripts/verify-release.sh release/v1.5.2
   ```
4. Test the exact hosted files on both supported architectures. Rebuilding either
   tarball requires regenerating the manifest and installer pins.
5. Publish the three release files and the installer together. Serve only over
   HTTPS, avoid redirects to non-HTTPS origins, and give `install-braid.sh` a short
   cache lifetime during rollout.

See `release/README.md` for the server layout and artifact contract.

## Security and upgrade behavior

- The selected tarball is verified against a SHA-256 digest embedded in the
  installer before any extraction.
- Extraction rejects traversal, absolute paths, multiple archive roots, links,
  devices, FIFOs, and special permission bits.
- Dependency, venv, download, checksum, package, and verification errors stop the
  installation.
- A release is built in a same-filesystem staging directory and verified before
  `current` is switched. Reinstalling v1.5.2 replaces that release cleanly.
- Verification runs `braid-client --version`. If the CLI advertises `keygen`, it
  also runs key generation with temporary HOME/XDG directories and deletes all
  generated test material afterward.
- There is no automatic local-source or review-candidate path.

`curl | bash` still trusts the HTTPS endpoint that serves the installer. For users
who want to inspect it first:

```bash
curl -fsSLo install-braid.sh https://intersignal.org/install-braid.sh
less install-braid.sh
bash install-braid.sh
```
