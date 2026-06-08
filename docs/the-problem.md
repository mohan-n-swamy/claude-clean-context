# The Problem

Claude Code does not start each session from an empty context window. Before you type anything, it has already loaded several layers of standing context. Some of those layers are useful. Some quietly become stale.

The usual layers are:

- **Auto-memory**: `MEMORY.md` and the files it indexes. This is always loaded.
- **Skills**: each skill's name and description load eagerly. Skill bodies usually lazy-load only when invoked.
- **MCP tool schemas**: often deferred or loaded on demand. Usually not the first thing to trim.
- **Custom agents**: usually small. Usually not the problem.

The movable fat is auto-memory and skills.

## How Context Accretes

Memory starts clean: a few project rules, API gotchas, or durable user preferences. Then normal work adds more. Session resumes become pointers. Shipped work gets summarized. Temporary project status gets preserved because it felt useful at the time.

The same happens with skills. Each installed skill has a small eager description. One skill is cheap. Dozens of skills become thousands of standing tokens across every session, including projects that never use most of them.

None of this gets garbage-collected automatically. The historical default is usually "keep." That default is how status logs become permanent context.

## Why It Matters

The obvious cost is tokens. Standing context consumes part of the window before the real task begins.

The deeper cost is signal dilution. Stale status competes with live rules. A memory surface full of old shipped work makes it harder for the few active guard rails to stay prominent. Context bloat is not just large; it is noisy.

Use `/context` in Claude Code to see your own baseline. The goal is not a tiny context at all costs. The goal is a context where every always-loaded line has earned its place.

## The Fix

One principle handles both memory and skills:

> A thing earns standing context ONLY if it must be present before you know you need it. Everything else loads on demand.

For memory, that means a guard-rail test. Keep only lines that must pre-fire to prevent a recurring mistake, cannot be derived elsewhere, and need to be active before any search or inspection.

For skills, keep only skills this project plausibly invokes. Archive the rest or move them into the project where they belong.

## What Belongs Elsewhere

Status belongs in a status document, wiki, note store, issue tracker, or search index. Session-resume state belongs in one canonical file that gets overwritten each save. Closed work belongs in history, not standing context.

The distiller in this repo never deletes those underlying files. It only moves pointers out of the always-loaded index and into `ARCHIVE.md`, where they remain recoverable.
