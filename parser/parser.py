

def parse_period(_period: str|None) -> list[int]:
    """
    Parses the period parameter.
    
    It validates against the following formats:
    - q1..q4
    - Jan..Dec
    - January..December
    - 1..12

    Returns: list of 1 based month indexes. It defaults to [1..12] if period is None.
    """

    months = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12, "january": 1, "february": 2, "march": 3, "april": 4, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}
    period = ""
    if period is None:
        return list(range(1, 13))
    if _period is not None:
        period = _period.strip()

    # q1..q4
    if period.lower().startswith("q"):
        try:
            quarter = int(period[1:])
        except ValueError:
            raise ValueError(f"Invalid quarter: {period}")
        if not 0 < quarter <= 4:
            raise ValueError(f"Invalid quarter: {period}")
        return list(range((quarter - 1) * 3 + 1, quarter * 3 + 1))
    # Jan..Dec or January..December
    if len(period) >= 3 and period.lower() in months:
        return [months[period.lower()]]
    # 1..12
    try:
        month = int(period)
    except ValueError:
        raise ValueError(f"Invalid month: {period}")
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {month}")
    
    return [month]

def parse_expense(amount: str|int) -> int:
    if type(amount) == int:
        return amount
    amount = amount.replace(",", "").replace("$", "")
    if amount.startswith("("):
        amount = "-" + amount.replace("(", "").replace(")", "")
    
    return int(amount)