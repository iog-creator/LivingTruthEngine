"""
Provenance utilities for verifiable ingestion bundles.

Provides SHA-256 hashing helpers and a simple Merkle root implementation
to support Phase 6 proof requirements.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any


def compute_sha256_bytes(content: bytes) -> str:
    """Compute SHA-256 hex digest of bytes.

    Args:
        content: Raw bytes to hash.

    Returns:
        Hex string of the SHA-256 digest.
    """
    return hashlib.sha256(content).hexdigest()


def compute_sha256_file(path: Path) -> str:
    """Compute SHA-256 hex digest of a file.

    Args:
        path: File path to hash.

    Returns:
        Hex string of the SHA-256 digest.
    """
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def build_merkle_root(hashes: List[str]) -> str:
    """Build a Merkle root from a list of hex digests.

    - Duplicates the last hash on odd-length levels (Bitcoin-style padding).
    - Returns the single root hex string for non-empty input.

    Args:
        hashes: List of hex digests (leaf hashes).

    Returns:
        The Merkle root hex digest. Empty string if no hashes provided.
    """
    if not hashes:
        return ""
    level = hashes[:]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        next_level: List[str] = []
        for i in range(0, len(level), 2):
            combined = bytes.fromhex(level[i]) + bytes.fromhex(level[i + 1])
            next_level.append(compute_sha256_bytes(combined))
        level = next_level
    return level[0]


def verify_merkle_root(hashes: List[str], expected_root: str) -> bool:
    """Verify that the Merkle root of leaves equals expected_root.

    Args:
        hashes: Leaf hex digests.
        expected_root: Expected Merkle root hex digest.

    Returns:
        True if computed root equals expected_root; otherwise False.
    """
    return build_merkle_root(hashes) == expected_root


def write_bundle_proofs(bundle_dir: Path, source_files: List[Path]) -> Dict[str, Any]:
    """Compute per-file hashes and Merkle root and write proofs JSON files.

    Files written under bundle_dir/proofs/:
      - source_hashes.json: {"files": {"rel/path": "sha256hex", ...}}
      - merkle_roots.json: {"root": "sha256hex", "count": N}

    Args:
        bundle_dir: The .veritasrun directory.
        source_files: List of source file paths.

    Returns:
        Dict with keys: files (mapping), merkle_root (str), count (int).
    """
    proofs_dir = bundle_dir / "proofs"
    proofs_dir.mkdir(parents=True, exist_ok=True)

    rel_map: Dict[str, str] = {}
    for p in source_files:
        try:
            rel = str(p.relative_to(bundle_dir)) if p.is_absolute() else str(p)
        except Exception:
            rel = p.name
        rel_map[rel] = compute_sha256_file(p)

    leaves = list(rel_map.values())
    merkle_root = build_merkle_root(leaves)

    (proofs_dir / "source_hashes.json").write_text(
        __to_json({"files": rel_map}), encoding="utf-8"
    )
    (proofs_dir / "merkle_roots.json").write_text(
        __to_json({"root": merkle_root, "count": len(leaves)}), encoding="utf-8"
    )

    return {"files": rel_map, "merkle_root": merkle_root, "count": len(leaves)}


def __to_json(obj: Any) -> str:
    import json
    return json.dumps(obj, indent=2, sort_keys=True)

def sha256_text(text: str) -> str:
    """
    Compute SHA-256 hash of text content.
    
    Args:
        text: Text content to hash
        
    Returns:
        SHA-256 hex digest
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def build_merkle(leaves: List[str]) -> Dict[str, Any]:
    """
    Build Merkle tree from list of leaf hashes.
    
    Args:
        leaves: List of SHA-256 hex digests
        
    Returns:
        Dictionary with root hash and leaf count
    """
    root = build_merkle_root(leaves)
    return {
        "root": root,
        "leaves": leaves,
        "count": len(leaves)
    }


