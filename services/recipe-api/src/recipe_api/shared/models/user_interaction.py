import uuid
from datetime import datetime

from sqlmodel import Field, Index, SQLModel


class UserRecipeInteraction(SQLModel, table=True):
    __tablename__ = "user_recipe_interactions"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)
    recipe_id: uuid.UUID = Field(foreign_key="recipes.id", index=True)
    is_favorite: bool = Field(default=False)
    is_liked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    __table_args__ = (Index("idx_user_recipe_unique", "user_id", "recipe_id", unique=True),)
