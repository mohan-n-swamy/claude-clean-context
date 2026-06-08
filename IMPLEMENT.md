Give this repo to a capable coding agent and say: *implement this for me*. It should follow the steps below.

# Implementation Runbook

This runbook turns the repo into a working lean-context rig: small standing memory, deterministic enforcement hooks, adoptable doctrine, and an optional retrieval layer.

## Step 1 - Lean Memory

Run the memory distiller in dry-run mode against each memory directory:

```sh
python3 memory-distill.py --mem-dir ~/.claude/projects/<project>/memory
```

Review each proposed demotion. Create an allowlist beside `MEMORY.md` for pointers that must remain always loaded:

```text
durable_api_rule   keep - prevents repeated API misuse
project_bootstrap  keep - always-needed setup pointer
```

Apply only after review:

```sh
python3 memory-distill.py --mem-dir ~/.claude/projects/<project>/memory --apply
```

Then audit skill standing context:

```sh
python3 skills-report.py
```

Archive skills that are never used or move project-only skills into that project's local skills directory.

V-gate: dry-run shows the exact demotion count, `MEMORY.md` still contains only durable guard rails, and `ARCHIVE.md` receives demoted pointers after apply.

## Step 2 - Enforcement

Copy the hook snippets from [hooks/README.md](hooks/README.md) into your agent settings file. Use absolute paths on your machine.

Run a local smoke test:

```sh
printf '%s\n' '{"message":"done"}' | hooks/claim-verify-gate.sh
printf '%s\n' '# Index\n- durable guard rail\n' > /tmp/MEMORY.md
hooks/memory-guardrail-check.sh /tmp/MEMORY.md
```

V-gate: the first command blocks an unsupported completion claim; the second exits cleanly for a pure pointer index.

## Step 3 - Doctrine

Adapt [doctrine/CLAUDE.md.template](doctrine/CLAUDE.md.template) into your global or project-level instruction file. Trim anything that does not match your workflow.

V-gate: a new session repeats the doctrine's core rules before acting: verify before claiming, lean context, design before non-trivial edits, and mechanism over intention.

## Step 4 - Optional Retrieval Layer

Use the reference blueprint only if you want on-demand recall with citations.

1. Copy [blueprint/.env.example](blueprint/.env.example) to a private `.env` file and fill in your own values.
2. Apply [blueprint/schema.sql](blueprint/schema.sql) to a SQL database with vector support.
3. Run an embeddings endpoint behind `EMBEDDINGS_API`.
4. Build an MCP server that implements [blueprint/mcp-tools.md](blueprint/mcp-tools.md).
5. Run [blueprint/docker-compose.example.yml](blueprint/docker-compose.example.yml) after replacing placeholder images and environment values.
6. Verify a capture/search round-trip:

```sh
# Pseudocode: adapt to your MCP client.
capture text="The retrieval layer is working." metadata='{"source":"smoke-test"}'
search query="retrieval layer working"
```

V-gate: search returns the just-captured chunk with a citation token like `[chunk:123]`.

Security rule: supply your own host, auth, and secrets. Bind private. Put auth in front of MCP and embedding endpoints. Do not commit real `.env` values.

## Checklist

- [ ] `memory-distill.py` dry-run reviewed.
- [ ] `.allowlist` created for durable memory pointers.
- [ ] Memory demotions applied where appropriate.
- [ ] `skills-report.py` reviewed and stale skills archived or moved.
- [ ] Claim verification hook wired and smoke-tested.
- [ ] Memory guardrail hook wired or scheduled and smoke-tested.
- [ ] Doctrine adapted into global or project instructions.
- [ ] Optional retrieval layer captures and searches one test fact.
- [ ] Completion claims are backed by visible evidence from this session.

This rig keeps standing context lean and every completion claim verified.
