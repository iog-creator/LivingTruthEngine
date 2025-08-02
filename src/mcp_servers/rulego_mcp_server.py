#!/usr/bin/env python3
"""
Rulego MCP Server
Workflow orchestration and chain management
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

class RulegoEngine:
    def __init__(self):
        self.rulego_url = os.getenv('RULEGO_URL', 'http://localhost:9127')
        self.config_file = project_root / 'config' / 'rulego.conf'
        self.workflows_dir = project_root / 'data' / 'workflows' / 'rulego'
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Rulego Engine initialized")
        logger.info(f"Rulego URL: {self.rulego_url}")

    def query_rulego_chain(self, query: str, chain_name: str = "default") -> str:
        """Query a Rulego workflow chain.
        
        Args:
            query: Input query
            chain_name: Name of the workflow chain
        
        Returns:
            Chain execution result
        """
        try:
            # Placeholder for Rulego chain execution
            # TODO: Implement actual Rulego chain query
            result = {
                "query": query,
                "chain": chain_name,
                "result": f"Rulego chain '{chain_name}' executed for query: {query}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "completed"
            }
            
            # Save result to workflows directory
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            result_file = self.workflows_dir / f"rulego_result_{timestamp}.json"
            
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            logger.info(f"Rulego chain query completed: {result_file}")
            return f"✅ Rulego chain query completed\n🔗 Chain: {chain_name}\n📁 Result: {result_file}\n⚠️ Note: This is a placeholder. Implement actual Rulego integration."
            
        except Exception as e:
            logger.error(f"Rulego chain query failed: {e}")
            return f"❌ Rulego chain query failed: {e}"

    def get_rulego_status(self) -> str:
        """Get Rulego server status."""
        try:
            response = requests.get(f"{self.rulego_url}/health", timeout=5)
            if response.status_code == 200:
                return f"✅ Rulego server is healthy\n🔗 URL: {self.rulego_url}"
            else:
                return f"❌ Rulego server unhealthy: {response.status_code}"
        except Exception as e:
            return f"❌ Rulego server connection failed: {e}"

    def list_rulego_chains(self) -> str:
        """List available Rulego workflow chains."""
        try:
            # Placeholder for chain listing
            # TODO: Implement actual Rulego chain listing
            chains = [
                "default",
                "analysis",
                "correlation",
                "visualization"
            ]
            
            return f"✅ Available Rulego chains:\n" + "\n".join([f"  - {chain}" for chain in chains])
            
        except Exception as e:
            logger.error(f"Failed to list Rulego chains: {e}")
            return f"❌ Failed to list Rulego chains: {e}"

    def create_rulego_chain(self, chain_name: str, chain_config: str) -> str:
        """Create a new Rulego workflow chain.
        
        Args:
            chain_name: Name of the new chain
            chain_config: Chain configuration (JSON string)
        
        Returns:
            Status of chain creation
        """
        try:
            # Validate JSON configuration
            config_data = json.loads(chain_config)
            
            # Save chain configuration
            chain_file = self.workflows_dir / f"{chain_name}.json"
            
            with open(chain_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info(f"Rulego chain created: {chain_file}")
            return f"✅ Rulego chain '{chain_name}' created\n📁 Config: {chain_file}\n⚠️ Note: This is a placeholder. Implement actual Rulego chain creation."
            
        except json.JSONDecodeError as e:
            return f"❌ Invalid JSON configuration: {e}"
        except Exception as e:
            logger.error(f"Failed to create Rulego chain: {e}")
            return f"❌ Failed to create Rulego chain: {e}"

# Create engine instance
engine = RulegoEngine()

# MCP Tools
@mcp.tool()
def query_rulego_chain(query: str, chain_name: str = "default") -> str:
    """Query a Rulego workflow chain."""
    return engine.query_rulego_chain(query, chain_name)

@mcp.tool()
def get_rulego_status() -> str:
    """Get Rulego server status."""
    return engine.get_rulego_status()

@mcp.tool()
def list_rulego_chains() -> str:
    """List available Rulego workflow chains."""
    return engine.list_rulego_chains()

@mcp.tool()
def create_rulego_chain(chain_name: str, chain_config: str) -> str:
    """Create a new Rulego workflow chain."""
    return engine.create_rulego_chain(chain_name, chain_config)

@mcp.tool()
def get_rulego_info() -> str:
    """Get Rulego project information."""
    try:
        info = []
        info.append("=== RULEGO PROJECT INFO ===")
        info.append(f"Project Root: {project_root}")
        info.append(f"Rulego URL: {engine.rulego_url}")
        info.append(f"Config File: {engine.config_file}")
        info.append(f"Workflows Directory: {engine.workflows_dir}")
        
        info.append("\n=== AVAILABLE TOOLS ===")
        tools = [
            "query_rulego_chain - Query a Rulego workflow chain",
            "get_rulego_status - Get Rulego server status",
            "list_rulego_chains - List available Rulego workflow chains",
            "create_rulego_chain - Create a new Rulego workflow chain",
            "get_rulego_info - Get Rulego project information"
        ]
        info.extend(tools)
        
        info.append("\n=== RULEGO VS LANGFLOW ===")
        info.append("Pros of Rulego:")
        info.append("  - Lighter weight (no database required)")
        info.append("  - Hot updates and reloading")
        info.append("  - Built-in visualization")
        info.append("  - Go-based performance")
        info.append("Cons of Rulego:")
        info.append("  - Less AI-focused than Langflow")
        info.append("  - Requires compilation")
        info.append("  - Smaller ecosystem")
        
        return "\n".join(info)
    except Exception as e:
        return f"❌ Error getting Rulego info: {e}"

if __name__ == "__main__":
    logger.info("Rulego MCP Server starting...")
    print("Rulego MCP Server started...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Rulego MCP Server stopped by user")
    except Exception as e:
        logger.error(f"Rulego MCP Server error: {e}")
        sys.exit(1) 