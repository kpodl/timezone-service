import pytest
from fastapi import status as http_status
from fastapi.testclient import TestClient

from timezone_service.main import TIMEZONES_ENDPOINT


class TestTimezonesEndpoint:
    @pytest.mark.parametrize(
        ("lat", "lon", "is_valid"),
        [
            # No coordinates
            (None, None, True),
            # Only one coordinate set
            (0, None, False),
            (None, 0, False),
            # Both coordinates set and within range
            (-15.0, 150.0, True),
            # Coordinates on the boundary
            (-90.0, -180.0, True),
            (-90.0, 180.0, True),
            (90.0, -180.0, True),
            (90.0, 180.0, True),
            # Coordinates beyond valid range
            (-90.1, 0, False),
            (90.1, 0, False),
            (0, 180.1, False),
            (0, -180.1, False),
            # one invalid coordinate
            ("A", 0, False),
            (0, "A", False),
        ],
    )
    def test_validates_coordinate_parameters(
        self,
        test_client: TestClient,
        lat: float | str | None,
        lon: float | str | None,
        is_valid: bool,
    ):
        params: dict[str, float | str] = {}
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        response = test_client.get(TIMEZONES_ENDPOINT, params=params)

        assert (
            response.status_code
            == {True: http_status.HTTP_200_OK, False: http_status.HTTP_422_UNPROCESSABLE_CONTENT}[is_valid]
        )
