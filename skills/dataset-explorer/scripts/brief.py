#!/usr/bin/env python
"""Describe a dataset, run basic stats, and suggest search terms + candidate models.

Usage: python brief.py <file> [--sheet NAME] [--out DIR] [--objective "text"] [--sample 200000]
Writes <out>/brief.md, <out>/stats.json and <out>/suggestions.json (default out: LAB/outputs/<file-stem>/).
Prints the markdown brief. Heuristic, name-based inference — Claude must review and refine it.
"""
import argparse
import json
import warnings
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROLE_PATTERNS = {
    "date": r"date|time|day|month|year|timestamp|dt$",
    "id": r"(^|_|\b)(id|no|number|code|barcode|sku|key)($|_|\b)|bill_?no|mobile|phone",
    "customer": r"customer|client|user|member|cust|loyal",
    "product": r"product|item|article|sku|brand|category|dept|division|section|hsn|desc",
    "store": r"store|site|branch|shop|outlet|location|city|region",
    "price": r"price|rate|mrp|amount|amt|revenue|sales|value|cost|margin|discount|total",
    "quantity": r"qty|quantity|units|count|volume",
    "target_churn": r"churn|attrit|cancel|left",
    "target_label": r"^(target|label|class|outcome|y)$|fraud|default|return(ed)?$|spoil|waste|expired",
}

DOMAIN_HINTS = {
    "retail / POS": r"bill|pos|store|site|mrp|sku|barcode|basket|article|hsn|invoice",
    "perishable / grocery": r"perish|expiry|shelf|spoil|fresh|waste|grocery|produce",
    "customer / CRM": r"customer|churn|tenure|loyal|rfm|segment",
    "finance": r"loan|credit|interest|balance|default|invoice",
    "healthcare": r"patient|diagnos|admission|drug|dose",
    "web / marketing": r"click|session|campaign|impression|utm|conversion",
}


def load(path: Path, sheet: str | None, sample: int) -> tuple[pd.DataFrame, int]:
    ext = path.suffix.lower()
    if ext in {".csv", ".tsv"}:
        df = pd.read_csv(path, sep="\t" if ext == ".tsv" else ",", low_memory=False, encoding_errors="replace")
    elif ext in {".xlsx", ".xls"}:
        df = pd.read_excel(path, sheet_name=sheet or 0)
    elif ext == ".parquet":
        df = pd.read_parquet(path)
    elif ext in {".json", ".jsonl"}:
        df = pd.read_json(path, lines=ext == ".jsonl")
    else:
        sys.exit(f"Unsupported file type: {ext}")
    n = len(df)
    if n > sample:
        df = df.sample(sample, random_state=42)
    return df, n


def infer_roles(df: pd.DataFrame) -> dict[str, list[str]]:
    roles: dict[str, list[str]] = {}
    for col in df.columns:
        name = str(col).lower()
        for role, pat in ROLE_PATTERNS.items():
            if re.search(pat, name):
                roles.setdefault(role, []).append(col)
    # parse-able date columns by content
    for col in df.select_dtypes(include="object").columns:
        if col in roles.get("date", []):
            continue
        s = df[col].dropna().astype(str).head(200)
        if len(s) and pd.to_datetime(s, errors="coerce").notna().mean() > 0.9 and s.str.contains(r"\d").all():
            roles.setdefault("date", []).append(col)
    return roles


def coerce_dates(df: pd.DataFrame, cols: list[str]) -> list[str]:
    ok = []
    for c in cols:
        parsed = pd.to_datetime(df[c], errors="coerce")
        if parsed.notna().mean() > 0.8 and parsed.nunique() > 1:
            df[c] = parsed
            ok.append(c)
    return ok


