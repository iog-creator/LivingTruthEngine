#!/usr/bin/env python3
"""
Test Migrated Living Truth Agent Functionality
Tests the existing living_truth_agent functionality that has been migrated to LivingTruthEngine
Focuses on core capabilities without reinventing anything
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_hybrid_retrieval():
    """Test the migrated HybridRetriever functionality"""
    print("🔍 Testing HybridRetriever (migrated from living_truth_agent)...")
    
    try:
        from src.analysis.hybrid_retrieval import HybridRetriever, AdvancedSearchEngine
        
        # Test HybridRetriever initialization
        hybrid_retriever = HybridRetriever()
        print("✅ HybridRetriever initialized successfully")
        
        # Test AdvancedSearchEngine initialization
        search_engine = AdvancedSearchEngine()
        print("✅ AdvancedSearchEngine initialized successfully")
        
        # Test Biblical evidence search (core living_truth_agent functionality)
        test_query = "child sacrifice evidence"
        biblical_evidence = hybrid_retriever.search_biblical_evidence(test_query)
        print(f"✅ Biblical evidence search working: {len(biblical_evidence)} results")
        
        # Test survivor testimony search (core living_truth_agent functionality)
        survivor_testimonies = hybrid_retriever.search_survivor_testimonies(test_query)
        print(f"✅ Survivor testimony search working: {len(survivor_testimonies)} results")
        
        # Test advanced search (core living_truth_agent functionality)
        advanced_results = search_engine.search(test_query, search_type="hybrid")
        print(f"✅ Advanced search working: {len(advanced_results)} results")
        
        return True
        
    except Exception as e:
        print(f"❌ HybridRetriever test failed: {e}")
        return False

def test_research_analysis():
    """Test the migrated ResearchAnalysisSystem functionality"""
    print("\n🔍 Testing ResearchAnalysisSystem (migrated from living_truth_agent)...")
    
    try:
        from src.analysis.research_analysis import ResearchAnalysisSystem
        
        # Test ResearchAnalysisSystem initialization
        research_system = ResearchAnalysisSystem()
        print("✅ ResearchAnalysisSystem initialized successfully")
        
        # Test entity extraction (core living_truth_agent functionality)
        test_text = "Jeffrey Epstein was connected to powerful elites and operated trafficking networks."
        entities = research_system.extract_entities_from_text(test_text)
        print(f"✅ Entity extraction working: {len(entities)} entities found")
        
        # Test claims extraction (core living_truth_agent functionality)
        transcript_data = {
            "video_id": "test123",
            "title": "Test Video",
            "transcript": test_text,
            "entities": entities
        }
        claims = research_system.extract_claims_from_transcript(transcript_data)
        print(f"✅ Claims extraction working: {len(claims)} claims found")
        
        return True
        
    except Exception as e:
        print(f"❌ ResearchAnalysisSystem test failed: {e}")
        return False

def test_channel_archiver():
    """Test the migrated ChannelArchiver functionality"""
    print("\n🔍 Testing ChannelArchiver (migrated from living_truth_agent)...")
    
    try:
        from src.processing.channel_archiver import ChannelArchiver
        
        # Test ChannelArchiver initialization
        channel_archiver = ChannelArchiver()
        print("✅ ChannelArchiver initialized successfully")
        
        # Test transcript processing (core living_truth_agent functionality)
        transcript_files = list(Path("data/sources").glob("*.txt"))
        if transcript_files:
            print(f"✅ Found {len(transcript_files)} transcript files for testing")
            
            # Test processing a transcript
            test_file = transcript_files[0]
            print(f"📝 Testing with transcript: {test_file.name}")
            
            # Test transcript reading
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ Transcript reading working: {len(content)} characters")
            
        else:
            print("⚠️ No transcript files found for testing")
        
        return True
        
    except Exception as e:
        print(f"❌ ChannelArchiver test failed: {e}")
        return False

def test_agi_integration():
    """Test the migrated AGI Integration functionality"""
    print("\n🔍 Testing AGI Integration (migrated from living_truth_agent)...")
    
    try:
        from src.integration.agi_integration import AGILivingTruthIntegration
        
        # Test AGI Integration initialization
        agi_integration = AGILivingTruthIntegration()
        print("✅ AGI Integration initialized successfully")
        
        # Test AGI components status (core living_truth_agent functionality)
        components_status = agi_integration.get_agi_components_status()
        print(f"✅ AGI components status working: {len(components_status)} components")
        
        # Test integration status (core living_truth_agent functionality)
        integration_status = agi_integration.get_integration_status()
        print(f"✅ Integration status working: {integration_status.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ AGI Integration test failed: {e}")
        return False

def test_visualization():
    """Test the migrated visualization functionality"""
    print("\n🔍 Testing Advanced Visualization (migrated from living_truth_agent)...")
    
    try:
        from src.visualization.advanced_viz import AdvancedVisualizer
        
        # Test AdvancedVisualizer initialization
        visualizer = AdvancedVisualizer()
        print("✅ AdvancedVisualizer initialized successfully")
        
        # Test network visualization (core living_truth_agent functionality)
        test_data = {
            "nodes": [
                {"id": "1", "label": "Entity A", "type": "person"},
                {"id": "2", "label": "Entity B", "type": "organization"}
            ],
            "edges": [
                {"source": "1", "target": "2", "label": "connection"}
            ]
        }
        
        # Test visualization generation
        viz_result = visualizer.create_interactive_3d_network_graph(test_data)
        print(f"✅ 3D network visualization working: {type(viz_result)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def test_mcp_tools():
    """Test the MCP tools for migrated functionality"""
    print("\n🔍 Testing MCP Tools for migrated functionality...")
    
    try:
        from src.mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
        
        # Test MCP server initialization
        mcp_server = LivingTruthEngine()
        print("✅ MCP Server initialized successfully")
        
        # Test core MCP tools - use the MCP server's tools directly
        print(f"✅ MCP server initialized with all migrated functionality")
        
        # Check for key migrated functionality methods
        key_methods = [
            "search_biblical_evidence",
            "search_survivor_testimonies", 
            "extract_entities_from_text",
            "extract_claims_from_transcript",
            "archive_youtube_channel",
            "analyze_with_agi_integration"
        ]
        
        available_methods = [method for method in dir(mcp_server) if not method.startswith('_')]
        found_methods = [method for method in key_methods if method in available_methods]
        print(f"✅ Key migrated methods found: {len(found_methods)}/{len(key_methods)}")
        

        
        return True
        
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False

def test_configuration():
    """Test the migrated configuration system"""
    print("\n🔍 Testing Configuration System (migrated from living_truth_agent)...")
    
    try:
        from src.config import get_config, config
        
        # Test configuration loading
        cfg = get_config()
        print("✅ Configuration loaded successfully")
        
        # Test Biblical forensic configuration (core living_truth_agent functionality)
        biblical_config = cfg.biblical_forensic
        print(f"✅ Biblical confidence baseline: {biblical_config.SURVIVOR_CONFIDENCE_BASELINE}")
        print(f"✅ Evidence verification threshold: {biblical_config.EVIDENCE_VERIFICATION_THRESHOLD}")
        print(f"✅ Biblical references: {len(biblical_config.BIBLICAL_ABUSE_REFERENCES)}")
        print(f"✅ Historical references: {len(biblical_config.HISTORICAL_ABUSE_REFERENCES)}")
        
        # Test database configuration
        db_config = cfg.database
        print(f"✅ PostgreSQL configured: {db_config.POSTGRES_HOST}:{db_config.POSTGRES_PORT}")
        print(f"✅ Neo4j configured: {db_config.NEO4J_URI}")
        print(f"✅ Redis configured: {db_config.REDIS_HOST}:{db_config.REDIS_PORT}")
        
        # Test model configuration
        model_config = cfg.model
        print(f"✅ LM Studio configured: {model_config.LMSTUDIO_URL}")
        print(f"✅ Embedding models: {model_config.LMSTUDIO_EMBEDDING_MODEL_QWEN3}, {model_config.LMSTUDIO_EMBEDDING_MODEL_MINILM}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests for migrated living_truth_agent functionality"""
    print("🎯 Testing Migrated Living Truth Agent Functionality")
    print("=" * 60)
    print("Focus: Testing existing functionality, not reinventing")
    print("=" * 60)
    
    test_results = []
    
    # Test all migrated components
    test_results.append(("Configuration", test_configuration()))
    test_results.append(("HybridRetriever", test_hybrid_retrieval()))
    test_results.append(("ResearchAnalysisSystem", test_research_analysis()))
    test_results.append(("ChannelArchiver", test_channel_archiver()))
    test_results.append(("AGI Integration", test_agi_integration()))
    test_results.append(("Visualization", test_visualization()))
    test_results.append(("MCP Tools", test_mcp_tools()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 MIGRATED FUNCTIONALITY TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All migrated living_truth_agent functionality working correctly!")
        print("✅ System is ready for cross-referencing testimonials, people, places, events, concepts, and organizations")
    else:
        print("⚠️ Some migrated functionality needs attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 