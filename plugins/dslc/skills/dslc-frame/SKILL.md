---
name: dslc-frame
description: DSLC stage 01 — turn a user's business context and data sample into a precise analytics problem statement (question, decision supported, problem type, target, unit of analysis, success metric, hypotheses, risks). Use when starting a data science project, when a user describes a business question to analyse, or when the dslc orchestrator reaches stage 01_frame.
---

# Stage 01 — Frame the problem

Most failed data science projects answer the wrong question well. This stage makes the question concrete enough that later stages can be judged against it.

## Inputs
- User's description of the business question, domain and decision it supports.
- A first look at the data: load a sample from `data/raw/` (shape, columns, 10 sample rows, dtypes) in `stages/01_frame.py` and run it (see orchestrator runtimes; scripts are in `../dslc/scripts/`).

## Do
1. Restate the question in one sentence and name the decision or action it informs. If vague ("analyse sales"), propose 2–3 sharper framings and ask.
2. Classify the problem type: descriptive / inferential (does X affect Y?) / classification / regression / forecasting / clustering / anomaly detection. Explain the choice in one line.
3. Identify the target column (or propose how to construct it), the unit of analysis (one row = ?), and the time dimension if any.
4. Pick a primary metric tied to business cost (e.g. recall for fraud, MAPE for demand, effect size + CI for inference) and a success threshold or a naive baseline to beat.
5. Write 3–6 testable hypotheses, and note data you'd want but don't have (feeds stage 02).
6. Flag risks early: target leakage candidates, tiny sample, class imbalance, sensitive attributes (fairness), confidentiality.
7. Optionally use `product-management:write-spec` style structure if the user wants a formal brief.

## Save
- `project.yaml` fields via `python ../dslc/scripts/stage.py <project> --set problem.target <col>` etc. (context.*, problem.*).
- `stages/01_frame_summary.md` with sections: Question, Decision, Problem type, Target & unit, Metric & baseline, Hypotheses, Data gaps, Risks.

## Gate
Ask: "Is this the right problem, target and success metric?" Options: approve / change target or metric / reframe question / add context.
