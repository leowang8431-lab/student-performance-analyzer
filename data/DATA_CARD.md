# Data card: synthetic student demo

**These 24 hand-authored records are simulated teaching data. They are not from a
university, survey, Kaggle dataset or real students.** IDs S001-S024 identify no
real people. The values were prepared with this AI-assisted starter to exercise
the program. Relationships were constructed, not discovered through research.
There is no claimed empirical generative model.

| Column | Meaning | Accepted range / rule |
| :--- | :--- | :--- |
| Student_ID | Fictional record identifier | Non-empty and unique |
| Hours_Studied | Study hours per week | 0-168 |
| Sleep_Hours | Average sleep hours per day | 0-24 |
| Attendance | Attendance percentage | 0-100; use 90, not 0.90 |
| Previous_Scores | Prior score | 0-100 |
| Exam_Score | Current score | 0-100 |

These ranges are software assumptions. The default pass mark of 60/100 is a
configurable demo choice, not a claim about any university's grading policy.

Use the file to learn CSV loading, validation, descriptive statistics, plotting
and testing. Do not claim its correlations establish real educational findings,
causal effects or prediction accuracy. No missing values were silently filled.

Keep the demo unchanged. Put authorised private input under `data/private/` and
use `--input`. Other datasets and `results/` are ignored by Git by default, but
ignore rules are not encryption or access control. Never force-add private data;
a file already tracked by Git is not protected by a newly added ignore rule.
Inspect changes before pushing. Replacing names with IDs does not by itself
ensure anonymisation.

For a later public-data extension, document the source, license, sampling method,
collection period and missing-value policy before interpreting results.
