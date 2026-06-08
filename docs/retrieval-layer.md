# Retrieval Layer

Vendor-neutral reference. Pick your own database, embedding model, and host. No live deployment is described here - these are the parts you build yourself.

## What It Is

A retrieval layer is a small service exposing two operations to an agent:

- `capture(text, metadata)`: store a fact, note, decision, or chunk with provenance.
- `search(query) -> cited chunks`: return relevant chunks with ids the agent can cite.

It is not the always-loaded memory. It is the recall layer the agent queries when it needs status, history, prior decisions, or related facts.

## Architecture

The reference stack has three parts.

The database is a SQL store with vector search support. The core table is `chunks(id, text, metadata jsonb, embedding vector, created_at)`. Add a vector similarity index for semantic search and a keyword index for exact matching.

The embeddings service sits behind a standard `/v1/embeddings` HTTP interface. It can be a local open model runner or a hosted embeddings API. The retrieval service should only depend on the interface, not the provider. Co-locate the database and embedder when possible to reduce latency.

The MCP server exposes the agent-facing tools: `capture` and `search`. `capture` writes text, metadata, and embedding. `search` runs hybrid retrieval:

- semantic similarity over embeddings
- keyword search over text and metadata
- recency weighting where newer facts should rank higher

The output must include stable chunk ids and citation tokens such as `[chunk:123]`.

## Discipline

The valuable part is not the database. The valuable part is the discipline.

Every captured fact carries metadata: date, source, folder or project, author or system if useful, and whether the chunk is canonical or stale.

Every retrieved claim is cited back to a chunk id. If the agent says a fact came from retrieval, the citation must be visible.

The store is for recall, not the source of truth for mutable state. The canonical record is the typed file, issue, commit, ticket, note, or database row that the store indexed afterward. Use retrieval to find, relate, and remember. Read the canonical source before acting on live mutable state.

On contradiction, newer source usually wins, but preserve the older chunk. Do not silently delete losing history; mark it stale or superseded so future searches can explain the change.

## How It Ties To This Repo

This repo keeps `MEMORY.md` lean. `MEMORY.md` should hold only guard rails that must fire before search. Status and history live in retrieval and are pulled on demand.

That split keeps standing context small without losing long-term recall. The agent starts lean, then asks retrieval for facts when the task calls for them.

## Security And Ops

Keep secrets out of captured text. Embeddings of private text are another recoverable copy of that text. Host on infrastructure you control or trust, and lock it down.

Put auth in front of MCP and embedding endpoints. Bind services to localhost or a private network. Do not expose unauthenticated retrieval or embeddings services to the public internet.

This layer is optional. The repo's lean-memory tools still work without it. If you skip retrieval, demote status into git-tracked docs and search those docs directly.

## Build Order

1. Create a SQL database with vector search support.
2. Apply [../blueprint/schema.sql](../blueprint/schema.sql).
3. Run an embeddings endpoint and set `EMBEDDINGS_API`.
4. Implement the MCP tools in [../blueprint/mcp-tools.md](../blueprint/mcp-tools.md).
5. Verify with one capture and one search that returns the captured chunk.
