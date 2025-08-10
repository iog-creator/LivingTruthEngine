#!/usr/bin/env python3
"""
Simple Analysis - Imagination Podcast Transcripts
Using local models and core analysis capabilities
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime
import re

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

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

def extract_claims_and_evidence(text):
    """Extract claims and evidence using pattern matching"""
    claims = []
    evidence = []
    
    # Look for claim patterns
    claim_patterns = [
        r'I (?:believe|think|know|claim|assert) (?:that )?([^.]*)',
        r'(?:The|This) (?:evidence|proof|fact) (?:shows|indicates|demonstrates) (?:that )?([^.]*)',
        r'(?:According to|Based on) (?:the evidence|research|testimony) ([^.]*)',
        r'(?:It is|This is) (?:clear|obvious|evident) (?:that )?([^.]*)',
        r'(?:I have|I\'ve) (?:seen|witnessed|experienced) ([^.]*)',
        r'(?:There is|There\'s) (?:evidence|proof) (?:that )?([^.]*)'
    ]
    
    for pattern in claim_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match.strip()) > 10:  # Only meaningful claims
                claims.append(match.strip())
    
    # Look for evidence patterns
    evidence_patterns = [
        r'(?:document|record|file|report|testimony|statement) (?:shows|indicates|states) ([^.]*)',
        r'(?:witness|person|individual) (?:said|stated|testified) ([^.]*)',
        r'(?:document|record|file|report) (?:from|dated|showing) ([^.]*)',
        r'(?:evidence|proof|documentation) (?:of|for|regarding) ([^.]*)',
        r'(?:I saw|I witnessed|I observed) ([^.]*)',
        r'(?:The|This) (?:document|record|file|report) ([^.]*)'
    ]
    
    for pattern in evidence_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match.strip()) > 10:  # Only meaningful evidence
                evidence.append(match.strip())
    
    return {
        "claims": list(set(claims)),  # Remove duplicates
        "evidence": list(set(evidence))  # Remove duplicates
    }

def extract_biblical_references(text):
    """Extract potential Biblical references and themes"""
    biblical_references = []
    
    # Biblical themes and concepts
    biblical_themes = [
        "good and evil", "light and darkness", "truth and lies", "justice", "redemption",
        "forgiveness", "love", "faith", "hope", "courage", "perseverance", "wisdom",
        "righteousness", "sin", "grace", "mercy", "compassion", "integrity", "honesty",
        "freedom", "slavery", "oppression", "liberation", "healing", "restoration"
    ]
    
    # Look for Biblical themes in the text
    for theme in biblical_themes:
        if theme.lower() in text.lower():
            biblical_references.append({
                "theme": theme,
                "context": "Found in transcript",
                "relevance": "Potential Biblical parallel"
            })
    
    # Look for specific Biblical references
    biblical_terms = [
        "God", "Lord", "Jesus", "Christ", "Holy Spirit", "Bible", "Scripture",
        "prophet", "apostle", "disciple", "faith", "prayer", "worship",
        "temple", "church", "ministry", "gospel", "salvation", "eternal life"
    ]
    
    for term in biblical_terms:
        if term.lower() in text.lower():
            biblical_references.append({
                "term": term,
                "context": "Direct Biblical reference",
                "relevance": "Explicit Biblical content"
            })
    
    return biblical_references

def extract_entities(text):
    """Extract named entities (people, places, organizations)"""
    entities = {
        "people": [],
        "organizations": [],
        "locations": [],
        "dates": [],
        "events": []
    }
    
    # Simple entity extraction patterns
    # People (capitalized names)
    people_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
    people_matches = re.findall(people_pattern, text)
    entities["people"] = list(set(people_matches))
    
    # Organizations (common patterns)
    org_patterns = [
        r'\b[A-Z][A-Z]+\b',  # Acronyms
        r'\b[A-Z][a-z]+ (?:Corporation|Company|Inc|LLC|Ltd|Foundation|Institute|Agency|Department)\b'
    ]
    
    for pattern in org_patterns:
        matches = re.findall(pattern, text)
        entities["organizations"].extend(matches)
    
    # Dates
    date_patterns = [
        r'\b\d{4}\b',  # Years
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b'
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        entities["dates"].extend(matches)
    
    # Remove duplicates
    for key in entities:
        entities[key] = list(set(entities[key]))
    
    return entities

def generate_summary(text, title):
    """Generate a simple summary of the transcript"""
    # Extract key sentences (sentences with important keywords)
    sentences = re.split(r'[.!?]+', text)
    
    important_keywords = [
        "evidence", "testimony", "witness", "document", "record", "claim", "allegation",
        "investigation", "research", "study", "analysis", "report", "finding",
        "survivor", "victim", "abuse", "trauma", "healing", "recovery", "justice",
        "truth", "lie", "cover-up", "conspiracy", "government", "agency", "organization"
    ]
    
    key_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20:  # Only meaningful sentences
            for keyword in important_keywords:
                if keyword.lower() in sentence.lower():
                    key_sentences.append(sentence)
                    break
    
    # Take the first few key sentences as summary
    summary = '. '.join(key_sentences[:5]) + '.'
    
    return {
        "title": title,
        "summary": summary,
        "key_points": key_sentences[:10],
        "word_count": len(text.split()),
        "sentence_count": len(sentences)
    }

def analyze_transcript_simple(transcript_text, video_title, video_id):
    """Simple analysis using pattern matching and local processing"""
    print(f"\n🔍 Analyzing: {video_title}")
    print("-" * 60)
    
    try:
        # Step 1: Extract claims and evidence
        print("📋 Extracting claims and evidence...")
        claims_evidence = extract_claims_and_evidence(transcript_text)
        
        # Step 2: Extract Biblical references
        print("📖 Extracting Biblical references...")
        biblical_refs = extract_biblical_references(transcript_text)
        
        # Step 3: Extract entities
        print("🏷️ Extracting entities...")
        entities = extract_entities(transcript_text)
        
        # Step 4: Generate summary
        print("📄 Generating summary...")
        summary = generate_summary(transcript_text, video_title)
        
        # Compile results
        analysis_result = {
            "video_id": video_id,
            "title": video_title,
            "analysis_date": datetime.now().isoformat(),
            "claims_and_evidence": claims_evidence,
            "biblical_references": biblical_refs,
            "entities": entities,
            "summary": summary,
            "transcript_length": len(transcript_text)
        }
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Error analyzing transcript: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🎙️ Simple Analysis - Imagination Podcast Transcripts")
    print("🔍 Using Local Pattern Matching and Analysis")
    print("=" * 70)
    
    # Find transcript files
    transcript_files = list(Path("data/sources").glob("*_transcript.vtt"))
    
    if not transcript_files:
        print("❌ No transcript files found in data/sources/")
        return
    
    print(f"📝 Found {len(transcript_files)} transcript files")
    
    # Video metadata
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
        analysis_result = analyze_transcript_simple(transcript_text, title, video_id)
        if analysis_result:
            all_analyses.append(analysis_result)
            print(f"✅ Analysis completed for {video_id}")
        else:
            print(f"❌ Analysis failed for {video_id}")
    
    # Save comprehensive results
    if all_analyses:
        results_file = Path("data/outputs/analysis/imagination_podcast_simple_analysis.json")
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
                "total_biblical_refs": sum(len(analysis.get("biblical_references", [])) for analysis in all_analyses),
                "total_entities": sum(len(analysis.get("entities", {}).get("people", [])) for analysis in all_analyses)
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
        print(f"🏷️ Total entities found: {comprehensive_results['summary']['total_entities']}")
        
        # Show individual results
        for analysis in all_analyses:
            print(f"\n📺 {analysis['title']}")
            print(f"   Claims: {len(analysis.get('claims_and_evidence', {}).get('claims', []))}")
            print(f"   Evidence: {len(analysis.get('claims_and_evidence', {}).get('evidence', []))}")
            print(f"   Biblical refs: {len(analysis.get('biblical_references', []))}")
            print(f"   People: {len(analysis.get('entities', {}).get('people', []))}")
            print(f"   Summary: {analysis.get('summary', {}).get('summary', 'No summary')[:100]}...")
    
    else:
        print("❌ No analyses completed successfully")

if __name__ == "__main__":
    main() 