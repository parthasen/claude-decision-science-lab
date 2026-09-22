# How to package and distribute skills as Claude Code plugins

A maintainer's how-to for turning a folder of skills into installable Claude Code plugins others can add with `/plugin marketplace add`. This repo (`claude-decision-science-lab`) is the worked example — every command below is exactly what was run to produce it.

## The end state

```
your-repo/
├── .claude-plugin/
│   └── marketplace.json          # lists every plugin in this repo
└── plugins/
    ├── dataset-explorer/
    │   ├── .claude-plugin/
    │   │   └── plugin.json       # this plugin's own manifest
    │   └── skills/
    │       └── dataset-explorer/
    │           └── SKILL.md
    └── dslc/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            ├── dslc/SKILL.md
            ├── dslc-frame/SKILL.md
            └── ...
```

Each **plugin** is a directory with `.claude-plugin/plugin.json` + a `skills/` subfolder holding one or more skills. The **marketplace** is one manifest at the repo root that points at each plugin directory.

## Step 1 — Wrap each skill as a plugin

For every skill (or group of related skills) you want to distribute independently, create a plugin directory with its own manifest:

```bash
mkdir -p plugins/<plugin-name>/.claude-plugin
mkdir -p plugins/<plugin-name>/skills
cp -R skills/<skill-name> plugins/<plugin-name>/skills/<skill-name>
```

Then write `plugins/<plugin-name>/.claude-plugin/plugin.json`:

```json
{
  "name": "<plugin-name>",
  "version": "0.1.0",
  "description": "One or two sentences: what it does and when to use it.",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "keywords": ["relevant", "search", "terms"]
}
```

`name` is what users type in `/plugin install <name>`, so keep it short and match the folder name.

**Note on sync:** if the skill also needs to keep living outside `plugins/` (e.g. for local, non-plugin use — this repo's `skills/dataset-explorer/` is the source of truth, copied rather than symlinked into `plugins/dataset-explorer/skills/dataset-explorer/`), you're maintaining two copies. Copy, don't symlink — symlinks are more fragile across zip downloads and some git tooling. See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for how this repo keeps them in sync.

## Step 2 — Add the marketplace manifest

At the repo root, create `.claude-plugin/marketplace.json` listing every plugin:

```json
{
  "name": "your-marketplace-name",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "plugins": [
    {
      "name": "dataset-explorer",
      "source": "./plugins/dataset-explorer",
      "description": "Matches the plugin's own description.",
      "version": "0.1.0"
    },
    {
      "name": "dslc",
      "source": "./plugins/dslc",
      "description": "...",
      "version": "0.1.0"
    }
  ]
}
```

`source` is a path relative to the repo root, pointing at each plugin's directory (the one containing `.claude-plugin/plugin.json`).

Validate both manifest types are well-formed JSON before committing:

```bash
for f in .claude-plugin/marketplace.json plugins/*/.claude-plugin/plugin.json; do
  python3 -m json.tool "$f" > /dev/null && echo "OK: $f"
done
```

## Step 3 — Push the repo to GitHub

```bash
git init
git add -A
git commit -m "Initial commit: package skills as Claude Code plugins"
gh repo create <owner>/<repo-name> --public --source=. --remote=origin --push
```

Use `--private` instead of `--public` if distribution should be limited to invited collaborators rather than anyone with Claude Code.

Anything you don't want distributed (generated outputs, real data, model artifacts) should be excluded via `.gitignore` *before* the first commit — see this repo's root `.gitignore` and `projects/*/.gitignore` for the pattern (ignore `outputs/`, `data/`, `models/`, `__pycache__/`).

## Step 4 — Installing it (what your users do)

No cloning, no manual copying. In their own Claude Code:

```
/plugin marketplace add <owner>/<repo-name>
/plugin install dataset-explorer
/plugin install dslc
```

`/plugin marketplace add` also accepts a full URL (`https://github.com/<owner>/<repo-name>`) or a local path, which is useful for testing your own changes before pushing — point it at your local clone instead of the GitHub remote.

## Keeping it updated

- Bump the `version` field in the changed plugin's `plugin.json` **and** its entry in the root `marketplace.json` — they should always match.
- Tag a release (`git tag -a vX.Y.Z`, `git push origin vX.Y.Z`, `gh release create vX.Y.Z`) so users and the README's release badge can tell what's current.
- Users already tracking your marketplace get the new version automatically on their next `/plugin` refresh — nothing further to push on your end beyond the git commit/tag.

Full worked example: this repo's own [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json), [`plugins/dataset-explorer/.claude-plugin/plugin.json`](../plugins/dataset-explorer/.claude-plugin/plugin.json), and [`plugins/dslc/.claude-plugin/plugin.json`](../plugins/dslc/.claude-plugin/plugin.json).
