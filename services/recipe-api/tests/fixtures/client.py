import pytest
from fastapi.testclient import TestClient

from recipe_api.main import app
from recipe_api.shared.config import Settings
from recipe_api_client import AuthenticatedClient


class AuthenticatedTestClient(AuthenticatedClient):
    def __init__(self, test_client: TestClient, token: str):
        super().__init__(base_url=str(test_client.base_url), token=token)
        self._test_client = test_client
        self._token = token

    def get_httpx_client(self):
        self._test_client.headers["Authorization"] = f"Bearer {self._token}"
        return self._test_client


@pytest.fixture(name="client")
def client_fixture():
    with TestClient(app) as c:
        yield c

@pytest.fixture(name="user1_client")
def api_client_user1_fixture(client: TestClient, test_settings: Settings):
    return AuthenticatedTestClient(client, test_settings.test_token_1)


@pytest.fixture(name="user2_client")
def api_client_user2_fixture(client: TestClient, test_settings: Settings):
    return AuthenticatedTestClient(client, test_settings.test_token_2)
