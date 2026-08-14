#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

readonly BRAID_VERSION="1.5.2"
readonly DEFAULT_RELEASE_BASE_URL="https://intersignal.org/releases/braid/v${BRAID_VERSION}"
readonly SHA256_AMD64="__BRAID_AMD64_SHA256__"
readonly SHA256_ARM64="__BRAID_ARM64_SHA256__"

PROGRAM_NAME="${0##*/}"
TMP_DIR=""
LOCK_DIR=""
STAGING_DIR=""

log() { printf '%s\n' "braid-installer: $*" >&2; }
die() { log "error: $*"; exit 1; }

cleanup() {
  local status=$?
  trap - EXIT INT TERM HUP
  if [[ -n "${STAGING_DIR}" && -d "${STAGING_DIR}" ]]; then
    rm -rf -- "${STAGING_DIR}"
  fi
  if [[ -n "${TMP_DIR}" && -d "${TMP_DIR}" ]]; then
    rm -rf -- "${TMP_DIR}"
  fi
  if [[ -n "${LOCK_DIR}" && -d "${LOCK_DIR}" ]]; then
    rmdir -- "${LOCK_DIR}" 2>/dev/null || true
  fi
  exit "${status}"
}
trap cleanup EXIT INT TERM HUP

usage() {
  cat <<EOF
Install Braid Client v${BRAID_VERSION} on Linux.

Usage:
  curl -fsSL https://intersignal.org/install-braid.sh | bash
  ${PROGRAM_NAME}

Run as a normal user for a per-user installation. Run as root for a system-wide
installation. This installer intentionally has no local-source fallback.
EOF
}

case "${1:-}" in
  -h|--help) usage; exit 0 ;;
  "") ;;
  *) die "unknown argument: $1" ;;
esac

[[ "$(uname -s)" == "Linux" ]] || die "this installer supports Linux only"

case "$(uname -m)" in
  x86_64|amd64)
    ARCH="amd64"
    EXPECTED_SHA256="${SHA256_AMD64}"
    ;;
  aarch64|arm64)
    ARCH="arm64"
    EXPECTED_SHA256="${SHA256_ARM64}"
    ;;
  *)
    die "unsupported architecture '$(uname -m)'; supported: x86_64 and arm64"
    ;;
esac

if [[ ! "${EXPECTED_SHA256}" =~ ^[0-9a-f]{64}$ ]]; then
  die "release checksum for ${ARCH} has not been configured; refusing an unverified install"
fi

command -v python3 >/dev/null 2>&1 || die "Python 3.9 or newer is required"
PYTHON_VERSION="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')" || die "cannot determine Python version"
python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 9))' \
  || die "Python 3.9 or newer is required (found ${PYTHON_VERSION})"
python3 -c 'import venv' >/dev/null 2>&1 \
  || die "Python venv support is required (on Debian/Ubuntu, install python3-venv)"
command -v tar >/dev/null 2>&1 || die "tar is required"

if (( EUID == 0 )); then
  INSTALL_ROOT="/opt/braid"
  BIN_DIR="/usr/local/bin"
  DESKTOP_DIR=""
else
  : "${HOME:?HOME must be set for a user installation}"
  INSTALL_ROOT="${HOME}/.local/share/braid"
  BIN_DIR="${HOME}/.local/bin"
  DESKTOP_DIR="${HOME}/.local/share/applications"
fi

RELEASES_DIR="${INSTALL_ROOT}/releases"
FINAL_RELEASE="${RELEASES_DIR}/${BRAID_VERSION}"
ARTIFACT="braid-${BRAID_VERSION}-linux-${ARCH}.tar.gz"
RELEASE_BASE_URL="${BRAID_RELEASE_BASE_URL:-${DEFAULT_RELEASE_BASE_URL}}"
ARTIFACT_URL="${RELEASE_BASE_URL%/}/${ARTIFACT}"

