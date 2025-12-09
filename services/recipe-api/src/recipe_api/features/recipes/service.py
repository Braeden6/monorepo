import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlmodel import Session, select

from recipe_api.features.recipes.schemas import RecipeCreate, RecipeUpdate
from recipe_api.shared.models.recipe import (
    FoodType,
    GenerationStatus,
    GenerationStep,
    Recipe,
    RecipeStatus,
)
from recipe_api.shared.services.embeddings import EmbeddingService


class RecipeService:
    def __init__(self, session: Session, embedding_service: EmbeddingService):
        self.session = session
        self.embedding_service = embedding_service

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

    def get_recipe(self, recipe_id: uuid.UUID, user_id: str | None = None) -> Recipe:
        recipe = self.session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found",
            )

        is_draft = recipe.status == RecipeStatus.DRAFT
        is_not_owner = user_id is None or recipe.created_by != user_id
        if is_draft and is_not_owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found",
            )

        return recipe

    def list_recipes(
        self, skip: int = 0, limit: int = 20, user_id: str | None = None
    ) -> list[Recipe]:
        visibility_filter = Recipe.status == RecipeStatus.PUBLISHED
        if user_id is not None:
            visibility_filter = or_(
                Recipe.status == RecipeStatus.PUBLISHED,  # type: ignore[arg-type]
                Recipe.created_by == user_id,  # type: ignore[arg-type]
            )

        recipes = self.session.exec(
            select(Recipe)
            .where(visibility_filter)
            .order_by(Recipe.created_at.desc())  # type: ignore[union-attr]
            .offset(skip)
            .limit(limit)
        ).all()
        return list(recipes)

    def update_recipe(
        self, recipe_id: uuid.UUID, recipe_update: RecipeUpdate, user_id: str
    ) -> Recipe:
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

        recipe.updated_at = datetime.utcnow()

        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)

        return recipe

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

    def update_generation_status(
        self,
        recipe_id: uuid.UUID,
        step: GenerationStep | None = None,
        status: GenerationStatus | None = None,
        error: str | None = None,
    ) -> None:
        recipe = self.get_recipe(recipe_id)
        if step:
            recipe.generation_step = step
        if status:
            recipe.generation_status = status
        if error:
            recipe.generation_error = error
        recipe.updated_at = datetime.utcnow()
        self.session.add(recipe)
        self.session.commit()

    def finalize_generated_recipe(
        self,
        recipe_id: uuid.UUID,
        name: str,
        description: str,
        ingredients: list[dict],
        instructions: str | list[str],
        food_type_str: str | None,
    ) -> Recipe:
        recipe = self.get_recipe(recipe_id)

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
        recipe.updated_at = datetime.utcnow()

        self.session.add(recipe)
        self.session.commit()
        self.session.refresh(recipe)
        return recipe
