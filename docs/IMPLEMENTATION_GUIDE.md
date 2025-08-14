---
phase: 9
status: active
last_reviewed: 2025-08-14
related_files: ['scripts/comprehensive_model_test.py', 'tests/test_missing_components.py', 'src/ai/dynamic_embedding_selector.py', 'src/visualization/enhanced_3d_visualizer.py', 'src/ai/prompt_manager.py']
---

# Implementation Guide
## Step-by-Step Rebuild Instructions for Missing Components

**Date**: August 14, 2025  
**Status**: Ready for Implementation  
**Priority**: High - Critical functionality missing

---

## 🚀 **PHASE 1: DYNAMIC EMBEDDING SELECTOR**

### **Step 1: Create the Core File**
Create `src/ai/dynamic_embedding_selector.py`:

```python
#!/usr/bin/env python3
"""
Dynamic Embedding Selector for Living Truth Engine

Selects appropriate embedding model based on task type:
- Qwen3-Embedding-0.6B (1024 dim) for general tasks
- MiniLM (384 dim) for Bible searching tasks
"""

import os
import logging
import requests
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)

class DynamicEmbeddingSelector:
    """Dynamic embedding model selector based on task type"""
    
    def __init__(self, config=None):
        # Model configurations
        self.models = {
            "qwen3": {
                "name": "text-embedding-qwen3-embedding-0.6b",
                "dimension": 1024,
                "url": "http://localhost:1234/v1/embeddings",
                "description": "Qwen3-Embedding-0.6B for general tasks"
            },
            "minilm": {
                "name": "text-embedding-all-minilm-l6-v2-embedding",
                "dimension": 384,
                "url": "http://localhost:1234/v1/embeddings",
                "description": "MiniLM for Bible searching tasks"
            }
        }
        
        # Task type to model mapping
        self.task_model_mapping = {
            "notebook_agent": "qwen3",
            "bible_search": "minilm",
            "general": "qwen3",
            "forensic": "qwen3",
            "survivor_testimony": "qwen3",
            "elite_network": "qwen3",
            "temporal_analysis": "qwen3"
        }
        
        logger.info("Dynamic embedding selector initialized")
    
    def get_model_for_task(self, task_type: str) -> Dict[str, Any]:
        """Get appropriate embedding model for task type"""
        model_key = self.task_model_mapping.get(task_type.lower(), "qwen3")
        model_config = self.models[model_key]
        
        logger.info(f"Selected {model_key} model for task: {task_type}")
        logger.info(f"Model: {model_config['name']}, Dimension: {model_config['dimension']}")
        
        return model_config
    
    def get_dimension_for_task(self, task_type: str) -> int:
        """Get embedding dimension for task type"""
        model_config = self.get_model_for_task(task_type)
        return model_config["dimension"]
    
    def validate_model_availability(self) -> Dict[str, bool]:
        """Validate that all models are available via LM Studio"""
        availability = {}
        
        for model_key, model_config in self.models.items():
            try:
                response = requests.post(
                    model_config["url"],
                    json={
                        "model": model_config["name"],
                        "input": ["test"]
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    availability[model_key] = True
                    logger.info(f"✅ Model {model_key} ({model_config['name']}) is available")
                else:
                    availability[model_key] = False
                    logger.warning(f"❌ Model {model_key} ({model_config['name']}) is not available: {response.status_code}")
                    
            except Exception as e:
                availability[model_key] = False
                logger.error(f"❌ Model {model_key} ({model_config['name']}) error: {e}")
        
        return availability

# Global instance
embedding_selector = DynamicEmbeddingSelector()

def get_embedding_model(task_type: str) -> Dict[str, Any]:
    """Convenience function to get embedding model for task"""
    return embedding_selector.get_model_for_task(task_type)

def get_embedding_dimension(task_type: str) -> int:
    """Convenience function to get embedding dimension for task"""
    return embedding_selector.get_dimension_for_task(task_type)
```

### **Step 2: Create Configuration**
Add to your config file:

