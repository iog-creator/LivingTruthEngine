#!/bin/bash

# Living Truth Engine Environment Activation Script
# This script ensures the correct virtual environment is activated

echo "🔧 Activating Living Truth Engine Environment..."

# Deactivate any existing virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Deactivating current environment: $VIRTUAL_ENV"
    deactivate
fi

# Activate the living_venv
echo "Activating living_venv..."
source /home/mccoy/Projects/NotebookLM/LivingTruthEngine/living_venv/bin/activate

# Set project-specific environment variables
export PYTHONPATH="/home/mccoy/Projects/NotebookLM/LivingTruthEngine:$PYTHONPATH"
export PROJECT_ROOT="/home/mccoy/Projects/NotebookLM/LivingTruthEngine"

# Verify activation
echo "✅ Environment activated: $VIRTUAL_ENV"
echo "✅ Python path: $(which python)"
echo "✅ PYTHONPATH: $PYTHONPATH"
echo "✅ Project root: $PROJECT_ROOT"

# Test Python import
python -c "import sys; print(f'Python version: {sys.version}')" 2>/dev/null && echo "✅ Python import test passed" || echo "❌ Python import test failed" 