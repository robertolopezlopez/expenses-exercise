from io import StringIO

from fastapi import FastAPI, HTTPException, Query, Request

from formatter.formatter import formatExpense
from parser.parser import parse_period
from reader.reader import read_total

app = FastAPI()

MAX_BODY_SIZE = 5 * 1024 * 1024  # 5MB

@app.post("/")
async def sum_expenses(
    request: Request,
    department: str = Query(..., min_length=1, ),
    year: int | None = Query(None, ge=1),
    period: str | None = None,
):
    body_generator = request.stream()
    body = []
    len_body = 0
    async for chunk in body_generator:
        body.append(chunk)
        len_body += len(chunk)
        if len_body > MAX_BODY_SIZE:
            raise HTTPException(status_code=413, detail="body is too large")
    if not body:
        raise HTTPException(status_code=400, detail="body should not be empty")

    if not department.strip():
        raise HTTPException(400, "department should not be whitespace")

    if period is not None and not parse_period(period):
        raise HTTPException(status_code=400, detail=f"given period is not valid: {period}")

    if period is not None and parse_period(period) and year is None:
        raise HTTPException(status_code=400, detail=f"given period is not valid without year: {period}")

    try:
        total = read_total(
            StringIO(b"".join(body).decode("utf-8")), ";",
            department, year, period,
        )
    except (UnicodeDecodeError, ValueError, IndexError) as exc:
        raise HTTPException(
            status_code=400,
            detail=f"invalid CSV or parameters: {exc}",
        ) from exc

    return {"total": formatExpense(total)}