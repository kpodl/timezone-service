from math import trunc
from typing import Self

import geopandas
from geopandas import GeoDataFrame
from shapely import Point


class TimezoneDatabase:
    TIMEZONE_HEADER = "TZID"
    GEOMETRY_HEADER = "geometry"  # this is a standard GeoDataFrame header
    CRS = "EPSG:4326"  # coordinate reference system, mainly used in tests
    UNINHABITED_TIMEZONE = "uninhabited"

    _timezones_df: GeoDataFrame

    @classmethod
    def from_file(cls, path_or_uri: str) -> Self:
        timezones_df = geopandas.read_file(path_or_uri)
        return cls(timezones_df)

    @classmethod
    def get_nautical_timezone_for_point(cls, point: Point) -> str:
        longitude = point.x
        tz_center, offset_from_center = divmod(longitude, 15.0)
        offset_from_utc = int(tz_center) + trunc(offset_from_center / 7.5)
        return f"Etc/GMT{-offset_from_utc:+n}"

    def __init__(self, timezones_df: GeoDataFrame):
        self._timezones_df = timezones_df

    def get_all_timezones(self) -> list[str]:
        return list(set(self._timezones_df[self.TIMEZONE_HEADER]))

    def get_timezone_for_point(self, point: Point) -> str:
        # Using `predicate = "within"` ensures that the result is unique under the
        # assumption that the geometries do not overlap (disjunct except for border).
        timezone_indexes = self._timezones_df.sindex.query(point, predicate="within")
        matching_df = self._timezones_df.iloc[timezone_indexes]
        valid_timezones_df = matching_df.loc[matching_df[self.TIMEZONE_HEADER] != self.UNINHABITED_TIMEZONE]
        valid_timezones = valid_timezones_df[self.TIMEZONE_HEADER].to_list()
        if valid_timezones:
            return valid_timezones[0]
        else:
            return self.get_nautical_timezone_for_point(point)
