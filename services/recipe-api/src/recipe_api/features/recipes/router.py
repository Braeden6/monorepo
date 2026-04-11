import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from recipe_api.features.recipes.schemas import (
    RecipeCreate,
    RecipeQueryRequest,
    RecipeQueryResponse,
    RecipeRead,
    RecipeUpdate,
    SortField,
    SortOrder,
)
from recipe_api.features.recipes.service import RecipeService
from recipe_api.shared.deps import CurrentUserDep, OptionalUserDep, SessionDep
from recipe_api.shared.models.recipe import FoodType, Recipe
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


@router.post("/query", response_model=RecipeQueryResponse)
def query_recipes(
    request: RecipeQueryRequest,
    service: Annotated[RecipeService, Depends(get_recipe_service)],
    current_user: OptionalUserDep = None,
) -> RecipeQueryResponse:
    """Unified endpoint for searching and filtering recipes."""

    return service.query_recipes(request, current_user)


@router.get("/", response_model=RecipeQueryResponse)
def list_recipes(
    service: Annotated[RecipeService, Depends(get_recipe_service)],
    current_user: OptionalUserDep = None,
    query: Annotated[str | None, Query(description="Text search query")] = None,
    food_types: Annotated[list[FoodType] | None, Query(description="Filter by food types")] = None,
    sort_by: Annotated[SortField, Query(description="Sort field")] = SortField.CREATED_AT,
    sort_order: Annotated[SortOrder, Query(description="Sort direction")] = SortOrder.DESC,
    limit: Annotated[int, Query(ge=1, le=100, description="Page size")] = 20,
    cursor: Annotated[str | None, Query(description="Pagination cursor")] = None,
    only_mine: Annotated[bool, Query(description="Only your recipes")] = False,
    only_favorites: Annotated[bool, Query(description="Only favorite recipes")] = False,
    include_drafts: Annotated[bool, Query(description="Include drafts")] = True,
    boost_popular: Annotated[bool, Query(description="Boost popular results")] = True,
) -> RecipeQueryResponse:
    """Unified GET endpoint for querying recipes."""
    request = RecipeQueryRequest(
        query=query,
        food_types=food_types,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        cursor=cursor,
        only_mine=only_mine,
        only_favorites=only_favorites,
        include_drafts=include_drafts,
        boost_popular=boost_popular,
    )
    return service.query_recipes(request, current_user)


@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(
    recipe_id: uuid.UUID,
    service: Annotated[RecipeService, Depends(get_recipe_service)],
    current_user: OptionalUserDep = None,
) -> RecipeRead:
    return service.get_recipe_read(recipe_id, current_user)


@router.patch("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: uuid.UUID,
    recipe_update: RecipeUpdate,
    current_user: CurrentUserDep,
    service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> RecipeRead:
    return service.update_recipe(recipe_id, recipe_update, current_user)

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: uuid.UUID,
    current_user: CurrentUserDep,
    service: Annotated[RecipeService, Depends(get_recipe_service)],
) -> None:
    service.delete_recipe(recipe_id, current_user)
