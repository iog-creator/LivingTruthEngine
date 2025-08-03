# System Architecture

## Description
This document provides a comprehensive overview of the Living Truth Engine system architecture, including service components, data flow, and integration patterns.

## 🎯 **System Overview**

### **Living Truth Engine**
The Living Truth Engine is an AI-powered system for survivor testimony corroboration and evidence analysis. It combines multiple technologies to provide comprehensive analysis capabilities, using multiple sources (including but not limited to Biblical references) to find supporting evidence and make connections.

### **Core Architecture Principles**
- **Modular Design**: Independent services with clear interfaces
- **Scalability**: Horizontal scaling capabilities for all components
- **Reliability**: Redundancy and failover mechanisms
- **Performance**: Optimized for real-time analysis and processing
- **Security**: Secure data handling and access controls

## 🏗️ **Service Architecture**

### **Docker Services (LivingTruthEngine Project)**

#### **1. Neo4j Graph Database**
- **Container**: `living-truth-neo4j`
- **Ports**: 7474 (HTTP), 7687 (Bolt)
- **Purpose**: Relationship analysis and graph data storage
- **Features**:
  - Graph database for complex relationship mapping
  - Cypher query language for graph operations
  - Web interface for data exploration
  - Relationship analysis for survivor testimony

#### **2. Redis Cache**
- **Container**: `living-truth-redis`
- **Port**: 6379
- **Purpose**: Caching and session management
- **Features**:
  - High-performance caching layer
  - Session state management
  - Temporary data storage
  - Performance optimization

#### **3. PostgreSQL Database**
- **Container**: `living-truth-postgres`
- **Port**: 5432
- **Purpose**: Primary data storage and Langflow database
- **Features**:
  - Relational data storage
  - Langflow workflow data
  - User management and authentication
  - Data integrity and ACID compliance

#### **4. Langflow Workflow Engine**
- **Container**: `living-truth-langflow`
- **Port**: 7860
- **Purpose**: AI workflow orchestration and management
- **Features**:
  - Visual workflow builder
  - Multi-agent orchestration
  - Python native integration
  - JSON import/export capabilities

#### **5. LM Studio Model Hosting**
- **Container**: `living-truth-lm-studio`
- **Port**: 1234
- **Purpose**: Local model hosting and inference
- **Features**:
  - Local model hosting
  - Text generation and inference
  - Model management and configuration
  - API-compatible interface

#### **6. Living Truth Engine Core**
- **Container**: `living-truth-engine`
- **Ports**: 9123-9124
- **Purpose**: Core analysis engine and API
- **Features**:
  - Survivor testimony analysis
  - Pattern recognition
  - Evidence correlation
  - API endpoints for external access

#### **7. Dash Dashboard**
- **Container**: `living-truth-dashboard`
- **Port**: 8050
- **Purpose**: Interactive data visualization
- **Features**:
  - Network graphs and visualizations
  - Timeline data presentation
  - Statistical analysis display
  - Interactive user interface

### **MCP Server Architecture**

#### **MCP Hub Server (Primary Gateway)**
- **File**: `src/mcp_servers/mcp_hub_server.py`
- **Purpose**: Single consolidated server providing access to all tools
- **Architecture**: Proxy/Gateway pattern with dynamic tool loading
- **Features**:
  - 15 meta-tools for Cursor integration
  - Access to 63 underlying tools
  - Performance monitoring and optimization
  - Automatic backup and recovery

#### **Underlying MCP Servers (8 servers)**
1. **Living Truth FastMCP Server** (22 tools) - Core analysis engine
2. **Langflow MCP Server** (12 tools) - Workflow management
3. **PostgreSQL MCP Server** (6 tools) - Database operations
4. **Hugging Face MCP Server** (5 tools) - Model access
5. **DevDocs MCP Server** (4 tools) - Documentation retrieval
6. **Rulego MCP Server** (5 tools) - Workflow orchestration
7. **MCP Solver Server** (5 tools) - Constraint solving
8. **GitHub MCP Server** (4 tools) - Repository management

## 📊 **Data Flow Architecture**

### **Input Processing**
```
User Input → API Gateway → Living Truth Engine → Analysis Pipeline
```

### **Analysis Pipeline**
```
Transcript Data → Text Processing → Pattern Recognition → Evidence Correlation → Results
```

### **Data Storage**
```
Raw Data → PostgreSQL (structured) → Neo4j (relationships) → Redis (cache)
```

### **Output Generation**
```
Analysis Results → Visualization Engine → Dash Dashboard → User Interface
```

## 🔧 **Integration Patterns**

