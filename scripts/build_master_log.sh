#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${1:-}" == "--rebuild" ]]; then
  python3 scripts/build_master_log.py --rebuild
elif [[ "${1:-}" == "--append" ]]; then
  phase="${2:-}"
  if [[ -z "$phase" ]]; then
    echo "Usage: $0 --append PHASE_9_2" >&2; exit 1
  fi
  python3 scripts/build_master_log.py --append "$phase"
else
  echo "Usage:"
  echo "  $0 --rebuild              # retroactively rebuild full log from all phases"
  echo "  $0 --append PHASE_9_2     # append a single new phase (plan + summary)"
  exit 1
fi

echo "✅ Updated docs/project_master_log.md"
