# Living Truth Engine

A comprehensive system for survivor testimony analysis and evidence discovery using advanced AI and MCP (Model Context Protocol) integration.

## 🚀 **Current Status: FULLY OPERATIONAL**

### **✅ What's Working**
- **Real AI Analysis**: Desktop LM Studio integration with actual LLM generation (no pattern matching)
- **Advanced Visualization**: Interactive 3D network graphs with entity extraction
- **Complete Analysis Pipeline**: Single-button orchestration of entire workflow
- **Modern Single-File UI**: Clean, responsive interface with dark theme
- **AI Chat Interface**: Real-time chat with AI using your local models
- **Health Monitoring**: Comprehensive service health gates with real-time monitoring
- **MCP Integration**: Full MCP server integration with 20+ tools available
- **Systematic Testing**: All critical tests passing with comprehensive verification

### **🎯 Key Features**
- **Real AI-Powered Analysis**: Actual LLM generation for summaries and claims extraction
- **Advanced 3D Visualization**: Interactive network graphs with dynamic entity extraction
- **Complete Analysis Pipeline**: Single button orchestrates document ingestion → AI analysis → visualization
- **Modern UI**: Dark theme, responsive design, real-time status updates
- **Multi-Model Support**: qwen/qwen3-8b, meta/llama-3.3-70b, mistralai/devstral-small-2505, etc.
- **Health Gates**: Automatic service monitoring with fail-fast behavior
- **No Fallbacks**: Clean error handling without silent failures

## 🏃‍♂️ **Quick Start**

### **1. Start the System**
```bash
# Start all services
docker compose -f docker/docker-compose.yml up -d

# Verify health
curl -s http://localhost:8050/api/health/full | jq .
```

### **2. Access the Modern UI**
Open your browser to: `http://localhost:8050/static/ui_status_chat.html`

**This is the new single-file UI with:**
- **🎨 Modern Design**: Dark theme with grid background and colored status cards
- **📊 Status Stack**: Real-time LLM, Embedding, and Progress indicators
- **🤖 AI Chat**: Direct chat with LM Studio models
- **🚀 Complete Analysis**: Single button orchestrates entire workflow
- **🎨 Advanced Visualization**: Interactive 3D network graphs
- **📋 Run Management**: Browse and select analysis runs

### **3. Key UI Features**

#### **Complete Analysis Pipeline**
- **"Start Complete Analysis"**: Single button orchestrates entire workflow
- **Step-by-Step Progress**: Visual indicators for each stage
- **Real-time Updates**: Live status and progress tracking
- **Comprehensive Results**: AI summary, claims, and visualization in one view

#### **AI Integration**
- **Real LLM Generation**: Uses desktop LM Studio on port 1234
- **AI Chat**: Direct conversation with AI models
- **AI Summary**: Real AI-powered document summarization
- **AI Claims**: AI-powered claim extraction and categorization

#### **Advanced Visualization**
- **3D Network Graphs**: Interactive Plotly-based visualizations
- **Entity Extraction**: JavaScript-based entity identification
- **Dynamic Generation**: Real-time graph creation from analysis data
- **HTML Rendering**: Proper visualization serving and embedding

#### **Status Management**
- **Real-time Indicators**: Live updates during processing
- **Progress Tracking**: Visual feedback for each stage
- **Error Handling**: Clear error messages and recovery
- **System Health**: Comprehensive service monitoring

## 🔧 **System Architecture**

### **Services**
- **Dashboard**: Port 8050 - Main UI and API interface
- **Desktop LM Studio**: Port 1234 - Real AI model inference (primary)
- **Docker LM Studio**: Port 1235 - Backup embedding models
- **Langflow**: Port 7860 - Workflow orchestration
- **Neo4j**: Port 7474 - Graph database
- **Redis**: Port 6379 - Caching and session management

### **Network Configuration**
```yaml
# Docker to Desktop LM Studio communication
services:
  dashboard:
    environment:
      - LM_STUDIO_ENDPOINT=http://host.docker.internal:1234
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

### **Health Gates**
The system monitors all critical services:
- ✅ **Dashboard**: UI and API interface status
- ✅ **MCP Server**: Tool availability and execution
- ✅ **LM Studio**: AI model availability and connectivity
- ✅ **Langflow**: Workflow service health
- ✅ **Neo4j**: Database connectivity
- ✅ **Redis**: Cache service status

## 🧠 **AI Analysis Capabilities**

### **Real LLM Generation**
- **No Pattern Matching**: All analysis uses actual LLM calls
- **Structured Output**: JSON-formatted responses for consistency
- **Error Handling**: Graceful fallbacks if AI service unavailable
- **Confidence Scores**: AI-generated confidence metrics

### **Document Analysis**
- **AI Summary**: Real AI-powered document summarization with key points and sentiment
- **AI Claims**: AI-powered claim extraction with categorization and confidence
- **Entity Extraction**: JavaScript-based entity identification from documents
- **Visualization**: Dynamic graph generation from analysis results

### **Available Models**
- qwen/qwen3-8b (primary for analysis)
- meta/llama-3.3-70b
- mistralai/devstral-small-2505
- microsoft/phi-4-reasoning-plus
- deepseek/deepseek-r1-0528-qwen3-8b
- google/gemma-3-12b
- And 10+ more models...

## 📊 **API Endpoints**

### **Health & Status**
- `GET /api/health` - Basic health check
- `GET /api/health/full` - Comprehensive health gates
- `GET /api/contract` - API contract specification

### **Analysis**
- `POST /api/execute` - Execute MCP tools
- `GET /api/tools` - List available tools
- `GET /api/runs` - List analysis runs
- `POST /api/ai/chat` - AI chat interface
- `GET /api/runs/{run_id}/corpus` - Get run corpus data
- `GET /api/runs/{run_id}/transcript/{doc_index}` - Get full transcript

### **Visualization**
- `GET /api/visualizations` - List available visualization files
- `GET /api/visualizations/{filename}` - Serve specific HTML visualization

### **UI**
- `GET /static/ui_status_chat.html` - Modern single-file UI (primary)
- `GET /` - Legacy comprehensive dashboard (alternative)

## 🧪 **Testing**

### **Run All Tests**
```bash
# Health gates and system tests
pytest tests/test_health_gates.py tests/test_no_fallbacks.py -v

