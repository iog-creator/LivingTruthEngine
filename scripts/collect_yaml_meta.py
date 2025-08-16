#!/usr/bin/env python3
"""
SSOT Metadata Indexer (read-only)
Collects YAML metadata from across the repo and writes a single JSON index:
  - Cursor rules frontmatter (.cursor/rules/*.mdc): {description, globs, alwaysApply}
  - Optional per-rule or per-doc "SSOT Meta" YAML blocks in the Markdown body
  - Frontmatter from PHASE_*_COMPLETION_SUMMARY.md and other docs (if present)

Output: reports/ssot_meta_index.json
Usage: make meta-index  (also runs as part of `make reports`)
"""
from __future__ import annotations
import argparse, json, os, re, sys, time
from pathlib import Path

try:
    import yaml
except ImportError as e:
    print(json.dumps({"status":"error","error":{"code":"pyyaml_missing","message":"PyYAML is required: pip install pyyaml"}}))
    raise SystemExit(1)

ROOT = Path(".").resolve()
RULES_DIR = ROOT / ".cursor" / "rules"
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)
SSOT_META_HDR = "### SSOT Meta"
FENCE_RE = re.compile(r"^```+")

def parse_frontmatter(text: str):
    """Return (frontmatter_dict_or_None, body_text)."""
    m = FM_RE.match(text)
    if not m:
        return None, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
        if not isinstance(meta, dict):
            meta = {}
        # Convert any non-serializable objects to strings
        meta = json.loads(json.dumps(meta, default=str))
    except (yaml.YAMLError, ValueError):
        meta = {}
    return meta, m.group(2)

def extract_ssot_meta_blocks(body: str):
    """
    Find '### SSOT Meta' then first fenced YAML block that follows.
    Return list of dict blocks (usually 0 or 1).
    """
    lines = body.splitlines()
    out = []
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].strip() == SSOT_META_HDR:
            i += 1
            # skip blank lines
            while i < n and not lines[i].strip():
                i += 1
            # expect YAML fence
            if i < n and lines[i].strip().startswith("```yaml"):
                i += 1
                buf = []
                while i < n and not FENCE_RE.match(lines[i].strip()):
                    buf.append(lines[i])
                    i += 1
                # skip closing fence
                if i < n:
                    i += 1
                try:
                    block = yaml.safe_load("\n".join(buf)) or {}
                    if isinstance(block, dict):
                        # Convert any non-serializable objects to strings
                        block = json.loads(json.dumps(block, default=str))
                        out.append(block)
                except (yaml.YAMLError, ValueError):
                    # ignore malformed blocks
                    pass
            else:
                # no fenced yaml; skip
                pass
        else:
            i += 1
    return out

def classify_rule(meta: dict, path: Path) -> str:
    if meta.get("alwaysApply") is True:
        return "Always"
    if "globs" in meta:
        return "Auto-Attached"
    return "Agent-Requested"

def collect_rules():
    rules = []
    if not RULES_DIR.exists():
        return rules
    for p in sorted(RULES_DIR.glob("*.mdc")):
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            fm, body = parse_frontmatter(txt)
            if fm is None:
                fm = {}
                body = txt
            # Keep only Cursor-spec fields in the index root
            rule_meta = {
                "file": str(p.relative_to(ROOT)),
                "description": fm.get("description", ""),
                "globs": fm.get("globs", None),
                "alwaysApply": bool(fm.get("alwaysApply", False)),
                "type": classify_rule(fm, p),
            }
            blocks = extract_ssot_meta_blocks(body)
            if blocks:
                rule_meta["ssot_meta"] = blocks  # list of dict
            rules.append(rule_meta)
        except (OSError, UnicodeDecodeError):
            # ignore unreadable files
            continue
    return rules

def collect_doc_frontmatter():
    docs = []
    # Phase summaries and key SSOT docs often start with YAML frontmatter — collect if present.
    candidates = list(ROOT.glob("PHASE_*_COMPLETION_SUMMARY.md")) + [
        ROOT / "README.md",
        ROOT / "project_master_log.md",
        ROOT / "MCP_REQUIREMENTS_REFERENCE.md",
        ROOT / "SERVICES_MANIFEST.md",
        ROOT / "LM_STUDIO_INTEGRATION.md",
    ]
    for p in candidates:
        if not p.exists():
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            fm, _ = parse_frontmatter(txt)
            if fm:
                docs.append({"file": str(p.relative_to(ROOT)), "frontmatter": fm})
        except (OSError, UnicodeDecodeError):
            continue
    return docs

def main():
    parser = argparse.ArgumentParser(description="Generate SSOT metadata index")
    parser.add_argument("--out", type=str, default="reports/ssot_meta_index.json", 
                       help="Output file path (default: reports/ssot_meta_index.json)")
    args = parser.parse_args()
    
    # Ensure output directory exists
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    idx = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rules": collect_rules(),
        "docs": collect_doc_frontmatter(),
    }
    
    # Write to file if --out specified, otherwise print to stdout
    if args.out:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(idx, f, indent=2, ensure_ascii=False)
    else:
        print(json.dumps(idx, indent=2))

if __name__ == "__main__":
    main()
