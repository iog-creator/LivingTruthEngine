"""
AI Activity Bus
----------------

Lightweight in-process pub/sub for broadcasting AI activity events to
websocket clients. Used by the dashboard to show model activity lights.

Events have the shape: {"ai_type": str, "status": str, "meta": dict}

ai_type: one of ["embedder", "reranker", "llm", "ocr", "js", "provenance"]
status: one of ["idle", "working", "inference", "done", "error"]
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, List, Optional
import os


@dataclass
class AIActivityEvent:
    """Represents a single AI activity event."""

    ai_type: str
    status: str
    meta: Dict[str, Any]


class AIActivityBus:
    """In-memory pub/sub for AI activity events.

    Provides subscribe/unsubscribe and emit APIs. Subscribers receive events via
    an asyncio.Queue to enable non-blocking fanout to multiple websocket clients.
    """

    def __init__(self) -> None:
        self._subscribers: List[asyncio.Queue[AIActivityEvent]] = []
        self._lock = asyncio.Lock()
        # Last-known state per kind for REST snapshot endpoint
        self._snapshot: Dict[str, Dict[str, Any]] = {}

    async def subscribe(self) -> AsyncIterator[AIActivityEvent]:
        """Subscribe to events. Yields events until unsubscribed.

        Usage:
            async for event in bus.subscribe():
                ...
        """
        queue: asyncio.Queue[AIActivityEvent] = asyncio.Queue(maxsize=100)
        async with self._lock:
            self._subscribers.append(queue)

        try:
            while True:
                event = await queue.get()
                yield event
        finally:
            async with self._lock:
                if queue in self._subscribers:
                    self._subscribers.remove(queue)

    async def emit(
        self, ai_type: str, status: str, meta: Optional[Dict[str, Any]] = None
    ) -> None:
        """Broadcast an event to all subscribers and update snapshot."""
        event = AIActivityEvent(ai_type=ai_type, status=status, meta=meta or {})
        # Update snapshot immediately for clients polling the snapshot REST
        self._snapshot[ai_type] = {"kind": ai_type, "status": status, **(meta or {})}
        async with self._lock:
            for queue in list(self._subscribers):
                # Best-effort put; drop if queue is full
                try:
                    queue.put_nowait(event)
                except asyncio.QueueFull:
                    # Skip slow client
                    continue


# Singleton bus for application-wide use
bus = AIActivityBus()


try:
    # Optional FastAPI router for snapshot and test emit; unified_dashboard will include it if available  # noqa: E501
    from fastapi import APIRouter, Body

    router = APIRouter()

    @router.get("/api/ai-activity/snapshot")
    async def get_snapshot() -> Dict[str, Any]:
        """Return last-known activity state by kind for initial UI paint."""
        return {"status": "ok", "data": bus._snapshot, "error": None}

    @router.post("/api/_test/ai-activity/emit")
    async def test_emit_event(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
        """Test-only endpoint to push events during Cypress/pytest.

        Guarded by TEST_MODE=1.
        """
        if os.getenv("TEST_MODE", "0") != "1":
            return {
                "status": "forbidden",
                "data": None,
                "error": "TEST_MODE not enabled",
            }
        try:
            kind = str(payload.get("kind", "llm"))
            status = str(payload.get("status", "working"))
            meta = {k: v for k, v in payload.items() if k not in ("kind", "status")}
            await bus.emit(kind, status, meta)
            return {
                "status": "ok",
                "data": {"kind": kind, "status": status, **meta},
                "error": None,
            }
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}
except (ImportError, ModuleNotFoundError):
    router = None
