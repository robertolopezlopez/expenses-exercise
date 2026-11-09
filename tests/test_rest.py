from __future__ import annotations

import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app import app

class RestHappyPathTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_happy_path(self):
        expenses_content = (Path(f"{__file__}").parent / "fixtures" / "Expenses.csv").read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"department": "consulting", "year": 2021, "period": "q1"},
                         )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text.strip())
        self.assertEqual(response.json(), {"total": "($16,806,062)"})

    def test_no_body(self):
        response = self.client.post("/", content="",
                                   params={"department": "consulting", "year": 2021, "period": "q1"},
                         )
        self.assertEqual(response.status_code, 400)

    def test_no_department(self):
        expenses_content = (Path(f"{__file__}").parent / "fixtures" / "Expenses.csv").read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"year": 2021, "period": "q1"},
                         )
        # pydantic schema validation - 422
        self.assertEqual(response.status_code, 422) 

    def test_blank_department(self):
        expenses_content = (Path(f"{__file__}").parent / "fixtures" / "Expenses.csv").read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"department": " ", "year": 2021, "period": "q1"},
                         )
        self.assertEqual(response.status_code, 400)

    def test_period_no_year(self):
        expenses_content = (Path(f"{__file__}").parent / "fixtures" / "Expenses.csv").read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"department": "consulting", "period": "q1"},
                         )
        self.assertEqual(response.status_code, 400)

    def test_period_not_valid(self):
        expenses_content = (Path(f"{__file__}").parent / "fixtures" / "Expenses.csv").read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"department": "consulting", "year": 2021, "period": "qqq"},
                         )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
