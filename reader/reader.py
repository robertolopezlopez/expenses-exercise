"""CSV expense aggregation.

Streams Expenses.csv-shaped input and sums matching rows by department, year,
and period. Shared by the CLI (``expenses.py``) and the REST service
(``app.py``).
"""

import csv
from collections.abc import Iterable

from parser.parser import parse_expense, parse_period


def read_total(input: Iterable[str], delimiter: str, department: str, year: int|None, period: str|None) -> int:
    """Sum expenses from CSV input, filtered by department, year, and period.

    Expects the Expenses.csv layout: a header with
    ``Department;Expense Type;Year;Jan;...;Dec`` data rows. Every
    non-empty data row must have 15 fields. Rows are matched by department
    (case-insensitive) and, when given, by year and period. All expense types
    for a matching row are summed.

    ``period`` accepts a quarter (``q1``..``q4``), a month name (``Jan``,
    ``January``), or a month number (``1``..``12``). When ``year`` is
    ``None``, the period is applied to the same months in every year.

    Args:
        input: Iterable of CSV text lines, such as an open file or ``sys.stdin``.
        delimiter: Field delimiter, e.g. ``";"``.
        department: Department name; case and surrounding whitespace are ignored.
        year: Year to include. ``None`` includes all years.
        period: Month or quarter to include. ``None`` includes all months.

    Returns:
        Total in whole currency units. Negative values represent credits.

    Raises:
        ValueError: The header is missing or does not start with ``Department``,
            a data row does not have 15 fields, or a year or amount cell is not
            a valid integer.
    """
    total = 0
    csv_reader = csv.reader(input, delimiter=delimiter)

    header = next(csv_reader, None)
    # FIXME what about the other header columns
    if not header or header[0].strip().lower() != "department":
        raise ValueError("the CSV input should have a valid header")

    # Read stdin, line by line. If we later want to read directly from the file, this wouuld avoid OOM errors for too big csv (I have seen that already)
    for line in csv_reader:
        if not line:
            continue
        if len(line) != 15: # FIXME just checks length, not semantics
            raise ValueError("the CSV input must have 15 columns")
        if line[0].lower().strip() != department.lower().strip():
            continue
        if year is not None and int(line[2]) != year:
            continue
        months = line[3:]
        if period is not None: # FIXME better period validation; validate period + !year
            period_parsed = parse_period(period)
            months = [line[3:][i-1] for i in period_parsed]
        total += sum(parse_expense(amount) for amount in months)

    return total
