
from typing import Annotated

from fastapi import APIRouter, Depends

from recipe_api.features.recipes.schemas import RecipeRead
from recipe_api.features.search.schemas import (
    RecipeGenerateRequest,
    SearchRequest,
    SearchResponse,
)
from recipe_api.features.search.service import SearchService
from recipe_api.shared.deps import CurrentUserDep, SessionDep
from recipe_api.shared.services.embeddings import EmbeddingService, get_embedding_service
from recipe_api.shared.services.llm import LLMService, get_llm_service

router = APIRouter(prefix="/search", tags=["search"])


def get_search_service(
    embedding_service: Annotated[EmbeddingService, Depends(get_embedding_service)],
    llm_service: Annotated[LLMService, Depends(get_llm_service)],
) -> SearchService:
    return SearchService(embedding_service, llm_service)


@router.post("/", response_model=SearchResponse)
def search_recipes(
    search_request: SearchRequest,
    session: SessionDep,
    service: Annotated[SearchService, Depends(get_search_service)],
    current_user: CurrentUserDep | None = None,
) -> SearchResponse:

    results = service.hybrid_search(
        session=session,
        query=search_request.query,
        limit=search_request.limit,
        user_id=current_user,
        boost_popular=True,
    )

    return SearchResponse(
        results=results,
        total=len(results),
        query=search_request.query,
    )


@router.post("/generate", response_model=list[RecipeRead])
def generate_recipe(
    generate_request: RecipeGenerateRequest,
    current_user: CurrentUserDep,
    session: SessionDep,
    service: Annotated[SearchService, Depends(get_search_service)],
) -> list[RecipeRead]:

    recipes = service.generate_recipe(
        session=session,
        prompt=generate_request.prompt,
        user_id=current_user,
        amount=generate_request.amount,
        ingredients=generate_request.ingredients,
        dietary_restrictions=generate_request.dietary_restrictions,
    )

    return recipes
