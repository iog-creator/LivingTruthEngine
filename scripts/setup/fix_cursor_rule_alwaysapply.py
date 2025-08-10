#!/usr/bin/env python3
"""
Fix cursor rule alwaysApply settings based on best practices.

This script sets alwaysApply: true only for critical project-wide rules
and sets alwaysApply: false for context-specific rules.
"""

import yaml
import re
from pathlib import Path

# Rules that should ALWAYS apply (critical project-wide)
ALWAYS_APPLY_RULES = {
    'coding_standards.mdc',  # Core coding standards
    'project_overview.mdc',  # Project architecture
    'current_working_state.mdc',  # Current system status
}

# Rules that should use globs (file-specific)
GLOB_RULES = {
    'docker_best_practices.mdc': ['**/docker/**', '**/Dockerfile*', '**/docker-compose*'],
    'docker_health_checks.mdc': ['**/docker/**', '**/Dockerfile*', '**/docker-compose*'],
    'mcp_server_integration.mdc': ['**/mcp*.py', '**/mcp*.json', '**/src/mcp_servers/**'],
    'mcp_hub_server.mdc': ['**/mcp*.py', '**/mcp*.json', '**/src/mcp_servers/**'],
    'mcp_hub_server_status.mdc': ['**/mcp*.py', '**/mcp*.json', '**/src/mcp_servers/**'],
    'development_workflow.mdc': ['**/*.py', '**/scripts/**', '**/tests/**'],
    'system_management.mdc': ['**/scripts/**', '**/setup/**', '**/deployment/**'],
    'error_handling_and_testing.mdc': ['**/*.py', '**/tests/**'],
    'analysis_batching.mdc': ['**/scripts/analyze/**', '**/src/analysis/**'],
    'automated_development_management.mdc': ['**/*.py', '**/scripts/**'],
    'living_truth_agent_integration.mdc': ['**/src/analysis/**', '**/src/integration/**'],
    'migrated_functionality.mdc': ['**/src/**', '**/docs/**'],
    'cursor_apparmor_fix.mdc': ['**/scripts/setup/**', '**/docs/**'],
}

def fix_cursor_rule_frontmatter(filename: str) -> bool:
    """Fix the frontmatter for a specific cursor rule file."""
    filepath = Path(f".cursor/rules/{filename}")
    if not filepath.exists():
        print(f"❌ File {filename} not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter and content
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not frontmatter_match:
        print(f"❌ {filename}: No valid frontmatter found")
        return False
    
    frontmatter_text = frontmatter_match.group(1)
    main_content = frontmatter_match.group(2)
    
    try:
        # Parse existing frontmatter
        frontmatter = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as e:
        print(f"❌ {filename}: Invalid YAML in frontmatter: {e}")
        return False
    
    # Determine the correct alwaysApply setting
    if filename in ALWAYS_APPLY_RULES:
        frontmatter['alwaysApply'] = True
        if 'globs' in frontmatter:
            del frontmatter['globs']  # Remove globs for always-apply rules
    elif filename in GLOB_RULES:
        frontmatter['alwaysApply'] = False
        frontmatter['globs'] = GLOB_RULES[filename]
    else:
        # Default: set to false, no globs (manual reference only)
        frontmatter['alwaysApply'] = False
        if 'globs' in frontmatter:
            del frontmatter['globs']
    
    # Ensure required fields are present
    if 'description' not in frontmatter:
        frontmatter['description'] = f"Rule for {filename.replace('.mdc', '')}"
    
    # Reconstruct the file
    new_frontmatter = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{new_frontmatter}---\n\n{main_content}"
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Fixed {filename}: alwaysApply={frontmatter['alwaysApply']}")
    return True

def main():
    """Fix all cursor rule frontmatter."""
    rules_dir = Path(".cursor/rules")
    if not rules_dir.exists():
        print("❌ .cursor/rules directory not found")
        return
    
    mdc_files = list(rules_dir.glob("*.mdc"))
    if not mdc_files:
        print("❌ No .mdc files found in .cursor/rules/")
        return
    
    print(f"🔧 Fixing alwaysApply settings for {len(mdc_files)} cursor rules...")
    print()
    
    success_count = 0
    for mdc_file in mdc_files:
        if fix_cursor_rule_frontmatter(mdc_file.name):
            success_count += 1
    
    print()
    print(f"✅ Fixed {success_count}/{len(mdc_files)} cursor rules")
    print()
    print("📋 Summary of alwaysApply settings:")
    print("   Always Apply (alwaysApply: true):")
    for rule in sorted(ALWAYS_APPLY_RULES):
        print(f"   - {rule}")
    print()
    print("   File-Specific (alwaysApply: false, with globs):")
    for rule in sorted(GLOB_RULES.keys()):
        print(f"   - {rule}")
    print()
    print("   Manual Reference (alwaysApply: false, no globs):")
    manual_rules = [f.name for f in mdc_files if f.name not in ALWAYS_APPLY_RULES and f.name not in GLOB_RULES]
    for rule in sorted(manual_rules):
        print(f"   - {rule}")

if __name__ == "__main__":
    main()
