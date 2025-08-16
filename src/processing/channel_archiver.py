#!/usr/bin/env python3
"""
YouTube Channel Archiver - Living Truth Engine Integration
Archives entire YouTube channels by fetching all video transcripts and building a comprehensive knowledge base.
Migrated from living_truth_agent with LivingTruthEngine integration.

Features:
- YouTube channel video extraction
- Video transcript fetching and processing
- Channel knowledge base generation
- RAG-based querying of archived content
- MCP tool integration
"""  # noqa: E501

import sys
import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urlparse, parse_qs
from dataclasses import dataclass, asdict
import yt_dlp
import logging
from datetime import datetime

# Import LivingTruthEngine configuration and components
from src.config import get_config, config
from src.analysis.notebook_agent import AdvancedNotebookAgent

# Setup logging
logger = logging.getLogger(__name__)


@dataclass
class VideoInfo:
    """Structured video information."""

    id: str
    title: str
    url: str
    duration: int
    upload_date: str
    view_count: int
    description: str


@dataclass
class ArchiveResult:
    """Structured archive result."""

    video_id: str
    title: str
    url: str
    status: str
    transcript_length: Optional[int]
    error: Optional[str]
    archived_at: str
    duration: Optional[int]
    upload_date: Optional[str]
    view_count: Optional[int]


@dataclass
class ChannelArchiveSummary:
    """Structured channel archive summary."""

    channel_url: str
    total_videos: int
    successful_archives: int
    failed_archives: int
    archive_date: str
    videos: List[ArchiveResult]


