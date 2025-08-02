# Living Truth Engine - Project Structure

## Overview

The Living Truth Engine is a Flowise-based NotebookLM clone designed for survivor testimony analysis and evidence corroboration. This document outlines the project structure and organization.

## Directory Structure

```
LivingTruthEngine/
├── .cursor/                          # Cursor IDE configuration
│   ├── mcp-server-docs.md           # MCP server documentation
│   ├── project-structure.md         # This file
│   ├── development-workflow.md      # Development workflow guide
│   ├── troubleshooting.md           # Troubleshooting guide
│   └── settings.json                # Cursor settings
├── .cursorrules                      # Cursor AI behavior rules
├── .env                             # Environment variables
├── living_venv/                     # Python virtual environment
├── flowise_mcp_server.py            # MCP server implementation
├── living_truth_full_flow.json      # Flowise graph configuration
├── README.md                        # Project documentation
├── sources/                         # Document storage
│   ├── documents/                   # Text documents
│   ├── pdfs/                        # PDF files
│   ├── audio/                       # Audio files
│   └── videos/                      # Video files
├── visualizations/                  # Output visualizations
│   ├── dashboards/                  # Dash dashboard files
│   ├── plots/                       # Plotly visualizations
│   └── reports/                     # Generated reports
└── logs/                            # Application logs
    ├── mcp_server.log              # MCP server logs
    └── flowise.log                 # Flowise logs
```

## Core Components

### 1. Flowise Integration
- **`flowise_mcp_server.py`**: MCP server for Cursor integration
- **`living_truth_full_flow.json`**: Flowise graph configuration
- **Flowise UI**: Web interface at http://localhost:3000

### 2. Environment Management
- **`living_venv/`**: Python virtual environment
- **`.env`**: Environment variables and configuration
- **Dependencies**: All required Python packages

### 3. Document Processing
- **`sources/`**: Input document storage
- **Support for**: Text, PDF, YouTube, audio files
- **Processing**: LangChain-based document ingestion

### 4. Visualization & Output
- **`visualizations/`**: Generated outputs
- **Dashboard**: Dash-based interactive dashboard
- **Reports**: Structured outputs (summaries, study guides, timelines)

## Configuration Files

### Environment Configuration (`.env`)
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

### Cursor Rules (`.cursorrules`)
- Project-specific AI behavior rules
- Environment management guidelines
- MCP server integration rules
- Code quality standards

### MCP Configuration (`~/.cursor/mcp.json`)
- Global MCP server configuration
- Tool definitions and parameters
- Environment variable mapping

## Technology Stack

### Backend
- **Python 3.13**: Core programming language
- **LangChain**: AI/ML framework
- **Flowise**: Visual AI workflow builder
- **PostgreSQL**: Database with PGVector extension

### AI Models
- **Qwen3-0.6B**: Embedding and reranking models
- **Qwen3-8B**: Large language model
- **LM Studio**: Local inference server

### Visualization
- **Dash**: Interactive web dashboard
- **Plotly**: Data visualization library
- **3D Visualizations**: Advanced data representation

### Development Tools
- **Cursor IDE**: Primary development environment
- **MCP Protocol**: Tool integration
- **Git**: Version control

## Data Flow

### 1. Document Ingestion
```
Sources → LangChain Processing → PGVector Storage
```

### 2. Query Processing
```
User Query → MCP Server → Flowise Graph → AI Models → Results
```

### 3. Output Generation
```
Results → Structured Output → Visualization → Dashboard
```

## Security & Privacy

### Data Protection
- **Anonymization**: Toggle for sensitive content
- **Environment Variables**: Secure configuration storage
- **Logging**: Audit trail for all operations

### Access Control
- **API Keys**: Secure authentication
- **Database**: PostgreSQL with proper access controls
- **File Permissions**: Appropriate file system security

## Performance Considerations

### Optimization
- **Batch Processing**: Efficient document ingestion
- **Caching**: Vector store optimization
- **Async Operations**: Non-blocking dashboard updates

### Scalability
- **Modular Architecture**: Easy component replacement
- **Configuration-Driven**: Environment-based settings
- **Extensible Design**: Plugin-based functionality

## Development Guidelines

### Code Organization
- **Separation of Concerns**: Clear module boundaries
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Inline and external documentation

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Load and stress testing

### Deployment
- **Environment Isolation**: Virtual environment usage
- **Configuration Management**: Environment-driven setup
- **Monitoring**: Logging and error tracking

## Maintenance

### Regular Tasks
- **Dependency Updates**: Keep packages current
- **Log Rotation**: Manage log file sizes
- **Database Maintenance**: Optimize vector store

### Backup Strategy
- **Configuration**: Version control for settings
- **Data**: Regular database backups
- **Code**: Git repository management

## Future Enhancements

### Planned Features
- **Multi-language Support**: Internationalization
- **Advanced Analytics**: Enhanced visualization capabilities
- **API Extensions**: Additional tool integrations
- **Mobile Support**: Responsive design improvements

### Architecture Evolution
- **Microservices**: Component decomposition
- **Cloud Integration**: Scalable deployment options
- **AI Model Updates**: Latest model integrations 