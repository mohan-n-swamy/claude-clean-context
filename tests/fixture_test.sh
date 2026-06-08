#!/usr/bin/env sh
# Deterministic checks: distiller reproduces the example fixture and is idempotent.
# Run from the repo root: sh tests/fixture_test.sh
set -eu

root=$(CDPATH= cd "$(dirname "$0")/.." && pwd)
cd "$root"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT INT TERM

cp examples/MEMORY.before.md "$tmp/MEMORY.md"
cp examples/.allowlist.example "$tmp/.allowlist"

# Apply distill, then assert output matches the committed "after" fixture.
python3 memory-distill.py --mem-dir "$tmp" --apply >/dev/null
if ! diff -u examples/MEMORY.after.md "$tmp/MEMORY.md"; then
  echo "FAIL: distill(before) != examples/MEMORY.after.md" >&2
  exit 1
fi
echo "PASS: distill(before) == examples/MEMORY.after.md"

# Re-run must demote nothing (idempotent).
out=$(python3 memory-distill.py --mem-dir "$tmp")
if ! printf '%s\n' "$out" | grep -q "demoted 0 pointer(s)"; then
  echo "FAIL: second run was not idempotent" >&2
  printf '%s\n' "$out" >&2
  exit 1
fi
echo "PASS: idempotent (second run demotes 0)"
