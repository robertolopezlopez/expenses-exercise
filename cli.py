import argparse
import csv
import sys

def parse_expense(amount: str|int) -> int:
    if type(amount) == int:
        return amount
    amount = amount.replace(",", "").replace("$", "")
    if amount.startswith("("):
        amount = "-" + amount.replace("(", "").replace(")", "")
    
    return int(amount)

def formatExpense(amount: int) -> str :
    """
    Formats the given amount accordingly to the provided csv. Actually, the reverse operation to parse_expense.

    Examples:
    -  parameter: 52455002 -> return: "$52,455,002"
    -  parameter: -22000 -> return: "($22,000)"
    """
    if amount < 0:
        return f"(${abs(amount):,})"
    return f"${amount:,}"

def parse_period(_period: str) -> list[int]:
    """
    Parses the period parameter.
    
    It does not do any validation. Instead, it assumes the following formats:
    - q1..q4
    - Jan..Dec
    - January..December
    - 1..12

    Returns: list of zero based month indexes. It defaults to []
    """

    months = {"jan": 0, "feb": 1, "mar": 2, "apr": 3, "may": 4, "jun": 5, "jul": 6, "aug": 7, "sep": 8, "oct": 9, "nov": 10, "dec": 11}
    quarters = {"q1", "q2", "q3", "q4"}
    period = _period.strip().lower()

    # q1..q4
    if period in quarters:
        quarter = int(period[1])
        return list(range((quarter - 1) * 3, quarter * 3))
    # Jan..Dec or January..December
    if len(period) >= 3 and period[:3] in months:
        return [months[period[:3]]]
    # 1..12
    try:
        return [int(period)-1]
    except KeyError:
        pass

    return []

# add CLI parameter handling
parser = argparse.ArgumentParser(
    prog="Company expenses"
)
parser.add_argument("department")
parser.add_argument("year", type=int, nargs="?")
parser.add_argument("period", nargs="?")
args = parser.parse_args()

# read stdin
total = 0
csv_reader = csv.reader(sys.stdin, delimiter=';')
next(csv_reader, None)

# Read stdin, line by line. If we later want to read directly from the file, this wouuld avoid OOM errors for too big csv (I have seen that already)
for line in csv_reader:
    if len(line) < 3 or line[0].lower().strip() != args.department.lower().strip():
        continue
    if args.year and int(line[2]) != args.year:
        continue
    months = line[3:]
    if args.period:
        months = [months[i] for i in parse_period(args.period)]
    total += sum(parse_expense(amount) for amount in months)


if __name__ == "__main__":
    print(formatExpense(total))




