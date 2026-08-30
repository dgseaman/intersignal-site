#!/usr/bin/env bash
set -euo pipefail

BUNDLE_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="dgseaman/intersignal-site"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/intersignal-site-kestrel-stripe.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

command -v git >/dev/null 2>&1 || {
  echo "git is required. Install Xcode Command Line Tools with: xcode-select --install"
  exit 1
}

if command -v gh >/dev/null 2>&1 && gh auth status -h github.com >/dev/null 2>&1; then
  gh repo clone "$REPO" "$WORK/site" -- --depth 1
else
  echo "GitHub CLI is not authenticated; trying the existing Git SSH identity."
  git clone --depth 1 "git@github.com:${REPO}.git" "$WORK/site"
fi

cd "$WORK/site"
git checkout main
git pull --ff-only origin main

cp "$BUNDLE_DIR/index.html" index.html
cp "$BUNDLE_DIR/site-config.js" site-config.js
cp "$BUNDLE_DIR/STRIPE_SETUP.md" STRIPE_SETUP.md
cp "$BUNDLE_DIR/NATIVE_1_6_TURNKEY_REQUIREMENTS.md" NATIVE_1_6_TURNKEY_REQUIREMENTS.md
mkdir -p research founding
cp "$BUNDLE_DIR"/research/* research/
cp "$BUNDLE_DIR"/founding/* founding/

python3 - <<'PYVALIDATE'
from html.parser import HTMLParser
from pathlib import Path

text = Path('index.html').read_text(encoding='utf-8')

class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if 'id' in data:
            self.ids.append(data['id'])
        if tag == 'a' and 'href' in data:
            self.links.append(data['href'])

checker = Checker()
checker.feed(text)
assert len(checker.ids) == len(set(checker.ids)), 'duplicate HTML id'
for link in checker.links:
    if link.startswith('#'):
        assert link[1:] in checker.ids, f'missing anchor target: {link}'
for required in (
    'Braid v1.6.0rc2',
    'A controlled kind of AI osmosis.',
    'Kestrel core proof passed',
    'Technical users can reproduce the mechanism now.',
    'Braid Founding Membership',
    '$99',
    'site-config.js',
    '0bf31ed3888069ff3e3f6685ad5ea794d1a16b03183c04b4c44d7892e7681645',
):
    assert required in text, f'missing required content: {required}'
assert Path('site-config.js').is_file(), 'site-config.js missing'
assert Path('NATIVE_1_6_TURNKEY_REQUIREMENTS.md').is_file(), 'turnkey requirements missing'
assert Path('founding/thanks.html').is_file(), 'founding success page missing'
print('Site validation: PASS')
PYVALIDATE

git diff --check

git config user.name >/dev/null 2>&1 || git config user.name "David Seaman"
git config user.email >/dev/null 2>&1 || git config user.email "dseaman@gmail.com"

git add index.html site-config.js STRIPE_SETUP.md NATIVE_1_6_TURNKEY_REQUIREMENTS.md research/ founding/
if git diff --cached --quiet; then
  echo "No changes to publish."
  exit 0
fi

echo
echo "Files to publish:"
git status --short

git commit -m "Add Braid semantic transfer proof and founding membership checkout"
git push origin main

echo
echo "PASS: site source pushed"
echo "Verify: https://intersignal.org/"
