#!/usr/bin/env python3
"""
Complete SSOT System Validation and Auto-Fix Script

This script combines all SSOT validation tools and automatically fixes common issues:
1. SSOT bundle verification
2. Cursor rules frontmatter validation
3. MCP validation
4. Master log generation (with correct root location)
5. Auto-fix common frontmatter issues
6. Proactive detection of common project issues
7. Semantic documentation analysis and consolidation
8. AI-powered analysis and intelligent suggestions

Usage:
  python scripts/verify_complete_ssot_system.py
  python scripts/verify_complete_ssot_system.py --fix  # auto-fix issues
  python scripts/verify_complete_ssot_system.py --ai   # enable AI analysis
"""
import sys
import subprocess
import pathlib
import re
import yaml
import difflib
import requests
import json
from typing import List, Dict, Tuple, Set, Optional
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
ERRORS = []
FIXES_APPLIED = []
AI_ANALYSIS_ENABLED = "--ai" in sys.argv

class LMStudioAIAnalyzer:
    """AI-powered analysis using LM Studio for intelligent SSOT validation"""
    
    def __init__(self):
        self.lm_studio_url = "http://localhost:1234/v1"
        self.model = "llama-3.2-3b-instruct"  # Better for structured output
        self.temperature = 0.1
        self.max_tokens = 100  # Smaller token limit for faster responses
        
        # Test LM Studio connection
        self._test_connection()
    
    def _test_connection(self):
        """Test LM Studio connection"""
        try:
            response = requests.get(f"{self.lm_studio_url}/models", timeout=5)
            if response.status_code == 200:
                models = response.json()
                print(f"🤖 AI Analysis: LM Studio connected. Available models: {len(models.get('data', []))}")
                return True
            else:
                print(f"⚠️ AI Analysis: LM Studio responded with status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ AI Analysis: LM Studio connection failed: {e}")
            return False
    
    def _is_available(self):
        """Check if AI analysis is available"""
        return self._test_connection()
    
    def quick_analyze_todo(self, todo_content: str, file_path: str) -> Dict[str, any]:
        """Quick AI analysis of TODO comments"""
        if not self._is_available():
            return {"error": "LM Studio not available"}
        
        # Extract just the TODO line, limit to 200 chars
        todo_line = todo_content[:200]
        
        prompt = f"TODO: {todo_line}\nFile: {file_path}\nRespond ONLY with JSON: {{\"task_type\": \"bug|feature|improvement\", \"priority\": \"high|medium|low\", \"effort\": \"low|medium|high\"}}"
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a JSON-only responder. Never explain, only provide valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 100
            }
            
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json=payload,
                timeout=15  # Shorter timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                try:
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                    else:
                        return {"error": "Could not parse response", "raw": content[:100]}
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON", "raw": content[:100]}
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)[:50]}"}
    
    def quick_analyze_error_handling(self, code_snippet: str, file_path: str) -> Dict[str, any]:
        """Quick AI analysis of error handling"""
        if not self._is_available():
            return {"error": "LM Studio not available"}
        
        # Limit code snippet to 300 chars
        code_preview = code_snippet[:300]
        
        prompt = f"Code: {code_preview}\nFile: {file_path}\nRespond ONLY with JSON: {{\"issues\": [\"top issue\"], \"priority\": \"high|medium|low\"}}"
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a JSON-only responder. Never explain, only provide valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 100
            }
            
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                try:
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                    else:
                        return {"error": "Could not parse response", "raw": content[:100]}
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON", "raw": content[:100]}
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)[:50]}"}
    
    def quick_analyze_documentation(self, content: str, file_path: str) -> Dict[str, any]:
        """Quick AI analysis of documentation quality"""
        if not self._is_available():
            return {"error": "LM Studio not available"}
        
        # Limit content to 400 chars
        content_preview = content[:400]
        
        prompt = f"Doc: {content_preview}\nFile: {file_path}\nRespond ONLY with JSON: {{\"quality_score\": 0-100, \"main_issue\": \"top issue\", \"priority\": \"high|medium|low\"}}"
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a JSON-only responder. Never explain, only provide valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 100
            }
            
            response = requests.post(
                f"{self.lm_studio_url}/chat/completions",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                try:
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                    else:
                        return {"error": "Could not parse response", "raw": content[:100]}
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON", "raw": content[:100]}
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)[:50]}"}

# Initialize AI analyzer
ai_analyzer = None
if AI_ANALYSIS_ENABLED:
    print("🤖 Initializing AI analysis capabilities...")
    try:
        ai_analyzer = LMStudioAIAnalyzer()
        print("✅ AI analysis initialized successfully")
    except Exception as e:
        print(f"⚠️ AI analysis initialization failed: {e}")
        print("   Continuing with standard validation only")
        ai_analyzer = None

