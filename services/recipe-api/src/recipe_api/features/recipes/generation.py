import uuid
from datetime import UTC, datetime

from sqlmodel import Session

from recipe_api.shared.models.recipe import (
    FoodType,
    GenerationStatus,
    GenerationStep,
    Recipe,
)
from recipe_api.shared.services.embeddings import EmbeddingService


class RecipeGenerationHandler:
    def __init__(self, session: Session, embedding_service: EmbeddingService):
        self.session = session
        self.embedding_service = embedding_service

    def create_placeholder(
        self,
        user_id: str,
        workflow_id: str,
        prompt: str,
    ) -> Recipe:
        recipe = Recipe(
            id=uuid.uuid4(),
            created_by=user_id,
            is_generated=True,
            workflow_id=workflow_id,
            generation_step=GenerationStep.QUEUED,
            generation_status=GenerationStatus.PENDING,
            generation_prompt=prompt,
        )
        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        return recipe

    def update_status(
        self,
        recipe: Recipe,
        step: GenerationStep | None = None,
        status: GenerationStatus | None = None,
        error: str | None = None,
    ) -> None:
        if step:
            recipe.generation_step = step
        if status:
            recipe.generation_status = status
        if error:
            recipe.generation_error = error
        recipe.updated_at = datetime.now(UTC)
        self.session.add(recipe)
        self.session.commit()

    def finalize_recipe(
        self,
        recipe: Recipe,
        name: str,
        description: str,
        ingredients: list[dict],
        instructions: str | list[str],
        food_type_str: str | None,
    ) -> Recipe:
        food_type = None
        if food_type_str:
            import contextlib

            with contextlib.suppress(ValueError):
                food_type = FoodType(food_type_str)

        if isinstance(instructions, list):
            instructions = "\n".join(instructions)

        description_embedding = self.embedding_service.encode(description)
        ingredient_text = " ".join([ing.get("name", "") for ing in ingredients])
        ingredient_embedding = self.embedding_service.encode(ingredient_text)

        recipe.name = name
        recipe.description = description
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.food_type = food_type
        recipe.description_embedding = description_embedding
        recipe.ingredient_embedding = ingredient_embedding

        recipe.generation_step = GenerationStep.COMPLETED
        recipe.generation_status = GenerationStatus.COMPLETED
        recipe.updated_at = datetime.now(UTC)

        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        return recipe
