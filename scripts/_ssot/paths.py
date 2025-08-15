from __future__ import annotations
import os, time
from pathlib import Path
from typing import Iterable, Iterator, Tuple, Dict, Any
try:
    import yaml
except Exception:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
CFG = {}
def load_cfg() -> Dict[str, Any]:
    global CFG
    if CFG: return CFG
    cfg_path = ROOT / ".config" / "ssot.yml"
    if yaml and cfg_path.exists():
        CFG = yaml.safe_load(cfg_path.read_text()) or {}
    else:
        CFG = {}
    return CFG

def iter_files(scope: str = "fast") -> Iterator[Path]:
    """Yield files with pruning, budget, and extension hints."""
    cfg = load_cfg()
    scan = cfg.get("scan", {})
    max_files = (scan.get("max_files") or {}).get(scope, 1000)
    exclude = set(scan.get("exclude_globs", []))
    include_hints = scan.get("include_hint_globs", []) or ["*.md", "*.py", "*.mdc"]
    count = 0
    for root, dirs, files in os.walk(ROOT, topdown=True, followlinks=False):
        relroot = Path(root).relative_to(ROOT)
        # prunes
        dprune = []
        for d in list(dirs):
            p = (relroot / d).as_posix() + "/"
            if any(Path(p).match(glob.replace("**/","")) or p.startswith(glob.rstrip("*")) for glob in exclude):
                dprune.append(d)
        for d in dprune:
            dirs.remove(d)
        for f in files:
            path = Path(root) / f
            # include hint
            if not any(path.match(g) for g in include_hints):
                continue
            yield path
            count += 1
            if count >= max_files:
                return

def read_bounded(path: Path, max_bytes: int) -> str:
    try:
        with open(path, "rb") as fh:
            data = fh.read(max_bytes)
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""
