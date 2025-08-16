"""
Bundle writing utilities for .veritasrun bundles.

Creates verifiable bundles with manifest, corpus, proofs, and metrics.
"""

import json
import os
import time
from pathlib import Path
from typing import List, Dict, Any
from .provenance import sha256_text, build_merkle


def write_bundle(
    run_dir: str, docs: List[Dict[str, Any]], flags: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Write a complete .veritasrun bundle.

    Args:
        run_dir: Directory path for the bundle
        docs: List of canonical documents
        flags: Configuration flags used for the run

    Returns:
        Dictionary with bundle metadata
    """
    bundle_path = Path(run_dir)
    bundle_path.mkdir(parents=True, exist_ok=True)

    # Write manifest.json
    manifest = create_manifest(docs, flags)
    with open(bundle_path / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    # Write corpus.jsonl
    write_corpus_jsonl(bundle_path / "corpus.jsonl", docs)

    # Write proofs
    proofs_dir = bundle_path / "proofs"
    proofs_dir.mkdir(exist_ok=True)

    # Create SHA-256 proofs for each document
    doc_hashes = []
    for doc in docs:
        doc_id = doc["doc_id"]
        text_hash = sha256_text(doc["text"])
        doc_hashes.append(text_hash)

        # Write individual proof file
        proof_file = proofs_dir / f"{doc_id}.sha256"
        with open(proof_file, "w") as f:
            f.write(text_hash)

    # Create merkle.json
    merkle_data = build_merkle(doc_hashes)
    with open(bundle_path / "merkle.json", "w") as f:
        json.dump(merkle_data, f, indent=2)

    # Write metrics.json
    metrics = create_metrics(docs, manifest)
    with open(bundle_path / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    return {
        "bundle_path": str(bundle_path),
        "doc_count": len(docs),
        "merkle_root": merkle_data["root"],
        "manifest": manifest,
    }


def create_manifest(
    docs: List[Dict[str, Any]], flags: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create manifest.json for the bundle.

    Args:
        docs: List of canonical documents
        flags: Configuration flags

    Returns:
        Manifest dictionary
    """
    # Extract topic from first document or use default
    topic = "general_ingestion"
    if docs and "title" in docs[0]:
        topic = docs[0]["title"][:50]  # Truncate long titles

    # Count documents by source type
    source_counts = {}
    for doc in docs:
        source_type = doc.get("source_type", "unknown")
        source_counts[source_type] = source_counts.get(source_type, 0) + 1

    manifest = {
        "topic": topic,
        "timestamp": time.time(),
        "doc_count": len(docs),
        "source_counts": source_counts,
        "flags": flags,
        "documents": [
            {
                "doc_id": doc["doc_id"],
                "source_type": doc["source_type"],
                "uri": doc["uri"],
                "title": doc["title"],
                "suspect": doc.get("suspect", False),
            }
            for doc in docs
        ],
    }

    return manifest


def write_corpus_jsonl(corpus_path: Path, docs: List[Dict[str, Any]]) -> None:
    """
    Write documents to corpus.jsonl file.

    Args:
        corpus_path: Path to corpus.jsonl file
        docs: List of canonical documents
    """
    with open(corpus_path, "w") as f:
        for doc in docs:
            f.write(json.dumps(doc) + "\n")


def create_metrics(
    docs: List[Dict[str, Any]], manifest: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create metrics.json for the bundle.

    Args:
        docs: List of canonical documents
        manifest: Manifest data

    Returns:
        Metrics dictionary
    """
    # Calculate basic metrics
    total_bytes = sum(len(json.dumps(doc)) for doc in docs)
    total_chars = sum(len(doc.get("text", "")) for doc in docs)

    # Count by source type
    docs_by_source = {}
    for doc in docs:
        source_type = doc.get("source_type", "unknown")
        docs_by_source[source_type] = docs_by_source.get(source_type, 0) + 1

    # Calculate duration (placeholder for now)
    duration_seconds = 0.0  # Would be calculated from actual run timing

    # Collect any errors
    errors = []
    for doc in docs:
        if "error" in doc.get("meta", {}):
            errors.append(f"{doc['doc_id']}: {doc['meta']['error']}")

    metrics = {
        "docs_total": len(docs),
        "docs_by_source": docs_by_source,
        "bytes_total": total_bytes,
        "chars_total": total_chars,
        "duration_seconds": duration_seconds,
        "errors": errors,
        "drift": 0.0,  # Placeholder for Phase 8
        "coverage": 1.0,  # Placeholder for Phase 8
    }

    return metrics
