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
        ],
        ids=str,
    )
    def test_get_timezone_for_point_returns_timezone_of_geometry_containing_point(
        self, tz_db: TimezoneDatabase, point: Point, resulting_tz: str | None
    ):
        timezone = tz_db.get_timezone_for_point(point)

        assert timezone == resulting_tz

    @pytest.mark.parametrize(
        ("point", "resulting_tz"),
        [
            # We generate a point outside of every geometry that is in the middle of the time zone.
            # WARNING: "Etc/GMT" timezones are reversed ("Etc/GMT+x" is UTC-x)!
            (Point(0 + offset * 15, 0), f"Etc/GMT{-offset:+n}")
            for offset in range(-11, 12)
        ]
        + [
            # 180°/-180° longitude is the date separator. This means we switch from UTC+12
            #  to UTC-12. To the east we have UTC-12, to the west UTC+12.
            (Point(180 - 5, 0), "Etc/GMT-12"),
            (Point(-180 + 5, 0), "Etc/GMT+12"),
            # At the border we just use the sign of the longitude.
            (Point(180, 0), "Etc/GMT-12"),
            (Point(-180, 0), "Etc/GMT+12"),
        ]
        # We include the left border of a timezone but not the right one.
        + [(Point(offset * 15 - 7.5, 0), f"Etc/GMT{-offset:+n}") for offset in range(-11, 12)]
        + [(Point(offset * 15 + 7.5, 0), f"Etc/GMT{-(offset + 1):+n}") for offset in range(-11, 12)],
        ids=str,
    )
    def test_get_timezone_for_point_returns_nautical_timezone_if_none_available(
        self, tz_db: TimezoneDatabase, point: Point, resulting_tz: str
    ):
        timezone = tz_db.get_timezone_for_point(point)

        assert timezone == resulting_tz
