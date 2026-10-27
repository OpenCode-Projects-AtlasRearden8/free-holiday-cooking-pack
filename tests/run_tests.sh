#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "test 1/3: building the pack fresh"
bash "$ROOT/build.sh"

echo "test 2/3: re-validating every PDF"
python3 "$ROOT/tests/validate.py" "$ROOT/printables"

echo "test 3/3: pack-wide checks (sheets, PDFs, docs, hygiene)"
python3 "$ROOT/tests/checks.py" "$ROOT"

echo ""
echo "ALL TESTS PASSED"