if [[ ! "${ARTIFACT_URL}" =~ ^https:// ]]; then
  die "artifact URL must use HTTPS"
fi

mkdir -p -- "${RELEASES_DIR}" "${BIN_DIR}"
if [[ -e "${INSTALL_ROOT}/current" && ! -L "${INSTALL_ROOT}/current" ]]; then
  die "${INSTALL_ROOT}/current exists but is not a symbolic link; refusing to replace it"
fi
LOCK_DIR="${INSTALL_ROOT}/.install.lock"
mkdir -- "${LOCK_DIR}" 2>/dev/null \
  || die "another Braid installation appears to be running (${LOCK_DIR})"

TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/braid-install.XXXXXXXX")" \
  || die "cannot create temporary directory"
ARCHIVE="${TMP_DIR}/${ARTIFACT}"

log "downloading Braid v${BRAID_VERSION} for ${ARCH}"
if command -v curl >/dev/null 2>&1; then
  curl --fail --silent --show-error --location \
    --proto '=https' --tlsv1.2 --retry 3 --retry-all-errors \
    --output "${ARCHIVE}" "${ARTIFACT_URL}"
elif command -v wget >/dev/null 2>&1; then
  wget --https-only --tries=3 --output-document="${ARCHIVE}" "${ARTIFACT_URL}"
else
  die "curl or wget is required"
fi
[[ -s "${ARCHIVE}" ]] || die "downloaded artifact is empty"

if command -v sha256sum >/dev/null 2>&1; then
  ACTUAL_SHA256="$(sha256sum "${ARCHIVE}" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
  ACTUAL_SHA256="$(shasum -a 256 "${ARCHIVE}" | awk '{print $1}')"
else
  ACTUAL_SHA256="$(python3 - "${ARCHIVE}" <<'PY'
import hashlib
import sys
h = hashlib.sha256()
with open(sys.argv[1], "rb") as source:
    for block in iter(lambda: source.read(1024 * 1024), b""):
        h.update(block)
print(h.hexdigest())
PY
)"
fi
[[ "${ACTUAL_SHA256}" == "${EXPECTED_SHA256}" ]] \
  || die "SHA-256 mismatch for ${ARTIFACT}; refusing to extract it"
log "verified SHA-256: ${ACTUAL_SHA256}"

STAGING_DIR="$(mktemp -d "${RELEASES_DIR}/.staging-${BRAID_VERSION}.XXXXXXXX")" \
  || die "cannot create release staging directory"
mkdir -p -- "${STAGING_DIR}/app"

# Extract regular files and directories only. Reject links, devices, absolute
# paths, traversal, multiple roots, and special permission bits.
python3 - "${ARCHIVE}" "${STAGING_DIR}/app" <<'PY'
import os
import pathlib
import shutil
import sys
import tarfile

archive, destination = sys.argv[1:]
dest = pathlib.Path(destination)
with tarfile.open(archive, "r:gz") as bundle:
    members = bundle.getmembers()
    if not members:
        raise SystemExit("archive is empty")
    roots = set()
    checked = []
    for member in members:
        path = pathlib.PurePosixPath(member.name)
        if path.is_absolute() or not path.parts or any(p in ("", ".", "..") for p in path.parts):
            raise SystemExit("unsafe archive path: %r" % member.name)
        roots.add(path.parts[0])
        if not (member.isdir() or member.isfile()):
            raise SystemExit("archive links and special files are not allowed: %r" % member.name)
        checked.append((member, path.parts[1:]))
    if len(roots) != 1:
        raise SystemExit("archive must contain exactly one top-level directory")
    for member, relative_parts in checked:
        if not relative_parts:
            continue
        target = dest.joinpath(*relative_parts)
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True, mode=0o755)
            os.chmod(target, 0o755)
            continue
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
        source = bundle.extractfile(member)
        if source is None:
            raise SystemExit("cannot read archive member: %r" % member.name)
        with source, open(target, "wb") as output:
            shutil.copyfileobj(source, output)
        os.chmod(target, member.mode & 0o777)
PY

[[ -f "${STAGING_DIR}/app/pyproject.toml" || -f "${STAGING_DIR}/app/setup.py" ]] \
  || die "artifact does not contain a Python package at its top level"

log "creating isolated Python environment"
python3 -m venv "${STAGING_DIR}/venv" \
  || die "failed to create the virtual environment"
