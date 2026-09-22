# Stage 01 — Frame

## Question
How many units of each fresh article will each store sell per week?

## Decision
Weekly replenishment quantities per store and article.

## Problem type
Forecasting (regression on a time series panel).

## Target & unit
`weekly_units` = sum of BILL_QUANTITY on Sale rows with quantity > 0, per SITE_NAME × ARTICLE × week (Mon–Sun). 145 series, 53 weeks; median series has sales in 50 of 53 weeks (min 26), so weekly is dense enough; daily is not.

## Metric & baselines
Primary: WAPE. Split: train Apr–Dec 2024 (5,363 series-weeks), test Jan–Mar 2025 (1,704).
Baselines on test (missing weeks = 0): last-week WAPE 0.674; trailing-4-week mean WAPE 0.548. Mean is only 10.6 units per series-week, so counts are small and noisy.
Seasonal-naive (same week last year) is impossible: only one year of data. Replaced by the 4-week mean.
Success threshold proposed: beat 0.548 WAPE with a clear margin (e.g. ≥ 10% lower) and not be biased.

## Hypotheses
1. Store and article identity explain most variance.
2. Day-of-week/month patterns exist (weekly aggregation removes the first).
3. Lagged units improve on plain averages.
4. Shelf life or category changes the level of demand.
Data is synthetic, so real seasonality may be absent.

## Data gaps
No promo, price change, stock, waste or holiday data. Stock-outs cannot be separated from zero demand. (Stage 02 skipped by user.)

## Risks
- SITE has junk codes (TBD, UNKNOWN, STORE_X, LOC99, BRANCH-01, missing); SITE_NAME is clean and used as the store.
- 2,773 of 33,540 Sale rows have quantity 0 (dropped); BILL_TYPE and amount signs conflict; 25% Returns. Returns are excluded from demand — this ignores refunds.
- One year only: no annual seasonality, and a 13-week test.
- Synthetic data: results test the pipeline, not real demand.
