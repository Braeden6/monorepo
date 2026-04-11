import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlmodel import Session, select

from recipe_api.features.recipes.generation import RecipeGenerationHandler
from recipe_api.features.recipes.query import RecipeQueryHandler
from recipe_api.features.recipes.schemas import (
    RecipeCreate,
    RecipeQueryRequest,
    RecipeQueryResponse,
    RecipeRead,
    RecipeUpdate,
)
from recipe_api.shared.models.recipe import (
    GenerationStatus,
    GenerationStep,
    Recipe,
    RecipeStatus,
)
from recipe_api.shared.models.user_interaction import UserRecipeInteraction
from recipe_api.shared.services.embeddings import EmbeddingService


class RecipeService:
    def __init__(self, session: Session, embedding_service: EmbeddingService):
        self.session = session
        self.embedding_service = embedding_service
        self.query = RecipeQueryHandler(session, embedding_service)
        self.generation = RecipeGenerationHandler(session, embedding_service)

    def create_recipe(self, recipe_create: RecipeCreate, user_id: str) -> Recipe:
        description_embedding = self.embedding_service.encode(recipe_create.description)
        ingredient_text = " ".join([ing.name for ing in recipe_create.ingredients])
        ingredient_embedding = self.embedding_service.encode(ingredient_text)

        db_recipe = Recipe(
            name=recipe_create.name,
            description=recipe_create.description,
            ingredients=[ing.model_dump() for ing in recipe_create.ingredients],
            instructions=recipe_create.instructions,
            food_type=recipe_create.food_type,
            status=recipe_create.status,
            is_generated=False,
            created_by=user_id,
            description_embedding=description_embedding,
            ingredient_embedding=ingredient_embedding,
        )

        self.session.add(db_recipe)
        self.session.commit()
        self.session.refresh(db_recipe)

        return db_recipe

    def get_recipe(
        self,
        recipe_id: uuid.UUID,
        user_id: str | None = None,
        check_visibility: bool = True,
    ) -> Recipe:
        recipe = self.session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found",
            )

        if not check_visibility:
            return recipe

        is_draft = recipe.status == RecipeStatus.DRAFT
        is_not_owner = user_id is None or recipe.created_by != user_id
        if is_draft and is_not_owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found",
            )

        return recipe

    def get_recipe_read(
        self,
        recipe_id: uuid.UUID,
        user_id: str | None = None,
    ) -> RecipeRead:
        recipe = self.get_recipe(recipe_id, user_id)
        recipe_read = RecipeRead.model_validate(recipe)

        if user_id:
            interaction = self.session.exec(
                select(UserRecipeInteraction).where(
                    UserRecipeInteraction.user_id == user_id,
                    UserRecipeInteraction.recipe_id == recipe_id,
                )
            ).first()
            if interaction:
                recipe_read.is_liked = interaction.is_liked
                recipe_read.is_favorited = interaction.is_favorite

        return recipe_read

    def query_recipes(
        self,
        request: RecipeQueryRequest,
        user_id: str | None = None,
    ) -> RecipeQueryResponse:
        """Proxies query requests to the query handler."""
        return self.query.query_recipes(request, user_id)

    def update_recipe(
        self, recipe_id: uuid.UUID, recipe_update: RecipeUpdate, user_id: str
    ) -> RecipeRead:
        recipe = self.get_recipe(recipe_id, user_id)

        if recipe.created_by != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own recipes",
            )

        update_data = recipe_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(recipe, field, value)

        if "description" in update_data:
            recipe.description_embedding = self.embedding_service.encode(recipe.description)

        if "ingredients" in update_data:
            ingredient_text = " ".join([ing.get("name", "") for ing in recipe.ingredients])
            recipe.ingredient_embedding = self.embedding_service.encode(ingredient_text)

        if (
            recipe.status == RecipeStatus.PUBLISHED
            and (recipe.description_embedding is None or recipe.ingredient_embedding is None)
        ):
            if recipe.description_embedding is None:
                recipe.description_embedding = self.embedding_service.encode(recipe.description)

            if recipe.ingredient_embedding is None:
                ingredient_text = " ".join([ing.get("name", "") for ing in recipe.ingredients])
                recipe.ingredient_embedding = self.embedding_service.encode(ingredient_text)

        recipe.updated_at = datetime.now(UTC)

        self.session.add(recipe)
        self.session.commit()

        return self.get_recipe_read(recipe.id, user_id)

    def delete_recipe(self, recipe_id: uuid.UUID, user_id: str) -> None:
        recipe = self.get_recipe(recipe_id, user_id)

        if recipe.created_by != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own recipes",
            )

        from recipe_api.shared.models.generation_log import GenerationLog

        logs = self.session.exec(
            select(GenerationLog).where(GenerationLog.recipe_id == recipe_id)
        ).all()
        for log in logs:
            self.session.delete(log)

        interactions = self.session.exec(
            select(UserRecipeInteraction).where(UserRecipeInteraction.recipe_id == recipe_id)
        ).all()
        for interaction in interactions:
            self.session.delete(interaction)

        self.session.delete(recipe)
        self.session.commit()

    def create_placeholder(
        self,
        user_id: str,
        workflow_id: str,
        prompt: str,
    ) -> Recipe:
        return self.generation.create_placeholder(user_id, workflow_id, prompt)

    def update_generation_status(
        self,
        recipe_id: uuid.UUID,
        step: GenerationStep | None = None,
        status: GenerationStatus | None = None,
        error: str | None = None,
    ) -> None:
        recipe = self.get_recipe(recipe_id, check_visibility=False)
        self.generation.update_status(recipe, step, status, error)

    def finalize_generated_recipe(
        self,
        recipe_id: uuid.UUID,
        name: str,
        description: str,
        ingredients: list[dict],
        instructions: str | list[str],
        food_type_str: str | None,
    ) -> Recipe:
        recipe = self.get_recipe(recipe_id, check_visibility=False)
        return self.generation.finalize_recipe(
            recipe, name, description, ingredients, instructions, food_type_str
        )
