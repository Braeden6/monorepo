import uuid

from sqlmodel import Session, select
from temporalio.client import Client

from recipe_api.features.generate.schemas import (
    GenerateRecipeInput,
    GenerateRequest,
    GenerateStatus,
)
from recipe_api.features.recipes.schemas import RecipeRead
from recipe_api.shared.config import settings
from recipe_api.shared.models.recipe import GenerationStatus, Recipe
from recipe_api.workflows.recipe_generation import RecipeGenerationWorkflow


class GenerateService:
    def __init__(self, temporal_client: Client, session: Session):
        self.client = temporal_client
        self.session = session

    async def start_generation(
        self,
        request: GenerateRequest,
        user_id: str,
    ) -> tuple[str, list[str]]:
        base_workflow_id = f"recipe-gen-{uuid.uuid4().hex[:12]}"
        workflow_ids: list[str] = []

        for i in range(request.amount):
            workflow_id = f"{base_workflow_id}-{i}" if request.amount > 1 else base_workflow_id

            input_data = GenerateRecipeInput(
                workflow_id=workflow_id,
                user_id=user_id,
                prompt=request.prompt,
                amount=1,
                ingredients=request.ingredients,
                dietary_restrictions=request.dietary_restrictions,
            )

            await self.client.start_workflow(
                RecipeGenerationWorkflow.run,
                input_data.model_dump(),
                id=workflow_id,
                task_queue=settings.temporal_task_queue,
            )

            workflow_ids.append(workflow_id)

        return base_workflow_id, workflow_ids

    async def get_status(self, workflow_id: str) -> dict:
        recipes = self.session.exec(
            select(Recipe).where(
                Recipe.workflow_id.startswith(workflow_id)  # type: ignore[union-attr]
            )
        ).all()

        if not recipes:
            return {
                "workflow_id": workflow_id,
                "status": GenerateStatus.PENDING,
                "current_step": "queued",
                "recipes": None,
                "error": None,
            }

        statuses = [r.generation_status for r in recipes]
        steps = [r.generation_step for r in recipes if r.generation_step]

        if any(s == GenerationStatus.FAILED for s in statuses):
            failed_recipe = next(r for r in recipes if r.generation_status == GenerationStatus.FAILED)
            return {
                "workflow_id": workflow_id,
                "status": GenerateStatus.FAILED,
                "current_step": failed_recipe.generation_step.value if failed_recipe.generation_step else "unknown",
                "recipes": None,
                "error": failed_recipe.generation_error,
            }

        if all(s == GenerationStatus.COMPLETED for s in statuses):
            return {
                "workflow_id": workflow_id,
                "status": GenerateStatus.COMPLETED,
                "current_step": "completed",
                "recipes": [RecipeRead.model_validate(r) for r in recipes],
                "error": None,
            }

        current_step = "generating"
        if steps:
            current_step = steps[-1].value.lower()

        return {
            "workflow_id": workflow_id,
            "status": GenerateStatus.GENERATING,
            "current_step": current_step,
            "recipes": None,
            "error": None,
        }

    def _map_step_to_status(self, step: str) -> GenerateStatus:
        if step in ("queued", "creating"):
            return GenerateStatus.PENDING
        elif step in ("generating", "reviewing", "fixing", "saving"):
            return GenerateStatus.GENERATING
        elif step == "completed":
            return GenerateStatus.COMPLETED
        elif step == "failed":
            return GenerateStatus.FAILED
        return GenerateStatus.PENDING
