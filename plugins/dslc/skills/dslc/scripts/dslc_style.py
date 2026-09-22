"""Shared chart style for DSLC notebooks (validated default palette from the dataviz skill).

Usage inside a stage notebook (cwd = project folder):
    import sys; sys.path.insert(0, "../../plugins/dslc/skills/dslc/scripts")
    from dslc_style import apply_style, SERIES, INK, save
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

# Categorical slots in fixed order - never cycle past what the chart needs.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
INK = {
    "surface": "#fcfcfb",
    "primary": "#0b0b0b",
    "secondary": "#52514e",
    "muted": "#898781",
    "grid": "#e1e0d9",
    "axis": "#c3c2b7",
}
STATUS = {"good": "#0ca30c", "warning": "#fab219", "serious": "#ec835a", "critical": "#d03b3b"}


def apply_style() -> None:
    mpl.rcParams.update({
        "figure.facecolor": INK["surface"],
        "axes.facecolor": INK["surface"],
        "savefig.facecolor": INK["surface"],
        "figure.dpi": 110,
        "savefig.dpi": 160,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.labelcolor": INK["secondary"],
        "axes.edgecolor": INK["axis"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": INK["grid"],
        "grid.linewidth": 0.6,
        "xtick.color": INK["muted"],
        "ytick.color": INK["muted"],
        "text.color": INK["primary"],
        "axes.prop_cycle": mpl.cycler(color=SERIES),
        "lines.linewidth": 2,
        "legend.frameon": False,
    })


def save(fig, name: str) -> str:
    Path("figures").mkdir(exist_ok=True)
    path = f"figures/{name}.png"
    fig.savefig(path, bbox_inches="tight")
    return path
