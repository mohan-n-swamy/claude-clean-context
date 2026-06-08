# The Problem

Claude Code does not start each session from an empty window. Before you type a word, it has loaded standing context — your memory index and every skill's description. Over weeks that context fills with things nobody reads: old session snapshots, shipped-work status, skills this project never invokes. It costs tokens, and worse, it buries the few rules you actually want firing.

This repo treats that as six connected problems. They share one answer: keep standing context to guard rails, push everything else to layers that load on demand.

## Context management

This is the goal everything else serves. The context window is finite and it reloads every session. Whatever sits in it permanently is paying rent on every turn, whether or not you use it. So the question for any line, rule, or skill is narrow: must this be present *before* I know I need it? If yes, it earns standing context. If it can be fetched when the moment comes, it should not be resident.

Run `/context` to see your own baseline. The target is not the smallest possible window. It is a window where every always-loaded line has earned its place.

## Memory management

Two surfaces load eagerly and both accrete: `MEMORY.md` and the name-plus-description of every installed skill.

`MEMORY.md` starts clean — a few durable rules. Then normal work adds to it. Session resumes become pointers. Shipped work gets summarized "in case it's useful." Nothing removes any of it. Skills follow the same curve: one description is cheap, dozens become thousands of standing tokens, much of it for skills a given project never touches. Neither surface garbage-collects itself, and the historical default — keep — is exactly how status logs turn into permanent context. Memory has to be managed, not set once and forgotten.

## Memory: the layer model

The fix starts with knowing where a fact belongs. Three stores, one job each:

- **Always-loaded** (`MEMORY.md`, skill descriptions) — guard rails that must pre-fire. Lean by design.
- **Retrieval** (a search index, vector store, or any "ask and get cited facts" system) — status, history, facts. Pulled on demand, cited, dated, unable to go stale-in-context.
- **Narrative** (docs, a wiki) — the long-form story, for humans.

The bloat problem is almost always a routing problem: status and history got written into layer one, where they sit and rot, instead of layer two, where they would stay fresh and out of the way. The guard-rail test is the router — a line stays in always-loaded memory only if it must be active before you act, can't be derived from code or docs, and prevents a concrete recurring error.

## Distill

Routing is the rule; distilling is the action. `memory-distill.py` walks the memory index and demotes anything that fails the test — session snapshots, closed work, project status not on an explicit allowlist — into a lazy `ARCHIVE.md` that does not load. The keep/demote logic is deterministic, pure regex and string matching with no model in the loop, so a run is reproducible and you can read exactly why each pointer moved. It is dry-run by default and never deletes: the underlying files stay on disk and in git.

The default is inverted on purpose. Project pointers are demoted unless you name them in a `.allowlist`. Keep-by-default is how the logs piled up in the first place; making each kept pointer a deliberate choice is the friction that stops it. `skills-report.py` does the same job for the skill layer — it prices each skill's standing cost and archives the ones a project never invokes, reversibly.

## Verify

A clean window is worth little if the agent fills it with claims that aren't true. The same discipline applies to output: a completion claim needs evidence from this session, not memory of one. The `claim-verify-gate` hook blocks the agent from asserting "done," "deployed," or "verified" until a verifying command has actually run and printed its result. It is the output-side counterpart to keeping memory honest — don't assert what you haven't checked.

## Mechanisms

This is the through-line, and the reason any of it holds. Good intentions drift; mechanisms don't. "I'll keep memory lean" and "I'll verify before I claim" are intentions — they fail the first busy day. So each rule here is paired with something that runs on its own: a check before the change (a count, a grep, a test with explicit pass criteria) and a durable detector after it (a hook, a lint rule, a CI step). The distiller, the allowlist friction, the verify hook, the memory-drift hook, the CI — none of them ask you to remember. They make the right state the default and surface the wrong one automatically.

That is the whole system in one line: context management is the goal, memory management is the surface, distilling and verifying are the actions, the layer model is the map, and mechanisms are why it stays clean instead of drifting back.
