"""
YouTube Adapter for Phase 9.5.0

Production-ready YouTube adapter with deduplication, transcript mode persistence,
and integration with existing YouTube adapter implementation.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse, parse_qs

from .base_adapter import BaseAdapter, DocumentLike

# Import existing YouTube adapter
try:
    from ..ingestion_general.adapters.youtube_adapter import YouTubeAdapter as LegacyYouTubeAdapter
    LEGACY_YOUTUBE_AVAILABLE = True
except ImportError:
    LEGACY_YOUTUBE_AVAILABLE = False
    logging.warning("Legacy YouTube adapter not available")

logger = logging.getLogger(__name__)

class YouTubeAdapter(BaseAdapter):
    """YouTube adapter with deduplication and transcript mode persistence."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize YouTube adapter."""
        super().__init__(config)
        
        # Initialize legacy adapter if available
        if LEGACY_YOUTUBE_AVAILABLE:
            self.legacy_adapter = LegacyYouTubeAdapter(config)
        else:
            self.legacy_adapter = None
            logger.warning("Legacy YouTube adapter not available, using mock implementation")
        
        # YouTube-specific configuration
        self.default_limit = config.get("youtube_default_limit", 10)
        self.default_sort = config.get("youtube_default_sort", "oldest")
        self.max_depth = config.get("youtube_max_depth", 3)
        self.transcript_timeout = config.get("transcript_timeout", 60)
        
    @property
    def source_type(self) -> str:
        """Return YouTube source type."""
        return "youtube"
    
    async def fetch_documents(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch YouTube documents using legacy adapter or mock implementation."""
        if self.legacy_adapter:
            return await self._fetch_with_legacy_adapter(params)
        else:
            return await self._fetch_mock_documents(params)
    
    async def _fetch_with_legacy_adapter(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch documents using legacy YouTube adapter."""
        try:
            # Extract parameters
            channel_url = params.get("channel_url")
            if not channel_url:
                raise ValueError("channel_url is required for YouTube adapter")
            
            limit = params.get("limit", self.default_limit)
            sort = params.get("sort", self.default_sort)
            max_depth = params.get("max_depth", self.max_depth)
            transcript_mode = params.get("transcript_mode", "autosubs")
            
            # Discover videos using legacy adapter
            videos = self.legacy_adapter.discover_videos(
                channel_url=channel_url,
                selection=sort,
                max_videos=limit
            )
            
            documents = []
            for video in videos:
                try:
                    # Fetch transcript based on mode
                    transcript = await self._fetch_transcript(video["id"], transcript_mode)
                    if transcript:
                        # Create document as dictionary
                        doc = {
                            "id": f"yt_{video['id']}",
                            "source": "youtube",
                            "url": f"https://www.youtube.com/watch?v={video['id']}",
                            "title": video.get("title", "Untitled Video"),
                            "text": transcript,
                            "metadata": {
                                "video_id": video["id"],
                                "channel_url": channel_url,
                                "transcript_mode": transcript_mode,
                                "duration": video.get("duration"),
                                "upload_date": video.get("upload_date"),
                                "view_count": video.get("view_count")
                            }
                        }
                        documents.append(doc)
                        
                except Exception as e:
                    logger.error(f"Error processing video {video.get('id', 'unknown')}: {e}")
                    continue
            
            return documents
            
        except Exception as e:
            logger.error(f"Error fetching YouTube documents: {e}")
            raise
    
    async def _fetch_transcript(self, video_id: str, mode: str) -> Optional[str]:
        """Fetch transcript using specified mode."""
        try:
            if mode == "autosubs":
                return self.legacy_adapter._fetch_transcript_autosubs(video_id)
            elif mode == "official":
                return self.legacy_adapter._fetch_transcript_official(video_id)
            elif mode == "whisper_local":
                return self.legacy_adapter._fetch_transcript_whisper_local(video_id)
            else:
                logger.warning(f"Unknown transcript mode: {mode}, using autosubs")
                return self.legacy_adapter._fetch_transcript_autosubs(video_id)
        except Exception as e:
            logger.error(f"Error fetching transcript for {video_id} with mode {mode}: {e}")
            return None
    
    async def _fetch_mock_documents(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch mock YouTube documents for testing."""
        import uuid
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        limit = params.get("limit", self.default_limit)
        transcript_mode = params.get("transcript_mode", "autosubs")
        
        documents = []
        for i in range(min(limit, 3)):  # Max 3 mock documents
            doc = {
                "id": f"yt_mock_{uuid.uuid4().hex[:8]}",
                "source": "youtube",
                "url": f"https://www.youtube.com/watch?v=mock_{i}",
                "title": f"Mock YouTube Video {i+1}",
                "text": f"This is mock transcript content for video {i+1}. It contains sample text that would normally be extracted from a YouTube video transcript using {transcript_mode} mode.",
                "metadata": {
                    "video_id": f"mock_{i}",
                    "channel_url": "https://www.youtube.com/@mockchannel",
                    "transcript_mode": transcript_mode,
                    "duration": 1200,
                    "upload_date": "2024-01-01",
                    "view_count": 1000
                }
            }
            documents.append(doc)
        
        return documents
    
    def _extract_channel_id(self, channel_url: str) -> Optional[str]:
        """Extract channel ID from various YouTube URL formats."""
        try:
            parsed = urlparse(channel_url)
            if parsed.hostname in ["youtube.com", "www.youtube.com"]:
                if parsed.path.startswith("/@"):
                    return parsed.path[2:]  # Remove /@ prefix
                elif parsed.path.startswith("/channel/"):
                    return parsed.path.split("/")[2]
                elif parsed.path.startswith("/c/"):
                    return parsed.path.split("/")[2]
            return None
        except Exception as e:
            logger.error(f"Error extracting channel ID from {channel_url}: {e}")
            return None
