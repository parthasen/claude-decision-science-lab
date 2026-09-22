#!/usr/bin/env python
"""List tabular datasets in a folder so the user can pick one.

Usage: python discover.py [folder] [--json] [--max-depth 6]
Prints a numbered table (file, type, size, rows, cols). --json emits machine-readable output.
Skips generated dirs (__pycache__, .git, envs, node_modules, output_*).
"""
import argparse
import json
import sys
from pathlib import Path

EXTS = {".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".json", ".jsonl"}
SKIP = {"__pycache__", ".git", "envs", "node_modules", ".venv", "venv", "outputs"}


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def peek(path: Path) -> tuple[str, str]:
    """Return (rows, cols) cheaply; '?' when unknown."""
    try:
        ext = path.suffix.lower()
        if ext in {".csv", ".tsv"}:
            sep = "\t" if ext == ".tsv" else ","
            with open(path, "rb") as f:
                rows = sum(chunk.count(b"\n") for chunk in iter(lambda: f.read(1 << 20), b"")) - 1
            with open(path, encoding="utf-8", errors="replace") as f:
                cols = len(f.readline().split(sep))
            return f"{max(rows, 0):,}", str(cols)
        if ext == ".parquet":
            import pyarrow.parquet as pq
            m = pq.ParquetFile(path).metadata
            return f"{m.num_rows:,}", str(m.num_columns)
        if ext in {".xlsx", ".xls"}:
            import pandas as pd
            df = pd.read_excel(path, nrows=5)
            return "?", str(df.shape[1])
    except Exception:
        pass
    return "?", "?"


def scan(folder: Path, max_depth: int) -> list[dict]:
    found = []
    for p in sorted(folder.rglob("*")):
        rel = p.relative_to(folder)
        if len(rel.parts) > max_depth or not p.is_file() or p.suffix.lower() not in EXTS:
            continue
        if any(part in SKIP or part.startswith("output_") for part in rel.parts[:-1]):
            continue
        rows, cols = peek(p)
        found.append({"path": str(p), "rel": str(rel), "type": p.suffix.lower().lstrip("."),
                      "size": p.stat().st_size, "rows": rows, "cols": cols})
    return found


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-depth", type=int, default=6)
    a = ap.parse_args()
    folder = Path(a.folder).expanduser().resolve()
    if not folder.is_dir():
        sys.exit(f"Not a folder: {folder}")
    items = scan(folder, a.max_depth)
    if a.json:
        print(json.dumps(items, indent=2))
        return
    if not items:
        print(f"No datasets ({', '.join(sorted(EXTS))}) found under {folder}")
        return
    print(f"Datasets under {folder}\n")
    print(f"{'#':>3}  {'type':<7} {'size':>9} {'rows':>10} {'cols':>5}  file")
    for i, d in enumerate(items, 1):
        print(f"{i:>3}  {d['type']:<7} {human(d['size']):>9} {d['rows']:>10} {d['cols']:>5}  {d['rel']}")
    print("\nPick one by number, or paste a path.")


if __name__ == "__main__":
    main()
