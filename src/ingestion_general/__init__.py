"""
Generalist Ingestion Module

Provides verifiable ingestion capabilities for web, PDF, and YouTube sources
with provenance tracking and bundle creation.
"""

from .runners import VeritasRunner
from .fetchers import fetch_web, fetch_pdf, fetch_youtube
from .canonicalize import to_canonical
from .provenance import sha256_text, build_merkle
from .bundles import write_bundle

__all__ = [
    'VeritasRunner',
    'fetch_web',
    'fetch_pdf', 
    'fetch_youtube',
    'to_canonical',
    'sha256_text',
    'build_merkle',
    'write_bundle'
]



