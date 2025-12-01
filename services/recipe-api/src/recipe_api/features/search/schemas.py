from pydantic import BaseModel, Field

from recipe_api.features.recipes.schemas import RecipeRead
from recipe_api.shared.models.recipe import FoodType


class RecipeSearchResult(RecipeRead):
    similarity_score: float
    food_type: FoodType | None = None


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class SearchResponse(BaseModel):
    results: list[RecipeSearchResult]
    total: int
    query: str


class RecipeGenerateRequest(BaseModel):
    prompt: str
    ingredients: list[str] | None = None
    dietary_restrictions: list[str] | None = None
    amount: int = Field(default=1, ge=1, le=5)
