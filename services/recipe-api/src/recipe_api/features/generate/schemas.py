from enum import Enum

from pydantic import BaseModel, Field

from recipe_api.features.recipes.schemas import RecipeRead
from recipe_api.shared.models.recipe import FoodType, GenerationStatus


class GenerateStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    REVIEWING = "reviewing"
    FIXING = "fixing"
    COMPLETED = "completed"
    FAILED = "failed"

class GenerateRecipeInput(BaseModel):
    workflow_id: str
    user_id: str
    prompt: str
    amount: int = 1
    ingredients: list[str] | None = None
    dietary_restrictions: list[str] | None = None


class WorkflowProgress(BaseModel):
    workflow_id: str
    status: GenerationStatus
    current_step: str
    progress: int  # Current step number
    total_steps: int  # Total steps in workflow
    recipe_ids: list[str] | None = None
    error: str | None = None


class IngredientIssue(BaseModel):
    ingredient_name: str
    issue: str = Field(description="Description of the issue, e.g., 'missing unit', 'unrealistic amount'")
    suggestion: str = Field(description="Suggested fix for this ingredient")


class RecipeReview(BaseModel):
    overall_quality: int = Field(description="Overall quality score from 1-10", ge=1, le=10)
    food_type_valid: bool = Field(description="Whether the food type is appropriate for the dish")
    food_type_suggestion: FoodType | None = Field(default=None, description="Suggested food type if current is invalid")
    ingredient_issues: list[IngredientIssue] = Field(default_factory=list, description="List of issues with ingredients")
    realism_issues: list[str] = Field(default_factory=list, description="Issues with recipe realism (e.g., impossible combinations, missing key steps)")
    instruction_issues: list[str] = Field(default_factory=list, description="Issues with instructions (e.g., unclear steps, missing times)")
    needs_fixes: bool = Field(description="Whether this recipe needs to be fixed")
    summary: str = Field(description="Brief summary of review findings")


class RecipeReviewList(BaseModel):
    reviews: list[RecipeReview]



class GenerateRequest(BaseModel):
    prompt: str = Field(
        description="Description of what kind of recipe to generate",
        min_length=3,
        max_length=500,
        examples=["healthy chicken dinner", "quick breakfast with eggs"],
    )
    amount: int = Field(
        default=1,
        description="Number of recipes to generate",
        ge=1,
        le=5,
    )
    ingredients: list[str] | None = Field(
        default=None,
        description="Ingredients to include in the recipe",
        examples=[["chicken", "broccoli", "garlic"]],
    )
    dietary_restrictions: list[str] | None = Field(
        default=None,
        description="Dietary restrictions to follow",
        examples=[["gluten-free", "dairy-free"]],
    )


class GenerateResponse(BaseModel):
    workflow_id: str = Field(description="Unique ID to track this generation request")
    status: GenerateStatus = Field(description="Current status of the generation")


class GenerateStatusResponse(BaseModel):
    workflow_id: str
    status: GenerateStatus
    current_step: str = Field(
        description="Current step: queued, generating, reviewing, fixing, saving, completed, failed"
    )
    recipes: list[RecipeRead] | None = Field(
        default=None,
        description="Generated recipes (only present when completed)",
    )
    error: str | None = Field(
        default=None,
        description="Error message (only present when failed)",
    )

class IngredientOutput(BaseModel):
    name: str = Field(description="Name of the ingredient")
    amount: str = Field(description="Quantity amount, e.g., '2', '1/2', '3-4'")
    unit: str = Field(
        description="Unit of measurement, e.g., 'cups', 'tablespoons', 'pieces', 'grams'"
    )


class GeneratedRecipe(BaseModel):
    name: str = Field(description="Name of the recipe", max_length=255)
    description: str = Field(
        description="Brief, appetizing description of the dish (2-3 sentences)"
    )
    ingredients: list[IngredientOutput] = Field(
        description="List of ingredients with amounts and units"
    )
    instructions: list[str] = Field(
        description="Step-by-step cooking instructions as a list of steps"
    )
    food_type: FoodType = Field(
        description="Category of the dish: BREAKFAST, LUNCH, DINNER, DESSERT, SNACK, or DRINK"
    )


class GeneratedRecipeList(BaseModel):
    recipes: list[GeneratedRecipe]



class FixedRecipe(BaseModel):
    name: str = Field(max_length=255)
    description: str
    ingredients: list[IngredientOutput]
    instructions: list[str]
    food_type: FoodType
    changes_made: list[str] = Field(
        description="List of changes made to fix the recipe"
    )

