# Deployment Guide

## Description
This document provides comprehensive deployment instructions for the Living Truth Engine, including environment setup, service deployment, and configuration management.

## 🎯 **Prerequisites**

### **System Requirements**
- **Operating System**: Linux (Ubuntu 22.04+ recommended)
- **Docker**: Version 20.10+ with Docker Compose v2
- **Python**: Version 3.12+ with virtual environment support
- **Memory**: Minimum 8GB RAM (16GB+ recommended)
- **Storage**: Minimum 50GB available disk space
- **Network**: Internet access for package downloads and model access

### **Required Software**
```bash
# Install Docker and Docker Compose
sudo apt update
sudo apt install docker.io docker-compose-plugin

# Install Python 3.12+
sudo apt install python3.12 python3.12-venv python3.12-pip

# Install Git
sudo apt install git

# Install additional dependencies
sudo apt install curl wget jq
```

## 🔧 **Environment Setup**

### **1. Clone Repository**
```bash
git clone https://github.com/iog-creator/LivingTruthEngine.git
cd LivingTruthEngine
```

### **2. Create Virtual Environment**
```bash
python3.12 -m venv living_venv
source living_venv/bin/activate
pip install --upgrade pip
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Configuration**
```bash
# Copy environment template
cp env.template .env

# Edit environment variables
nano .env
```

### **Required Environment Variables**
```bash
# Langflow Configuration
LANGFLOW_API_ENDPOINT=http://localhost:7860
LANGFLOW_API_KEY=your_api_key_here
LANGFLOW_PROJECT_ID=your_project_id_here

# Database Configuration
POSTGRES_DB=living_truth_engine
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# Service Endpoints
LM_STUDIO_ENDPOINT=http://localhost:1234

# Python Path
PYTHONPATH=/path/to/LivingTruthEngine/src
```

## 🐳 **Docker Deployment**

### **1. Start All Services**
```bash
# Start all services in background
docker compose -f docker/docker-compose.yml up -d

# Check service status
docker compose -f docker/docker-compose.yml ps
```

### **2. Verify Service Health**
```bash
# Check individual service health
curl -f http://localhost:7860/health  # Langflow
curl -f http://localhost:1234/v1/models  # LM Studio
curl -f http://localhost:7474/  # Neo4j
redis-cli ping  # Redis
```

### **3. Service Ports and Access**
- **Langflow**: http://localhost:7860 (admin/admin)
- **Dash Dashboard**: http://localhost:8050
- **Neo4j Browser**: http://localhost:7474
- **LM Studio**: http://localhost:1234

## 🔧 **MCP Server Setup**

### **1. Start MCP Hub Server**
```bash
# Activate virtual environment
source living_venv/bin/activate

# Start MCP Hub Server
python3 src/mcp_servers/mcp_hub_server.py &
```

### **2. Verify MCP Server Status**
```bash
# Check if MCP Hub Server is running
ps aux | grep mcp_hub_server

# Test MCP server functionality
python3 -c "
import sys; sys.path.append('src')
from mcp_servers.mcp_hub_server import MCPHubServer
server = MCPHubServer()
print('MCP Hub Server loaded with:', server.registry.get('total_tools', 0), 'tools')
"
```

### **3. Cursor Integration**
Ensure `.cursor/mcp.json` is configured correctly:
```json
{
  "mcpServers": {
    "mcp_hub_server": {
      "command": "python3",
      "args": ["/path/to/LivingTruthEngine/src/mcp_servers/mcp_hub_server.py"],
      "env": {
        "LANGFLOW_API_ENDPOINT": "http://localhost:7860",
        "LANGFLOW_API_KEY": "${LANGFLOW_API_KEY}",
        "LANGFLOW_PROJECT_ID": "${LANGFLOW_PROJECT_ID}",
        "LM_STUDIO_ENDPOINT": "http://localhost:1234",
        "PYTHONPATH": "/path/to/LivingTruthEngine/src"
      }
    }
  }
}
```

## 🧪 **Testing and Validation**

### **1. Run Functional Tests**
```bash
# Run comprehensive functional tests
python3 scripts/testing/functional_tests.py

# Run performance tests
./scripts/testing/trace_performance.sh

# Run simple performance tests
./scripts/testing/simple_performance_test.sh
```

### **2. Verify System Health**
```bash
# Check all services
./scripts/setup/check_system.sh

# Validate Docker setup
./scripts/setup/validate_docker.sh
```

### **3. Test MCP Tools**
```bash
# Test MCP Hub Server tools
python3 -c "
import sys; sys.path.append('src')
from mcp_servers.mcp_hub_server import MCPHubServer
server = MCPHubServer()
result = server.execute_tool('get_status', {})
print('System status:', result)
"
```

## 📊 **Monitoring and Maintenance**

### **1. Service Monitoring**
```bash
# Monitor service logs
docker compose -f docker/docker-compose.yml logs -f

