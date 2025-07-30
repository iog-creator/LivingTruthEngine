# Living Truth Engine

A Flowise-based NotebookLM clone for Biblical forensic analysis and survivor testimony corroboration.

## Overview

The Living Truth Engine is an AI-powered system designed for deep analysis of Biblical texts and survivor testimonies. It uses advanced language models, hybrid retrieval systems, and interactive visualizations to provide comprehensive insights while maintaining privacy and security.

## Features

- **Document Ingestion**: Support for text, PDF, YouTube, and audio files
- **Hybrid Retrieval**: Combines dense and sparse retrieval with reranking
- **Privacy Controls**: Anonymization toggle for sensitive content
- **Structured Outputs**: Summaries, study guides, timelines, and audio overviews
- **Interactive Dashboard**: Real-time visualizations with Plotly/Dash
- **3D Visualizations**: Advanced data representation capabilities

## Architecture

- **Frontend**: Flowise UI + Dash Dashboard
- **Backend**: Flowise graph with LangChain chains
- **Models**: Qwen3-0.6B (embedder/reranker) + Qwen3-8B (LLM)
- **Database**: PostgreSQL with PGVector extension
- **Inference**: LM Studio on localhost:1234
- **TTS**: Piper (en_US-lessac-medium)

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+ with PGVector extension
- LM Studio running on localhost:1234
- NVIDIA GPU (optional, for acceleration)

## Installation

### 1. Clone and Setup

```bash
# Create project directory
mkdir LivingTruthEngine
cd LivingTruthEngine

# Create virtual environment
python -m venv mcp_env
source mcp_env/bin/activate  # On Windows: mcp_env\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install langchain langchain-huggingface langchain-openai langchain-community \
    yt_dlp spacy plotly psycopg2-binary dash piper-tts serpapi requests
```

### 3. Setup Flowise

```bash
npm install -g flowise
flowise start
```

### 4. Database Setup

```sql
-- Create database
CREATE DATABASE living_truth_engine;

-- Enable PGVector extension
CREATE EXTENSION IF NOT EXISTS vector;
```

### 5. Environment Configuration

Update `.env` file with your actual values:

```env
FLOWISE_API_ENDPOINT=http://localhost:3000
FLOWISE_API_KEY=your_flowise_api_key
FLOWISE_CHATFLOW_ID=your_chatflow_id
LANGCHAIN_API_KEY=your_langsmith_key
SERP_API_KEY=your_serpapi_key
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=living_truth_engine
POSTGRES_USER=postgres
POSTGRES_PASSWORD=pass
LM_STUDIO_URL=http://localhost:1234/v1
TTS_MODEL_PATH=en_US-lessac-medium.onnx
TTS_CONFIG_PATH=en_US-lessac-medium.json
```

## Usage

### 1. Start Services

```bash
# Start Flowise (if not already running)
flowise start

# Start MCP server
python flowise_mcp_server.py
```

### 2. Import Flow Graph

1. Open Flowise UI at `http://localhost:3000`
2. Import `living_truth_full_flow.json`
3. Configure credentials and variables in the UI

### 3. Query the System

Use the MCP server to query the system:

```python
# Example query
query_flowise(
    query="Biblical abuse patterns",
    anonymize=True,
    output_type="study_guide"
)
```

### 4. Access Dashboard

Open `http://localhost:8050` to view the interactive dashboard with visualizations.

## API Endpoints

- **Flowise API**: `http://localhost:3000`
- **Dashboard**: `http://localhost:8050`
- **LM Studio**: `http://localhost:1234`

## Model Configuration

### Embedding Model
- **Model**: `text-embedding-qwen3-embedding-0.6b`
- **Dimensions**: 1024
- **Provider**: LM Studio

### Reranker Model
- **Model**: `qwen.qwen3-reranker-0.6b`
- **Provider**: LM Studio

### LLM Model
- **Model**: `qwen/qwen3-8b`
- **Temperature**: 0.7
- **Max Tokens**: 2048
- **Provider**: LM Studio

## Project Structure

```
LivingTruthEngine/
├── .cursor/
│   ├── mcp.json              # MCP server configuration
├── .cursorrules              # Cursor IDE rules
├── .env                      # Environment variables
├── flowise_mcp_server.py     # MCP server implementation
├── living_truth_full_flow.json # Flowise graph configuration
├── README.md                 # This file
├── sources/                  # Document storage
└── visualizations/           # Output visualizations
```

## Development

### Adding New Features

1. **Flowise Nodes**: Add custom nodes in Flowise UI
2. **MCP Functions**: Extend `flowise_mcp_server.py`
3. **Visualizations**: Add new chart types to dashboard
4. **Documentation**: Update README and comments

### Testing

```bash
# Test MCP server
python -c "from flowise_mcp_server import FlowiseMCPServer; server = FlowiseMCPServer(); print(server.get_status())"

# Test database connection
python -c "import psycopg2; conn = psycopg2.connect('postgresql://postgres:pass@localhost:5432/living_truth_engine'); print('Connected')"
```

## Troubleshooting

### Common Issues

1. **Flowise not running**
   - Check if Flowise is started: `flowise start`
   - Verify port 3000 is available

2. **Database connection failed**
   - Ensure PostgreSQL is running
   - Check credentials in `.env`
   - Verify PGVector extension is installed

3. **LM Studio not responding**
   - Start LM Studio on localhost:1234
   - Load required models (Qwen3-0.6B, Qwen3-8B)

4. **MCP server errors**
   - Check environment variables
   - Verify Flowise API key and chatflow ID
   - Check logs for detailed error messages

### Logs

View system logs:

```bash
# Get recent logs
python flowise_mcp_server.py --logs

# Check Flowise logs
tail -f ~/.flowise/logs/flowise.log
```

## Security

- **Anonymization**: Toggle to protect sensitive information
- **Environment Variables**: Never hardcode credentials
- **Database Security**: Use strong passwords and proper access controls
- **API Security**: Implement proper authentication for production

## Contributing

1. Follow the coding standards in `.cursorrules`
2. Test all changes thoroughly
3. Update documentation
4. Use the MCP server for all operations
5. Maintain environment consistency

## License

This project is for research and educational purposes. Please ensure compliance with all applicable laws and regulations regarding data privacy and security.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs for error details
3. Verify environment configuration
4. Test individual components

---

**Living Truth Engine** - Empowering truth through AI-driven analysis 