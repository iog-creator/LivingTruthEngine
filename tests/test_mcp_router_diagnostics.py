#!/usr/bin/env python3
"""
Test MCP Router Diagnostics Script

Tests the MCP router diagnostics functionality to ensure:
1. Script can be imported and executed
2. Command line arguments are parsed correctly
3. JSON-RPC communication works
4. Error handling follows project standards
5. Reports are generated correctly
"""
import json
import subprocess
import tempfile
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import the script functions for testing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from mcp_router_diagnostics import (
    envelope_ok, 
    envelope_err, 
    JsonRpcIO, 
    start_server,
    sanity_check_tool_schema,
    compute_metrics
)

def test_envelope_ok():
    """Test envelope_ok function"""
    data = {"test": "value"}
    result = envelope_ok(data)
    assert result["status"] == "ok"
    assert result["data"] == data

def test_envelope_err():
    """Test envelope_err function"""
    code = "test_error"
    message = "Test error message"
    details = {"detail": "test"}
    
    result = envelope_err(code, message, details)
    assert result["status"] == "error"
    assert result["error"]["code"] == code
    assert result["error"]["message"] == message
    assert result["error"]["details"] == details

def test_envelope_err_no_details():
    """Test envelope_err function without details"""
    code = "test_error"
    message = "Test error message"
    
    result = envelope_err(code, message)
    assert result["status"] == "error"
    assert result["error"]["code"] == code
    assert result["error"]["message"] == message
    assert "details" not in result["error"]

def test_sanity_check_tool_schema_valid():
    """Test sanity_check_tool_schema with valid tool"""
    tool = {
        "name": "test.tool",
        "inputSchema": {
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            }
        }
    }
    issues = sanity_check_tool_schema(tool)
    assert issues == []

def test_sanity_check_tool_schema_invalid_name():
    """Test sanity_check_tool_schema with invalid name"""
    tool = {
        "name": "",  # Invalid empty name
        "inputSchema": {"type": "object"}
    }
    issues = sanity_check_tool_schema(tool)
    assert "missing_or_invalid_name" in issues

def test_sanity_check_tool_schema_invalid_input_schema():
    """Test sanity_check_tool_schema with invalid input schema"""
    tool = {
        "name": "test.tool",
        "inputSchema": "not_an_object"  # Should be dict
    }
    issues = sanity_check_tool_schema(tool)
    assert "inputSchema_not_object" in issues

def test_compute_metrics():
    """Test compute_metrics function"""
    tools = [
        {"name": "test.tool1", "description": "Short desc"},
        {"name": "test.tool2", "description": "Short desc"},
        {"name": "other.tool1", "description": "Short desc"}
    ]
    list_latency = {"calls": 2, "samples_ms": [10.0, 20.0]}
    
    metrics = compute_metrics(tools, list_latency)
    
    assert metrics["count"] == 3
    assert metrics["duplicates"] == []
    assert len(metrics["namespaces_top"]) > 0
    assert metrics["list_latency"]["calls"] == 2
    assert metrics["list_latency"]["p50_ms"] == 15.0

def test_compute_metrics_with_duplicates():
    """Test compute_metrics with duplicate tool names"""
    tools = [
        {"name": "test.tool", "description": "Short desc"},
        {"name": "test.tool", "description": "Short desc"},  # Duplicate
        {"name": "other.tool", "description": "Short desc"}
    ]
    list_latency = {"calls": 1, "samples_ms": [10.0]}
    
    metrics = compute_metrics(tools, list_latency)
    
    assert metrics["count"] == 3
    assert "test.tool" in metrics["duplicates"]

def test_script_execution():
    """Test that the script can be executed"""
    script_path = Path(__file__).parent.parent / "scripts" / "mcp_router_diagnostics.py"
    
    # Test help output
    result = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert "MCP Router Diagnostics" in result.stdout

def test_script_with_invalid_command():
    """Test script behavior with invalid command"""
    script_path = Path(__file__).parent.parent / "scripts" / "mcp_router_diagnostics.py"
    
    result = subprocess.run(
        [sys.executable, str(script_path), "--cmd", "nonexistent_command"],
        capture_output=True,
        text=True
    )
    
    # Should fail gracefully with error envelope
    output = json.loads(result.stdout)
    assert output["status"] == "error"
    assert "server_start_failed" in output["error"]["code"]

@patch('subprocess.Popen')
def test_start_server(mock_popen):
    """Test start_server function"""
    mock_proc = MagicMock()
    mock_popen.return_value = mock_proc
    
    cmd = "test_command"
    proc = start_server(cmd)
    
    mock_popen.assert_called_once()
    assert proc == mock_proc

def test_json_rpc_io_initialization():
    """Test JsonRpcIO initialization"""
    mock_proc = MagicMock()
    timeout = 5.0
    
    rpc = JsonRpcIO(mock_proc, timeout)
    
    assert rpc.proc == mock_proc
    assert rpc.timeout == timeout
    assert rpc.buf == {}
    assert rpc.pending == {}

if __name__ == "__main__":
    pytest.main([__file__])
