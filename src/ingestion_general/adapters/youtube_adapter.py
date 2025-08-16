"""
YouTube Adapter for Phase 8: Real-data ingestion
Handles video discovery and transcript fetching for YouTube channels
"""

import logging
import subprocess
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    from youtube_transcript_api import YouTubeTranscriptApi

    YOUTUBE_TRANSCRIPT_AVAILABLE = True
except ImportError:
    YOUTUBE_TRANSCRIPT_AVAILABLE = False
    logging.warning("youtube_transcript_api not available, using fallback methods")

logger = logging.getLogger(__name__)


class YouTubeAdapter:
    """YouTube video discovery and transcript fetching adapter"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize YouTube adapter with configuration"""
        self.config = config
        self.extract_flat_timeout = config.get("extract_flat_timeout", 30)
        self.transcript_timeout = config.get("transcript_timeout", 60)
        self.max_video_age_days = config.get("max_video_age_days", 3650)

    def discover_videos(
        self,
        channel_url: str,
        selection: str = "oldest",
        max_videos: int = 10,
        date_range: Optional[Dict[str, str]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Discover videos from a YouTube channel using yt-dlp extract_flat

        Args:
            channel_url: YouTube channel URL
            selection: Video selection method (oldest|latest|by_date_range|ids)
            max_videos: Maximum number of videos to discover
            date_range: Date range filter (start_date, end_date)
            ids: Specific video IDs to fetch

        Returns:
            List of video metadata dictionaries
        """
        logger.info(
            f"Discovering videos from {channel_url} with selection={selection}, max_videos={max_videos}"  # noqa: E501
        )

        if ids:
            # Fetch specific video IDs
            return self._fetch_specific_videos(ids, max_videos)

        # Build yt-dlp command for channel extraction
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--no-playlist",
            "--print",
            "id,title,upload_date,view_count,duration,webpage_url",
            "--max-downloads",
            str(max_videos),
            "--ignore-errors",
            "--no-warnings",
        ]

        # Add date range filter if specified
        if date_range and selection == "by_date_range":
            start_date = date_range.get("start_date")
            end_date = date_range.get("end_date")
            if start_date:
                cmd.extend(["--dateafter", start_date])
            if end_date:
                cmd.extend(["--datebefore", end_date])

        # Add channel URL
        cmd.append(channel_url)

        try:
            logger.debug(f"Running yt-dlp command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.extract_flat_timeout
            )

            if result.returncode != 0:
                logger.error(f"yt-dlp failed: {result.stderr}")
                return []

            # Parse the output
            videos = self._parse_yt_dlp_output(result.stdout)

            # Apply selection logic
            videos = self._apply_selection(videos, selection, max_videos)

            logger.info(f"Discovered {len(videos)} videos from {channel_url}")
            return videos

        except subprocess.TimeoutExpired:
            logger.error(f"yt-dlp timeout after {self.extract_flat_timeout}s")
            return []
        except Exception as e:
            logger.error(f"Error discovering videos: {e}")
            return []

    def _fetch_specific_videos(
        self, ids: List[str], max_videos: int
    ) -> List[Dict[str, Any]]:
        """Fetch specific video IDs"""
        videos = []
        for video_id in ids[:max_videos]:
            try:
                cmd = [
                    "yt-dlp",
                    "--flat-playlist",
                    "--print",
                    "id,title,upload_date,view_count,duration,webpage_url",
                    f"https://www.youtube.com/watch?v={video_id}",
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    video_data = self._parse_single_video_output(result.stdout)
                    if video_data:
                        videos.append(video_data)

            except Exception as e:
                logger.warning(f"Failed to fetch video {video_id}: {e}")

        return videos

    def _parse_yt_dlp_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse yt-dlp extract_flat output"""
        videos = []
        lines = output.strip().split("\n")

        # Group lines into video entries (6 lines per video)
        for i in range(0, len(lines), 6):
            if i + 5 < len(lines):
                try:
                    video_data = {
                        "id": lines[i].split("v=")[-1]
                        if "v=" in lines[i]
                        else lines[i],
                        "title": lines[i + 1],
                        "upload_date": lines[i + 2],
                        "view_count": int(lines[i + 3])
                        if lines[i + 3].isdigit()
                        else 0,
                        "duration": float(lines[i + 4])
                        if lines[i + 4].replace(".", "").isdigit()
                        else 0,
                        "webpage_url": lines[i + 5],
                        "source_type": "youtube",
                    }
                    videos.append(video_data)
                except Exception as e:
                    logger.warning(
                        f"Failed to parse video group starting at line {i}: {e}"
                    )
                    continue

        return videos

    def _parse_single_video_output(self, output: str) -> Optional[Dict[str, Any]]:
        """Parse single video output from yt-dlp"""
        lines = output.strip().split("\n")
        if lines:
            return (
                self._parse_yt_dlp_output(lines[0])[0]
                if self._parse_yt_dlp_output(lines[0])
                else None
            )
        return None

    def _apply_selection(
        self, videos: List[Dict[str, Any]], selection: str, max_videos: int
    ) -> List[Dict[str, Any]]:
        """Apply selection logic to video list"""
        if not videos:
            return []

        if selection == "oldest":
            # Sort by upload date (oldest first)
            videos.sort(key=lambda x: x.get("upload_date", "99999999"))
        elif selection == "latest":
            # Sort by upload date (newest first)
            videos.sort(key=lambda x: x.get("upload_date", "00000000"), reverse=True)
        elif selection == "popular":
            # Sort by view count (highest first)
            videos.sort(key=lambda x: x.get("view_count", 0), reverse=True)

        # Apply max_videos limit
        return videos[:max_videos]

    def fetch_transcript(
        self,
        video_id: str,
        transcript_pref: str = "yt_api",
    ) -> str:
        """
        Fetch transcript for a YouTube video

        Args:
            video_id: YouTube video ID
            transcript_pref: Transcript preference (yt_api|whisper_local|both)

        Returns:
            Transcript text or None if not available
        """
        logger.info(
            f"Fetching transcript for video {video_id} with preference {transcript_pref}"  # noqa: E501
        )

        method = transcript_pref.strip().lower()

        if method == "yt_api":
            if not YOUTUBE_TRANSCRIPT_AVAILABLE:
                raise RuntimeError("youtube_transcript_api not available")
            try:
                api = YouTubeTranscriptApi()
                transcript = api.fetch(video_id)
                text_content = " ".join([entry.text for entry in transcript])
                if not text_content.strip():
                    raise ValueError("empty transcript text")
                return text_content
            except Exception as e:
                raise RuntimeError(f"YouTube Transcript API failed: {e}")

        if method == "autosubs":
            text_content = self._fetch_transcript_autosubs(video_id)
            if not text_content or not text_content.strip():
                raise RuntimeError("yt-dlp autosubs returned empty transcript")
            return text_content

        raise ValueError(f"Unsupported transcript_pref: {transcript_pref}")

    def _fetch_transcript_whisper_local(self, video_id: str) -> Optional[str]:
        """
        Fetch transcript using local Whisper (placeholder implementation)

        This is a placeholder for future Whisper integration.
        For now, it returns None to indicate no local transcript available.
        """
        # Task: Whisper Transcription - See TASKS.md for details
        # This would involve:
        # 1. Downloading the audio using yt-dlp
        # 2. Running Whisper locally on the audio
        # 3. Returning the transcribed text

        logger.debug(f"Whisper local transcription not implemented for {video_id}")
        raise NotImplementedError("whisper_local transcription not implemented")

    def _fetch_transcript_autosubs(self, video_id: str) -> Optional[str]:
        """Fetch subtitles via yt-dlp auto-sub feature and parse VTT."""
        sources_dir = Path("data/sources")
        sources_dir.mkdir(parents=True, exist_ok=True)
        url = f"https://www.youtube.com/watch?v={video_id}"
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--sub-lang",
            "en",
            "--convert-subs",
            "vtt",
            "-o",
            str(sources_dir / f"{video_id}_%(ext)s.%(ext)s"),
            url,
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=self.transcript_timeout
        )
        if result.returncode != 0:
            logger.warning(
                f"yt-dlp returned {result.returncode} for {video_id}: {result.stderr.strip()}"  # noqa: E501
            )
            return None
        vtts = list(sources_dir.glob(f"{video_id}_*.vtt"))
        if not vtts:
            return None
        return self._parse_vtt_file(vtts[0])

    def _parse_vtt_file(self, vtt_path: Path) -> str:
        """Parse a .vtt subtitle file into plain text."""
        try:
            lines: list[str] = []
            with open(vtt_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    s = line.strip()
                    if not s:
                        continue
                    if s.startswith("WEBVTT"):
                        continue
                    if "-->" in s:
                        continue
                    if s.isdigit():
                        continue
                    lines.append(s)
            return "\n".join(lines)
        except Exception as e:
            logger.warning(f"Failed to parse VTT {vtt_path}: {e}")
            return ""

    def get_video_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get additional video metadata"""
        try:
            cmd = [
                "yt-dlp",
                "--extract-flat",
                "--print",
                "id,title,upload_date,view_count,duration,webpage_url,description,channel,channel_id",
                f"https://www.youtube.com/watch?v={video_id}",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                video_data = self._parse_single_video_output(result.stdout)
                return video_data

        except Exception as e:
            logger.warning(f"Failed to get metadata for video {video_id}: {e}")

        return None
