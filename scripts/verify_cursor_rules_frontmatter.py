#!/usr/bin/env python3
"""
Cursor Rules Frontmatter Validation Script

This script validates that all .cursor/rules/*.mdc files have proper frontmatter structure:
- Only one frontmatter section at the top
- No duplicate frontmatter sections
- Valid YAML syntax
"""

import sys
import re
import yaml
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / ".cursor" / "rules"
ERR = []

def validate_single_file(filepath: Path) -> List[str]:
    """Validate a single .mdc file for proper frontmatter structure."""
    errors = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        errors.append(f"Error reading {filepath.name}: {e}")
        return errors
    
    # Count frontmatter sections
    frontmatter_sections = re.findall(r'^---\s*$', content, re.MULTILINE)
    
    if len(frontmatter_sections) == 0:
        # No frontmatter is acceptable for some files
        return errors
    
    if len(frontmatter_sections) < 2:
        errors.append(f"{filepath.name}: Incomplete frontmatter (need opening and closing ---)")
        return errors
    
    if len(frontmatter_sections) > 2:
        errors.append(f"{filepath.name}: Multiple frontmatter sections detected - only one allowed at top")
        return errors
    
    # Check that frontmatter is at the very beginning
    lines = content.split('\n')
    if not lines[0].strip().startswith('---'):
        errors.append(f"{filepath.name}: Frontmatter must be at the very beginning of the file")
        return errors
    
    # Extract and validate YAML frontmatter
    try:
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL)
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        errors.append(f"{filepath.name}: Invalid YAML in frontmatter: {e}")
    except Exception as e:
        errors.append(f"{filepath.name}: Error parsing frontmatter: {e}")
    
    return errors

def main():
    """Main validation function."""
    print("🔍 Validating Cursor Rules Frontmatter...")
    
    # Check if a specific file was provided
    if len(sys.argv) > 1:
        test_file = Path(sys.argv[1])
        if not test_file.exists():
            print(f"❌ Test file not found: {test_file}")
            sys.exit(1)
        mdc_files = [test_file]
        print(f"📋 Testing specific file: {test_file.name}")
    else:
        # Validate all .mdc files in rules directory
        if not RULES_DIR.exists():
            print(f"❌ Rules directory not found: {RULES_DIR}")
            sys.exit(1)
        
        mdc_files = list(RULES_DIR.glob("*.mdc"))
        
        if not mdc_files:
            print("❌ No .mdc files found in rules directory")
            sys.exit(1)
    
    print(f"📋 Found {len(mdc_files)} .mdc files")
    
    # Validate each file
    for filepath in mdc_files:
        print(f"  🔍 Checking {filepath.name}...")
        errors = validate_single_file(filepath)
        
        if errors:
            for error in errors:
                ERR.append(f"{filepath.name}: {error}")
        else:
            print(f"    ✅ {filepath.name} frontmatter valid")
    
    # Report results
    print("\n" + "="*60)
    print("📊 Cursor Rules Frontmatter Validation Results")
    print("="*60)
    
    if ERR:
        print("\n❌ FRONTMATTER VIOLATIONS FOUND:")
        for error in ERR:
            print(f"  {error}")
        print("\n🚨 FRONTMATTER VALIDATION FAILED")
        print("💡 Remember: NEVER add `---` frontmatter sections to existing markdown files!")
        print("💡 Only one frontmatter section allowed at the very top of each file.")
        sys.exit(1)
    else:
        print("\n✅ ALL CURSOR RULES HAVE VALID FRONTMATTER")
        print("✅ No duplicate frontmatter sections detected")
        sys.exit(0)

if __name__ == "__main__":
    main()
