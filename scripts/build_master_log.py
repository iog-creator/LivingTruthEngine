import re, sys, os, json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "docs" / "project_master_log.md"

PHASE_PLAN_PAT = re.compile(r"^PHASE_(.+?)_PLAN\.md$", re.I)
PHASE_COMP_PAT = re.compile(r"^PHASE_(.+?)_COMPLETION_SUMMARY\.md$", re.I)
DATE_PATTERNS = [
    re.compile(r"^Date:\s*(.+)$", re.I | re.M),
    re.compile(r"^Completion Date:\s*(.+)$", re.I | re.M),
    re.compile(r"^\*\*Date\*\*:\s*(.+)$", re.I | re.M),
]
PHASE_KEY_ORDER = ["",]  # placeholder to keep stable sort when dates tie

def human_date_to_iso(s: str) -> str:
    s = s.strip()
    for fmt in [
        "%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d %B %Y",
    ]:
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            pass
    # fallback: return original string
    return s

def extract_date(text: str) -> str:
    for pat in DATE_PATTERNS:
        m = pat.search(text or "")
        if m:
            return human_date_to_iso(m.group(1))
    return ""

def discover_phase_files(limit_phase_prefix=None):
    plans, comps = {}, {}
    for p in ROOT.rglob("PHASE_*_PLAN.md"):
        m = PHASE_PLAN_PAT.match(p.name)
        if not m: continue
        phase = m.group(1)
        if limit_phase_prefix and not phase.lower().startswith(limit_phase_prefix.lower().replace("phase_", "")):
            continue
        plans[phase] = p
    for c in ROOT.rglob("PHASE_*_COMPLETION_SUMMARY.md"):
        m = PHASE_COMP_PAT.match(c.name)
        if not m: continue
        phase = m.group(1)
        if limit_phase_prefix and not phase.lower().startswith(limit_phase_prefix.lower().replace("phase_", "")):
            continue
        comps[phase] = c
    phases = set(plans.keys()) | set(comps.keys())
    return plans, comps, phases

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError, PermissionError):
        return f"_Unable to read file: {p}_"

def load_git_date(path: Path) -> str:
    # Try to get the last commit date for this file (if repo present)
    try:
        import subprocess
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=str(ROOT),
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return out
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return ""

def section_for_phase(phase: str, plan_p: Path|None, comp_p: Path|None) -> dict:
    plan_txt = read_text(plan_p) if plan_p else "_No plan found for this phase._"
    comp_txt = read_text(comp_p) if comp_p else "_No completion summary found for this phase._"
    # Try dates (prefer completion date, fallback to git date, fallback '')
    date = extract_date(comp_txt) or extract_date(plan_txt)
    if not date and comp_p: date = load_git_date(comp_p)
    if not date and plan_p: date = load_git_date(plan_p)
    return {
        "phase": phase,
        "date": date,
        "plan_path": str(plan_p) if plan_p else "",
        "comp_path": str(comp_p) if comp_p else "",
        "plan_txt": plan_txt,
        "comp_txt": comp_txt,
    }

def sort_key(entry: dict):
    # Sort by date (if present), then numeric-ish phase order, then name
    date = entry["date"] or "9999-99-99"
    # Normalize phase like "9_1", "8_3_2" to sortable tuple
    def parse_phase(ph):
        parts = []
        for t in re.split(r"[^\d]+", ph):
            if t.isdigit(): parts.append(int(t))
        return tuple(parts) if parts else (9999,)
    return (date, parse_phase(entry["phase"]), entry["phase"])

def write_log(entries: list[dict], mode: str):
    # Append-only: if mode == "append", only add new sections for phases not already present.
    existing = ""
    if LOG.exists():
        existing = LOG.read_text(encoding="utf-8")

    new_sections = []
    for e in sorted(entries, key=sort_key):
        hdr = f"# Phase {e['phase']} — PLAN"
        # Skip if already present in append mode
        if mode == "append" and hdr in existing:
            continue
        s = []
        s.append(hdr + "\n")
        s.append(e["plan_txt"].rstrip() + "\n\n")
        s.append(f"# Phase {e['phase']} — COMPLETION SUMMARY\n")
        s.append(e["comp_txt"].rstrip() + "\n\n")
        s.append(f"# Source Files\n- Plan: `{e['plan_path'] or 'N/A'}`\n- Summary: `{e['comp_path'] or 'N/A'}`\n")
        s.append("\n---\n\n")
        new_sections.append("".join(s))

    if mode == "rebuild" or not LOG.exists():
        header = (
            "# Living Truth Engine — Project Master Log\n\n"
            "_Append‑only historical record of all phase plans & completion summaries._\n\n"
            "> Built by scripts/build_master_log.py\n\n"
            "---\n\n"
        )
        LOG.write_text(header + "".join(new_sections), encoding="utf-8")
    else:
        LOG.write_text(existing + "".join(new_sections), encoding="utf-8")

def main():
    mode = "rebuild" if "--rebuild" in sys.argv else "append"
    limit = None
    for i,a in enumerate(sys.argv):
        if a == "--append" and i+1 < len(sys.argv):
            limit = sys.argv[i+1]
    plans, comps, phases = discover_phase_files(limit)
    entries = []
    for ph in phases:
        entries.append(section_for_phase(ph, plans.get(ph), comps.get(ph)))
    write_log(entries, mode)

if __name__ == "__main__":
    main()
