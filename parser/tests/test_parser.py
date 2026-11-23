import unittest

from parser.parser import parse_period


class TestParse(unittest.TestCase):

    def test_parse_period(self):
        for period, expected, expected_error in [
            ("Jan", [1], None),
            ("feb", [2], None),
            ("mar", [3], None),
            ("apr", [4], None),
            ("may", [5], None),
            ("jun", [6], None),
            ("jul", [7], None),
            ("aug", [8], None),
            ("sep", [9], None),
            ("oct", [10], None),
            ("nov", [11], None),
            ("dec", [12], None),
            ("january", [1], None),
            ("february", [2], None),
            ("march", [3], None),
            ("april", [4], None),
            ("may", [5], None),
            ("june", [6], None),
            ("july", [7], None),
            ("august", [8], None),
            ("september", [9], None),
            ("october", [10], None),
            ("november", [11], None),
            ("december", [12], None),

            ("1", [1], None),
            ("2", [2], None),
            ("3", [3], None),
            ("4", [4], None),
            ("5", [5], None),
            ("6", [6], None),
            ("7", [7], None),
            ("8", [8], None),
            ("9", [9], None),
            ("10", [10], None),
            ("11", [11], None),
            ("12", [12], None),
            ("q1", [1, 2, 3], None),
            ("q2", [4, 5, 6], None),
            ("q3", [7, 8, 9], None),
            ("q4", [10, 11, 12], None),

            ("q5", [], ValueError("Invalid quarter: q5")),
            ("q0", [], ValueError("Invalid quarter: q0")),
            ("q-1", [], ValueError("Invalid quarter: q-1")),
            ("13", [], ValueError("Invalid month: 13")),
            ("0", [], ValueError("Invalid month: 0")),
            ("-1", [], ValueError("Invalid month: -1")),
            ("Janasdfsfd", [], ValueError("Invalid month: Janasdfsfd")),
            ("", [], ValueError("Invalid month: ")),
            ("qqq", [], ValueError("Invalid quarter: qqq")),
        ]:
            if expected_error is not None:
                result = None
                try:
                    result = parse_period(period)
                except ValueError as exc:
                    assert str(exc) == str(expected_error), f"Expected ValueError for period: {period}, wanted: {expected_error}, got: {exc}"
                else:
                    assert False, f"Expected ValueError for period: {period}, got: {result}"
            else:
                assert parse_period(period) == expected, f"Failed for period: {period}, expected: {expected}, got: {parse_period(period)}"
