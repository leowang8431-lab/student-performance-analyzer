# Student Performance Report

Dataset: **Synthetic demo (if unchanged)**

Validated records: **24**. No rows were dropped or imputed.

## Exam scores

| Statistic | Value |
| :--- | ---: |
| Mean | 70.67 |
| Median | 71.50 |
| Minimum | 45.00 |
| Maximum | 91.00 |
| Sample variance (ddof=1) | 161.71 |
| Sample standard deviation (ddof=1) | 12.72 |

Pass threshold: 60/100 (configurable demo rule).
Passing records: 19/24 (79.17%).

## Pearson correlations with exam score

| Factor | Paired observations | Pearson r |
| :--- | ---: | ---: |
| Hours_Studied | 24 | 0.824 |
| Sleep_Hours | 24 | 0.289 |
| Attendance | 24 | 0.939 |
| Previous_Scores | 24 | 0.969 |

## Interpretation and limitations

- The bundled demo is synthetic: illustrative numbers, not research findings.
- Custom data needs a documented source, permission and sampling context.
- Correlation describes association, not causation or an independent causal effect.
- No p-values, confidence intervals, causal estimates or predictions are produced.
- Sample variance/std use n - 1; they are N/A when n < 2.
- Correlation is N/A with fewer than two rows or a constant input/score column.
- With only two non-constant observations, r is necessarily +1 or -1; do not interpret this as robust evidence.
- Results describe this input only and do not justify population claims.
