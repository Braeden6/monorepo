from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.food_type import FoodType
from ...models.http_validation_error import HTTPValidationError
from ...models.recipe_query_response import RecipeQueryResponse
from ...models.sort_field import SortField
from ...models.sort_order import SortOrder
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    query: None | str | Unset = UNSET,
    food_types: list[FoodType] | None | Unset = UNSET,
    sort_by: SortField | Unset = UNSET,
    sort_order: SortOrder | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: None | str | Unset = UNSET,
    only_mine: bool | Unset = False,
    only_favorites: bool | Unset = False,
    include_drafts: bool | Unset = True,
    boost_popular: bool | Unset = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_query: None | str | Unset
    if isinstance(query, Unset):
        json_query = UNSET
    else:
        json_query = query
    params["query"] = json_query

    json_food_types: list[str] | None | Unset
    if isinstance(food_types, Unset):
        json_food_types = UNSET
    elif isinstance(food_types, list):
        json_food_types = []
        for food_types_type_0_item_data in food_types:
            food_types_type_0_item = food_types_type_0_item_data.value
            json_food_types.append(food_types_type_0_item)

    else:
        json_food_types = food_types
    params["food_types"] = json_food_types

    json_sort_by: str | Unset = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sort_by"] = json_sort_by

    json_sort_order: str | Unset = UNSET
    if not isinstance(sort_order, Unset):
        json_sort_order = sort_order.value

    params["sort_order"] = json_sort_order

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    params["only_mine"] = only_mine

    params["only_favorites"] = only_favorites

    params["include_drafts"] = include_drafts

    params["boost_popular"] = boost_popular

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/recipes/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RecipeQueryResponse | None:
    if response.status_code == 200:
        response_200 = RecipeQueryResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | RecipeQueryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: None | str | Unset = UNSET,
    food_types: list[FoodType] | None | Unset = UNSET,
    sort_by: SortField | Unset = UNSET,
    sort_order: SortOrder | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: None | str | Unset = UNSET,
    only_mine: bool | Unset = False,
    only_favorites: bool | Unset = False,
    include_drafts: bool | Unset = True,
    boost_popular: bool | Unset = True,
) -> Response[HTTPValidationError | RecipeQueryResponse]:
    """List Recipes

     Unified GET endpoint for querying recipes.

    Args:
        query (None | str | Unset): Text search query
        food_types (list[FoodType] | None | Unset): Filter by food types
        sort_by (SortField | Unset): Available fields for sorting recipes.
        sort_order (SortOrder | Unset): Sort direction.
        limit (int | Unset): Page size Default: 20.
        cursor (None | str | Unset): Pagination cursor
        only_mine (bool | Unset): Only your recipes Default: False.
        only_favorites (bool | Unset): Only favorite recipes Default: False.
        include_drafts (bool | Unset): Include drafts Default: True.
        boost_popular (bool | Unset): Boost popular results Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecipeQueryResponse]
    """

    kwargs = _get_kwargs(
        query=query,
        food_types=food_types,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        cursor=cursor,
        only_mine=only_mine,
        only_favorites=only_favorites,
        include_drafts=include_drafts,
        boost_popular=boost_popular,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: None | str | Unset = UNSET,
    food_types: list[FoodType] | None | Unset = UNSET,
    sort_by: SortField | Unset = UNSET,
    sort_order: SortOrder | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: None | str | Unset = UNSET,
    only_mine: bool | Unset = False,
    only_favorites: bool | Unset = False,
    include_drafts: bool | Unset = True,
    boost_popular: bool | Unset = True,
) -> HTTPValidationError | RecipeQueryResponse | None:
    """List Recipes

     Unified GET endpoint for querying recipes.

    Args:
        query (None | str | Unset): Text search query
        food_types (list[FoodType] | None | Unset): Filter by food types
        sort_by (SortField | Unset): Available fields for sorting recipes.
        sort_order (SortOrder | Unset): Sort direction.
        limit (int | Unset): Page size Default: 20.
        cursor (None | str | Unset): Pagination cursor
        only_mine (bool | Unset): Only your recipes Default: False.
        only_favorites (bool | Unset): Only favorite recipes Default: False.
        include_drafts (bool | Unset): Include drafts Default: True.
        boost_popular (bool | Unset): Boost popular results Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecipeQueryResponse
    """

    return sync_detailed(
        client=client,
        query=query,
        food_types=food_types,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        cursor=cursor,
        only_mine=only_mine,
        only_favorites=only_favorites,
        include_drafts=include_drafts,
        boost_popular=boost_popular,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: None | str | Unset = UNSET,
    food_types: list[FoodType] | None | Unset = UNSET,
    sort_by: SortField | Unset = UNSET,
    sort_order: SortOrder | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: None | str | Unset = UNSET,
    only_mine: bool | Unset = False,
    only_favorites: bool | Unset = False,
    include_drafts: bool | Unset = True,
    boost_popular: bool | Unset = True,
) -> Response[HTTPValidationError | RecipeQueryResponse]:
    """List Recipes

     Unified GET endpoint for querying recipes.

    Args:
        query (None | str | Unset): Text search query
        food_types (list[FoodType] | None | Unset): Filter by food types
        sort_by (SortField | Unset): Available fields for sorting recipes.
        sort_order (SortOrder | Unset): Sort direction.
        limit (int | Unset): Page size Default: 20.
        cursor (None | str | Unset): Pagination cursor
        only_mine (bool | Unset): Only your recipes Default: False.
        only_favorites (bool | Unset): Only favorite recipes Default: False.
        include_drafts (bool | Unset): Include drafts Default: True.
        boost_popular (bool | Unset): Boost popular results Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecipeQueryResponse]
    """

    kwargs = _get_kwargs(
        query=query,
        food_types=food_types,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        cursor=cursor,
        only_mine=only_mine,
        only_favorites=only_favorites,
        include_drafts=include_drafts,
        boost_popular=boost_popular,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: None | str | Unset = UNSET,
    food_types: list[FoodType] | None | Unset = UNSET,
    sort_by: SortField | Unset = UNSET,
    sort_order: SortOrder | Unset = UNSET,
    limit: int | Unset = 20,
    cursor: None | str | Unset = UNSET,
    only_mine: bool | Unset = False,
    only_favorites: bool | Unset = False,
    include_drafts: bool | Unset = True,
    boost_popular: bool | Unset = True,
) -> HTTPValidationError | RecipeQueryResponse | None:
    """List Recipes

     Unified GET endpoint for querying recipes.

    Args:
        query (None | str | Unset): Text search query
        food_types (list[FoodType] | None | Unset): Filter by food types
        sort_by (SortField | Unset): Available fields for sorting recipes.
        sort_order (SortOrder | Unset): Sort direction.
        limit (int | Unset): Page size Default: 20.
        cursor (None | str | Unset): Pagination cursor
        only_mine (bool | Unset): Only your recipes Default: False.
        only_favorites (bool | Unset): Only favorite recipes Default: False.
        include_drafts (bool | Unset): Include drafts Default: True.
        boost_popular (bool | Unset): Boost popular results Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecipeQueryResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            food_types=food_types,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            cursor=cursor,
            only_mine=only_mine,
            only_favorites=only_favorites,
            include_drafts=include_drafts,
            boost_popular=boost_popular,
        )
    ).parsed
