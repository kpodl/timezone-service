from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from timezone_service import app as timezone_service_app


@pytest.fixture
def app() -> FastAPI:
    return timezone_service_app


@pytest.fixture
def test_client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
