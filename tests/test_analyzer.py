"""Run: python -m unittest discover -s tests -v"""
from __future__ import annotations

import contextlib
import io
import math
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from main import main
from src.analyzer import (
    correlations, format_number, load_data, make_report, summarize, validate_data,
)


class AnalyzerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = pd.DataFrame({
            "Student_ID": ["A", "B", "C"], "Hours_Studied": [1, 2, 3],
            "Sleep_Hours": [6, 7, 8], "Attendance": [70, 80, 90],
            "Previous_Scores": [40, 60, 80], "Exam_Score": [50, 60, 70],
        })

    def test_known_summary_and_sample_ddof(self) -> None:
        stats = summarize(validate_data(self.frame))
        for key, value in {"count": 3, "mean": 60, "median": 60, "minimum": 50,
                           "maximum": 70, "sample_variance": 100, "sample_std": 10}.items():
            self.assertAlmostEqual(stats[key], value)
        self.assertAlmostEqual(stats["pass_rate"], 2 / 3)

    def test_positive_and_negative_correlations(self) -> None:
        self.assertAlmostEqual(correlations(validate_data(self.frame))["Hours_Studied"], 1)
        self.frame["Hours_Studied"] = [3, 2, 1]
        self.assertAlmostEqual(correlations(validate_data(self.frame))["Hours_Studied"], -1)

    def test_constant_factor_is_undefined(self) -> None:
        self.frame["Hours_Studied"] = [2, 2, 2]
        self.assertIsNone(correlations(validate_data(self.frame))["Hours_Studied"])

    def test_constant_scores_are_undefined(self) -> None:
        self.frame["Exam_Score"] = [60, 60, 60]
        self.assertTrue(all(v is None for v in correlations(validate_data(self.frame)).values()))

    def test_single_row(self) -> None:
        data = validate_data(self.frame.iloc[:1])
        self.assertIsNone(summarize(data)["sample_std"])
        self.assertIsNone(summarize(data)["sample_variance"])
        self.assertTrue(all(v is None for v in correlations(data).values()))

    def test_missing_column_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            validate_data(self.frame.drop(columns="Exam_Score"))

    def test_empty_frame_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "no student records"):
            validate_data(self.frame.iloc[:0])

    def test_bad_numeric_values_rejected(self) -> None:
        for bad in (None, "oops", "", math.inf, -math.inf, -1, 101):
            with self.subTest(value=bad):
                frame = self.frame.copy()
                frame["Exam_Score"] = pd.Series([bad, 60, 70], dtype=object)
                with self.assertRaisesRegex(ValueError, "Exam_Score"):
                    validate_data(frame)

    def test_duplicate_and_empty_identifiers_rejected(self) -> None:
        for ids in (["A", "A", "C"], ["A", "  ", "C"], ["A", None, "C"]):
            with self.subTest(ids=ids):
                self.frame["Student_ID"] = ids
                with self.assertRaises(ValueError):
                    validate_data(self.frame)

    def test_validation_does_not_mutate_input(self) -> None:
        before = self.frame.copy(deep=True)
        validate_data(self.frame)
        assert_frame_equal(self.frame, before)

    def test_threshold_validation_and_custom_threshold(self) -> None:
        data = validate_data(self.frame)
        self.assertEqual(summarize(data, pass_mark=65)["pass_count"], 1)
        for invalid in (-1, 101, math.inf, math.nan):
            with self.subTest(threshold=invalid), self.assertRaises(ValueError):
                summarize(data, pass_mark=invalid)

    def test_csv_roundtrip_preserves_leading_zero_ids(self) -> None:
        self.frame["Student_ID"] = ["001", "002", "003"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "students.csv"
            self.frame.to_csv(path, index=False, encoding="utf-8-sig")
            data = load_data(path)
            self.assertEqual(data["Student_ID"].iloc[0], "001")
            self.assertEqual(len(data), 3)

    def test_missing_and_empty_csv_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.csv"
            with self.assertRaisesRegex(ValueError, "not found"):
                load_data(path)
            path.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Cannot read"):
                load_data(path)

    def test_report_discloses_limitations(self) -> None:
        data = validate_data(self.frame)
        report = make_report(summarize(data), correlations(data), "Synthetic demo")
        for text in ("synthetic", "not causation", "n - 1", "+1 or -1"):
            self.assertIn(text, report)
        self.assertEqual(format_number(None), "N/A")

    def test_cli_missing_file_returns_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stderr(io.StringIO()) as err:
            code = main(["--input", str(Path(directory) / "missing.csv")])
            self.assertEqual(code, 2)
            self.assertIn("Error:", err.getvalue())


if __name__ == "__main__":
    unittest.main()
