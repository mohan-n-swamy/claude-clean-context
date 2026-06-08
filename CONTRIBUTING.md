# Contributing

PRs are welcome.

Keep the core behavior deterministic:

- No LLM calls in the keep/demote path.
- Standard library only.
- Dry-run must remain the default.
- Scripts should be auditable from source and reproducible from the same inputs.
- Never delete user memory or skills; move or report instead.

For behavior changes, include a small fixture or command transcript showing the before and after.
