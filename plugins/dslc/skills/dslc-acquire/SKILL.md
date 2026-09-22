---
name: dslc-acquire
description: DSLC stage 02 — gather and enrich data: load the user's files, research the domain on the web, and find complementary datasets from Kaggle, Hugging Face, Google Drive, BigQuery public data and open-data APIs (World Bank, FRED, UCI, data.gov), with provenance and licence tracking. Use when a data science project needs more data, context, benchmarks or domain research, or when the dslc orchestrator reaches stage 02_acquire.
---

# Stage 02 — Acquire and enrich

Goal: the minimum extra data and domain knowledge that materially improves the answer — every source traceable and licence-checked.

## Inputs
`stages/01_frame_summary.md` (data gaps, hypotheses), `project.yaml → data_policy`.

## Do
1. **Inventory user data** in `data/raw/`: files, rows, date range, keys that could join to external data (country, date, zip, product code).
2. **Domain research** (WebSearch/WebFetch): typical drivers of the target, known benchmarks, definitions, pitfalls. Cite URLs. Never include confidential values in search queries.
3. **Find candidate datasets** — search in this order and shortlist 3–6:
   - Kaggle: `kaggle datasets list -s "<terms>" --sort-by votes` then `kaggle datasets files <ref>`; download with `kaggle datasets download <ref> -p data/external/<name> --unzip`. Needs the user's token (`~/.kaggle/kaggle.json`); if missing, say so and continue with other sources.
   - Hugging Face: the Hugging Face connector's dataset search if connected, else `huggingface_hub` / `datasets.load_dataset`.
   - Google Drive connector: user's own shared files.
   - BigQuery connector: public datasets (`bigquery-public-data`) when connected — estimate query cost first.
   - Open APIs: World Bank (`api.worldbank.org/v2`), FRED (needs `FRED_API_KEY`), UCI, data.gov, OECD, national statistics offices.
4. Present the shortlist as a table: source, what it adds, join key, size, licence, freshness, risk. **Downloading needs the user's approval** — ask which to fetch.
5. Download approved data to `data/external/`, validate the join (match rate) in `stages/02_acquire.py`, and write the merged or linked dataset to `data/interim/`.

## Save
- Append every source to `SOURCES.md` (origin URL, licence/terms, retrieval date, approver).
- `stages/02_acquire_summary.md`: sources used/rejected and why, join coverage, research findings with citations.

## Gate
"Which external datasets and research should we use?" Options: use shortlisted / only my data / search more / add a source I know.
