"""
Test that health gates properly prevent runs from starting when dependencies are unhealthy.

This test verifies Phase 8.3 requirements for health gate enforcement.
"""

import pytest
import requests
import json
import time
from pathlib import Path


class TestHealthGates:
    """Test that health gates properly block runs when dependencies are unhealthy."""
    
    BASE_URL = "http://localhost:8050"
    
    def test_health_gates_structure(self):
        """Test that health gates return the expected structure."""
        response = requests.get(f"{self.BASE_URL}/api/health/full")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Check required fields
        assert "status" in data, "Response should have status"
        assert "service" in data, "Response should have service"
        assert "gates" in data, "Response should have gates"
        assert "all_gates_passed" in data, "Response should have all_gates_passed"
        
        # Check that status is either "healthy" or "unhealthy"
        assert data["status"] in ["healthy", "unhealthy"], f"Status should be healthy or unhealthy, got {data['status']}"
        
        # Check that service is correct
        assert data["service"] == "unified_dashboard", f"Service should be unified_dashboard, got {data['service']}"
        
        # Check that all_gates_passed is boolean
        assert isinstance(data["all_gates_passed"], bool), "all_gates_passed should be boolean"
    
    def test_required_gates_present(self):
        """Test that all required health gates are present."""
        response = requests.get(f"{self.BASE_URL}/api/health/full")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        gates = data["gates"]
        
        # Check that all required gates are present
        required_gates = ["mcp_hub", "veritas_tools", "langflow", "lm_studio", "neo4j", "redis"]
        for gate in required_gates:
            assert gate in gates, f"Missing required gate: {gate}"
            assert isinstance(gates[gate], bool), f"Gate {gate} should be boolean"
    
    def test_errors_field_structure(self):
        """Test that errors field has correct structure when gates fail."""
        response = requests.get(f"{self.BASE_URL}/api/health/full")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        if not data["all_gates_passed"]:
            # When gates fail, errors should be present
            assert "errors" in data, "Should have errors when gates fail"
            assert isinstance(data["errors"], dict), "Errors should be a dictionary"
            
            # Check that failed gates have error messages
            for gate, passed in data["gates"].items():
                if not passed:
                    assert gate in data["errors"], f"Failed gate {gate} should have error message"
                    assert isinstance(data["errors"][gate], str), f"Error for gate {gate} should be string"
        else:
            # When all gates pass, errors should be empty
            assert "errors" in data, "Should have errors field even when all gates pass"
            assert data["errors"] == {}, "Errors should be empty when all gates pass"
    
    def test_youtube_start_blocks_on_health_gate_failure(self):
        """Test that YouTube start endpoint blocks when health gates fail."""
        # First check current health status
        health_response = requests.get(f"{self.BASE_URL}/api/health/full")
        assert health_response.status_code == 200, "Health check should work"
        
        health_data = health_response.json()
        
        if not health_data["all_gates_passed"]:
            # If health gates are failing, YouTube start should return 503
            response = requests.post(
                f"{self.BASE_URL}/api/runs/youtube/start",
                json={
                    "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                    "limit": 1,
                    "max_depth": 0
                }
            )
            
            assert response.status_code == 503, f"Expected 503 when health gates fail, got {response.status_code}"
            
            data = response.json()
            assert "detail" in data, "503 response should have detail"
            assert data["detail"]["error"]["code"] == "HEALTH_GATES_FAILED", "Should be HEALTH_GATES_FAILED error"
            assert "failed_gates" in data["detail"]["error"], "Should list failed gates"
            assert "gate_errors" in data["detail"]["error"], "Should list gate errors"
        else:
            # If health gates are passing, YouTube start should either succeed or fail for other reasons
            response = requests.post(
                f"{self.BASE_URL}/api/runs/youtube/start",
                json={
                    "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                    "limit": 1,
                    "max_depth": 0
                }
            )
            
            # Should not be 503 due to health gates
            assert response.status_code != 503 or "HEALTH_GATES_FAILED" not in response.text, "Should not fail due to health gates when they pass"
    
    def test_health_gates_timeout(self):
        """Test that health gates have reasonable timeout behavior."""
        start_time = time.time()
        response = requests.get(f"{self.BASE_URL}/api/health/full", timeout=10)
        end_time = time.time()
        
        assert response.status_code == 200, "Health check should complete"
        assert end_time - start_time < 5, "Health check should complete within 5 seconds"
    
    def test_individual_gate_validation(self):
        """Test that individual gates provide meaningful error messages."""
        response = requests.get(f"{self.BASE_URL}/api/health/full")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        
        # Check that failed gates have descriptive error messages
        for gate, passed in data["gates"].items():
            if not passed:
                assert gate in data["errors"], f"Failed gate {gate} should have error message"
                error_msg = data["errors"][gate]
                assert len(error_msg) > 0, f"Error message for gate {gate} should not be empty"
                assert isinstance(error_msg, str), f"Error message for gate {gate} should be string"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
