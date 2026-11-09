# Expenses exercise

CLI tool and stateless FastAPI service which aggregate expenses from `Expenses.csv` or other csv with the same format.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

Requires Python 3.14+.

## CLI

Reads CSV from stdin. The entry point is `expenses.py`.

```bash
cat Expenses.csv | python3 expenses.py Sales
cat Expenses.csv | python3 expenses.py Sales 2023
cat Expenses.csv | python3 expenses.py Sales 2023 Q1
cat Expenses.csv | python3 expenses.py Sales 2023 Jan
```

Department name and period are case insensitive.

Accepted period values:

- Quarters (`Q1`..`Q4`).
- Month names (`Jan`, `January`)
- Month numbers (`1`..`12`)

## REST API

Start the service:

```bash
uvicorn app:app --reload
```

Send CSV data in the request body. The department, year and period filters can be set as GET parameters:

```bash
curl -X POST \
  'http://127.0.0.1:8000/?department=Sales&year=2023&period=Q1' \
  -H 'Content-Type: text/csv' \
  --data-binary @Expenses.csv
```

```json
{"total": "$781,696,332"}
```

Parameters:

- `department` required
- `year` optional
- `period` optional, requires `year`

Invalid input returns `400`; FastAPI validation errors return `422`.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Database schema

`schema.sql` is the PostgreSQL schema for Task 4. It stores one row per CSV month and preserves duplications by expense_type. It is not normalized intentionally, given the small dataset.