def stats(df: pd.DataFrame, total_rows: int, date_cols: list[str], id_cols: list[str]) -> dict:
    num = df.select_dtypes(include="number").drop(columns=[c for c in id_cols if c in df.columns], errors="ignore")
    cat = df.select_dtypes(exclude=["number", "datetime"])
    s: dict = {
        "rows": total_rows, "cols": df.shape[1],
        "duplicate_rows_in_sample": int(df.duplicated().sum()),
        "missing_pct": (df.isna().mean() * 100).round(2).sort_values(ascending=False).head(15).to_dict(),
        "constant_cols": [c for c in df.columns if df[c].nunique(dropna=False) <= 1],
        "numeric": {}, "categorical": {}, "dates": {}, "top_correlations": [],
    }
    if not num.empty:
        d = num.describe().T
        d["skew"] = num.skew()
        s["numeric"] = d.round(3).replace({np.nan: None}).to_dict("index")
        if num.shape[1] > 1:
            c = num.corr(numeric_only=True).abs().where(lambda x: np.triu(np.ones(x.shape), 1).astype(bool)).stack()
            s["top_correlations"] = [(a, b, round(float(v), 3)) for (a, b), v in c.sort_values(ascending=False).head(8).items()]
    for col in cat.columns[:30]:
        vc = df[col].value_counts(dropna=True)
        s["categorical"][col] = {"unique": int(df[col].nunique()), "top": {str(k): int(v) for k, v in vc.head(5).items()}}
    for col in date_cols:
        s["dates"][col] = {"min": str(df[col].min()), "max": str(df[col].max())}
    return s


def pick_money(cols: list[str]) -> str:
    pref = [c for c in cols if re.search(r"net|sales|revenue|total", str(c).lower()) and not re.search(r"tax|gst", str(c).lower())]
    clean = [c for c in cols if not re.search(r"tax|gst", str(c).lower())]
    return (pref or clean or cols)[0]


def suggest(df: pd.DataFrame, roles: dict, date_cols: list[str], objective: str | None) -> dict:
    cols_text = " ".join(map(str, df.columns)).lower()
    domains = [d for d, p in DOMAIN_HINTS.items() if re.search(p, cols_text)] or ["general tabular"]
    has = lambda r: bool(roles.get(r))
    models = []
    if has("date") and (has("price") or has("quantity")):
        models.append({"objective": "Forecast sales / demand by store, product or day", "type": "time-series regression",
                       "models": "Seasonal-naive baseline, ETS/Prophet, LightGBM with lags", "target": roles["quantity"][0] if has("quantity") else pick_money(roles["price"]),
                       "metric": "MAPE / WAPE, RMSE"})
    if has("customer") and has("date") and has("price"):
        models.append({"objective": "Segment customers by value and behaviour (RFM)", "type": "clustering",
                       "models": "RFM scoring, K-Means, Gaussian mixture", "target": "none (unsupervised)", "metric": "Silhouette, business interpretability"})
        models.append({"objective": "Predict customer churn / lapse or next-purchase propensity", "type": "classification",
                       "models": "Logistic regression baseline, XGBoost/LightGBM", "target": "derive: no purchase in next N days", "metric": "PR-AUC, recall@k, lift"})
        models.append({"objective": "Estimate customer lifetime value", "type": "regression",
                       "models": "BG/NBD + Gamma-Gamma, gradient boosting", "target": "future spend", "metric": "MAE, decile lift"})
    if has("product") and has("id"):
        models.append({"objective": "Market-basket analysis: cross-sell and bundles", "type": "association rules / recommender",
                       "models": "Apriori / FP-Growth, item-item similarity", "target": "none (unsupervised)", "metric": "Support, confidence, lift"})
    if has("price") and has("quantity"):
        models.append({"objective": "Price elasticity and promotion impact", "type": "regression",
                       "models": "Log-log OLS, mixed effects, causal uplift", "target": "log(quantity)", "metric": "Elasticity CI, holdout error"})
    if "perishable / grocery" in domains:
        models.append({"objective": "Reduce spoilage: demand forecast + markdown / reorder optimisation", "type": "forecast + optimisation",
                       "models": "Quantile LightGBM, newsvendor policy", "target": "units sold / waste units", "metric": "Waste %, service level"})
    if has("target_churn") or has("target_label"):
        t = (roles.get("target_churn") or roles.get("target_label"))[0]
        models.append({"objective": f"Predict `{t}` (labelled target detected)", "type": "classification",
                       "models": "Logistic regression, random forest, XGBoost/LightGBM", "target": t, "metric": "ROC-AUC, PR-AUC, calibration"})
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) >= 4:
        models.append({"objective": "Detect anomalies (bad bills, data errors, fraud)", "type": "anomaly detection",
                       "models": "Isolation Forest, robust z-score, LOF", "target": "none (unsupervised)", "metric": "Precision@k on reviewed cases"})
    if not models:
        models.append({"objective": "Explore structure first", "type": "EDA + clustering",
                       "models": "PCA, K-Means", "target": "to be defined with user", "metric": "n/a"})

    kw = [c for c in df.columns if not re.search(r"^unnamed|^\d+$", str(c).lower())]
    core = re.sub(r"[_\-]+", " ", " ".join(map(str, kw[:6])))
    return {"domains": domains, "candidate_models": models,
            "search_queries": [
                f"kaggle {domains[0]} dataset {core}",
                f"{domains[0]} transactions dataset csv open data",
                f"{domains[0]} sales dataset {' '.join(roles.get('product', [''])[:1])} kaggle",
                f"site:huggingface.co/datasets {domains[0]}",
                f"UCI machine learning repository {domains[0]}",
            ],
            "kaggle_cli": f'kaggle datasets list -s "{domains[0].split(" /")[0]} {"sales" if has("price") else ""}" --sort-by votes',
            "objective_given": objective}


