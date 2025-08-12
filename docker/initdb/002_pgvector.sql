CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS lte;
CREATE TABLE IF NOT EXISTS lte.documents (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  source_type TEXT NOT NULL,
  text TEXT NOT NULL,
  meta JSONB DEFAULT '{}'::jsonb
);
CREATE TABLE IF NOT EXISTS lte.doc_embeddings (
  id TEXT PRIMARY KEY,
  doc_id TEXT REFERENCES lte.documents(id) ON DELETE CASCADE,
  run_id TEXT NOT NULL,
  embedding vector(384) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_doc_embed_run ON lte.doc_embeddings(run_id);

