-- Phase 9.5.1: Model-Aware Embedding Storage Migration
-- Remove magic dimensions and partition embeddings by (model_key, dim)

-- Ensure vector extension is loaded
CREATE EXTENSION IF NOT EXISTS vector;

-- Create new model-aware embedding table
CREATE TABLE IF NOT EXISTS lte.model_aware_embeddings (
  id TEXT PRIMARY KEY,
  doc_id TEXT REFERENCES lte.documents(id) ON DELETE CASCADE,
  run_id TEXT NOT NULL,
  model_key TEXT NOT NULL,
  embedding_dim INTEGER NOT NULL,
  embedding vector NOT NULL,  -- No hard-coded dimension
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_model_aware_embeddings_run_id ON lte.model_aware_embeddings(run_id);
CREATE INDEX IF NOT EXISTS idx_model_aware_embeddings_model_key ON lte.model_aware_embeddings(model_key);
CREATE INDEX IF NOT EXISTS idx_model_aware_embeddings_dim ON lte.model_aware_embeddings(embedding_dim);
CREATE INDEX IF NOT EXISTS idx_model_aware_embeddings_model_dim ON lte.model_aware_embeddings(model_key, embedding_dim);

-- Create composite index for KNN search
CREATE INDEX IF NOT EXISTS idx_model_aware_embeddings_knn ON lte.model_aware_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Migration: Copy existing embeddings to new table
-- This preserves existing data while adding model awareness
INSERT INTO lte.model_aware_embeddings (id, doc_id, run_id, model_key, embedding_dim, embedding)
SELECT 
  id,
  doc_id,
  run_id,
  'default' as model_key,  -- Default model key for existing embeddings
  384 as embedding_dim,    -- Current dimension from models.toml
  embedding
FROM lte.doc_embeddings
ON CONFLICT (id) DO NOTHING;

-- Create view for backward compatibility (optional, for gradual migration)
CREATE OR REPLACE VIEW lte.doc_embeddings_compat AS
SELECT 
  id,
  doc_id,
  run_id,
  embedding
FROM lte.model_aware_embeddings
WHERE model_key = 'default' AND embedding_dim = 384;

-- Add comments for documentation
COMMENT ON TABLE lte.model_aware_embeddings IS 'Model-aware embedding storage with dynamic dimensions';
COMMENT ON COLUMN lte.model_aware_embeddings.model_key IS 'Model identifier (e.g., default, qwen3, minilm)';
COMMENT ON COLUMN lte.model_aware_embeddings.embedding_dim IS 'Embedding dimension for this model';
COMMENT ON COLUMN lte.model_aware_embeddings.embedding IS 'Vector embedding with dynamic dimension';
