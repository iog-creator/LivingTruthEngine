"""
Phase 8: Generalist Ingestion Module

Provides verifiable ingestion capabilities for web, PDF, and YouTube sources
with provenance tracking and bundle creation.
"""

from .runners import VeritasRunner

# Phase 8 components
from .adapters.youtube_adapter import YouTubeAdapter
from .fetchers.web_fetcher import WebFetcher
from .extractors.pdf_extractor import PDFExtractor
from .pipeline.canonicalize import CanonicalizePipeline
from .pipeline.provenance import ProvenancePipeline

__all__ = [
    'VeritasRunner',
    'YouTubeAdapter',
    'WebFetcher',
    'PDFExtractor',
    'CanonicalizePipeline',
    'ProvenancePipeline'
]



