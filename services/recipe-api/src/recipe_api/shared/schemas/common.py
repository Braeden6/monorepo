from pydantic import BaseModel


class IngredientItem(BaseModel):
    name: str
    amount: str | None = None
    unit: str | None = None