# Expected output: All tests passing
```

### **Manual Testing**
```bash
# Test health gates
curl -s http://localhost:8050/api/health/full | jq .

# Test LM Studio
curl -s http://localhost:1234/v1/models | jq '.data | length'

# Test AI chat
curl -s -X POST http://localhost:8050/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello, how are you?"}' | jq .

# Test UI accessibility
curl -s http://localhost:8050/static/ui_status_chat.html | head -5

# Test complete workflow
bash scripts/smoke_envelope.sh
```

## 📈 **Performance**

### **Response Times**
- Health checks: <2s
- AI analysis: 5-30s (depending on model and text length)
- UI loading: <1s
- Service startup: <60s
- Visualization generation: 10-30s

### **Reliability**
- Health gates prevent operation when services are down
- Real AI generation with no pattern matching fallbacks
- Graceful error handling with descriptive messages
- No silent failures or hidden fallbacks

## 🔍 **Troubleshooting**

### **Common Issues**
1. **LM Studio not responding**: Check if desktop LM Studio is running on port 1234
2. **Health gates failing**: Check Docker container status with `docker ps`
3. **UI not loading**: Verify dashboard container is running on port 8050
4. **Visualization blank**: Check entity extraction and graph data generation
5. **AI chat not working**: Verify LM Studio model availability

### **Logs**
```bash
# Dashboard logs
docker logs living-truth-dashboard

# MCP server logs
tail -f data/outputs/logs/living_truth_fastmcp.log

# Health check
bash scripts/smoke_envelope.sh
```

## 📚 **Documentation**

- [Phase 8.3 New UI Completion](PHASE_8_3_NEW_UI_COMPLETION.md)
- [System Integration Status](.cursor/rules/system_integration_status.mdc)
- [AI Integration Patterns](.cursor/rules/ai_integration.mdc)
- [Visualization System](.cursor/rules/visualization_system.mdc)
- [Complete Analysis Pipeline](.cursor/rules/complete_analysis_pipeline.mdc)
- [Development Workflow](.cursor/rules/workflow.mdc)

## 🤝 **Contributing**

This project follows strict development workflows:
1. **Build → Verify → Iterate**: All changes must pass health gates
2. **Systematic Testing**: Each component tested before moving to next
3. **No Fallbacks**: Explicit error handling only, no silent failures
4. **Documentation**: Complete usage instructions and cursor rules updated with each change

## 🎯 **Key Achievements**

### **Real AI Integration**
- ✅ **No Pattern Matching**: All analysis uses actual LLM generation
- ✅ **Desktop LM Studio**: Direct integration with port 1234
- ✅ **AI Tools**: `analyze_veritas_summary`, `analyze_veritas_claims`, `generate_lm_studio_text`
- ✅ **Structured Output**: JSON-formatted AI responses

### **Advanced Visualization**
- ✅ **3D Network Graphs**: Interactive Plotly visualizations
- ✅ **Entity Extraction**: JavaScript-based entity identification
- ✅ **Dynamic Generation**: Real-time graph creation from analysis data
- ✅ **HTML Rendering**: Proper visualization serving and embedding

### **Complete Analysis Pipeline**
- ✅ **Single Button**: "Start Complete Analysis" orchestrates entire workflow
- ✅ **Step-by-Step Progress**: Visual indicators for each stage
- ✅ **Comprehensive Results**: Summary, claims, and visualization in one view
- ✅ **Real-time Updates**: Live status and progress tracking

### **Modern UI**
- ✅ **Single File**: Complete UI in `ui_status_chat.html`
- ✅ **Dark Theme**: Modern design with grid background
- ✅ **Responsive**: Works on desktop and mobile
- ✅ **Status Stack**: Real-time system status indicators

---

**Status**: ✅ **FULLY OPERATIONAL** - All systems operational with real AI analysis, advanced visualization, and complete analysis pipeline.

**🎯 Use the modern UI at http://localhost:8050/static/ui_status_chat.html for the full experience!** 