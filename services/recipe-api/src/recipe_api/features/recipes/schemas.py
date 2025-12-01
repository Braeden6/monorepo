import uuid
from datetime import datetime

from pydantic import BaseModel

from recipe_api.shared.models.recipe import FoodType, RecipeStatus
from recipe_api.shared.schemas.common import IngredientItem


class RecipeBase(BaseModel):
    name: str
    description: str
    ingredients: list[IngredientItem]
    instructions: str
    food_type: FoodType | None = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    ingredients: list[IngredientItem] | None = None
    instructions: str | None = None
    food_type: FoodType | None = None
    status: RecipeStatus | None = None


class RecipeRead(RecipeBase):
    id: uuid.UUID
    created_by: str
    created_at: datetime
    updated_at: datetime
    like_count: int
    favorite_count: int
    status: RecipeStatus
    is_generated: bool
    is_liked: bool = False
    is_favorited: bool = False

    model_config = {"from_attributes": True}
