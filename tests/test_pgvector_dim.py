"""
Test pgvector dimension SSOT integration
Verifies that embedding dimensions come from model registry instead of hard-coded values
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from storage.pgvector_store import PgVectorStore
from common.model_registry import ModelRegistry


class TestPgVectorDimensionSSOT:
    """Test that pgvector store uses SSOT dimensions from model registry"""

    def test_embedding_config_loaded_from_registry(self):
        """Test that embedding config is loaded from model registry on initialization"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            
            # Mock the embedder
            mock_embedder = Mock()
            mock_embedder.encode.return_value = [0.1] * 384  # 384-dim vector
            
            store = PgVectorStore("fake_dsn", embedder=mock_embedder)
            
            # Verify that embedding dimension was loaded from registry
            assert store._embedding_dim == 384  # From models.toml
            assert store._model_key == 'default'

    def test_embedding_dimension_validation(self):
        """Test that embedding dimension validation works correctly"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            
            mock_embedder = Mock()
            store = PgVectorStore("fake_dsn", embedder=mock_embedder)
            
            # Test valid dimension
            valid_embedding = np.array([0.1] * 384)
            assert store._validate_embedding_dimension(valid_embedding) is True
            
            # Test invalid dimension
            invalid_embedding = np.array([0.1] * 768)  # Wrong dimension
            assert store._validate_embedding_dimension(invalid_embedding) is False

    def test_upsert_docs_validates_dimensions(self):
        """Test that upsert_docs validates embedding dimensions"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            mock_embedder = Mock()
            mock_embedder.encode.return_value = [0.1] * 384  # Valid dimension
            
            store = PgVectorStore("fake_dsn", embedder=mock_embedder)
            
            docs = [{"id": "test1", "text": "test document", "source_type": "web"}]
            
            # Should not raise error with valid dimensions
            store.upsert_docs("test_run", docs)
            
            # Verify that the correct dimension was used in the SQL
            call_args = mock_cursor.execute.call_args_list
            embedding_call = None
            for call in call_args:
                if 'INSERT INTO lte.doc_embeddings' in str(call):
                    embedding_call = call
                    break
            
            assert embedding_call is not None
            # Check that dim=384 was passed in the parameters tuple
            args, kwargs = embedding_call
            params = args[1]  # Get the parameters tuple
            # The dimension should be the last parameter
            assert params[-1] == 384  # Check the last parameter is the dimension

    def test_upsert_docs_rejects_invalid_dimensions(self):
        """Test that upsert_docs rejects embeddings with wrong dimensions"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            
            mock_embedder = Mock()
            mock_embedder.encode.return_value = [0.1] * 768  # Wrong dimension
            
            store = PgVectorStore("fake_dsn", embedder=mock_embedder)
            
            docs = [{"id": "test1", "text": "test document", "source_type": "web"}]
            
            # Should raise error with invalid dimensions
            with pytest.raises(ValueError, match="Embedding dimension validation failed"):
                store.upsert_docs("test_run", docs)

    def test_search_validates_query_dimensions(self):
        """Test that search validates query embedding dimensions"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            mock_cursor = Mock()
            mock_cursor.fetchall.return_value = []
            mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            mock_embedder = Mock()
            mock_embedder.encode.return_value = [0.1] * 384  # Valid dimension
            
            store = PgVectorStore("fake_dsn", embedder=mock_embedder)
            
            # Should not raise error with valid dimensions
            results = store.search("test_run", "test query")
            assert results == []

    def test_search_rejects_invalid_query_dimensions(self):
        """Test that search rejects queries with wrong dimensions"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            
            mock_embedder = Mock()
            mock_embedder.encode.return_value = [0.1] * 768  # Wrong dimension
            
            store = PgVectorStore("fake_dsn", embedder=mock_embedder)
            
            # Should raise error with invalid dimensions
            with pytest.raises(ValueError, match="Query embedding dimension validation failed"):
                store.search("test_run", "test query")

    def test_store_claim_embedding_validates_dimensions(self):
        """Test that store_claim_embedding validates dimensions"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            
            store = PgVectorStore("fake_dsn")
            
            # Valid embedding
            valid_embedding = np.array([0.1] * 384)
            store.store_claim_embedding(1, valid_embedding)
            
            # Verify that the correct dimension was used
            call_args = mock_cursor.execute.call_args_list
            embedding_call = None
            for call in call_args:
                if 'INSERT INTO lte.claim_embeddings' in str(call):
                    embedding_call = call
                    break
            
            assert embedding_call is not None
            # Check that dim=384 was passed in the parameters tuple
            args, kwargs = embedding_call
            assert 384 in args[1]  # Check the parameters tuple (second element)

    def test_store_claim_embedding_rejects_invalid_dimensions(self):
        """Test that store_claim_embedding rejects wrong dimensions"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            
            store = PgVectorStore("fake_dsn")
            
            # Invalid embedding
            invalid_embedding = np.array([0.1] * 768)
            
            with pytest.raises(ValueError, match="Claim embedding dimension validation failed"):
                store.store_claim_embedding(1, invalid_embedding)

    def test_model_registry_integration(self):
        """Test that model registry provides correct embedding dimensions"""
        reg = ModelRegistry()
        embedding_spec = reg.embedding()
        
        # Verify that the embedding spec has the expected dimension
        assert embedding_spec.extra.get('dim') == 384  # From models.toml
        assert embedding_spec.name == "sentence-transformers/all-MiniLM-L6-v2"

    def test_no_hardcoded_dimensions(self):
        """Test that no hard-coded dimensions like 768 are used"""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.autocommit = True
            
            store = PgVectorStore("fake_dsn")
            
            # Verify that the dimension comes from model registry, not hard-coded
            assert store._embedding_dim == 384  # From models.toml, not hard-coded 768
            assert store._embedding_dim is not None
            assert store._embedding_dim != 768  # Should not be hard-coded 768