class ChannelArchiver:
    """
    YouTube Channel Archiver for Living Truth Engine.

    Features:
    - YouTube channel video extraction
    - Video transcript fetching and processing
    - Channel knowledge base generation
    - RAG-based querying of archived content
    - MCP tool integration
    """

    def __init__(self, sources_dir: Optional[str] = None, save_mode: str = "full"):
        """Initialize the Channel Archiver.

        Sets base `sources_dir` and default organized output directory. Channel-scoped
        directories are set via `_set_channel_scope` when a channel URL is known.
        """
        self.config = get_config()

        # Set sources directory
        if sources_dir:
            self.sources_dir = Path(sources_dir)
        else:
            self.sources_dir = Path(self.config.paths["sources_dir"])

        self.sources_dir.mkdir(exist_ok=True)

        # Initialize notebook agent for transcript processing
        try:
            self.notebook_agent = AdvancedNotebookAgent()
            logger.info("✅ Notebook agent initialized for channel archiving")
        except Exception as e:
            logger.error(f"❌ Notebook agent initialization failed: {e}")
            self.notebook_agent = None

        # Channel data file
        self.channel_data_file = self.sources_dir / "channel_archive.json"
        # Organized output directory (base). Channel scope applied per channel.
        self.organized_base_dir = self.sources_dir / "organized"
        self.organized_base_dir.mkdir(exist_ok=True)
        # Active organized dir for current channel scope
        self.organized_dir = self.organized_base_dir

        # Telemetry directories/files
        self.logs_dir = self.sources_dir.parent / "outputs" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.telemetry_dir = self.logs_dir / "archive_telemetry"
        self.telemetry_dir.mkdir(parents=True, exist_ok=True)
        self.telemetry_status_file = self.telemetry_dir / "status.json"
        self.telemetry_stream_file = self.telemetry_dir / "current.jsonl"

        # Save mode controls duplication of artifacts
        # minimal: transcript.txt + record.json
        # standard: transcript.txt + transcript_segments.json + record.json (default)
        # full: transcript.txt + transcript_segments.json + subtitles.vtt + record.json
        valid_modes = {"minimal", "standard", "full"}
        env_mode = os.getenv("ARCHIVER_SAVE_MODE", save_mode).strip().lower()
        self.save_mode = env_mode if env_mode in valid_modes else "standard"

        logger.info("✅ ChannelArchiver initialized successfully")

    def _now_iso(self) -> str:
        return datetime.utcnow().isoformat() + "Z"

    def _emit_telemetry(self, event: str, payload: Dict[str, Any]) -> None:
        try:
            record: Dict[str, Any] = {"ts": self._now_iso(), "event": event}
            record.update(payload)
            # Append to stream file
            with self.telemetry_stream_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            # Update status snapshot (overwrite)
            status_snapshot = {
                "ts": record["ts"],
                "event": event,
                "channel_url": payload.get("channel_url"),
                "current_video_id": payload.get("video_id"),
                "current_title": payload.get("title"),
                "progress": payload.get("progress"),
                "total": payload.get("total"),
                "successful": payload.get("successful"),
                "failed": payload.get("failed"),
                "message": payload.get("message"),
            }
            self.telemetry_status_file.write_text(
                json.dumps(status_snapshot, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            logger.debug(f"Telemetry emit failed: {e}")

    def extract_channel_id_from_url(self, url: str) -> Optional[str]:
        """Extract channel ID from various YouTube URL formats."""
        try:
            # Handle different YouTube URL formats
            if "/@" in url:
                # Format: https://www.youtube.com/@channelname
                return url.split("/@")[1].split("/")[0]
            elif "/channel/" in url:
                # Format: https://www.youtube.com/channel/UC...
                return url.split("/channel/")[1].split("/")[0]
            elif "/c/" in url:
                # Format: https://www.youtube.com/c/channelname
                return url.split("/c/")[1].split("/")[0]
            else:
                logger.error(f"Unsupported URL format: {url}")
                return None
        except Exception as e:
            logger.error(f"Error extracting channel ID: {e}")
            return None

    def _set_channel_scope(self, channel_url: str) -> None:
        """Set `self.organized_dir` to a channel-scoped folder under organized/.

        Args:
            channel_url: The YouTube channel URL.
        """
        channel_id = self.extract_channel_id_from_url(channel_url) or "unknown_channel"
        scoped_dir = self.organized_base_dir / channel_id
        scoped_dir.mkdir(parents=True, exist_ok=True)
        self.organized_dir = scoped_dir
        logger.info(f"📁 Using organized channel scope: {self.organized_dir}")

    def get_channel_videos(self, channel_url: str) -> List[VideoInfo]:
        """Get all videos from a YouTube channel."""
        try:
            logger.info(f"Fetching videos from channel: {channel_url}")

            # Configure yt-dlp for channel extraction
            ydl_opts = {
                "extract_flat": True,  # Don't download, just get metadata
                "quiet": True,
                "no_warnings": True,
                "extract_info": True,
                "ignoreerrors": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract channel info
                channel_info = ydl.extract_info(channel_url, download=False)

                if not channel_info:
                    logger.error("Failed to extract channel information")
                    return []

                videos = []
                if "entries" in channel_info:
                    for entry in channel_info["entries"]:
                        if entry and "id" in entry:
                            video_info = VideoInfo(
                                id=entry["id"],
                                title=entry.get("title", "Unknown Title"),
                                url=f"https://www.youtube.com/watch?v={entry['id']}",
                                duration=entry.get("duration", 0),
                                upload_date=entry.get("upload_date", ""),
                                view_count=entry.get("view_count", 0),
                                description=entry.get("description", "")[:500] + "..."
                                if entry.get("description")
                                else "",
                            )
                            videos.append(video_info)

                logger.info(f"Found {len(videos)} videos in channel")
                return videos

        except Exception as e:
            logger.error(f"Error fetching channel videos: {e}")
            return []

    def archive_video(self, video_info: VideoInfo) -> ArchiveResult:
        """Archive a single video by fetching its transcript with retry/backoff.

        Returns a detailed `ArchiveResult` including explicit skip reasons when available.
        """  # noqa: E501
        try:
            video_id = video_info.id
            video_url = video_info.url
            title = video_info.title

            logger.info(f"Archiving video: {title}")

            # Use notebook agent's YouTube tool to fetch transcript (with retries)
            if self.notebook_agent:
                try:
                    # Create the transcript tool
                    from src.analysis.notebook_agent import (
                        create_youtube_transcript_tool,
                    )

                    transcript_tool = create_youtube_transcript_tool(
                        str(self.sources_dir)
                    )

                    max_attempts = 3
                    backoff_seconds = 2
                    result = ""
                    for attempt in range(1, max_attempts + 1):
                        result = transcript_tool.run(video_url)
                        # Explicit skip reasons
                        skip_markers = [
                            "Premieres in",
                            "is a Premiere",
                            "This video is unavailable",
                            "The uploader has not made this video available",
                            "Sign in to confirm your age",
                            "This live event will begin",
                        ]
                        if any(marker in result for marker in skip_markers):
                            break
                        if "❌" not in result and "No subtitles found" not in result:
                            break
                        if attempt < max_attempts:
                            time.sleep(backoff_seconds * attempt)

                    # Check if transcript was successfully fetched
                    if "❌" in result or "No subtitles found" in result:
                        logger.warning(
                            f"Failed to get transcript for {title}: {result}"
                        )
                        return ArchiveResult(
                            video_id=video_id,
                            title=title,
                            url=video_url,
                            status="failed",
                            transcript_length=None,
                            error=result,
                            archived_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                            duration=video_info.duration,
                            upload_date=video_info.upload_date,
                            view_count=video_info.view_count,
                        )

                    # Check if transcript file was created
                    transcript_file = self.sources_dir / f"{video_id}_transcript.txt"
                    if transcript_file.exists():
                        with open(transcript_file, "r", encoding="utf-8") as f:
                            transcript_content = f.read()

                        # Organize per-video assets
                        try:
                            vtt_file = self._find_vtt_file(video_id)
                            self._save_organized_assets(
                                video_info=video_info,
                                transcript_file=transcript_file,
                                vtt_file=vtt_file,
                                archive_result={
                                    "status": "success",
                                    "archived_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                                },
                            )
                        except Exception as organize_error:
                            logger.warning(
                                f"Organization step failed for {title}: {organize_error}"  # noqa: E501
                            )

                        return ArchiveResult(
                            video_id=video_id,
                            title=title,
                            url=video_url,
                            status="success",
                            transcript_length=len(transcript_content),
                            error=None,
                            archived_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                            duration=video_info.duration,
                            upload_date=video_info.upload_date,
                            view_count=video_info.view_count,
                        )
                    else:
                        logger.warning(f"Transcript file not found for {title}")
                        return ArchiveResult(
                            video_id=video_id,
                            title=title,
                            url=video_url,
                            status="failed",
                            transcript_length=None,
                            error="Transcript file not created",
                            archived_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                            duration=video_info.duration,
                            upload_date=video_info.upload_date,
                            view_count=video_info.view_count,
                        )

                except Exception as e:
                    logger.error(f"Error using notebook agent for {title}: {e}")
                    return ArchiveResult(
                        video_id=video_id,
                        title=title,
                        url=video_url,
                        status="failed",
                        transcript_length=None,
                        error=str(e),
                        archived_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                        duration=video_info.duration,
                        upload_date=video_info.upload_date,
                        view_count=video_info.view_count,
                    )
            else:
                logger.error("Notebook agent not available for transcript fetching")
                return ArchiveResult(
                    video_id=video_id,
                    title=title,
                    url=video_url,
                    status="failed",
                    transcript_length=None,
                    error="Notebook agent not available",
                    archived_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                    duration=video_info.duration,
                    upload_date=video_info.upload_date,
                    view_count=video_info.view_count,
                )

        except Exception as e:
            logger.error(f"Error archiving video {video_info.title}: {e}")
            return ArchiveResult(
                video_id=video_info.id,
                title=video_info.title,
                url=video_info.url,
                status="failed",
                transcript_length=None,
                error=str(e),
                archived_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                duration=video_info.duration,
                upload_date=video_info.upload_date,
                view_count=video_info.view_count,
            )

    def _find_vtt_file(self, video_id: str) -> Optional[Path]:
        """Find a VTT subtitle file for a given video id in sources directory."""
        try:
            candidates = sorted(self.sources_dir.glob(f"{video_id}_*.vtt"))
            return candidates[0] if candidates else None
        except Exception:
            return None

    def _parse_vtt_to_segments(self, vtt_file: Path) -> List[Dict[str, Any]]:
        """Parse a WebVTT file into a list of segments with start/end and text."""
        segments: List[Dict[str, Any]] = []
        try:
            with open(vtt_file, "r", encoding="utf-8") as f:
                lines = [line.rstrip("\n") for line in f]

            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if "-->" in line:
                    # Time cue line
                    try:
                        start_str, end_str = [x.strip() for x in line.split("-->")]
                    except Exception:
                        i += 1
                        continue
                    i += 1
                    text_lines: List[str] = []
                    while i < len(lines) and lines[i].strip() and "-->" not in lines[i]:
                        # skip indices like '1', '2'
                        if (
                            lines[i].strip().isdigit()
                            or lines[i].strip().upper() == "WEBVTT"
                        ):
                            i += 1
                            continue
                        text_lines.append(lines[i].strip())
                        i += 1
                    if text_lines:
                        segments.append(
                            {
                                "start": start_str,
                                "end": end_str,
                                "text": " ".join(text_lines),
                            }
                        )
                else:
                    i += 1
        except Exception as e:
            logger.warning(f"Failed to parse VTT segments from {vtt_file}: {e}")
        return segments

    def _save_organized_assets(
        self,
        video_info: VideoInfo,
        transcript_file: Path,
        vtt_file: Optional[Path],
        archive_result: Dict[str, Any],
    ) -> Path:
        """
        Save per-video organized assets:
        - Directory: data/sources/organized/<video_id>/
        - Files: transcript.txt, transcript_segments.json (if VTT available), metadata.json, subtitles.vtt
        Also updates organized index at data/sources/organized/organized_transcripts.json
        """  # noqa: E501
        video_dir = self.organized_dir / video_info.id
        video_dir.mkdir(parents=True, exist_ok=True)

        # Save transcript
        organized_transcript = video_dir / "transcript.txt"
        organized_transcript.write_text(
            transcript_file.read_text(encoding="utf-8"), encoding="utf-8"
        )

        # Copy subtitles and parse segments according to save_mode
        organized_vtt_path = None
        segments: List[Dict[str, Any]] = []
        if vtt_file and vtt_file.exists():
            # Always parse segments if available for standard/full modes
            if self.save_mode in {"standard", "full"}:
                segments = self._parse_vtt_to_segments(vtt_file)
                if segments:
                    (video_dir / "transcript_segments.json").write_text(
                        json.dumps(segments, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )
            # Only keep raw VTT when in full mode
            if self.save_mode == "full":
                organized_vtt_path = video_dir / "subtitles.vtt"
                try:
                    organized_vtt_path.write_text(
                        vtt_file.read_text(encoding="utf-8"), encoding="utf-8"
                    )
                except Exception as e:
                    logger.warning(f"Failed to copy VTT file for {video_info.id}: {e}")

        # Write metadata (lightweight)
        metadata: Dict[str, Any] = {
            "video_id": video_info.id,
            "title": video_info.title,
            "url": video_info.url,
            "duration": video_info.duration,
            "upload_date": video_info.upload_date,
            "view_count": video_info.view_count,
            "transcript_path": str(organized_transcript),
            "subtitles_path": str(organized_vtt_path) if organized_vtt_path else None,
            "segments_count": len(segments),
            "archived_at": archive_result.get("archived_at"),
            "status": archive_result.get("status", "success"),
        }
        (video_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Write consolidated record with readable fields (no timestamps)
        record: Dict[str, Any] = {
            "video_id": video_info.id,
            "title": video_info.title,
            "url": video_info.url,
            "summary": {
                "duration": video_info.duration,
                "upload_date": video_info.upload_date,
                "view_count": video_info.view_count,
                "segments": len(segments),
            },
            "paths": {
                "transcript": str(organized_transcript),
                "segments": str(video_dir / "transcript_segments.json")
                if segments
                else None,
                "subtitles": str(organized_vtt_path) if organized_vtt_path else None,
            },
        }
        (video_dir / "record.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Ensure editable space exists for user-added information
        notes_path = video_dir / "notes.md"
        annotations_path = video_dir / "annotations.json"
        if not notes_path.exists():
            notes_path.write_text(
                f"# Notes for {video_info.title}\n\n- Add observations, hypotheses, corroborations here.\n",  # noqa: E501
                encoding="utf-8",
            )
        if not annotations_path.exists():
            annotations_path.write_text(
                json.dumps(
                    {"tags": [], "entities": [], "links": []},
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

        # Update organized index
        organized_index = self.organized_dir / "organized_transcripts.json"
        try:
            index_data: List[Dict[str, Any]] = []
            if organized_index.exists():
                index_data = json.loads(organized_index.read_text(encoding="utf-8"))
            # de-duplicate by video_id
            index_data = [
                item for item in index_data if item.get("video_id") != video_info.id
            ]
            index_entry = {
                "video_id": video_info.id,
                "title": video_info.title,
                "organized_dir": str(video_dir),
                "transcript": str(organized_transcript),
                "segments": len(segments),
                "url": video_info.url,
            }
            index_data.append(index_entry)
            organized_index.write_text(
                json.dumps(index_data, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as e:
            logger.warning(f"Failed updating organized index for {video_info.id}: {e}")

        return video_dir

    def organize_existing_archives(self) -> Dict[str, Any]:
        """
        Organize any existing successful archives into per-video directories,
        building metadata and segment JSON where possible.
        """
        summary: Dict[str, Any] = {"processed": 0, "skipped": 0}
        if not self.channel_data_file.exists():
            return summary
        data = json.loads(self.channel_data_file.read_text(encoding="utf-8"))
        # Apply channel scope based on saved archive channel URL
        channel_url = data.get("channel_url")
        if channel_url:
            self._set_channel_scope(channel_url)
        videos = data.get("videos", [])
        for v in videos:
            if v.get("status") != "success":
                summary["skipped"] += 1
                continue
            video_id = v.get("video_id")
            title = v.get("title", "")
            url = v.get("url", "")
            duration = v.get("duration") or 0
            upload_date = v.get("upload_date", "")
            view_count = v.get("view_count") or 0
            video_info = VideoInfo(
                id=video_id,
                title=title,
                url=url,
                duration=duration,
                upload_date=upload_date,
                view_count=view_count,
                description="",
            )
            transcript_file = self.sources_dir / f"{video_id}_transcript.txt"
            if not transcript_file.exists():
                summary["skipped"] += 1
                continue
            vtt_file = self._find_vtt_file(video_id)
            try:
                self._save_organized_assets(
                    video_info,
                    transcript_file,
                    vtt_file,
                    {"status": "success", "archived_at": v.get("archived_at")},
                )
                summary["processed"] += 1
            except Exception as e:
                logger.warning(f"Organize existing failed for {video_id}: {e}")
        return summary

    def rebuild_organized_index(
        self, channel_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Rebuild the organized index JSON by scanning the channel-scoped directory.

        Args:
            channel_url: If provided, scope the rebuild to this channel; otherwise, use
                         the scope from the existing `channel_archive.json` if present.

        Returns:
            Summary with counts and output path.
        """
        try:
            if channel_url:
                self._set_channel_scope(channel_url)
            elif self.channel_data_file.exists():
                archive = json.loads(self.channel_data_file.read_text(encoding="utf-8"))
                if archive.get("channel_url"):
                    self._set_channel_scope(archive["channel_url"])

            index_path = self.organized_dir / "organized_transcripts.json"
            entries: List[Dict[str, Any]] = []
            if not self.organized_dir.exists():
                return {"rebuilt": 0, "index": str(index_path)}

            for video_dir in sorted(self.organized_dir.iterdir()):
                if not video_dir.is_dir():
                    continue
                meta = video_dir / "metadata.json"
                transcript = video_dir / "transcript.txt"
                segments_path = video_dir / "transcript_segments.json"
                if not transcript.exists():
                    continue
                entry: Dict[str, Any] = {
                    "video_id": video_dir.name,
                    "organized_dir": str(video_dir),
                    "transcript": str(transcript),
                    "segments": 0,
                    "url": None,
                    "title": None,
                }
                if meta.exists():
                    try:
                        meta_data = json.loads(meta.read_text(encoding="utf-8"))
                        entry.update(
                            {
                                "title": meta_data.get("title"),
                                "url": meta_data.get("url"),
                                "segments": int(meta_data.get("segments_count", 0)),
                            }
                        )
                    except Exception:
                        pass
                elif segments_path.exists():
                    try:
                        segs = json.loads(segments_path.read_text(encoding="utf-8"))
                        entry["segments"] = len(segs) if isinstance(segs, list) else 0
                    except Exception:
                        entry["segments"] = 0
                entries.append(entry)

            index_path.write_text(
                json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            return {"rebuilt": len(entries), "index": str(index_path)}
        except Exception as e:
            logger.error(f"Failed to rebuild organized index: {e}")
            return {"error": str(e)}

    def archive_channel(
        self, channel_url: str, max_videos: Optional[int] = None
    ) -> ChannelArchiveSummary:
        """Archive an entire YouTube channel."""
        try:
            logger.info(f"Starting channel archive: {channel_url}")
            # Ensure organized dir is scoped to this channel
            self._set_channel_scope(channel_url)
            # Start telemetry
            self._emit_telemetry(
                "archive_start",
                {"channel_url": channel_url, "message": "Starting archive"},
            )

            # Get all videos from the channel
            videos = self.get_channel_videos(channel_url)

            if not videos:
                logger.error("No videos found in channel")
                return ChannelArchiveSummary(
                    channel_url=channel_url,
                    total_videos=0,
                    successful_archives=0,
                    failed_archives=0,
                    archive_date=time.strftime("%Y-%m-%d %H:%M:%S"),
                    videos=[],
                )

            # Limit videos if specified
            if max_videos:
                videos = videos[:max_videos]
                logger.info(f"Limited to {max_videos} videos")

            # Archive each video
            archive_results = []
            successful_archives = 0
            failed_archives = 0

            total = len(videos)
            for i, video in enumerate(videos, 1):
                logger.info(f"Processing video {i}/{total}: {video.title}")
                self._emit_telemetry(
                    "video_start",
                    {
                        "channel_url": channel_url,
                        "video_id": video.id,
                        "title": video.title,
                        "progress": i,
                        "total": total,
                        "successful": successful_archives,
                        "failed": failed_archives,
                        "message": "Archiving video",
                    },
                )

                result = self.archive_video(video)
                archive_results.append(result)

                if result.status == "success":
                    successful_archives += 1
                else:
                    failed_archives += 1

                self._emit_telemetry(
                    "video_result",
                    {
                        "channel_url": channel_url,
                        "video_id": result.video_id,
                        "title": result.title,
                        "progress": i,
                        "total": total,
                        "successful": successful_archives,
                        "failed": failed_archives,
                        "status": result.status,
                        "error": result.error,
                        "transcript_length": result.transcript_length,
                        "message": "Video archived",
                    },
                )

                # Add delay to be respectful to YouTube
                time.sleep(2)

            # Create archive summary
            archive_summary = ChannelArchiveSummary(
                channel_url=channel_url,
                total_videos=len(videos),
                successful_archives=successful_archives,
                failed_archives=failed_archives,
                archive_date=time.strftime("%Y-%m-%d %H:%M:%S"),
                videos=archive_results,
            )

            # Save archive data
            with open(self.channel_data_file, "w", encoding="utf-8") as f:
                json.dump(asdict(archive_summary), f, indent=2, ensure_ascii=False)

            logger.info(f"Channel archive completed!")
            logger.info(
                f"Successfully archived: {successful_archives}/{len(videos)} videos"
            )

            # Complete telemetry
            self._emit_telemetry(
                "archive_complete",
                {
                    "channel_url": channel_url,
                    "successful": successful_archives,
                    "failed": failed_archives,
                    "total": len(videos),
                    "message": "Archive complete",
                },
            )

            return archive_summary

        except Exception as e:
            logger.error(f"Error archiving channel: {e}")
            return ChannelArchiveSummary(
                channel_url=channel_url,
                total_videos=0,
                successful_archives=0,
                failed_archives=0,
                archive_date=time.strftime("%Y-%m-%d %H:%M:%S"),
                videos=[],
            )

    def build_channel_knowledge_base(self) -> str:
        """Build a comprehensive knowledge base from all archived videos."""
        try:
            if not self.channel_data_file.exists():
                return "No channel archive found. Please run archive_channel() first."

            # Load archive data
            with open(self.channel_data_file, "r", encoding="utf-8") as f:
                archive_data = json.load(f)

            # Get all successful transcripts
            successful_videos = [
                v for v in archive_data["videos"] if v["status"] == "success"
            ]

            if not successful_videos:
                return "No successful transcripts found in archive."

            # Build knowledge base
            knowledge_base = f"# Channel Knowledge Base\n\n"
            knowledge_base += f"**Channel**: {archive_data['channel_url']}\n"
            knowledge_base += f"**Archive Date**: {archive_data['archive_date']}\n"
            knowledge_base += f"**Total Videos**: {archive_data['total_videos']}\n"
            knowledge_base += (
                f"**Successfully Archived**: {archive_data['successful_archives']}\n\n"
            )

            knowledge_base += "## Video Index\n\n"

            for video in successful_videos:
                knowledge_base += f"### {video['title']}\n"
                knowledge_base += f"- **URL**: {video['url']}\n"
                knowledge_base += (
                    f"- **Duration**: {video.get('duration', 'Unknown')} seconds\n"
                )
                knowledge_base += (
                    f"- **Upload Date**: {video.get('upload_date', 'Unknown')}\n"
                )
                knowledge_base += f"- **Transcript Length**: {video['transcript_length']} characters\n\n"  # noqa: E501

            # Save knowledge base
            kb_file = self.sources_dir / "channel_knowledge_base.md"
            with open(kb_file, "w", encoding="utf-8") as f:
                f.write(knowledge_base)

            logger.info(f"Knowledge base created: {kb_file}")
            return f"Knowledge base created with {len(successful_videos)} videos"

        except Exception as e:
            logger.error(f"Error building knowledge base: {e}")
            return f"Error building knowledge base: {str(e)}"

    def query_channel_knowledge(self, query: str) -> str:
        """Query the archived channel knowledge using RAG."""
        try:
            if not self.notebook_agent:
                return "Notebook agent not available for querying"

            # Rebuild RAG system with all archived content
            self.notebook_agent.build_rag_system()

            # Process query using RAG
            response = self.notebook_agent._process_with_rag(query)
            return response

        except Exception as e:
            logger.error(f"Error querying channel knowledge: {e}")
            return f"Error querying knowledge base: {str(e)}"

    def get_archive_status(self) -> Dict[str, Any]:
        """Get status of channel archive."""
        try:
            status = {
                "archive_exists": self.channel_data_file.exists(),
                "sources_directory": str(self.sources_dir),
                "channel_data_file": str(self.channel_data_file),
                "notebook_agent_available": bool(self.notebook_agent),
            }

            if self.channel_data_file.exists():
                with open(self.channel_data_file, "r", encoding="utf-8") as f:
                    archive_data = json.load(f)

                status.update(
                    {
                        "channel_url": archive_data.get("channel_url", "Unknown"),
                        "total_videos": archive_data.get("total_videos", 0),
                        "successful_archives": archive_data.get(
                            "successful_archives", 0
                        ),
                        "failed_archives": archive_data.get("failed_archives", 0),
                        "archive_date": archive_data.get("archive_date", "Unknown"),
                    }
                )

            return status

        except Exception as e:
            logger.error(f"Error getting archive status: {e}")
            return {"error": str(e)}

    def list_archived_videos(self) -> List[Dict[str, Any]]:
        """List all archived videos with their status."""
        try:
            if not self.channel_data_file.exists():
                return []

            with open(self.channel_data_file, "r", encoding="utf-8") as f:
                archive_data = json.load(f)

            return archive_data.get("videos", [])

        except Exception as e:
            logger.error(f"Error listing archived videos: {e}")
            return []

    def get_video_transcript(self, video_id: str) -> str:
        """Get transcript for a specific video."""
        try:
            transcript_file = self.sources_dir / f"{video_id}_transcript.txt"

            if not transcript_file.exists():
                return f"Transcript not found for video {video_id}"

            with open(transcript_file, "r", encoding="utf-8") as f:
                transcript = f.read()

            return transcript

        except Exception as e:
            logger.error(f"Error getting video transcript: {e}")
            return f"Error retrieving transcript: {str(e)}"

    def download_transcripts(self, channel_url: str, max_videos: int = 10) -> List[str]:
        """
        Download transcripts from a YouTube channel.

        Args:
            channel_url: URL of the YouTube channel
            max_videos: Maximum number of videos to process

        Returns:
            List of transcript file paths
        """
        logger.info(f"Starting transcript download for channel: {channel_url}")

        try:
            # Get channel videos
            videos = self.get_channel_videos(channel_url)
            if not videos:
                logger.error(f"No videos found for channel: {channel_url}")
                return []

            # Limit to max_videos
            videos = videos[:max_videos]
            logger.info(f"Processing {len(videos)} videos from channel")

            transcript_files = []

            for video in videos:
                try:
                    # Archive the video (this includes transcript download)
                    result = self.archive_video(video)

                    if result.status == "success" and result.transcript_length:
                        transcript_file = (
                            self.sources_dir / f"{video.id}_transcript.txt"
                        )
                        if transcript_file.exists():
                            transcript_files.append(str(transcript_file))
                            logger.info(f"✅ Downloaded transcript for: {video.title}")
                        else:
                            logger.warning(
                                f"Transcript file not found for: {video.title}"
                            )
                    else:
                        logger.warning(
                            f"Failed to download transcript for: {video.title} - {result.error}"  # noqa: E501
                        )

                except Exception as e:
                    logger.error(f"Error processing video {video.title}: {e}")
                    continue

            logger.info(f"Downloaded {len(transcript_files)} transcripts successfully")
            return transcript_files

        except Exception as e:
            logger.error(f"Error downloading transcripts: {e}")
            return []

    def close(self):
        """Clean up resources."""
        try:
            # Clean up notebook agent if needed
            if self.notebook_agent:
                # Add cleanup logic if needed
                pass

            logger.info("✅ ChannelArchiver resources cleaned up")

        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")


def main():
    """Main function for testing the channel archiver."""
    try:
        print("🎥 YouTube Channel Archiver - Living Truth Engine")
        print("=" * 60)

        # Create archiver
        archiver = ChannelArchiver()

        # Test channel URL
        channel_url = "https://www.youtube.com/@imaginationpodcastofficial"

        print(f"📺 Archiving channel: {channel_url}")
        print("This will fetch all video transcripts and build a knowledge base.")
        print("This may take a while depending on the number of videos...")
        print()

        # Archive the channel (limit to first 5 videos for testing)
        print("🔄 Starting channel archive...")
        result = archiver.archive_channel(channel_url, max_videos=5)

        # Print results
        print(f"\n✅ Archive completed!")
        print(f"📊 Results:")
        print(f"   - Total videos found: {result.total_videos}")
        print(f"   - Successfully archived: {result.successful_archives}")
        print(f"   - Failed archives: {result.failed_archives}")

        # Build knowledge base
        print(f"\n📚 Building knowledge base...")
        kb_result = archiver.build_channel_knowledge_base()
        print(f"✅ {kb_result}")

        # Test query
        print(f"\n🔍 Testing knowledge base query...")
        test_query = "What are the main topics discussed in this channel?"
        response = archiver.query_channel_knowledge(test_query)
        print(f"📝 Response: {response}")

        print(f"\n🎉 Channel archive complete!")
        print(f"📁 Check the 'sources/' directory for archived content")
        print(f"📄 Channel data saved to: {archiver.channel_data_file}")

    except Exception as e:
        logger.error(f"Main function error: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
