---
phase: 9
status: active
last_reviewed: 2025-08-14
related_files: ['scripts/comprehensive_model_test.py', 'src/ai/prompt_manager.py', 'src/ai/dynamic_embedding_selector.py']
---

# Quick Implementation Guide
## Critical Missing Components from living_truth_agent

**Priority**: High - Core functionality missing  
**Estimated Time**: 1-2 weeks  
**Risk Level**: Low

---

## 🚨 **CRITICAL MISSING COMPONENTS**

### 1. **Dynamic Embedding Selector** ⭐⭐⭐⭐⭐
**File**: `src/ai/dynamic_embedding_selector.py`

```python
#!/usr/bin/env python3
import logging
import requests
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DynamicEmbeddingSelector:
    def __init__(self):
        self.models = {
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
        
        self.task_model_mapping = {
            "notebook_agent": "qwen3",
            "bible_search": "minilm",
            "general": "qwen3",
            "forensic": "qwen3",
            "survivor_testimony": "qwen3"
        }
    
    def get_model_for_task(self, task_type: str) -> Dict[str, Any]:
        model_key = self.task_model_mapping.get(task_type.lower(), "qwen3")
        return self.models[model_key]
    
    def get_dimension_for_task(self, task_type: str) -> int:
        model_config = self.get_model_for_task(task_type)
        return model_config["dimension"]

# Global instance
embedding_selector = DynamicEmbeddingSelector()
```

### 2. **Enhanced Biblical Prompts** ⭐⭐⭐⭐⭐
**Directory**: `prompts/enhanced_prompts/`

#### **biblical_evidence_extraction.txt**
```text
You are a Biblical forensic analyst specializing in evidence extraction and survivor protection.

TASK: Extract Biblical evidence and abuse patterns from the provided document.

RESPONSE FORMAT: Respond with ONLY valid JSON:

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
```

#### **elite_network_analysis.txt**
```text
You are a Biblical forensic analyst specializing in elite network analysis and justice-seeking.

TASK: Analyze elite networks and their connections to abuse patterns.

RESPONSE FORMAT: Respond with ONLY valid JSON:

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
```

#### **survivor_testimony_analysis.txt**
```text
You are a trauma-informed Biblical forensic analyst specializing in survivor testimony analysis.

TASK: Analyze survivor testimony while protecting privacy and dignity.

RESPONSE FORMAT: Respond with ONLY valid JSON:

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
```

### 3. **Prompt Manager** ⭐⭐⭐⭐
**File**: `src/ai/prompt_manager.py`

```python
#!/usr/bin/env python3
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self, prompts_dir: str = "prompts/enhanced_prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts = {}
        self._load_prompts()
    
    def _load_prompts(self):
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
    
    def get_prompt(self, prompt_type: str, **kwargs) -> str:
        if prompt_type not in self.prompts:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        prompt_template = self.prompts[prompt_type]
        return prompt_template.format(**kwargs)
    
    def validate_json_response(self, response: str) -> Dict[str, Any]:
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in response")
            
            json_str = response[json_start:json_end]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")

# Global instance
prompt_manager = PromptManager()
```

### 4. **Comprehensive Model Testing** ⭐⭐⭐⭐
**File**: `scripts/comprehensive_model_test.py`

```python
#!/usr/bin/env python3
import time
import json
import logging
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

class ComprehensiveModelTester:
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0
    
    def test_lm_studio_connection(self) -> bool:
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
    
    def run_all_tests(self) -> Dict[str, Any]:
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
        
        # Test 4: Qwen3 LLM
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
            "success_rate": f"{success_rate:.1f}%",
            "duration": f"{duration:.2f}s",
            "results": self.results
        }
        
        logger.info(f"✅ Testing complete: {self.passed_count}/{self.test_count} passed ({success_rate:.1f}%)")
        return summary

def main():
    tester = ComprehensiveModelTester()
    results = tester.run_all_tests()
    
    print("\n" + "="*50)
    print("COMPREHENSIVE MODEL TEST RESULTS")
    print("="*50)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Success Rate: {results['success_rate']}")
    print(f"Duration: {results['duration']}")
    
    # Save results
    output_file = Path("logs/comprehensive_model_test_results.json")
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
```

---

## 🔧 **IMPLEMENTATION STEPS**

### **Step 1: Create Files**
```bash
# Create directories
mkdir -p src/ai
mkdir -p prompts/enhanced_prompts
mkdir -p scripts

# Create files
touch src/ai/dynamic_embedding_selector.py
touch src/ai/prompt_manager.py
touch prompts/enhanced_prompts/biblical_evidence_extraction.txt
touch prompts/enhanced_prompts/elite_network_analysis.txt
touch prompts/enhanced_prompts/survivor_testimony_analysis.txt
touch scripts/comprehensive_model_test.py
```

### **Step 2: Copy Code**
Copy the code templates above into the respective files.

### **Step 3: Test Components**
```bash
# Test dynamic embedding selector
python -c "from src.ai.dynamic_embedding_selector import embedding_selector; print('✅ Dynamic embedding selector working')"

# Test prompt manager
python -c "from src.ai.prompt_manager import prompt_manager; print('✅ Prompt manager working')"

# Test comprehensive model testing
python scripts/comprehensive_model_test.py
```

### **Step 4: Integrate with Existing Code**
Add to your main application:

```python
# Import new components
from src.ai.dynamic_embedding_selector import get_embedding_model, get_embedding_dimension
from src.ai.prompt_manager import prompt_manager

# Use in your analysis
def analyze_document(document: str, task_type: str = "general"):
    # Get appropriate embedding model
    model_config = get_embedding_model(task_type)
    dimension = get_embedding_dimension(task_type)
    
    # Get appropriate prompt
    if task_type == "biblical_evidence":
        prompt = prompt_manager.get_prompt("biblical_evidence", document=document)
    elif task_type == "elite_network":
        prompt = prompt_manager.get_prompt("elite_network", network_data=document)
    elif task_type == "survivor_testimony":
        prompt = prompt_manager.get_prompt("survivor_testimony", testimony=document)
    
    # Send to LLM and process response
    # response = send_to_llm(prompt)
    # result = prompt_manager.validate_json_response(response)
    
    return {"model_config": model_config, "dimension": dimension, "prompt": prompt}
```

---

## ✅ **SUCCESS CRITERIA**

### **Functional Requirements**
- [ ] Dynamic embedding selector operational
- [ ] Enhanced Biblical prompts functional
- [ ] Prompt manager working
- [ ] Model testing framework complete
- [ ] All components integrated

### **Performance Requirements**
- [ ] Dynamic embedding: 50ms response time
- [ ] Model testing: 88.9% success rate
- [ ] No regression in existing functionality

### **Quality Requirements**
- [ ] All components tested
- [ ] Error handling comprehensive
- [ ] Documentation updated

---

**Status**: Ready for Implementation  
**Estimated Time**: 1-2 weeks  
**Risk Level**: Low  
**Next Steps**: Begin with Dynamic Embedding Selector
