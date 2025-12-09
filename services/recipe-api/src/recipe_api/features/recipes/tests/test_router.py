import uuid

import pytest

from recipe_api.features.recipes.tests.utils import create_test_recipe
from recipe_api_client import AuthenticatedClient
from recipe_api_client.api.recipes import (
    create_recipe_recipes_post,
    get_recipe_recipes_recipe_id_get,
    list_recipes_recipes_get,
    update_recipe_recipes_recipe_id_patch,
)
from recipe_api_client.models.food_type import FoodType
from recipe_api_client.models.ingredient_item import IngredientItem
from recipe_api_client.models.recipe_create import RecipeCreate
from recipe_api_client.models.recipe_read import RecipeRead
from recipe_api_client.models.recipe_status import RecipeStatus
from recipe_api_client.models.recipe_update import RecipeUpdate

# =============================================================================
# Authentication Tests
# =============================================================================


@pytest.mark.e2e
def test_create_recipe_without_auth(no_user_client: AuthenticatedClient) -> None:
    recipe_data = RecipeCreate(
        name="Unauthorized Recipe",
        description="Should fail",
        ingredients=[IngredientItem(name="Salt", amount="1", unit="tsp")],
        instructions="Mix it.",
        food_type=FoodType.DINNER,
    )
    response = create_recipe_recipes_post.sync_detailed(client=no_user_client, body=recipe_data)
    assert response.status_code == 401


@pytest.mark.e2e
def test_update_recipe_without_auth(
    user1_client: AuthenticatedClient,
    no_user_client: AuthenticatedClient,
) -> None:
    recipe = create_test_recipe(user1_client, title="Auth Test Recipe", description="Test")
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client, recipe_id=recipe.id, body=RecipeUpdate(status=RecipeStatus.PUBLISHED)
    )

    response = update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=no_user_client, recipe_id=recipe.id, body=RecipeUpdate(name="Hacked")
    )
    assert response.status_code == 401


@pytest.mark.e2e
def test_get_published_recipe_without_auth(
    user1_client: AuthenticatedClient,
    no_user_client: AuthenticatedClient,
) -> None:
    recipe = create_test_recipe(user1_client, title="Public Recipe", description="Anyone can see")
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client, recipe_id=recipe.id, body=RecipeUpdate(status=RecipeStatus.PUBLISHED)
    )

    response = get_recipe_recipes_recipe_id_get.sync_detailed(client=no_user_client, recipe_id=recipe.id)
    assert response.status_code == 200
    assert isinstance(response.parsed, RecipeRead)
    assert response.parsed.id == recipe.id


@pytest.mark.e2e
def test_get_draft_recipe_without_auth(
    user1_client: AuthenticatedClient,
    no_user_client: AuthenticatedClient,
) -> None:
    recipe = create_test_recipe(user1_client, title="Draft Recipe", description="Private")

    response = get_recipe_recipes_recipe_id_get.sync_detailed(client=no_user_client, recipe_id=recipe.id)
    assert response.status_code == 404


@pytest.mark.e2e
def test_list_recipes_without_auth_shows_only_published(
    user1_client: AuthenticatedClient,
    no_user_client: AuthenticatedClient,
) -> None:
    draft_recipe = create_test_recipe(user1_client, title="Draft Recipe", description="Private")

    published_recipe = create_test_recipe(user1_client, title="Published Recipe", description="Public")
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client,
        recipe_id=published_recipe.id,
        body=RecipeUpdate(status=RecipeStatus.PUBLISHED),
    )

    response = list_recipes_recipes_get.sync_detailed(client=no_user_client)
    assert response.status_code == 200
    recipes = response.parsed
    assert isinstance(recipes, list)
    assert any(r.id == published_recipe.id for r in recipes)
    assert not any(r.id == draft_recipe.id for r in recipes)


# =============================================================================
# Input Validation Tests
# =============================================================================


