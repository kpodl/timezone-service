from fastapi import FastAPI

TIMEZONES_ENDPOINT = "/timezones"

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}
