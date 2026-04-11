"""Tests for the unified search and query functionality in the recipes feature.
"""

import pytest

from recipe_api.features.recipes.tests.utils import create_test_recipe
from recipe_api_client import AuthenticatedClient
from recipe_api_client.api.recipes import (
    list_recipes_recipes_get,
    query_recipes_recipes_query_post,
    update_recipe_recipes_recipe_id_patch,
)
from recipe_api_client.models.food_type import FoodType
from recipe_api_client.models.recipe_query_request import RecipeQueryRequest
from recipe_api_client.models.recipe_query_response import RecipeQueryResponse
from recipe_api_client.models.recipe_status import RecipeStatus
from recipe_api_client.models.recipe_update import RecipeUpdate


@pytest.mark.e2e
def test_text_search_returns_relevant_results(user1_client: AuthenticatedClient) -> None:
    """Test that text search returns semantically relevant results."""
    chocolate_recipe = create_test_recipe(
        user1_client,
        title="Triple Chocolate Brownies",
        description="Rich and fudgy brownies with dark chocolate.",
        food_type=FoodType.DESSERT,
    )
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client,
        recipe_id=chocolate_recipe.id,
        body=RecipeUpdate(status=RecipeStatus.PUBLISHED),
    )

    request = RecipeQueryRequest(query="chocolate dessert")
    response = query_recipes_recipes_query_post.sync_detailed(
        client=user1_client, body=request
    )
    assert response.status_code == 200
    assert isinstance(response.parsed, RecipeQueryResponse)
    assert any(r.id == chocolate_recipe.id for r in response.parsed.results)


@pytest.mark.e2e
def test_filter_by_food_type(user1_client: AuthenticatedClient) -> None:
    """Test filtering by food type."""
    dessert = create_test_recipe(
        user1_client,
        title="Cake",
        food_type=FoodType.DESSERT,
    )
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client,
        recipe_id=dessert.id,
        body=RecipeUpdate(status=RecipeStatus.PUBLISHED),
    )

    dinner = create_test_recipe(
        user1_client,
        title="Steak",
        food_type=FoodType.DINNER,
    )
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client,
        recipe_id=dinner.id,
        body=RecipeUpdate(status=RecipeStatus.PUBLISHED),
    )

    request = RecipeQueryRequest(food_types=[FoodType.DESSERT])
    response = query_recipes_recipes_query_post.sync_detailed(
        client=user1_client, body=request
    )
    assert response.status_code == 200
    result_ids = [r.id for r in response.parsed.results]
    assert dessert.id in result_ids
    assert dinner.id not in result_ids


@pytest.mark.e2e
def test_only_mine_filter(
    user1_client: AuthenticatedClient,
    user2_client: AuthenticatedClient,
) -> None:
    """Test filtering for only the user's recipes."""
    user1_recipe = create_test_recipe(user1_client, title="User 1 Recipe")
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client,
        recipe_id=user1_recipe.id,
        body=RecipeUpdate(status=RecipeStatus.PUBLISHED),
    )

    user2_recipe = create_test_recipe(user2_client, title="User 2 Recipe")
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user2_client,
        recipe_id=user2_recipe.id,
        body=RecipeUpdate(status=RecipeStatus.PUBLISHED),
    )

    request = RecipeQueryRequest(only_mine=True)
    response = query_recipes_recipes_query_post.sync_detailed(
        client=user1_client, body=request
    )
    assert response.status_code == 200
    result_ids = [r.id for r in response.parsed.results]
    assert user1_recipe.id in result_ids
    assert user2_recipe.id not in result_ids


@pytest.mark.e2e
def test_cursor_pagination(user1_client: AuthenticatedClient) -> None:
    """Test that cursor pagination works for navigating results."""
    created_ids = []
    for i in range(3):
        recipe = create_test_recipe(user1_client, title=f"Paginated {i}")
        update_recipe_recipes_recipe_id_patch.sync_detailed(
            client=user1_client,
            recipe_id=recipe.id,
            body=RecipeUpdate(status=RecipeStatus.PUBLISHED),
        )
        created_ids.append(recipe.id)

    # First page
    request = RecipeQueryRequest(limit=1)
    response = query_recipes_recipes_query_post.sync_detailed(
        client=user1_client, body=request
    )
    assert response.status_code == 200
    assert len(response.parsed.results) == 1
    assert response.parsed.pagination.has_next is True

    # Second page
    cursor = response.parsed.pagination.next_cursor
    request2 = RecipeQueryRequest(limit=1, cursor=cursor)
    response2 = query_recipes_recipes_query_post.sync_detailed(
        client=user1_client, body=request2
    )
    assert response2.status_code == 200
    assert len(response2.parsed.results) == 1
    assert response2.parsed.results[0].id != response.parsed.results[0].id


@pytest.mark.e2e
def test_get_endpoint_with_query_params(user1_client: AuthenticatedClient) -> None:
    """Test the unified GET endpoint with query parameters."""
    recipe = create_test_recipe(user1_client, title="GET Param Test")
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client,
        recipe_id=recipe.id,
        body=RecipeUpdate(status=RecipeStatus.PUBLISHED),
    )

    response = list_recipes_recipes_get.sync_detailed(
        client=user1_client,
        query="GET Param Test",
    )
    assert response.status_code == 200
    assert isinstance(response.parsed, RecipeQueryResponse)
    assert any(r.id == recipe.id for r in response.parsed.results)
