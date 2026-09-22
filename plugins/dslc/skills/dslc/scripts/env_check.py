#!/usr/bin/env python
"""Report which DSLC capabilities are ready. Never prints secret values."""
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path

PY_PKGS = ["pandas", "numpy", "scipy", "statsmodels", "pingouin", "sklearn", "xgboost", "lightgbm",
           "optuna", "shap", "matplotlib", "seaborn", "plotly", "ydata_profiling", "pandera",
           "feature_engine", "fairlearn", "papermill", "nbclient", "kaggle", "huggingface_hub", "datasets"]


def ok(flag: bool) -> str:
    return "OK " if flag else "-- "


def main() -> None:
    print("Python packages")
    for p in PY_PKGS:
        print(f"  {ok(importlib.util.find_spec(p) is not None)}{p}")

    print("\nJupyter kernels")
    try:
        specs = json.loads(subprocess.run(["jupyter", "kernelspec", "list", "--json"],
                                          capture_output=True, text=True).stdout)["kernelspecs"]
    except Exception:
        specs = {}
    for k in ["dslc", "ir-dslc"]:
        print(f"  {ok(k in specs)}{k}")

    print("\nCredentials (presence only)")
    kaggle = Path.home() / ".kaggle" / "kaggle.json"
    print(f"  {ok(kaggle.exists() or bool(os.getenv('KAGGLE_KEY')))}Kaggle token")
    print(f"  {ok(bool(os.getenv('HF_TOKEN')))}HF_TOKEN (optional; public datasets work without it)")
    print(f"  {ok(bool(os.getenv('FRED_API_KEY')))}FRED_API_KEY (optional)")

    print("\nTools")
    for t in ["uvx", "Rscript"]:
        print(f"  {ok(shutil.which(t) is not None)}{t}")


if __name__ == "__main__":
    main()
