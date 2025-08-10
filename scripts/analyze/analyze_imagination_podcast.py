#!/usr/bin/env python3
"""
Analyze Imagination Podcast Transcripts
Using Living Truth Engine's advanced analysis capabilities
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analysis.hybrid_retrieval import HybridRetriever
from analysis.research_analysis import ResearchAnalysisSystem
from analysis.notebook_agent import AdvancedNotebookAgent
from visualization.advanced_viz import AdvancedVisualizer

def read_transcript(file_path):
    """Read and parse VTT transcript file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple VTT parsing - extract text content
        lines = content.split('\n')
        transcript_text = []
        
        for line in lines:
            line = line.strip()
            # Skip timestamp lines and empty lines
            if line and not line.startswith('-->') and not line.startswith('WEBVTT') and not line[0].isdigit():
                transcript_text.append(line)
        
        return ' '.join(transcript_text)
    except Exception as e:
        print(f"❌ Error reading transcript {file_path}: {e}")
        return None

def analyze_transcript(transcript_text, video_title, video_id):
    """Analyze a single transcript using Living Truth Engine"""
    print(f"\n🔍 Analyzing: {video_title}")
    print("-" * 60)
    
    try:
        # Initialize analysis systems
        retriever = HybridRetriever()
        research_system = ResearchAnalysisSystem()
        notebook_agent = AdvancedNotebookAgent()
        
        # Step 1: Extract claims and evidence
        print("📋 Extracting claims and evidence...")
        claims_result = research_system.extract_claims_and_evidence(transcript_text)
        
        # Step 2: Perform Biblical forensic analysis
        print("📖 Performing Biblical forensic analysis...")
        biblical_result = research_system.biblical_forensic_analysis(transcript_text)
        
        # Step 3: Generate study guide
        print("📚 Generating study guide...")
        study_guide = notebook_agent.generate_study_guide(transcript_text, video_title)
        
        # Step 4: Create research report
        print("📄 Creating research report...")
        research_report = notebook_agent.generate_research_report(transcript_text, video_title)
        
        # Step 5: Generate visualizations
        print("📊 Generating visualizations...")
        visualizer = AdvancedVisualizer()
        
        # Create network visualization
        network_viz = visualizer.create_network_visualization(
            transcript_text, 
            f"imagination_podcast_{video_id}_network"
        )
        
        # Create timeline visualization
        timeline_viz = visualizer.create_timeline_visualization(
            transcript_text,
            f"imagination_podcast_{video_id}_timeline"
        )
        
        # Compile results
        analysis_result = {
            "video_id": video_id,
            "title": video_title,
            "analysis_date": datetime.now().isoformat(),
            "claims_and_evidence": claims_result,
            "biblical_forensic_analysis": biblical_result,
            "study_guide": study_guide,
            "research_report": research_report,
            "visualizations": {
                "network": network_viz,
                "timeline": timeline_viz
            }
        }
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Error analyzing transcript: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🎙️ Imagination Podcast Transcript Analysis")
    print("🔍 Using Living Truth Engine Advanced Analysis")
    print("=" * 70)
    
    # Find transcript files
    transcript_files = list(Path("data/sources").glob("*_transcript.vtt"))
    
    if not transcript_files:
        print("❌ No transcript files found in data/sources/")
        return
    
    print(f"📝 Found {len(transcript_files)} transcript files")
    
    # Video metadata (from the download summary)
    video_metadata = {
        "D691xfozd3A": {
            "title": "S5E93 | Anya Wick - Jeffrey Epstein's Niece, The Cult of Ba'al Survivor, & a Voice for the Voiceless",
            "duration": "6985.0 seconds"
        },
        "Bdrwd8p4fKc": {
            "title": "S5E92 | JR Sweet - MK ULTRA Mass Shootings & Assassinations, Amnesic Slavery, & Bloodline Networks",
            "duration": "8230.0 seconds"
        }
    }
    
    all_analyses = []
    
    # Analyze each transcript
    for transcript_file in transcript_files:
        video_id = transcript_file.stem.replace('_transcript', '')
        
        if video_id in video_metadata:
            title = video_metadata[video_id]["title"]
        else:
            title = f"Unknown Title ({video_id})"
        
        print(f"\n🎬 Processing: {title}")
        print(f"📁 File: {transcript_file}")
        
        # Read transcript
        transcript_text = read_transcript(transcript_file)
        if not transcript_text:
            print(f"❌ Failed to read transcript: {transcript_file}")
            continue
        
        print(f"📝 Transcript length: {len(transcript_text)} characters")
        
        # Analyze transcript
        analysis_result = analyze_transcript(transcript_text, title, video_id)
        if analysis_result:
            all_analyses.append(analysis_result)
            print(f"✅ Analysis completed for {video_id}")
        else:
            print(f"❌ Analysis failed for {video_id}")
    
    # Save comprehensive results
    if all_analyses:
        results_file = Path("data/outputs/analysis/imagination_podcast_analysis.json")
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
                "biblical_references": sum(len(analysis.get("biblical_forensic_analysis", {}).get("biblical_references", [])) for analysis in all_analyses)
            }
        }
        
        with open(results_file, 'w') as f:
            json.dump(comprehensive_results, f, indent=2)
        
        print(f"\n📄 Comprehensive analysis saved to: {results_file}")
        
        # Display summary
        print(f"\n🎉 Analysis Complete!")
        print(f"✅ Analyzed {len(all_analyses)} videos")
        print(f"📊 Total claims found: {comprehensive_results['summary']['total_claims']}")
        print(f"🔍 Total evidence items: {comprehensive_results['summary']['total_evidence']}")
        print(f"📖 Total Biblical references: {comprehensive_results['summary']['biblical_references']}")
        
        # Show individual results
        for analysis in all_analyses:
            print(f"\n📺 {analysis['title']}")
            print(f"   Claims: {len(analysis.get('claims_and_evidence', {}).get('claims', []))}")
            print(f"   Evidence: {len(analysis.get('claims_and_evidence', {}).get('evidence', []))}")
            print(f"   Biblical refs: {len(analysis.get('biblical_forensic_analysis', {}).get('biblical_references', []))}")
    
    else:
        print("❌ No analyses completed successfully")

if __name__ == "__main__":
    main() 