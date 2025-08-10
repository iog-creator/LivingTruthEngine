"""
Canonicalize Pipeline for Phase 8: Real-data ingestion
Handles document canonicalization with enhanced provenance tracking
"""

import logging
import hashlib
import json
from datetime import datetime, UTC
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class CanonicalizePipeline:
    """Document canonicalization pipeline with enhanced provenance tracking"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize canonicalization pipeline"""
        self.config = config
        self.proof_format = config.get("proof_format", "sha256")
        
    def canonicalize_documents(
        self, 
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Canonicalize a list of documents with enhanced provenance
        
        Args:
            documents: List of raw document dictionaries
            
        Returns:
            List of canonicalized documents
        """
        logger.info(f"Canonicalizing {len(documents)} documents")
        
        canonicalized = []
        for i, doc in enumerate(documents):
            try:
                canonical_doc = self._canonicalize_single_document(doc, i)
                canonicalized.append(canonical_doc)
            except Exception as e:
                logger.error(f"Error canonicalizing document {i}: {e}")
                # Create error document
                error_doc = self._create_error_document(doc, i, str(e))
                canonicalized.append(error_doc)
        
        logger.info(f"Successfully canonicalized {len(canonicalized)} documents")
        return canonicalized
    
    def _canonicalize_single_document(
        self, 
        doc: Dict[str, Any], 
        index: int
    ) -> Dict[str, Any]:
        """Canonicalize a single document"""
        
        # Extract basic fields
        source_type = doc.get("source_type", "unknown")
        uri = doc.get("uri", "")
        title = doc.get("title", "")
        text = doc.get("text", "")
        
        # Generate document ID
        doc_id = self._generate_document_id(uri, text)
        
        # Create canonical document
        canonical_doc = {
            "id": doc_id,
            "index": index,
            "source_type": source_type,
            "uri": uri,
            "title": title,
            "text": text,
            "canonicalized_at": datetime.now(UTC).isoformat(),
            "provenance": self._create_provenance(doc),
            "metadata": self._extract_metadata(doc)
        }
        
        # Add source-specific fields
        if source_type == "youtube":
            canonical_doc.update(self._canonicalize_youtube_document(doc))
        elif source_type == "web":
            canonical_doc.update(self._canonicalize_web_document(doc))
        elif source_type == "pdf":
            canonical_doc.update(self._canonicalize_pdf_document(doc))
        
        return canonical_doc
    
    def _generate_document_id(self, uri: str, text: str) -> str:
        """Generate unique document ID"""
        # Use URI + first 100 chars of text for ID generation
        content = f"{uri}:{text[:100]}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _create_provenance(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Create provenance information for document"""
        provenance = {
            "extraction_method": doc.get("meta", {}).get("extraction_method", "unknown"),
            "crawl_depth": doc.get("crawl_depth", 0),
            "crawl_parent": doc.get("crawl_parent"),
            "processing_timestamp": datetime.now(UTC).isoformat()
        }
        
        # Add source-specific provenance
        source_type = doc.get("source_type", "unknown")
        if source_type == "youtube":
            provenance.update({
                "video_id": doc.get("meta", {}).get("video_id"),
                "upload_date": doc.get("meta", {}).get("upload_date"),
                "view_count": doc.get("meta", {}).get("view_count"),
                "duration": doc.get("meta", {}).get("duration")
            })
        elif source_type == "web":
            provenance.update({
                "content_type": doc.get("meta", {}).get("content_type"),
                "links_count": doc.get("meta", {}).get("links_count", 0)
            })
        elif source_type == "pdf":
            provenance.update({
                "page_count": doc.get("meta", {}).get("page_count"),
                "ocr_attempts": doc.get("meta", {}).get("ocr_attempts", 0),
                "needs_ocr": doc.get("meta", {}).get("needs_ocr", False)
            })
        
        return provenance
    
    def _extract_metadata(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from document"""
        metadata = doc.get("meta", {}).copy()
        
        # Add common metadata
        metadata.update({
            "char_count": len(doc.get("text", "")),
            "word_count": len(doc.get("text", "").split()),
            "source_type": doc.get("source_type", "unknown")
        })
        
        return metadata
    
    def _canonicalize_youtube_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Canonicalize YouTube-specific fields"""
        meta = doc.get("meta", {})
        
        return {
            "youtube": {
                "video_id": meta.get("video_id"),
                "upload_date": meta.get("upload_date"),
                "view_count": meta.get("view_count", 0),
                "duration": meta.get("duration", 0),
                "channel": meta.get("channel"),
                "channel_id": meta.get("channel_id")
            }
        }
    
    def _canonicalize_web_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Canonicalize web-specific fields"""
        meta = doc.get("meta", {})
        
        return {
            "web": {
                "content_type": meta.get("content_type"),
                "extraction_method": meta.get("extraction_method"),
                "links_count": meta.get("links_count", 0),
                "links": doc.get("links", [])
            }
        }
    
    def _canonicalize_pdf_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Canonicalize PDF-specific fields"""
        meta = doc.get("meta", {})
        
        return {
            "pdf": {
                "page_count": meta.get("page_count"),
                "extraction_method": meta.get("extraction_method"),
                "ocr_attempts": meta.get("ocr_attempts", 0),
                "needs_ocr": meta.get("needs_ocr", False),
                "char_count": meta.get("char_count", 0),
                "file_size": meta.get("size_bytes")
            }
        }
    
    def _create_error_document(
        self, 
        original_doc: Dict[str, Any], 
        index: int, 
        error_message: str
    ) -> Dict[str, Any]:
        """Create error document when canonicalization fails"""
        return {
            "id": f"error_{index}_{hashlib.md5(error_message.encode()).hexdigest()[:8]}",
            "index": index,
            "source_type": original_doc.get("source_type", "unknown"),
            "uri": original_doc.get("uri", ""),
            "title": f"Error: {original_doc.get('title', 'Unknown')}",
            "text": f"[Canonicalization error: {error_message}]",
            "canonicalized_at": datetime.utcnow().isoformat(),
            "provenance": {
                "extraction_method": "error",
                "error_message": error_message,
                "processing_timestamp": datetime.utcnow().isoformat()
            },
            "metadata": {
                "char_count": 0,
                "word_count": 0,
                "source_type": "error"
            }
        }
    
    def create_corpus_jsonl(self, canonicalized_docs: List[Dict[str, Any]]) -> str:
        """Create corpus.jsonl content from canonicalized documents"""
        lines = []
        for doc in canonicalized_docs:
            # Create a clean version for JSONL (remove any non-serializable objects)
            clean_doc = self._clean_for_jsonl(doc)
            lines.append(json.dumps(clean_doc, ensure_ascii=False))
        
        return "\n".join(lines)
    
    def _clean_for_jsonl(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Clean document for JSONL serialization"""
        # Remove any non-serializable objects and ensure all values are JSON-compatible
        clean_doc = {}
        
        for key, value in doc.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                clean_doc[key] = value
            elif isinstance(value, dict):
                clean_doc[key] = self._clean_for_jsonl(value)
            elif isinstance(value, list):
                clean_doc[key] = [
                    self._clean_for_jsonl(item) if isinstance(item, dict) else item
                    for item in value
                    if isinstance(item, (str, int, float, bool, type(None), dict))
                ]
            else:
                # Convert other types to string
                clean_doc[key] = str(value)
        
        return clean_doc
