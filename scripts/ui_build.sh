#!/usr/bin/env bash
set -euo pipefail

echo "=== Building Living Truth Engine UI ==="

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

# Build the application
echo "🔨 Building Next.js application..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo "   - Static files are in: ui/.next"
    echo "   - To start production server: npm start"
    echo "   - To preview build: npm run preview"
else
    echo "❌ Build failed!"
    exit 1
fi
