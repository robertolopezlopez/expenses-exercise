from io import StringIO

from fastapi import FastAPI, HTTPException, Query, Request

from formatter.formatter import formatExpense
from reader.reader import read_total

app = FastAPI()

@app.post("/")
async def sum_expenses(
    request: Request,
    department: str = Query(..., min_length=1, ),
    year: int | None = Query(None, ge=1),
    period: str | None = None,
):
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="body should not be empty")

    if not department.strip():
        raise HTTPException(400, "department should not be whitespace")

    try:
        total = read_total(
            StringIO(body.decode("utf-8")), ";",
            department, year, period,
        )
    except (UnicodeDecodeError, ValueError, IndexError) as exc:
        raise HTTPException(
            status_code=400,
            detail=f"invalid CSV or parameters: {exc}",
        ) from exc

    return {"total": formatExpense(total)}