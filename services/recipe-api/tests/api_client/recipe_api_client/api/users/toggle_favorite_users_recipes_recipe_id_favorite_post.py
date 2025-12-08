from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.toggle_favorite_users_recipes_recipe_id_favorite_post_response_toggle_favorite_users_recipes_recipe_id_favorite_post import (
    ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost,
)
from ...types import Response


def _get_kwargs(
    recipe_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/users/recipes/{recipe_id}/favorite".format(
            recipe_id=quote(str(recipe_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    HTTPValidationError
    | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost
    | None
):
    if response.status_code == 200:
        response_200 = ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost.from_dict(
            response.json()
        )

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    HTTPValidationError
    | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    recipe_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[
    HTTPValidationError
    | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost
]:
    """Toggle Favorite

    Args:
        recipe_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost]
    """

    kwargs = _get_kwargs(
        recipe_id=recipe_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    recipe_id: UUID,
    *,
    client: AuthenticatedClient,
) -> (
    HTTPValidationError
    | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost
    | None
):
    """Toggle Favorite

    Args:
        recipe_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost
    """

    return sync_detailed(
        recipe_id=recipe_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    recipe_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[
    HTTPValidationError
    | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost
]:
    """Toggle Favorite

    Args:
        recipe_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost]
    """

    kwargs = _get_kwargs(
        recipe_id=recipe_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    recipe_id: UUID,
    *,
    client: AuthenticatedClient,
) -> (
    HTTPValidationError
    | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost
    | None
):
    """Toggle Favorite

    Args:
        recipe_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ToggleFavoriteUsersRecipesRecipeIdFavoritePostResponseToggleFavoriteUsersRecipesRecipeIdFavoritePost
    """

    return (
        await asyncio_detailed(
            recipe_id=recipe_id,
            client=client,
        )
    ).parsed
