# Changelog

[![Latest release](https://img.shields.io/github/v/release/parthasen/claude-decision-science-lab)](https://github.com/parthasen/claude-decision-science-lab/releases/latest)

All notable changes to this repo are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions below track the `dataset-explorer` and `dslc` plugins together since they've moved in lockstep so far.

## [Unreleased]

### Added
- `guides/manager-guide.md` — plain-English user guide for non-coders (managers), walking through how to start, what happens at each step, and what deliverables you get, with no jargon.

## [0.2.0] - 2026-09-22

### Added
- `.github/ISSUE_TEMPLATE/` — bug report and feature request forms, plus config.
- `CHANGELOG.md`.
- Latest-release badge in the README.

### Changed
- Bumped `dataset-explorer` and `dslc` plugin versions (and their marketplace listing) to 0.2.0.

## [0.1.0] - 2026-09-22

### Added
- Initial public release: `dataset-explorer` and `dslc` packaged as installable Claude Code plugins, with a `.claude-plugin/marketplace.json` so they can be installed via `/plugin marketplace add`.
- `dslc` plugin: 8-stage data science lifecycle skills (frame, acquire, profile, prepare, stats, model, explain, report).
- `dataset-explorer` plugin: dataset discovery, briefing, similar-dataset search, and model proposal, handing off to `dslc`.
- `guides/` — decision-science workflow map, prompt guide, LLM-selection guide, retail LLM use cases.
- `projects/perishable-demand-forecast/` — worked example of the full pipeline, run end to end.
- MIT license.
- GitHub Actions `validate.yml` — checks plugin/marketplace JSON validity and compiles all Python scripts on every push/PR.
- `CONTRIBUTING.md`, `CODEOWNERS`, and a pull request template.

[Unreleased]: https://github.com/parthasen/claude-decision-science-lab/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/parthasen/claude-decision-science-lab/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/parthasen/claude-decision-science-lab/releases/tag/v0.1.0
