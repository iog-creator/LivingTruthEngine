import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8050"

def test_resilience_score_endpoint():
    """Test the resilience score endpoint returns proper envelope format."""
    response = requests.get(f"{BASE_URL}/api/resilience/score")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "data" in data
    assert "score" in data["data"]
    assert "components" in data["data"]
    assert "series" in data["data"]
    assert "ci" in data["data"]
    
    # Validate score is numeric and reasonable
    score = data["data"]["score"]
    assert isinstance(score, (int, float))
    assert 0 <= score <= 100

def test_resilience_chaos_endpoint():
    """Test the chaos endpoint returns proper envelope format."""
    response = requests.get(f"{BASE_URL}/api/resilience/chaos")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "data" in data
    assert "items" in data["data"]
    assert "count" in data["data"]
    
    # Validate items is a list
    assert isinstance(data["data"]["items"], list)

def test_resilience_anomalies_endpoint():
    """Test the anomalies endpoint returns proper envelope format."""
    response = requests.get(f"{BASE_URL}/api/resilience/anomalies")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "data" in data
    assert "items" in data["data"]
    assert "count" in data["data"]
    
    # Validate items is a list
    assert isinstance(data["data"]["items"], list)

def test_resilience_score_threshold():
    """Test that resilience score meets minimum threshold."""
    response = requests.get(f"{BASE_URL}/api/resilience/score")
    assert response.status_code == 200
    
    data = response.json()
    score = data["data"]["score"]
    
    # Score should be >= 80% for CI to pass
    assert score >= 80, f"Resilience score {score} is below threshold of 80"

def test_resilience_score_with_window():
    """Test resilience score with custom window parameter."""
    response = requests.get(f"{BASE_URL}/api/resilience/score?window_hours=48")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "data" in data
    assert "series" in data["data"]
    
    # Should have 48 data points for 48-hour window
    series = data["data"]["series"]
    assert len(series) == 48
