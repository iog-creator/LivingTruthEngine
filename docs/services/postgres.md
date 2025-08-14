---
phase: 9.5.7
status: active
last_reviewed: 2025-08-14
related_files: []
---

# Service: postgres

## Role
(brief)

## Ports
- 5434:5432

## Environment
- `POSTGRES_DB`: `${POSTGRES_DB:-living_truth_engine}`
- `POSTGRES_USER`: `${POSTGRES_USER:-postgres}`
- `POSTGRES_PASSWORD`: `${POSTGRES_PASSWORD:-pass}`
- `POSTGRES_MULTIPLE_DATABASES`: `langflow`

## Healthcheck
- Test: `['CMD', 'pg_isready']`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
