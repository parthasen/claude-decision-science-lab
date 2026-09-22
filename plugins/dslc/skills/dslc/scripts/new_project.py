#!/usr/bin/env python
"""Create a DSLC project workspace.

Usage: python new_project.py <project-name> [--root projects] [--runtime local|jupyter-live|colab]
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

STAGES = [
    "01_frame", "02_acquire", "03_profile", "04_prepare",
    "05_stats", "06_model", "07_explain", "08_report",
]


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--root", default="projects")
    ap.add_argument("--runtime", default="local", choices=["local", "jupyter-live", "colab"])
    args = ap.parse_args()

    slug = slugify(args.name)
    proj = Path(args.root) / slug
    if (proj / "project.yaml").exists():
        sys.exit(f"Project already exists: {proj}")

    for sub in ["data/raw", "data/external", "data/interim", "data/processed",
                "notebooks", "models", "figures", "reports", "stages"]:
        (proj / sub).mkdir(parents=True, exist_ok=True)

    config = {
        "name": args.name,
        "slug": slug,
        "created": dt.date.today().isoformat(),
        "runtime": args.runtime,
        "python": sys.executable,
        "kernels": {"python": "dslc", "r": "ir-dslc"},
        "language": "python",  # python | r | both
        "random_seed": 42,
        "context": {
            "business_question": None,
            "domain": None,
            "decision_to_support": None,
            "stakeholders": None,
            "constraints": None,
        },
        "problem": {
            "type": None,  # classification | regression | forecasting | clustering | inference | descriptive
            "target": None,
            "unit_of_analysis": None,
            "primary_metric": None,
            "success_threshold": None,
        },
        "data_policy": {
            "confidential": True,  # if True, never send raw rows to external services
            "external_enrichment_allowed": False,
        },
        "stages": {s: {"status": "pending", "approved_on": None} for s in STAGES},
    }
    (proj / "project.yaml").write_text(yaml.safe_dump(config, sort_keys=False))
    (proj / "SOURCES.md").write_text(
        "# Data sources\n\n| File | Origin (URL / owner) | License / terms | Retrieved | Approved by |\n|---|---|---|---|---|\n"
    )
    (proj / "DECISIONS.md").write_text("# Decision log\n\n| Date | Stage | Decision | Rationale | Approved by |\n|---|---|---|---|---|\n")
    (proj / ".gitignore").write_text("data/\nmodels/\n.ipynb_checkpoints/\n")
    print(f"Created {proj.resolve()}")


if __name__ == "__main__":
    main()
