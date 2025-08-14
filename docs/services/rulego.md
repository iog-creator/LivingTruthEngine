---
phase: 9.5.7
status: active
last_reviewed: 2025-08-14
related_files: []
---

# Service: rulego

## Role
(brief)

## Ports
- 9127:8080

## Environment
- (none)

## Healthcheck
- Test: `['CMD', 'curl', '-f', 'http://localhost:8080/health']`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
