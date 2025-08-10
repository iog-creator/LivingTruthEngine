#!/usr/bin/env python3
"""
Extract Langflow Component Schemas
==================================

Extract predefined component templates from local Langflow code
to ensure accurate JSON flow generation.
"""

import importlib.util
import os
import json
import sys
from pathlib import Path
from typing import Dict, Any

def extract_component_schemas(langflow_path: str) -> Dict[str, Any]:
    """Extract component schemas from local Langflow code."""
    
    schemas = {}
    components_dir = Path(langflow_path) / "src" / "backend" / "base" / "langflow" / "components"
    
    print(f"🔍 Extracting schemas from: {components_dir}")
    
    if not components_dir.exists():
        print(f"❌ Components directory not found: {components_dir}")
        return schemas
    
    # Add langflow path to Python path
    langflow_src = Path(langflow_path) / "src"
    if str(langflow_src) not in sys.path:
        sys.path.insert(0, str(langflow_src))
    
    for file_path in components_dir.glob("*.py"):
        if file_path.name == "__init__.py":
            continue
            
        module_name = file_path.stem
        print(f"📦 Processing module: {module_name}")
        
        try:
            # Import the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for component classes
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                # Check if it's a component class
                if (hasattr(attr, '__class__') and 
                    hasattr(attr, 'display_name') and 
                    hasattr(attr, 'template')):
                    
                    try:
                        # Get the template
                        template = attr.template
                        if template:
                            schemas[module_name] = {
                                "display_name": getattr(attr, 'display_name', module_name),
                                "description": getattr(attr, 'description', ''),
                                "template": template
                            }
                            print(f"  ✅ Found template for {attr_name}")
                    except Exception as e:
                        print(f"  ⚠️  Error extracting template for {attr_name}: {e}")
                        
        except Exception as e:
            print(f"  ❌ Error processing {module_name}: {e}")
    
    return schemas

def extract_specific_components(langflow_path: str) -> Dict[str, Any]:
    """Extract specific components needed for Living Truth Engine flow."""
    
    # Map component names to their actual file paths
    component_paths = {
        "ChatInput": "input_output/chat.py",
        "ChatOutput": "input_output/chat.py", 
        "Agent": "agents/agent.py",
        "LLM": "openai/openai_chat_model.py",
        "Loop": "logic/loop.py",
        "Condition": "logic/conditional_router.py",
        "CustomTool": "agents/mcp_component.py"
    }
    
    schemas = {}
    components_dir = Path(langflow_path) / "src" / "backend" / "base" / "langflow" / "components"
    
    # Add langflow path to Python path
    langflow_src = Path(langflow_path) / "src"
    if str(langflow_src) not in sys.path:
        sys.path.insert(0, str(langflow_src))
    
    for component_name, relative_path in component_paths.items():
        file_path = components_dir / relative_path
        
        if not file_path.exists():
            print(f"⚠️  Component file not found: {file_path}")
            continue
            
        print(f"📦 Processing component: {component_name} from {relative_path}")
        
        try:
            # Import the module
            module_name = relative_path.replace('/', '.').replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for the main component class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                if (hasattr(attr, '__class__') and 
                    hasattr(attr, 'display_name') and 
                    hasattr(attr, 'template')):
                    
                    try:
                        # Get the template
                        template = attr.template
                        if template:
                            schemas[component_name] = {
                                "display_name": getattr(attr, 'display_name', component_name),
                                "description": getattr(attr, 'description', ''),
                                "template": template
                            }
                            print(f"  ✅ Found template for {attr_name}")
                            break
                    except Exception as e:
                        print(f"  ⚠️  Error extracting template for {attr_name}: {e}")
                        
        except Exception as e:
            print(f"  ❌ Error processing {component_name}: {e}")
    
    return schemas

def save_schemas(schemas: Dict[str, Any], output_path: str) -> None:
    """Save extracted schemas to JSON file."""
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(schemas, f, indent=2)
    
    print(f"💾 Saved {len(schemas)} schemas to: {output_file}")

def main():
    """Main function to extract and save schemas."""
    
    print("🚀 Langflow Component Schema Extraction")
    print("=" * 50)
    
    # Langflow path
    langflow_path = "/home/mccoy/Projects/NotebookLM/langflow"
    
    if not Path(langflow_path).exists():
        print(f"❌ Langflow path not found: {langflow_path}")
        print("Please ensure Langflow is cloned to the correct location")
        return
    
    # Extract specific components for Living Truth Engine flow
    print("\n🔍 Extracting specific components...")
    schemas = extract_specific_components(langflow_path)
    
    if not schemas:
        print("❌ No schemas extracted. Trying general extraction...")
        schemas = extract_component_schemas(langflow_path)
    
    if schemas:
        # Save schemas
        output_path = "config/langflow_schemas.json"
        save_schemas(schemas, output_path)
        
        print(f"\n✅ Successfully extracted {len(schemas)} component schemas:")
        for component, data in schemas.items():
            print(f"  - {component}: {data.get('display_name', component)}")
        
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