def run_cmd(cmd: str, description: str) -> Tuple[bool, str]:
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ROOT)
        success = result.returncode == 0
        output = result.stdout.strip()
        if result.stderr:
            output += f"\nSTDERR: {result.stderr.strip()}"
        return success, output
    except Exception as e:
        return False, f"Command failed: {e}"

def extract_keywords_from_text(text: str) -> Set[str]:
    """Extract meaningful keywords from text for semantic analysis"""
    # Remove common words and punctuation
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs'
    }
    
    # Extract words, convert to lowercase, filter out stop words and short words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    keywords = {word for word in words if word not in stop_words and len(word) > 2}
    
    return keywords

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using keyword overlap"""
    keywords1 = extract_keywords_from_text(text1)
    keywords2 = extract_keywords_from_text(text2)
    
    if not keywords1 or not keywords2:
        return 0.0
    
    intersection = keywords1.intersection(keywords2)
    union = keywords1.union(keywords2)
    
    return len(intersection) / len(union) if union else 0.0

def check_for_semantic_documentation_duplicates():
    """Check for semantically similar documentation that should be consolidated"""
    print("🔍 Checking for semantic documentation duplicates...")
    
    # Collect all documentation files
    doc_files = []
    for pattern in ["*.md", "*.rst", "*.txt"]:
        for file_path in ROOT.rglob(pattern):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            if file_path.is_file():
                doc_files.append(file_path)
    
    # Read and analyze content
    file_contents = {}
    for file_path in doc_files:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            # Skip very short files
            if len(content.strip()) < 100:
                continue
            file_contents[file_path] = content
        except Exception:
            continue
    
    # Find similar documents
    similar_groups = []
    processed = set()
    
    for file1, content1 in file_contents.items():
        if file1 in processed:
            continue
            
        similar_files = [file1]
        processed.add(file1)
        
        for file2, content2 in file_contents.items():
            if file2 in processed:
                continue
                
            similarity = calculate_similarity(content1, content2)
            if similarity > 0.6:  # High similarity threshold
                similar_files.append(file2)
                processed.add(file2)
        
        if len(similar_files) > 1:
            similar_groups.append(similar_files)
    
    if similar_groups:
        print("  ❌ Semantically similar documentation found:")
        for group in similar_groups:
            print(f"    Similar group ({len(group)} files):")
            for file_path in group:
                print(f"      - {file_path.relative_to(ROOT)}")
        ERRORS.append(f"Found {len(similar_groups)} groups of semantically similar documentation - consider consolidation")
        return False
    
    print("  ✅ No semantic documentation duplicates detected")
    return True

def check_for_topic_scattered_documentation():
    """Check if documentation about the same topic is scattered across multiple files"""
    print("🔍 Checking for scattered topic documentation...")
    
    # Define common topics and their keywords
    topics = {
        "SSOT": ["ssot", "single source of truth", "documentation", "reference", "authoritative"],
        "MCP": ["mcp", "master control program", "server", "validation", "tools"],
        "Phase Management": ["phase", "completion", "summary", "status", "depends"],
        "Testing": ["test", "pytest", "validation", "verify", "check"],
        "Docker": ["docker", "container", "compose", "deployment", "build"],
        "API": ["api", "endpoint", "rest", "json", "response"],
        "UI": ["ui", "dashboard", "frontend", "react", "component"],
        "Analysis": ["analysis", "corpus", "processing", "pipeline", "workflow"],
        "Configuration": ["config", "settings", "environment", "parameters"],
        "Documentation": ["docs", "readme", "guide", "manual", "tutorial"]
    }
    
    topic_files = defaultdict(list)
    
    for topic, keywords in topics.items():
        for file_path in ROOT.rglob("*.md"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
                # Count keyword matches
                matches = sum(1 for keyword in keywords if keyword in content)
                if matches >= 2:  # At least 2 keywords match
                    topic_files[topic].append((file_path, matches))
            except Exception:
                continue
    
    scattered_topics = []
    for topic, files in topic_files.items():
        if len(files) > 3:  # More than 3 files covering the same topic
            scattered_topics.append((topic, files))
    
    if scattered_topics:
        print("  ❌ Topic documentation is scattered across multiple files:")
        for topic, files in scattered_topics:
            print(f"    {topic} ({len(files)} files):")
            for file_path, matches in sorted(files, key=lambda x: x[1], reverse=True)[:5]:
                print(f"      - {file_path.relative_to(ROOT)} ({matches} keyword matches)")
        ERRORS.append(f"Found {len(scattered_topics)} topics with scattered documentation - consider consolidation")
        return False
    
    print("  ✅ No scattered topic documentation detected")
    return True

def check_for_outdated_documentation_references():
    """Check for documentation that references outdated or moved files"""
    print("🔍 Checking for outdated documentation references...")
    
    # Collect all markdown files
    md_files = list(ROOT.rglob("*.md"))
    
    outdated_refs = []
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            
            # Look for file references
            file_refs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)  # Markdown links
            file_refs.extend(re.findall(r'`([^`]+\.(?:md|py|json|yml|yaml))`', content))  # Code blocks
            
            for ref_text, ref_path in file_refs:
                if ref_path.startswith('http'):
                    continue  # Skip external links
                    
                # Resolve relative paths
                if ref_path.startswith('./'):
                    ref_path = ref_path[2:]
                elif ref_path.startswith('../'):
                    ref_path = ref_path[3:]
                
                # Check if file exists
                ref_file = md_file.parent / ref_path
                if not ref_file.exists():
                    outdated_refs.append((md_file, ref_path, ref_text))
            
            # Also check for code block references
            for ref_path in file_refs:
                if isinstance(ref_path, str) and '.' in ref_path:
                    ref_file = md_file.parent / ref_path
                    if not ref_file.exists():
                        outdated_refs.append((md_file, ref_path, "code reference"))
                        
        except Exception:
            continue
    
    if outdated_refs:
        print("  ❌ Outdated documentation references found:")
        for md_file, ref_path, ref_text in outdated_refs[:10]:  # Limit output
            print(f"    - {md_file.relative_to(ROOT)} references missing file: {ref_path}")
        if len(outdated_refs) > 10:
            print(f"    ... and {len(outdated_refs) - 10} more")
        ERRORS.append(f"Found {len(outdated_refs)} outdated documentation references")
        return False
    
    print("  ✅ No outdated documentation references found")
    return True

def check_for_inconsistent_documentation_structure():
    """Check for inconsistent documentation structure and formatting"""
    print("🔍 Checking for inconsistent documentation structure...")
    
    md_files = list(ROOT.rglob("*.md"))
    structure_issues = []
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            # Check for common structure issues
            issues = []
            
            # Check for missing headers
            if not any(line.startswith('#') for line in lines[:10]):
                issues.append("missing main header")
            
            # Check for inconsistent header levels
            header_levels = []
            for line in lines:
                if line.startswith('#'):
                    level = len(line) - len(line.lstrip('#'))
                    header_levels.append(level)
            
            # Check for skipped header levels (e.g., # to ###)
            for i in range(1, len(header_levels)):
                if header_levels[i] > header_levels[i-1] + 1:
                    issues.append("skipped header level")
                    break
            
            # Check for very long lines
            long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 120]
            if long_lines:
                issues.append(f"long lines at {long_lines[:3]}")
            
            # Check for trailing whitespace
            trailing_ws = [i+1 for i, line in enumerate(lines) if line.rstrip() != line and line.strip()]
            if trailing_ws:
                issues.append(f"trailing whitespace at {trailing_ws[:3]}")
            
            if issues:
                structure_issues.append((md_file, issues))
                
        except Exception:
            continue
    
    if structure_issues:
        print("  ❌ Documentation structure issues found:")
        for md_file, issues in structure_issues[:10]:  # Limit output
            print(f"    - {md_file.relative_to(ROOT)}: {', '.join(issues)}")
        if len(structure_issues) > 10:
            print(f"    ... and {len(structure_issues) - 10} more")
        ERRORS.append(f"Found {len(structure_issues)} files with documentation structure issues")
        return False
    
    print("  ✅ No documentation structure issues found")
    return True

def check_for_missing_documentation_sections():
    """Check for missing standard documentation sections"""
    print("🔍 Checking for missing documentation sections...")
    
    # Define standard sections that should be present in certain file types
    required_sections = {
        "README.md": ["overview", "installation", "usage", "contributing"],
        "PHASE_*_COMPLETION_SUMMARY.md": ["status", "completion_date", "summary", "objectives"],
        "SERVICES_MANIFEST.md": ["services", "endpoints", "configuration"],
        "project_master_log.md": ["project", "history", "phases", "status"]
    }
    
    missing_sections = []
    
    for pattern, required in required_sections.items():
        for file_path in ROOT.glob(pattern):
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
                missing = []
                for section in required:
                    if section not in content:
                        missing.append(section)
                
                if missing:
                    missing_sections.append((file_path, missing))
                    
            except Exception:
                continue
    
    if missing_sections:
        print("  ❌ Missing standard documentation sections:")
        for file_path, missing in missing_sections:
            print(f"    - {file_path.relative_to(ROOT)}: missing {', '.join(missing)}")
        
        # AI analysis of documentation quality
        if ai_analyzer and missing_sections:
            print("  🤖 AI Analysis of documentation quality:")
            for file_path, missing in missing_sections[:3]:  # Limit to first 3 for analysis
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    analysis = ai_analyzer.quick_analyze_documentation(content, str(file_path.relative_to(ROOT)))
                    if "error" not in analysis:
                        print(f"    📊 {file_path.relative_to(ROOT)}:")
                        print(f"      Quality Score: {analysis.get('quality_score', 'N/A')}/100")
                        print(f"      Priority: {analysis.get('priority', 'unknown')}")
                        print(f"      Main Issue: {analysis.get('main_issue', 'N/A')}")
                    else:
                        print(f"    ❌ AI analysis failed for {file_path.relative_to(ROOT)}: {analysis.get('error', 'Unknown error')}")
                except Exception as e:
                    print(f"    ❌ Could not analyze {file_path.relative_to(ROOT)}: {e}")
        
        ERRORS.append(f"Found {len(missing_sections)} files missing standard documentation sections")
        return False
    
    print("  ✅ All standard documentation sections present")
    return True

def suggest_documentation_consolidation():
    """Suggest documentation consolidation opportunities"""
    print("🔍 Analyzing documentation consolidation opportunities...")
    
    # Group files by directory and analyze content similarity
    dir_groups = defaultdict(list)
    
    for file_path in ROOT.rglob("*.md"):
        if "venv" in str(file_path) or "__pycache__" in str(file_path):
            continue
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            if len(content.strip()) > 200:  # Only consider substantial files
                dir_groups[file_path.parent].append((file_path, content))
        except Exception:
            continue
    
    consolidation_suggestions = []
    
    for directory, files in dir_groups.items():
        if len(files) > 3:  # Only suggest for directories with multiple files
            # Analyze similarity within directory
            for i, (file1, content1) in enumerate(files):
                for j, (file2, content2) in enumerate(files[i+1:], i+1):
                    similarity = calculate_similarity(content1, content2)
                    if similarity > 0.4:  # Moderate similarity threshold
                        consolidation_suggestions.append((file1, file2, similarity))
    
    if consolidation_suggestions:
        print("  💡 Documentation consolidation suggestions:")
        # Sort by similarity and show top suggestions
        top_suggestions = sorted(consolidation_suggestions, key=lambda x: x[2], reverse=True)[:5]
        for file1, file2, similarity in top_suggestions:
            print(f"    - Consider consolidating:")
            print(f"      {file1.relative_to(ROOT)}")
            print(f"      {file2.relative_to(ROOT)}")
            print(f"      Similarity: {similarity:.2f}")
            print()
        
        # AI-powered consolidation strategy
        if ai_analyzer and top_suggestions:
            print("  🤖 AI-Powered Consolidation Strategy:")
            files_to_analyze = []
            similarity_scores = []
            
            for file1, file2, similarity in top_suggestions[:3]:  # Limit to top 3
                files_to_analyze.append((str(file1.relative_to(ROOT)), str(file2.relative_to(ROOT))))
                similarity_scores.append(similarity)
            
            strategy = ai_analyzer.quick_analyze_documentation(f"Analyze these similar documentation files and suggest an intelligent consolidation strategy. Files to consolidate: {files_to_analyze}. Provide JSON: {{'primary_file': 'path to keep as main file', 'files_to_merge': ['list of files to merge into primary'], 'files_to_archive': ['list of files to move to archive'], 'consolidation_approach': 'description of how to merge content', 'new_structure': 'suggested new file structure', 'priority': 'high|medium|low', 'estimated_effort': 'low|medium|high', 'benefits': ['list of benefits from consolidation']}}", "Consolidation Strategy")
            if "error" not in strategy:
                print(f"    🎯 Primary File: {strategy.get('primary_file', 'N/A')}")
                print(f"    📁 Files to Merge: {', '.join(strategy.get('files_to_merge', [])[:3])}")
                print(f"    📦 Files to Archive: {', '.join(strategy.get('files_to_archive', [])[:3])}")
                print(f"    🔄 Approach: {strategy.get('consolidation_approach', 'N/A')}")
                print(f"    ⚡ Priority: {strategy.get('priority', 'unknown')}")
                print(f"    💪 Estimated Effort: {strategy.get('estimated_effort', 'unknown')}")
                print(f"    ✅ Benefits: {', '.join(strategy.get('benefits', [])[:3])}")
            else:
                print(f"    ❌ AI strategy analysis failed: {strategy.get('error', 'Unknown error')}")
    
    return True

def check_for_todo_comments():
    """Check for TODO comments that should be converted to proper tasks"""
    print("🔍 Checking for TODO comments...")
    
    todo_patterns = [
        r'TODO[:\s]',
        r'FIXME[:\s]',
        r'XXX[:\s]',
        r'HACK[:\s]'
    ]
    
    todo_files = []
    todo_content = []
    
    for pattern in todo_patterns:
        for file_path in ROOT.rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Extract the TODO comment and surrounding context
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 200)
                    context = content[start:end]
                    todo_files.append((file_path, pattern))
                    todo_content.append((str(file_path.relative_to(ROOT)), context))
            except Exception:
                continue
    
    if todo_files:
        print("  ❌ TODO comments found in code files:")
        for file_path, pattern in todo_files:
            print(f"    - {file_path.relative_to(ROOT)} ({pattern})")
        
        # AI analysis of TODO comments
        if ai_analyzer and todo_content:
            print("  🤖 AI Analysis of TODO comments:")
            for i, (file_path, content) in enumerate(todo_content[:2]):  # Limit to first 2 for analysis
                print(f"    🔍 Analyzing {file_path}...")
                try:
                    analysis = ai_analyzer.quick_analyze_todo(content, file_path)
                    if "error" not in analysis:
                        print(f"    📋 {file_path}:")
                        print(f"      Task Type: {analysis.get('task_type', 'unknown')}")
                        print(f"      Priority: {analysis.get('priority', 'unknown')}")
                        print(f"      Estimated Effort: {analysis.get('effort', 'unknown')}")
                    else:
                        print(f"    ❌ AI analysis failed for {file_path}: {analysis.get('error', 'Unknown error')}")
                except Exception as e:
                    print(f"    ❌ AI analysis error for {file_path}: {e}")
                    break  # Stop on first error to avoid hanging
        
        ERRORS.append(f"Found {len(todo_files)} files with TODO comments - convert to proper tasks")
        return False
    
    print("  ✅ No TODO comments found in code files")
    return True

def check_for_silent_fallbacks():
    """Check for silent fallbacks instead of explicit error handling"""
    print("🔍 Checking for silent fallbacks...")
    
    silent_patterns = [
        r'except\s*:',
        r'except\s+Exception\s*:',
        r'except\s+BaseException\s*:',
        r'pass\s*#\s*silent',
        r'return\s+None\s*#\s*fallback'
    ]
    
    silent_files = []
    silent_code_snippets = []
    
    for pattern in silent_patterns:
        for file_path in ROOT.rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Extract the code snippet with context
                    start = max(0, match.start() - 100)
                    end = min(len(content), match.end() + 200)
                    context = content[start:end]
                    silent_files.append((file_path, pattern))
                    silent_code_snippets.append((str(file_path.relative_to(ROOT)), context))
            except Exception:
                continue
    
    if silent_files:
        print("  ❌ Silent fallbacks found:")
        for file_path, pattern in silent_files:
            print(f"    - {file_path.relative_to(ROOT)} ({pattern})")
        
        # AI analysis of silent fallbacks
        if ai_analyzer and silent_code_snippets:
            print("  🤖 AI Analysis of silent fallbacks:")
            for file_path, code_snippet in silent_code_snippets[:3]:  # Limit to first 3 for analysis
                analysis = ai_analyzer.quick_analyze_error_handling(code_snippet, file_path)
                if "error" not in analysis:
                    print(f"    🔧 {file_path}:")
                    print(f"      Priority: {analysis.get('priority', 'unknown')}")
                    print(f"      Issues: {', '.join(analysis.get('issues', [])[:2])}")
                else:
                    print(f"    ❌ AI analysis failed for {file_path}: {analysis.get('error', 'Unknown error')}")
        
        ERRORS.append(f"Found {len(silent_files)} files with silent fallbacks - use explicit error handling")
        return False
    
    print("  ✅ No silent fallbacks found")
    return True

def check_for_missing_tests():
    """Check for new functionality without corresponding tests"""
    print("🔍 Checking for missing tests...")
    
    # Check if new Python files have corresponding test files
    python_files = []
    test_files = []
    
    for file_path in ROOT.rglob("*.py"):
        if "venv" in str(file_path) or "__pycache__" in str(file_path):
            continue
        if "test" in file_path.name.lower():
            test_files.append(file_path)
        elif file_path.parent.name != "tests":
            python_files.append(file_path)
    
    missing_tests = []
    for py_file in python_files:
        if py_file.parent.name == "scripts":
            continue  # Skip scripts directory
        
        # Look for corresponding test file
        test_file = ROOT / "tests" / f"test_{py_file.stem}.py"
        if not test_file.exists():
            missing_tests.append(py_file)
    
    if missing_tests:
        print("  ❌ Missing test files:")
        for file_path in missing_tests[:10]:  # Limit output
            print(f"    - {file_path.relative_to(ROOT)}")
        if len(missing_tests) > 10:
            print(f"    ... and {len(missing_tests) - 10} more")
        ERRORS.append(f"Found {len(missing_tests)} Python files without corresponding tests")
        return False
    
    print("  ✅ All Python files have corresponding tests")
    return True

def check_for_hardcoded_paths():
    """Check for hardcoded paths that might break"""
    print("🔍 Checking for hardcoded paths...")
    
    hardcoded_patterns = [
        r'/home/[^/]+/',
        r'C:\\',
        r'/usr/local/',
        r'/opt/',
        r'\.\./\.\./\.\./'
    ]
    
    hardcoded_files = []
    for pattern in hardcoded_patterns:
        for file_path in ROOT.rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if re.search(pattern, content):
                    hardcoded_files.append((file_path, pattern))
            except Exception:
                continue
    
    if hardcoded_files:
        print("  ❌ Hardcoded paths found:")
        for file_path, pattern in hardcoded_files:
            print(f"    - {file_path.relative_to(ROOT)} ({pattern})")
        ERRORS.append(f"Found {len(hardcoded_files)} files with hardcoded paths")
        return False
    
    print("  ✅ No hardcoded paths found")
    return True

def check_for_inconsistent_terminology():
    """Check for inconsistent terminology across documentation"""
    print("🔍 Checking for inconsistent terminology...")
    
    # Define expected terminology
    expected_terms = {
        "SSOT": ["Single Source of Truth", "SSOT"],
        "Living Truth Engine": ["Living Truth Engine", "LTE"],
        "Phase": ["Phase", "phase"],
        "MCP": ["MCP", "Master Control Program"]
    }
    
    inconsistent_files = []
    for term, variants in expected_terms.items():
        for file_path in ROOT.rglob("*.md"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                found_variants = []
                for variant in variants:
                    if variant in content:
                        found_variants.append(variant)
                
                if len(found_variants) > 1:
                    inconsistent_files.append((file_path, term, found_variants))
            except Exception:
                continue
    
    if inconsistent_files:
        print("  ❌ Inconsistent terminology found:")
        for file_path, term, variants in inconsistent_files[:5]:  # Limit output
            print(f"    - {file_path.relative_to(ROOT)} ({term}: {variants})")
        if len(inconsistent_files) > 5:
            print(f"    ... and {len(inconsistent_files) - 5} more")
        ERRORS.append(f"Found {len(inconsistent_files)} files with inconsistent terminology")
        return False
    
    print("  ✅ Terminology is consistent across documentation")
    return True

def check_for_circular_dependencies():
    """Check for circular dependencies in phase files"""
    print("🔍 Checking for circular dependencies...")
    
    phase_files = list(ROOT.glob("PHASE_*_COMPLETION_SUMMARY.md"))
    dependencies = {}
    
    for phase_file in phase_files:
        try:
            content = phase_file.read_text(encoding='utf-8', errors='ignore')
            # Extract phase number
            phase_match = re.search(r'phase:\s*([^\n]+)', content)
            if phase_match:
                phase = phase_match.group(1).strip()
                
                # Extract dependencies
                deps_match = re.search(r'depends_on:\s*\n((?:\s*-\s*[^\n]+\n?)+)', content)
                if deps_match:
                    deps_text = deps_match.group(1)
                    deps = re.findall(r'-\s*([^\n]+)', deps_text)
                    dependencies[phase] = [dep.strip() for dep in deps]
        except Exception:
            continue
    
    # Check for circular dependencies
    def has_cycle(phase, visited, rec_stack):
        visited.add(phase)
        rec_stack.add(phase)
        
        for dep in dependencies.get(phase, []):
            if dep not in visited:
                if has_cycle(dep, visited, rec_stack):
                    return True
            elif dep in rec_stack:
                return True
        
        rec_stack.remove(phase)
        return False
    
    circular_deps = []
    for phase in dependencies:
        if has_cycle(phase, set(), set()):
            circular_deps.append(phase)
    
    if circular_deps:
        print("  ❌ Circular dependencies found:")
        for phase in circular_deps:
            print(f"    - Phase {phase}")
        ERRORS.append(f"Found {len(circular_deps)} phases with circular dependencies")
        return False
    
    print("  ✅ No circular dependencies found")
    return True

def check_for_missing_ssot_references():
    """Check if important files reference SSOT files"""
    print("🔍 Checking for missing SSOT references...")
    
    ssot_files = ["README.md", "project_master_log.md", "SERVICES_MANIFEST.md"]
    important_files = ["README.md", "docs/*.md", "scripts/*.py"]
    
    missing_refs = []
    for pattern in important_files:
        for file_path in ROOT.glob(pattern):
            if file_path.name in ssot_files:
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                has_ssot_ref = any(ssot_file in content for ssot_file in ssot_files)
                if not has_ssot_ref:
                    missing_refs.append(file_path)
            except Exception:
                continue
    
    if missing_refs:
        print("  ❌ Files missing SSOT references:")
        for file_path in missing_refs[:5]:  # Limit output
            print(f"    - {file_path.relative_to(ROOT)}")
        if len(missing_refs) > 5:
            print(f"    ... and {len(missing_refs) - 5} more")
        ERRORS.append(f"Found {len(missing_refs)} files missing SSOT references")
        return False
    
    print("  ✅ All important files reference SSOT files")
    return True

def fix_cursor_rule_frontmatter(file_path: pathlib.Path) -> bool:
    """Fix common frontmatter issues in cursor rules"""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Check if frontmatter exists and is at the beginning
        if not content.strip().startswith('---'):
            print(f"  ❌ {file_path.name}: No frontmatter found")
            return False
            
        # Check for blank lines before frontmatter
        lines = content.split('\n')
        if lines[0].strip() == '':
            print(f"  🔧 {file_path.name}: Removing blank line before frontmatter")
            lines = [line for line in lines if line.strip() != '' or line != '']
            content = '\n'.join(lines)
            file_path.write_text(content, encoding='utf-8')
            FIXES_APPLIED.append(f"Fixed blank line before frontmatter in {file_path.name}")
            return True
            
        return True
    except Exception as e:
        print(f"  ❌ {file_path.name}: Error fixing frontmatter: {e}")
        return False

def fix_master_log_location():
    """Ensure master log is in root, not docs/"""
    docs_log = ROOT / "docs" / "project_master_log.md"
    root_log = ROOT / "project_master_log.md"
    
    if docs_log.exists() and not root_log.exists():
        print("  🔧 Moving project_master_log.md from docs/ to root/")
        docs_log.rename(root_log)
        FIXES_APPLIED.append("Moved project_master_log.md from docs/ to root/")
    elif docs_log.exists() and root_log.exists():
        print("  🔧 Removing duplicate project_master_log.md from docs/")
        docs_log.unlink()
        FIXES_APPLIED.append("Removed duplicate project_master_log.md from docs/")

def run_ssot_bundle_verification() -> bool:
    """Run SSOT bundle verification"""
    print("🔍 Running SSOT bundle verification...")
    success, output = run_cmd("python scripts/verify_ssot_bundle.py", "SSOT bundle verification")
    print(f"  {'✅' if success else '❌'} {output}")
    if not success:
        ERRORS.append("SSOT bundle verification failed")
    return success

def run_cursor_rules_validation() -> bool:
    """Run cursor rules frontmatter validation"""
    print("🔍 Running cursor rules frontmatter validation...")
    success, output = run_cmd("python scripts/verify_cursor_rules_frontmatter.py", "Cursor rules validation")
    print(f"  {'✅' if success else '❌'} {output}")
    if not success:
        ERRORS.append("Cursor rules frontmatter validation failed")
    return success

def run_mcp_validation() -> bool:
    """Run MCP validation"""
    print("🔍 Running MCP validation...")
    success, output = run_cmd(
        'python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; server = Phase9MCPServer(); result = server.validate_cursor_rules(); print(\'MCP Validation:\', result)"',
        "MCP validation"
    )
    print(f"  {'✅' if success else '❌'} {output}")
    if not success:
        ERRORS.append("MCP validation failed")
    return success

def run_master_log_build() -> bool:
    """Build master log in correct location"""
    print("🔍 Building master log...")
    
    # First, ensure we're building to root, not docs
    fix_master_log_location()
    
    # Run the build script
    success, output = run_cmd("python build_master_log.py", "Master log build")
    print(f"  {'✅' if success else '❌'} {output}")
    
    # Check if it created the file in the right place
    root_log = ROOT / "project_master_log.md"
    if not root_log.exists():
        print("  🔧 Master log not in root, moving from docs/...")
        fix_master_log_location()
        if not root_log.exists():
            ERRORS.append("Master log build failed - file not in root")
            return False
    
    return success

def check_for_duplicate_phase_summaries():
    """Check for duplicate phase completion summaries that should be consolidated"""
    print("🔍 Checking for duplicate phase completion summaries...")
    
    # Look for patterns that suggest duplicates
    phase_files = list(ROOT.glob("PHASE_*_COMPLETION_SUMMARY.md"))
    
    # Group by major phase number
    phase_groups = {}
    for file_path in phase_files:
        # Extract phase number (e.g., "9" from "PHASE_9_5_7_3_COMPLETION_SUMMARY.md")
        match = re.search(r'PHASE_(\d+)', file_path.name)
        if match:
            major_phase = match.group(1)
            if major_phase not in phase_groups:
                phase_groups[major_phase] = []
            phase_groups[major_phase].append(file_path)
    
    # Check for groups with multiple files (potential duplicates)
    duplicates_found = []
    for major_phase, files in phase_groups.items():
        if len(files) > 1:
            duplicates_found.append((major_phase, files))
    
    if duplicates_found:
        print("  ❌ Potential duplicate phase completion summaries found:")
        for major_phase, files in duplicates_found:
            print(f"    Phase {major_phase}: {len(files)} files")
            for file_path in files:
                print(f"      - {file_path.name}")
        ERRORS.append(f"Found {len(duplicates_found)} phase(s) with multiple completion summaries - consolidate into single document")
        return False
    
    print("  ✅ No duplicate phase completion summaries detected")
    return True

def auto_fix_cursor_rules():
    """Auto-fix common cursor rule issues"""
    print("🔧 Auto-fixing cursor rule issues...")
    cursor_rules_dir = ROOT / ".cursor" / "rules"
    
    if not cursor_rules_dir.exists():
        print("  ❌ .cursor/rules directory not found")
        return
        
    for mdc_file in cursor_rules_dir.glob("*.mdc"):
        if not fix_cursor_rule_frontmatter(mdc_file):
            ERRORS.append(f"Failed to fix frontmatter in {mdc_file.name}")

def main():
    """Main validation and fix routine"""
    print("🚀 Complete SSOT System Validation")
    print("=" * 50)
    
    # Check if --fix flag is provided
    auto_fix = "--fix" in sys.argv
    
    # Run all validations
    ssot_ok = run_ssot_bundle_verification()
    cursor_ok = run_cursor_rules_validation()
    mcp_ok = run_mcp_validation()
    master_ok = run_master_log_build()
    duplicate_check = check_for_duplicate_phase_summaries()
    
    # Run proactive checks
    todo_check = check_for_todo_comments()
    fallback_check = check_for_silent_fallbacks()
    test_check = check_for_missing_tests()
    path_check = check_for_hardcoded_paths()
    terminology_check = check_for_inconsistent_terminology()
    dependency_check = check_for_circular_dependencies()
    ssot_ref_check = check_for_missing_ssot_references()
    semantic_doc_check = check_for_semantic_documentation_duplicates()
    topic_scattered_check = check_for_topic_scattered_documentation()
    outdated_refs_check = check_for_outdated_documentation_references()
    structure_check = check_for_inconsistent_documentation_structure()
    missing_sections_check = check_for_missing_documentation_sections()
    
    # Run consolidation suggestions (informational only)
    consolidation_suggestions = suggest_documentation_consolidation()
    
    # Auto-fix if requested and there are issues
    if auto_fix and not all([ssot_ok, cursor_ok, mcp_ok, master_ok, duplicate_check]):
        print("\n🔧 Applying auto-fixes...")
        auto_fix_cursor_rules()
        fix_master_log_location()
        
        # Re-run validations after fixes
        print("\n🔄 Re-running validations after fixes...")
        ssot_ok = run_ssot_bundle_verification()
        cursor_ok = run_cursor_rules_validation()
        mcp_ok = run_mcp_validation()
        master_ok = run_master_log_build()
        duplicate_check = check_for_duplicate_phase_summaries()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    all_passed = all([
        ssot_ok, cursor_ok, mcp_ok, master_ok, duplicate_check,
        todo_check, fallback_check, test_check, path_check,
        terminology_check, dependency_check, ssot_ref_check,
        semantic_doc_check, topic_scattered_check, outdated_refs_check,
        structure_check, missing_sections_check
    ])
    
    print(f"SSOT Bundle:        {'✅ PASS' if ssot_ok else '❌ FAIL'}")
    print(f"Cursor Rules:       {'✅ PASS' if cursor_ok else '❌ FAIL'}")
    print(f"MCP Validation:     {'✅ PASS' if mcp_ok else '❌ FAIL'}")
    print(f"Master Log:         {'✅ PASS' if master_ok else '❌ FAIL'}")
    print(f"Phase Summaries:    {'✅ PASS' if duplicate_check else '❌ FAIL'}")
    print(f"TODO Comments:      {'✅ PASS' if todo_check else '❌ FAIL'}")
    print(f"Silent Fallbacks:   {'✅ PASS' if fallback_check else '❌ FAIL'}")
    print(f"Missing Tests:      {'✅ PASS' if test_check else '❌ FAIL'}")
    print(f"Hardcoded Paths:    {'✅ PASS' if path_check else '❌ FAIL'}")
    print(f"Terminology:        {'✅ PASS' if terminology_check else '❌ FAIL'}")
    print(f"Dependencies:       {'✅ PASS' if dependency_check else '❌ FAIL'}")
    print(f"SSOT References:    {'✅ PASS' if ssot_ref_check else '❌ FAIL'}")
    print(f"Semantic Docs:      {'✅ PASS' if semantic_doc_check else '❌ FAIL'}")
    print(f"Topic Scattered:    {'✅ PASS' if topic_scattered_check else '❌ FAIL'}")
    print(f"Outdated Refs:      {'✅ PASS' if outdated_refs_check else '❌ FAIL'}")
    print(f"Structure Issues:   {'✅ PASS' if structure_check else '❌ FAIL'}")
    print(f"Missing Sections:   {'✅ PASS' if missing_sections_check else '❌ FAIL'}")
    
    if FIXES_APPLIED:
        print(f"\n🔧 Fixes Applied:")
        for fix in FIXES_APPLIED:
            print(f"  - {fix}")
    
    if ERRORS:
        print(f"\n❌ Errors Found:")
        for error in ERRORS:
            print(f"  - {error}")
    
    print(f"\n{'🎉 ALL VALIDATIONS PASSED' if all_passed else '🚨 VALIDATION FAILED'}")
    
    if not all_passed:
        print("\n💡 To auto-fix issues, run: python scripts/verify_complete_ssot_system.py --fix")
        sys.exit(1)
    
    print("\n✅ SSOT system is fully validated and consistent!")

if __name__ == "__main__":
    main()
