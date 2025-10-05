from pathlib import Path
from textwrap import dedent
from typing import Annotated, Self

from fastapi import FastAPI, Query
from fastapi import status as http_status
from pydantic import BaseModel, Field, model_validator
from shapely import Point

from .timezone_db import TimezoneDatabase

TIMEZONES_ENDPOINT = "/timezones"
TIMEZONE_DATA_PATH = Path(__file__).parent.parent.parent / "data" / "tz_world.zip"
TIMEZONE_DATA_ZIP_URI = "zip://" + str(TIMEZONE_DATA_PATH) + "/world/"

app = FastAPI(
    title="Timezones API",
    summary="Provides timezone information for specific coordinates.",
    version="1.0.0",
    description=dedent(
        """
        This API allows you to retrieve the timezone for any point on Earth. It uses WGS 84
        for the coordinates.
        """
    ),
)

timezone_db: TimezoneDatabase = TimezoneDatabase.from_file(TIMEZONE_DATA_ZIP_URI)


class CoordinateParams(BaseModel):
    model_config = {"extra": "forbid"}

    lat: float | None = Field(
        None,
        ge=-90,
        le=90,
        title="Latitude",
        description="The latitude in decimal degrees according to WGS 84. North is positive, south is negative.",
        examples=[48.2081],
    )
    lon: float | None = Field(
        None,
        ge=-180,
        le=180,
        title="Longitude",
        description="The longitude in decimal degrees according to WGS 84. East is positive, west is negative.",
        examples=[16.3713],
    )

    @model_validator(mode="after")
    def validate_all_or_no_coordinates_set(self) -> Self:
        if (self.lat is None) is not (self.lon is None):
            raise ValueError("Either both 'lat' and 'lon' must be set or none of them.")
        return self

    def as_point(self) -> Point | None:
        # At this point we know that the validation has run. So either
        # all coordinates are set or none of them is.
        if self.lat is not None and self.lon is not None:
            return Point(self.lon, self.lat)
        else:
            return None


@app.get(
    TIMEZONES_ENDPOINT,
    name="Timezones",
    summary="Retrieve timezones",
    description=dedent(
        """
        This endpoint retrieves timezones.

        - By providing longitude (`lon` parameter) and latitude (`lat` parameter) the timezone
            for that coordinate will be returned.
        - Without any parameters a list of all available timezones will be returned.

        A timezone will be returned for every point on Earth with valid coordinates:

        - Either a local timezone such as `Europe/Paris`,
        - or a generic timezone (`Etc/GMT±N`) for points on an ocean or in uninhabited areas.

        The timezone on the poles (latitude `±90`) is undefined. This service will return
        generic timezones derived from the longitude.
        """,
    ),
    responses={http_status.HTTP_200_OK: {"content": {"application/json": {"example": "Europe/Paris"}}}},
)
async def timezones(coordinates_query: Annotated[CoordinateParams, Query()]) -> list[str] | str:
    point = coordinates_query.as_point()
    if not point:
        return timezone_db.get_all_timezones()
    else:
        return timezone_db.get_timezone_for_point(point)
