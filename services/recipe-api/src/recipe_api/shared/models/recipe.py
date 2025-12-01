import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Index
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, SQLModel


class FoodType(str, Enum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    DESSERT = "DESSERT"
    SNACK = "SNACK"
    DRINK = "DRINK"

class RecipeStatus(str, Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"

class Recipe(SQLModel, table=True):
    __tablename__ = "recipes"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, max_length=255)
    description: str
    ingredients: list[dict[str, Any]] = Field(sa_column=Column(JSON))
    instructions: str
    food_type: FoodType | None = Field(default=None)
    status: RecipeStatus = Field(default=RecipeStatus.DRAFT, index=True)
    is_generated: bool = Field(default=False)
    created_by: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    description_embedding: Any = Field(
        default=None,
        sa_column=Column(Vector(384)),
    )
    ingredient_embedding: Any = Field(
        default=None,
        sa_column=Column(Vector(384)),
    )

    like_count: int = Field(default=0)
    favorite_count: int = Field(default=0)

    __table_args__ = (
        Index(
            "idx_description_embedding",
            "description_embedding",
            postgresql_using="ivfflat",
            postgresql_with={"lists": 100},
            postgresql_ops={"description_embedding": "vector_cosine_ops"},
        ),
        Index(
            "idx_ingredient_embedding",
            "ingredient_embedding",
            postgresql_using="ivfflat",
            postgresql_with={"lists": 100},
            postgresql_ops={"ingredient_embedding": "vector_cosine_ops"},
        ),
    )
