---
name: dslc-profile
description: DSLC stage 03 — data profiling and quality assessment: schema and types, missingness, duplicates, outliers, distributions, cardinality, target balance, leakage suspects, time drift and a data dictionary. Use when a user wants to understand or check the quality of a dataset before analysis or modelling, or when the dslc orchestrator reaches stage 03_profile.
---

# Stage 03 — Profile and assess quality

Goal: know exactly what is in the data and what could mislead later stages.

## Do (in `stages/03_profile.py`, or `.R`)
1. Load `data/interim/` (or `data/raw/`). Record rows, columns, memory, date span.
2. Build a **data dictionary** table: column, inferred type (numeric/categorical/datetime/text/id), semantic meaning (ask the user when unclear), % missing, # unique, example values.
3. Quality checks:
   - Missingness pattern (overall and vs. target) — is it random or informative?
   - Exact and key-based duplicates.
   - Outliers (IQR / robust z) and impossible values (negative ages, future dates).
   - Inconsistent categories (case, spelling), mixed units.
   - Target distribution / class balance.
   - **Leakage suspects**: columns created after the outcome, near-perfect correlation with target, IDs encoding the target.
   - Drift over time for key columns if there's a time dimension.
4. Generate a full HTML profile with `ydata_profiling.ProfileReport(df, minimal=len(df) > 100_000)` to `reports/03_profile.html` for power users; in R, `skimr::skim` and `DataExplorer`.
5. Figures (load `dataviz` skill first): missingness overview, target distribution, top distributions.
6. Optional: encode checks as a `pandera` schema in `data/processed/schema.py` for future data refreshes.

## Save
`reports/tables/data_dictionary.csv`, `stages/03_profile_summary.md` with: dataset overview, top quality issues ranked by impact, proposed fix for each, leakage suspects, questions for the user.

## Gate
"Are these data-quality issues and proposed fixes acceptable?" Options: accept fixes / discuss specific columns / get more/cleaner data / proceed as-is with caveats.
