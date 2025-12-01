import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlmodel import Session, select

from recipe_api.features.recipes.schemas import RecipeRead
from recipe_api.shared.models.recipe import Recipe
from recipe_api.shared.models.user_interaction import UserRecipeInteraction


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def toggle_favorite(self, recipe_id: uuid.UUID, user_id: str) -> dict[str, bool]:
        recipe = self.session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found",
            )
        interaction = self.session.exec(
            select(UserRecipeInteraction).where(
                UserRecipeInteraction.user_id == user_id,
                UserRecipeInteraction.recipe_id == recipe_id,
            )
        ).first()

        if not interaction:
            interaction = UserRecipeInteraction(
                user_id=user_id,
                recipe_id=recipe_id,
                is_favorite=True,
            )
            recipe.favorite_count += 1
        else:
            interaction.is_favorite = not interaction.is_favorite
            interaction.updated_at = datetime.utcnow()
            recipe.favorite_count += 1 if interaction.is_favorite else -1

        self.session.add(interaction)
        self.session.add(recipe)
        self.session.commit()

        return {"is_favorite": interaction.is_favorite}

    def toggle_like(self, recipe_id: uuid.UUID, user_id: str) -> dict[str, bool]:
        recipe = self.session.get(Recipe, recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found",
            )

        interaction = self.session.exec(
            select(UserRecipeInteraction).where(
                UserRecipeInteraction.user_id == user_id,
                UserRecipeInteraction.recipe_id == recipe_id,
            )
        ).first()

        if not interaction:
            interaction = UserRecipeInteraction(
                user_id=user_id,
                recipe_id=recipe_id,
                is_liked=True,
            )
            recipe.like_count += 1
        else:
            interaction.is_liked = not interaction.is_liked
            interaction.updated_at = datetime.utcnow()
            recipe.like_count += 1 if interaction.is_liked else -1

        self.session.add(interaction)
        self.session.add(recipe)
        self.session.commit()

        return {"is_liked": interaction.is_liked}

    def get_my_favorites(self, user_id: str) -> list[RecipeRead]:
        statement = (
            select(Recipe)
            .join(UserRecipeInteraction)
            .where(
                UserRecipeInteraction.user_id == user_id,
                UserRecipeInteraction.is_favorite == True,  # noqa: E712
            )
        )
        recipes = self.session.exec(statement).all()

        return [
            RecipeRead.model_validate(recipe, from_attributes=True)
            for recipe in recipes
        ]
