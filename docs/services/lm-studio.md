---
phase: 9.5.7
status: active
last_reviewed: 2025-08-14
related_files: []
---

# Service: lm-studio

## Role
(brief)

## Ports
- 1235:1234

## Environment
- `HOST`: `0.0.0.0`
- `PORT`: `1234`
- `MODELS_PATH`: `/app/models`
- `CONFIG_PATH`: `/app/.lmstudio`
- `LOG_LEVEL`: `INFO`
- `DEVICE`: `auto`
- `THREADS`: `auto`
- `CONTEXT_LENGTH`: `4096`
- `BATCH_SIZE`: `512`
- `GPU_LAYERS`: `0`
- `CPU_ONLY`: `False`
- `VERBOSE`: `False`
- `QUIET`: `False`
- `HELP`: `False`
- `VERSION`: `False`
- `MODEL`: ``
- `CONFIG`: ``
- `PROMPT`: ``
- `SYSTEM`: ``
- `TEMPLATE`: ``
- `STOP`: ``
- `REPEAT_PENALTY`: `1.1`
- `REPEAT_PENALTY_TOKENS`: `64`
- `TEMPERATURE`: `0.7`
- `TOP_P`: `0.9`
- `TOP_K`: `40`
- `TFS_Z`: `1.0`
- `TYPICAL_P`: `1.0`
- `MIROSTAT`: `0`
- `MIROSTAT_TAU`: `5.0`
- `MIROSTAT_ETA`: `0.1`
- `MULTILINE_INPUT`: `False`
- `SIMPLE_UI`: `False`
- `COLOR`: `False`
- `MLOCK`: `False`
- `MMAP`: `True`
- `NUM_PREDICT`: `128`
- `N_KEEP`: `0`
- `N_PROBS`: `0`
- `LOGIT_BIAS`: ``
- `IGNORE_EOS`: `False`
- `INTERACTIVE`: `False`
- `INTERACTIVE_FIRST`: `False`
- `INTERACTIVE_SPEC`: ``
- `INVERSE_PROP`: `False`
- `LOGDISABLE`: `False`
- `LOGDIR`: ``
- `LOGFILE`: ``
- `LOG_NEWLINE`: `False`
- `LOG_TIMESTAMP`: `False`

## Healthcheck
- Test: `['CMD-SHELL', "timeout 10 bash -c '</dev/tcp/localhost/1234' || exit 1"]`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
