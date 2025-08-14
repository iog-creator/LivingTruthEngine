---
phase: 9.5.7
status: active
last_reviewed: 2025-08-14
related_files: []
---

# Service: langflow

## Role
(brief)

## Ports
- 7860:7860

## Environment
- `LANGFLOW_DATABASE_URL=postgresql://langflow:langflow@postgres:5432/langflow`
- `LANGFLOW_CONFIG_DIR=/app/langflow`
- `PYTHONPATH=/app/langflow_source:/app/langchain_source`

## Healthcheck
- Test: `['CMD', 'curl', '-f', 'http://localhost:7860/health']`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
