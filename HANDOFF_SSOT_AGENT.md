---
title: SSOT Orchestrator + LM Studio Integration — Handoff
phase: 9.5.7.4.7
status: active
summary: How to run, extend, and keep the SSOT validator + LM Studio copilot stable.
---

## What exists
- **SSOT validator**: `scripts/verify_complete_ssot_system.py` (now with `--scope fast|full|ai`, time budgets, bounded reads).
- **LM Studio bridge**: `scripts/bridge/lmstudio_tools_bridge.py` (read-only tools; uses FAST scope).
- **LangChain copilot** (optional): `scripts/agent/ssot_copilot.py` (local triage; read-only by default).
- **CI**: PRs run FAST scope; Nightly runs FULL sweep; artifacts in `reports/`.

## Rituals
- Pre-edit (Cursor): `python scripts/verify_complete_ssot_system.py --scope fast`
- After edits (local): `python scripts/verify_complete_ssot_system.py --scope full --fix`
- Bridge: `make lm-tools` → LM Studio calls `/tools/verify_ssot` (FAST)
- Optional AI triage: `make ai-quick` (no repo writes)

## Guards
- CI never enables AI; LM Studio bridge is read-only; Cursor remains executor.
- Budgets: adjust in `.config/ssot.yml` under `scan.time_budget` and `scan.max_files`.
- Do not expand include globs without increasing budgets.

## Acceptance
- FAST completes < 1 min on PRs.
- FULL completes nightly and uploads reports.
- No hanging scans; LM Studio verify call returns promptly.
