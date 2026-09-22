# Stage 04 — Prepare summary

## Cleaning (as approved)
45,000 rows → 28,816 Sale lines kept (dropped: all Returns, qty-0 sales, missing ARTICLE, the one-day final week 2025-03-31). Store = SITE_NAME. Dropped columns: _quality_tier, _generated_at, SITE, TAXABLEAMT, IGST*, RETURN_AMOUNT, all amounts/tax (derived from the target).

## Panel
145 store × article series × 52 complete weeks (2024-04-01 → 2025-03-24) = 7,540 series-weeks; weeks with no sales filled with 0. After needing 4 weeks of history: 6,960 modelling rows.
File: `data/processed/weekly_panel.parquet` (+ `article_dim.csv`).

## Features (forecast horizon = 1 week; every feature uses weeks before t)
lag1–lag4, roll4/roll8 mean, roll4 std, expanding mean, store total last week, ISO week, month, and static article facts (division, shelf-life days, storage condition, median rate). Categorical: store, article.

## Split (time-ordered, no shuffling)
- Train: weeks 2024-04-29 → 2024-12-30 (5,220 rows).
- Test: weeks 2025-01-06 → 2025-03-24 (1,740 rows, 12 weeks), touched only once, in stage 06.
- Tuning inside train uses rolling-origin (expanding window) CV, not random folds.
- Checked: lags/rolling means rebuilt independently on 500 sampled rows match; train ends before test starts.

## Corrected baselines on test (WAPE, lower is better)
| baseline | WAPE |
|---|---|
| last week | 0.617 |
| 4-week mean | 0.488 |
| 8-week mean | 0.460 |
| **expanding mean (best)** | **0.443** |

The stage-01 numbers (0.674 / 0.548) were inflated by the partial last week; the best baseline is now the expanding mean.
**Proposed success threshold: WAPE ≤ 0.40 (≥ 10% better than 0.443)**, with no systematic bias.

## Watch-outs
- Test mean is 11.35 units per series-week, so counts are small; much of the error is random. The data is flat with no trend/seasonality, so expect models to gain little over averages. If they don't beat 0.443, that is the honest result.
- Article and store levels are learned from ~8 months only.
