#!/usr/bin/env python3
"""
Phase 5 Integration Tests for Living Truth Engine
Tests all migrated components from living_truth_agent
"""

import sys
import os
import json
import time
import logging
import requests
from pathlib import Path
from typing import Dict, Any, List

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Phase5IntegrationTester:
    def __init__(self):
        self.base_urls = {
            'langflow': 'http://localhost:7860',
            'dashboard': 'http://localhost:8050',
            'lm_studio': 'http://localhost:1234',
            'living_truth_engine': 'http://localhost:9123',
            'neo4j': 'http://localhost:7474',
            'postgres': 'localhost:5434'
        }
        self.test_results = {}
        
    def test_phase1_core_systems(self):
        """Test Phase 1: Core System Integration"""
        logger.info("🧪 Testing Phase 1: Core System Integration")
        
        results = {}
        
        # Test 1.1: Configuration System
        try:
            from config.living_truth_config import LivingTruthConfig
            config = LivingTruthConfig()
            logger.info("✅ Configuration system imported successfully")
            results['config_system'] = True
        except Exception as e:
            logger.error(f"❌ Configuration system failed: {e}")
            results['config_system'] = False
        
        # Test 1.2: Hybrid Retrieval System
        try:
            from analysis.hybrid_retrieval import HybridRetriever, AdvancedSearchEngine
            logger.info("✅ Hybrid retrieval system imported successfully")
            results['hybrid_retrieval'] = True
        except Exception as e:
            logger.error(f"❌ Hybrid retrieval system failed: {e}")
            results['hybrid_retrieval'] = False
        
        # Test 1.3: Research Analysis System
        try:
            from analysis.research_analysis import ResearchAnalysisSystem, Claim, Entity, Relationship
            logger.info("✅ Research analysis system imported successfully")
            results['research_analysis'] = True
        except Exception as e:
            logger.error(f"❌ Research analysis system failed: {e}")
            results['research_analysis'] = False
        
        self.test_results['phase1'] = results
        return all(results.values())
    
    def test_phase2_advanced_features(self):
        """Test Phase 2: Advanced Features Integration"""
        logger.info("🧪 Testing Phase 2: Advanced Features Integration")
        
        results = {}
        
        # Test 2.1: Notebook Agent System
        try:
            from analysis.notebook_agent import AdvancedNotebookAgent, StudyGuide, DocumentSummary, ResearchReport
            logger.info("✅ Notebook agent system imported successfully")
            results['notebook_agent'] = True
        except Exception as e:
            logger.error(f"❌ Notebook agent system failed: {e}")
            results['notebook_agent'] = False
        
        # Test 2.2: AGI Integration Layer
        try:
            from integration.agi_integration import AGILivingTruthIntegration
            logger.info("✅ AGI integration system imported successfully")
            results['agi_integration'] = True
        except Exception as e:
            logger.error(f"❌ AGI integration system failed: {e}")
            results['agi_integration'] = False
        
        # Test 2.3: Channel Archiver System
        try:
            from processing.channel_archiver import ChannelArchiver
            logger.info("✅ Channel archiver system imported successfully")
            results['channel_archiver'] = True
        except Exception as e:
            logger.error(f"❌ Channel archiver system failed: {e}")
            results['channel_archiver'] = False
        
        self.test_results['phase2'] = results
        return all(results.values())
    
    def test_phase3_mcp_integration(self):
        """Test Phase 3: Enhanced MCP Integration"""
        logger.info("🧪 Testing Phase 3: Enhanced MCP Integration")
        
        results = {}
        
        # Test 3.1: MCP Hub Server
        try:
            from mcp_servers.mcp_hub_server import MCPHubServer
            logger.info("✅ MCP Hub Server imported successfully")
            results['mcp_hub_server'] = True
        except Exception as e:
            logger.error(f"❌ MCP Hub Server failed: {e}")
            results['mcp_hub_server'] = False
        
        # Test 3.2: Tool Registry
        try:
            registry_path = Path("config/tool_registry.json")
            if registry_path.exists():
                with open(registry_path, 'r') as f:
                    registry = json.load(f)
                tool_count = len(registry.get('tools', []))
                logger.info(f"✅ Tool registry loaded successfully with {tool_count} tools")
                results['tool_registry'] = True
            else:
                logger.error("❌ Tool registry file not found")
                results['tool_registry'] = False
        except Exception as e:
            logger.error(f"❌ Tool registry failed: {e}")
            results['tool_registry'] = False
        
        # Test 3.3: MCP Server Tools
        try:
            from mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
            engine = LivingTruthEngine()
            status = engine.get_status()
            if status:
                logger.info("✅ MCP server tools working")
                results['mcp_tools'] = True
            else:
                logger.error("❌ MCP server tools not responding")
                results['mcp_tools'] = False
        except Exception as e:
            logger.error(f"❌ MCP server tools failed: {e}")
            results['mcp_tools'] = False
        
        self.test_results['phase3'] = results
        return all(results.values())
    
    def test_phase4_visualization(self):
        """Test Phase 4: Visualization and Dashboard Enhancement"""
        logger.info("🧪 Testing Phase 4: Visualization and Dashboard Enhancement")
        
        results = {}
        
        # Test 4.1: Advanced Visualization System
        try:
            from visualization.advanced_viz import AdvancedVisualizer
            logger.info("✅ Advanced visualization system imported successfully")
            results['advanced_viz'] = True
        except Exception as e:
            logger.error(f"❌ Advanced visualization system failed: {e}")
            results['advanced_viz'] = False
        
        # Test 4.2: Dash Dashboard
        try:
            response = requests.get(f"{self.base_urls['dashboard']}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get("status") == "healthy":
                    logger.info("✅ Dash dashboard is healthy")
                    results['dash_dashboard'] = True
                else:
                    logger.error(f"❌ Dash dashboard health check failed: {health_data}")
                    results['dash_dashboard'] = False
            else:
                logger.error(f"❌ Dash dashboard not responding: {response.status_code}")
                results['dash_dashboard'] = False
        except Exception as e:
            logger.error(f"❌ Dash dashboard test failed: {e}")
            results['dash_dashboard'] = False
        
        self.test_results['phase4'] = results
        return all(results.values())
    
    def test_data_migration(self):
        """Test Phase 5.1: Data Migration"""
        logger.info("🧪 Testing Phase 5.1: Data Migration")
        
        results = {}
        
        # Test data directory structure
        data_dirs = [
            "data/sources",
            "data/outputs",
            "data/outputs/visualizations",
            "data/outputs/audio",
            "data/outputs/logs",
            "data/processed",
            "data/models"
        ]
        
        for dir_path in data_dirs:
            path = Path(dir_path)
            if path.exists():
                logger.info(f"✅ Data directory exists: {dir_path}")
                results[f'dir_{dir_path.replace("/", "_")}'] = True
            else:
                logger.warning(f"⚠️ Data directory missing: {dir_path}")
                results[f'dir_{dir_path.replace("/", "_")}'] = False
        
        # Test source data files
        sources_dir = Path("data/sources")
        if sources_dir.exists():
            transcript_files = list(sources_dir.glob("*transcript*.txt"))
            if transcript_files:
                logger.info(f"✅ Found {len(transcript_files)} transcript files")
                results['source_transcripts'] = True
            else:
                logger.warning("⚠️ No transcript files found")
                results['source_transcripts'] = False
        else:
            logger.error("❌ Sources directory not found")
            results['source_transcripts'] = False
        
        # Test visualization files
        viz_dir = Path("data/outputs/visualizations")
        if viz_dir.exists():
            viz_files = list(viz_dir.glob("*.json"))
            if viz_files:
                logger.info(f"✅ Found {len(viz_files)} visualization files")
                results['visualization_files'] = True
            else:
                logger.warning("⚠️ No visualization files found")
                results['visualization_files'] = False
        else:
            logger.error("❌ Visualization directory not found")
            results['visualization_files'] = False
        
        self.test_results['data_migration'] = results
        return all(results.values())
    
    def test_comprehensive_functionality(self):
        """Test Phase 5.2: Comprehensive Functionality"""
        logger.info("🧪 Testing Phase 5.2: Comprehensive Functionality")
        
        results = {}
        
        # Test service health
        services = {
            'langflow': f"{self.base_urls['langflow']}/health",
            'dashboard': f"{self.base_urls['dashboard']}/health",
            'lm_studio': f"{self.base_urls['lm_studio']}/v1/models",
            'neo4j': f"{self.base_urls['neo4j']}/",
        }
        
        for service_name, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ {service_name} service is healthy")
                    results[f'{service_name}_health'] = True
                else:
                    logger.error(f"❌ {service_name} service failed: {response.status_code}")
                    results[f'{service_name}_health'] = False
            except Exception as e:
                logger.error(f"❌ {service_name} service test failed: {e}")
                results[f'{service_name}_health'] = False
        
        # Test Docker services
        try:
            import subprocess
            result = subprocess.run(['docker', 'compose', '-f', 'docker/docker-compose.yml', 'ps'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logger.info("✅ Docker services are running")
                results['docker_services'] = True
            else:
                logger.error(f"❌ Docker services failed: {result.stderr}")
                results['docker_services'] = False
        except Exception as e:
            logger.error(f"❌ Docker services test failed: {e}")
            results['docker_services'] = False
        
        # Test MCP server functionality
        try:
            from mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
            engine = LivingTruthEngine()
            
            # Test basic functionality
            status = engine.get_status()
            if status:
                logger.info("✅ MCP server basic functionality working")
                results['mcp_basic'] = True
            else:
                logger.error("❌ MCP server basic functionality failed")
                results['mcp_basic'] = False
            
            # Test LM Studio connection
            lm_test = engine.test_lm_studio_connection()
            if lm_test:
                logger.info("✅ LM Studio connection working")
                results['lm_studio_connection'] = True
            else:
                logger.error("❌ LM Studio connection failed")
                results['lm_studio_connection'] = False
                
        except Exception as e:
            logger.error(f"❌ MCP server functionality test failed: {e}")
            results['mcp_basic'] = False
            results['lm_studio_connection'] = False
        
        self.test_results['comprehensive_functionality'] = results
        return all(results.values())
    
    def test_performance_benchmarks(self):
        """Test Phase 5.3: Performance Benchmarks"""
        logger.info("🧪 Testing Phase 5.3: Performance Benchmarks")
        
        results = {}
        
        # Test response times
        services = {
            'langflow': f"{self.base_urls['langflow']}/health",
            'dashboard': f"{self.base_urls['dashboard']}/health",
            'lm_studio': f"{self.base_urls['lm_studio']}/v1/models",
        }
        
        for service_name, url in services.items():
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                end_time = time.time()
                response_time = end_time - start_time
                
                if response.status_code == 200:
                    if response_time < 2.0:
                        logger.info(f"✅ {service_name} response time: {response_time:.2f}s (good)")
                        results[f'{service_name}_performance'] = True
                    elif response_time < 5.0:
                        logger.warning(f"⚠️ {service_name} response time: {response_time:.2f}s (slow)")
                        results[f'{service_name}_performance'] = True
                    else:
                        logger.error(f"❌ {service_name} response time: {response_time:.2f}s (too slow)")
                        results[f'{service_name}_performance'] = False
                else:
                    logger.error(f"❌ {service_name} failed: {response.status_code}")
                    results[f'{service_name}_performance'] = False
            except Exception as e:
                logger.error(f"❌ {service_name} performance test failed: {e}")
                results[f'{service_name}_performance'] = False
        
        # Test MCP server performance
        try:
            from mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
            engine = LivingTruthEngine()
            
            start_time = time.time()
            status = engine.get_status()
            end_time = time.time()
            response_time = end_time - start_time
            
            if status and response_time < 2.0:
                logger.info(f"✅ MCP server response time: {response_time:.2f}s (good)")
                results['mcp_performance'] = True
            elif status and response_time < 5.0:
                logger.warning(f"⚠️ MCP server response time: {response_time:.2f}s (slow)")
                results['mcp_performance'] = True
            else:
                logger.error(f"❌ MCP server response time: {response_time:.2f}s (too slow)")
                results['mcp_performance'] = False
                
        except Exception as e:
            logger.error(f"❌ MCP server performance test failed: {e}")
            results['mcp_performance'] = False
        
        self.test_results['performance_benchmarks'] = results
        return all(results.values())
    
    def test_biblical_forensic_analysis(self):
        """Test Phase 5.4: Biblical Forensic Analysis Accuracy"""
        logger.info("🧪 Testing Phase 5.4: Biblical Forensic Analysis Accuracy")
        
        results = {}
        
        # Test configuration system
        try:
            from config.living_truth_config import LivingTruthConfig
            config = LivingTruthConfig()
            
            # Check Biblical forensic settings
            if hasattr(config, 'biblical_forensic') and hasattr(config.biblical_forensic, 'SURVIVOR_CONFIDENCE_BASELINE'):
                logger.info(f"✅ Biblical confidence baseline: {config.biblical_forensic.SURVIVOR_CONFIDENCE_BASELINE}")
                results['biblical_config'] = True
            else:
                logger.error("❌ Biblical confidence baseline not found")
                results['biblical_config'] = False
                
        except Exception as e:
            logger.error(f"❌ Biblical configuration test failed: {e}")
            results['biblical_config'] = False
        
        # Test hybrid retrieval system
        try:
            from analysis.hybrid_retrieval import HybridRetriever
            retriever = HybridRetriever()
            logger.info("✅ Hybrid retriever initialized successfully")
            results['hybrid_retriever'] = True
        except Exception as e:
            logger.error(f"❌ Hybrid retriever test failed: {e}")
            results['hybrid_retriever'] = False
        
        # Test research analysis system
        try:
            from analysis.research_analysis import ResearchAnalysisSystem
            analyzer = ResearchAnalysisSystem()
            logger.info("✅ Research analysis system initialized successfully")
            results['research_analyzer'] = True
        except Exception as e:
            logger.error(f"❌ Research analysis system test failed: {e}")
            results['research_analyzer'] = False
        
        # Test AGI integration
        try:
            from integration.agi_integration import AGILivingTruthIntegration
            agi_integration = AGILivingTruthIntegration()
            logger.info("✅ AGI integration initialized successfully")
            results['agi_integration'] = True
        except Exception as e:
            logger.error(f"❌ AGI integration test failed: {e}")
            results['agi_integration'] = False
        
        self.test_results['biblical_forensic_analysis'] = results
        return all(results.values())
    
    def run_all_phase5_tests(self):
        """Run all Phase 5 integration tests"""
        logger.info("🚀 Starting Phase 5 Integration Tests for Living Truth Engine")
        logger.info("=" * 80)
        
        test_phases = [
            ("Phase 1: Core Systems", self.test_phase1_core_systems),
            ("Phase 2: Advanced Features", self.test_phase2_advanced_features),
            ("Phase 3: MCP Integration", self.test_phase3_mcp_integration),
            ("Phase 4: Visualization", self.test_phase4_visualization),
            ("Phase 5.1: Data Migration", self.test_data_migration),
            ("Phase 5.2: Comprehensive Functionality", self.test_comprehensive_functionality),
            ("Phase 5.3: Performance Benchmarks", self.test_performance_benchmarks),
            ("Phase 5.4: Biblical Forensic Analysis", self.test_biblical_forensic_analysis),
        ]
        
        overall_results = {}
        passed = 0
        total = len(test_phases)
        
        for phase_name, test_func in test_phases:
            logger.info(f"\n🔍 Running {phase_name}...")
            try:
                result = test_func()
                overall_results[phase_name] = result
                if result:
                    passed += 1
                    logger.info(f"✅ {phase_name} PASSED")
                else:
                    logger.error(f"❌ {phase_name} FAILED")
            except Exception as e:
                logger.error(f"❌ {phase_name} ERROR: {e}")
                overall_results[phase_name] = False
        
        # Generate detailed report
        self.generate_integration_report(overall_results)
        
        # Summary
        logger.info("\n" + "=" * 80)
        logger.info("📊 PHASE 5 INTEGRATION TEST SUMMARY")
        logger.info("=" * 80)
        
        for phase_name, result in overall_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{status} {phase_name}")
        
        logger.info(f"\n🎯 Overall: {passed}/{total} phases passed")
        
        if passed == total:
            logger.info("🎉 ALL PHASES PASSED! Integration is complete and successful.")
        elif passed >= total * 0.8:
            logger.info("⚠️ Most phases passed. Integration is mostly successful.")
        else:
            logger.error("❌ Many phases failed. Integration needs attention.")
        
        return passed == total
    
    def generate_integration_report(self, overall_results: Dict[str, bool]):
        """Generate detailed integration report"""
        logger.info("\n📋 Generating Integration Report...")
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "overall_results": overall_results,
            "detailed_results": self.test_results,
            "summary": {
                "total_phases": len(overall_results),
                "passed_phases": sum(overall_results.values()),
                "success_rate": sum(overall_results.values()) / len(overall_results) * 100
            }
        }
        
        # Save report
        report_path = Path("data/outputs/logs/phase5_integration_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Integration report saved to: {report_path}")
        
        # Also save as markdown for readability
        markdown_path = Path("data/outputs/logs/phase5_integration_report.md")
        with open(markdown_path, 'w') as f:
            f.write("# Phase 5 Integration Test Report\n\n")
            f.write(f"**Generated:** {report['timestamp']}\n\n")
            f.write(f"**Overall Success Rate:** {report['summary']['success_rate']:.1f}%\n\n")
            f.write(f"**Phases Passed:** {report['summary']['passed_phases']}/{report['summary']['total_phases']}\n\n")
            
            f.write("## Phase Results\n\n")
            for phase_name, result in overall_results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                f.write(f"- {status} {phase_name}\n")
            
            f.write("\n## Detailed Results\n\n")
            for phase_name, results in self.test_results.items():
                f.write(f"### {phase_name}\n\n")
                for test_name, test_result in results.items():
                    status = "✅ PASS" if test_result else "❌ FAIL"
                    f.write(f"- {status} {test_name}\n")
                f.write("\n")
        
        logger.info(f"📄 Markdown report saved to: {markdown_path}")

if __name__ == "__main__":
    tester = Phase5IntegrationTester()
    success = tester.run_all_phase5_tests()
    sys.exit(0 if success else 1) 