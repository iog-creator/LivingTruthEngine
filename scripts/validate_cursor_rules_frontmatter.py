#!/usr/bin/env python3
"""
Cursor Rules Frontmatter Validator (Cursor-spec)
Valid schema: YAML frontmatter with keys:
  - description: str (required)
  - globs: str | list[str] (optional; implies Auto-Attached if present)
  - alwaysApply: bool (optional; implies Always when true)
Other keys are nonstandard and will be flagged (error by default).

Special case: 00-global.mdc must have alwaysApply: true.

Refs:
  - Cursor docs "Rules for AI": frontmatter controls (description, globs, alwaysApply)
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
try:
	import yaml
except ImportError:
	print(json.dumps({"status":"error","error":{"code":"pyyaml_missing","message":"PyYAML is required: pip install pyyaml"}}))
	sys.exit(1)

ROOT = Path(".").resolve()
RULES_DIR = ROOT/".cursor"/"rules"
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)
ALLOWED_KEYS = {"description","globs","alwaysApply"}

def parse_frontmatter(path: Path):
	txt = path.read_text(encoding="utf-8", errors="ignore")
	m = FM_RE.match(txt)
	if not m:
		return None, txt
	try:
		meta = yaml.safe_load(m.group(1)) or {}
		if not isinstance(meta, dict):
			meta = {}
	except yaml.YAMLError:
		meta = {}
	body = m.group(2)
	return meta, body

def is_string_list(x):
	return isinstance(x, list) and all(isinstance(i,str) for i in x)

def validate_rule(path: Path):
	meta, body = parse_frontmatter(path)
	errs, warns = [], []
	if meta is None:
		errs.append("missing_or_invalid_frontmatter"); return errs, warns
	# required: description
	if "description" not in meta or not isinstance(meta["description"], str) or not meta["description"].strip():
		errs.append("missing_or_invalid:description")
	# optional: globs (str or list[str])
	if "globs" in meta and not (isinstance(meta["globs"], str) or is_string_list(meta["globs"])):
		errs.append("invalid_type:globs")
	# optional: alwaysApply (bool)
	if "alwaysApply" in meta and not isinstance(meta["alwaysApply"], bool):
		errs.append("invalid_type:alwaysApply")
	# special case 00-global
	if path.name == "00-global.mdc":
		if not meta.get("alwaysApply", False):
			errs.append("global_must_set_alwaysApply_true")
		# globs is not needed for 00-global; warn if present
		if "globs" in meta:
			warns.append("global_globs_unnecessary")
	# nonstandard keys
	extras = [k for k in meta.keys() if k not in ALLOWED_KEYS]
	if extras:
		errs.append(f"nonstandard_keys:{extras}")
	return errs, warns

def main():
	checked=0; errors=[]; warnings=[]
	if not RULES_DIR.exists():
		print(json.dumps({"status":"ok","data":{"checked":0,"notes":["no .cursor/rules directory"]}})); return
	for p in sorted(RULES_DIR.glob("*.mdc")):
		checked+=1
		e,w = validate_rule(p)
		if e: errors.append({"file":p.name,"issues":e})
		if w: warnings.append({"file":p.name,"issues":w})
	status = "ok" if not errors else "error"
	out = {"status":status,"data":{"checked":checked,"errors":errors,"warnings":warnings}}
	print(json.dumps(out, indent=2))
	sys.exit(0 if status=="ok" else 1)

if __name__ == "__main__":
	main()
