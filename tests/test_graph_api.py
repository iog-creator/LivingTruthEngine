#!/usr/bin/env python3
"""
Tests for Phase 9.3: Graph API Endpoints
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.dashboard.unified_dashboard import UnifiedDashboard


class TestGraphAPI:
    """Test the graph API endpoints."""
    
    @pytest.fixture
    def dashboard(self):
        """Create dashboard instance for testing."""
        return UnifiedDashboard()
    
    @pytest.fixture
    def client(self, dashboard):
        """Create test client."""
        return TestClient(dashboard.app)
    
    @pytest.fixture
    def mock_health_gate(self):
        """Mock health gate to return True."""
        with patch('src.dashboard.unified_dashboard._health_gate', return_value=True):
            yield
    
    def test_get_graph_endpoint(self, client, mock_health_gate):
        """Test GET /api/graph/{run_id} endpoint."""
        # Mock pgvector store
        with patch('src.storage.pgvector_store.PgVectorStore') as mock_store:
            mock_instance = Mock()
            mock_instance.get_graph_snapshot.return_value = {
                "run_id": "test-run",
                "nodes": {"documents": [], "entities": [], "claims": []},
                "edges": {"entity_links": [], "claim_links": []}
            }
            mock_store.return_value = mock_instance
            
            response = client.get("/api/graph/test-run")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert "data" in data
            assert data["data"]["run_id"] == "test-run"
    
    def test_get_graph_not_found(self, client, mock_health_gate):
        """Test GET /api/graph/{run_id} with non-existent run."""
        # Mock pgvector store returning None
        with patch('src.storage.pgvector_store.PgVectorStore') as mock_store:
            mock_instance = Mock()
            mock_instance.get_graph_snapshot.return_value = None
            mock_store.return_value = mock_instance
            
            response = client.get("/api/graph/non-existent-run")
            
            assert response.status_code == 200  # FastAPI returns 200 for envelope errors
            data = response.json()
            assert data["status"] == "error"
            assert "error" in data
            assert data["error"]["code"] == 404
    
    def test_build_graph_endpoint(self, client, mock_health_gate):
        """Test POST /api/graph/{run_id}/build endpoint."""
        # Mock components
        with patch('src.analysis.linking_pipeline.LinkingPipeline') as mock_pipeline_class:
            with patch('src.storage.pgvector_store.PgVectorStore') as mock_store:
                # Mock store
                mock_store_instance = Mock()
                mock_store_instance.get_documents_by_run.return_value = [
                    {"id": 1, "title": "Test Document"}
                ]
                mock_store.return_value = mock_store_instance
                
                # Mock pipeline
                mock_pipeline_instance = Mock()
                mock_pipeline_instance.process_run.return_value = {
                    "run_id": "test-run",
                    "status": "completed",
                    "documents_processed": 1
                }
                mock_pipeline_class.return_value = mock_pipeline_instance
                
                response = client.post("/api/graph/test-run/build")
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "ok"
                assert "data" in data
                assert data["data"]["run_id"] == "test-run"
    
    def test_build_graph_no_documents(self, client, mock_health_gate):
        """Test POST /api/graph/{run_id}/build with no documents."""
        # Mock store returning empty documents
        with patch('src.storage.pgvector_store.PgVectorStore') as mock_store:
            mock_instance = Mock()
            mock_instance.get_documents_by_run.return_value = []
            mock_store.return_value = mock_instance
            
            response = client.post("/api/graph/test-run/build")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "error"
            assert "error" in data
            assert data["error"]["code"] == 404
    
    def test_build_graph_pipeline_failure(self, client, mock_health_gate):
        """Test POST /api/graph/{run_id}/build with pipeline failure."""
        # Mock components
        with patch('src.analysis.linking_pipeline.LinkingPipeline') as mock_pipeline_class:
            with patch('src.storage.pgvector_store.PgVectorStore') as mock_store:
                # Mock store
                mock_store_instance = Mock()
                mock_store_instance.get_documents_by_run.return_value = [
                    {"id": 1, "title": "Test Document"}
                ]
                mock_store.return_value = mock_store_instance
                
                # Mock pipeline failure
                mock_pipeline_instance = Mock()
                mock_pipeline_instance.process_run.return_value = {
                    "run_id": "test-run",
                    "status": "failed",
                    "error": "Pipeline error"
                }
                mock_pipeline_class.return_value = mock_pipeline_instance
                
                response = client.post("/api/graph/test-run/build")
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "error"
                assert "error" in data
                assert data["error"]["code"] == 500
    
    def test_get_claims_endpoint(self, client, mock_health_gate):
        """Test GET /api/claims/{run_id} endpoint."""
        # Mock pgvector store
        with patch('src.storage.pgvector_store.PgVectorStore') as mock_store:
            mock_instance = Mock()
            mock_instance.get_claims_by_run.return_value = [
                {"id": 1, "text": "Test claim", "normalized": "test claim", "conf": 0.9}
            ]
            mock_instance.get_claim_links_by_run.return_value = []
            mock_instance.get_graph_snapshot.return_value = {
                "findings": {
                    "corroboration": [
                        {
                            "claim_id": 1,
                            "label": "corroborated",
                            "confidence": 0.85
                        }
                    ]
                }
            }
            mock_store.return_value = mock_instance
            
            response = client.get("/api/claims/test-run")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert "data" in data
            assert "claims" in data["data"]
            assert len(data["data"]["claims"]) == 1
            assert data["data"]["total_claims"] == 1
            
            # Check that corroboration labels are included
            claim = data["data"]["claims"][0]
            assert "corroboration_label" in claim
            assert "corroboration_confidence" in claim
    
    def test_get_entities_endpoint(self, client, mock_health_gate):
        """Test GET /api/entities/{run_id} endpoint."""
        # Mock pgvector store
        with patch('src.storage.pgvector_store.PgVectorStore') as mock_store:
            mock_instance = Mock()
            mock_instance.get_entities_by_run.return_value = [
                {"id": 1, "type": "person", "value": "John Smith", "conf": 0.8}
            ]
            mock_instance.get_entity_links_by_run.return_value = []
            mock_store.return_value = mock_instance
            
            response = client.get("/api/entities/test-run")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert "data" in data
            assert "entities" in data["data"]
            assert len(data["data"]["entities"]) == 1
            assert data["data"]["total_entities"] == 1
    
    def test_health_gate_failure(self, client):
        """Test endpoints with health gate failure."""
        # Mock health gate to return False
        with patch('src.dashboard.unified_dashboard._health_gate', return_value=False):
            # Test graph endpoint
            response = client.get("/api/graph/test-run")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "error"
            assert data["error"]["code"] == 503
            
            # Test build endpoint
            response = client.post("/api/graph/test-run/build")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "error"
            assert data["error"]["code"] == 503
    
    def test_envelope_format(self, client, mock_health_gate):
        """Test that all endpoints return proper envelope format."""
        # Mock successful responses
        with patch('src.storage.pgvector_store.PgVectorStore') as mock_store:
            mock_instance = Mock()
            mock_instance.get_graph_snapshot.return_value = {"run_id": "test-run"}
            mock_instance.get_documents_by_run.return_value = [{"id": 1}]
            mock_instance.get_claims_by_run.return_value = []
            mock_instance.get_entities_by_run.return_value = []
            mock_instance.get_claim_links_by_run.return_value = []
            mock_instance.get_entity_links_by_run.return_value = []
            mock_store.return_value = mock_instance
            
            with patch('src.analysis.linking_pipeline.LinkingPipeline') as mock_pipeline_class:
                mock_pipeline_instance = Mock()
                mock_pipeline_instance.process_run.return_value = {
                    "run_id": "test-run", "status": "completed"
                }
                mock_pipeline_class.return_value = mock_pipeline_instance
                
                # Test all endpoints
                endpoints = [
                    ("GET", "/api/graph/test-run"),
                    ("POST", "/api/graph/test-run/build"),
                    ("GET", "/api/claims/test-run"),
                    ("GET", "/api/entities/test-run")
                ]
                
                for method, endpoint in endpoints:
                    if method == "POST":
                        response = client.post(endpoint)
                    else:
                        response = client.get(endpoint)
                    
                    assert response.status_code == 200
                    data = response.json()
                    
                    # Check envelope format
                    assert "status" in data
                    assert data["status"] in ["ok", "error"]
                    
                    if data["status"] == "ok":
                        assert "data" in data
                        assert "error" not in data or data["error"] is None
                    else:
                        assert "error" in data
                        assert "data" not in data or data["data"] == {}
                        assert "code" in data["error"]
                        assert "message" in data["error"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
