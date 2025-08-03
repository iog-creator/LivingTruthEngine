#!/bin/bash

# Living Truth Engine MCP Server Startup Script
# This script ensures proper environment setup for the MCP server

# Set the target directory
TARGET_DIR="/home/mccoy/Projects/NotebookLM/LivingTruthEngine"
cd "${TARGET_DIR}"

# Activate virtual environment
source living_venv/bin/activate

# Set environment variables
export FLOWISE_API_ENDPOINT="http://localhost:3000"
export FLOWISE_API_KEY="kkUVM9tTVKzL9btjElkJwn2fWQiXGQy1J_BvV3Mw-14"
export FLOWISE_CHATFLOW_ID="9f8013d8-351a-4bd9-a973-fab86df45491"
export PYTHONPATH="${TARGET_DIR}"
export PYTHONIOENCODING=utf-8

# Ensure proper signal handling
trap 'exit 0' SIGTERM SIGINT

# Start the MCP server with proper error handling
# Use exec to replace shell process and prevent timeout issues
exec python3 living_truth_engine_mcp.py 