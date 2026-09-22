# Decision science workflow: data → brief → analysis → decision

One page. Every step is a skill that already exists in this LAB (`.claude/skills/`, source in `skills/` and `plugins/dslc/skills/`). Nothing here needs to be built — just invoked, in order, one gate at a time.

## The flow

| # | Stage | Question it answers | Skill | Saves to | You decide (gate) |
|---|---|---|---|---|---|
| 0 | **Find data** | What data do I actually have? | `dataset-explorer` step 1 | numbered file list | which file to use |
| 0b | **Brief** | What is it, grain, period, size, quality? | `dataset-explorer` step 2 (`brief.py`) | `outputs/<stem>/brief.md`, `stats.json` | corrections, which objective |
| 1 | **Frame** | What's the question, and what decision does it inform? | `dslc-frame` | `stages/01_frame_summary.md`, `project.yaml` | target, metric, problem type |
| 2 | **Acquire** | What extra data/context would materially help? | `dslc-acquire` | `SOURCES.md`, `02_acquire_summary.md` | which external sources |
| 3 | **Profile** | What's really in the data, what's wrong with it? | `dslc-profile` | data dictionary, `03_profile_summary.md` | accept fixes / get better data |
| 4 | **Prepare** | Clean, features, leakage-safe split | `dslc-prepare` | `data/processed/*`, preprocessor | split strategy, feature list |
| 5 | **Stats → insight** | What does the data say, and is it real (not noise)? | `dslc-stats` | `hypothesis_tests.csv`, `05_stats_summary.md` | proceed to model / stop here / dig deeper |
| 6 | **Model** | Can we predict/classify/forecast it, beating a naive baseline? | `dslc-model` | `final_model.joblib`, comparison table | which model to keep |
| 7 | **Explain → trust** | Why does it predict that, where does it fail, is it fair? | `dslc-explain` | `model_card.md`, SHAP figures | accept / mitigate / revisit model |
| 8 | **Report → decide** | What do we tell people, what do we do about it? | `dslc-report` | web report, deck, doc, xlsx, scoring script | which deliverables, for whom |
| ↻ | **Further analysis** | What's still unanswered? | new pass through `dslc-frame` (new question) or `dslc-stats` ("dig deeper") | new `stages/` entries | new hypothesis or new project |

`dataset-explorer` is the front door — it covers 0/0b, proposes a model (step 4 of its own numbering), then hands off to `dslc`, which runs stages 1–8. You never call the `dslc-*` stage skills out of order; the `dslc` orchestrator sequences them and stops for approval after each one.

## Why it's gated, not automatic
At every row above, the assistant presents findings + 2–4 concrete options and waits — it does not decide for you. That's the whole decision-science discipline: recommend, don't bury the decision in prose. Decisions taken at each gate belong in `DECISIONS.md` inside the project folder.

## Start or resume a project
- New: describe the business question + point at a data file → `dataset-explorer` step 1, or go straight to `dslc` if you already know the file and question.
- Resume: `dslc` checks `projects/` and asks whether to continue an existing one (e.g. `projects/perishable-demand-forecast`, already run end to end — a worked example of every stage above) or start new.

## Confirmed installed
`dataset-explorer`, `dslc`, `dslc-frame`, `dslc-acquire`, `dslc-profile`, `dslc-prepare`, `dslc-stats`, `dslc-model`, `dslc-explain`, `dslc-report` — all present under `.claude/skills/` (and their source under `skills/` / `plugins/dslc/skills/`). Nothing to build; say what data or question you want to start with.
