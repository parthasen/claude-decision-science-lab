# %% [markdown]
# # Stage 05 — EDA and statistics (train period only)
# Where is the signal? store vs article, autocorrelation, seasonality, shelf life. Test weeks are not used.
# %%
import sys
sys.path.insert(0, "../../plugins/dslc/skills/dslc/scripts")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import statsmodels.formula.api as smf, statsmodels.api as sm
from scipy import stats
from dslc_style import apply_style, SERIES, INK, save
apply_style()
p = pd.read_parquet("data/processed/weekly_panel.parquet")
tr = p[p.split == "train"].copy()
print(tr.shape, tr.week.min().date(), tr.week.max().date())
print(tr.units.describe().round(2).to_string())
# %% [markdown]
# ## 1. How much variance is store vs article? (ANOVA, eta-squared)
# %%
res = {}
for f in ["C(ARTICLE)", "C(SITE_NAME)", "C(division)", "C(month)", "C(ARTICLE) + C(SITE_NAME)", "C(ARTICLE) * C(SITE_NAME)"]:
    m = smf.ols(f"units ~ {f}", tr).fit(); res[f] = (round(m.rsquared, 3), round(m.rsquared_adj, 3), int(m.df_model))
print(pd.DataFrame(res, index=["R2", "adjR2", "df"]).T.to_string())
a = sm.stats.anova_lm(smf.ols("units ~ C(ARTICLE) + C(SITE_NAME)", tr).fit(), typ=2)
a["eta_sq"] = a["sum_sq"] / a["sum_sq"].sum(); print(a.round(4).to_string())
# %% [markdown]
# ## 2. Store differences (total units per store-week) and month effect
# %%
st_week = tr.groupby(["SITE_NAME", "week"]).units.sum().reset_index()
print(st_week.groupby("SITE_NAME").units.agg(["mean", "std"]).round(1).to_string())
print("Kruskal-Wallis store:", stats.kruskal(*[g.units.values for _, g in st_week.groupby("SITE_NAME")]))
tot_week = tr.groupby("week").units.sum().reset_index(); tot_week["month"] = tot_week.week.dt.month
print("Kruskal-Wallis month (total units):", stats.kruskal(*[g.units.values for _, g in tot_week.groupby("month")]))
x = np.arange(len(tot_week)); sl = stats.linregress(x, tot_week.units)
print(f"trend in total weekly units: slope {sl.slope:.2f}/wk, p={sl.pvalue:.3f}")
# %% [markdown]
# ## 3. Is there week-to-week memory after removing the article-store level?
# %%
tr["level"] = tr.groupby(["SITE_NAME", "ARTICLE"]).units.transform("mean")
tr["resid"] = tr.units - tr.level
tr["resid_l1"] = tr.groupby(["SITE_NAME", "ARTICLE"]).resid.shift(1)
ok = tr.dropna(subset=["resid_l1"])
r, pv = stats.pearsonr(ok.resid, ok.resid_l1); print(f"lag-1 autocorr of residuals: r={r:.3f} p={pv:.3f}")
r2 = stats.pearsonr(tr.units, tr.lag1)[0]; print(f"raw units vs lag1 corr: {r2:.3f}")
# %% [markdown]
# ## 4. Noise: overdispersion (variance / mean) and the achievable floor
# %%
ser = tr.groupby(["SITE_NAME", "ARTICLE"]).units.agg(["mean", "var"])
ser["disp"] = ser["var"] / ser["mean"]
print("variance/mean per series: median", round(ser.disp.median(), 2), "(1 = Poisson)")
# in-sample floor: WAPE of predicting each series its own train mean
floor = np.abs(tr.units - tr.level).sum() / tr.units.sum(); print("WAPE using true series mean (in-sample floor-ish):", round(floor, 3))
# %% [markdown]
# ## 5. Shelf life and category
# %%
art = tr.groupby("ARTICLE").agg(mean_units=("units", "mean"), shelf=("shelf_life_days", "first"), rate=("avg_rate", "first"), div=("division", "first"))
print("corr(mean units, shelf life) spearman:", stats.spearmanr(art.mean_units, art.shelf_life_days if "shelf_life_days" in art else art.shelf))
print("corr(mean units, price) spearman:", stats.spearmanr(art.mean_units, art.rate))
print(tr.groupby("division").units.agg(["mean", "std", "count"]).round(2).to_string())
print("Kruskal division:", stats.kruskal(*[g.units.values for _, g in tr.groupby("division")]))
# %%
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
order = art.sort_values("mean_units").index
ax[0].barh(order, art.loc[order, "mean_units"], color=SERIES[0]); ax[0].set_title("Average weekly units per store, by article"); ax[0].set_xlabel("units per store per week"); ax[0].tick_params(axis="y", labelsize=7)
tw = tr.groupby("week").units.sum(); ax[1].plot(tw.index, tw.values, color=SERIES[0]); ax[1].axhline(tw.mean(), color=INK["muted"], ls="--", lw=1)
ax[1].set_title("Total weekly units (train): flat, no trend"); ax[1].set_ylabel("units"); fig.autofmt_xdate()
save(fig, "05_signal")
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.scatter(ok.resid_l1, ok.resid, s=6, alpha=.25, color=SERIES[0]); ax.set_xlabel("last week's deviation from series average"); ax.set_ylabel("this week's deviation")
ax.set_title(f"Week-to-week memory: r = {r:.2f}"); save(fig, "05_autocorr")
