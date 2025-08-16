"""
Lightweight Rulego stub service

Provides health and basic info endpoints compatible with our MCP Rulego adapter.
This replaces the fragile clone-and-build of upstream during container startup.
"""

from typing import Dict
from fastapi import FastAPI


app = FastAPI(title="Rulego Stub", version="1.0.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "rulego"}


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Rulego stub running"}
