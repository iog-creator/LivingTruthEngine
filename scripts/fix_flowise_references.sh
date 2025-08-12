#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Replacing Langflow references with Langflow..."

# Function to replace in a file
replace_in_file() {
    local file="$1"
    if [[ -f "$file" ]]; then
        echo "Processing: $file"
        
        # Replace Langflow with Langflow (case-insensitive)
        sed -i 's/Langflow/Langflow/gI' "$file"
        sed -i 's/Langflow/Langflow/g' "$file"
        
        # Fix specific patterns
        sed -i 's/Langflow API endpoint/Langflow API endpoint/g' "$file"
        sed -i 's/Langflow API key/Langflow API key/g' "$file"
        sed -i 's/Langflow chatflow/Langflow workflow/g' "$file"
        sed -i 's/Langflow graph/Langflow workflow/g' "$file"
        sed -i 's/Langflow workflowflow/Langflow workflow/g' "$file"  # Fix double replacement
        
        # Fix port references
        sed -i 's/localhost:7860/localhost:7860/g' "$file"
        sed -i 's/port 3000/port 7860/g' "$file"
        
        # Fix API endpoints
        sed -i 's|/api/v1/chatflows|/api/v1/workflows|g' "$file"
        
        # Fix environment variables
        sed -i 's/Langflow_API_ENDPOINT/LANGFLOW_API_ENDPOINT/g' "$file"
        sed -i 's/Langflow_API_KEY/LANGFLOW_API_KEY/g' "$file"
        sed -i 's/Langflow_CHATFLOW_ID/LANGFLOW_WORKFLOW_ID/g' "$file"
        sed -i 's/Langflow_PORT/LANGFLOW_PORT/g' "$file"
        sed -i 's/Langflow_HOST/LANGFLOW_HOST/g' "$file"
        
        # Fix file names
        sed -i 's/Langflow_mcp_server/langflow_mcp_server/g' "$file"
        sed -i 's/Langflow-mcp-server/langflow-mcp-server/g' "$file"
        sed -i 's/Langflow_mcp_server.py/langflow_mcp_server.py/g' "$file"
        sed -i 's/Langflow-mcp-server.js/langflow-mcp-server.js/g' "$file"
        
        # Fix directory names
        sed -i 's/\.Langflow/\.langflow/g' "$file"
        
        # Fix function names
        sed -i 's/query_Langflow/query_langflow/g' "$file"
        
        # Fix descriptions
        sed -i 's/Langflow-based/Langflow-based/g' "$file"
        sed -i 's/Langflow integration/Langflow integration/g' "$file"
    fi
}

# Files to process (excluding Archive_Legacy and .git)
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" -o -name "*.sh" -o -name "*.yml" -o -name "*.yaml" \) \
    ! -path "./Archive_Legacy/*" \
    ! -path "./.git/*" \
    ! -path "./living_venv/*" \
    ! -path "./node_modules/*" \
    ! -path "./docs/snapshots/*" \
    -exec bash -c 'replace_in_file "$1"' _ {} \;

echo "✅ Langflow references replaced with Langflow!"
echo ""
echo "Note: Some references in Archive_Legacy/ are intentionally preserved as historical documentation."
