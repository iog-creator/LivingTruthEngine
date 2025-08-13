#!/usr/bin/env bash
set -euo pipefail

echo "=== Starting Living Truth Engine UI Development ==="

# Check if we're in the right directory
if [ ! -f "ui/package.json" ]; then
    echo "❌ Error: ui/package.json not found. Make sure you're in the project root."
    exit 1
fi

# Navigate to UI directory
cd ui

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start development server
echo "🚀 Starting Next.js development server..."
echo "   - UI will be available at: http://localhost:3000"
echo "   - API proxy: http://localhost:3000/api/* → http://localhost:8050"
echo "   - Press Ctrl+C to stop"
echo ""

npm run dev
