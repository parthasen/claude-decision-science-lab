# %% [markdown]
# # Stage 07 — Explain and validate the chosen model (article mean)
# The model is transparent: forecast = the article's average weekly units per store in training. SHAP/PDP add nothing;
# the useful checks are where it is wrong, whether it is calibrated, and how stable the article levels are.
# %%
import sys, json
sys.path.insert(0, "../../plugins/dslc/skills/dslc/scripts")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from dslc_style import apply_style, SERIES, INK, save
apply_style()
p = pd.read_parquet("data/processed/weekly_panel.parquet")
tr = p[p.split == "train"]
t = pd.read_csv("reports/tables/06_test_predictions.csv", parse_dates=["week"]).merge(p[["SITE_NAME", "ARTICLE", "week", "division", "shelf_life_days", "storage"]], on=["SITE_NAME", "ARTICLE", "week"])
t["ae"] = (t.units - t.pred).abs(); t["err"] = t.pred - t.units
def seg(col):
    g = t.groupby(col).agg(units=("units", "sum"), pred=("pred", "sum"), ae=("ae", "sum"), n=("units", "size"))
    g["wape"] = g.ae / g.units; g["bias"] = (g.pred - g.units) / g.units; return g.round(3)
# %% [markdown]
# ## Where is it wrong?
# %%
for c in ["division", "SITE_NAME", "storage"]:
    print(seg(c).to_string(), "\n")
a = seg("ARTICLE").sort_values("wape"); print(a.to_string())
a.to_csv("reports/tables/07_error_by_article.csv")
t["vol_band"] = pd.qcut(t.pred, 4, labels=["lowest 25%", "25-50%", "50-75%", "top 25%"]); print(seg("vol_band").to_string())
print(seg(t.week.dt.to_period("M")).to_string())
# %% [markdown]
# ## Calibration: do the P10–P90 bands hold for every store and division?
# %%
t["in80"] = (t.units >= t.p10) & (t.units <= t.p90); t["below_p80"] = t.units <= t.p80
print(t.groupby("SITE_NAME")[["in80", "below_p80"]].mean().round(3).to_string()); print(t.groupby("division")[["in80", "below_p80"]].mean().round(3).to_string())
# calibration of the point forecast: predicted-band vs actual mean
t["pbin"] = pd.qcut(t.pred, 8, duplicates="drop"); cal = t.groupby("pbin", observed=True).agg(pred=("pred", "mean"), actual=("units", "mean")).round(2); print(cal.to_string())
# %% [markdown]
# ## Stability: how much would the article levels have moved with a different window?
# %%
first = tr[tr.week < "2024-08-26"].groupby(["SITE_NAME", "ARTICLE"]).units.mean(); last = tr[tr.week >= "2024-08-26"].groupby(["SITE_NAME", "ARTICLE"]).units.mean()
allm = tr.groupby(["SITE_NAME", "ARTICLE"]).units.mean()
print("corr first-half vs second-half series means:", round(first.corr(last), 3))
te = p[p.split == "test"]
def wape(y, f): return float(np.abs(y - f).sum() / y.sum())
for name, m in [("all train", allm), ("first half of train only", first), ("second half of train only", last)]:
    f = te.set_index(["SITE_NAME", "ARTICLE"]).index.map(m).values; print(f"{name:28s} test WAPE {wape(te.units.values, f):.3f}")
# pooled across stores (article only) vs per store
am = tr.groupby("ARTICLE").units.mean(); print("article-pooled mean test WAPE:", round(wape(te.units.values, te.ARTICLE.map(am).values), 3))
# %% [markdown]
# ## Fairness / sensitive groups
# Not applicable: units are product-level counts, no individuals or protected attributes are modelled.
# %%
fig, ax = plt.subplots(figsize=(8, 6)); a2 = a.sort_values("wape")
ax.barh(a2.index, a2.wape, color=SERIES[0]); ax.axvline(t.ae.sum() / t.units.sum(), color=SERIES[1], lw=1.5); ax.tick_params(axis="y", labelsize=7)
ax.set_xlabel("Test WAPE (orange line = overall)"); ax.set_title("Forecast error by article"); save(fig, "07_error_article")
fig, ax = plt.subplots(figsize=(5.5, 5)); mx = max(cal.pred.max(), cal.actual.max()) * 1.05
ax.plot([0, mx], [0, mx], color=INK["muted"], ls="--", lw=1); ax.scatter(cal.pred, cal.actual, color=SERIES[0], s=40)
ax.set_xlabel("forecast (avg units)"); ax.set_ylabel("actual (avg units)"); ax.set_title("Calibration on test"); save(fig, "07_calibration")
