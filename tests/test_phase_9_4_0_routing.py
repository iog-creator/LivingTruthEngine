"""
Test Phase 9.4.0 routing and single-origin architecture
Verifies that reverse proxy correctly routes API and UI requests
"""

import pytest
import requests
import time

BASE = "http://localhost"

class TestPhase940Routing:
    """Test Phase 9.4.0 single-origin routing"""
    
    def test_ui_shell_root(self):
        """Test that root serves UI shell HTML"""
        response = requests.get(f"{BASE}/", timeout=10)
        assert response.status_code == 200
        assert "Living Truth Engine" in response.text
        # Check for the title in the HTML head
        assert "<title>Living Truth Engine</title>" in response.text
    
    def test_api_health_ok(self):
        """Test that API health endpoint works via proxy"""
        response = requests.get(f"{BASE}/api/health", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_api_health_full_ok(self):
        """Test that API health/full endpoint works via proxy"""
        response = requests.get(f"{BASE}/api/health/full", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "data" in data
    
    def test_api_models_ok(self):
        """Test that API models endpoint works via proxy"""
        response = requests.get(f"{BASE}/api/models", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "data" in data
    
    def test_api_direct_access(self):
        """Test that API is accessible directly on port 8050"""
        response = requests.get("http://localhost:8050/api/health", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_ui_direct_access(self):
        """Test that UI is accessible directly on port 4173"""
        response = requests.get("http://localhost:4173", timeout=10)
        assert response.status_code == 200
        assert "Living Truth Engine" in response.text
    
    def test_proxy_routing(self):
        """Test that proxy correctly routes different paths"""
        # Test API routing
        api_response = requests.get(f"{BASE}/api/health", timeout=10)
        assert api_response.status_code == 200
        
        # Test UI routing
        ui_response = requests.get(f"{BASE}/", timeout=10)
        assert ui_response.status_code == 200
        assert "Living Truth Engine" in ui_response.text
        
        # Verify they're different responses
        assert api_response.headers.get("content-type") != ui_response.headers.get("content-type")
