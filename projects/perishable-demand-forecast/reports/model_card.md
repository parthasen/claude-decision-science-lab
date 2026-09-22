# Model card — weekly demand forecast (perishable_45k)

**Model:** article mean. Forecast for article A in any store = mean weekly units of A per store over training weeks. Bands = forecast × 0.14 (P10), 0.89 (P50), 1.48 (P80), 1.82 (P90), from 3 rolling-origin CV folds.
**Purpose:** weekly replenishment planning per store and article, 1 week ahead.
**Data:** perishable_45k.csv — synthetic POS lines (generated 2026-05-22), 2024-04-01 → 2025-03-31, 5 stores × 29 articles. Sale rows only, qty>0, article known. Train weeks 2024-04-29 → 2024-12-30; test 2025-01-06 → 2025-03-24.
**Performance (test):** WAPE 0.439, bias −1.1%, MAE 4.98 units (mean 11.35). Expanding-mean baseline 0.443; difference −0.004, 95% CI [−0.008, +0.0001]. P10–P90 coverage 80.6%, ≤P80 in 79.0%.
**Not learned:** trend, seasonality, store effects, promotions, holidays, stock-outs (absent or no signal in the data).
**Limitations:** synthetic data; one year; 8% of sale lines dropped for missing article; returns excluded; demand censoring by stock-outs unknown. Dairy intervals slightly narrow (75% coverage).
**Ethical/fairness:** no personal data used; not applicable.
**Retrain/monitor:** retrain monthly; alert if weekly WAPE exceeds 0.55 for 4 weeks or bias beyond ±10%.
**Reproduce:** projects/perishable-demand-forecast/stages/04_prepare.py, 06_model.py (seed 42).
