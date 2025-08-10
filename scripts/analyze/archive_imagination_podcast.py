#!/usr/bin/env python3
"""
Archive Imagination Podcast Channel - Focus on 10 Oldest Videos
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from processing.channel_archiver import ChannelArchiver
import json
from datetime import datetime

def main():
    print("🎙️ Starting Imagination Podcast Channel Archive")
    print("=" * 60)
    
    # Initialize channel archiver
    archiver = ChannelArchiver()
    
    # Channel URL
    channel_url = "https://www.youtube.com/@imaginationpodcastofficial"
    channel_name = "imagination_podcast"
    
    print(f"📺 Channel: {channel_url}")
    print(f"📁 Channel Name: {channel_name}")
    print()
    
    try:
        # Step 1: Archive the channel
        print("🔄 Step 1: Archiving channel...")
        archive_result = archiver.archive_channel(channel_url)
        
        if archive_result and "success" in archive_result.lower():
            print("✅ Channel archive initiated successfully")
        else:
            print(f"⚠️ Channel archive result: {archive_result}")
        
        print()
        
        # Step 2: Get channel archive status
        print("📊 Step 2: Getting archive status...")
        status = archiver.get_archive_status()
        print(f"Archive Status: {status}")
        
        print()
        
        # Step 3: List archived videos
        print("📋 Step 3: Listing archived videos...")
        videos = archiver.list_archived_videos()
        
        if videos and isinstance(videos, list):
            print(f"✅ Found {len(videos)} archived videos")
            
            # Sort by upload date to get oldest first
            sorted_videos = sorted(videos, key=lambda x: x.get('upload_date', ''))
            
            print("\n📅 10 Oldest Videos:")
            print("-" * 80)
            
            for i, video in enumerate(sorted_videos[:10], 1):
                video_id = video.get('id', 'Unknown')
                title = video.get('title', 'Unknown Title')
                upload_date = video.get('upload_date', 'Unknown Date')
                duration = video.get('duration', 'Unknown Duration')
                
                print(f"{i:2d}. {title}")
                print(f"    ID: {video_id}")
                print(f"    Upload Date: {upload_date}")
                print(f"    Duration: {duration}")
                print()
            
            # Step 4: Process the 10 oldest videos
            print("🎬 Step 4: Processing 10 oldest videos...")
            print("-" * 80)
            
            for i, video in enumerate(sorted_videos[:10], 1):
                video_id = video.get('id', '')
                title = video.get('title', 'Unknown Title')
                
                print(f"Processing {i}/10: {title}")
                print(f"Video ID: {video_id}")
                
                # Get transcript for this video
                try:
                    transcript_result = archiver.get_video_transcript(video_id)
                    if transcript_result and "success" in transcript_result.lower():
                        print(f"✅ Transcript processed for: {title}")
                    else:
                        print(f"⚠️ Transcript processing result: {transcript_result}")
                except Exception as e:
                    print(f"❌ Error processing transcript: {e}")
                
                print()
            
            # Step 5: Build knowledge base from processed videos
            print("🧠 Step 5: Building knowledge base...")
            kb_result = archiver.build_channel_knowledge_base(channel_name)
            print(f"Knowledge Base Result: {kb_result}")
            
            print()
            
            # Step 6: Test querying the knowledge base
            print("🔍 Step 6: Testing knowledge base queries...")
            test_queries = [
                "What are the main themes discussed in the oldest episodes?",
                "What topics are covered in the early episodes?",
                "What insights are shared about imagination and creativity?"
            ]
            
            for query in test_queries:
                print(f"\nQuery: {query}")
                try:
                    result = archiver.query_channel_knowledge(query)
                    if result:
                        print(f"✅ Query result: {result[:200]}...")
                    else:
                        print("⚠️ No results found")
                except Exception as e:
                    print(f"❌ Query error: {e}")
            
        else:
            print("❌ No videos found or error listing videos")
            print(f"Videos result: {videos}")
        
        print()
        print("🎉 Imagination Podcast Archive Process Complete!")
        print("=" * 60)
        
        # Save summary
        summary = {
            "channel_url": channel_url,
            "channel_name": channel_name,
            "archive_date": datetime.now().isoformat(),
            "total_videos": len(videos) if videos else 0,
            "processed_videos": min(10, len(videos)) if videos else 0,
            "status": "completed"
        }
        
        summary_file = Path("data/outputs/logs/imagination_podcast_archive_summary.json")
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📄 Summary saved to: {summary_file}")
        
    except Exception as e:
        print(f"❌ Error during archive process: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 