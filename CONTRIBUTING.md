# Contributing

PRs are welcome.

Keep the core behavior deterministic:

- No LLM calls in the keep/demote path.
- Standard library only.
- Dry-run must remain the default.
- Scripts should be auditable from source and reproducible from the same inputs.
- Never delete user memory or skills; move or report instead.

For behavior changes, include a small fixture or command transcript showing the before and after.

## Security

Found a vulnerability? Don't open a public issue — report it privately per
[SECURITY.md](SECURITY.md) (GitHub private vulnerability reporting).

When contributing, preserve the security posture: no network calls in the distiller/report
path, dry-run stays the default, nothing gets deleted (move or report instead), and no real
secrets in commits — `blueprint/.env.example` stays placeholder-only.
