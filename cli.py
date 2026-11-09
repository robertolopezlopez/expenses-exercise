import argparse
import sys

from formatter.formatter import formatExpense
from reader.reader import read_total


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("department")
    parser.add_argument("year", type=int, nargs="?")
    parser.add_argument("period", nargs="?")
    return parser

def main() -> str:
    # add CLI parameter handling
    args = build_parser().parse_args()

    # read stdin
    total = read_total(sys.stdin, ';', args.department, args.year, args.period)
    return formatExpense(total)


if __name__ == "__main__":
    print(main())
