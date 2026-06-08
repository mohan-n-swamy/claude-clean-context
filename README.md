# claude-clean-context

[![ci](https://github.com/mohan-n-swamy/claude-clean-context/actions/workflows/ci.yml/badge.svg)](https://github.com/mohan-n-swamy/claude-clean-context/actions/workflows/ci.yml)

Keep Claude Code's always-loaded context lean by demoting stale memory pointers and auditing skill descriptions.

This repo gives Claude Code users a small, deterministic toolkit for cleaning the context that loads before every prompt. It focuses on the two movable layers that tend to grow over time: auto-memory indexes and skill descriptions.

## The Problem

Claude Code starts each session with standing context already loaded. Some of that context is useful: durable rules, corrections, and project-specific guard rails. Some of it quietly turns into stale status: old session snapshots, shipped work notes, and skills that are no longer relevant to the current project.

That costs tokens and dilutes signal. The more stale context is always present, the easier it is for live rules to get crowded out. See [docs/the-problem.md](docs/the-problem.md) for the full explanation.

## The Principle

> A thing earns standing context ONLY if it must be present before you know you need it. Everything else loads on demand.

Memory should hold guard rails, not status logs. Skills should stay eager only when the current project plausibly invokes them.

## The Guard-Rail Test

A `MEMORY.md` line belongs in always-loaded context only if it passes all three:

- **Active before you act**: the agent must already hold it to avoid a mistake.
- **Not derivable**: it cannot be reconstructed from code, git history, or docs.
- **Prevents a concrete recurring error**: it names a real repeated failure it stops.

If a line is status, a resume snapshot, or closed work, it belongs in a lazy retrieval layer instead.

## Quick Start

Clone the repo, then run a dry-run against one memory directory:

```bash
python3 memory-distill.py --mem-dir ~/.claude/projects/<your-project>/memory
```

Review the proposed demotions. Add a `.allowlist` beside `MEMORY.md` for project or reference pointers that truly need to stay eager:

```text
durable_api_rule   keep - prevents repeated API misuse
project_bootstrap  keep - always-needed setup pointer
```

Apply after review:

```bash
python3 memory-distill.py --mem-dir ~/.claude/projects/<your-project>/memory --apply
```

Then inspect skill standing cost:

```bash
python3 skills-report.py
```

To scan every Claude project memory directory:

```bash
python3 memory-distill.py --all
```

## How The Distiller Decides

| Match | Decision |
| --- | --- |
| Target contains `resume-state` | Keep |
| Target contains `feedback_` | Keep |
| Session resume snapshot | Demote |
| Title or hook says closed/resolved/done | Demote |
| Target contains `project_` or `reference_` | Keep only if target contains an allowlisted stem |
| Unknown shape | Keep |

The inverted default is deliberate: project and reference pointers are demoted unless explicitly allowlisted.

## The Skills Layer

Every skill's name and description loads eagerly. `skills-report.py` estimates that standing cost and shows whether each skill is global or project-local. See [docs/skills-layer.md](docs/skills-layer.md).

Global archiving is reversible:

```bash
python3 skills-report.py --archive <skill-name>
```

Archiving a global skill removes it from all projects. If a skill belongs to one project, move it into that project's `.claude/skills/` instead.

## Best-practice layers

- [hooks/](hooks/) - drop-in checks that enforce verification and memory guardrails.
- [doctrine/](doctrine/) - adaptable instruction template for agent-assisted engineering.
- [docs/memory-architecture.md](docs/memory-architecture.md) - the three-layer model for lean standing context, retrieval, and narrative docs.
- [docs/retrieval-layer.md](docs/retrieval-layer.md) - generic self-hostable retrieval blueprint with citations.
- [IMPLEMENT.md](IMPLEMENT.md) - copy-pasteable runbook for standing up the rig.

## Safety

- Dry-run is the default.
- The distiller never deletes files.
- Demoted memory pointers move to `ARCHIVE.md`.
- Skill archiving moves directories to `~/.claude/skills-archive/`.
- Git remains the backstop for review and recovery.

## License

MIT.
