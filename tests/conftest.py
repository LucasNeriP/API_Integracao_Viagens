import pytest
from fastapi.testclient import TestClient

from app.main import app

URL = "/api/v1/viagens/normalizar"


@pytest.fixture
def cliente():
    return TestClient(app)
