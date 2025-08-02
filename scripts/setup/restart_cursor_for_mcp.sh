#!/bin/bash

echo "🔄 Restarting Cursor for MCP Server Detection"
echo "=============================================="

# Kill all Cursor processes
echo "📱 Stopping Cursor..."
pkill -f cursor

# Wait a moment
sleep 3

# Check if Cursor is still running
if pgrep -f cursor > /dev/null; then
    echo "⚠️  Cursor processes still running, force killing..."
    pkill -9 -f cursor
    sleep 2
fi

echo "✅ Cursor stopped"

# Verify MCP config is correct
echo ""
echo "🔧 Checking MCP Configuration..."
if [ -f "/home/mccoy/.cursor/mcp.json" ]; then
    echo "✅ MCP config file exists"
    
    # Check if our server is in the config
    if grep -q "cursor-test-server" "/home/mccoy/.cursor/mcp.json"; then
        echo "✅ cursor-test-server found in config"
    else
        echo "❌ cursor-test-server not found in config"
        exit 1
    fi
    
    # Validate JSON
    if python3 -m json.tool "/home/mccoy/.cursor/mcp.json" > /dev/null 2>&1; then
        echo "✅ MCP config JSON is valid"
    else
        echo "❌ MCP config JSON is invalid"
        exit 1
    fi
else
    echo "❌ MCP config file not found"
    exit 1
fi

# Check if our MCP server file exists
echo ""
echo "🔍 Checking MCP Server Files..."
if [ -f "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/cursor_detectable_mcp.py" ]; then
    echo "✅ cursor_detectable_mcp.py exists"
else
    echo "❌ cursor_detectable_mcp.py not found"
    exit 1
fi

if [ -f "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/living_venv/bin/python3" ]; then
    echo "✅ Python executable exists"
else
    echo "❌ Python executable not found"
    exit 1
fi

# Test the MCP server
echo ""
echo "🧪 Testing MCP Server..."
cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine
source living_venv/bin/activate

# Quick test
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | timeout 5 python3 cursor_detectable_mcp.py > /tmp/mcp_test.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ MCP server test successful"
    echo "📄 Server response:"
    cat /tmp/mcp_test.log
else
    echo "❌ MCP server test failed"
    echo "📄 Error output:"
    cat /tmp/mcp_test.log
fi

echo ""
echo "🚀 Starting Cursor..."
echo "   (This will open Cursor in a new window)"

# Start Cursor
nohup /home/mccoy/.local/share/cursor/launch_cursor.sh > /dev/null 2>&1 &

echo ""
echo "⏳ Waiting for Cursor to start..."
sleep 5

echo ""
echo "📋 Next Steps:"
echo "1. Look for Cursor to open"
echo "2. Go to Settings (Ctrl+,)"
echo "3. Look for 'MCP Servers' section"
echo "4. Check if 'cursor-test-server' appears with a green dot"
echo "5. If it appears, try asking: 'Use test_tool with message hello'"
echo ""
echo "🔍 If you don't see the MCP Servers section:"
echo "   - Make sure you're using Cursor version 0.46+"
echo "   - Try Cmd+Shift+J (or Ctrl+Shift+J) to open Cursor settings"
echo ""
echo "📝 Debug Info:"
echo "   - MCP Config: /home/mccoy/.cursor/mcp.json"
echo "   - Server Log: /home/mccoy/Projects/NotebookLM/LivingTruthEngine/logs/cursor_mcp.log"
echo "   - Test Log: /tmp/mcp_test.log"

echo ""
echo "🎯 Expected Result:"
echo "   - Green dot next to 'cursor-test-server'"
echo "   - '1 tool' displayed"
echo "   - Tool 'test_tool' available for use" 