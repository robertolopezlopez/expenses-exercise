from __future__ import annotations

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app import app

EXPENSES_FILE = Path(__file__).resolve().parents[1] / "Expenses.csv"

class RestHappyPathTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_happy_path(self):
        expenses_content = EXPENSES_FILE.read_text()
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

    def test_zero_year(self):
        expenses_content = EXPENSES_FILE.read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"department": "Sales", "year": 0, "period": "Q1"},
                         )
        self.assertEqual(response.status_code, 422)
        self.assertTrue(response.is_error)
        self.assertEqual(response.json()["detail"][0]["msg"], "Input should be greater than or equal to 1")

    def test_no_department(self):
        expenses_content = EXPENSES_FILE.read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"year": 2021, "period": "q1"},
                         )
        # pydantic schema validation - 422
        self.assertEqual(response.status_code, 422) 

    def test_blank_department(self):
        expenses_content = EXPENSES_FILE.read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"department": " ", "year": 2021, "period": "q1"},
                         )
        self.assertEqual(response.status_code, 400)

    def test_period_no_year(self):
        expenses_content = EXPENSES_FILE.read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"department": "consulting", "period": "q1"},
                         )
        self.assertEqual(response.status_code, 400)

    def test_period_not_valid(self):
        expenses_content = EXPENSES_FILE.read_text()
        response = self.client.post("/", content=expenses_content,
                                   params={"department": "consulting", "year": 2021, "period": "qqq"},
                         )
        self.assertEqual(response.status_code, 400)
        self.assertTrue("invalid quarter: qqq" in response.text)


if __name__ == "__main__":
    unittest.main()
