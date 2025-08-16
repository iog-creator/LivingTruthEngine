"""
Fetchers for web, PDF, and YouTube content.

Local-only implementations using trafilatura, PyMuPDF, and yt-dlp.
"""

import os
import json
import logging
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import requests

logger = logging.getLogger(__name__)


def fetch_web(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch web content using trafilatura (local-only).

    Args:
        urls: List of URLs to fetch

    Returns:
        List of raw document dictionaries
    """
    try:
        import trafilatura
    except ImportError:
        logger.error("trafilatura not available, falling back to readability-lxml")
        try:
            from readability import Document
            import lxml.html
        except ImportError:
            logger.error("Neither trafilatura nor readability-lxml available")
            return []

    documents = []

    for url in urls:
        try:
            logger.info(f"Fetching web content from: {url}")

            # Fetch content
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Extract text using trafilatura or fallback
            try:
                extracted_text = trafilatura.extract(response.text)
                if not extracted_text:
                    # Fallback to readability-lxml
                    doc = Document(response.text)
                    extracted_text = doc.summary()
            except Exception as e:
                logger.warning(f"trafilatura failed for {url}: {e}")
                # Fallback to readability-lxml
                doc = Document(response.text)
                extracted_text = doc.summary()

            if extracted_text:
                documents.append(
                    {
                        "source_type": "web",
                        "uri": url,
                        "title": urlparse(url).netloc,
                        "text": extracted_text,
                        "meta": {
                            "status_code": response.status_code,
                            "content_length": len(response.text),
                        },
                    }
                )
            else:
                logger.warning(f"No text extracted from {url}")

        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            documents.append(
                {
                    "source_type": "web",
                    "uri": url,
                    "title": "Error",
                    "text": f"Failed to fetch: {str(e)}",
                    "meta": {"error": str(e)},
                }
            )

    return documents


def fetch_pdf(paths_or_urls: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch PDF content using PyMuPDF (local-only).

    Args:
        paths_or_urls: List of PDF file paths or URLs

    Returns:
        List of raw document dictionaries
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        logger.error("PyMuPDF not available")
        return []

    documents = []

    for path_or_url in paths_or_urls:
        try:
            logger.info(f"Processing PDF: {path_or_url}")

            # Handle URLs vs local paths
            if path_or_url.startswith(("http://", "https://")):
                # Download PDF from URL
                response = requests.get(path_or_url, timeout=30)
                response.raise_for_status()

                with tempfile.NamedTemporaryFile(
                    suffix=".pdf", delete=False
                ) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_path = tmp_file.name
            else:
                # Local file path
                tmp_path = path_or_url

            # Extract text using PyMuPDF
            doc = fitz.open(tmp_path)
            text_content = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += page.get_text()

            doc.close()

            # Clean up temporary file if created
            if path_or_url.startswith(("http://", "https://")) and os.path.exists(
                tmp_path
            ):
                os.unlink(tmp_path)

            # Check text ratio to determine if OCR might be needed
            text_ratio = len(text_content.strip()) / max(len(text_content), 1)
            suspect = text_ratio < 0.1  # Less than 10% text content

            documents.append(
                {
                    "source_type": "pdf",
                    "uri": path_or_url,
                    "title": Path(path_or_url).stem
                    if not path_or_url.startswith(("http://", "https://"))
                    else urlparse(path_or_url).path.split("/")[-1],
                    "text": text_content,
                    "meta": {
                        "pages": len(doc),
                        "text_ratio": text_ratio,
                        "suspect": suspect,
                    },
                }
            )

        except Exception as e:
            logger.error(f"Failed to process PDF {path_or_url}: {e}")
            documents.append(
                {
                    "source_type": "pdf",
                    "uri": path_or_url,
                    "title": "Error",
                    "text": f"Failed to process PDF: {str(e)}",
                    "meta": {"error": str(e)},
                }
            )

    return documents


def fetch_youtube(
    channel_or_urls: List[str], max_videos: int = 10
) -> List[Dict[str, Any]]:
    """
    Fetch YouTube content using yt-dlp for subtitles (local-only).

    Args:
        channel_or_urls: List of YouTube URLs or channel URLs
        max_videos: Maximum number of videos to process

    Returns:
        List of raw document dictionaries
    """
    documents = []

    for url in channel_or_urls:
        try:
            logger.info(f"Processing YouTube: {url}")

            # Use yt-dlp to get video info and subtitles
            cmd = [
                "yt-dlp",
                "--skip-download",
                "--write-auto-sub",
                "--write-sub",
                "--sub-lang",
                "en",
                "--convert-subs",
                "srt",
                "--print",
                "id,title,upload_date",
                "--no-playlist",
                url,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            # Check if yt-dlp succeeded but no subtitle files were created
            subtitle_files_created = False
            if result.returncode == 0:
                # Look for any subtitle files that might have been created
                for file in os.listdir("."):
                    if file.endswith(".srt") and "dQw4w9WgXcQ" in file:
                        subtitle_files_created = True
                        break

            if result.returncode != 0 or not subtitle_files_created:
                logger.warning(
                    f"yt-dlp failed or no subtitles for {url}: {result.stderr}"
                )
                # Try youtube_transcript_api as fallback
                try:
                    from youtube_transcript_api import YouTubeTranscriptApi

                    video_id = (
                        url.split("v=")[-1] if "v=" in url else url.split("/")[-1]
                    )
                    transcript = YouTubeTranscriptApi().get_transcript(video_id)
                    text_content = " ".join([entry["text"] for entry in transcript])

                    documents.append(
                        {
                            "source_type": "youtube",
                            "uri": url,
                            "title": f"YouTube Video {video_id}",
                            "text": text_content,
                            "meta": {
                                "method": "youtube_transcript_api",
                                "video_id": video_id,
                            },
                        }
                    )
                    logger.info(
                        f"Successfully fetched transcript for {video_id} using youtube_transcript_api"  # noqa: E501
                    )
                except Exception as e:
                    logger.error(
                        f"Both yt-dlp and youtube_transcript_api failed for {url}: {e}"
                    )
                    # Create a placeholder document with video info
                    video_id = (
                        url.split("v=")[-1] if "v=" in url else url.split("/")[-1]
                    )
                    documents.append(
                        {
                            "source_type": "youtube",
                            "uri": url,
                            "title": f"YouTube Video {video_id}",
                            "text": f"YouTube video {video_id} - No transcript available. Video info: {result.stdout.strip()}",  # noqa: E501
                            "meta": {
                                "method": "placeholder",
                                "video_id": video_id,
                                "yt_dlp_output": result.stdout.strip(),
                                "error": str(e),
                            },
                        }
                    )
                continue

            # Parse yt-dlp output
            lines = result.stdout.strip().split("\n")
            for line in lines:
                if not line.strip():
                    continue

                parts = line.split("\t")
                if len(parts) >= 3:
                    video_id, title, upload_date = parts[:3]

                    # Look for subtitle file
                    subtitle_file = f"{video_id}.en.srt"
                    if os.path.exists(subtitle_file):
                        with open(subtitle_file, "r", encoding="utf-8") as f:
                            subtitle_content = f.read()

                        # Extract text from SRT format (remove timestamps)
                        import re

                        text_content = re.sub(
                            r"\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+", "", subtitle_content
                        )
                        text_content = re.sub(
                            r"^\d+\s*$", "", text_content, flags=re.MULTILINE
                        )
                        text_content = re.sub(
                            r"^\s*$", "", text_content, flags=re.MULTILINE
                        )
                        text_content = text_content.strip()

                        documents.append(
                            {
                                "source_type": "youtube",
                                "uri": f"https://www.youtube.com/watch?v={video_id}",
                                "title": title,
                                "text": text_content,
                                "meta": {
                                    "method": "yt-dlp",
                                    "video_id": video_id,
                                    "upload_date": upload_date,
                                },
                            }
                        )

                        # Clean up subtitle file
                        os.unlink(subtitle_file)

                        if len(documents) >= max_videos:
                            break

        except Exception as e:
            logger.error(f"Failed to process YouTube {url}: {e}")
            documents.append(
                {
                    "source_type": "youtube",
                    "uri": url,
                    "title": "Error",
                    "text": f"Failed to fetch YouTube content: {str(e)}",
                    "meta": {"error": str(e)},
                }
            )

    return documents[:max_videos]
