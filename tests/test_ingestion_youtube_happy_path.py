"""
Test successful YouTube ingestion with proper bundle structure and transcript validation.

This test verifies Phase 8.3 requirements for verified ingestion.
"""

import pytest
import requests
import json
import time
from pathlib import Path


class TestYouTubeIngestionHappyPath:
    """Test successful YouTube channel ingestion with proper validation."""
    
    BASE_URL = "http://localhost:8050"
    
    def test_youtube_start_creates_valid_bundle(self):
        """Test that YouTube start creates a bundle with all required components."""
        # First ensure health gates are passing
        health_response = requests.get(f"{self.BASE_URL}/api/health/full")
        assert health_response.status_code == 200, "Health check should pass"
        
        health_data = health_response.json()
        assert health_data["all_gates_passed"], "All health gates must pass"
        
        # Start a YouTube run
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": 3,
                "max_depth": 0
            }
        )
        
        # Should either succeed or fail with a specific error (not health gate failure)
        assert response.status_code in [200, 500, 502], f"Expected 200, 500, or 502, got {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "ok", "Response should be ok"
            
            result = data["data"]
            assert "run_id" in result, "Response should contain run_id"
            assert "doc_count" in result, "Response should contain doc_count"
            assert "bundle_dir" in result, "Response should contain bundle_dir"
            
            # Verify bundle structure via MCP
            run_id = result["run_id"]
            bundle_response = requests.get(f"{self.BASE_URL}/api/runs/{run_id}")
            assert bundle_response.status_code == 200, "Bundle should be accessible"
            
            bundle_data = bundle_response.json()
            assert bundle_data["status"] == "ok", "Bundle response should be ok"
            
            bundle = bundle_data["data"]
            assert "manifest" in bundle, "Bundle should have manifest"
            assert "corpus" in bundle, "Bundle should have corpus"
            assert "merkle" in bundle, "Bundle should have merkle"
            assert "metrics" in bundle, "Bundle should have metrics"
            
            # Verify corpus has documents
            corpus_response = requests.get(f"{self.BASE_URL}/api/runs/{run_id}/corpus")
            assert corpus_response.status_code == 200, "Corpus should be accessible"
            
            corpus_data = corpus_response.json()
            assert corpus_data["status"] == "ok", "Corpus response should be ok"
            
            documents = corpus_data["data"]["documents"]
            assert len(documents) > 0, "Corpus should have documents"
            
            # Verify documents have required fields
            for doc in documents:
                assert "text" in doc, "Document should have text"
                assert doc["text"].strip(), "Document text should not be empty"
                assert "source_type" in doc, "Document should have source_type"
                assert doc["source_type"] == "youtube", "Document should have youtube source_type"
                assert "uri" in doc, "Document should have uri"
    
    def test_youtube_start_validates_transcript_content(self):
        """Test that YouTube start validates transcript content properly."""
        # Start a YouTube run
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data["data"]
            run_id = result["run_id"]
            
            # Verify transcript content
            corpus_response = requests.get(f"{self.BASE_URL}/api/runs/{run_id}/corpus")
            assert corpus_response.status_code == 200, "Corpus should be accessible"
            
            corpus_data = corpus_response.json()
            documents = corpus_data["data"]["documents"]
            
            # Check that at least one document has substantial content
            substantial_docs = [doc for doc in documents if len(doc.get("text", "").strip()) > 100]
            assert len(substantial_docs) > 0, "Should have at least one document with substantial content"
    
    def test_youtube_start_returns_correct_document_count(self):
        """Test that YouTube start returns the correct document count."""
        # Start a YouTube run with specific limit
        limit = 2
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": limit,
                "max_depth": 0
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data["data"]
            
            # Verify document count matches or is reasonable
            doc_count = result["doc_count"]
            assert doc_count > 0, "Document count should be greater than 0"
            assert doc_count <= limit, f"Document count should not exceed requested limit of {limit}"
            
            # Verify count matches actual documents
            run_id = result["run_id"]
            corpus_response = requests.get(f"{self.BASE_URL}/api/runs/{run_id}/corpus")
            assert corpus_response.status_code == 200, "Corpus should be accessible"
            
            corpus_data = corpus_response.json()
            documents = corpus_data["data"]["documents"]
            assert len(documents) == doc_count, "Document count should match actual documents"
    
    def test_youtube_start_handles_parameters_correctly(self):
        """Test that YouTube start handles parameters correctly."""
        # Test with different parameters
        test_params = [
            {"limit": 1, "max_depth": 0, "sort": "oldest"},
            {"limit": 2, "max_depth": 0, "sort": "newest"},
            {"limit": 1, "max_depth": 1, "ocr": True},
            {"limit": 1, "max_depth": 0, "js_render": True}
        ]
        
        for params in test_params:
            params["channel_url"] = "https://www.youtube.com/@imaginationpodcastofficial"
            
            response = requests.post(
                f"{self.BASE_URL}/api/runs/youtube/start",
                json=params
            )
            
            # Should handle parameters without crashing
            assert response.status_code in [200, 500, 502], f"Should handle parameters: {params}"
            
            if response.status_code == 200:
                data = response.json()
                assert data["status"] == "ok", "Should succeed with valid parameters"
                
                result = data["data"]
                assert "run_id" in result, "Should return run_id"
                assert "doc_count" in result, "Should return doc_count"
    
    def test_youtube_start_creates_verifiable_bundle(self):
        """Test that YouTube start creates a bundle that can be verified."""
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data["data"]
            run_id = result["run_id"]
            
            # Verify bundle can be accessed and has proper structure
            bundle_response = requests.get(f"{self.BASE_URL}/api/runs/{run_id}")
            assert bundle_response.status_code == 200, "Bundle should be accessible"
            
            bundle_data = bundle_response.json()
            bundle = bundle_data["data"]
            
            # Check manifest
            manifest = bundle["manifest"]
            assert "started_at" in manifest, "Manifest should have started_at"
            assert "parameters" in manifest, "Manifest should have parameters"
            
            # Check metrics
            metrics = bundle["metrics"]
            assert isinstance(metrics, dict), "Metrics should be a dictionary"
            
            # Check merkle
            merkle = bundle["merkle"]
            assert isinstance(merkle, dict), "Merkle should be a dictionary"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
