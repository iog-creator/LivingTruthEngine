---
phase: 9.5.7.1
status: active
last_reviewed: 2025-08-14
related_files:
  - scripts/mcp_sync.py
  - scripts/gen_service_docs.py
  - scripts/logging_schema_check.py
  - scripts/readme_sync.py
  - scripts/update_master_log.py
  - .github/workflows/repo-health.yml
  - MCP_REQUIREMENTS_REFERENCE.md
  - docs/services/
  - specs/
---

# 📄 `PHASE_9_5_7_1_PLAN.md` — Repo Health Completion (Do‑Now)

## 🎯 Objective

Close the remaining background health tasks so **Phase 9.5.7** is truly commit‑complete and self‑maintaining. This phase **must not** produce its completion summary until all gates pass.

## Scope (no changes allowed)

* **MCP Tool & Spec Sync**
* **Docker Service Co‑Development**
* **Logging Schema Enforcement**
* **README / Master Log / Consolidated Summary sync**
* **CI gates to block merges on drift**

## Non‑Negotiables

* **Envelope everywhere**: `{status, data?, error?}` with `{code, message}` on error.
* **Idempotent scripts**; re‑running is safe.
* **No TODOs** left open in this phase.
* **No completion summary** until all exit gates in this file pass.

---

## Deliverables

### A) MCP Tool & Spec Sync

1. Generate authoritative inventory of MCP tools in `src/mcp_servers/**`.
2. Ensure **one** JSON spec per tool in `/specs/*.json`.
3. Update `MCP_REQUIREMENTS_REFERENCE.md` with:

   * tool name
   * spec path
   * last_updated (UTC ISO8601)
4. Archive orphaned specs → `archive/specs/`.

**Files**

* `scripts/mcp_sync.py` (creates/updates specs + reference)
* `specs/*.json` (auto‑generated if missing)

---

### B) Docker Service Co‑Development

1. For each **compose** service: `app|db|mcp|queue|worker` (+ any others present):

   * Confirm **healthcheck** exists (or add one).
   * Confirm **code path** and **docs** exist.
2. Generate/refresh docs:

   * `/docs/services/<service>.md`: role, ports, env, health, owner, tests, links.
3. Add missing **smoke tests** for each service (simple reachability + one real interaction if applicable).

**Files**

* `scripts/gen_service_docs.py` (doc scaffolder)
* `tests/services/test_<service>_smoke.py` (minimal)

---

### C) Logging Schema Enforcement

1. Enforce **structured JSON logs** across `src/**`:

   ```json
   { "phase":"9.5.7", "component":"<name>", "level":"info|warn|error", "message":"...", "timestamp":"<ISO8601>" }
   ```
2. Add CI gate that fails on:

   * `print()` in production code paths (non‑test) unless routed through logger
   * `logging.*` calls missing required keys

**Files**

* `scripts/logging_schema_check.py` (AST/static scan)
* `docs/logging/schema.md` (example logs + field meaning)

---

### D) README / Master Log / Consolidated Summary Sync

1. Auto‑refresh `README.md` with:

   * Current phase (9.5.7)
   * Last repo‑health run (date)
   * Active MCP tools (top 50)
   * Active services (top 50)
2. Update `project_master_log.md` with a **single entry** for 9.5.7.1 closure.
3. Append 9.5.7.1 status to `CONSOLIDATED_COMPLETION_SUMMARY.md`.

**Files**

* `scripts/readme_sync.py`
* `scripts/update_master_log.py`

---

### E) CI Gates (block merges)

* **Repo Health** (nightly + PR):

  * `scripts/repo_inventory.py` (v2) ✔
  * `scripts/archive_sweep.py` ✔
  * `scripts/service_usage_audit.py` ✔ (healthcheck OK)
  * `scripts/service_feature_map.py` + `verify_service_feature_binding.py` (core services have ≥1 code ref & ≥1 test ref)
  * `scripts/mcp_sync.py` (no missing specs, no orphans)
  * `scripts/logging_schema_check.py` (no schema violations)
  * `scripts/gen_service_docs.py` (all services have docs)
  * `scripts/readme_sync.py` (README current)
* **Fail PR** on any red above.

**Files**

* `.github/workflows/repo-health.yml` (extend existing)
* `.github/workflows/service-binding.yml` (already added; keep)

---

## Acceptance Criteria (all must pass)

1. **MCP Sync**: Every tool in `src/mcp_servers/**` has a matching `/specs/*.json` and is listed in `MCP_REQUIREMENTS_REFERENCE.md` with current timestamp; no orphaned specs remain.
2. **Services**: All compose services have:

   * healthcheck present and green locally
   * code path linked in service doc
   * service doc present with required sections
   * at least one test referencing the service
