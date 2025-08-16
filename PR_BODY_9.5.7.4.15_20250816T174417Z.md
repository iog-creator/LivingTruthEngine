# Phase 9.5.7.4.15 — MCP-first loop hardened ✅

## What's in this PR
- Dashboard mount: `../reports:/app/reports` (canonical compose path).
- SSOT Watchdog endpoints visible in UI and API.
- Make target `dash-ssot-check` for one-command verification.
- Cursor rule `dashboard_ssot_watchdog.mdc` (minimal frontmatter + SSOT Meta in body).
- SSOT gates (meta index/validate + fast verify) re-run and passing.

## Checks
- [x] `make snapshot`
- [x] `make dash-ssot-check`
- [x] `/api/ssot/snapshot/latest` ⇒ `{status:"ok", data.file}` not null
- [x] Meta index + validate pass
- [x] Commit prefixed `[SSOT Verified]`

## Notes
- This locks MCP→snapshot→dashboard so regressions surface immediately.
- Next phase: Playwright e2e for the Advanced → SSOT Watchdog card; optional CI job to run `dash-ssot-check`.
