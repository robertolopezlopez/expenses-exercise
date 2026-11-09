import csv
from typing import Iterable

from parser.parser import parse_expense, parse_period


def read_total(input: Iterable[str], delimiter: str, department: str, year: int, period: str|int|None) -> int:
    total = 0
    csv_reader = csv.reader(input, delimiter=delimiter)

    next(csv_reader, None) # TODO there may be header or not

    # Read stdin, line by line. If we later want to read directly from the file, this wouuld avoid OOM errors for too big csv (I have seen that already)
    for line in csv_reader:
        if len(line) < 3 or line[0].lower().strip() != department.lower().strip():
            continue
        if year and int(line[2]) != year:
            continue
        months = line[3:]
        if period:
            months = [months[i] for i in parse_period(period)]
        total += sum(parse_expense(amount) for amount in months)

    return total
