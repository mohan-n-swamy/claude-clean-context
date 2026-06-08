# Security Policy

## Reporting a vulnerability

Please report security issues **privately**, not in a public issue.

Use GitHub's private vulnerability reporting: open the repository's **Security** tab →
**Report a vulnerability** (GitHub Security Advisories). This keeps the report private
until a fix is available.

Include: what the issue is, how to reproduce it, and the impact. We aim to acknowledge
within a few days. There is no bug-bounty program — this is a small open-source project.

## Supported versions

Only the latest release on `main` is supported. Fixes ship forward; older tags are not
back-patched.

## Security posture of the tools

These properties are intentional — treat a change to any of them as a security-relevant change:

- **No code execution on your data.** `memory-distill.py` and `skills-report.py` are
  standard-library Python with no network calls and no LLM in the loop. They read your
  files and print or move pointers. That's it.
- **Non-destructive by default.** The distiller is dry-run by default and **never deletes**
  files — it moves pointers to a lazy `ARCHIVE.md`. `skills-report.py` archives by **moving**
  a directory, never deleting. Git is the backstop.
- **No secrets handled.** The tools do not read, store, or transmit credentials. Keep secrets
  out of `MEMORY.md` and skill files — the tools will happily move a pointer, but they are not
  a secrets manager.

## Retrieval-layer blueprint — your responsibility

`docs/retrieval-layer.md` and `blueprint/` describe an **optional, self-hosted** service. It
is a reference design, not a hosted service — **you** run it, on infrastructure **you**
control. If you build it:

- The OAuth/API tokens, database, and embedding endpoint are yours to secure. Bind to a
  private network or localhost; never expose the MCP or embedding endpoints publicly.
- Put authentication in front of the capture/search endpoints.
- Embeddings of private text are a recoverable copy of that text — host accordingly.
- `blueprint/.env.example` contains **placeholders only**. Never commit real values; keep your
  real `.env` out of version control.

## Hooks

The example hooks in `hooks/` are **fail-open** by design (a parse error must not trap your
session). They are guard rails, not a security boundary — do not rely on them to stop a
determined or malicious actor. Review any hook before wiring it into your `settings.json`.
