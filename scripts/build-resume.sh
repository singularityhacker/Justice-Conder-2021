#!/usr/bin/env bash
# Render resume-src/resume.html to Justice_Conder_Resume.pdf with headless Chrome.
#
# Usage:
#   scripts/build-resume.sh                 # writes ./Justice_Conder_Resume.pdf
#   scripts/build-resume.sh out.pdf         # writes to a custom path
#   NO_PHOTO=1 scripts/build-resume.sh      # same layout without the headshot
#   CHROME=/path/to/chrome scripts/build-resume.sh
#
# Edit the content in resume-src/resume.html, keep Justice_Conder_Resume.txt in
# sync, then re-run this script.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$ROOT/Justice_Conder_Resume.pdf}"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
SRC="$ROOT/resume-src/resume.html"

if [[ ! -x "$CHROME" ]]; then
	echo "Chrome not found at: $CHROME" >&2
	echo "Set CHROME=/path/to/chrome and retry." >&2
	exit 1
fi

URL="file://$SRC"
if [[ "${NO_PHOTO:-0}" == "1" ]]; then
	URL="$URL?photo=0"
fi

PROFILE="$(mktemp -d "${TMPDIR:-/tmp}/resume-chrome.XXXXXX")"
TMP_OUT="$PROFILE/out.pdf"
CHROME_PID=""

cleanup() {
	if [[ -n "$CHROME_PID" ]] && kill -0 "$CHROME_PID" 2>/dev/null; then
		kill "$CHROME_PID" 2>/dev/null || true
		wait "$CHROME_PID" 2>/dev/null || true
	fi
	rm -rf "$PROFILE"
}
trap cleanup EXIT

# Recent Chrome builds keep running after --print-to-pdf finishes (background
# services hold the process open), so run it in the background, wait for the
# PDF to land, then stop it ourselves.
"$CHROME" \
	--headless=new \
	--disable-gpu \
	--no-first-run \
	--no-default-browser-check \
	--disable-background-networking \
	--disable-sync \
	--disable-component-update \
	--disable-default-apps \
	--disable-extensions \
	--user-data-dir="$PROFILE" \
	--no-pdf-header-footer \
	--print-to-pdf="$TMP_OUT" \
	"$URL" >/dev/null 2>&1 &
CHROME_PID=$!

for _ in $(seq 1 120); do
	if [[ -s "$TMP_OUT" ]]; then
		size1=$(stat -f %z "$TMP_OUT" 2>/dev/null || stat -c %s "$TMP_OUT")
		sleep 0.5
		size2=$(stat -f %z "$TMP_OUT" 2>/dev/null || stat -c %s "$TMP_OUT")
		[[ "$size1" == "$size2" ]] && break
	fi
	if ! kill -0 "$CHROME_PID" 2>/dev/null; then
		break
	fi
	sleep 0.5
done

if [[ ! -s "$TMP_OUT" ]]; then
	echo "Chrome did not produce a PDF within 60s." >&2
	exit 1
fi

mv "$TMP_OUT" "$OUT"
echo "Wrote $OUT ($(du -h "$OUT" | cut -f1 | tr -d ' '))"