```python
# Add to your configuration
EMBEDDING_MODELS = {
    "qwen3": {
        "name": "text-embedding-qwen3-embedding-0.6b",
        "dimension": 1024,
        "url": "http://localhost:1234/v1/embeddings"
    },
    "minilm": {
        "name": "text-embedding-all-minilm-l6-v2-embedding", 
        "dimension": 384,
        "url": "http://localhost:1234/v1/embeddings"
    }
}
```

### **Step 3: Integration**
Update your existing embedding pipeline to use the selector:

```python
from src.ai.dynamic_embedding_selector import get_embedding_model, get_embedding_dimension

# In your embedding code:
def get_embeddings(text: str, task_type: str = "general"):
    model_config = get_embedding_model(task_type)
    dimension = get_embedding_dimension(task_type)
    
    # Use model_config for API calls
    # Use dimension for database operations
```

---

## 🚀 **PHASE 2: ENHANCED BIBLICAL PROMPTS**

### **Step 1: Create Directory Structure**
```bash
mkdir -p prompts/enhanced_prompts
```

### **Step 2: Biblical Evidence Extraction Prompt**
Create `prompts/enhanced_prompts/biblical_evidence_extraction.txt`:

```text
You are a Biblical forensic analyst specializing in evidence extraction and survivor protection.

TASK: Extract Biblical evidence and abuse patterns from the provided document.

CRITICAL REQUIREMENTS:
- Focus on Biblical references (pre-300 AD)
- Identify survivor testimony indicators
- Detect elite network patterns
- Maintain survivor dignity and privacy
- Provide confidence scores based on evidence quality

RESPONSE FORMAT: You must respond with ONLY valid JSON matching this exact structure:

{
  "biblical_references": [
    {
      "reference": "Psalm 82:3-4",
      "relevance": "Defend the weak and fatherless",
      "confidence": 0.85,
      "context": "Direct Biblical command for justice"
    }
  ],
  "survivor_indicators": [
    {
      "type": "testimony",
      "confidence": 0.78,
      "privacy_protected": true,
      "pattern": "first_person_experience"
    }
  ],
  "elite_networks": [
    {
      "network": "Epstein",
      "confidence": 0.82,
      "evidence_type": "direct_mention",
      "biblical_parallel": "Moloch_worship"
    }
  ],
  "abuse_patterns": [
    {
      "pattern": "ritual_abuse",
      "confidence": 0.75,
      "biblical_reference": "Ezekiel 16:20-21",
      "historical_corroboration": true
    }
  ],
  "overall_confidence": 0.80,
  "privacy_compliance": true,
  "biblical_compliance": true
}

DOCUMENT TO ANALYZE:
{document}

CRITICAL: Respond ONLY with valid JSON matching the example format above. Do not include any thinking tags, explanations, or text outside the JSON object.
```

### **Step 3: Elite Network Analysis Prompt**
Create `prompts/enhanced_prompts/elite_network_analysis.txt`:

```text
You are a Biblical forensic analyst specializing in elite network analysis and justice-seeking.

TASK: Analyze elite networks and their connections to abuse patterns.

CRITICAL REQUIREMENTS:
- Focus on Biblical justice principles
- Identify network connections and patterns
- Maintain survivor privacy and dignity
- Provide evidence-based confidence scores
- Apply Isaiah 1:17 principles (seek justice, correct oppression)

RESPONSE FORMAT: You must respond with ONLY valid JSON matching this exact structure:

{
  "elite_networks": [
    {
      "network": "Epstein",
      "confidence": 0.85,
      "connections": ["political_elite", "business_elite"],
      "biblical_parallel": "Moloch_worship",
      "evidence_type": "direct_mention"
    }
  ],
  "network_connections": [
    {
      "from_network": "Epstein",
      "to_network": "political_elite",
      "connection_type": "financial",
      "confidence": 0.78,
      "biblical_principle": "Isaiah 1:17"
    }
  ],
  "abuse_patterns": [
    {
      "pattern": "ritual_abuse",
      "confidence": 0.82,
      "biblical_reference": "Ezekiel 16:20-21",
      "network_involvement": ["Epstein", "religious_elite"]
    }
  ],
  "biblical_justice_applications": [
    {
      "principle": "Isaiah 1:17",
      "application": "correct_oppression",
      "confidence": 0.88,
      "network_target": "Epstein"
    }
  ],
  "overall_confidence": 0.83,
  "justice_focus": true,
  "survivor_protection": true
}

NETWORK DATA TO ANALYZE:
{network_data}

CRITICAL: Respond ONLY with valid JSON matching the example format above. Do not include any thinking tags, explanations, or text outside the JSON object.
```

