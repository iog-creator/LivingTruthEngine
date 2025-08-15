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

Usage:
  python scripts/verify_complete_ssot_system.py
  python scripts/verify_complete_ssot_system.py --fix  # auto-fix issues
"""
import sys
import subprocess
import pathlib
import re
import yaml
from typing import List, Dict, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[1]
ERRORS = []
FIXES_APPLIED = []

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
    for pattern in todo_patterns:
        for file_path in ROOT.rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if re.search(pattern, content, re.IGNORECASE):
                    todo_files.append((file_path, pattern))
            except Exception:
                continue
    
    if todo_files:
        print("  ❌ TODO comments found in code files:")
        for file_path, pattern in todo_files:
            print(f"    - {file_path.relative_to(ROOT)} ({pattern})")
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
    for pattern in silent_patterns:
        for file_path in ROOT.rglob("*.py"):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                if re.search(pattern, content, re.IGNORECASE):
                    silent_files.append((file_path, pattern))
            except Exception:
                continue
    
    if silent_files:
        print("  ❌ Silent fallbacks found:")
        for file_path, pattern in silent_files:
            print(f"    - {file_path.relative_to(ROOT)} ({pattern})")
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
        terminology_check, dependency_check, ssot_ref_check
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
