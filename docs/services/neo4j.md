---
phase: 9.5.7
status: active
last_reviewed: 2025-08-14
related_files: []
---

# Service: neo4j

## Role
(brief)

## Ports
- 7474:7474
- 7687:7687

## Environment
- `NEO4J_AUTH`: `neo4j/livingtruth123`
- `NEO4J_PLUGINS`: `["apoc"]`
- `NEO4J_dbms_security_procedures_unrestricted`: `apoc.*`

## Healthcheck
- Test: `['CMD-SHELL', "cypher-shell -u neo4j -p livingtruth123 'RETURN 1'"]`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
