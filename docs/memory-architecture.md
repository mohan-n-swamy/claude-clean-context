# Memory Architecture

This repo assumes three memory layers. Each layer has one job. Mixing the jobs creates stale context, contradiction, and slow sessions.

## 1. Always-Loaded Layer

The always-loaded layer is the small set of rules and pointers the agent sees before every prompt. Examples include auto-memory, `MEMORY.md`, and short skill descriptions.

This layer is for guard rails that must pre-fire: rules that prevent a repeated mistake before the agent knows it needs a search. It is deliberately lean. This repo's tools demote status and history out of this layer so durable rules remain visible.

Good always-loaded content:

- A recurring correction that prevents a concrete error.
- A pointer to a canonical workflow.
- A small instruction that must be present before action.

Bad always-loaded content:

- Old session status.
- TODO lists.
- Closed work notes.
- Long explanations that can be retrieved on demand.

## 2. Retrieval Layer

The retrieval layer is an on-demand store. It can be notes search, a vector database, a structured index, or any system where the agent asks a question and gets cited facts back.

This layer holds status, history, decisions, and facts. It is pulled when needed, not parked in standing context where it goes stale. A useful retrieval layer returns provenance: where the fact came from, when it was captured, and a stable citation id.

See [retrieval-layer.md](retrieval-layer.md) for a self-hostable reference design.

## 3. Narrative Layer

The narrative layer is for humans. It is a wiki, docs folder, handbook, research note, design doc, or any browsable explanation that tells the compiled story.

Use this layer for long-form thinking: why a system exists, how parts relate, what tradeoffs were made, and how someone should understand the whole thing. The agent may read it, but it should not all load by default.

## Why Not One Big Wiki?

A single flat, always-loaded wiki fails in three predictable ways.

First, staleness becomes misinformation. Old status remains visible after reality changes, and the agent treats it as current.

Second, contradictions get smoothed away. Large context encourages the model to average conflicting notes instead of asking which source is newer or canonical.

Third, precision falls off at scale. As the wiki grows, the agent spends more context carrying possibly relevant text and less attention using the few lines that matter.

The common "wiki versus retrieval memory" debate points at this same split. Search for public discussion of LLM memory, retrieval, and second-brain systems: the short version is that durable human docs and queryable machine memory solve different jobs. Do not collapse them into one always-loaded pile.

## Practical Rule

If the agent must know it before choosing a tool, keep it always loaded. If the agent can ask for it after understanding the task, put it in retrieval. If a human needs to browse or reason through it, write narrative docs.