### **Step 4: Survivor Testimony Analysis Prompt**
Create `prompts/enhanced_prompts/survivor_testimony_analysis.txt`:

```text
You are a trauma-informed Biblical forensic analyst specializing in survivor testimony analysis.

TASK: Analyze survivor testimony while protecting privacy and dignity.

CRITICAL REQUIREMENTS:
- Protect survivor privacy and dignity
- Focus on Biblical justice principles
- Identify patterns without exposing personal details
- Maintain Psalm 82:3-4 compliance (defend the weak)
- Provide confidence scores for evidence quality

RESPONSE FORMAT: You must respond with ONLY valid JSON matching this exact structure:

{
  "testimony_indicators": [
    {
      "type": "first_person_experience",
      "confidence": 0.85,
      "privacy_protected": true,
      "biblical_principle": "Psalm 82:3-4"
    }
  ],
  "abuse_patterns": [
    {
      "pattern": "psychological_manipulation",
      "confidence": 0.78,
      "biblical_reference": "Isaiah 1:17",
      "justice_focus": true
    }
  ],
  "elite_networks": [
    {
      "network": "religious_institution",
      "confidence": 0.75,
      "evidence_type": "institutional_pattern",
      "privacy_protected": true
    }
  ],
  "biblical_justice_applications": [
    {
      "principle": "Isaiah 1:17",
      "application": "seek_justice",
      "confidence": 0.82
    }
  ],
  "overall_confidence": 0.80,
  "privacy_compliance": true,
  "survivor_protection": true
}

TESTIMONY TO ANALYZE:
{testimony}

CRITICAL: Respond ONLY with valid JSON matching the example format above. Do not include any thinking tags, explanations, or text outside the JSON object.
```

### **Step 5: Prompt Management System**
Create `src/ai/prompt_manager.py`:

```python
#!/usr/bin/env python3
"""
Prompt Management System for Enhanced Biblical Analysis
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PromptManager:
    """Manages enhanced Biblical forensic prompts"""
    
    def __init__(self, prompts_dir: str = "prompts/enhanced_prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts = {}
        self._load_prompts()
    
    def _load_prompts(self):
        """Load all prompts from the prompts directory"""
        prompt_files = {
            "biblical_evidence": "biblical_evidence_extraction.txt",
            "elite_network": "elite_network_analysis.txt",
            "survivor_testimony": "survivor_testimony_analysis.txt"
        }
        
        for prompt_type, filename in prompt_files.items():
            file_path = self.prompts_dir / filename
            if file_path.exists():
                self.prompts[prompt_type] = file_path.read_text()
                logger.info(f"Loaded prompt: {prompt_type}")
            else:
                logger.warning(f"Prompt file not found: {file_path}")
    
    def get_prompt(self, prompt_type: str, **kwargs) -> str:
        """Get formatted prompt for specific analysis type"""
        if prompt_type not in self.prompts:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        prompt_template = self.prompts[prompt_type]
        
        # Format the prompt with provided parameters
        try:
            formatted_prompt = prompt_template.format(**kwargs)
            return formatted_prompt
        except KeyError as e:
            logger.error(f"Missing required parameter for prompt {prompt_type}: {e}")
            raise
    
    def validate_json_response(self, response: str) -> Dict[str, Any]:
        """Validate and parse JSON response from LLM"""
        try:
            # Clean the response (remove any non-JSON text)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in response")
            
            json_str = response[json_start:json_end]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")
    
    def analyze_biblical_evidence(self, document: str) -> Dict[str, Any]:
        """Analyze document for Biblical evidence"""
        prompt = self.get_prompt("biblical_evidence", document=document)
        # This would be sent to your LLM
        # For now, return a placeholder
        return {"status": "prompt_ready", "prompt": prompt}
    
    def analyze_elite_networks(self, network_data: str) -> Dict[str, Any]:
        """Analyze elite network data"""
        prompt = self.get_prompt("elite_network", network_data=network_data)
        return {"status": "prompt_ready", "prompt": prompt}
    
    def analyze_survivor_testimony(self, testimony: str) -> Dict[str, Any]:
        """Analyze survivor testimony"""
        prompt = self.get_prompt("survivor_testimony", testimony=testimony)
        return {"status": "prompt_ready", "prompt": prompt}

# Global instance
prompt_manager = PromptManager()
```

