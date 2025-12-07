from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from recipe_api.features.generate.schemas import GenerateRecipeInput
    from recipe_api.shared.config import settings
    from recipe_api.workflows.activities import (
        create_recipe_placeholder,
        finalize_recipe,
        fix_recipe_issues,
        generate_recipe_content,
        mark_recipe_failed,
        review_recipe_quality,
    )


LLM_RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=settings.llm_retry_initial_interval_seconds),
    backoff_coefficient=settings.llm_retry_backoff_coefficient,
    maximum_attempts=settings.llm_retry_max_attempts,
    maximum_interval=timedelta(seconds=settings.llm_retry_max_interval_seconds),
)

DB_RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(milliseconds=500),
    backoff_coefficient=1.5,
    maximum_attempts=3,
    maximum_interval=timedelta(seconds=5),
)


@workflow.defn
class RecipeGenerationWorkflow:
    def __init__(self) -> None:
        self._recipe_id: str | None = None
        self._current_step = "queued"
        self._error: str | None = None

    @workflow.query
    def get_progress(self) -> dict:
        return {
            "recipe_id": self._recipe_id,
            "current_step": self._current_step,
            "error": self._error,
        }

    @workflow.run
    async def run(self, input_data: dict) -> dict:
        workflow_input = GenerateRecipeInput(**input_data)
        workflow.logger.info(
            f"Starting recipe generation workflow {workflow_input.workflow_id}"
        )

        try:
            # Step 1: Create placeholder recipe
            self._current_step = "creating"
            self._recipe_id = await workflow.execute_activity(
                create_recipe_placeholder,
                input_data,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=DB_RETRY_POLICY,
            )

            workflow.logger.info(f"Created recipe placeholder: {self._recipe_id}")

            # Step 2: Generate recipe content
            self._current_step = "generating"
            recipe_data = await workflow.execute_activity(
                generate_recipe_content,
                args=[self._recipe_id, workflow_input.workflow_id, input_data],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=LLM_RETRY_POLICY,
            )

            workflow.logger.info(f"Generated recipe: {recipe_data.get('name', 'Unknown')}")

            # Step 3: Review recipe quality
            self._current_step = "reviewing"
            review_data = await workflow.execute_activity(
                review_recipe_quality,
                args=[self._recipe_id, workflow_input.workflow_id, recipe_data],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=LLM_RETRY_POLICY,
            )

            workflow.logger.info(
                f"Review complete. Needs fixes: {review_data.get('needs_fixes', False)}"
            )

            # Step 4: Fix issues if needed
            self._current_step = "fixing"
            final_recipe_data = await workflow.execute_activity(
                fix_recipe_issues,
                args=[
                    self._recipe_id,
                    workflow_input.workflow_id,
                    recipe_data,
                    review_data,
                ],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=LLM_RETRY_POLICY,
            )

            # Step 5: Finalize recipe
            self._current_step = "saving"
            await workflow.execute_activity(
                finalize_recipe,
                args=[self._recipe_id, workflow_input.workflow_id, final_recipe_data],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=DB_RETRY_POLICY,
            )

            self._current_step = "completed"

            workflow.logger.info(
                f"Workflow {workflow_input.workflow_id} completed. "
                f"Recipe: {self._recipe_id}"
            )

            return {
                "workflow_id": workflow_input.workflow_id,
                "recipe_id": self._recipe_id,
                "status": "completed",
            }

        except Exception as e:
            self._error = str(e)
            failed_step = self._current_step
            self._current_step = "failed"

            workflow.logger.error(f"Workflow failed at step '{failed_step}': {e}")
            if self._recipe_id:
                await workflow.execute_activity(
                    mark_recipe_failed,
                    args=[self._recipe_id, f"Failed at {failed_step}: {e!s}"],
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=DB_RETRY_POLICY,
                )

            return {
                "workflow_id": workflow_input.workflow_id,
                "recipe_id": self._recipe_id,
                "status": "failed",
                "failed_at_step": failed_step,
                "error": str(e),
            }
