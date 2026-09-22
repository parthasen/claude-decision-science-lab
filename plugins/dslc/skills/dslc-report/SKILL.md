---
name: dslc-report
description: DSLC stage 08 — communicate and operationalise results: interactive HTML report artifact, executive slide deck, Word report, Excel workbook of tables, model card, reusable scoring script and optional scheduled refresh. Use when a user wants to present, share or export data science findings, build a dashboard or deck from an analysis, package a model for reuse, or when the dslc orchestrator reaches stage 08_report.
---

# Stage 08 — Report and deploy

Goal: the right audience gets the answer in a format they'll actually use, and the work can be rerun.

## Ask first
Which deliverables, for which audience (executives, analysts, data scientists, clients)? Offer: interactive web report (Artifact) · slide deck · Word report · Excel tables · scoring script · scheduled refresh. Recommend a default: web report + 5-slide exec deck.

## Build from the stage summaries — don't re-run analysis
Read all `stages/*_summary.md`, `DECISIONS.md`, `SOURCES.md`, key figures and tables.

Narrative structure (all formats):
1. The question and the decision it supports
2. The answer in one sentence, with the headline number and its uncertainty
3. 3–5 key findings, each with one chart
4. Model performance vs. baseline (if modelled) and top drivers
5. Limitations, risks, fairness notes
6. Recommendations and next steps
7. Appendix: data sources, methods, reproducibility (notebook list, environment)

## Deliverables → skills
- **Interactive web report / dashboard**: load `artifact-design` (and `dataviz`) then publish with the Artifact tool; embed charts as data (interactive) rather than screenshots where practical. Private by default — the user decides whom to share with.
- **Slides**: `pptx` skill. **Word report**: `docx` skill. **Excel tables**: `xlsx` skill. **PDF**: `pdf` skill.
- **Scoring script** `models/score.py`: loads `final_model.joblib`, validates input columns (pandera schema from stage 03 if present), writes predictions.
- **Scheduled refresh**: `schedule` skill to rerun `run_notebook.py` over stages 03–07 on new data and alert on metric drift.
- **Colab/Drive sharing**: upload notebooks and report to Google Drive via the Drive connector when the user asks.

## Save
Everything under `reports/`; update `project.yaml` and `stages/08_report_summary.md` with links/paths to each deliverable.

## Gate
"Anything to change before we call this done?" Options: done / revise report / add deliverable / start a follow-up analysis.