---

## 🚀 **PHASE 3: COMPREHENSIVE MODEL TESTING**

### **Step 1: Create Testing Framework**
Create `scripts/comprehensive_model_test.py`:

```python
#!/usr/bin/env python3
"""
Comprehensive Model Testing Framework
Tests all models in the Living Truth Engine system
"""

import time
import json
import logging
import requests
from typing import Dict, List, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class ComprehensiveModelTester:
    """Comprehensive testing framework for all models"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0
        self.skipped_count = 0
    
    def test_lm_studio_connection(self) -> bool:
        """Test LM Studio connection and available models"""
        try:
            response = requests.get("http://localhost:1234/v1/models", timeout=10)
            if response.status_code == 200:
                models = response.json()
                logger.info(f"✅ LM Studio connection successful. {len(models['data'])} models available")
                return True
            else:
                logger.error(f"❌ LM Studio connection failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ LM Studio connection error: {e}")
            return False
    
    def test_embedding_model(self, model_name: str, expected_dim: int) -> bool:
        """Test embedding model"""
        try:
            response = requests.post(
                "http://localhost:1234/v1/embeddings",
                json={
                    "model": model_name,
                    "input": ["test embedding"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                embedding = result["data"][0]["embedding"]
                actual_dim = len(embedding)
                
                if actual_dim == expected_dim:
                    logger.info(f"✅ {model_name}: {actual_dim} dimensions (expected {expected_dim})")
                    return True
                else:
                    logger.error(f"❌ {model_name}: {actual_dim} dimensions (expected {expected_dim})")
                    return False
            else:
                logger.error(f"❌ {model_name}: API error {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ {model_name}: {e}")
            return False
    
    def test_llm_model(self, model_name: str) -> bool:
        """Test LLM model"""
        try:
            response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                json={
                    "model": model_name,
                    "messages": [{"role": "user", "content": "Test response"}],
                    "max_tokens": 100
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                logger.info(f"✅ {model_name}: Generated {len(content)} characters")
                return True
            else:
                logger.error(f"❌ {model_name}: API error {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ {model_name}: {e}")
            return False
    
    def test_reranker_model(self, model_name: str) -> bool:
        """Test reranker model"""
        try:
            response = requests.post(
                "http://localhost:1234/v1/rerank",
                json={
                    "model": model_name,
                    "query": "test query",
                    "documents": ["test document 1", "test document 2"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ {model_name}: Reranking successful")
                return True
            else:
                logger.warning(f"⚠️ {model_name}: API error {response.status_code} (may not support reranking)")
                return False
                
        except Exception as e:
            logger.warning(f"⚠️ {model_name}: {e} (may not support reranking)")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all comprehensive model tests"""
        logger.info("🔍 Starting comprehensive model testing...")
        
        # Test 1: LM Studio Connection
        self.test_count += 1
        if self.test_lm_studio_connection():
            self.passed_count += 1
            self.results["lm_studio_connection"] = "PASS"
        else:
            self.failed_count += 1
            self.results["lm_studio_connection"] = "FAIL"
        
        # Test 2: Qwen3 Embedding
        self.test_count += 1
        if self.test_embedding_model("text-embedding-qwen3-embedding-0.6b", 1024):
            self.passed_count += 1
            self.results["qwen3_embedding"] = "PASS"
        else:
            self.failed_count += 1
            self.results["qwen3_embedding"] = "FAIL"
        
        # Test 3: MiniLM Embedding
        self.test_count += 1
        if self.test_embedding_model("text-embedding-all-minilm-l6-v2-embedding", 384):
            self.passed_count += 1
            self.results["minilm_embedding"] = "PASS"
        else:
            self.failed_count += 1
            self.results["minilm_embedding"] = "FAIL"
        
        # Test 4: Qwen3 Reranker
        self.test_count += 1
        if self.test_reranker_model("qwen.qwen3-reranker-0.6b"):
            self.passed_count += 1
            self.results["qwen3_reranker"] = "PASS"
        else:
            self.skipped_count += 1
            self.results["qwen3_reranker"] = "SKIP"
        
        # Test 5: Qwen3 LLM
        self.test_count += 1
        if self.test_llm_model("qwen/qwen3-8b"):
            self.passed_count += 1
            self.results["qwen3_llm"] = "PASS"
        else:
            self.failed_count += 1
            self.results["qwen3_llm"] = "FAIL"
        
        # Calculate metrics
        duration = time.time() - self.start_time
        success_rate = (self.passed_count / self.test_count) * 100 if self.test_count > 0 else 0
        
        summary = {
            "total_tests": self.test_count,
            "passed": self.passed_count,
            "failed": self.failed_count,
            "skipped": self.skipped_count,
            "success_rate": f"{success_rate:.1f}%",
            "duration": f"{duration:.2f}s",
            "results": self.results
        }
        
        logger.info(f"✅ Testing complete: {self.passed_count}/{self.test_count} passed ({success_rate:.1f}%)")
        return summary

def main():
    """Main testing function"""
    tester = ComprehensiveModelTester()
    results = tester.run_all_tests()
    
    # Print summary
    print("\n" + "="*50)
    print("COMPREHENSIVE MODEL TEST RESULTS")
    print("="*50)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Success Rate: {results['success_rate']}")
    print(f"Duration: {results['duration']}")
    print("\nDetailed Results:")
    for test, result in results['results'].items():
        print(f"  {test}: {result}")
    
    # Save results
    output_file = Path("logs/comprehensive_model_test_results.json")
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
```

