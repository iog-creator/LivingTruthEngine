#!/usr/bin/env python3
"""
Consolidate Cursor Rules Script

This script copies all MDC rules from .cursor/rules folder into a consolidated file,
excluding archive files. The goal is to organize rules for refactoring and consolidation.
"""

import os
import glob
from pathlib import Path
from datetime import datetime
import re

def get_rule_metadata(content):
    """Extract metadata from MDC rule content."""
    metadata = {}
    
    # Extract title
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    # Extract phase if present
    phase_match = re.search(r'phase:\s*([^\n]+)', content, re.IGNORECASE)
    if phase_match:
        metadata['phase'] = phase_match.group(1).strip()
    
    # Extract scope if present
    scope_match = re.search(r'scope:\s*([^\n]+)', content, re.IGNORECASE)
    if scope_match:
        metadata['scope'] = scope_match.group(1).strip()
    
    # Extract summary if present
    summary_match = re.search(r'summary:\s*([^\n]+)', content, re.IGNORECASE)
    if summary_match:
        metadata['summary'] = summary_match.group(1).strip()
    
    return metadata

def consolidate_cursor_rules():
    """Copy and consolidate all MDC rules from .cursor/rules folder."""
    
    # Define paths
    rules_dir = Path('.cursor/rules')
    output_file = Path('CURSOR_RULES_CONSOLIDATED.md')
    
    # Get all MDC files, excluding archive directory
    mdc_files = []
    for mdc_file in rules_dir.glob('*.mdc'):
        # Skip files in archive directory
        if 'archive' not in str(mdc_file):
            mdc_files.append(mdc_file)
    
    # Sort files for consistent ordering
    mdc_files.sort()
    
    print(f"Found {len(mdc_files)} MDC files to consolidate:")
    for file in mdc_files:
        print(f"  - {file.name}")
    
    # Create consolidated content
    consolidated_content = []
    
    # Header
    consolidated_content.append("# Cursor Rules Consolidated")
    consolidated_content.append("")
    consolidated_content.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    consolidated_content.append(f"**Total Rules:** {len(mdc_files)}")
    consolidated_content.append("")
    consolidated_content.append("## Purpose")
    consolidated_content.append("This file contains all active Cursor rules from `.cursor/rules/` folder,")
    consolidated_content.append("consolidated for refactoring and reorganization purposes.")
    consolidated_content.append("")
    consolidated_content.append("## Rules Index")
    consolidated_content.append("")
    
    # Create index
    for i, mdc_file in enumerate(mdc_files, 1):
        try:
            with open(mdc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                metadata = get_rule_metadata(content)
                
                title = metadata.get('title', mdc_file.stem.replace('_', ' ').title())
                phase = metadata.get('phase', 'N/A')
                scope = metadata.get('scope', 'N/A')
                summary = metadata.get('summary', 'No summary available')
                
                consolidated_content.append(f"{i}. **{title}** (`{mdc_file.name}`)")
                consolidated_content.append(f"   - Phase: {phase}")
                consolidated_content.append(f"   - Scope: {scope}")
                consolidated_content.append(f"   - Summary: {summary}")
                consolidated_content.append("")
        except Exception as e:
            print(f"Error reading {mdc_file}: {e}")
            consolidated_content.append(f"{i}. **{mdc_file.name}** (Error reading file)")
            consolidated_content.append("")
    
    consolidated_content.append("---")
    consolidated_content.append("")
    consolidated_content.append("## Consolidated Rules Content")
    consolidated_content.append("")
    
    # Add each rule's content
    for i, mdc_file in enumerate(mdc_files, 1):
        try:
            with open(mdc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                metadata = get_rule_metadata(content)
                title = metadata.get('title', mdc_file.stem.replace('_', ' ').title())
                
                consolidated_content.append(f"### {i}. {title}")
                consolidated_content.append(f"**File:** `{mdc_file.name}`")
                consolidated_content.append("")
                
                # Add metadata if available
                if metadata:
                    consolidated_content.append("**Metadata:**")
                    for key, value in metadata.items():
                        if key != 'title':
                            consolidated_content.append(f"- {key}: {value}")
                    consolidated_content.append("")
                
                consolidated_content.append("**Content:**")
                consolidated_content.append("```mdc")
                consolidated_content.append(content)
                consolidated_content.append("```")
                consolidated_content.append("")
                consolidated_content.append("---")
                consolidated_content.append("")
                
        except Exception as e:
            print(f"Error processing {mdc_file}: {e}")
            consolidated_content.append(f"### {i}. {mdc_file.name} (Error)")
            consolidated_content.append(f"Error reading file: {e}")
            consolidated_content.append("")
            consolidated_content.append("---")
            consolidated_content.append("")
    
    # Write consolidated file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(consolidated_content))
        
        print(f"\n✅ Successfully created consolidated file: {output_file}")
        print(f"📊 Total rules processed: {len(mdc_files)}")
        print(f"📁 Output file size: {output_file.stat().st_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing consolidated file: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Starting Cursor Rules Consolidation...")
    success = consolidate_cursor_rules()
    
    if success:
        print("\n🎉 Consolidation completed successfully!")
        print("\nNext steps:")
        print("1. Review the consolidated file: CURSOR_RULES_CONSOLIDATED.md")
        print("2. Identify duplicate content and overlapping rules")
        print("3. Plan refactoring to reduce rule count and improve organization")
        print("4. Update README.md to reference the consolidated file")
    else:
        print("\n❌ Consolidation failed!")
        exit(1)
