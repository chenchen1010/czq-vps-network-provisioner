#!/usr/bin/env bash
set -euo pipefail

proxy_url=${1:-http://127.0.0.1:17900}
expected_ip=${2:-}

probe() {
  local name=$1
  local url=$2
  local result
  result=$(curl --proxy "$proxy_url" -L --max-time 15 -sS -o /dev/null -w '%{http_code} %{time_total}' "$url" 2>&1 || true)
  printf '%-10s %s\n' "$name" "$result"
}

probe Google https://www.google.com/generate_204
probe YouTube https://www.youtube.com/generate_204
probe TikTok https://www.tiktok.com/
probe Facebook https://www.facebook.com/
probe Instagram https://www.instagram.com/
probe ChatGPT https://chatgpt.com/
probe Claude https://claude.ai/
probe Gemini https://gemini.google.com/
probe Grok https://grok.com/

exit_ip=$(curl --proxy "$proxy_url" --max-time 15 -sS https://api.ipify.org 2>/dev/null || true)
if [[ -n "$expected_ip" ]]; then
  if [[ "$exit_ip" == "$expected_ip" ]]; then
    echo "ExitIP    MATCH"
  else
    echo "ExitIP    MISMATCH"
    exit 1
  fi
else
  echo "ExitIP    observed (redacted from output by default)"
fi