---

## 🚀 **PHASE 4: ADVANCED 3D VISUALIZATION**

### **Step 1: Create Enhanced 3D Visualizer**
Create `src/visualization/enhanced_3d_visualizer.py`:

```python
#!/usr/bin/env python3
"""
Enhanced 3D Visualization System for Biblical Forensic Analysis
"""

import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Enhanced3DVisualizer:
    """Enhanced 3D graph visualization for Biblical forensic analysis"""
    
    def __init__(self):
        # Color schemes for different entity types
        self.color_schemes = {
            'survivor': '#FF6B6B',  # Red for survivors
            'perpetrator': '#4ECDC4',  # Teal for perpetrators
            'elite_network': '#45B7D1',  # Blue for elite networks
            'location': '#96CEB4',  # Green for locations
            'biblical_reference': '#FFEAA7',  # Yellow for Biblical references
            'temporal': '#DDA0DD',  # Plum for temporal patterns
            'covert_operation': '#FF8C42',  # Orange for covert operations
            'trafficking': '#FF69B4',  # Pink for trafficking
            'abuse_relationship': '#FF4757',  # Bright red for abuse
            'legal_control': '#747D8C',  # Gray for legal control
            'spiritual_warfare': '#A55EEA',  # Purple for spiritual warfare
            'mind_control': '#26DE81'  # Bright green for mind control
        }
        
        # Node sizes based on importance
        self.node_sizes = {
            'survivor': 20,
            'perpetrator': 16,
            'elite_network': 25,
            'location': 12,
            'biblical_reference': 10,
            'temporal': 8,
            'covert_operation': 18,
            'trafficking': 22,
            'abuse_relationship': 24,
            'legal_control': 14,
            'spiritual_warfare': 20,
            'mind_control': 18
        }
    
    def create_3d_network_graph(self, graph_data: Dict[str, Any], output_file: str = None) -> go.Figure:
        """Create interactive 3D network graph visualization"""
        try:
            # Create NetworkX graph
            G = nx.Graph()
            
            # Add nodes
            for node_id, node_data in graph_data.get('nodes', {}).items():
                G.add_node(node_id, **node_data)
            
            # Add edges
            for edge in graph_data.get('edges', []):
                G.add_edge(edge['source'], edge['target'], **edge.get('attributes', {}))
            
            # Calculate 3D layout
            pos_3d = nx.spring_layout(G, dim=3, k=1, iterations=50)
            
            # Create interactive 3D scatter plot
            fig = go.Figure()
            
            # Group nodes by type
            node_types = {}
            for node_id, node_data in G.nodes(data=True):
                node_type = node_data.get('type', 'unknown')
                if node_type not in node_types:
                    node_types[node_type] = []
                node_types[node_type].append((node_id, node_data))
            
            # Add nodes by type
            for node_type, nodes in node_types.items():
                x_coords, y_coords, z_coords = [], [], []
                labels, confidences = [], []
                
                for node_id, node_data in nodes:
                    if node_id in pos_3d:
                        pos = pos_3d[node_id]
                        x_coords.append(pos[0])
                        y_coords.append(pos[1])
                        z_coords.append(pos[2])
                        
                        # Create hover text
                        confidence = node_data.get('confidence', 0)
                        description = node_data.get('description', '')
                        label = f"{node_id}<br>Confidence: {confidence:.2f}<br>{description}"
                        labels.append(label)
                        confidences.append(confidence)
                
                if x_coords:  # Only add if we have coordinates
                    fig.add_trace(go.Scatter3d(
                        x=x_coords,
                        y=y_coords,
                        z=z_coords,
                        mode='markers',
                        name=node_type.replace('_', ' ').title(),
                        marker=dict(
                            size=[self.node_sizes.get(node_type, 10)] * len(x_coords),
                            color=self.color_schemes.get(node_type, '#808080'),
                            opacity=0.8
                        ),
                        text=labels,
                        hovertemplate='%{text}<extra></extra>'
                    ))
            
            # Add edges
            edge_x, edge_y, edge_z = [], [], []
            for edge in G.edges():
                if edge[0] in pos_3d and edge[1] in pos_3d:
                    x0, y0, z0 = pos_3d[edge[0]]
                    x1, y1, z1 = pos_3d[edge[1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                    edge_z.extend([z0, z1, None])
            
            if edge_x:  # Only add if we have edges
                fig.add_trace(go.Scatter3d(
                    x=edge_x,
                    y=edge_y,
                    z=edge_z,
                    mode='lines',
                    line=dict(color='rgba(125,125,125,0.5)', width=1),
                    hoverinfo='none',
                    showlegend=False
                ))
            
            # Update layout
            fig.update_layout(
                title="Biblical Forensic Analysis - 3D Network Graph",
                scene=dict(
                    xaxis_title="X",
                    yaxis_title="Y", 
                    zaxis_title="Z",
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.5)
                    )
                ),
                width=1000,
                height=800,
                showlegend=True
            )
            
            # Save if output file specified
            if output_file:
                fig.write_html(output_file)
                logger.info(f"3D graph saved to: {output_file}")
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating 3D graph: {e}")
            raise
    
    def create_biblical_analysis_dashboard(self, analysis_data: Dict[str, Any]) -> go.Figure:
        """Create comprehensive Biblical analysis dashboard"""
        try:
            # Create subplots
            fig = go.Figure()
            
            # Add confidence scores
            if 'confidence_scores' in analysis_data:
                scores = analysis_data['confidence_scores']
                categories = list(scores.keys())
                values = list(scores.values())
                
                fig.add_trace(go.Bar(
                    x=categories,
                    y=values,
                    name="Confidence Scores",
                    marker_color='lightblue'
                ))
            
            # Update layout
            fig.update_layout(
                title="Biblical Analysis Dashboard",
                xaxis_title="Analysis Categories",
                yaxis_title="Confidence Score",
                width=800,
                height=600
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating dashboard: {e}")
            raise

# Global instance
visualizer = Enhanced3DVisualizer()
```

