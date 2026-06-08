#!/usr/bin/env sh
#
# PostToolUse/manual check: keeps MEMORY.md as a lean pointer index, not a
# status board. Enable from your agent settings PostToolUse hook or run:
#   /path/to/claude-clean-context/hooks/memory-guardrail-check.sh /path/to/MEMORY.md
#
# Dependency-free POSIX sh. Fails open when no files are found or a file cannot
# be read; flags only clear drift patterns.

MAX_POINTER_LINES="${MAX_POINTER_LINES:-60}"
status=0
found=0

check_file() {
  file=$1
  [ -r "$file" ] || {
    echo "memory-guardrail-check: fail-open; cannot read $file" >&2
    return 0
  }

  found=1

  if grep -Eq 'RESUME POINT|OPEN TODO|^##[[:space:]]+Status|^###[[:space:]]+' "$file" 2>/dev/null; then
    echo "memory-guardrail-check: $file looks like status/TODO content, not a lean pointer index" >&2
    status=1
  fi

  pointer_lines=$(grep -Ec '^[[:space:]]*[-*][[:space:]]+' "$file" 2>/dev/null || printf '0\n')
  case $pointer_lines in
    ''|*[!0-9]*) pointer_lines=0 ;;
  esac

  if [ "$pointer_lines" -gt "$MAX_POINTER_LINES" ] 2>/dev/null; then
    echo "memory-guardrail-check: $file has $pointer_lines pointer lines; max is $MAX_POINTER_LINES" >&2
    status=1
  fi
}

if [ "$#" -gt 0 ]; then
  for file in "$@"; do
    check_file "$file"
  done
else
  for file in "$HOME"/.claude/projects/*/memory/MEMORY.md; do
    [ -e "$file" ] || continue
    check_file "$file"
  done
fi

[ "$found" -eq 1 ] || exit 0
exit "$status"
