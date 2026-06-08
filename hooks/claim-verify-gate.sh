#!/usr/bin/env sh
#
# Stop hook: blocks unsupported completion claims unless the assistant message
# includes simple evidence. Enable it from your agent settings Stop hook:
#   "command": "/path/to/claude-clean-context/hooks/claim-verify-gate.sh"
#
# Conservative by design: dependency-free, no jq, and fail-open on unexpected
# input so the hook does not trap a user session by accident.

CLAIM_WORDS="${CLAIM_WORDS:-done|fixed|works|verified|passing|passed|deployed|shipped|live|complete|completed}"
EVIDENCE_WORDS="${EVIDENCE_WORDS:-SUCCESS|PASS|PASSED|OK|exit 0|[0-9]+ passed|tests? passed|build succeeded}"

payload=$(sed -n '1,400p' 2>/dev/null) || {
  echo "claim-verify-gate: fail-open; could not read hook input" >&2
  exit 0
}

[ -n "$payload" ] || exit 0

tmp="${TMPDIR:-/tmp}/claim-verify-gate.$$"
trap 'rm -f "$tmp"' EXIT HUP INT TERM

printf '%s\n' "$payload" > "$tmp" 2>/dev/null || {
  echo "claim-verify-gate: fail-open; could not buffer hook input" >&2
  exit 0
}

grep -Eiq "(^|[^[:alnum:]_])(${CLAIM_WORDS})([^[:alnum:]_]|$)" "$tmp" 2>/dev/null || exit 0

if grep -Eq '```' "$tmp" 2>/dev/null; then
  exit 0
fi

if grep -Eiq "(^|[^[:alnum:]_])(${EVIDENCE_WORDS})([^[:alnum:]_]|$)" "$tmp" 2>/dev/null; then
  exit 0
fi

echo "claim-verify-gate: completion claim needs evidence. Run a verifying command (test/build/curl/status), include output, then re-assert." >&2
exit 1