---

## 🚀 **PHASE 5: INTEGRATION AND TESTING**

### **Step 1: Create Integration Test**
Create `tests/test_missing_components.py`:

```python
#!/usr/bin/env python3
"""
Integration tests for missing components
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai.dynamic_embedding_selector import DynamicEmbeddingSelector
from ai.prompt_manager import PromptManager
from visualization.enhanced_3d_visualizer import Enhanced3DVisualizer

class TestDynamicEmbeddingSelector:
    """Test dynamic embedding selector"""
    
    def test_initialization(self):
        """Test selector initialization"""
        selector = DynamicEmbeddingSelector()
        assert selector is not None
        assert len(selector.models) == 2
        assert len(selector.task_model_mapping) > 0
    
    def test_task_mapping(self):
        """Test task to model mapping"""
        selector = DynamicEmbeddingSelector()
        
        # Test Bible search
        model = selector.get_model_for_task("bible_search")
        assert model["name"] == "text-embedding-all-minilm-l6-v2-embedding"
        assert model["dimension"] == 384
        
        # Test general task
        model = selector.get_model_for_task("general")
        assert model["name"] == "text-embedding-qwen3-embedding-0.6b"
        assert model["dimension"] == 1024
    
    def test_dimension_handling(self):
        """Test dimension handling"""
        selector = DynamicEmbeddingSelector()
        
        dim = selector.get_dimension_for_task("bible_search")
        assert dim == 384
        
        dim = selector.get_dimension_for_task("general")
        assert dim == 1024

class TestPromptManager:
    """Test prompt manager"""
    
    def test_initialization(self):
        """Test prompt manager initialization"""
        manager = PromptManager()
        assert manager is not None
        assert len(manager.prompts) > 0
    
    def test_prompt_loading(self):
        """Test prompt loading"""
        manager = PromptManager()
        
        # Check that all prompts are loaded
        expected_prompts = ["biblical_evidence", "elite_network", "survivor_testimony"]
        for prompt_type in expected_prompts:
            assert prompt_type in manager.prompts
    
    def test_prompt_formatting(self):
        """Test prompt formatting"""
        manager = PromptManager()
        
        # Test Biblical evidence prompt
        prompt = manager.get_prompt("biblical_evidence", document="Test document")
        assert "Test document" in prompt
        assert "biblical_evidence_extraction" in prompt.lower()

class TestEnhanced3DVisualizer:
    """Test enhanced 3D visualizer"""
    
    def test_initialization(self):
        """Test visualizer initialization"""
        visualizer = Enhanced3DVisualizer()
        assert visualizer is not None
        assert len(visualizer.color_schemes) > 0
        assert len(visualizer.node_sizes) > 0
    
    def test_3d_graph_creation(self):
        """Test 3D graph creation"""
        visualizer = Enhanced3DVisualizer()
        
        # Create test data
        test_data = {
            "nodes": {
                "node1": {"type": "survivor", "confidence": 0.8, "description": "Test survivor"},
                "node2": {"type": "perpetrator", "confidence": 0.7, "description": "Test perpetrator"}
            },
            "edges": [
                {"source": "node1", "target": "node2", "attributes": {"weight": 0.5}}
            ]
        }
        
        # Create graph
        fig = visualizer.create_3d_network_graph(test_data)
        assert fig is not None
        assert len(fig.data) > 0

def test_integration():
    """Test full integration"""
    # Test that all components work together
    selector = DynamicEmbeddingSelector()
    manager = PromptManager()
    visualizer = Enhanced3DVisualizer()
    
    # Test end-to-end workflow
    model = selector.get_model_for_task("bible_search")
    prompt = manager.get_prompt("biblical_evidence", document="Test")
    
    assert model is not None
    assert prompt is not None
    assert visualizer is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### **Step 2: Update Requirements**
Add to your `requirements.txt`:

```txt
# Enhanced visualization
plotly>=5.0.0
networkx>=3.0

