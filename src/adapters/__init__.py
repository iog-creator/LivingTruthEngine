"""
Phase 9.5.0: Production Adapters Module

Provides production-ready adapters for YouTube, Web, and PDF sources
with normalization, deduplication, and DocumentLike output.
"""

from .base_adapter import BaseAdapter
from .youtube_adapter import YouTubeAdapter
from .web_adapter import WebAdapter
from .pdf_adapter import PDFAdapter

__all__ = [
    'BaseAdapter',
    'YouTubeAdapter', 
    'WebAdapter',
    'PDFAdapter'
]