@pytest.mark.e2e
def test_create_recipe_with_empty_name(user1_client: AuthenticatedClient) -> None:
    recipe_data = RecipeCreate(
        name="",
        description="Valid description",
        ingredients=[IngredientItem(name="Salt", amount="1", unit="tsp")],
        instructions="Valid instructions",
        food_type=FoodType.DINNER,
    )
    response = create_recipe_recipes_post.sync_detailed(client=user1_client, body=recipe_data)
    assert response.status_code == 422


@pytest.mark.e2e
def test_create_recipe_with_empty_ingredients(user1_client: AuthenticatedClient) -> None:
    recipe_data = RecipeCreate(
        name="Valid Name",
        description="Valid description",
        ingredients=[],
        instructions="Valid instructions",
        food_type=FoodType.DINNER,
    )
    response = create_recipe_recipes_post.sync_detailed(client=user1_client, body=recipe_data)
    assert response.status_code == 422


# =============================================================================
# Edge Cases & Error Handling
# =============================================================================


@pytest.mark.e2e
def test_get_nonexistent_recipe(user1_client: AuthenticatedClient) -> None:
    fake_id = uuid.uuid4()
    response = get_recipe_recipes_recipe_id_get.sync_detailed(client=user1_client, recipe_id=fake_id)
    assert response.status_code == 404


@pytest.mark.e2e
def test_update_nonexistent_recipe(user1_client: AuthenticatedClient) -> None:
    fake_id = uuid.uuid4()
    response = update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client, recipe_id=fake_id, body=RecipeUpdate(name="New Name")
    )
    assert response.status_code == 404


# =============================================================================
# Pagination Tests
# =============================================================================


@pytest.mark.e2e
def test_list_recipes_pagination(user1_client: AuthenticatedClient) -> None:
    recipes_created = []
    for i in range(3):
        recipe = create_test_recipe(user1_client, title=f"Pagination Test {i}", description=f"Recipe {i}")
        update_recipe_recipes_recipe_id_patch.sync_detailed(
            client=user1_client, recipe_id=recipe.id, body=RecipeUpdate(status=RecipeStatus.PUBLISHED)
        )
        recipes_created.append(recipe)

    response = list_recipes_recipes_get.sync_detailed(client=user1_client, skip=0, limit=2)
    assert response.status_code == 200
    recipes = response.parsed
    assert isinstance(recipes, list)
    assert len(recipes) <= 2

    response = list_recipes_recipes_get.sync_detailed(client=user1_client, skip=2, limit=2)
    assert response.status_code == 200
    recipes = response.parsed
    assert isinstance(recipes, list)


# =============================================================================
# Data Integrity Tests
# =============================================================================


@pytest.mark.e2e
def test_create_recipe_returns_correct_data(user1_client: AuthenticatedClient) -> None:
    recipe_data = RecipeCreate(
        name="Complete Recipe",
        description="Full description",
        ingredients=[
            IngredientItem(name="Flour", amount="2", unit="cups"),
            IngredientItem(name="Sugar", amount="1", unit="cup"),
        ],
        instructions="Mix and bake.",
        food_type=FoodType.DESSERT,
    )
    response = create_recipe_recipes_post.sync_detailed(client=user1_client, body=recipe_data)
    assert response.status_code == 201
    assert isinstance(response.parsed, RecipeRead)

    recipe = response.parsed
    assert recipe.name == "Complete Recipe"
    assert recipe.description == "Full description"
    assert recipe.instructions == "Mix and bake."
    assert recipe.food_type == FoodType.DESSERT
    assert recipe.status == RecipeStatus.DRAFT
    assert len(recipe.ingredients) == 2


@pytest.mark.e2e
def test_update_recipe_updates_only_specified_fields(user1_client: AuthenticatedClient) -> None:
    recipe = create_test_recipe(user1_client, title="Original Name", description="Original Description")
    original_description = recipe.description

    response = update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client, recipe_id=recipe.id, body=RecipeUpdate(name="Updated Name")
    )
    assert response.status_code == 200
    assert isinstance(response.parsed, RecipeRead)

    updated_recipe = response.parsed
    assert updated_recipe.name == "Updated Name"
    assert updated_recipe.description == original_description


