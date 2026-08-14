#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

readonly VERSION="1.5.2"
readonly ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly RELEASE_DIR="${1:-${ROOT_DIR}/release/v${VERSION}}"
readonly INSTALLER="${ROOT_DIR}/install-braid.sh"

die() { printf 'prepare-release: error: %s\n' "$*" >&2; exit 1; }

AMD64_ARTIFACT="${RELEASE_DIR}/braid-${VERSION}-linux-amd64.tar.gz"
ARM64_ARTIFACT="${RELEASE_DIR}/braid-${VERSION}-linux-arm64.tar.gz"
[[ -f "${AMD64_ARTIFACT}" ]] || die "missing ${AMD64_ARTIFACT}"
[[ -f "${ARM64_ARTIFACT}" ]] || die "missing ${ARM64_ARTIFACT}"

hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    die "sha256sum or shasum is required"
  fi
}

AMD64_SHA="$(hash_file "${AMD64_ARTIFACT}")"
ARM64_SHA="$(hash_file "${ARM64_ARTIFACT}")"

cat >"${RELEASE_DIR}/SHA256SUMS" <<EOF
${AMD64_SHA}  braid-${VERSION}-linux-amd64.tar.gz
${ARM64_SHA}  braid-${VERSION}-linux-arm64.tar.gz
EOF

python3 - "${INSTALLER}" "${AMD64_SHA}" "${ARM64_SHA}" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
values = {"AMD64": sys.argv[2], "ARM64": sys.argv[3]}
for arch, digest in values.items():
    pattern = rf'^(readonly SHA256_{arch}=")[^"]*(")$'
    text, count = re.subn(pattern, rf'\g<1>{digest}\2', text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f"cannot locate SHA256_{arch} in installer")
with path.open("w", encoding="utf-8", newline="\n") as output:
    output.write(text)
PY

printf 'Prepared v%s checksums and pinned them in install-braid.sh.\n' "${VERSION}"
printf 'Review the diff, test both architectures, then commit the installer and SHA256SUMS together.\n'
