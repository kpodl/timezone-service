from fastapi.testclient import TestClient

from timezone_service import app
from timezone_service.main import TIMEZONES_ENDPOINT


def test_timezones_endpoint_without_parameter_returns_all_timezones():
    client = TestClient(app)

    response = client.get(TIMEZONES_ENDPOINT)

    assert response.is_success
    timezones: list[str] = response.json()
    assert isinstance(timezones, list)
    assert len(timezones) > 0
