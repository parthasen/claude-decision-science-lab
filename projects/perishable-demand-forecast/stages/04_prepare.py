# %% [markdown]
# # Stage 04 — Prepare: weekly panel, leakage-safe features, time split
# Forecast horizon: 1 week ahead. Every feature for week t uses only weeks < t (plus static article facts).
# %%
import os
import numpy as np, pandas as pd
d = pd.read_csv("data/raw/perishable_45k.csv", low_memory=False, parse_dates=["BILL_DATE"])
n0 = len(d)
s = d[(d.BILL_TYPE == "Sale") & (d.BILL_QUANTITY > 0) & d.ARTICLE.notna()].copy()
s = s[s.BILL_DATE < "2025-03-31"]           # drop final one-day week
print(f"rows {n0} -> {len(s)} sale lines kept")
s["week"] = s.BILL_DATE.dt.to_period("W-SUN").dt.start_time
# %%
w = s.groupby(["SITE_NAME", "ARTICLE", "week"]).BILL_QUANTITY.sum().rename("units").reset_index()
weeks = pd.date_range(w.week.min(), w.week.max(), freq="7D")
series = w[["SITE_NAME", "ARTICLE"]].drop_duplicates()
grid = series.merge(pd.DataFrame({"week": weeks}), how="cross")
p = grid.merge(w, how="left", on=["SITE_NAME", "ARTICLE", "week"]).fillna({"units": 0})
p = p.sort_values(["SITE_NAME", "ARTICLE", "week"]).reset_index(drop=True)
print("weeks", len(weeks), weeks.min().date(), weeks.max().date(), "| series", len(series), "| rows", len(p))
# %%
# static article facts (mode; identical for the whole article in the source)
art = (d.dropna(subset=["ARTICLE"]).groupby("ARTICLE")
        .agg(division=("DIVISION", lambda x: x.mode().iat[0] if x.notna().any() else np.nan),
             shelf_life_days=("SHELF_LIFE_DAYS", "median"),
             storage=("STORAGE_CONDITION", lambda x: x.mode().iat[0] if x.notna().any() else "Unknown"),
             avg_rate=("RATE", "median")).reset_index())
print(art.isna().sum().to_string())
p = p.merge(art, on="ARTICLE", how="left")
# %%
g = p.groupby(["SITE_NAME", "ARTICLE"]).units
for k in (1, 2, 3, 4):
    p[f"lag{k}"] = g.shift(k)
p["roll4_mean"] = g.transform(lambda x: x.shift(1).rolling(4, min_periods=1).mean())
p["roll8_mean"] = g.transform(lambda x: x.shift(1).rolling(8, min_periods=1).mean())
p["roll4_std"] = g.transform(lambda x: x.shift(1).rolling(4, min_periods=2).std())
p["expanding_mean"] = g.transform(lambda x: x.shift(1).expanding(min_periods=1).mean())
p["woy"] = p.week.dt.isocalendar().week.astype(int)
p["month"] = p.week.dt.month
tot = p.groupby(["SITE_NAME", "week"]).units.sum().rename("t").reset_index().sort_values(["SITE_NAME", "week"])
tot["store_total_lag1"] = tot.groupby("SITE_NAME").t.shift(1)
p = p.merge(tot[["SITE_NAME", "week", "store_total_lag1"]], on=["SITE_NAME", "week"])
# %%
# time split: train weeks starting <= 2024-12-30 ; test weeks starting >= 2025-01-06
p["split"] = np.where(p.week >= "2025-01-06", "test", "train")
p = p.dropna(subset=["lag4"]).reset_index(drop=True)      # need 4 weeks of history
print(p.split.value_counts().to_string())
print("train weeks", p[p.split == "train"].week.min().date(), p[p.split == "train"].week.max().date(),
      "| test weeks", p[p.split == "test"].week.min().date(), p[p.split == "test"].week.max().date())
# leakage assertions: rebuild lags/rolling means independently from the raw weekly grid
key = ["SITE_NAME", "ARTICLE"]
raw = grid.merge(w, how="left", on=key + ["week"]).fillna({"units": 0}).set_index(key + ["week"]).units
chk = p.sample(500, random_state=42)
for _, r in chk.iterrows():
    hist = raw.loc[(r.SITE_NAME, r.ARTICLE)]
    prev = hist[hist.index < r.week]
    assert r.lag1 == prev.iloc[-1] and r.lag4 == prev.iloc[-4], "lag mismatch"
    assert abs(r.roll4_mean - prev.iloc[-4:].mean()) < 1e-9 and abs(r.expanding_mean - prev.mean()) < 1e-9, "rolling mismatch"
    assert prev.index.max() < r.week
print("leakage checks passed on 500 sampled rows")
assert p[p.split == "train"].week.max() < p[p.split == "test"].week.min()
te = p[p.split == "test"]
print("target NaN:", p.units.isna().sum(), "| features NaN:\n", p.isna().sum()[lambda x: x > 0].to_string())
# %%
os.makedirs("data/processed", exist_ok=True)
p.to_parquet("data/processed/weekly_panel.parquet", index=False)
art.to_csv("data/processed/article_dim.csv", index=False)
# baselines on the corrected test window
def wape(y, f): return float(np.abs(y - f).sum() / y.sum())
print("test WAPE  last-week:", round(wape(te.units, te.lag1), 3),
      "| 4wk-mean:", round(wape(te.units, te.roll4_mean), 3),
      "| 8wk-mean:", round(wape(te.units, te.roll8_mean), 3),
      "| expanding-mean:", round(wape(te.units, te.expanding_mean), 3))
print("test mean units:", round(te.units.mean(), 2), "| zero share:", round((te.units == 0).mean(), 3))
