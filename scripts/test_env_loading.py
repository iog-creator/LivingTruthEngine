#!/usr/bin/env python3
"""
Test script to verify environment variables are loading correctly
"""

import os
import pathlib
from dotenv import load_dotenv

# Load environment variables from project root
project_root = pathlib.Path(__file__).parent
load_dotenv(project_root / '.env')

print("=== Environment Variables Test ===")
print(f"Project root: {project_root}")
print(f".env file exists: {(project_root / '.env').exists()}")

# Test key environment variables
env_vars = [
    'FLOWISE_API_ENDPOINT',
    'FLOWISE_API_KEY', 
    'FLOWISE_CHATFLOW_ID',
    'LANGCHAIN_API_KEY',
    'SERP_API_KEY'
]

print("\n=== Environment Variables ===")
for var in env_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if 'KEY' in var or 'PASSWORD' in var:
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: Not found")

print("\n=== Test Complete ===") 