"${STAGING_DIR}/venv/bin/python" -m pip install --disable-pip-version-check \
  "${STAGING_DIR}/app" \
  || die "failed to install Braid or one of its dependencies"

CLIENT="${STAGING_DIR}/venv/bin/braid-client"
[[ -x "${CLIENT}" ]] || die "installed package did not provide the braid-client command"

log "verifying braid-client --version"
"${CLIENT}" --version >/dev/null \
  || die "braid-client --version verification failed"

HELP_OUTPUT="$("${CLIENT}" --help 2>&1 || true)"
if grep -Eq '(^|[[:space:]])keygen([[:space:]]|$)' <<<"${HELP_OUTPUT}"; then
  KEYGEN_DIR="${TMP_DIR}/keygen-smoke"
  mkdir -p -- "${KEYGEN_DIR}/home" "${KEYGEN_DIR}/config" "${KEYGEN_DIR}/data"
  log "running temporary keygen verification"
  (
    cd "${KEYGEN_DIR}"
    HOME="${KEYGEN_DIR}/home" \
    XDG_CONFIG_HOME="${KEYGEN_DIR}/config" \
    XDG_DATA_HOME="${KEYGEN_DIR}/data" \
      "${CLIENT}" keygen </dev/null >/dev/null
  ) || die "temporary keygen verification failed"
else
  log "keygen command not advertised by this build; skipping keygen verification"
fi

OLD_RELEASE=""
if [[ -e "${FINAL_RELEASE}" ]]; then
  OLD_RELEASE="${RELEASES_DIR}/.previous-${BRAID_VERSION}.$$"
  mv -- "${FINAL_RELEASE}" "${OLD_RELEASE}"
fi
if ! mv -- "${STAGING_DIR}" "${FINAL_RELEASE}"; then
  [[ -n "${OLD_RELEASE}" ]] && mv -- "${OLD_RELEASE}" "${FINAL_RELEASE}"
  die "failed to publish the staged release"
fi
STAGING_DIR=""

CURRENT_TMP="${INSTALL_ROOT}/.current.$$"
ln -s -- "releases/${BRAID_VERSION}" "${CURRENT_TMP}"
mv -Tf -- "${CURRENT_TMP}" "${INSTALL_ROOT}/current" \
  || die "failed to activate Braid v${BRAID_VERSION}"

write_launcher() {
  local destination="$1"
  local temporary="${destination}.tmp.$$"
  {
    printf '%s\n' '#!/usr/bin/env bash'
    printf 'exec %q "$@"\n' "${INSTALL_ROOT}/current/venv/bin/braid-client"
  } >"${temporary}"
  chmod 0755 "${temporary}"
  mv -f -- "${temporary}" "${destination}"
}
write_launcher "${BIN_DIR}/braid-client"
write_launcher "${BIN_DIR}/braid"

if [[ -n "${DESKTOP_DIR}" ]]; then
  mkdir -p -- "${DESKTOP_DIR}"
  DESKTOP_TMP="${DESKTOP_DIR}/.braid-client.desktop.$$"
  DESKTOP_EXEC="${BIN_DIR}/braid-client"
  DESKTOP_EXEC="${DESKTOP_EXEC//\\/\\\\}"
  DESKTOP_EXEC="${DESKTOP_EXEC//\"/\\\"}"
  DESKTOP_EXEC="${DESKTOP_EXEC//\$/\\\$}"
  DESKTOP_EXEC="${DESKTOP_EXEC//\`/\\\`}"
  cat >"${DESKTOP_TMP}" <<EOF
[Desktop Entry]
Type=Application
Name=Braid Client
Comment=Intersignal Braid light client
Exec="${DESKTOP_EXEC}"
Terminal=true
Categories=Network;Utility;
EOF
  chmod 0644 "${DESKTOP_TMP}"
  mv -f -- "${DESKTOP_TMP}" "${DESKTOP_DIR}/braid-client.desktop"
fi

[[ -z "${OLD_RELEASE}" ]] || rm -rf -- "${OLD_RELEASE}"

log "installed Braid v${BRAID_VERSION} successfully"
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
  log "add ${BIN_DIR} to the front of PATH, then run: braid --version"
else
  log "run: braid --version"
fi
