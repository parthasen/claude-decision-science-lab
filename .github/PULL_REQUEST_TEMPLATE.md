## What changed

<!-- Which skill/plugin, and what behavior changed. Keep it scoped to one skill or one clear change. -->

## Why

<!-- The problem this fixes, or the capability it adds. -->

## How I tested it

<!-- Which dataset and skill you ran it against, and what you saw at each gate (findings + options presented, waited for a pick). -->

## Checklist

[![Latest release](https://img.shields.io/github/v/release/parthasen/claude-decision-science-lab)](https://github.com/parthasen/claude-decision-science-lab/releases/latest)

- [ ] If I edited `skills/dataset-explorer/`, I mirrored the change into `plugins/dataset-explorer/skills/dataset-explorer/` (or vice versa) — see [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Any `.claude-plugin/*.json` I touched is valid JSON
- [ ] Any `.py` file I added/edited compiles (`python -m py_compile <file>`)
- [ ] No real/sensitive data or generated artifacts (`outputs/`, project `data/`, `models/`) included in this PR
- [ ] CI (`validate.yml`) passes
- [ ] If this changes plugin behavior, I bumped the relevant `plugin.json`/`marketplace.json` version and added a CHANGELOG entry
