# Stage 06 — Modelling summary

## Setup
Target: weekly units per store × article, 1 week ahead. Rolling-origin CV inside train (cuts 2024-10-07, 11-04, 12-02; 4 validation weeks each). Rule: pick lowest CV WAPE, but prefer the simplest model within 1%. Test (12 weeks, 1,740 series-weeks) scored once.

## CV results (WAPE, lower = better; ±SD across folds ≈ 0.01)
| model | CV WAPE | bias |
|---|---|---|
| LightGBM L1 (4 leaves) | 0.468 | −4.2% |
| LightGBM Poisson (8 / 4 leaves) | 0.470 / 0.471 | +2.2% / +2.8% |
| **Article mean (train)** = Poisson GLM on article | **0.471** | +3.3% |
| Poisson GLM article + store / + lags | 0.472 / 0.472 | +3.3% |
| Baseline expanding mean | 0.475 | +3.1% |
| Baseline 8-week mean | 0.499 | +1.8% |
| Baseline last week | 0.653 | +0.8% |
All models except the last two are within one fold-SD of each other: **no meaningful difference**.

## Chosen: article mean (each article's average weekly units per store, pooled over all 5 stores, from training weeks; every store gets the same forecast for an article)
Simplest model within 1% of the best. LightGBM would be 0.7% better in CV, which is inside the noise.

## Test result (used once)
| | WAPE | bias |
|---|---|---|
| **Chosen: article mean** | **0.439** | −1.1% |
| Expanding mean | 0.443 | — |
| 8-week mean | 0.460 | — |
| Last week | 0.617 | — |
MAE 4.98 units per series-week (mean demand 11.35). Paired bootstrap over series: chosen − expanding mean = −0.004 WAPE, 95% CI [−0.008, +0.0001], i.e. **not distinguishable from the baseline**.
By division: Vegetables 0.41, Fruits 0.44, Dairy 0.50.

## Against the criteria agreed at stage 05
- Match best baseline (~0.44), unbiased: **met** (0.439, bias −1.1%).
- Prediction intervals: **met**. P10–P90 covers 80.6% of test weeks (nominal 80%); demand ≤ P80 in 79.0% (nominal 80%). Intervals are the point forecast × 0.14 to 1.82 (P10–P90), calibrated on CV folds; they are wide.
- Original stretch goal WAPE ≤ 0.40: **not met**, and not expected to be achievable on this data.

## Honest conclusion
There is no forecastable signal beyond each article's typical level. A learned model adds nothing, which fits the synthetic generator. Use the article mean plus the P50/P80 ratios for replenishment on this data. On real data, re-run the same pipeline: it would pick up trend, seasonality, promotions and store effects if they exist.

Artifacts: models/article_means.csv, models/final_metrics.json, reports/tables/06_cv_results.csv, reports/tables/06_test_predictions.csv, figures/06_cv.png, figures/06_test_total.png.
