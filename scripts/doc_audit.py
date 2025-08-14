#!/usr/bin/env python3
"""
Documentation Audit Script for Living Truth Engine

Scans all documentation files and adds missing frontmatter with proper metadata.
Ensures all .md and .mdc files have consistent frontmatter structure.
"""

import os
import re
import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Root directory of the project
ROOT = Path(__file__).parent.parent

# Frontmatter regex pattern
FRONTMATTER_RE = re.compile(r'^---\n.*?^---\n', re.S | re.M)

def get_current_phase() -> str:
    """Determine the current phase from phase files."""
    phase_files = list(ROOT.glob('PHASE_*.md'))
    if not phase_files:
        return "9.5.7"  # Default fallback
    
    # Find the highest phase number
    phases = []
    for file in phase_files:
        match = re.search(r'PHASE_(\d+(?:\.\d+)*)', file.name)
        if match:
            phases.append(match.group(1))
    
    if phases:
        # Sort by version number and return the latest
        phases.sort(key=lambda x: [int(n) for n in x.split('.')])
        return phases[-1]
    
    return "9.5.7"

def determine_file_status(file_path: str) -> str:
    """Determine the status of a documentation file."""
    file_lower = file_path.lower()
    
    # Check for archived or legacy files
    if any(keyword in file_lower for keyword in ['archive', 'legacy', 'deprecated', 'old']):
        return "archived"
    
    # Check for outdated files
    if any(keyword in file_lower for keyword in ['v1', 'v2', 'old_', 'previous']):
        return "outdated"
    
    # Default to active
    return "active"

def determine_related_files(file_path: str) -> List[str]:
    """Determine related files based on content and location."""
    related = []
    
    try:
        with open(ROOT / file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Look for references to other files
            file_refs = re.findall(r'`([^`]+\.(?:md|py|ts|tsx|json))`', content)
            related.extend(file_refs)
            
            # Look for phase references
            phase_refs = re.findall(r'PHASE_(\d+(?:\.\d+)*)', content)
            for phase in phase_refs:
                related.append(f"PHASE_{phase}.md")
                
    except Exception:
        pass
    
    return list(set(related))  # Remove duplicates

def create_frontmatter(file_path: str, current_phase: str) -> str:
    """Create frontmatter for a documentation file."""
    status = determine_file_status(file_path)
    related_files = determine_related_files(file_path)
    
    frontmatter = f"""---
phase: {current_phase}
status: {status}
last_reviewed: {datetime.date.today()}
related_files: {related_files}
---

"""
    return frontmatter

def ensure_frontmatter(file_path: str) -> Tuple[bool, str]:
    """
    Ensure a file has proper frontmatter.
    
    Returns:
        Tuple of (was_changed, message)
    """
    try:
        with open(ROOT / file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file already has frontmatter
        if FRONTMATTER_RE.match(content):
            # Validate existing frontmatter
            frontmatter_match = FRONTMATTER_RE.match(content)
            frontmatter_content = frontmatter_match.group(0)
            
            # Check if it has required fields
            has_phase = 'phase:' in frontmatter_content
            has_status = 'status:' in frontmatter_content
            has_last_reviewed = 'last_reviewed:' in frontmatter_content
            
            if has_phase and has_status and has_last_reviewed:
                return False, "Frontmatter already complete"
            else:
                # Update existing frontmatter
                current_phase = get_current_phase()
                new_frontmatter = create_frontmatter(file_path, current_phase)
                
                # Replace existing frontmatter
                new_content = FRONTMATTER_RE.sub(new_frontmatter, content, count=1)
                
                with open(ROOT / file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True, "Updated existing frontmatter"
        else:
            # Add new frontmatter
            current_phase = get_current_phase()
            new_frontmatter = create_frontmatter(file_path, current_phase)
            
            with open(ROOT / file_path, 'w', encoding='utf-8') as f:
                f.write(new_frontmatter + content)
            
            return True, "Added new frontmatter"
            
    except Exception as e:
        return False, f"Error processing {file_path}: {e}"

def should_process_file(file_path: str) -> bool:
    """Determine if a file should be processed."""
    # Skip files in archive directories
    if '/archive/' in file_path or '/Archive_Legacy/' in file_path:
        return False
    
    # Skip certain file types
    if file_path.endswith(('.py', '.js', '.ts', '.json', '.yaml', '.yml')):
        return False
    
    # Only process markdown files
    return file_path.endswith(('.md', '.mdc'))

def main():
    """Main function to audit and fix documentation frontmatter."""
    print("📚 Starting documentation audit...")
    
    changed_files = []
    error_files = []
    skipped_files = []
    
    # Walk through all files in the repository
    for root, dirs, files in os.walk(ROOT):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'living_venv']]
        
        for file in files:
            if file.endswith(('.md', '.mdc')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, ROOT)
                
                if should_process_file(rel_path):
                    was_changed, message = ensure_frontmatter(rel_path)
                    
                    if was_changed:
                        changed_files.append((rel_path, message))
                        print(f"✅ {rel_path}: {message}")
                    elif "Error" in message:
                        error_files.append((rel_path, message))
                        print(f"❌ {rel_path}: {message}")
                    else:
                        print(f"ℹ️  {rel_path}: {message}")
                else:
                    skipped_files.append(rel_path)
    
    # Print summary
    print(f"\n📊 Audit Summary:")
    print(f"   - Files changed: {len(changed_files)}")
    print(f"   - Files with errors: {len(error_files)}")
    print(f"   - Files skipped: {len(skipped_files)}")
    
    if changed_files:
        print(f"\n✅ Successfully updated {len(changed_files)} files:")
        for file_path, message in changed_files:
            print(f"   - {file_path}: {message}")
    
    if error_files:
        print(f"\n❌ Errors encountered:")
        for file_path, message in error_files:
            print(f"   - {file_path}: {message}")
    
    # Return results for CI/CD integration
    return {
        "changed_files": len(changed_files),
        "error_files": len(error_files),
        "skipped_files": len(skipped_files),
        "success": len(error_files) == 0
    }

if __name__ == "__main__":
    main()
