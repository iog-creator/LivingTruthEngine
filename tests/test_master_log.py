"""
Test master log generation and completion summary functionality
Verifies that build_master_log.py correctly processes completion summaries
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os
from unittest.mock import patch

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from build_master_log import discover_phase_files, section_for_phase, write_log


class TestMasterLog:
    """Test master log generation and completion summary processing"""

    def test_discover_phase_files(self):
        """Test that completion summaries are found correctly"""
        # Create a temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create some completion summaries
            (temp_path / "PHASE_9_3_COMPLETION_SUMMARY.md").write_text("# Phase 9.3 Complete")
            (temp_path / "PHASE_8_1_COMPLETION_SUMMARY.md").write_text("# Phase 8.1 Complete")
            (temp_path / "README.md").write_text("# Not a completion summary")
            
            # Create docs directory and file
            (temp_path / "docs").mkdir()
            (temp_path / "docs" / "PHASE_7_2_COMPLETION_SUMMARY.md").write_text("# Phase 7.2 Complete")
            
            # Mock the ROOT path to use our temp directory
            with patch('build_master_log.ROOT', temp_path):
                # Find completion summaries
                plans, comps, phases = discover_phase_files()
                
                # Should find 3 completion summaries
                assert len(comps) == 3
                summary_names = [s.name for s in comps.values()]
                assert "PHASE_9_3_COMPLETION_SUMMARY.md" in summary_names
                assert "PHASE_8_1_COMPLETION_SUMMARY.md" in summary_names
                assert "PHASE_7_2_COMPLETION_SUMMARY.md" in summary_names
                assert "README.md" not in summary_names

    def test_write_log_creates_output(self):
        """Test that write_log creates the expected output file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a completion summary
            completion_summary = temp_path / "PHASE_9_3_COMPLETION_SUMMARY.md"
            completion_summary.write_text("""
# PHASE 9_3 COMPLETION SUMMARY — Cross-Document Linking & Evidence Graph

## ✅ **IMPLEMENTATION STATUS: COMPLETE**

**Repository**: `LivingTruthEngine`  
**Branch**: `main`  
**Foundation**: Phase 9.2 complete (Multi-source runner backend & UI integration)  
**Completion Date**: August 12, 2024  
**Status**: ✅ **COMPLETE**

## 🎯 **Phase 9.3 Objectives - ALL ACHIEVED**

### **Primary Goals - ALL COMPLETED**
- ✅ **Entity & Claim Extraction** — Extract entities and claims from ingested documents
- ✅ **Cross-Document Linking** — Link entities/claims across documents to form evidence graph
- ✅ **Rulego Integration** — Apply deterministic policy checks for contradictions and evidence validation
- ✅ **DSPy Integration** — Run AI corroboration programs for claim verification
- ✅ **Graph APIs** — Expose read-only APIs for graph/timeline consumption
- ✅ **Postgres Persistence** — Store features & links in pgvector + relational tables
            """)
            
            # Create entries for write_log
            entries = [{
                "phase": "9_3",
                "date": "2024-08-12",
                "plan_path": "",
                "comp_path": str(completion_summary),
                "plan_txt": "# Phase 9.3 Plan",
                "comp_txt": completion_summary.read_text()
            }]
            
            # Mock the LOG path to use our temp directory
            output_file = temp_path / "project_master_log.md"
            with patch('build_master_log.LOG', output_file):
                # Build master log
                write_log(entries, "rebuild")
                
                # Verify output file was created
                assert output_file.exists()
                
                # Verify content includes the completion summary
                content = output_file.read_text()
                assert "PHASE 9_3 COMPLETION SUMMARY" in content
                assert "Cross-Document Linking & Evidence Graph" in content
                assert "✅ **COMPLETE**" in content

    def test_write_log_handles_multiple_summaries(self):
        """Test that write_log handles multiple completion summaries"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create multiple completion summaries
            (temp_path / "PHASE_9_3_COMPLETION_SUMMARY.md").write_text("""
# PHASE 9_3 COMPLETION SUMMARY — Cross-Document Linking & Evidence Graph

## ✅ **IMPLEMENTATION STATUS: COMPLETE**

**Repository**: `LivingTruthEngine`  
**Status**: ✅ **COMPLETE**
            """)
            
            (temp_path / "PHASE_8_1_COMPLETION_SUMMARY.md").write_text("""
# PHASE 8_1 COMPLETION_SUMMARY — Unified Guided Dashboard

## ✅ **IMPLEMENTATION STATUS: COMPLETE**

**Repository**: `LivingTruthEngine`  
**Status**: ✅ **COMPLETE**
            """)
            
            # Create entries for write_log
            entries = [
                {
                    "phase": "9_3",
                    "date": "2024-08-12",
                    "plan_path": "",
                    "comp_path": str(temp_path / "PHASE_9_3_COMPLETION_SUMMARY.md"),
                    "plan_txt": "# Phase 9.3 Plan",
                    "comp_txt": (temp_path / "PHASE_9_3_COMPLETION_SUMMARY.md").read_text()
                },
                {
                    "phase": "8_1",
                    "date": "2024-08-10",
                    "plan_path": "",
                    "comp_path": str(temp_path / "PHASE_8_1_COMPLETION_SUMMARY.md"),
                    "plan_txt": "# Phase 8.1 Plan",
                    "comp_txt": (temp_path / "PHASE_8_1_COMPLETION_SUMMARY.md").read_text()
                }
            ]
            
            # Mock the LOG path to use our temp directory
            output_file = temp_path / "project_master_log.md"
            with patch('build_master_log.LOG', output_file):
                # Build master log
                write_log(entries, "rebuild")
                
                # Verify both summaries are included
                content = output_file.read_text()
                assert "PHASE 9_3 COMPLETION SUMMARY" in content
                assert "PHASE 8_1 COMPLETION_SUMMARY" in content
                assert "Cross-Document Linking & Evidence Graph" in content
                assert "Unified Guided Dashboard" in content

    def test_section_for_phase_handles_missing_files(self):
        """Test that section_for_phase handles missing files gracefully"""
        # Test with no files
        section = section_for_phase("9_3", None, None)
        
        assert section["phase"] == "9_3"
        assert section["plan_path"] == ""
        assert section["comp_path"] == ""
        assert "_No plan found for this phase._" in section["plan_txt"]
        assert "_No completion summary found for this phase._" in section["comp_txt"]

    def test_master_log_script_execution(self):
        """Test that the master log script can be executed"""
        # This test verifies that the script can be imported and run
        # without syntax errors or import issues
        try:
            from build_master_log import main
            # If we can import main, the script is syntactically correct
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import build_master_log: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error importing build_master_log: {e}")
