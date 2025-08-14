#!/usr/bin/env python3
"""
SSOT (Single Source of Truth) Bundle Verification Script

This script verifies that all critical LivingTruthEngine reference files are:
1. Present in the project root directory
2. Have correct frontmatter (for phase completions)
3. Are complete and properly formatted
4. Are not duplicated in docs/ or archive/docs/

Usage:
    python scripts/verify_ssot_bundle.py
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def get_ssot_files() -> List[str]:
    """Define the SSOT bundle files that must be in root."""
    return [
        "README.md",
        "project_master_log.md", 
        "MCP_REQUIREMENTS_REFERENCE.md",
        "SERVICES_MANIFEST.md"
    ]

def get_phase_completion_files() -> List[str]:
    """Get all phase completion summary files."""
    phase_files = []
    for file in project_root.glob("PHASE_*_COMPLETION_SUMMARY.md"):
        phase_files.append(file.name)
    return sorted(phase_files)

def check_file_exists(file_path: Path, file_name: str) -> Tuple[bool, str]:
    """Check if a file exists and is in the correct location."""
    if not file_path.exists():
        return False, f"❌ {file_name} - MISSING from root directory"
    
    if file_path.parent != project_root:
        return False, f"❌ {file_name} - WRONG LOCATION (should be in root, found in {file_path.parent})"
    
    return True, f"✅ {file_name} - in root"

def validate_frontmatter(file_path: Path) -> Tuple[bool, str]:
    """Validate frontmatter in markdown files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has frontmatter
        if not content.startswith('---'):
            return True, "No frontmatter required"
        
        # Extract frontmatter
        lines = content.split('\n')
        if len(lines) < 2 or lines[0] != '---':
            return False, "Invalid frontmatter format"
        
        # Find end of frontmatter
        end_index = -1
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                end_index = i
                break
        
        if end_index == -1:
            return False, "Unclosed frontmatter"
        
        # Parse YAML frontmatter
        frontmatter_text = '\n'.join(lines[1:end_index])
        frontmatter = yaml.safe_load(frontmatter_text)
        
        # Validate required fields for phase completions
        if file_path.name.startswith('PHASE_') and file_path.name.endswith('_COMPLETION_SUMMARY.md'):
            required_fields = ['phase', 'status', 'completion_date', 'depends_on', 'summary']
            missing_fields = [field for field in required_fields if field not in frontmatter]
            
            if missing_fields:
                return False, f"Missing required frontmatter fields: {', '.join(missing_fields)}"
            
            # Validate phase format
            phase = frontmatter.get('phase', '')
            if not isinstance(phase, (int, str)):
                return False, "Invalid phase format in frontmatter"
        
        return True, "Valid frontmatter"
        
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def check_for_duplicates(file_name: str) -> Tuple[bool, str]:
    """Check for duplicate files in docs/ or archive/docs/."""
    docs_path = project_root / "docs" / file_name
    archive_docs_path = project_root / "archive" / "docs" / file_name
    
    duplicates = []
    if docs_path.exists():
        duplicates.append(f"docs/{file_name}")
    if archive_docs_path.exists():
        duplicates.append(f"archive/docs/{file_name}")
    
    if duplicates:
        return False, f"❌ {file_name} - DUPLICATES found in: {', '.join(duplicates)}"
    
    return True, f"✅ {file_name} - No duplicates found"

def validate_services_manifest() -> Tuple[bool, str]:
    """Validate SERVICES_MANIFEST.md for completeness."""
    manifest_path = project_root / "SERVICES_MANIFEST.md"
    
    if not manifest_path.exists():
        return False, "❌ SERVICES_MANIFEST.md - MISSING"
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required sections
        required_sections = [
            "Core Services",
            "Supporting/Optional Services",
            "## Legend"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            return False, f"❌ SERVICES_MANIFEST.md - Missing sections: {', '.join(missing_sections)}"
        
        # Check for service entries
        if "### " not in content:
            return False, "❌ SERVICES_MANIFEST.md - No service entries found"
        
        return True, "✅ SERVICES_MANIFEST.md - Complete and valid"
        
    except Exception as e:
        return False, f"❌ SERVICES_MANIFEST.md - Error reading file: {e}"

def main():
    """Main verification function."""
    print("🔍 Verifying SSOT (Single Source of Truth) Bundle...")
    print(f"📁 Project root: {project_root}")
    print()
    
    all_passed = True
    results = []
    
    # Check SSOT files
    print("📋 Checking SSOT files...")
    ssot_files = get_ssot_files()
    for file_name in ssot_files:
        file_path = project_root / file_name
        
        # Check existence and location
        exists, exists_msg = check_file_exists(file_path, file_name)
        results.append((file_name, exists, exists_msg))
        if not exists:
            all_passed = False
        
        # Check for duplicates
        if exists:
            no_duplicates, dup_msg = check_for_duplicates(file_name)
            results.append((f"{file_name} (duplicates)", no_duplicates, dup_msg))
            if not no_duplicates:
                all_passed = False
        
        # Validate frontmatter
        if exists:
            valid_fm, fm_msg = validate_frontmatter(file_path)
            results.append((f"{file_name} (frontmatter)", valid_fm, fm_msg))
            if not valid_fm:
                all_passed = False
    
    # Special validation for SERVICES_MANIFEST.md
    print("\n🔧 Validating SERVICES_MANIFEST.md...")
    manifest_valid, manifest_msg = validate_services_manifest()
    results.append(("SERVICES_MANIFEST.md (completeness)", manifest_valid, manifest_msg))
    if not manifest_valid:
        all_passed = False
    
    # Check phase completion files
    print("\n📚 Checking phase completion files...")
    phase_files = get_phase_completion_files()
    print(f"Found {len(phase_files)} phase completion files:")
    
    for file_name in phase_files:
        file_path = project_root / file_name
        
        # Check existence and location
        exists, exists_msg = check_file_exists(file_path, file_name)
        results.append((file_name, exists, exists_msg))
        if not exists:
            all_passed = False
        
        # Check for duplicates
        if exists:
            no_duplicates, dup_msg = check_for_duplicates(file_name)
            results.append((f"{file_name} (duplicates)", no_duplicates, dup_msg))
            if not no_duplicates:
                all_passed = False
        
        # Validate frontmatter
        if exists:
            valid_fm, fm_msg = validate_frontmatter(file_path)
            results.append((f"{file_name} (frontmatter)", valid_fm, fm_msg))
            if not valid_fm:
                all_passed = False
    
    # Print results
    print("\n📊 SSOT Bundle Verification Results:")
    print("=" * 60)
    
    for item_name, passed, message in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {message}")
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 SSOT Bundle Verification: ✅ PASSED")
        print("✅ All SSOT files present and valid")
        print("✅ No duplicates found")
        print("✅ All frontmatter valid")
        print("✅ SERVICES_MANIFEST.md complete")
        return 0
    else:
        print("\n💥 SSOT Bundle Verification: ❌ FAILED")
        print("❌ Some SSOT files missing, invalid, or duplicated")
        print("❌ Please fix the issues above before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())
