#!/usr/bin/env python3
"""
Verify service documentation completeness.
Supports both single manifest and per-service docs during transition.
"""

import os
import re
import sys
from pathlib import Path

def check_manifest_mode():
    """Check if we're using the single manifest approach."""
    manifest_path = Path("SERVICES_MANIFEST.md")
    if not manifest_path.exists():
        return False
    
    # Check if manifest has required sections
    content = manifest_path.read_text()
    required_sections = [
        "## Core Services",
        "## Supporting/Optional Services",
        "**Role**:",
        "**Ports**:",
        "**Healthcheck**:"
    ]
    
    for section in required_sections:
        if section not in content:
            return False
    
    return True

def check_per_service_mode():
    """Check if we're using per-service docs approach."""
    services_dir = Path("docs/services")
    if not services_dir.exists():
        return False
    
    # Check for service docs
    service_files = list(services_dir.glob("*.md"))
    if not service_files:
        return False
    
    # Check if they have required sections
    for service_file in service_files:
        content = service_file.read_text()
        required_sections = ["**Role**:", "**Ports**:", "**Healthcheck**:"]
        for section in required_sections:
            if section not in content:
                print(f"❌ {service_file.name}: missing {section}")
                return False
    
    return True

def verify_manifest_completeness():
    """Verify the single manifest has all required information."""
    manifest_path = Path("SERVICES_MANIFEST.md")
    content = manifest_path.read_text()
    
    # Check for core services (numbered format)
    core_services = ["dashboard", "postgres", "mcp‑solver", "redis", "veritas_worker"]
    for service in core_services:
        # Check for numbered format: "### 1) dashboard" or "### 2) postgres"
        pattern = rf'### \d+\) {re.escape(service)}'
        if not re.search(pattern, content):
            print(f"❌ Missing core service: {service}")
            return False
    
    # Check for required sections in each service
    service_blocks = re.findall(r'### \d+\) ([^(]+)', content)
    for service in service_blocks:
        service_name = service.strip()
        # Find the service block
        pattern = rf'### \d+\) {re.escape(service_name)}.*?(?=###|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            continue
        
        service_content = match.group(0)
        required_fields = ["**Role**:", "**Ports**:", "**Healthcheck**:"]
        for field in required_fields:
            if field not in service_content:
                print(f"❌ {service_name}: missing {field}")
                return False
    
    print("✅ Manifest verification passed")
    return True

def main():
    """Main verification logic."""
    print("🔍 Verifying service documentation completeness...")
    
    # Check if we have the manifest
    if check_manifest_mode():
        print("📋 Using single manifest mode")
        if verify_manifest_completeness():
            print("✅ Service documentation verification PASSED")
            return 0
        else:
            print("❌ Service documentation verification FAILED")
            return 1
    
    # Fallback to per-service mode
    elif check_per_service_mode():
        print("📁 Using per-service docs mode")
        if check_per_service_mode():
            print("✅ Service documentation verification PASSED")
            return 0
        else:
            print("❌ Service documentation verification FAILED")
            return 1
    
    else:
        print("❌ No valid service documentation found")
        print("   Expected either:")
        print("   - SERVICES_MANIFEST.md (single manifest)")
        print("   - docs/services/*.md (per-service docs)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
