# Hooks

These hooks are small enforcement examples. Adapt paths and event wiring for your own setup.

"I'll be careful" is not a mechanism. A check that runs in a hook is.

## Claim Verification Gate

`claim-verify-gate.sh` is a Stop hook. It blocks unsupported completion claims such as "done", "works", "verified", or "deployed" unless the final message includes simple evidence, such as a fenced command output block, `PASS`, `SUCCESS`, `OK`, `exit 0`, or a test summary.

Example settings snippet:

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "/path/to/claude-clean-context/hooks/claim-verify-gate.sh"
      }
    ]
  }
}
```

Smoke test:

```sh
printf '%s\n' '{"message":"done"}' | /path/to/claude-clean-context/hooks/claim-verify-gate.sh
printf '%s\n' '{"message":"done\n\n```text\nPASS\n```"}' | /path/to/claude-clean-context/hooks/claim-verify-gate.sh
```

## Memory Guardrail Check

`memory-guardrail-check.sh` is a PostToolUse hook or manual check. It flags `MEMORY.md` files that have drifted from lean pointer indexes into status boards.

Example settings snippet:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "command": "/path/to/claude-clean-context/hooks/memory-guardrail-check.sh"
      }
    ]
  }
}
```

Manual run:

```sh
/path/to/claude-clean-context/hooks/memory-guardrail-check.sh ~/.claude/projects/<project>/memory/MEMORY.md
```

The check flags resume markers, open TODO blocks, status headings, nested `###` headings, and oversized pointer indexes.