### **Service Communication**
- **REST APIs**: Standard HTTP-based communication
- **GraphQL**: Flexible data querying for complex relationships
- **Message Queues**: Asynchronous processing for heavy workloads
- **Event Streaming**: Real-time data processing and analysis

### **Data Integration**
- **ETL Pipelines**: Extract, Transform, Load processes
- **Real-time Streaming**: Live data processing and analysis
- **Batch Processing**: Large-scale data analysis and correlation
- **Incremental Updates**: Efficient data synchronization

### **External Integrations**
- **API Gateways**: Secure external access and rate limiting
- **Authentication**: OAuth2 and JWT-based security
- **Rate Limiting**: Protection against abuse and overload
- **Monitoring**: Comprehensive logging and metrics

## 🛡️ **Security Architecture**

### **Authentication & Authorization**
- **Multi-factor Authentication**: Enhanced security for sensitive operations
- **Role-based Access Control**: Granular permissions and access management
- **API Key Management**: Secure API access and usage tracking
- **Session Management**: Secure user session handling

### **Data Security**
- **Encryption at Rest**: All data encrypted in storage
- **Encryption in Transit**: TLS/SSL for all communications
- **Data Masking**: Sensitive data protection and anonymization
- **Audit Logging**: Comprehensive security event tracking

### **Network Security**
- **Firewall Protection**: Network-level security controls
- **VPC Isolation**: Virtual private cloud for service isolation
- **Load Balancing**: Distributed traffic and DDoS protection
- **SSL/TLS Termination**: Secure communication handling

## 📈 **Performance Architecture**

### **Scaling Strategies**
- **Horizontal Scaling**: Add more instances for increased capacity
- **Vertical Scaling**: Increase resources for individual services
- **Auto-scaling**: Automatic resource allocation based on demand
- **Load Balancing**: Distribute traffic across multiple instances

### **Performance Optimization**
- **Caching Layers**: Multi-level caching for improved response times
- **Database Optimization**: Query optimization and indexing
- **CDN Integration**: Content delivery for global performance
- **Compression**: Data compression for reduced bandwidth usage

### **Monitoring & Alerting**
- **Real-time Monitoring**: Live performance and health tracking
- **Performance Metrics**: Response times, throughput, and resource usage
- **Alert Systems**: Automated notifications for issues and anomalies
- **Capacity Planning**: Predictive scaling based on usage patterns

## 🔄 **Deployment Architecture**

### **Container Orchestration**
- **Docker Compose**: Local development and testing
- **Kubernetes**: Production deployment and scaling
- **Service Mesh**: Advanced service-to-service communication
- **Helm Charts**: Kubernetes deployment automation

### **CI/CD Pipeline**
- **Source Control**: Git-based version control and collaboration
- **Automated Testing**: Comprehensive test suite execution
- **Build Automation**: Automated build and packaging
- **Deployment Automation**: Automated deployment and rollback

### **Environment Management**
- **Development**: Local development environment
- **Staging**: Pre-production testing and validation
- **Production**: Live system with high availability
- **Disaster Recovery**: Backup and recovery procedures

## 📊 **Monitoring & Observability**

### **Logging Strategy**
- **Centralized Logging**: Unified log collection and analysis
- **Structured Logging**: Consistent log format and parsing
- **Log Levels**: Appropriate logging levels for different environments
- **Log Retention**: Configurable log retention and archival

### **Metrics Collection**
- **Application Metrics**: Custom application performance metrics
- **Infrastructure Metrics**: System and resource utilization
- **Business Metrics**: Key performance indicators and business metrics
- **Real-time Dashboards**: Live monitoring and visualization

### **Tracing & Profiling**
- **Distributed Tracing**: End-to-end request tracing
- **Performance Profiling**: Detailed performance analysis
- **Error Tracking**: Comprehensive error monitoring and alerting
- **User Experience**: Real user monitoring and feedback

## 🎯 **Success Metrics**

### **Performance Metrics**
- **Response Time**: <2 seconds for all API calls
- **Throughput**: 1000+ requests per second
- **Availability**: 99.9% uptime
- **Error Rate**: <1% error rate

### **Scalability Metrics**
- **Horizontal Scaling**: Linear scaling with additional instances
- **Resource Utilization**: <80% CPU and memory usage
- **Database Performance**: <1 second query response times
- **Cache Hit Rate**: >90% cache hit rate

### **Reliability Metrics**
- **Service Uptime**: 99.9% availability
- **Data Integrity**: 100% data consistency
- **Recovery Time**: <5 minutes for service recovery
- **Backup Success**: 100% backup and recovery success

---

**This system architecture provides a robust, scalable, and performant foundation for the Living Truth Engine, ensuring high availability, security, and reliability for all operations.** 