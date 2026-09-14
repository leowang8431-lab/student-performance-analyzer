"""CSV validation and descriptive statistics. No machine learning in v0.1."""
from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

# Demo schema rules, not a university's course or grading policy.
RANGES = {
    "Hours_Studied": (0, 168),   # Hours per week / 每周学习小时数
    "Sleep_Hours": (0, 24),      # Hours per day / 每天睡眠小时数
    "Attendance": (0, 100),      # Percentage / 出勤率（百分数）
    "Previous_Scores": (0, 100),
    "Exam_Score": (0, 100),
}
REQUIRED_COLUMNS = ("Student_ID", *RANGES)
FACTORS = tuple(name for name in RANGES if name != "Exam_Score")


def validate_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a validated copy, or fail clearly. Never silently drop/fill rows."""
    missing = [name for name in REQUIRED_COLUMNS if name not in frame.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    if frame.empty:
        raise ValueError("The CSV contains no student records.")
    # Keep only the schema columns; do not carry extra personal data forward.
    data = frame.loc[:, list(REQUIRED_COLUMNS)].copy().reset_index(drop=True)
    ids = data["Student_ID"].astype("string").str.strip()
    if ids.isna().any() or ids.eq("").any():
        raise ValueError("Student_ID must be present for every record.")
    if ids.duplicated().any():
        raise ValueError("Duplicate Student_ID: use one row per student.")
    data["Student_ID"] = ids
    for name, (lower, upper) in RANGES.items():
        values = pd.to_numeric(data[name], errors="coerce")
        valid = values.notna() & values.between(lower, upper)
        if not valid.all():
            records = ", ".join(str(i + 1) for i in data.index[~valid][:5])
            raise ValueError(
                f"{name}: expected a finite number from {lower:g} to {upper:g}. "
                f"Check data record(s) {records} (header not counted). "
                "No rows were removed or filled automatically."
            )
        data[name] = values.astype(float)
    return data


def load_data(path: Path | str) -> pd.DataFrame:
    """Read a comma-separated UTF-8 CSV, with or without a UTF-8 BOM."""
    try:
        frame = pd.read_csv(path, encoding="utf-8-sig", dtype={"Student_ID": "string"})
    except FileNotFoundError as exc:
        raise ValueError(f"CSV file not found: {path}") from exc
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeError) as exc:
        raise ValueError("Cannot read CSV. Use a non-empty UTF-8, comma-separated file.") from exc
    return validate_data(frame)


def summarize(data: pd.DataFrame, pass_mark: float = 60.0) -> dict:
    """Summarize validated data. Sample variance/std use n - 1 (ddof=1)."""
    if not math.isfinite(pass_mark) or not 0 <= pass_mark <= 100:
        raise ValueError("pass_mark must be a finite number between 0 and 100.")
    scores = data["Exam_Score"]
    n = len(scores)
    if n == 0:
        raise ValueError("Cannot summarize an empty dataset.")
    return {
        "count": n,
        "mean": float(scores.mean()),
        "median": float(scores.median()),
        "minimum": float(scores.min()),
        "maximum": float(scores.max()),
        "sample_variance": float(scores.var(ddof=1)) if n > 1 else None,
        "sample_std": float(scores.std(ddof=1)) if n > 1 else None,
        "pass_mark": float(pass_mark),
        "pass_count": int((scores >= pass_mark).sum()),
        "pass_rate": float((scores >= pass_mark).mean()),
    }


def correlations(data: pd.DataFrame) -> dict[str, float | None]:
    """Pearson linear associations, not causal effects. None means undefined."""
    result = {}
    scores = data["Exam_Score"]
    for name in FACTORS:
        if len(data) < 2 or data[name].nunique() < 2 or scores.nunique() < 2:
            result[name] = None
        else:
            value = float(data[name].corr(scores, method="pearson"))
            result[name] = value if math.isfinite(value) else None
    return result


def format_number(value: int | float | None, decimals: int = 2) -> str:
    """Do not present an undefined statistic as zero."""
    return "N/A" if value is None else f"{value:.{decimals}f}"


def make_report(summary: dict, associations: dict, dataset_label: str) -> str:
    """Build an aggregate Markdown report without individual records."""
    n = summary["count"]
    metrics = [
        ("Mean", summary["mean"]), ("Median", summary["median"]),
        ("Minimum", summary["minimum"]), ("Maximum", summary["maximum"]),
        ("Sample variance (ddof=1)", summary["sample_variance"]),
        ("Sample standard deviation (ddof=1)", summary["sample_std"]),
    ]
    lines = [
        "# Student Performance Report", "",
        f"Dataset: **{dataset_label}**", "",
        f"Validated records: **{n}**. No rows were dropped or imputed.", "",
        "## Exam scores", "", "| Statistic | Value |", "| :--- | ---: |",
        *[f"| {label} | {format_number(value)} |" for label, value in metrics], "",
        f"Pass threshold: {summary['pass_mark']:g}/100 (configurable demo rule).",
        f"Passing records: {summary['pass_count']}/{n} ({100 * summary['pass_rate']:.2f}%).", "",
        "## Pearson correlations with exam score", "",
        "| Factor | Paired observations | Pearson r |", "| :--- | ---: | ---: |",
        *[f"| {name} | {n} | {format_number(value, 3)} |"
          for name, value in associations.items()], "",
        "## Interpretation and limitations", "",
        "- The bundled demo is synthetic: illustrative numbers, not research findings.",
        "- Custom data needs a documented source, permission and sampling context.",
        "- Correlation describes association, not causation or an independent causal effect.",
        "- No p-values, confidence intervals, causal estimates or predictions are produced.",
        "- Sample variance/std use n - 1; they are N/A when n < 2.",
        "- Correlation is N/A with fewer than two rows or a constant input/score column.",
        "- With only two non-constant observations, r is necessarily +1 or -1; "
        "do not interpret this as robust evidence.",
        "- Results describe this input only and do not justify population claims.", "",
    ]
    return "\n".join(lines)
