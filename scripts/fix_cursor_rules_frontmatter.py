#!/usr/bin/env python3
"""
Cursor Rules Frontmatter Fixer (Cursor-spec)
- Converts any .mdc frontmatter to: description, globs, alwaysApply
- 00-global.mdc: enforces alwaysApply: true
- Migrates any nonstandard keys (e.g., rule_id, phase, checksum, enforcement, owner, summary)
  into a "Meta (migrated)" section at the top of the Markdown body.
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

def split_frontmatter(txt: str):
	m = FM_RE.match(txt)
	if not m:
		return {}, txt  # no or bad frontmatter
	try:
		meta = yaml.safe_load(m.group(1)) or {}
		if not isinstance(meta, dict):
			meta = {}
	except yaml.YAMLError:
		meta = {}
	return meta, m.group(2)

def first_heading(md: str) -> str:
	for line in md.splitlines():
		if line.strip().startswith("#"):
			return line.lstrip("# ").strip()
	return ""

def build_meta(path: Path, meta: dict, body: str) -> tuple[dict,str]:
	m = dict(meta) if isinstance(meta, dict) else {}
	# Construct minimal Cursor-spec
	desc = (m.get("description") or first_heading(body) or f"Rule: {path.stem}").strip()
	out = {"description": desc}
	if "globs" in m and (isinstance(m["globs"], str) or (isinstance(m["globs"], list) and all(isinstance(i,str) for i in m["globs"]))):
		out["globs"] = m["globs"]
	if path.name == "00-global.mdc":
		out["alwaysApply"] = True
	elif isinstance(m.get("alwaysApply"), bool) and m["alwaysApply"]:
		out["alwaysApply"] = True
	# Migrate extra keys into body so they aren’t lost
	extras = {k:v for k,v in m.items() if k not in ALLOWED_KEYS}
	if extras:
		# Avoid duplicating an existing migrated block
		block_header = "### Meta (migrated from nonstandard frontmatter)"
		if block_header not in body:
			import pprint
			pretty = pprint.pformat(extras, width=100, compact=True)
			body = f"{block_header}\n\n```yaml\n{pretty}\n```\n\n{body}"
	return out, body

def write_rule(path: Path, meta: dict, body: str):
	new = "---\n" + yaml.safe_dump(meta, sort_keys=False).strip() + "\n---\n" + (body or "")
	path.write_text(new, encoding="utf-8")

def fix_all():
	fixed=[]
	if not RULES_DIR.exists():
		return {"status":"ok","data":{"fixed":0,"note":"no .cursor/rules found"}}
	for p in sorted(RULES_DIR.glob("*.mdc")):
		txt = p.read_text(encoding="utf-8", errors="ignore")
		meta, body = split_frontmatter(txt)
		new_meta, new_body = build_meta(p, meta, body)
		write_rule(p, new_meta, new_body)
		fixed.append(p.name)
	return {"status":"ok","data":{"fixed":len(fixed),"files":fixed}}

if __name__ == "__main__":
	print(json.dumps(fix_all(), indent=2))
