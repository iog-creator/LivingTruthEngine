---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['MCP_REQUIREMENTS_REFERENCE.md', 'scripts/repo_inventory.py', 'python scripts/repo_inventory.py', '/archive/README.md', 'python scripts/doc_audit.py', 'PHASE_*.md', '/docs/services/<service>.md', 'README.md', 'scripts/doc_audit.py', 'logs/repo_health/YYYY-MM-DD.json', 'project_master_log.md']
---

# Phase Background – Repo Health & Alignment System

## 🎯 Objective

Run a **continuous repo alignment process** that:

* Analyzes and updates all documentation with proper frontmatter.
* Verifies all MCP tools, specs, and references are in sync.
* Aligns Docker services with code & docs.
* Validates logging standards.
* Archives outdated/legacy materials.
* Updates the README and master log automatically.

This runs **daily** or before **any merge** to prevent drift between code, docs, and MCP enforcement.

---

## 📌 Core Tasks

### **1. Documentation Inventory & Frontmatter**

* Scan all `.md` and `.mdc` files in:
  * `/docs`
  * `/.cursor/rules`
  * Root phase files (`PHASE_*.md`)
  * `README.md`
* If missing frontmatter, prepend:
  ```yaml
  ---
  phase: <current_phase>
  status: active|archived|outdated
  last_reviewed: YYYY-MM-DD
  related_files: []
  ---
  ```
* Move outdated docs to `/archive/docs` and update `/archive/README.md`.

---

### **2. MCP Tool & Spec Sync**

* Enumerate all MCP tools in `src/mcp_servers/**`.
* Ensure each has:
  * A JSON spec in `/specs`.
  * An entry in `MCP_REQUIREMENTS_REFERENCE.md` with last updated date.
* Remove orphaned specs or archive them.

---

### **3. Docker Service Co-Development**

* Read `docker/docker-compose.yml`.
* For each service:
  * Check for:
    * Health check endpoint in config or code.
    * Docs in `/docs/services/<service>.md` with description & usage.
    * Corresponding code in `src/<service>` or named volume mapping.
* Create missing service docs.

---

### **4. Logging & Observability**

* Check all code for `logging` or `print` statements.
* Ensure JSON structured logging with:
  ```json
  {
    "phase": "9.5.7",
    "component": "<component_name>",
    "level": "info|error",
    "message": "...",
    "timestamp": "ISO8601"
  }
  ```
* Update `/docs/logging/` with schema and log examples.
* Fail CI if logs don't match schema.

---

### **5. Repo Health Report**

* Generate `logs/repo_health/YYYY-MM-DD.json` containing:
  * All active docs with frontmatter.
  * MCP tools list + spec status.
  * Docker services list + doc status.
  * Log compliance %.
* Summary is posted to `project_master_log.md`.

---

### **6. CI/CD Gates**

Fail CI if:
* Active docs missing frontmatter.
* MCP tools without matching specs.
* Docker service missing doc or code.
* Logs non-compliant with schema.

---

## 🔩 Scripts to Implement

### **`scripts/repo_inventory.py`**

```python
import os, json, datetime
ROOT = os.path.dirname(os.path.dirname(__file__))

def list_files(exts):
    for root, _, files in os.walk(ROOT):
        for f in files:
            if any(f.endswith(e) for e in exts):
                yield os.path.join(root, f)

def main():
    inventory = {
        "docs": list(list_files((".md", ".mdc"))),
        "specs": list(list_files((".json",))),
        "mcp_tools": [],
        "docker_services": [],
        "logs": [],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    # Enumerate MCP tools
    for f in list_files((".py",)):
        if "/mcp_servers/" in f:
            with open(f) as fh:
                if "@mcp.tool" in fh.read():
                    inventory["mcp_tools"].append(f)
    # Parse docker-compose
    compose = os.path.join(ROOT, "docker", "docker-compose.yml")
    if os.path.exists(compose):
        with open(compose) as fh:
            inventory["docker_services"] = [line.strip().split(":")[0]
                for line in fh if line.strip().endswith(":") and not line.startswith(" ")]
    outdir = os.path.join(ROOT, "logs", "repo_health")
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, f"{datetime.date.today()}.json")
    with open(outfile, "w") as fh:
        json.dump(inventory, fh, indent=2)
    print(f"Inventory saved to {outfile}")

if __name__ == "__main__":
    main()
```

