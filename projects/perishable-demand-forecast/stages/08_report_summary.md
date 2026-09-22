# Stage 08 — Deliverables

Chosen by user: interactive HTML report, scoring script. (Not requested: slides/Word, Excel, scheduled refresh.)

| Deliverable | Path |
|---|---|
| Interactive report (self-contained, works offline; forecast lookup + sortable error table) | projects/perishable-demand-forecast/reports/report.html (copy: LAB/outputs/perishable_45k/perishable_demand_forecast_report.html) |
| Scoring script | projects/perishable-demand-forecast/models/score.py (needs models/article_means.csv + final_metrics.json beside it) |
| Model card | reports/model_card.md (copy in LAB/outputs/perishable_45k/) |
| Notebooks | notebooks/01_frame … 07_explain.ipynb; stages/*.py sources; 08_report.py builds the report |
| Decisions / sources | DECISIONS.md, SOURCES.md |

Verified: report opens, lookup values match score.py (Kiwi 3.7 / 0.5 / 3.3 / 5.5 / 6.7); score.py rejects unknown articles and accepts a custom store × article list.
Not published: the report was NOT uploaded anywhere; it is a local file. Publishing as a private claude.ai Artifact is available on request.
Correction made along the way: pickled model could not be loaded outside the notebook; replaced by plain-file model (article_means.csv).
