"""
Living Truth Engine Analysis Module

This package intentionally avoids heavy imports at module import time to ensure
headless environments (e.g., Docker dashboard service) can import
`analysis.dash_app` without optional GUI dependencies like Tkinter.

Downstream modules should import concrete components directly, e.g.:
    from analysis.hybrid_retrieval import HybridRetriever
    from analysis.research_analysis import ResearchAnalysisSystem
"""

from typing import TYPE_CHECKING

# Re-export symbols when available, but do not fail package import if optional
# dependencies (e.g., Tk) are missing in the environment.
try:  # Lightweight retrieval components
    from .hybrid_retrieval import (
        HybridRetriever,
        AdvancedSearchEngine,
        BiblicalReranker,
        LMStudioEmbeddings,
    )
except (
    ImportError,
    ModuleNotFoundError,
):  # pragma: no cover - optional in minimal environments
    pass

try:  # Research components may require GUI deps in some environments
    from .research_analysis import (
        ResearchAnalysisSystem,
        ResearchAnalysisGUI,
        Claim,
        Entity,
        Relationship,
    )
except (
    ImportError,
    ModuleNotFoundError,
):  # pragma: no cover - optional in minimal environments
    pass

try:  # Notebook agent utilities
    from .notebook_agent import (
        AdvancedNotebookAgent,
        StudyGuide,
        DocumentSummary,
        ResearchReport,
        ContextManager,
        create_youtube_transcript_tool,
    )
except (
    ImportError,
    ModuleNotFoundError,
):  # pragma: no cover - optional in minimal environments
    pass

__all__ = [name for name in globals().keys() if not name.startswith("_")]
