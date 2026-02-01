#!/usr/bin/env bash
# run_tests.sh - cross-platform helper (Unix/macOS)
set -euo pipefail
cd "$(dirname "$0")/.."

if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    PY=python
else
    echo "Python introuvable. Installez Python 3.10+"
    exit 1
fi

if [ ! -d .venv ]; then
    $PY -m venv .venv
fi

# shellcheck disable=SC1091
. .venv/bin/activate

$PY -m pip install --upgrade pip
pip install -r requirements.txt

$PY -m tests.test_pipeline
