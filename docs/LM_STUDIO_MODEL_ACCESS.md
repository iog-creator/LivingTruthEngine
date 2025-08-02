# LM Studio Model Access Configuration

## Overview
This document explains how the Docker version of LM Studio accesses and uses the same models installed on your system.

## ✅ **Current Configuration**

### **Volume Mounts**
The LM Studio Docker container is configured with these volume mounts:

```yaml
volumes:
  - /home/mccoy/.lmstudio/models:/app/models    # Your system models
  - /home/mccoy/.lmstudio:/app/.lmstudio        # LM Studio config & cache
```

This means:
- **Your system models** (`/home/mccoy/.lmstudio/models/`) → **Container models** (`/app/models/`)
- **Your system config** (`/home/mccoy/.lmstudio/`) → **Container config** (`/app/.lmstudio/`)

### **Available Models**
The Docker container can access all models installed in your system LM Studio:

```
/app/models/
├── DevQuasar/
│   └── Qwen.Qwen3-Reranker-0.6B-GGUF/
├── Qwen/
│   ├── Qwen3-Embedding-4B-GGUF/
│   └── Qwen3-Embedding-0.6B-GGUF/
├── abetlen/
│   └── Phi-3.5-vision-instruct-gguf/
├── lmstudio-community/
│   ├── Qwen2.5-VL-7B-Instruct-GGUF/
│   ├── Qwen3-8B-GGUF/
│   └── gemma-3-4b-it-GGUF/
└── second-state/
    └── All-MiniLM-L6-v2-Embedding-GGUF/
```

## 🔧 **How It Works**

### **1. Model Discovery**
- LM Studio automatically discovers models in `/app/models/`
- Models are loaded on-demand when requested
- Configuration is preserved from your system installation

### **2. API Access**
- Models are accessible via LM Studio API at `http://localhost:1234`
- MCP server tools can list and use these models
- Same models available in both system and Docker versions

### **3. Performance**
- Models run in the container environment
- Uses container's CPU/GPU resources
- No performance impact from volume mounting

## 🛠️ **MCP Server Integration**

### **Available Tools**
The Living Truth FastMCP Server includes these LM Studio tools:

1. **`get_lm_studio_models`** - List available models
2. **`generate_lm_studio_text`** - Generate text using models
3. **`test_lm_studio_connection`** - Test connection
4. **`get_lm_studio_status`** - Get server status

### **Usage Examples**
```python
# List available models
mcp_living_truth_fastmcp_server_get_lm_studio_models()

# Generate text with specific model
mcp_living_truth_fastmcp_server_generate_lm_studio_text(
    prompt="Explain Biblical forensic analysis",
    model="gemma-3-4b-it-GGUF",
    max_tokens=500
)

# Test connection
mcp_living_truth_fastmcp_server_test_lm_studio_connection()

# Get server status
mcp_living_truth_fastmcp_server_get_lm_studio_status()
```

## 📋 **Model Management**

### **Adding New Models**
1. **Install in system LM Studio**:
   - Download models to `/home/mccoy/.lmstudio/models/`
   - Or use LM Studio GUI to download models

2. **Restart Docker container**:
   ```bash
   docker compose -f docker/docker-compose.yml restart lm-studio
   ```

3. **Verify access**:
   ```bash
   curl http://localhost:1234/v1/models
   ```

### **Model Configuration**
- Models use the same configuration as your system installation
- Settings are preserved in `/app/.lmstudio/`
- No additional configuration needed

## 🔍 **Verification Steps**

### **1. Check Volume Mounts**
```bash
docker inspect living_truth_lm_studio --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'
```

### **2. List Models in Container**
```bash
docker exec living_truth_lm_studio ls -la /app/models/
```

### **3. Test API Access**
```bash
curl http://localhost:1234/v1/models
```

### **4. Test MCP Tools**
```python
# Using the MCP server
mcp_living_truth_fastmcp_server_get_lm_studio_models()
mcp_living_truth_fastmcp_server_test_lm_studio_connection()
```

## 🎯 **Benefits**

### **1. Unified Model Access**
- Same models available in both system and Docker
- No need to duplicate model files
- Consistent model versions

### **2. Easy Management**
- Install models once in system LM Studio
- Automatically available in Docker container
- No additional configuration required

### **3. Performance**
- Models run in optimized container environment
- No performance overhead from volume mounting
- Efficient resource utilization

### **4. Integration**
- Seamless integration with Living Truth Engine
- MCP server tools for model management
- API access for external applications

## 🚨 **Troubleshooting**

### **Models Not Visible**
1. **Check volume mounts**:
   ```bash
   docker inspect living_truth_lm_studio --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}'
   ```

2. **Verify model directory**:
   ```bash
   ls -la /home/mccoy/.lmstudio/models/
   ```

3. **Restart container**:
   ```bash
   docker compose -f docker/docker-compose.yml restart lm-studio
   ```

### **Connection Issues**
1. **Check container status**:
   ```bash
   docker ps | grep lm-studio
   ```

2. **Test API endpoint**:
   ```bash
   curl http://localhost:1234/v1/models
   ```

3. **Check logs**:
   ```bash
   docker logs living_truth_lm_studio
   ```

## 📊 **Current Status**
- ✅ **Volume mounts configured** correctly
- ✅ **Models accessible** in container
- ✅ **API responding** on port 1234
- ✅ **MCP tools working** for model access
- ✅ **Connection tested** and verified

---

**Status**: ✅ **OPERATIONAL** - Docker LM Studio can access all system models.

**Last Updated**: August 1, 2025
**Updated By**: AI Assistant
**Reason**: LM Studio model access configuration and verification 