import json
from unittest.mock import MagicMock

from sqlmodel import Session, SQLModel, create_engine

from recipe_api.features.recipes.schemas import RecipeCreate, RecipeUpdate
from recipe_api.features.recipes.service import RecipeService
from recipe_api.features.search.service import SearchService
from recipe_api.shared.models.recipe import FoodType, Recipe, RecipeStatus
from recipe_api.shared.schemas.common import IngredientItem
from recipe_api.shared.services.embeddings import EmbeddingService
from recipe_api.shared.services.llm import LLMService

# Setup in-memory DB
engine = create_engine("sqlite:///:memory:")
SQLModel.metadata.create_all(engine)

def test_publish_flow():
    # Mock services
    mock_embedding_service = MagicMock(spec=EmbeddingService)
    mock_embedding_service.encode.return_value = [0.1] * 384

    mock_llm_service = MagicMock(spec=LLMService)
    mock_llm_service.generate.return_value = json.dumps({
        "recipes": [{
            "name": "Gen Recipe",
            "description": "Gen Desc",
            "ingredients": [{"name": "ing", "amount": "1", "unit": "cup"}],
            "instructions": "Step 1",
            "food_type": "dinner"
        }]
    })

    recipe_service = RecipeService(Session(engine), mock_embedding_service)
    search_service = SearchService(mock_embedding_service, mock_llm_service)

    with Session(engine) as session:
        # 1. Test Manual Creation
        print("Testing Manual Creation...")
        manual_create = RecipeCreate(
            name="Manual Recipe",
            description="Manual Desc",
            ingredients=[IngredientItem(name="ing", amount="1", unit="cup")],
            instructions="Step 1",
            food_type=FoodType.BREAKFAST
        )
        # Manually set status to GENERATED to verify it's ignored/overwritten
        # Note: Pydantic model doesn't have status field anymore, so we can't even pass it easily
        # But let's verify the service enforces it.

        manual_recipe = recipe_service.create_recipe(manual_create, "user1")
        assert manual_recipe.status == RecipeStatus.PUBLISHED
        assert manual_recipe.is_generated is False
        assert manual_recipe.food_type == FoodType.BREAKFAST
        assert manual_recipe.description_embedding is not None
        print("Manual Creation Verified")

        # 2. Test Generation
        print("Testing Generation...")
        generated_recipes = search_service.generate_recipe(
            session=session,
            prompt="test",
            user_id="user1"
        )
        gen_recipe = generated_recipes[0]
        # Reload from DB to check fields
        db_gen_recipe = session.get(Recipe, gen_recipe.id)
        assert db_gen_recipe.status == RecipeStatus.DRAFT
        assert db_gen_recipe.is_generated is True
        assert db_gen_recipe.description_embedding is None
        print("Generation Verified")

        # 3. Test Publishing
        print("Testing Publishing...")
        # Update status to PUBLISHED
        update_data = RecipeUpdate(status=RecipeStatus.PUBLISHED)

        # Re-instantiate service with fresh session for update
        recipe_service.session = session

        published_recipe = recipe_service.update_recipe(
            recipe_id=db_gen_recipe.id,
            recipe_update=update_data,
            user_id="user1"
        )

        assert published_recipe.status == RecipeStatus.PUBLISHED
        assert published_recipe.is_generated is True # Should still be true
        assert published_recipe.description_embedding is not None # Should be generated
        print("Publishing Verified")

if __name__ == "__main__":
    test_publish_flow()
