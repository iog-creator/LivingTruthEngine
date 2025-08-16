# SSOT Metadata — How to Add Rich YAML (Without Breaking Cursor)

Cursor rules require **minimal frontmatter**:
```yaml
---
description: <short rule description>
# globs: "src/**/*.ts"      # optional → Auto-Attached
# alwaysApply: true         # optional → Always
---
```

To attach richer, machine-readable metadata (owners, severity, tags, budgets, etc.) **without** touching the frontmatter, add this block anywhere in the Markdown body:

```md
### SSOT Meta

```yaml
owner: team-ssot
severity: high            # low|medium|high|critical
tags: [ssot, rules, guard]
phase: 9.5.7.4.10
dependsOn: [verify-complete-ssot, mcp-router-check]
autofixAllowed: false
notes: "Enforce SSOT gates on every commit"
```
```

> You can add **one** SSOT Meta block per rule/doc. The metadata is harvested by `make meta-index` into `reports/ssot_meta_index.json`.

## Generate / View the Index
```bash
make meta-index
cat reports/ssot_meta_index.json | jq .
```

## What we do with this metadata
- **Dashboards**: show counts by owner, severity, tags.
- **Routing hints**: prioritize tools/agents based on tags or severity.
- **Gates**: in future phases we can fail builds when `autofixAllowed: false` and a tool suggests a write, etc.

## Compatibility
This pattern **keeps Cursor happy**: minimal frontmatter stays canonical; SSOT Meta lives in the body and is ignored by Cursor but indexed by our tooling.
