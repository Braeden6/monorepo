import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, SQLModel


class LogGenerationStep(str, Enum):
    GENERATE = "GENERATE"
    REVIEW = "REVIEW"
    FIX = "FIX"


class GenerationLog(SQLModel, table=True):
    __tablename__ = "generation_logs"  # type: ignore

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    recipe_id: uuid.UUID = Field(foreign_key="recipes.id", index=True)
    workflow_id: str = Field(index=True)
    step: LogGenerationStep
    system_prompt: str
    user_prompt: str
    raw_response: str
    parsed_response: dict | None = Field(default=None, sa_column=Column(JSON))
    success: bool = Field(default=True)
    error: str | None = Field(default=None)

    model: str
    tokens_used: int | None = Field(default=None)
    duration_ms: int | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
