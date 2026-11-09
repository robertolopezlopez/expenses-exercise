import csv
from collections.abc import Iterable

from parser.parser import parse_expense, parse_period


def read_total(input: Iterable[str], delimiter: str, department: str, year: int|None, period: str|None) -> int:
    total = 0
    csv_reader = csv.reader(input, delimiter=delimiter)

    header = next(csv_reader, None)
    if not header or header[0].strip().lower() != "department":
        raise ValueError("the CSV input should have a valid header")

    # Read stdin, line by line. If we later want to read directly from the file, this wouuld avoid OOM errors for too big csv (I have seen that already)
    for line in csv_reader:
        if not line:
            continue
        if len(line) != 15:
            raise ValueError("the CSV input must have 15 columns")
        if line[0].lower().strip() != department.lower().strip():
            continue
        if year is not None and int(line[2]) != year:
            continue
        months = line[3:]
        if period is not None:
            months = [line[3:][i] for i in parse_period(period)]
        total += sum(parse_expense(amount) for amount in months)

    return total
