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


if __name__ == "__main__":
    unittest.main()
