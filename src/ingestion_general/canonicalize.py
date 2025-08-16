"""
Canonicalization module for normalizing documents to standard format.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Any, List
import re


def to_canonical(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert raw document to canonical format.

    Args:
        raw: Raw document dictionary from fetchers

    Returns:
        Canonical document dictionary
    """
    # Generate stable doc_id
    doc_id = generate_doc_id(raw)

    # Extract and clean title
    title = extract_title(raw)

    # Extract and clean text
    text = extract_text(raw)

    # Determine language (default to English for now)
    lang = "en"

    # Check if document is suspect (e.g., PDF with low text ratio)
    suspect = raw.get("meta", {}).get("suspect", False)

    # Build canonical document
    canonical = {
        "doc_id": doc_id,
        "source_type": raw.get("source_type", "unknown"),
        "uri": raw.get("uri", ""),
        "retrieved_at": datetime.utcnow().isoformat() + "Z",
        "title": title,
        "text": text,
        "lang": lang,
        "suspect": suspect,
        "meta": raw.get("meta", {}),
    }

    return canonical


def generate_doc_id(raw: Dict[str, Any]) -> str:
    """
    Generate a stable document ID based on content and source.

    Args:
        raw: Raw document dictionary

    Returns:
        Stable document ID string
    """
    # Use URI as primary identifier
    uri = raw.get("uri", "")

    # For YouTube, include video ID
    if raw.get("source_type") == "youtube":
        meta = raw.get("meta", {})
        video_id = meta.get("video_id", "")
        if video_id:
            return f"yt_{video_id}"

    # For PDFs, use filename
    if raw.get("source_type") == "pdf":
        if uri.startswith(("http://", "https://")):
            # Extract filename from URL
            import urllib.parse

            parsed = urllib.parse.urlparse(uri)
            filename = parsed.path.split("/")[-1]
            if filename:
                return f"pdf_{filename}"
        else:
            # Local file path
            import os

            filename = os.path.basename(uri)
            if filename:
                return f"pdf_{filename}"

    # For web, use domain + path hash
    if raw.get("source_type") == "web":
        import urllib.parse

        parsed = urllib.parse.urlparse(uri)
        domain = parsed.netloc
        path = parsed.path
        path_hash = hashlib.md5(path.encode()).hexdigest()[:8]
        return f"web_{domain}_{path_hash}"

    # Fallback: hash the URI
    return f"doc_{hashlib.md5(uri.encode()).hexdigest()[:12]}"


def extract_title(raw: Dict[str, Any]) -> str:
    """
    Extract and clean document title.

    Args:
        raw: Raw document dictionary

    Returns:
        Cleaned title string
    """
    title = raw.get("title", "")

    if not title:
        # Try to extract from URI
        uri = raw.get("uri", "")
        if uri.startswith(("http://", "https://")):
            import urllib.parse

            parsed = urllib.parse.urlparse(uri)
            title = parsed.netloc
        else:
            # Local file
            import os

            title = os.path.basename(uri)

    # Clean title
    title = re.sub(r"[^\w\s\-_.]", "", title)
    title = re.sub(r"\s+", " ", title).strip()

    return title or "Untitled"


def extract_text(raw: Dict[str, Any]) -> str:
    """
    Extract and clean document text.

    Args:
        raw: Raw document dictionary

    Returns:
        Cleaned text string
    """
    text = raw.get("text", "")

    if not text:
        return ""

    # Basic text cleaning
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove control characters
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove empty lines
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]

    return "\n".join(lines).strip()
