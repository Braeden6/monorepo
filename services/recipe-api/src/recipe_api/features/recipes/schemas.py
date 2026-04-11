import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from recipe_api.shared.models.recipe import FoodType, RecipeStatus
from recipe_api.shared.schemas.common import IngredientItem


class RecipeBase(BaseModel):
    name: str
    description: str
    ingredients: list[IngredientItem]
    instructions: str
    food_type: FoodType | None = None


class RecipeCreate(RecipeBase):
    status: RecipeStatus = RecipeStatus.DRAFT

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Name cannot be empty")
        return stripped

    @field_validator("ingredients")
    @classmethod
    def ingredients_must_not_be_empty(cls, v: list[IngredientItem]) -> list[IngredientItem]:
        if not v:
            raise ValueError("Ingredients list cannot be empty")
        return v


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
    similarity_score: float | None = None

    model_config = {"from_attributes": True}


# =============================================================================
# Query & Search Schemas
# =============================================================================


class SortField(str, Enum):
    """Available fields for sorting recipes."""

    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    LIKE_COUNT = "like_count"
    FAVORITE_COUNT = "favorite_count"
    RELEVANCE = "relevance"  # Only valid when query is provided


class SortOrder(str, Enum):
    """Sort direction."""

    ASC = "asc"
    DESC = "desc"


class PaginationMeta(BaseModel):
    """Pagination metadata for cursor-based pagination."""

    total: int = Field(description="Total count of matching records")
    limit: int = Field(description="Number of items requested per page")
    has_next: bool = Field(description="Whether there are more items after this page")
    has_prev: bool = Field(description="Whether there are items before this page")
    next_cursor: str | None = Field(default=None, description="Cursor for the next page")
    prev_cursor: str | None = Field(default=None, description="Cursor for the previous page")


class RecipeQueryRequest(BaseModel):
    """Unified query request for searching and filtering recipes."""

    query: str | None = Field(
        default=None,
        description="Text query for semantic search (RAG).",
        min_length=1,
        max_length=500,
    )

    # Filtering
    food_types: list[FoodType] | None = Field(
        default=None,
        description="Filter by one or more food types",
    )
    include_drafts: bool = Field(
        default=True,
        description="Include your own draft recipes (only applies when authenticated)",
    )
    only_mine: bool = Field(
        default=False,
        description="Only return recipes created by you",
    )
    only_favorites: bool = Field(
        default=False,
        description="Only return recipes you have favorited",
    )

    # Sorting
    sort_by: SortField = Field(
        default=SortField.CREATED_AT,
        description="Field to sort by.",
    )
    sort_order: SortOrder = Field(
        default=SortOrder.DESC,
        description="Sort direction",
    )

    # Pagination
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of results to return",
    )
    cursor: str | None = Field(
        default=None,
        description="Pagination cursor from previous response",
    )

    # Search options
    boost_popular: bool = Field(
        default=True,
        description="Boost popular recipes in search results",
    )

    @field_validator("sort_by")
    @classmethod
    def validate_sort_field(cls, v: SortField, info: Any) -> SortField:
        _ = info
        return v


class RecipeQueryResponse(BaseModel):
    """Response for recipe queries with pagination metadata."""

    results: list[RecipeRead]
    pagination: PaginationMeta
    query: str | None = Field(default=None, description="The search query if provided")
    filters_applied: dict[str, Any] = Field(
        default_factory=dict, description="Summary of filters that were applied"
    )
