---
name: dslc-stats
description: DSLC stage 05 — exploratory data analysis and statistical inference: descriptive statistics, visual EDA, correlation, hypothesis tests (t-test, ANOVA, chi-square, non-parametric), regression with assumption checks, effect sizes and confidence intervals, time-series decomposition, segmentation. Use when a user asks what drives an outcome, whether groups differ, if a relationship is significant, wants EDA charts or a statistical report, or when the dslc orchestrator reaches stage 05_stats.
---

# Stage 05 — Statistics and EDA

Goal: evidence-based answers to the stage-01 hypotheses, with the uncertainty stated honestly. Use training data only if a model will follow (keep the test set clean).

## Do (in `stages/05_stats.py`, or `.R` for classical stats)
1. **Descriptive**: summary tables by key segments; univariate and bivariate charts against the target (load `dataviz` skill first).
2. **Relationships**: correlation matrix (Spearman when skewed), cross-tabs with Cramér's V for categoricals, mutual information for mixed types.
3. **Hypothesis tests** — for each stage-01 hypothesis pick the test by data type and assumptions, and report *effect size + 95% CI + p-value*, never p-value alone:
   - two groups: Welch t-test / Mann-Whitney; paired: paired t / Wilcoxon
   - 3+ groups: ANOVA / Welch ANOVA / Kruskal-Wallis with post-hoc (Tukey / Dunn)
   - categorical association: chi-square / Fisher
   - Python: `pingouin`, `scipy.stats`; R: base `stats`, `car`, `rstatix`
   - Many tests → adjust (Benjamini-Hochberg) and say so.
4. **Modelled inference** when needed: OLS/logistic/Poisson (`statsmodels` formulas or R `lm/glm`), mixed models for repeated measures (`lme4`), with residual/assumption diagnostics (normality, heteroscedasticity, VIF). Report coefficients as business-readable effects ("each extra visit ≈ +3.2% conversion, CI 1.1–5.3%").
5. **Time series** (if temporal): trend/seasonality decomposition (STL), stationarity (ADF), autocorrelation.
6. Distinguish correlation from causation explicitly; list plausible confounders.

## Save
`reports/tables/hypothesis_tests.csv`, key figures in `figures/05_*.png`, `stages/05_stats_summary.md`: each hypothesis → supported / not supported / inconclusive with the evidence, plus surprising findings.

## Gate
"Which findings matter, and should we move on to modelling?" Options: proceed to modelling / dig deeper into a finding / stop here and report (descriptive project) / test new hypotheses.
