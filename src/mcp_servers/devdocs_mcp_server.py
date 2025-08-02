#!/usr/bin/env python3
"""
DevDocs MCP Server
Document retrieval and crawling functionality
"""

import os
import sys
import json
import logging
import requests
import time
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP()

class DevDocsEngine:
    def __init__(self):
        self.devdocs_url = os.getenv('DEVDOCS_URL', 'http://localhost:9126')
        self.crawl_results_dir = project_root / 'data' / 'sources' / 'devdocs'
        self.crawl_results_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"DevDocs Engine initialized")
        logger.info(f"DevDocs URL: {self.devdocs_url}")

    def crawl_docs(self, depth: int = 3) -> str:
        """Crawl documentation from DevDocs.
        
        Args:
            depth: Crawl depth (default: 3)
        
        Returns:
            Status of crawl operation
        """
        try:
            # Create crawl results file
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            results_file = self.crawl_results_dir / f"crawl_results_{timestamp}.json"
            
            # Placeholder for actual crawling logic
            # TODO: Implement actual DevDocs crawling
            crawl_data = {
                "timestamp": timestamp,
                "depth": depth,
                "status": "initiated",
                "urls_crawled": [],
                "documents_found": 0
            }
            
            with open(results_file, 'w') as f:
                json.dump(crawl_data, f, indent=2)
            
            logger.info(f"Document crawl initiated: {results_file}")
            return f"✅ Document crawl initiated\n📁 Results: {results_file}\n⚠️ Note: This is a placeholder. Implement actual DevDocs crawling."
            
        except Exception as e:
            logger.error(f"Document crawl failed: {e}")
            return f"❌ Document crawl failed: {e}"

    def retrieve_docs(self, query: str) -> str:
        """Retrieve documents from DevDocs.
        
        Args:
            query: Search query
        
        Returns:
            Retrieved documents
        """
        try:
            # Placeholder for document retrieval
            # TODO: Implement actual DevDocs retrieval
            results = {
                "query": query,
                "results": [],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info(f"Document retrieval for query: {query}")
            return f"✅ Document retrieval completed\n🔍 Query: {query}\n📄 Results: {len(results['results'])} documents\n⚠️ Note: This is a placeholder. Implement actual DevDocs retrieval."
            
        except Exception as e:
            logger.error(f"Document retrieval failed: {e}")
            return f"❌ Document retrieval failed: {e}"

    def get_devdocs_status(self) -> str:
        """Get DevDocs server status."""
        try:
            response = requests.get(f"{self.devdocs_url}/health", timeout=5)
            if response.status_code == 200:
                return f"✅ DevDocs server is healthy\n🔗 URL: {self.devdocs_url}"
            else:
                return f"❌ DevDocs server unhealthy: {response.status_code}"
        except Exception as e:
            return f"❌ DevDocs server connection failed: {e}"

# Create engine instance
engine = DevDocsEngine()

# MCP Tools
@mcp.tool()
def crawl_docs(depth: int = 3) -> str:
    """Crawl documentation from DevDocs."""
    return engine.crawl_docs(depth)

@mcp.tool()
def retrieve_docs(query: str) -> str:
    """Retrieve documents from DevDocs."""
    return engine.retrieve_docs(query)

@mcp.tool()
def get_devdocs_status() -> str:
    """Get DevDocs server status."""
    return engine.get_devdocs_status()

@mcp.tool()
def get_devdocs_info() -> str:
    """Get DevDocs project information."""
    try:
        info = []
        info.append("=== DEVDOCS PROJECT INFO ===")
        info.append(f"Project Root: {project_root}")
        info.append(f"DevDocs URL: {engine.devdocs_url}")
        info.append(f"Crawl Results Directory: {engine.crawl_results_dir}")
        
        info.append("\n=== AVAILABLE TOOLS ===")
        tools = [
            "crawl_docs - Crawl documentation from DevDocs",
            "retrieve_docs - Retrieve documents from DevDocs",
            "get_devdocs_status - Get DevDocs server status",
            "get_devdocs_info - Get DevDocs project information"
        ]
        info.extend(tools)
        
        return "\n".join(info)
    except Exception as e:
        return f"❌ Error getting DevDocs info: {e}"

if __name__ == "__main__":
    logger.info("DevDocs MCP Server starting...")
    print("DevDocs MCP Server started...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("DevDocs MCP Server stopped by user")
    except Exception as e:
        logger.error(f"DevDocs MCP Server error: {e}")
        sys.exit(1) 