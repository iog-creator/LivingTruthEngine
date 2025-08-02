# Living Truth Engine - Langflow Setup and Workflow

## Overview

The Living Truth Engine now uses Langflow as the primary workflow orchestration platform for survivor testimony analysis. Langflow provides a modern, Python-native interface for building complex multi-agent workflows and has replaced Flowise as the main workflow engine.

## Architecture

### Services Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Langflow      │    │   PostgreSQL    │    │   LM Studio     │
│   (Port 7860)   │    │   (Port 5434)   │    │   (Port 1234)   │
│                 │    │                 │    │                 │
│ • Multi-Agent   │    │ • Data Storage  │    │ • Local Models  │
│ • Python Native │    │ • PGVector      │    │ • Qwen3 Models  │
│ • Workflow UI   │    │ • Evidence DB   │    │ • API Endpoint  │
│ • Langflow DB   │    │ • Langflow DB   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Neo4j         │
                    │   (Port 7474)   │
                    │                 │
                    │ • Graph DB      │
                    │ • Relationships │
                    │ • Network Data  │
                    └─────────────────┘
```

### Survivor Testimony Analysis Workflow

The Langflow workflow implements a sophisticated multi-agent system for analyzing survivor testimony for evidence patterns:

#### Workflow Components

1. **Start Node (Form Input)**
   - Query/Transcript input
   - Anonymization toggle
   - Output type selection (summary, study_guide, timeline, audio)

2. **Planner Agent (Qwen3-8B)**
   - Analyzes input for evidence themes
   - Creates structured research plan
   - Generates subagent tasks

3. **SubAgent System (Qwen3-0.6B)**
   - Specialized research agents
   - Tools: Arxiv, Google Search, Web Scraper, pgVectorSearch
   - Evidence reference analysis

4. **Writer Agent (Qwen3-8B)**
   - Synthesizes findings
   - Generates structured reports
   - Handles anonymization

5. **Condition Agent**
   - Determines if more research is needed
   - Controls workflow iteration

## Setup Instructions

### Prerequisites

- Docker and Docker Compose v2
- Python 3.12+ with virtual environment
- Required API keys (see Environment Variables section)

### Quick Setup

1. **Clone and navigate to project:**
   ```bash
   cd LivingTruthEngine
   ```

2. **Activate virtual environment:**
   ```bash
   source living_venv/bin/activate
   ```

3. **Run setup script:**
   ```bash
   ./scripts/setup/setup_langflow_workflow.sh
   ```

### Manual Setup

1. **Start services (notebook_agent group):**
   ```bash
   cd /home/mccoy/Projects/RippleAGI/notebook_agent
   docker compose -f docker/docker-compose.yml up -d
   ```

2. **Wait for services to be ready:**
   ```bash
   # Check service health
   curl -f http://localhost:7860/health  # Langflow
   curl -f http://localhost:1234/v1/models  # LM Studio
   curl -f http://localhost:7474/  # Neo4j
   ```

3. **Import workflow:**
   ```bash
   python scripts/setup/import_langflow_workflow.py
   ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Langflow Configuration
LANGFLOW_SECRET_KEY=your-secret-key-here
LANGFLOW_SUPERUSER=admin
LANGFLOW_SUPERUSER_PASSWORD=admin

# API Keys
SERP_API_KEY=your-serp-api-key
GOOGLE_CSE_ID=your-google-cse-id
MCP_API_KEY=your-mcp-api-key

# Database Configuration
POSTGRES_DB=living_truth_engine
POSTGRES_USER=postgres
POSTGRES_PASSWORD=pass

