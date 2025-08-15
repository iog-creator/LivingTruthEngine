#!/usr/bin/env python3
"""
Test AI Analysis Components Only
"""
import sys
import pathlib

# Add the current directory to path so we can import the AI analyzer
sys.path.append(str(pathlib.Path(__file__).parent))

# Import the AI analyzer class
from verify_complete_ssot_system import LMStudioAIAnalyzer

def test_ai_components():
    """Test just the AI analysis components"""
    print("🚀 Testing AI Analysis Components Only")
    print("=" * 50)
    
    # Initialize AI analyzer
    print("🤖 Initializing AI analyzer...")
    try:
        ai_analyzer = LMStudioAIAnalyzer()
        print("✅ AI analyzer initialized successfully")
    except Exception as e:
        print(f"❌ AI analyzer initialization failed: {e}")
        return
    
    # Test TODO analysis
    print("\n📋 Testing TODO analysis...")
    try:
        todo_content = "TODO: Fix error handling in main.py - need to add proper exception handling"
        result = ai_analyzer.quick_analyze_todo(todo_content, "main.py")
        print(f"✅ TODO analysis result: {result}")
    except Exception as e:
        print(f"❌ TODO analysis failed: {e}")
    
    # Test error handling analysis
    print("\n🔧 Testing error handling analysis...")
    try:
        code_snippet = "try:\n    result = process_data()\nexcept:\n    pass  # silent fallback"
        result = ai_analyzer.quick_analyze_error_handling(code_snippet, "test.py")
        print(f"✅ Error handling analysis result: {result}")
    except Exception as e:
        print(f"❌ Error handling analysis failed: {e}")
    
    # Test documentation analysis
    print("\n📊 Testing documentation analysis...")
    try:
        doc_content = "# Test Documentation\n\nThis is a test document that needs improvement."
        result = ai_analyzer.quick_analyze_documentation(doc_content, "test.md")
        print(f"✅ Documentation analysis result: {result}")
    except Exception as e:
        print(f"❌ Documentation analysis failed: {e}")
    
    print("\n🎉 AI component testing completed!")

if __name__ == "__main__":
    test_ai_components()
