#!/usr/bin/env python3
"""
Unit tests for Langflow MCP Server
Tests the create_langflow functionality and error handling
"""

import pytest
import json
import requests
from unittest.mock import Mock, patch
from src.mcp_servers.langflow_mcp_server import LangflowMCP

class TestLangflowMCP:
    """Test cases for LangflowMCP class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with patch.dict('os.environ', {
            'LANGFLOW_API_ENDPOINT': 'http://localhost:7860',
            'LANGFLOW_API_KEY': 'test-api-key',
            'LANGFLOW_PROJECT_ID': 'test-project-id'
        }):
            self.langflow = LangflowMCP()
    
    def test_create_langflow_valid_config(self):
        """Test creating a workflow with valid configuration."""
        valid_config = {
            "name": "Test Workflow",
            "data": {
                "nodes": [],
                "edges": []
            },
            "description": "Test workflow description"
        }
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "test-flow-id",
            "name": "Test Workflow",
            "data": {"nodes": [], "edges": []}
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.request', return_value=mock_response) as mock_request:
            result = self.langflow.create_langflow(valid_config)
            
            # Verify the request was made correctly
            mock_request.assert_called_once_with(
                "POST",
                "http://localhost:7860/api/v1/flows",
                json=valid_config,
                headers={
                    "x-api-key": "test-api-key",
                    "Content-Type": "application/json",
                    "accept": "application/json"
                },
                timeout=10
            )
            
            # Verify the result
            assert result["id"] == "test-flow-id"
            assert result["name"] == "Test Workflow"
    
    def test_create_langflow_update_existing(self):
        """Test updating an existing workflow."""
        valid_config = {
            "name": "Updated Workflow",
            "data": {
                "nodes": [{"id": "node1", "type": "input"}],
                "edges": []
            }
        }
        flow_id = "existing-flow-id"
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": flow_id,
            "name": "Updated Workflow",
            "data": {"nodes": [{"id": "node1", "type": "input"}], "edges": []}
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.request', return_value=mock_response) as mock_request:
            result = self.langflow.create_langflow(valid_config, flow_id)
            
            # Verify PATCH request was made
            mock_request.assert_called_once_with(
                "PATCH",
                f"http://localhost:7860/api/v1/flows/{flow_id}",
                json=valid_config,
                headers={
                    "x-api-key": "test-api-key",
                    "Content-Type": "application/json",
                    "accept": "application/json"
                },
                timeout=10
            )
            
            assert result["id"] == flow_id
    
    def test_create_langflow_invalid_config_none(self):
        """Test creating workflow with None configuration."""
        with pytest.raises(ValueError, match="Flow configuration must be a non-empty dictionary"):
            self.langflow.create_langflow(None)
    
    def test_create_langflow_invalid_config_empty_dict(self):
        """Test creating workflow with empty dictionary."""
        with pytest.raises(ValueError, match="Flow configuration must be a non-empty dictionary"):
            self.langflow.create_langflow({})
    
    def test_create_langflow_invalid_config_wrong_type(self):
        """Test creating workflow with wrong configuration type."""
        with pytest.raises(ValueError, match="Flow configuration must be a non-empty dictionary"):
            self.langflow.create_langflow("not a dict")
    
    def test_create_langflow_missing_name(self):
        """Test creating workflow with missing name field."""
        invalid_config = {
            "data": {"nodes": [], "edges": []}
        }
        
        with pytest.raises(ValueError, match="Flow configuration must include: \['name', 'data'\]"):
            self.langflow.create_langflow(invalid_config)
    
    def test_create_langflow_missing_data(self):
        """Test creating workflow with missing data field."""
        invalid_config = {
            "name": "Test Workflow"
        }
        
        with pytest.raises(ValueError, match="Flow configuration must include: \['name', 'data'\]"):
            self.langflow.create_langflow(invalid_config)
    
    def test_create_langflow_connection_error(self):
        """Test handling of connection errors."""
        valid_config = {
            "name": "Test Workflow",
            "data": {"nodes": [], "edges": []}
        }
        
        with patch('requests.request', side_effect=requests.exceptions.ConnectionError("Connection failed")):
            with pytest.raises(ConnectionError, match="Langflow API unavailable"):
                self.langflow.create_langflow(valid_config)
    
    def test_create_langflow_http_error(self):
        """Test handling of HTTP errors."""
        valid_config = {
            "name": "Test Workflow",
            "data": {"nodes": [], "edges": []}
        }
        
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        
        with patch('requests.request', return_value=mock_response):
            with pytest.raises(Exception):  # HTTPException would be raised
                self.langflow.create_langflow(valid_config)
    
    def test_create_langflow_unexpected_error(self):
        """Test handling of unexpected errors."""
        valid_config = {
            "name": "Test Workflow",
            "data": {"nodes": [], "edges": []}
        }
        
        with patch('requests.request', side_effect=Exception("Unexpected error")):
            with pytest.raises(ConnectionError, match="Error processing workflow: Unexpected error"):
                self.langflow.create_langflow(valid_config)

if __name__ == "__main__":
    pytest.main([__file__]) 