

def parse_period(_period: str|None) -> list[int]:
    """
    Parses the period parameter.
    
    It validates against the following formats:
    - q1..q4
    - Jan..Dec
    - January..December
    - 1..12

    Returns: list of zero based month indexes. Default is all months (1..12) if period is None.
    Raises ValueError if the period is invalid.
    """

    months = {"jan": 0, "feb": 1, "mar": 2, "apr": 3, "may": 4, "jun": 5, "jul": 6, "aug": 7, "sep": 8, "oct": 9, "nov": 10, "dec": 11, "january": 0, "february": 1, "march": 2, "april": 3, "june": 5, "july": 6, "august": 7, "september": 8, "october": 9, "november": 10, "december": 11}
    period = ""
    if _period is None:
        return [i for i in range(12)]
    
    period = _period.strip().lower()

    # q1..q4
    if period.startswith("q"):
        try:
            quarter = int(period[1:])
        except ValueError:
            raise ValueError(f"invalid quarter: {period}")
        if not 0 < quarter <= 4:
            raise ValueError(f"invalid quarter: {period}")
        return list(range((quarter - 1) * 3, quarter * 3))
    period = period.strip().lower()
    # Jan..Dec or January..December
    if len(period) >= 3 and period in months:
        return [months[period]]
    # 1..12
    try:
        month = int(period)
        if not 1 <= month <= 12:
            raise ValueError(f"invalid month: {period}")
    except ValueError:
        raise ValueError(f"invalid period: {period}")

    return [month-1] 

def parse_expense(amount: str|int) -> int:
    if type(amount) == int:
        return amount
    amount = amount.replace(",", "").replace("$", "")
    if amount.startswith("("):
        amount = "-" + amount.replace("(", "").replace(")", "")
    
    return int(amount)