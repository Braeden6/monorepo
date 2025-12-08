from recipe_api_client import AuthenticatedClient
from recipe_api_client.api.recipes import create_recipe_recipes_post
from recipe_api_client.models.food_type import FoodType
from recipe_api_client.models.ingredient_item import IngredientItem
from recipe_api_client.models.recipe_create import RecipeCreate
from recipe_api_client.models.recipe_read import RecipeRead


def create_test_recipe(
    client: AuthenticatedClient, title: str = "Test Recipe", description: str = "Test Description"
) -> RecipeRead:
    recipe_data = RecipeCreate(
        name=title,
        description=description,
        ingredients=[
            IngredientItem(name="Ingredient 1", amount="100", unit="g"),
            IngredientItem(name="Ingredient 2", amount="2", unit="cups"),
        ],
        instructions="Mix everything together.",
        food_type=FoodType.DINNER,
    )

    response = create_recipe_recipes_post.sync_detailed(client=client, body=recipe_data)
    assert response.status_code == 201
    assert isinstance(response.parsed, RecipeRead)
    return response.parsed
