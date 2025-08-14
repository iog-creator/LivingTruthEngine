#!/usr/bin/env python3
"""
Verify documentation organization policy.
Important docs must be in root for easy access.
"""

import os
import glob
import sys

def verify_doc_organization():
    """Verify that important documentation is properly organized."""
    print("🔍 Verifying documentation organization...")
    
    # Important docs that MUST be in root
    required_root_docs = [
        'README.md',
        'project_master_log.md',
        'MCP_REQUIREMENTS_REFERENCE.md',
        'SERVICES_MANIFEST.md'
    ]
    
    # Phase completion summaries that MUST be in root
    phase_completion_pattern = 'PHASE_*_COMPLETION_SUMMARY.md'
    
    # Check required docs in root
    missing_root_docs = []
    for doc in required_root_docs:
        if not os.path.exists(doc):
            missing_root_docs.append(doc)
        else:
            print(f"✅ {doc} - in root")
    
    # Check phase completions in root
    phase_completions = glob.glob(phase_completion_pattern)
    if phase_completions:
        for doc in phase_completions:
            print(f"✅ {doc} - in root")
    else:
        print("⚠️  No phase completion summaries found in root")
    
    # Check for important docs misplaced in docs/
    docs_dir = 'docs/'
    misplaced_docs = []
    if os.path.exists(docs_dir):
        for doc in required_root_docs:
            docs_path = os.path.join(docs_dir, doc)
            if os.path.exists(docs_path):
                misplaced_docs.append(docs_path)
        
        # Check for phase completions in docs/
        docs_phase_completions = glob.glob(os.path.join(docs_dir, phase_completion_pattern))
        misplaced_docs.extend(docs_phase_completions)
    
    # Check for important docs misplaced in archive/
    archive_dir = 'archive/docs/'
    misplaced_archive_docs = []
    if os.path.exists(archive_dir):
        for doc in required_root_docs:
            archive_path = os.path.join(archive_dir, doc)
            if os.path.exists(archive_path):
                misplaced_archive_docs.append(archive_path)
        
        # Check for phase completions in archive/
        archive_phase_completions = glob.glob(os.path.join(archive_dir, phase_completion_pattern))
        misplaced_archive_docs.extend(archive_phase_completions)
    
    # Report results
    print("\n📋 Documentation Organization Report:")
    
    if missing_root_docs:
        print(f"❌ Missing required docs in root: {missing_root_docs}")
    
    if misplaced_docs:
        print(f"❌ Important docs misplaced in docs/: {misplaced_docs}")
        print("   → Move these to root directory")
    
    if misplaced_archive_docs:
        print(f"❌ Important docs misplaced in archive/: {misplaced_archive_docs}")
        print("   → Move these to root directory")
    
    if not missing_root_docs and not misplaced_docs and not misplaced_archive_docs:
        print("✅ All important documentation properly organized")
        print("✅ Phase completions in root")
        print("✅ Persistently updated docs in root")
        return True
    else:
        print("\n🚨 Documentation organization violations found!")
        print("   → Move important docs to root directory")
        print("   → Keep reference docs in docs/")
        print("   → Keep historical docs in archive/docs/")
        return False

if __name__ == "__main__":
    success = verify_doc_organization()
    sys.exit(0 if success else 1)
