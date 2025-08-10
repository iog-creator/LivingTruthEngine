#!/usr/bin/env python3
"""
Transcript-Only Archive - First 3 Videos from Imagination Podcast Channel
ONLY downloads transcripts, NO video files
"""

import sys
import os
from pathlib import Path
import yt_dlp
import json
from datetime import datetime
import requests

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def get_channel_videos(channel_url, max_videos=3):
    """Get the first few videos from a channel"""
    print(f"🔍 Getting first {max_videos} videos from: {channel_url}")
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'extract_info': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get channel info
            channel_info = ydl.extract_info(channel_url, download=False)
            
            if 'entries' in channel_info:
                videos = channel_info['entries'][:max_videos]
                print(f"✅ Found {len(videos)} videos")
                return videos
            else:
                print("❌ No videos found")
                return []
                
    except Exception as e:
        print(f"❌ Error getting channel videos: {e}")
        return []

def download_transcript_only(video_id, video_title):
    """Download ONLY transcript for a single video - NO video files"""
    print(f"📝 Downloading transcript ONLY for: {video_title}")
    
    # Use yt-dlp to get transcript URL without downloading video
    ydl_opts = {
        'extract_info': True,
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,  # Don't download video
    }
    
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Try to get automatic captions
            if 'automatic_captions' in info and 'en' in info['automatic_captions']:
                caption_url = info['automatic_captions']['en'][0]['url']
                print(f"✅ Found automatic captions for {video_id}")
            elif 'subtitles' in info and 'en' in info['subtitles']:
                caption_url = info['subtitles']['en'][0]['url']
                print(f"✅ Found manual captions for {video_id}")
            else:
                print(f"⚠️ No captions found for {video_id}")
                return None
            
            # Download the transcript file directly
            transcript_file = Path(f"data/sources/{video_id}_transcript.vtt")
            response = requests.get(caption_url)
            
            if response.status_code == 200:
                with open(transcript_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✅ Transcript saved: {transcript_file}")
                return str(transcript_file)
            else:
                print(f"❌ Failed to download transcript: {response.status_code}")
                return None
                
    except Exception as e:
        print(f"❌ Error downloading transcript: {e}")
        return None

def main():
    print("🎙️ Transcript-Only Archive - Imagination Podcast (First 3 Videos)")
    print("📝 ONLY downloading transcripts - NO video files")
    print("=" * 70)
    
    # Channel URL
    channel_url = "https://www.youtube.com/@imaginationpodcastofficial"
    
    # Ensure data directory exists
    Path("data/sources").mkdir(parents=True, exist_ok=True)
    
    try:
        # Step 1: Get first 3 videos
        videos = get_channel_videos(channel_url, max_videos=3)
        
        if not videos:
            print("❌ No videos found. Exiting.")
            return
        
        print("\n📋 First 3 Videos:")
        print("-" * 60)
        
        downloaded_transcripts = []
        
        # Step 2: Process each video (transcript only)
        for i, video in enumerate(videos, 1):
            video_id = video.get('id', '')
            title = video.get('title', 'Unknown Title')
            upload_date = video.get('upload_date', 'Unknown Date')
            duration = video.get('duration', 'Unknown Duration')
            
            print(f"\n{i}. {title}")
            print(f"   ID: {video_id}")
            print(f"   Upload Date: {upload_date}")
            print(f"   Duration: {duration} seconds")
            
            # Download transcript ONLY
            transcript_file = download_transcript_only(video_id, title)
            if transcript_file:
                downloaded_transcripts.append({
                    'video_id': video_id,
                    'title': title,
                    'upload_date': upload_date,
                    'duration': duration,
                    'transcript_file': transcript_file
                })
        
        # Step 3: Save summary
        summary = {
            "channel_url": channel_url,
            "channel_name": "imagination_podcast",
            "archive_date": datetime.now().isoformat(),
            "videos_processed": len(downloaded_transcripts),
            "videos": downloaded_transcripts,
            "status": "completed",
            "note": "Transcripts only - no video files downloaded"
        }
        
        summary_file = Path("data/outputs/logs/imagination_podcast_transcripts_summary.json")
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Summary saved to: {summary_file}")
        
        # Step 4: Display results
        print(f"\n🎉 Transcript-Only Archive Complete!")
        print(f"✅ Processed {len(downloaded_transcripts)} videos")
        print(f"📁 Transcripts saved in: data/sources/")
        print(f"💾 No video files downloaded (saved bandwidth and time)")
        
        if downloaded_transcripts:
            print(f"\n📝 Downloaded Transcripts:")
            for video in downloaded_transcripts:
                print(f"   - {video['title']}")
                print(f"     File: {video['transcript_file']}")
        
    except Exception as e:
        print(f"❌ Error during transcript archive: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 