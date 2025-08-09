#!/usr/bin/env python3
"""
Living Truth Engine - FastAPI Server
Main entry point for the Living Truth Engine API
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from pathlib import Path
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Living Truth Engine", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Living Truth Engine"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Living Truth Engine API", "status": "operational"}

@app.get("/dashboard")
async def dashboard():
    """Dashboard endpoint."""
    return {"message": "Dashboard endpoint", "status": "ready"}


@app.get("/telemetry/status")
async def telemetry_status() -> JSONResponse:
    """Return the latest archive telemetry status snapshot."""
    status_file = Path("data/outputs/logs/archive_telemetry/status.json")
    if not status_file.exists():
        return JSONResponse({"status": "idle"})
    try:
        return JSONResponse(content=json.loads(status_file.read_text(encoding="utf-8")))
    except Exception:
        return JSONResponse({"error": "Failed reading status"}, status_code=500)


@app.get("/telemetry/stream")
async def telemetry_stream(lines: int = 200) -> PlainTextResponse:
    """Return the last N lines of the archive telemetry stream (JSONL)."""
    stream_file = Path("data/outputs/logs/archive_telemetry/current.jsonl")
    if not stream_file.exists():
        return PlainTextResponse("")
    try:
        content = stream_file.read_text(encoding="utf-8").splitlines()[-lines:]
        return PlainTextResponse("\n".join(content))
    except Exception:
        return PlainTextResponse("", status_code=500)


# Ingestion API
import json
from src.analysis.ingestion import IngestionPipeline


@app.post("/ingest")
async def ingest(channel: Optional[str] = None) -> JSONResponse:
    """Run ingestion from organized transcripts into vector store."""
    try:
        pipeline = IngestionPipeline()
        summary = pipeline.ingest(channel=channel)
        return JSONResponse({
            "total_files": summary.total_files,
            "chunks_indexed": summary.chunks_indexed,
            "channel": summary.channel,
            "started_at": summary.started_at,
            "completed_at": summary.completed_at,
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/ingest/telemetry/stream")
async def ingest_telemetry(lines: int = 200) -> PlainTextResponse:
    base = Path("data/outputs/logs/ingest_telemetry")
    stream = base / "current.jsonl"
    if not stream.exists():
        return PlainTextResponse("")
    try:
        return PlainTextResponse("\n".join(stream.read_text(encoding="utf-8").splitlines()[-lines:]))
    except Exception:
        return PlainTextResponse("", status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 