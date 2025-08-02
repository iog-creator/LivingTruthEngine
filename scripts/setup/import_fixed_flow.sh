#!/bin/bash

# Living Truth Engine - Import Fixed Flowise Flow
# This script imports the fixed Flowise flow configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

print_status "Living Truth Engine - Flowise Flow Import"
print_status "=========================================="

# Check if we're in the right directory
if [[ ! -f "$PROJECT_ROOT/LivingTruthFlowise_Fixed.json" ]]; then
    print_error "Fixed flow file not found in project root"
    print_error "Expected: $PROJECT_ROOT/LivingTruthFlowise_Fixed.json"
    exit 1
fi

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    print_warning "Virtual environment not detected"
    print_status "Attempting to activate living_venv..."
    
    if [[ -f "$PROJECT_ROOT/living_venv/bin/activate" ]]; then
        source "$PROJECT_ROOT/living_venv/bin/activate"
        print_success "Activated virtual environment"
    else
        print_error "Virtual environment not found at $PROJECT_ROOT/living_venv"
        print_status "Please activate the virtual environment manually"
        exit 1
    fi
fi

# Check if required packages are installed
print_status "Checking dependencies..."
python -c "import requests, json" 2>/dev/null || {
    print_error "Required packages not found"
    print_status "Installing dependencies..."
    pip install requests
}

# Run the Python import script
print_status "Running import script..."
cd "$PROJECT_ROOT"
python scripts/setup/import_fixed_flow.py

if [[ $? -eq 0 ]]; then
    print_success "Flow import completed successfully!"
    print_status ""
    print_status "Next steps:"
    print_status "1. Open Flowise at http://localhost:3000"
    print_status "2. Navigate to the imported flow"
    print_status "3. Configure any missing credentials"
    print_status "4. Test the flow with a research query"
else
    print_error "Flow import failed"
    exit 1
fi 