# Enhanced prompts
jinja2>=3.0.0

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
```

### **Step 3: Create Configuration**
Update your configuration to include the new components:

```python
# Add to your config
ENHANCED_COMPONENTS = {
    "dynamic_embedding": {
        "enabled": True,
        "models": {
            "qwen3": {
                "name": "text-embedding-qwen3-embedding-0.6b",
                "dimension": 1024
            },
            "minilm": {
                "name": "text-embedding-all-minilm-l6-v2-embedding",
                "dimension": 384
            }
        }
    },
    "enhanced_prompts": {
        "enabled": True,
        "prompts_dir": "prompts/enhanced_prompts"
    },
    "3d_visualization": {
        "enabled": True,
        "color_schemes": True,
        "interactive": True
    }
}
```

---

## ✅ **FINAL INTEGRATION STEPS**

### **Step 1: Update Main Application**
Integrate the new components into your main application:

```python
# In your main application file
from src.ai.dynamic_embedding_selector import get_embedding_model
from src.ai.prompt_manager import prompt_manager
from src.visualization.enhanced_3d_visualizer import visualizer

# Use dynamic embedding selector
def analyze_document(document: str, task_type: str = "general"):
    model_config = get_embedding_model(task_type)
    # Use model_config for your analysis
    
    # Use enhanced prompts
    if task_type == "biblical_evidence":
        prompt = prompt_manager.get_prompt("biblical_evidence", document=document)
    elif task_type == "elite_network":
        prompt = prompt_manager.get_prompt("elite_network", network_data=document)
    elif task_type == "survivor_testimony":
        prompt = prompt_manager.get_prompt("survivor_testimony", testimony=document)
    
    # Send to LLM and get response
    # response = send_to_llm(prompt)
    
    # Use enhanced visualization
    # fig = visualizer.create_3d_network_graph(graph_data)
