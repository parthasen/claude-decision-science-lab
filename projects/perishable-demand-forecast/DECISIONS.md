# Decision log

| Date | Stage | Decision | Rationale | Approved by |
|---|---|---|---|---|
| 2026-09-20 | 02_acquire | Skipped | User chose to skip external datasets after seeing shortlist (LAB/outputs/perishable_45k/similar_datasets.md) | user |
| 2026-09-20 | 01_frame | Approved: weekly units per SITE_NAME x ARTICLE, WAPE, split Apr-Dec/Jan-Mar, beat 4-wk mean (0.548) by >=10% | Objective chosen from model_options.md; seasonal-naive replaced (1 year of data) | user |
| 2026-09-20 | 03_profile | Approved fixes: drop last partial week, qty-0 sales, missing-ARTICLE rows; use SITE_NAME; exclude _quality_tier/_generated_at; test = weeks from 2025-01-06 to 2025-03-24 | Profile summary issues 1-5 | user |
| 2026-09-20 | 04_prepare | Approved cleaning, features, split (train to 2024-12-30, test 2025-01-06..03-24), success = WAPE <= 0.40 vs best baseline 0.443 (expanding mean) | Stage 04 summary | user |
| 2026-09-20 | 05_stats | Approved; revised success: match best baseline (~0.44 WAPE) unbiased with P50/P80 intervals; simplest model wins ties | Noise floor ~0.44-0.47 (stage 05) | user |
| 2026-09-20 | 06_model | Approved: article mean (train), pooled over stores; ratio quantiles for P10/P80/P90; pooled across stores (same forecast per article in every store) | Test WAPE 0.439 vs 0.443 expanding mean (n.s.); LightGBM no gain | user |
| 2026-09-20 | 07_explain | Accepted; known weak spots: low-volume articles, dairy interval coverage 75% | Stage 07 summary | user |
| 2026-09-20 | 08_report | Approved: HTML report + scoring script; not published externally | User chose deliverables | user |
