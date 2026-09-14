# Student Performance Analyzer

An AI-assisted Python learning starter that validates a CSV, calculates descriptive
statistics, explores linear associations and writes a report and scatter plot.

**v0.1: a runnable starter, not a finished research study or prediction system.**
**All 24 bundled records are synthetic, not real student information.**

中文分步说明：[START_HERE_zh.md](START_HERE_zh.md)

## Features

Validate required columns, unique IDs and numeric ranges; refuse invalid records
rather than silently dropping them or imputing values. Report mean, median,
minimum, maximum, sample variance/std, a configurable pass rate and Pearson
correlations. Save one scatter plot with study hours on x and exam score on y.

No causal drivers, predictions, p-values or confidence intervals are estimated.
See the [data card](data/DATA_CARD.md).

## Windows PowerShell quick start

Start in the extracted folder containing `main.py` and `requirements.txt`.
The starter targets Python 3.11+. Actual tested versions and platform are recorded
in [TEST_RESULTS.txt](docs/TEST_RESULTS.txt); this is not Windows certification.

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Stop at any failed command. If `py` is missing but `python --version` prints a
Python 3 version, use `python -m venv .venv` for the environment-creation step.
If neither works, resolve the interpreter installation before proceeding.

These commands call the environment's interpreter directly: no activation script,
administrator shell or execution-policy change is needed. Installation needs
package-index access; the analysis itself runs locally with no account or API.
Dependencies are compatibility ranges, not a complete reproducible lock file.

The program writes `results/report.md` and `results/study_hours.png`. Re-running
replaces these generated files, not the input CSV. `results/` is ignored by Git.
[Sample report](examples/report.md) and [sample plot](examples/study_hours.png)
were generated from the bundled synthetic data, not private inputs.

## Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

If `venv` is unavailable, resolve that Python installation issue before continuing.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On Linux/macOS, substitute `.venv/bin/python`. Tests cover known-value statistics,
sample denominators, positive/negative and undefined correlations, single rows,
invalid input, duplicate identifiers, CSV encoding/IDs, non-mutation and errors.

## Custom input

Keep the bundled demo unchanged. Store authorised data under `data/private/`:

```powershell
.\.venv\Scripts\python.exe main.py --input data/private/my_students.csv --pass-mark 65
```

CSV must be UTF-8 and comma-separated with this header:

```csv
Student_ID,Hours_Studied,Sleep_Hours,Attendance,Previous_Scores,Exam_Score
S001,5,7,70,48,52
```

One row represents one student. Attendance is a percentage (90, not 0.90); scores
use 0-100. See the data card for units and limits. Keep private inputs and reports
local. A `.gitignore` is not access control and cannot untrack committed files.

## Statistical choices

Sample variance is `sum((x - mean)**2) / (n - 1)`, and sample standard deviation is
its square root. Code uses `ddof=1` explicitly. With one record both are `N/A`.
Pearson r describes linear association, not causation. With fewer than two
records or a constant column it is `N/A`; two non-constant observations necessarily
give +1 or -1, not robust evidence. No factor is labelled the "biggest influence".
The 60/100 passing threshold is a demo default, not a university grading policy.

## Project map

```text
student-performance-analyzer/
├── main.py                    # Command-line entry point
├── src/
│   ├── __init__.py
│   ├── analyzer.py             # Validation, statistics, report
│   └── visualizer.py           # Scatter plot
├── data/
│   ├── demo_students.csv       # Synthetic only
│   └── DATA_CARD.md
├── tests/test_analyzer.py
├── examples/                  # Actual demo outputs
├── docs/
│   ├── LEARNING_TASKS_zh.md
│   └── TEST_RESULTS.txt
├── requirements.txt
├── .gitignore
├── README.md
└── START_HERE_zh.md
```

## Your own contributions

The scaffold was prepared with AI assistance. Read, run and verify it before
claiming expertise. Track your own improvements with meaningful commits and
explain the decisions. See [learning tasks](docs/LEARNING_TASKS_zh.md).
OOP refactoring, licensed public data and inference are later extensions, not
completed features. The package does not create or upload a GitHub repository.

## Official references

- [Python virtual environments](https://docs.python.org/3/library/venv.html)
- [pandas Series.std / ddof](https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html)
- [pandas Series.corr](https://pandas.pydata.org/docs/reference/api/pandas.Series.corr.html)
- [Matplotlib scatter](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html)