```

### **Step 2: Run Tests**
```bash
# Run comprehensive model tests
python scripts/comprehensive_model_test.py

# Run integration tests
pytest tests/test_missing_components.py -v

# Run all tests
pytest tests/ -v
```

### **Step 3: Update Documentation**
Update your documentation to include the new components:

```markdown
# Enhanced Components

## Dynamic Embedding Selector
Automatically selects the best embedding model based on task type.

## Enhanced Biblical Prompts
Specialized prompts for Biblical forensic analysis.

## Advanced 3D Visualization
Interactive 3D network graphs for analysis visualization.

## Comprehensive Model Testing
Complete testing framework for all models.
```

---

## 🎯 **SUCCESS CRITERIA**

### **Functional Requirements**
- [ ] Dynamic embedding selector operational
- [ ] Enhanced Biblical prompts functional
- [ ] 3D visualization system working
- [ ] Model testing framework complete
- [ ] All integration tests passing

### **Performance Requirements**
- [ ] Dynamic embedding: 50ms response time
- [ ] Model testing: 88.9% success rate
- [ ] 3D visualization: <2s load time
- [ ] No regression in existing functionality

### **Quality Requirements**
- [ ] All components unit tested
- [ ] Code coverage >90%
- [ ] Documentation complete
- [ ] Error handling comprehensive

---

**Status**: Ready for Implementation  
**Estimated Time**: 2-3 weeks  
**Risk Level**: Low (well-documented original code)  
**Next Steps**: Begin with Dynamic Embedding Selector