# Check resource usage
docker stats

# Monitor system resources
htop
```

### **2. Backup Procedures**
```bash
# Backup database
docker exec living-truth-postgres pg_dump -U postgres living_truth_engine > backup.sql

# Backup configuration
tar -czf config_backup.tar.gz config/ .env

# Backup data
tar -czf data_backup.tar.gz data/
```

### **3. Update Procedures**
```bash
# Update system components
./scripts/setup/update_system.sh

# Restart services
docker compose -f docker/docker-compose.yml restart

# Update MCP server
pkill -f mcp_hub_server
python3 src/mcp_servers/mcp_hub_server.py &
```

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Service Startup Failures**
```bash
# Check service logs
docker compose -f docker/docker-compose.yml logs service_name

# Restart specific service
docker compose -f docker/docker-compose.yml restart service_name

# Check port conflicts
netstat -tulpn | grep :port_number
```

#### **2. MCP Server Issues**
```bash
# Check MCP server status
ps aux | grep mcp_hub_server

# Restart MCP server
pkill -f mcp_hub_server
python3 src/mcp_servers/mcp_hub_server.py &

# Check registry
python3 -c "import json; data=json.load(open('config/tool_registry.json')); print('Tools:', data.get('total_tools', 0))"
```

#### **3. Performance Issues**
```bash
# Check resource usage
docker stats
htop

# Monitor performance
./scripts/testing/trace_performance.sh

# Check logs for errors
tail -f logs/*.log
```

### **Recovery Procedures**

#### **1. Service Recovery**
```bash
# Stop all services
docker compose -f docker/docker-compose.yml down

# Clean up containers
docker system prune -f

# Restart services
docker compose -f docker/docker-compose.yml up -d
```

#### **2. Data Recovery**
```bash
# Restore database
docker exec -i living-truth-postgres psql -U postgres living_truth_engine < backup.sql

# Restore configuration
tar -xzf config_backup.tar.gz

# Restore data
tar -xzf data_backup.tar.gz
```

#### **3. MCP Server Recovery**
```bash
# Regenerate tool registry
python3 scripts/setup/regenerate_tool_registry.py

# Restart MCP server
pkill -f mcp_hub_server
python3 src/mcp_servers/mcp_hub_server.py &
```

## 🔒 **Security Considerations**

### **1. Environment Security**
- **Secure passwords**: Use strong, unique passwords for all services
- **API keys**: Store API keys securely and rotate regularly
- **Network security**: Use firewalls and VPNs for remote access
- **Access control**: Implement proper user authentication and authorization

### **2. Data Security**
- **Encryption**: Enable encryption for data at rest and in transit
- **Backup security**: Secure backup storage and access
- **Audit logging**: Enable comprehensive audit logging
- **Data retention**: Implement proper data retention policies

### **3. Service Security**
- **Container security**: Use security scanning for Docker images
- **Service isolation**: Implement proper network isolation
- **Update management**: Regular security updates and patches
- **Monitoring**: Security monitoring and alerting

## 📈 **Scaling and Optimization**

### **1. Horizontal Scaling**
```bash
# Scale specific services
docker compose -f docker/docker-compose.yml up -d --scale service_name=3

# Load balancing configuration
# Add load balancer configuration for multiple instances
```

### **2. Performance Optimization**
```bash
# Optimize database queries
# Add database indexes and query optimization

# Optimize caching
# Configure Redis caching strategies

# Optimize resource allocation
# Adjust Docker resource limits
```

### **3. Monitoring and Alerting**
```bash
# Set up monitoring dashboards
# Configure alerting for critical metrics

# Performance tracking
# Monitor response times and resource usage
```

## 🎯 **Success Metrics**

### **Deployment Success Criteria**
- ✅ **All services running**: 7 Docker services operational
- ✅ **MCP Hub Server active**: 15 meta-tools accessible
- ✅ **Functional tests passing**: 12/13 tests passing (92% success)
- ✅ **Performance targets met**: <2s response time for all services
- ✅ **Health checks passing**: All services responding to health checks

### **Operational Metrics**
- **Service uptime**: 99.9% availability
- **Response time**: <2 seconds for all API calls
- **Error rate**: <1% error rate
- **Resource utilization**: <80% CPU and memory usage

---

**This deployment guide ensures successful deployment and operation of the Living Truth Engine with proper monitoring, maintenance, and troubleshooting procedures.** 