---
name: dslc-model
description: DSLC stage 06 — machine-learning modelling: baselines, candidate models (linear, tree ensembles, XGBoost, LightGBM, time-series, clustering), cross-validation, hyperparameter tuning with Optuna, model comparison and final held-out test evaluation. Use when a user wants to predict, classify, forecast or segment with ML, compare models, or when the dslc orchestrator reaches stage 06_model.
---

# Stage 06 — Model

Goal: the simplest model that meets the success metric, with an honest estimate of real-world performance.

## Do (in `stages/06_model.py`; `.R` with tidymodels if requested)
1. Load processed splits and `models/preprocessor.joblib` from stage 04. Seed everything from `project.yaml`.
2. **Baseline first** (majority class / mean / seasonal naive / last value). Every model is judged against it.
3. **Candidates** by problem type (keep it to 3–5):
   - classification/regression: regularised linear/logistic, random forest, LightGBM or XGBoost; `FLAML`/`PyCaret`-style AutoML only if installed and the user wants breadth.
   - forecasting: seasonal naive, ETS/ARIMA (`statsmodels`; R `forecast` only if installed — it needs R ≥ 4.3 on this machine), gradient boosting with lag features.
   - clustering: k-means / Gaussian mixture / HDBSCAN with silhouette and business interpretation of segments.
4. **Validation**: stratified/grouped/time-series CV on train (matching the stage-04 split logic). Report mean ± std of the primary metric plus 1–2 secondary metrics.
5. **Tuning**: Optuna (30–100 trials, early stopping) on the top 1–2 candidates only. Long runs → run in background and tell the user the expected time. Use the `colab` runtime if the user wants a GPU.
6. **Imbalance / costs**: class weights or threshold tuning on validation data against the business cost; don't resample the test set.
7. **Final evaluation once** on the held-out test set. Classification: confusion matrix, ROC/PR curves, calibration. Regression: residual plots, error by segment. Forecast: backtest plot with intervals.

## Save
`models/final_model.joblib` (full pipeline incl. preprocessing), `reports/tables/model_comparison.csv`, `figures/06_*.png`, `stages/06_model_summary.md`: comparison table, chosen model and why (accuracy vs. interpretability vs. latency), test performance vs. baseline and success threshold, known limitations.

## Gate
"Which model should we keep?" Options: best-performing / simpler interpretable one / tune further / revisit features.
