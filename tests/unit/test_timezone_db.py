from geopandas import GeoDataFrame
from shapely import Point

from timezone_service import TimezoneDatabase


class TestTimezoneDatabase:
    def test_get_all_timezones_returns_all_unique_timezones(self):
        tz_db = TimezoneDatabase(
            GeoDataFrame(
                {
                    TimezoneDatabase.TIMEZONE_HEADER: [
                        "America/Toronto",
                        "Europe/Vienna",
                        "Europe/Vienna",
                    ],
                    "geometry": [
                        Point(0, 0),
                        Point(0, 1),
                        Point(1, 1),
                    ],
                },
                crs="EPSG:4326",
            )
        )

        all_timezones_list = list(tz_db.get_all_timezones())

        assert len(all_timezones_list) > 0
        assert len(all_timezones_list) == len(set(all_timezones_list))
