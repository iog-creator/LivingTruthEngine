#!/usr/bin/env python3
"""
Hugging Face MCP Server for Living Truth Engine
Provides access to Hugging Face models and datasets
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
mcp = FastMCP("Hugging Face MCP Server")

class HuggingFaceIntegration:
    def __init__(self):
        self.hf_token = os.getenv('HUGGINGFACE_TOKEN')
        self.base_url = "https://huggingface.co/api"
        
        if not self.hf_token:
            logger.warning("HUGGINGFACE_TOKEN not configured")
        
        logger.info("Hugging Face integration initialized")

    def _get_headers(self) -> Dict[str, str]:
        """Get Hugging Face API headers."""
        headers = {
            "Content-Type": "application/json"
        }
        if self.hf_token:
            headers["Authorization"] = f"Bearer {self.hf_token}"
        return headers

    def search_models(self, query: str, limit: int = 10) -> str:
        """Search for models on Hugging Face."""
        try:
            url = f"{self.base_url}/models"
            params = {
                "search": query,
                "limit": limit,
                "sort": "downloads",
                "direction": "-1"
            }
            
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 200:
                models = response.json()
                
                result = f"🤗 **Hugging Face Models for '{query}'**:\n\n"
                for model in models:
                    result += f"- **{model['modelId']}**: {model.get('description', 'No description')}\n"
                    result += f"  - Downloads: 📥 {model.get('downloads', 0):,}\n"
                    result += f"  - Likes: ❤️ {model.get('likes', 0)}\n"
                    result += f"  - Tags: {', '.join(model.get('tags', []))}\n"
                    result += f"  - URL: https://huggingface.co/{model['modelId']}\n\n"
                return result
            else:
                return f"❌ Search failed: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error searching models: {e}")
            return f"❌ Error: {str(e)}"

    def get_model_info(self, model_id: str) -> str:
        """Get detailed information about a specific model."""
        try:
            url = f"{self.base_url}/models/{model_id}"
            
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 200:
                model = response.json()
                
                result = f"🤗 **Model Information: {model_id}**\n\n"
                result += f"**Description**: {model.get('description', 'No description')}\n\n"
                result += f"**Stats**:\n"
                result += f"- Downloads: 📥 {model.get('downloads', 0):,}\n"
                result += f"- Likes: ❤️ {model.get('likes', 0)}\n"
                result += f"- Author: 👤 {model.get('author', 'Unknown')}\n\n"
                result += f"**Tags**: {', '.join(model.get('tags', []))}\n\n"
                result += f"**URL**: https://huggingface.co/{model_id}\n"
                
                return result
            else:
                return f"❌ Model not found: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return f"❌ Error: {str(e)}"

    def search_datasets(self, query: str, limit: int = 10) -> str:
        """Search for datasets on Hugging Face."""
        try:
            url = f"{self.base_url}/datasets"
            params = {
                "search": query,
                "limit": limit,
                "sort": "downloads",
                "direction": "-1"
            }
            
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 200:
                datasets = response.json()
                
                result = f"📊 **Hugging Face Datasets for '{query}'**:\n\n"
                for dataset in datasets:
                    result += f"- **{dataset['id']}**: {dataset.get('description', 'No description')}\n"
                    result += f"  - Downloads: 📥 {dataset.get('downloads', 0):,}\n"
                    result += f"  - Likes: ❤️ {dataset.get('likes', 0)}\n"
                    result += f"  - Tags: {', '.join(dataset.get('tags', []))}\n"
                    result += f"  - URL: https://huggingface.co/datasets/{dataset['id']}\n\n"
                return result
            else:
                return f"❌ Search failed: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error searching datasets: {e}")
            return f"❌ Error: {str(e)}"

    def get_recommended_models(self, task: str = "text-generation") -> str:
        """Get recommended models for a specific task."""
        try:
            url = f"{self.base_url}/models"
            params = {
                "filter": task,
                "limit": 10,
                "sort": "downloads",
                "direction": "-1"
            }
            
            response = requests.get(url, params=params, headers=self._get_headers(), timeout=30)
            
            if response.status_code == 200:
                models = response.json()
                
                result = f"🎯 **Recommended Models for '{task}'**:\n\n"
                for model in models:
                    result += f"- **{model['modelId']}**: {model.get('description', 'No description')}\n"
                    result += f"  - Downloads: 📥 {model.get('downloads', 0):,}\n"
                    result += f"  - URL: https://huggingface.co/{model['modelId']}\n\n"
                return result
            else:
                return f"❌ Failed to get recommendations: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return f"❌ Error: {str(e)}"

# MCP Tool Definitions
@mcp.tool()
def search_models(query: str, limit: int = 10) -> str:
    """Search for models on Hugging Face Hub."""
    hf = HuggingFaceIntegration()
    return hf.search_models(query, limit)

@mcp.tool()
def get_model_info(model_id: str) -> str:
    """Get detailed information about a specific Hugging Face model."""
    hf = HuggingFaceIntegration()
    return hf.get_model_info(model_id)

@mcp.tool()
def search_datasets(query: str, limit: int = 10) -> str:
    """Search for datasets on Hugging Face Hub."""
    hf = HuggingFaceIntegration()
    return hf.search_datasets(query, limit)

@mcp.tool()
def get_recommended_models(task: str = "text-generation") -> str:
    """Get recommended models for a specific task."""
    hf = HuggingFaceIntegration()
    return hf.get_recommended_models(task)

@mcp.tool()
def get_huggingface_status() -> str:
    """Get Hugging Face integration status and configuration."""
    hf = HuggingFaceIntegration()
    status = {
        "huggingface_token": "✅ Configured" if hf.hf_token else "❌ Not configured",
        "base_url": hf.base_url
    }
    return json.dumps(status, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio") 