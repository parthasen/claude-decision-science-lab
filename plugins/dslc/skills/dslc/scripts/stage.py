#!/usr/bin/env python
"""Show or update DSLC stage status.

Usage:
  python stage.py <project-dir>                       # print tracker
  python stage.py <project-dir> <stage> <status>      # status: pending|in_progress|awaiting_approval|approved|skipped
  python stage.py <project-dir> --set key.path value  # e.g. --set problem.target churn
"""
import datetime as dt
import sys
from pathlib import Path

import yaml

ICONS = {"pending": "[ ]", "in_progress": "[~]", "awaiting_approval": "[?]", "approved": "[x]", "skipped": "[-]"}
VALID = set(ICONS)


def load(p: Path) -> dict:
    return yaml.safe_load((p / "project.yaml").read_text())


def save(p: Path, cfg: dict) -> None:
    (p / "project.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False))


def coerce(v: str):
    low = v.lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "none"):
        return None
    for cast in (int, float):
        try:
            return cast(v)
        except ValueError:
            pass
    return v


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    proj = Path(sys.argv[1])
    cfg = load(proj)

    if len(sys.argv) == 5 and sys.argv[2] == "--set":
        node = cfg
        *parents, leaf = sys.argv[3].split(".")
        for k in parents:
            node = node.setdefault(k, {})
        node[leaf] = coerce(sys.argv[4])
        save(proj, cfg)
    elif len(sys.argv) == 4:
        stage, status = sys.argv[2], sys.argv[3]
        if stage not in cfg["stages"] or status not in VALID:
            sys.exit(f"Unknown stage or status. Stages: {list(cfg['stages'])}; statuses: {sorted(VALID)}")
        cfg["stages"][stage]["status"] = status
        cfg["stages"][stage]["approved_on"] = dt.date.today().isoformat() if status == "approved" else None
        save(proj, cfg)

    print(f"Project: {cfg['name']}  |  runtime: {cfg['runtime']}  |  language: {cfg['language']}")
    for s, info in cfg["stages"].items():
        print(f"  {ICONS.get(info['status'], '[ ]')} {s:<12} {info['status']}")


if __name__ == "__main__":
    main()
