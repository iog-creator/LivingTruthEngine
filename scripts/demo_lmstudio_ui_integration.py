#!/usr/bin/env python3
"""
Demo: How to see LM Studio inference in developer logs
"""
import json

def main():
    print("🎬 LM Studio Developer Logs Demo")
    print("=" * 50)
    
    print("📋 To see LM Studio inference in developer logs:")
    print()
    print("1. Start the tools bridge:")
    print("   make lm-tools")
    print()
    print("2. In LM Studio UI, send this exact message:")
    print("   'Can you verify the SSOT status of the project?'")
    print()
    print("3. LM Studio should call the tools and you'll see:")
    print("   - Inference happening in developer logs")
    print("   - Tool calls in the bridge logs")
    print()
    print("🔧 If LM Studio doesn't call tools automatically,")
    print("   you need to configure it to use the tools.")
    print()
    print("📋 LM Studio Configuration Options:")
    print("   Option A: Use OpenAI-compatible client")
    print("   Option B: Configure LM Studio UI settings")
    print("   Option C: Use MCP connection")
    print()
    print("💡 The test script I ran earlier was direct HTTP,")
    print("   not through the LM Studio UI, so no developer logs.")
    print()
    print("🎯 Try asking LM Studio directly in the UI:")
    print("   'Can you verify the SSOT status of the project?'")

if __name__ == "__main__":
    main()
