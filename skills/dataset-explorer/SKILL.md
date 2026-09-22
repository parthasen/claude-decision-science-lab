---
name: dataset-explorer
description: Discover, understand and model datasets in a local folder. Lists the datasets found, lets the user pick one, writes a plain-language brief with basic statistics, searches Kaggle / Hugging Face / UCI / open-data portals for similar datasets, proposes which models fit and what user objective each serves, then builds the chosen model through the DSLC lifecycle. Use when the user says "what data do I have", "show datasets in this folder", "pick a dataset", "describe this data", "find similar datasets", "what models can I build", or wants a guided start on a folder of CSV/Excel/Parquet files — especially retail or POS data.
---

# Dataset Explorer

A guided, gated walk from "a folder of files" to "a trained model". Do one step, show the result, and wait for the user before the next. Save everything under `outputs/<dataset-stem>/`.

**Working directory: the LAB folder.** All paths below are relative to it. LAB is self-contained: it carries its own copy of the DSLC plugin (`plugins/dslc/`) and its own `projects/` and `outputs/`.
Python for all scripts (`PY`): any Python with pandas, numpy, pyarrow, openpyxl, scikit-learn, statsmodels, lightgbm, matplotlib, nbclient, ipykernel, pyyaml. Inside the DSLC repo use `../envs/dslc/bin/python` (do not use conda; it is broken on this machine).
Script dir: `skills/dataset-explorer/scripts/`.

## Step 1 — Find and show datasets
Run `discover.py <folder>` (default folder: `.`; skip `perishableRetailStore`-style raw folders only if the user says so). Show the numbered table as-is.
Ask which to use with AskUserQuestion — offer the 3–4 most plausible (largest, most recent, non-derived) plus "Other". Files named `sim_*`, `*_quality*`, `output_*` are usually generated derivatives: say so, and prefer the raw original.

## Step 2 — Brief + basic statistics
Run `brief.py <file> [--objective "..."]`. It writes `brief.md`, `stats.json`, `suggestions.json`.
The output is heuristic (column-name based). Read it, correct anything wrong (e.g. a tax column mistaken for revenue, an ID read as numeric), and present:
1. One-paragraph description: what the data is, grain, period, size.
2. Quality flags: missingness, duplicates, constant columns, negatives/returns, extreme skew.
3. The stats tables. Do not invent numbers not in the output; if you need more (e.g. monthly trend), compute it and say so.
Excel with several sheets: ask which sheet, pass `--sheet`.

## Step 3 — Similar datasets (Kaggle, public, web)
Use the queries in `suggestions.json` and shortlist 4–6. Order of sources:
1. Kaggle CLI: `kaggle datasets list -s "<terms>" --sort-by votes` (needs `~/.kaggle/kaggle.json`; if absent say so and continue).
2. WebSearch for Kaggle / Hugging Face / UCI / data.gov / Google Dataset Search.
3. Connectors if enabled (see `references/connectors-and-skills.md`): Hugging Face, BigQuery public data, Google Drive.
Never put confidential values from the user's data into a search query — use column names and domain words only.
Present a table: name, source URL, rows/size, what it adds, licence, how it relates (same schema / complementary / benchmark). **Only list; download nothing without approval.** Hand approved downloads to the `dslc-acquire` skill so provenance goes in `SOURCES.md`.
Save the table to `outputs/<stem>/similar_datasets.md`.

## Step 4 — Models and user objectives
Start from `suggestions.json → candidate_models`, then adapt using `references/model-catalog.md` (retail objectives, target definitions, metrics, data requirements, pitfalls). Present a table: user objective → model type → target → metric → data readiness (ready / needs derivation / missing data). Recommend one, with the reason. Ask the user to choose, or state their own objective. Save `outputs/<stem>/model_options.md`.

## Step 5 — Build the model via the data science life cycle
Hand off to the `dslc` skill; do not rebuild its pipeline.
1. `PY plugins/dslc/skills/dslc/scripts/new_project.py "<name>" --root projects`
2. Copy (never move) the chosen file into `projects/<slug>/data/raw/`.
3. Run stages 01 frame → 08 report through the dslc stage skills (`dslc-frame`, `dslc-acquire`, `dslc-profile`, `dslc-prepare`, `dslc-stats`, `dslc-model`, `dslc-explain`, `dslc-report`), with the objective and target confirmed in Step 4 pre-filled into stage 01. Respect each stage's approval gate.
4. Copy the final report and model card into `outputs/<stem>/` and link the project folder.
Retail guard rails: split by time, never randomly, for forecasting/churn; group by customer or bill to avoid leakage; treat returns (negative quantity/amount) explicitly; report against a naive baseline.

## Related guides (in `guides/`)
`prompt-guide.md`, `llm-selection.md`, `retail-llm-use-cases.md`. Offer them when the user asks how to prompt, or which assistant to use.

## Do not
- Modify or delete the user's source files.
- Send data rows to external services or search engines.
- Claim a model is good without a held-out, time-ordered test and a baseline comparison.