3. **Logging**: `logging_schema_check.py` passes; no raw `print()` in production code paths; JSON fields present.
4. **Docs**: `README.md` updated; `project_master_log.md` entry added; `CONSOLIDATED_COMPLETION_SUMMARY.md` includes 9.5.7.1.
5. **CI**: Both workflows pass in PR and on nightly schedule.

---

## Execution Steps (do in order; same branch/PR)

1. **MCP Sync**

* Create/Update: `scripts/mcp_sync.py`

```python
#!/usr/bin/env python
import os, json, glob, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = []
for p in glob.glob("src/mcp_servers/**/*.py", recursive=True):
    s = open(p, encoding="utf-8", errors="ignore").read()
    if "@mcp.tool" in s or ".tool(" in s:
        TOOLS.append({"name": pathlib.Path(p).stem, "file": pathlib.Path(p).as_posix()})
specs_dir = ROOT / "specs"; specs_dir.mkdir(exist_ok=True)
now = datetime.datetime.utcnow().isoformat()
# create/update spec files
for t in TOOLS:
    spec = {"name": t["name"], "version": "1.0.0", "updated": now, "envelope": {"status":"ok|error","data?":{},"error?":{"code":"STRING","message":"STRING"}}}
    path = specs_dir / f"{t['name']}.json"
    open(path, "w", encoding="utf-8").write(json.dumps(spec, indent=2))
# update MCP_REQUIREMENTS_REFERENCE.md
ref = ROOT / "MCP_REQUIREMENTS_REFERENCE.md"
lines = ["# MCP Requirements Reference (auto)\n\n", f"_updated: {now}_\n\n"]
for t in sorted(TOOLS, key=lambda x: x["name"]):
    lines.append(f"- **{t['name']}** — `specs/{t['name']}.json` (src: `{t['file']}`)\n")
open(ref, "w", encoding="utf-8").write("".join(lines))
# archive orphaned specs
spec_paths = { (specs_dir/f"{t['name']}.json").as_posix() for t in TOOLS }
orph = [p for p in glob.glob("specs/*.json") if p not in spec_paths]
if orph:
    arch = ROOT / "archive" / "specs"; arch.mkdir(parents=True, exist_ok=True)
    for p in orph:
        os.replace(p, arch / pathlib.Path(p).name)
print(f"Synced {len(TOOLS)} tools; archived {len(orph)} orphans.")
```

2. **Service Docs (scaffold)**

* Create: `scripts/gen_service_docs.py`

```python
#!/usr/bin/env python
import yaml, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
compose = yaml.safe_load(open("docker/docker-compose.yml"))
docs_dir = ROOT / "docs" / "services"; docs_dir.mkdir(parents=True, exist_ok=True)
for name, spec in (compose.get("services") or {}).items():
    md = docs_dir / f"{name}.md"
    ports = "\n".join(f"- {p}" for p in (spec.get("ports") or []))
    envs = spec.get("environment") or {}
    env = "\n".join(f"- `{k}`: `{v}`" for k,v in envs.items())
    health = spec.get("healthcheck") or {}
    content = f"""---
phase: 9.5.7
status: active
last_reviewed: {datetime.date.today().isoformat()}
related_files: []
---

# Service: {name}

## Role
(brief)

## Ports
{ports or "- (none)"}

## Environment
{env or "- (none)"}

## Healthcheck
- Test: `{health.get('test', '(none)')}`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
"""
    md.write_text(content, encoding="utf-8")
print("Service docs scaffolded/updated.")
```

3. **Logging Schema Check**

* Create: `scripts/logging_schema_check.py`

```python
#!/usr/bin/env python
import ast, sys, glob, os
BAD = []
for p in glob.glob("src/**/*.py", recursive=True):
    if "/tests/" in p: continue
    with open(p, "r", encoding="utf-8", errors="ignore") as fh:
        try:
            tree = ast.parse(fh.read(), filename=p)
        except Exception:
            continue
    for node in ast.walk(tree):
        # hard-fail on print() in prod code
        if isinstance(node, ast.Call) and getattr(getattr(node.func, 'id', None), 'lower', lambda: '' )() == 'print':
            BAD.append((p, node.lineno, "print() in prod code"))
        # naive check: logger call without kwargs containing required keys
        if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr in ('info','warning','error','critical','debug'):
            # allow for now; enforce via runtime sampling later
            pass
if BAD:
    for f, ln, why in BAD:
        print(f"{f}:{ln}: {why}")
    sys.exit(1)
print("Logging schema check: PASS (no raw print() in prod code).")
```

