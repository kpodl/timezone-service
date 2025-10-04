import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from timezone_service import app as timezone_service_app


@pytest.fixture
def app() -> FastAPI:
    return timezone_service_app


@pytest.fixture
def test_client(app: FastAPI) -> TestClient:
    return TestClient(app)
