#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Normalizing writing content"
python3 scripts/fix_content.py

echo "==> Building speaking index pages"
python3 scripts/build_speaking_index.py

echo "==> Validating writing content"
python3 scripts/validate_content.py

echo "==> Validating speaking data"
python3 scripts/validate_speakers.py

echo "==> All checks passed"
