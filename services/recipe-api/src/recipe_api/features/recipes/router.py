import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from recipe_api.features.recipes.schemas import RecipeCreate, RecipeRead, RecipeUpdate
from recipe_api.features.recipes.service import RecipeService
from recipe_api.shared.deps import CurrentUserDep, SessionDep
from recipe_api.shared.models.recipe import Recipe
from recipe_api.shared.services.embeddings import EmbeddingService, get_embedding_service

router = APIRouter(prefix="/recipes", tags=["recipes"])


def get_recipe_service(
    session: SessionDep,
    embedding_service: Annotated[EmbeddingService, Depends(get_embedding_service)],
) -> RecipeService:
    return RecipeService(session, embedding_service)


@router.post("/", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe: RecipeCreate,
    current_user: CurrentUserDep,
    service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> Recipe:
    return service.create_recipe(recipe, current_user)


@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(
    recipe_id: uuid.UUID,
    service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> Recipe:
    return service.get_recipe(recipe_id)


@router.get("/", response_model=list[RecipeRead])
def list_recipes(
    service: Annotated[RecipeService, Depends(get_recipe_service)],
    skip: int = 0,
    limit: int = 20,
) -> list[Recipe]:
    return service.list_recipes(skip, limit)


@router.patch("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: uuid.UUID,
    recipe_update: RecipeUpdate,
    current_user: CurrentUserDep,
    service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> Recipe:
    return service.update_recipe(recipe_id, recipe_update, current_user)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: uuid.UUID,
    current_user: CurrentUserDep,
    service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> None:
    service.delete_recipe(recipe_id, current_user)
