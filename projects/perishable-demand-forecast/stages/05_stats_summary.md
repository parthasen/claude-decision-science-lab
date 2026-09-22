# Stage 05 — Statistics summary (train weeks only)

## Findings
1. **Article is the only strong driver.** Article alone explains 53.6% of weekly-unit variance (ANOVA F=214, p<0.001, η²=0.54). Adding store adds nothing (η²=0.0005, p=0.24); store × article interaction adds ~1 point of R² for 116 extra parameters (adj. R² unchanged at 0.534).
2. **No store effect.** Store weekly totals 314–332 units; Kruskal-Wallis p=0.81.
3. **No seasonality or trend.** Month effect p=0.33 (R²=0.002); trend −2.4 units/week, p=0.18 on a mean of ~1,600. Total weekly units are flat.
4. **No week-to-week memory after removing the series average.** Residual lag-1 autocorrelation r=−0.04 (p=0.005 only because n=5,000; effect negligible). The raw lag-1 correlation of 0.53 just reflects the article level.
5. **Category matters mostly through article:** mean weekly units Vegetables 14.0, Fruits 10.3, Dairy 9.0 (Kruskal p<0.001). Shelf life shows no link with volume (ρ=−0.06, p=0.77). Higher-priced articles sell fewer units (ρ=−0.36, p=0.055, borderline, 29 articles).
6. **Counts are noisy.** Variance/mean is 3.8 per series (Poisson would be 1). Using each series' own train mean gives WAPE 0.441 in-sample; median 0.434.

## Exploratory holdout inside train (fit on Apr–Oct, score Nov–Dec)
| predictor | WAPE |
|---|---|
| store×article mean | 0.480 |
| store×article median | 0.481 |
| article-only mean | 0.476 |
| article-only median | 0.471 |
Article-only matches or beats store×article, and mean vs median makes no difference.

## What this means for the goal
The data behaves like independent random draws around an article-level mean. **The noise floor is about WAPE 0.44–0.47.** The stage-04 baseline (expanding mean, 0.443 on test) is already near it, so the ≤0.40 target (10% better) is very likely unreachable, and a complex model should not be expected to beat it. Any model that appears to must be checked for leakage.
This is consistent with the data being synthetic. It says nothing about real store demand.

## Recommendation
- Revise the success criterion for stage 06 to: **match the best baseline (≈0.44) within noise, be unbiased, and produce sensible prediction intervals**, and pick the simplest model that achieves it. (Original ≤0.40 would be kept as a stretch.)
- Model candidates: expanding-mean and article-mean baselines, Poisson/negative-binomial GLM (article + store), LightGBM with lags; compare by rolling-origin CV in train, test used once.
- Add prediction intervals or quantiles (P50/P80), which are more useful for replenishment than a point forecast.

Figures: figures/05_signal.png, figures/05_autocorr.png.
