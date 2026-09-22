#!/usr/bin/env python
"""Build a notebook from a percent-format script and execute it headlessly.

The source file uses `# %%` to start a code cell and `# %% [markdown]` for a
markdown cell (same convention as Jupytext / VS Code), so Python and R stage
code can be written as plain text and still produce a real .ipynb.

Usage:
  python run_notebook.py <project-dir> <source.py|source.R> [--name 03_profile] [--kernel dslc|ir-dslc] [--timeout 1800]

The executed notebook is written to <project-dir>/notebooks/<name>.ipynb.
Execution happens with the project directory as working directory, so code
should use relative paths such as data/raw/... and figures/....
Exit code is non-zero if any cell failed; the failing cell and traceback are printed.
"""
import argparse
import re
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

CELL_RE = re.compile(r"^# %%(.*)$")


def parse(text: str, is_r: bool):
    cells, kind, buf = [], "code", []

    def flush():
        body = "\n".join(buf).strip("\n")
        if not body:
            return
        if kind == "markdown":
            body = "\n".join(re.sub(r"^# ?", "", ln) for ln in body.splitlines())
            cells.append(nbformat.v4.new_markdown_cell(body))
        else:
            cells.append(nbformat.v4.new_code_cell(body))

    for line in text.splitlines():
        m = CELL_RE.match(line)
        if m:
            flush()
            buf = []
            kind = "markdown" if "[markdown]" in m.group(1) else "code"
        else:
            buf.append(line)
    flush()
    return cells


def summarize(nb) -> None:
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        for out in cell.get("outputs", []):
            if out.output_type == "stream":
                txt = out.text.strip()
                if txt:
                    print(f"--- cell {i} stdout ---\n{txt[-3000:]}")
            elif out.output_type in ("execute_result", "display_data"):
                data = out.get("data", {})
                if "image/png" in data:
                    print(f"--- cell {i}: [figure]")
                elif "text/plain" in data:
                    print(f"--- cell {i} result ---\n{data['text/plain'][-2000:]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("source")
    ap.add_argument("--name")
    ap.add_argument("--kernel")
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()

    proj = Path(args.project).resolve()
    src = Path(args.source)
    is_r = src.suffix.lower() == ".r"
    kernel = args.kernel or ("ir-dslc" if is_r else "dslc")
    name = args.name or src.stem

    nb = nbformat.v4.new_notebook()
    nb.cells = parse(src.read_text(), is_r)
    nb.metadata["kernelspec"] = {
        "name": kernel,
        "display_name": kernel,
        "language": "R" if is_r else "python",
    }

    out_path = proj / "notebooks" / f"{name}.ipynb"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    client = NotebookClient(nb, timeout=args.timeout, kernel_name=kernel,
                            resources={"metadata": {"path": str(proj)}})
    failed = False
    try:
        client.execute()
    except CellExecutionError as e:
        failed = True
        print("CELL FAILED:\n" + str(e)[-4000:], file=sys.stderr)
    finally:
        nbformat.write(nb, out_path)

    summarize(nb)
    print(f"\nNotebook written: {out_path}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
