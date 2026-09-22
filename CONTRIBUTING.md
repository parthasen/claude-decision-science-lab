# Contributing

This repo is a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`) with two plugins:

- `plugins/dataset-explorer/` — dataset discovery, briefing, and model proposal
- `plugins/dslc/` — the 8-stage data science lifecycle (frame → acquire → profile → prepare → stats → model → explain → report)

Each plugin's skills live under `plugins/<plugin>/skills/<skill>/SKILL.md`, following the standard Claude Code skill format (YAML frontmatter + instructions body, optional `scripts/` and `references/`).

## Before you start

Open an issue first for anything beyond a small fix — a new skill, a new stage, or a change to an existing skill's behavior — so we can agree on scope before you write it.

## Making a change

1. Fork and clone the repo.
2. Edit the relevant `SKILL.md` and/or its `scripts/`. Keep instructions imperative and gated (present findings, ask before proceeding) — see any existing `SKILL.md` for the tone.
3. If you touch `skills/dataset-explorer/` (the standalone copy outside `plugins/`), mirror the same change into `plugins/dataset-explorer/skills/dataset-explorer/`, and vice versa. They're kept in sync manually, not symlinked, for distribution robustness.
4. Test locally: point Claude Code at your local checkout as a marketplace source —
   ```
   /plugin marketplace add /path/to/your/clone
   /plugin install dataset-explorer   # or dslc
   ```
   then run the relevant skill against a real dataset and confirm the gates (findings + options, waiting for your pick) still behave as documented.
5. If you add or edit a `.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json`, make sure it's valid JSON (`python -m json.tool <file>`).
6. If you add a Python script, make sure it compiles (`python -m py_compile <file>`) and has no hard dependency on packages beyond what's listed in the relevant `SKILL.md`.

## CI

Every push and PR runs [`.github/workflows/validate.yml`](.github/workflows/validate.yml): it validates all plugin/marketplace JSON and compile-checks every `.py` file. A PR won't merge with a red check.

## Pull requests

- Keep PRs scoped to one skill or one clear change — easier to review, easier to revert.
- Describe what you tested and how (which dataset, which skill, what you saw at each gate).
- Don't commit real or sensitive data. `outputs/`, `**/data/interim/`, and project `data/`/`models/` folders are gitignored on purpose — leave generated artifacts out of PRs.

## License

By contributing, you agree your contribution is licensed under the repo's [MIT license](LICENSE).
