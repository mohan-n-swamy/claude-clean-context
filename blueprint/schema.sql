-- Reference retrieval-layer schema.
--
-- Columns:
--   id: stable citation id for agent responses.
--   text: chunk content to retrieve.
--   metadata: provenance and filters such as source, folder, date, tags, stale.
--   embedding: vector produced by your chosen embeddings endpoint.
--   created_at: capture timestamp for recency weighting.
--
-- Replace VECTOR_DIMENSION with your embedding model dimension before applying.

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
  id BIGSERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  embedding vector(VECTOR_DIMENSION) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS chunks_embedding_idx
  ON chunks
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

CREATE INDEX IF NOT EXISTS chunks_metadata_gin_idx
  ON chunks
  USING gin (metadata);

CREATE INDEX IF NOT EXISTS chunks_text_tsv_idx
  ON chunks
  USING gin (to_tsvector('simple', text));

CREATE INDEX IF NOT EXISTS chunks_created_at_idx
  ON chunks (created_at DESC);
