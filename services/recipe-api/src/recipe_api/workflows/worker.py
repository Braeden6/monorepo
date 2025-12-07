import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from recipe_api.shared.config import settings
from recipe_api.workflows.activities import (
    create_recipe_placeholder,
    finalize_recipe,
    fix_recipe_issues,
    generate_recipe_content,
    mark_recipe_failed,
    review_recipe_quality,
)
from recipe_api.workflows.recipe_generation import RecipeGenerationWorkflow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info(f"Connecting to Temporal at {settings.temporal_host}")

    client = await Client.connect(
        settings.temporal_host,
        namespace=settings.temporal_namespace,
    )

    logger.info(f"Starting worker on task queue: {settings.temporal_task_queue}")

    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=[RecipeGenerationWorkflow],
        activities=[
            create_recipe_placeholder,
            generate_recipe_content,
            review_recipe_quality,
            fix_recipe_issues,
            finalize_recipe,
            mark_recipe_failed,
        ],
        max_concurrent_activities=settings.worker_max_concurrent_activities,
        max_concurrent_workflow_tasks=settings.worker_max_concurrent_workflow_tasks,
    )

    logger.info("Worker started. Waiting for tasks...")

    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped")
