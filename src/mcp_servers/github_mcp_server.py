#!/usr/bin/env python3
"""
GitHub MCP Server for Living Truth Engine
Provides GitHub repository management and collaboration tools
"""

import os
import sys
import json
import logging
import requests
from typing import Dict, Any, List, Optional
from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
project_root = Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP("GitHub MCP Server")

class GitHubIntegration:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_username = os.getenv('GITHUB_USERNAME')
        self.base_url = "https://api.github.com"
        
        if not self.github_token:
            logger.warning("GITHUB_TOKEN not configured")
        
        logger.info(f"GitHub integration initialized for user: {self.github_username}")

    def _get_headers(self) -> Dict[str, str]:
        """Get GitHub API headers."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers

    def list_repositories(self) -> str:
        """List user repositories."""
        try:
            if not self.github_username:
                return "❌ GITHUB_USERNAME not configured"
            
            url = f"{self.base_url}/users/{self.github_username}/repos"
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 200:
                repos = response.json()
                result = "📚 **Available Repositories:**\n\n"
                for repo in repos[:10]:  # Show first 10
                    result += f"- **{repo['name']}**: {repo['description'] or 'No description'}\n"
                    result += f"  - URL: {repo['html_url']}\n"
                    result += f"  - Language: {repo['language'] or 'Not specified'}\n\n"
                return result
            else:
                return f"❌ Failed to fetch repositories: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error listing repositories: {e}")
            return f"❌ Error: {str(e)}"

    def create_issue(self, repo: str, title: str, body: str, labels: List[str] = None) -> str:
        """Create a GitHub issue."""
        try:
            if not self.github_token:
                return "❌ GITHUB_TOKEN not configured"
            
            url = f"{self.base_url}/repos/{self.github_username}/{repo}/issues"
            payload = {
                "title": title,
                "body": body
            }
            if labels:
                payload["labels"] = labels
            
            response = requests.post(url, json=payload, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 201:
                issue = response.json()
                return f"✅ Issue created successfully!\n\n**Title**: {issue['title']}\n**URL**: {issue['html_url']}\n**Number**: #{issue['number']}"
            else:
                return f"❌ Failed to create issue: {response.status_code} - {response.text}"
                
        except Exception as e:
            logger.error(f"Error creating issue: {e}")
            return f"❌ Error: {str(e)}"

    def search_repositories(self, query: str, language: str = None) -> str:
        """Search GitHub repositories."""
        try:
            search_query = query
            if language:
                search_query += f" language:{language}"
            
            url = f"{self.base_url}/search/repositories"
            params = {"q": search_query, "sort": "stars", "order": "desc"}
            
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                repos = data.get('items', [])
                
                result = f"🔍 **Search Results for '{query}'**:\n\n"
                for repo in repos[:5]:  # Show top 5
                    result += f"- **{repo['full_name']}**: {repo['description'] or 'No description'}\n"
                    result += f"  - Stars: ⭐ {repo['stargazers_count']}\n"
                    result += f"  - Language: {repo['language'] or 'Not specified'}\n"
                    result += f"  - URL: {repo['html_url']}\n\n"
                return result
            else:
                return f"❌ Search failed: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error searching repositories: {e}")
            return f"❌ Error: {str(e)}"

# MCP Tool Definitions
@mcp.tool()
def list_repositories() -> str:
    """List GitHub repositories for the configured user."""
    github = GitHubIntegration()
    return github.list_repositories()

@mcp.tool()
def create_issue(repo: str, title: str, body: str, labels: str = "") -> str:
    """Create a GitHub issue in the specified repository."""
    github = GitHubIntegration()
    label_list = [label.strip() for label in labels.split(",")] if labels else []
    return github.create_issue(repo, title, body, label_list)

@mcp.tool()
def search_repositories(query: str, language: str = "") -> str:
    """Search GitHub repositories by query and optional language filter."""
    github = GitHubIntegration()
    return github.search_repositories(query, language if language else None)

@mcp.tool()
def get_github_status() -> str:
    """Get GitHub integration status and configuration."""
    github = GitHubIntegration()
    status = {
        "github_username": github.github_username or "❌ Not configured",
        "github_token": "✅ Configured" if github.github_token else "❌ Not configured",
        "base_url": github.base_url
    }
    return json.dumps(status, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio") 