from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .provenance import write_bundle_proofs
from .fetchers import fetch_web, fetch_pdf, fetch_youtube
from .canonicalize import to_canonical
from .bundles import write_bundle
import toml

@dataclass
class VeritasRunStatus:
    run_id: str
    topic: str
    started_at: str
    completed_at: Optional[str]
    status: str
    bundle_dir: Optional[str]


class VeritasRunner:
    """Coordinates a verifiable, local-first ingestion run and writes a .veritasrun bundle.

    Minimal scaffold to satisfy tests and dashboard integration; full
    implementation will populate sources, canonical, claims, and proofs.
    """

    def __init__(self, project_root: Optional[Path] = None) -> None:
        self.project_root = project_root or Path(__file__).resolve().parents[3]
        self.runs_dir = self.project_root / "data" / "outputs" / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self._status_index: Dict[str, VeritasRunStatus] = {}

    def _slugify(self, text: str) -> str:
        return "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-")[:40]

    def start(self, topic: str, max_docs: int = 10, sources: Optional[List[str]] = None) -> VeritasRunStatus:
        sources = sources or ["youtube", "web", "pdf"]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = f"{ts}_{self._slugify(topic)}"
        bundle_dir = self.runs_dir / f"{run_id}.veritasrun"
        
        # Load flags from config
        flags = self._load_flags()
        
        # Fetch documents based on sources
        all_docs = []
        
        # For now, use placeholder data since we don't have actual sources
        # In a real implementation, this would fetch from actual URLs/files
        if "youtube" in sources:
            # Placeholder YouTube data
            all_docs.append({
                "source_type": "youtube",
                "uri": "https://www.youtube.com/watch?v=placeholder",
                "title": f"YouTube content for {topic}",
                "text": f"This is placeholder YouTube content for the topic: {topic}",
                "meta": {"video_id": "placeholder", "method": "placeholder"}
            })
        
        if "web" in sources:
            # Placeholder web data
            all_docs.append({
                "source_type": "web",
                "uri": "https://example.com/placeholder",
                "title": f"Web content for {topic}",
                "text": f"This is placeholder web content for the topic: {topic}",
                "meta": {"status_code": 200, "content_length": 100}
            })
        
        if "pdf" in sources:
            # Placeholder PDF data
            all_docs.append({
                "source_type": "pdf",
                "uri": "placeholder.pdf",
                "title": f"PDF content for {topic}",
                "text": f"This is placeholder PDF content for the topic: {topic}",
                "meta": {"pages": 1, "text_ratio": 0.8, "suspect": False}
            })
        
        # Limit to max_docs
        all_docs = all_docs[:max_docs]
        
        # Canonicalize documents
        canonical_docs = [to_canonical(doc) for doc in all_docs]
        
        # Write bundle
        bundle_info = write_bundle(str(bundle_dir), canonical_docs, flags)
        
        status = VeritasRunStatus(
            run_id=run_id,
            topic=topic,
            started_at=ts,
            completed_at=datetime.now().strftime("%Y%m%d_%H%M%S"),
            status="completed",
            bundle_dir=str(bundle_dir),
        )
        self._status_index[run_id] = status
        return status
    
    def _load_flags(self) -> Dict[str, Any]:
        """Load flags from config/veritas_flags.toml"""
        try:
            flags_path = self.project_root / "config" / "veritas_flags.toml"
            if flags_path.exists():
                return toml.load(flags_path)
            else:
                # Return default flags if file doesn't exist
                return {
                    "HF_BURST": "off",
                    "OCR_REQUIRED": "false", 
                    "PII_SCRUB": "standard",
                    "MAX_DOCS_DEFAULT": 10
                }
        except Exception as e:
            print(f"Warning: Could not load flags: {e}")
            return {
                "HF_BURST": "off",
                "OCR_REQUIRED": "false",
                "PII_SCRUB": "standard", 
                "MAX_DOCS_DEFAULT": 10
            }

    def complete(self, run_id: str) -> VeritasRunStatus:
        status = self._status_index.get(run_id)
        if not status:
            raise ValueError(f"Unknown run_id: {run_id}")
        status.completed_at = datetime.now().strftime("%Y%m%d_%H%M%S")
        status.status = "completed"
        return status

    def get_status(self, run_id: str) -> VeritasRunStatus:
        status = self._status_index.get(run_id)
        if status:
            return status
        # If process restarted, reconstruct minimal status from manifest
        bundle = next((p for p in self.runs_dir.glob(f"{run_id}.veritasrun") if p.is_dir()), None)
        if not bundle:
            raise ValueError(f"Run not found: {run_id}")
        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        return VeritasRunStatus(
            run_id=manifest["run_id"],
            topic=manifest["topic"],
            started_at=manifest["created_at"],
            completed_at=None,
            status="unknown",
            bundle_dir=str(bundle),
        )

    def list_runs(self, limit: int = 20) -> List[str]:
        runs = sorted([p.name[:-11] for p in self.runs_dir.glob("*.veritasrun") if p.is_dir()], reverse=True)
        return runs[: max(0, limit)]

    def open_bundle(self, run_id: str) -> Dict[str, Any]:
        bundle = self.runs_dir / f"{run_id}.veritasrun"
        if not bundle.exists():
            raise ValueError(f"Bundle not found: {run_id}")
        
        # Load manifest
        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        
        # Load metrics
        metrics = json.loads((bundle / "metrics.json").read_text(encoding="utf-8"))
        
        # Load merkle data
        merkle = json.loads((bundle / "merkle.json").read_text(encoding="utf-8"))
        
        # Load individual proof files
        proofs_dir = bundle / "proofs"
        proof_files = {}
        if proofs_dir.exists():
            for proof_file in proofs_dir.glob("*.sha256"):
                doc_id = proof_file.stem
                proof_files[doc_id] = proof_file.read_text(encoding="utf-8").strip()
        
        return {
            "run_id": run_id, 
            "bundle_dir": str(bundle), 
            "manifest": manifest, 
            "metrics": metrics,
            "merkle": merkle,
            "proofs": proof_files
        }



