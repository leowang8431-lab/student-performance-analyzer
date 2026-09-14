"""Run from the project folder: python main.py"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.analyzer import correlations, format_number, load_data, make_report, summarize
from src.visualizer import save_scatter

ROOT = Path(__file__).resolve().parent
DEMO = ROOT / "data" / "demo_students.csv"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze student CSV data (learning project).")
    parser.add_argument("--input", type=Path, default=DEMO, help="UTF-8 CSV input file")
    parser.add_argument("--output", type=Path, default=ROOT / "results", help="Generated report folder")
    parser.add_argument("--pass-mark", type=float, default=60.0, help="Passing score, 0-100 (default: 60)")
    args = parser.parse_args(argv)
    report_path = args.output / "report.md"
    plot_path = args.output / "study_hours.png"
    try:
        source = args.input.resolve()
        if source in {report_path.resolve(), plot_path.resolve()}:
            raise ValueError("An output would overwrite your input. Choose another output folder.")
        data = load_data(args.input)
        summary = summarize(data, pass_mark=args.pass_mark)
        associations = correlations(data)
        label = ("Synthetic demo (if unchanged)" if source == DEMO.resolve()
                 else "User-supplied data; provenance not verified")
        report = make_report(summary, associations, label)
        args.output.mkdir(parents=True, exist_ok=True)
        save_scatter(data, plot_path, label)
        report_path.write_text(report, encoding="utf-8")
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print("Student Performance Analyzer | v0.1")
    print(f"Dataset: {label}")
    print(f"Valid records: {summary['count']}")
    print(f"Mean exam score: {format_number(summary['mean'])}")
    print(f"Median exam score: {format_number(summary['median'])}")
    print(f"Sample standard deviation (ddof=1): {format_number(summary['sample_std'])}")
    print(f"Pass rate (>= {summary['pass_mark']:g}): {100 * summary['pass_rate']:.2f}%")
    print(f"Study-hours / score Pearson r: {format_number(associations['Hours_Studied'], 3)}")
    print(f"Report saved: {report_path}")
    print(f"Chart saved: {plot_path}")
    print("Reminder: correlation does not establish causation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
