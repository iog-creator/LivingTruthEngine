import json, os, requests

def mcp_call(server: str, tool: str, payload: dict) -> dict:
    # In Phase 1, MCP servers are local child processes; expose simple HTTP shim in future.
    # For MVP, directly import servers is heavy—so we simplify by calling within same process in tasks.py where needed.
    # Leave as placeholder if we later wrap servers with HTTP.
    return {}
