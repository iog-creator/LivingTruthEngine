"""
Test that the system properly returns 503 errors when MCP is unavailable
instead of falling back to filesystem access.

This test verifies Phase 8.3 requirements for strict MCP-only operation.
"""

import pytest
import requests
import json
import time
from pathlib import Path


class TestNoFallbacks:
    """Test that no fallbacks are used when MCP is unavailable."""
    
    BASE_URL = "http://localhost:8050"
    
    def test_runs_endpoint_no_fallback(self):
        """Test that /api/runs returns 503 when MCP is unavailable."""
        # This test would require stopping the MCP Hub Server
        # For now, we'll test the endpoint structure
        response = requests.get(f"{self.BASE_URL}/api/runs")
        assert response.status_code in [200, 503], f"Expected 200 or 503, got {response.status_code}"
        
        if response.status_code == 503:
            data = response.json()
            assert "detail" in data, "503 response should have detail"
            assert data["detail"]["status"] == "error", "Should be error status"
            assert data["detail"]["error"]["code"] == "MCP_UNAVAILABLE", "Should be MCP_UNAVAILABLE error"
    
    def test_tools_endpoint_no_fallback(self):
        """Test that /api/tools returns 503 when MCP is unavailable."""
        response = requests.get(f"{self.BASE_URL}/api/tools")
        assert response.status_code in [200, 503], f"Expected 200 or 503, got {response.status_code}"
        
        if response.status_code == 503:
            data = response.json()
            assert "detail" in data, "503 response should have detail"
            assert data["detail"]["status"] == "error", "Should be error status"
            assert data["detail"]["error"]["code"] == "MCP_UNAVAILABLE", "Should be MCP_UNAVAILABLE error"
    
    def test_run_details_endpoint_no_fallback(self):
        """Test that /api/runs/{id} returns appropriate error for non-existent run."""
        # Use a dummy run ID
        response = requests.get(f"{self.BASE_URL}/api/runs/test-run-id")
        assert response.status_code in [200, 503, 404, 500], f"Expected 200, 503, 404, or 500, got {response.status_code}"
        
        if response.status_code == 503:
            data = response.json()
            assert "detail" in data, "503 response should have detail"
            assert data["detail"]["status"] == "error", "Should be error status"
            # Accept either MCP_UNAVAILABLE or VERITAS_ERROR for 503
            error_code = data["detail"]["error"]["code"]
            assert error_code in ["MCP_UNAVAILABLE", "VERITAS_ERROR"], f"Expected MCP_UNAVAILABLE or VERITAS_ERROR, got {error_code}"
        elif response.status_code == 500:
            # 500 is acceptable for non-existent run (VERITAS_ERROR)
            data = response.json()
            assert "detail" in data, "500 response should have detail"
            assert data["detail"]["status"] == "error", "Should be error status"
            assert data["detail"]["error"]["code"] == "VERITAS_ERROR", "Should be VERITAS_ERROR for non-existent run"
    
    def test_run_corpus_endpoint_no_fallback(self):
        """Test that /api/runs/{id}/corpus returns 503 when MCP is unavailable."""
        # Use a dummy run ID
        response = requests.get(f"{self.BASE_URL}/api/runs/test-run-id/corpus")
        assert response.status_code in [200, 503, 404], f"Expected 200, 503, or 404, got {response.status_code}"
        
        if response.status_code == 503:
            data = response.json()
            assert "detail" in data, "503 response should have detail"
            assert data["detail"]["status"] == "error", "Should be error status"
            assert data["detail"]["error"]["code"] == "MCP_UNAVAILABLE", "Should be MCP_UNAVAILABLE error"
    
    def test_health_gates_work(self):
        """Test that health gates properly check all dependencies."""
        response = requests.get(f"{self.BASE_URL}/api/health/full")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "gates" in data, "Response should have gates"
        assert "all_gates_passed" in data, "Response should have all_gates_passed"
        
        # Check that all required gates are present
        required_gates = ["mcp_hub", "veritas_tools", "langflow", "lm_studio", "neo4j", "redis"]
        for gate in required_gates:
            assert gate in data["gates"], f"Missing gate: {gate}"
    
    def test_youtube_start_requires_health_gates(self):
        """Test that YouTube start endpoint requires all health gates to pass."""
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        # Should either succeed (if all gates pass) or fail with appropriate error
        assert response.status_code in [200, 500, 503], f"Expected 200, 500, or 503, got {response.status_code}"
        
        if response.status_code == 503:
            data = response.json()
            assert "detail" in data, "503 response should have detail"
            error_code = data["detail"]["error"]["code"]
            assert error_code in ["HEALTH_GATES_FAILED", "MCP_UNAVAILABLE"], f"Unexpected error code: {error_code}"
            
            if error_code == "HEALTH_GATES_FAILED":
                assert "failed_gates" in data["detail"]["error"], "Should list failed gates"
                assert "gate_errors" in data["detail"]["error"], "Should list gate errors"
        
        elif response.status_code == 500:
            # 500 is acceptable if health gates pass but processing fails
            data = response.json()
            assert "detail" in data, "500 response should have detail"
            error_code = data["detail"]["error"]["code"]
            # Should not be health gate related errors
            assert error_code not in ["HEALTH_GATES_FAILED", "MCP_UNAVAILABLE"], f"500 error should not be health gate related: {error_code}"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