---

### **`scripts/doc_audit.py`**

```python
import os, re, datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
FRONTMATTER_RE = re.compile(r"^---\n.*?^---\n", re.S | re.M)

def ensure_frontmatter(path):
    with open(path, "r+", encoding="utf-8") as fh:
        content = fh.read()
        if not FRONTMATTER_RE.match(content):
            front = f"---\nphase: 9.5.7\nstatus: active\nlast_reviewed: {datetime.date.today()}\nrelated_files: []\n---\n\n"
            fh.seek(0)
            fh.write(front + content)
            fh.truncate()
            return True
    return False

def main():
    changed = 0
    for root, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith((".md", ".mdc")) and "/archive/" not in root:
                if ensure_frontmatter(os.path.join(root, f)):
                    changed += 1
    print(f"Frontmatter added to {changed} files.")

if __name__ == "__main__":
    main()
```

---

## 🚦 Execution Order for Cursor

1. Run `python scripts/repo_inventory.py` → save inventory JSON.
2. Run `python scripts/doc_audit.py` → add missing frontmatter.
3. Cross-check MCP tools ↔ specs ↔ MCP reference.
4. Cross-check Docker services ↔ docs ↔ code.
5. Run log schema validation.
6. Generate/update `logs/repo_health/YYYY-MM-DD.json`.
7. Update:
   * `project_master_log.md`
   * `README.md` (phase, active tools, services, last health check)
8. Commit with message:
   ```
   Repo health update: docs, MCP sync, Docker services, logs aligned
   ```

---

## 📅 Scheduling

* **Daily** at 02:00 UTC via CI job.
* **Pre-merge**: run on every PR; fail if violations found.

---

## 📋 Implementation Checklist

- [ ] Create `scripts/repo_inventory.py`
- [ ] Create `scripts/doc_audit.py`
- [ ] Create `logs/repo_health/` directory
- [ ] Add CI job for daily execution
- [ ] Add pre-merge validation
- [ ] Update README.md with health system
- [ ] Create initial inventory baseline
- [ ] Archive outdated documentation
- [ ] Validate MCP tool ↔ spec alignment
- [ ] Create missing service documentation
- [ ] Implement logging schema validation

---

## 🔧 MCP Integration

### **Required MCP Tools**
- `validate_repo_health()` - Run full health check
- `fix_documentation_frontmatter()` - Add missing frontmatter
- `sync_mcp_tools_and_specs()` - Align MCP tools with specs
- `archive_outdated_docs()` - Move outdated docs to archive
- `generate_repo_health_report()` - Create health report

### **MCP Tool Implementation**
```python
@mcp.tool()
def validate_repo_health() -> dict:
    """Run comprehensive repo health validation."""
    # Implementation in src/mcp_servers/phase9_mcp_server.py
    pass

@mcp.tool()
def fix_documentation_frontmatter() -> dict:
    """Add missing frontmatter to documentation files."""
    # Implementation in src/mcp_servers/phase9_mcp_server.py
    pass
```

---

## 📊 Success Metrics

- [ ] 100% documentation has proper frontmatter
- [ ] 100% MCP tools have matching specs
- [ ] 100% Docker services have documentation
- [ ] 100% logs follow structured schema
- [ ] Daily health reports generated
- [ ] Pre-merge validation passes
- [ ] No orphaned files or specs
- [ ] Archive properly organized

---

**This background system ensures the repository stays healthy and aligned while feature development continues.**
