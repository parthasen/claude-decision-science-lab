# LAB

[![Validate](https://github.com/parthasen/claude-decision-science-lab/actions/workflows/validate.yml/badge.svg)](https://github.com/parthasen/claude-decision-science-lab/actions/workflows/validate.yml)
[![Latest release](https://img.shields.io/github/v/release/parthasen/claude-decision-science-lab)](https://github.com/parthasen/claude-decision-science-lab/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Not a coder / just here to get an answer from your data?** Start with [`guides/manager-guide.md`](guides/manager-guide.md) — a plain-English walkthrough, no coding knowledge needed.

- `skills/dataset-explorer/` — skill: find datasets in a folder → pick → brief → basic stats → similar public datasets → model options → build via DSLC. Install by symlinking or copying into `.claude/skills/` (or a plugin's `skills/`).
- `guides/manager-guide.md` — plain-English guide for non-coders: how to start, what happens at each step, what you get, in business terms.
- `guides/free-chat-guide.md` — for users with only free Claude.ai chat (no Claude Code): copy-paste prompts covering the same thinking manually, no plugin install needed.
- `guides/decision-science-workflow.md` — one-page map of the whole flow: find data → brief → frame → acquire → profile → prepare → stats/insight → model → explain → report/decide → further analysis, with the skill and gate for each step.
- `guides/prompt-guide.md` — prompt structure and templates for data work.
- `guides/llm-selection.md` — Claude vs ChatGPT vs Gemini decision guide.
- `guides/retail-llm-use-cases.md` — retail use cases for all three.
- `outputs/<dataset>/` — generated briefs, stats, suggestions.
- `plugins/dslc/` — copy of the DSLC plugin (8 stage skills + scripts) so LAB runs on its own.
- `projects/perishable-demand-forecast/` — the worked example (copy).
- `.claude/skills/` — links that register the skills when LAB is opened as the working folder.
- `perishableRetailStore/` — original raw data (not in git; not needed to run anything).
- `CHANGELOG.md` [![Latest release](https://img.shields.io/github/v/release/parthasen/claude-decision-science-lab)](https://github.com/parthasen/claude-decision-science-lab/releases/latest) — version history, tracks tagged releases.

Independent of the repo except for Python packages. From this folder:
`<python-with-packages> skills/dataset-explorer/scripts/discover.py <your-data-folder>`
The copy under `LAB/` can drift from `../plugins/dslc`; treat the repo version as the source of truth.

## Install as plugins (for other Claude Code users)
This repo is also a plugin marketplace (`.claude-plugin/marketplace.json`) exposing `dataset-explorer` and `dslc` as installable plugins (`plugins/dataset-explorer/`, `plugins/dslc/`). Anyone with Claude Code can run:
```
/plugin marketplace add parthasen/claude-decision-science-lab
/plugin install dataset-explorer
/plugin install dslc
```
No manual copying or symlinking needed — the plugin skills activate automatically once installed.

Maintaining this repo, or setting up your own marketplace the same way? See [`guides/distribute-as-plugins.md`](guides/distribute-as-plugins.md) for the exact steps.
