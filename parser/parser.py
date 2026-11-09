

def parse_period(_period: str|None) -> list[int]:
    """
    Parses the period parameter.
    
    It validates against the following formats:
    - q1..q4
    - Jan..Dec
    - January..December
    - 1..12

    Returns: list of zero based month indexes. It defaults to []
    """

    months = {"jan": 0, "feb": 1, "mar": 2, "apr": 3, "may": 4, "jun": 5, "jul": 6, "aug": 7, "sep": 8, "oct": 9, "nov": 10, "dec": 11}
    period = ""
    if _period is not None:
        period = _period.strip().lower()

    # q1..q4
    if period.startswith("q"):
        try:
            quarter = int(period[1:])
        except ValueError:
            return []
        if not 0 < quarter <= 4:
            return []
        return list(range((quarter - 1) * 3, quarter * 3))
    # Jan..Dec or January..December
    if len(period) >= 3 and period[:3] in months:
        return [months[period[:3]]]
    # 1..12
    try:
        month = int(period)
        if not 1 <= month <= 12:
            return []
    except ValueError:
        return []

    return [month-1] 

def parse_expense(amount: str|int) -> int:
    if type(amount) == int:
        return amount
    amount = amount.replace(",", "").replace("$", "")
    if amount.startswith("("):
        amount = "-" + amount.replace("(", "").replace(")", "")
    
    return int(amount)