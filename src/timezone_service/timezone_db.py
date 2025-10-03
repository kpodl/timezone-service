from typing import Self

import geopandas
from geopandas import GeoDataFrame


class TimezoneDatabase:
    TIMEZONE_HEADER = "TZID"

    _timezones_df: GeoDataFrame

    @classmethod
    def from_file(cls, path_or_uri: str) -> Self:
        timezones_df = geopandas.read_file(path_or_uri)
        return cls(timezones_df)

    def __init__(self, timezones_df: GeoDataFrame):
        self._timezones_df = timezones_df

    def get_all_timezones(self) -> set[str]:
        return set(self._timezones_df[self.TIMEZONE_HEADER])
