---
name: dslc-prepare
description: DSLC stage 04 — data cleaning, feature engineering and train/validation/test split as a leakage-safe, reusable pipeline (scikit-learn Pipeline/ColumnTransformer or R recipes). Use when data needs cleaning, imputation, encoding, feature creation or splitting before modelling, or when the dslc orchestrator reaches stage 04_prepare.
---

# Stage 04 — Prepare data and features

Goal: a clean analysis table plus a fitted-on-train-only transformation pipeline that can be applied to new data.

## Do (in `stages/04_prepare.py` or `.R`)
1. Apply the cleaning rules approved in stage 03 (dedupe, fix types, harmonise categories, cap/remove impossible values). Deterministic rules go here; statistical ones (imputation, scaling) go inside the pipeline.
2. **Split first, then fit transforms.** Choose the split to mirror real use:
   - Random stratified 70/15/15 for i.i.d. data (seed from `project.yaml`).
   - Time-based split for anything temporal (train on past, test on future).
   - Group split when rows share an entity (customer, patient) to avoid identity leakage.
   Save split indices so every later stage uses the same test set; the test set stays untouched until final evaluation.
3. Feature engineering, explained to the user in business terms: date parts/lags/rolling stats, ratios, counts per entity, text length/TF-IDF, domain features suggested by stage 02 research. Drop leakage columns confirmed in stage 03.
4. Build a `Pipeline`/`ColumnTransformer` (imputation, one-hot or target encoding for high cardinality, scaling where the model needs it); `feature_engine` for rare-label grouping, outlier capping. In R use `recipes`.
5. Save `data/processed/{train,valid,test}.parquet`, `models/preprocessor.joblib` (or `.rds`), and a feature list with descriptions.

## Save
`stages/04_prepare_summary.md`: rules applied (with row counts before/after), split strategy and sizes, feature list, anything dropped and why.

## Gate
"Approve the cleaning rules, features and the train/test split?" Options: approve / change split strategy / add or remove features / revisit cleaning.
