import pytest

from recipe_api.features.recipes.tests.utils import create_test_recipe
from recipe_api_client import AuthenticatedClient
from recipe_api_client.api.users import (
    get_my_favorites_users_me_favorites_get,
    toggle_favorite_users_recipes_recipe_id_favorite_post,
)


@pytest.mark.e2e
def test_favorite_recipe(api_client: AuthenticatedClient):
    recipe = create_test_recipe(api_client, title="Fav Recipe", description="To be favored")
    recipe_id = recipe.id

    # favorite recipe
    response = toggle_favorite_users_recipes_recipe_id_favorite_post.sync_detailed(
        client=api_client, recipe_id=recipe_id
    )
    assert response.status_code == 200
    assert response.parsed is not None
    assert response.parsed["is_favorite"] is True

    # check favorite recipe in list
    response = get_my_favorites_users_me_favorites_get.sync_detailed(client=api_client)
    assert response.status_code == 200
    favorites = response.parsed
    assert favorites is not None
    assert any(f.id == recipe_id for f in favorites)

    # unfavorite
    response = toggle_favorite_users_recipes_recipe_id_favorite_post.sync_detailed(
        client=api_client, recipe_id=recipe_id
    )
    assert response.status_code == 200
    assert response.parsed is not None
    assert response.parsed["is_favorite"] is False

    # check not in favorites
    response = get_my_favorites_users_me_favorites_get.sync_detailed(client=api_client)
    assert response.status_code == 200
    favorites = response.parsed
    assert favorites is not None
    assert not any(f.id == recipe_id for f in favorites)
