"""
Pipeline package for Phase 8: Real-data ingestion
"""

from .canonicalize import CanonicalizePipeline
from .provenance import ProvenancePipeline

__all__ = ['CanonicalizePipeline', 'ProvenancePipeline']
