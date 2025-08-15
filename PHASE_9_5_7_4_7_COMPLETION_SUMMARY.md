---
phase: 9.5.7.4.7
status: completed
completion_date: 2025-08-14
depends_on:
  - 9.5.7.4.6
summary: SSOT Validator Stabilization — scopes, budgets, bounded reads; CI fast; nightly full; LM Studio fast verify; handoff doc.
---

## Deliverables
- `.config/ssot.yml` (scan budgets, limits, globs)
- `scripts/_ssot/paths.py` (bounded file walker)
- Updated `verify_complete_ssot_system.py` (scope/budget support)
- CI workflows: `ssot-guard.yml` (FAST) and `ssot-nightly.yml` (FULL)
- Handoff: `HANDOFF_SSOT_AGENT.md`

## Acceptance
- `make check` returns in < 1 min
- CI PRs green with FAST scope
- Nightly FULL artifacts available
- LM Studio `/tools/verify_ssot` is responsive
