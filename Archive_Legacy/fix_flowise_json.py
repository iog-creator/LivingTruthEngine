#!/usr/bin/env python3
"""
Fix corrupted Flowise JSON file by removing HTML entities and fixing JSON syntax.
"""

import re
import json
import sys
from pathlib import Path

def fix_flowise_json(input_file: str, output_file: str = None) -> bool:
    """
    Fix corrupted Flowise JSON file by removing HTML entities and fixing syntax.
    
    Args:
        input_file: Path to the corrupted JSON file
        output_file: Path for the cleaned JSON file (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the corrupted file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Reading corrupted file: {input_file}")
        print(f"📏 Original size: {len(content)} characters")
        
        # Remove HTML entities
        content = content.replace('&nbsp;', ' ')
        
        # Remove extra whitespace and fix indentation
        content = re.sub(r'\s+', ' ', content)
        
        # Fix common JSON syntax issues
        content = re.sub(r',\s*}', '}', content)  # Remove trailing commas
        content = re.sub(r',\s*]', ']', content)  # Remove trailing commas in arrays
        
        # Try to parse and format the JSON
        try:
            parsed_json = json.loads(content)
            cleaned_content = json.dumps(parsed_json, indent=2, ensure_ascii=False)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("🔧 Attempting manual fixes...")
            
            # Additional manual fixes
            content = re.sub(r'}\s*,\s*$', '}', content)  # Remove trailing comma before closing brace
            content = re.sub(r']\s*,\s*$', ']', content)  # Remove trailing comma before closing bracket
            
            # Try parsing again
            try:
                parsed_json = json.loads(content)
                cleaned_content = json.dumps(parsed_json, indent=2, ensure_ascii=False)
            except json.JSONDecodeError as e2:
                print(f"❌ Manual fixes failed: {e2}")
                return False
        
        # Determine output file
        if output_file is None:
            input_path = Path(input_file)
            output_file = str(input_path.parent / f"{input_path.stem}_fixed{input_path.suffix}")
        
        # Write the cleaned file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"✅ Successfully cleaned JSON file")
        print(f"📁 Output saved to: {output_file}")
        print(f"📏 Cleaned size: {len(cleaned_content)} characters")
        
        # Validate the cleaned JSON
        try:
            json.loads(cleaned_content)
            print("✅ JSON validation passed")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ JSON validation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def main():
    """Main function to fix Flowise JSON file."""
    if len(sys.argv) < 2:
        print("Usage: python fix_flowise_json.py <input_file> [output_file]")
        print("Example: python fix_flowise_json.py LivingTruthFlowise.json")
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
