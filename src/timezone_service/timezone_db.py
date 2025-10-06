from __future__ import annotations

from functools import cache
from math import trunc
from typing import TYPE_CHECKING, Self

from shapely import Point

if TYPE_CHECKING:
    from geopandas import GeoDataFrame

GMT_TIMEZONE_PREFIX = "Etc/GMT"

GMT_TIMEZONE_BY_OFFSET: dict[int, str] = {
    # Due to conventions "Etc/GMT" timezones are reversed ("Etc/GMT+x" is UTC-x)!
    utc_offset: f"{GMT_TIMEZONE_PREFIX}{-utc_offset:+n}"
    for utc_offset in range(-12, 13)
}


class TimezoneDatabase:
    TIMEZONE_HEADER = "TZID"
    GEOMETRY_HEADER = "geometry"  # this is a standard GeoDataFrame header
    CRS = "EPSG:4326"  # coordinate reference system, mainly used in tests
    UNINHABITED_TIMEZONE = "uninhabited"

    _timezones_df: GeoDataFrame

    @classmethod
    def from_file(cls, path_or_uri: str) -> Self:
        import geopandas

        timezones_df = geopandas.read_file(path_or_uri)
        return cls(timezones_df)

    @classmethod
    def get_nautical_timezone_for_point(cls, point: Point) -> str:
        longitude = point.x
        tz_center, offset_from_center = divmod(longitude, 15.0)
        offset_from_utc = int(tz_center) + trunc(offset_from_center / 7.5)
        return GMT_TIMEZONE_BY_OFFSET[offset_from_utc]

    @classmethod
    def _to_valid_timezones_df(cls, timezones_df: GeoDataFrame) -> GeoDataFrame:
        valid_timezones_df = timezones_df.loc[timezones_df[cls.TIMEZONE_HEADER] != cls.UNINHABITED_TIMEZONE]
        return valid_timezones_df

    def __init__(self, timezones_df: GeoDataFrame):
        self._timezones_df = self._to_valid_timezones_df(timezones_df)

    @cache
    def get_all_timezones(self) -> list[str]:
        return sorted(list(self._timezones_df[self.TIMEZONE_HEADER].unique()) + list(GMT_TIMEZONE_BY_OFFSET.values()))

    def get_timezone_for_point(self, point: Point) -> str:
        # Using `predicate = "intersects"` means that for points on a shared border
        # the timezones off all geometries sharing that point will be found.
        # We only return the first, though.
        timezone_indexes = self._timezones_df.sindex.query(point, predicate="intersects")
        matching_df = self._timezones_df.iloc[timezone_indexes]
        matching_timezones = matching_df[self.TIMEZONE_HEADER].to_list()
        if matching_timezones:
            return matching_timezones[0]
        else:
            return self.get_nautical_timezone_for_point(point)
