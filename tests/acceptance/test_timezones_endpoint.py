from fastapi.testclient import TestClient

from timezone_service.main import TIMEZONES_ENDPOINT


def test_timezones_endpoint_without_parameter_returns_all_timezones(test_client: TestClient):
    # When all timezones are requested,
    response = test_client.get(TIMEZONES_ENDPOINT)

    # Then a list of timezone strings will be returned.
    assert response.is_success
    timezones: list[str] = response.json()
    assert isinstance(timezones, list)
    assert len(timezones) > 0


def test_timezones_endpoint_with_lon_and_lat_returns_timezone_of_coordinate(test_client: TestClient):
    # When the timezone for the coordinates of Vienna is requested,
    response = test_client.get(TIMEZONES_ENDPOINT, params={"lat": 48.2081, "lon": 16.3713})

    # Then the timezone "Europe/Vienna" will be returned.
    assert response.is_success
    timezone: str = response.json()
    assert timezone == "Europe/Vienna"


def test_timezones_endpoint_for_point_in_ocean_returns_nautical_timezone(test_client: TestClient):
    # When the timezone for a point in the Atlantic is requested,
    response = test_client.get(TIMEZONES_ENDPOINT, params={"lat": -10, "lon": -29})

    # Then the nautical timezone using the "Etc/GMT" prefix is returned.
    assert response.is_success
    timezone: str = response.json()
    assert timezone == "Etc/GMT+2"
