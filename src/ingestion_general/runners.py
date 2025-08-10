from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Phase 8 imports
from .pipeline.provenance import ProvenancePipeline
from .pipeline.canonicalize import CanonicalizePipeline
from .adapters.youtube_adapter import YouTubeAdapter
from .fetchers.web_fetcher import WebFetcher
from .extractors.pdf_extractor import PDFExtractor
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
    """Phase 8: Coordinates a verifiable, local-first ingestion run with flexible parameters.

    Supports YouTube channel processing, web crawling, PDF extraction with OCR,
    and comprehensive provenance tracking.
    """

    def __init__(self, project_root: Optional[Path] = None) -> None:
        self.project_root = project_root or Path(__file__).resolve().parents[3]
        self.runs_dir = self.project_root / "data" / "outputs" / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self._status_index: Dict[str, VeritasRunStatus] = {}
        
        # Load configuration
        self.flags = self._load_flags()
        
        # Initialize Phase 8 components
        self.youtube_adapter = YouTubeAdapter(self.flags)
        self.web_fetcher = WebFetcher(self.flags)
        self.pdf_extractor = PDFExtractor(self.flags)
        self.canonicalize_pipeline = CanonicalizePipeline(self.flags)
        self.provenance_pipeline = ProvenancePipeline(self.flags)

    def _slugify(self, text: str) -> str:
        return "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-")[:40]

    def start(
        self, 
        topic: str, 
        channel_url: Optional[str] = None,
        selection: str = "oldest",
        max_videos: int = 10,
        crawl_depth: int = 1,
        allow_domains: Optional[List[str]] = None,
        deny_domains: Optional[List[str]] = None,
        transcript_pref: str = "yt_api",
        ocr_mode: str = "off",
        auto_retry_attempts: int = 2,
        sources: Optional[List[str]] = None
    ) -> VeritasRunStatus:
        """
        Start a Phase 8 veritas run with flexible parameters
        
        Args:
            topic: Run topic/name
            channel_url: YouTube channel URL (defaults to Imagination Podcast)
            selection: Video selection method (oldest|latest|by_date_range|ids)
            max_videos: Maximum videos to process
            crawl_depth: Web crawling depth (0-3)
            allow_domains: Allowed domains for web crawling
            deny_domains: Denied domains for web crawling
            transcript_pref: Transcript preference (yt_api|whisper_local|both)
            ocr_mode: OCR mode (off|auto|manual|auto_retry)
            auto_retry_attempts: Number of OCR retry attempts
            sources: Source types to process
        """
        sources = sources or ["youtube"]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = f"{ts}_{self._slugify(topic)}"
        bundle_dir = self.runs_dir / f"{run_id}.veritasrun"
        
        # Use default channel if not provided
        if not channel_url:
            channel_url = self.flags.get("default_channel", "https://www.youtube.com/@imaginationpodcastofficial")
        
        # Create run parameters
        run_params = {
            "topic": topic,
            "channel_url": channel_url,
            "selection": selection,
            "max_videos": max_videos,
            "crawl_depth": crawl_depth,
            "allow_domains": allow_domains or self.flags.get("allow_domains", []),
            "deny_domains": deny_domains or self.flags.get("deny_domains", []),
            "transcript_pref": transcript_pref,
            "ocr_mode": ocr_mode,
            "auto_retry_attempts": auto_retry_attempts,
            "sources": sources,
            "started_at": datetime.now(UTC).isoformat()
        }
        
        logger.info(f"Starting Phase 8 veritas run: {run_id}")
        logger.info(f"Channel: {channel_url}")
        logger.info(f"Selection: {selection}, Max videos: {max_videos}")
        logger.info(f"Crawl depth: {crawl_depth}, OCR mode: {ocr_mode}")
        
        # Fetch documents based on sources
        all_docs = []
        
        # Process YouTube sources
        if "youtube" in sources:
            try:
                logger.info(f"Processing YouTube channel: {channel_url}")
                videos = self.youtube_adapter.discover_videos(
                    channel_url=channel_url,
                    selection=selection,
                    max_videos=max_videos
                )
                
                for video in videos:
                    video_id = video.get("id")
                    if video_id:
                        # Fetch transcript
                        transcript = self.youtube_adapter.fetch_transcript(
                            video_id, 
                            transcript_pref
                        )
                        
                        # Create document
                        doc = {
                            "source_type": "youtube",
                            "uri": video.get("webpage_url", f"https://www.youtube.com/watch?v={video_id}"),
                            "title": video.get("title", f"YouTube Video {video_id}"),
                            "text": transcript or f"[No transcript available for {video_id}]",
                            "meta": {
                                "video_id": video_id,
                                "upload_date": video.get("upload_date"),
                                "view_count": video.get("view_count", 0),
                                "duration": video.get("duration", 0),
                                "extraction_method": "youtube_api"
                            }
                        }
                        all_docs.append(doc)
                
                logger.info(f"Processed {len(videos)} YouTube videos")
                
            except Exception as e:
                logger.error(f"Failed to process YouTube channel: {e}")
                # Create error document
                all_docs.append({
                    "source_type": "youtube",
                    "uri": channel_url,
                    "title": f"YouTube Error: {topic}",
                    "text": f"[Error processing YouTube channel: {e}]",
                    "meta": {"error": str(e), "extraction_method": "error"}
                })
        
        # Process web sources (if crawl_depth > 0)
        if "web" in sources and crawl_depth > 0:
            try:
                logger.info(f"Processing web crawling with depth {crawl_depth}")
                
                # For now, crawl the YouTube channel page for external links
                web_docs = self.web_fetcher.fetch_url(
                    url=channel_url,
                    crawl_depth=0,
                    max_depth=crawl_depth
                )
                
                all_docs.extend(web_docs)
                logger.info(f"Fetched {len(web_docs)} web documents")
                
            except Exception as e:
                logger.error(f"Failed to fetch web content: {e}")
                all_docs.append({
                    "source_type": "web",
                    "uri": channel_url,
                    "title": f"Web Error: {topic}",
                    "text": f"[Error fetching web content: {e}]",
                    "meta": {"error": str(e), "extraction_method": "error"}
                })
        
        # Process PDF sources (placeholder for now)
        if "pdf" in sources:
            logger.info("PDF processing not yet implemented in Phase 8")
            all_docs.append({
                "source_type": "pdf",
                "uri": "https://example.com/placeholder.pdf",
                "title": f"PDF placeholder for {topic}",
                "text": f"[PDF processing not yet implemented for {topic}]",
                "meta": {"extraction_method": "placeholder"}
            })
        
        # Canonicalize documents using Phase 8 pipeline
        logger.info(f"Canonicalizing {len(all_docs)} documents")
        canonicalized_docs = self.canonicalize_pipeline.canonicalize_documents(all_docs)
        
        # Create provenance data
        logger.info("Creating provenance data")
        provenance_data = self.provenance_pipeline.create_provenance_data(
            canonicalized_docs, 
            run_params
        )
        
        # Create bundle directory
        bundle_dir.mkdir(parents=True, exist_ok=True)
        
        # Write corpus.jsonl
        corpus_content = self.canonicalize_pipeline.create_corpus_jsonl(canonicalized_docs)
        with open(bundle_dir / "corpus.jsonl", 'w', encoding='utf-8') as f:
            f.write(corpus_content)
        
        # Load flags from config
        flags = self._load_flags()
        
        # Write manifest.json
        manifest = {
            "run_id": run_id,
            "topic": topic,
            "started_at": run_params["started_at"],
            "completed_at": datetime.now(UTC).isoformat(),
            "parameters": run_params,
            "document_count": len(canonicalized_docs),
            "merkle_root": provenance_data["merkle"]["root"],
            "bundle_version": "phase8",
            # Phase 8 specific fields
            "channel_url": run_params.get("channel_url"),
            "selection": run_params.get("selection"),
            "max_videos": run_params.get("max_videos"),
            "crawl_depth": run_params.get("crawl_depth"),
            "ocr_mode": run_params.get("ocr_mode"),
            "flags": flags,
            "documents": [doc.get("id") for doc in canonicalized_docs]
        }
        
        with open(bundle_dir / "manifest.json", 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        # Save provenance data
        self.provenance_pipeline.save_provenance_data(provenance_data, bundle_dir)
        
        logger.info(f"Phase 8 bundle written to {bundle_dir}")
        logger.info(f"Documents: {len(canonicalized_docs)}")
        logger.info(f"Merkle root: {provenance_data['merkle']['root']}")
        
        # Update status
        status = VeritasRunStatus(
            run_id=run_id,
            topic=topic,
            started_at=run_params["started_at"],
            completed_at=datetime.now(UTC).isoformat(),
            status="completed",
            bundle_dir=str(bundle_dir)
        )
        self._status_index[run_id] = status
        
        return status
    
    def _load_flags(self) -> Dict[str, Any]:
        """Load Phase 8 flags from config/veritas_flags.toml"""
        try:
            flags_path = self.project_root / "config" / "veritas_flags.toml"
            if flags_path.exists():
                config_data = toml.load(flags_path)
                
                # Extract top-level flags (not nested sections)
                flags = {}
                
                # Add top-level flags that are not dictionaries
                for key, value in config_data.items():
                    if not isinstance(value, dict):
                        flags[key] = value
                
                return flags
            else:
                # Return default Phase 8 flags if file doesn't exist
                return {
                    "HF_BURST": "off",
                    "OCR_REQUIRED": "false",
                    "PII_SCRUB": "standard",
                    "MAX_DOCS_DEFAULT": 10
                }
        except Exception as e:
            logger.warning(f"Could not load Phase 8 flags: {e}")
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



