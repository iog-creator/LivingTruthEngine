# SSOT Meta — Suggested Schema (optional)

Add rich YAML in a rule/doc body under:
```md
### SSOT Meta
```yaml
owner: researcher-ssot         # string
severity: high                 # one of: low|medium|high|critical
tags: [ssot, rules, guard]     # list of strings
phase: 9.5.7.4.12              # dotted numbers
dependsOn: [verify-ssot, mcp-router-check]   # list of strings
autofixAllowed: false          # boolean
notes: "human note"            # string, optional
```
```

The validator accepts unknown keys (forward-compatible) but **validates types** for the keys above.

## Freshness
`make meta-validate` fails if `reports/ssot_meta_index.json` is older than the latest change in:
- `.cursor/rules/*.mdc`
- SSOT core docs (README, project_master_log, etc.)
- `PHASE_*_COMPLETION_SUMMARY.md`

Run `make meta-index` (or `make reports`) to refresh.
