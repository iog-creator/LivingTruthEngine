-- Phase 9.3.1: Safe migration for SSOT-driven embedding dimensions
-- This migration makes embedding dimensions configurable via model registry
-- instead of hard-coded values like 768

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS lte;

-- Add model_key and dim columns to embedding tables for SSOT tracking
ALTER TABLE IF EXISTS lte.doc_embeddings 
ADD COLUMN IF NOT EXISTS model_key VARCHAR(100) DEFAULT 'default',
ADD COLUMN IF NOT EXISTS dim INTEGER;

ALTER TABLE IF EXISTS lte.claim_embeddings 
ADD COLUMN IF NOT EXISTS model_key VARCHAR(100) DEFAULT 'default',
ADD COLUMN IF NOT EXISTS dim INTEGER;

-- Add comments for documentation
COMMENT ON COLUMN lte.doc_embeddings.model_key IS 'Model registry key (SSOT) for embedding model';
COMMENT ON COLUMN lte.doc_embeddings.dim IS 'Embedding dimension from model registry (SSOT)';
COMMENT ON COLUMN lte.claim_embeddings.model_key IS 'Model registry key (SSOT) for embedding model';
COMMENT ON COLUMN lte.claim_embeddings.dim IS 'Embedding dimension from model registry (SSOT)';

-- Create indexes for model-aware queries
CREATE INDEX IF NOT EXISTS idx_doc_embeddings_model_key ON lte.doc_embeddings(model_key);
CREATE INDEX IF NOT EXISTS idx_claim_embeddings_model_key ON lte.claim_embeddings(model_key);

-- Add constraint to ensure dim is always set (enforced by application)
-- Note: We don't add NOT NULL constraint here as existing data might not have dim
-- The application will enforce this for new inserts
