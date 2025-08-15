#!/usr/bin/env python3
import sys, re, pathlib, fnmatch, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
ERR = []

REQUIRED_ROOT = [
  "README.md",
  "project_master_log.md",
  "MCP_REQUIREMENTS_REFERENCE.md",
  "SERVICES_MANIFEST.md",
]
PHASE_GLOB = "PHASE_*_COMPLETION_SUMMARY.md"
PHASE_REQUIRED_FIELDS = ["phase","status","completion_date","depends_on","summary"]

def die():
  if ERR:
    print("SSOT verification FAILED:\n- " + "\n- ".join(ERR))
    sys.exit(1)
  print("SSOT verification PASS")
  sys.exit(0)

def must_exist_in_root(paths):
  for p in paths:
    if not (ROOT / p).exists():
      ERR.append(f"Missing required SSOT file in root: {p}")

def no_duplicates():
  # Disallow duplicates under docs/ or archive/docs/
  for name in REQUIRED_ROOT + [PHASE_GLOB]:
    pattern = name if "*" in name else name
    for sub in ["docs", "archive/docs"]:
      for f in (ROOT / sub).rglob("*"):
        if f.is_file():
          if "*" in pattern:
            if fnmatch.fnmatch(f.name, pattern):
              ERR.append(f"Duplicate SSOT file in {sub}: {f}")
          else:
            if f.name == pattern:
              ERR.append(f"Duplicate SSOT file in {sub}: {f}")

def validate_phase_frontmatter():
  for f in ROOT.glob(PHASE_GLOB):
    txt = f.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\s*\n(.*?)\n---\s*", txt, re.DOTALL)
    if not m:
      ERR.append(f"{f.name}: missing YAML frontmatter block")
      continue
    try:
      fm = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
      ERR.append(f"{f.name}: invalid YAML frontmatter ({e})")
      continue
    missing = [k for k in PHASE_REQUIRED_FIELDS if k not in fm]
    if missing:
      ERR.append(f"{f.name}: missing fields in frontmatter: {', '.join(missing)}")

def validate_services_manifest():
  mf = ROOT / "SERVICES_MANIFEST.md"
  if not mf.exists():
    ERR.append("SERVICES_MANIFEST.md missing")
    return
  txt = mf.read_text(encoding="utf-8", errors="ignore")
  # Minimal structural checks (don't be brittle)
  required_sections = ["Role", "Ports", "Environment", "Healthcheck", "Code Paths", "Tests"]
  for sec in required_sections:
    if sec not in txt:
      ERR.append(f"SERVICES_MANIFEST.md: missing section '{sec}'")

def main():
  must_exist_in_root(REQUIRED_ROOT)
  no_duplicates()
  validate_phase_frontmatter()
  validate_services_manifest()
  die()

if __name__ == "__main__":
  main()