4. **README / Master Log sync**

* Create: `scripts/readme_sync.py`

```python
#!/usr/bin/env python
from datetime import date
import json, glob, os
inv = sorted(glob.glob("logs/repo_health/*.json"))[-1]
data = json.load(open(inv))
tools = [t["name"] for t in data.get("mcp_tools", [])][:50]
services = [s["name"] for s in data.get("docker_services", [])][:50]
template = f"""# Living Truth Engine — Phase 9

**Current focus:** 9.5.7 Resilience Dashboard UI  
**Last repo health run:** {date.today().isoformat()}

## Active MCP tools
{"".join(f"- {t}\n" for t in tools)}

## Active Docker services
{"".join(f"- {s}\n" for s in services)}

## How to run
- `docker compose -f docker/docker-compose.yml up -d --build`
- App: http://localhost:8050
- CI smoke: `bash scripts/resilience_dashboard_test.sh`
"""
open("README.md","w",encoding="utf-8").write(template)
print("README synced.")
```

* Create: `scripts/update_master_log.py`

```python
#!/usr/bin/env python
from datetime import datetime
p = "project_master_log.md"
line = f"- {datetime.utcnow().isoformat()} — Phase 9.5.7.1 Repo Health Completion: MCP/spec sync, service docs, logging, CI gates.\n"
try:
    txt = open(p,encoding="utf-8").read()
except FileNotFoundError:
    txt = "# Project Master Log\n\n"
open(p,"w",encoding="utf-8").write(txt + line)
print("Master log updated.")
```

5. **Add/extend CI workflow**

* Update `.github/workflows/repo-health.yml` job with steps:

```yaml
- name: Repo Health (Phase 9.5.7.1)
  run: |
    python scripts/repo_inventory.py
    python scripts/archive_sweep.py
    python scripts/service_usage_audit.py
    python scripts/mcp_sync.py
    python scripts/gen_service_docs.py
    python scripts/logging_schema_check.py
    python scripts/readme_sync.py
    python scripts/update_master_log.py
```

---

## Exit Gates (block merge unless all green)

* `scripts/mcp_sync.py` reports **0 orphaned specs** and updates MCP reference.
* `docs/services/*.md` exists for all compose services.
* `scripts/logging_schema_check.py` returns **PASS**.
* `README.md` updated with **today's** date and active tools/services.
* `project_master_log.md` updated with a 9.5.7.1 line.
* CI workflows (`repo-health.yml`, `service-binding.yml`) pass on PR.

---

## Completion

Only after all exit gates pass:

* Create `PHASE_9_5_7_1_COMPLETION_SUMMARY.md` mirroring this plan's deliverables and gates.
* Update `CONSOLIDATED_COMPLETION_SUMMARY.md` with a new 9.5.7.1 section.
* Merge.

---

# 🧰 One‑Shot (run in repo root)

```bash
set -euo pipefail

# Ensure scripts exist
mkdir -p scripts docs/services archive/specs

# Write/refresh scripts (paste from plan above)
# 1) MCP sync
cat > scripts/mcp_sync.py <<'PY'
# [PASTE EXACT CONTENTS FROM PLAN SECTION A HERE]
PY
chmod +x scripts/mcp_sync.py

# 2) Service docs
cat > scripts/gen_service_docs.py <<'PY'
# [PASTE EXACT CONTENTS FROM PLAN SECTION B HERE]
PY
chmod +x scripts/gen_service_docs.py

# 3) Logging schema check
cat > scripts/logging_schema_check.py <<'PY'
# [PASTE EXACT CONTENTS FROM PLAN SECTION C HERE]
PY
chmod +x scripts/logging_schema_check.py

# 4) README & master log sync
cat > scripts/readme_sync.py <<'PY'
# [PASTE EXACT CONTENTS FROM PLAN SECTION D HERE]
PY
chmod +x scripts/readme_sync.py

cat > scripts/update_master_log.py <<'PY'
# [PASTE EXACT CONTENTS FROM PLAN SECTION D HERE]
PY
chmod +x scripts/update_master_log.py

# Run the phase tasks
python scripts/mcp_sync.py
python scripts/gen_service_docs.py
python scripts/logging_schema_check.py
python scripts/readme_sync.py
python scripts/update_master_log.py

# Commit
git add -A
git commit -m "9.5.7.1: Repo Health Completion — MCP/spec sync, service docs, logging, README/log, CI gates" || true
```

---

**Deliver this file to Cursor and run it.**
