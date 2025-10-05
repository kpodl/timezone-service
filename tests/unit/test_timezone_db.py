import pytest
from geopandas import GeoDataFrame
from shapely import Point, Polygon

from timezone_service import TimezoneDatabase


class TestTimezoneDatabase:
    TZ_1 = "TZ1"
    TZ_2 = "TZ2"
    TZ_3 = "TZ3"
    ALL_TZ = (TZ_1, TZ_2, TZ_3)
    POINT_IN_TZ_1 = Point(3, 5)
    POINT_IN_TZ_2 = Point(2, -2)
    POINT_ON_BORDER_OF_TZ_1 = Point(0, 0)

    @pytest.fixture
    def geo_df(self) -> GeoDataFrame:
        return GeoDataFrame(
            {
                TimezoneDatabase.TIMEZONE_HEADER: [
                    self.TZ_1,
                    self.TZ_2,
                    self.TZ_3,
                ],
                TimezoneDatabase.GEOMETRY_HEADER: [
                    Polygon(((0, 0), (10, 0), (0, 10))),
                    Polygon(((0, 0), (3, 0), (3, -2), (0, -5))),
                    Polygon(((0, -5), (-5, -5), (0, -10))),
                ],
            },
            crs=TimezoneDatabase.CRS,
        )

    @pytest.fixture
    def tz_db(self, geo_df: GeoDataFrame) -> TimezoneDatabase:
        return TimezoneDatabase(geo_df)

    def test_get_all_timezones_returns_all_unique_timezones(self):
        tz_db = TimezoneDatabase(
            GeoDataFrame(
                {
                    TimezoneDatabase.TIMEZONE_HEADER: [
                        "America/Toronto",
                        "Europe/Vienna",
                        "Europe/Vienna",
                    ],
                    TimezoneDatabase.GEOMETRY_HEADER: [
                        Point(0, 0),
                        Point(0, 1),
                        Point(1, 1),
                    ],
                },
                crs=TimezoneDatabase.CRS,
            )
        )

        all_timezones_list = list(tz_db.get_all_timezones())

        assert len(all_timezones_list) > 0
        assert len(all_timezones_list) == len(set(all_timezones_list))

    @pytest.mark.parametrize(
        ("point", "resulting_tz"),
        [
            (POINT_IN_TZ_1, TZ_1),
            (POINT_IN_TZ_2, TZ_2),
            (POINT_ON_BORDER_OF_TZ_1, None),
        ],
    )
    def test_get_timezone_for_point_returns_timezone_of_geometry_containing_point(
        self, tz_db: TimezoneDatabase, point: Point, resulting_tz: str | None
    ):
        timezone = tz_db.get_timezone_for_point(point)

        assert timezone == resulting_tz
