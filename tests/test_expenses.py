from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from cli import main

FILE_PARENTS = Path(__file__).resolve().parents
EXPENSES_FILE = FILE_PARENTS[0] / "fixtures" / "Expenses.csv"

class CliTest(unittest.TestCase):
    def assert_total(
        self, expected: str, *args: str
    ) -> None:
        stdin = io.StringIO(EXPENSES_FILE.read_text(encoding="utf-8"))
        with patch.object(sys, "argv", ["cli.py", *args]), patch.object(
            sys, "stdin", stdin
        ):
            result = main()

        self.assertEqual(result, expected)

    def test_department_sums_all_years_and_expense_types(self):
        self.assert_total("$7,069,662,522", "Sales")

    def test_year_totals(self):
        expected = {
            "2020": "$1,251,656,782",
            "2021": "$1,377,022,938",
            "2022": "$1,495,748,375",
            "2023": "$2,945,234,427",
        }
        for year, total in expected.items():
            with self.subTest(year=year):
                self.assert_total(total, "Sales", year)

    def test_quarters(self):
        expected = {
            "Q1": "$781,696,332",
            "Q2": "$674,205,919",
            "Q3": "$743,914,102",
            "Q4": "$745,418,074",
        }
        for quarter, total in expected.items():
            with self.subTest(quarter=quarter):
                self.assert_total(total, "Sales", "2023", quarter)

    def test_month_aliases(self):
        self.assert_total("$266,293,985", "Sales", "2023", "Jan")
        self.assert_total("$266,293,985", "Sales", "2023", "January")
        self.assert_total("$224,426,256", "Sales", "2023", "Apr")
        self.assert_total("$224,426,256", "Sales", "2023", "4")
        self.assert_total("$259,647,116", "Sales", "2023", "Dec")
        self.assert_total("$259,647,116", "Sales", "2023", "12")

    def test_month_filter_across_years(self):
        self.assert_total("$138,640,128", "Sales", "2022", "Dec")
        self.assert_total("$266,293,985", "Sales", "2023", "Jan")

    def test_negative_amounts_format(self):
        self.assert_total("($552,890,328)", "Human Resources", "2020")
        self.assert_total("($153,956,471)", "Human Resources", "2020", "Q1")

    def test_sum_department_year_type_rows(self):
        # Sales 2023 appears twice in Expenses.csv: Software and Advertising
        # assert sum of both rows
        self.assert_total("$2,945,234,427", "Sales", "2023")


if __name__ == "__main__":
    unittest.main()
