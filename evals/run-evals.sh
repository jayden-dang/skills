#!/usr/bin/env bash
# Run the skill evals. Thin wrapper so CI and humans have one entry point.
# Forwards all arguments to evals.py (e.g. --tier 1, --json, --strict).
# Dependency-free: needs only the python3 (3.9+) already required by the linters.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${here}/evals.py" "$@"
