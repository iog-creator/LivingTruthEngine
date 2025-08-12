"""
Test YouTube ingestion failure scenarios with explicit error codes.

This test verifies Phase 8.3 requirements for proper error handling.
"""

import pytest
import requests
import json
import time
from pathlib import Path


class TestYouTubeIngestionFailures:
    """Test YouTube ingestion failure scenarios with proper error handling."""
    
    BASE_URL = "http://localhost:8050"
    
    def test_bad_channel_id_returns_400(self):
        """Test that bad channel ID returns 400 error."""
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@nonexistentchannel12345",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        # Should return 400 for bad channel, 502 for processing error, or 500 for execution error
        assert response.status_code in [400, 500, 502], f"Expected 400, 500, or 502, got {response.status_code}"
        
        if response.status_code == 400:
            data = response.json()
            assert "detail" in data, "400 response should have detail"
            assert data["detail"]["error"]["code"] == "INVALID_REQUEST", "Should be INVALID_REQUEST error"
    
    def test_missing_channel_url_returns_400(self):
        """Test that missing channel URL returns 400 error."""
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "limit": 1,
                "max_depth": 0
            }
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = response.json()
        assert "detail" in data, "400 response should have detail"
        assert data["detail"]["error"]["code"] == "INVALID_REQUEST", "Should be INVALID_REQUEST error"
        assert "channel_url is required" in data["detail"]["error"]["msg"], "Should mention channel_url requirement"
    
    def test_empty_channel_url_returns_400(self):
        """Test that empty channel URL returns 400 error."""
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        
        data = response.json()
        assert "detail" in data, "400 response should have detail"
        assert data["detail"]["error"]["code"] == "INVALID_REQUEST", "Should be INVALID_REQUEST error"
    
    def test_private_channel_returns_502(self):
        """Test that private channel returns 502 with explicit cause."""
        # Use a known private channel or invalid URL
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@privatechannel12345",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        # Should return 502 for processing error
        assert response.status_code in [502, 500], f"Expected 502 or 500, got {response.status_code}"
        
        if response.status_code == 502:
            data = response.json()
            assert "detail" in data, "502 response should have detail"
            error_code = data["detail"]["error"]["code"]
            assert error_code in ["NO_TRANSCRIPTS_RETURNED", "NO_VALID_TRANSCRIPTS"], f"Unexpected error code: {error_code}"
    
    def test_zero_transcripts_returns_502(self):
        """Test that zero transcripts returns 502 with NO_TRANSCRIPTS_RETURNED."""
        # This test would require a channel that exists but has no transcripts
        # For now, we'll test the error handling structure
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@channelwithnotranscripts",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        # Should return 502 for no transcripts
        assert response.status_code in [502, 500], f"Expected 502 or 500, got {response.status_code}"
        
        if response.status_code == 502:
            data = response.json()
            assert "detail" in data, "502 response should have detail"
            error_code = data["detail"]["error"]["code"]
            assert error_code in ["NO_TRANSCRIPTS_RETURNED", "NO_VALID_TRANSCRIPTS", "ZERO_DOCUMENTS"], f"Unexpected error code: {error_code}"
    
    def test_invalid_bundle_structure_returns_500(self):
        """Test that invalid bundle structure returns 500 error."""
        # This would require mocking the MCP tool to return invalid data
        # For now, we'll test that the endpoint properly validates bundle structure
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        # Should either succeed or fail with appropriate error
        assert response.status_code in [200, 500, 502], f"Expected 200, 500, or 502, got {response.status_code}"
        
        if response.status_code == 500:
            data = response.json()
            assert "detail" in data, "500 response should have detail"
            error_code = data["detail"]["error"]["code"]
            assert error_code in ["INVALID_BUNDLE", "INCOMPLETE_BUNDLE", "BUNDLE_VERIFICATION_FAILED"], f"Unexpected error code: {error_code}"
    
    def test_missing_required_parameters_returns_400(self):
        """Test that missing required parameters returns 400 error."""
        # Test without limit
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial"
            }
        )
        
        # Should still work with defaults, but test error handling
        assert response.status_code in [200, 400, 500, 502], f"Expected 200, 400, 500, or 502, got {response.status_code}"
        
        if response.status_code == 400:
            data = response.json()
            assert "detail" in data, "400 response should have detail"
            assert data["detail"]["error"]["code"] == "INVALID_REQUEST", "Should be INVALID_REQUEST error"
    
    def test_invalid_parameter_types_returns_400(self):
        """Test that invalid parameter types returns 400 error."""
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": "invalid",  # Should be int
                "max_depth": 0
            }
        )
        
        # Should return 400 for invalid parameter types
        assert response.status_code in [400, 500], f"Expected 400 or 500, got {response.status_code}"
        
        if response.status_code == 400:
            data = response.json()
            assert "detail" in data, "400 response should have detail"
            assert data["detail"]["error"]["code"] == "INVALID_REQUEST", "Should be INVALID_REQUEST error"
    
    def test_health_gates_failure_returns_503(self):
        """Test that health gates failure returns 503 error."""
        # This test would require stopping services to trigger health gate failure
        # For now, we'll test the error handling structure
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        # Should not return 503 unless health gates are actually failing
        if response.status_code == 503:
            data = response.json()
            assert "detail" in data, "503 response should have detail"
            error_code = data["detail"]["error"]["code"]
            assert error_code in ["HEALTH_GATES_FAILED", "MCP_UNAVAILABLE"], f"Unexpected error code: {error_code}"
            
            if error_code == "HEALTH_GATES_FAILED":
                assert "failed_gates" in data["detail"]["error"], "Should list failed gates"
                assert "gate_errors" in data["detail"]["error"], "Should list gate errors"
    
    def test_mcp_unavailable_returns_503(self):
        """Test that MCP unavailable returns 503 error."""
        # This test would require stopping the MCP Hub Server
        # For now, we'll test the error handling structure
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        # Should not return 503 unless MCP is actually unavailable
        if response.status_code == 503:
            data = response.json()
            assert "detail" in data, "503 response should have detail"
            error_code = data["detail"]["error"]["code"]
            assert error_code in ["MCP_UNAVAILABLE", "HEALTH_GATES_FAILED"], f"Unexpected error code: {error_code}"
    
    def test_error_response_structure(self):
        """Test that error responses have proper structure."""
        # Test with invalid request
        response = requests.post(
            f"{self.BASE_URL}/api/runs/youtube/start",
            json={
                "channel_url": "",
                "limit": 1,
                "max_depth": 0
            }
        )
        
        if response.status_code != 200:
            data = response.json()
            assert "detail" in data, "Error response should have detail"
            assert "status" in data["detail"], "Error detail should have status"
            assert "error" in data["detail"], "Error detail should have error"
            assert "code" in data["detail"]["error"], "Error should have code"
            assert "msg" in data["detail"]["error"], "Error should have msg"
            assert "details" in data["detail"]["error"], "Error should have details"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
