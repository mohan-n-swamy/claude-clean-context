# Guard-Rail Test

`MEMORY.md` is an always-on guard-rail surface. It is not a status board, changelog, or session log.

A line earns standing context only if it passes all three checks.

## 1. Active Before You Act

The rule must be present before the agent takes action. If the agent would only need the fact after searching, reading a file, or inspecting history, it does not belong in always-loaded memory.

Good guard rails pre-fire. They stop predictable mistakes before the first command or edit.

## 2. Not Derivable

The line should not be reconstructable from source code, tests, docs, git history, or a retrieval store. If the information can be looked up when needed, it should load on demand.

Always-loaded memory is for information that retrieval would find too late.

## 3. Prevents A Concrete Recurring Error

The line should name a durable correction, preference, or behavior rule that prevents a repeated failure.

Examples that pass:

- "Always use the wrapper field, not the raw timestamp field."
- "Never run the deploy command without the served-version check."
- "This project expects generated files to stay out of hand-edited docs."

Examples that fail:

- "Feature X shipped last week."
- "Current status: waiting on review."
- "Session resume: next step is to fix tests."
- "Closed: migration completed."

## Invert The Default

Project and reference pointers should not survive by default. A pointer stays eager only when its filename stem appears in `.allowlist`.

That friction is intentional. Adding a stem says: this pointer still needs to pre-fire.

## Never Demote Into A Void

Demotion should not destroy knowledge. Durable content should remain recoverable in docs, git, a note store, or another retrieval layer.

`memory-distill.py` only moves pointer lines from `MEMORY.md` to `ARCHIVE.md`. It never deletes target files.
