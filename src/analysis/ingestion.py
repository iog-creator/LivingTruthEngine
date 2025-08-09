"""
Living Truth Engine - Ingestion Pipeline
Builds vector and keyword indices from organized transcripts with telemetry.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from src.config import get_config
from src.analysis.hybrid_retrieval import LMStudioEmbeddings

try:
    from langchain_community.vectorstores.pgvector import PGVector
except Exception:  # pragma: no cover
    PGVector = None  # type: ignore


logger = logging.getLogger(__name__)


@dataclass
class IngestSummary:
    total_files: int
    chunks_indexed: int
    channel: Optional[str]
    started_at: str
    completed_at: str


class IngestionPipeline:
    def __init__(self) -> None:
        self.config = get_config()
        self.sources_dir = self.config.SOURCES_DIR
        self.organized_base = self.sources_dir / "organized"
        self.logs_dir = self.config.LOGS_DIR / "ingest_telemetry"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.status_file = self.logs_dir / "status.json"
        self.stream_file = self.logs_dir / "current.jsonl"

        # Text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.processing.CHUNK_SIZE,
            chunk_overlap=self.config.processing.CHUNK_OVERLAP,
        )

        # Embeddings (LM Studio)
        self.embeddings = LMStudioEmbeddings(self.config.model.LMSTUDIO_EMBEDDING_MODEL_QWEN3)

        # Vector store connection (lazy)
        self._vector_store = None

    def _emit(self, event: str, payload: Dict[str, Any]) -> None:
        record: Dict[str, Any] = {"ts": datetime.utcnow().isoformat() + "Z", "event": event}
        record.update(payload)
        try:
            self.stream_file.parent.mkdir(parents=True, exist_ok=True)
            with self.stream_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            self.status_file.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def _vector_store_handle(self):
        if self._vector_store is None:
            if PGVector is None:
                raise RuntimeError("PGVector not available")
            self._vector_store = PGVector(
                connection_string=self.config.database.postgres_connection_string,
                embedding_function=self.embeddings,
                collection_name="living_truth_documents",
            )
        return self._vector_store

    def _collect_documents(self, channel: Optional[str]) -> List[Document]:
        """Collect Documents from organized transcripts (transcript.txt and notes.md)."""
        docs: List[Document] = []
        base = self.organized_base
        if channel:
            base = base / channel
        if not base.exists():
            return []

        text_exts = {".txt", ".md"}
        for video_dir in sorted([p for p in base.rglob("*") if p.is_dir()]):
            transcript = video_dir / "transcript.txt"
            notes = video_dir / "notes.md"
            for p in [transcript, notes]:
                if p.exists() and p.suffix.lower() in text_exts:
                    try:
                        content = p.read_text(encoding="utf-8")
                        if not content.strip():
                            continue
                        meta = {
                            "source": str(p),
                            "video_id": video_dir.name,
                            "channel": base.name if channel else video_dir.parent.name,
                            "filename": p.name,
                            "file_type": p.suffix,
                            "created_at": datetime.utcnow().isoformat() + "Z",
                        }
                        docs.append(Document(page_content=content, metadata=meta))
                    except Exception as e:
                        logger.warning(f"Failed to read {p}: {e}")
        return docs

    def ingest(self, channel: Optional[str] = None, clear_index: bool = False) -> IngestSummary:
        start = datetime.utcnow().isoformat() + "Z"
        self._emit("ingest_start", {"channel": channel, "message": "Starting ingestion"})

        docs = self._collect_documents(channel)
        self._emit("ingest_collected", {"count": len(docs)})
        chunks_total = 0

        if not docs:
            end = datetime.utcnow().isoformat() + "Z"
            self._emit("ingest_complete", {"channel": channel, "chunks": 0, "message": "No documents"})
            return IngestSummary(total_files=0, chunks_indexed=0, channel=channel, started_at=start, completed_at=end)

        # Split into chunks
        chunk_docs: List[Document] = []
        for d in docs:
            for chunk in self.splitter.split_text(d.page_content):
                chunk_docs.append(Document(page_content=chunk, metadata=d.metadata))
        chunks_total = len(chunk_docs)
        self._emit("ingest_chunked", {"chunks": chunks_total})

        # Optionally clear index (not implemented here to avoid destructive ops)
        if clear_index:
            self._emit("ingest_warning", {"message": "clear_index requested but not implemented (safety)"})

        # Upsert to vector store
        try:
            vs = self._vector_store_handle()
            # LangChain PGVector does not expose explicit upsert; using similarity search triggers implicit table creation
            # We add via from_documents to index chunks
            PGVector.from_documents(
                documents=chunk_docs,
                embedding=self.embeddings,
                connection_string=self.config.database.postgres_connection_string,
                collection_name="living_truth_documents",
            )
        except Exception as e:
            self._emit("ingest_error", {"error": str(e)})
            raise

        end = datetime.utcnow().isoformat() + "Z"
        self._emit("ingest_complete", {"channel": channel, "chunks": chunks_total, "message": "Ingestion complete"})
        return IngestSummary(total_files=len(docs), chunks_indexed=chunks_total, channel=channel, started_at=start, completed_at=end)



