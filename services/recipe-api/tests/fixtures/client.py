
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from recipe_api.main import app
from recipe_api.shared.db import get_session
from recipe_api_client import AuthenticatedClient


@pytest.fixture(name="client")
def client_fixture(session: Session, test_settings):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        if test_settings.test_token:
            client.headers["Authorization"] = f"Bearer {test_settings.test_token}"
        yield client

    app.dependency_overrides.clear()

@pytest.fixture(name="api_client")
def api_client_fixture(client: TestClient):
    api_client = AuthenticatedClient(base_url=str(client.base_url), token="dummy")
    api_client.set_httpx_client(client)
    return api_client
