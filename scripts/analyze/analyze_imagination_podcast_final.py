#!/usr/bin/env python3
"""
Final Analysis - Imagination Podcast Transcripts
Using correct classes and methods from existing Living Truth Engine components
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analysis.research_analysis import ResearchAnalysisSystem
from analysis.hybrid_retrieval import HybridRetriever, AdvancedSearchEngine

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

def analyze_with_correct_classes(transcript_text, video_title, video_id):
    """Analyze using the correct classes and methods"""
    print(f"\n🔍 Analyzing: {video_title}")
    print("-" * 60)
    
    try:
        # Initialize existing components with correct classes
        research_system = ResearchAnalysisSystem()
        hybrid_retriever = HybridRetriever()
        search_engine = AdvancedSearchEngine()
        
        # Step 1: Extract entities from text using existing method
        print("🏷️ Extracting entities...")
        entities = research_system.extract_entities_from_text(transcript_text)
        
        # Step 2: Create transcript data structure for claims extraction
        transcript_data = {
            "video_id": video_id,
            "title": video_title,
            "transcript": transcript_text,
            "entities": entities
        }
        
        # Step 3: Extract claims using existing method
        print("📋 Extracting claims...")
        claims = research_system.extract_claims_from_transcript(transcript_data)
        
        # Step 4: Use hybrid retriever for Biblical evidence (correct class)
        print("📖 Searching for Biblical evidence...")
        biblical_evidence = hybrid_retriever.search_biblical_evidence(transcript_text)
        
        # Step 5: Search for survivor testimonies (correct class)
        print("🎙️ Searching for survivor testimonies...")
        survivor_testimonies = hybrid_retriever.search_survivor_testimonies(transcript_text)
        
        # Step 6: Use advanced search for general analysis
        print("🔍 Performing advanced search analysis...")
        advanced_search = search_engine.search(transcript_text, search_type="hybrid")
        
        # Compile results
        analysis_result = {
            "video_id": video_id,
            "title": video_title,
            "analysis_date": datetime.now().isoformat(),
            "entities": entities,
            "claims": [asdict(claim) for claim in claims],
            "biblical_evidence": biblical_evidence,
            "survivor_testimonies": survivor_testimonies,
            "advanced_search": advanced_search,
            "transcript_length": len(transcript_text)
        }
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Error analyzing transcript: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🎙️ Final Analysis - Imagination Podcast Transcripts")
    print("🔍 Using Correct Classes and Methods from Existing Components")
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
    
    # Analyze each transcript using correct classes
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
        
        # Analyze transcript using correct classes
        analysis_result = analyze_with_correct_classes(transcript_text, title, video_id)
        if analysis_result:
            all_analyses.append(analysis_result)
            print(f"✅ Analysis completed for {video_id}")
        else:
            print(f"❌ Analysis failed for {video_id}")
    
    # Save comprehensive results
    if all_analyses:
        results_file = Path("data/outputs/analysis/imagination_podcast_final_analysis.json")
        results_file.parent.mkdir(parents=True, exist_ok=True)
        
        comprehensive_results = {
            "analysis_date": datetime.now().isoformat(),
            "channel": "Imagination Podcast",
            "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
            "videos_analyzed": len(all_analyses),
            "analyses": all_analyses,
            "summary": {
                "total_entities": sum(len(analysis.get("entities", [])) for analysis in all_analyses),
                "total_claims": sum(len(analysis.get("claims", [])) for analysis in all_analyses),
                "total_biblical_evidence": sum(len(analysis.get("biblical_evidence", [])) for analysis in all_analyses),
                "total_survivor_testimonies": sum(len(analysis.get("survivor_testimonies", [])) for analysis in all_analyses)
            }
        }
        
        with open(results_file, 'w') as f:
            json.dump(comprehensive_results, f, indent=2, default=str)
        
        print(f"\n📄 Analysis saved to: {results_file}")
        
        # Display summary
        print(f"\n🎉 Analysis Complete!")
        print(f"✅ Analyzed {len(all_analyses)} videos")
        print(f"🏷️ Total entities found: {comprehensive_results['summary']['total_entities']}")
        print(f"📊 Total claims found: {comprehensive_results['summary']['total_claims']}")
        print(f"📖 Total Biblical evidence: {comprehensive_results['summary']['total_biblical_evidence']}")
        print(f"🎙️ Total survivor testimonies: {comprehensive_results['summary']['total_survivor_testimonies']}")
        
        # Show individual results
        for analysis in all_analyses:
            print(f"\n📺 {analysis['title']}")
            print(f"   Entities: {len(analysis.get('entities', []))}")
            print(f"   Claims: {len(analysis.get('claims', []))}")
            print(f"   Biblical evidence: {len(analysis.get('biblical_evidence', []))}")
            print(f"   Survivor testimonies: {len(analysis.get('survivor_testimonies', []))}")
            
            # Show some sample entities
            entities = analysis.get('entities', [])
            if entities:
                print(f"   Sample entities: {entities[:3]}")
            
            # Show some sample claims
            claims = analysis.get('claims', [])
            if claims:
                print(f"   Sample claim: {claims[0].get('text', '')[:100]}...")
    
    else:
        print("❌ No analyses completed successfully")

if __name__ == "__main__":
    main() 