#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: validate_mihomo_profile.sh /path/to/profile.yaml" >&2
  exit 2
fi

profile=$1
mihomo_bin=${MIHOMO_BIN:-/Applications/Clash Verge.app/Contents/MacOS/verge-mihomo}
mihomo_data=${MIHOMO_DATA_DIR:-$HOME/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev}

[[ -f "$profile" ]] || { echo "profile not found" >&2; exit 2; }
[[ -x "$mihomo_bin" ]] || { echo "mihomo binary not found; set MIHOMO_BIN" >&2; exit 2; }
[[ -d "$mihomo_data" ]] || { echo "mihomo data directory not found; set MIHOMO_DATA_DIR" >&2; exit 2; }

"$mihomo_bin" -t -f "$profile" -d "$mihomo_data"
