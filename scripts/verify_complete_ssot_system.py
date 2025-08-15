#!/usr/bin/env python3
"""
Complete SSOT System Validation and Auto-Fix Script

This script combines all SSOT validation tools and automatically fixes common issues:
1. SSOT bundle verification
2. Cursor rules frontmatter validation
3. MCP validation
4. Master log generation (with correct root location)
5. Auto-fix common frontmatter issues

Usage:
  python scripts/verify_complete_ssot_system.py
  python scripts/verify_complete_ssot_system.py --fix  # auto-fix issues
"""
import sys
import subprocess
import pathlib
import re
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
    
    # Auto-fix if requested and there are issues
    if auto_fix and not all([ssot_ok, cursor_ok, mcp_ok, master_ok]):
        print("\n🔧 Applying auto-fixes...")
        auto_fix_cursor_rules()
        fix_master_log_location()
        
        # Re-run validations after fixes
        print("\n🔄 Re-running validations after fixes...")
        ssot_ok = run_ssot_bundle_verification()
        cursor_ok = run_cursor_rules_validation()
        mcp_ok = run_mcp_validation()
        master_ok = run_master_log_build()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    all_passed = all([ssot_ok, cursor_ok, mcp_ok, master_ok])
    
    print(f"SSOT Bundle:        {'✅ PASS' if ssot_ok else '❌ FAIL'}")
    print(f"Cursor Rules:       {'✅ PASS' if cursor_ok else '❌ FAIL'}")
    print(f"MCP Validation:     {'✅ PASS' if mcp_ok else '❌ FAIL'}")
    print(f"Master Log:         {'✅ PASS' if master_ok else '❌ FAIL'}")
    
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
