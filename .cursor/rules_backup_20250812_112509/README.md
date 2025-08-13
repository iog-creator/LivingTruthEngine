# Living Truth Engine - Cursor Rules

## Overview
This directory contains comprehensive cursor rules for the Living Truth Engine project, ensuring consistent development practices, code quality, and system management.

## 📋 **Available Rules**

### **1. Project Overview** (`project_overview.mdc`)
- **Purpose**: Comprehensive project overview and architecture
- **Scope**: All files (`**/*`)
- **Always Apply**: Yes
- **Key Topics**:
  - Project architecture and components
  - Technology stack and dependencies
  - Development guidelines and workflows
  - Quality metrics and monitoring
  - Troubleshooting procedures

### **2. Coding Standards** (`coding_standards.mdc`)
- **Purpose**: AI-optimized coding standards
- **Scope**: Python, JavaScript, TypeScript, JSON files
- **Always Apply**: Yes
- **Key Topics**:
  - Type hints and docstrings (required)
  - Naming conventions and patterns
  - Error handling and logging
  - Code organization and structure
  - AI understanding optimization

### **3. Development Workflow** (`development_workflow.mdc`)
- **Purpose**: AI-assisted development process
- **Scope**: Python, JavaScript, TypeScript, Shell, Markdown files
- **Always Apply**: Yes
- **Key Topics**:
  - AI-assisted code generation
  - Testing and validation procedures
  - Documentation standards
  - MCP server integration
  - Quality assurance processes

### **4. Docker Best Practices** (`docker_best_practices.mdc`)
- **Purpose**: Modern Docker configuration and deployment
- **Scope**: Docker files and configurations
- **Always Apply**: Yes
- **Key Topics**:
  - Docker Compose v2 syntax
  - Security best practices (non-root users)
  - Performance optimization (BuildKit, slim images)
  - Health checks and monitoring
  - Volume and network configuration

### **5. System Management** (`system_management.mdc`)
- **Purpose**: Environment and automation management
- **Scope**: Shell scripts, Python files, configuration files
- **Always Apply**: Yes
- **Key Topics**:
  - Virtual environment management
  - System updates and maintenance
  - Automation scripts and workflows
  - Monitoring and validation
  - Troubleshooting procedures

### **6. MCP Server Integration** (`mcp_server_integration.mdc`)
- **Purpose**: MCP server configuration and tool usage
- **Scope**: Python files, MCP server files, configuration
- **Always Apply**: Yes
- **Key Topics**:
  - MCP server setup and configuration
  - Tool naming conventions (<60 characters)
  - Error handling and fallbacks
  - Performance monitoring
  - Troubleshooting and recovery

## 🎯 **Rule Dependencies**

```
project_overview.mdc
├── coding_standards.mdc
├── development_workflow.mdc
├── docker_best_practices.mdc
├── system_management.mdc
└── mcp_server_integration.mdc
```

## 📊 **Rule Coverage**

### **File Types Covered**
- ✅ **Python** (`.py`) - All rules apply
- ✅ **JavaScript/TypeScript** (`.js`, `.ts`) - Coding standards, workflow
- ✅ **Shell Scripts** (`.sh`) - System management, workflow
- ✅ **Docker Files** (Dockerfile, docker-compose.yml) - Docker best practices
- ✅ **Configuration** (`.json`, `.env`) - System management, MCP integration
- ✅ **Documentation** (`.md`) - Workflow, project overview

### **Development Areas Covered**
- ✅ **Code Quality** - Type hints, docstrings, error handling
- ✅ **System Management** - Environment, automation, monitoring
- ✅ **Docker Configuration** - Security, performance, best practices
- ✅ **MCP Integration** - Tool usage, error handling, monitoring
- ✅ **Project Architecture** - Overview, guidelines, workflows

## 🚀 **Usage Guidelines**

### **For Developers**
1. **Always reference relevant rules** when working on specific areas
2. **Follow rule checklists** before committing code
3. **Use rule examples** as templates for new code
4. **Update rules** when patterns or requirements change
5. **Validate against rules** during code review

### **For AI Assistance**
1. **Reference specific rules** using `@ruleName` syntax
2. **Follow rule patterns** for consistent code generation
3. **Use rule examples** as templates
4. **Apply rule checklists** before completing tasks
5. **Suggest rule updates** when improvements are identified

## 🔧 **Rule Maintenance**

### **When to Update Rules**
- **New patterns** emerge in the codebase
- **Technology stack** changes or updates
- **Best practices** evolve or improve
- **Project requirements** change
- **Issues** are identified in current rules

### **How to Update Rules**
1. **Identify the need** for rule changes
2. **Update the specific rule** with new content
3. **Update cross-references** in other rules
4. **Test the changes** with actual development work
5. **Document the changes** in this README

## 📈 **Quality Metrics**

### **Rule Effectiveness**
- **Coverage**: 100% of development areas covered
- **Consistency**: Standardized patterns across all rules
- **Clarity**: Clear, actionable guidance
- **Maintainability**: Easy to update and extend
- **Integration**: Cross-referenced and interconnected

### **Development Impact**
- **Code Quality**: Improved type coverage and documentation
- **System Reliability**: Better Docker and system management
- **Development Speed**: Faster AI-assisted development
- **Error Reduction**: Fewer common mistakes
- **Team Consistency**: Standardized development practices

---

**These rules provide a comprehensive foundation for consistent, high-quality development of the Living Truth Engine project.** 