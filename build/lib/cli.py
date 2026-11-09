import argparse
import sys

from formatter.formatter import formatExpense
from reader.reader import read_total

# add CLI parameter handling
parser = argparse.ArgumentParser(
    prog="Company expenses"
)
parser.add_argument("department")
parser.add_argument("year", type=int, nargs="?")
parser.add_argument("period", nargs="?")
args = parser.parse_args()

# read stdin
total = read_total(sys.stdin, ';', args.department, args.year, args.period)


if __name__ == "__main__":
    print(formatExpense(total))
