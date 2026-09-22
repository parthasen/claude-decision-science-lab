# Execution runtimes

Set per project in `project.yaml → runtime`. Switch any time with
`python scripts/stage.py projects/<slug> --set runtime <local|jupyter-live|colab>`.

## local (default, no-code users, scheduled reruns)

- Kernels: `dslc` (Python 3.11 env at `envs/dslc`) and `ir-dslc` (R).
- Command: `python scripts/run_notebook.py <project> <stage-source> --name <stage> [--kernel ...]`
- Working directory during execution is the project folder, so use `data/raw/...` style paths.
- On failure: read the printed traceback, fix the source file, rerun the whole stage (don't hand-patch the .ipynb) — keeps the notebook runnable top to bottom.
- Long jobs (tuning): run with Bash `run_in_background` and tell the user roughly how long.

## jupyter-live (data scientist co-editing)

- User starts JupyterLab from the workspace: `./scripts/start_jupyter.sh` (port 8888, token from `.env`, collaboration enabled).
- MCP server `jupyter` (Datalayer jupyter-mcp-server) must show as connected. If its tools are missing, tell the user JupyterLab isn't running or Claude Code needs a restart after starting it.
- Workflow: open/create `projects/<slug>/notebooks/<stage>.ipynb`, insert cells one logical step at a time, execute, inspect outputs/images, fix, continue. The user sees edits live and may edit too — re-read cells before overwriting anything they changed.
- Mirror the final cell sources into `stages/<stage>.py` so the `local` runtime can reproduce it.
- R: choose the `ir-dslc` kernel when creating the notebook; if the server can't drive R, fall back to `local` for that stage and say so.

## colab (GPU/TPU, large models)

- Requires: user has a Colab notebook open in their browser, and the `colab-mcp` server connected in Claude Code.
- Before uploading data: if `data_policy.confidential` is true, ask explicitly — the data goes to the user's Google account/Colab VM.
- Install extra packages in the first cell (`%pip install -q lightgbm optuna shap`), set seeds, mount Drive only if the user wants.
- Colab VMs are ephemeral: save models/figures to Drive or download them back into the project (`models/`, `figures/`) before the session ends, and keep the stage source in `stages/`.
- Alternatives when the MCP server isn't available: write the notebook to Google Drive (Drive connector) and ask the user to open it with Colab, or use the VS Code Colab extension.
