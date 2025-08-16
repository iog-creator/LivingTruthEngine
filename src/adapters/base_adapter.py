"""
Base Adapter for Phase 9.5.0

Provides common functionality for all source adapters including
deduplication, document normalization, and database persistence.
"""

import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class DocumentLike:
    """Standardized document format for all adapters."""

    id: str
    source: str
    url: str
    title: str
    text: str
    metadata: Dict[str, Any]
    sha256: str
    created_at: datetime
    transcript_mode: Optional[str] = None


class BaseAdapter(ABC):
    """Base class for all source adapters."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize adapter with configuration."""
        self.config = config
        self.seen_hashes: Set[str] = set()
        self.deduplication_enabled = config.get("deduplication_enabled", True)
        self.persist_transcript_mode = config.get("persist_transcript_mode", True)

    def _generate_sha256(self, content: str) -> str:
        """Generate SHA256 hash of content for deduplication."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _is_duplicate(self, content: str) -> bool:
        """Check if content is a duplicate based on SHA256."""
        if not self.deduplication_enabled:
            return False
        content_hash = self._generate_sha256(content)
        if content_hash in self.seen_hashes:
            logger.info(f"Duplicate content detected (hash: {content_hash[:8]}...)")
            return True
        self.seen_hashes.add(content_hash)
        return False

    def _normalize_document(
        self,
        raw_doc: Dict[str, Any],
        source_type: str,
        transcript_mode: Optional[str] = None,
    ) -> DocumentLike:
        """Normalize raw document to DocumentLike format."""
        # Generate content hash
        content = raw_doc.get("text", "") or raw_doc.get("content", "")
        sha256 = self._generate_sha256(content)

        # Create normalized document
        doc = DocumentLike(
            id=raw_doc.get("id", f"{source_type}_{sha256[:8]}"),
            source=source_type,
            url=raw_doc.get("url", raw_doc.get("uri", "")),
            title=raw_doc.get("title", "Untitled"),
            text=content,
            metadata=raw_doc.get("metadata", {}),
            sha256=sha256,
            created_at=datetime.now(),
            transcript_mode=transcript_mode,
        )

        return doc

    def _filter_duplicates(self, documents: List[DocumentLike]) -> List[DocumentLike]:
        """Filter out duplicate documents based on SHA256."""
        if not self.deduplication_enabled:
            return documents

        unique_docs = []
        seen_hashes = set()

        for doc in documents:
            if doc.sha256 not in seen_hashes:
                seen_hashes.add(doc.sha256)
                unique_docs.append(doc)
            else:
                logger.info(
                    f"Filtering duplicate document: {doc.title} (hash: {doc.sha256[:8]}...)"  # noqa: E501
                )

        return unique_docs

    @abstractmethod
    async def fetch_documents(self, params: Dict[str, Any]) -> List[DocumentLike]:
        """Fetch documents from the source. Must be implemented by subclasses."""
        pass

    async def process_source(self, params: Dict[str, Any]) -> List[DocumentLike]:
        """Process source with deduplication and normalization."""
        try:
            # Fetch raw documents
            raw_docs = await self.fetch_documents(params)

            # Normalize to DocumentLike format
            normalized_docs = []
            for raw_doc in raw_docs:
                if not self._is_duplicate(
                    raw_doc.get("text", "") or raw_doc.get("content", "")
                ):
                    doc = self._normalize_document(
                        raw_doc, self.source_type, params.get("transcript_mode")
                    )
                    normalized_docs.append(doc)

            # Final deduplication pass
            final_docs = self._filter_duplicates(normalized_docs)

            logger.info(
                f"Processed {len(raw_docs)} documents, {len(final_docs)} unique after deduplication"  # noqa: E501
            )
            return final_docs

        except Exception as e:
            logger.error(f"Error processing source: {e}")
            raise

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return the source type identifier. Must be implemented by subclasses."""
        pass