# Service Endpoints
LANGFLOW_API_ENDPOINT=http://localhost:7860
LM_STUDIO_ENDPOINT=http://localhost:1234
```

## Service Access

### Web Interfaces

- **Langflow**: http://localhost:7860 (admin/admin)
- **Neo4j**: http://localhost:7474
- **LM Studio**: http://localhost:1234

### API Endpoints

- **Langflow API**: http://localhost:7860/api/v1
- **LM Studio API**: http://localhost:1234/v1
- **MCP Server**: http://localhost:8000
- **Neo4j API**: http://localhost:7474

## Workflow Features

### Multi-Agent Architecture

The workflow uses a sophisticated multi-agent system:

1. **Planner Agent**: Analyzes input and creates research plan
2. **Research SubAgents**: Specialized agents for different aspects
3. **Writer Agent**: Synthesizes findings into reports
4. **Condition Agent**: Controls workflow iteration

### Evidence Analysis Capabilities

- **Pattern Recognition**: Identifies evidence themes and motifs
- **Reference Extraction**: Finds explicit and implicit evidence references
- **Theological Analysis**: Examines doctrinal implications
- **Historical Context**: Researches cultural and historical background
- **Cross-Reference Validation**: Verifies findings against multiple sources

### Output Types

1. **Summary**: Concise analysis of key findings
2. **Study Guide**: Detailed guide with discussion questions
3. **Timeline**: Chronological organization with evidence parallels
4. **Audio**: Structured for spoken presentation

### Tools Integration

- **Arxiv**: Academic research papers
- **Google Custom Search**: Web-based research
- **Web Scraper**: Content extraction from websites
- **pgVectorSearch**: Evidence reference database search
- **MCP Server Tools**: Custom Living Truth Engine tools

## Usage

### Accessing the Workflow

1. Open Langflow at http://localhost:7860
2. Login with admin/admin
3. Find "Living Truth Engine Survivor Testimony Analysis"
4. Click to open the workflow

### Running Analysis

1. **Input Form**: Fill in the required fields
   - Query/Transcript: Your text for analysis
   - Anonymize: Toggle for privacy protection
   - Output Type: Choose desired output format

2. **Execution**: The workflow will automatically:
   - Analyze the input for evidence patterns
   - Create specialized research tasks
   - Execute research using multiple tools
   - Synthesize findings into a report

3. **Output**: Receive a structured analysis report

### Example Queries

- "Analyze this survivor testimony for evidence patterns of healing and restoration"
- "Identify evidence themes in this narrative about forgiveness"
- "Find evidence parallels to this story of redemption"
- "Examine the implications of this testimony"

## Troubleshooting

### Common Issues

1. **Services not starting:**
   ```bash
   # Check Docker status
   docker compose -f docker/docker-compose.yml ps
   
   # Check logs
   docker compose -f docker/docker-compose.yml logs
   ```

2. **Workflow import fails:**
   ```bash
   # Check Langflow health
   curl -f http://localhost:7860/health
   
   # Check database connection
   docker exec living_truth_postgres psql -U postgres -c "\\l"
   
   # Manual import
   python scripts/setup/import_langflow_workflow.py
   ```

3. **API key errors:**
   - Verify all required API keys are set in `.env`
   - Check API key validity and permissions

4. **Model loading issues:**
   - Ensure LM Studio is running and accessible
   - Check model files are properly loaded
   - Verify Qwen3 models are available

### Health Checks

```bash
# Service health check script
./scripts/setup/check_system.sh

# Individual service checks
curl -f http://localhost:7860/health  # Langflow
curl -f http://localhost:1234/v1/models  # LM Studio
curl -f http://localhost:7474/  # Neo4j
curl -f http://localhost:8000/health  # MCP Server
```

## Development

### Customizing the Workflow

1. **Modify workflow JSON**: Edit `LivingTruthEngine_SurvivorTestimonyAnalysis_Langflow.json`
2. **Add new tools**: Extend the tools array in subagent nodes
3. **Update prompts**: Modify system messages for different agents
4. **Add new output types**: Extend the form options and writer agent logic

### Adding New Models

1. **Update LM Studio**: Add new models to LM Studio
2. **Modify workflow**: Update model references in workflow JSON
3. **Test integration**: Verify model compatibility and performance

### Extending MCP Integration

1. **Add new tools**: Extend `living_truth_fastmcp_server.py`
2. **Update workflow**: Add new tools to subagent configurations
3. **Test functionality**: Verify tool integration and performance

## Security Considerations

- **API Keys**: Store securely in `.env` file, never commit to version control
- **Authentication**: Use strong passwords for Langflow admin account
- **Network Security**: Consider firewall rules for production deployment
- **Data Privacy**: Anonymization features protect sensitive information
- **Access Control**: Limit access to sensitive analysis capabilities

## Performance Optimization

- **Model Selection**: Choose appropriate model sizes for your hardware
- **Resource Allocation**: Adjust Docker resource limits as needed
- **Caching**: Enable Langflow caching for improved performance
- **Parallel Processing**: Subagents can run in parallel for efficiency

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review service logs for error details
3. Verify environment configuration
4. Test individual components separately

## Future Enhancements

- **Additional Models**: Support for more specialized models
- **Enhanced Tools**: More research and analysis tools
- **Advanced Analytics**: Statistical analysis of patterns
- **Visualization**: Interactive charts and graphs
- **Collaboration**: Multi-user workflow sharing 