#!/usr/bin/env python3
"""
Repo Inventory Script for Living Truth Engine

Scans the repository to create a comprehensive inventory of:
- Documentation files (.md, .mdc)
- MCP tools and specs
- Docker services
- Log files
- Configuration files

Generates a JSON report for the repo health system.
"""

import os
import json
import datetime
import re
from pathlib import Path
from typing import List, Dict, Any

# Root directory of the project
ROOT = Path(__file__).parent.parent

def list_files(extensions: List[str], exclude_dirs: List[str] = None) -> List[str]:
    """List all files with given extensions, excluding specified directories."""
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', '__pycache__', '.venv', 'living_venv']
    
    files = []
    for root, dirs, files_in_dir in os.walk(ROOT):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files_in_dir:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                # Convert to relative path from project root
                rel_path = os.path.relpath(file_path, ROOT)
                files.append(rel_path)
    
    return sorted(files)

def find_mcp_tools() -> List[Dict[str, Any]]:
    """Find all MCP tools in the codebase."""
    mcp_tools = []
    
    # Look for MCP server files
    mcp_server_files = list_files(['.py'], exclude_dirs=['.git', 'node_modules', '__pycache__', '.venv', 'living_venv'])
    
    for file_path in mcp_server_files:
        if '/mcp_servers/' in file_path or 'mcp' in file_path.lower():
            try:
                with open(ROOT / file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Look for MCP tool decorators
                    tool_matches = re.findall(r'@mcp\.tool\(\)\s*def\s+(\w+)', content)
                    
                    for tool_name in tool_matches:
                        mcp_tools.append({
                            'name': tool_name,
                            'file': file_path,
                            'type': 'mcp_tool'
                        })
                        
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
    
    return mcp_tools

def parse_docker_compose() -> List[Dict[str, Any]]:
    """Parse docker-compose files to find services."""
    services = []
    
    # Look for docker-compose files
    compose_files = [
        'docker/docker-compose.yml',
        'docker/compose.v2.yml',
        'docker/docker-compose.langflow.yml',
        'docker/docker-compose.veritas.yml'
    ]
    
    for compose_file in compose_files:
        file_path = ROOT / compose_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Simple regex to find service names
                    # This is a basic implementation - could be enhanced with proper YAML parsing
                    service_matches = re.findall(r'^\s+(\w+):\s*$', content, re.MULTILINE)
                    
                    for service_name in service_matches:
                        if service_name not in ['version', 'services', 'networks', 'volumes']:
                            services.append({
                                'name': service_name,
                                'compose_file': compose_file,
                                'type': 'docker_service'
                            })
                            
            except Exception as e:
                print(f"Warning: Could not read {compose_file}: {e}")
    
    return services

def check_frontmatter(file_path: str) -> Dict[str, Any]:
    """Check if a markdown file has proper frontmatter."""
    try:
        with open(ROOT / file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for YAML frontmatter
            frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            
            if frontmatter_match:
                frontmatter_content = frontmatter_match.group(1)
                # Basic frontmatter validation
                has_phase = 'phase:' in frontmatter_content
                has_status = 'status:' in frontmatter_content
                has_last_reviewed = 'last_reviewed:' in frontmatter_content
                
                return {
                    'has_frontmatter': True,
                    'has_phase': has_phase,
                    'has_status': has_status,
                    'has_last_reviewed': has_last_reviewed,
                    'complete': has_phase and has_status and has_last_reviewed
                }
            else:
                return {
                    'has_frontmatter': False,
                    'has_phase': False,
                    'has_status': False,
                    'has_last_reviewed': False,
                    'complete': False
                }
                
    except Exception as e:
        return {
            'has_frontmatter': False,
            'error': str(e)
        }

def main():
    """Main function to generate repo inventory."""
    print("🔍 Generating repository inventory...")
    
    # Create inventory structure
    inventory = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "repo_root": str(ROOT),
        "docs": [],
        "mcp_tools": [],
        "docker_services": [],
        "specs": [],
        "configs": [],
        "logs": [],
        "summary": {}
    }
    
    # 1. Documentation files
    print("📚 Scanning documentation...")
    doc_files = list_files(['.md', '.mdc'])
    for doc_file in doc_files:
        frontmatter_status = check_frontmatter(doc_file)
        inventory["docs"].append({
            "file": doc_file,
            "frontmatter": frontmatter_status
        })
    
    # 2. MCP tools
    print("🔧 Scanning MCP tools...")
    inventory["mcp_tools"] = find_mcp_tools()
    
    # 3. Docker services
    print("🐳 Scanning Docker services...")
    inventory["docker_services"] = parse_docker_compose()
    
    # 4. Spec files
    print("📋 Scanning spec files...")
    spec_files = list_files(['.json'])
    for spec_file in spec_files:
        if 'spec' in spec_file.lower() or '/specs/' in spec_file:
            inventory["specs"].append({
                "file": spec_file,
                "type": "mcp_spec" if 'mcp' in spec_file.lower() else "other"
            })
    
    # 5. Configuration files
    print("⚙️ Scanning configuration files...")
    config_files = list_files(['.json', '.toml', '.yaml', '.yml', '.conf', '.ini'])
    for config_file in config_files:
        if any(keyword in config_file.lower() for keyword in ['config', 'conf', 'settings']):
            inventory["configs"].append({
                "file": config_file,
                "type": "configuration"
            })
    
    # 6. Log files
    print("📝 Scanning log files...")
    log_files = list_files(['.log', '.json'])
    for log_file in log_files:
        if '/logs/' in log_file or log_file.endswith('.log'):
            inventory["logs"].append({
                "file": log_file,
                "type": "log"
            })
    
    # Generate summary statistics
    inventory["summary"] = {
        "total_docs": len(inventory["docs"]),
        "docs_with_frontmatter": sum(1 for doc in inventory["docs"] if doc["frontmatter"].get("has_frontmatter", False)),
        "docs_complete_frontmatter": sum(1 for doc in inventory["docs"] if doc["frontmatter"].get("complete", False)),
        "total_mcp_tools": len(inventory["mcp_tools"]),
        "total_docker_services": len(inventory["docker_services"]),
        "total_specs": len(inventory["specs"]),
        "total_configs": len(inventory["configs"]),
        "total_logs": len(inventory["logs"])
    }
    
    # Create output directory
    outdir = ROOT / "logs" / "repo_health"
    outdir.mkdir(parents=True, exist_ok=True)
    
    # Save inventory to file
    outfile = outdir / f"{datetime.date.today()}.json"
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Inventory saved to {outfile}")
    print(f"📊 Summary:")
    print(f"   - Documentation files: {inventory['summary']['total_docs']}")
    print(f"   - Docs with frontmatter: {inventory['summary']['docs_with_frontmatter']}")
    print(f"   - MCP tools: {inventory['summary']['total_mcp_tools']}")
    print(f"   - Docker services: {inventory['summary']['total_docker_services']}")
    print(f"   - Spec files: {inventory['summary']['total_specs']}")
    
    # Return summary for CI/CD integration
    return inventory["summary"]

if __name__ == "__main__":
    main()
