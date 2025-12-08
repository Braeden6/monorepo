import pytest

from recipe_api_client import Client as ApiClient
from recipe_api_client.api.health import health_health_get, root_get


@pytest.mark.e2e
def test_root(api_client: ApiClient) -> None:
    response = root_get.sync_detailed(client=api_client)
    assert response.status_code == 200
    assert response.parsed is not None
    assert response.parsed["message"] == "Recipe API"
    assert "version" in response.parsed


@pytest.mark.e2e
def test_health(api_client: ApiClient) -> None:
    response = health_health_get.sync_detailed(client=api_client)
    assert response.status_code == 200
    assert response.parsed is not None
    assert response.parsed["status"] == "healthy"
