import unittest

from parser.parser import parse_period


class TestParser(unittest.TestCase):
    def test_parse_period(self):
        for period, expected in [
            ("q1", [0, 1, 2]),
            ("q2", [3, 4, 5]),
            ("q3", [6, 7, 8]),
            ("q4", [9, 10, 11]),
            ("jan", [0]),
            ("feb", [1]),
            ("mar", [2]),
            ("apr", [3]),
            ("may", [4]),
            ("jun", [5]),
            ("jul", [6]),
            ("aug", [7]),
            ("sep", [8]),
            ("oct", [9]),
            ("nov", [10]),
            ("dec", [11]),
            ("january", [0]),
            ("february", [1]),
            ("march", [2]),
            ("april", [3]),
            ("may", [4]),
            ("june", [5]),
            ("july", [6]),
            ("august", [7]),
            ("september", [8]),
            ("october", [9]),
            ("november", [10]),
            ("december", [11]),
            (None, [x for x in range(12)])
        ]:
            self.assertEqual(parse_period(period), expected, msg=f"period: {period}")

    def test_parse_period_invalid(self):
        for period in ["", "q", "q5", "q0", "q-1", "q1.5", "q1a", "Janasdasd"]:
            with self.assertRaises(ValueError, msg=f"period: {period}"):
                parse_period(period)