"""
Lightweight MCP Solver stub service

Provides health endpoint and minimal identity needed by MCP solver adapter and health checks.
"""

from typing import Dict
from fastapi import FastAPI


app = FastAPI(title="MCP Solver Stub", version="1.0.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "mcp-solver"}


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "MCP Solver stub running"}



