#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <task-slug> [base-dir]" >&2
  exit 64
fi

task_slug="$1"
base_dir="${2:-$(pwd)}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$script_dir/presentation_director.py" \
  --base-dir "$base_dir" \
  guard \
  --task "$task_slug"
