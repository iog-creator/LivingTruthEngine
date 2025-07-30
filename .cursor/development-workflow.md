# Living Truth Engine - Development Workflow

## Overview

This document outlines the development workflow for the Living Truth Engine project, including best practices, coding standards, and collaboration guidelines.

## Development Environment Setup

### Prerequisites
- **Python 3.13+**: Core development language
- **Node.js 18+**: For Flowise installation
- **PostgreSQL 12+**: Database with PGVector extension
- **Cursor IDE**: Primary development environment
- **Git**: Version control

### Initial Setup
```bash
# Clone repository
git clone <repository-url>
cd LivingTruthEngine

# Create virtual environment
python -m venv living_venv
source living_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Flowise
npm install -g flowise

# Setup database
createdb living_truth_engine
psql -d living_truth_engine -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## Development Workflow

### 1. Environment Management

#### Virtual Environment
- **Always use `living_venv`**: Never use system Python
- **Activation**: `source living_venv/bin/activate`
- **Verification**: `which python` should point to `living_venv/bin/python`

#### Environment Variables
- **Configuration**: Use `.env` file for all settings
- **Never hardcode**: API keys, database credentials, etc.
- **Template**: Copy `.env.example` and fill in values

### 2. Code Development

#### File Management
- **Check existing files**: Use `file_search()` and `grep_search()` before creating
- **Update over create**: Modify existing files instead of creating duplicates
- **Preserve history**: Comment out rather than delete original code

#### Coding Standards
- **PEP 8**: Follow Python style guidelines
- **Type hints**: Use comprehensive type annotations
- **Documentation**: Docstrings for all functions and classes
- **Error handling**: Proper exception handling and logging

#### MCP Server Development
- **Tool definitions**: Add to `list_tools()` method
- **Implementation**: Create corresponding private methods
- **Testing**: Test with JSON-RPC protocol
- **Documentation**: Update MCP server docs

### 3. Flowise Integration

#### Graph Development
- **Visual editing**: Use Flowise UI at http://localhost:3000
- **Configuration**: Export graphs as JSON
- **Version control**: Commit graph changes
- **Testing**: Test flows before committing

#### Node Development
- **Custom nodes**: Python/JavaScript implementation
- **Error handling**: Robust error handling in nodes
- **Documentation**: Clear node descriptions
- **Testing**: Test nodes individually

### 4. Testing Strategy

#### Unit Testing
```python
# Example test structure
def test_query_flowise():
    """Test query_flowise tool functionality"""
    server = FlowiseMCPServer()
    result = server._query_flowise({
        "query": "test query",
        "anonymize": False,
        "output_type": "summary"
    })
    assert "result" in result
```

#### Integration Testing
- **End-to-end**: Test complete workflows
- **API testing**: Test Flowise API integration
- **Database testing**: Test vector store operations
- **Performance testing**: Load and stress testing

#### Manual Testing
- **MCP server**: Test tool listing and execution
- **Flowise UI**: Test graph functionality
- **Dashboard**: Test visualization outputs
- **Documentation**: Verify documentation accuracy

### 5. Documentation

#### Code Documentation
- **Docstrings**: Comprehensive function documentation
- **Type hints**: Clear parameter and return types
- **Comments**: Explain complex logic
- **Examples**: Include usage examples

#### Project Documentation
- **README.md**: Project overview and setup
- **API documentation**: Tool and endpoint documentation
- **Architecture docs**: System design and components
- **Troubleshooting**: Common issues and solutions

### 6. Version Control

#### Git Workflow
```bash
# Feature development
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature: description"
git push origin feature/new-feature

# Code review and merge
git checkout main
git merge feature/new-feature
git push origin main
```

#### Commit Standards
- **Conventional commits**: Use standard commit message format
- **Descriptive messages**: Clear commit descriptions
- **Atomic commits**: One logical change per commit
- **Reference issues**: Link to relevant issues/tickets

### 7. Code Review

#### Review Process
- **Self-review**: Review your own code before submission
- **Peer review**: Have team members review changes
- **Automated checks**: Run linting and tests
- **Documentation review**: Ensure docs are updated

#### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Error handling is appropriate
- [ ] Security considerations addressed
- [ ] Performance impact considered

### 8. Deployment

#### Local Development
- **Environment setup**: Ensure all services running
- **Database migration**: Apply any schema changes
- **Configuration**: Update environment variables
- **Testing**: Run full test suite

#### Production Deployment
- **Environment isolation**: Use production environment
- **Database backup**: Backup before deployment
- **Rollback plan**: Prepare rollback procedures
- **Monitoring**: Set up monitoring and alerting

## Quality Assurance

### Code Quality
- **Linting**: Use flake8, black, mypy
- **Testing**: Maintain high test coverage
- **Security**: Regular security audits
- **Performance**: Monitor performance metrics

### Documentation Quality
- **Accuracy**: Ensure documentation matches code
- **Completeness**: Cover all features and APIs
- **Clarity**: Write for target audience
- **Maintenance**: Keep documentation current

### Process Improvement
- **Retrospectives**: Regular process reviews
- **Feedback**: Collect and act on feedback
- **Metrics**: Track development metrics
- **Automation**: Automate repetitive tasks

## Collaboration Guidelines

### Communication
- **Clear communication**: Use clear, concise language
- **Documentation**: Document decisions and rationale
- **Feedback**: Provide constructive feedback
- **Knowledge sharing**: Share knowledge and best practices

### Team Coordination
- **Code ownership**: Clear ownership of components
- **Dependencies**: Communicate dependencies early
- **Timeline management**: Realistic timelines and milestones
- **Risk management**: Identify and mitigate risks

### Conflict Resolution
- **Open discussion**: Address conflicts openly
- **Data-driven**: Use data to support decisions
- **Consensus building**: Work toward team consensus
- **Escalation**: Escalate when needed

## Tools and Resources

### Development Tools
- **Cursor IDE**: Primary development environment
- **Git**: Version control
- **Docker**: Containerization (optional)
- **Postman**: API testing

### Monitoring Tools
- **Logs**: Application and error logs
- **Metrics**: Performance and usage metrics
- **Alerts**: Automated alerting system
- **Dashboards**: Monitoring dashboards

### Documentation Tools
- **Markdown**: Documentation format
- **Mermaid**: Diagram generation
- **Swagger**: API documentation
- **Jupyter**: Interactive documentation

## Best Practices

### General Practices
- **Consistency**: Maintain consistent patterns
- **Simplicity**: Keep solutions simple
- **Maintainability**: Write maintainable code
- **Reusability**: Create reusable components

### Security Practices
- **Input validation**: Validate all inputs
- **Authentication**: Proper authentication
- **Authorization**: Appropriate access controls
- **Data protection**: Protect sensitive data

### Performance Practices
- **Optimization**: Optimize for performance
- **Caching**: Use appropriate caching
- **Monitoring**: Monitor performance metrics
- **Scaling**: Design for scalability 