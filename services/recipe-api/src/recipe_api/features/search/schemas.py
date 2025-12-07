from pydantic import BaseModel

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
