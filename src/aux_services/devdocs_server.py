"""
Lightweight DevDocs stub service

Exposes a minimal HTTP API used by our MCP DevDocs adapter for health checks and future expansion.
This service intentionally provides only basic endpoints to satisfy integration and stability.
"""  # noqa: E501

from typing import Dict
from fastapi import FastAPI


app = FastAPI(title="DevDocs Stub", version="1.0.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "devdocs"}


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "DevDocs stub running"}
