-- Phase 9.5.1: Model-Aware Embedding Storage Migration (Simplified)
-- This migration works with the current schema and focuses on model awareness

-- Add model_key and embedding_dim columns to existing doc_embeddings table
ALTER TABLE lte.doc_embeddings 
ADD COLUMN IF NOT EXISTS model_key TEXT DEFAULT 'default',
ADD COLUMN IF NOT EXISTS embedding_dim INTEGER DEFAULT 384;

-- Create index for efficient querying by model and dimension
CREATE INDEX IF NOT EXISTS idx_doc_embeddings_model_dim 
ON lte.doc_embeddings(model_key, embedding_dim);

-- Create index for run_id queries
CREATE INDEX IF NOT EXISTS idx_doc_embeddings_run_id 
ON lte.doc_embeddings(doc_id) WHERE doc_id IS NOT NULL;

-- Add comments for documentation
COMMENT ON COLUMN lte.doc_embeddings.model_key IS 'Model identifier (e.g., default, qwen3, minilm)';
COMMENT ON COLUMN lte.doc_embeddings.embedding_dim IS 'Embedding dimension for this model';

-- Create a view for backward compatibility
CREATE OR REPLACE VIEW lte.doc_embeddings_compat AS
SELECT 
  doc_id,
  embedding_text,
  model,
  created_at
FROM lte.doc_embeddings
WHERE model_key = 'default' AND embedding_dim = 384;

-- Update existing records to have proper model_key and embedding_dim
UPDATE lte.doc_embeddings 
SET model_key = 'default', embedding_dim = 384 
WHERE model_key IS NULL OR embedding_dim IS NULL;
