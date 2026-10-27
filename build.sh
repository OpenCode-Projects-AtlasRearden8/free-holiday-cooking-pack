#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHEETS_DIR="$ROOT/sheets"
OUT_DIR="$ROOT/printables"

mkdir -p "$OUT_DIR"
rm -f "$OUT_DIR"/*.pdf

shopt -s nullglob
sheets=("$SHEETS_DIR"/*.html)
shopt -u nullglob

if [ "${#sheets[@]}" -eq 0 ]; then
  echo "build: no HTML sheets found in $SHEETS_DIR" >&2
  exit 1
fi

renderer=""
chrome_bin=""
for candidate in google-chrome google-chrome-stable chromium chromium-browser; do
  if command -v "$candidate" >/dev/null 2>&1; then
    renderer="chrome"
    chrome_bin="$candidate"
    break
  fi
done

if [ -z "$renderer" ] && python3 -c "import weasyprint" >/dev/null 2>&1; then
  renderer="weasyprint"
fi

if [ -z "$renderer" ]; then
  echo "build: no HTML-to-PDF renderer found." >&2
  echo "       Install Google Chrome, Chromium, or WeasyPrint (python3 -m pip install weasyprint)." >&2
  exit 1
fi

echo "build: renderer = $renderer ($([ "$renderer" = "chrome" ] && echo "$chrome_bin" || echo "weasyprint module"))"
echo "build: sheets to build = ${#sheets[@]}"

for src in "${sheets[@]}"; do
  base="$(basename "$src" .html)"
  out="$OUT_DIR/$base.pdf"
  case "$renderer" in
    chrome)
      "$chrome_bin" \
        --headless \
        --disable-gpu \
        --no-sandbox \
        --disable-dev-shm-usage \
        --disable-extensions \
        --no-pdf-header-footer \
        --print-to-pdf="$out" \
        "file://$src" >/dev/null 2>&1 || true
      ;;
    weasyprint)
      python3 -m weasyprint "$src" "$out" >/dev/null 2>&1 || true
      ;;
  esac
  if [ ! -s "$out" ]; then
    echo "build: FAILED to render $base" >&2
    exit 1
  fi
  echo "build: ok  $base.pdf"
done

python3 "$ROOT/tests/validate.py" "$OUT_DIR"

echo "build: done — PDFs are in $OUT_DIR"
