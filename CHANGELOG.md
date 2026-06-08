# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-08

Initial release.

### Added

- **memory-distill.py** — deterministic `MEMORY.md` distiller. Guard-rail keep/demote
  logic (pure regex/string, no LLM), inverted default (project/reference pointers
  demote unless named in a per-dir `.allowlist`). Dry-run by default; demoted pointers
  move to a lazy `ARCHIVE.md`; never deletes underlying files. Runs against one dir
  (`--mem-dir`) or all project memory dirs (`--all`).
- **skills-report.py** — estimates each skill's per-session description cost, flags
  global vs project-local scope, and archives unused skills to `~/.claude/skills-archive/`
  (reversible move, never deletes).
- **Hooks** — `claim-verify-gate.sh` (Stop hook: blocks unverified completion claims
  until a verifying command has run; fail-open) and `memory-guardrail-check.sh`
  (detects when `MEMORY.md` drifts back into a status board). POSIX sh, dependency-free.
- **doctrine/CLAUDE.md.template** — vendor-neutral best-practice doctrine to adapt into
  your own `CLAUDE.md` (verify-before-claim, V-gate/G-guard, dry-run default,
  restructure-over-patch).
- **Retrieval-layer blueprint** — self-hostable reference design: `blueprint/schema.sql`,
  `docker-compose.example.yml`, `mcp-tools.md` (capture/search contract), `.env.example`.
  Generic placeholders only; no live infrastructure.
- **IMPLEMENT.md** — runbook to hand the repo to Claude Code ("implement this for me"),
  with a verification gate per step.
- **Docs** — `the-problem.md` (the six-theme spine), `guard-rail-test.md`,
  `memory-architecture.md`, `skills-layer.md`, `retrieval-layer.md`.
- **Examples** — `.allowlist.example` plus a before/after `MEMORY.md` fixture.
- **CI** — GitHub Actions: `py_compile`, `sh -n` lint, and a fixture/idempotency test
  (`tests/fixture_test.sh`). Status badge in the README.
- **README visuals** — watercolor concept hero and a faithful SVG terminal screenshot
  of a real distiller dry-run.
- **LAUNCH.md** — launch blurbs (Reddit, X, Show HN, LinkedIn) and a topics/hashtags line.

[Unreleased]: https://github.com/mohan-n-swamy/claude-clean-context/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mohan-n-swamy/claude-clean-context/releases/tag/v0.1.0
