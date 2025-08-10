#!/usr/bin/env python3
"""
Proper Analysis - Imagination Podcast Transcripts
Using existing Living Truth Engine components and correct transcript files
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analysis.research_analysis import ResearchAnalysisSystem
from analysis.hybrid_retrieval import HybridRetriever

def read_vtt_transcript(file_path):
    """Read and parse VTT transcript file properly"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse VTT format properly
        lines = content.split('\n')
        transcript_text = []
        
        for line in lines:
            line = line.strip()
            # Skip timestamp lines, WEBVTT header, and empty lines
            if (line and 
                not line.startswith('-->') and 
                not line.startswith('WEBVTT') and 
                not line[0].isdigit() and
                not line.startswith('#')):
                transcript_text.append(line)
        
        return ' '.join(transcript_text)
    except Exception as e:
        print(f"❌ Error reading transcript {file_path}: {e}")
        return None

def analyze_with_existing_components(transcript_text, video_title, video_id):
    """Analyze using existing Living Truth Engine components"""
    print(f"\n🔍 Analyzing: {video_title}")
    print("-" * 60)
    
    try:
        # Initialize existing components
        research_system = ResearchAnalysisSystem()
        retriever = HybridRetriever()
        
        # Step 1: Extract claims and evidence using existing system
        print("📋 Extracting claims and evidence...")
        claims_result = research_system.extract_claims_and_evidence(transcript_text)
        
        # Step 2: Perform Biblical forensic analysis using existing system
        print("📖 Performing Biblical forensic analysis...")
        biblical_result = research_system.biblical_forensic_analysis(transcript_text)
        
        # Step 3: Use hybrid retrieval for additional analysis
        print("🔍 Performing hybrid retrieval analysis...")
        retrieval_result = retriever.analyze_text(transcript_text)
        
        # Compile results
        analysis_result = {
            "video_id": video_id,
            "title": video_title,
            "analysis_date": datetime.now().isoformat(),
            "claims_and_evidence": claims_result,
            "biblical_forensic_analysis": biblical_result,
            "hybrid_retrieval_analysis": retrieval_result,
            "transcript_length": len(transcript_text)
        }
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Error analyzing transcript: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🎙️ Proper Analysis - Imagination Podcast Transcripts")
    print("🔍 Using Existing Living Truth Engine Components")
    print("=" * 70)
    
    # Use the correct transcript files that were already downloaded
    transcript_files = [
        "data/sources/Bdrwd8p4fKc_mp4.en.vtt",
        "data/sources/D691xfozd3A_webm.en.vtt"
    ]
    
    # Video metadata
    video_metadata = {
        "Bdrwd8p4fKc": {
            "title": "S5E92 | JR Sweet - MK ULTRA Mass Shootings & Assassinations, Amnesic Slavery, & Bloodline Networks",
            "duration": "8230.0 seconds"
        },
        "D691xfozd3A": {
            "title": "S5E93 | Anya Wick - Jeffrey Epstein's Niece, The Cult of Ba'al Survivor, & a Voice for the Voiceless",
            "duration": "6985.0 seconds"
        }
    }
    
    all_analyses = []
    
    # Analyze each transcript using existing components
    for transcript_file in transcript_files:
        if not Path(transcript_file).exists():
            print(f"❌ Transcript file not found: {transcript_file}")
            continue
            
        # Extract video ID from filename
        video_id = Path(transcript_file).stem.split('_')[0]
        
        if video_id in video_metadata:
            title = video_metadata[video_id]["title"]
        else:
            title = f"Unknown Title ({video_id})"
        
        print(f"\n🎬 Processing: {title}")
        print(f"📁 File: {transcript_file}")
        
        # Read transcript
        transcript_text = read_vtt_transcript(transcript_file)
        if not transcript_text:
            print(f"❌ Failed to read transcript: {transcript_file}")
            continue
        
        print(f"📝 Transcript length: {len(transcript_text)} characters")
        
        # Analyze transcript using existing components
        analysis_result = analyze_with_existing_components(transcript_text, title, video_id)
        if analysis_result:
            all_analyses.append(analysis_result)
            print(f"✅ Analysis completed for {video_id}")
        else:
            print(f"❌ Analysis failed for {video_id}")
    
    # Save comprehensive results
    if all_analyses:
        results_file = Path("data/outputs/analysis/imagination_podcast_proper_analysis.json")
        results_file.parent.mkdir(parents=True, exist_ok=True)
        
        comprehensive_results = {
            "analysis_date": datetime.now().isoformat(),
            "channel": "Imagination Podcast",
            "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
            "videos_analyzed": len(all_analyses),
            "analyses": all_analyses,
            "summary": {
                "total_claims": sum(len(analysis.get("claims_and_evidence", {}).get("claims", [])) for analysis in all_analyses),
                "total_evidence": sum(len(analysis.get("claims_and_evidence", {}).get("evidence", [])) for analysis in all_analyses),
                "total_biblical_refs": sum(len(analysis.get("biblical_forensic_analysis", {}).get("biblical_references", [])) for analysis in all_analyses)
            }
        }
        
        with open(results_file, 'w') as f:
            json.dump(comprehensive_results, f, indent=2)
        
        print(f"\n📄 Analysis saved to: {results_file}")
        
        # Display summary
        print(f"\n🎉 Analysis Complete!")
        print(f"✅ Analyzed {len(all_analyses)} videos")
        print(f"📊 Total claims found: {comprehensive_results['summary']['total_claims']}")
        print(f"🔍 Total evidence items: {comprehensive_results['summary']['total_evidence']}")
        print(f"📖 Total Biblical references: {comprehensive_results['summary']['total_biblical_refs']}")
        
        # Show individual results
        for analysis in all_analyses:
            print(f"\n📺 {analysis['title']}")
            print(f"   Claims: {len(analysis.get('claims_and_evidence', {}).get('claims', []))}")
            print(f"   Evidence: {len(analysis.get('claims_and_evidence', {}).get('evidence', []))}")
            print(f"   Biblical refs: {len(analysis.get('biblical_forensic_analysis', {}).get('biblical_references', []))}")
            
            # Show some sample claims
            claims = analysis.get('claims_and_evidence', {}).get('claims', [])
            if claims:
                print(f"   Sample claim: {claims[0][:100]}...")
    
    else:
        print("❌ No analyses completed successfully")

if __name__ == "__main__":
    main() 