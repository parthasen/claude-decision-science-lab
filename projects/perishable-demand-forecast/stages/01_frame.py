# %% [markdown]
# # Stage 01 — Frame: weekly demand forecast per store x article
# Goal: confirm target, unit of analysis and baselines using the raw file.
# %%
import pandas as pd
d = pd.read_csv("data/raw/perishable_45k.csv", low_memory=False, parse_dates=["BILL_DATE"])
print(d.shape); print(d.dtypes.head(20))
# %%
sale = d[d.BILL_TYPE.eq("Sale")]
sale = sale.assign(week=sale.BILL_DATE.dt.to_period("W-SUN").dt.start_time)
print("sale rows", len(sale), "qty==0:", (sale.BILL_QUANTITY == 0).sum())
sale = sale[sale.BILL_QUANTITY > 0]
# store code hygiene: SITE (10 codes) vs SITE_NAME (5)
print(d.groupby("SITE_NAME").SITE.unique())
# %%
w = sale.groupby(["SITE_NAME", "ARTICLE", "week"]).BILL_QUANTITY.sum().rename("weekly_units").reset_index()
print("series:", w.groupby(["SITE_NAME", "ARTICLE"]).ngroups, "weeks:", w.week.nunique())
full = w.groupby(["SITE_NAME", "ARTICLE"]).week.nunique()
print("weeks with sales per series (of ~53): median", full.median(), "min", full.min())
print("train weeks <2025-01-01:", (w.week < "2025-01-01").sum(), "test:", (w.week >= "2025-01-01").sum())
# %%
# naive baselines on the proposed split (missing weeks = 0 units)
import numpy as np
g = w.set_index(["SITE_NAME","ARTICLE","week"]).weekly_units
wide = g.unstack("week").fillna(0)
test = [c for c in wide.columns if c >= pd.Timestamp("2025-01-01")]
last = wide.shift(1, axis=1)[test]
yt = wide[test]
print("last-week WAPE:", round((yt - last).abs().sum().sum() / yt.sum().sum(), 3))
# %%
# seasonal-naive (same week previous year) is impossible with 1 year of data -> use last-week and trailing-4-week mean
m4 = wide.T.rolling(4).mean().shift(1).T[test]
print("trailing-4wk-mean WAPE:", round((yt - m4).abs().sum().sum() / yt.sum().sum(), 3))
print("mean weekly units per series:", round(yt.values.mean(), 1))
