#!/usr/bin/env python3
"""
Simple Langflow Component Schema Extraction
==========================================

Extract component templates by parsing Python files directly
without importing them to avoid dependency issues.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any

def parse_component_file(file_path: Path) -> Dict[str, Any]:
    """Parse a component file to extract template information."""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract class information
    class_match = re.search(r'class\s+(\w+).*?:', content)
    if not class_match:
        return {}
    
    class_name = class_match.group(1)
    
    # Extract display_name
    display_name_match = re.search(r'display_name\s*=\s*["\']([^"\']+)["\']', content)
    display_name = display_name_match.group(1) if display_name_match else class_name
    
    # Extract description
    description_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
    description = description_match.group(1) if description_match else ""
    
    # Extract icon
    icon_match = re.search(r'icon\s*=\s*["\']([^"\']+)["\']', content)
    icon = icon_match.group(1) if icon_match else ""
    
    # Extract inputs section
    inputs_section = re.search(r'inputs\s*=\s*\[(.*?)\]', content, re.DOTALL)
    inputs = []
    
    if inputs_section:
        input_content = inputs_section.group(1)
        # Find all input definitions
        input_matches = re.finditer(r'(\w+Input)\s*\(\s*([^)]+)\)', input_content)
        
        for match in input_matches:
            input_type = match.group(1)
            input_params = match.group(2)
            
            # Parse input parameters
            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', input_params)
            display_name_match = re.search(r'display_name\s*=\s*["\']([^"\']+)["\']', input_params)
            value_match = re.search(r'value\s*=\s*([^,]+)', input_params)
            info_match = re.search(r'info\s*=\s*["\']([^"\']+)["\']', input_params)
            
            input_def = {
                "type": input_type,
                "name": name_match.group(1) if name_match else "",
                "display_name": display_name_match.group(1) if display_name_match else "",
                "value": value_match.group(1).strip() if value_match else "",
                "info": info_match.group(1) if info_match else ""
            }
            inputs.append(input_def)
    
    return {
        "class_name": class_name,
        "display_name": display_name,
        "description": description,
        "icon": icon,
        "inputs": inputs
    }

def extract_component_schemas(langflow_path: str) -> Dict[str, Any]:
    """Extract component schemas from Langflow code."""
    
    schemas = {}
    components_dir = Path(langflow_path) / "src" / "backend" / "base" / "langflow" / "components"
    
    print(f"🔍 Extracting schemas from: {components_dir}")
    
    if not components_dir.exists():
        print(f"❌ Components directory not found: {components_dir}")
        return schemas
    
    # Define target components and their paths
    target_components = {
        "ChatInput": "input_output/chat.py",
        "ChatOutput": "input_output/chat.py",
        "Agent": "agents/agent.py",
        "LLM": "openai/openai_chat_model.py",
        "Loop": "logic/loop.py",
        "Condition": "logic/conditional_router.py",
        "MCPComponent": "agents/mcp_component.py"
    }
    
    for component_name, relative_path in target_components.items():
        file_path = components_dir / relative_path
        
        if not file_path.exists():
            print(f"⚠️  Component file not found: {file_path}")
            continue
            
        print(f"📦 Processing component: {component_name} from {relative_path}")
        
        try:
            component_info = parse_component_file(file_path)
            if component_info:
                schemas[component_name] = component_info
                print(f"  ✅ Extracted {component_name}: {component_info.get('display_name', component_name)}")
            else:
                print(f"  ⚠️  No component info extracted from {component_name}")
                
        except Exception as e:
            print(f"  ❌ Error processing {component_name}: {e}")
    
    return schemas

def create_template_from_schema(component_info: Dict[str, Any]) -> Dict[str, Any]:
    """Create a template structure from component info."""
    
    template = {}
    
    # Add inputs to template
    for input_def in component_info.get("inputs", []):
        input_name = input_def.get("name", "")
        if input_name:
            template[input_name] = {
                "type": "str",  # Default type
                "required": False,
                "default": input_def.get("value", ""),
                "placeholder": input_def.get("info", "")
            }
    
    return template

def save_schemas(schemas: Dict[str, Any], output_path: str) -> None:
    """Save extracted schemas to JSON file."""
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create enhanced schemas with templates
    enhanced_schemas = {}
    for component_name, component_info in schemas.items():
        enhanced_schemas[component_name] = {
            "display_name": component_info.get("display_name", component_name),
            "description": component_info.get("description", ""),
            "icon": component_info.get("icon", ""),
            "template": create_template_from_schema(component_info),
            "inputs": component_info.get("inputs", [])
        }
    
    with open(output_file, 'w') as f:
        json.dump(enhanced_schemas, f, indent=2)
    
    print(f"💾 Saved {len(enhanced_schemas)} schemas to: {output_file}")

def main():
    """Main function to extract and save schemas."""
    
    print("🚀 Simple Langflow Component Schema Extraction")
    print("=" * 50)
    
    # Langflow path
    langflow_path = "/home/mccoy/Projects/NotebookLM/langflow"
    
    if not Path(langflow_path).exists():
        print(f"❌ Langflow path not found: {langflow_path}")
        print("Please ensure Langflow is cloned to the correct location")
        return
    
    # Extract component schemas
    print("\n🔍 Extracting component schemas...")
    schemas = extract_component_schemas(langflow_path)
    
    if schemas:
        # Save schemas
        output_path = "config/langflow_schemas.json"
        save_schemas(schemas, output_path)
        
        print(f"\n✅ Successfully extracted {len(schemas)} component schemas:")
        for component, data in schemas.items():
            print(f"  - {component}: {data.get('display_name', component)}")
            print(f"    Inputs: {len(data.get('inputs', []))}")
        
        print(f"\n📋 Schemas saved to: {output_path}")
        print("🎯 Ready for Living Truth Engine flow generation!")
        
    else:
        print("❌ No schemas could be extracted")
        print("Please check:")
        print("  1. Langflow path is correct")
        print("  2. Langflow code is up to date")
        print("  3. Component files exist")

if __name__ == "__main__":
    main() 