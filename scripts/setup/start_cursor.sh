#!/bin/bash

# Start Cursor with correct Living Truth Engine environment
# This ensures Cursor uses the right virtual environment and project structure

echo "🚀 Starting Cursor with Living Truth Engine environment..."

# Ensure we're in the right directory
cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine

# Activate the correct virtual environment
source living_venv/bin/activate

# Set the correct environment variables
export PYTHONPATH=/home/mccoy/Projects/NotebookLM/LivingTruthEngine
export PROJECT_ROOT=/home/mccoy/Projects/NotebookLM

# Start Cursor from this directory
cursor .

echo "✅ Cursor started with Living Truth Engine environment"
echo "📁 Working directory: $(pwd)"
echo "🐍 Python environment: $VIRTUAL_ENV"
echo "🔧 PYTHONPATH: $PYTHONPATH" 