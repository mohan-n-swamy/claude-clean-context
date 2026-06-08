# Launch blurbs

Draft copy for announcing `claude-clean-context`. Pick per channel; edit the hook from comments after the first post lands.

---

## 1. r/ClaudeAI

**Title:** I kept finding stale session-logs in Claude Code's context every morning, so I built a tool to clean it

Open a fresh Claude Code session and a chunk of the context is already spent — before you type anything. Your `MEMORY.md` loads in full, every skill's description loads, and over weeks it accretes: old "here's where I left off" snapshots, shipped-work notes, status nobody reads. Stale context doesn't just cost tokens. It crowds out the rules you actually want firing.

`claude-clean-context` is a small, deterministic toolkit to fix that. One principle runs through it: **a thing earns always-loaded context only if it must be present before you know you need it. Everything else loads on demand.**

What's in it:
- **memory-distill.py** — demotes stale/session/closed pointers out of `MEMORY.md` into a lazy archive. Dry-run by default, never deletes, git is the backstop.
- **skills-report.py** — shows what each skill's description costs you per session, and lets you archive the ones this project never invokes (reversible).
- **Drop-in hooks** — one blocks "done/shipped/verified" claims until you've actually run a verifying command; one detects when `MEMORY.md` drifts back into a status board.
- **A doctrine template + a full retrieval-layer blueprint** — if you want the on-demand recall layer too, the schema, MCP tool contract, and compose are all there to self-host.

Hand the repo to Claude, say "implement this for me," and follow `IMPLEMENT.md`. Stdlib-only, MIT, CI green.

https://github.com/mohan-n-swamy/claude-clean-context

Curious what others park in `MEMORY.md` that turned out to be dead weight.

---

## 2. X / short

Every fresh Claude Code session loads your full MEMORY.md + every skill description — before you type. Over weeks it fills with stale session-logs that crowd out the rules you want firing.

claude-clean-context: a deterministic toolkit to keep that context lean. Demote stale memory, audit skill cost, enforce-with-hooks. Dry-run default, never deletes, MIT.

github.com/mohan-n-swamy/claude-clean-context

---

## 3. Show HN

**Title:** Show HN: Keep Claude Code's always-loaded context lean

Claude Code loads two things into context at the start of every session, before you type: your `MEMORY.md` index, and the name + description of every installed skill. Skill *bodies* lazy-load only when invoked — but the descriptions are always resident. Dozens of skills runs to thousands of tokens of standing cost, much of it for skills a given project never touches. Add accreting `MEMORY.md` snapshots on top, and a real fraction of every fresh session is spent before you've asked anything.

`claude-clean-context` attacks both layers with one rule: a thing earns always-loaded context only if it must be present before you know you need it. Everything else loads on demand.

Two stdlib-only Python scripts:
- **memory-distill.py** — keep/demote logic is deterministic (pure regex/string, no LLM in the loop), so a run is reproducible and you can read exactly why each pointer was demoted. Dry-run by default, never deletes; demoted pointers move to a lazy `ARCHIVE.md`, files stay in git.
- **skills-report.py** — estimates each skill's per-session description cost, flags global vs project-local scope, and archives the ones this project never invokes (a move, fully reversible). Global skills load in *every* project; if a skill belongs to one project, the fix is to scope it there, not delete it.

The design choice worth debating: the memory default is **demote, not keep**. Project pointers survive only if you name them in an explicit `.allowlist`. Keep-by-default is exactly how session-logs silently pile up; the allowlist is deliberate friction.

Two parts lean on Claude Code itself. First, two drop-in hooks: one blocks the agent from claiming "done/deployed/verified" until a verifying command has actually run in the session; one detects when `MEMORY.md` drifts back into a status board. Second — and the reason it installs fast — you can hand the whole repo to Claude Code and say "implement this for me." It follows `IMPLEMENT.md`: distills your memory, audits skills, wires the hooks, adapts a doctrine template into your `CLAUDE.md`, and (optionally) stands up the retrieval-layer blueprint (schema + MCP capture/search contract) so status lives in an on-demand store instead of standing context. Each step has a verification gate the agent has to pass.

MIT, CI green, no dependencies.

https://github.com/mohan-n-swamy/claude-clean-context

---

## 4. LinkedIn

I kept opening fresh Claude Code sessions and finding the context already half-spent — before I'd typed a thing.

Claude Code loads standing context every session: your memory index, and every installed skill's description. Mine had quietly turned into a graveyard. The line that made it click was a `session_2026-02` snapshot, "paused while fixing parser tests," from a project I'd shipped weeks earlier, still loading into every new session. Behind it, dozens more like it. Shipped-work status I'd never read again. Skill descriptions for skills this project never invokes. None of it garbage-collects. The default is to keep, and keep-by-default is exactly how a clean memory file becomes a status dump.

The cost isn't just tokens. Stale status competes with the rules you actually want firing. A window full of old work makes the few live guard rails harder to find.

So I built `claude-clean-context` — a small, deterministic toolkit to keep that context lean, and made it open source.

One rule decides everything: a thing earns always-loaded context only if it must be present before you know you need it. Everything else loads on demand.

It demotes stale memory (dry-run by default, never deletes), prices and prunes unused skills, and ships drop-in hooks — including one that blocks the agent from claiming "done" until it has actually run a verifying command. You can hand the repo to Claude and say "implement this for me."

MIT, no dependencies.

https://github.com/mohan-n-swamy/claude-clean-context
