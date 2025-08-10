#!/usr/bin/env python3
"""
Quick Archive - First 3 Videos from Imagination Podcast Channel
"""

import sys
import os
from pathlib import Path
import yt_dlp
import json
from datetime import datetime

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

def download_video_transcript(video_id, video_title):
    """Download transcript for a single video"""
    print(f"📝 Downloading transcript for: {video_title}")
    
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'outtmpl': f'data/sources/{video_id}_%(ext)s.%(ext)s',
        'quiet': True,
    }
    
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # Check if transcript was downloaded
        transcript_file = Path(f"data/sources/{video_id}_en.vtt")
        if transcript_file.exists():
            print(f"✅ Transcript downloaded: {transcript_file}")
            return str(transcript_file)
        else:
            print(f"⚠️ No transcript found for {video_id}")
            return None
            
    except Exception as e:
        print(f"❌ Error downloading transcript: {e}")
        return None

def main():
    print("🎙️ Quick Archive - Imagination Podcast (First 3 Videos)")
    print("=" * 60)
    
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
        
        # Step 2: Process each video
        for i, video in enumerate(videos, 1):
            video_id = video.get('id', '')
            title = video.get('title', 'Unknown Title')
            upload_date = video.get('upload_date', 'Unknown Date')
            duration = video.get('duration', 'Unknown Duration')
            
            print(f"\n{i}. {title}")
            print(f"   ID: {video_id}")
            print(f"   Upload Date: {upload_date}")
            print(f"   Duration: {duration} seconds")
            
            # Download transcript
            transcript_file = download_video_transcript(video_id, title)
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
            "status": "completed"
        }
        
        summary_file = Path("data/outputs/logs/imagination_podcast_quick_summary.json")
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Summary saved to: {summary_file}")
        
        # Step 4: Display results
        print(f"\n🎉 Quick Archive Complete!")
        print(f"✅ Processed {len(downloaded_transcripts)} videos")
        print(f"📁 Transcripts saved in: data/sources/")
        
        if downloaded_transcripts:
            print(f"\n📝 Downloaded Transcripts:")
            for video in downloaded_transcripts:
                print(f"   - {video['title']}")
                print(f"     File: {video['transcript_file']}")
        
    except Exception as e:
        print(f"❌ Error during quick archive: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 