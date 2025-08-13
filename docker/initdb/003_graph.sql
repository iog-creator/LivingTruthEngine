-- Phase 9.3: Cross-Document Linking & Evidence Graph Schema
-- Creates tables for entity extraction, claim analysis, and cross-document linking
-- Includes pgvector support for document and claim embeddings

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS lte;

-- Documents table (extends existing structure)
CREATE TABLE IF NOT EXISTS lte.documents (
    id SERIAL PRIMARY KEY,
    run_id UUID NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- 'youtube', 'web', 'pdf'
    uri TEXT,
    title TEXT,
    published_at TIMESTAMP,
    shard_no INTEGER DEFAULT 1,
    text_len INTEGER,
    sha256 VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(run_id, source_type, uri, shard_no)
);

-- Entities extracted from documents
CREATE TABLE IF NOT EXISTS lte.entities (
    id SERIAL PRIMARY KEY,
    doc_id INTEGER REFERENCES lte.documents(id) ON DELETE CASCADE,
    type VARCHAR(100) NOT NULL, -- 'person', 'organization', 'location', 'date', 'event'
    value TEXT NOT NULL,
    span_start INTEGER,
    span_end INTEGER,
    conf DECIMAL(3,2) DEFAULT 1.0, -- confidence score 0.0-1.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Claims extracted from documents
CREATE TABLE IF NOT EXISTS lte.claims (
    id SERIAL PRIMARY KEY,
    doc_id INTEGER REFERENCES lte.documents(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    normalized TEXT, -- normalized form for comparison
    conf DECIMAL(3,2) DEFAULT 1.0, -- confidence score 0.0-1.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Entity links across documents
CREATE TABLE IF NOT EXISTS lte.entity_links (
    id SERIAL PRIMARY KEY,
    left_entity_id INTEGER REFERENCES lte.entities(id) ON DELETE CASCADE,
    right_entity_id INTEGER REFERENCES lte.entities(id) ON DELETE CASCADE,
    link_type VARCHAR(100) NOT NULL, -- 'same_as', 'related_to', 'part_of', 'located_in'
    score DECIMAL(3,2) DEFAULT 1.0, -- similarity/link strength 0.0-1.0
    method VARCHAR(50) NOT NULL, -- 'block+rerank', 'vector_similarity', 'rule_based'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(left_entity_id, right_entity_id, link_type)
);

-- Claim links across documents
CREATE TABLE IF NOT EXISTS lte.claim_links (
    id SERIAL PRIMARY KEY,
    left_claim_id INTEGER REFERENCES lte.claims(id) ON DELETE CASCADE,
    right_claim_id INTEGER REFERENCES lte.claims(id) ON DELETE CASCADE,
    link_type VARCHAR(100) NOT NULL, -- 'corroborates', 'contradicts', 'elaborates', 'similar'
    score DECIMAL(3,2) DEFAULT 1.0, -- similarity/link strength 0.0-1.0
    method VARCHAR(50) NOT NULL, -- 'block+rerank', 'vector_similarity', 'rule_based'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(left_claim_id, right_claim_id, link_type)
);

-- Document embeddings (Phase 9.3 - with pgvector support)
CREATE TABLE IF NOT EXISTS lte.doc_embeddings (
    doc_id INTEGER PRIMARY KEY REFERENCES lte.documents(id) ON DELETE CASCADE,
    embedding vector(768), -- 768-dimensional embeddings
    model VARCHAR(100) NOT NULL, -- embedding model name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Claim embeddings (Phase 9.3 - with pgvector support)
CREATE TABLE IF NOT EXISTS lte.claim_embeddings (
    claim_id INTEGER PRIMARY KEY REFERENCES lte.claims(id) ON DELETE CASCADE,
    embedding vector(768), -- 768-dimensional embeddings
    model VARCHAR(100) NOT NULL, -- embedding model name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Graph snapshots for UI caching
CREATE TABLE IF NOT EXISTS lte.graph_snapshots (
    id SERIAL PRIMARY KEY,
    run_id UUID NOT NULL,
    payload_json JSONB NOT NULL, -- complete graph structure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_documents_run_id ON lte.documents(run_id);
CREATE INDEX IF NOT EXISTS idx_documents_source_type ON lte.documents(source_type);
CREATE INDEX IF NOT EXISTS idx_documents_sha256 ON lte.documents(sha256);

CREATE INDEX IF NOT EXISTS idx_entities_doc_id ON lte.entities(doc_id);
CREATE INDEX IF NOT EXISTS idx_entities_type ON lte.entities(type);
CREATE INDEX IF NOT EXISTS idx_entities_value ON lte.entities(value);

CREATE INDEX IF NOT EXISTS idx_claims_doc_id ON lte.claims(doc_id);
CREATE INDEX IF NOT EXISTS idx_claims_normalized ON lte.claims(normalized);

CREATE INDEX IF NOT EXISTS idx_entity_links_left ON lte.entity_links(left_entity_id);
CREATE INDEX IF NOT EXISTS idx_entity_links_right ON lte.entity_links(right_entity_id);
CREATE INDEX IF NOT EXISTS idx_entity_links_type ON lte.entity_links(link_type);

CREATE INDEX IF NOT EXISTS idx_claim_links_left ON lte.claim_links(left_claim_id);
CREATE INDEX IF NOT EXISTS idx_claim_links_right ON lte.claim_links(right_claim_id);
CREATE INDEX IF NOT EXISTS idx_claim_links_type ON lte.claim_links(link_type);

-- pgvector indexes for similarity search
CREATE INDEX IF NOT EXISTS idx_doc_embeddings_ivfflat ON lte.doc_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_claim_embeddings_ivfflat ON lte.claim_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Graph snapshot index
CREATE INDEX IF NOT EXISTS idx_graph_snapshots_run_id ON lte.graph_snapshots(run_id);

-- Comments for documentation
COMMENT ON TABLE lte.documents IS 'Documents ingested from various sources with metadata';
COMMENT ON TABLE lte.entities IS 'Named entities extracted from documents using NER';
COMMENT ON TABLE lte.claims IS 'Claims and assertions extracted from documents';
COMMENT ON TABLE lte.entity_links IS 'Cross-document entity relationships and links';
COMMENT ON TABLE lte.claim_links IS 'Cross-document claim relationships and links';
COMMENT ON TABLE lte.doc_embeddings IS 'Vector embeddings for documents using pgvector';
COMMENT ON TABLE lte.claim_embeddings IS 'Vector embeddings for claims using pgvector';
COMMENT ON TABLE lte.graph_snapshots IS 'Cached graph structures for UI rendering';
