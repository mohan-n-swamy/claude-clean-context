# MCP Tool Contract

This contract defines the retrieval MCP server an agent can implement. Names are generic; keep auth and transport details in your server config.

## Tool: `capture`

Description: Store one text chunk with provenance metadata and an embedding.

Input schema:

```json
{
  "type": "object",
  "required": ["text"],
  "properties": {
    "text": {
      "type": "string",
      "description": "Chunk text to store."
    },
    "metadata": {
      "type": "object",
      "description": "Provenance and filters: source, folder, tags, date, canonical, stale."
    }
  }
}
```

Result shape:

```json
{
  "id": 123,
  "citation": "[chunk:123]",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "metadata": {
    "source": "example"
  }
}
```

Behavior:

- Reject empty text.
- Add capture timestamp if caller does not provide one.
- Embed the text with `EMBEDDINGS_API`.
- Store original text, metadata, embedding, and timestamp.
- Return a stable citation token.

## Tool: `search`

Description: Search captured chunks and return cited results.

Input schema:

```json
{
  "type": "object",
  "required": ["query"],
  "properties": {
    "query": {
      "type": "string",
      "description": "Natural-language or keyword query."
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 50,
      "default": 10
    },
    "filters": {
      "type": "object",
      "description": "Optional filters: after, before, source, folder, tags, include_stale."
    }
  }
}
```

Result shape:

```json
{
  "chunks": [
    {
      "id": 123,
      "text": "Stored chunk text.",
      "metadata": {
        "source": "example"
      },
      "score": 0.91,
      "citation": "[chunk:123]",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ]
}
```

Supported filters:

- `after`: include chunks created on or after a date.
- `before`: include chunks created on or before a date.
- `source`: match a source field in metadata.
- `folder`: match a folder or namespace field in metadata.
- `tags`: include chunks with one or more metadata tags.
- `include_stale`: include chunks marked stale; default should be false.

Retrieval guidance:

- Combine vector similarity, keyword ranking, and recency weighting.
- Return enough text for citation, but not more than the caller needs.
- Include chunk ids on every result.
- Do not hide contradictions. If stale and fresh chunks both match and `include_stale` is true, return both with metadata.