def render(path: Path, df: pd.DataFrame, s: dict, roles: dict, sug: dict) -> str:
    L = [f"# Dataset brief — {path.name}", "",
         f"**Shape:** {s['rows']:,} rows × {s['cols']} columns  ", f"**Likely domain:** {', '.join(sug['domains'])}  ",
         f"**Grain (guess):** one row per {'line item / transaction' if roles.get('id') and roles.get('product') else 'record'}", ""]
    L += ["## What it contains", ""]
    for role, cols in roles.items():
        L.append(f"- **{role}**: {', '.join(f'`{c}`' for c in cols[:6])}")
    for c, d in s["dates"].items():
        L.append(f"- `{c}` spans {d['min']} → {d['max']}")
    L += ["", "## Data quality", "",
          f"- Duplicate rows (in analysed sample): {s['duplicate_rows_in_sample']:,}",
          f"- Constant columns: {', '.join(s['constant_cols']) or 'none'}"]
    miss = {k: v for k, v in s["missing_pct"].items() if v > 0}
    L.append("- Missing values: " + (", ".join(f"`{k}` {v}%" for k, v in miss.items()) or "none"))
    if s["numeric"]:
        L += ["", "## Numeric summary", "", "| column | mean | std | min | median | max | skew |", "|---|---|---|---|---|---|---|"]
        for c, d in list(s["numeric"].items())[:15]:
            L.append(f"| {c} | {d['mean']} | {d['std']} | {d['min']} | {d['50%']} | {d['max']} | {d['skew']} |")
    if s["categorical"]:
        L += ["", "## Categorical summary", "", "| column | unique | top values |", "|---|---|---|"]
        for c, d in list(s["categorical"].items())[:12]:
            L.append(f"| {c} | {d['unique']} | {', '.join(f'{k} ({v})' for k, v in d['top'].items())} |")
    if s["top_correlations"]:
        L += ["", "## Strongest numeric correlations (|r|)", ""]
        L += [f"- `{a}` ~ `{b}`: {v}" for a, b, v in s["top_correlations"]]
    L += ["", "## Candidate models and objectives", "", "| objective | type | models | target | metric |", "|---|---|---|---|---|"]
    for m in sug["candidate_models"]:
        L.append(f"| {m['objective']} | {m['type']} | {m['models']} | {m['target']} | {m['metric']} |")
    L += ["", "## Similar-dataset search", "", "Queries: " + "; ".join(f"`{q}`" for q in sug["search_queries"]),
          "", f"Kaggle CLI: `{sug['kaggle_cli']}`", "",
          "> Auto-generated from column names and values. Confirm meaning with the data owner before modelling."]
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--sheet")
    ap.add_argument("--out")
    ap.add_argument("--objective")
    ap.add_argument("--sample", type=int, default=200_000)
    a = ap.parse_args()
    path = Path(a.file).expanduser().resolve()
    df, total = load(path, a.sheet, a.sample)
    roles = infer_roles(df)
    date_cols = coerce_dates(df, roles.get("date", []))
    roles["date"] = date_cols
    roles = {k: v for k, v in roles.items() if v}
    s = stats(df, total, date_cols, roles.get("id", []))
    sug = suggest(df, roles, date_cols, a.objective)
    md = render(path, df, s, roles, sug)
    out = Path(a.out) if a.out else Path(__file__).resolve().parents[3] / "outputs" / re.sub(r"\W+", "_", path.stem)
    out.mkdir(parents=True, exist_ok=True)
    (out / "brief.md").write_text(md)
    (out / "stats.json").write_text(json.dumps(s, indent=2, default=str))
    (out / "suggestions.json").write_text(json.dumps(sug, indent=2, default=str))
    print(md)
    print(f"\n[saved to {out}]")


if __name__ == "__main__":
    main()
