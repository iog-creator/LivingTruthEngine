#!/usr/bin/env python3
"""
Enhanced fix for corrupted Flowise JSON file.
"""

import re
import json
import sys
from pathlib import Path

def fix_flowise_json(input_file: str, output_file: str = None) -> bool:
    """Enhanced fix for corrupted Flowise JSON file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Reading corrupted file: {input_file}")
        print(f"📏 Original size: {len(content)} characters")
        
        # Step 1: Remove HTML entities
        content = content.replace('&nbsp;', ' ')
        
        # Step 2: Fix line breaks and whitespace
        content = re.sub(r'\n\s*\n', '\n', content)  # Remove empty lines
        content = re.sub(r'[ \t]+', ' ', content)    # Normalize whitespace
        
        # Step 3: Find the actual JSON content
        # Look for the start of JSON structure
        json_start = content.find('{')
        if json_start == -1:
            print("❌ No JSON structure found")
            return False
        
        # Look for the end of JSON structure
        brace_count = 0
        json_end = -1
        for i, char in enumerate(content[json_start:], json_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break
        
        if json_end == -1:
            print("❌ Could not find end of JSON structure")
            return False
        
        # Extract the JSON content
        json_content = content[json_start:json_end]
        print(f"🔍 Extracted JSON content: {len(json_content)} characters")
        
        # Step 4: Clean up the JSON content
        # Remove trailing commas
        json_content = re.sub(r',(\s*[}\]])', r'\1', json_content)
        
        # Fix common syntax issues
        json_content = re.sub(r'}\s*,(\s*[}\]])', r'}\1', json_content)
        json_content = re.sub(r']\s*,(\s*[}\]])', r']\1', json_content)
        
        # Step 5: Try to parse and format
        try:
            parsed_json = json.loads(json_content)
            cleaned_content = json.dumps(parsed_json, indent=2, ensure_ascii=False)
            
            # Determine output file
            if output_file is None:
                input_path = Path(input_file)
                output_file = str(input_path.parent / f"{input_path.stem}_fixed{input_path.suffix}")
            
            # Write the cleaned file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✅ Successfully cleaned JSON file")
            print(f"�� Output saved to: {output_file}")
            print(f"📏 Cleaned size: {len(cleaned_content)} characters")
            
            # Validate
            json.loads(cleaned_content)
            print("✅ JSON validation passed")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("🔧 Attempting to show the problematic area...")
            
            # Show the area around the error
            error_pos = e.pos
            start = max(0, error_pos - 100)
            end = min(len(json_content), error_pos + 100)
            print(f"Error around position {error_pos}:")
            print(json_content[start:end])
            return False
            
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python fix_flowise_json_v2.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(input_file).exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    success = fix_flowise_json(input_file, output_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
