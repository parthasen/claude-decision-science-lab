# %% [markdown]
# # Stage 03 — Profile and data quality (forecasting-focused)
# Goal: know what could mislead a weekly demand model on SITE_NAME x ARTICLE.
# %%
import sys
sys.path.insert(0, "../../plugins/dslc/skills/dslc/scripts")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from dslc_style import apply_style, SERIES, INK, save
apply_style()
d = pd.read_csv("data/raw/perishable_45k.csv", low_memory=False, parse_dates=["BILL_DATE", "EXPIRY_DATE"])
print(d.shape, d.memory_usage(deep=True).sum() // 2**20, "MB", d.BILL_DATE.min(), d.BILL_DATE.max())
# %% [markdown]
# ## Data dictionary
# %%
dd = pd.DataFrame({"dtype": d.dtypes.astype(str), "pct_missing": (d.isna().mean() * 100).round(1),
                   "n_unique": d.nunique(), "example": [d[c].dropna().iloc[0] if d[c].notna().any() else None for c in d.columns]})
import os; os.makedirs("reports/tables", exist_ok=True)
dd.to_csv("reports/tables/data_dictionary.csv"); print(dd.to_string())
# %% [markdown]
# ## Quality checks
# %%
q = {}
q["exact_duplicate_rows"] = int(d.duplicated().sum())
q["dup_bill_article"] = int(d.dropna(subset=["BILL_NO"]).duplicated(["BILL_NO", "ARTICLE"]).sum())
q["sale_qty0"] = int(((d.BILL_TYPE == "Sale") & (d.BILL_QUANTITY == 0)).sum())
q["return_rows"] = int((d.BILL_TYPE == "Return").sum())
q["return_positive_net"] = int(((d.BILL_TYPE == "Return") & (d.NET_AMOUNT > 0)).sum())
q["sale_negative_net"] = int(((d.BILL_TYPE == "Sale") & (d.NET_AMOUNT < 0)).sum())
q["expiry_before_bill"] = int((d.EXPIRY_DATE < d.BILL_DATE).sum())
q["article_missing"] = int(d.ARTICLE.isna().sum())
q["division_missing"] = int(d.DIVISION.isna().sum())
q["site_name_missing"] = int(d.SITE_NAME.isna().sum())
site_ok = {"East-Fresh", "Metro-Fresh", "RVM1-Fresh", "RVM2-Fresh", "West-Fresh"}
q["site_junk_codes"] = int((~d.SITE.isin(site_ok)).sum())
print(pd.Series(q).to_string())
print(d._quality_tier.value_counts(dropna=False).to_string())
print(d.SALES_CHANNEL.value_counts(dropna=False).to_string())
print(sorted(d.ARTICLE.dropna().unique()))
# article -> division consistency
print(d.groupby("ARTICLE").DIVISION.nunique().value_counts().to_string())
# %%
# amount consistency: NET_AMOUNT vs RATE_TOTAL+TAX on Sale rows
s = d[(d.BILL_TYPE == "Sale") & (d.BILL_QUANTITY > 0)].copy()
s["calc"] = s.RATE_TOTAL + s.TAXAMT
print("Sale rows |NET - (RATE_TOTAL+TAX)| > 1:", int(((s.NET_AMOUNT - s.calc).abs() > 1).sum()), "of", len(s))
print("RATE per unit vs RATE_TOTAL/qty mismatch:", int(((s.RATE_TOTAL / s.BILL_QUANTITY - s.RATE).abs() > 0.05).sum()))
# outliers in rate within article
z = s.groupby("ARTICLE").RATE.transform(lambda x: (x - x.median()) / (x.mad() if hasattr(x, "mad") else (x - x.median()).abs().median() * 1.4826 + 1e-9))
print("rate robust-z > 5:", int((z.abs() > 5).sum()))
print("rate CV within article (median):", round(s.groupby("ARTICLE").RATE.agg(lambda x: x.std() / x.mean()).median(), 3))
# %% [markdown]
# ## Target: weekly units per store x article (Sale, qty>0)
# %%
s = s[s.SITE_NAME.notna() & s.ARTICLE.notna()]
s["week"] = s.BILL_DATE.dt.to_period("W-SUN").dt.start_time
w = s.groupby(["SITE_NAME", "ARTICLE", "week"]).BILL_QUANTITY.sum().rename("weekly_units").reset_index()
print(w.weekly_units.describe().round(2).to_string())
print("zero-inflation: share of series-weeks with no sales (of full grid):",
      round(1 - len(w) / (w.groupby(["SITE_NAME", "ARTICLE"]).ngroups * w.week.nunique()), 3))
tot = w.groupby("week").weekly_units.sum()
print("first/last week partial? units:", tot.iloc[0], tot.iloc[-1], "median", tot.median())
# %%
# drift by month
m = s.groupby(s.BILL_DATE.dt.to_period("M")).agg(units=("BILL_QUANTITY", "sum"), rate=("RATE", "mean"), lines=("RATE", "size"))
print(m.round(1).to_string())
by_site = w.groupby("SITE_NAME").weekly_units.sum(); print(by_site.to_string())
# %%
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
tot.plot(ax=ax[0], color=SERIES[0]); ax[0].set_title("Total units per week (all stores)"); ax[0].set_ylabel("units"); ax[0].set_xlabel("")
w.weekly_units.clip(upper=w.weekly_units.quantile(.99)).plot.hist(bins=30, ax=ax[1], color=SERIES[0]); ax[1].set_title("Weekly units per store x article"); ax[1].set_xlabel("units (99th pct capped)")
save(fig, "03_target")
miss = (d.isna().mean() * 100).sort_values(ascending=False); miss = miss[miss > 0]
fig, ax = plt.subplots(figsize=(7, 4)); miss.iloc[::-1].plot.barh(ax=ax, color=SERIES[0]); ax.set_xlabel("% missing"); ax.set_title("Missing values by column")
save(fig, "03_missing")
# %%
try:
    from ydata_profiling import ProfileReport
    ProfileReport(d, minimal=True, title="perishable_45k profile").to_file("reports/03_profile.html")
    print("profile html written")
except Exception as e:
    print("ydata-profiling skipped:", type(e).__name__, e)
