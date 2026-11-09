

def formatExpense(amount: int|None) -> str :
    """
    Formats the given amount accordingly to the provided csv. Actually, the reverse operation to parse_expense.

    Examples:
    -  parameter: 52455002 -> return: "$52,455,002"
    -  parameter: -22000 -> return: "($22,000)"
    """
    if not amount:
        return "$0"
    if amount < 0:
        return f"(${abs(amount):,})"
    return f"${amount:,}"