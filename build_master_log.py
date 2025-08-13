#!/usr/bin/env python3
"""
Builds docs/project_master_log.md by sweeping all PHASE_*_PLAN.md and
PHASE_*_COMPLETION_SUMMARY.md files and stitching them chronologically.

Usage:
  python build_master_log.py rebuild
  python build_master_log.py append  # (re-scan and update changed/new phases)
"""
from __future__ import annotations
import sys, re, os, time, hashlib
from pathlib import Path
from typing import List, Tuple, Dict

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
OUT = DOCS / "project_master_log.md"

PHASE_FILE_RE = re.compile(
    r"^(PHASE(?:_|-)?(?P<major>\d+)(?:[._-](?P<minor>\d+))?(?:[._-](?P<patch>\d+))?)_?(?P<kind>PLAN|COMPLETION_SUMMARY)\.md$",
    re.IGNORECASE,
)

def phase_sort_key(fname: str) -> Tuple[int, int, int, int]:
    m = PHASE_FILE_RE.match(fname)
    if not m:
        return (9999, 9999, 9999, 1 if "PLAN" in fname.upper() else 2)
    maj = int(m.group("major") or 0)
    minr = int(m.group("minor") or 0)
    pat = int(m.group("patch") or 0)
    # always put PLAN before COMPLETION for same phase
    kind_rank = 1 if m.group("kind").upper() == "PLAN" else 2
    return (maj, minr, pat, kind_rank)

def find_phase_files() -> List[Path]:
    # search repo root + docs/ for PHASE_* files
    candidates: List[Path] = []
    for base in [ROOT, DOCS]:
        for p in base.glob("PHASE*_*.*md"):
            if PHASE_FILE_RE.match(p.name):
                candidates.append(p)
    # also sweep top-level for single-underscore variants
    for p in ROOT.glob("PHASE_*_*.md"):
        if PHASE_FILE_RE.match(p.name):
            candidates.append(p)
    # de-dupe by stem
    seen = set()
    uniq: List[Path] = []
    for p in candidates:
        if p.name not in seen:
            uniq.append(p)
            seen.add(p.name)
    uniq.sort(key=lambda x: phase_sort_key(x.name))
    return uniq

def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8").strip()
    except Exception as e:
        return f"_Error reading {p}: {e}_"

def short_sha(contents: str) -> str:
    return hashlib.sha1(contents.encode("utf-8")).hexdigest()[:10]

def build(sections: List[Tuple[str, Path, str]]) -> str:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    lines: List[str] = []
    lines.append("# Living Truth Engine — Project Master Log")
    lines.append("")
    lines.append(f"_Auto-generated on **{ts}** by `build_master_log.py`. Do not hand-edit this file._")
    lines.append("")
    # TOC
    lines.append("## Table of Contents")
    for title, path, _ in sections:
        anchor = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        lines.append(f"- [{title}](#{anchor}) — `{path.name}`")
    lines.append("")
    # Sections
    for title, path, body in sections:
        lines.append(f"## {title}")
        lines.append(f"_Source: `{path.relative_to(ROOT)}` | SHA: `{short_sha(body)}`_")
        lines.append("")
        lines.append(body)
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def make_title(p: Path) -> str:
    # PHASE_9_2_PLAN.md -> "Phase 9.2 — PLAN"
    m = PHASE_FILE_RE.match(p.name)
    if not m:
        return p.stem
    maj = m.group("major") or "0"
    minr = m.group("minor")
    pat = m.group("patch")
    kind = m.group("kind").upper()
    ver = maj
    if minr:
        ver += f".{minr}"
    if pat:
        ver += f".{pat}"
    return f"Phase {ver} — {('PLAN' if kind=='PLAN' else 'COMPLETION SUMMARY')}"

def main():
    mode = (sys.argv[1].lower() if len(sys.argv) > 1 else "append").strip()
    files = find_phase_files()
    if not files:
        print("No PHASE_* files found. Nothing to do.")
        return
    sections: List[Tuple[str, Path, str]] = []
    for p in files:
        title = make_title(p)
        body = read(p)
        sections.append((title, p, body))

    new_contents = build(sections)

    if OUT.exists():
        old = OUT.read_text(encoding="utf-8")
        if mode == "append" and old == new_contents:
            print("No changes. Master log is up to date.")
            return

    OUT.write_text(new_contents, encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()