# =============================================================================
# Visibility & Permissions Tests (Split from original)
# =============================================================================


@pytest.mark.e2e
def test_owner_can_see_own_draft_recipe(user1_client: AuthenticatedClient) -> None:
    recipe = create_test_recipe(user1_client, title="My Draft", description="Draft recipe")

    response = list_recipes_recipes_get.sync_detailed(client=user1_client)
    assert response.status_code == 200
    recipes = response.parsed
    assert isinstance(recipes, list)
    assert any(r.id == recipe.id for r in recipes)

    response = get_recipe_recipes_recipe_id_get.sync_detailed(client=user1_client, recipe_id=recipe.id)
    assert response.status_code == 200
    assert isinstance(response.parsed, RecipeRead)
    assert response.parsed.id == recipe.id


@pytest.mark.e2e
def test_other_user_cannot_see_draft_recipe(
    user1_client: AuthenticatedClient,
    user2_client: AuthenticatedClient,
) -> None:
    recipe = create_test_recipe(user1_client, title="User1 Draft", description="Private")

    response = list_recipes_recipes_get.sync_detailed(client=user2_client)
    assert response.status_code == 200
    recipes = response.parsed
    assert isinstance(recipes, list)
    assert not any(r.id == recipe.id for r in recipes)

    response = get_recipe_recipes_recipe_id_get.sync_detailed(client=user2_client, recipe_id=recipe.id)
    assert response.status_code == 404


@pytest.mark.e2e
def test_other_user_cannot_update_draft_recipe(
    user1_client: AuthenticatedClient,
    user2_client: AuthenticatedClient,
) -> None:
    recipe = create_test_recipe(user1_client, title="Protected Recipe", description="No modifications")

    response = update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user2_client, recipe_id=recipe.id, body=RecipeUpdate(name="Hacked Name")
    )
    assert response.status_code in (403, 404)


@pytest.mark.e2e
def test_published_recipe_visible_to_all(
    user1_client: AuthenticatedClient,
    user2_client: AuthenticatedClient,
) -> None:
    recipe = create_test_recipe(user1_client, title="Public Recipe", description="Everyone can see")
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client, recipe_id=recipe.id, body=RecipeUpdate(status=RecipeStatus.PUBLISHED)
    )

    response = list_recipes_recipes_get.sync_detailed(client=user2_client)
    assert response.status_code == 200
    recipes = response.parsed
    assert isinstance(recipes, list)
    assert any(r.id == recipe.id for r in recipes)

    response = get_recipe_recipes_recipe_id_get.sync_detailed(client=user2_client, recipe_id=recipe.id)
    assert response.status_code == 200
    assert isinstance(response.parsed, RecipeRead)


@pytest.mark.e2e
def test_other_user_cannot_update_published_recipe(
    user1_client: AuthenticatedClient,
    user2_client: AuthenticatedClient,
) -> None:
    recipe = create_test_recipe(user1_client, title="Published Protected", description="Still protected")
    update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client, recipe_id=recipe.id, body=RecipeUpdate(status=RecipeStatus.PUBLISHED)
    )

    response = update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user2_client, recipe_id=recipe.id, body=RecipeUpdate(name="Attempted Update")
    )
    assert response.status_code in (403, 404)


@pytest.mark.e2e
def test_owner_can_publish_recipe(user1_client: AuthenticatedClient) -> None:
    recipe = create_test_recipe(user1_client, title="To Be Published", description="Going public")

    response = update_recipe_recipes_recipe_id_patch.sync_detailed(
        client=user1_client, recipe_id=recipe.id, body=RecipeUpdate(status=RecipeStatus.PUBLISHED)
    )
    assert response.status_code == 200
    assert isinstance(response.parsed, RecipeRead)
    assert response.parsed.status == RecipeStatus.PUBLISHED
