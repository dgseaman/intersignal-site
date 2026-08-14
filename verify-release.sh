#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

readonly VERSION="1.5.2"
readonly ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly RELEASE_DIR="${1:-${ROOT_DIR}/release/v${VERSION}}"
readonly INSTALLER="${ROOT_DIR}/install-braid.sh"

die() { printf 'verify-release: error: %s\n' "$*" >&2; exit 1; }

bash -n "${INSTALLER}" || die "installer has invalid Bash syntax"
[[ "$(LC_ALL=C od -An -tx1 -N3 "${INSTALLER}" | tr -d '[:space:]')" == "23212f" ]] \
  || die "installer must start with #!/ at byte zero"
if LC_ALL=C grep -q $'\r' "${INSTALLER}"; then
  die "installer contains CRLF/CR line endings"
fi

MANIFEST="${RELEASE_DIR}/SHA256SUMS"
[[ -f "${MANIFEST}" ]] || die "missing ${MANIFEST}"
[[ "$(awk 'NF { count++ } END { print count + 0 }' "${MANIFEST}")" == "2" ]] \
  || die "SHA256SUMS must contain exactly two non-empty entries"

hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    die "sha256sum or shasum is required"
  fi
}

for arch in amd64 arm64; do
  artifact="braid-${VERSION}-linux-${arch}.tar.gz"
  artifact_path="${RELEASE_DIR}/${artifact}"
  [[ -f "${artifact_path}" ]] || die "missing ${artifact_path}"
  manifest_hash="$(awk -v name="${artifact}" '$2 == name { print $1 }' "${MANIFEST}")"
  [[ "${manifest_hash}" =~ ^[0-9a-f]{64}$ ]] || die "invalid or missing manifest entry for ${artifact}"
  [[ "${manifest_hash}" == "$(hash_file "${artifact_path}")" ]] || die "manifest mismatch for ${artifact}"
  if [[ "${arch}" == "amd64" ]]; then
    variable="SHA256_AMD64"
  else
    variable="SHA256_ARM64"
  fi
  pinned_hash="$(awk -F'"' -v key="${variable}" '$0 ~ "^readonly " key "=" { print $2 }' "${INSTALLER}")"
  [[ "${pinned_hash}" == "${manifest_hash}" ]] || die "installer pin mismatch for ${artifact}"
done

python3 - "${RELEASE_DIR}" "${VERSION}" <<'PY'
import pathlib
import sys
import tarfile

release_dir = pathlib.Path(sys.argv[1])
version = sys.argv[2]
for arch in ("amd64", "arm64"):
    archive = release_dir / f"braid-{version}-linux-{arch}.tar.gz"
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        if not members:
            raise SystemExit(f"{archive.name}: archive is empty")
        roots = set()
        package_files = set()
        for member in members:
            path = pathlib.PurePosixPath(member.name)
            if path.is_absolute() or not path.parts or any(p in ("", ".", "..") for p in path.parts):
                raise SystemExit(f"{archive.name}: unsafe path {member.name!r}")
            roots.add(path.parts[0])
            if not (member.isdir() or member.isfile()):
                raise SystemExit(f"{archive.name}: link or special file {member.name!r}")
            if len(path.parts) == 2 and member.isfile():
                package_files.add(path.parts[1])
        if len(roots) != 1:
            raise SystemExit(f"{archive.name}: expected exactly one top-level directory")
        if not ({"pyproject.toml", "setup.py"} & package_files):
            raise SystemExit(f"{archive.name}: missing top-level Python package metadata")
PY

printf 'Verified Braid v%s release artifacts, manifest, and installer pins.\n' "${VERSION}"
