#!/usr/bin/env python3
"""
Validate Cursor rule files: .cursor/rules/*.mdc
- Requires YAML frontmatter at the top delimited by '---' ... '---'
- Enforces required keys + types
- Verifies body checksum if provided; suggests fix otherwise

Exit code:
  0 on success
  1 on schema or checksum errors
Output: JSON envelope to STDOUT
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
try:
    import yaml
except Exception as e:
    print(json.dumps({"status":"error","error":{"code":"pyyaml_missing","message":"PyYAML is required: pip install pyyaml"}}))
    sys.exit(1)

ROOT = Path(".").resolve()
RULES_DIR = ROOT/".cursor"/"rules"

REQUIRED = {
    "rule_id": str,
    "title": str,
    "phase": str,            # e.g., "9.5.7.4.6"
    "applies": str,          # "always" | "phase" | "optional"
    "enforcement": str,      # "strict" | "advisory"
    "owner": str,
    "updated": str,          # ISO date YYYY-MM-DD
    "version": int,
    "scope": (str, list),    # "all" or ["**/*", ...]
    "summary": str,
}
OPTIONAL = {
    "links": list,
    "checksum": str,         # sha256 of *body* (content after closing frontmatter)
}

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def parse_rule(path: Path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    m = FM_RE.match(txt)
    if not m:
        return None, txt  # no or invalid frontmatter
    front, body = m.group(1), m.group(2)
    try:
        meta = yaml.safe_load(front) or {}
        if not isinstance(meta, dict):
            meta = {}
    except Exception:
        meta = {}
    return meta, body

def validate():
    errors, warnings = [], []
    checked = []
    if not RULES_DIR.exists():
        return {"status":"ok","data":{"checked":0,"notes":["No .cursor/rules directory found"]}}
    for path in sorted(RULES_DIR.glob("*.mdc")):
        meta, body = parse_rule(path)
        rule_name = path.name
        if meta is None:
            errors.append({"file": rule_name, "issue":"missing_or_invalid_frontmatter"})
            continue
        # required keys/types
        for k, t in REQUIRED.items():
            if k not in meta:
                errors.append({"file": rule_name, "issue": f"missing_key:{k}"})
            else:
                ok = isinstance(meta[k], t if isinstance(t, type) else t)
                if not ok:
                    errors.append({"file": rule_name, "issue": f"type_mismatch:{k}", "expected": str(t), "actual": str(type(meta[k]).__name__)})
        # special constraints for 00-global.mdc
        if path.name == "00-global.mdc":
            if meta.get("applies") != "always":
                errors.append({"file": rule_name, "issue": "global_applies_must_be_always"})
            if meta.get("enforcement") != "strict":
                errors.append({"file": rule_name, "issue": "global_enforcement_must_be_strict"})
            if meta.get("scope") not in ("all", ["**/*"]):
                warnings.append({"file": rule_name, "issue":"global_scope_should_be_all"})
        # checksum (optional but recommended)
        body_hash = sha256_text(body or "")
        if "checksum" in meta and meta.get("checksum") != body_hash:
            errors.append({"file": rule_name, "issue":"checksum_mismatch","expected":body_hash,"actual":meta.get("checksum")})
        elif "checksum" not in meta:
            warnings.append({"file": rule_name, "issue":"checksum_missing","expected":body_hash})
        checked.append(rule_name)
    status = "ok" if not errors else "error"
    out = {"status": status, "data": {"checked": len(checked), "errors": errors, "warnings": warnings}}
    return out

if __name__ == "__main__":
    res = validate()
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["status"]=="ok" else 1)
