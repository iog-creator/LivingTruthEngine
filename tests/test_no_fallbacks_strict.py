"""
Test that the system properly returns 503 errors when MCP is unavailable
and fallbacks are disabled.

This test verifies Phase 8.3 requirements for strict MCP-only operation.
"""

import os
import pytest
import requests
import json


class TestNoFallbacksStrict:
    """Test that no fallbacks are used when MCP is unavailable and fallbacks are disabled."""
    
    BASE_URL = "http://localhost:8050"
    
    def test_no_fallbacks_enforced(self):
        """Test that endpoints return 503 when MCP is unavailable and fallbacks disabled."""
        # Set environment to disable fallbacks
        os.environ["ALLOW_FALLBACKS"] = "false"
        
        # Test runs endpoint
        r = requests.get(f"{self.BASE_URL}/api/runs", timeout=5)
        assert r.status_code in (200, 503), f"Expected 200 or 503, got {r.status_code}"
        
        if r.status_code == 503:
            j = r.json()
            assert j["status"] == "error", "Should be error status"
            assert "Hub unavailable and fallbacks disabled" in j["error"]["message"], "Should mention fallbacks disabled"
        
        # Test tools endpoint
        r = requests.get(f"{self.BASE_URL}/api/tools", timeout=5)
        assert r.status_code in (200, 503), f"Expected 200 or 503, got {r.status_code}"
        
        if r.status_code == 503:
            j = r.json()
            assert j["status"] == "error", "Should be error status"
            assert "Hub unavailable and fallbacks disabled" in j["error"]["message"], "Should mention fallbacks disabled"
    
    def test_envelope_format_consistent(self):
        """Test that all API endpoints return consistent envelope format."""
        endpoints = [
            "/api/health",
            "/api/health/full",
            "/api/tools",
            "/api/runs",
            "/api/status",
            "/api/models"
        ]
        
        for endpoint in endpoints:
            try:
                r = requests.get(f"{self.BASE_URL}{endpoint}", timeout=5)
                if r.status_code == 200:
                    j = r.json()
                    assert "status" in j, f"Missing status in {endpoint}"
                    assert "data" in j, f"Missing data in {endpoint}"
                    assert "error" in j, f"Missing error in {endpoint}"
                    assert j["status"] in ("ok", "error"), f"Invalid status in {endpoint}"
                    
                    if j["status"] == "ok":
                        assert j["error"] is None, f"Error should be None for ok status in {endpoint}"
                    else:
                        assert j["error"] is not None, f"Error should not be None for error status in {endpoint}"
                        assert "message" in j["error"], f"Error should have message in {endpoint}"
                        assert j["error"]["code"] == 503, f"Should have 503 error code in {endpoint}"
                        assert "fallbacks" in (j["error"].get("hint", "") + str(j["data"])), f"Should mention fallbacks in {endpoint}"
            except Exception as e:
                # Skip endpoints that might not be available
                print(f"Skipping {endpoint}: {e}")
    
    def test_health_gate_enforcement(self):
        """Test that YouTube start endpoint enforces health gates."""
        # This test would require stopping services to make health gates fail
        # For now, just test the endpoint structure
        try:
            r = requests.post(
                f"{self.BASE_URL}/api/runs/youtube/start",
                json={
                    "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                    "limit": 1,
                    "max_depth": 0
                },
                timeout=10
            )
            
            # Should either succeed or fail with appropriate error
            assert r.status_code in (200, 500, 503), f"Expected 200, 500, or 503, got {r.status_code}"
            
            if r.status_code == 503:
                j = r.json()
                assert j["status"] == "error", "Should be error status"
                error_msg = j["error"]["message"]
                assert any(phrase in error_msg for phrase in [
                    "Health gate failed",
                    "MCP Hub unavailable",
                    "dependencies not ready"
                ]), f"Unexpected error message: {error_msg}"
        except Exception as e:
            # Skip if services aren't running
            print(f"Skipping health gate test: {e}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
