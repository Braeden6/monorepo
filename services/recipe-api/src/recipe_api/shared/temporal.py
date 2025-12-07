from typing import cast

from temporalio.client import Client

from recipe_api.shared.config import settings

_client: Client | None = None

async def get_temporal_client() -> Client:
    global _client
    if _client is None:
        _client = await Client.connect(
            settings.temporal_host,
            namespace=settings.temporal_namespace,
        )
    return cast(Client, _client)


async def close_temporal_client() -> None:
    global _client
    if _client:
        _client = None
