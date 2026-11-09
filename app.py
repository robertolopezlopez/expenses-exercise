from fastapi import FastAPI

app = FastAPI()

@app.post("/")
async def sum_expenses():
    return "HELLO, WORLD!"