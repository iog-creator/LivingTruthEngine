---
phase: 9.5.7
status: active
last_reviewed: 2025-08-14
related_files: []
---

# Service: living-truth-engine

## Role
(brief)

## Ports
- 9123:8000
- 9124:8001

## Environment
- `POSTGRES_HOST`: `postgres`
- `POSTGRES_PORT`: `5432`
- `POSTGRES_DB`: `living_truth_engine`
- `POSTGRES_USER`: `postgres`
- `POSTGRES_PASSWORD`: `pass`
- `NEO4J_URI`: `bolt://neo4j:7687`
- `NEO4J_USER`: `neo4j`
- `NEO4J_PASSWORD`: `livingtruth123`
- `REDIS_HOST`: `redis`
- `REDIS_PORT`: `6379`
- `REDIS_DB`: `0`
- `LOG_LEVEL`: `INFO`
- `ENCRYPTION_KEY`: `${ENCRYPTION_KEY:-default-key-change-in-production}`
- `VISION_MODEL`: `google/gemma-3-4b`
- `LLM_MODEL`: `qwen/qwen3-8b`
- `LMSTUDIO_EMBEDDING_MODEL_QWEN3`: `text-embedding-qwen3-embedding-0.6b`
- `LMSTUDIO_RERANKER_MODEL`: `qwen.qwen3-reranker-0.6b`
- `LMSTUDIO_EMBEDDING_URL`: `http://host.docker.internal:1234/v1/embeddings`
- `LMSTUDIO_CHAT_URL`: `http://host.docker.internal:1234/v1/chat/completions`
- `PYTHONPATH`: `/app`
- `PYTHONUNBUFFERED`: `1`

## Healthcheck
- Test: `['CMD', 'python', '-c', "import requests; requests.get('http://localhost:8000/health')"]`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
