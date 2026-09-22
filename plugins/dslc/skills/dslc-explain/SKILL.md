---
name: dslc-explain
description: DSLC stage 07 — model explainability and validation: SHAP global and local explanations, permutation importance, partial dependence, error analysis by segment, calibration, robustness and fairness checks (fairlearn) across sensitive groups, and a model card. Use when a user asks why a model predicts something, which factors drive predictions, whether a model is fair or trustworthy, or when the dslc orchestrator reaches stage 07_explain.
---

# Stage 07 — Explain and validate

Goal: stakeholders can trust (or knowingly distrust) the model — they know what drives it, where it fails, and who it may treat unfairly.

## Do (in `stages/07_explain.py`)
1. **Global drivers**: SHAP summary (TreeExplainer for tree models, LinearExplainer/KernelExplainer otherwise; sample ≤ 2,000 rows) and permutation importance on the test set. Translate the top 5–10 drivers into business language and compare with stage-05 findings — agreement builds trust, disagreement needs explanation.
2. **Shape of effects**: partial dependence / SHAP dependence plots for the top 3 drivers.
3. **Local explanations**: 3 illustrative cases (a correct confident prediction, a wrong one, a borderline one) with SHAP waterfall plots.
4. **Error analysis**: performance by segment (region, product, time period, size); where is it much worse?
5. **Fairness** (if people are affected and sensitive or proxy attributes exist, ask which apply): `fairlearn.metrics.MetricFrame` for selection rate, TPR/FPR by group; flag disparities > 20% relative and discuss mitigation (threshold per group, reweighting, feature removal) with the user.
6. **Robustness**: sensitivity to missing key features, performance over time if temporal (drift risk).
7. **Model card** `reports/model_card.md`: intended use, not-intended use, data, metrics, drivers, fairness results, limitations, retraining trigger.

## Save
`figures/07_*.png`, `reports/tables/segment_performance.csv`, `reports/model_card.md`, `stages/07_explain_summary.md`.

## Gate
"Are the drivers, error patterns and fairness results acceptable?" Options: accept / mitigate a fairness issue / go back to modelling / add caveats and proceed.
