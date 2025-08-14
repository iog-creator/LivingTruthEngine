---
phase: 9.5.7
status: active
last_reviewed: 2025-08-14
related_files: []
---

# Service: dashboard

## Role
(brief)

## Ports
- 8050:8050

## Environment
- `PYTHONPATH=/app:/app/src`
- `LM_STUDIO_ENDPOINT=http://host.docker.internal:1234/v1`

## Healthcheck
- Test: `['CMD', 'curl', '-f', 'http://localhost:8050/api/health']`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
