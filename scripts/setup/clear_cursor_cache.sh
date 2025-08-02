#!/bin/bash

# Clear Cursor cache and force correct environment
# This script helps resolve terminal environment issues

echo "🧹 Clearing Cursor cache and fixing environment..."

# Kill any running Cursor processes
pkill -f "cursor" 2>/dev/null || true

# Clear Cursor's workspace cache (but keep important configs)
echo "📁 Clearing workspace cache..."
rm -rf ~/.config/Cursor/User/workspaceStorage/* 2>/dev/null || true
rm -rf ~/.config/Cursor/User/globalStorage/storage.json 2>/dev/null || true

# Ensure the correct workspace configuration exists
echo "⚙️ Setting up correct workspace configuration..."
mkdir -p ~/.config/Cursor/Workspaces/1753464840539/

cat > ~/.config/Cursor/Workspaces/1753464840539/workspace.json << 'EOF'
{
	"folders": [
		{
			"path": "../../../../Projects/NotebookLM"
		},
		{
			"path": "../../../../Projects/living_truth_agent"
		}
	],
	"settings": {
		"terminal.integrated.env.linux": {
			"PATH": "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/living_venv/bin:/usr/local/bin:/usr/bin:/bin",
			"PYTHONPATH": "/home/mccoy/Projects/NotebookLM/LivingTruthEngine"
		},
		"terminal.integrated.defaultProfile.linux": "bash",
		"terminal.integrated.profiles.linux": {
			"bash": {
				"path": "bash",
				"args": [
					"-c",
					"source /home/mccoy/Projects/NotebookLM/LivingTruthEngine/living_venv/bin/activate && export PYTHONPATH=/home/mccoy/Projects/NotebookLM/LivingTruthEngine && exec bash"
				]
			}
		}
	}
}
EOF

echo "✅ Cursor cache cleared and environment fixed!"
echo "🚀 Now restart Cursor completely:"
echo "   1. Close Cursor completely"
echo "   2. Wait 10 seconds"
echo "   3. Run: ./start_cursor.sh"
echo ""
echo "📁 Or manually start from:"
echo "   cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine"
echo "   cursor ." 