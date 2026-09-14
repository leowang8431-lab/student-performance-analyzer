"""One scatter plot with correctly labelled axes; no fitted causal model."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save a file without needing a desktop GUI.
import matplotlib.pyplot as plt
import pandas as pd


def save_scatter(data: pd.DataFrame, path: Path, dataset_label: str) -> None:
    """Study hours on x, exam score on y. Always close the figure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5.3))
    try:
        ax.scatter(data["Hours_Studied"], data["Exam_Score"], s=46, alpha=0.8)
        ax.set_xlabel("Study hours per week (hours)")
        ax.set_ylabel("Exam score (0-100)")
        ax.set_title(f"Study hours and exam score\n{dataset_label} | n={len(data)}", pad=14)
        ax.set_ylim(0, 100)
        ax.set_xlim(left=0)
        ax.grid(True, alpha=0.25)
        ax.set_axisbelow(True)
        fig.text(0.5, 0.025, "Association only; not evidence of causation.",
                 ha="center", fontsize=10)
        fig.tight_layout(rect=(0, 0.05, 1, 1))
        fig.savefig(path, dpi=160)
    finally:
        plt.close(fig)
