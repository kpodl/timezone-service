from collections.abc import Iterable
from pathlib import Path

from fastapi import FastAPI

from .timezone_db import TimezoneDatabase

TIMEZONES_ENDPOINT = "/timezones"
TIMEZONE_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "tz_world.zip"
TIMEZONE_DATA_ZIP_URI = "zip://" + str(TIMEZONE_DATA_PATH) + "/world/"

app = FastAPI()

timezone_db: TimezoneDatabase = TimezoneDatabase.from_file(TIMEZONE_DATA_ZIP_URI)


@app.get(TIMEZONES_ENDPOINT)
async def timezones() -> Iterable[str]:
    return timezone_db.get_all_timezones()
